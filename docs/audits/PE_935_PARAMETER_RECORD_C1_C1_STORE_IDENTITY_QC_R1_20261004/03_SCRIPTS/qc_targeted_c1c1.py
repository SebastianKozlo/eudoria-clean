# qc_targeted_c1c1.py
# TARGETED QC — PE_935_PARAMETER_RECORD_C1_C1_STORE_IDENTITY_QC_R1_20261004
# QC_SCOPE = SELF_CHECK_C1_C1_STORE_IDENTITY (executor self-check; explicitly
# NOT an independent PE-MASTER audit).
#
# MISSION (bounded): fix EXACTLY the remaining C1-C1/P2 — the prior
# CLIENT_DESTINATION_MAPPING_CHECK (verify_destination_table in the C1-correction
# package 03_SCRIPTS/qc_targeted.py, published at BASE 97bdf95) confirms only that
# at the documented VA there exists an instruction writing the declared
# displacement. It does NOT prove payload index / field identity -> the correct
# store instruction -> the correct destination. Desktop mutant C (payload[1] row
# pointing at the REAL payload[2] store VA 0x00730D14 with a MATCHING
# displacement; payload[2] row pointing at the REAL payload[1] store VA
# 0x00730CE6) passes it undetected — the false PASS this run reproduces first
# (mode base_repro) and then closes.
#
# THE CORRECTED GATE validates THREE identities SIMULTANEOUSLY per payload
# field, ALL judged against an INDEPENDENT, HARD-CODED parser-sequence oracle
# (byte-backed at runtime from the pinned EXE + the pinned EXE SHA; the tested
# document is NEVER a source of truth for the mapping):
#   1. PAYLOAD FIELD IDENTITY: documented payload index == oracle payload index
#      AND documented semantic name == oracle audited field identity;
#   2. STORE INSTRUCTION IDENTITY: documented store VA == the store VA the
#      oracle independently assigns to that payload index (a REAL MOV with a
#      MATCHING displacement at the OTHER field's store VA FAILS — mutant C);
#   3. DESTINATION FIELD IDENTITY: documented destination == the destination of
#      that same independently assigned instruction (and the documented
#      instruction displacement == that destination).
# plus byte-backing (EXE bytes at the oracle VA == oracle instruction bytes) and
# table completeness (exactly one row per expected payload index, no unexpected
# payload rows, the D row present).
#
# Modes (all STATIC-ONLY; READ-ONLY vs Entropia.exe, templates.vfs, every
# canonical repo file, and the historical C1-correction package; private
# mutation copies live ONLY in the run temp dir and are deleted afterwards):
#   base_repro -> 01_RAW/BASE_MUTANT_C_REPRODUCTION.json
#       Reproduces the defect on the PRISTINE BASE historical verifier (imported
#       read-only): (a) BASE canonical QC (expect 10/10 QC_PASS), (b) BASE A/B
#       falsifier (expect DETECTED), (c) BASE mutant C on a PRIVATE doc copy
#       (expect TQ1 PASS + TQ2 PASS + FULL QC_PASS — the FALSE PASS).
#   normal     -> 01_RAW/QC_TARGETED.json
#       Corrected full QC (TQ0..TQ9 with the corrected TQ2 identity gate) on the
#       canonical document. Expected: QC_PASS.
#   battery    -> 01_RAW/QC_MUTATION_BATTERY_POST_FIX.json
#       POST-FIX mutation battery on PRIVATE doc copies: canonical copy (MUST
#       PASS — negative control proving a correct field-index/name/VA/destination
#       tuple passes), mutant A (MUST FAIL), mutant B (MUST FAIL), mutant C
#       (MUST FAIL). The full QC is re-run per case and FAILS whenever TQ2 fails.
#   oracle     -> 01_RAW/ORACLE_EVIDENCE.json
#       Byte evidence backing the hard-coded oracle (six pins + the normal
#       read/store sequence of FUN_00730C90 + the byte-identical FSTP twin note).
#
# ANTI-CIRCULARITY (explicit, per the dispatch contract):
#   MEASURED_QUANTITY = payload-index to exact-store-VA identity.
#   INDEPENDENT_SOURCE_OF_TRUTH = the pinned Entropia.exe bytes (SHA-pinned,
#     byte-verified at runtime) + the independently fixed normal parser
#     instruction order of FUN_00730C90 (each payload field is read in payload
#     order and its store follows; the six store/FLD/FSTP VAs below strictly
#     increase with payload index).
#   WHY_NON_CIRCULAR = the document row under test cannot choose an arbitrary
#     correct MOV and thereby change the payload-index identity: the expected
#     payload-index -> store-VA -> destination mapping is hard-coded in this
#     script BEFORE the tested document is read and is byte-backed from the
#     pinned EXE. The tested PARSER_CHAIN table is NEVER used to generate the
#     expected payload-index -> VA mapping.
#   FAILURE_CASE_DETECTED = Desktop mutant C (BASE false PASS:
#     01_RAW/BASE_MUTANT_C_REPRODUCTION.json; POST-FIX detection:
#     01_RAW/QC_MUTATION_BATTERY_POST_FIX.json).
#
# No client launch, no runtime execution, no network, no Ghidra.
import sys, os, json, re, struct, hashlib, tempfile, shutil, importlib.util
sys.dont_write_bytecode = True

RUN = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PARAMETER_RECORD_C1_C1_STORE_IDENTITY_QC_R1_20261004"
REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
R1_CANON = os.path.join(REPO, "docs", "audits", "PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004")
C1CORR = os.path.join(REPO, "docs", "audits",
                      "PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_C1_REPORT_QC_CORRECTION_R1_20261004")
HIST_QC = os.path.join(C1CORR, "03_SCRIPTS", "qc_targeted.py")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
TPL = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs"
TMPROOT = os.path.join(r"C:\Users\User\AppData\Local\Temp\opencode",
                       "PE_935_PARAMETER_RECORD_C1_C1_STORE_IDENTITY_QC_R1_20261004")

# module-level "current doc root" — the battery/base_repro point this at a
# private copy; normal mode leaves it at the canonical R1 package.
R1 = R1_CANON

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

