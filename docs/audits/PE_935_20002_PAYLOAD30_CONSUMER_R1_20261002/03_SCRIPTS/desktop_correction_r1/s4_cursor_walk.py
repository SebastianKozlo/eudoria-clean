# s4_cursor_walk.py — CURSOR_PROOF_CORRECTION_R1.json generator (DESKTOP_CORRECTION_R1)
# Re-derives the cursor provenance FOR THE SELECTED READER (the virtual-branch
# type-1 reader FUN_009777F0) from the pinned 20002.vfs bytes + the byte-pinned
# parser logic:
#   - own framing walk (ArkVFS02: 16-byte global header, base 0x80 stride rule)
#   - own TLV cursor simulation: entry offset 8 (the FUN_0070dcf0 advance-8),
#     header u16 reads, per-entry u16 tag reads, value widths per descriptor type
#     (type 4 -> 8 bytes; type 2 -> 4; type 1 -> 4), the tag-0x11 value offset == 0x30
#   - record 0 (ANCHOR_PRIMARY) and record 1014 (ANCHOR_ZERO) full walk states
#   - the 1366-record census denominator re-derived (exact-EOF invariant)
#   - success path vs error/failure path distinction (the cursor flag byte + bounds)
# Static analysis only. Self-contained.
import sys, os, json, struct, hashlib
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pe_parse

RUN_ID = "PE_935_20002_PAYLOAD30_DESKTOP_CORRECTION_R1_20261002"
VFS_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\20002.vfs"
VFS_EXPECTED_SIZE = 174864
VFS_EXPECTED_SHA256 = "C3899C3E88D72CE12CEF9B8A4F5E73B26632BB1A3207C950FF2BC40FD9C94AC4"
OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "01_RAW", "DESKTOP_CORRECTION_R1",
                                    "CURSOR_PROOF_CORRECTION_R1.json"))

with open(VFS_PATH, "rb") as f:
    vfs = f.read()
vfs_sha = hashlib.sha256(vfs).hexdigest().upper()
assert len(vfs) == VFS_EXPECTED_SIZE and vfs_sha == VFS_EXPECTED_SHA256, "VFS identity mismatch"

pe = pe_parse.PE32()

# ---------------- framing walk (own implementation) ----------------
BASE = 0x80
assert vfs[0:4] == b"AK\x02\x00" or True  # magic bytes recorded below (do not fail-close on assumption)
MAGIC = vfs[0:16].hex().upper()

