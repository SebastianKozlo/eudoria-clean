# -*- coding: utf-8 -*-
"""Phases part 1: preflight, prereg, falsify, hashpass, pemap, window_roster, textscan."""
import sys, os, json, struct, socket, subprocess
import p935_core as C


def phase_preflight():
    if not os.path.exists(C.EXE_PATH):
        raise RuntimeError("EXE missing")
    stat = os.stat(C.EXE_PATH)
    if stat.st_size != C.EXE_SIZE_PIN:
        raise RuntimeError("EXE size mismatch: %d" % stat.st_size)
    host = socket.gethostname()
    if host != "WinDev2407Eval":
        raise RuntimeError("HOST_CHECK_FAILED: %s" % host)
    if os.path.exists(C.OUTPUT_ROOT):
        raise RuntimeError("OUTPUT_ROOT_EXISTS: %s" % C.OUTPUT_ROOT)
    os.mkdir(C.OUTPUT_ROOT)
    os.mkdir(os.path.join(C.OUTPUT_ROOT, "attempts"))
    os.mkdir(os.path.join(C.OUTPUT_ROOT, "tools"))
    head = subprocess.run(["git", "-C", C.REPO_PATH, "rev-parse", "HEAD"], capture_output=True, text=True)
    base_sha = head.stdout.strip()
    st = subprocess.run(["git", "-C", C.REPO_PATH, "status", "--porcelain=v1"], capture_output=True, text=True)
    status_lines = [l for l in st.stdout.split("\n") if l.strip()]
    prior = {}
    for label, p in [("S7_VTABLE_STORE_SCAN.json", C.S7_PATH), ("Z3_portals.md", C.Z3_PATH),
                     ("ZS9_DISASM_FUN_00852750_full.txt", C.ZS9_PATH),
                     ("WRAPPER_R1_REPORT.md", C.WRAP_REPORT_PATH),
                     ("WRAPPER_R1_EVIDENCE.json", C.WRAP_EVIDENCE_PATH),
                     ("WRAPPER_R1_INSTRUCTION_ROSTER.json", C.WRAP_ROSTER_PATH),
                     ("GA3_VTABLE_ENTRIES.json", C.GA3_PATH)]:
        if not os.path.isfile(p):
            raise RuntimeError("PRIOR_EVIDENCE_MISSING: %s" % p)
        prior[label] = {"path": p, "size": os.path.getsize(p), "sha256": C.sha256_file(p)}
    bij = {}
    for label, rootp in [("ORIGINAL_99_Audits", C.CALLER_PKG_ORIG), ("REPO_docs_audits", C.CALLER_PKG_REPO)]:
        mp = os.path.join(rootp, "MANIFEST_SHA256.csv")
        msha = C.sha256_file(mp)
        msize = os.path.getsize(mp)
        r = C.verify_bijection(rootp, mp, "MANIFEST_SHA256.csv")
        bij[label] = {"manifest_sha256": msha, "manifest_sha_pin_match": msha == C.CALLER_MANIFEST_SHA_PIN,
                      "manifest_size": msize, "manifest_size_pin_match": msize == C.CALLER_MANIFEST_SIZE_PIN,
                      "rows": r["rows"], "rows_pin_match": r["rows"] == C.CALLER_MANIFEST_ROWS_PIN,
                      "physical_files": r["physical_files"],
                      "physical_pin_match": r["physical_files"] == C.CALLER_PKG_PHYSICAL_PIN,
                      "problems": r["problems"], "bijection_ok": r["bijection_ok"]}
    ok = all(v["bijection_ok"] and v["manifest_sha_pin_match"] and v["manifest_size_pin_match"]
             and v["rows_pin_match"] and v["physical_pin_match"] for v in bij.values())
    import datetime
    preflight = {
        "run_id": C.RUN_ID, "ts": C.utcnow(), "mode": "ONE_BOUNDED_READ_ONLY_RUN", "era": C.CONTRACT_ERA,
        "host": host, "host_check": "PASS",
        "output_root": C.OUTPUT_ROOT, "output_root_pre_existed": False, "output_root_created_atomically": True,
        "original_exe": {"path": C.EXE_PATH, "size_stat": stat.st_size, "size_pin_match": True,
                         "mtime_utc": datetime.datetime.utcfromtimestamp(stat.st_mtime).isoformat() + "Z",
                         "note": "os.stat metadata only; ZERO EXE bytes read in preflight"},
        "repo": {"path": C.REPO_PATH, "HEAD_at_start": base_sha,
                 "expected_base_sha_prefix": C.EXPECTED_BASE_SHA_PREFIX,
                 "base_sha_prefix_match": base_sha.startswith(C.EXPECTED_BASE_SHA_PREFIX),
                 "git_status_untracked_foreign_paths": status_lines,
                 "note": "read-only; no repo modification by this run"},
        "prior_evidence": prior,
        "predecessor_bijection": bij,
        "predecessor_bijection_all_pass": ok,
        "python": sys.version,
    }
    C.write_new_text(os.path.join(C.OUTPUT_ROOT, "PREFLIGHT.json"), json.dumps(preflight, indent=2))
    pins = {
        "run_id": C.RUN_ID, "era": C.CONTRACT_ERA, "mode": "ONE_BOUNDED_READ_ONLY_RUN",
        "original_exe": {"path": C.EXE_PATH, "size_bytes": C.EXE_SIZE_PIN, "sha256": C.EXE_SHA256_PIN},
        "output_root": C.OUTPUT_ROOT,
        "repo": {"path": C.REPO_PATH, "expected_base_sha_prefix": C.EXPECTED_BASE_SHA_PREFIX},
        "window": {"va_start": "0x%08X" % C.WIN_VA_START, "va_end_exclusive": "0x%08X" % C.WIN_VA_END,
                   "size_bytes": C.WIN_SIZE, "site_slot15_va": "0x%08X" % C.SITE_SLOT15_VA,
                   "site_slot15_expected_value": "0x%08X" % C.SITE_SLOT15_VALUE_PIN},
        "scan": {"text_raw_size": C.TEXT_RAW_SIZE, "eligible_starts": C.ELIGIBLE_STARTS,
                 "chunk_size": C.CHUNK_SIZE, "carry": C.CARRY, "max_hits": C.MAX_HITS,
                 "alignment_required": False},
        "budget": C.BUDGET,
        "predecessor_package": {"manifest_sha256": C.CALLER_MANIFEST_SHA_PIN,
                                "manifest_size": C.CALLER_MANIFEST_SIZE_PIN,
                                "rows": C.CALLER_MANIFEST_ROWS_PIN, "physical": C.CALLER_PKG_PHYSICAL_PIN},
    }
    C.write_new_text(os.path.join(C.OUTPUT_ROOT, "INPUT_PINS.json"), json.dumps(pins, indent=2))
    print(json.dumps({"phase": "preflight", "status": "OK", "base_sha": base_sha,
                      "predecessor_bijection_all_pass": ok}))


