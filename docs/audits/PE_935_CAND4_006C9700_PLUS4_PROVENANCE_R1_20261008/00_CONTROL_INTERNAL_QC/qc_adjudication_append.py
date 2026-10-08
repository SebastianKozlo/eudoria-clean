# -*- coding: utf-8 -*-
"""qc_adjudication_append.py — appends the QC worker's analytical adjudication
layers (claim matrix re-adjudication, ledger content re-adjudication, ceilings,
budget consumption, coverage, findings, verdict) to QC_RESULTS.json produced by
qc_independent_check.py. The measured values were produced by
qc_independent_check.py (own PE mapping + own reads); this script adds the
QC-worker adjudication derived from the full package read (all 22 files,
read to EOF) plus those measurements.

python -B; writes ONLY QC_RESULTS.json in this directory.
"""
import json
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "QC_RESULTS.json")

with open(OUT, "r", encoding="utf-8") as f:
    res = json.load(f)

# ---------------------------------------------------------------------------
# CLAIM MATRIX re-adjudication (CL-1..CL-22) — content, not just shape.
# Evidence statuses per the project vocabulary; each verdict cites the QC's
# independent measurement where one exists.
# ---------------------------------------------------------------------------
claims = [
    ("CL-1", "ACCEPT", "Byte-verified by QC (own pins: pair stores @0x006C973A/0x006C9742; push order in the pump hex); request pair {0x66, A} CONFIRMED."),
    ("CL-2", "ACCEPT", "Own pins 8B C8 @0x006C974B-adjacent call bytes (E8 BE A4 15 00) + 85 F6/74 4D; S==NULL gates the NULL returns. CONFIRMED."),
    ("CL-3", "ACCEPT", "Own pins: pre-clear C7 06 @0x006C95A0; receiver 8B 49 10; flag cmp/jne @0x006C95AE/BE (CAND-4 path, arg4=0); E8 7A E3 0E 00 @0x006C9631; slot store 89 3E @0x006C9651; addref 01 5F 04 @0x006C9657. CONFIRMED."),
    ("CL-4", "ACCEPT", "Own pins: 6A 10 @0x006C97B9; E8 04 3C 29 00 @0x006C97BB; 51/56/8B C8; E8 93 F7 01 00 @0x006C97D8 (own rel32 -> 0x006E8F70). CONFIRMED."),
    ("CL-5", "ACCEPT", "Own pins: 89 06; 89 46 04; 01 48 04; C7 07 00..; C7 46 0C 00..; 8B C6 @0x006E9014. The ctor stores and return-this CONFIRMED byte-level."),
    ("CL-6", "ACCEPT", "Return-path table re-derived from the pump bytes (5 paths; all branch targets own-recomputed, 15/15 rel8 match); PATH_B is the only R-producing path on the recorded CAND-4 conditions; static path correctly NOT named an observed execution."),
    ("CL-7", "ACCEPT", "QC own no-vptr scan of the ctor window (byte-identical to physical EXE): the ONLY R-base stores are 89 06 ([R+0]=S), 89 46 04 ([R+4]=P), and TWO zero immediates (C7 07 00 00 00 00 -> R+8; C7 46 0C 00 00 00 00 -> R+0xC). No vtable immediate exists; R's class name is not RTTI-derivable in bound. The negative is CONFIRMED by construction-dataflow enumeration."),
    ("CL-8", "ACCEPT", "The +4 writer pin 89 46 04 @0x006E8FA5 and addref 01 48 04 @0x006E8FAF byte-verified by QC; first-init classification supported by CL-10's bounded negative."),
    ("CL-9", "ACCEPT", "Source CONFIRMED to the getter-return boundary (slot store + getter call pins byte-verified); deeper origin honestly PARTIAL/NOT_ESTABLISHED_WITHIN_BOUND (body #4 window cut 0x007B7A0F; edge budget 12/12 — QC confirms no 13th unit exists)."),
    ("CL-10", "ACCEPT", "QC re-enumerated every [x+4]-destination write in the four opened bodies from the raw hex (byte-compared to the EXE): PW-1 (R+4) + refcount ops with base P/old (01 48 04; 01 5F 04; 83 40 04 FF x2; 83 41 04 FF). No other [R+4] writer; correctly labeled NOT_ENCOUNTERED_WITHIN_BOUND, explicitly not a global census."),
    ("CL-11", "ACCEPT", "Refcount protocol byte-forms verified (ADD 01 48 04/01 5F 04; DEC 83 40 04 FF; destroy via vtable slot 1 = [vtable+4]); class identity NOT claimed. CONFIRMED as protocol facts."),
    ("CL-12", "ACCEPT", "Own pins: 8B 4E 04/8B 11/8B 42 44 (P -> vtable slot 17), 68 A4 5D A8 00 (own string read 'Geowater:0'), FF D0. Callee body NOT opened; no role-name claim. CONFIRMED at the call-site level."),
    ("CL-13", "ACCEPT", "T==P alias adjudicated across the two RECORDED callers + this run's measured store (same base R, same offset +4; installer load 8B 78 04 @0x006C67BE byte-verified), explicitly NOT one observed execution; R != T (handle vs contained object). The alias is dataflow-based, not assumed. ACCEPTED as CONFIRMED alias-of-roles."),
    ("CL-14", "ACCEPT", "0x10 vs 0xC allocation sizes byte-verified (6A 10 @0x006C97B9 vs 6A 0C @0x006CB819); different construction sites/callers; CAND-4 path creates no W; no class(R)==class(W) claim either way."),
    ("CL-15", "ACCEPT", "RESOLVED_AS_POINTER for the CAND-4 chain by measured same-base dataflow ([R+4] stores an object pointer with refcount at [P+4]); W's count@+4 map confined to W's base. The conditional premise was resolved by measurement, not assumed (CTRL_D discipline)."),
    ("CL-16", "ACCEPT", "Prior-canon family linkage correctly cited as PRIOR (not re-derived); marked CONSISTENT, not promoted."),
    ("CL-17", "ACCEPT", "Callee identity of 0x0095D3C4 cited at ITS prior-canon sites only; the run's new fact is the 0x10 size at ITS OWN site (byte-verified). Correctly a re-pin, not a new adjudication."),
    ("CL-18", "ACCEPT", "BB 01 00 00 00 @0x006C67C9 byte-verified = MOV ebx,1 (not an INC opcode); ADD idiom (01 5F 04 / 01 48 04) byte-verified at all cited sites."),
    ("CL-19", "ACCEPT", "Standing-science list compared word-for-word against contract §7: all 13 statuses preserved verbatim in CLAIM_MATRIX/FINAL_REPORT §14/HANDOFF/SOURCE_STATE §5; no promotion by analogy."),
    ("CL-20", "ACCEPT", "The H-2/[instance+4] resolution is reported as THIS run's measured result ([R+4] = P, a contained refcounted object pointer) with explicit ceiling discipline; the prior UNRESOLVED concern is exactly this run's question, so reporting the measured store is legal under the contract's preserve-until-exact-claim rule; no automatic top-level promotion claimed."),
    ("CL-21", "ACCEPT", "P/T class identity UNKNOWN within bound (P's vtable is runtime data; construction site unopened) — honest."),
    ("CL-22", "ACCEPT", "Transform owner / coordinate frame NOT_ADJUDICATED_BY_THIS_RUN; no visual/world/channel/XYZ promotion anywhere in the package (QC full-read confirms)."),
]
res["claim_matrix_readjudication"] = [
    {"claim_id": c, "qc_disposition": d, "qc_rationale": r} for (c, d, r) in claims
]

