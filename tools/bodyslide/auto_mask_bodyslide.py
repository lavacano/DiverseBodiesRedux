#!/usr/bin/env python3
"""
Automated BodySlide / OutfitStudio Collision Masker & Pruner
Applies strict priority: Physics >= Dismemberment > Quality > Low Quality
Preserves user's tasteful Crimsomrider 1950's outfits built in BodySlide_files.
Completely non-destructive: creates .bak_before_masking and moves files to _masked/.
"""

import os
import sys
import shutil
import xml.etree.ElementTree as ET
from collections import defaultdict

PROFILE_DIR = os.path.dirname(os.path.abspath(__file__))
MODS_DIR = os.path.join(PROFILE_DIR, "mods")
MODLIST_PATH = os.path.join(PROFILE_DIR, "modlist.txt")

def backup_file(path):
    bak = path + ".bak_before_masking"
    if not os.path.exists(bak):
        shutil.copy2(path, bak)
        print(f"  [BACKUP] Created {os.path.basename(bak)}")

def mask_file(mod_name, rel_path):
    m_dir = os.path.join(MODS_DIR, mod_name)
    src = os.path.join(m_dir, rel_path)
    if not os.path.isfile(src):
        return False
    dst = os.path.join(m_dir, "_masked", rel_path)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.move(src, dst)
    print(f"  [MASKED] [{mod_name}] {rel_path}")
    return True

def prune_sets(osp_path, sets_to_remove):
    backup_file(osp_path)
    tree = ET.parse(osp_path)
    root = tree.getroot()
    removed = 0
    for sset in list(root.findall(".//SliderSet")):
        sname = sset.get("name")
        if sname in sets_to_remove:
            root.remove(sset)
            removed += 1
    tree.write(osp_path, encoding="utf-8", xml_declaration=True)
    print(f"  [PRUNED] {removed} SliderSets removed from {os.path.basename(osp_path)}")
    return removed

def extract_sets(src_osp, dst_osp, sets_to_keep):
    backup_file(src_osp)
    tree = ET.parse(src_osp)
    root = tree.getroot()
    # Create new tree with identical root tag
    new_root = ET.Element(root.tag)
    kept = 0
    for sset in root.findall(".//SliderSet"):
        sname = sset.get("name")
        if sname in sets_to_keep:
            new_root.append(sset)
            kept += 1
    new_tree = ET.ElementTree(new_root)
    os.makedirs(os.path.dirname(dst_osp), exist_ok=True)
    new_tree.write(dst_osp, encoding="utf-8", xml_declaration=True)
    print(f"  [EXTRACTED] {kept} SliderSets written to {os.path.basename(dst_osp)}")
    return kept

