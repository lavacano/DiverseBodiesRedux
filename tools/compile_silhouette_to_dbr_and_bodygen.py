#!/usr/bin/env python3
"""
Compile Silhouette (ReidenXerx/fo4-silhouette) body morph pools, faction pools,
and named character presets into Diverse Bodies Redux (Option B — Sole Morph Authority).

In-Engine Resolution Hierarchy (DBR PresetsGenerator.hpp + Conditions.cpp):
  1. Named Characters (Sil_Char_*_conds.json):
     Uses "formIDs" -> CoincidenceLevel::FULL (0x7FFFFFFF). Wins unconditionally.
  2. Faction Members (Sil_Faction_*_conds.json):
     Uses "inFaction" + priority-ordered "notInFaction" ("formIDs": [])
     -> CoincidenceLevel::GENDER | CoincidenceLevel::FACTIONS (5).
  3. General Population / Settlers (Sil_Pool_* + curated DBR presets):
     Uses directory conds.json fallback -> CoincidenceLevel::GENDER (1).

Pass --with-bodygen to also emit LooksMenu BodyGen templates.ini / morphs.ini (Option A).
"""
import os, sys, re, json, struct, zlib, shutil

WITH_BODYGEN = "--with-bodygen" in sys.argv

data_dir = "/home/lavac/.local/share/Steam/steamapps/common/Fallout 4/Data"
plugins_txt = "/home/lavac/.local/share/Steam/steamapps/compatdata/377160/pfx/drive_c/users/steamuser/AppData/Local/Fallout4/plugins.txt"

script_dir = os.path.dirname(os.path.abspath(__file__))
sil_dir = os.path.join(script_dir, "silhouette")
if not os.path.exists(sil_dir):
    sil_dir = "/home/lavac/.gemini/antigravity/brain/f414056b-e88d-4f2a-8025-fc9a9dedef6e/scratch/silhouette"

dbr_mod_root = "/home/lavac/Games/Amethyst/Fallout 4/profiles/Such_Fallout_4/mods/Diverse Bodies Redux"
dbr_mod_base = os.path.join(dbr_mod_root, "DiverseBodiesRedux")
dbr_ini_path = os.path.join(dbr_mod_root, "MCM/Settings/DiverseBodiesRedux.ini")
f4ee_ini_path = "/home/lavac/Games/Amethyst/Fallout 4/profiles/Such_Fallout_4/mods/LooksMenu v1/F4SE/Plugins/f4ee.ini"
dbr_data_base = os.path.join(data_dir, "DiverseBodiesRedux")

templates_ini_path = "/home/lavac/Games/Amethyst/Fallout 4/profiles/Such_Fallout_4/mods/Real Body Randomizer CBBE/Data/F4SE/Plugins/F4EE/BodyGen/Fallout4.esm/templates.ini"
morphs_ini_path = "/home/lavac/Games/Amethyst/Fallout 4/profiles/Such_Fallout_4/mods/CBBE Morphs NO Balloons (Immersion Version)/Data/F4SE/Plugins/F4EE/BodyGen/Fallout4.esm/morphs.ini"

# 1. Strip embedded BodyMorphs from DBR Head presets so Head randomizer only touches heads/faces
stripped_heads = 0
for sub in ["HeadsFemale", "HeadsMale", "HeadsFemaleRaiders", "HeadsFemaleSlaves", "HeadsFemaleFanatics"]:
    p = os.path.join(dbr_mod_base, sub)
    if not os.path.exists(p):
        continue
    for fn in sorted(os.listdir(p)):
        if fn.endswith(".json") and not fn.endswith("conds.json"):
            fp = os.path.join(p, fn)
            with open(fp) as f:
                d = json.load(f)
            if d.get("BodyMorphs") is not None:
                d["BodyMorphs"] = None
                with open(fp, "w") as f:
                    json.dump(d, f, indent=4)
                stripped_heads += 1
print(f"[1/5] Ensured embedded BodyMorphs=null across DBR Head preset folders (updated {stripped_heads} files).")