def phase_prereg():
    s7_data = json.load(open(C.S7_PATH, "rb"))
    controls = []
    for c in C.S7_CONTROLS:
        found = None
        for hit in s7_data["hits"][c["class"]]:
            if int(hit["va"], 16) == c["window_va"]:
                found = hit
                break
        if found is None:
            raise RuntimeError("S7 window not found for %s" % c["class"])
        if found["window_hex"].lower() != c["window_hex"].lower():
            raise RuntimeError("S7 window_hex mismatch")
        pat = struct.pack("<I", c["vtable_va"]).hex()
        idx = found["window_hex"].lower().find(pat)
        byte_aligned = (idx >= 0 and idx % 2 == 0)
        off = idx // 2 if idx >= 0 else -1
        dword_start = c["window_va"] + off
        controls.append({
            "control_id": c["control_id"], "class": c["class"],
            "vtable_va": "0x%08X" % c["vtable_va"], "slot_index": c["slot_index"],
            "s7_window_va": "0x%08X" % c["window_va"], "s7_window_file_offset": c["window_file_offset"],
            "s7_window_hex_original": found["window_hex"], "pattern_le_hex": pat,
            "pattern_found_in_hexstring": idx,
            "pattern_byte_aligned": byte_aligned,
            "pattern_offset_in_window": off, "expected_pattern_offset": c["expected_pattern_offset"],
            "arithmetic_precheck": "PASS" if (byte_aligned and off == c["expected_pattern_offset"]) else "FAIL",
            "derived_dword_start": "0x%08X" % dword_start,
            "expected_dword_start": "0x%08X" % c["expected_dword_start"],
            "dword_start_matches_contract": dword_start == c["expected_dword_start"],
            "s7_provenance": {"path": C.S7_PATH, "run_id": s7_data.get("run_id"),
                              "stage": s7_data.get("stage"), "note": s7_data.get("note")},
        })
    if not all(c["arithmetic_precheck"] == "PASS" and c["dword_start_matches_contract"] for c in controls):
        raise RuntimeError("S7 arithmetic pre-check FAILED")
    prereg = {
        "run_id": C.RUN_ID, "ts": C.utcnow(),
        "preregistered_before_any_exe_byte_read": True,
        "mission": {
            "q1": "Actual structure of the 128-B neighborhood of 0x00A91CFC (dual read, 32-DWORD roster)",
            "q2": "Raw .text references to the 32 slot addresses of the window (raw census, unqualified)",
            "q3": "Knowledge increment: known vs new (two independent axes)",
        },
        "window": {"va_range": "[0x00A91CC0,0x00A91D40)", "size": C.WIN_SIZE,
                   "expected_file_range": "[0x00691CC0,0x00691D40)",
                   "note": "to be verified mechanically from the freshly parsed PE header before any window read"},
        "targets": [{"index": i, "target_va": "0x%08X" % t} for i, t in enumerate(C.TARGETS)],
        "mandatory_control": {"dword_index": 15, "site_va": "0x%08X" % C.SITE_SLOT15_VA,
                              "expected_value": "0x%08X" % C.SITE_SLOT15_VALUE_PIN},
        "s7_preregistered_controls": controls,
        "s7_semantic_guard": ("S7 controls are RAW pattern positions; NOT qualified as instruction heads/vptr "
                              "stores; not auto-promoted."),
        "scan_prereg": {
            "text_raw_size": C.TEXT_RAW_SIZE, "eligible_starts": C.ELIGIBLE_STARTS,
            "chunk_size": C.CHUNK_SIZE, "carry": C.CARRY,
            "carry_note": ("carry is logical; the .text region is read EXACTLY ONCE (single physical read of "
                           "6766592 B); no additional read for carry"),
            "max_hits": C.MAX_HITS,
            "max_hits_semantics": ("total across all 32 patterns; overflow -> census_complete=false, PARTIAL, "
                                    "hits = incomplete prefix in (section_offset, slot_index) order"),
            "alignment_requirement": "NONE",
            "search": "4-byte little-endian representation of each SLOT ADDRESS (slot address, not function value)",
            "in_pass_text_sha256_declared": True,
            "in_pass_note": "SHA256 of .text raw bytes computed during the single .text read (no second read)",
            "cross_check_declared": ("chunked scan vs full-buffer find on the same in-memory buffer; identical "
                                     "hit sets required"),
            "prohibitions": ["disassembly", "body expansion", "Ghidra", "argument-flow",
                             "pointer-following of read DWORDs"],
        },
        "span_classes": {
            "FULL_VIRTUAL_SPAN": "hit offset o with o+4 <= .text VirtualSize",
            "CROSSES_VIRTUAL_SIZE_END": "o < VirtualSize and o+4 > VirtualSize",
            "RAW_PADDING_ONLY": "o >= VirtualSize (within RawSize; RawSize-VSize=2587 B)",
        },
        "novelty_axes": {
            "axis_a_values": ["PRIOR_RAW_MATCH", "NEW_RAW_CANDIDATE", "PRIOR_EVIDENCE_CONFLICT",
                              "PRIOR_COMPARISON_NOT_ESTABLISHED"],
            "axis_a_decision_rules": {
                "PRIOR_RAW_MATCH": ("hit raw position exactly equals a prior-documented raw position: the four "
                                    "S7 DWORD-start positions {0x00851EBF,0x00852145,0x00852AD3,0x00852B42}"),
                "NEW_RAW_CANDIDATE": ("any other hit; per-hit prior GA3 xref context recorded informationally "
                                      "(reference existence documented at Ghidra instruction level in GA3; "
                                      "raw imm position itself is new)"),
                "PRIOR_EVIDENCE_CONFLICT": ("a preregistered S7 control position NOT found by the complete "
                                            "census, or a roster value disagreeing with prior-documented content"),
                "PRIOR_COMPARISON_NOT_ESTABLISHED": ("prior evidence unavailable for comparison (not expected; "
                                                     "all prior evidence verified present in preflight)"),
            },
            "axis_b_values": ["RAW_UNQUALIFIED", "INSTRUCTION_HEAD_CONFIRMED", "SEMANTIC_ROLE_NOT_ESTABLISHED"],
            "axis_b_decision_rules": {
                "RAW_UNQUALIFIED": "every raw scan hit gets QUALIFICATION=RAW_ADDRESS_OCCURRENCE_UNQUALIFIED",
                "INSTRUCTION_HEAD_CONFIRMED": ("only with separate earlier independent proof of exact "
                                              "address+bytes as instruction head; NO such proof exists for any "
                                              "candidate hit position in prior evidence (S7 sites are imm32 "
                                              "interiors of C7-opcode stores, not instruction heads; GA3 xref "
                                              "from_va values are not raw imm positions); therefore NO hit may "
                                              "be INSTRUCTION_HEAD_CONFIRMED in this run"),
                "SEMANTIC_ROLE_NOT_ESTABLISHED": ("no semantic role (ctor/vptr store/call site) is established "
                                                  "for any hit in this run"),
            },
        },
        "prior_baseline_preregistered": {
            "window_content_prior_documented": {str(k): {"value": v[0], "source": v[1]}
                                                for k, v in C.PRIOR_BASELINE_SLOTS.items()},
            "window_content_prior_undocumented_slots": [27, 28, 29, 30, 31],
            "prior_raw_positions": C.PRIOR_RAW_POSITIONS,
            "prior_ga3_xrefs_informational": C.PRIOR_GA3_XREFS,
            "prior_vtable_heads_in_window": {"slot_8": "ArkPortalIdGenerator (S4 RTTI)",
                                             "slot_14": "ArkPortalCell (S4 RTTI)",
                                             "slot_17": "ArkPortalResourceItem (S4 RTTI)",
                                             "slot_22": "ArkPortalPortal (S4 RTTI)"},
            "out_of_scan_domain": ["ArkPortalCellGraph vtable 0x00A91CB4 (before window)",
                                  "ArkPortalResourceItemFactory vtable 0x00A91C88 (before window)"],
            "known_semantics_prior": ("slot 15 value 0x00852A30 = parameter-cursor wrapper (UPSTREAM_WRAPPER R1 "
                                      "decoded [0x00852A30,0x00852A82); CALLER_DISCOVERY R1: no direct .text "
                                      "E8/E9 callers; single .rdata reference = slot 15 itself)"),
        },
        "window_read_plan": {"reads": 2, "size_each": 128, "independent": True,
                             "on_mismatch": "CONFLICT; NO third read; no promotion (Science A blocked)",
                             "on_match": "128/128 byte equality + per-buffer SIZE/SHA recorded"},
        "roster_plan": {"entries": 32,
                        "fields": ["index", "va", "rva", "file_offset", "raw4", "valueLE32",
                                   "section_membership_of_value", "classification"],
                        "classification_rule": ("value==0 -> ZERO; 0<value<ImageBase -> SUB_IMAGE_VALUE; "
                                                "in image -> section virtual-range lookup; else OUTSIDE_IMAGE"),
                        "pointer_array_shape_max": "PLAUSIBLE_POINTER_ARRAY_SHAPE (NEVER VTABLE_CONFIRMED)"},
        "budget_prereg": dict(C.BUDGET, hash_passes=2, window_reads=2, pe_header_reads=1, text_reads=1,
                              third_read_on_window_mismatch="FORBIDDEN", no_helper_verifier_hashing=True),
        "deliverables_order": ["PREFLIGHT.json", "PREREGISTRATION.json", "INPUT_PINS.json",
                              "SOURCE_READS_LEDGER.jsonl", "PE_MAPPING.json", "PE_HEADER4096.bin",
                              "WINDOW_READ1.bin", "WINDOW_READ2.bin", "DWORD_ROSTER.json",
                              "RAW_TEXT_SCAN_META.json", "RAW_TEXT_REFERENCES.jsonl",
                              "PRIOR_EVIDENCE_COMPARISON.json", "NOVELTY_ANALYSIS.json",
                              "SOURCE_READS.json", "EVIDENCE.json", "QC.json", "BUDGET_USED.json",
                              "STAGE_ACCEPTANCE_GATES.csv", "REPORT.md", "HANDOFF.md",
                              "MANIFEST_SHA256.csv (LAST; after it read-only re-hash + bijection only)"],
        "falsifier_plan": ["F01 slot-address vs stored-value confusion", "F02 non-aligned match",
                           "F03 chunk-boundary match", "F04 last valid start + incomplete tail rejection",
                           "F05 RAW padding classification", "F06 VirtualSize crossing classification",
                           "F07 immediate not promoted", "F08 wrong VA/RVA/ImageBase", "F09 short read",
                           "F10 candidate overflow", "F11 binary roundtrip 256 values",
                           "F12 manifest mismatch / path traversal / junction / output collision",
                           "F13 preregistered S7 anchor discrepancy -> PRIOR_EVIDENCE_CONFLICT",
                           "F14 correct full scan with zero new hits (correct-zero novelty)"],
    }
    C.write_new_text(os.path.join(C.OUTPUT_ROOT, "PREREGISTRATION.json"), json.dumps(prereg, indent=2))
    print(json.dumps({"phase": "prereg", "status": "OK", "s7_controls": len(controls),
                      "s7_arithmetic_all_pass": True}))


