"""qc_ind_finalize.py — INDEPENDENT internal QC, part 3 (finalize), for
PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007.

Author: pe-master-auditor. Assembles the FINAL machine record QC_IND_RESULTS.json
from the part-1/part-2 result files + the manual adjudication results of this QC
(science-preservation token sweep, lineage mechanical checks, standing-status
presence, executor-file integrity after the QC's own executions). Read-only over
the package; writes only under 00_CONTROL_INTERNAL_QC/.
"""
import hashlib
import json
import os

REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
PKG = os.path.join(REPO, "docs", "audits", "PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007")
QC_DIR = os.path.join(PKG, "00_CONTROL_INTERNAL_QC")

p1 = json.load(open(os.path.join(QC_DIR, "QC_IND_PART1_RESULTS.json"), encoding="utf-8"))
p2 = json.load(open(os.path.join(QC_DIR, "QC_IND_PART2_RESULTS.json"), encoding="utf-8"))

# --- executor-file integrity AFTER this QC's executions (nothing rewritten)
manifest = {}
for ln in open(os.path.join(PKG, "MANIFEST_SHA256.csv"), encoding="utf-8"):
    ln = ln.strip()
    if ln.startswith("docs/"):
        p, s, h = ln.rsplit(",", 2)
        manifest[p] = (int(s), h)
integrity = []
for p, (s, h) in manifest.items():
    data = open(os.path.join(REPO, p.replace("/", "\\")), "rb").read()
    if len(data) != s or hashlib.sha256(data).hexdigest() != h:
        integrity.append(p)
assert not integrity, f"executor files modified by the QC: {integrity}"

# --- this QC's own file census + hashes
qc_files = {}
for fn in sorted(os.listdir(QC_DIR)):
    data = open(os.path.join(QC_DIR, fn), "rb").read()
    qc_files[fn] = {"size": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                    "utf8_nobom_lf": not data.startswith(b"\xef\xbb\xbf") and b"\r" not in data}
bad_enc = [k for k, v in qc_files.items() if not v["utf8_nobom_lf"]]