# 1b. Disable exaggerated/balloon original DBR female presets (>0.55 Breasts / DoubleMelon / SEXY)
fem_mod_dir = os.path.join(dbr_mod_base, "BodymorphsFemale")
fem_disabled_dir = os.path.join(dbr_mod_base, "BodymorphsFemale_Disabled")
mal_mod_dir = os.path.join(dbr_mod_base, "BodymorphsMale")
fem_data_dir = os.path.join(dbr_data_base, "BodymorphsFemale")
mal_data_dir = os.path.join(dbr_data_base, "BodymorphsMale")

os.makedirs(fem_disabled_dir, exist_ok=True)
disabled_moved = 0
if os.path.exists(fem_mod_dir):
    for fn in sorted(os.listdir(fem_mod_dir)):
        if fn.startswith("Sil_") or fn == "conds.json" or fn.endswith("_conds.json"):
            continue
        if "ANTEGO_4_Ivy" in fn:
            continue
        fp = os.path.join(fem_mod_dir, fn)
        should_disable = False
        if fn.startswith("F_!SEXY!_") or fn in ("F_!FAT!_NAE_2.json", "F_!SLIM!_Zallbard_SLIM_SEXY01.json") or fn.endswith(".xml"):
            should_disable = True
        elif fn.endswith(".json"):
            try:
                with open(fp) as f:
                    d = json.load(f)
                bm = d.get("BodyMorphs") or {}
                if bm.get("Breasts", 0) > 0.55 or bm.get("DoubleMelon", 0) > 0 or bm.get("BreastFantasy", 0) > 0:
                    should_disable = True
            except Exception:
                pass
        if should_disable:
            shutil.move(fp, os.path.join(fem_disabled_dir, fn))
            disabled_moved += 1
            cond_fn = os.path.splitext(fn)[0] + "_conds.json"
            cond_fp = os.path.join(fem_mod_dir, cond_fn)
            if os.path.exists(cond_fp):
                shutil.move(cond_fp, os.path.join(fem_disabled_dir, cond_fn))

# 2. Scan active plugins in load order
base_masters = [
    "Fallout4.esm",
    "DLCRobot.esm",
    "DLCworkshop01.esm",
    "DLCCoast.esm",
    "DLCworkshop02.esm",
    "DLCworkshop03.esm",
    "DLCNukaWorld.esm",
]
cc_files = sorted([f for f in os.listdir(data_dir) if f.lower().startswith("cc") and f.lower().endswith((".esl", ".esm", ".esp"))])
active_plugins = list(base_masters) + [c for c in cc_files if c not in base_masters]
if os.path.exists(plugins_txt):
    with open(plugins_txt, errors="ignore") as f:
        for line in f:
            line = line.strip()
            if line.startswith("*"):
                p = line[1:]
                if p not in active_plugins and os.path.exists(os.path.join(data_dir, p)):
                    active_plugins.append(p)

disk_files = {f.lower(): f for f in os.listdir(data_dir)}
active_map = {p.lower(): p for p in active_plugins}

def resolve_fid(fid, masters, current_plugin):
    if fid == 0:
        return None
    idx = (fid >> 24) & 0xFF
    local_id = fid & 0x00FFFFFF
    if idx < len(masters):
        m_name = disk_files.get(masters[idx].lower(), masters[idx])
        return (m_name, local_id)
    else:
        return (current_plugin, local_id)

def parse_subrecords(raw):
    pos = 0
    n = len(raw)
    xxxx_size = None
    while pos + 6 <= n:
        stype = raw[pos:pos+4]
        sz = struct.unpack_from("<H", raw, pos+4)[0]
        pos += 6
        if stype == b"XXXX" and sz == 4:
            xxxx_size = struct.unpack_from("<I", raw, pos)[0]
            pos += 4
            continue
        if xxxx_size is not None:
            sz = xxxx_size
            xxxx_size = None
        sdata = raw[pos:pos+sz]
        pos += sz
        yield stype, sdata

