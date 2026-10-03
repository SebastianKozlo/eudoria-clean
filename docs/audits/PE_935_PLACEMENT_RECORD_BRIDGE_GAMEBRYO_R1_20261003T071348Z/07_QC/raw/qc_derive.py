#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QC_DERIVE — independent re-derivations for the fresh-context QC of
PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z.

Written by the fresh QC auditor (pe-master-auditor), 2026-10-03.
STATIC_ONLY: reads physical bytes; launches nothing; modifies no executor file.

Everything below is an INDEPENDENT implementation (no reuse of the executor's
python scripts): own PE section mapper, own VFS container walk, own BNT2
trailer-index parser, own CALL-site scan of .text, own rel32 decoder.
"""

import hashlib
import json
import os
import struct
import zlib

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
TEMPLATES = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs"
V20002 = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\20002.vfs"
MODELS = r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"
OUT = os.path.join(PKG, "07_QC", "raw", "QC_DERIVATIONS.json")

R = {"inputs": {}, "pe": {}, "windows_crosscheck": {}, "vfs": {}, "bnt": {},
     "call_census": {}, "vtable": {}, "probes": {}, "errors": []}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


# ---------------------------------------------------------------- PE mapping
def load_pe(path):
    data = open(path, "rb").read()
    assert data[:2] == b"MZ", "no MZ"
    e_lfanew, = struct.unpack_from("<I", data, 0x3C)
    assert data[e_lfanew:e_lfanew + 4] == b"PE\x00\x00", "no PE sig"
    machine, nsec = struct.unpack_from("<HH", data, e_lfanew + 4)
    opt_size, = struct.unpack_from("<H", data, e_lfanew + 20)
    magic_opt, = struct.unpack_from("<H", data, e_lfanew + 24)
    image_base, = struct.unpack_from("<I", data, e_lfanew + 24 + 28)
    secs = []
    so = e_lfanew + 24 + opt_size
    for i in range(nsec):
        o = so + i * 40
        nm = data[o:o + 8].rstrip(b"\x00").decode("latin-1")
        vsz, vaddr, rsz, rptr = struct.unpack_from("<4I", data, o + 8)
        secs.append({"name": nm, "vsize": vsz, "vaddr": vaddr,
                     "rawsize": rsz, "rawptr": rptr})
    return data, {"machine": machine, "opt_magic": magic_opt,
                  "image_base": image_base, "sections": secs}


def va2fo(info, va):
    rva = va - info["image_base"]
    for s in info["sections"]:
        if s["vaddr"] <= rva < s["vaddr"] + s["rawsize"]:
            return s["rawptr"] + (rva - s["vaddr"])
    return None


def read_va(data, info, va, n):
    off = va2fo(info, va)
    if off is None:
        return None
    return data[off:off + n]


def hx(b):
    return " ".join("%02X" % c for c in b)


# ---------------------------------------------------------------- main
def main():
    # input identity pins
    for lbl, p in (("exe", EXE), ("templates_vfs", TEMPLATES),
                   ("v20002_vfs", V20002)):
        R["inputs"][lbl] = {"path": p,
                            "size": os.path.getsize(p),
                            "sha256": sha256_file(p)}

    data, pe = load_pe(EXE)
    R["pe"] = {
        "machine": "0x%04X" % pe["machine"],
        "opt_magic": "0x%04X" % pe["opt_magic"],
        "image_base": "0x%08X" % pe["image_base"],
        "sections": [{"name": s["name"], "vaddr": "0x%08X" % s["vaddr"],
                      "rawsize": s["rawsize"], "rawptr": s["rawptr"]}
                     for s in pe["sections"]],
    }

    # ---- (B) C9 listing windows vs raw bytes: FULL independent re-check
    l9 = json.load(open(os.path.join(PKG, "01_RAW", "C9_LISTING_WINDOWS.json"),
                        encoding="utf-8"))
    tot = 0
    same = 0
    mism = []
    calls = []
    for wl, w in l9["measured"]["windows"].items():
        for ins in w["instructions"]:
            va = int(ins["addr"], 16)
            toks = ins["bytes"].split()
            lb = []
            bad = False
            for t in toks:
                v = int(t, 16)
                if v < 0:
                    v &= 0xFF
                if v > 255:
                    bad = True
                lb.append(v)
            n = len(lb)
            off = va2fo(pe, va)
            raw = data[off:off + n] if off is not None else None
            tot += 1
            if raw is not None and bytes(lb) == raw and not bad:
                same += 1
            else:
                mism.append({"window": wl, "addr": ins["addr"],
                             "listing": ins["bytes"],
                             "raw": hx(raw) if raw is not None else "UNMAPPED"})
            # independent rel32 decode for E8 calls
            if raw and len(raw) >= 5 and raw[0] == 0xE8:
                rel, = struct.unpack_from("<i", raw, 1)
                tgt = va + 5 + rel
                txt = ins["text"]
                # extract listing target
                lt = None
                if "CALL" in txt:
                    for tok in txt.replace(",", " ").split():
                        if tok.startswith("0x"):
                            try:
                                lt = int(tok, 16)
                            except ValueError:
                                pass
                            break
                calls.append({"addr": "0x%08X" % va,
                              "raw_target": "0x%08X" % tgt,
                              "listing_target": ("0x%08X" % lt) if lt else None,
                              "match": (lt == tgt) if lt is not None else None,
                              "text": txt})
            # B8/68 imm32 decode
            if raw and len(raw) >= 5 and raw[0] in (0xB8, 0x68):
                imm, = struct.unpack_from("<I", raw, 1)
                lt = None
                for tok in ins["text"].replace(",", " ").split():
                    if tok.startswith("0x"):
                        try:
                            lt = int(tok, 16)
                        except ValueError:
                            pass
                        break
                calls.append({"addr": "0x%08X" % va,
                              "raw_imm32": "0x%08X" % imm,
                              "listing_imm32": ("0x%08X" % lt) if lt is not None else None,
                              "match": (lt == imm) if lt is not None else None,
                              "text": ins["text"]})
    R["windows_crosscheck"] = {
        "instructions_total": tot,
        "instructions_byte_identical": same,
        "mismatches": mism[:40],
        "n_mismatches": len(mism),
        "call_imm_checks": len(calls),
        "call_imm_matches": sum(1 for c in calls if c["match"] is True),
        "call_imm_mismatch": [c for c in calls if c["match"] is False][:20],
    }

    # ---- (C) own VFS walk (templates)
    def walk_vfs(path):
        d = open(path, "rb").read()
        magic = d[:8]
        base, = struct.unpack_from("<I", d, 8)
        recs = []
        pos = 16
        crcfail = 0
        while pos + 16 <= len(d):
            bid, bsz, bver, bcrc = struct.unpack_from("<IIII", d, pos)
            if pos + 16 + bsz > len(d):
                return {"ok": False, "err": "truncated@%d" % pos,
                        "magic": magic.decode("latin-1", "replace"),
                        "base": base, "recs": recs, "crcfail": crcfail}
            pl = d[pos + 16:pos + 16 + bsz]
            if bcrc != 0 and (zlib.crc32(pl) & 0xFFFFFFFF) != bcrc:
                crcfail += 1
            recs.append((pos, bid, bsz, bver, bcrc, pl))
            pos += ((16 + bsz + base - 1) // base) * base
        return {"ok": pos == len(d), "magic": magic.decode("latin-1", "replace"),
                "base": base, "recs": recs, "crcfail": crcfail,
                "stop_pos": pos, "size": len(d)}

    tv = walk_vfs(TEMPLATES)
    R["vfs"]["templates"] = {
        "magic": tv["magic"], "base": tv["base"], "ok": tv["ok"],
        "record_count": len(tv["recs"]), "crc_fail": tv["crcfail"],
        "stop_pos": tv["stop_pos"], "file_size": tv["size"],
        "unique_ids": len(set(r[1] for r in tv["recs"])),
    }
    # record 4508 by own scan
    r4508 = None
    for (pos, bid, bsz, bver, bcrc, pl) in tv["recs"]:
        if bid == 4508:
            r4508 = {"file_offset": pos, "size": bsz, "ver": bver,
                     "crc32_field": "%08X" % bcrc,
                     "payload_hex": hx(pl),
                     "payload_len": len(pl)}
            break
    R["vfs"]["templates_rec4508"] = r4508
    if r4508:
        for (pos, bid, bsz, bver, bcrc, pl) in tv["recs"]:
            if bid == 4508:
                u32s = struct.unpack("<7I", pl[:28])
                f32_at16 = struct.unpack_from("<f", pl, 16)[0]
                R["vfs"]["templates_rec4508_parse"] = {
                    "u32_0": u32s[0], "u32_4": u32s[1], "u32_8": u32s[2],
                    "u32_12": u32s[3], "u32_16_raw": u32s[4],
                    "u32_20": u32s[5], "u32_24": u32s[6],
                    "f32_at16": f32_at16,
                    "f32_at16_bits": "0x%08X" % u32s[4],
                    "list1_count_u16_at20": struct.unpack_from("<H", pl, 20)[0],
                    "list2_count_u16_at22": struct.unpack_from("<H", pl, 22)[0],
                    "f11_u32_at24": struct.unpack_from("<I", pl, 24)[0],
                    "crc32_recomputed": "%08X" % (zlib.crc32(pl) & 0xFFFFFFFF),
                    "crc32_matches_field": ("%08X" % (zlib.crc32(pl) & 0xFFFFFFFF)) == r4508["crc32_field"].upper(),
                }
                break
    # direct byte read at 96,496 (header) and 96,516 (A field)
    with open(TEMPLATES, "rb") as f:
        f.seek(96496)
        hdr = f.read(16)
        R["vfs"]["direct_read_at_96496"] = {
            "header_hex": hx(hdr),
            "id": struct.unpack_from("<I", hdr, 0)[0],
            "size": struct.unpack_from("<I", hdr, 4)[0],
            "ver": struct.unpack_from("<I", hdr, 8)[0],
            "crc": "%08X" % struct.unpack_from("<I", hdr, 12)[0],
        }
        f.seek(96516)
        R["vfs"]["direct_read_at_96516_A"] = hx(f.read(4))
        f.seek(96512)
        R["vfs"]["direct_read_at_96512_D"] = hx(f.read(4))
    # record 11963
    for (pos, bid, bsz, bver, bcrc, pl) in tv["recs"]:
        if bid == 11963:
            R["vfs"]["templates_rec11963"] = {
                "file_offset": pos, "size": bsz, "payload_len": len(pl),
                "payload_first32": hx(pl[:32]),
                "list1_count_u16_at20": struct.unpack_from("<H", pl, 20)[0],
                "A_u32_at4": struct.unpack_from("<I", pl, 4)[0],
            }
            break

    # 20002 walk + record 0 + off-0x30 column
    v = walk_vfs(V20002)
    R["vfs"]["v20002"] = {"ok": v["ok"], "base": v["base"],
                          "record_count": len(v["recs"]),
                          "crc_fail": v["crcfail"], "stop_pos": v["stop_pos"],
                          "file_size": v["size"]}
    p0 = v["recs"][0][5]
    R["vfs"]["v20002_rec0"] = {
        "file_offset": v["recs"][0][0], "id": v["recs"][0][1],
        "payload_len": len(p0), "payload_hex": hx(p0),
        "u32_at48": struct.unpack_from("<I", p0, 48)[0],
    }
    id2set = set(r[1] for r in tv["recs"])
    hits = 0
    miss = []
    for (pos, bid, bsz, bver, bcrc, pl) in v["recs"]:
        if len(pl) >= 52:
            x = struct.unpack_from("<I", pl, 48)[0]
            if x in id2set:
                hits += 1
            else:
                miss.append(x)
    R["vfs"]["v20002_off48_column"] = {"scanned": len(v["recs"]),
                                       "hits": hits, "misses": len(miss),
                                       "miss_values": miss[:10]}

    # ---- (D) Models.bnt index (own trailer parser)
    size = os.path.getsize(MODELS)
    with open(MODELS, "rb") as f:
        f.seek(size - 8)
        tail = f.read(8)
    idx_start, = struct.unpack_from("<I", tail, 0)
    R["bnt"]["tail"] = {"magic": tail[4:8].decode("latin-1"),
                        "index_start": idx_start, "file_size": size}
    with open(MODELS, "rb") as f:
        f.seek(idx_start)
        blob = f.read()
    count, = struct.unpack_from("<I", blob, 0)
    names = {}
    pos = 4
    cnt = 0
    while pos < len(blob):
        nl = blob.find(b"\x0a", pos)
        if nl < 0:
            break
        nm = blob[pos:nl].decode("latin-1")
        names[idx_start + pos] = nm
        pos = nl + 1 + 16
        cnt += 1
    R["bnt"]["index"] = {"entry_count_u32": count, "entries_walked": cnt,
                         "unique_names": len(set(names.values()))}
    want = {"296445.nif", "551661.nif", "296446.nif", "460563.nif",
            "4508.nif", "16082.nif"}
    found = {}
    for off, nm in names.items():
        if nm in want:
            found[nm] = off
    R["bnt"]["wanted"] = found
    # direct read at 395,268,773: expect "296445.nif\x0a"
    with open(MODELS, "rb") as f:
        f.seek(395268773)
        b = f.read(12)
    R["bnt"]["direct_at_395268773"] = b.hex(" ")
    with open(MODELS, "rb") as f:
        f.seek(395323507)
        R["bnt"]["direct_at_395323507"] = f.read(12).hex(" ")

    # ---- (F) own CALL-site census of .text (E8 rel32 anywhere in .text)
    text = None
    for s in pe["sections"]:
        if s["name"] == ".text":
            text = s
    base_va = pe["image_base"] + text["vaddr"]
    seg = data[text["rawptr"]:text["rawptr"] + text["rawsize"]]
    targets = {
        "lookup_FUN_0072F580": 0x0072F580,
        "reader_FUN_0072FA30": 0x0072FA30,
        "getter_FUN_007CE1E0": 0x007CE1E0,
        "ArkObject_ctor_FUN_00726E70": 0x00726E70,
        "pump_FUN_006C9700": 0x006C9700,
        "inst_creator_FUN_006CB6F0": 0x006CB6F0,
        "named_inst_FUN_006CB020": 0x006CB020,
        "pending_attach_FUN_006CB3C0": 0x006CB3C0,
        "callback_0x008BD720": 0x008BD720,
        "SetName_FUN_007B67E0": 0x007B67E0,
        "NiNode_ctor_FUN_007B6000": 0x007B6000,
        "mapfind_FUN_004D1430": 0x004D1430,
        "deserA_FUN_007453D0": 0x007453D0,
        "parse_FUN_00730C90": 0x00730C90,
        "pos_setter_FUN_00730F90": 0x00730F90,
        "rot_setter_FUN_00730FB0": 0x00730FB0,
        "pair_setter_FUN_00730FD0": 0x00730FD0,
        "insert_FUN_0072F8D0": 0x0072F8D0,
    }
    census = {}
    for i in range(len(seg) - 5):
        if seg[i] == 0xE8:
            rel, = struct.unpack_from("<i", seg, i + 1)
            tgt = base_va + i + 5 + rel
            for lbl, tv_ in targets.items():
                if tgt == tv_:
                    census.setdefault(lbl, []).append("0x%08X" % (base_va + i))
    R["call_census"] = {lbl: {"callsites": len(v), "sites": v[:60]}
                        for lbl, v in census.items()}
    # also: how many of the E8 hits coincide with C2's Ghidra census numbers?

    # ---- (G) NiNode vtable re-derivation from ctor bytes
    ctor = read_va(data, pe, 0x007B6000, 128)
    vt = None
    for i in range(120):
        if ctor[i] == 0xC7 and (ctor[i + 1] & 0xC0) == 0x00:
            imm, = struct.unpack_from("<I", ctor, i + 2)
            vt = imm
            R["vtable"]["ctor_store_site_va"] = "0x%08X" % (0x007B6000 + i)
            break
    R["vtable"]["vtable_va"] = "0x%08X" % vt
    vtbytes = read_va(data, pe, vt, 47 * 4)
    slots = [struct.unpack_from("<I", vtbytes, i * 4)[0] for i in range(47)]
    R["vtable"]["slot_count"] = 47
    R["vtable"]["slot17"] = "0x%08X" % slots[17]
    R["vtable"]["slot27"] = "0x%08X" % slots[27]
    R["vtable"]["slot0"] = "0x%08X" % slots[0]
    R["vtable"]["slot_last"] = "0x%08X" % slots[46]
    # slot 27 probe: rep movsd in first 512 bytes (own scan)
    s27 = slots[27]
    body = read_va(data, pe, s27, 512)
    reps = [i for i in range(len(body) - 1) if body[i] == 0xF3 and body[i + 1] == 0xA5]
    # consecutive runs
    runs = []
    i = 0
    while i < len(reps):
        j = i
        c = 1
        while j + 1 < len(reps) and reps[j + 1] == reps[j] + 2:
            c += 1
            j += 1
        runs.append(c)
        i = j + 1
    R["vtable"]["slot27_probe"] = {
        "rep_movsd_offsets_512B": reps[:20],
        "n_rep_movsd": len(reps),
        "max_consecutive": max(runs) if runs else 0,
        "first_24_bytes": hx(body[:24]),
    }
    # prolog check of slot 17 (0x007B5390)
    R["vtable"]["slot17_bytes_12"] = hx(read_va(data, pe, slots[17], 12))

    # ---- (H) probes: getter body, SetName body, reader prolog, callback,
    #           dispatcher immediates, emitter bytes
    R["probes"]["getter_FUN_007CE1E0_first16"] = hx(read_va(data, pe, 0x007CE1E0, 16))
    R["probes"]["SetName_FUN_007B67E0_first48"] = hx(read_va(data, pe, 0x007B67E0, 48))
    R["probes"]["reader_FUN_0072FA30_first32"] = hx(read_va(data, pe, 0x0072FA30, 32))
    R["probes"]["callback_0x008BD720_first32"] = hx(read_va(data, pe, 0x008BD720, 32))
    R["probes"]["emitter_006C3F50_006C3FB0"] = hx(read_va(data, pe, 0x006C3F50, 0x60))
    R["probes"]["lookup_FUN_0072F580_first48"] = hx(read_va(data, pe, 0x0072F580, 48))
    R["probes"]["mapfind_FUN_004D1430_first16"] = hx(read_va(data, pe, 0x004D1430, 16))
    R["probes"]["parse_FUN_00730C90_first32"] = hx(read_va(data, pe, 0x00730C90, 32))
    R["probes"]["insert_FUN_0072F8D0_first16"] = hx(read_va(data, pe, 0x0072F8D0, 16))
    # dispatcher window: look for immediates 0xA2..0xC7 in FUN_004B18D0..+0x900
    win = read_va(data, pe, 0x004B18D0, 0x900)
    imm_hits = {}
    for i in range(len(win) - 4):
        if win[i] in (0x3D, 0x81) and win[i + 1] == 0xF8:  # CMP EAX, imm32/imm8 variants
            pass
        # cmp eax, imm32 = 3D imm32 ; cmp reg, imm32 = 81 F8+r imm32 ; sub cmp imm8 = 83 F8+r imm8
        if win[i] == 0x3D:
            imm, = struct.unpack_from("<I", win, i + 1)
            if 0xA2 <= imm <= 0xC7:
                imm_hits.setdefault("cmp_eax_imm32_0x%02X" % imm, []).append("0x%08X" % (0x004B18D0 + i))
        if win[i] == 0x81 and win[i + 1] in (0xF8, 0xF9, 0xFA, 0xFB, 0xFC, 0xFD, 0xFE, 0xFF):
            imm, = struct.unpack_from("<I", win, i + 2)
            if 0xA2 <= imm <= 0xC7:
                imm_hits.setdefault("cmp_r_imm32_0x%02X" % imm, []).append("0x%08X" % (0x004B18D0 + i))
        if win[i] == 0x83 and win[i + 1] in (0xF8, 0xF9, 0xFA, 0xFB, 0xFC, 0xFD, 0xFE, 0xFF):
            imm = win[i + 2]
            if 0xA2 <= imm <= 0xC7:
                imm_hits.setdefault("cmp_r_imm8_0x%02X" % imm, []).append("0x%08X" % (0x004B18D0 + i))
        if win[i] == 0x68:
            imm, = struct.unpack_from("<I", win, i + 1)
            if 0xA2 <= imm <= 0xC7:
                imm_hits.setdefault("push_imm32_0x%02X" % imm, []).append("0x%08X" % (0x004B18D0 + i))
    R["probes"]["dispatcher_004B18D0_imm_scan"] = {k: v[:8] for k, v in imm_hits.items()}

    # string pin: Parameters\templates.vfs
    needle = b"Parameters\\templates.vfs\x00"
    i = data.find(needle)
    hits = []
    while i >= 0 and len(hits) < 10:
        for s in pe["sections"]:
            if s["rawptr"] <= i < s["rawptr"] + s["rawsize"]:
                hits.append({"file_offset": i,
                             "va": "0x%08X" % (pe["image_base"] + s["vaddr"] + (i - s["rawptr"])),
                             "section": s["name"]})
                break
        i = data.find(needle, i + 1)
    R["probes"]["string_pin"] = hits

    # scene root string
    n2 = b"NetImmerseScene::Root\x00"
    j = data.find(n2)
    R["probes"]["scene_root_string"] = None if j < 0 else {
        "file_offset": j, "va": "0x%08X" % (pe["image_base"] + 0x675000 + (j - [s["rawptr"] for s in pe["sections"] if s["name"] == ".rdata"][0]))}
    # ArkAnimation gate string
    n3 = b"ArkAnimation"
    k = data.find(n3)
    R["probes"]["arkanimation_string_fileoff"] = k

    # NiControllerSequence RTTI probe
    n4 = b"NiControllerSequence"
    m = data.find(n4)
    R["probes"]["nics_string_fileoff"] = m

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(R, f, indent=2)
    print("QC_DERIVE written:", OUT)
    print("windows: %d/%d identical, mismatches=%d" % (
        R["windows_crosscheck"]["instructions_byte_identical"],
        R["windows_crosscheck"]["instructions_total"],
        R["windows_crosscheck"]["n_mismatches"]))
    print("call/imm checks:", R["windows_crosscheck"]["call_imm_checks"],
          "matches:", R["windows_crosscheck"]["call_imm_matches"])
    print("templates records:", R["vfs"]["templates"]["record_count"],
          "unique:", R["vfs"]["templates"]["unique_ids"])
    print("rec4508:", R["vfs"]["templates_rec4508"])
    print("call census:", {k: v["callsites"] for k, v in R["call_census"].items()})
    print("bnt wanted:", R["bnt"]["wanted"])


if __name__ == "__main__":
    main()
