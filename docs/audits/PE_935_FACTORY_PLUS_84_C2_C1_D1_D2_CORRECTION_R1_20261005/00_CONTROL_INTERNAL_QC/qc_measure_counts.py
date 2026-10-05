# QC measurement script (independent count re-derivation from raw artifacts)
# RUN_ID: PE_935_QC_INTERNAL_20261005 (worker: pe-master-auditor, fresh context)
# Reads ONLY. Writes nothing. Static census of every load-bearing raw artifact.
import json, csv, hashlib, os, sys

sys.dont_write_bytecode = True

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005"

def load_json(rel):
    with open(os.path.join(PKG, rel), "r", encoding="utf-8-sig") as f:
        return json.load(f)

def load_csv(rel):
    with open(os.path.join(PKG, rel), "r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def sha256(rel):
    h = hashlib.sha256()
    with open(os.path.join(PKG, rel), "rb") as f:
        h.update(f.read())
    return h.hexdigest().upper()

print("=== 1. C1_PIN_EVIDENCE.json ===")
c1 = load_json(r"01_RAW\C1_PIN_EVIDENCE.json")
print("top_keys:", sorted(c1.keys()))
print("run:", c1.get("run"))
pins = c1.get("pins")
if pins is None:
    for k in c1:
        if isinstance(c1[k], list) and c1[k] and isinstance(c1[k][0], dict):
            print("candidate list:", k, "len:", len(c1[k]))
    pins = c1.get("pin_records") or c1.get("pin_evidence")
print("pin_count:", len(pins) if pins is not None else "STRUCTURE?")
if pins:
    kinds = {}
    statuses = {}
    ea_count = 0
    claim_ids = []
    for p in pins:
        kinds[p.get("kind")] = kinds.get(p.get("kind"), 0) + 1
        st = p.get("status") or p.get("pin_status") or "?"
        statuses[st] = statuses.get(st, 0) + 1
        if p.get("effective_address") is not None:
            ea_count += 1
        claim_ids.append(p.get("claim_id") or p.get("id"))
    print("kind_tally:", kinds)
    print("status_tally:", statuses)
    print("ea_objects:", ea_count)
    dup = len(claim_ids) - len(set(claim_ids))
    print("claim_ids:", len(claim_ids), "duplicates:", dup)
if "pin_totals" in c1:
    print("declared pin_totals:", c1["pin_totals"])

print()
print("=== 2. CORRECTED_PIN_LEDGER.csv ===")
rows = load_csv("CORRECTED_PIN_LEDGER.csv")
print("rows:", len(rows))
st = {}
ids = []
vas = []
for r in rows:
    k = r.get("status") or "?"
    st[k] = st.get(k, 0) + 1
    ids.append(r.get("claim_id") or r.get("id"))
    vas.append(r.get("instruction_va") or r.get("va"))
print("status_tally:", st)
print("unique_claim_ids:", len(set(ids)), "duplicates:", len(ids) - len(set(ids)))
print("unique_va:", len(set(vas)), "dup_va:", len(vas) - len(set(vas)))
print("columns:", list(rows[0].keys()))

print()
print("=== 3. CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv ===")
rows = load_csv("CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv")
print("rows:", len(rows))
cols = list(rows[0].keys())
print("columns:", cols)
# tally over plausible status-like columns
for col in cols:
    vals = {}
    n_unique = len(set(r[col] for r in rows))
    if n_unique <= 25:
        for r in rows:
            vals[r[col]] = vals.get(r[col], 0) + 1
        print("col", col, "->", vals)

print()
print("=== 4. AF3_PROVENANCE_LEDGER.csv ===")
rows = load_csv("AF3_PROVENANCE_LEDGER.csv")
print("rows:", len(rows))
for r in rows:
    print("  ", r.get("CANDIDATE_VA"), "|", r.get("FINAL_CLASSIFICATION"))

print()
print("=== 5. AF1_MUTATION_MATRIX.csv ===")
rows = load_csv("AF1_MUTATION_MATRIX.csv")
print("rows:", len(rows))
print("columns:", list(rows[0].keys()))
for r in rows:
    mid = r.get("MUTATION_ID") or r.get("ID") or r.get("mutation_id")
    unm = r.get("UNMUTATED_RESULT") or r.get("UNMUTATED")
    mut = r.get("MUTATED_RESULT") or r.get("MUTATED")
    print("  ", mid, "| unm:", unm, "| mut:", mut)

print()
print("=== 6. AF2_BOUNDARY_TEST_MATRIX.csv ===")
rows = load_csv("AF2_BOUNDARY_TEST_MATRIX.csv")
print("rows:", len(rows))
for r in rows:
    cid = r.get("CASE_ID") or r.get("ID") or r.get("case_id")
    bs = r.get("BOUNDARY_STATUS") or r.get("EXPECTED") or "?"
    print("  ", cid, "|", bs)

print()
print("=== 7. CQC_DECODER_UNIT_TESTS.json ===")
d = load_json(r"01_RAW\CQC_DECODER_UNIT_TESTS.json")
print("top_keys:", sorted(d.keys()))
for k in d:
    v = d[k]
    if isinstance(v, list) and v and isinstance(v[0], dict):
        print("list", k, "len:", len(v))
        fails = [x for x in v if str(x.get("result", x.get("status", ""))).upper() not in ("PASS", "OK", "TRUE")]
        print("  non-PASS:", len(fails))
        for x in v[:3]:
            print("   sample:", json.dumps(x)[:160])

print()
print("=== 8. CQC_BOUNDARY_COUNTEREXAMPLES.json ===")
d = load_json(r"01_RAW\CQC_BOUNDARY_COUNTEREXAMPLES.json")
print("top_keys:", sorted(d.keys()))
for k in d:
    v = d[k]
    if isinstance(v, list) and v and isinstance(v[0], dict):
        print("list", k, "len:", len(v), "ids:", [x.get("case_id") or x.get("id") or x.get("CASE_ID") for x in v])

print()
print("=== 9. CQC_MUTATION_RESULTS.json ===")
d = load_json(r"01_RAW\CQC_MUTATION_RESULTS.json")
print("top_keys:", sorted(d.keys()))
print(json.dumps(d)[:2000])

print()
print("=== 10. D2_MUTATION_RESULTS.json ===")
d = load_json(r"01_RAW\D2_MUTATION_RESULTS.json")
print("top_keys:", sorted(d.keys()))
for k in d:
    v = d[k]
    if isinstance(v, list) and v and isinstance(v[0], dict):
        print("list", k, "len:", len(v))
        for x in v:
            mid = x.get("mutation_id") or x.get("id") or "?"
            print("  ", mid, "| unm:", x.get("unmutated_result") or x.get("clean_result"),
                  "| mut:", x.get("mutated_result"),
                  "| predicates:", x.get("failing_predicates") or x.get("failed_predicates"),
                  "| substitute_fail:", x.get("substitute_failure") or x.get("substitute_failure_check"))

print()
print("=== 11. D1_INDEPENDENT_ORACLE_RECORDS.json ===")
d = load_json(r"01_RAW\D1_INDEPENDENT_ORACLE_RECORDS.json")
print("top_keys:", sorted(d.keys()))
fx = None
for k in d:
    v = d[k]
    if isinstance(v, list) and v and isinstance(v[0], dict):
        print("list", k, "len:", len(v))
        if fx is None:
            fx = v
if fx:
    print("fixture sample keys:", sorted(fx[0].keys()))
    for x in fx:
        fid = x.get("fixture_id") or x.get("id") or "?"
        if "D1" in str(fid):
            print("  D1 fixture:", fid, "| expected:", str(x.get("expected"))[:80], "| verdict/oracle:", str(x.get("oracle_verdict") or x.get("raw_stdout") or "")[:100].replace("\n", " "))

print()
print("=== 12. D1_BOUNDARY_FALSIFIER.json ===")
d = load_json(r"01_RAW\D1_BOUNDARY_FALSIFIER.json")
print(json.dumps(d, indent=1)[:3500])

print()
print("=== 13. EXPECTED_PIN_REGISTRY.json ===")
d = load_json("EXPECTED_PIN_REGISTRY.json")
print("expected_total:", d.get("expected_total"), "| tally:", d.get("expected_role_tally"), "| ea_req:", d.get("expected_ea_required_count"))
pr = d.get("pins", [])
print("pins len:", len(pr))
t = {}
for p in pr:
    t[p["role"]] = t.get(p["role"], 0) + 1
print("measured role tally:", t)
ids = [p["claim_id"] for p in pr]
print("unique:", len(set(ids)), "dup:", len(ids) - len(set(ids)))
eacnt = sum(1 for p in pr if p.get("expect_ea"))
print("pins with expect_ea:", eacnt)

print()
print("=== 14. CQC_FINAL.json ===")
d = load_json(r"01_RAW\CQC_FINAL.json")
print("top_keys:", sorted(d.keys()))
g = d.get("gates") or d.get("gate_results")
if g:
    print("gates:", g)
mt = d.get("mutations") or d.get("mutation_summary") or {}
print("mutation summary:", json.dumps(mt)[:800])
print("verdict:", d.get("verdict") or d.get("qc_verdict"))
gd = d.get("gate_details") or {}
if "Q2" in gd:
    q2 = gd["Q2"]
    print("Q2 keys:", sorted(q2.keys()) if isinstance(q2, dict) else type(q2))
    print("Q2 d2_pin_universe:", json.dumps(q2.get("d2_pin_universe"))[:1200] if isinstance(q2, dict) else "")