def scan_plugin(plugin_name, target_types={b"FACT", b"NPC_", b"LVLN", b"RACE"}):
    path = os.path.join(data_dir, plugin_name)
    with open(path, "rb") as f:
        buf = f.read()
    if len(buf) < 24 or buf[:4] != b"TES4":
        return None, [], []
    tes4_size, tes4_flags = struct.unpack_from("<II", buf, 4)
    is_esl = bool(tes4_flags & 0x200) or plugin_name.lower().endswith(".esl")
    masters = []
    for stype, sdata in parse_subrecords(buf[24:24+tes4_size]):
        if stype == b"MAST":
            masters.append(sdata.rstrip(b"\x00").decode("utf-8", errors="ignore"))

    records = []
    def walk_range(start, end):
        pos = start
        while pos + 24 <= end:
            rtype = buf[pos:pos+4]
            if rtype == b"GRUP":
                gsize = struct.unpack_from("<I", buf, pos+4)[0]
                glabel = buf[pos+8:pos+12]
                gtype = struct.unpack_from("<I", buf, pos+12)[0]
                if gsize < 24:
                    break
                if gtype == 0 and glabel not in target_types:
                    pos += gsize
                    continue
                walk_range(pos + 24, min(end, pos + gsize))
                pos += gsize
            else:
                rsize, rflags, rfid = struct.unpack_from("<III", buf, pos+4)
                pos_next = pos + 24 + rsize
                if rtype in target_types:
                    raw = buf[pos+24:pos_next]
                    if rflags & 0x00040000:
                        if len(raw) >= 4:
                            try:
                                raw = zlib.decompress(raw[4:])
                            except Exception:
                                raw = b""
                    records.append((rtype, rflags, rfid, raw))
                pos = pos_next

    walk_range(24 + tes4_size, len(buf))
    return is_esl, masters, records

plugin_is_esl = {}
facts = {}
races = {}
npcs = {}
lvlns = {}

for p in active_plugins:
    res = scan_plugin(p)
    if res[0] is None:
        continue
    is_esl, masters, recs = res
    plugin_is_esl[p] = is_esl
    for rtype, rflags, rfid, raw in recs:
        key = resolve_fid(rfid, masters, p)
        if not key:
            continue
        if rtype == b"FACT":
            for st, sd in parse_subrecords(raw):
                if st == b"EDID":
                    facts[key] = sd.rstrip(b"\x00").decode("utf-8", errors="ignore")
        elif rtype == b"RACE":
            for st, sd in parse_subrecords(raw):
                if st == b"EDID":
                    races[key] = sd.rstrip(b"\x00").decode("utf-8", errors="ignore")
        elif rtype == b"NPC_":
            entry = npcs.get(key, {
                "edid": "",
                "acbs_flags": 0,
                "template_flags": 0,
                "rnam": None,
                "snams": [],
                "tplt": None,
                "tptas": [],
            })
            snams = []
            has_snam = False
            for st, sd in parse_subrecords(raw):
                if st == b"EDID":
                    entry["edid"] = sd.rstrip(b"\x00").decode("utf-8", errors="ignore")
                elif st == b"ACBS" and len(sd) >= 20:
                    entry["acbs_flags"] = struct.unpack_from("<I", sd, 0)[0]
                    entry["template_flags"] = struct.unpack_from("<H", sd, 14)[0]
                elif st == b"RNAM" and len(sd) >= 4:
                    entry["rnam"] = resolve_fid(struct.unpack_from("<I", sd, 0)[0], masters, p)
                elif st == b"SNAM" and len(sd) >= 4:
                    has_snam = True
                    f_ref = resolve_fid(struct.unpack_from("<I", sd, 0)[0], masters, p)
                    if f_ref:
                        snams.append(f_ref)
                elif st == b"TPLT" and len(sd) >= 4:
                    entry["tplt"] = resolve_fid(struct.unpack_from("<I", sd, 0)[0], masters, p)
                elif st == b"TPTA" and len(sd) >= 4:
                    entry["tptas"] = [resolve_fid(struct.unpack_from("<I", sd, off)[0], masters, p)
                                      for off in range(0, len(sd) - 3, 4)]
            if has_snam:
                entry["snams"] = snams
            npcs[key] = entry
        elif rtype == b"LVLN":
            entry = lvlns.get(key, {"edid": "", "lvlos": []})
            lvlos = []
            has_lvlo = False
            for st, sd in parse_subrecords(raw):
                if st == b"EDID":
                    entry["edid"] = sd.rstrip(b"\x00").decode("utf-8", errors="ignore")
                elif st == b"LVLO" and len(sd) >= 8:
                    has_lvlo = True
                    ref = resolve_fid(struct.unpack_from("<I", sd, 4)[0], masters, p)
                    if ref:
                        lvlos.append(ref)
            if has_lvlo:
                entry["lvlos"] = lvlos
            lvlns[key] = entry

