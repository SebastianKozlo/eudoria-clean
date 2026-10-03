#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S2 CALL-SITE RAW PIN — PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003
Executor: pe-reconstruction. ERA: PCG/EU 9.3.5 (pcg_install). STATIC-ONLY.

Contract §9 (Phase 2): physical raw bytes of Entropia.exe at/around VA
0x0059AB12 — BEFORE Ghidra-based phases:
  - own PE-header parse (image base, ASLR state, section table);
  - own VA->file-offset mapper;
  - two independent calibrations of the mapper against canon byte anchors:
      (a) .rdata string "Parameters\\templates.vfs" @VA 0x00A86D30 ->
          canon file offset 6,843,696 (record-bridge E1 raw pin);
      (b) code anchor PUSH 0x3ED3 @VA 0x005B6597 (bytes 68 D3 3E 00 00;
          record-bridge E9 byte pin);
  - instruction opcode + immediate verification at VA 0x0059AB12
    (expected, per the lead: 68 D9 0F 00 00 = PUSH imm32 0x00000FD9 = 4057);
  - containing executable section identity;
  - bounded raw window dump (default: VA-0x180 .. VA+0x280);
  - optional: --crosscheck <g1_json> verifies every (addr, bytes) pair of a
    Ghidra listing dump against the physical EXE (c10v2-equivalent method,
    own implementation) and appends the result to RAW_BYTE_PINS.json;
  - optional: --window START END (hex VAs) adds one extra bounded window
    (used after Phase 3 to cover the exact containing-function extent).

Interpreter: python 3.12.10 (local Windows). Invoke:
  python 03_SCRIPTS/s2_callsite_rawpin.py
  python 03_SCRIPTS/s2_callsite_rawpin.py --window 0x0059A900 0x0059AD00
  python 03_SCRIPTS/s2_callsite_rawpin.py --crosscheck <scratch>/g1_callsite_dump.json
Outputs: 01_RAW/RAW_BYTE_PINS.json + 01_RAW/CALLSITE_WINDOW.json. No input modified.
"""

import hashlib
import json
import os
import struct
import sys

RUN_ID = "PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003"
HERE = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.normpath(os.path.join(HERE, "..", "01_RAW"))
OUT_PINS = os.path.join(RAWDIR, "RAW_BYTE_PINS.json")
OUT_WIN = os.path.join(RAWDIR, "CALLSITE_WINDOW.json")

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
EXPECT_SIZE = 8015872
EXPECT_SHA256 = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"

ANCHOR_VA = 0x0059AB12
CAL_STR_VA = 0x00A86D30
CAL_STR_OFF = 6843696
CAL_STR_BYTES = b"Parameters\\templates.vfs"
CAL_PUSH_VA = 0x005B6597
CAL_PUSH_BYTES = bytes.fromhex("68 D3 3E 00 00")
EXPECTED_CALLSITE_BYTES = bytes.fromhex("68 D9 0F 00 00")  # PUSH imm32 0x00000FD9


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def parse_pe(path):
    data_head = open(path, "rb").read(0x400)
    if data_head[:2] != b"MZ":
        return None, "no MZ"
    e_lfanew = struct.unpack_from("<I", data_head, 0x3C)[0]
    pe = data_head[e_lfanew:e_lfanew + 24]
    if pe[:4] != b"PE\x00\x00":
        return None, "no PE sig"
    machine, nsec, _tdate, _pptr, _nsym, _optsize, _chars = struct.unpack_from("<HHIIIHH", pe, 4)
    opt_off = e_lfanew + 24
    opt = data_head[opt_off:opt_off + 96]
    magic = struct.unpack_from("<H", opt, 0)[0]
    if magic != 0x10B:
        return None, "not PE32 (magic 0x%X)" % magic
    image_base = struct.unpack_from("<I", opt, 28)[0]
    dll_chars = struct.unpack_from("<H", opt, 70)[0]
    entry_rva = struct.unpack_from("<I", opt, 16)[0]
    secs = []
    sec_off = opt_off + struct.unpack_from("<H", pe, 20)[0]
    with open(path, "rb") as f:
        f.seek(sec_off)
        sect_blob = f.read(40 * nsec)
    for i in range(nsec):
        s = sect_blob[i * 40:(i + 1) * 40]
        name = s[:8].rstrip(b"\x00").decode("latin-1")
        vsize, vaddr, rawsize, rawptr = struct.unpack_from("<IIII", s, 8)
        secs.append({"name": name, "virtual_size": vsize, "virtual_address": vaddr,
                     "raw_size": rawsize, "raw_ptr": rawptr})
    return {"machine": machine, "nsec": nsec, "image_base": image_base,
            "dll_chars": dll_chars, "entry_rva": entry_rva, "sections": secs,
            "e_lfanew": e_lfanew, "opt_magic": magic}, None


def va_to_off(pe, va):
    rva = va - pe["image_base"]
    for s in pe["sections"]:
        lo = s["virtual_address"]
        hi = lo + max(s["virtual_size"], s["raw_size"])
        if lo <= rva < hi:
            if s["raw_ptr"] == 0 or (rva - lo) >= s["raw_size"]:
                return None, s["name"]
            return s["raw_ptr"] + (rva - lo), s["name"]
    return None, None


def read_at(path, off, n):
    with open(path, "rb") as f:
        f.seek(off)
        return f.read(n)


def hex_window(data_path, pe, va_start, va_end):
    rows = []
    va = va_start
    while va < va_end:
        off, sec = va_to_off(pe, va)
        chunk_len = min(16, va_end - va)
        if off is None:
            rows.append({"va": "0x%08X" % va, "file_offset": None,
                         "hex": None, "note": "not raw-mapped (section tail)"})
            va += chunk_len
            continue
        chunk = read_at(data_path, off, chunk_len)
        printable = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        rows.append({"va": "0x%08X" % va, "file_offset": off,
                     "hex": chunk.hex(" "), "ascii": printable})
        va += chunk_len
    return rows


def parse_ghidra_bytes(bstr):
    """Parse a Ghidra listing bytes field into bytes. Handles both clean
    unsigned hex ('68 D9 0F') and Jython signed-hex artifacts ('-27' = 0xD9,
    produced by '%02X' % signed_byte in Python/Jython 2.7)."""
    out = bytearray()
    for tok in bstr.split():
        if tok.startswith("-"):
            out.append((-int(tok[1:], 16)) & 0xFF)
        else:
            out.append(int(tok, 16) & 0xFF)
    return bytes(out)


def crosscheck_g1(exe_path, pe, g1_path):
    """Verify every (addr, bytes) pair from a Ghidra listing dump against the
    physical EXE via this run's own mapper. Returns per-instruction results."""
    with open(g1_path, "r") as f:
        g1 = json.load(f)
    pairs = []
    fn = g1.get("measured", {}).get("function", {})
    for ins in fn.get("listing", []):
        pairs.append((int(ins["addr"], 16), parse_ghidra_bytes(ins["bytes"])))
    total = len(pairs)
    match = 0
    mismatch = []
    for va, bts in pairs:
        off, sec = va_to_off(pe, va)
        if off is None:
            mismatch.append({"va": "0x%08X" % va, "error": "no raw mapping"})
            continue
        phys = read_at(exe_path, off, len(bts))
        if phys == bts:
            match += 1
        else:
            mismatch.append({"va": "0x%08X" % va, "ghidra": bts.hex(" "),
                             "physical": phys.hex(" ")})
    return {"pairs": total, "match": match, "mismatch_count": len(mismatch),
            "mismatches": mismatch[:50], "all_match": (match == total and total > 0)}