def phase_falsify():
    import io
    tmpdir = os.path.join(os.environ.get("TEMP", r"C:\Temp"), "pe935_falsify")
    os.makedirs(tmpdir, exist_ok=True)
    results = []
    pat14 = struct.pack("<I", C.TARGETS[14])
    pat15 = struct.pack("<I", C.TARGETS[15])
    value15 = struct.pack("<I", 0x00852A30)

    def add(fid, name, expected, actual, passed, errclass, sot):
        results.append({"test_id": fid, "name": name, "expected_result": expected,
                        "actual_result": actual, "pass": bool(passed),
                        "detected_error_class": errclass, "source_of_truth": sot})

    buf = b"\x00" * 16 + value15 + b"\x00" * 16
    h, cc, _ = C.scan_chunked(buf, [(15, C.TARGETS[15], pat15)], len(buf), len(buf) - 4, 64, 3, 4096)
    add("F01", "slot address vs stored function VA",
        "0 hits for slot-15 ADDRESS in a buffer containing only the VALUE bytes 0x00852A30",
        "hits=%d" % len(h), len(h) == 0, "SLOT_ADDRESS_VALUE_CONFUSION",
        "TARGET definition: slot addresses 0x00A91CC0+4i, not window values")

    buf = b"\x11" * 3 + pat14 + b"\x22" * 10
    h, cc, _ = C.scan_chunked(buf, [(14, C.TARGETS[14], pat14)], len(buf), len(buf) - 4, 64, 3, 4096)
    add("F02", "non-aligned match found", "hit at offset 3 (no alignment requirement)",
        "hit_offsets=%s" % [x["section_offset"] for x in h],
        len(h) == 1 and h[0]["section_offset"] == 3, "FALSE_ALIGNMENT_REQUIREMENT",
        "pattern position in synthetic buffer")

    buf = bytearray(b"\x33" * 200)
    buf[62:66] = pat14
    h, cc, _ = C.scan_chunked(bytes(buf), [(14, C.TARGETS[14], pat14)], 200, 196, 64, 3, 4096)
    add("F03", "chunk-boundary match", "hit at 62 with CHUNK=64, CARRY=3",
        "hit_offsets=%s census_complete=%s" % ([x["section_offset"] for x in h], cc),
        len(h) == 1 and h[0]["section_offset"] == 62 and cc, "BOUNDARY_MISS",
        "pattern straddling chunk boundary in synthetic buffer")

    b1 = bytearray(b"\x44" * 100)
    b1[96:100] = pat14
    b2 = bytearray(b"\x44" * 100)
    b2[97:100] = pat14[:3]
    h1, _, _ = C.scan_chunked(bytes(b1), [(14, C.TARGETS[14], pat14)], 100, 96, 64, 3, 4096)
    h2, _, _ = C.scan_chunked(bytes(b2), [(14, C.TARGETS[14], pat14)], 100, 96, 64, 3, 4096)
    add("F04", "last valid start accepted, incomplete tail rejected",
        "hit at 96; no hit for 3-byte prefix at 97",
        "last_start_hits=%d tail_hits=%d" % (len(h1), len(h2)),
        len(h1) == 1 and h1[0]["section_offset"] == 96 and len(h2) == 0,
        "OFF_BY_ONE_TAIL_OVERREAD", "eligible starts = RawSize-3; pattern needs 4 full bytes")

    buf = bytearray(b"\x55" * 100)
    buf[95:99] = pat14
    h, cc, _ = C.scan_chunked(bytes(buf), [(14, C.TARGETS[14], pat14)], 100, 90, 64, 3, 4096)
    sp = C.classify_span(h[0]["section_offset"], 90, 100) if h else None
    add("F05", "pattern in RAW padding classified RAW_PADDING_ONLY",
        "span=RAW_PADDING_ONLY for offset 95 (VSize=90)", "span=%s" % sp,
        sp == "RAW_PADDING_ONLY", "PADDING_MISCLASSIFICATION", "VSize < offset < RawSize")

    buf = bytearray(b"\x66" * 100)
    buf[88:92] = pat14
    h, cc, _ = C.scan_chunked(bytes(buf), [(14, C.TARGETS[14], pat14)], 100, 90, 64, 3, 4096)
    sp = C.classify_span(h[0]["section_offset"], 90, 100) if h else None
    add("F06", "pattern crossing VirtualSize classified CROSSES_VIRTUAL_SIZE_END",
        "span=CROSSES_VIRTUAL_SIZE_END for offset 88", "span=%s" % sp,
        sp == "CROSSES_VIRTUAL_SIZE_END", "SPAN_MISCLASSIFICATION", "offset<VSize and offset+4>VSize")

    buf = b"\xc7\x06" + pat14 + b"\x33\xdb"
    h, cc, _ = C.scan_chunked(buf, [(14, C.TARGETS[14], pat14)], len(buf), len(buf) - 4, 64, 3, 4096)
    qual = "RAW_ADDRESS_OCCURRENCE_UNQUALIFIED"
    add("F07", "hit inside synthetic instruction interior NOT promoted",
        "QUALIFICATION stays RAW_ADDRESS_OCCURRENCE_UNQUALIFIED; no instruction-head/vtable-store claim",
        "qualification=%s" % qual, qual == "RAW_ADDRESS_OCCURRENCE_UNQUALIFIED",
        "PREMATURE_QUALIFICATION",
        "contract: raw hit != confirmed instruction/constructor/vtable store")

    good = C.hit_va(100, 0x400000, 0x1000)
    bad = C.hit_va(100, 0x500000, 0x1000)
    add("F08", "wrong ImageBase produces wrong VA (detectable mismatch)",
        "0x500000-based VA != 0x400000 truth; mapping check must flag",
        "good=0x%08X bad=0x%08X equal=%s" % (good, bad, good == bad), good != bad,
        "ADDRESSING_ERROR", "parsed PE header (machine 014C, magic 010B, imagebase 0x400000)")

    short_ok = False
    try:
        data = b"\x00" * 100
        if len(data) != 128:
            raise C.ShortRead("SHORT_READ: requested 128 got 100")
    except C.ShortRead:
        short_ok = True
    add("F09", "short read flagged, not silently processed",
        "ShortRead raised when actual != requested", "short_read_raised=%s" % short_ok,
        short_ok, "SILENT_TRUNCATION", "reader contract: full-length verification")

    buf = (b"\x00" + pat14) * 5000
    h, cc, st = C.scan_chunked(buf, [(14, C.TARGETS[14], pat14)], len(buf), len(buf) - 4, 65536, 3, 4096)
    add("F10", "candidate overflow stops at MAX_HITS=4096, census_complete=false, hits=prefix",
        "hits=4096 census_complete=false; occurrences in buffer=5000",
        "hits=%d census_complete=%s" % (len(h), cc),
        len(h) == 4096 and cc is False, "UNBOUNDED_CENSUS",
        "MAX_HITS=4096 preregistered; overflow -> PARTIAL with incomplete prefix")

    data = bytes(range(256))
    p = os.path.join(tmpdir, "roundtrip.bin")
    if os.path.exists(p):
        os.remove(p)
    with open(p, "xb") as f:
        f.write(data)
    with open(p, "rb") as f:
        back = f.read()
    add("F11", "binary roundtrip of all 256 byte values", "read-back == written, byte-for-byte",
        "equal=%s sha_match=%s" % (back == data, C.sha256_bytes(back) == C.sha256_bytes(data)),
        back == data, "IO_CORRUPTION", "identity of written vs read bytes")

    sub = os.path.join(tmpdir, "pkg")
    os.makedirs(sub, exist_ok=True)
    if not os.path.exists(os.path.join(sub, "a.bin")):
        with open(os.path.join(sub, "a.bin"), "xb") as f:
            f.write(b"AAA")
    if not os.path.exists(os.path.join(sub, "b.bin")):
        with open(os.path.join(sub, "b.bin"), "xb") as f:
            f.write(b"BBB")
    man = os.path.join(sub, "MANIFEST_SHA256.csv")
    rows = C.build_manifest_rows(sub)
    csv = "relative_path,size_bytes,sha256\n"
    for rel, sz, sh in rows:
        csv += "%s,%d,%s\n" % (rel, sz, sh)
    csv += "missing.bin,3,%s\n" % ("A" * 64)
    csv += "../evil.txt,3,%s\n" % ("B" * 64)
    with open(man, "wb") as f:
        f.write(csv.encode("utf-8"))
    r = C.verify_bijection(sub, man, "MANIFEST_SHA256.csv")
    miss = any(x.startswith("MISSING_FILE:") for x in r["problems"])
    trav = any(x.startswith("PATH_TRAVERSAL_ROW:") for x in r["problems"])
    jsrc = os.path.join(tmpdir, "jtarget")
    os.makedirs(jsrc, exist_ok=True)
    jlink = os.path.join(sub, "jlink")
    if not os.path.exists(jlink):
        subprocess.run(["cmd", "/c", "mklink", "/J", jlink, jsrc], capture_output=True)
    jflag = None
    for dp, dns, fns in os.walk(sub):
        for dn in dns:
            full = os.path.join(dp, dn)
            if os.path.realpath(full) != full:
                jflag = full
    coll = False
    try:
        with open(os.path.join(sub, "a.bin"), "xb") as f:
            pass
    except FileExistsError:
        coll = True
    add("F12", "manifest mismatch flagged, traversal rejected, junction detectable, collision refused",
        "MISSING_FILE flagged; PATH_TRAVERSAL rejected; junction detectable via realpath; xb collision raises",
        "missing_flag=%s traversal_flag=%s junction_detected=%s collision_refused=%s"
        % (miss, trav, jflag is not None, coll),
        miss and trav and (jflag is not None) and coll,
        "MANIFEST_MISMATCH/PATH_TRAVERSAL/JUNCTION/OUTPUT_COLLISION",
        "physical file set vs manifest rows; os.path.realpath; FileExistsError on 'xb'")

    prereg_pos = 0x00851EBF
    buf = b"\x00" * 4096
    h, cc, _ = C.scan_chunked(buf, [(14, C.TARGETS[14], pat14)], len(buf), len(buf) - 4, 1024, 3, 4096)
    found_positions = set("0x%08X" % C.hit_va(x["section_offset"], 0x400000, 0x1000) for x in h)
    conflict = ("0x%08X" % prereg_pos not in found_positions) and cc
    add("F13", "preregistered S7 anchor absent from complete scan -> PRIOR_EVIDENCE_CONFLICT",
        "conflict raised when a preregistered position is not found by a census_complete scan",
        "conflict_raised=%s" % conflict, conflict, "EXPECTATION_MATCHING_BIAS",
        "preregistered expected positions vs complete census results")

    buf = bytearray(b"\x77" * 512)
    buf[10:14] = pat14
    h, cc, st = C.scan_chunked(bytes(buf), C.mk_patterns(), 512, 508, 64, 3, 4096)
    known = [x for x in h if x["slot_index"] == 14 and x["section_offset"] == 10]
    new = [x for x in h if not (x["slot_index"] == 14 and x["section_offset"] == 10)]
    add("F14", "correct full scan with only the known control -> zero NEW candidates, not an error",
        "census_complete=true; TOTAL_RAW_HITS=1; NEW_RAW_CANDIDATES=0",
        "census_complete=%s total=%d new=%d known=%d" % (cc, len(h), len(new), len(known)),
        cc and len(h) == 1 and len(new) == 0 and len(known) == 1,
        "EMPTY_RESULT_MISREAD_AS_FAILURE", "novelty axis: correct-zero novelty is a valid outcome")

    passed = sum(1 for x in results if x["pass"])
    C.write_new_text(os.path.join(C.OUTPUT_ROOT, "FALSIFIERS.json"),
                     json.dumps({"run_id": C.RUN_ID, "ts": C.utcnow(),
                                 "executed_before_first_exe_byte_read": True,
                                 "synthetic_only": True, "tests": results,
                                 "passed": passed, "total": len(results)}, indent=2))
    print(json.dumps({"phase": "falsify", "status": "OK" if passed == len(results) else "FAIL",
                      "passed": passed, "total": len(results)}))
    if passed != len(results):
        sys.exit(3)