def format_local_fid(plugin, raw_local_id):
    if plugin_is_esl.get(plugin, False):
        return f"{raw_local_id & 0xFFF:X}"
    return f"{raw_local_id & 0xFFFFFF:X}"

with open(os.path.join(sil_dir, "pool.json")) as f:
    pool_data = json.load(f)
with open(os.path.join(sil_dir, "factions.json")) as f:
    factions_data = json.load(f)
with open(os.path.join(sil_dir, "characters.json")) as f:
    chars_data = json.load(f)

edid_to_fact = {edid.lower(): k for k, edid in facts.items()}
fact_to_sil = {}
for fk, fv in factions_data["factions"].items():
    for f_plug, f_edid in fv["factions"]:
        fk_id = edid_to_fact.get(f_edid.lower())
        if fk_id:
            fact_to_sil[fk_id] = fk

extra_subfactions = {
    "bos": ["BoSGenericNPCFaction", "BoSSquireFaction", "SS2C3_BoSRemnantsFaction", "BunkerHillBoSFaction"],
    "minutemen": ["PotentialMinutemen", "Min02_MinutemenFaction", "RESC_FactionMinutemenFaction"],
    "gunner": ["DN102_FrenziedGunnerFaction", "SS2_C2_AlgernonGunnerFaction", "SS2C2_MQ16_ConcordGunnerFaction", "SS2C2_Vault75_GunnerFaction", "SS2C2_WesGunnerFaction", "SS2C3_LamontGunnerFaction"],
    "triggermen": ["TriggermanFriendFaction", "MS16TriggermanFaction"],
    "raiders": ["DLC01RaiderFaction", "DLC03TrapperFaction", "DLC03TrapperFactionCoast", "DLC03TrapperFactionWoods", "TheForgedFaction", "CZRaiderFaction", "DLC04CommonwealthRaiderFaction", "SS2_MQ04RaiderFaction", "SS2C3_Faction_CainRaiders", "SS2C3_BostonBattersFaction"],
    "institute": ["BunkerHillInstituteFaction", "InstituteMaintenanceFaction", "InstituteRefugeeFaction"],
    "railroad": ["RailroadGenericNPCFaction", "RailroadOvertAgentFaction"],
    "atom": ["DLC03ChildrenofAtomGenericNPCFaction", "DN166AtomFaction", "SS2_AtomAcolyteFaction"],
}
for fk, edids in extra_subfactions.items():
    for ed in edids:
        fk_id = edid_to_fact.get(ed.lower())
        if fk_id:
            fact_to_sil[fk_id] = fk

USE_TRAITS, USE_FACTIONS = 0x0001, 0x0004
SLOT_TRAITS, SLOT_FACTIONS = 0, 2

def template_for(n, flag, slot):
    if not (n["template_flags"] & flag):
        return None
    if len(n["tptas"]) > slot and n["tptas"][slot]:
        return n["tptas"][slot]
    return n["tplt"]