# ---------------------------------------------------------------------------
# SCOPE LEDGER content re-adjudication (row content, not only sums).
# ---------------------------------------------------------------------------
res["ledger_readjudication"] = {
    "bodies": {
        "declared": "4/6 used (B-1 RESOLVED, B-2 RESOLVED, B-3 RESOLVED, B-4 PARTIAL)",
        "qc_check": "QC byte-compared all four body windows against the physical EXE (byte-identical); "
                    "extent proofs verified by own pins (ret C3 @0x006C981B; ret 8 @0x006E9027; "
                    "ret 8 x2 @0x006C962E/@0x006C966C; B-4 cut at 0x007B7A0F). RAW_WINDOW_OVERFLOW "
                    "neighbors disclosed and NOT interpreted anywhere in the package (QC full-read). "
                    "Re-open ranges rule: no second charge; no un-charged body interpretation found.",
        "verdict": "HONEST",
    },
    "edges": {
        "declared": "12 counted (E1..E12) + 9 RAW_VISIBLE_ONLY (R-1..R-9)",
        "qc_check": "QC enumerated every call instruction in the four opened extents from the "
                    "byte-verified body hex: pump 8 callsites (E1..E8), ctor 5 (E9, E10, R-1..R-3), "
                    "setter 5 (E11, E12, R-4..R-6), P-getter head 3 (R-7..R-9) = 12 charged + 9 RAW "
                    "= COMPLETE; no 13th interpreted unit exists; each RAW row's NOT_COUNTED_REASON "
                    "is genuine (no interpretation hidden behind a RAW label; R-3's receiver fact is "
                    "declared body-dataflow, not a callee claim; R-7/R-8 explicitly refuse to transfer "
                    "the operator-new identity from prior canon to this site). E12 is honestly "
                    "charged for the off-CAND-4 variant interpretation. STOP_BEFORE_EXCEED at the "
                    "FUN_007B79B0 boundary is real: the continuation was NOT decoded and no claim is "
                    "made past 0x007B7A0F. Prior-scope re-pins (0x006C6FFC, 0x006C7049, 0x006CB7CF, "
                    "0x006CB81B, 0x006CB836) are byte re-reads of prior records without new "
                    "callsite interpretation — correctly not charged.",
        "verdict": "HONEST (12/12 AT limit, never exceeded; complete enumeration)",
    },
    "writers": {
        "declared": "2/4 (PW-1, PW-2; PW-3 = the honest boundary row, NOT a writer)",
        "qc_check": "PW-1 (89 46 04 @0x006E8FA5) and PW-2 (89 3E @0x006C9651 + pre-clear) byte-verified; "
                    "PW-3 correctly classified as NOT an assignment site and NOT_ESTABLISHED_WITHIN_BOUND; "
                    "later-overwrite negative matches the QC's own [x+4]-write enumeration of the opened bodies.",
        "verdict": "HONEST",
    },
    "hops": {
        "declared": "3/3 (HP-1 R->P WRAPPER_CONTAINS; HP-2 S->P source leg; HP-3 T==P SAME_OBJECT alias)",
        "qc_check": "Each hop cites its physical instructions (byte-verified); prior-canon manager stores "
                    "are explicitly NOT charged as this run's hops; HP-3 is an adjudication of the two "
                    "recorded flows (store: this run; load: prior record re-pinned) — a legitimate "
                    "interpreted transition between roles; no 4th hop exists in the package.",
        "verdict": "HONEST (AT limit, not exceeded)",
    },
    "prohibited_scope": {
        "qc_check": "FUN_006C8BB0 / FUN_007B6C30 / FUN_007BF900 / FUN_007BF630 / FUN_007BF470 / join "
                    "implementation: no decode record, no pin, no claim anywhere in the package (QC "
                    "full-read of all 22 files); no runtime evidence; no transform/XYZ/visual-role "
                    "search; no decoder hardening.",
        "verdict": "COMPLIANT",
    },
}

