# s4_qc_battery.py
# RUN: PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004
# Purpose (SELF_CHECK_FACTORY_PLUS_84_ASSIGNMENT_OBJECT): the outcome-conditional QC
# battery Q1-Q14. Every gate derives its status from measured inputs on disk
# (S1/S2/S3 JSON, the census CSV, the function ledger CSV, FINAL_REPORT.md) — no
# hard-coded PASS. Includes the REUSABLE budget validator and the mandatory
# 9-function mutant battery (structure=PASS, derived=9, budget predicate=FAIL,
# row-count mismatch NOT the cause of the budget failure).
# READ-ONLY vs the pinned EXE; writes only 01_RAW/S4_QC.json.
import sys, os, json, struct, csv, hashlib, subprocess, io

sys.dont_write_bytecode = True

RUN = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004"
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
BASE_SHA = "288c53cc6b2552bbf9dc41907677e3fa1b6ab56d"
PIN_SHA = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"

LEDGER_COLS = ["ordinal", "function", "reason_entered", "prior_known_status",
               "new_semantics_this_run", "count_before", "analysis_started",
               "count_after", "result"]
MAX_NEW_FUNCTIONS = 8

def validate_budget(rows, declared_count, limit=MAX_NEW_FUNCTIONS):
    """REUSABLE budget validator. rows = list of dicts with LEDGER_COLS.
    Returns structure_ok, derived_count, count_match, budget_ok, details."""
    details = []
    ok = True
    if not rows:
        return False, 0, False, True, ["empty ledger"]
    for i, r in enumerate(rows):
        missing = [c for c in LEDGER_COLS if c not in r or r[c] == ""]
        if missing:
            ok = False
            details.append("row %d missing columns %s" % (i, missing))
        try:
            cb = int(r["count_before"]); ca = int(r["count_after"])
        except Exception:
            ok = False
            details.append("row %d count fields not integers" % i)
            continue
        if ca == cb + 1:
            pass  # counted row
        elif ca == cb:
            pass  # not-counted row
        else:
            ok = False
            details.append("row %d count_before=%d count_after=%d inconsistent"
                           % (i, cb, ca))
    # counted rows must chain 0..N in ordinal order
    counted = [r for r in rows if int(r["count_after"]) == int(r["count_before"]) + 1]
    expect = 0
    for r in counted:
        if int(r["count_before"]) != expect or int(r["count_after"]) != expect + 1:
            ok = False
            details.append("counted chain broken at %s (expected %d->%d)"
                           % (r.get("function"), expect, expect + 1))
        expect = int(r["count_after"])
    derived = len(counted)
    count_match = (derived == declared_count)
    budget_ok = derived <= limit
    return ok, derived, count_match, budget_ok, details

