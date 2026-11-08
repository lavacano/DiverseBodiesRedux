#include "FaceGenFix.h"
#include "PatchesMemUtils.h"

#define WIN32_LEAN_AND_MEAN
#include <Windows.h>

#include <cstring>
#include <cstdint>

namespace patches {
	namespace {
		// Fallout 4 Next-Gen 1.11.240.0 FaceGen Engine RVAs
		constexpr std::uintptr_t kFaceGen_ProceduralFallback_RVA = 0x6E2625;
		constexpr std::uintptr_t kFaceGen_NullGuard_RVA          = 0x6E0880;
		constexpr std::uintptr_t kFaceGen_Resume_RVA             = 0x6E088F;
		constexpr std::uintptr_t kFaceGen_Bypass_RVA             = 0x6E0B53;

		// Patch A: Expected 16 bytes at 0x6E2625
		// 48 8B CE             mov rcx, rsi
		// E8 73 CD FF FF       call 0x1406df3a0
		// 84 C0                test al, al
		// 74 61                je 0x1406e2692
		// 85 ED                test ebp, ebp
		// 75 5D                jne 0x1406e2692
		constexpr std::uint8_t kExpectedPatchA[16] = {
			0x48, 0x8b, 0xce, 0xe8, 0x73, 0xcd, 0xff, 0xff,
			0x84, 0xc0, 0x74, 0x61, 0x85, 0xed, 0x75, 0x5d
		};

		// Patch A replacement: jmp +0x6b (eb 6b) into 0x1406e2692 (procedural face generator), plus 14 NOPs
		constexpr std::uint8_t kReplacementPatchA[16] = {
			0xeb, 0x6b, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90,
			0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90
		};

		// Patch B: Expected 15 bytes at 0x6E0880
		// 48 8B 55 E7          mov rdx, [rbp-0x19]
		// 45 8B DC             mov r11d, r12d
		// 44 0F B7 92 34 01 00 00 movzx r10d, word ptr [rdx+0x134]
		constexpr std::uint8_t kExpectedPatchB[15] = {
			0x48, 0x8b, 0x55, 0xe7, 0x45, 0x8b, 0xdc,
			0x44, 0x0f, 0xb7, 0x92, 0x34, 0x01, 0x00, 0x00
		};

		bool g_patchesInstalled = false;
	}

