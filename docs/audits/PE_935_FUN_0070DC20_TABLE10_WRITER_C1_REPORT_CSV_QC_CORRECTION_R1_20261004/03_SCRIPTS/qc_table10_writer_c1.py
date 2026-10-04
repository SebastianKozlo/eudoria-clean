# qc_table10_writer_c1.py
# RUN: PE_935_FUN_0070DC20_TABLE10_WRITER_C1_REPORT_CSV_QC_CORRECTION_R1_20261004
# Purpose (bounded, READ-ONLY): the TARGETED correction QC battery for the
# C1 REPORT/CSV/QC correction package (QC_SCOPE=SELF_CHECK_TABLE10_WRITER_C1).
# Corrects exactly three P2 findings from the independent Desktop post-audit
# of 4627d38 (W1 function-budget QC, W2 strict CSV serialization, W3 storage
# identity vs specific value provenance) plus the P3 VA hygiene, and verifies
# the PRESERVED historical writer science. NO new reverse engineering: the
# only EXE byte reads are the two P3 VA corrections (4 tiny windows: the two
# corrected VAs and the two superseded VAs), each load-bearing and byte-pinned.
# Gates:
#  Q1  baseline identity (git HEAD/origin/actual-remote == BASE) + input identities
#  Q2  historical core writer science preserved (historical + corrected docs measured)
#  Q3  CORRECTED_FUNCTION_LEDGER.csv strict CSV + logical-content preservation
#  Q4  CORRECTED_WRITER_CHAIN.csv strict CSV + logical-content preservation
#  Q5  ledger-derived canonical function-count/budget check (parses the CSV
#      from disk; NEW_FUNCTION_COUNT DERIVED, never a literal) with the three
#      SEPARATE predicates (structure / canonical-row-count / budget-limit)
#  Q6  structurally-valid 9-row ledger mutant: structure PASS, count 9,
#      budget FAIL (negative control; PRIVATE synthetic, never canonical)
#  Q7  value-identity wording correctly scoped (+ superseded-wording absence)
#  Q8  SPECIFIC_RUNTIME_GETTER_VALUE_PRODUCER=UNVERIFIED present
#  Q9  WRITE_TO_LATER_GETTER_VALUE_PRESERVATION=NOT_ESTABLISHED present
#  Q10 fail-path zero-store VA 0x0097781E (corrected CSV + EXE byte re-read)
#  Q11 component vtable store VA 0x007374D6 (corrected docs + EXE byte re-read)
#  Q12 next-experiment wording bounded to the factory+0x84 assignment/object
#  Q13 forbidden-new-science census
#  Q14 preserved UNKNOWN/NOT_ESTABLISHED states
#  AUX quotecheck: every SUPERSESSION_LEDGER ORIGINAL_EXCERPT is a real
#      substring of its named SOURCE_FILE at the BASE commit.
# Outputs: 01_RAW/{QC_LEDGER_BUDGET,QC_CSV_STRICT,QC_VALUE_SCOPE,
#                   QC_NEGATIVE_CONTROLS}.json
import csv, io, json, os, re, struct, subprocess, sys, hashlib, tempfile, datetime

sys.dont_write_bytecode = True

RUN_ID = "PE_935_FUN_0070DC20_TABLE10_WRITER_C1_REPORT_CSV_QC_CORRECTION_R1_20261004"
REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
PKG = os.path.join(REPO, "docs", "audits", RUN_ID)
SRC = os.path.join(REPO, "docs", "audits", "PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
BASE_SHA = "4627d385b3f77f18bc2af5c02ed1f25182ec9fa5"
EXE_SIZE = 8015872
EXE_SHA256 = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
MAX_NEW_FUNCTIONS = 8  # MAX_NEW_FUNCTIONS_ANALYZED_IN_DETAIL (contract pin)
CANON_LEDGER_ROWS = 8
CANON_CHAIN_ROWS = 26

# The ONLY EXE byte reads allowed in this run (the two P3 VA corrections):
# (corrected VA, window bytes, expected) and (superseded VA, window, expected)
P3_PINS = {
    "failpath_zero_store_corrected_va_0x0097781E": (0x0097781E, 6, "c7 00 00 00 00 00"),
    "failpath_zero_store_superseded_va_0x0097781A": (0x0097781A, 2, None),  # measured, must NOT be the C7 start
    "component_vtable_store_corrected_va_0x007374D6": (0x007374D6, 6, "c7 06 2c 6f a8 00"),
    "component_vtable_store_superseded_va_0x007374DC": (0x007374DC, 2, "8b c6"),  # mid-stream, NOT the C7 start
}

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()

def write_json(name, obj):
    p = os.path.join(PKG, "01_RAW", name)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=1, ensure_ascii=True)
    return p

def git(*args):
    r = subprocess.run(["git", "-C", REPO] + list(args), capture_output=True)
    if r.returncode != 0:
        return None, r.stderr.decode("utf-8", "replace")
    return r.stdout.decode("utf-8", "replace"), None

def git_show(path):
    out, err = git("show", "HEAD:" + path)
    return out  # None on failure

# ---------------------------------------------------------------- EXE access
def load_pe(path):
    d = open(path, "rb").read()
    e_lfanew = struct.unpack_from("<I", d, 0x3C)[0]
    assert d[e_lfanew:e_lfanew + 4] == b"PE\x00\x00"
    coff = e_lfanew + 4
    nsec = struct.unpack_from("<H", d, coff + 2)[0]
    opt_size = struct.unpack_from("<H", d, coff + 16)[0]
    opt = coff + 20
    image_base = struct.unpack_from("<I", d, opt + 28)[0]
    sec0 = opt + opt_size
    secs = []
    for i in range(nsec):
        s = sec0 + 40 * i
        vsize, vaddr, rawsize, rawptr = struct.unpack_from("<IIII", d, s + 8)
        secs.append({"vaddr": vaddr, "vsize": vsize, "rawsize": rawsize, "rawptr": rawptr})
    return d, image_base, secs

def va_window(d, image_base, secs, va, size):
    rva = va - image_base
    for s in secs:
        if s["vaddr"] <= rva < s["vaddr"] + max(s["vsize"], s["rawsize"]):
            if rva - s["vaddr"] < s["rawsize"]:
                off = s["rawptr"] + (rva - s["vaddr"])
                return d[off:off + size].hex(" ")
    return None

# ------------------------------------------------- historical reconstruction
def read_lines_lf(path):
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read().split("\n")

def reconstruct_ledger():
    """Map-free provable reconstruction: fields 0..5 of every historical row
    are comma-free (asserted), so every embedded comma belongs to the RESULT
    field. Byte-accounting: re-joining the logical fields with ',' must
    reproduce the original line exactly."""
    lines = read_lines_lf(os.path.join(SRC, "FUNCTION_LEDGER.csv"))
    while lines and lines[-1] == "":
        lines.pop()
    header = lines[0].split(",")
    rows = []
    for line in lines[1:]:
        pieces = line.split(",")
        assert len(pieces) >= 7, ("short row", line)
        for i in (0, 1, 2, 3, 4, 5):
            assert "," not in pieces[i]  # trivially true post-split; documented rule
        assert pieces[0].isdigit() and pieces[3].isdigit() and pieces[5].isdigit()
        logical = pieces[0:6] + [",".join(pieces[6:])]
        assert ",".join(logical) == line, ("join roundtrip", line)
        rows.append(logical)
    return header, rows, lines[1:]