# ---------------------------------------------------------------- INDEPENDENT
# PARSER-SEQUENCE ORACLE — HARD-CODED. Fixed from the audited FUN_00730C90
# normal read/store sequence of the pinned Entropia.exe, INDEPENDENTLY of the
# tested PARSER_CHAIN.md document (anti-circularity contract above). Byte-backed
# at runtime by verify_oracle(): the pinned-EXE SHA must match and the exact
# instruction bytes must be present at these VAs. These six VAs were byte-pinned
# by PE-MASTER at dispatch and independently re-verified by this run.
ORACLE_U32 = [
    {"idx": 0, "name": "id2", "store_va": 0x00730CB6, "dest": 0x00,
     "instr_bytes": [0x89, 0x07]},                       # MOV [EDI],EAX
    {"idx": 1, "name": "A",  "store_va": 0x00730CE6, "dest": 0x08,
     "instr_bytes": [0x89, 0x47, 0x08]},                 # MOV [EDI+0x08],EAX
    {"idx": 2, "name": "B",  "store_va": 0x00730D14, "dest": 0x04,
     "instr_bytes": [0x89, 0x47, 0x04]},                 # MOV [EDI+0x04],EAX
    {"idx": 3, "name": "C",  "store_va": 0x00730D42, "dest": 0x0C,
     "instr_bytes": [0x89, 0x47, 0x0C]},                 # MOV [EDI+0x0C],EAX
]
ORACLE_D = {"idx": 4, "name": "D_f32",
            "fld_va": 0x00730D69,  "fld_bytes": [0xD9, 0x04, 0x10],   # FLD [EDX+EAX]
            "fstp_va": 0x00730D70, "fstp_bytes": [0xD9, 0x5F, 0x10],  # FSTP [EDI+0x10]
            "dest": 0x10}
# The normal-path field reads (MOV EAX,[EDX+EAX] = 8B 04 10 / FLD D9 04 10) that
# immediately precede each store in the parser's payload order — recorded as
# oracle sequence evidence (read VA -> store VA adjacency per payload index).
ORACLE_READS = [
    {"idx": 0, "read_va": 0x00730CAB, "read_bytes": [0x8B, 0x04, 0x10]},
    {"idx": 1, "read_va": 0x00730CDF, "read_bytes": [0x8B, 0x04, 0x10]},
    {"idx": 2, "read_va": 0x00730D0D, "read_bytes": [0x8B, 0x04, 0x10]},
    {"idx": 3, "read_va": 0x00730D3B, "read_bytes": [0x8B, 0x04, 0x10]},
    {"idx": 4, "read_va": 0x00730D69, "read_bytes": [0xD9, 0x04, 0x10]},
]

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

R1_DOC_SET = ["PARSER_CHAIN.md", "PLACEMENT_CONSUMER_EDGE.md", "FINAL_REPORT.md",
              "HANDOFF.md", "QC_REPORT.md", "RECEIVER_INSERTION_CHAIN.md",
              "RECORD_A.md", "RECORD_B.md"]

def make_private_r1(tmpdir, parser_chain_text):
    """Private copy of ONLY the 8 top-level docs run_checks reads. The canonical
    repo files are NEVER touched; the mutation lives only in the private copy.
    Written with newline='\\n' so a private copy of the UNMUTATED canonical text is
    byte-identical to the canonical disk file (LF endings preserved) and each
    mutant document differs from the canonical by exactly its stated mutation."""
    priv = tempfile.mkdtemp(prefix="r1copy_", dir=tmpdir)
    for f in R1_DOC_SET:
        shutil.copyfile(os.path.join(R1_CANON, f), os.path.join(priv, f))
    if parser_chain_text is not None:
        with open(os.path.join(priv, "PARSER_CHAIN.md"), "w", encoding="utf-8",
                  newline="\n") as f:
            f.write(parser_chain_text)
    return priv

RETRACTION_MARKERS = ["SUPERSEDES", "supersedes", "SUPERSESSION", "was FALSE",
                      "was WRONG", "retract", "corrected from", "NOT @", "was @",
                      "C1-corrected", "C1/P3-corrected", "C2-corrected",
                      "P3-corrected", "corrected —"]

def retired_claim_residue(text, pattern):
    """Count occurrences of a retired claim that are NOT inside a retraction quote.
    Searches the FULL text (retired phrases may span line breaks), maps each hit
    to its line, and exempts a hit when any line within +/-3 lines contains a
    retraction marker (the supersession-quote evidence is REQUIRED to remain in
    the docs)."""
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

# ---------------------------------------------------------------- oracle byte-backing
def verify_oracle(dexe, ib, secs):
    """Fail-closed byte-backing of the HARD-CODED oracle against the pinned EXE.
    The oracle is INDEPENDENT of the tested document; if the pinned EXE does not
    carry these exact instruction bytes at these exact VAs, everything fails."""
    def rd(va, n):
        return dexe[va_to_off(ib, secs, va): va_to_off(ib, secs, va) + n]
    res = {"definition": "HARD-CODED parser-sequence oracle (03_SCRIPTS/qc_targeted_c1c1.py ORACLE_U32/ORACLE_D); NEVER derived from the tested document",
           "exe_sha256": sha256_file(EXE),
           "exe_sha_match": sha256_file(EXE) == EXPECT["exe_sha"],
           "pins": [], "reads": [], }
    for e in ORACLE_U32:
        exp = bytes(e["instr_bytes"])
        act = rd(e["store_va"], len(exp))
        res["pins"].append({"pin": "payload[%d] (%s) store" % (e["idx"], e["name"]),
                            "va": "0x%08X" % e["store_va"],
                            "expected": exp.hex(" ").upper(),
                            "actual": act.hex(" ").upper(),
                            "ok": act == exp})
    for key_va, key_bytes, label in [
            ("fld_va", ORACLE_D["fld_bytes"], "payload[4] (D_f32) FLD"),
            ("fstp_va", ORACLE_D["fstp_bytes"], "payload[4] (D_f32) FSTP")]:
        exp = bytes(key_bytes)
        act = rd(ORACLE_D[key_va], len(exp))
        res["pins"].append({"pin": label,
                            "va": "0x%08X" % ORACLE_D[key_va],
                            "expected": exp.hex(" ").upper(),
                            "actual": act.hex(" ").upper(),
                            "ok": act == exp})
    for e in ORACLE_READS:
        exp = bytes(e["read_bytes"])
        act = rd(e["read_va"], len(exp))
        res["reads"].append({"pin": "payload[%d] read" % e["idx"],
                             "va": "0x%08X" % e["read_va"],
                             "expected": exp.hex(" ").upper(),
                             "actual": act.hex(" ").upper(),
                             "ok": act == exp})
    store_vas = [e["store_va"] for e in ORACLE_U32] + [ORACLE_D["fld_va"], ORACLE_D["fstp_va"]]
    res["store_va_order_strictly_increasing_with_payload_index"] = all(
        store_vas[i] < store_vas[i + 1] for i in range(len(store_vas) - 1))
    res["pass"] = (res["exe_sha_match"]
                   and all(p["ok"] for p in res["pins"])
                   and all(p["ok"] for p in res["reads"])
                   and res["store_va_order_strictly_increasing_with_payload_index"])
    return res