def run_masking():
    print("=================================================================")
    print("STARTING AUTOMATIC BODYSLIDE COLLISION MASKING & PRUNING")
    print("=================================================================")

    # 1. Eli's Armour Compendium
    print("\n--- 1. Eli's Armour Compendium ---")
    mask_file("Eli's Armour Compendium - CBBE and BodySlide 1.5", "Tools/BodySlide/SliderSets/Eli Armour Compendium.osp")
    mask_file("Eli's Armour Compendium - EAC", "Tools/BodySlide/SliderSets/Anatomy3BBB Eli Armour Compendium.osp")

    # 2. Grease Rat Garbs
    print("\n--- 2. Grease Rat Garbs ---")
    grg_cbbe_osp = os.path.join(MODS_DIR, "Grease Rat Garbs - CBBE", "Tools/BodySlide/SliderSets/Grease Rat Garbs.osp")
    if os.path.exists(grg_cbbe_osp):
        # 21 duplicate body outfits
        grg_tree = ET.parse(grg_cbbe_osp)
        grg_sets = [s.get("name") for s in grg_tree.findall(".//SliderSet")]
        # Keep only backpack and accessories
        grg_remove = [s for s in grg_sets if not ("BackPack" in s or "Wings" in s or "Mae West" in s)]
        prune_sets(grg_cbbe_osp, set(grg_remove))

    # 3. Crimsomrider 1950s Feminine Outfits
    print("\n--- 3. Crimsomrider 1950s Feminine Outfits ---")
    # Mask all 18 OSPs in 1950s Feminine Outfits (CBBE - BODYSLIDE)
    cr_cbbe_dir = os.path.join(MODS_DIR, "1950s Feminine Outfits (CBBE - BODYSLIDE)", "Tools/BodySlide/SliderSets")
    if os.path.isdir(cr_cbbe_dir):
        for f in sorted(os.listdir(cr_cbbe_dir)):
            if f.endswith(".osp"):
                mask_file("1950s Feminine Outfits (CBBE - BODYSLIDE)", f"Tools/BodySlide/SliderSets/{f}")

    # Prune duplicate in Crimsomrider TWB.osp
    cr_twb_osp = os.path.join(MODS_DIR, "1950's Feminine Outfits TWB 3BBB-51071-3BBB-UNI", "Tools/Bodyslide/SliderSets/Crimsomrider TWB.osp")
    if os.path.exists(cr_twb_osp):
        # Remove non-TWB named duplicate set for Red Leather Trench Coat
        prune_sets(cr_twb_osp, {"Crimsomrider's Feminine Red Leather Trench Coat"})

    # Prune competing vanilla sets in TWB Vanilla.osp
    twb_van_osp = os.path.join(MODS_DIR, "TWB VANILLA 3BBB-UNI.1-51071-3BBB-UNI-REV1", "Tools/BodySlide/SliderSets/TWB Vanilla.osp")
    if os.path.exists(twb_van_osp):
        twb_remove = {
            "TWB Vanilla - Womens Casual",
            "TWB Vanilla - Short Sleeves and Slacks",
            "TWB Vanilla - Sweater Vest",
            "TWB Vanilla - Irma",
            "TWB Vanilla - Red Rocket Jumpsuit",
            "TWB Vanilla - Mayor",
            "TWB Vanilla - Postman",
            "TWB Vanilla - Suit Clean",
            "TWB Vanilla - Suit (Clean)",
            "TWB Vanilla - Suit Dirty",
            "TWB Vanilla - Suit",
            "TWB Vanilla - Vault Tec Salesman",
            "TWB Vanilla - Vault Tec Salesman (Post War)",
            "TWB Vanilla - Valentine",
            "TWB Vanilla - T-Shirt Slacks",
            "TWB Vanilla - Tuxedo",
            "TWB Vanilla - Sturgess",
            "TWB Vanilla - Vault 111 Suit",
            "TWB Vanilla - Piper",
            "TWB Vanilla - Silver Shroud",
            "TWB Vanilla - Army Fatigues",
            "NeverNude TWB", # Collides with TWB SMP body
            # Non-3BBB duplicate armor pieces inside TWB Vanilla (yielding to 3BBB counterparts)
            "TWB Vanilla - Leather - Torso Heavy",
            "TWB Vanilla - Leather - Torso Heavy (Studs)",
            "TWB Vanilla - Leather - Torso Mid",
            "TWB Vanilla - Leather - Torso Mid (Studs)",
            "TWB Vanilla - Metal - Torso Heavy",
            "TWB Vanilla - Metal - Torso Lite",
            "TWB Vanilla - Metal - Torso Mid"
        }
        prune_sets(twb_van_osp, twb_remove)

    # 4. TWB AIO Armor except raider chest armor (202 redundant OSPs)
    print("\n--- 4. TWB AIO Fallout 4 Armor ---")
    aio_dir = os.path.join(MODS_DIR, "TWB AIO Fallout 4 Armor except raider chest armor", "Tools/BodySlide/SliderSets")
    unique_aio_keep = {
        "CBBE Vanilla - Cait Bandolier.osp",
        "CBBE Nuka World - Operators - Tie.osp",
        "Abe Operators Heavy Torso.osp",
        "Abe Pack Torso.osp"
    }
    if os.path.isdir(aio_dir):
        for f in sorted(os.listdir(aio_dir)):
            if f.endswith(".osp") and f not in unique_aio_keep:
                mask_file("TWB AIO Fallout 4 Armor except raider chest armor", f"Tools/BodySlide/SliderSets/{f}")

    # 5. Caliente's Beautiful Bodies Enhancer - v2.7.2
    print("\n--- 5. Caliente's Beautiful Bodies Enhancer - v2.7.2 ---")
    cbbe_base_dir = os.path.join(MODS_DIR, "Caliente's Beautiful Bodies Enhancer - v2.7.2", "Tools/BodySlide/SliderSets")
    mask_file("Caliente's Beautiful Bodies Enhancer - v2.7.2", "Tools/BodySlide/SliderSets/CBBE Automatron.osp")
    mask_file("Caliente's Beautiful Bodies Enhancer - v2.7.2", "Tools/BodySlide/SliderSets/CBBE Far Harbor.osp")

    # CBBE Vanilla: extract 3 unique sets, then mask
    cbbe_van_osp = os.path.join(cbbe_base_dir, "CBBE Vanilla.osp")
    if os.path.exists(cbbe_van_osp):
        cbbe_van_unique = {
            "CBBE Vanilla - Knight Underarmor (Cape Maxon)",
            "CBBE Vanilla - Knight Underarmor (Coat Kells)",
            "CBBE Vanilla - Knight Underarmor (Lab Coat)"
        }
        cbbe_van_uniq_osp = os.path.join(cbbe_base_dir, "CBBE Vanilla Unique.osp")
        extract_sets(cbbe_van_osp, cbbe_van_uniq_osp, cbbe_van_unique)
        mask_file("Caliente's Beautiful Bodies Enhancer - v2.7.2", "Tools/BodySlide/SliderSets/CBBE Vanilla.osp")

    # CBBE Nuka World: extract 1 unique set, then mask
    cbbe_nw_osp = os.path.join(cbbe_base_dir, "CBBE Nuka World.osp")
    if os.path.exists(cbbe_nw_osp):
        cbbe_nw_unique = {
            "CBBE Nuka World - Western - Duster"
        }
        cbbe_nw_uniq_osp = os.path.join(cbbe_base_dir, "CBBE Nuka World Unique.osp")
        extract_sets(cbbe_nw_osp, cbbe_nw_uniq_osp, cbbe_nw_unique)
        mask_file("Caliente's Beautiful Bodies Enhancer - v2.7.2", "Tools/BodySlide/SliderSets/CBBE Nuka World.osp")

    # CBBE Creation Club: prune 5 colliding sets
    cbbe_cc_osp = os.path.join(cbbe_base_dir, "CBBE Creation Club.osp")
    if os.path.exists(cbbe_cc_osp):
        cbbe_cc_remove = {
            "CBBE Creation Club - Captain Cosmos Spacesuit",
            "CBBE Creation Club - Chinese Stealth Armor",
            "CBBE Creation Club - Doom Marine Armor",
            "CBBE Creation Club - Graphic T-Shirt",
            "CBBE Creation Club - Morgan's Space Suit"
        }
        prune_sets(cbbe_cc_osp, cbbe_cc_remove)

    # CBBE.osp: prune 5 body sets
    cbbe_body_osp = os.path.join(cbbe_base_dir, "CBBE.osp")
    if os.path.exists(cbbe_body_osp):
        cbbe_body_remove = {
            "CBBE Body",
            "CBBE Body Physics",
            "CBBE Body Reduced",
            "CBBE NeverNude",
            "CBBE NeverNude Alt"
        }
        prune_sets(cbbe_body_osp, cbbe_body_remove)

    # 6. Creation Club mods & Body Mods
    print("\n--- 6. Creation Club & Body Mods ---")
    # CC CBBE Collection: mask all 24 OSPs
    cc_coll_dir = os.path.join(MODS_DIR, "CC CBBE Collection", "Tools/Bodyslide/SliderSets")
    if os.path.isdir(cc_coll_dir):
        for f in sorted(os.listdir(cc_coll_dir)):
            if f.endswith(".osp"):
                mask_file("CC CBBE Collection", f"Tools/Bodyslide/SliderSets/{f}")

    # CC armor CBBE conversion AiO
    for f in ["EEJ_NukaFatiguesF.osp", "EEJ_NukaLeathersF.osp", "EEJ_NukaPunkF.osp", "EEJ_NukaQuantumF.osp", "EEJ_NukaRaiderF.osp", "EEJ_NukaSkirtF.osp", "TunnelSnake_F.osp"]:
        mask_file("CC armor CBBE conversion AiO", f"Tools/BodySlide/SliderSets/{f}")

    # Prey Armor.osp: prune duplicate 'Test'
    prey_osp = os.path.join(MODS_DIR, "CC armor CBBE conversion AiO", "Tools/BodySlide/SliderSets/Prey Armor.osp")
    if os.path.exists(prey_osp):
        prune_sets(prey_osp, {"Test"})

    # Nuka Pack Patch 1.2
    mask_file("Nuka Pack Patch 1.2", "Tools/BodySlide/SliderSets/Creation Club - Nuka Outfits.osp")

    # True Wasteland Body (static)
    mask_file("True Wasteland Body", "Tools/BodySlide/SliderSets/True Wasteland Body.osp")

    # CBBE 3BBB Body
    mask_file("Caliente's Beautiful Bodies Enhancer (CBBE) 3BBB Body", "Tools/Bodyslide/SliderSets/CBBE 3BBB Body.osp")

    print("\n=================================================================")
    print("MASKING AND PRUNING COMPLETE! VERIFYING REMAINING COLLISIONS...")
    print("=================================================================")
    verify_collisions()