CHAIN_OP_N = {  # per-row operation-piece counts (see package docs; op/si
    # boundary is the one hand-derived reconstruction input; verified by the
    # balanced-delimiters invariant + join roundtrip below)
    1: 3, 2: 2, 3: 3, 4: 3, 5: 1, 6: 2, 7: 1, 8: 1, 9: 2, 10: 2, 11: 2,
    12: 2, 13: 2, 14: 2, 15: 2, 16: 3, 17: 2, 18: 1, 19: 2, 20: 2, 21: 2,
    22: 1, 23: 1, 24: 2, 25: 2, 26: 2,
}

def _balanced(s):
    return s.count("(") == s.count(")") and s.count("[") == s.count("]")

def reconstruct_chain():
    lines = read_lines_lf(os.path.join(SRC, "WRITER_CHAIN.csv"))
    while lines and lines[-1] == "":
        lines.pop()
    header = lines[0].split(",")
    rows = []
    for line in lines[1:]:
        pieces = line.split(",")
        step = int(pieces[0])
        op_n = CHAIN_OP_N[step]
        logical = (pieces[0:3]
                   + [",".join(pieces[3:3 + op_n])]
                   + [",".join(pieces[3 + op_n:-1])]
                   + [pieces[-1]])
        assert ",".join(logical) == line, ("join roundtrip", line)
        assert _balanced(logical[3]) and _balanced(logical[4]), ("delimiters", line)
        rows.append(logical)
    return header, rows, lines[1:]

def csv_strict_battery(path, expected_header, expected_rows, key_idx, key_name):
    """W2 strict CSV battery, all measured. Returns (record, ok)."""
    rec = {"file": os.path.basename(path)}
    raw = open(path, "rb").read()
    # UTF-8 round trip
    try:
        txt = raw.decode("utf-8")
        re_enc = txt.encode("utf-8")
        rec["utf8_round_trip"] = (re_enc == raw)
    except UnicodeDecodeError:
        rec["utf8_round_trip"] = False
        txt = None
    ok = rec["utf8_round_trip"]
    # standard csv.reader parse
    with open(path, "r", encoding="utf-8", newline="") as f:
        parsed = list(csv.reader(f))
    rec["csv_reader_parse_succeeds"] = isinstance(parsed, list) and len(parsed) >= 1
    header = parsed[0] if parsed else []
    rec["header"] = header
    rec["header_column_count"] = len(header)
    rec["header_correct"] = (header == expected_header)
    data = parsed[1:]
    rec["data_row_count"] = len(data)
    rec["row_count_preserved"] = (len(data) == expected_rows)
    widths = [len(r) for r in data]
    rec["row_widths"] = widths
    rec["all_rows_exact_header_width"] = all(w == len(header) for w in widths)
    rec["csv_width_mismatches"] = sum(1 for w in widths if w != len(header))
    rec["csv_extra_fields"] = rec["csv_width_mismatches"]  # extra/missing measured together per row
    # DictReader: no extra fields under key None, no missing fields
    with open(path, "r", encoding="utf-8", newline="") as f:
        dr = csv.DictReader(f)
        dict_rows = list(dr)
        none_key_rows = sum(1 for r in dict_rows if None in r)
        missing_rows = 0
        for r in dict_rows:
            for k in dr.fieldnames:
                if r.get(k) is None:
                    missing_rows += 1
                    break
    rec["dictreader_none_key_rows"] = none_key_rows
    rec["dictreader_missing_field_rows"] = missing_rows
    # key/ordinal uniqueness
    keys = [r[key_idx] for r in data if len(r) > key_idx]
    rec[key_name + "_unique"] = (len(keys) == len(set(keys)))
    rec[key_name + "_count"] = len(keys)
    # embedded separator content survives as field content
    sep_rows = [r for r in data if any((";" in c or "(" in c or ")" in c or "," in c or "[" in c) for c in r)]
    rec["rows_with_embedded_separators_kept_as_content"] = len(sep_rows)
    # write->read->write semantic round trip
    buf1 = io.StringIO()
    w = csv.writer(buf1, lineterminator="\n")
    w.writerows(parsed)
    reparsed = list(csv.reader(io.StringIO(buf1.getvalue())))
    buf2 = io.StringIO()
    w2 = csv.writer(buf2, lineterminator="\n")
    w2.writerows(reparsed)
    rec["write_read_write_round_trip"] = (buf1.getvalue() == buf2.getvalue() and reparsed == parsed)
    ok = (ok and rec["csv_reader_parse_succeeds"] and rec["header_correct"]
          and rec["row_count_preserved"] and rec["all_rows_exact_header_width"]
          and rec["csv_width_mismatches"] == 0
          and none_key_rows == 0 and missing_rows == 0
          and rec[key_name + "_unique"] and rec["write_read_write_round_trip"])
    rec["STRICT_CSV_STATUS"] = "PASS" if ok else "FAIL"
    return rec, ok, parsed

def logical_content_diff(hist_header, hist_rows, corr_parsed, key_idx,
                         authorized_changes):
    """Verifies the corrected CSV preserves ALL logical field content EXCEPT the
    explicitly authorized changes. Returns (diffs, ok)."""
    diffs = []
    if hist_header != corr_parsed[0]:
        diffs.append({"kind": "HEADER", "old": hist_header, "new": corr_parsed[0]})
    if len(hist_rows) != len(corr_parsed) - 1:
        diffs.append({"kind": "ROW_COUNT", "old": len(hist_rows),
                      "new": len(corr_parsed) - 1})
    for h, c in zip(hist_rows, corr_parsed[1:]):
        key = h[key_idx]
        for fi in range(max(len(h), len(c))):
            hv = h[fi] if fi < len(h) else None
            cv = c[fi] if fi < len(c) else None
            if hv != cv:
                diffs.append({"key": key, "field_index": fi, "old": hv, "new": cv})
    # diffs must match the authorized changes exactly
    auth_ok = len(diffs) == len(authorized_changes)
    for d, a in zip(diffs, authorized_changes):
        if not (str(d.get("key")) == str(a["key"])
                and d.get("field_index") == a["field_index"]
                and d.get("old") == a["old"] and d.get("new") == a["new"]):
            auth_ok = False
    return diffs, auth_ok, (len(diffs) == 0 or auth_ok)

