# HANDOFF — PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002

Executor: pe-reconstruction (STATIC-ONLY executor session).
Dispatch: PE-MASTER direct, under human authorization PE_935_20002_PAYLOAD30_CONSUMER_HUMAN_AUTH_R1_20261002.

## Delivery notice (compact)

- RUN_STATUS = CONSUMER_REACHED_ROLE_STRONGLY_SUPPORTED
- HARD_STOP_REASON = Contract §19 terminal hard stop after completion of the single authorized science question; no further experiment authorized (NEXT_EXPERIMENT_AUTHORIZED = NO).
- AUDIT_OUTPUT_ROOT = D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002\
- FINAL_REPORT_PATH = <root>\06_REPORT\REPORT.md
- PRIMARY_EVIDENCE_PATHS (top):
  1. <root>\01_RAW\CLIENT_READ_BYTES.json — 45/45 byte-pins of the routing + client-read + store chain
  2. <root>\01_RAW\RECORD_FRAMING.jsonl + RECORD_FRAMING_SUMMARY.json — full-file framing census (1,366 records, exact EOF, NC-FRAMING)
  3. <root>\01_RAW\FIELD_BYTE_ANCHOR.json — anchored records with machine-checked bounds assertions
  4. <root>\01_RAW\TLV_WALK_CENSUS.json — client-semantics walk over all 1,366 records (tag 0x11 value at +0x30 in 1366/1366; tail 0 in 1366/1366)
  5. <root>\01_RAW\ROUTING_CENSUS_RAW.json — imm32 0x4E22 / mangling / string census
  6. <root>\01_RAW\GHIDRA_ROUTING\PASS15_GHIDRA_DUMP.json — the 202-site consumer census
  7. <root>\01_RAW\RELEVANT_XREFS.json — consolidated reference censuses
  8. <root>\02_ANALYSIS\VFS_TO_PARSER_TRACE.md — the byte-pinned routing chain (§8)
  9. <root>\02_ANALYSIS\FIELD_TO_DESTINATION_TRACE.md — the §9 read/store chain
  10. <root>\02_ANALYSIS\NEGATIVE_CONTROLS.md — NC-FRAMING / NC-ANCHOR-ADJ / NC-RECORD / NC-VALUE
- ACTUAL_HEAD_end = 9203b6d1ad5025f4158d5165863594132aaac49f (== BASE_SHA; unchanged)
- Git-status-delta: ONLY the new package dir `docs/audits/PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002/` added (untracked); the 5 pre-existing untracked groups byte-identical (see process note below); 0 staged entries; 0 commits.
- NO-COMMIT / NO-PUSH / NO-RUNTIME: CONFIRMED (no git commit/push/stage performed; the client Entropia.exe was never launched — all evidence is static; no runtime hooks).
- Package file count at delivery: 364 files outside 04_QC (363 covered by MANIFEST_SHA256.csv + the manifest itself, self-excluded per the L12 precedent; the manifest additionally carries one NOTE row that is not a file row; 04_QC\ was reserved for the fresh QC worker and is excluded from the executor manifest).
- REPORT.md SHA256: recorded in MANIFEST_SHA256.csv (the manifest is the authoritative in-package hash census; it is KNOWN-STALE until the final regeneration after the QC round and the PE-MASTER verdict).

## Result in one paragraph

The value at payload+0x30 of a 20002.vfs record is the tag-0x11 (17th) property value of the record's TLV property block: every record carries six entries (tags 1, 0xC, 0xD, 0xE, 0x10, 0x11) under flags 0x80 / count 6, and the tag-0x11 value sits at payload+0x30 in 1366/1366 records. Class 20002 is ArkParameterArmor (RTTI-confirmed); its class object opens its own data file as itoa(20002)+".vfs" and loads records on demand into ArkParameterArmor instances (0x58 bytes, 22-slot value arrays). The generic property parser reads the +0x30 field with a native 4-byte little-endian load (VA 0x00412553) and stores it — a pure copy, no comparison/lookup — into the instance's value-array slot 21 (VA 0x0041255A), exposed thereafter to the client's generic property-read machinery (no statically-coded tag-0x11 reader exists; reads are runtime-tag-driven). The gameplay semantics of the property remain UNVERIFIED; no world/model/placement edge is claimed or demonstrated.

## Process notes (full disclosure)

