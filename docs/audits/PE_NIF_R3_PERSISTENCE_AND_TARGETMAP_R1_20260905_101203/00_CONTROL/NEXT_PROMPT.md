# PE_NIF_R3_PERSISTENCE_AND_TARGETMAP_R1 — corrective governance run

VERDICT CONTEXT: MASTER_PARTIAL_PASS (PE-MASTER follow-up review of the R3 persistence).
R3 technical package = ACCEPTED; HR-R3-3 = HOLD (no proposal application); wiki HOLD; M2 blocked.

SCOPE (governance-only; per the human-relayed verdict):
1. [DONE by master-auditor, verified separately] R3 row restored in AUDIT_ENTRYPOINT.md
   with corrected claim status (14 CONFIRMED + 1 REJECTED-as-worded R3C-08).
2. [DONE by master-auditor] The 14+1 correction recorded in the entry-point row.
3. THIS RUN: write GATE_WEAKNESS_ADDENDUM.md — the THREE gate weaknesses from the
   follow-up review (R3G6c empty-CRC-vector coverage label via `if vec[1]` predicate;
   R3G10 PASS predicate forces only Adler-name + 5 CRCs, does not fail on wrong
   Adler-payload/FNV; "four independent implementations per defect-affected class"
   overstated — full FNV has 2, Adler 3, + iterative payload leg on a sample) —
   PLUS the minor artifact_index omission of STAGE_ACCEPTANCE_GATES.csv.
   The completed R3 package is NOT modified; this is an addendum in THIS run dir.
4. THIS RUN: build TARGET_MAP.json — the FULL P1–P5 proposal→target map:
   for each of P1R2-5-R3 / P2R2-2-R3 / P3R3 / P4R3 / P5R3 (from
   99_Audits\PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627\06_REPORT\PROPOSED_DOC_CORRECTIONS_R3.md,
   SHA256 84B3D05DB719AB09A6CEECE8300BBEE059655B5443F6B5CFC1090B4C8B7EC8E6):
   proposal_id → target file (docs/nif/...) → EXACT old fragment (verbatim, with
   current line number) → operation (replace/insert/delete) → proposed new text
   (verbatim from the proposal, with the P2/P3 fixes applied — see item 5) →
   evidence pointer. Machine-verify each old fragment appears EXACTLY ONCE.
5. THIS RUN: write PROPOSALS_P2P3_FIXED.md — the corrected P2 and P3 texts:
   P2: remove the risky "every BYTE-EXACT VALIDATOR … 100%" scope (C-MORPH-1 is
   partial — morph family presence is 3 files/29 occurrences ASCII-only); scope
   to the measured claim population.
   P3: replace the general "zero-match is insensitive to value errors" with the
   evidence-bounded statement (insensitivity PROVEN for the specific wrong-value
   controls and the two hash defects on THESE two corpora; not a general property).
6. [master-auditor] Final commit: PATH-LIMITED with full staged-index control.
7. HARD BOUNDARIES: no docs/nif application; no wiki edits; no M2; no morph
   research; no modification of the completed R3 package or any historical run.

INPUTS:
- 99_Audits\PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627\ (read-only; esp.
  06_REPORT\PROPOSED_DOC_CORRECTIONS_R3.md, CLAIM_MATRIX.csv, 00_CONTROL\revalidate_r3.py)
- 12_WebGame\eudoria-clean\docs\nif\ (read-only census of contradictory phrasings:
  position deltas / delta triples / true structure; the cross-era 100% generalization
  in 10-containers-corpus.md — exact lines from the review: 09-semantics.md:180,
  08-ark-proprietary.md:196, 10-containers-corpus.md:121 — verify current lines)
- The CONTRADICTION_CENSUS.json: every docs/nif sentence carrying the flagged
  phrasings + any other location where R3-superseded wording still stands.

OUTPUTS (in this run dir):
- 00_CONTROL\NEXT_PROMPT.md (this file, formalized)
- 00_CONTROL\SHA256_DRIVER.txt (any script hashes)
- 05_ANALYSIS\TARGET_MAP.json (item 4 — machine-verified old fragments)
- 05_ANALYSIS\CONTRADICTION_CENSUS.json (docs/nif census)
- 06_REPORT\GATE_WEAKNESS_ADDENDUM.md (item 3)
- 06_REPORT\PROPOSALS_P2P3_FIXED.md (item 5)
- REPORT.md, HANDOFF.md, STAGE_ACCEPTANCE_GATES.csv, artifact_index.csv (real SHA-256)

RUN_STATUS target: COMPLETED. All outputs = proposals/maps/addenda only. NO repo writes.