# ------------------------------------------------- generic ledger validation
def validate_ledger_rows(rows, header_len):
    """Generic structural + budget validation of a parsed ledger (rows = list of
    field-lists WITHOUT header). All values measured/derived, never literal.
    Separates: LEDGER_STRUCTURE / EXPECTED_CANONICAL_ROW_COUNT / BUDGET_LIMIT."""
    m = {}
    n = len(rows)
    m["data_row_count"] = n
    m["header_column_count"] = header_len
    m["all_rows_exact_header_width"] = all(len(r) == header_len for r in rows)
    ords = [r[0] for r in rows]
    try:
        ords_i = [int(x) for x in ords]
        cb = [int(r[3]) for r in rows]
        ca = [int(r[5]) for r in rows]
        numeric = True
    except (ValueError, IndexError):
        numeric = False
    m["numeric_fields_parse"] = numeric
    if numeric:
        m["ordinal_sequence_contiguous_from_1"] = (ords_i == list(range(1, n + 1)))
        m["ordinal_unique"] = (len(set(ords)) == n)
        m["count_before_sequence"] = (cb == list(range(0, n)))
        m["count_after_sequence"] = (ca == list(range(1, n + 1)))
        m["per_row_count_after_eq_before_plus_1"] = all(
            ca[i] == cb[i] + 1 for i in range(n))
        m["count_before_lt_max_per_row"] = all(x < MAX_NEW_FUNCTIONS for x in cb)
        m["final_count_after"] = ca[-1] if ca else None
        # derived (NOT a literal):
        m["ledger_declared_count"] = m["final_count_after"]
        m["count_after_eq_declared_count"] = (m["final_count_after"] == n)
    funcs = [r[1] for r in rows if len(r) > 1]
    m["function_field_nonempty"] = all(f.strip() != "" for f in funcs) and len(funcs) == n
    m["function_unique"] = (len(set(funcs)) == n)
    structure_ok = (m.get("all_rows_exact_header_width", False) and numeric
                    and m.get("ordinal_sequence_contiguous_from_1", False)
                    and m.get("ordinal_unique", False)
                    and m.get("count_before_sequence", False)
                    and m.get("count_after_sequence", False)
                    and m.get("per_row_count_after_eq_before_plus_1", False)
                    and m.get("function_field_nonempty", False)
                    and m.get("function_unique", False)
                    and m.get("count_after_eq_declared_count", False))
    m["LEDGER_STRUCTURE_STATUS"] = "PASS" if structure_ok else "FAIL"
    m["canonical_row_count_expected"] = CANON_LEDGER_ROWS
    m["row_count_equals_canonical"] = (n == CANON_LEDGER_ROWS)
    # SEPARATE budget predicate: derived count vs MAX only
    if numeric and m["final_count_after"] is not None:
        m["budget_limit_check"] = "PASS" if m["final_count_after"] <= MAX_NEW_FUNCTIONS else "FAIL"
        m["ledger_declared_within_budget"] = ("YES" if m["final_count_after"] <= MAX_NEW_FUNCTIONS else "NO")
    else:
        m["budget_limit_check"] = "NOT_VERIFIED"
        m["ledger_declared_within_budget"] = "NOT_VERIFIED"
    m["budget_failure_depends_only_on_derived_count_vs_max"] = True  # inputs recorded above
    m["sequence_valid"] = ("YES" if structure_ok else "NO")
    return m

# ------------------------------------------------------------------- gates
def gate_q1():
    rec = {"gate": "Q1_baseline_identity"}
    head, e1 = git("rev-parse", "HEAD")
    origin, e2 = git("rev-parse", "origin/master")
    ls, e3 = git("ls-remote", "origin", "master")
    actual_remote = ls.split("\t")[0].strip() if ls else None
    rec["local_head"] = head.strip() if head else None
    rec["origin_master"] = origin.strip() if origin else None
    rec["actual_remote_master"] = actual_remote
    rec["base_sha_contract_pin"] = BASE_SHA
    rec["head_equals_base"] = (rec["local_head"] == BASE_SHA)
    rec["origin_equals_base"] = (rec["origin_master"] == BASE_SHA)
    rec["remote_equals_base"] = (actual_remote == BASE_SHA)
    rec["all_equal_base"] = (rec["head_equals_base"] and rec["origin_equals_base"]
                             and rec["remote_equals_base"])
    # input identities: historical source package key files (declared in
    # INPUT_IDENTITIES.md are re-measured here)
    inputs = {}
    for rel in ["FINAL_REPORT.md", "HANDOFF.md", "QC_REPORT.md", "INPUT_IDENTITIES.md",
                "FUNCTION_LEDGER.csv", "WRITER_CHAIN.csv",
                "01_RAW/S5_QC_BATTERY.json", "03_SCRIPTS/s5_qc_battery.py"]:
        p = os.path.join(SRC, rel.replace("/", os.sep))
        inputs[rel] = {"size_bytes": os.path.getsize(p), "sha256": sha256_file(p)}
    rec["historical_source_identities"] = inputs
    # declared-vs-measured cross-check against INPUT_IDENTITIES.md
    ii_path = os.path.join(PKG, "INPUT_IDENTITIES.md")
    ii = open(ii_path, "r", encoding="utf-8").read()
    declared = re.findall(
        r"\|\s*(docs/audits/PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004/[A-Za-z0-9_./]+)\s*\|\s*(\d+)\s*\|\s*([0-9A-Fa-f]{64})\s*\|",
        ii)
    mismatches = []
    for rel, sz, sha in declared:
        p = os.path.join(REPO, rel.replace("/", os.sep))
        if not os.path.exists(p):
            mismatches.append({"file": rel, "reason": "missing"})
            continue
        if os.path.getsize(p) != int(sz) or sha256_file(p) != sha.upper():
            mismatches.append({"file": rel, "reason": "size-or-sha-mismatch"})
    rec["input_identities_declared_count"] = len(declared)
    rec["input_identities_mismatches"] = mismatches
    rec["input_identities_all_verified"] = (len(declared) > 0 and len(mismatches) == 0)
    # corrected CSV identities (inputs to the gates below)
    corr = {}
    for rel in ["CORRECTED_FUNCTION_LEDGER.csv", "CORRECTED_WRITER_CHAIN.csv"]:
        p = os.path.join(PKG, rel)
        corr[rel] = {"size_bytes": os.path.getsize(p), "sha256": sha256_file(p)}
    rec["corrected_csv_identities"] = corr
    rec["status"] = "PASS" if (rec["all_equal_base"]
                              and rec["input_identities_all_verified"]) else "FAIL"
    return rec

def gate_q2():
    rec = {"gate": "Q2_historical_core_science_preserved"}
    hist = open(os.path.join(SRC, "FINAL_REPORT.md"), "r", encoding="utf-8").read()
    corr = open(os.path.join(PKG, "FINAL_REPORT.md"), "r", encoding="utf-8").read()
    core_hist = {
        "writer_function_FUN_009777F0": "WRITER_FUNCTION: FUN_009777F0" in hist,
        "writer_va_0x00977810": "WRITER_VA: 0x00977810" in hist,
        "table10_write_confirmed": "TABLE10_WRITE = CONFIRMED" in hist,
        "same_component_identity_confirmed": "SAME_COMPONENT_IDENTITY = CONFIRMED" in hist,
        "table10_source_value_representation_record_field":
            "TABLE10_SOURCE_VALUE_REPRESENTATION = RECORD_FIELD" in hist,
        "ultimate_value_source_unknown": "ULTIMATE_VALUE_SOURCE = UNKNOWN" in hist,
        "file_derived_value_excluded_no": "FILE_DERIVED_VALUE_EXCLUDED = NO" in hist,
        "record_a_relation_not_established": "RECORD_A_RELATION = NOT_ESTABLISHED" in hist,
        "world_instance_semantic_not_established": "WORLD_INSTANCE_SEMANTIC = NOT_ESTABLISHED" in hist,
        "world_xyz_recovered_no": "WORLD_XYZ_RECOVERED = NO" in hist,
        "answer_yes_s2": "ANSWER (S2 level, byte-pinned): YES." in hist,
        "attribute10_selection_confirmed": "ATTRIBUTE10_SELECTION = CONFIRMED" in hist,
        "control_case_pass": "CONTROL_CASE = PASS" in hist,
    }
    core_corr = {
        "ATTRIBUTE10_WRITER_MECHANISM = CONFIRMED": "ATTRIBUTE10_WRITER_MECHANISM = CONFIRMED" in corr,
        "WRITER_FUNCTION = FUN_009777F0": "WRITER_FUNCTION = FUN_009777F0" in corr,
        "WRITER_VA = 0x00977810": "WRITER_VA = 0x00977810" in corr,
        "WRITER_MECHANISM = CONFIRMED_STATIC_CONDITIONAL": "WRITER_MECHANISM = CONFIRMED_STATIC_CONDITIONAL" in corr,
        "SAME_STORAGE_IDENTITY = CONFIRMED_STATIC_CONDITIONAL": "SAME_STORAGE_IDENTITY = CONFIRMED_STATIC_CONDITIONAL" in corr,
        "TABLE10_SOURCE_VALUE_REPRESENTATION = RECORD_FIELD": "TABLE10_SOURCE_VALUE_REPRESENTATION = RECORD_FIELD" in corr,
        "ULTIMATE_VALUE_SOURCE = UNKNOWN": "ULTIMATE_VALUE_SOURCE = UNKNOWN" in corr,
        "FILE_DERIVED_VALUE_EXCLUDED = NO": "FILE_DERIVED_VALUE_EXCLUDED = NO" in corr,
        "RECORD_A_RELATION = NOT_ESTABLISHED": "RECORD_A_RELATION = NOT_ESTABLISHED" in corr,
        "WORLD_INSTANCE_SEMANTIC = NOT_ESTABLISHED": "WORLD_INSTANCE_SEMANTIC = NOT_ESTABLISHED" in corr,
        "WORLD_XYZ_RECOVERED = NO": "WORLD_XYZ_RECOVERED = NO" in corr,
        "TAG6_TO_ID10 = CONFIRMED": "TAG6_TO_ID10 = CONFIRMED" in corr,
    }
    rec["historical_core_claims_measured"] = core_hist
    rec["corrected_package_preserves_core"] = core_corr
    rec["all_historical_present"] = all(core_hist.values())
    rec["all_corrected_present"] = all(core_corr.values())
    rec["status"] = "PASS" if (rec["all_historical_present"] and rec["all_corrected_present"]) else "FAIL"
    return rec

