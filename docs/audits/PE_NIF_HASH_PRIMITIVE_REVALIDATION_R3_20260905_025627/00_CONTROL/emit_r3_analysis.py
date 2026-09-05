"""emit_r3_analysis.py — generates 05_ANALYSIS CSVs for R3 with real hashes and
verbatim-quote verification (each supersession quote is asserted present in the
pinned R2 artifact at emit time, mirroring the R2G15 discipline).

Deterministic; nonzero exit on any failure. Writes ONLY inside this run dir.
"""
from __future__ import annotations

import csv
import hashlib
import re
import sys
from pathlib import Path

RUN = Path(r'D:\Eudoria_Reconstruction\99_Audits\PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627')
R2 = Path(r'D:\Eudoria_Reconstruction\99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054')
ANA = RUN / '05_ANALYSIS'


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


H = {
    'comparison': sha(RUN / '01_RAW/PRIMITIVE_VALUE_COMPARISON.json'),
    'census': sha(RUN / '01_RAW/CENSUS_RECOUNT_R3.json'),
    'probe': sha(RUN / '01_RAW/R2_HELPER_PROBE.json'),
    'r34': sha(RUN / '01_RAW/R34_RESUM.json'),
    'r35': sha(RUN / '01_RAW/R35_CLAIM_TABLE_PRESERVED.json'),
    'r2state': sha(RUN / '01_RAW/R2_STATE_RESUM.json'),
    'sidecar': sha(RUN / '01_RAW/SIDECAR_BARE_CR_ANALYSIS.json'),
    'tests': sha(RUN / '02_LOGS/TEST_RESULTS.json'),
    'kat_r2py': sha(RUN / '02_LOGS/kat_r2_literal_python.json'),
    'kat_wrong': sha(RUN / '02_LOGS/kat_wrong_value_controls.json'),
    'kat_ts_neg': sha(RUN / '02_LOGS/kat_three_state_r2_coercion.json'),
    'primitives': sha(RUN / '00_CONTROL/r3_primitives.py'),
    'probe_cjs': sha(RUN / '00_CONTROL/probe_r2_helpers.cjs'),
    'r2_control': sha(R2 / '00_CONTROL/control_r2.cjs'),
    'r2_recounts': sha(R2 / '01_RAW/RECOUNTS.json'),
    'r2_tests': sha(R2 / '02_LOGS/TEST_RESULTS.json'),
    'r2_matrix': sha(R2 / '05_ANALYSIS/CLAIM_MATRIX.csv'),
    'r2_report': sha(R2 / '06_REPORT/00_FINAL_REPORT.md'),
    'r2_handoff': sha(R2 / 'HANDOFF.md'),
    'r2_proposals': sha(R2 / '06_REPORT/PROPOSED_DOC_CORRECTIONS_R2.md'),
    'r2_gates_csv': sha(R2 / 'STAGE_ACCEPTANCE_GATES.csv'),
}