# ---------------------------------------------------------------------------
# STATUS CEILINGS verification.
# ---------------------------------------------------------------------------
res["ceilings_verification"] = {
    "deeper_origin_of_P": "NOT_ESTABLISHED_WITHIN_BOUND — verified (PW-3, body #4 PARTIAL, R-7..R-9 RAW, no claim past 0x007B7A0F)",
    "S_O_identity": "NOT_ADJUDICATED — verified (FUN_00415670/FUN_00823C10 bodies unopened; FINAL_REPORT §10.2)",
    "R_class_name": "UNKNOWN — verified by the QC's own no-vptr-store enumeration of the ctor body (all R-base stores: 2 argument pointers + 2 zero immediates; no vtable immediate)",
    "P_T_class_names": "UNKNOWN — verified (CL-21; P's vtable is runtime data)",
    "release_on_destroy": "NOT_CHECKED — verified (the 0x006C9820 neighbor is RAW display only; role not adjudicated)",
    "T_downstream": "NOT_ADJUDICATED — verified (no downstream trace performed; FINAL_REPORT §6)",
    "transform_owner_coordinate_frame": "NOT_ADJUDICATED_BY_THIS_RUN — verified (CL-22, FINAL_REPORT §15)",
    "standing_science": "PRESERVED VERBATIM — all 13 contract §7 statuses compared word-for-word across CLAIM_MATRIX CL-19 / FINAL_REPORT §14 / HANDOFF / SOURCE_STATE §5; no promotion performed",
    "real_science_auto_qualification": "DISABLED — respected (no status auto-promotion anywhere; publication is not acceptance)",
}