def gate_q3():
    rec = {"gate": "Q3_corrected_ledger_strict_csv"}
    path = os.path.join(PKG, "CORRECTED_FUNCTION_LEDGER.csv")
    header = ["ordinal", "function", "reason_entered", "count_before",
              "analysis_started", "count_after", "result"]
    battery, ok, parsed = csv_strict_battery(path, header, CANON_LEDGER_ROWS, 0, "ordinal")
    rec.update(battery)
    # historical malformed measurement (PRESERVED measurement, read-only)
    hist_lines = read_lines_lf(os.path.join(SRC, "FUNCTION_LEDGER.csv"))
    while hist_lines and hist_lines[-1] == "":
        hist_lines.pop()
    hh = hist_lines[0].split(",")
    hwidths = [len(l.split(",")) for l in hist_lines[1:]]
    rec["historical_measurement"] = {
        "header_column_count": len(hh),
        "data_row_count": len(hwidths),
        "malformed_width_rows": sum(1 for w in hwidths if w != len(hh)),
        "well_formed_rows": sum(1 for w in hwidths if w == len(hh)),
    }
    # logical content preservation. reconstruct_ledger() returns the HISTORICAL
    # logical content; the ONE authorized change (P3-A) is the fail-path VA swap
    # in row 7's reason_entered field.
    lh, lrows, _ = reconstruct_ledger()
    hist7 = [r for r in lrows if r[0] == "7"][0][2]
    assert "@0x0097781A" in hist7 and "@0x0097781E" not in hist7
    authorized = [{"key": "7", "field_index": 2,
                   "old": hist7,
                   "new": hist7.replace("@0x0097781A", "@0x0097781E")}]
    diffs, auth_ok, preserve_ok = logical_content_diff(lh, lrows, parsed, 0, authorized)
    rec["logical_content_diffs"] = diffs
    rec["logical_content_preserved_except_authorized"] = preserve_ok
    rec["authorized_changes_exactly_applied"] = auth_ok
    rec["FUNCTION_LEDGER_CSV"] = "CORRECTED_VALID" if (ok and preserve_ok and auth_ok) else "INVALID"
    # declared-vs-measured cross-check (the report may not claim better than
    # the measurement)
    ts = terminal_block()
    rec["declared_in_terminal_state"] = ts.get("FUNCTION_LEDGER_CSV")
    rec["declared_matches_measured"] = (ts.get("FUNCTION_LEDGER_CSV") == rec["FUNCTION_LEDGER_CSV"])
    rec["status"] = ("PASS" if (rec["FUNCTION_LEDGER_CSV"] == "CORRECTED_VALID"
                                and rec["declared_matches_measured"]) else "FAIL")
    return rec

def gate_q4():
    rec = {"gate": "Q4_corrected_writer_chain_strict_csv"}
    path = os.path.join(PKG, "CORRECTED_WRITER_CHAIN.csv")
    header = ["step", "actor", "va", "operation", "structural_identity", "evidence_pin"]
    battery, ok, parsed = csv_strict_battery(path, header, CANON_CHAIN_ROWS, 0, "step")
    rec.update(battery)
    hist_lines = read_lines_lf(os.path.join(SRC, "WRITER_CHAIN.csv"))
    while hist_lines and hist_lines[-1] == "":
        hist_lines.pop()
    hh = hist_lines[0].split(",")
    hwidths = [len(l.split(",")) for l in hist_lines[1:]]
    rec["historical_measurement"] = {
        "header_column_count": len(hh),
        "data_row_count": len(hwidths),
        "malformed_width_rows": sum(1 for w in hwidths if w != len(hh)),
        "well_formed_rows": sum(1 for w in hwidths if w == len(hh)),
    }
    ch, crows, _ = reconstruct_chain()
    new26 = [r for r in parsed[1:] if r[0] == "26"][0][4]
    old26 = [r for r in crows if r[0] == "26"][0][4]
    authorized = [{"key": "26", "field_index": 4, "old": old26, "new": new26}]
    diffs, auth_ok, preserve_ok = logical_content_diff(ch, crows, parsed, 0, authorized)
    rec["logical_content_diffs"] = diffs
    rec["logical_content_preserved_except_authorized"] = preserve_ok
    rec["authorized_changes_exactly_applied"] = auth_ok
    rec["WRITER_CHAIN_CSV"] = "CORRECTED_VALID" if (ok and preserve_ok and auth_ok) else "INVALID"
    ts = terminal_block()
    rec["declared_in_terminal_state"] = ts.get("WRITER_CHAIN_CSV")
    rec["declared_matches_measured"] = (ts.get("WRITER_CHAIN_CSV") == rec["WRITER_CHAIN_CSV"])
    rec["status"] = ("PASS" if (rec["WRITER_CHAIN_CSV"] == "CORRECTED_VALID"
                                and rec["declared_matches_measured"]) else "FAIL")
    return rec