# ---------------------------------------------------------------- claim matrix
CLAIMS = [
    ('R3C-01', 'PRIM', 'supersedes the R2 method-provenance claims (C2-B-01 method wording)',
     'The two R2 Node helpers do not implement their named algorithms. Measured from the literal '
     'declarations extracted from the hash-pinned R2 source and EXECUTED as pure functions: '
     'adler32("")=0x00010000 (correct 0x00000001); adler32("a")=0x00620061 (correct 0x00620062); '
     'adler32("hello")=0x06280214 (correct 0x062c0215); fnv1a("hello")=0xa82fb4a1 (correct '
     '0x4f9f2cab); fnv1a("548296.nif")=0x200d96de (correct 0x4e2b6736)',
     '02_LOGS/TEST_RESULTS.json gate R3G6b; 01_RAW/R2_HELPER_PROBE.json (executed KAT values)',
     H['tests'], 'both Models.bnt corpora + KAT vectors', '5 counterexamples + 5 reference values',
     'STAGE_LOCAL_REPRODUCTION (extracted-pure-declaration execution; historical script NOT executed)',
     'expected values from zlib + exact-int/BigInt + published RFC vectors, all independent of the R2 code',
     'if the executed literals had produced the correct values, the prompt counterexamples would be falsified (gate would fail)',
     'CONFIRMED', 'ACCEPTED (defect reproduced from actual bytes, not auditor assertion)',
     'The R2 helper values differ from the named algorithms on these counterexamples.',
     'none — the defect is directly measured'),
    ('R3C-02', 'PRIM', 'none (root cause)',
     'Root cause: R2 adler32 swaps the RFC1950 roles/initials (byte-sum accumulator starts at 0, '
     'accumulated-sum starts at 1; RFC1950 requires s1=1, s2=0); R2 fnv1a multiplies in float64 '
     'before >>>0 — products above 2^53 round before the 32-bit reduction. The exact-int Python '
     'transcription of the SAME fnv formula produces the CORRECT values, isolating the defect to '
     'the float64 arithmetic',
     '03_STATIC/SOURCE_QUOTES.md (R2 control_r2.cjs L37-38, hash-pinned); 02_LOGS/kat_r2_literal_python.json',
     H['r2_control'], 'R2 source bytes', '2 helper declarations',
     'SOURCE_INSPECTION + STAGE_LOCAL_REPRODUCTION (transcription characterization)',
     'the transcription uses exact integers; it matches the RFC while the float execution does not',
     'an algorithm-shape defect (adler) and an arithmetic defect (fnv) are distinguished',
     'CONFIRMED', 'ACCEPTED (mechanism identified)',
     'Adler: roles/initials misassigned. FNV: float64 multiply is insufficient; exact multiply mod 2^32 is required.',
     'none'),
    ('R3C-03', 'PRIM', 'bounds the R2 defect census',
     'The R2 crc32 helper is NOT defective: the executed literal equals zlib.crc32 on all 14 KAT '
     'vectors and on every entry of all five crc32 candidate input classes (11022/11022 each: '
     'name, name+0x0A, name+u32size_le, u32size_le+name, payload). The defect census is bounded to '
     'adler32 + fnv1a',
     '01_RAW/PRIMITIVE_VALUE_COMPARISON.json r2_vs_corrected (0 mismatches on all crc32 candidates)',
     H['comparison'], 'both corpora', '11,022 entries x 5 crc32 input classes',
     'STAGE_LOCAL_REPRODUCTION + PHYSICAL_RECOMPUTATION (zlib oracle)',
     'the same executed-literal method that reproduced the adler/fnv defects shows crc32 clean',
     'any crc32 value mismatch would have widened the defect census (gate R3G6c/identity fail)',
     'CONFIRMED', 'ACCEPTED (positive control)',
     'R2 crc32 and the size/offset candidates were computed correctly; only adler32 and fnv1a are defective.',
     'none'),
    ('R3C-04', 'PRIM', 'none (corrected primitives)',
     'Corrected stage-local primitives pass the executable KAT suite BEFORE corpus aggregation: '
     '14 vectors (empty, single byte, multi-byte, binary with zero/high bytes, overflow-sensitive, '
     'repeated, incremental), streaming carry-in identity for adler/fnv/crc, and oracle '
     'self-validation against published constants (zlib.adler32("Wikipedia")=0x11E60398, '
     'zlib.crc32("123456789")=0xCBF43926, FNV vectors 0x811C9DC5/0xE40C292C/0xBF9CF968/0x4F9F2CAB)',
     '02_LOGS/kat_corrected.json; 02_LOGS/kat_oracle_self_vectors.json (exit 0 each)',
     H['tests'], 'n/a', '14 vectors + 4 incremental checks + 8 oracle checks',
     'EXECUTABLE (subprocess exit codes recorded)',
     'own implementation vs C oracle vs published constants — three independent sources',
     'any vector mismatch aborts the run before aggregation (nonzero exit, enforced)',
     'CONFIRMED', 'ACCEPTED',
     'RFC1950 Adler (s1=1, s2=0, mod 65521) and RFC9923 FNV-1a (exact multiply mod 2^32) as specified.',
     'none'),
    ('R3C-05', 'PRIM', 'none (identity pass)',
     'Per-entry primitive/input identity: corrected Python == zlib == corrected Node for '
     'adler32(name) and adler32(payload) on every one of 11,022 entries (plus numpy closed-form '
     'and an iterative-spec sample of 6,335 entries / 247.0 MB); fnv1a(name) exact-int == Node '
     'BigInt 11022/11022; all five crc32 input classes 11022/11022',
     '01_RAW/PRIMITIVE_VALUE_COMPARISON.json identity_pass; gate R3G9',
     H['comparison'], 'both corpora', '11,022 entries x 8 candidate input classes',
     'PHYSICAL_RECOMPUTATION',
     'four independent implementations per defect-affected class (zlib C, numpy closed form, Node Number/BigInt, own table/iterative)',
     'any single-entry mismatch fails the gate and blocks match-count derivation',
     'CONFIRMED', 'ACCEPTED',
     'Value identity holds per entry before any aggregate is derived.',
     'none'),
    ('R3C-06', 'PRIM', 'extends the external post-audit measurement',
     'Complete R2-vs-corrected per-entry mismatch census: adler32(name) 11022/11022 mismatches; '
     'adler32(payload) 11022/11022 mismatches (FIRST complete per-payload census — the post-audit '
     'explicitly did not claim one); fnv1a(name) 11016/11022 mismatches with exactly 6 coincidences '
     '(508629.nif, 186733.nif, 147508.nif — same three names in both eras; float64 rounding landed '
     'on the exact value); all crc32 candidates 0 mismatches',
     '01_RAW/PRIMITIVE_VALUE_COMPARISON.json r2_vs_corrected (complete mismatch census keyed by era+file)',
     H['comparison'], 'both corpora', '11,022 entries x 8 candidate input classes',
     'PHYSICAL_RECOMPUTATION',
     'R2 values from the executed literals; corrected values from oracle-validated primitives',
     'aggregate-only comparison would conceal these mismatches (the P0 mechanism)',
     'CONFIRMED', 'ACCEPTED',
     'The erroneous functions differ in VALUE on every defect-affected input except the 6 named FNV coincidences.',
     'none'),
    ('R3C-07', 'AGG', 'supersedes R2G8 method assurance; retains the physical result',
     'The corrected ten-candidate census reproduces the physical result UNCHANGED: nine exact-zero '
     'candidates on both corpora; d==crc32(payload)=3,435/5,596 and 3,299/5,426; c==CRC32(payload) '
     '11,022/11,022 with 0 directory mismatches; agreement with the R2 aggregates AND the R36 '
     'historical FIELD_D_TESTS.json on 20/20 candidate-era pairs',
     '01_RAW/CENSUS_RECOUNT_R3.json; gate R3G11',
     H['census'], 'both corpora', '10 candidates x 2 corpora',
     'PHYSICAL_RECOMPUTATION',
     'three sources compared (R3 corrected, R2 aggregates, R36 historical); the R2 Python and R36 legs were already correct (zlib/exact-int)',
     'any count change vs the historical aggregates would indicate value-level sensitivity (would be investigated, not accepted)',
     'CONFIRMED', 'ACCEPTED (physical result retained; method assurance superseded)',
     'Nine zero-match candidates + CRC subset reconfirmed with CORRECT primitives.',
     'none'),
    ('R3C-08', 'SUP', 'supersedes R2G8 wording + R2 report L100-110 + HANDOFF key-result 2',
     'REJECTED as previously worded: "Node hand-rolled CRC32/adler32/FNV-1a cross-checked against '
     'Python zlib" and "three independent computations (Node, Python, R36 historical)". The R2 '
     'Node leg computed different functions whose zero-match AGGREGATES coincidentally agreed; '
     'aggregate agreement does not prove implementation identity. The physical counts remain '
     'CONFIRMED via the corrected recount (R3C-07); the independent Python (zlib/exact-int) and '
     'R36 historical legs were correct all along',
     '03_STATIC/SOURCE_QUOTES.md; 05_ANALYSIS/SUPERSESSION_MAP.csv rows S-03..S-08',
     H['r2_report'], 'R2 artifacts (hash-pinned)', '3 method-assurance statements',
     'SOURCE_INSPECTION + value-level evidence (R3C-06)',
     'the value census disproves implementation identity while the aggregate equality stands',
     '20/20 aggregate agreement held while 11022+11022+11016 value mismatches existed underneath',
     'REJECTED (as worded)', 'ACCEPTED (superseded; history not rewritten)',
     'Corrected wording: agreement of corrected primitives with R2 Python and R36 historical; the R2 Node values are recorded as a defect.',
     'none'),
    ('R3C-09', 'P0', 'none (gate-requirement proof)',
     'Aggregate zero-match preservation demonstrated: deliberately wrong-value primitives '
     '(adler32 XOR 0x5A5A5A5A; fnv1a with offset basis 0x811C9DC6) FAIL every value-identity KAT '
     'predicate (actual exit code 1) yet preserve the zero-match census on BOTH full corpora '
     '(0 d-matches for all three wrong candidates in both eras). Aggregate-only acceptance cannot '
     'detect value errors; value-identity gates (KAT + per-entry oracle agreement) are REQUIRED '
     'before aggregate acceptance (this is P0)',
     '02_LOGS/kat_wrong_value_controls.json (exit 1); 01_RAW/PRIMITIVE_VALUE_COMPARISON.json '
     'aggregate_zero_match_preservation_of_wrong_value_controls; gates R3G7a/R3G7b',
     H['comparison'], 'both corpora', '11,022 entries x 3 wrong candidates x 2 eras + 14 KAT vectors',
     'EXECUTABLE (subprocess exit codes) + PHYSICAL_RECOMPUTATION',
     'the same wrong primitives fail the KATs and keep the aggregates — the insensitivity is measured, not asserted',
     'an aggregate-only gate would have passed the wrong-value implementations',
     'CONFIRMED', 'ACCEPTED (P0 demonstrated)',
     'Hash-primitive VALUE IDENTITY must be established BEFORE aggregate acceptance.',
     'none'),
    ('R3C-10', 'F2', 'supersedes R2 P1R2-5 wording',
     'R34 per-span re-sum: 334 is the VARIABLE-K residual among the 2,427 classifier-real spans '
     '(2,093 fit = 86.2%), NOT "fit no tested grammar": of the 334, 62 have another recorded fit '
     '(g1_ok/g2_ok/mscan_ok_m) and 272 have none among the recorded alternatives. Concrete '
     'counterexamples: 592572.nif (bi=65, si=45, mscan_ok_m=[30]); 579739.nif (bi=109, si=138, '
     'mscan_ok_m=[4]); 574751.nif (bi=80, si=4, g2_ok=1, mscan_ok_m=[11]). All-span fit 3,186/6,167 '
     'preserved. Alternative-model fits are NOT promoted to true segmentation',
     '01_RAW/R34_RESUM.json (independent re-filter of the hash-pinned per_span raw records); gate R3G12',
     H['r34'], 'R34 2003-side per-span records', '6,167 per-span records',
     'HISTORICAL_RESUM (NOT a new physical grammar execution)',
     'raw rows re-filtered with the exact R34 classifier condition; prose not trusted',
     'the R2 wording is contradicted by 62 recorded alternative fits (counterexample listed)',
     'CONFIRMED', 'ACCEPTED (F2 confirmed; wording corrected as P1R2-5-R3 proposal)',
     '334 classifier-real spans do not fit the tested VARIABLE-K model; 62 of them have another recorded fit.',
     'none'),
    ('R3C-11', 'F2', 'supersedes R2 P2R2-2 summary reading',
     'The 21 R35 grammar claims are NOT all 100% fits: 19 ERA-STABLE + 2 EVOLVED (C-G3B-3 '
     'failure-profile delta; C-SHAD-2 vocabulary delta). C-MORPH-1 is a PARTIAL-FIT claim '
     '(rr 2,093/2,427 = 86.2% on 9.3.5; 1,180/1,457 = 81.0% on 2003). "Every byte-exact grammar '
     'reproduced at 100%" is valid only for the byte-exact validator populations, not as a summary '
     'of all 21 claims. Exact claim IDs, denominators and evidence statuses retained',
     '01_RAW/R35_CLAIM_TABLE_PRESERVED.json (verbatim transcription, hash recorded); gate R3G13',
     H['r35'], 'R35 claim table', '21 claims',
     'HISTORICAL_TRANSCRIPTION (source inspection)',
     'transcribed from the R35 REPORT.md table; the overstatement is corrected, nothing promoted',
     'presenting all 21 claims as 100% fits would contradict the C-MORPH-1 row and the 2 EVOLVED verdicts',
     'CONFIRMED', 'ACCEPTED (wording corrected as P2R2-2-R3 proposal)',
     '19 ERA-STABLE / 2 EVOLVED with per-claim denominators; C-MORPH-1 partial fit stated explicitly.',
     'none'),
    ('R3C-12', 'F3', 'supersedes R2 run_gates.py serialization',
     'Three-state preservation: PENDING is distinct from FAIL and PASS through the gate function '
     '(three_state), TEST_RESULTS.json (HR gates carry pass=null, state=PENDING), the gates CSV '
     'and the report. R2\'s bool(None)->false/FAIL serialization is reproduced and DETECTED as a '
     'negative control (actual exit code 1; failed predicate "serialize(None) == \'PENDING\'" with '
     'actual "FAIL"). OVERALL EXECUTABLE PASS is explicitly NOT human acceptance',
     '02_LOGS/kat_three_state_r2_coercion.json (exit 1); 02_LOGS/kat_three_state_corrected.json (exit 0); '
     '01_RAW/R2_STATE_RESUM.json (R2 HR-1..4 pass=false / CSV FAIL as inspected)',
     H['r2state'], 'R2 artifacts + R3 gate machinery', '3 predicates x 2 serializers',
     'STAGE_LOCAL_REPRODUCTION + EXECUTABLE',
     'the corrected predicates are applied to the historical coercion; actual outputs captured',
     'R2 serialized 4 PENDING human-review gates as false/FAIL (no human had reviewed them)',
     'CONFIRMED', 'ACCEPTED (F3 confirmed; repaired in R3 artifacts)',
     'Pending human review must never serialize as FAIL; OVERALL pass never means human acceptance.',
     'none'),
    ('R3C-13', 'F3', 'supersedes the R2G13 gate label',
     'The R2G13 gate name "tally {CONFIRMED 17, REJECTED 7}" is STALE: the actual R2 CLAIM_MATRIX.csv '
     'rows tally CONFIRMED 16 / REJECTED 8 (recounted from the emitted CSV). R3 tally labels are '
     'derived from actual rows at emit time',
     '01_RAW/R2_STATE_RESUM.json; gate R3G16',
     H['r2_matrix'], 'R2 CLAIM_MATRIX.csv', '24 claim rows',
     'HISTORICAL_RESUM (parse of the actual emitted rows)',
     'labels derived from parsed rows, never copied from gate names',
     'the stale {17,7} label and the pending-as-FAIL serialization are both detected',
     'CONFIRMED', 'ACCEPTED (presentation defect; the table itself was never invalid)',
     'Actual R2 tally: 16 CONFIRMED / 8 REJECTED.',
     'none'),
    ('R3C-14', 'F5', 'preserves R2 Area C acceptance; documents the bare-CR policy',
     '12/12 lossless sidecars re-verified by full-file byte reconstruction; field-level mapping '
     'independently compared under the EXPLICIT custom physical-line contract: 0 mapping errors '
     'across all strict rows (R39 row 10 computed_by="n/a\\r" matches the sidecar exactly). Under '
     'standard CSV record semantics the same row parses as "n/a" — an interpretive difference, NOT '
     'raw-byte loss; both layers preserve the original bytes. No manifest migration is authorized',
     '01_RAW/SIDECAR_BARE_CR_ANALYSIS.json; gate R3G14',
     H['sidecar'], '12 R2 sidecars + their original manifests', '12 files / all strict rows',
     'PHYSICAL_RECOMPUTATION (byte reconstruction + independent state-machine field comparison)',
     'reassembly is byte-level; the field comparison uses an independently written parser with the R2 builder semantics',
     'any byte difference or mapping mismatch fails the gate',
     'CONFIRMED', 'ACCEPTED (byte-lossless 12/12 retained; policy documented)',
     'Bare CR inside a physical row is DATA under the custom contract; CSV-record parsing differs by interpretation on exactly one row.',
     'none'),
    ('R3C-15', 'SCOPE', 'none',
     'Scope discipline: all writes confined to the run dir + the single authorized publication '
     'path; R2 and historical runs unmodified (hash pins re-verified before use); no game/Ghidra '
     'execution; no wiki application; no canonical/vault update; no milestone promotion; no '
     'morph-boundary research; the unrelated untracked docs/audits/PE_MILESTONE_1_WORLD_SURFACE_R1_GATE/ '
     'untouched',
     '02_LOGS/LOGS.md (command log); publication record in HANDOFF.md',
     H['tests'], 'n/a', 'structural',
     'STRUCTURAL (file inventory + git status at publication)',
     'the run writes only enumerated paths; sources are opened read-only',
     'any out-of-scope write would appear in the inventory/git status and fail publication',
     'CONFIRMED', 'ACCEPTED',
     'Read-only on sources; new run-local work + one bounded publication only.',
     'none'),
]