# ---------------------------------------------------------------------------
# QC budget consumption (contract §4 shared-ledger rules).
# ---------------------------------------------------------------------------
res["budget_consumption_qc"] = {
    "new_body_units": 0, "note_bodies": "4/6 used by the run; QC opened NO new body range; "
                       "all QC reads are pins/re-pins of already-charged bodies (free repetition)",
    "new_edge_units": 0, "note_edges": "12/12 at limit; QC performed NO new callsite interpretation "
                      "(all rel32/rel8 recomputations are repetitions of already-charged or RAW "
                      "arithmetic units — free)",
    "new_writer_units": 0, "note_writers": "2/4 used; QC identified no new writer (and did not hunt one)",
    "new_hop_units": 0, "note_hops": "3/3 at limit; NO new hop interpretations by QC (prohibited by the dispatch)",
    "within_shares": True,
}

# ---------------------------------------------------------------------------
# Coverage / FULL READ LOG / NOT_CHECKED.
# ---------------------------------------------------------------------------
res["coverage_full_read_log"] = {
    "files_read_in_full_by_qc": [
        "Contract OPENCODE_FUN006C9700_PLUS4_MICRORUN_R2.md (336 lines; SIZE 17487 / SHA256 verified at QC start)",
        "00_CONTROL_INTERNAL_QC/QC_PHASE_INPUTS.md (59 lines)",
        "PREREGISTRATION.md (177 lines)",
        "INPUT_IDENTITIES.md (175 lines)",
        "SOURCE_STATE.md (167 lines)",
        "01_RAW/FUN_006C9700_PUMP_FULL.txt (149 lines)",
        "01_RAW/FUN_006E8F70_CTOR_R.txt (85 lines)",
        "01_RAW/FUN_006C9570_SLOT_SETTER.txt (89 lines)",
        "01_RAW/FUN_007B79B0_P_GETTER_PARTIAL.txt (70 lines)",
        "01_RAW/MANUAL_ENCODING_CROSSCHECK.txt (91 lines)",
        "01_RAW/PINS_AND_REL32.txt (146 lines)",
        "01_RAW/RTTI_AND_STRINGS.txt (62 lines)",
        "RETURN_VALUE_TRACE.csv (19 lines)",
        "PLUS4_PROVENANCE.csv (20 lines)",
        "POINTER_LINEAGE.csv (16 lines)",
        "FUNCTION_BODY_ACCOUNTING.csv (26 lines)",
        "EDGE_ACCOUNTING_LEDGER.csv (38 lines)",
        "CLAIM_MATRIX.csv (28 lines)",
        "CONTROL_RESULTS.json (114 lines)",
        "03_SCRIPTS/checker_plus4.py (297 lines)",
        "03_SCRIPTS/run_controls.py (364 lines)",
        "FINAL_REPORT.md (274 lines)",
        "HANDOFF.md (163 lines)",
    ],
    "read_mode": "FULL_READ (all 22 package files to EOF) + QC own measurements (26 anchor pins, "
                 "19 rel32, 15 rel8, 4 body windows, 3 RTTI chains, 4 strings, section table)",
    "not_checked_by_qc": [
        "The two pinned external reports (NC2_NC3_DESKTOP_REPORT / ENGINE_RESEARCH_REPORT) — QC relied "
        "on the executor's recorded identity measurements of these administrative inputs; their "
        "internal content was not re-read by the QC worker (not load-bearing for the byte-level "
        "results audited here; identities were re-verified only via the executor's preflight record)",
        "The five historical source packages' 263 files — QC did not re-hash all 263 (out of QC budget "
        "discipline); spot re-pins of the load-bearing prior-canon bytes (installer/producer/historical "
        "caller pins, 8 anchor pins + 5 rel32) were independently re-measured from the physical EXE and MATCH",
        "git ls-remote live remote — QC verified LOCAL_HEAD == origin/master == EXPECTED_BASE_SHA "
        "(both 97823c6...); the live remote was NOT re-queried by the QC worker (no publication action "
        "in this phase; the executor's transient-failure disclosure was reviewed and is plausible)",
    ],
    "independence_lineages": {
        "bytes": "QC's own PE32 mapping (raw-vs-virtual split) + own fail-closed EXE identity + own "
                 "reads of the physical EXE; expected values taken from the raw claims in the package "
                 "and the QC task list, then compared byte-for-byte",
        "decoder": "QC used NO disassembler; instruction identities verified by own opcode/modrm "
                   "encoding arithmetic (the executor's capstone decode was checked against the "
                   "physical bytes, not against another decode)",
        "dataflow": "QC re-derived the return-path/branch-target algebra from the physical bytes "
                    "(15/15 rel8, 19/19 rel32 own recomputes); claim adjudication is the QC worker's "
                    "own (fresh context; not the executor, not a prior reviewer)",
        "scope_adjudication": "QC enumerated every callsite of the four opened bodies from the "
                              "byte-verified hex (12+9 complete census) and re-adjudicated every "
                              "ledger row's content, not just the sums",
    },
}