# ---------------------------------------------------------------- TQ2 (CORRECTED)
ROW_U32 = re.compile(
    r"\| payload\[(\d+)\] \((id2|A|B|C)\) \| template\+0x([0-9A-Fa-f]{2}) \| "
    r"MOV \[EDI(?:\+0x([0-9A-Fa-f]{2}))?\],EAX @0x([0-9A-Fa-f]{8}) \|")
ROW_D = re.compile(
    r"\| payload\[4\] \(D_f32\) \| template\+0x10 \(FLD/FSTP\) \| "
    r"FLD \[EDX\+EAX\] @0x([0-9A-Fa-f]{8}); FSTP \[EDI\+0x10\] @0x([0-9A-Fa-f]{8}) \|")

def _oracle_owner_of_va(va):
    """Which payload index does this store VA belong to, per the oracle?"""
    for e in ORACLE_U32:
        if va == e["store_va"]:
            return e
    return None

def verify_destination_table_identity(dexe, ib, secs, table_text, oracle_backing):
    """CORRECTED CLIENT_DESTINATION_MAPPING_CHECK. Validates THREE identities
    SIMULTANEOUSLY per payload field, ALL judged against the INDEPENDENT
    hard-coded parser-sequence oracle — never against the document's own rows:
      PAYLOAD FIELD IDENTITY (documented idx == oracle idx; documented semantic
        name == oracle audited field identity)
      -> STORE INSTRUCTION IDENTITY (documented store VA == the store VA the
         oracle independently assigns to that payload index; a REAL MOV with a
         MATCHING displacement at a DIFFERENT VA — the other field's store —
         FAILS, closing Desktop mutant C)
      -> DESTINATION FIELD IDENTITY (documented destination == the destination
         of that same independently assigned instruction; documented instruction
         displacement == that destination).
    Plus byte-backing (oracle_backing['pass']) and completeness (exactly one row
    per expected payload index, no unexpected payload rows, the D row present).
    Returns (rows, identity_ok, table_ok, failed_rows_with_reasons)."""
    def rd(va, n):
        return dexe[va_to_off(ib, secs, va): va_to_off(ib, secs, va) + n]

    rows, failed_reasons = [], []
    # ---- parse documented u32 rows, grouped by documented payload index
    doc = {}
    for m in ROW_U32.finditer(table_text):
        idx, name, dest, disp, va = m.groups()
        doc.setdefault(int(idx), []).append({
            "name": name,
            "dest": int(dest, 16),
            "disp": int(disp, 16) if disp else 0,
            "va": int(va, 16),
            "row_text": m.group(0)})
    identity_ok = True
    table_ok = oracle_backing["pass"]   # the corrected gate is byte-backed or nothing

    # ---- completeness: exactly the expected payload indices, no extras
    expected_idx = set(e["idx"] for e in ORACLE_U32)
    documented_idx = set(doc.keys())
    for extra in sorted(documented_idx - expected_idx):
        table_ok = False
        failed_reasons.append(
            "documented payload[%d] row is NOT in the expected payload-index set "
            "%s (unexpected row)" % (extra, sorted(expected_idx)))

    # ---- per-oracle-entry identity checks
    for e in ORACLE_U32:
        matches = doc.get(e["idx"], [])
        exp_va = e["store_va"]
        exp_dest = e["dest"]
        reasons = []
        if len(matches) == 0:
            reasons.append("MISSING documented row for payload[%d] (%s) — the "
                           "oracle expects a row for every payload field"
                           % (e["idx"], e["name"]))
        elif len(matches) > 1:
            reasons.append("DUPLICATE documented rows for payload[%d] (%s): %d rows"
                           % (e["idx"], e["name"], len(matches)))
        else:
            r = matches[0]
            if r["name"] != e["name"]:
                reasons.append(
                    "documented semantic name '%s' != oracle audited field identity "
                    "'%s' for payload[%d]" % (r["name"], e["name"], e["idx"]))
            if r["va"] != exp_va:
                owner = _oracle_owner_of_va(r["va"])
                if owner is not None:
                    reasons.append(
                        "STORE INSTRUCTION IDENTITY FAIL: documented store VA 0x%08X "
                        "is the store of payload[%d] (%s) per the independent "
                        "parser-sequence oracle, NOT the store of payload[%d] (%s) "
                        "(oracle assigns payload[%d] (%s) store VA 0x%08X, bytes %s)"
                        % (r["va"], owner["idx"], owner["name"], e["idx"], e["name"],
                           e["idx"], e["name"], exp_va,
                           bytes(e["instr_bytes"]).hex(" ").upper()))
                else:
                    reasons.append(
                        "STORE INSTRUCTION IDENTITY FAIL: documented store VA 0x%08X "
                        "is NOT the store of payload[%d] (%s) per the independent "
                        "parser-sequence oracle (expected store VA 0x%08X, bytes %s)"
                        % (r["va"], e["idx"], e["name"], exp_va,
                           bytes(e["instr_bytes"]).hex(" ").upper()))
            if r["dest"] != exp_dest:
                reasons.append(
                    "DESTINATION FIELD IDENTITY FAIL: documented destination "
                    "template+0x%02X != oracle destination template+0x%02X for "
                    "payload[%d] (%s)" % (r["dest"], exp_dest, e["idx"], e["name"]))
            if r["disp"] != exp_dest:
                reasons.append(
                    "documented instruction displacement 0x%02X != oracle destination "
                    "0x%02X of payload[%d] (%s)'s assigned store instruction"
                    % (r["disp"], exp_dest, e["idx"], e["name"]))
        # evidence: what the OLD (BASE) row check would have concluded for the
        # single-row case — the deceptive property of mutant C is that this is
        # TRUE while the identity fails.
        old_pass = None
        doc_bytes = None
        if len(matches) == 1:
            r = matches[0]
            expected_old = (bytes([0x89, 0x07]) if r["dest"] == 0
                            else bytes([0x89, 0x47, r["dest"]]))
            doc_bytes = rd(r["va"], len(expected_old))
            old_pass = (r["dest"] == r["disp"]) and (doc_bytes == expected_old)
        row_ok = len(reasons) == 0
        rows.append({
            "payload": "payload[%d] (%s)" % (e["idx"], e["name"]),
            "expected_oracle": {"payload_index": e["idx"], "name": e["name"],
                                "store_va": "0x%08X" % exp_va,
                                "destination": "template+0x%02X" % exp_dest,
                                "instr_bytes": bytes(e["instr_bytes"]).hex(" ").upper()},
            "documented": ({"row_text": matches[0]["row_text"],
                            "name": matches[0]["name"],
                            "dest": "template+0x%02X" % matches[0]["dest"],
                            "disp": "0x%02X" % matches[0]["disp"],
                            "store_va": "0x%08X" % matches[0]["va"]}
                           if len(matches) == 1 else
                           {"row_texts": [x["row_text"] for x in matches]}
                           if len(matches) > 1 else None),
            "bytes_at_documented_va": (doc_bytes.hex(" ").upper()
                                      if doc_bytes is not None else None),
            "old_base_row_check_would_pass": old_pass,
            "identity_pass": row_ok,
            "reasons": reasons,
            "pass": row_ok})
        if not row_ok:
            identity_ok = False
            table_ok = False
            failed_reasons.extend(
                "payload[%d] (%s): %s" % (e["idx"], e["name"], x) for x in reasons)

    # ---- D row (payload[4] D_f32): oracle-fixed FLD/FSTP VA identity
    m = ROW_D.search(table_text)
    d_reasons = []
    if m:
        fld_va, fstp_va = int(m.group(1), 16), int(m.group(2), 16)
        if fld_va != ORACLE_D["fld_va"]:
            d_reasons.append(
                "STORE INSTRUCTION IDENTITY FAIL (FLD): documented FLD VA 0x%08X != "
                "oracle FLD VA 0x%08X for payload[4] (D_f32)"
                % (fld_va, ORACLE_D["fld_va"]))
        if fstp_va != ORACLE_D["fstp_va"]:
            d_reasons.append(
                "STORE INSTRUCTION IDENTITY FAIL (FSTP): documented FSTP VA 0x%08X != "
                "oracle FSTP VA 0x%08X for payload[4] (D_f32)"
                % (fstp_va, ORACLE_D["fstp_va"]))
    else:
        d_reasons.append("MISSING documented row for payload[4] (D_f32)")
        fld_va = fstp_va = None
    d_ok = len(d_reasons) == 0
    rows.append({
        "payload": "payload[4] (D_f32)",
        "expected_oracle": {"payload_index": 4, "name": "D_f32",
                            "fld_va": "0x%08X" % ORACLE_D["fld_va"],
                            "fstp_va": "0x%08X" % ORACLE_D["fstp_va"],
                            "destination": "template+0x10 (FLD/FSTP)",
                            "fld_bytes": bytes(ORACLE_D["fld_bytes"]).hex(" ").upper(),
                            "fstp_bytes": bytes(ORACLE_D["fstp_bytes"]).hex(" ").upper()},
        "documented": ({"fld_va": "0x%08X" % fld_va, "fstp_va": "0x%08X" % fstp_va}
                       if fld_va is not None else None),
        "identity_pass": d_ok,
        "reasons": d_reasons,
        "pass": d_ok})
    if not d_ok:
        identity_ok = False
        table_ok = False
        failed_reasons.extend("payload[4] (D_f32): %s" % x for x in d_reasons)

    return rows, identity_ok, table_ok, failed_reasons

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

    # TQ2 CLIENT_DESTINATION_MAPPING_CHECK (CORRECTED — three simultaneous
    # identities against the independent hard-coded parser-sequence oracle)
    oracle_backing = verify_oracle(dexe, ib, secs)
    parser_chain = read_doc("PARSER_CHAIN.md")
    rows, identity_ok, table_ok, failed_reasons = verify_destination_table_identity(
        dexe, ib, secs, parser_chain, oracle_backing)
    qc["tq2_client_destination_mapping"] = {
        "source": "PARSER_CHAIN.md destination table (document under test)",
        "independent_oracle": (
            "HARD-CODED parser-sequence oracle in this script, byte-backed from the "
            "pinned Entropia.exe (see 01_RAW/ORACLE_EVIDENCE.json); NEVER derived "
            "from the tested document — the document cannot supply the mapping"),
        "anti_circularity": {
            "MEASURED_QUANTITY": "payload-index to exact-store-VA identity",
            "INDEPENDENT_SOURCE_OF_TRUTH": (
                "pinned Entropia.exe bytes (SHA "
                + EXPECT["exe_sha"][:16] + "... byte-verified) + the independently "
                "fixed normal parser instruction order of FUN_00730C90"),
            "WHY_NON_CIRCULAR": (
                "the document row under test cannot choose an arbitrary correct MOV "
                "and thereby change the payload-index identity"),
            "FAILURE_CASE_DETECTED": "Desktop mutant C (payload[1] row pointed at "
                                     "the REAL payload[2] store 0x00730D14 with "
                                     "matching displacement, and vice versa)"},
        "oracle_byte_backing": oracle_backing,
        "rows": rows,
        "PAYLOAD_INDEX_STORE_IDENTITY_CHECK": identity_ok,
        "CLIENT_DESTINATION_MAPPING_CHECK": table_ok,
        "failed_rows_with_reasons": failed_reasons,
        "pass": identity_ok and table_ok,
    }

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

    # overall — FULL_QC FAILS whenever TQ2 (the mapping check) fails
    keys = [k for k in qc if k.startswith("tq")]
    qc["QC_VERDICT"] = "QC_PASS" if all(qc[k]["pass"] for k in keys) else "QC_FAIL"
    qc["QC_SCOPE"] = "SELF_CHECK_C1_C1_STORE_IDENTITY"
    qc["checks_passed"] = sum(1 for k in keys if qc[k]["pass"])
    qc["checks_total"] = len(keys)
    return qc

