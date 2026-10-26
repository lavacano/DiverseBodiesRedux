#include <windows.h>
#include "PatchesMemUtils.h"
#define PAGE_EXECUTE_READWRITE_ 0x40

namespace patches
{
	bool IsReadableFast(const void* p, std::size_t minSize)
	{
		if (!p) return false;

		MEMORY_BASIC_INFORMATION mbi{};
		if (!VirtualQuery(p, &mbi, sizeof(mbi)))
			return false;

		if ((mbi.State & MEM_COMMIT) == 0)
			return false;

		if (mbi.Protect & (PAGE_GUARD | PAGE_NOACCESS))
			return false;

		const DWORD prot = mbi.Protect & 0xFF;
		switch (prot) {
		case PAGE_READONLY:
		case PAGE_READWRITE:
		case PAGE_WRITECOPY:
		case PAGE_EXECUTE_READ:
		case PAGE_EXECUTE_READWRITE_:
		case PAGE_EXECUTE_WRITECOPY:
			break;
		default:
			return false;
		}

		const auto start = reinterpret_cast<std::uintptr_t>(p);
		const auto base = reinterpret_cast<std::uintptr_t>(mbi.BaseAddress);
		const auto off = start - base;
		return (off + minSize) <= mbi.RegionSize;
	}

	bool IsWritableFast(void* p, std::size_t minSize)
	{
		if (!p) return false;

		MEMORY_BASIC_INFORMATION mbi{};
		if (!VirtualQuery(p, &mbi, sizeof(mbi)))
			return false;

		if ((mbi.State & MEM_COMMIT) == 0)
			return false;

		if (mbi.Protect & (PAGE_GUARD | PAGE_NOACCESS))
			return false;

		const DWORD prot = mbi.Protect & 0xFF;
		switch (prot) {
		case PAGE_READWRITE:
		case PAGE_WRITECOPY:
		case PAGE_EXECUTE_READWRITE_:
		case PAGE_EXECUTE_WRITECOPY:
			break;
		default:
			return false;
		}

		const auto start = reinterpret_cast<std::uintptr_t>(p);
		const auto base = reinterpret_cast<std::uintptr_t>(mbi.BaseAddress);
		const auto off = start - base;
		return (off + minSize) <= mbi.RegionSize;
	}

	static const std::uint32_t* s_gameTlsIndexPtr = nullptr;
	static std::atomic<bool> s_tlsPtrResolved{ false };

	const std::uint32_t* GetGameTlsIndexPtr()
	{
		if (s_tlsPtrResolved.load(std::memory_order_acquire)) {
			return s_gameTlsIndexPtr;
		}

		const auto base = reinterpret_cast<std::uintptr_t>(::GetModuleHandleA(nullptr)); // Fallout4.exe base (0x140000000)
		if (!base) return nullptr;

		const auto fn = reinterpret_cast<const std::uint8_t*>(base + kBSClothExtraData_SetWorld_RVA);
		if (fn) {
			// Ищем сигнатуру: 44 8B 05 xx xx xx xx
			for (std::size_t i = 0; i < 0x80; ++i) {
				const auto p = fn + i;
				if (p[0] == 0x44 && p[1] == 0x8B && p[2] == 0x05) {
					const auto disp = *reinterpret_cast<const std::int32_t*>(p + 3);
					const auto next = reinterpret_cast<std::uintptr_t>(p + 7);
					const auto idxAddr = reinterpret_cast<const std::uint32_t*>(next + disp);
					if (IsReadableFast(idxAddr, sizeof(std::uint32_t))) {
						s_gameTlsIndexPtr = idxAddr;
						s_tlsPtrResolved.store(true, std::memory_order_release);
						return s_gameTlsIndexPtr;
					}
					break;
				}
			}
		}

		// Fallback для Fallout 4 1.10.980 (Next-Gen) RVA 0x3E73018
		const auto fallbackAddr = reinterpret_cast<const std::uint32_t*>(base + 0x3E73018);
		if (IsReadableFast(fallbackAddr, sizeof(std::uint32_t))) {
			s_gameTlsIndexPtr = fallbackAddr;
		}

		s_tlsPtrResolved.store(true, std::memory_order_release);
		return s_gameTlsIndexPtr;
	}

	bool ResolveGameTlsIndex(std::uint32_t& outIdx)
	{
		const auto* ptr = GetGameTlsIndexPtr();
		if (!ptr) return false;
		outIdx = *ptr;
		return outIdx != 0;
	}

	bool HasGameTLSGuardSlot()
	{
		const auto tlsArray = reinterpret_cast<const void* const*>(__readgsqword(0x58));
		if (!tlsArray) return false;

		const auto* ptr = GetGameTlsIndexPtr();
		if (!ptr) return false;

		const auto idx = *ptr;
		if (idx == 0) return false;

		const void* slot = nullptr;
#ifdef _MSC_VER
		__try {
			slot = tlsArray[idx];
		} __except (EXCEPTION_EXECUTE_HANDLER) {
			return false;
		}
#else
		slot = tlsArray[idx];
#endif

		return slot != nullptr;
	}
}