def _walk(npc_key, flag, slot, own_fn, visited):
    if npc_key in visited:
        return set()
    visited.add(npc_key)
    if npc_key in npcs:
        n = npcs[npc_key]
        t = template_for(n, flag, slot)
        if t:
            return _walk(t, flag, slot, own_fn, visited)
        return own_fn(n)
    if npc_key in lvlns:
        res = set()
        for c in lvlns[npc_key]["lvlos"]:
            res |= _walk(c, flag, slot, own_fn, visited)
        return res
    return set()

def get_npc_races(k):
    return _walk(k, USE_TRAITS, SLOT_TRAITS,
                 lambda n: {races[n["rnam"]]} if n["rnam"] in races else set(), set())

def get_npc_factions(k):
    return _walk(k, USE_FACTIONS, SLOT_FACTIONS,
                 lambda n: {fact_to_sil[f] for f in n["snams"] if f in fact_to_sil}, set())

faction_priority = [
    "disciples",
    "operators",
    "pack",
    "triggermen",
    "atom",
    "railroad",
    "institute",
    "bos",
    "gunner",
    "minutemen",
    "raiders",
]

faction_npc_targets = {fk: [] for fk in factions_data["factions"]}
for nk in sorted(npcs.keys(), key=lambda x: (active_plugins.index(x[0]) if x[0] in active_plugins else 999, x[1])):
    if nk[0] not in active_map.values():
        continue
    if nk[0] == "Fallout4.esm" and (nk[1] & 0xFFFFFF) in (0x7, 0xA7D34, 0xA7D35):
        continue
    rset = get_npc_races(nk)
    if "HumanRace" not in rset or "HumanChildRace" in rset:
        continue
    fset = get_npc_factions(nk)
    if not fset:
        continue
    winning_fk = None
    for p_fk in faction_priority:
        if p_fk in fset:
            winning_fk = p_fk
            break
    if winning_fk:
        faction_npc_targets[winning_fk].append((nk[0], nk[1], npcs[nk]["edid"]))

print("[2/5] Resolved adult HumanRace NPC_ records per faction (with TPLT + TPTA):")
for fk in factions_data["factions"]:
    print(f"  {fk:12s}: {len(faction_npc_targets[fk]):4d} NPC_ records")

def convert_sliders(val_dict):
    out = {}
    for k, v in val_dict.items():
        if k in ("DoubleMelon", "BreastFantasy"):
            continue
        fv = round(float(v) / 100.0, 4)
        if k == "Breasts" and fv > 0.55:
            fv = 0.55
        if fv != 0.0:
            out[k] = fv
    return out

def format_template_rhs(norm_dict, is_female=True):
    if not norm_dict:
        return "Ankles@0.00:0.00" if is_female else "BTAbDefinition@0.00:0.00"
    parts = [f"{k}@{v:.2f}:{v:.2f}" for k, v in sorted(norm_dict.items())]
    return ",".join(parts)

# 3. Write DBR JSON files + _conds.json in BodymorphsFemale and BodymorphsMale and sync symlinks
for d in (fem_mod_dir, mal_mod_dir, fem_data_dir, mal_data_dir):
    if os.path.exists(d):
        for fn in os.listdir(d):
            if fn.startswith("Sil_") or (os.path.islink(os.path.join(d, fn)) and not os.path.exists(os.path.join(d, fn))):
                os.unlink(os.path.join(d, fn))

# Ensure directory fallback conds.json exists in BodymorphsFemale (gender 1) and BodymorphsMale (gender 0)
for target_dir, g_val in [(fem_mod_dir, 1), (mal_mod_dir, 0)]:
    os.makedirs(target_dir, exist_ok=True)
    with open(os.path.join(target_dir, "conds.json"), "w") as f:
        json.dump({
            "gender": g_val,
            "formIDs": [],
            "notFormIDs": [],
            "inFaction": [],
            "notInFaction": [],
            "hasKeyword": [],
            "hasNotKeyword": []
        }, f, indent=4)

