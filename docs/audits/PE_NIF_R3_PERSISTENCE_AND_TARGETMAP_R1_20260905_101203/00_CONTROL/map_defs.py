# -*- coding: utf-8 -*-
"""map_defs.py — data definitions for the PE_NIF_R3_PERSISTENCE_AND_TARGETMAP_R1
driver (build_package_r1.py). All old fragments are authored with LF line breaks;
the driver adapts to CRLF target files when counting. All new texts marked
'verbatim' are checked by the driver as whitespace-normalized substrings of the
hash-pinned R3 proposal file (PROPOSED_DOC_CORRECTIONS_R3.md, SHA256
84B3D05DB719AB09A6CEECE8300BBEE059655B5443F6B5CFC1090B4C8B7EC8E6) or, for the
P2/P3-FIXED texts, of this run's 06_REPORT/PROPOSALS_P2P3_FIXED.md.
"""
import os

RUN_ID = "PE_NIF_R3_PERSISTENCE_AND_TARGETMAP_R1_20260905_101203"
RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIF_R3_PERSISTENCE_AND_TARGETMAP_R1_20260905_101203"
R3_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627"
R2_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054"
DOCS_NIF = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\nif"

EXPECTED_PROMPT_SHA256 = "c9ccb5bb56fa8dd8f140f4c3126adc8aa9beddc4cb14d50fb9d0b7c0329276a2"
EXPECTED_PROPOSAL_SHA256 = "84b3d05db719ab09a6ceece8300bbee059655b5443f6b5cfc1090b4c8b7ec8e6"

# ---- target files -----------------------------------------------------------
DOC09 = os.path.join(DOCS_NIF, "09-semantics.md")
DOC10 = os.path.join(DOCS_NIF, "10-containers-corpus.md")
R2_REPORT = os.path.join(R2_ROOT, "06_REPORT", "00_FINAL_REPORT.md")
R2_GATES_PY = os.path.join(R2_ROOT, "00_CONTROL", "run_gates.py")
R2_TR_JSON = os.path.join(R2_ROOT, "02_LOGS", "TEST_RESULTS.json")
R2_GATES_CSV = os.path.join(R2_ROOT, "STAGE_ACCEPTANCE_GATES.csv")

# ---- old fragments (verbatim, LF-authored; newline-aware counting) ----------
F_POS_DELTAS = "[9 × f32 position deltas]"
F_K_RECORD = "with k per-record ∈ {2,3,4} —\n  byte-exact on 86.2% of real-record spans (ITER-34)"
F_ERA_CONCL = ("**Conclusion (CONFIRMED): the NIF extension formats are era-stable at the\n"
               "byte level — across a half-decade corpus gap every byte-exact grammar\n"
               "reproduces at 100% and the rare-family and importer pattern censuses are\n"
               "count-identical. The era drift is CONTENT (which directive/effect names\n"
               "and which records appear), never GRAMMAR.**")
F_R2_AREA_B = "Node hand-rolled CRC32/adler32/\nFNV-1a cross-checked against Python zlib"
F_THREE_INDEP = "three independent computations (Node, Python, R36 historical)"
F_PY_EQ_NODE = "Python == Node == R36 historical"
F_BOOL_COERCE = "'pass': bool(ok)"
F_TALLY_17_7 = "tally {CONFIRMED 17, REJECTED 7}"
F_R2_AREA_C = ("VERIFIED LOSSLESS by full-file byte reconstruction: the\n"
               "reassembly of all rows (decode + terminators, in order) equals the original file\n"
               "byte-for-byte — 12/12 SHA256 equality (R2G10, verified by BOTH the Node builder and\n"
               "the independent Python checker using the strict csv module).")

# ---- new texts (verbatim from the R3 proposal unless noted) -----------------
NEW_P1A = ("[9 × f32 trailing values; grouping and semantic role UNVERIFIED — the tested "
           "variable-k model consumes 9 × f32 after the weight list; grouping them into "
           "three triples (e.g. 3 morph states × XYZ) is an OPEN HYPOTHESIS, not an "
           "established structure; divisibility of nine does not establish the grouping.]")
