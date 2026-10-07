"""Fresh-context internal QC re-verification — PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006.
Independent re-measurement of the load-bearing pins (own reads from the hash-pinned EXE),
receiver-preservation checks, budget and ledger checks, repo-state checks.
Writes 03_SCRIPTS/qc_reverify_results.json. QC does not repair executor evidence in place;
it records its own findings.
"""
import csv, hashlib, json, struct, subprocess, sys

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006"
REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
OUT = PKG + r"\03_SCRIPTS\qc_reverify_results.json"

data = open(EXE, "rb").read()
res = {"checks": {}, "findings": []}

def chk(name, ok, detail):
    res["checks"][name] = {"ok": bool(ok), "detail": detail}

# S1 EXE identity
chk("S1_exe_identity", len(data) == 8015872 and hashlib.sha256(data).hexdigest().upper() == "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31",
    f"size {len(data)}, sha {hashlib.sha256(data).hexdigest().upper()}")

# PE mapper
e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
coff = e_lfanew + 4
nsec = struct.unpack_from("<H", data, coff + 2)[0]
size_opt = struct.unpack_from("<H", data, coff + 16)[0]
sec0 = coff + 20 + size_opt
sections = []
for i in range(nsec):
    off = sec0 + 40 * i
    vsize, va, rsize, roff = struct.unpack_from("<IIII", data, off + 8)
    sections.append((va, max(vsize, rsize), roff))
def rd(va, n):
    rva = va - 0x400000
    for va_s, sz, roff in sections:
        if va_s <= rva < va_s + sz:
            return data[roff + (rva - va_s):roff + (rva - va_s) + n]
    raise ValueError(va)
def hx(va, n):
    return " ".join(f"{b:02X}" for b in rd(va, n))

# S2 load-bearing byte pins (independent re-reads)
pins = {
    "PA1_store_SF30":            (0x005093C3, 3, "89 45 30"),
    "PA1_ninode_ctor_call":      (0x005093B8, 5, "E8 43 CC 2A 00"),
    "PA2_extradata_reg_window":  (0x00509494, 14, "8B 4D 30 50 68 44 D4 A7 00 C6 44 24 4C 02"),
    "PA2_reg_call":              (0x0050A0A2 if False else 0x005094A2, 5, "E8 D9 D5 2A 00"),
    "PA3_slot3_read_SF30":       (0x0050A05B, 3, "8B 4E 30"),
    "PA3_slot3_dispatch":        (0x0050A064, 2, "FF D0"),
    "PA4_cmo_key_call":          (0x00528FD9, 5, "E8 52 B1 EE FF"),
    "PA4_sf_store":              (0x00528FEA, 6, "89 86 C0 00 00 00"),
    "CH1_callback_imm":          (0x006C3FB0, 5, "BB 20 D7 8B 00"),
    "CH1_scheduler_call":        (0x006C3FCD, 5, "E8 6E F6 FF FF"),
    "CL06_8bd720_body":          (0x008BD720, 4, "8D 41 18 C3"),
    "CL07_cmo_calls_509510":     (0x0052902F, 5, "E8 DC 04 FE FF"),
    "CL07_cmo_calls_509070":    (0x0052903E, 5, "E8 2D 00 FE FF"),
    "CL07_cmo_calls_509850":    (0x00529050, 5, "E8 FB 07 FE FF"),
    "CL08_transform_translate":  (0x00509913, 2, "89 08"),
    "CL09_7bf500_nochild_head":  (0x007BF506, 3, "8B 4E 2C"),
    "CL10_sf20_store":           (0x0050A3AC, 3, "89 7E 20"),
    "CL10_child_getter_call":    (0x0050A3AF, 5, "E8 1C C3 1B 00"),
    "CL12_join_parent_load":     (0x0050A3E9, 3, "8B 4E 30"),
    "CL12_join_virtual_call":    (0x0050A3F7, 2, "FF D2"),
    "CL11_attach_inc_refcount":  (0x007B5846, 3, "01 5E 04"),
    "CL11_attach_children_obj":  (0x007B5864, 6, "8D 8F C8 00 00 00"),
    "CL11_attach_used_field":    (0x007B5898, 5, "8B 5F 0C 3B 5F"),
    "CL11_attach_setat_call":    (0x007B58B5, 5, "E8 16 38 FC FF"),
    "CL11_attach_dec_destroy":   (0x007B58CF, 3, "01 7E 04"),
}
bad = []
for name, (va, n, exp) in pins.items():
    got = hx(va, n)
    if got != exp:
        bad.append(f"{name}: va {va:#010x} got '{got}' expect '{exp}'")
chk("S2_load_bearing_pins", len(bad) == 0, f"{len(pins)} pins re-read; mismatches: {bad if bad else 'NONE'}")

