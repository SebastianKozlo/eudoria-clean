# PROPOSALS_P2P3_FIXED — PE_NIF_R3_PERSISTENCE_AND_TARGETMAP_R1

RUN_ID = PE_NIF_R3_PERSISTENCE_AND_TARGETMAP_R1_20260905_101203
STATUS = PROPOSALS ONLY (corrected wording). Nothing here is applied to
docs/nif, the wiki, canon or any historical artifact. This document provides
the CORRECTED P2R2-2-R3 and P3R3 texts per the human-relayed follow-up review
(MASTER_PARTIAL_PASS): the R3 file
06_REPORT\PROPOSED_DOC_CORRECTIONS_R3.md (SHA256
84B3D05DB719AB09A6CEECE8300BBEE059655B5443F6B5CFC1090B4C8B7EC8E6, verified
this run) is UNMODIFIED; the texts below supersede it IN INTENT ONLY, and an
authorized applier must use THESE texts (not the uncorrected R3 clauses)
where the follow-up review flagged risk. Evidence sources unchanged from R3:
01_RAW\R35_CLAIM_TABLE_PRESERVED.json (21-claim verbatim transcription),
02_LOGS\kat_wrong_value_controls.json + gates R3G7b/R3G10/R3G11.

WHAT CHANGED AND WHY (summary):
- P2: the R3 P2R2-2-R3 clause "every BYTE-EXACT VALIDATOR reproduced at 100%
  WITHIN ITS TESTED POPULATION" is REMOVED. It is a categorical statement
  that C-MORPH-1 falsifies as worded (C-MORPH-1 IS a byte-exact validator
  claim and is a PARTIAL FIT — 86.2%/81.0%; its changed-payload family
  presence witness is ASCII-name presence only, 3 files / 29 occurrences,
  NOT a validator claim). The 100% statement is replaced by an explicit
  per-claim scoping to the measured claim population (the R35 table, exact
  claim IDs and denominators, nothing summarized beyond a recorded
  denominator).
- P3: the R3 clauses "zero-match is insensitive to value errors" /
  "provably insensitive to value errors" are replaced by the
  evidence-bounded statement: the insensitivity is PROVEN for the specific
  R3 wrong-value controls (adler32_wrong_xor, fnv1a_wrong_basis) and for the
  two R2 hash defects on the 2003 and 9.3.5 Models.bnt corpora — NOT a
  general property of arbitrary hash functions, candidate sets or corpora.

---

## P2R2-2-R3-FIXED (corrected P2; replaces the R3 P2R2-2-R3 NEW text)

Target: docs/nif/10-containers-corpus.md lines 121-125 (the standing
"Conclusion (CONFIRMED)" block — the R1 P2-2 / R2 P2R2-2 / R3 P2R2-2-R3
proposal lineage target; none of the predecessors was ever applied).
Operation: REPLACE. The old fragment (verbatim, current lines) is recorded
in 05_ANALYSIS\TARGET_MAP.json (machine-verified to occur exactly once).

Forbidden exports (both): "All 21 claims reproduced at 100%" AND "every
BYTE-EXACT VALIDATOR reproduced at 100%" must NOT be exported anywhere.

<!-- EXTRACT:P2R2-2-R3-FIXED:START -->
**Conclusion (CONFIRMED at the tested scope): in the 21 tested grammar claims on the 2003 and 9.3.5 Models.bnt corpora (5,426/5,426 + 5,596/5,596 parse closure; note 5,208/5,422 shared files are byte-identical across eras), 19 claims are ERA-STABLE and 2 are EVOLVED (C-G3B-3 failure-profile delta; C-SHAD-2 vocabulary delta). Per-claim validator results are exactly as recorded in the R35 21-claim table (verbatim transcription with exact claim IDs, denominators, verdicts and evidence statuses; no result is summarized beyond its recorded denominator): C-MORPH-1 is a PARTIAL-FIT claim (rr 2,093/2,427 = 86.2% on 9.3.5; 1,180/1,457 = 81.0% on 2003), not a 100% fit — and its changed-payload family-presence witness is ASCII-NAME PRESENCE ONLY (3 files / 29 occurrences), not a validator claim; C-MORPH-2 is a statistical-signature match (99.4% / 99.31% strict-00, same grid profile), not a 100% validator; C-G3B-3's rule has failures in both eras (182 / 180, same 3 classes — failure-count profile EVOLVED, every failure still fits the C-G3B-1 grammar); C-SHAD-2's vocabulary is 16/17 shared names (BaseTexture absent in 2003). The byte-exact validator claims with full-population results in both eras are enumerated in the R35 table (C-G3B-1, C-G3B-2, the five rare-family claims C-RARE-G9_RTTI/G3E/BINARY/SHORT28/G3A_PREAMBLE, C-TEX-1..C-TEX-5, C-SHAD-1, C-IMP-1..C-IMP-4 — per-claim statuses as recorded there, including C-IMP-4 STRONGLY_SUPPORTED with the 38/38 link-chain targets and a content-level state-census delta); no categorical "every validator at 100%" statement is made. The rare-family and importer pattern censuses were count-identical. All drift observed in the tested claims was CONTENT; no grammar-level drift was found. No claim is made about untested claims, other archives, or other versions.**
<!-- EXTRACT:P2R2-2-R3-FIXED:END -->