# ------------------------------------------------------- finding dispositions
FINDINGS = [
    ('F1', 'external post-audit', 'Two R2 Node hash primitives are wrong; aggregate agreement conceals it',
     'R3C-01, R3C-02, R3C-03, R3C-05, R3C-06', 'CONFIRMED',
     'reproduced from the executed literal declarations (counterexamples tested, not assumed); '
     'root causes identified (adler roles/initials; fnv float64); defect census bounded (crc32 clean); '
     'per-entry value census complete; repaired STAGE-LOCALLY (00_CONTROL/r3_primitives.py + probe); '
     'R2 preserved unchanged (hash-pinned, read-only); supersession rows S-01..S-08'),
    ('F2', 'external post-audit', 'P1R2-5 overstates the morph residual population (334 = all-tested-grammar miss)',
     'R3C-10', 'CONFIRMED',
     'independent re-sum of the hash-pinned R34 per_span raw records: 334 VARIABLE-K residual; '
     '62 with another recorded fit; 272 none; 3 concrete counterexamples; corrected wording '
     'proposed (P1R2-5-R3); alternative fits NOT promoted; scoped denominators 2,093/2,427 and '
     '3,186/6,167 re-derived'),
    ('F2b', 'external post-audit section 3 (broader P2R2-2 reading)', 
     '"every byte-exact grammar reproduced at 100%" must not be exported as all 21 claims passing at 100%',
     'R3C-11', 'CONFIRMED',
     'R35 21-claim table transcribed with exact IDs/denominators/verdicts: 19 ERA-STABLE + 2 EVOLVED; '
     'C-MORPH-1 partial fit (86.2%/81.0%); corrected wording proposed (P2R2-2-R3)'),
    ('F3', 'external post-audit', 'Pending human review serialized as false/FAIL; R2G13 tally label stale',
     'R3C-12, R3C-13', 'CONFIRMED',
     'R2 bool(None)->false reproduced and detected (negative control exit 1, failed predicate captured); '
     'three-state PENDING/PASS/FAIL preserved through R3 gate function/JSON/CSV/report; actual R2 '
     'tally recounted from rows: 16/8 vs the stale 17/7 label; R3 labels derived from actual rows'),
    ('F5', 'external post-audit section 5', 'Sidecar semantic scope: R39 final-row bare CR; R2G10 checks mapping only as a dict',
     'R3C-14', 'CONFIRMED',
     'bare-CR policy documented explicitly; field-level comparison added under the custom '
     'physical-line contract (0 errors, R39 row 10 included); CSV-record difference recorded as '
     'interpretive, not byte loss; 12/12 byte-lossless acceptance retained; no manifest migration'),
    ('N1', 'this run (new measurement)', 'adler32(payload): complete per-payload value census (11022/11022 mismatches)',
     'R3C-06', 'CONFIRMED',
     'the external post-audit measured name inputs only and explicitly did not claim a per-payload '
     'census; R3 measures it: the R2 adler differs from RFC1950 adler on every payload in both corpora'),
    ('N2', 'this run (new measurement)', 'The 6 FNV coincidence inputs are identified (508629.nif, 186733.nif, 147508.nif in both eras)',
     'R3C-06', 'CONFIRMED',
     'coincidence mechanism: float64 products stay exact when (x XOR b) is divisible by 4 (magnitude '
     '2^54-2^55 spacing 4); census recorded with values'),
]

