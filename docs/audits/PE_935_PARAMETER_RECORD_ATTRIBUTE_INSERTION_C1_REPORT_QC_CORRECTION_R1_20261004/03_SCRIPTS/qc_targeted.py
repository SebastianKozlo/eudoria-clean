# qc_targeted.py
# TARGETED QC — PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_C1_REPORT_QC_CORRECTION_R1_20261004
# QC_SCOPE = SELF_CHECK_REPORT_QC_HANDOFF_CORRECTION (executor self-check; explicitly
# NOT an independent PE-MASTER audit).
#
# Modes:
#   normal   -> writes 01_RAW/QC_TARGETED.json        (all checks + overall verdict)
#   mutation -> writes 01_RAW/QC_MUTATION_AB_SWAP.json (A/B destination-documentation
#               swap falsifier: BOTH mutants must FAIL the destination check while the
#               raw VFS values stay unchanged; canonical repo files are untouched —
#               mutants are produced in a private temp copy)
#
# READ-ONLY vs originals: Entropia.exe, templates.vfs, and every canonical repo file.
# sys.dont_write_bytecode = True. No client launch, no runtime execution, no network.
import sys, os, json, re, struct, hashlib, tempfile, shutil
sys.dont_write_bytecode = True

RUN = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_C1_REPORT_QC_CORRECTION_R1_20261004"
REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
R1 = os.path.join(REPO, "docs", "audits", "PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
TPL = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs"

EXPECT = {
    "exe_sha": "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31",
    "tpl_sha": "BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77",
    "tpl_size": 560788,
    "ra": {"id2": 16083, "offset": 560212, "size": 28, "A": 410620, "B": 0, "C": 0,
           "d_bits": 1056947864,
           "payload_sha": "9E22B8AF3A7B63CECFA41B7D3C46775BBBE0C7A8B505B7635214EDE89898D74B",
           "window_sha": "1987B5C48724FC5BDA2D752928479CCFDF2879230D41068F02BC6046EEAB46B5"},
    "rb": {"id2": 4508, "offset": 96496, "size": 28, "A": 296445, "B": 296446, "C": 0,
           "d_bits": 1123672523,
           "payload_sha": "890A50E5DDE3942A59E171659025C2F518057466161945471CDDF0FFB339004B",
           "window_sha": "4345305B0A8598EC3FBB41831E7C7DD255401092B9B22D3C6E459BDAD57D155E"},
}

# ---------------------------------------------------------------- PE mapper
def load_pe(path):
    d = open(path, "rb").read()
    e_lfanew = struct.unpack_from("<I", d, 0x3C)[0]
    assert d[e_lfanew:e_lfanew + 4] == b"PE\x00\x00", "not a PE file"
    nsec = struct.unpack_from("<H", d, e_lfanew + 6)[0]
    opt_size = struct.unpack_from("<H", d, e_lfanew + 20)[0]
    sec_off = e_lfanew + 24 + opt_size
    secs = []
    for i in range(nsec):
        o = sec_off + 40 * i
        name = d[o:o + 8].rstrip(b"\x00").decode()
        vsize, vaddr, rawsize, rawptr = struct.unpack_from("<IIII", d, o + 8)
        secs.append((name, vaddr, vsize, rawsize, rawptr))
    ib = struct.unpack_from("<I", d, e_lfanew + 24 + 28)[0]
    return d, ib, secs

def va_to_off(ib, secs, va):
    rva = va - ib
    for name, vaddr, vsize, rawsize, rawptr in secs:
        if vaddr <= rva < vaddr + max(vsize, rawsize):
            return rawptr + (rva - vaddr)
    raise ValueError("VA not mapped: 0x%08X" % va)

def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest().upper()

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()

# ---------------------------------------------------------------- helpers
def read_doc(relname):
    with open(os.path.join(R1, relname), "r", encoding="utf-8") as f:
        return f.read()

RETRACTION_MARKERS = ["SUPERSEDES", "supersedes", "SUPERSESSION", "was FALSE",
                      "was WRONG", "retract", "corrected from", "NOT @", "was @",
                      "C1-corrected", "C1/P3-corrected", "C2-corrected",
                      "P3-corrected", "corrected —"]

def retired_claim_residue(text, pattern):
    """Count occurrences of a retired claim that are NOT inside a retraction quote.
    Searches the FULL text (retired phrases may span line breaks), maps each hit to
    its line, and exempts a hit when any line within +/-3 lines contains a retraction
    marker (the supersession-quote evidence is REQUIRED to remain in the docs)."""
    lines = text.splitlines()
    starts = []
    pos = 0
    for ln in lines:
        starts.append(pos)
        pos += len(ln) + 1
    hits, exempt = [], []
    # literal phrases; spaces match any whitespace incl. line breaks (the retired
    # sentence may be line-wrapped inside the retraction quote)
    pat = re.compile(re.escape(pattern).replace(r"\ ", r"\s+"))
    for m in pat.finditer(text):
        li = max(i for i, s in enumerate(starts) if s <= m.start())
        ctx = "\n".join(lines[max(0, li - 3): li + 4])
        (exempt if any(k in ctx for k in RETRACTION_MARKERS) else hits).append(
            {"line": li + 1, "text": lines[li].strip()})
    return hits, exempt

# ---------------------------------------------------------------- TQ1 payload decode
def tq1_payload_field_decode(tpl_bytes):
    r = {}
    for tag in ("ra", "rb"):
        e = EXPECT[tag]
        off = e["offset"]
        hdr = struct.unpack_from("<IIII", tpl_bytes, off)
        payload = tpl_bytes[off + 16: off + 16 + e["size"]]
        got = {
            "header": {"id": hdr[0], "size": hdr[1], "ver": hdr[2], "crc": "%08X" % hdr[3]},
            "id2": struct.unpack_from("<I", payload, 0)[0],
            "A": struct.unpack_from("<I", payload, 4)[0],
            "B": struct.unpack_from("<I", payload, 8)[0],
            "C": struct.unpack_from("<I", payload, 12)[0],
            "D_bits": struct.unpack_from("<I", payload, 16)[0],
            "list1_count": struct.unpack_from("<H", payload, 20)[0],
            "list2_count": struct.unpack_from("<H", payload, 22)[0],
            "f11": struct.unpack_from("<I", payload, 24)[0],
            "payload_sha256": sha256_bytes(payload),
            "window_sha256": sha256_bytes(tpl_bytes[off: off + 16 + e["size"]]),
        }
        ok = (hdr[0] == e["id2"] and hdr[1] == e["size"] and got["id2"] == e["id2"]
              and got["A"] == e["A"] and got["B"] == e["B"] and got["C"] == e["C"]
              and got["D_bits"] == e["d_bits"] and got["list1_count"] == 0
              and got["list2_count"] == 0 and got["f11"] == 0
              and got["payload_sha256"] == e["payload_sha"]
              and got["window_sha256"] == e["window_sha"])
        r[tag] = {"measured": got, "pass": ok}
    r["pass"] = r["ra"]["pass"] and r["rb"]["pass"]
    return r

# ---------------------------------------------------------------- TQ2 destination mapping
ROW_U32 = re.compile(
    r"\| payload\[(\d+)\] \((id2|A|B|C)\) \| template\+0x([0-9A-Fa-f]{2}) \| "
    r"MOV \[EDI(?:\+0x([0-9A-Fa-f]{2}))?\],EAX @0x([0-9A-Fa-f]{8}) \|")
ROW_D = re.compile(
    r"\| payload\[4\] \(D_f32\) \| template\+0x10 \(FLD/FSTP\) \| "
    r"FLD \[EDX\+EAX\] @0x([0-9A-Fa-f]{8}); FSTP \[EDI\+0x10\] @0x([0-9A-Fa-f]{8}) \|")

def verify_destination_table(dexe, ib, secs, table_text):
    """Parse the PARSER_CHAIN destination table and byte-verify each documented
    destination against the pinned-EXE store instruction. Returns (rows, pass)."""
    def rd(va, n):
        return dexe[va_to_off(ib, secs, va): va_to_off(ib, secs, va) + n]
    rows, ok = [], True
    for m in ROW_U32.finditer(table_text):
        idx, name, dest, disp, va = m.groups()
        dest_i = int(dest, 16)
        disp_i = int(disp, 16) if disp else 0
        va_i = int(va, 16)
        expected = bytes([0x89, 0x07]) if dest_i == 0 else bytes([0x89, 0x47, dest_i])
        actual = rd(va_i, len(expected))
        row_ok = (dest_i == disp_i) and (actual == expected)
        ok = ok and row_ok
        rows.append({"payload": "payload[%s] (%s)" % (idx, name),
                     "documented_dest": "template+0x%02X" % dest_i,
                     "documented_instr_disp": disp_i,
                     "instr_va": "0x%08X" % va_i,
                     "expected_bytes": expected.hex(" ").upper(),
                     "actual_bytes": actual.hex(" ").upper(),
                     "dest_eq_disp": dest_i == disp_i,
                     "bytes_match": actual == expected,
                     "pass": row_ok})
    m = ROW_D.search(table_text)
    if m:
        fld_va, fstp_va = int(m.group(1), 16), int(m.group(2), 16)
        fld_ok = rd(fld_va, 3) == bytes([0xD9, 0x04, 0x10])
        fstp_ok = rd(fstp_va, 3) == bytes([0xD9, 0x5F, 0x10])
        ok = ok and fld_ok and fstp_ok
        rows.append({"payload": "payload[4] (D_f32)",
                     "documented_dest": "template+0x10 (FLD/FSTP)",
                     "instr_va": "FLD 0x%08X; FSTP 0x%08X" % (fld_va, fstp_va),
                     "expected_bytes": "D9 04 10 (FLD); D9 5F 10 (FSTP)",
                     "actual_bytes": "%s (FLD); %s (FSTP)" % (
                         rd(fld_va, 3).hex(" ").upper(), rd(fstp_va, 3).hex(" ").upper()),
                     "bytes_match": fld_ok and fstp_ok,
                     "pass": fld_ok and fstp_ok})
    else:
        ok = False
        rows.append({"payload": "payload[4] (D_f32)", "error": "D row not found", "pass": False})
    n_u32 = len([r for r in rows if r.get("payload", "").startswith("payload[") and "D_f32" not in r["payload"]])
    table_complete = n_u32 == 4
    return rows, ok and table_complete, table_complete

# ---------------------------------------------------------------- main checks
def run_checks(dexe, ib, secs, tpl_bytes):
    qc = {}
    def rd(va, n):
        return dexe[va_to_off(ib, secs, va): va_to_off(ib, secs, va) + n]
    def call_target(va):
        b = rd(va, 5)
        assert b[0] == 0xE8, "not a CALL at 0x%08X: %s" % (va, b.hex(" ").upper())
        return va + 5 + struct.unpack("<i", b[1:5])[0]
    def beq(va, expected, label):
        got = rd(va, len(expected))
        return {"pin": label, "va": "0x%08X" % va,
                "expected": bytes(expected).hex(" ").upper(),
                "actual": got.hex(" ").upper(), "ok": got == bytes(expected)}

    # TQ0 corpus identities
    qc["tq0_identities"] = {
        "exe_sha256": sha256_file(EXE),
        "exe_sha_match": sha256_file(EXE) == EXPECT["exe_sha"],
        "tpl_sha256": sha256_file(TPL),
        "tpl_sha_match": sha256_file(TPL) == EXPECT["tpl_sha"],
        "tpl_size": os.path.getsize(TPL),
        "tpl_size_match": os.path.getsize(TPL) == EXPECT["tpl_size"],
    }
    qc["tq0_identities"]["pass"] = (qc["tq0_identities"]["exe_sha_match"]
                                    and qc["tq0_identities"]["tpl_sha_match"]
                                    and qc["tq0_identities"]["tpl_size_match"])

    # TQ1 PAYLOAD_FIELD_DECODE_CHECK
    qc["tq1_payload_field_decode"] = tq1_payload_field_decode(tpl_bytes)

    # TQ2 CLIENT_DESTINATION_MAPPING_CHECK (corrected canonical doc)
    parser_chain = read_doc("PARSER_CHAIN.md")
    rows, dest_ok, complete = verify_destination_table(dexe, ib, secs, parser_chain)
    qc["tq2_client_destination_mapping"] = {
        "source": "corrected PARSER_CHAIN.md destination table (canonical repo file)",
        "rows": rows, "u32_rows_parsed": len(rows) - 1, "table_complete": complete,
        "pass": dest_ok}

    # TQ3 CLASS_SELECTOR vs PROPERTY_TAG
    t3 = {}
    t3["resolver_call_004C54B2"] = beq(0x004C54B2, [0xE8], "CALL start (resolver)")
    t3["resolver_call_target"] = {"target": "0x%08X" % call_target(0x004C54B2),
                                  "ok": call_target(0x004C54B2) == 0x00843DD0}
    t3["class_selector_store_004C54C2"] = beq(
        0x004C54C2, [0xC7, 0x44, 0x24, 0x1C, 0x26, 0x4E, 0x00, 0x00],
        "MOV [ESP+0x1C],0x4E26 (CLASS_SELECTOR 20006 pair constant)")
    t3["wrapper_call_004C54CE"] = beq(0x004C54CE, [0xE8], "wrapper CALL start")
    t3["wrapper_call_target"] = {"target": "0x%08X" % call_target(0x004C54CE),
                                 "ok": call_target(0x004C54CE) == 0x00703B80}
    t3["receiver_mov_004C551C"] = beq(0x004C551C, [0x8B, 0x48, 0x04],
                                      "MOV ECX,[EAX+4] (exact receiver)")
    t3["property_tag_push6_004C551F"] = beq(0x004C551F, [0x6A, 0x06],
                                            "PUSH 6 (PROPERTY_TAG 6)")
    t3["tag6_getter_call_004C5523"] = beq(0x004C5523, [0xE8], "tag-6 getter CALL start")
    t3["tag6_getter_target"] = {"target": "0x%08X" % call_target(0x004C5523),
                                "ok": call_target(0x004C5523) == 0x0070C180}
    t3["identity_arithmetic"] = {"0x4E26 == 20006": 0x4E26 == 20006,
                                 "6 != 20006": 6 != 20006,
                                 "6 != 0x4E26": 6 != 0x4E26,
                                 "distinct_sites": 0x004C54C2 != 0x004C551F}
    docs_cs, docs_pt = {}, {}
    for f in ("PLACEMENT_CONSUMER_EDGE.md", "FINAL_REPORT.md", "HANDOFF.md", "QC_REPORT.md"):
        t = read_doc(f)
        docs_cs[f] = ("CLASS_SELECTOR" in t) or ("class-selector-20006" in t) or ("class-selector 0x4E26" in t)
        docs_pt[f] = ("PROPERTY_TAG" in t) or ("property-tag-6" in t)
    t3["docs_layered_wording"] = {"class_selector_named": docs_cs,
                                  "property_tag_named": {k: v for k, v in docs_pt.items()
                                                         if k != "QC_REPORT.md"}}
    t3["pass"] = (all(v["ok"] for v in t3.values() if isinstance(v, dict) and "ok" in v)
                  and t3["resolver_call_target"]["ok"] and t3["wrapper_call_target"]["ok"]
                  and t3["tag6_getter_target"]["ok"]
                  and all(t3["identity_arithmetic"].values())
                  and all(docs_cs.values())
                  and all(t3["docs_layered_wording"]["property_tag_named"].values()))
    qc["tq3_class_selector_vs_property_tag"] = t3

    # TQ4 receiver provenance
    t4 = {}
    t4["wrapper_call_00452490"] = beq(0x00452490, [0xE8], "CALL FUN_0043A550 start")
    t4["wrapper_call_target"] = {"target": "0x%08X" % call_target(0x00452490),
                                 "ok": call_target(0x00452490) == 0x0043A550}
    t4["wrapper_mov_ecx_eax_00452495"] = beq(0x00452495, [0x8B, 0xC8], "MOV ECX,EAX")
    t4["wrapper_tail_jmp_00452497"] = beq(0x00452497, [0xE9], "tail JMP start")
    jmp_target = 0x00452497 + 5 + struct.unpack("<i", rd(0x00452498, 4))[0]
    t4["wrapper_jmp_target"] = {"target": "0x%08X" % jmp_target,
                                "ok": jmp_target == 0x0072FA30}
    t4["loader_preserve_0072FA6B"] = beq(0x0072FA6B, [0x89, 0x4C, 0x24, 0x38],
                                         "MOV [ESP+0x38],ECX (preserve incoming ECX)")
    t4["loader_recover_0072FBD4"] = beq(0x0072FBD4, [0x8B, 0x4C, 0x24, 0x3C],
                                         "MOV ECX,[ESP+0x3C] (recover before insert)")
    t4["insert_call_0072FBE5"] = beq(0x0072FBE5, [0xE8], "CALL FUN_0072F8D0 start")
    t4["insert_call_target"] = {"target": "0x%08X" % call_target(0x0072FBE5),
                                "ok": call_target(0x0072FBE5) == 0x0072F8D0}
    # bounded scan: NO call to FUN_0043A550 inside the loader extent
    LOADER_START, LOADER_END = 0x0072FA30, 0x0072FCA0
    hits = []
    for va in range(LOADER_START, LOADER_END - 5):
        if rd(va, 1) == b"\xE8":
            if va + 5 + struct.unpack("<i", rd(va + 1, 4))[0] == 0x0043A550:
                hits.append("0x%08X" % va)
    t4["loader_singleton_call_sites"] = {"extent": "0x0072FA30..0x0072FCA0",
                                         "count": len(hits), "sites": hits,
                                         "ok": len(hits) == 0}
    ric = read_doc("RECEIVER_INSERTION_CHAIN.md")
    t4["doc_wording"] = {
        "does_NOT_call_singleton": "does NOT itself call the singleton" in ric,
        "wrapper_chain_present": all(k in ric for k in
            ("@0x00452490", "@0x00452495", "@0x00452497", "@0x0072FA6B", "@0x0072FBD4")),
        "no_active_fetch_claim": retired_claim_residue(ric, r"fetches the registry via")[0] == [],
    }
    t4["pass"] = (all(v["ok"] for v in t4.values() if isinstance(v, dict) and "ok" in v)
                  and t4["wrapper_call_target"]["ok"] and t4["wrapper_jmp_target"]["ok"]
                  and t4["insert_call_target"]["ok"]
                  and t4["loader_singleton_call_sites"]["ok"]
                  and all(t4["doc_wording"].values()))
    qc["tq4_receiver_provenance"] = t4

    # TQ5 FUN_00730C90 failure-path ZERO-WRITE pins + FUN_0040DE60 flag semantics
    t5 = {}
    t5["xor_ebx_zero_00730C96"] = beq(0x00730C96, [0x33, 0xDB], "XOR EBX,EBX (zero source)")
    t5["zero_id2_00730CC3"] = beq(0x00730CC3, [0x89, 0x1F], "MOV [EDI],EBX")
    t5["zero_A_00730CF0"] = beq(0x00730CF0, [0x89, 0x5F, 0x08], "MOV [EDI+8],EBX")
    t5["zero_B_00730D1E"] = beq(0x00730D1E, [0x89, 0x5F, 0x04], "MOV [EDI+4],EBX")
    t5["zero_C_00730D4C"] = beq(0x00730D4C, [0x89, 0x5F, 0x0C], "MOV [EDI+0xC],EBX")
    t5["zero_D_flDz_00730D7A"] = beq(0x00730D7A, [0xD9, 0xEE], "FLDZ")
    t5["zero_D_fstp_00730D7C"] = beq(0x00730D7C, [0xD9, 0x5F, 0x10], "FSTP [EDI+0x10]")
    t5["f40de60_add"] = beq(0x0040DE64, [0x01, 0x41, 0x0C], "ADD [ECX+0xC],EAX")
    t5["f40de60_cmp"] = beq(0x0040DE6A, [0x3B, 0x41, 0x08], "CMP EAX,[ECX+8]")
    t5["f40de60_jbe"] = beq(0x0040DE6D, [0x76, 0x04], "JBE +4 (skip flag-zero)")
    t5["f40de60_flagzero"] = beq(0x0040DE6F, [0xC6, 0x41, 0x11, 0x00],
                                 "MOV BYTE [ECX+0x11],0 (flag zero on exceed)")
    pc = read_doc("PARSER_CHAIN.md")
    residue_samevalue = retired_claim_residue(pc, r"stores the same value")
    t5["doc_wording"] = {
        "zero_write_documented": all(k in pc for k in
            ("@0x00730CC3", "@0x00730CF0", "@0x00730D1E", "@0x00730D4C",
             "FLDZ", "ZEROES")),
        "fun_40de60_flag_zero_documented": "ZEROES the cursor flag" in pc,
        "retired_same_value_claim_only_in_retraction": len(residue_samevalue[0]) == 0,
        "retraction_quote_occurrences": len(residue_samevalue[1]),
    }
    t5["pass"] = (all(v["ok"] for v in t5.values() if isinstance(v, dict) and "ok" in v)
                  and t5["doc_wording"]["zero_write_documented"]
                  and t5["doc_wording"]["fun_40de60_flag_zero_documented"]
                  and t5["doc_wording"]["retired_same_value_claim_only_in_retraction"]
                  and t5["doc_wording"]["retraction_quote_occurrences"] >= 1)
    qc["tq5_failure_path_zero_write"] = t5

    # TQ6 instruction-start corrections (negative controls on the OLD wrong addresses)
    t6 = {"old_address_negative_controls": {}, "new_address_positive_controls": {}}
    for va, expected, label in [
        (0x00730D16, [0x89, 0x47, 0x04], "old B-store addr must NOT hold 89 47 04"),
        (0x00730D36, [0x89, 0x47, 0x0C], "old C-store addr must NOT hold 89 47 0C"),
        (0x00730D6D, [0xD9, 0x04, 0x10], "old FLD addr must NOT hold D9 04 10"),
        (0x0072F5A8, [0xB8], "old default addr must NOT hold B8 opcode"),
        (0x0072F825, [0xC7], "old node-size addr must NOT hold C7 opcode"),
        (0x004C54AD, [0xE8], "old resolver addr must NOT hold E8 opcode"),
    ]:
        t6["old_address_negative_controls"]["0x%08X" % va] = {
            "must_not_equal": bytes(expected).hex(" ").upper(),
            "actual": rd(va, len(expected)).hex(" ").upper(),
            "ok": rd(va, len(expected)) != bytes(expected)}
    for va, expected, label in [
        (0x00730D14, [0x89, 0x47, 0x04], "B store MOV [EDI+4],EAX @0x00730D14"),
        (0x00730D42, [0x89, 0x47, 0x0C], "C store MOV [EDI+0xC],EAX @0x00730D42"),
        (0x00730D69, [0xD9, 0x04, 0x10], "D FLD [EDX+EAX] @0x00730D69"),
        (0x00730D70, [0xD9, 0x5F, 0x10], "D FSTP [EDI+0x10] @0x00730D70"),
        (0x0072F5A5, [0xB8, 0x00, 0x58, 0xBA, 0x00], "MOV EAX,0x00BA5800 @0x0072F5A5"),
        (0x0072F822, [0xC7, 0x45, 0xEC, 0x44, 0x00, 0x00, 0x00],
         "MOV [EBP-0x14],0x44 @0x0072F822"),
        (0x004C54B2, [0xE8, 0x19, 0xE9, 0x37, 0x00], "resolver CALL @0x004C54B2"),
    ]:
        t6["new_address_positive_controls"]["0x%08X" % va] = {
            "label": label, "expected": bytes(expected).hex(" ").upper(),
            "actual": rd(va, len(expected)).hex(" ").upper(),
            "ok": rd(va, len(expected)) == bytes(expected)}
    t6["pass"] = (all(v["ok"] for v in t6["old_address_negative_controls"].values())
                  and all(v["ok"] for v in t6["new_address_positive_controls"].values()))
    qc["tq6_instruction_start_corrections"] = t6

    # TQ7 next-experiment wording
    TAXONOMY = ("PHYSICAL_RECORD_DERIVED | CONSTANT_INITIALIZATION | LOCAL_COMPUTED | "
                "CACHE_PROVIDER | MESSAGE_DERIVED | FALLBACK_BRANCH | UNKNOWN")
    def norm_ws(s):
        return " ".join(s.split())
    t7 = {}
    for f in ("FINAL_REPORT.md", "HANDOFF.md", "PLACEMENT_CONSUMER_EDGE.md"):
        t = read_doc(f)
        residues = retired_claim_residue(t, r"Decode the WRITERS of the 0x4E26")
        t7[f] = {
            "specific_getter_result_wording": ("SPECIFIC RUNTIME VALUE" in t
                                               and "class-selector-20006" in t
                                               and "property-tag-6" in t),
            "open_taxonomy_present": norm_ws(TAXONOMY) in norm_ws(t),
            "overbroad_writers_wording_active_claims": len(residues[0]),
            "retraction_quote_occurrences": len(residues[1]),
        }
    t7["pass"] = all(v["specific_getter_result_wording"] and v["open_taxonomy_present"]
                     and v["overbroad_writers_wording_active_claims"] == 0
                     for v in t7.values() if isinstance(v, dict))
    qc["tq7_next_experiment_wording"] = t7

    # TQ8 S1 canonical facts preserved
    fr = read_doc("FINAL_REPORT.md")
    ra_doc = read_doc("RECORD_A.md")
    rb_doc = read_doc("RECORD_B.md")
    pce = read_doc("PLACEMENT_CONSUMER_EDGE.md")
    t8 = {
        "docs": {
            "PARSER_TO_RUNTIME_VALUE_SEAM_CONFIRMED": "PARSER_TO_RUNTIME_VALUE_SEAM = CONFIRMED" in fr,
            "CONTAINER_ROLE_DEFINITION_REGISTRY": "CONTAINER_ROLE = DEFINITION_REGISTRY" in fr,
            "record_a_values": all(s in fr for s in
                ("16083", "410620", "0.49950098991394043")) and "B=0" in fr,
            "record_b_id_in_final_report": "4508" in fr,
            "record_b_values_pinned_in_record_b_doc": all(s in rb_doc for s in
                ("4508", "296445", "296446")),
            "record_a_doc_values": all(s in ra_doc for s in ("16083", "410620", "0.49950098991394043")),
            "sibling_key_static_push_documented": "PUSH 0x3ED3 @0x005B6597" in pce,
            "consumer_edge_still_strongly_supported": "PLACEMENT_CONSUMER_EDGE = STRONGLY_SUPPORTED" in pce,
        },
        "exe": {
            "push_3ed3_005B6597": beq(0x005B6597, [0x68, 0xD3, 0x3E, 0x00, 0x00],
                                      "PUSH 0x3ED3 (static sibling key)"),
            "call_5b5f90_target": {"target": "0x%08X" % call_target(0x005B659C),
                                   "ok": call_target(0x005B659C) == 0x005B5F90},
            "call_43a550_target": {"target": "0x%08X" % call_target(0x005B5FE8),
                                   "ok": call_target(0x005B5FE8) == 0x0043A550},
            "call_72f580_target": {"target": "0x%08X" % call_target(0x005B5FEF),
                                   "ok": call_target(0x005B5FEF) == 0x0072F580},
            "call_5670a0_target": {"target": "0x%08X" % call_target(0x005B5FFC),
                                   "ok": call_target(0x005B5FFC) == 0x005670A0},
        },
    }
    t8["pass"] = (all(t8["docs"].values())
                  and all(v["ok"] for v in t8["exe"].values() if isinstance(v, dict) and "ok" in v)
                  and t8["exe"]["call_5b5f90_target"]["ok"]
                  and t8["exe"]["call_43a550_target"]["ok"]
                  and t8["exe"]["call_72f580_target"]["ok"]
                  and t8["exe"]["call_5670a0_target"]["ok"])
    qc["tq8_s1_facts_preserved"] = t8

    # TQ9 forbidden overclaims / no-upgrade / corrected census wording
    ric = read_doc("RECEIVER_INSERTION_CHAIN.md")
    ho = read_doc("HANDOFF.md")
    t9 = {
        "no_upgrade_markers": {
            "PHYSICAL_RECORD_TO_PLACEMENT_ATTRIBUTE_NOT_ESTABLISHED":
                "PHYSICAL_RECORD_TO_PLACEMENT_ATTRIBUTE = NOT_ESTABLISHED" in fr,
            "WORLD_INSTANCE_SEMANTIC_NOT_ESTABLISHED":
                "WORLD_INSTANCE_SEMANTIC = NOT_ESTABLISHED" in fr,
            "WORLD_XYZ_RECOVERED_NO": "WORLD_XYZ_RECOVERED = NO" in fr,
            "named_builder_key_still_not_provable":
                "NOT statically provable" in fr,
        },
        "census_wording": {
            "proprietary_corrected": ("no complete original proprietary" in ho),
            "scan_4508_measured_scope": ("NOT excluded" in rb_doc
                                         and "measured scan" in rb_doc),
        },
        "no_value_changes": qc["tq1_payload_field_decode"]["pass"],
    }
    t9["pass"] = (all(t9["no_upgrade_markers"].values())
                  and all(t9["census_wording"].values()) and t9["no_value_changes"])
    qc["tq9_forbidden_overclaims_absent"] = t9

    # overall
    keys = [k for k in qc if k.startswith("tq")]
    qc["QC_VERDICT"] = "QC_PASS" if all(qc[k]["pass"] for k in keys) else "QC_FAIL"
    qc["QC_SCOPE"] = "SELF_CHECK_REPORT_QC_HANDOFF_CORRECTION"
    qc["checks_passed"] = sum(1 for k in keys if qc[k]["pass"])
    qc["checks_total"] = len(keys)
    return qc

# ---------------------------------------------------------------- mutation mode
def run_mutation(dexe, ib, secs, tpl_bytes):
    """A/B destination-documentation swap falsifier. Canonical repo files untouched:
    mutants live in a private temp copy of PARSER_CHAIN.md only."""
    out = {"QC_SCOPE": "SELF_CHECK_REPORT_QC_HANDOFF_CORRECTION",
           "falsifier": "AB_MAPPING_MUTATION_FALSIFIER",
           "design": ("Copy the corrected PARSER_CHAIN.md to a private temp file, swap the "
                      "documented A/B destination mapping, and re-run the SAME "
                      "CLIENT_DESTINATION_MAPPING_CHECK verifier against the UNCHANGED "
                      "pinned EXE and UNCHANGED templates.vfs. The check must FAIL for "
                      "both mutants. This reproduces and closes the Desktop QC-7 "
                      "counterexample class (a deliberate A/B documentation swap passed "
                      "the published QC-7).")}
    original = read_doc("PARSER_CHAIN.md")
    mutants = {}
    # mutant A — Desktop replica: destination cells only (exactly the two replaces
    # the Desktop qc_counterexample.py performed on the R1 table)
    ma = original.replace("| payload[1] (A) | template+0x08 |", "| payload[1] (A) | template+0x04 |")
    ma = ma.replace("| payload[2] (B) | template+0x04 |", "| payload[2] (B) | template+0x08 |")
    assert ma != original, "mutant A substitution did not apply"
    mutants["mutantA_destination_cell_only_desktop_replica"] = ma
    # mutant B — fully self-consistent swap: destination AND instruction displacement
    mb = original.replace(
        "| payload[1] (A) | template+0x08 | MOV [EDI+0x08],EAX @0x00730CE6 |",
        "| payload[1] (A) | template+0x04 | MOV [EDI+0x04],EAX @0x00730CE6 |")
    mb = mb.replace(
        "| payload[2] (B) | template+0x04 | MOV [EDI+0x04],EAX @0x00730D14 |",
        "| payload[2] (B) | template+0x08 | MOV [EDI+0x08],EAX @0x00730D14 |")
    assert mb != original, "mutant B substitution did not apply"
    mutants["mutantB_self_consistent_swap"] = mb

    tmpdir = tempfile.mkdtemp(prefix="pe935_c1_mutation_")
    try:
        results = {}
        for name, text in mutants.items():
            tmppath = os.path.join(tmpdir, "PARSER_CHAIN.md")
            with open(tmppath, "w", encoding="utf-8") as f:
                f.write(text)
            with open(tmppath, "r", encoding="utf-8") as f:
                reread = f.read()
            rows, ok, complete = verify_destination_table(dexe, ib, secs, reread)
            tq1 = tq1_payload_field_decode(tpl_bytes)
            failed_rows = [r["payload"] for r in rows if not r.get("pass", False)]
            results[name] = {
                "mutated_file": "temp copy of PARSER_CHAIN.md (canonical repo file untouched)",
                "mutated_rows": [ln for ln in reread.splitlines()
                                 if ln.startswith("| payload[1] ") or ln.startswith("| payload[2] ")],
                "raw_vfs_values_unchanged_tq1_pass": tq1["pass"],
                "destination_check_pass": ok,
                "destination_check_failed_rows": failed_rows,
                "expected": "FAIL (mutation must be detected)",
                "detected": (not ok) and tq1["pass"],
            }
        out["mutants"] = results
        out["AB_MAPPING_MUTATION_FALSIFIER"] = ("DETECTED"
            if all(r["detected"] for r in results.values()) else "NOT_DETECTED")
        out["pass"] = out["AB_MAPPING_MUTATION_FALSIFIER"] == "DETECTED"
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
    return out

# ---------------------------------------------------------------- byte-proof extraction
def exe_byte_proofs(dexe, ib, secs):
    def window(va, size, label):
        off = va_to_off(ib, secs, va)
        return {"label": label, "va": "0x%08X" % va, "size": size,
                "bytes": dexe[off:off + size].hex(" ").upper()}
    return {
        "exe_sha256": sha256_file(EXE),
        "windows": [
            window(0x00730C90, 0x130, "FUN_00730C90 parse body (stores + zero-writes + FLD/FSTP/FLDZ)"),
            window(0x0040DE60, 21, "FUN_0040DE60 cursor advance + flag zero on exceed"),
            window(0x004C54A0, 0x80, "FUN_004C5480 receiver resolve + class-selector pair + wrapper"),
            window(0x004C5510, 0x40, "FUN_004C5480 tag-6 getter (PUSH 6; CALL FUN_0070C180)"),
            window(0x00452490, 12, "FUN_00452490 wrapper (CALL FUN_0043A550; MOV ECX,EAX; JMP loader)"),
            window(0x0072FA58, 0x28, "loader prologue (preserve incoming ECX @0x0072FA6B)"),
            window(0x0072FBC0, 0x40, "loader insert region (recover ECX @0x0072FBD4; CALL FUN_0072F8D0 @0x0072FBE5)"),
            window(0x0072F580, 48, "FUN_0072F580 lookup (default MOV EAX,0x00BA5800 starts @0x0072F5A5)"),
            window(0x0072F815, 0x18, "FUN_0072F7F0 node-size MOV [EBP-0x14],0x44 starts @0x0072F822"),
            window(0x005B6590, 0x28, "FUN_005B6370 static key PUSH 0x3ED3 @0x005B6597 + CALL FUN_005B5F90"),
            window(0x005B5FE0, 0x28, "FUN_005B5F90 registry chain (FUN_0043A550/FUN_0072F580/FUN_005670A0)"),
        ],
    }

# ---------------------------------------------------------------- entry
def main():
    dexe, ib, secs = load_pe(EXE)
    tpl_bytes = open(TPL, "rb").read()
    mode = sys.argv[1] if len(sys.argv) > 1 else "normal"
    if mode == "normal":
        qc = run_checks(dexe, ib, secs, tpl_bytes)
        with open(os.path.join(RUN, "01_RAW", "QC_TARGETED.json"), "w") as f:
            json.dump({"measured": qc}, f, indent=1)
        proofs = exe_byte_proofs(dexe, ib, secs)
        with open(os.path.join(RUN, "01_RAW", "EXE_BYTE_PROOFS.json"), "w") as f:
            json.dump(proofs, f, indent=1)
        print(json.dumps({k: (v["pass"] if isinstance(v, dict) and "pass" in v else v)
                          for k, v in qc.items()}, indent=1))
    elif mode == "mutation":
        out = run_mutation(dexe, ib, secs, tpl_bytes)
        with open(os.path.join(RUN, "01_RAW", "QC_MUTATION_AB_SWAP.json"), "w") as f:
            json.dump({"measured": out}, f, indent=1)
        print(json.dumps({k: v for k, v in out.items() if k != "mutants"} | {
            "mutant_results": {n: {"destination_check_pass": r["destination_check_pass"],
                                   "detected": r["detected"]}
                               for n, r in out["mutants"].items()}}, indent=1))
    else:
        raise SystemExit("usage: qc_targeted.py [normal|mutation]")

if __name__ == "__main__":
    main()