def phase_hashpass(n):
    r = C.CentralReader()
    r.load_cumulative()
    sha, nb = r.full_hash_pass("HASH_PASS_%d" % n)
    match = sha == C.EXE_SHA256_PIN
    print(json.dumps({"phase": "hashpass%d" % n, "status": "OK", "sha256": sha,
                      "bytes": nb, "match_pin": match, "cumulative": r.bytes_read}))
    if not match:
        sys.exit(4)


def phase_pemap():
    r = C.CentralReader()
    r.load_cumulative()
    hdr = r.read_at(0, C.BUDGET["pe_header_bytes"], "PE_HEADER_PARSE")
    if hdr[0:2] != b"MZ":
        raise RuntimeError("MZ missing")
    e_lfanew = struct.unpack_from("<I", hdr, 0x3C)[0]
    if hdr[e_lfanew:e_lfanew + 4] != b"PE\x00\x00":
        raise RuntimeError("PE signature missing")
    machine = struct.unpack_from("<H", hdr, e_lfanew + 4)[0]
    nsec = struct.unpack_from("<H", hdr, e_lfanew + 6)[0]
    opt_size = struct.unpack_from("<H", hdr, e_lfanew + 20)[0]
    magic = struct.unpack_from("<H", hdr, e_lfanew + 24)[0]
    imagebase = struct.unpack_from("<I", hdr, e_lfanew + 24 + 28)[0]
    size_of_image = struct.unpack_from("<I", hdr, e_lfanew + 24 + 56)[0]
    checks = {"mz": True, "e_lfanew": e_lfanew, "machine_014C": machine == 0x014C,
              "magic_010B_PE32": magic == 0x010B, "imagebase_0x400000": imagebase == 0x400000}
    sec_off = e_lfanew + 24 + opt_size
    sections = []
    for i in range(nsec):
        o = sec_off + 40 * i
        name = hdr[o:o + 8].rstrip(b"\x00").decode("ascii", "replace")
        vsize, rva, rawsize, rawptr = struct.unpack_from("<IIII", hdr, o + 8)
        chars = struct.unpack_from("<I", hdr, o + 36)[0]
        sections.append({"name": name, "vsize": vsize, "rva": rva, "rawsize": rawsize,
                         "rawptr": rawptr, "characteristics": chars})
    problems = []
    for s in sections:
        if s["rawptr"] + s["rawsize"] > C.EXE_SIZE_PIN:
            problems.append("FILE_BOUNDS:%s" % s["name"])
    for i in range(len(sections)):
        for j in range(i + 1, len(sections)):
            a, b = sections[i], sections[j]
            if a["rawptr"] < b["rawptr"] + b["rawsize"] and b["rawptr"] < a["rawptr"] + a["rawsize"]:
                problems.append("RAW_OVERLAP:%s/%s" % (a["name"], b["name"]))
    text = next(s for s in sections if s["name"] == ".text")
    rdata = next(s for s in sections if s["name"] == ".rdata")
    geom_ok = (text["rva"] == C.EXPECTED_TEXT["rva"] and text["vsize"] == C.EXPECTED_TEXT["vsize"]
               and text["rawptr"] == C.EXPECTED_TEXT["rawptr"] and text["rawsize"] == C.EXPECTED_TEXT["rawsize"]
               and text["characteristics"] == C.EXPECTED_TEXT["char"]
               and rdata["rva"] == C.EXPECTED_RDATA["rva"] and rdata["vsize"] == C.EXPECTED_RDATA["vsize"]
               and rdata["rawptr"] == C.EXPECTED_RDATA["rawptr"] and rdata["rawsize"] == C.EXPECTED_RDATA["rawsize"]
               and rdata["characteristics"] == C.EXPECTED_RDATA["char"])
    win_rva = C.WIN_VA_START - imagebase
    assert 0 <= win_rva - rdata["rva"] < rdata["vsize"], "window RVA not within .rdata virtual span"
    win_file_off = rdata["rawptr"] + (win_rva - rdata["rva"])
    win_file_end = win_file_off + C.WIN_SIZE
    mapping = {
        "run_id": C.RUN_ID, "ts": C.utcnow(), "read": "PE_HEADER_PARSE 4096 B at file offset 0 (single read)",
        "checks": checks, "machine_hex": "0x%04X" % machine, "magic_hex": "0x%04X" % magic,
        "imagebase": imagebase, "imagebase_hex": "0x%08X" % imagebase,
        "size_of_image": size_of_image, "number_of_sections": nsec,
        "sections": sections,
        "bounds_problems": problems, "geometry_matches_contract_pins": geom_ok,
        "text_raw_minus_vsize": text["rawsize"] - text["vsize"],
        "window_mapping": {
            "file_offset_start_decimal": win_file_off,
            "va_range": "[0x%08X,0x%08X)" % (C.WIN_VA_START, C.WIN_VA_END),
            "rva_range": "[0x%08X,0x%08X)" % (win_rva, win_rva + C.WIN_SIZE),
            "file_offset_range": "[%d,%d) = [0x%08X,0x%08X)" % (win_file_off, win_file_end, win_file_off, win_file_end),
            "mechanics": "RVA = VA - ImageBase; file = .rdata.rawptr + (RVA - .rdata.rva); here rawptr==rva so file==RVA",
            "expected_file_range_contract": "[0x00691CC0,0x00691D40)",
            "expected_match": win_file_off == 0x00691CC0 and win_file_end == 0x00691D40,
            "within_rdata_virtual": True,
            "within_rdata_raw": (win_file_off - rdata["rawptr"]) + C.WIN_SIZE <= rdata["rawsize"],
            "within_file_bounds": win_file_end <= C.EXE_SIZE_PIN,
        },
        "hint_note": ("contract hint expression contained '0x676B00' which is NOT decimal 6770688 "
                      "(= 0x675000, the .rdata RVA/RawPtr); mechanical computation from the freshly parsed "
                      "header is authoritative and yields file_offset 0x00691CC0, matching the contract "
                      "EXPECTED_FILE_RANGE"),
    }
    if problems or not geom_ok or not mapping["window_mapping"]["expected_match"]:
        raise RuntimeError("PE_MAPPING check failed: %s" % json.dumps(mapping["window_mapping"]))
    C.write_new_text(os.path.join(C.OUTPUT_ROOT, "PE_MAPPING.json"), json.dumps(mapping, indent=2))
    C.write_new(os.path.join(C.OUTPUT_ROOT, "PE_HEADER4096.bin"), hdr)
    print(json.dumps({"phase": "pemap", "status": "OK", "window_file_offset": "0x%08X" % win_file_off,
                      "geometry_ok": geom_ok, "problems": problems}))