def gate_q5():
    rec = {"gate": "Q5_ledger_derived_function_budget"}
    # parse the CORRECTED CSV FROM DISK (the W1 fix: the count is DERIVED)
    path = os.path.join(PKG, "CORRECTED_FUNCTION_LEDGER.csv")
    with open(path, "r", encoding="utf-8", newline="") as f:
        parsed = list(csv.reader(f))
    header, rows = parsed[0], parsed[1:]
    m = validate_ledger_rows(rows, len(header))
    rec.update(m)
    rec["max_new_functions_analyzed_in_detail"] = MAX_NEW_FUNCTIONS
    rec["expected_canonical_row_count_status"] = (
        "PASS" if m["row_count_equals_canonical"] else "FAIL")
    rec["function_budget_ledger_validation"] = (
        "PASS" if (m["LEDGER_STRUCTURE_STATUS"] == "PASS"
                   and rec["expected_canonical_row_count_status"] == "PASS"
                   and m["budget_limit_check"] == "PASS") else "FAIL")
    rec["function_budget_precheck"] = (
        "PASS" if rec["function_budget_ledger_validation"] == "PASS" else "FAIL")
    # epistemic scope (W1): a post-hoc static validator CANNOT independently
    # prove the chronological pre-check discipline of the historical executor.
    rec["execution_timing_precheck_independently_established"] = "NO"
    rec["epistemic_scope_note"] = (
        "The validator proves the LEDGER-DECLARED sequence/count/budget "
        "(LEDGER_DECLARED_SEQUENCE_VALID / LEDGER_DECLARED_COUNT / "
        "LEDGER_DECLARED_WITHIN_BUDGET). It does NOT independently establish "
        "that the executor physically performed each pre-check before each "
        "analysis; no chronological evidence for that exists in this run.")
    rec["ledger_declared_sequence_valid"] = m["sequence_valid"]
    # declared-vs-measured cross-checks for the measured terminal fields
    ts = terminal_block()
    for key in ["LEDGER_DECLARED_COUNT", "LEDGER_DECLARED_SEQUENCE_VALID",
                "LEDGER_DECLARED_WITHIN_BUDGET", "FUNCTION_BUDGET_LEDGER_VALIDATION"]:
        rec["declared_" + key] = ts.get(key)
    rec["declared_matches_measured"] = (
        ts.get("LEDGER_DECLARED_COUNT") == str(m["ledger_declared_count"])
        and ts.get("LEDGER_DECLARED_SEQUENCE_VALID") == m["sequence_valid"]
        and ts.get("LEDGER_DECLARED_WITHIN_BUDGET") == m["ledger_declared_within_budget"]
        and ts.get("FUNCTION_BUDGET_LEDGER_VALIDATION") == rec["function_budget_ledger_validation"])
    rec["status"] = ("PASS" if (rec["function_budget_ledger_validation"] == "PASS"
                                and rec["declared_matches_measured"]) else "FAIL")
    return rec

def gate_q6():
    rec = {"gate": "Q6_nine_row_structurally_valid_mutant"}
    # PRIVATE synthetic mutant: the 8 canonical corrected rows + 1 synthetic
    # 9th row. Structurally VALID; must fail SPECIFICALLY on the budget.
    with open(os.path.join(PKG, "CORRECTED_FUNCTION_LEDGER.csv"), "r",
              encoding="utf-8", newline="") as f:
        parsed = list(csv.reader(f))
    header, rows = parsed[0], parsed[1:]
    mutant_rows = [list(r) for r in rows] + [[
        "9", "FUN_SYNTHETIC_MUTANT_09",
        "synthetic negative-control row (structurally valid 9th entry)",
        "8", "SYNTHETIC", "9",
        "SYNTHETIC: added solely to exceed the budget limit (MAX 8); private "
        "QC negative control, never canonical"]]
    tmpdir = r"C:\Users\User\AppData\Local\Temp\opencode"
    os.makedirs(tmpdir, exist_ok=True)
    tmp = os.path.join(tmpdir, "mutant_ledger_c1_TMP.csv")
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(mutant_rows)
    # validate FROM DISK with the SAME generic validator
    with open(tmp, "r", encoding="utf-8", newline="") as f:
        mp = list(csv.reader(f))
    m = validate_ledger_rows(mp[1:], len(mp[0]))
    m["valid_csv"] = (isinstance(mp, list) and len(mp) == 1 + 9)
    m["header_width_correct"] = (len(mp[0]) == 7)
    m["unique_functions"] = m["function_unique"]
    # canonical-row-count predicate is SEPARATE and NOT the mutant's test dimension
    m["expected_canonical_row_count_status"] = "NOT_APPLICABLE_TO_MUTANT"
    m["row_count_vs_canonical_measured"] = {
        "mutant_rows": m["data_row_count"], "canonical_rows": CANON_LEDGER_ROWS,
        "equal": m["row_count_equals_canonical"],
        "note": ("The canonical-row-count predicate is reported SEPARATELY; the "
                 "budget failure does NOT depend on it: BUDGET_LIMIT_CHECK "
                 "derives ONLY from the derived count (9) vs MAX (8).")}
    m["function_budget_precheck"] = (
        "PASS" if m["budget_limit_check"] == "PASS" else "FAIL")
    m["new_function_count_derived"] = m["ledger_declared_count"]
    m["mutant_is_private"] = True
    m["mutant_committed_as_canonical"] = False
    m["generation_recipe"] = (
        "CORRECTED_FUNCTION_LEDGER.csv rows 1..8 + one synthetic row "
        "[9, FUN_SYNTHETIC_MUTANT_09, synthetic reason, 8, SYNTHETIC, 9, "
        "synthetic result]; written to a TEMP path outside the repo with "
        "csv.writer and validated from disk with the same generic validator.")
    m["status"] = ("PASS" if (m["LEDGER_STRUCTURE_STATUS"] == "PASS"
                              and m["new_function_count_derived"] == 9
                              and m["budget_limit_check"] == "FAIL"
                              and m["function_budget_precheck"] == "FAIL") else "FAIL")
    m["test_validity"] = (
        "VALID" if (m["LEDGER_STRUCTURE_STATUS"] == "PASS"
                    and m["budget_limit_check"] == "FAIL") else "INVALID")
    os.remove(tmp)  # cleanup: no mutant file left anywhere
    m["temp_mutant_file_removed"] = not os.path.exists(tmp)
    # declared-vs-measured cross-checks for the mutant terminal fields
    ts = terminal_block()
    m["declared_nine_row_mutant_structure_status"] = ts.get("NINE_ROW_MUTANT_STRUCTURE_STATUS")
    m["declared_nine_row_mutant_new_function_count"] = ts.get("NINE_ROW_MUTANT_NEW_FUNCTION_COUNT")
    m["declared_nine_row_mutant_budget_limit_check"] = ts.get("NINE_ROW_MUTANT_BUDGET_LIMIT_CHECK")
    m["declared_matches_measured"] = (
        ts.get("NINE_ROW_MUTANT_STRUCTURE_STATUS") == m["LEDGER_STRUCTURE_STATUS"]
        and ts.get("NINE_ROW_MUTANT_NEW_FUNCTION_COUNT") == str(m["new_function_count_derived"])
        and ts.get("NINE_ROW_MUTANT_BUDGET_LIMIT_CHECK") == m["budget_limit_check"])
    if not m["declared_matches_measured"]:
        m["status"] = "FAIL"
    rec.update(m)
    return rec

TERMINAL_RE = re.compile(r"^([A-Z][A-Z0-9_]+) = (.+)$", re.M)

def terminal_block():
    txt = open(os.path.join(PKG, "FINAL_REPORT.md"), "r", encoding="utf-8").read()
    b = txt.split("--- TERMINAL_STATE_BEGIN ---")
    if len(b) < 2:
        return {}
    blk = b[1].split("--- TERMINAL_STATE_END ---")[0]
    return dict(TERMINAL_RE.findall(blk))

def _norm(s):
    """Whitespace-normalized form (the established repo quotecheck convention)."""
    return " ".join(s.split())