out = {
    "QC_RUN_ID": "PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_INTERNAL_QC_R1_20261007",
    "QC_ORIGIN": ("INDEPENDENT internal QC by pe-master-auditor (a FRESH session, NOT the executor; "
                  "the executor's own QC is the honestly-labeled SELF-REVIEW in QC_REPORT.md). "
                  "Under PE-MASTER direct dispatch; RECORDS/QC-MACHINERY ONLY — zero EXE access, "
                  "zero new RE; replicas on published byte buffers and synthetic in-memory copies only."),
    "AUDITED_PACKAGE": "docs/audits/PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007/ (19 executor files)",
    "BASE_SHA": "790e83735b439e2d76a250868a47a599c2c10184 (HEAD unchanged; package untracked; no commit/push by this QC)",
    "part1_records_identity_results": p1["I_results"],
    "part2_controls_results": p2["C_results"],
    "mandatory_matrix_mine_vs_executor_vs_old": p2["mandatory_matrix"],
    "adversarial_mutant_matrix": p2["adversarial_mutant_matrix"],
    "ctrl3_matrix": p2["ctrl3_matrix"],
    "manual_adjudication_results": {
        "science_preservation_token_sweep": {
            "method": ("my own enumeration of forbidden/promotable tokens over all package record files "
                       "(excluding this QC dir), with per-occurrence CONTEXT ADJUDICATION by this QC"),
            "occurrences": 16,
            "adjudication": ("ALL 16 occurrences are in legitimate negation / superseded / policy / "
                             "quotation contexts (CORRECTED_LINEAGE_STATUS S-7 quote; FINAL_REPORT "
                             "'No SCIENCE_PASS is issued anywhere'; GOVERNANCE 'no tool of this run "
                             "issues a SCIENCE_PASS'; HANDOFF supersession row; QC_REPORT's own "
                             "forbidden-token enumeration; SUPERSESSION S-7 declaration + citations). "
                             "ZERO active promotions."),
        },
        "lineage_record_mechanical_checks": {
            "WRAPPER_DEPTH = UNRESOLVED": True,
            "MODEL_ROOT_RELATION = UNKNOWN": True,
            "POINTER_LINEAGE_TRANSITIONS_OBSERVED = 2 (description, not census)": True,
            "H-2 RELATION_TYPE = UNRESOLVED": True,
            "NEW_WRAPPER_HOPS = 2 preserved (charged units)": True,
            "MAX_NEW_WRAPPER_HOPS = 3 unchanged": True,
            "no 2-wrapper-layers claim": True,
            "unresolved H-2 still consumes the budget": True,
            "H-3/H-4 SAME_OBJECT not lineage transitions": True,
        },
        "standing_status_presence": {
            "MODEL_ROOT_RELATION = UNKNOWN": "6 package files",
            "CHILD_VISUAL_ROLE = UNRESOLVED": "4 package files",
            "CHILD_TO_JOIN_IDENTITY = STRONGLY_SUPPORTED (NOT CONFIRMED)": "5 package files",
            "CAND4_CHILD_ROOT_CLOSURE = NOT_ESTABLISHED_WITHIN_BOUND": "5 package files",
            "CHILD_RESOURCE_PROVENANCE = STRONGLY_SUPPORTED_MODEL_DERIVED (ceiling)": "2 package files",
            "EXACT_PARENT = CONFIRMED_EXACT_SCENEFEEDER_PLUS_30 (carried, scoped)": "4 package files",
            "promotions_found": 0,
        },
        "stricter_reading_observation": (
            "MY OWN stricter reading of the literal rule would potentially COUNT NEIGH-04 ('new(0x68)' "
            "argument-flow) and NEIGH-15 ('receiver [esp+0x40]') — and possibly further candidate rows — "
            "which would RAISE the floor above 32. This cannot change any disposition (the budget FAIL "
            "vs MAX 8 stands either way; EXACT = UNRESOLVED already carries it); the correction's "
            "conservative 32-floor follows the authoritative Desktop post-audit exactly."),
        "bonus_observation_old_checker_head": (
            "MY adversarial mutant A1b (alternative head encoding 89 C7 = mov edi,eax) revealed an "
            "ADDITIONAL weakness of the OLD checker: the old head check (mnemonic 'mov' + 'edi, eax' in "
            "op_str) accepted the non-canonical encoding; the rebuilt checker's exact-byte requirement "
            "(8B F8) closes this class too. Old logic PASSED A1b; the rebuilt checker FAILs it (P1)."),
    },
    "findings": {
        "F-IND-1_P3_supersession_S4_quote_file_attribution": (
            "SUPERSESSION.md S-4 'Where' cites \"FINAL_REPORT.md §4 ('no analysis is hidden behind RAW "
            "labels')\" — the quoted phrase does NOT exist in FINAL_REPORT.md; it exists in "
            "CLAIM_MATRIX.csv CL-14 (evidence cell). The superseded CLAIM is real in three loci "
            "(EDGE_ACCOUNTING_LEDGER.csv header line 8; PE_MASTER_REVIEW.md line 23; CLAIM_MATRIX.csv "
            "CL-14), so supersession S-4 stands; only the middle citation's file attribution is wrong. "
            "Correction: re-attribute to CLAIM_MATRIX.csv CL-14 (or quote FINAL_REPORT §4's actual "
            "wording 'every uncounted row carries an explicit reason — the J2 discipline'). Secondary "
            "trivial imprecision in the same file: S-3's QC-I10 quote 'exceeded by exactly 16' vs the "
            "source's 'EXCEEDED by exactly 16'; several S-quotes span the source's ~78-col hard line "
            "wraps / drop backticks (S-1 ledger header; S-6 FINAL_REPORT §3; S-7 FINAL_REPORT §1) — "
            "substance identical in every case. Revalidation: grep the corrected citation strings in "
            "the named source files."),
        "F-IND-2_P3_executor_qc_independence_wording": (
            "QC_REPORT.md §1 (and FINAL_REPORT §3 / HANDOFF equivalently) claims the fresh QC's "
            "re-derivation did not trust LEDGER_CLASS — but qc_correction.py check C2 uses "
            "LEDGER_CLASS as the branch selector for the 24 E-rows and hard-derives 'not counted' for "
            "every other row (the RP rows' interpretation text is never content-derivation-checked), so "
            "the 'content-based re-derivation' is partially class-gated and its C4 agreement with the "
            "corrected ledger is structurally guaranteed for the non-E/non-marker rows. MATERIALITY LOW: "
            "the 24 E-rows' content IS verified non-empty, the 8 mandatory rows' content IS verified, "
            "and THIS QC's genuinely independent per-row content adjudication (I6) confirms the full "
            "32/11/17/9 classification. Correction: reword the QC_REPORT §1 self-description to state "
            "the C2 derivation's actual structure. Revalidation: the sentence cites the C2 code path "
            "accurately."),
    },
    "verdict_inputs": {
        "part1_checks_passed": sum(1 for v in p1["I_results"].values() if v["ok"]),
        "part1_checks_total": len(p1["I_results"]),
        "part2_checks_passed": sum(1 for v in p2["C_results"].values() if v["ok"]),
        "part2_checks_total": len(p2["C_results"]),
        "findings_P1_P2": 0,
        "findings_P3": 2,
        "executor_files_modified_by_qc": integrity,
        "qc_files_encoding_ok": not bad_enc,
    },
    "QC_VERDICT": "QC_PASS_WITH_FINDINGS",
    "verdict_statement": (
        "The correction package PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007 is verified "
        "by THIS independent QC: the 69-row re-adjudication (32 counted = 24 historical + RV-01..07 + "
        "NEIGH-09, exactly the Desktop-proven defensive floor) is confirmed by my own row-by-row "
        "content adjudication with ZERO differences; the verbatim round-trip is byte-exact; the body "
        "accounting (>= 7 with the verified-at-source FUN_006C0EE0 probe) is correct; the rebuilt "
        "CTRL_4 exact-endpoint predicate passes the mandatory 4-case matrix AND all 9 of MY adversarial "
        "mutants (zero false PASS; fail-closed on undecodable forms; exact-address and exact-byte-form "
        "enforced); CTRL_3 rebuilt is synthetic/prior-pin only with zero EXE access; the supersessions "
        "S-1..S-9 are grounded in real source loci (with the S-4 citation imprecision = F-IND-1); "
        "science standings are preserved without a single active promotion; SOURCE_PACKAGE is "
        "immutably preserved (38/38 BASE blobs); the historical budget FAILs stand; "
        "CORRECTION_RECORDS_QC and ORIGINAL_SCOPE_COMPLIANCE = FAIL stay separated. Two P3 findings "
        "(S-4 quote file attribution; executor-QC independence wording) — both records-precision class, "
        "neither overturns a disposition. C4-C1/C4-C2 corrections: VERIFIED as records; closure of the "
        "correction itself belongs to PE-MASTER + the persistence phase + the future independent "
        "Desktop post-audit of the new SHA."),
    "qc_files": qc_files,
}

path = os.path.join(QC_DIR, "QC_IND_RESULTS.json")
with open(path, "w", encoding="utf-8", newline="\n") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(json.dumps(out["verdict_inputs"], indent=2))
print("QC_VERDICT:", out["QC_VERDICT"])
print("wrote", path)