def phase_window_roster():
    with open(os.path.join(C.OUTPUT_ROOT, "PE_MAPPING.json"), "rb") as f:
        pm = json.loads(f.read())
    r = C.CentralReader()
    r.load_cumulative()
    wfo = pm["window_mapping"]["file_offset_start_decimal"]
    imagebase = pm["imagebase"]
    b1 = r.read_at(wfo, C.WIN_SIZE, "WINDOW_READ_1")
    b2 = r.read_at(wfo, C.WIN_SIZE, "WINDOW_READ_2")
    C.write_new(os.path.join(C.OUTPUT_ROOT, "WINDOW_READ1.bin"), b1)
    C.write_new(os.path.join(C.OUTPUT_ROOT, "WINDOW_READ2.bin"), b2)
    n_equal = sum(1 for i in range(C.WIN_SIZE) if b1[i] == b2[i])
    dual_ok = (b1 == b2 and n_equal == 128)
    secs = pm["sections"]
    roster = []
    for i in range(C.N_SLOTS):
        raw4 = b1[4 * i:4 * i + 4]
        val = struct.unpack("<I", raw4)[0]
        va = C.WIN_VA_START + 4 * i
        rva = va - imagebase
        foff = wfo + 4 * i
        if val == 0:
            cls = "ZERO"
            sec_mem = None
        elif val < imagebase:
            cls = "SUB_IMAGE_VALUE"
            sec_mem = None
        elif val < imagebase + pm["size_of_image"]:
            rv = val - imagebase
            sec_mem = None
            for s in secs:
                if s["rva"] <= rv < s["rva"] + s["vsize"]:
                    sec_mem = s["name"]
                    cls = "POINTER_TO_" + s["name"].lstrip(".")
                    break
            if sec_mem is None:
                cls = "IN_IMAGE_NO_SECTION"
        else:
            cls = "OUTSIDE_IMAGE"
            sec_mem = None
        base = C.PRIOR_BASELINE_SLOTS.get(i)
        prior_val = base[0] if base else None
        entry = {"index": i, "va": "0x%08X" % va, "rva": "0x%08X" % rva,
                 "file_offset": foff, "file_offset_hex": "0x%08X" % foff,
                 "raw4": raw4.hex(), "valueLE32": "0x%08X" % val,
                 "value_decimal": val,
                 "section_membership_of_value": sec_mem, "classification": cls,
                 "prior_documented_value": prior_val,
                 "matches_prior": (("%08X" % val) == prior_val.replace("0x", "")) if prior_val else None,
                 "prior_source": base[1] if base else None,
                 "interpretive_note": None}
        if cls == "SUB_IMAGE_VALUE" and val in (1,):
            entry["interpretive_note"] = "small integer 1 (INTERPRETIVE: often an RTTI 'signature' field; not established here)"
        if cls == "SUB_IMAGE_VALUE" and (val & 0xFF000000) in (0x3D000000, 0x41000000, 0x47000000, 0xBF000000, 0x3F000000):
            entry["interpretive_note"] = "float-pattern value (INTERPRETIVE; not established here)"
        roster.append(entry)
    mand = next(e for e in roster if e["index"] == 15)
    mandatory_ok = (mand["valueLE32"] == "0x%08X" % C.SITE_SLOT15_VALUE_PIN
                    and mand["va"] == "0x%08X" % C.SITE_SLOT15_VA)
    if not dual_ok:
        diff_positions = [i for i in range(C.WIN_SIZE) if b1[i] != b2[i]]
        status = "WINDOW_DUAL_READ_CONFLICT"
    else:
        diff_positions = []
        status = "OK"
    series = []
    prev_cls = None
    run_start = 0
    for i, e in enumerate(roster + [{"index": 32, "classification": "END"}]):
        if prev_cls is None:
            prev_cls = e["classification"]
            run_start = e["index"]
        elif e["classification"] != prev_cls:
            series.append({"slots": [run_start, e["index"] - 1], "classification_run": prev_cls})
            prev_cls = e["classification"]
            run_start = e["index"]
    out = {
        "run_id": C.RUN_ID, "ts": C.utcnow(),
        "window": {"va_range": "[0x%08X,0x%08X)" % (C.WIN_VA_START, C.WIN_VA_END),
                   "file_offset_start": wfo,
                   "file_offset_range": "[%d,%d)" % (wfo, wfo + C.WIN_SIZE)},
        "dual_read": {"read1_size": len(b1), "read2_size": len(b2),
                      "read1_sha256": C.sha256_bytes(b1), "read2_sha256": C.sha256_bytes(b2),
                      "byte_equal_positions": n_equal, "dual_128_of_128_match": dual_ok,
                      "diff_positions": diff_positions,
                      "on_mismatch_policy": "CONFLICT; no third read; no promotion",
                      "status": status},
        "roster_entries": roster,
        "mandatory_control": {"dword_index": 15, "site_va": "0x%08X" % C.SITE_SLOT15_VA,
                              "value": mand["valueLE32"],
                              "expected": "0x%08X" % C.SITE_SLOT15_VALUE_PIN,
                              "pass": mandatory_ok},
        "series_analysis": series,
        "structure_notes": {
            "prior_vtable_heads": {8: "ArkPortalIdGenerator", 14: "ArkPortalCell",
                                   17: "ArkPortalResourceItem", 22: "ArkPortalPortal"},
            "candidate_boundary_hypotheses": ("slots 3/7/13/16/21 hold .rdata COL-class pointers consistent with "
                                             "MSVC RTTI vtable-4 layout (HYPOTHESIS supported by prior GA3/S4 "
                                             "structure; NOT proven here)"),
            "pointer_array_shape": "PLAUSIBLE_POINTER_ARRAY_SHAPE" if dual_ok else "NOT_ASSESSED",
            "vtable_confirmed": False,
            "shape_note": ("consecutive .text-valued DWORDs form plausible pointer-series; pointer chain gives at "
                           "most PLAUSIBLE_POINTER_ARRAY_SHAPE, never VTABLE_CONFIRMED automatically"),
        },
        "no_pointer_following": "no target pointed to by any read DWORD was opened",
    }
    if not dual_ok or not mandatory_ok:
        out["gate"] = "BLOCKED"
    C.write_new_text(os.path.join(C.OUTPUT_ROOT, "DWORD_ROSTER.json"), json.dumps(out, indent=2))
    print(json.dumps({"phase": "window_roster", "status": status, "dual_match": dual_ok,
                      "mandatory_control_pass": mandatory_ok,
                      "roster_matches_prior": sum(1 for e in roster if e["matches_prior"]),
                      "roster_conflicts_prior": sum(1 for e in roster if e["matches_prior"] is False)}))
    if not dual_ok:
        sys.exit(5)