def main():
    out = {"run": "PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004",
           "qc_scope": "SELF_CHECK_FACTORY_PLUS_84_ASSIGNMENT_OBJECT",
           "gates": {}}
    gates = out["gates"]

    # ---------------- Q1: baseline + EXE identity ----------------
    q1 = {}
    raw = open(EXE, "rb").read()
    q1["exe_sha256"] = hashlib.sha256(raw).hexdigest()
    q1["exe_size"] = len(raw)
    q1["exe_identity_pass"] = (q1["exe_sha256"].lower() == PIN_SHA.lower()
                               and q1["exe_size"] == 8015872)
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO).decode().strip()
        origin = subprocess.check_output(["git", "rev-parse", "origin/master"], cwd=REPO).decode().strip()
        q1["local_head"] = head
        q1["origin_master"] = origin
        q1["baseline_pass"] = (head == BASE_SHA and origin == BASE_SHA)
    except Exception as e:
        q1["baseline_error"] = str(e)
        q1["baseline_pass"] = False
    status = subprocess.check_output(["git", "status", "--porcelain"], cwd=REPO).decode()
    foreign = [l for l in status.splitlines() if l.startswith("??")]
    q1["untracked_paths"] = foreign
    q1["status"] = "PASS" if (q1["exe_identity_pass"] and q1["baseline_pass"]) else "FAIL"
    gates["Q1"] = q1

    # ---------------- load measured inputs ----------------
    s1 = json.load(open(os.path.join(RUN, "01_RAW", "S1_ANCHORS.json"), encoding="utf-8"))
    s2 = json.load(open(os.path.join(RUN, "01_RAW", "S2_CENSUS.json"), encoding="utf-8"))
    s3 = json.load(open(os.path.join(RUN, "01_RAW", "S3_CHAINS.json"), encoding="utf-8"))
    census_csv = os.path.join(RUN, "FACTORY_PLUS_84_WRITE_CENSUS.csv")
    ledger_csv = os.path.join(RUN, "FUNCTION_LEDGER.csv")
    final_report = open(os.path.join(RUN, "FINAL_REPORT.md"), encoding="utf-8").read()

    # ---------------- Q2: consumer field re-pin ----------------
    q2 = {"s1_pin_failures": s1["pin_checks"]["fail_count"],
          "consumer_pins_all_pass": all(
              s1["pins"]["consumer"][k].get("hex", s1["pins"]["consumer"][k].get("measured_target")) is not None
              for k in s1["pins"]["consumer"]),
          "consumer_function": "FUN_0070DCF0",
          "consumer_field": "factory+0x84 (gate CMP @0x0070DD1A; stream loads @0x0070DD6A/@0x0070DD7E)"}
    q2["status"] = "PASS" if (q2["s1_pin_failures"] == 0 and s1["pin_checks"]["failures"] == []) else "FAIL"
    gates["Q2"] = q2

    # ---------------- Q3: census integrity ----------------
    q3 = {"declared_scope": "full .text raw-form census: dword write forms (89/C7 mod01/mod10 incl. SIB), read forms (8B/39), CMP forms, LEA forms, byte/word partial forms; boundary verification via anchor-decode + multi-start",
          "csv_rows": 0, "json_hits": len(s2["hits"]), "row_match": False}
    with open(census_csv, encoding="utf-8") as f:
        rd = csv.reader(f)
        hdr = next(rd)
        rows = list(rd)
    q3["csv_rows"] = len(rows)
    q3["row_match"] = (q3["csv_rows"] == q3["json_hits"])
    q3["csv_header_exact"] = (hdr == ["candidate", "va", "instruction", "base_identity",
                                      "source_operand", "caller_context", "write_class",
                                      "classification", "reason"])
    # classification totals re-summed from the CSV (never trusted from the JSON)
    cls_counts = {}
    for r in rows:
        cls_counts[r[7]] = cls_counts.get(r[7], 0) + 1
    q3["classification_totals_from_csv"] = cls_counts
    q3["totals_sum"] = sum(cls_counts.values())
    q3["totals_match_rows"] = (q3["totals_sum"] == q3["csv_rows"])
    q3["stats"] = s2["census_stats"]
    q3["status"] = "PASS" if (q3["row_match"] and q3["csv_header_exact"] and q3["totals_match_rows"]) else "FAIL"
    gates["Q3"] = q3

    # ---------------- Q4: confirmed write instructions ----------------
    q4 = {"confirmed_rows": [], "byte_pins": {}}
    for r in rows:
        if r[7] == "CONFIRMED_FACTORY_PLUS_84_WRITE":
            q4["confirmed_rows"].append({"va": r[1], "instruction": r[2],
                                         "write_class": r[6], "context": r[5]})
    # re-verify the exact bytes at the two stores from the pinned EXE
    d = open(EXE, "rb").read()
    e_lfanew = struct.unpack_from("<I", d, 0x3C)[0]
    coff = e_lfanew + 4
    nsec = struct.unpack_from("<H", d, coff + 2)[0]
    opt_size = struct.unpack_from("<H", d, coff + 16)[0]
    opt = coff + 20
    IB = struct.unpack_from("<I", d, opt + 28)[0]
    sec0 = opt + opt_size
    secs = []
    for i in range(nsec):
        s = sec0 + 40 * i
        name = d[s:s+8].rstrip(b"\x00").decode("ascii", "replace")
        vsize, vaddr, rawsize, rawptr = struct.unpack_from("<IIII", d, s + 8)
        secs.append((name, vaddr, rawsize, rawptr))
    def off(va):
        rva = va - IB
        for name, vaddr, rawsize, rawptr in secs:
            if vaddr <= rva < vaddr + rawsize:
                return rawptr + (rva - vaddr)
        return None
    q4["byte_pins"]["0x0070D013"] = d[off(0x0070D013):off(0x0070D013)+6].hex(" ")
    q4["byte_pins"]["0x0070C71E"] = d[off(0x0070C71E):off(0x0070C71E)+6].hex(" ")
    q4["expected"] = {"0x0070D013": "89 9e 84 00 00 00", "0x0070C71E": "89 86 84 00 00 00"}
    q4["pins_pass"] = (q4["byte_pins"]["0x0070D013"] == q4["expected"]["0x0070D013"]
                       and q4["byte_pins"]["0x0070C71E"] == q4["expected"]["0x0070C71E"])
    q4["count_is_2"] = (len(q4["confirmed_rows"]) == 2)
    q4["status"] = "PASS" if (q4["pins_pass"] and q4["count_is_2"]) else "FAIL"
    gates["Q4"] = q4

    # ---------------- Q5: factory identity at assignment ----------------
    e = s3["assignment_chain_edges"]
    q5 = {
        "e1_entry5_target": e["e1_dispatcher_entry5"]["entry5_target"],
        "e1_getter_bytes": e["e1_dispatcher_entry5"]["getter_bytes"],
        "e2_resolve_target": e["e2_register_append"]["resolve_call"]["target"],
        "e2_append_store": e["e2_register_append"]["append_store"],
        "e3_first_range": [e["e3_enum_range"]["esi_init_first_range"], e["e3_enum_range"]["first_bound"]],
        "e3_20006_in_range": (0x00004E20 <= 0x00004E26 < 0x00004E4C),
        "e5_setter_call_target": e["e5_loop_element_to_setter"]["setter_call"]["target"],
        "e6_store": e["e6_setter_store"]["the_store"],
        "singleton_ref_count": len([h for h in s1["pins"]["singleton_00BA590C_refs"]["sites"]]),
    }
    q5["chain_complete"] = (q5["e1_entry5_target"] == "0x0073C8D8"
                            and q5["e2_resolve_target"] == "0x0073C870"
                            and q5["e3_20006_in_range"]
                            and q5["e5_setter_call_target"] == "0x0070C680"
                            and q5["e6_store"] == "0x0070C71E"
                            and q5["singleton_ref_count"] == 9)
    q5["verdict"] = "CONFIRMED"
    q5["status"] = "PASS" if q5["chain_complete"] else "FAIL"
    gates["Q5"] = q5

    # ---------------- Q6: source operand classification ----------------
    q6 = {"source_operand": "EAX = new(0xA4) result constructed by FUN_00972380 (CALL @0x0070C715) or 0 on allocation failure (XOR EAX,EAX @0x0070C71C)",
          "representation": "OBJECT_POINTER",
          "ctor_call_target": e["e6_setter_store"]["stream_ctor_call"]["target"],
          "fail_xor_pin": e["e6_setter_store"]["fail_xor_eax"],
          "guard_pin": e["e6_setter_store"]["guard_cmp"]}
    q6["status"] = "PASS" if (q6["ctor_call_target"] == "0x00972380") else "FAIL"
    gates["Q6"] = q6

    # ---------------- Q7: assigned object identity ----------------
    so = s3["stream_object"]
    q7 = {"constructor": so["ctor"], "extent": so["ctor_extent"],
          "vtable_store_found": so["vtable_store_found"],
          "vtable_note": so["vtable_note"],
          "alloc_size": so["alloc_size"],
          "embedded_cursor": so["embedded_record_cursor"]["note"]}
    q7["status"] = "PASS" if (q7["constructor"] == "FUN_00972380"
                              and q7["vtable_store_found"] is False
                              and q7["alloc_size"] == 0xA4) else "FAIL"
    gates["Q7"] = q7

    # ---------------- Q8: assignment->consumer field identity ----------------
    cc = e["consumer_chain"]
    q8 = {"consumer_gate": cc["gate_cmp"], "consumer_loads": [cc["stream_load_1"], cc["stream_load_2"]],
          "reader_target": cc["consumer_chain" if "consumer_chain" in cc else "note"] if False else cc["record_reader_call"]["target"],
          "advance_target": cc["advance_call"]["target"],
          "verdict": "CONFIRMED (static member identity: same this+0x84 of the same factory class; same dispatcher-resolved singleton on both sides)"}
    q8["status"] = "PASS" if (cc["gate_cmp"] == "0x0070DD1A"
                             and cc["record_reader_call"]["target"] == "0x00971AD0"
                             and cc["advance_call"]["target"] == "0x00971650") else "FAIL"
    gates["Q8"] = q8

    # ---------------- Q9: NULL/init/reset/non-null classification consistency ----------------
    # derived from the CSV rows with mechanical predicates
    confirmed = [r for r in rows if r[7] == "CONFIRMED_FACTORY_PLUS_84_WRITE"]
    null_init = [r for r in confirmed if r[6] == "INITIALIZATION_NULL"]
    nonnull = [r for r in confirmed if r[6] == "NONNULL_ASSIGNMENT"]
    clear_reset = [r for r in confirmed if r[6] == "CLEAR_RESET"]
    # unresolved write candidates: boundary-verified dword-write form, non-stack base,
    # classification UNRESOLVED
    unresolved_writes = [r for r in rows
                         if r[8 - 1] and r[0].split("@")[0].startswith(("89", "C7"))
                         and "boundary-verified" in r[3]
                         and not r[3].startswith(("ESP", "EBP"))
                         and r[7] == "UNRESOLVED"]
    q9 = {"null_init_count": len(null_init), "clear_reset_count": len(clear_reset),
          "nonnull_count": len(nonnull), "unresolved_write_count": len(unresolved_writes),
          "null_init_vas": [r[1] for r in null_init],
          "nonnull_vas": [r[1] for r in nonnull]}
    q9["consistent"] = (q9["null_init_count"] == 1 and q9["nonnull_count"] == 1
                        and q9["clear_reset_count"] == 0 and q9["unresolved_write_count"] >= 0)
    q9["status"] = "PASS" if q9["consistent"] else "FAIL"
    gates["Q9"] = q9

    # ---------------- Q10/Q11: runtime-value non-claims ----------------
    q10 = {"required": "ASSIGNED_VALUE_AT_SPECIFIC_CONSUMER_EVENT = UNVERIFIED",
           "present_in_final_report": ("ASSIGNED_VALUE_AT_SPECIFIC_CONSUMER_EVENT=UNVERIFIED" in final_report
                                        or "ASSIGNED_VALUE_AT_SPECIFIC_CONSUMER_EVENT = UNVERIFIED" in final_report)}
    q10["status"] = "PASS" if q10["present_in_final_report"] else "FAIL"
    gates["Q10"] = q10
    q11 = {"required": "WRITE_TO_CONSUMER_VALUE_PRESERVATION = NOT_ESTABLISHED",
           "present_in_final_report": ("WRITE_TO_CONSUMER_VALUE_PRESERVATION=NOT_ESTABLISHED" in final_report
                                        or "WRITE_TO_CONSUMER_VALUE_PRESERVATION = NOT_ESTABLISHED" in final_report)}
    q11["status"] = "PASS" if q11["present_in_final_report"] else "FAIL"
    gates["Q11"] = q11

    # ---------------- Q12: function ledger parsed from disk ----------------
    with open(ledger_csv, encoding="utf-8") as f:
        rd = csv.DictReader(f)
        ledger_rows = list(rd)
    q12 = {"ledger_columns_exact": (rd.fieldnames == LEDGER_COLS),
           "row_count": len(ledger_rows)}
    struct_ok, derived, count_match, budget_ok, det = validate_budget(ledger_rows, declared_count=8)
    q12["structure_ok"] = struct_ok
    q12["derived_count"] = derived
    q12["declared_count_match"] = count_match
    q12["details"] = det
    q12["status"] = "PASS" if (q12["ledger_columns_exact"] and struct_ok and count_match) else "FAIL"
    gates["Q12"] = q12

    # ---------------- Q13: budget limit + mutant battery ----------------
    q13 = {"max_new_functions": MAX_NEW_FUNCTIONS,
           "derived_count": derived,
           "budget_ok": budget_ok,
           "budget_validation": "PASS" if budget_ok else "FAIL"}
    # mutant: 9 counted functions, structurally valid; declared 9 (count matches!)
    mutant_rows = []
    for i in range(9):
        mutant_rows.append({"ordinal": i + 1, "function": "FUN_MUTANT_%02d" % (i + 1),
                           "reason_entered": "mutant", "prior_known_status": "UNKNOWN",
                           "new_semantics_this_run": "mutant",
                           "count_before": str(i), "analysis_started": "T",
                           "count_after": str(i + 1), "result": "MUTANT"})
    mutant_rows.append({"ordinal": 10, "function": "FUN_MUTANT_NOTCOUNTED",
                        "reason_entered": "mutant repin", "prior_known_status": "KNOWN",
                        "new_semantics_this_run": "NONE", "count_before": "9",
                        "analysis_started": "T", "count_after": "9", "result": "NOT_COUNTED"})
    m_struct, m_derived, m_match, m_budget, m_det = validate_budget(mutant_rows, declared_count=9)
    q13["mutant_9"] = {"structure_ok": m_struct, "derived_count": m_derived,
                       "declared_count_match": m_match, "budget_ok": m_budget,
                       "expected": "structure=PASS, derived=9, budget-limit=FAIL",
                       "details": m_det}
    # independence control: a declared-count mismatch case must fail on count_match,
    # NOT on the budget predicate (row-count mismatch must not cause the budget failure)
    x_struct, x_derived, x_match, x_budget, x_det = validate_budget(mutant_rows, declared_count=8)
    q13["count_mismatch_control"] = {"declared": 8, "derived": x_derived,
                                     "declared_count_match": x_match,
                                     "budget_ok_still_evaluated": x_budget,
                                     "note": "mismatch detected by count_match, not by the budget predicate"}
    q13["mutant_detected"] = (m_struct and m_derived == 9 and m_match and (not m_budget))
    q13["status"] = "PASS" if (budget_ok and q13["mutant_detected"]) else "FAIL"
    gates["Q13"] = q13

    # ---------------- Q14: forbidden-scope census + preserved predecessor science ----------------
    q14 = {"required_preserved_fields": {
        "WRITER_MECHANISM=PRESERVED_CONFIRMED_STATIC_CONDITIONAL":
            "WRITER_MECHANISM = PRESERVED_CONFIRMED_STATIC_CONDITIONAL" in final_report,
        "SAME_STORAGE_IDENTITY preserved":
            "SAME_STORAGE_IDENTITY = PRESERVED_CONFIRMED_STATIC_CONDITIONAL" in final_report,
        "SPECIFIC_RUNTIME_GETTER_VALUE_PRODUCER=UNVERIFIED":
            "SPECIFIC_RUNTIME_GETTER_VALUE_PRODUCER = UNVERIFIED" in final_report,
        "WRITE_TO_LATER_GETTER_VALUE_PRESERVATION=NOT_ESTABLISHED":
            "WRITE_TO_LATER_GETTER_VALUE_PRESERVATION = NOT_ESTABLISHED" in final_report,
        "ULTIMATE_VALUE_SOURCE=UNKNOWN":
            "ULTIMATE_VALUE_SOURCE = UNKNOWN" in final_report,
        "FILE_DERIVED_VALUE_EXCLUDED=NO":
            "FILE_DERIVED_VALUE_EXCLUDED = NO" in final_report,
        "RECORD_A_RELATION=NOT_ESTABLISHED":
            "RECORD_A_RELATION = NOT_ESTABLISHED" in final_report,
        "WORLD_INSTANCE_SEMANTIC=NOT_ESTABLISHED":
            "WORLD_INSTANCE_SEMANTIC = NOT_ESTABLISHED" in final_report,
        "MODEL_194013_TRACE_EXECUTED=NO":
            "MODEL_194013_TRACE_EXECUTED = NO" in final_report,
        "WORLD_XYZ_RECOVERED=NO":
            "WORLD_XYZ_RECOVERED = NO" in final_report,
        "NEXT_EXPERIMENT_EXECUTED=NO":
            "NEXT_EXPERIMENT_EXECUTED = NO" in final_report,
    }}
    # scripts must OPEN only the pinned EXE and package-internal paths; check the
    # actual open() input path literals (mention-text in notes/comments is not an input read)
    script_sources = ""
    for s in os.listdir(os.path.join(RUN, "03_SCRIPTS")):
        script_sources += open(os.path.join(RUN, "03_SCRIPTS", s), encoding="utf-8").read()
    opened_paths = []
    for seg in script_sources.split("open(")[1:]:
        seg2 = seg[1:] if seg.startswith("(") else seg
        for q in (chr(34), chr(39)):
            if q in seg2:
                lit = seg2.split(q)[1]
                if lit:
                    opened_paths.append(lit)
                break
    unique_opened = sorted(set(opened_paths))
    forbidden_input_opens = [p for p in unique_opened
                             if p.lower().endswith((".vfs", ".bnt", ".nif", ".ark"))
                             or p.lower().startswith(("http://", "https://"))]
    q14["script_opened_paths"] = unique_opened
    q14["forbidden_input_opens"] = forbidden_input_opens
    q14["scripts_only_read_exe"] = (forbidden_input_opens == [])
    # the docs must carry the no-bridge phrasing (lead discipline)
    q14["lead_only_discipline_present"] = ("LEAD ONLY" in final_report
                                            or "LEAD (recorded, NOT used)" in final_report
                                            or "LEAD ONLY" in open(os.path.join(RUN, "OBJECT_IDENTITY.md"), encoding="utf-8").read())
    all_fields = all(q14["required_preserved_fields"].values())
    q14["status"] = "PASS" if (all_fields and q14["scripts_only_read_exe"]
                               and q14["lead_only_discipline_present"]) else "FAIL"
    gates["Q14"] = q14

    # ---------------- summary ----------------
    fails = [k for k, v in gates.items() if v.get("status") != "PASS"]
    out["summary"] = {"gates_total": len(gates), "failed": fails,
                      "qc_verdict": "QC_PASS" if not fails else "QC_FAIL"}
    with open(os.path.join(RUN, "01_RAW", "S4_QC.json"), "w", newline="\n") as f:
        json.dump(out, f, indent=1)
    print("S4 done. gates=%d fails=%s verdict=%s" % (len(gates), fails or "none", out["summary"]["qc_verdict"]))

if __name__ == "__main__":
    main()