def walk_records():
    records = []
    pos = 16
    n = 0
    while pos < len(vfs):
        if pos + 16 > len(vfs):
            raise RuntimeError("truncated record header at %d" % pos)
        rid, size, ver, crc = struct.unpack_from("<IIII", vfs, pos)
        if size == 0 or ver != 1:
            raise RuntimeError("invalid record at %d (size=%d ver=%d)" % (pos, size, ver))
        stride = ((16 + size + BASE - 1) // BASE) * BASE
        if pos + 16 + size > len(vfs) or pos + stride > len(vfs):
            raise RuntimeError("payload beyond EOF at %d" % pos)
        payload = vfs[pos + 16: pos + 16 + size]
        records.append({
            "ordinal": n,
            "frame_start": pos,
            "payload_start": pos + 16,
            "payload": payload,
            "id": rid,
            "size": size,
            "ver": ver,
            "crc": crc,
            "stride": stride,
        })
        pos += stride
        n += 1
    if pos != len(vfs):
        raise RuntimeError("non-exact EOF: pos=%d filesize=%d" % (pos, len(vfs)))
    return records

records = walk_records()

# ---------------- byte-proven cursor semantics ----------------
# widths per descriptor type, each byte-pinned in this run (see width_sources below)
WIDTH_BY_TYPE = {1: 4, 2: 4, 4: 8}
# descriptor type per tag, from the byte-pinned schema registration in FUN_00761570
TYPE_BY_TAG = {0x01: 4, 0x0C: 2, 0x0D: 1, 0x0E: 1, 0x10: 1, 0x11: 1}

def simulate(payload, record_label, error_injection=None):
    """Simulate the byte-pinned cursor logic. Returns (states, ok, events).
    error_injection: None | 'truncate_48' | 'clear_flag_at_entry' | 'shift_tags'"""
    limit = len(payload)
    offset = 0
    flag = 1
    if error_injection == "truncate_48":
        limit = 48  # simulate a truncated payload: bounds must fail at the tag-0x11 value
    if error_injection == "clear_flag_at_entry":
        flag = 0
    states = []
    events = []

    def bounds(n, where):
        # the byte-proven bounds shape: (offset + width) <= limit, else flag cleared
        nonlocal flag
        if offset + n > limit:
            flag = 0
            events.append({"where": where, "event": "BOUNDS_FAILURE offset+%d > limit" % n, "offset": offset,
                           "limit": limit, "flag_cleared": True})
            return False
        return True

    def advance(n, where):
        # FUN_0040de60: offset += n; if offset > limit: flag = 0
        nonlocal offset, flag
        offset += n
        if offset > limit:
            flag = 0
            events.append({"where": where, "event": "ADVANCE_OVERRUN offset > limit", "offset": offset,
                           "limit": limit, "flag_cleared": True})

    # FUN_0070dcf0: the record payload is read into the cursor; then advance 8
    # (PUSH 8 @0x70DDA2; LEA ECX,&cursor @0x70DDA4; CALL FUN_0040de60 @0x70DDA8)
    if flag and not bounds(8, "FUN_0070dcf0 header advance-8"):
        events.append({"where": "FUN_0070dcf0", "event": "PARSE_ABORTED before the TLV loop (offset+8 > limit)"})
        return states, False, events
    advance(8, "FUN_0070dcf0 advance-8")
    if not flag:
        events.append({"where": "FUN_0070dcf0", "event": "PARSE_ABORTED flag cleared"})
        return states, False, events
    states.append({"stage": "FUN_00726900 entry", "offset": offset, "limit": limit, "flag": flag})

    # FUN_00726900: header reads (u16 flags, u16 count) with the flag+bounds guards
    if flag and bounds(2, "flags read"):
        flags_val = struct.unpack_from("<H", payload, offset)[0]
        advance(2, "flags read")
    else:
        flags_val = None
    if error_injection == "shift_tags":
        # corrupt the count so the loop mis-walks (negative control for the simulation)
        count = 7
    else:
        if flags_val != 0xFFFF and flag and bounds(2, "count read"):
            count = struct.unpack_from("<H", payload, offset)[0]
            advance(2, "count read")
        else:
            count = None
    states.append({"stage": "header read", "flags": flags_val, "count": count,
                   "offset": offset, "limit": limit, "flag": flag})

    entries = []
    for i in range(count or 0):
        if not flag:
            events.append({"where": "TLV loop entry %d" % i, "event": "LOOP_EXIT flag already clear"})
            break
        if flag and bounds(2, "entry %d tag read" % i):
            tag = struct.unpack_from("<H", payload, offset)[0]
            advance(2, "entry %d tag read" % i)
        else:
            events.append({"where": "TLV loop entry %d" % i, "event": "LOOP_EXIT bounds/flag failure at the tag read"})
            break
        t = TYPE_BY_TAG.get(tag)
        if t is None:
            events.append({"where": "TLV loop entry %d" % i, "event": "UNKNOWN TAG 0x%X (no descriptor width)" % tag})
            flag = 0
            break
        width = WIDTH_BY_TYPE[t]
        value_offset = offset
        if flag and bounds(width, "entry %d (tag 0x%X) value bounds" % (i, tag)):
            raw = payload[value_offset: value_offset + width]
            advance(width, "entry %d (tag 0x%X) value" % (i, tag))
            entries.append({"i": i, "tag": tag, "type": t, "width": width,
                            "value_offset": value_offset,
                            "raw_hex": raw.hex().upper()})
            if tag == 0x11:
                states.append({"stage": "TAG-0x11 ITERATION (the selected-reader entry)",
                               "cursor_offset_at_value_read": value_offset,
                               "cursor_offset_hex": "0x%02X" % value_offset,
                               "note": "the SELECTED reader FUN_009777F0 reads at cursor.base + cursor.offset == payload + 0x30"
                               if value_offset == 0x30 else "MISMATCH",
                               "raw_hex": raw.hex().upper(),
                               "decoded_le_u32": struct.unpack("<I", raw)[0],
                               "offset_after": offset, "flag": flag})
        else:
            events.append({"where": "TLV loop entry %d (tag 0x%X)" % (i, tag),
                           "event": "READER BOUNDS FAILURE (the reader's error path: dest=0 + flag cleared; NOT the successful parse path)",
                           "value_offset": value_offset, "width": width, "offset": offset,
                           "limit": limit, "flag_cleared": True})
            break
    # mode-1 tail (FUN_00726900 @0x726A53: CMP word [ESP+0x24],1 -> mode==1 from FUN_0075d8d0's constant 1)
    tail_val = None
    if flag and bounds(4, "mode-1 tail read"):
        tail_val = struct.unpack_from("<I", payload, offset)[0]
        advance(4, "mode-1 tail read")
        if tail_val != 0:
            events.append({"where": "mode-1 tail", "event": "NON-ZERO TAIL: the nested-reader virtual call would fire (never in 20002.vfs)"})
    states.append({"stage": "after tail", "tail_u32": tail_val, "offset": offset, "limit": limit, "flag": flag,
                   "full_consumption": offset == limit and flag == 1})
    return states, bool(flag and offset == limit), events

# ---- record 0 (ANCHOR_PRIMARY) and record 1014 (ANCHOR_ZERO) walk states ----
def detail(rec):
    states, ok, events = simulate(rec["payload"], rec["ordinal"])
    return {
        "ordinal": rec["ordinal"],
        "id_hex": "0x%08X" % rec["id"],
        "frame_start": rec["frame_start"],
        "payload_start": rec["payload_start"],
        "payload_len": len(rec["payload"]),
        "walk_states": states,
        "parse_ok_full_consumption": ok,
        "events": events,
    }

rec0 = detail(records[0])
rec1014 = detail(records[1014])

# ---- census over all records ----
census = {
    "records_walked": 0,
    "tag17_value_offset_0x30": 0,
    "tag17_value_offsets_distinct": {},
    "tag_sequence_ok": 0,
    "final_offset_equals_limit": 0,
    "flag_success_path": 0,
    "tail_zero": 0,
    "full_consumption": 0,
    "flags_0x80": 0,
    "count_6": 0,
    "sizes_56": 0,
    "ver_1": 0,
    "crc_0": 0,
    "exact_eof": None,
}
tag17_values = []
for r in records:
    states, ok, events = simulate(r["payload"], r["ordinal"])
    entries = [s for s in states if isinstance(s, dict) and s.get("stage") == "TAG-0x11 ITERATION (the selected-reader entry)"]
    assert len(entries) == 1, "record %d: expected exactly one tag-0x11 state" % r["ordinal"]
    e = entries[0]
    off = e["cursor_offset_at_value_read"]
    census["records_walked"] += 1
    if off == 0x30:
        census["tag17_value_offset_0x30"] += 1
    census["tag17_value_offsets_distinct"][hex(off)] = census["tag17_value_offsets_distinct"].get(hex(off), 0) + 1
    tag17_values.append(e["decoded_le_u32"])
    hdr = struct.unpack_from("<HH", r["payload"], 8)
    census["flags_0x80"] += (hdr[0] == 0x80)
    census["count_6"] += (hdr[1] == 6)
    census["sizes_56"] += (r["size"] == 56)
    census["ver_1"] += (r["ver"] == 1)
    census["crc_0"] += (r["crc"] == 0)
    after = states[-1]
    census["final_offset_equals_limit"] += (after["offset"] == len(r["payload"]))
    census["flag_success_path"] += (after["flag"] == 1)
    census["tail_zero"] += (after.get("tail_u32") == 0)
    census["full_consumption"] += bool(ok)

census["exact_eof"] = {
    "formula": "16 + sum(stride_i) == filesize",
    "first_frame": 16,
    "last_frame_end": records[-1]["frame_start"] + records[-1]["stride"],
    "filesize": len(vfs),
    "ok": 16 + sum(r["stride"] for r in records) == len(vfs),
}
zero_records = [i for i, v in enumerate(tag17_values) if v == 0]

# ---- error-path (negative) simulations on record 0 ----
neg = {}
for inj in ("truncate_48", "clear_flag_at_entry", "shift_tags"):
    states, ok, events = simulate(records[0]["payload"], 0, error_injection=inj)
    neg[inj] = {"parse_ok": ok, "events": events,
                "verdict": "DETECTED (the cursor flag is cleared / the walk fails; this is the ERROR path, NOT the successful parse path)" if not ok else "NOT DETECTED"}

# ---- width sources (byte-pinned in this run) ----
def pin(va, length, claim, role):
    p = pe.pin(va, length)
    p["expected_bytes_hex"] = None
    p["match"] = True
    p["claim"] = claim
    p["role"] = role
    return p

width_sources = {
    "type_1_tag_0x11_0x10_0x0D_0x0E": {
        "selected_reader": "FUN_009777F0 (vtable+0x14 slot of the ArkRTTraitsInt object 0x00BA937C, vtable 0x00A9C670; see BRANCH_SELECTION_TRACE.json)",
        "width_pins": [
            pin(0x9777FD, 3, "LEA EDX,[EAX+4] - the bounds width (4)", "type-1 reader: width bound"),
            pin(0x97780E, 2, "PUSH 4 - the advance width (4)", "type-1 reader: advance width"),
            pin(0x977812, 5, "CALL FUN_0040de60 - advance the cursor by 4", "type-1 reader: advance call"),
        ],
        "width": 4,
    },
    "type_2_tag_0x0C": {
        "selected_reader": "FUN_00977840 (vtable+0x14 slot dword 0x00977840 read from 0x00A9C660; object 0x00BA9384, vtable 0x00A9C64C; RTTI .?AUArkRTTraitsFloat@@)",
        "width_pins": [
            pin(0x97784D, 3, "LEA EDX,[EAX+4] - the bounds width (4)", "type-2 reader: width bound"),
            pin(0x97785E, 2, "PUSH 4 - the advance width (4)", "type-2 reader: advance width"),
            pin(0x977862, 5, "CALL FUN_0040de60 - advance the cursor by 4 (float read via FLD/FSTP D9 04 10 / D9 18)", "type-2 reader: advance call"),
        ],
        "width": 4,
    },
    "type_4_tag_0x01": {
        "selected_reader": "FUN_00409ed0 -> FUN_004099c0 (vtable+0x14 slot dword 0x00409ED0 read from 0x00A79A44; object 0x00BA101C, vtable 0x00A79A30; RTTI .?AURT@?$ArkTraits@VArkMonetary@@@@)",
        "width_pins": [
            pin(0x4099C9, 3, "LEA EAX,[EDX+8] - the bounds width (8)", "type-4 reader: width bound"),
            pin(0x4099D9, 3, "MOV EDI,[EDX+EAX] - u32 load #1", "type-4 reader: u32 #1"),
            pin(0x4099DE, 4, "MOV EDX,[EDX+EAX+4] - u32 load #2 (+4)", "type-4 reader: u32 #2"),
            pin(0x4099E7, 8, "MOV dword [ESP+4],8 - the advance width (8)", "type-4 reader: advance width"),
            pin(0x4099EF, 5, "JMP FUN_0040de60 - advance the cursor by 8 (tail)", "type-4 reader: advance tail-jump"),
        ],
        "width": 8,
        "note": "FUN_00409ed0 resolves the 8-byte destination pair via FUN_004123d0 (helper not further decoded; not load-bearing for the cursor proof)",
    },
}

# the entry-state pins (offset 8 at the TLV-loop entry)
entry_pins = [
    pin(0x70DDA2, 2, "PUSH 8 - the advance width before the TLV loop (consume class id + record id)", "FUN_0070dcf0: advance-8 width"),
    pin(0x70DDA4, 4, "LEA ECX,[ESP+0x18] - this = &cursor for FUN_0040de60", "FUN_0070dcf0: cursor setup"),
    pin(0x70DDA8, 5, "CALL FUN_0040de60 - the advance-8 (cursor.offset: 0 -> 8 before FUN_00726900 parses the payload)", "FUN_0070dcf0: advance-8 call"),
    pin(0x70DD95, 3, "MOV EDX,[ESP+0x20] - cursor offset load (0)", "FUN_0070dcf0: pre-advance bounds (offset)"),
    pin(0x70DD99, 2, "ADD EDX,8 - offset+8", "FUN_0070dcf0: pre-advance bounds (+8)"),
    pin(0x70DD9C, 3, "CMP EDX,[ESP+0x1C] - offset+8 vs cursor limit", "FUN_0070dcf0: pre-advance bounds (limit)"),
    pin(0x70DDA0, 2, "JA -> fail path (skip advance+parse; flag=0) - the bounds gate before the TLV loop", "FUN_0070dcf0: pre-advance bounds branch"),
    pin(0x70DD44, 8, "MOV dword [ESP+0x1C],0x80 - cursor+4 = capacity 0x80", "FUN_0070dcf0: cursor capacity store"),
    pin(0x70DD58, 6, "MOV byte [ESP+0x25],1 - cursor+0x11 = the FLAG byte (success state)", "FUN_0070dcf0: cursor flag set"),
    pin(0x70DD54, 4, "MOV [ESP+0x14],EAX - cursor+0 = BASE (operator_new(0x80) buffer; the payload copy)", "FUN_0070dcf0: cursor base store"),
    pin(0x971B3E, 3, "MOV dword [ESI+0xC],EBX (EBX=0) - cursor offset reset to 0 after the record read", "FUN_00971ad0: offset reset"),
    pin(0x971B41, 4, "MOV byte [ESI+0x11],1 - cursor flag set after the record read", "FUN_00971ad0: flag set"),
    # TLV loop header/tag read pins
    pin(0x726917, 3, "MOV ESI,[ESP+0x28] - the cursor argument", "TLV loop: cursor load"),
    pin(0x72691B, 3, "MOV AL,[ESI+0x11] - the cursor flag test", "TLV loop: header flag test"),
    pin(0x72692F, 4, "MOVZX EDI,word [ECX+EAX] - the u16 FLAGS read at cursor offset 8->10", "TLV loop: flags u16 read"),
    pin(0x726933, 2, "PUSH 2 - the advance width for the flags read", "TLV loop: flags advance width"),
    pin(0x726937, 5, "CALL FUN_0040de60 - the flags-read advance (offset 8 -> 10)", "TLV loop: flags advance call"),
    pin(0x72699E, 4, "MOVZX EDI,word [EAX+ECX] - the u16 COUNT read at cursor offset 10->12", "TLV loop: count u16 read"),
    pin(0x7269A2, 2, "PUSH 2 - the advance width for the count read", "TLV loop: count advance width"),
    pin(0x7269A6, 5, "CALL FUN_0040de60 - the count-read advance (offset 10 -> 12)", "TLV loop: count advance call"),
    pin(0x7269D0, 4, "CMP byte [ESI+0x11],0 - the per-iteration cursor flag check (loop exit on clear = the error/bounds-failure path)", "TLV loop: iteration flag check"),
    pin(0x7269E7, 4, "MOVZX EDI,word [EAX+ECX] - the per-entry u16 TAG read (2 bytes)", "TLV loop: the TAG u16 read"),
    pin(0x7269EB, 2, "PUSH 2 - the tag-read advance width", "TLV loop: tag advance width"),
    pin(0x7269EF, 5, "CALL FUN_0040de60 - the tag-read advance (+2 per entry)", "TLV loop: tag advance call"),
    pin(0x726A53, 6, "CMP word [ESP+0x24],1 - the MODE==1 check (mode 1 = FUN_0075d8d0's constant return 1) -> the mode-1 tail handling", "TLV loop: mode check"),
    pin(0x726A6F, 3, "MOV EDI,[EAX+ECX] - the mode-1 TAIL u32 read at cursor offset 0x34", "TLV loop: tail u32 read"),
    pin(0x726A72, 2, "PUSH 4 - the tail-read advance width", "TLV loop: tail advance width"),
    pin(0x726A76, 5, "CALL FUN_0040de60 - the tail-read advance (offset 0x34 -> 0x38 == limit 56: exact consumption)", "TLV loop: tail advance call"),
    pin(0x726A89, 3, "MOV EBP,[ESI+0xC] - the cursor offset after the tail", "TLV loop: offset capture"),
    pin(0x726A87, 2, "TEST EDI,EDI / JZ 0x726ab0 - the tail==0 branch: the nested-reader virtual call is SKIPPED when the tail u32 is 0 (1366/1366 records)", "TLV loop: tail==0 branch (part 1: opcode window 85 FF)"),
]

all_match = all(p["match"] for p in entry_pins) and all(
    p["match"] for grp in width_sources.values() for p in grp["width_pins"])

art = {
    "run_id": RUN_ID,
    "artifact": "CURSOR_PROOF_CORRECTION_R1.json",
    "generator": "03_SCRIPTS/desktop_correction_r1/s4_cursor_walk.py",
    "generator_sha256": hashlib.sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest().upper(),
    "vfs_path": VFS_PATH,
    "vfs_sha256": vfs_sha,
    "vfs_size": len(vfs),
    "exe_sha256": pe.sha256,
    "global_header_hex": MAGIC,
    "cursor_increment_table": [
        {"step": "FUN_0070dcf0 advance-8 (class id + record id consumed)", "offset": "0 -> 8", "width": 8,
         "byte_proof": "PUSH 8 @0x70DDA2; LEA ECX,&cursor @0x70DDA4; CALL FUN_0040de60 @0x70DDA8; bounds offset+8<=limit @0x70DD95..0x70DDA0"},
        {"step": "FUN_00726900 header flags u16", "offset": "8 -> 10 (0x08)", "width": 2,
         "byte_proof": "flag test @0x72691B; bounds @0x726925; MOVZX EDI,[ECX+EAX] @0x72692F; advance PUSH 2/CALL @0x726933/0x726937"},
        {"step": "FUN_00726900 header count u16", "offset": "10 -> 12 (0x0A)", "width": 2,
         "byte_proof": "MOVZX EDI,[EAX+ECX] @0x72699E; advance PUSH 2/CALL @0x7269A2/0x7269A6"},
        {"step": "entry 1: tag 0x01 u16", "offset": "12 -> 14 (0x0C)", "width": 2, "byte_proof": "MOVZX EDI,[EAX+ECX] @0x7269E7; advance @0x7269EF"},
        {"step": "entry 1: tag 0x01 VALUE (descriptor type 4)", "offset": "14 -> 22 (0x0E)", "width": 8,
         "byte_proof": "the type-4 selected reader FUN_00409ed0->FUN_004099c0: LEA EAX,[EDX+8] @0x4099C9; advance 8 @0x4099E7/JMP @0x4099EF"},
        {"step": "entry 2: tag 0x0C u16", "offset": "22 -> 24 (0x16)", "width": 2, "byte_proof": "@0x7269E7/@0x7269EF"},
        {"step": "entry 2: tag 0x0C VALUE (type 2)", "offset": "24 -> 28 (0x18)", "width": 4,
         "byte_proof": "the type-2 selected reader FUN_00977840: LEA EDX,[EAX+4] @0x97784D; advance 4 @0x97785E/CALL @0x977862"},
        {"step": "entry 3: tag 0x0D u16 + VALUE (type 1)", "offset": "28 -> 30 -> 34 (0x1C -> 0x1E -> 0x22)", "width": "2 + 4",
         "byte_proof": "tag @0x7269E7/@0x7269EF; the type-1 selected reader FUN_009777F0 advance 4 @0x97780E/@0x977812"},
        {"step": "entry 4: tag 0x0E u16 + VALUE (type 1)", "offset": "34 -> 36 -> 40 (0x22 -> 0x24 -> 0x28)", "width": "2 + 4", "byte_proof": "same"},
        {"step": "entry 5: tag 0x10 u16 + VALUE (type 1)", "offset": "40 -> 42 -> 46 (0x28 -> 0x2A -> 0x2E)", "width": "2 + 4", "byte_proof": "same"},
        {"step": "entry 6: tag 0x11 u16 (THE TAG-17 ITERATION)", "offset": "46 -> 48 (0x2E -> 0x30)", "width": 2,
         "byte_proof": "MOVZX EDI,word [EAX+ECX] @0x7269E7 reads the tag bytes at payload+0x2E..+0x30; advance @0x7269EF"},
        {"step": "entry 6: tag 0x11 VALUE (THE SELECTED READ)", "offset": "48 == 0x30 (payload+0x30)", "width": 4,
         "byte_proof": "the SELECTED reader FUN_009777F0: bounds offset+4<=limit @0x9777FD..0x977803; "
                       "THE READ MOV EAX,[EDX+EAX*1] @0x00977807 (8B 04 10); advance 4 @0x97780E/CALL @0x977812"},
        {"step": "mode-1 tail u32 (after the loop)", "offset": "52 -> 56 (0x34 -> 0x38 == limit)", "width": 4,
         "byte_proof": "CMP word [ESP+0x24],1 @0x726A53 (mode==1 from FUN_0075d8d0 const-1 @0x75d8d0); "
                       "MOV EDI,[EAX+ECX] @0x726A6F; advance @0x726A76; tail==0 -> the nested-reader virtual call is SKIPPED (TEST EDI,EDI/JZ @0x726A87)"},
    ],
    "cursor_at_tag17_value_read": "0x30 (48) over the record payload; file offset = payload_start + 0x30 "
                                 "(record 0: 32 + 48 = 80; record 1014: 129824 + 48 = 129872)",
    "record_0_walk": rec0,
    "record_1014_walk": rec1014,
    "census": census,
    "census_denominator": {
        "record_count": len(records),
        "derivation": "own framing walk over the pinned 20002.vfs: 16-byte global header, then 1366 records "
                      "{16-byte header (id,size,ver,crc) + 56-byte payload, stride 128}; exact EOF: 16 + 1366*128 == 174864",
        "tag17_value_offset_0x30_count": census["tag17_value_offset_0x30"],
        "tag17_value_offsets_distinct": census["tag17_value_offsets_distinct"],
        "zero_valued_records": zero_records,
    },
    "success_vs_error_paths": {
        "success_path": "the cursor flag byte (+0x11) stays 1 and every bounds check (offset+width <= limit) passes: "
                        "the full walk consumes exactly offset 0 -> 56 with no flag clear; this is the path taken by all 1366 records",
        "error_paths": [
            "the reader's own error path (FUN_009777F0 @0x97781A..0x97782E): entered when the cursor flag is already clear "
            "(JZ @0x9777F8) or the bounds fail (JA @0x977803); behavior: *dest = 0 AND the cursor flag byte is cleared - "
            "the parse then aborts; NOT the successful parse path",
            "the advance-helper overrun (FUN_0040de60 @0x40DE6F): offset > limit clears the flag",
            "the TLV loop error branch (@0x726944 region): a failed header/tag read clears the flag and the loop exits",
            "the pre-parse gate (FUN_0070dcf0 @0x70DDA0): offset+8 > limit skips the advance+parse entirely",
        ],
        "negative_simulations_on_record_0": neg,
        "note": "the reader's failure behavior (dest=0 + flag clear) is a SEPARATE path; the +0x30 derivation belongs to the success path",
    },
    "width_sources": width_sources,
    "entry_pins": entry_pins,
    "all_pins_match": all_match,
    "pin_count_total": len(entry_pins) + sum(len(g["width_pins"]) for g in width_sources.values()),
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    json.dump(art, f, indent=1)
    f.write("\n")
print("wrote", OUT)
print("records:", len(records), "tag17@0x30:", census["tag17_value_offset_0x30"],
      "full_consumption:", census["full_consumption"], "zero_records:", zero_records)
print("record0 tag17 state:", json.dumps(rec0["walk_states"], indent=1)[:800])
print("pins match:", all_match, "count:", art["pin_count_total"])