# ---------------------------------------------------------------- canonical table rows
CANON_ROW_A = "| payload[1] (A) | template+0x08 | MOV [EDI+0x08],EAX @0x00730CE6 |"
CANON_ROW_B = "| payload[2] (B) | template+0x04 | MOV [EDI+0x04],EAX @0x00730D14 |"

def build_mutants(original):
    """The three historical + mandatory mutants, EXACT text substitutions on the
    canonical destination rows (and nothing else)."""
    # MUTANT A — destination-cell-only swap (Desktop replica)
    ma = original.replace("| payload[1] (A) | template+0x08 |", "| payload[1] (A) | template+0x04 |")
    ma = ma.replace("| payload[2] (B) | template+0x04 |", "| payload[2] (B) | template+0x08 |")
    assert ma != original and "| payload[1] (A) | template+0x04 |" in ma, "mutant A substitution did not apply"
    # MUTANT B — destination+displacement swap, OLD store VAs kept
    mb = original.replace(
        "| payload[1] (A) | template+0x08 | MOV [EDI+0x08],EAX @0x00730CE6 |",
        "| payload[1] (A) | template+0x04 | MOV [EDI+0x04],EAX @0x00730CE6 |")
    mb = mb.replace(
        "| payload[2] (B) | template+0x04 | MOV [EDI+0x04],EAX @0x00730D14 |",
        "| payload[2] (B) | template+0x08 | MOV [EDI+0x08],EAX @0x00730D14 |")
    assert mb != original and "MOV [EDI+0x04],EAX @0x00730CE6" in mb, "mutant B substitution did not apply"
    # MUTANT C — the C1-C1 defect class: destination+displacement+MATCHING REAL
    # STORE VA swap — each row now points at the OTHER field's REAL store
    # (payload[1](A)->template+0x04->@0x00730D14; payload[2](B)->template+0x08->
    # @0x00730CE6). Both VAs are REAL stores with MATCHING displacements.
    mc = original.replace(CANON_ROW_A,
        "| payload[1] (A) | template+0x04 | MOV [EDI+0x04],EAX @0x00730D14 |")
    mc = mc.replace(CANON_ROW_B,
        "| payload[2] (B) | template+0x08 | MOV [EDI+0x08],EAX @0x00730CE6 |")
    assert mc != original and "MOV [EDI+0x04],EAX @0x00730D14" in mc, "mutant C substitution did not apply"
    assert "payload[1] (A) | template+0x04 | MOV [EDI+0x04],EAX @0x00730D14" in mc
    assert "payload[2] (B) | template+0x08 | MOV [EDI+0x08],EAX @0x00730CE6" in mc
    return ma, mb, mc