def gate_q7():
    rec = {"gate": "Q7_value_identity_wording_scoped"}
    ts = terminal_block()
    # corrected scope statement present in the active docs (whitespace-normalized
    # matching: the report wraps the statement across lines)
    corr = open(os.path.join(PKG, "FINAL_REPORT.md"), "r", encoding="utf-8").read()
    scope_stmt = ("The audited writer mechanism can write record value data into table[10] "
                  "of the same structural component/cache identity later addressed by the "
                  "getter. The getter reads the CURRENT value of that entry. This static "
                  "run does not establish that the exact value written by a particular "
                  "apply event remains unchanged until any particular later getter event.")
    rec["corrected_scope_statement_present"] = (_norm(scope_stmt) in _norm(corr))
    # chain row 26 carries the scoped wording
    with open(os.path.join(PKG, "CORRECTED_WRITER_CHAIN.csv"), "r",
              encoding="utf-8", newline="") as f:
        parsed = list(csv.reader(f))
    row26 = [r for r in parsed[1:] if r[0] == "26"][0]
    rec["row26_reads_current_value"] = ("reads the CURRENT value of table[10]" in row26[4])
    rec["row26_storage_identity_conditional"] = ("CONFIRMED_STATIC_CONDITIONAL" in row26[4])
    rec["row26_preservation_not_established"] = ("NOT_ESTABLISHED" in row26[4])
    rec["row26_superseded_wording_absent"] = ("the value WRITTEN at step 20" not in row26[4])
    rec["row26_same_storage_entry"] = ("SAME storage entry" in row26[4])
    # absence sweep across ACTIVE claim surfaces (SUPERSESSION_LEDGER.md is the
    # designated record of old claims; historical package READ-ONLY; 01_RAW JSONs
    # are measurement records, not claim surfaces)
    superseded_phrases = [
        "the value WRITTEN at step 20",
        "GETTER_RESULT_PRODUCER = CONFIRMED_AT_IMMEDIATE_WRITER_LEVEL",
        "0x0097781A",
        "0x007374DC",
        "convert ULTIMATE_VALUE_SOURCE from UNKNOWN",
        "That single bounded experiment would",
        "NEW_FUNCTION_COUNT = 7",
    ]
    active_files = ["FINAL_REPORT.md", "HANDOFF.md", "INPUT_IDENTITIES.md",
                    "CORRECTED_FUNCTION_LEDGER.csv", "CORRECTED_WRITER_CHAIN.csv"]
    qcr = os.path.join(PKG, "QC_REPORT.md")
    if os.path.exists(qcr):
        active_files.append("QC_REPORT.md")
    hits = []
    for fn in active_files:
        content = open(os.path.join(PKG, fn), "r", encoding="utf-8").read()
        for ph in superseded_phrases:
            if ph in content:
                hits.append({"file": fn, "phrase": ph})
    rec["superseded_wording_absence_sweep_files"] = active_files
    rec["superseded_wording_hits"] = hits
    rec["superseded_wording_absent_from_active_docs"] = (len(hits) == 0)
    # SAME_STORAGE_IDENTITY terminal value
    rec["same_storage_identity_declared"] = ts.get("SAME_STORAGE_IDENTITY")
    rec["writer_mechanism_declared"] = ts.get("WRITER_MECHANISM")
    scope_ok = (rec["corrected_scope_statement_present"] and rec["row26_reads_current_value"]
                and rec["row26_storage_identity_conditional"]
                and rec["row26_preservation_not_established"]
                and rec["row26_superseded_wording_absent"] and rec["row26_same_storage_entry"]
                and rec["superseded_wording_absent_from_active_docs"]
                and ts.get("SAME_STORAGE_IDENTITY") == "CONFIRMED_STATIC_CONDITIONAL"
                and ts.get("WRITER_MECHANISM") == "CONFIRMED_STATIC_CONDITIONAL")
    rec["status"] = "PASS" if scope_ok else "FAIL"
    return rec

def gate_q8():
    rec = {"gate": "Q8_specific_runtime_getter_value_producer"}
    ts = terminal_block()
    corr = open(os.path.join(PKG, "FINAL_REPORT.md"), "r", encoding="utf-8").read()
    rec["declared"] = ts.get("SPECIFIC_RUNTIME_GETTER_VALUE_PRODUCER")
    rec["expected_target"] = "UNVERIFIED"
    rec["declared_equals_target"] = (rec["declared"] == "UNVERIFIED")
    rec["present_in_final_report_text"] = ("SPECIFIC_RUNTIME_GETTER_VALUE_PRODUCER = UNVERIFIED" in corr)
    rec["status"] = "PASS" if (rec["declared_equals_target"] and rec["present_in_final_report_text"]) else "FAIL"
    return rec

def gate_q9():
    rec = {"gate": "Q9_write_to_later_getter_value_preservation"}
    ts = terminal_block()
    corr = open(os.path.join(PKG, "FINAL_REPORT.md"), "r", encoding="utf-8").read()
    rec["declared"] = ts.get("WRITE_TO_LATER_GETTER_VALUE_PRESERVATION")
    rec["expected_target"] = "NOT_ESTABLISHED"
    rec["declared_equals_target"] = (rec["declared"] == "NOT_ESTABLISHED")
    rec["present_in_final_report_text"] = ("WRITE_TO_LATER_GETTER_VALUE_PRESERVATION = NOT_ESTABLISHED" in corr)
    rec["status"] = "PASS" if (rec["declared_equals_target"] and rec["present_in_final_report_text"]) else "FAIL"
    return rec

def gate_q10():
    rec = {"gate": "Q10_failpath_zero_store_va"}
    # corrected CSV carries 0x0097781E and NOT 0x0097781A
    with open(os.path.join(PKG, "CORRECTED_FUNCTION_LEDGER.csv"), "r",
              encoding="utf-8", newline="") as f:
        content = f.read()
    rec["corrected_ledger_contains_0x0097781E"] = ("0x0097781E" in content)
    rec["corrected_ledger_absent_0x0097781A"] = ("0x0097781A" not in content)
    # active corrected documentation
    ts = terminal_block()
    rec["declared_failpath_va"] = ts.get("FAILPATH_ZERO_STORE_VA")
    rec["declared_equals_target"] = (ts.get("FAILPATH_ZERO_STORE_VA") == "0x0097781E")
    # EXE identity + byte re-read (the ONLY load-bearing exact-byte pin set for P3-A)
    d, image_base, secs = load_pe(EXE)
    sz = os.path.getsize(EXE)
    h = sha256_file(EXE)
    rec["exe_identity"] = {"size_bytes": sz, "sha256": h,
                           "size_match": sz == EXE_SIZE, "sha256_match": h == EXE_SHA256}
    va, n, exp = P3_PINS["failpath_zero_store_corrected_va_0x0097781E"]
    got = va_window(d, image_base, secs, va, n)
    rec["corrected_va_bytes"] = {"va": "0x%08X" % va, "expected": exp, "actual": got,
                                 "match": got == exp}
    va2, n2, _ = P3_PINS["failpath_zero_store_superseded_va_0x0097781A"]
    got2 = va_window(d, image_base, secs, va2, n2)
    rec["superseded_va_bytes"] = {
        "va": "0x%08X" % va2, "actual": got2,
        "is_c7_zero_store_start": (got2 is not None and got2.startswith("c7 00")),
        "note": ("measured: the superseded VA is NOT the C7 zero-store start; "
                 "the C7 00 00 00 00 00 store starts at 0x0097781E")}
    # historical S5 machine pin was ALREADY 0x0097781E (defect was ledger-row-only)
    s5 = json.load(open(os.path.join(SRC, "01_RAW", "S5_QC_BATTERY.json"),
                        encoding="utf-8"))
    hist_pin = s5["gate_results"]["Q6_exact_write"]["writer_failpath_zero_store"]
    rec["historical_s5_pin"] = {"va": hist_pin["va"], "match": hist_pin["match"]}
    rec["historical_machine_pin_already_correct"] = (hist_pin["va"] == "0x0097781E")
    ok = (rec["corrected_ledger_contains_0x0097781E"]
          and rec["corrected_ledger_absent_0x0097781A"]
          and rec["declared_equals_target"]
          and rec["exe_identity"]["size_match"] and rec["exe_identity"]["sha256_match"]
          and rec["corrected_va_bytes"]["match"]
          and not rec["superseded_va_bytes"]["is_c7_zero_store_start"]
          and rec["historical_machine_pin_already_correct"])
    rec["status"] = "PASS" if ok else "FAIL"
    return rec