# ---------------------------------------------------------------------------
# Findings (severity per the PE-MASTER finding vocabulary).
# ---------------------------------------------------------------------------
res["findings"] = [
    {
        "id": "F-1", "severity": "P3", "title": "Notational residue in PINS_AND_REL32.txt prior-scope row (hist_caller_null_check)",
        "source": "01_RAW/PINS_AND_REL32.txt line 90: 'hist_caller_null_check @0x006CB811: 8B F0? — record cites \"TEST ESI,ESI\" (85 F6) @0x006CB811'",
        "counter_measurement": "QC own read @0x006CB811 = 85 F6 (TEST ESI,ESI) — the prior record's cited bytes are CORRECT; the '8B F0?' fragment in the pin row is a leftover working artifact, not a measurement",
        "effect": "None on any load-bearing claim (the row's cited prior-record bytes match the physical EXE); reader confusion only",
        "correction": "In a future run's package (this package is read-only for the QC), drop the '8B F0?' fragment; keep '85 F6 @0x006CB811'",
        "revalidation": "Byte read @0x006CB811 == 85 F6 (already performed by this QC)",
    },
    {
        "id": "F-2", "severity": "P2", "title": "checker OwnPE.va_to_off lacks the raw-vs-virtual boundary: .data zero-init-tail VAs map onto .tls/.rsrc file bytes",
        "source": "03_SCRIPTS/checker_plus4.py OwnPE.va_to_off: 'if va_s <= rva < va_s + max(vsize, rsize)' with no rsize boundary; CONTROL_RESULTS.json MC6 labels VA 0x00BA1100 an 'unpinned .rsrc byte'",
        "counter_measurement": "QC own section table: .data RVA 0x76C000, vsize 0x3D6E4 (end 0x7A9CE4), raw size 0x34000 (raw end RVA 0x7A0000); VA 0x00BA1100 (RVA 0x7A1100) lies in the .data VIRTUAL tail — QCPE classifies it VIRTUAL_BSS (no file bytes); the executor's mapping resolves it to file offset 0x7A1100, which is .rsrc raw (ROFF 0x7A1000 + 0x100)",
        "effect": "For THIS run: no pin is affected (all 80 gate checks operate on raw-backed VAs; clean 80/80 re-verified by QC). MC6's stated VA is mislabeled as '.rsrc' — the corruption lands on a .rsrc byte only via the mapping defect; the specificity conclusion still holds (QC re-ran MC6 with DIRECT file offsets 0x7A1100/0x7A1200: anchor gates PASS). Residual risk: a future read of any .data-tail VA (runtime-initialized globals, e.g. 0x00BA73BC) could silently read .rsrc bytes instead of failing/returning zero — the RTTI_AND_STRINGS description of 0x00BA73BC was written correctly by hand, but the checker would not enforce it",
        "correction": "In the NEXT run's checker generation (not this package — read-only for QC): bound va_to_off by raw size (rva < va_s + rsize -> RAW; else VIRTUAL_BSS/unmapped), and re-label MC6's corruption as a direct file-offset corruption of an unpinned .rsrc byte (which is what it effectively is)",
        "revalidation": "A future checker with the boundary must (a) return None/VIRTUAL for 0x00BA73BC and 0x00BA1100; (b) still pass 80/80 clean; (c) still detect MC1..MC5 corruptions",
    },
    {
        "id": "F-3", "severity": "P3", "title": "Notational arithmetic residue in the PINS prior-scope rel32 note for the CAND-4 callsite",
        "source": "01_RAW/PINS_AND_REL32.txt line 111: '0x006C6FFC -> 0x006C9700 (the CAND-4 pump callsite, -0x2701+... = 0x26FF rel32)'",
        "counter_measurement": "QC own read @0x006C6FFC = E8 FF 26 00 00; own rel32 = +0x26FF; 0x006C7001 + 0x26FF = 0x006C9700 (target MATCH; the SOURCE_STATE.md and pump-context records correctly say 'E8 FF 26 00 00'). The '-0x2701' fragment is an incorrect/misleading arithmetic residue — -0x2701 would target 0x006C6900, not 0x006C9700",
        "effect": "None on any gate (the checker recomputes rel32 from the physical bytes and passes); reader confusion only",
        "correction": "Future package: write the rel32 as '+0x26FF' and delete the '-0x2701+...' fragment",
        "revalidation": "QC own rel32 recompute (recorded in QC_RESULTS.rel32_recompute, id prior_cand4_caller_pump) — already performed",
    },
]
res["findings_note"] = ("No finding contradicts a load-bearing claim, an anchor pin, a ledger row's "
                        "honesty, a control result or a status ceiling. F-2 is a tooling-precision "
                        "defect with zero effect on this run's 80 gate checks (all pins are "
                        "raw-backed VAs) — it is disclosed for the next checker generation and for "
                        "the parent's adjudication.")