1. EXECUTOR INCIDENT (found and repaired in-run): the first execution of the cross-validation script (03_SCRIPTS\s3_crossval_vfs_common.py) imported the prior tool without suppressing CPython bytecode, causing CPython to create `docs\audits\PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928\04_TOOLS\__pycache__\vfs_common.cpython-312.pyc` — a write outside OUTPUT_ROOT into a pre-existing untracked group. REPAIR: the artifact was deleted; the group was re-verified byte-identical to its pre-run state (228 files; latest write 2026-09-30, before this run); the script was patched with `sys.dont_write_bytecode = True` and re-run (cross-validation re-confirmed FULL_BOUNDARY_AGREEMENT 1366/1366) without recreating the artifact. No other pre-existing group was touched (all latest writes 2026-09-11..09-30).
2. Ghidra usage: headless analyzeHeadless against a project in the pre-approved temp dir (C:\Users\User\AppData\Local\Temp\opencode\pe935_20002_ghidra); the analyzed program was imported from the pinned physical Entropia.exe; every load-bearing claim is byte-pinned by re-reading the pinned EXE directly (01_RAW\CLIENT_READ_BYTES.json) — Ghidra output is analysis context, never the sole basis of a load-bearing claim. All java processes exited before this handoff (verified; no untracked writer remains). The temp Ghidra project persists in the temp dir (bounded tooling state; safe to delete).
3. Ghidra postScript execution quirks (documented for QC): pass 1 postScript initially failed on Jython-2 os.makedirs(exist_ok) and was fixed + re-run via -process on the already-analyzed program; an early crash on mem.getBytes was fixed with a jarray buffer. These were tooling fixes inside OUTPUT_ROOT, not science changes.
4. The 202-site consumer census (PASS15) scanned the instruction context before each FUN_0070c180 call for a static immediate tag 0x11; the 2 candidate hits were examined and shown to be false positives (the parse loop's own register tag; a state-variable byte with actual tag 0x2 for class 24017). The conclusion "no static tag-0x11 reader" is therefore evidence-based, not an absence of search.

## SELF_CHECK (executor self-check; explicitly NOT the independent MASTER/QC audit)

- S0: HEAD/EXE/VFS re-measured, all MATCH (00_CONTROL\PREFLIGHT.md). Gate PASS.
- S1: in-run framing implementation (own code), byte-exact EOF walk, 1,366 records with derivation; anchored records' boundaries recorded; NC-FRAMING executed and falsifies (4/4 mandatory classes). Gate PASS.
- S2: bounds assertions present and machine-checked for all analyzed records (1366/1366 true); census denominator == record count; width/endianness provenance labeled (HYPOTHESIS_DERIVED in census rows, upgraded to RAW after the instruction pin — documented per V2-009). Gate PASS.
- S3: §8 outputs present; GENERIC_PARSER_IDENTIFIED=YES; 20002_VFS_ROUTED_TO_GENERIC_PARSER=CONFIRMED with byte-level evidence (45/45 pins); the §B parser-family lead was re-verified and corrected to its actual file (EnvironmentZones.vfs) — recorded per the LEADS_TO_REVERIFY discipline. Gate PASS.
- S4: CLIENT_READ_IDENTIFIED=YES; every load-bearing instruction byte-pinned (45/45: bytes at FILE_OFFSET in the pinned EXE == recorded ORIGINAL_BYTES); full §9 chain fields recorded; no decompiler-text-only claim. Gate PASS.
- S5: scopes/counts/unresolved-lists present; V2-012 exhaustiveness wording applied (ONLY_DIRECT_WRITER_FOUND / bounded read census / global exhaustiveness UNVERIFIED). Gate PASS.
- S6: KEY_ROLE/LOOKUP_CONTAINER N-A documented (no lookup at the traced instructions); FIELD_IDENTITY / OBSERVED_OPERATION / FINAL_SEMANTIC_ROLE reported separately; §13 controls executed (NC-VALUE not-applicable documented with its measured precondition). Gate PASS.
- S7 wording honesty: no §2-forbidden label applied to the value anywhere in the package (checked: the only label applied is the structural "tag-0x11 property value / armor-parameter slot" — identity established in-run; the id2-domain observation is cited as CONTEXT ONLY with no significance language; all conclusions STATIC_ONLY; runtime reachability NOT_TESTED; prior citations labeled PRIOR_EVIDENCE/LEAD). Gate PASS.
- S8: all §17 artifacts exist (00_CONTROL/01_RAW/02_ANALYSIS/03_SCRIPTS/06_REPORT; 04_QC reserved-empty); REPORT carries all §18 fields (key-by-key present); git delta == only the new package dir + 5 byte-identical pre-existing groups (post-repair verified); HEAD unchanged; ZERO commits; ZERO staged; no Entropia.exe process ever launched; manifest census documented (362 rows + self-exclusion). Gate PASS (after the disclosed incident repair).
- Contract gates: no gate failed at delivery time. No default-success fallback: the RUN_STATUS is derived from the reached evidence, and the UNVERIFIED semantic axis is preserved rather than inflated.

## Next steps (per contract §19 — NOT for the executor to perform)

- Fresh internal-QC worker (04_QC\; §C requirements; share no code with the executor implementations).
- INDEPENDENT_CHATGPT_DESKTOP_POST_AUDIT_REQUIRED = YES (human-side).
- AUTO_FOLLOWUP_RE = NO; NEXT_EXPERIMENT_AUTHORIZED = NO; HARD_STOP = YES.