def write_dbr_preset(is_female, base_name, norm_sliders, conds_obj=None):
    target_dir = fem_mod_dir if is_female else mal_mod_dir
    safe = re.sub(r"[^A-Za-z0-9_\-]", "_", base_name)
    json_fn = f"{safe}.json"
    json_path = os.path.join(target_dir, json_fn)
    payload = {
        "BodyMorphs": norm_sliders,
        "Gender": 1 if is_female else 0
    }
    with open(json_path, "w") as f:
        json.dump(payload, f, indent=4)
    if conds_obj is not None:
        conds_fn = f"{safe}_conds.json"
        conds_path = os.path.join(target_dir, conds_fn)
        with open(conds_path, "w") as f:
            json.dump(conds_obj, f, indent=4)

# 3a. General Pool -> DBR JSON (uses directory conds.json -> CoincidenceLevel::GENDER = 1)
for pname, pinfo in pool_data["presets"].items():
    is_fem = (pinfo["sex"] == "female")
    norm_s = convert_sliders(pinfo["values"])
    write_dbr_preset(is_fem, f"Sil_Pool_{pname}", norm_s, None)

# 3b. Faction Pool -> DBR JSON + _conds.json (uses inFaction + priority notInFaction -> CoincidenceLevel::GENDER | FACTIONS = 5)
# Note: Keeping formIDs=[] is critical so Conditions.cpp evaluates inFaction (score 5) instead of short-circuiting
# to CoincidenceLevel::FULL (0x7FFFFFFF) and colliding with Named Character presets!
faction_in_faction_strs = {}
for fk, fv in factions_data["factions"].items():
    inf_list = []
    all_edids = [f_edid for _, f_edid in fv["factions"]] + extra_subfactions.get(fk, [])
    for f_edid in all_edids:
        fk_id = edid_to_fact.get(f_edid.lower())
        if fk_id:
            f_hex = format_local_fid(fk_id[0], fk_id[1])
            entry_str = f"0x{f_hex}|{fk_id[0]}"
            if entry_str not in inf_list:
                inf_list.append(entry_str)
    faction_in_faction_strs[fk] = inf_list

faction_not_in_faction_strs = {}
for idx, fk in enumerate(faction_priority):
    higher_factions = []
    for higher_fk in faction_priority[:idx]:
        for f_str in faction_in_faction_strs.get(higher_fk, []):
            if f_str not in higher_factions:
                higher_factions.append(f_str)
    faction_not_in_faction_strs[fk] = higher_factions

for pname, pinfo in factions_data["presets"].items():
    is_fem = (pinfo["sex"] == "female")
    fk = pinfo["faction"]
    norm_s = convert_sliders(pinfo["values"])
    conds = {
        "gender": 1 if is_fem else 0,
        "formIDs": [],
        "notFormIDs": [],
        "inFaction": faction_in_faction_strs.get(fk, []),
        "notInFaction": faction_not_in_faction_strs.get(fk, []),
        "hasKeyword": [],
        "hasNotKeyword": []
    }
    write_dbr_preset(is_fem, f"Sil_Faction_{pname}", norm_s, conds)

# 3c. Named Characters -> DBR JSON + _conds.json (uses formIDs -> CoincidenceLevel::FULL = 0x7FFFFFFF)
for cname, cinfo in chars_data["characters"].items():
    is_fem = (cinfo["sex"] == "female")
    norm_s = convert_sliders(cinfo["values"])
    c_fids = []
    for plug, edid, fid_hex in cinfo["forms"]:
        if plug.lower() not in active_map:
            continue
        real_plug = active_map[plug.lower()]
        fid_int = int(fid_hex, 16)
        f_hex = format_local_fid(real_plug, fid_int)
        c_fids.append(f"0x{f_hex}|{real_plug}")
    if not c_fids:
        continue
    conds = {
        "gender": 1 if is_fem else 0,
        "formIDs": c_fids,
        "notFormIDs": [],
        "inFaction": [],
        "notInFaction": [],
        "hasKeyword": [],
        "hasNotKeyword": []
    }
    write_dbr_preset(is_fem, f"Sil_Char_{cname}", norm_s, conds)