	bool InstallFaceGenFallbackPatches()
	{
		if (g_patchesInstalled) {
			return true;
		}

		const auto base = reinterpret_cast<std::uintptr_t>(::GetModuleHandleA(nullptr));
		if (!base) {
			logger::error("[FaceGenFix] Failed to get Fallout4.exe base address.");
			return false;
		}

		// Verify DOS header
		const auto* dos = reinterpret_cast<const IMAGE_DOS_HEADER*>(base);
		if (!IsReadableFast(dos, sizeof(IMAGE_DOS_HEADER)) || dos->e_magic != IMAGE_DOS_SIGNATURE) {
			logger::error("[FaceGenFix] Invalid DOS header at Fallout4.exe base (0x{:X}).", base);
			return false;
		}

		// -------------------------------------------------------------
		// 1. Install Patch A: Procedural Face Fallback at RVA 0x6E2625
		// -------------------------------------------------------------
		const auto patchA_Addr = base + kFaceGen_ProceduralFallback_RVA;
		if (!IsReadableFast(reinterpret_cast<const void*>(patchA_Addr), sizeof(kExpectedPatchA))) {
			logger::error("[FaceGenFix] Address Fallout4.exe+0x{:X} is not readable.", kFaceGen_ProceduralFallback_RVA);
			return false;
		}

		if (std::memcmp(reinterpret_cast<const void*>(patchA_Addr), kExpectedPatchA, sizeof(kExpectedPatchA)) == 0) {
			DWORD oldProt = 0;
			if (::VirtualProtect(reinterpret_cast<void*>(patchA_Addr), sizeof(kReplacementPatchA), F4SE::WinAPI::PAGE_EXECUTE_READWRITE, &oldProt)) {
				std::memcpy(reinterpret_cast<void*>(patchA_Addr), kReplacementPatchA, sizeof(kReplacementPatchA));
				::VirtualProtect(reinterpret_cast<void*>(patchA_Addr), sizeof(kReplacementPatchA), oldProt, &oldProt);
				::FlushInstructionCache(::GetCurrentProcess(), reinterpret_cast<void*>(patchA_Addr), sizeof(kReplacementPatchA));
				logger::info("[FaceGenFix] Successfully installed Patch A (Procedural Face Fallback) at Fallout4.exe+0x{:X}.",
					kFaceGen_ProceduralFallback_RVA);
			} else {
				logger::error("[FaceGenFix] VirtualProtect failed on Patch A at Fallout4.exe+0x{:X}.", kFaceGen_ProceduralFallback_RVA);
				return false;
			}
		} else if (std::memcmp(reinterpret_cast<const void*>(patchA_Addr), kReplacementPatchA, sizeof(kReplacementPatchA)) == 0) {
			logger::info("[FaceGenFix] Patch A already installed at Fallout4.exe+0x{:X}.", kFaceGen_ProceduralFallback_RVA);
		} else {
			logger::warn("[FaceGenFix] Bytes at Fallout4.exe+0x{:X} mismatch expected prologue; skipping Patch A.",
				kFaceGen_ProceduralFallback_RVA);
		}

		// -------------------------------------------------------------
		// 2. Install Patch B: Null Pointer Guard Trampoline at RVA 0x6E0880
		// -------------------------------------------------------------
		const auto patchB_Addr = base + kFaceGen_NullGuard_RVA;
		if (!IsReadableFast(reinterpret_cast<const void*>(patchB_Addr), sizeof(kExpectedPatchB))) {
			logger::error("[FaceGenFix] Address Fallout4.exe+0x{:X} is not readable.", kFaceGen_NullGuard_RVA);
			return false;
		}

		if (std::memcmp(reinterpret_cast<const void*>(patchB_Addr), kExpectedPatchB, sizeof(kExpectedPatchB)) == 0) {
			// Allocate executable memory for the 48-byte stub
			void* stubMem = ::VirtualAlloc(nullptr, 4096, MEM_COMMIT | MEM_RESERVE, F4SE::WinAPI::PAGE_EXECUTE_READWRITE);
			if (!stubMem) {
				logger::error("[FaceGenFix] VirtualAlloc failed for Patch B stub.");
				return false;
			}

			const std::uint64_t resumeAddr = base + kFaceGen_Resume_RVA;
			const std::uint64_t bypassAddr = base + kFaceGen_Bypass_RVA;

			std::uint8_t* p = reinterpret_cast<std::uint8_t*>(stubMem);

			// mov rdx, [rbp-0x19]
			p[0] = 0x48; p[1] = 0x8B; p[2] = 0x55; p[3] = 0xE7;
			// test rdx, rdx
			p[4] = 0x48; p[5] = 0x85; p[6] = 0xD2;
			// jz +0x19 (.bypass)
			p[7] = 0x74; p[8] = 0x19;
			// mov r11d, r12d
			p[9] = 0x45; p[10] = 0x8B; p[11] = 0xDC;
			// movzx r10d, word ptr [rdx+0x134]
			p[12] = 0x44; p[13] = 0x0F; p[14] = 0xB7; p[15] = 0x92;
			p[16] = 0x34; p[17] = 0x01; p[18] = 0x00; p[19] = 0x00;
			// jmp qword ptr [rip+0] -> resumeAddr
			p[20] = 0xFF; p[21] = 0x25; p[22] = 0x00; p[23] = 0x00; p[24] = 0x00; p[25] = 0x00;
			std::memcpy(p + 26, &resumeAddr, sizeof(resumeAddr));

			// .bypass:
			// jmp qword ptr [rip+0] -> bypassAddr
			p[34] = 0xFF; p[35] = 0x25; p[36] = 0x00; p[37] = 0x00; p[38] = 0x00; p[39] = 0x00;
			std::memcpy(p + 40, &bypassAddr, sizeof(bypassAddr));

			::FlushInstructionCache(::GetCurrentProcess(), stubMem, 48);

			// Write 15-byte absolute jump at patchB_Addr:
			// FF 25 00 00 00 00 <8-byte stubMem> 90
			std::uint8_t patchB_Bytes[15];
			patchB_Bytes[0] = 0xFF;
			patchB_Bytes[1] = 0x25;
			patchB_Bytes[2] = 0x00;
			patchB_Bytes[3] = 0x00;
			patchB_Bytes[4] = 0x00;
			patchB_Bytes[5] = 0x00;
			const std::uint64_t stubAddrVal = reinterpret_cast<std::uint64_t>(stubMem);
			std::memcpy(patchB_Bytes + 6, &stubAddrVal, sizeof(stubAddrVal));
			patchB_Bytes[14] = 0x90; // NOP to pad to 15 bytes

			DWORD oldProt = 0;
			if (::VirtualProtect(reinterpret_cast<void*>(patchB_Addr), sizeof(patchB_Bytes), F4SE::WinAPI::PAGE_EXECUTE_READWRITE, &oldProt)) {
				std::memcpy(reinterpret_cast<void*>(patchB_Addr), patchB_Bytes, sizeof(patchB_Bytes));
				::VirtualProtect(reinterpret_cast<void*>(patchB_Addr), sizeof(patchB_Bytes), oldProt, &oldProt);
				::FlushInstructionCache(::GetCurrentProcess(), reinterpret_cast<void*>(patchB_Addr), sizeof(patchB_Bytes));
				logger::info("[FaceGenFix] Successfully installed Patch B (Null Guard Stub at 0x{:X}) at Fallout4.exe+0x{:X}.",
					stubAddrVal, kFaceGen_NullGuard_RVA);
			} else {
				logger::error("[FaceGenFix] VirtualProtect failed on Patch B at Fallout4.exe+0x{:X}.", kFaceGen_NullGuard_RVA);
				return false;
			}
		} else {
			logger::warn("[FaceGenFix] Bytes at Fallout4.exe+0x{:X} mismatch expected prologue; skipping Patch B.",
				kFaceGen_NullGuard_RVA);
		}

		g_patchesInstalled = true;
		return true;
	}
}