NEW_P1B = ("[Scope limits that MUST travel with this wording: the parser takes the SMALLEST "
           "k in 1..8 whose weight prefix sums ≈1.0 (first-match; segmentation uniqueness "
           "NOT proven); byte-exact on 2,093/2,427 classifier-real spans (86.2%; the "
           "'real-record' class is a hypothesis-aligned classifier) and 3,186/6,167 all fit "
           "spans; **334 classifier-real spans do not fit the tested VARIABLE-K model — of "
           "those 334, 62 have another recorded fit among the recorded alternatives "
           "(g1/g2/mscan; e.g. 592572.nif bi=65 si=45 mscan_ok_m=[30]) and 272 have none "
           "among the recorded alternatives; alternative-model fits are recorded fits, NOT "
           "true segmentation and NOT semantic confirmation**; observed k ∈ {1,2,3,4} on "
           "9.3.5 exact examples and k ∈ {1..5} on 2003.]")
NEW_P3B = ("corrected primitives == R2 Python (zlib/exact-int) == R36 historical "
           "(zlib/exact-int); the R2 Node leg computed different functions whose zero-match "
           "aggregates coincidentally agreed")
NEW_P4A = ("Human-review gate state MUST be serialized three-state: PASS / FAIL / PENDING "
           "(R2's `'pass': bool(ok)` turned pending into false/FAIL — R2 HR-1..4 were "
           "PENDING, not FAIL; reproduced as a negative control with exit code 1).")
NEW_P4B = ("Gate tally labels MUST be derived from the actual emitted rows at emit time "
           "(R2G13's \"{CONFIRMED 17, REJECTED 7}\" label vs the actual 16/8 rows).")
NEW_P4C = ("OVERALL EXECUTABLE PASS must always be presented as distinct from human "
           "acceptance (explicit human_acceptance field: PENDING_HUMAN_REVIEW).")
NEW_P5A = ("The accepted 12/12 byte-lossless sidecars (R2 Area C) are PRESERVED; no "
           "manifest migration is requested or authorized.")
NEW_P5B = ("Where semantic header normalization is restated, the policy line is explicit: "
           "semantic mapping follows the CUSTOM PHYSICAL-LINE CONTRACT (a bare CR inside "
           "a physical row is DATA; the R2 builder csvParse semantics). Under standard CSV "
           "record semantics exactly one row (R39 row 10) parses differently (computed_by "
           "\"n/a\\r\" vs \"n/a\") — an INTERPRETIVE difference, NOT raw-byte loss; both "
           "layers reconstruct the original bytes exactly (R3G14: 12/12 SHA-equal "
           "reconstruction + 0 field-mapping errors under the custom contract, R39 row 10 "
           "included).")

# unchanged heads of the FIXED P3 texts (verbatim-in-proposal check boundaries)
P3FIX1_HEAD = ("the candidate census was recomputed with stage-local primitives validated "
               "by known-answer tests and per-entry oracle identity (R3); the R2 Node "
               "adler32 and fnv1a helpers are CONFIRMED defective (value mismatches on "
               "11,022/11,022 name inputs, 11,022/11,022 payload inputs, and 11,016/11,022 "
               "name inputs respectively); the R2 crc32 helper and the size/offset "
               "candidates were correct;")
P3FIX3_HEAD = ("Standing rule (the P0): hash-primitive VALUE IDENTITY (known-answer tests "
               "+ per-entry oracle agreement) must be established BEFORE aggregate "
               "acceptance, because")

# forbidden clauses (must NOT appear in the fixed texts)
P2_REMOVED_CLAUSE = "every BYTE-EXACT VALIDATOR reproduced at 100"
P3_REMOVED_CLAUSE = "zero-match is insensitive to value errors"
P3_REMOVED_CLAUSE2 = "provably insensitive to value errors"

# ---- evidence pointers ------------------------------------------------------
EV_R34 = "R3 01_RAW/R34_RESUM.json (independent re-sum; gate R3G12); claim R3C-10"
EV_R35 = "R3 01_RAW/R35_CLAIM_TABLE_PRESERVED.json (21-claim verbatim transcription; gate R3G13); claim R3C-11"
EV_PRIM = "R3 01_RAW/PRIMITIVE_VALUE_COMPARISON.json (r2_vs_corrected complete mismatch census); claims R3C-01..R3C-09"
EV_WVC = "R3 02_LOGS/kat_wrong_value_controls.json (wrong-value controls; gates R3G7a/R3G7b); P0 demonstration"
EV_R3G11 = "R3 gate R3G11 (corrected == R2 Python == R36 historical, 20/20); claim R3C-08"
EV_R2STATE = "R3 01_RAW/R2_STATE_RESUM.json (HR-1..4 pass=false/CSV=FAIL; actual tally 16/8 vs stale 17/7); claims R3C-12/R3C-13"
EV_SIDECAR = "R3 01_RAW/SIDECAR_BARE_CR_ANALYSIS.json (R3G14: 12/12 SHA-equal + 0 field-mapping errors, R39 row 10); claim R3C-14"