for mod_d, data_d in [(fem_mod_dir, fem_data_dir), (mal_mod_dir, mal_data_dir)]:
    os.makedirs(data_d, exist_ok=True)
    for fn in sorted(os.listdir(mod_d)):
        src = os.path.join(mod_d, fn)
        dst = os.path.join(data_d, fn)
        if not os.path.lexists(dst):
            os.symlink(src, dst)

print(f"[3/5] Wrote DBR JSONs & _conds.json: BodymorphsFemale={len(os.listdir(fem_mod_dir))} files, BodymorphsMale={len(os.listdir(mal_mod_dir))} files (moved {disabled_moved} extreme presets to BodymorphsFemale_Disabled).")

# 4. Enforce Option B INI settings (DBR Sole Morph Authority) unless --with-bodygen is passed
if not WITH_BODYGEN:
    if os.path.exists(f4ee_ini_path):
        with open(f4ee_ini_path, "rb") as f:
            c = f.read()
        nc = c.replace(b"bEnableBodyGen=1", b"bEnableBodyGen=0")
        if nc != c:
            with open(f4ee_ini_path, "wb") as f:
                f.write(nc)
    if os.path.exists(dbr_ini_path):
        with open(dbr_ini_path, "rb") as f:
            c = f.read()
        target_line = b"sBodymorphsFolders=Data/DiverseBodiesRedux/BodymorphsFemale,Data/DiverseBodiesRedux/BodymorphsMale"
        if target_line not in c:
            nc = re.sub(rb"sBodymorphsFolders=[^\r\n]*", target_line, c)
            with open(dbr_ini_path, "wb") as f:
                f.write(nc)
    print("[4/5] Option B active (DBR Sole Morph Authority): bEnableBodyGen=0 in f4ee.ini, sBodymorphsFolders enabled in DiverseBodiesRedux.ini.")
    print("[5/5] Skipped BodyGen templates.ini / morphs.ini generation (pass --with-bodygen for Option A).")
    sys.exit(0)

# Optional Option A: Update BodyGen templates.ini & morphs.ini
with open(templates_ini_path) as f:
    orig_templates = f.read()

marker = "# === SILHOUETTE TEMPLATES (POOL + FACTIONS + CHARACTERS) ==="
if marker in orig_templates:
    base_templates = orig_templates.split(marker)[0].rstrip()
else:
    base_templates = orig_templates.rstrip()

sil_template_lines = [
    "",
    marker,
    "# Auto-generated from ReidenXerx/fo4-silhouette (pool.json, factions.json, characters.json)",
]

for pname, pinfo in pool_data["presets"].items():
    is_fem = (pinfo["sex"] == "female")
    tname = f"Sil_{pname}"
    rhs = format_template_rhs(convert_sliders(pinfo["values"]), is_fem)
    sil_template_lines.append(f"{tname}={rhs}")

for pname, pinfo in factions_data["presets"].items():
    is_fem = (pinfo["sex"] == "female")
    tname = f"Sil_{pname}"
    rhs = format_template_rhs(convert_sliders(pinfo["values"]), is_fem)
    sil_template_lines.append(f"{tname}={rhs}")

for cname, cinfo in chars_data["characters"].items():
    is_fem = (cinfo["sex"] == "female")
    tname = f"Sil_Char_{cname}"
    rhs = format_template_rhs(convert_sliders(cinfo["values"]), is_fem)
    sil_template_lines.append(f"{tname}={rhs}")

with open(templates_ini_path, "w") as f:
    f.write(base_templates + "\n" + "\n".join(sil_template_lines) + "\n")

print(f"[4/5] Updated templates.ini with {len(pool_data['presets']) + len(factions_data['presets']) + len(chars_data['characters'])} Silhouette templates.")