# ---------------------------------------------------------------------------
# Verdict.
# ---------------------------------------------------------------------------
res["qc_verdict"] = {
    "verdict": "QC_PASS",
    "scope": "return/source identity, used bytes, status ceilings, and the CONTENT of the whole scope ledger "
             "(contract §6 fresh-context internal QC mandate)",
    "basis": [
        "26/26 anchor pins independently re-measured from the physical EXE with the QC's own PE mapping — zero mismatches",
        "19/19 rel32 and 15/15 rel8 independently recomputed by the QC's own arithmetic — zero mismatches",
        "All four opened body windows byte-identical to the physical EXE (byte-for-byte hex compare)",
        "Own no-vptr enumeration confirms CL-7 (R has no vptr store; all R-base stores enumerated)",
        "RTTI W chain independently re-walked (W = .?AVArkModelResourceInstanceRef@@ — correctly NOT used for R)",
        "Clean production gate independently re-run: 80/80 PASS",
        "MC1 (+4 writer) and MC4 (ctor rel32) re-verified with the QC's OWN corruption bytes (different from the executor's) on in-memory copies — the same production gate detects each at the exact anchor; MC6 specificity re-verified with direct file-offset corruptions of two unpinned .rsrc bytes + the executor's exact VA replay (all anchor gates stay PASS); physical EXE unchanged after all controls (SHA256 re-measured)",
        "Claim matrix CL-1..CL-22 re-adjudicated row by row — every claim within its evidence class; no classic error class found (no R+4/T+4 base confusion — the alias is proven, not assumed; no class-by-name; no static-possibility-as-observed; no refcount-vs-INC mislabel; no oracle promoted to PCG status)",
        "Ledger content re-adjudicated: bodies 4/6, edges 12+9 (complete callsite census of the opened extents; no hidden interpretation; no 13th unit), writers 2/4, hops 3/3 — honest; STOP_BEFORE_EXCEED at FUN_007B79B0 verified real",
        "All status ceilings hold; standing science preserved verbatim; REAL_SCIENCE_AUTO_QUALIFICATION=DISABLED respected",
        "QC budget consumption: 0 new units of any class (all QC work is free repetition of already-charged units)",
    ],
    "open_findings": ["F-1 (P3, notation)", "F-2 (P2, checker mapping boundary — zero effect on this run's gates; disclosed for the next checker generation)", "F-3 (P3, notation)"],
    "not_a": "QC_PASS is an internal-QC result, NOT MASTER_ACCEPTED and NOT milestone closure; publication remains the parent's phase; this QC did NOT perform a Desktop post-audit (NEW_DESKTOP_POST_AUDIT = NOT_PERFORMED); the QC is internal to PE-MASTER (not independent of PE-MASTER)",
}

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    json.dump(res, f, indent=2, ensure_ascii=False)

print("adjudication layers appended:", list(res.keys()))
print("verdict:", res["qc_verdict"]["verdict"])