# --------------------------------------------------------- supersession map
SUPER = [
    ('S-01', 'R2 00_CONTROL/control_r2.cjs', 'function adler32(b) { let a = 1, s = 0;',
     'the defective R2 Node adler32 declaration',
     'R3 00_CONTROL/r3_primitives.py adler32_rfc1950 (RFC1950: s1=1, s2=0, mod 65521) — stage-local; '
     'the R2 file is preserved read-only and hash-pinned', 'VALUE-LEVEL SUPERSESSION (R2 preserved)'),
    ('S-02', 'R2 00_CONTROL/control_r2.cjs', 'function fnv1a(b) { let x = 0x811C9DC5;',
     'the defective R2 Node fnv1a declaration (float64 multiply)',
     'R3 00_CONTROL/r3_primitives.py fnv1a_rfc9923 (exact multiply mod 2^32) + Node BigInt leg — '
     'stage-local; R2 preserved', 'VALUE-LEVEL SUPERSESSION (R2 preserved)'),
    ('S-03', 'R2 01_RAW/RECOUNTS.json',
     '"method": "PHYSICAL RECOMPUTATION this run over both full containers (Node hand-rolled CRC32/adler32/FNV-1a',
     'R2 census method provenance (Node named as correct implementation)',
     'R3 01_RAW/CENSUS_RECOUNT_R3.json: corrected primitives after identity pass; the R2 Node values '
     'are recorded as a defect; aggregate counts UNCHANGED', 'METHOD-PROVENANCE SUPERSESSION (result retained)'),
    ('S-04', 'R2 02_LOGS/TEST_RESULTS.json',
     'candidate recount: NINE exact-zero + payload-CRC nonzero (Python == Node == R36 historical)',
     'R2G8 independence assurance ("three independent computations (Node, Python, R36 historical)")',
     'R3 gate R3G11: corrected == R2 Python == R36 historical (20/20); the R2 Node leg computed '
     'different functions with coincidentally identical zero aggregates; physical result retained',
     'METHOD-ASSURANCE SUPERSESSION (gate result retained)'),
    ('S-05', 'R2 06_REPORT/00_FINAL_REPORT.md',
     'Node hand-rolled CRC32/adler32/', 'R2 report method claim "cross-checked against Python zlib"',
     'R3 06_REPORT/00_FINAL_REPORT.md Area B wording: the cross-check was aggregate-only; value-level '
     'cross-check FAILS for adler/fnv (11022/11022, 11016/11022); crc32 clean; historical file not edited',
     'REPORT-WORDING SUPERSESSION (ledger entry; history not rewritten)'),
    ('S-06', 'R2 05_ANALYSIS/CLAIM_MATRIX.csv',
     'PHYSICAL RECOMPUTATION this run (Node hand-rolled crc32/adler32/fnv1a',
     'C2-B-01 method provenance wording',
     'R3C-07: the nine-zero + CRC-subset result is CONFIRMED via the corrected recount; the Node '
     'hand-rolled provenance is superseded (the named functions were not computed by the R2 Node leg)',
     'METHOD-PROVENANCE SUPERSESSION (claim result retained)'),
    ('S-07', 'R2 05_ANALYSIS/CLAIM_MATRIX.csv',
     'The R2 executable gate suite DETECTS the erroneous R1 fixtures',
     'C2-E-02 gate-detection assurance',
     'R3: the R2 suite did NOT detect the R2 helper value defects (no value-identity gate existed); '
     'R3 adds KAT + per-entry identity gates that DO detect them (R3G4/R3G9/R3G6b) plus the '
     'wrong-value aggregate-preservation control (R3G7a/R3G7b)',
     'GATE-ASSURANCE SUPERSESSION (demonstrated by negative controls)'),
    ('S-08', 'R2 HANDOFF.md', 'three-way agreement (Node/Python/R36 historical)',
     'R2 handoff wording',
     'R3 HANDOFF wording: corrected-primitives agreement with R2 Python and R36 historical; R2 Node '
     'values recorded as a defect', 'HANDOFF-WORDING SUPERSESSION'),
    ('S-09', 'R2 00_CONTROL/run_gates.py', "'pass': bool(ok)})", 'R2 gate serialization (pending -> false/FAIL)',
     'R3 00_CONTROL/r3_primitives.py three_state(): PENDING/PASS/FAIL; R3 gate records carry '
     'state + pass=null for human-review gates; OVERALL is distinct from human acceptance',
     'SERIALIZATION SUPERSESSION (R2 preserved; R2 HR-1..4 were PENDING, not FAIL)'),
    ('S-10', 'R2 02_LOGS/TEST_RESULTS.json',
     'tally {CONFIRMED 17, REJECTED 7}', 'R2G13 stale tally label',
     'R3 gate R3G16 + emit_r3_outputs.py: tally labels derived from ACTUAL emitted rows (R2 actual: '
     '16/8; R3 labels derived at emit time)', 'LABEL-ORIGIN SUPERSESSION (table was never invalid)'),
    ('S-11', 'R2 06_REPORT/PROPOSED_DOC_CORRECTIONS_R2.md',
     '334 real-record spans fit no tested grammar', 'R2 P1R2-5 wording (overstates the residual)',
     'R3 06_REPORT/PROPOSED_DOC_CORRECTIONS_R3.md P1R2-5-R3: 334 = VARIABLE-K residual among '
     'classifier-real spans; 62 with another recorded fit; 272 none among recorded alternatives; '
     'alternative fits not promoted; scope 2,093/2,427 and 3,186/6,167 unchanged',
     'PROPOSAL-WORDING SUPERSESSION (both are proposals; neither applied)'),
    ('S-12', 'R2 06_REPORT/PROPOSED_DOC_CORRECTIONS_R2.md',
     'every byte-exact grammar reproduced at 100%', 'R2 P2R2-2 conclusion sentence (as a 21-claim summary)',
     'R3 06_REPORT/PROPOSED_DOC_CORRECTIONS_R3.md P2R2-2-R3: 100% scoped to the byte-exact validator '
     'populations; 19 ERA-STABLE + 2 EVOLVED; C-MORPH-1 partial fit (86.2%/81.0%) stated; exact '
     'claim IDs/denominators retained', 'PROPOSAL-WORDING SUPERSESSION (both are proposals; neither applied)'),
]