---

## P3R3-FIXED (corrected P3; replaces the R3 P3R3 ledger-entry texts)

Correction-ledger entries for the R2 texts that asserted the R2 Node hash
primitives as correct implementations (historical files are NOT edited; the
entries record the superseded wording). Three entries; entry 2 is unchanged
from R3 (it contains no insensitivity claim); entries 1 and 3 carry the
evidence-bounded insensitivity statement.

### Entry 1 — R2 06_REPORT/00_FINAL_REPORT.md Area B sentence

Old (superseded R2 wording, verified present exactly once in the historical
file; see TARGET_MAP.json P3R3/a): "Node hand-rolled CRC32/adler32/FNV-1a
cross-checked against Python zlib".

<!-- EXTRACT:P3R3-FIXED-1:START -->
the candidate census was recomputed with stage-local primitives validated by known-answer tests and per-entry oracle identity (R3); the R2 Node adler32 and fnv1a helpers are CONFIRMED defective (value mismatches on 11,022/11,022 name inputs, 11,022/11,022 payload inputs, and 11,016/11,022 name inputs respectively); the R2 crc32 helper and the size/offset candidates were correct; the aggregate counts were never affected because the aggregate zero-match property was DEMONSTRATED insensitive to these specific value errors on these two corpora: the R3 wrong-value controls (adler32_wrong_xor, fnv1a_wrong_basis) failed their known-answer tests (exit 1) while producing the identical zero-match census, and the two R2 defects themselves yielded zero-match aggregates identical to the corrected primitives (02_LOGS/kat_wrong_value_controls.json + R3G7b; R3G10/R3G11). The insensitivity is PROVEN for those controls and those defects on the 2003 and 9.3.5 Models.bnt corpora — NOT asserted as a general property of arbitrary hash functions, candidate sets, or corpora.
<!-- EXTRACT:P3R3-FIXED-1:END -->

### Entry 2 — R2G8 wording (UNCHANGED from R3; no fix required)

Old (superseded R2 wording; see TARGET_MAP.json P3R3/b): "Python == Node ==
R36 historical" / "three independent computations (Node, Python, R36
historical)". Corrected (verbatim from R3 P3R3 — retained): "corrected
primitives == R2 Python (zlib/exact-int) == R36 historical (zlib/exact-int);
the R2 Node leg computed different functions whose zero-match aggregates
coincidentally agreed".

### Entry 3 — Standing rule (the P0)

<!-- EXTRACT:P3R3-FIXED-3:START -->
Standing rule (the P0): hash-primitive VALUE IDENTITY (known-answer tests + per-entry oracle agreement) must be established BEFORE aggregate acceptance, because aggregate zero-match counts were DEMONSTRATED insensitive to the tested value errors — insensitivity PROVEN for the specific R3 wrong-value controls (adler32_wrong_xor, fnv1a_wrong_basis: KAT exit 1 with identical zero-match census, 02_LOGS/kat_wrong_value_controls.json + R3G7b) and for the two R2 hash defects on the 2003 and 9.3.5 Models.bnt corpora, NOT a general property of arbitrary functions or corpora — which is precisely why value identity cannot be inferred from aggregate agreement and must be established per run.
<!-- EXTRACT:P3R3-FIXED-3:END -->

---

## Machine-verification note

The EXTRACT-marked blocks above are the canonical fixed texts;
00_CONTROL\build_package_r1.py extracts them verbatim (marker-to-marker,
marker lines stripped) and embeds them into
05_ANALYSIS\TARGET_MAP.json as the proposed new texts for the
P2R2-2-R3-FIXED and P3R3-FIXED entries, and verifies (whitespace-normalized)
that the unchanged portions of Entry 2 remain substrings of the hash-verified
PROPOSED_DOC_CORRECTIONS_R3.md. All other R3 proposal texts (P1R2-5-R3,
P4R3, P5R3) are carried verbatim from PROPOSED_DOC_CORRECTIONS_R3.md with no
fix (verified as whitespace-normalized substrings of that file by the same
driver).