def verify_collisions():
    enabled_mods = []
    with open(MODLIST_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("+"):
                enabled_mods.append(line[1:])

    mesh_to_sets = defaultdict(list)
    for mod in enabled_mods:
        m_dir = os.path.join(MODS_DIR, mod)
        if not os.path.isdir(m_dir):
            continue
        for root, dirs, files in os.walk(m_dir):
            if "_masked" in root:
                continue
            rel_root = os.path.relpath(root, m_dir)
            parts = [p.lower() for p in rel_root.split(os.sep)]
            if parts and parts[0] == "data":
                parts = parts[1:]
            if len(parts) >= 2 and parts[0] == "tools" and parts[1] == "bodyslide" and (len(parts) == 2 or parts[2] == "slidersets"):
                for f in files:
                    if f.endswith(".osp"):
                        osp_path = os.path.join(root, f)
                        rel_path = os.path.relpath(osp_path, m_dir)
                        try:
                            tree = ET.parse(osp_path)
                            for sset in tree.findall(".//SliderSet"):
                                sname = sset.get("name", "UNKNOWN")
                                outp_elem = sset.find("OutputPath")
                                outf_elem = sset.find("OutputFile")
                                if outf_elem is not None and outf_elem.text:
                                    outp = outp_elem.text.strip().replace("\\\\", "/").strip("/") if outp_elem is not None and outp_elem.text else ""
                                    outf = outf_elem.text.strip().replace("\\\\", "/").strip("/")
                                    full_mesh = f"{outp}/{outf}.nif".lower().replace("//", "/")
                                    sliders = len(sset.findall("Slider"))
                                    mesh_to_sets[full_mesh].append({
                                        "mod": mod,
                                        "osp": rel_path,
                                        "set_name": sname,
                                        "sliders": sliders
                                    })
                        except Exception as e:
                            pass

    collisions = {m: s for m, s in mesh_to_sets.items() if len(s) > 1}
    print(f"Total destination meshes tracked: {len(mesh_to_sets)}")
    print(f"Total meshes with collisions: {len(collisions)}")
    if collisions:
        print("\nWARNING: Unresolved collisions remaining:")
        for m, s in collisions.items():
            print(f"  Mesh: {m}")
            for item in s:
                print(f"    Mod: {item['mod']} | OSP: {item['osp']} | Set: {item['set_name']} ({item['sliders']} sliders)")
    else:
        print("\nSUCCESS: 0 COLLISIONS REMAINING! All output meshes have exactly 1 winning variant.")

if __name__ == "__main__":
    run_masking()