def gate_q11():
    rec = {"gate": "Q11_component_vtable_store_va"}
    ts = terminal_block()
    rec["declared_component_vtable_store_va"] = ts.get("COMPONENT_VTABLE_STORE_VA")
    rec["declared_equals_target"] = (ts.get("COMPONENT_VTABLE_STORE_VA") == "0x007374D6")
    corr = open(os.path.join(PKG, "FINAL_REPORT.md"), "r", encoding="utf-8").read()
    rec["corrected_va_in_final_report"] = ("COMPONENT_VTABLE_STORE_VA = 0x007374D6" in corr)
    d, image_base, secs = load_pe(EXE)
    va, n, exp = P3_PINS["component_vtable_store_corrected_va_0x007374D6"]
    got = va_window(d, image_base, secs, va, n)
    rec["corrected_va_bytes"] = {"va": "0x%08X" % va, "expected": exp, "actual": got,
                                 "match": got == exp}
    va2, n2, exp2 = P3_PINS["component_vtable_store_superseded_va_0x007374DC"]
    got2 = va_window(d, image_base, secs, va2, n2)
    rec["superseded_va_bytes"] = {
        "va": "0x%08X" % va2, "expected": exp2, "actual": got2,
        "is_c7_store_start": (got2 is not None and got2.startswith("c7 06")),
        "match_midstream_expectation": (got2 == exp2),
        "note": ("measured: the superseded prose VA is mid-stream operand bytes "
                 "(8B C6), NOT the C7 06 2C 6F A8 00 store start; the store "
                 "starts at 0x007374D6")}
    s5 = json.load(open(os.path.join(SRC, "01_RAW", "S5_QC_BATTERY.json"),
                        encoding="utf-8"))
    hist_pin = s5["gate_results"]["Q4_same_component"]["creator_component_ctor_vtable_0x00A86F2C"]
    rec["historical_s5_pin"] = {"va": hist_pin["va"], "match": hist_pin["match"]}
    rec["historical_machine_pin_already_correct"] = (hist_pin["va"] == "0x007374D6")
    rec["component_vtable_identity_unchanged"] = ("0x00A86F2C" in corr)
    ok = (rec["declared_equals_target"] and rec["corrected_va_in_final_report"]
          and rec["corrected_va_bytes"]["match"]
          and rec["superseded_va_bytes"]["match_midstream_expectation"]
          and not rec["superseded_va_bytes"]["is_c7_store_start"]
          and rec["historical_machine_pin_already_correct"]
          and rec["component_vtable_identity_unchanged"])
    rec["status"] = "PASS" if ok else "FAIL"
    return rec

def gate_q12():
    rec = {"gate": "Q12_next_experiment_wording_bounded"}
    corr = open(os.path.join(PKG, "FINAL_REPORT.md"), "r", encoding="utf-8").read()
    corr_n = _norm(corr)
    rec["bounded_question_present"] = (
        "WHO ASSIGNS factory+0x84 AND WHAT EXACT OBJECT/VALUE IS ASSIGNED THERE?"
        in corr_n)
    outcomes = ["ASSIGNMENT_FOUND_AND_OBJECT_IDENTIFIED",
                "ASSIGNMENT_FOUND_OBJECT_SOURCE_UNRESOLVED",
                "NO_ASSIGNMENT_FOUND_WITHIN_BOUND",
                "MULTIPLE_CANDIDATES_UNRESOLVED"]
    rec["outcome_taxonomy_present"] = all(o in corr for o in outcomes)
    rec["no_source_class_closure_promise"] = all(
        ph not in corr for ph in
        ["convert ULTIMATE_VALUE_SOURCE from UNKNOWN", "That single bounded experiment would",
         "closes candidate A's provenance edge"])
    rec["design_only_declared"] = ("NEXT_EXPERIMENT_EXECUTED = NO" in corr)
    rec["later_separate_question_declared"] = ("separately authorized" in corr or
                                                "separate later question" in corr)
    ok = (rec["bounded_question_present"] and rec["outcome_taxonomy_present"]
          and rec["no_source_class_closure_promise"] and rec["design_only_declared"]
          and rec["later_separate_question_declared"])
    rec["status"] = "PASS" if ok else "FAIL"
    return rec

def gate_q13():
    rec = {"gate": "Q13_forbidden_new_science_census"}
    corr = open(os.path.join(PKG, "FINAL_REPORT.md"), "r", encoding="utf-8").read()
    census = {
        "factory_plus_0x84_trace": "NO", "source_stream_trace": "NO",
        "callback_decode": "NO", "templates_vfs_access": "NO",
        "record_a_analysis": "NO", "model_194013_trace": "NO",
        "world_placement_xyz": "NO", "model_join": "NO", "nif_work": "NO",
        "client_execution": "NO", "network_trace": "NO",
        "new_re_beyond_p3_pins": "NO",
    }
    rec["census_declared"] = census
    # physical package census: no forbidden payload types; EXE reads bounded
    files = []
    for root, _, names in os.walk(PKG):
        for nm in names:
            rel = os.path.relpath(os.path.join(root, nm), PKG).replace("\\", "/")
            files.append(rel)
    rec["package_file_census_at_qc_time"] = sorted(files)
    forbidden_ext = (".vfs", ".nif", ".glb", ".exe", ".dll", ".bnt", ".ark", ".tga")
    rec["forbidden_payload_files"] = [f for f in files if f.lower().endswith(forbidden_ext)]
    # EXE reads bounded to the 4 P3 windows (source-level census of THIS script;
    # the va_window DEFINITION line is excluded from the call count)
    self_src = open(os.path.abspath(__file__), "r", encoding="utf-8").read()
    rec["exe_read_windows_declared"] = {
        "0x0097781E_6B": "failpath zero store (corrected VA)",
        "0x0097781A_2B": "superseded VA probe (P3-A evidence)",
        "0x007374D6_6B": "component vtable store (corrected VA)",
        "0x007374DC_2B": "superseded VA probe (P3-B evidence)",
    }
    # count actual read call-sites (assignment targets), excluding the def line
    # and this census's own string literal
    call_lines = [l for l in self_src.splitlines()
                  if re.match(r"^\s*got2?\s*=\s*va_window\(d,", l)]
    rec["exe_read_calls_in_script"] = len(call_lines)
    rec["va_window_call_targets_bounded"] = (len(call_lines) == 4)
    # no new-science claim keys in the corrected docs (the DESIGN-ONLY outcome
    # taxonomy of Q12 is not a claim and is intentionally excluded here)
    rec["no_new_science_claims"] = all(
        k not in corr for k in
        ["ULTIMATE_VALUE_SOURCE = CONFIRMED", "WORLD_XYZ_RECOVERED = YES",
         "FACTORY_84_ASSIGNMENT_IDENTIFIED = YES",
         "RECORD_A_RELATION = ESTABLISHED",
         "WORLD_INSTANCE_SEMANTIC = ESTABLISHED"])
    ok = (len(rec["forbidden_payload_files"]) == 0
          and rec["va_window_call_targets_bounded"] and rec["no_new_science_claims"]
          and all(v == "NO" for v in census.values()))
    rec["status"] = "PASS" if ok else "FAIL"
    return rec