# S3 rel32 target arithmetic (independent recomputation)
rel_checks = {
    0x005093B8: 0x007B6000,
    0x005094A2: 0x007B6A80,
    0x00528FD9: 0x00414130,
    0x00528FE1: 0x005247C0,
    0x006A39ED: 0x005247C0,
    0x006A3A9D: 0x0050A310,
    0x0050A3AF: 0x006C66D0,
    0x0050A3D8: 0x0050A1E0,
    0x0050A3FB: 0x007BF900,
    0x0050A402: 0x007BF630,
    0x0050A412: 0x007BF500,
    0x00509972: 0x007BF500,
    0x007B584C: 0x007BF470,
    0x007B5872: 0x007B55E0,
    0x007B58A8: 0x00788570,
    0x007B58B5: 0x007790D0,
    0x006C3FCD: 0x006C3640,
}
bad = []
for va, exp in rel_checks.items():
    rel = int.from_bytes(rd(va + 1, 4), "little", signed=True)
    tgt = va + 5 + rel
    if tgt != exp:
        bad.append(f"{va:#010x}: target {tgt:#010x} != {exp:#010x}")
chk("S3_rel32_arithmetic", len(bad) == 0, f"{len(rel_checks)} call targets recomputed; mismatches: {bad if bad else 'NONE'}")

# S4 receiver preservation at the join site (ECX not clobbered between the load and the call)
win = rd(0x0050A3E9, 0x0050A3F7 - 0x0050A3E9 + 2)
expected_win = "8B 4E 30 8B 01 8B 90 A4 00 00 00 6A 00 57 FF D2"
chk("S4_join_receiver_preservation", hx(0x0050A3E9, len(win)) == expected_win,
    f"window 0x0050A3E9..0x0050A3F8 = '{hx(0x0050A3E9, len(win))}'; ECX loaded at 0x0050A3E9, only MOV EAX,[ECX] (read) between, no ECX write before CALL EDX at 0x0050A3F7")

# S5 the join-site ESI==SF: function head re-read
chk("S5_fun_50a310_head_esi_sf", hx(0x0050A310, 8) == "51 55 56 8B F1 80 7E 24",
    "push ecx; push ebp; push esi; mov esi,ecx (this=SF at entry per the E5 callsite chain); then flags check")

# S6 the SF creation chain in FUN_006A3930 (independent re-read of the two load-bearing sites)
chk("S6_sf_creation_chain", hx(0x006A39EB, 11) == "8B C8 E8 CE 0D E8 FF 8D 4C 24 18" and hx(0x006A39F2, 7) == "8D 4C 24 18 89 46 18",
    "mov ecx,eax (SF result) -> call FUN_005247C0 @0x006A39ED -> mov [esi+0x18],eax @0x006A39F6 (SF stored at [ACLD+0x18])")

# S7 the manager chain in FUN_006A3930
chk("S7_manager_chain", hx(0x006A3A48, 16) == "68 30 01 00 00 E8 72 99 2B 00 8B E8 83 C4 04 89" and hx(0x006A3A75, 8) == "8B CD E8 D4 D2 01 00 8B",
    "push 0x130; call operator new; ebp=block; FUN_006C0D50(this=block) @0x006A3A77; then FUN_006C8B20/BB0 and mov ecx,[esi+0x18] (SF) -> FUN_0050A310")

# S8 NiNode vtable slot 41 (data read)
import struct as st
vt = 0x00A8CCF4
slot41 = st.unpack("<I", rd(vt + 0xA4, 4))[0]
slot42 = st.unpack("<I", rd(vt + 0xA8, 4))[0]
chk("S8_ninode_vtable_slots", slot41 == 0x007B5810 and slot42 == 0x007B5A00,
    f"slot 41 (+0xA4) = {slot41:#010x} (expect 0x007B5810); slot 42 (+0xA8) = {slot42:#010x} (detach-shaped call at 0x0050A35A)")

# S9 budgets
def rows(path):
    with open(PKG + "\\" + path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))
fn = rows("FUNCTION_BUDGET.csv")
ed = rows("EDGE_LEDGER.csv")
cd = rows("CANDIDATE_LEDGER.csv")
chk("S9_budgets", len(fn) == 8 and len(ed) == 6 and len(cd) == 4,
    f"NEW_DETAILED_FUNCTIONS {len(fn)}/8 (max 8); NEW_INTERPROCEDURAL_EDGES {len(ed)}/6 (max 6); JOIN_CANDIDATES_DETAILED {len(cd)}/4 (max 4); ORACLE_MECHANISMS 1/1 (AttachChild); budget NOT exceeded")