def mutated_rows_of(text):
    return [ln.strip() for ln in text.splitlines()
            if ln.strip().startswith("| payload[1] ") or ln.strip().startswith("| payload[2] ")]

# ---------------------------------------------------------------- base_repro mode
def run_base_repro(dexe, ib, secs, tpl_bytes):
    """Reproduce the C1-C1/P2 defect on the PRISTINE BASE historical verifier
    (imported READ-ONLY from the C1-correction package). Historical package and
    canonical repo files are NEVER modified; the mutant C document exists only
    as a private temp copy that the historical verifier is pointed at."""
    out = {
        "QC_SCOPE": "SELF_CHECK_C1_C1_STORE_IDENTITY",
        "falsifier": "BASE_MUTANT_C_FALSE_PASS_REPRODUCTION",
        "design": (
            "On the pristine BASE (97bdf959cb742490a0e974bddf5a2dd25f93f5f7) "
            "historical CLIENT_DESTINATION_MAPPING_CHECK verifier, swap ONLY the "
            "destination documentation: payload[1](A) -> template+0x04 -> MOV "
            "[EDI+0x04],EAX @0x00730D14 AND payload[2](B) -> template+0x08 -> MOV "
            "[EDI+0x08],EAX @0x00730CE6 — both VAs are REAL stores with MATCHING "
            "displacements belonging to the OTHER payload field. EXE unchanged, "
            "VFS unchanged, canonical docs unchanged. Expected BASE behavior: "
            "PAYLOAD_FIELD_DECODE_CHECK=PASS, CLIENT_DESTINATION_MAPPING_CHECK=PASS, "
            "FULL_QC=QC_PASS — the FALSE PASS (the C1-C1/P2 defect)."),
        "historical_instrument": {
            "path": "docs/audits/PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_C1_REPORT_QC_CORRECTION_R1_20261004/03_SCRIPTS/qc_targeted.py",
            "sha256": sha256_file(HIST_QC),
            "imported_read_only": True,
            "unmodified_base_verifier": True,
        },
        "inputs": {
            "exe_sha256": sha256_file(EXE),
            "exe_sha_match": sha256_file(EXE) == EXPECT["exe_sha"],
            "tpl_sha256": sha256_file(TPL),
            "tpl_sha_match": sha256_file(TPL) == EXPECT["tpl_sha"],
            "canonical_parser_chain_sha256": sha256_file(os.path.join(R1_CANON, "PARSER_CHAIN.md")),
        },
    }
    # import the historical script READ-ONLY (no bytecode written)
    assert sys.dont_write_bytecode
    spec = importlib.util.spec_from_file_location("qc_targeted_base", HIST_QC)
    hist = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hist)

    # (a) BASE canonical behavior — pristine QC state
    qc_a = hist.run_checks(dexe, ib, secs, tpl_bytes)
    out["base_canonical_qc"] = {
        "QC_VERDICT": qc_a["QC_VERDICT"],
        "checks_passed": qc_a["checks_passed"],
        "checks_total": qc_a["checks_total"],
        "tq1_payload_field_decode_pass": qc_a["tq1_payload_field_decode"]["pass"],
        "tq2_client_destination_mapping_pass": qc_a["tq2_client_destination_mapping"]["pass"],
    }
    # (b) BASE A/B mutation falsifier — the published detection scope
    mut_b = hist.run_mutation(dexe, ib, secs, tpl_bytes)
    out["base_ab_mutation_falsifier"] = {
        "AB_MAPPING_MUTATION_FALSIFIER": mut_b["AB_MAPPING_MUTATION_FALSIFIER"],
        "mutantA_detected": mut_b["mutants"]["mutantA_destination_cell_only_desktop_replica"]["detected"],
        "mutantB_detected": mut_b["mutants"]["mutantB_self_consistent_swap"]["detected"],
    }

    # (c) BASE mutant C — the defect: expect the FALSE PASS
    original = hist.read_doc("PARSER_CHAIN.md")
    ma, mb, mc = build_mutants(original)
    del ma, mb  # only mutant C is the BASE reproduction input
    os.makedirs(TMPROOT, exist_ok=True)
    tmpdir = tempfile.mkdtemp(prefix="pe935_c1c1_baserepro_", dir=TMPROOT)
    try:
        priv = make_private_r1(tmpdir, mc)
        mutated_sha = sha256_file(os.path.join(priv, "PARSER_CHAIN.md"))
        saved_r1 = hist.R1
        hist.R1 = priv
        try:
            qc_c = hist.run_checks(dexe, ib, secs, tpl_bytes)
        finally:
            hist.R1 = saved_r1
        tq2 = qc_c["tq2_client_destination_mapping"]
        false_pass = (qc_c["tq1_payload_field_decode"]["pass"]
                      and tq2["pass"] and qc_c["QC_VERDICT"] == "QC_PASS")
        out["base_mutant_c"] = {
            "mutation_text": (
                "payload[1](A) row -> template+0x04 -> MOV [EDI+0x04],EAX @0x00730D14; "
                "payload[2](B) row -> template+0x08 -> MOV [EDI+0x08],EAX @0x00730CE6 "
                "(both VAs REAL stores with MATCHING displacements belonging to the "
                "OTHER payload field)"),
            "mutated_parser_chain_sha256": mutated_sha,
            "mutated_rows": mutated_rows_of(mc),
            "raw_vfs_values_unchanged": qc_c["tq1_payload_field_decode"]["pass"],
            "PAYLOAD_FIELD_DECODE_CHECK": ("PASS" if qc_c["tq1_payload_field_decode"]["pass"] else "FAIL"),
            "CLIENT_DESTINATION_MAPPING_CHECK": ("PASS" if tq2["pass"] else "FAIL"),
            "tq2_row_results": [
                {"payload": r["payload"],
                 "documented_dest": r.get("documented_dest"),
                 "documented_instr_disp": r.get("documented_instr_disp"),
                 "instr_va": r.get("instr_va"),
                 "bytes_match": r.get("bytes_match"),
                 "dest_eq_disp": r.get("dest_eq_disp"),
                 "pass": r.get("pass")}
                for r in tq2["rows"]],
            "FULL_QC": qc_c["QC_VERDICT"],
            "checks_passed": qc_c["checks_passed"],
            "checks_total": qc_c["checks_total"],
            "expected_base_behavior": {
                "PAYLOAD_FIELD_DECODE_CHECK": "PASS",
                "CLIENT_DESTINATION_MAPPING_CHECK": "PASS (the FALSE PASS — the defect)",
                "FULL_QC": "QC_PASS (the FALSE PASS — the defect)"},
            "false_pass_reproduced": false_pass,
        }
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
    out["BASE_MUTANT_C_FALSE_PASS_REPRODUCED"] = "YES" if false_pass else "NO"
    out["pass"] = false_pass
    return out