# ---- the P1..P5 target map --------------------------------------------------
# Each edit: old_fragment (verbatim file substring, LF-authored), operation,
# new_text, new_text_source, evidence_pointer. Operations:
#   REPLACE            — future docs/nif application edit (NOT this run)
#   LEDGER-ENTRY       — historical file preserved byte-identical; the entry
#                        records the superseded wording; no edit ever
#   STANDING-RULE      — new standing text, no superseded file wording
#   STANDING-POLICY    — acceptance/policy guard; anchor fragment verifies the
#                        historical wording the policy references
MAP_PROPOSALS = [
    {
        "proposal_id": "P1R2-5-R3",
        "area": "F2 morph-residual wording",
        "claims": ["R3C-10"],
        "supersedes": ("R2 P1R2-5 (S-11) / R1 P1-5 — neither predecessor was applied; "
                       "the standing docs/nif wording predates R1"),
        "target_file": "docs/nif/09-semantics.md",
        "target_file_abs": DOC09,
        "edits": [
            {
                "edit_id": "P1R2-5-R3/a",
                "old_fragment": F_POS_DELTAS,
                "operation": "REPLACE",
                "new_text": NEW_P1A,
                "new_text_source": ("PROPOSED_DOC_CORRECTIONS_R3.md P1R2-5-R3 NEW, segment 1 of 2 "
                                    "(trailing-values wording; bracket split documented); join-checked "
                                    "against the full proposal NEW"),
                "evidence_pointer": EV_R34 + "; PROPOSED_DOC_CORRECTIONS_R3.md ## P1R2-5-R3",
                "lineage_ref": "R1 P1-5 first OLD/NEW pair",
            },
            {
                "edit_id": "P1R2-5-R3/b",
                "old_fragment": F_K_RECORD,
                "operation": "REPLACE",
                "new_text": NEW_P1B,
                "new_text_source": ("PROPOSED_DOC_CORRECTIONS_R3.md P1R2-5-R3 NEW, segment 2 of 2 "
                                    "(k-record + scope limits incl. the 334/62/272 residual "
                                    "decomposition); join-checked against the full proposal NEW"),
                "evidence_pointer": EV_R34 + "; PROPOSED_DOC_CORRECTIONS_R3.md ## P1R2-5-R3",
                "lineage_ref": "R1 P1-5 second OLD/NEW pair",
            },
        ],
    },
    {
        "proposal_id": "P2R2-2-R3-FIXED",
        "area": "21-claim summary wording (with this run's P2 fix applied)",
        "claims": ["R3C-11"],
        "supersedes": ("R3 P2R2-2-R3 NEW text as corrected by 06_REPORT/PROPOSALS_P2P3_FIXED.md "
                       "(this run); R2 P2R2-2 (S-12) / R1 P2-2 — neither predecessor was applied"),
        "target_file": "docs/nif/10-containers-corpus.md",
        "target_file_abs": DOC10,
        "edits": [
            {
                "edit_id": "P2R2-2-R3-FIXED/main",
                "old_fragment": F_ERA_CONCL,
                "operation": "REPLACE",
                "new_text": "@EXTRACT:P2R2-2-R3-FIXED",
                "new_text_source": ("06_REPORT/PROPOSALS_P2P3_FIXED.md (this run) EXTRACT:P2R2-2-R3-FIXED "
                                     "— the categorical 'every BYTE-EXACT VALIDATOR ... 100%' clause "
                                     "REMOVED and scoped to the measured claim population per the "
                                     "follow-up review (C-MORPH-1 partial fit; changed-payload morph "
                                     "family presence 3 files / 29 occurrences ASCII-only)"),
                "evidence_pointer": EV_R35 + "; 06_REPORT/PROPOSALS_P2P3_FIXED.md ## P2R2-2-R3-FIXED",
                "lineage_ref": "R1 P2-2 target (lines 121-125)",
            },
        ],
    },
    {
        "proposal_id": "P3R3",
        "area": "PRIM correction-ledger entries (R2 hash-primitive method provenance)",
        "claims": ["R3C-01", "R3C-02", "R3C-03", "R3C-04", "R3C-05", "R3C-06", "R3C-07", "R3C-08", "R3C-09"],
        "supersedes": "R2 method-provenance wordings S-03..S-08",
        "target_file": "historical R2 artifacts (NOT edited; ledger entries)",
        "target_file_abs": None,
        "edits": [
            {
                "edit_id": "P3R3/a",
                "old_fragment": F_R2_AREA_B,
                "target_file_override": "R2 06_REPORT/00_FINAL_REPORT.md",
                "target_file_abs_override": R2_REPORT,
                "operation": "LEDGER-ENTRY",
                "new_text": "@EXTRACT:P3R3-FIXED-1",
                "new_text_source": ("06_REPORT/PROPOSALS_P2P3_FIXED.md (this run) EXTRACT:P3R3-FIXED-1 — "
                                     "R3 P3R3 entry 1 with the evidence-bounded insensitivity statement "
                                     "(P3 fix); unchanged head verified verbatim against the proposal"),
                "evidence_pointer": EV_PRIM + "; " + EV_WVC,
                "lineage_ref": "R3 proposal P3R3 first bullet (R2 report Area B sentence)",
            },
            {
                "edit_id": "P3R3/b1",
                "old_fragment": F_THREE_INDEP,
                "target_file_override": "R2 00_CONTROL/run_gates.py",
                "target_file_abs_override": R2_GATES_PY,
                "operation": "LEDGER-ENTRY",
                "new_text": NEW_P3B,
                "new_text_source": "PROPOSED_DOC_CORRECTIONS_R3.md P3R3 second bullet (verbatim)",
                "evidence_pointer": EV_R3G11,
                "lineage_ref": "R2G8 independence wording (S-04)",
            },
            {
                "edit_id": "P3R3/b2",
                "old_fragment": F_THREE_INDEP,
                "target_file_override": "R2 02_LOGS/TEST_RESULTS.json",
                "target_file_abs_override": R2_TR_JSON,
                "operation": "LEDGER-ENTRY",
                "new_text": NEW_P3B,
                "new_text_source": "PROPOSED_DOC_CORRECTIONS_R3.md P3R3 second bullet (verbatim)",
                "evidence_pointer": EV_R3G11,
                "lineage_ref": "R2G8 independence wording (S-04)",
            },
            {
                "edit_id": "P3R3/b3",
                "old_fragment": F_THREE_INDEP,
                "target_file_override": "R2 STAGE_ACCEPTANCE_GATES.csv",
                "target_file_abs_override": R2_GATES_CSV,
                "operation": "LEDGER-ENTRY",
                "new_text": NEW_P3B,
                "new_text_source": "PROPOSED_DOC_CORRECTIONS_R3.md P3R3 second bullet (verbatim)",
                "evidence_pointer": EV_R3G11,
                "lineage_ref": "R2G8 independence wording (S-04)",
            },
            {
                "edit_id": "P3R3/b4",
                "old_fragment": F_PY_EQ_NODE,
                "target_file_override": "R2 STAGE_ACCEPTANCE_GATES.csv",
                "target_file_abs_override": R2_GATES_CSV,
                "operation": "LEDGER-ENTRY",
                "new_text": NEW_P3B,
                "new_text_source": "PROPOSED_DOC_CORRECTIONS_R3.md P3R3 second bullet (verbatim)",
                "evidence_pointer": EV_R3G11,
                "lineage_ref": "R2G8 gate label phrase (S-04)",
            },
            {
                "edit_id": "P3R3/c",
                "old_fragment": None,
                "target_file_override": None,
                "target_file_abs_override": None,
                "operation": "STANDING-RULE",
                "new_text": "@EXTRACT:P3R3-FIXED-3",
                "new_text_source": ("06_REPORT/PROPOSALS_P2P3_FIXED.md (this run) EXTRACT:P3R3-FIXED-3 — "
                                     "R3 P3R3 standing rule (the P0) with the evidence-bounded "
                                     "insensitivity statement (P3 fix); unchanged head verified "
                                     "verbatim against the proposal"),
                "evidence_pointer": EV_WVC,
                "lineage_ref": "R3 proposal P3R3 standing rule",
            },
        ],
    },
    {
        "proposal_id": "P4R3",
        "area": "F3 three-state gate policy",
        "claims": ["R3C-12", "R3C-13"],
        "supersedes": "R2 gate serialization/label wordings S-09/S-10",
        "target_file": "historical R2 artifacts (NOT edited; ledger entries + standing rules)",
        "target_file_abs": None,
        "edits": [
            {
                "edit_id": "P4R3/a",
                "old_fragment": F_BOOL_COERCE,
                "target_file_override": "R2 00_CONTROL/run_gates.py",
                "target_file_abs_override": R2_GATES_PY,
                "operation": "LEDGER-ENTRY",
                "new_text": NEW_P4A,
                "new_text_source": "PROPOSED_DOC_CORRECTIONS_R3.md P4R3 first bullet (verbatim)",
                "evidence_pointer": EV_R2STATE,
                "lineage_ref": "R2 run_gates.py L50 bool coercion (S-09)",
            },
            {
                "edit_id": "P4R3/b1",
                "old_fragment": F_TALLY_17_7,
                "target_file_override": "R2 00_CONTROL/run_gates.py",
                "target_file_abs_override": R2_GATES_PY,
                "operation": "LEDGER-ENTRY",
                "new_text": NEW_P4B,
                "new_text_source": "PROPOSED_DOC_CORRECTIONS_R3.md P4R3 second bullet (verbatim)",
                "evidence_pointer": EV_R2STATE,
                "lineage_ref": "R2G13 stale tally label (S-10)",
            },
            {
                "edit_id": "P4R3/b2",
                "old_fragment": F_TALLY_17_7,
                "target_file_override": "R2 02_LOGS/TEST_RESULTS.json",
                "target_file_abs_override": R2_TR_JSON,
                "operation": "LEDGER-ENTRY",
                "new_text": NEW_P4B,
                "new_text_source": "PROPOSED_DOC_CORRECTIONS_R3.md P4R3 second bullet (verbatim)",
                "evidence_pointer": EV_R2STATE,
                "lineage_ref": "R2G13 stale tally label (S-10)",
            },
            {
                "edit_id": "P4R3/b3",
                "old_fragment": F_TALLY_17_7,
                "target_file_override": "R2 STAGE_ACCEPTANCE_GATES.csv",
                "target_file_abs_override": R2_GATES_CSV,
                "operation": "LEDGER-ENTRY",
                "new_text": NEW_P4B,
                "new_text_source": "PROPOSED_DOC_CORRECTIONS_R3.md P4R3 second bullet (verbatim)",
                "evidence_pointer": EV_R2STATE,
                "lineage_ref": "R2G13 stale tally label (S-10)",
            },
            {
                "edit_id": "P4R3/c",
                "old_fragment": None,
                "target_file_override": None,
                "target_file_abs_override": None,
                "operation": "STANDING-RULE",
                "new_text": NEW_P4C,
                "new_text_source": "PROPOSED_DOC_CORRECTIONS_R3.md P4R3 third bullet (verbatim)",
                "evidence_pointer": EV_R2STATE,
                "lineage_ref": "R3 proposal P4R3 third bullet",
            },
        ],
    },
    {
        "proposal_id": "P5R3",
        "area": "F5 sidecar bare-CR policy",
        "claims": ["R3C-14"],
        "supersedes": "none (documents the R2 Area C acceptance; no migration authorized)",
        "target_file": "historical R2 artifacts (NOT edited; standing policy)",
        "target_file_abs": None,
        "edits": [
            {
                "edit_id": "P5R3/a",
                "old_fragment": F_R2_AREA_C,
                "target_file_override": "R2 06_REPORT/00_FINAL_REPORT.md",
                "target_file_abs_override": R2_REPORT,
                "operation": "STANDING-POLICY",
                "new_text": NEW_P5A,
                "new_text_source": "PROPOSED_DOC_CORRECTIONS_R3.md P5R3 first bullet (verbatim)",
                "evidence_pointer": EV_SIDECAR,
                "lineage_ref": "R2 Area C acceptance anchor (12/12 lossless; R2G10)",
            },
            {
                "edit_id": "P5R3/b",
                "old_fragment": None,
                "target_file_override": None,
                "target_file_abs_override": None,
                "operation": "STANDING-POLICY",
                "new_text": NEW_P5B,
                "new_text_source": ("PROPOSED_DOC_CORRECTIONS_R3.md P5R3 second bullet (verbatim); "
                                     "no current restatement exists in docs/nif (absence-checked by "
                                     "the census)"),
                "evidence_pointer": EV_SIDECAR,
                "lineage_ref": "R3 proposal P5R3 second bullet (future-restatement guard)",
            },
        ],
    },
]

