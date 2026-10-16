# HANDOFF — PE_935_WRAPPER_POINTER_NEIGHBORHOOD_R2_20261016

RUN_STATUS = COMPLETE_WITHIN_BOUND
FINAL_REPORT_PATH = D:\Eudoria_Reconstruction\99_Audits\PE_935_WRAPPER_POINTER_NEIGHBORHOOD_R2_20261016\REPORT.md
PRIMARY_EVIDENCE_PATHS =
  D:\Eudoria_Reconstruction\99_Audits\PE_935_WRAPPER_POINTER_NEIGHBORHOOD_R2_20261016\DWORD_ROSTER.json
  D:\Eudoria_Reconstruction\99_Audits\PE_935_WRAPPER_POINTER_NEIGHBORHOOD_R2_20261016\RAW_TEXT_REFERENCES.jsonl
  D:\Eudoria_Reconstruction\99_Audits\PE_935_WRAPPER_POINTER_NEIGHBORHOOD_R2_20261016\RAW_TEXT_SCAN_META.json
  D:\Eudoria_Reconstruction\99_Audits\PE_935_WRAPPER_POINTER_NEIGHBORHOOD_R2_20261016\NOVELTY_ANALYSIS.json
  D:\Eudoria_Reconstruction\99_Audits\PE_935_WRAPPER_POINTER_NEIGHBORHOOD_R2_20261016\PRIOR_EVIDENCE_COMPARISON.json
  D:\Eudoria_Reconstruction\99_Audits\PE_935_WRAPPER_POINTER_NEIGHBORHOOD_R2_20261016\CONFLICT_INVESTIGATION.json
  D:\Eudoria_Reconstruction\99_Audits\PE_935_WRAPPER_POINTER_NEIGHBORHOOD_R2_20261016\WINDOW_READ1.bin / WINDOW_READ2.bin
  D:\Eudoria_Reconstruction\99_Audits\PE_935_WRAPPER_POINTER_NEIGHBORHOOD_R2_20261016\SOURCE_READS_LEDGER.jsonl
HARD_STOP_REASON = NONE (single bounded run completed; hard stop per contract)

Summary for PE-MASTER:
- Science A: window [0x00A91CC0,0x00A91D40) dual-read 128/128; 32-DWORD roster; mandatory control slot 15 =
  0x00852A30 PASS; slots 0-26 CONFIRM prior documentation; slots 27-31 newly documented.
- Science B: single full .text read; census COMPLETE; TOTAL_RAW_HITS = 13; frozen basis
  PRIOR_RAW_MATCHES = 0 / NEW_RAW_CANDIDATES = 13; investigation-refined (POST-HOC) basis
  PRIOR_RAW_MATCHES = 4 / NEW_RAW_CANDIDATES = 9; all hits RAW_ADDRESS_OCCURRENCE_UNQUALIFIED.
- S7 controls: 4 formal PRIOR_EVIDENCE_CONFLICTs at the preregistered va+8 positions; §3 investigation
  (already-read data only) proved the S7 window format is CENTERED (S7 va = raw imm32 position): patterns
  + post-bytes byte-confirmed at the S7 va anchors; census hits exactly there; NO massaging; dual basis
  reported (CONFLICT_INVESTIGATION.json).
- Novelty: NEW_STRUCTURAL_KNOWLEDGE = NEW_STRUCTURAL_FACTS_CONFIRMED_RAW; NEW_SEMANTIC_KNOWLEDGE = NOT_ESTABLISHED.
- Advisory (assessment only): GO_PORTAL_ROSETTA (assessment only, NOT executed): 5 raw occurrence(s) of window slot address(es) have NO prior documentation at any level — slot 4 (0x00A91CD0) @ 0x008506BA; slot 12 (0x00A91CF0) @ 0x00851F36; slot 25 (0x00A91D24) @ 0x00853522; slot 26 (0x00A91D28) @ 0x00853C1D; slot 25 (0x00A91D24) @ 0x00891561. Each is a concrete falsifiable edge: a separate bounded decode run could qualify the exact instruction at that position (candidate edges include the unnamed-class vtable-store region near 0x008506BA and the raw occurrences at 0x00851F36 / 0x00853522 / 0x00891561 / 0x00853C1D).
- Budget: EXACTLY 22,802,688 B of EXE reads; output within limits; 1 correction round (of 2).
- SELF_QC != INDEPENDENT_QC; external post-audit pending (PE-MASTER decision).