# ---------------------------------------------------------------- battery mode
def run_battery(dexe, ib, secs, tpl_bytes):
    """POST-FIX mutation battery against the CORRECTED gate. Canonical repo files
    untouched: every case is a PRIVATE temp copy of the 8 R1 docs with only
    PARSER_CHAIN.md text-mutated. The full QC is re-run per case; FULL_QC FAILS
    whenever TQ2 fails."""
    global R1
    out = {
        "QC_SCOPE": "SELF_CHECK_C1_C1_STORE_IDENTITY",
        "falsifier": "POST_FIX_MUTATION_BATTERY (canonical negative control + mutants A/B/C)",
        "design": (
            "Run the CORRECTED CLIENT_DESTINATION_MAPPING_CHECK (three simultaneous "
            "identities against the independent hard-coded parser-sequence oracle) "
            "against: (0) an unmutated private copy of the canonical document (MUST "
            "PASS — negative control proving a correct field-index/name/VA/"
            "destination tuple passes); (A) destination-cell-only swap (MUST FAIL); "
            "(B) destination+displacement swap with the OLD VAs (MUST FAIL); (C) "
            "destination+displacement+MATCHING REAL STORE VA swap — each row at the "
            "OTHER field's real store (MUST FAIL; the class the BASE verifier passed "
            "undetected). Raw VFS values stay unchanged in every case; the full QC "
            "is re-run per case and must FAIL whenever TQ2 fails."),
        "inputs": {
            "exe_sha256": sha256_file(EXE),
            "tpl_sha256": sha256_file(TPL),
            "canonical_parser_chain_sha256": sha256_file(os.path.join(R1_CANON, "PARSER_CHAIN.md")),
        },
    }
    original = read_doc_canonical("PARSER_CHAIN.md")
    ma, mb, mc = build_mutants(original)
    cases = [
        ("canonical_copy_negative_control",
         "unmutated private copy of the canonical document (nothing replaced)",
         original, [], "PASS"),
        ("mutantA_destination_cell_only",
         "destination cells swapped only (Desktop replica): payload[1] dest +0x04 / payload[2] dest +0x08, instruction cells unchanged",
         ma, mutated_rows_of(ma), "FAIL"),
        ("mutantB_destination_disp_old_va",
         "destination+displacement swap with the OLD store VAs kept (@0x00730CE6 / @0x00730D14)",
         mb, mutated_rows_of(mb), "FAIL"),
        ("mutantC_destination_disp_real_store_va_swap",
         "destination+displacement+MATCHING REAL STORE VA swap: payload[1](A)->template+0x04->MOV [EDI+0x04],EAX @0x00730D14; payload[2](B)->template+0x08->MOV [EDI+0x08],EAX @0x00730CE6 (each row at the OTHER payload field's REAL store)",
         mc, mutated_rows_of(mc), "FAIL"),
    ]
    os.makedirs(TMPROOT, exist_ok=True)
    tmpdir = tempfile.mkdtemp(prefix="pe935_c1c1_battery_", dir=TMPROOT)
    results = {}
    try:
        for name, desc, text, mrows, expected in cases:
            priv = make_private_r1(tmpdir, text)
            doc_sha = sha256_file(os.path.join(priv, "PARSER_CHAIN.md"))
            saved = R1
            R1 = priv
            try:
                qc = run_checks(dexe, ib, secs, tpl_bytes)
            finally:
                R1 = saved
            tq2 = qc["tq2_client_destination_mapping"]
            tq1_pass = qc["tq1_payload_field_decode"]["pass"]
            detected = (not tq2["pass"]) and tq1_pass
            results[name] = {
                "description": desc,
                "document_sha256": doc_sha,
                "mutated_rows": mrows,
                "PAYLOAD_FIELD_DECODE_CHECK": "PASS" if tq1_pass else "FAIL",
                "PAYLOAD_INDEX_STORE_IDENTITY_CHECK": ("PASS" if tq2["PAYLOAD_INDEX_STORE_IDENTITY_CHECK"] else "FAIL"),
                "CLIENT_DESTINATION_MAPPING_CHECK": ("PASS" if tq2["CLIENT_DESTINATION_MAPPING_CHECK"] else "FAIL"),
                "per_row_reasons": [r for r in tq2["failed_rows_with_reasons"]],
                "FULL_QC": qc["QC_VERDICT"],
                "expected": expected,
                "detected": detected,
            }
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
    out["cases"] = results
    det = results
    out["MUTANT_A_DETECTED"] = "YES" if det["mutantA_destination_cell_only"]["detected"] else "NO"
    out["MUTANT_B_DETECTED"] = "YES" if det["mutantB_destination_disp_old_va"]["detected"] else "NO"
    out["MUTANT_C_POST_FIX_DETECTED"] = "YES" if det["mutantC_destination_disp_real_store_va_swap"]["detected"] else "NO"
    out["canonical_negative_control_pass"] = det["canonical_copy_negative_control"]["CLIENT_DESTINATION_MAPPING_CHECK"] == "PASS"
    out["battery_pass"] = (out["MUTANT_A_DETECTED"] == "YES"
                           and out["MUTANT_B_DETECTED"] == "YES"
                           and out["MUTANT_C_POST_FIX_DETECTED"] == "YES"
                           and out["canonical_negative_control_pass"])
    out["pass"] = out["battery_pass"]
    return out