def main():
    argv = sys.argv[1:]
    extra_window = None
    crosscheck_path = None
    i = 0
    while i < len(argv):
        if argv[i] == "--window" and i + 2 < len(argv):
            extra_window = (int(argv[i + 1], 16), int(argv[i + 2], 16))
            i += 3
        elif argv[i] == "--crosscheck" and i + 1 < len(argv):
            crosscheck_path = argv[i + 1]
            i += 2
        else:
            i += 1

    res = {"run_id": RUN_ID, "stage": "S2_callsite_raw_pin",
           "measured": {}, "interpreted": {}, "errors": []}
    M = res["measured"]
    os.makedirs(RAWDIR, exist_ok=True)

    size = os.path.getsize(EXE)
    sha = sha256_file(EXE)
    M["exe_identity"] = {"path": EXE, "size_bytes": size, "sha256": sha}
    pin_ok = (size == EXPECT_SIZE and sha == EXPECT_SHA256)

    pe, err = parse_pe(EXE)
    if pe is None:
        res["errors"].append("PE parse failed: %s" % err)
        print("S2 FATAL: PE parse failed:", err)
        sys.exit(1)
    M["pe_header"] = {"machine": "0x%04X" % pe["machine"], "nsec": pe["nsec"],
                      "image_base": "0x%08X" % pe["image_base"],
                      "dll_characteristics": "0x%04X" % pe["dll_chars"],
                      "aslr": bool(pe["dll_chars"] & 0x0040),
                      "entry_rva": "0x%08X" % pe["entry_rva"],
                      "sections": pe["sections"]}

    # calibrations of the VA->file mapper
    cal1_off, cal1_sec = va_to_off(pe, CAL_STR_VA)
    cal1_bytes = read_at(EXE, cal1_off, len(CAL_STR_BYTES)) if cal1_off is not None else b""
    cal2_off, cal2_sec = va_to_off(pe, CAL_PUSH_VA)
    cal2_bytes = read_at(EXE, cal2_off, len(CAL_PUSH_BYTES)) if cal2_off is not None else b""
    M["mapper_calibrations"] = {
        "string_anchor": {"va": "0x%08X" % CAL_STR_VA, "file_offset": cal1_off,
                          "section": cal1_sec, "expected_file_offset": CAL_STR_OFF,
                          "bytes": cal1_bytes.decode("latin-1"),
                          "ok": (cal1_off == CAL_STR_OFF and cal1_bytes == CAL_STR_BYTES)},
        "code_anchor_push_3ED3": {"va": "0x%08X" % CAL_PUSH_VA, "file_offset": cal2_off,
                                  "section": cal2_sec, "bytes_hex": cal2_bytes.hex(" "),
                                  "ok": (cal2_bytes == CAL_PUSH_BYTES)},
    }

    # callsite pin
    off, sec = va_to_off(pe, ANCHOR_VA)
    site5 = read_at(EXE, off, 5) if off is not None else b""
    prev16 = read_at(EXE, off - 16, 16) if (off or 0) >= 16 else b""
    next16 = read_at(EXE, off + 5, 16) if off is not None else b""
    M["callsite"] = {
        "anchor_va": "0x%08X" % ANCHOR_VA, "file_offset": off, "section": sec,
        "rva": "0x%08X" % (ANCHOR_VA - pe["image_base"]),
        "bytes_at_anchor_hex": site5.hex(" "),
        "expected_bytes_hex": EXPECTED_CALLSITE_BYTES.hex(" "),
        "is_push_imm32_4057": (site5 == EXPECTED_CALLSITE_BYTES),
        "imm32_value_if_push": struct.unpack("<I", site5[1:5])[0] if len(site5) == 5 and site5[0] == 0x68 else None,
        "preceding_16B_hex": prev16.hex(" "),
        "following_16B_hex": next16.hex(" "),
    }

    I = res["interpreted"]
    I["INPUT_EXE_PIN_OK"] = pin_ok
    I["MAPPER_CALIBRATED"] = (M["mapper_calibrations"]["string_anchor"]["ok"]
                              and M["mapper_calibrations"]["code_anchor_push_3ED3"]["ok"])
    I["IMMEDIATE_4057_RAW_PIN"] = "CONFIRMED" if M["callsite"]["is_push_imm32_4057"] else "REJECTED"
    I["IMMEDIATE_4057_AT_0x0059AB12"] = "CONFIRMED" if M["callsite"]["is_push_imm32_4057"] else "REJECTED"
    I["pin_provenance"] = {
        "callsite_raw": {
            "MEASURED_QUANTITY": "the 5 physical bytes at the file offset mapped from VA 0x0059AB12, plus surrounding bytes",
            "INDEPENDENT_SOURCE_OF_TRUTH": "physical bytes of Entropia.exe (re-hashed this run) read via this run's own PE mapper (no disassembler involved)",
            "WHY_NON_CIRCULAR": "the mapper is calibrated on two independent canon byte anchors (string @0x00A86D30->6,843,696; PUSH 0x3ED3 @0x005B6597) before the callsite bytes are trusted; the PUSH/4057 hypothesis enters only as the expected-value comparison",
            "FAILURE_CASE_DETECTED": "wrong mapping => calibration anchors fail; bytes not 68 D9 0F 00 00 => IMMEDIATE_4057_RAW_PIN=REJECTED (STOP S1)"},
    }

    if crosscheck_path:
        M["g1_byte_crosscheck"] = crosscheck_g1(EXE, pe, crosscheck_path)

    with open(OUT_PINS, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    print("S2 pins written:", OUT_PINS)
    print("exe pin ok:", pin_ok, "| mapper calibrated:", I["MAPPER_CALIBRATED"])
    print("callsite bytes:", site5.hex(" "), "| PUSH imm32:", M["callsite"]["imm32_value_if_push"],
          "| PIN:", I["IMMEDIATE_4057_RAW_PIN"])
    if crosscheck_path:
        print("g1 crosscheck:", M["g1_byte_crosscheck"]["match"], "/", M["g1_byte_crosscheck"]["pairs"],
              "all_match:", M["g1_byte_crosscheck"]["all_match"])

    # window file
    win = {"run_id": RUN_ID, "stage": "S2_callsite_window",
           "measured": {"exe_sha256": sha, "image_base": "0x%08X" % pe["image_base"]}, "windows": {}}
    win["windows"]["callsite_default"] = {
        "va_start": "0x%08X" % (ANCHOR_VA - 0x180), "va_end": "0x%08X" % (ANCHOR_VA + 0x280),
        "anchor_va": "0x%08X" % ANCHOR_VA,
        "rows": hex_window(EXE, pe, ANCHOR_VA - 0x180, ANCHOR_VA + 0x280)}
    if extra_window:
        win["windows"]["extra_window"] = {
            "va_start": "0x%08X" % extra_window[0], "va_end": "0x%08X" % extra_window[1],
            "rows": hex_window(EXE, pe, extra_window[0], extra_window[1])}
    if crosscheck_path:
        win["windows"]["note"] = "g1 crosscheck result lives in RAW_BYTE_PINS.json"
    with open(OUT_WIN, "w", encoding="utf-8") as f:
        json.dump(win, f, indent=2)
    print("S2 window written:", OUT_WIN, "| extra_window:", extra_window is not None)


if __name__ == "__main__":
    main()