# S10 ledger schema
chk("S10_ledger_schema", all(json.load(open(PKG + r"\03_SCRIPTS\ledger_build_results.json"))["schema_validation"][k]["pass"] for k in
    ["FUNCTION_BUDGET.csv", "EDGE_LEDGER.csv", "CANDIDATE_LEDGER.csv", "CLAIM_MATRIX.csv"]),
    "header/order/width/dup/null validated by build_ledgers.py validator")

# S11 no claim-context overclaims (string sweep of the package prose)
import re
overclaim_hits = []
for f_ in ["CLAIM_MATRIX.csv", "CANDIDATE_LEDGER.csv", "FINAL_REPORT_PLACEHOLDER"]:
    pass
sweep_targets = [PKG + "\\CLAIM_MATRIX.csv", PKG + "\\CANDIDATE_LEDGER.csv"]
for t in sweep_targets:
    try:
        txt = open(t, encoding="utf-8").read()
    except FileNotFoundError:
        continue
    for bad_token in ["INSTANCE_MODEL_NODE_JOIN=CONFIRMED", "CHILD_PROVENANCE_STATUS=CONFIRMED_MODEL_DERIVED",
                      "RUNTIME_JOIN_OBSERVED=YES", "TRANSFORM_TO_MODEL=CONFIRMED", "ATTACHCHILD_CONFIRMED"]:
        if bad_token in txt:
            overclaim_hits.append(f"{t}: {bad_token}")
chk("S11_no_overclaims_in_ledgers", len(overclaim_hits) == 0, f"overclaim token sweep: {overclaim_hits if overclaim_hits else 'CLEAN'}")

# S12 repo state: BASE unchanged, foreign untracked untouched, no staged changes
r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip()
r2 = subprocess.run(["git", "status", "--porcelain"], cwd=REPO, capture_output=True, text=True).stdout
tracked_modified = [l for l in r2.splitlines() if l and not l.startswith("??")]
untracked = sorted(set(l[3:].split("/")[0] for l in r2.splitlines() if l.startswith("??")))
chk("S12_repo_state", r == "24f45e0108b922c26ff584fee9ef7749de0390b6" and not tracked_modified,
    f"HEAD {r}; tracked modifications: {tracked_modified if tracked_modified else 'NONE'}; untracked roots: {untracked}")

# S13 the qualification gate results
q = json.load(open(PKG + r"\03_SCRIPTS\qualification_results.json"))
chk("S13_qualification_gate", q["OVERALL"] == "PASS" and q["gate_self_checks"]["baseline_passes"]
    and q["gate_self_checks"]["ctrl_a_fails_by_parent_predicate"] and q["gate_self_checks"]["ctrl_b_fails_by_child_predicate"]
    and q["gate_self_checks"]["ctrl_c_fails_by_parent_identity_predicate"] and q["gate_self_checks"]["real_candidate_fails"]
    and q["gate_self_checks"]["not_checker_always_fail"] and q["gate_self_checks"]["real_candidate_bytes_verified_against_exe"],
    "baseline PASS; CTRL-A/B/C each rejected by the proper predicate; real candidate FAIL; not checker-always-FAIL; real-chain bytes verified against the EXE")

# S14 A-D status algebra consistency (A,B,D unresolved/confirmed states vs the gate outcome)
cand4 = [c for c in cd if c["CANDIDATE_ID"] == "CAND-4-ACLD-PATH-SLOT41-ATTACH"][0]
consistent = ("UNRESOLVED" in cand4["CHILD_PROVENANCE"] and "UNRESOLVED" in cand4["CHILD_ROLE"]
              and "CONFIRMED_EXACT_SCENEFEEDER_PLUS_30" in cand4["PARENT_STATUS"]
              and cand4["JOIN_OPERATION_STATUS"].startswith("STRONGLY_SUPPORTED"))
chk("S14_status_algebra", consistent,
    "CAND-4: A=UNRESOLVED, B=CONFIRMED (scoped), C=STRONGLY_SUPPORTED, D=UNRESOLVED -> INSTANCE_MODEL_NODE_JOIN=NOT_ESTABLISHED (no averaging up)")

# overall
res["OVERALL"] = "QC_PASS" if all(c["ok"] for c in res["checks"].values()) else "QC_FAIL"
res["note"] = "SELF-CLASSIFICATION: this is the executor's own fresh-context internal QC (SELF_CHECK), NOT independent external Desktop post-audit and NOT PE-MASTER qualification."
for name, c in res["checks"].items():
    if not c["ok"]:
        res["findings"].append(f"FAILED CHECK: {name}: {c['detail']}")
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    json.dump(res, f, indent=2)
    f.write("\n")
print(json.dumps(res, indent=2))