def read_doc_canonical(relname):
    with open(os.path.join(R1_CANON, relname), "r", encoding="utf-8") as f:
        return f.read()

# ---------------------------------------------------------------- oracle mode
def oracle_evidence(dexe, ib, secs):
    def window(va, size, label):
        off = va_to_off(ib, secs, va)
        return {"label": label, "va": "0x%08X" % va, "size": size,
                "bytes": dexe[off:off + size].hex(" ").upper()}
    backing = verify_oracle(dexe, ib, secs)
    def rd(va, n):
        return dexe[va_to_off(ib, secs, va): va_to_off(ib, secs, va) + n]
    return {
        "oracle_definition": (
            "HARD-CODED in 03_SCRIPTS/qc_targeted_c1c1.py (ORACLE_U32/ORACLE_D/"
            "ORACLE_READS): payload-index -> exact store instruction VA -> "
            "destination template offset -> expected instruction bytes"),
        "independent_source_of_truth": (
            "pinned Entropia.exe bytes (SHA256 " + EXPECT["exe_sha"] + ") + the "
            "independently fixed normal parser instruction order of FUN_00730C90 "
            "(payload fields are read in payload order; each store follows its "
            "read; the six store/FLD/FSTP VAs strictly increase with payload index)"),
        "why_non_circular": (
            "the expected payload-index -> VA mapping is fixed BEFORE and "
            "INDEPENDENT of the tested document and is byte-backed from the "
            "pinned EXE; the tested PARSER_CHAIN table is NEVER used to generate "
            "the expected mapping; a document row pointing at ANY other real MOV "
            "with the right displacement FAILS, because the oracle fixes which "
            "store VA belongs to which payload index"),
        "failure_case_detected": (
            "Desktop mutant C — BASE false PASS reproduced in "
            "01_RAW/BASE_MUTANT_C_REPRODUCTION.json; POST-FIX detection in "
            "01_RAW/QC_MUTATION_BATTERY_POST_FIX.json"),
        "oracle_byte_backing": backing,
        "normal_read_store_sequence": {
            "payload[0] id2":  {"read": "MOV EAX,[EDX+EAX] @0x00730CAB (8B 04 10)",
                                "store": "MOV [EDI],EAX @0x00730CB6 (89 07) -> template+0x00",
                                "zero_path": "MOV [EDI],EBX @0x00730CC3 (89 1F)"},
            "payload[1] A":    {"read": "MOV EAX,[EDX+EAX] @0x00730CDF (8B 04 10)",
                                "store": "MOV [EDI+0x08],EAX @0x00730CE6 (89 47 08) -> template+0x08",
                                "zero_path": "MOV [EDI+8],EBX @0x00730CF0 (89 5F 08)"},
            "payload[2] B":    {"read": "MOV EAX,[EDX+EAX] @0x00730D0D (8B 04 10)",
                                "store": "MOV [EDI+0x04],EAX @0x00730D14 (89 47 04) -> template+0x04",
                                "zero_path": "MOV [EDI+4],EBX @0x00730D1E (89 5F 04)"},
            "payload[3] C":    {"read": "MOV EAX,[EDX+EAX] @0x00730D3B (8B 04 10)",
                                "store": "MOV [EDI+0x0C],EAX @0x00730D42 (89 47 0C) -> template+0x0C",
                                "zero_path": "MOV [EDI+0xC],EBX @0x00730D4C (89 5F 0C)"},
            "payload[4] D_f32": {"read": "FLD [EDX+EAX] @0x00730D69 (D9 04 10)",
                                 "store": "FSTP [EDI+0x10] @0x00730D70 (D9 5F 10) -> template+0x10",
                                 "zero_path": "FLDZ @0x00730D7A (D9 EE) + FSTP [EDI+0x10] @0x00730D7C (D9 5F 10)"}},
        "byte_identical_fstp_twin_note": (
            "FSTP [EDI+0x10] (D9 5F 10) appears TWICE in FUN_00730C90: the normal "
            "store @0x00730D70 and the zero-path store @0x00730D7C — byte-identical. "
            "A document row pointing the D store at 0x00730D7C would ALSO have "
            "passed the BASE verifier (same bytes); only the VA identity of the "
            "corrected oracle rejects it. Recorded as an additional closed class; "
            "not part of the A/B/C battery."),
        "byte_windows": [
            window(0x00730C90, 0x130, "FUN_00730C90 parse body (reads + stores + zero-writes + FLD/FSTP/FLDZ)"),
            window(0x00730CA9, 0x24, "payload[0] id2 block: read @0x00730CAB; store @0x00730CB6; zero @0x00730CC3"),
            window(0x00730CDD, 0x1F, "payload[1] A block: read @0x00730CDF; store @0x00730CE6; zero @0x00730CF0"),
            window(0x00730D0B, 0x17, "payload[2] B block: read @0x00730D0D; store @0x00730D14; zero @0x00730D1E"),
            window(0x00730D39, 0x1B, "payload[3] C block: read @0x00730D3B; store @0x00730D42; zero @0x00730D4C"),
            window(0x00730D67, 0x19, "payload[4] D_f32 block: FLD @0x00730D69; FSTP @0x00730D70; FLDZ @0x00730D7A; zero-FSTP @0x00730D7C"),
        ],
        "exe_sha256": sha256_file(EXE),
        "pass": backing["pass"],
    }