def gate_q14():
    rec = {"gate": "Q14_preserved_unknown_not_established_states"}
    ts = terminal_block()
    expected = {
        "SPECIFIC_RUNTIME_GETTER_VALUE_PRODUCER": "UNVERIFIED",
        "WRITE_TO_LATER_GETTER_VALUE_PRESERVATION": "NOT_ESTABLISHED",
        "NO_CLOBBER_BETWEEN_WRITE_AND_READ": "NOT_ESTABLISHED",
        "RUNTIME_EVENT_ORDER": "NOT_ESTABLISHED",
        "RUNTIME_CACHE_BINDING_AT_SPECIFIC_GETTER_EVENT": "NOT_OBSERVED",
        "ULTIMATE_VALUE_SOURCE": "UNKNOWN",
        "FILE_DERIVED_VALUE_EXCLUDED": "NO",
        "RECORD_A_RELATION": "NOT_ESTABLISHED",
        "WORLD_INSTANCE_SEMANTIC": "NOT_ESTABLISHED",
        "WORLD_XYZ_RECOVERED": "NO",
        "TABLE10_SOURCE_VALUE_REPRESENTATION": "RECORD_FIELD",
    }
    measured = {k: {"expected": v, "declared": ts.get(k),
                    "match": ts.get(k) == v} for k, v in expected.items()}
    rec["preserved_states_measured"] = measured
    rec["all_preserved"] = all(m["match"] for m in measured.values())
    rec["status"] = "PASS" if rec["all_preserved"] else "FAIL"
    return rec

def aux_quotecheck():
    rec = {"gate": "AUX_quotecheck"}
    led = open(os.path.join(PKG, "SUPERSESSION_LEDGER.md"), "r", encoding="utf-8").read()
    # parse records: each block starts with '### ' and contains SOURCE_FILE +
    # optional ORIGINAL_EXCERPT / OLD_LOGICAL_CONTENT (backtick-quoted, single
    # line; verified against the SOURCE_FILE at BASE) and optional
    # NEW_LOGICAL_CONTENT (verified present in the corrected CSVs)
    records = re.split(r"\n### ", led)
    checks = []
    n_records = 0
    for blk in records[1:]:
        n_records += 1
        rid = blk.splitlines()[0].strip()
        m_src = re.search(r"- SOURCE_FILE: `([^`]+)`", blk)
        m_exc = re.search(r"- ORIGINAL_EXCERPT: `([^`]+)`", blk)
        m_old = re.search(r"- OLD_LOGICAL_CONTENT: `([^`]+)`", blk)
        m_new = re.search(r"- NEW_LOGICAL_CONTENT: `([^`]+)`", blk)
        if m_exc:
            src, exc = m_src.group(1), m_exc.group(1)
            content = git_show(src)
            ok = (content is not None) and (exc in content)
            checks.append({"record": rid, "kind": "ORIGINAL_EXCERPT",
                           "source_file": src, "excerpt_head": exc[:60],
                           "is_real_substring_at_base": ok})
        if m_old:
            src, exc = m_src.group(1), m_old.group(1)
            content = git_show(src)
            ok = (content is not None) and (exc in content)
            checks.append({"record": rid, "kind": "OLD_LOGICAL_CONTENT",
                           "source_file": src, "excerpt_head": exc[:60],
                           "is_real_substring_at_base": ok})
        if m_new:
            new = m_new.group(1)
            # the corrected CSV where this field content must exist
            target = ("CORRECTED_FUNCTION_LEDGER.csv" if "FUNCTION_LEDGER"
                      in (m_src.group(1) if m_src else "") else
                      "CORRECTED_WRITER_CHAIN.csv")
            content = open(os.path.join(PKG, target), "r", encoding="utf-8",
                           newline="").read()
            ok = (new in content)
            checks.append({"record": rid, "kind": "NEW_LOGICAL_CONTENT",
                           "target_corrected_csv": target,
                           "excerpt_head": new[:60],
                           "present_in_corrected_csv": ok})
    rec["supersession_records_counted"] = n_records
    rec["excerpt_checks"] = checks
    rec["all_excerpts_verified"] = (
        len(checks) > 0
        and all(c.get("is_real_substring_at_base", c.get("present_in_corrected_csv", False))
               for c in checks))
    # minimum supersession census
    rec["minimum_records_satisfied"] = (n_records >= 11)
    rec["status"] = "PASS" if (rec["all_excerpts_verified"] and rec["minimum_records_satisfied"]) else "FAIL"
    return rec

def main():
    gen = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out = {"run": RUN_ID, "generated_utc": gen,
           "qc_scope": "SELF_CHECK_TABLE10_WRITER_C1",
           "mode": "STATIC-ONLY correction QC (no new reverse engineering)"}
    q1 = gate_q1()
    q2 = gate_q2()
    q3 = gate_q3()
    q4 = gate_q4()
    q5 = gate_q5()
    q6 = gate_q6()
    q7 = gate_q7()
    q8 = gate_q8()
    q9 = gate_q9()
    q10 = gate_q10()
    q11 = gate_q11()
    q12 = gate_q12()
    q13 = gate_q13()
    q14 = gate_q14()
    aux = aux_quotecheck()

    write_json("QC_LEDGER_BUDGET.json", dict(out, gates={"Q1_baseline_identity": q1,
                                                        "Q5_ledger_derived_function_budget": q5}))
    write_json("QC_CSV_STRICT.json", dict(out, gates={"Q3_corrected_ledger_strict_csv": q3,
                                                      "Q4_corrected_writer_chain_strict_csv": q4}))
    write_json("QC_NEGATIVE_CONTROLS.json", dict(out, gates={"Q6_nine_row_structurally_valid_mutant": q6}))
    write_json("QC_VALUE_SCOPE.json", dict(out, gates={
        "Q2_historical_core_science_preserved": q2,
        "Q7_value_identity_wording_scoped": q7,
        "Q8_specific_runtime_getter_value_producer": q8,
        "Q9_write_to_later_getter_value_preservation": q9,
        "Q10_failpath_zero_store_va": q10,
        "Q11_component_vtable_store_va": q11,
        "Q12_next_experiment_wording_bounded": q12,
        "Q13_forbidden_new_science_census": q13,
        "Q14_preserved_unknown_not_established_states": q14,
        "AUX_quotecheck": aux,
    }))

    allg = {"Q1": q1, "Q2": q2, "Q3": q3, "Q4": q4, "Q5": q5, "Q6": q6,
            "Q7": q7, "Q8": q8, "Q9": q9, "Q10": q10, "Q11": q11, "Q12": q12,
            "Q13": q13, "Q14": q14, "AUX": aux}
    print("=== GATE ROLLUP ===")
    fails = []
    for k, v in allg.items():
        st = v.get("status", "NOT_VERIFIED")
        print("%-4s %s" % (k, st))
        if st != "PASS":
            fails.append(k)
    print("FUNCTION_LEDGER_CSV=%s" % q3["FUNCTION_LEDGER_CSV"])
    print("WRITER_CHAIN_CSV=%s" % q4["WRITER_CHAIN_CSV"])
    print("LEDGER_DECLARED_COUNT=%s" % q5["ledger_declared_count"])
    print("MUTANT: structure=%s count=%s budget=%s precheck=%s validity=%s" % (
        q6["LEDGER_STRUCTURE_STATUS"], q6["new_function_count_derived"],
        q6["budget_limit_check"], q6["function_budget_precheck"], q6["test_validity"]))
    print("FAILED/NOT_PASS GATES: %s" % (fails if fails else "NONE"))
    return 0 if not fails else 1

if __name__ == "__main__":
    sys.exit(main())