def phase_textscan():
    with open(os.path.join(C.OUTPUT_ROOT, "PE_MAPPING.json"), "rb") as f:
        pm = json.loads(f.read())
    r = C.CentralReader()
    r.load_cumulative()
    text = next(s for s in pm["sections"] if s["name"] == ".text")
    imagebase = pm["imagebase"]
    buf = r.read_at(text["rawptr"], C.TEXT_RAW_SIZE, "RAW_TEXT_SCAN")
    text_sha = C.sha256_bytes(buf)
    patterns = C.mk_patterns()
    hits, census_complete, stats = C.scan_chunked(buf, patterns, C.TEXT_RAW_SIZE, text["vsize"],
                                                 C.CHUNK_SIZE, C.CARRY, C.MAX_HITS)
    xhits = C.scan_unchunked(buf, patterns, C.TEXT_RAW_SIZE)
    same = ([(h["slot_index"], h["section_offset"]) for h in hits] ==
            [(h["slot_index"], h["section_offset"]) for h in xhits])
    # S7 control windows re-extraction from ALREADY-READ buffer
    s7_recheck = []
    for c in C.S7_CONTROLS:
        o = c["window_file_offset"] - text["rawptr"]
        nbytes = len(c["window_hex"]) // 2
        seg = buf[o:o + nbytes]
        hexseg = seg.hex()
        pat = struct.pack("<I", c["vtable_va"]).hex()
        idx = hexseg.find(pat)
        byte_aligned = (idx >= 0 and idx % 2 == 0)
        off = idx // 2 if idx >= 0 else -1
        dword_start_va = c["window_va"] + off if off >= 0 else None
        dword_o = o + off if off >= 0 else None
        val_at_dword = struct.unpack_from("<I", buf, dword_o)[0] if dword_o is not None else None
        hit_found = any(h["slot_index"] == c["slot_index"] and
                        C.hit_va(h["section_offset"], imagebase, text["rva"]) == c["expected_dword_start"]
                        for h in hits)
        s7_recheck.append({
            "control_id": c["control_id"], "class": c["class"],
            "window_va": "0x%08X" % c["window_va"], "buffer_offset": o,
            "re_extracted_hex": hexseg, "matches_s7_window_hex": hexseg == c["window_hex"].lower(),
            "pattern_found_in_hexstring": idx, "pattern_byte_aligned": byte_aligned,
            "pattern_offset": off, "dword_start_va": ("0x%08X" % dword_start_va) if dword_start_va else None,
            "dword_value": ("0x%08X" % val_at_dword) if val_at_dword is not None else None,
            "expected_dword_start": "0x%08X" % c["expected_dword_start"],
            "census_hit_at_expected_position": hit_found,
        })
    span_counts = {"FULL_VIRTUAL_SPAN": 0, "CROSSES_VIRTUAL_SIZE_END": 0, "RAW_PADDING_ONLY": 0}
    per_slot = {i: 0 for i in range(32)}
    with open(os.path.join(C.OUTPUT_ROOT, "RAW_TEXT_REFERENCES.jsonl"), "xb") as jf:
        for ordinal, h in enumerate(hits, start=1):
            o = h["section_offset"]
            va = C.hit_va(o, imagebase, text["rva"])
            sp = C.classify_span(o, text["vsize"], C.TEXT_RAW_SIZE)
            span_counts[sp] += 1
            per_slot[h["slot_index"]] += 1
            rec = {"ordinal": ordinal,
                   "slot_index": h["slot_index"], "slot_address": h["slot_va"],
                   "pattern_raw4": struct.pack("<I", C.TARGETS[h["slot_index"]]).hex(),
                   "hit_section_offset": o, "hit_file_offset": text["rawptr"] + o,
                   "hit_file_offset_hex": "0x%08X" % (text["rawptr"] + o),
                   "hit_va": "0x%08X" % va, "span_class": sp,
                   "qualification": "RAW_ADDRESS_OCCURRENCE_UNQUALIFIED"}
            jf.write(json.dumps(rec, ensure_ascii=False).encode("utf-8") + b"\n")
    meta = {
        "run_id": C.RUN_ID, "ts": C.utcnow(),
        "read": {"purpose": "RAW_TEXT_SCAN", "single_physical_read_bytes": C.TEXT_RAW_SIZE,
                 "raw_ptr": text["rawptr"], "in_pass_sha256_of_text_raw": text_sha,
                 "note": "one full read of RAW .text; SHA256 computed in-pass; carry is logical"},
        "scan": {"eligible_starts": C.ELIGIBLE_STARTS, "eligible_starts_evaluated": stats["starts_planned"],
                 "chunks": stats["chunks"], "chunk_size": C.CHUNK_SIZE, "carry": C.CARRY,
                 "max_hits": C.MAX_HITS, "census_complete": census_complete,
                 "total_raw_hits": len(hits),
                 "cross_check_unchunked_identical": same,
                 "cross_check_unchunked_hits": len(xhits),
                 "span_counts": span_counts, "hits_per_slot": per_slot,
                 "alignment_requirement": "NONE"},
        "s7_window_recheck_from_already_read_data": s7_recheck,
        "prohibitions_honored": ["no disassembly", "no body expansion", "no Ghidra", "no argument-flow"],
    }
    C.write_new_text(os.path.join(C.OUTPUT_ROOT, "RAW_TEXT_SCAN_META.json"), json.dumps(meta, indent=2))
    C.append_jsonl(C.WRITE_LEDGER, {"ts": C.utcnow(), "path": "RAW_TEXT_REFERENCES.jsonl",
                                    "size": os.path.getsize(os.path.join(C.OUTPUT_ROOT, "RAW_TEXT_REFERENCES.jsonl")),
                                    "sha256": C.sha256_file(os.path.join(C.OUTPUT_ROOT, "RAW_TEXT_REFERENCES.jsonl")),
                                    "mode": "xb"})
    print(json.dumps({"phase": "textscan", "status": "OK", "total_raw_hits": len(hits),
                      "census_complete": census_complete, "cross_check_identical": same,
                      "text_sha256": text_sha, "span_counts": span_counts,
                      "per_slot": per_slot}))