# ---------------------------------------------------------------- entry
def main():
    dexe, ib, secs = load_pe(EXE)
    tpl_bytes = open(TPL, "rb").read()
    mode = sys.argv[1] if len(sys.argv) > 1 else "normal"
    os.makedirs(os.path.join(RUN, "01_RAW"), exist_ok=True)
    if mode == "base_repro":
        out = run_base_repro(dexe, ib, secs, tpl_bytes)
        with open(os.path.join(RUN, "01_RAW", "BASE_MUTANT_C_REPRODUCTION.json"), "w") as f:
            json.dump({"measured": out}, f, indent=1)
        summary = {k: v for k, v in out.items() if k != "base_mutant_c"}
        summary["base_mutant_c"] = {k2: v2 for k2, v2 in out["base_mutant_c"].items()
                                    if k2 != "tq2_row_results"}
        print(json.dumps(summary, indent=1))
    elif mode == "normal":
        qc = run_checks(dexe, ib, secs, tpl_bytes)
        with open(os.path.join(RUN, "01_RAW", "QC_TARGETED.json"), "w") as f:
            json.dump({"measured": qc}, f, indent=1)
        print(json.dumps({k: (v["pass"] if isinstance(v, dict) and "pass" in v else v)
                          for k, v in qc.items()}, indent=1))
    elif mode == "battery":
        out = run_battery(dexe, ib, secs, tpl_bytes)
        with open(os.path.join(RUN, "01_RAW", "QC_MUTATION_BATTERY_POST_FIX.json"), "w") as f:
            json.dump({"measured": out}, f, indent=1)
        print(json.dumps({
            "MUTANT_A_DETECTED": out["MUTANT_A_DETECTED"],
            "MUTANT_B_DETECTED": out["MUTANT_B_DETECTED"],
            "MUTANT_C_POST_FIX_DETECTED": out["MUTANT_C_POST_FIX_DETECTED"],
            "canonical_negative_control_pass": out["canonical_negative_control_pass"],
            "battery_pass": out["battery_pass"],
            "cases": {n: {"PAYLOAD_FIELD_DECODE_CHECK": c["PAYLOAD_FIELD_DECODE_CHECK"],
                          "PAYLOAD_INDEX_STORE_IDENTITY_CHECK": c["PAYLOAD_INDEX_STORE_IDENTITY_CHECK"],
                          "CLIENT_DESTINATION_MAPPING_CHECK": c["CLIENT_DESTINATION_MAPPING_CHECK"],
                          "FULL_QC": c["FULL_QC"],
                          "detected": c["detected"]}
                      for n, c in out["cases"].items()}}, indent=1))
    elif mode == "oracle":
        ev = oracle_evidence(dexe, ib, secs)
        with open(os.path.join(RUN, "01_RAW", "ORACLE_EVIDENCE.json"), "w") as f:
            json.dump(ev, f, indent=1)
        print(json.dumps({"oracle_byte_backing_pass": ev["oracle_byte_backing"]["pass"],
                          "store_va_order_strictly_increasing": ev["oracle_byte_backing"]["store_va_order_strictly_increasing_with_payload_index"],
                          "pins_ok": all(p["ok"] for p in ev["oracle_byte_backing"]["pins"]),
                          "reads_ok": all(p["ok"] for p in ev["oracle_byte_backing"]["reads"])}, indent=1))
    else:
        raise SystemExit("usage: qc_targeted_c1c1.py [base_repro|normal|battery|oracle]")

if __name__ == "__main__":
    main()