def main():
    ANA.mkdir(parents=True, exist_ok=True)
    # quote verification: each supersession quote must exist in the pinned R2 artifact
    artifacts = {
        'R2 00_CONTROL/control_r2.cjs': R2 / '00_CONTROL/control_r2.cjs',
        'R2 01_RAW/RECOUNTS.json': R2 / '01_RAW/RECOUNTS.json',
        'R2 02_LOGS/TEST_RESULTS.json': R2 / '02_LOGS/TEST_RESULTS.json',
        'R2 06_REPORT/00_FINAL_REPORT.md': R2 / '06_REPORT/00_FINAL_REPORT.md',
        'R2 05_ANALYSIS/CLAIM_MATRIX.csv': R2 / '05_ANALYSIS/CLAIM_MATRIX.csv',
        'R2 HANDOFF.md': R2 / 'HANDOFF.md',
        'R2 00_CONTROL/run_gates.py': R2 / '00_CONTROL/run_gates.py',
        'R2 06_REPORT/PROPOSED_DOC_CORRECTIONS_R2.md': R2 / '06_REPORT/PROPOSED_DOC_CORRECTIONS_R2.md',
    }
    cache = {}
    failures = []

    def norm(s: str) -> str:
        return re.sub(r'\s+', ' ', s)

    for sid, art, quote, _, _, _ in SUPER:
        if art not in artifacts:
            failures.append((sid, 'unknown artifact ' + art))
            continue
        if art not in cache:
            cache[art] = artifacts[art].read_text(encoding='utf-8', errors='replace')
        if norm(quote) not in norm(cache[art]):
            failures.append((sid, 'quote not found in ' + art))
    if failures:
        for f in failures:
            print('QUOTE VERIFICATION FAILURE:', f, file=sys.stderr)
        sys.exit(1)

    with open(ANA / 'CLAIM_MATRIX.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['claim_id', 'area', 'supersedes', 'literal_claim', 'source_location',
                    'source_sha256', 'corpus_era', 'denominator', 'method_class',
                    'test_independence', 'counterexample', 'knowledge_status', 'disposition',
                    'proposed_wording', 'missing_for_stronger'])
        for c in CLAIMS:
            w.writerow(c)

    with open(ANA / 'FINDING_DISPOSITIONS.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['finding_id', 'origin', 'finding', 'evidence_claims', 'status', 'disposition'])
        for f in FINDINGS:
            w.writerow(f)

    with open(ANA / 'SUPERSESSION_MAP.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['supersession_id', 'r2_artifact', 'quote_verified_present', 'r2_item',
                    'r3_replacement', 'supersession_class'])
        for sid, art, quote, item, repl, cls in SUPER:
            w.writerow([sid, art, 'true (verified at emit time)', item, repl, cls])

    print(json.dumps({'claims': len(CLAIMS), 'findings': len(FINDINGS), 'supersessions': len(SUPER),
                      'quote_verification': 'ALL PRESENT (%d quotes)' % len(SUPER)}))


if __name__ == '__main__':
    import json
    main()