# ---- census pattern definitions ----------------------------------------------
# category: FLAGGED (review-flagged contradictory phrasing), ADJACENT-INTERACTION
# (interacts with R3 proposal targets), ADJACENT-HEDGED (already-hedged variant),
# ABSENCE (R3-superseded wording expected ABSENT from docs/nif),
# OUT-OF-SCOPE (R1/R2-pending proposal targets — NOT R3-superseded; recorded for
# completeness only)
CENSUS_PATTERNS = [
    ("A_position_deltas", "position deltas", "FLAGGED",
     "target-quantity asserted as position — R3 P1R2-5-R3: semantic role UNVERIFIED"),
    ("B_delta_triples", "delta triples", "FLAGGED",
     "grouping asserted as structural triples — R3 P1R2-5-R3: grouping is an OPEN HYPOTHESIS"),
    ("C_true_structure", "true structure", "FLAGGED",
     "morph structure asserted as 'true' — R3 P1R2-5-R3: NOT true segmentation"),
    ("D_every_byte_exact_grammar", "every byte-exact grammar", "FLAGGED",
     "cross-era 100% generalization — R3 P2R2-2-R3-FIXED scopes per-claim"),
    ("D_era_stable_at_byte_level", "era-stable at the byte level", "FLAGGED",
     "cross-era 100% generalization opener (same sentence)"),
    ("D_all_grammars_opener", "All grammars confirmed", "FLAGGED",
     "cross-era generalization opener of the R35 validation section"),
    ("D_revalidated_byte_exact", "re-validated byte-exact on the 2003 corpus", "FLAGGED",
     "the 'All grammars ... re-validated byte-exact' clause (same sentence)"),
    ("B_adjacent_9float_triple_grouping", "9-float triple grouping", "ADJACENT-HEDGED",
     "already hedged with '(3 morph states × XYZ?)' — open question mark retained"),
    ("E_fit_no_single_grammar", "fit no single grammar", "ADJACENT-INTERACTION",
     "ITER-21 residual census; interacts with the R3 P1R2-5-R3 334/62/272 wording (different populations)"),
    ("E_325_heterogeneous", "325 heterogeneous spans", "ADJACENT-INTERACTION",
     "ITER-21 residual count; not contradicted by R3 (different denominator/scope) but coexists with the 334 wording after application"),
    ("E_325_spans", "325 spans", "ADJACENT-INTERACTION",
     "ITER-21 residual count (08-ark residual paragraph)"),
    ("ABSENCE_hand_rolled", "hand-rolled", "ABSENCE",
     "R3-superseded R2 method-provenance wording — expected ABSENT from docs/nif"),
    ("ABSENCE_cross_checked_zlib", "cross-checked against Python zlib", "ABSENCE",
     "R3-superseded R2 method-provenance wording — expected ABSENT from docs/nif"),
    ("ABSENCE_three_independent", "three independent computations", "ABSENCE",
     "R3-superseded R2G8 wording — expected ABSENT from docs/nif"),
    ("ABSENCE_stale_tally", "CONFIRMED 17, REJECTED 7", "ABSENCE",
     "R3-superseded R2G13 stale tally label — expected ABSENT from docs/nif"),
    ("OOS_biconditional", "⟺", "OUT-OF-SCOPE",
     "d==c biconditional — R1 P1-6/P2-1/P3-1 and R2 P1R2-6/P2R2-1/P3R2-1 PENDING proposals (not R3-superseded)"),
    ("OOS_complete_wording", "This is the complete, evidence-based", "OUT-OF-SCOPE",
     "README 'complete' wording — R1 P4-3/R2 P4R2-3 PENDING proposal (not R3-superseded)"),
]

# review-cited lines to verify at their CURRENT positions
REVIEW_CITATIONS = [
    {"file": "09-semantics.md", "claimed_line": 180, "pattern": "position deltas",
     "citation_for": "position deltas"},
    {"file": "08-ark-proprietary.md", "claimed_line": 196, "pattern": "true structure",
     "citation_for": "true structure / delta triples (line-span start)"},
    {"file": "10-containers-corpus.md", "claimed_line": 121, "pattern": "era-stable at the byte level",
     "citation_for": "cross-era 100% generalization (conclusion block start)"},
]
