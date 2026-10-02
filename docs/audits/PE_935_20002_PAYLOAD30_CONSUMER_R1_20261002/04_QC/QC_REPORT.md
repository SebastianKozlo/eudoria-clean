# QC_REPORT — PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002 (internal QC, fresh context)

- RUN_ID = PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002
- ASSIGNMENT_MODE = INTERNAL_QC (contract §C; PE-MASTER direct dispatch; NO_NESTED_TASKS)
- QC worker = pe-master-auditor internal-QC session (fresh context; not the formalizer; not the executor)
- QC scope = contract §C minimum duties (1)–(10) + the dispatched risk probes; NO new science; NO executor-evidence modification; QC wrote ONLY inside `04_QC\` (+ `04_QC\qc_tools\`).
- Independence statement: all QC tools (`04_QC\qc_tools\qc1…qc5`) are this worker's own implementations. They share NO code with the executor's `03_SCRIPTS` (never imported/copied) and NO code with JOIN R1's `vfs_common.py`. Every load-bearing number below was recomputed from the pinned physical bytes.
- Inputs re-verified by QC at session start (independent measurement):
  - RUN_CONTRACT.md = 27,270 B, SHA256 `24B3A5599FA16FE1E465BB82462344B35362CA7E1185F712EBC7730065D28657` — MATCHES the frozen identity (00_CONTROL\CONTRACT_FREEZE.json).
  - Entropia.exe = 8,015,872 B, SHA256 `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31` — MATCHES.
  - 20002.vfs = 174,864 B, SHA256 `C3899C3E88D72CE12CEF9B8A4F5E73B26632BB1A3207C950FF2BC40FD9C94AC4` — MATCHES.
  - git HEAD = `9203b6d1ad5025f4158d5165863594132aaac49f` = origin/master = BASE_SHA — MATCHES.

## QC_VERDICT = PASS_WITH_FINDINGS

0×P0, 0×P1, 2×P2, 5×P3 (+2 disclosed limitations). The executor's primary trace
(routing → client read → store → bounded census → statuses) was INDEPENDENTLY
REPRODUCED at every load-bearing link (framing 1366/1366, pins 45/45, RTTI chains,
call-edge denominators 202/202, TLV grammar 1366/1366, CRC-gate-skip, slot-21
derivation). The findings do not touch the primary chain; they concern (a) a §15
blast-radius mis-verification of a prior claim's function attribution, (b) the
disclosed forbidden-path `__pycache__` incident (repair verified complete), and
(c) minor provenance/labeling defects.

---

## 1. Counterchecks executed by QC (all outputs in 04_QC\; tools in 04_QC\qc_tools\)

| # | COUNTERCHECK | TOOL | RESULT |
|---|---|---|---|
| QC1 | Independent re-parse of 20002.vfs framing (own grammar derivation incl. exact-EOF base-selection test; full 1366-row comparison vs executor artifacts; anchors; TLV grammar re-derivation; CRC census; value/flags/count/tag census) | qc1_reparse_vfs.py | 1366 records, exact EOF, FULL boundary+value agreement 1366/1366 with RECORD_FRAMING.jsonl; anchors agree (rec 0: BB 2E 00 00 = 11963 @ fo 80; rec 1014: 00 00 00 00 @ fo 129872); TLV shape {1,0xC,0xD,0xE,0x10,0x11} + tail 0 in 1366/1366; tag-0x11 value offset == +0x30 in 1366/1366; crc fields all 0 (1366/1366); flags 0x80 (1366/1366), count 6 (1366/1366), u32@+0 == 20002 (1366/1366), u16@+0x2E == 0x11 (1366/1366); zeros exactly at 1014/1015; 142 distinct values, min 0, max 16409; 37 id-groups; id==composite all records |
| QC2 | Independent byte-pin verification of all 45 pins (own PE32 section parser; own VA→RVA→file-offset recomputation; own re-read of the pinned EXE) + explicit headline-instruction conversion chains + hand-decode of the FUN_00412540 window | qc2_pinverify.py | 45/45 pins OK (file-offset conversion OK for every pin; measured bytes == recorded ORIGINAL_BYTES; all expected-byte assertions pass); headline: 0x00412553 → RVA 0x12553 → fo 0x12553 → `8B 04 10` OK; 0x0041255A → fo 0x1255A → `89 02` OK; window decode confirms pure-copy (see §4.2) |
| QC3 | Independent negative controls (NOT a re-run of executor scripts): NCQ1a–e (my own corruption classes incl. a framing-NEUTRAL id-mutation control), NCQ2 (wrong-displacement +0x2C/+0x34), NCQ3 (independent imm32/mangling census), NCQ4 (TLV-absence falsifier) | qc3_negcontrols.py | NCQ1b/1c/1d: walk FAILS as required; NCQ1a: bounds assertion must flag (55 < 0x34) — recorded; NCQ1e: id garbage does NOT fail the walk (controls spurious failure); NCQ2: +0x2C = 2 distinct values (0x110000 ×1337, 0x11FFFF ×29) and +0x34 = constant 0 — structurally distinct from +0x30 (142 distinct, varying); NCQ3: imm32 `22 4E 00 00` = 3 hits at EXACTLY the executor's 3 file offsets; ASCII "20002" = 0; `$0EOCC@` = 2; `$0EOCG@` = 2; family census identical (incl. absent $0EOCD@) — FULL AGREEMENT; NCQ4: count=5 variant → tag-0x11 value-at-+0x30 predicate turns FALSE (census detects absence) |
| QC4 | RTTI chain verification (vtable→COL→TypeDescriptor→name) + independent call-edge census (E8 rel32 scan, own implementation) + "EnvironmentZones" string location/reference census + FUN_0070e810 window probe | qc4_rtti_edges.py | class-object vtable 0xA86FE0 → COL 0xAA8B00 → TD 0xB8DBC0 → name `.?AV?$ArkObjectClassImpl@VArkParameterArmor@@$0EOCC@@@` (byte-proven); instance vtable 0xA878BC → TD 0xB8EE20 → name `.?AVArkParameterArmor@@`; instance vtable slots [0x761510, 0x8E0010, 0x9154A0, 0x7263E0, 0x8E0110, 0x726340] (slot+0xC = FUN_007263e0 nested reader ✓); call-edge census reproduces every claimed edge: FUN_0075f660 callers = exactly 1 (0x726A1B); FUN_0070c180 callers = exactly 202; FUN_0070c680 callers = exactly 1 (0x703EF0); FUN_00959090 caller = 1 (0x94BDAD); FUN_0094bd30 callers = 2 (0x94E2D6/0x94E42F); FUN_0094dfc0 callers = 2 (0x94E1FC/0x94E3B7); FUN_0094e1d0 caller = 1 (0x94E4D2); FUN_0040e900 (int→string) sites = 5, NONE inside FUN_0070e810; "EnvironmentZones" @0xA9808C (.rdata), exactly 1 code ref @0x958DCE (inside FUN_00958d90); FUN_0070e810 probe → see §5 |
| QC4b | Follow-up canon-conflict probes: "textures" literal inside FUN_0070e470; family edge census; JOIN R1 claim-5 pins re-measured; Parameters-path strings | qc4b_canonconflict.py | "textures" string @0xA86858 (.rdata), code ref (PUSH 0xA86858) @0x70E4AE inside FUN_0070e470; callers of FUN_0094b9e0 = 1 (0x94E05A, inside FUN_0094dfc0); callers of FUN_0094e470 = 1 (0x94EA9C, inside FUN_0094e890); callers of FUN_0094e390 = 1 (0x94E745, inside FUN_0094e610); JOIN R1 pin @0x94D9F5 = `83 42 04` (+imm8 0x58) OK; @0x70E841 = `C7 44 24 1C 80 00 00 00` (8-byte MOV dword [ESP+0x1C],0x80; JOIN R1's 6-byte citation is a truncated transcription of the same instruction); "Data\Parameters\" string exists @0xA97E58 (.rdata) |
| QC5 | Denominator recomputation from raw artifacts; manifest census + 14 spot re-hashes; EVIDENCE_INDEX artifact census; JOIN R1 package spot-check (10 files vs its own manifest) | qc5_denominators.py | RECORD_FRAMING.jsonl = 1366 rows, 1366 bounds_ok, zeros [1014,1015], 142 distinct, min 0 max 16409; TLV_WALK_CENSUS fields consistent; PASS15: 202 sites, 2 candidates (0x726A03, 0x8AEAD5) — matches REPORT exactly; CLIENT_READ_BYTES: 45 pins, 45 matches, all_match true; manifest = 363 data rows, self-excluded, manifest↔disk PERFECT (0 missing, 0 stale), 14/14 spot re-hash OK (SHA+size); EVIDENCE_INDEX: 20 distinct artifacts cited, ALL exist on disk; JOIN R1 spot-check 10/10 SHA+size match (vfs_common.py, G2_FUN_00959090_DECOMP.txt, G3_FUN_0094d9b0_DECOMP.txt, G3_CALLERS_FUN_0094d9b0.txt, PE_MASTER_REVIEW.md, REPORT.md, UNRESOLVED.md, RUN_CONTRACT.md, AMEND_R2_ID2_MEMBERSHIP_20002_48.json, HANDOFF.md) |
| — | `__pycache__` residue sweep of the JOIN R1 package; file count; mtime census | shell (Get-ChildItem) | 0 `*.pyc`, 0 `__pycache__` dirs, 228 files total (matches the executor's repair claim), latest write 2026-09-30 22:52:33 (predates this run) |
| — | Git compliance at QC end | git | HEAD == origin/master == BASE_SHA `9203b6d1...`; `git status --short` = EXACTLY the 6 untracked groups (this run's package + the 5 pre-existing); ZERO staged; ZERO commits since base |
| — | Process liveness | Get-Process | NO Entropia process; NO ghidra/analyzeHeadless process (consistent with STATIC_ONLY; QC also launched nothing) |

QC tool bugs found and fixed in-session (disclosed): qc1's first TLV walk ignored the
entry-count field and consumed the tail's low u16 as a phantom 7th entry (QC tool
defect — fixed in qc1 V2 and re-run; the executor's artifacts were never in question;
QC1's final results are from the corrected walk).

---

## 2. Findings

### **P2-1 — BLAST_RADIUS item 6 mis-verifies JOIN R1 claim 5's FUN_0070E810 attribution as PRIOR_CLAIMS_CONFIRMED, contradicting the package's own persisted evidence**

- SOURCE: `02_ANALYSIS\BLAST_RADIUS.md` item 6 (lines 56–63): "FUN_0070e810 builds
  `'<classID>.vfs'`-style names and opens via FUN_00972df0; … re-verified in-run
  (pins 0x70C40E, 0x70C742; FUN_00972df0 disasm). PRIOR_CLAIMS_CONFIRMED
  (independently re-verified in this binary, byte-pinned)"; mirrored by
  `06_REPORT\EVIDENCE_INDEX.md` §S8 row "Loader-chain VAs (JOIN R1 claim 5) …
  PRIOR_CLAIMS_CONFIRMED (re-verified in-run)".
- CONTRADICTED BY (in-package + QC physical evidence):
  1. The package's OWN dumps `01_RAW\GHIDRA_ROUTING\DECOMP_FUN_0070e810.txt` and
     `DISASM_FUN_0070e810.txt` show FUN_0070E810 = `FUN_00972df0(FUN_00401e70(
     FUN_00401fd0(dst, param_1, FUN_0070e470("textures")), ".vfs"), {1, 0x80, 8})`
     — a filename built from the **"textures"** literal + ".vfs", with NO itoa and
     NO class-ID immediate anywhere in the function.
  2. QC byte probe (QC4/QC4b): "textures" string @VA 0xA86858 (.rdata), referenced by
     `PUSH 0xA86858` @0x70E4AE inside FUN_0070e470, which FUN_0070E810 calls
     @0x70E866; `PUSH 0xA86820` (".vfs") @0x70E886; open `CALL 0x972DF0` @0x70E8B6.
     QC's independent call-edge census of FUN_0040e900 (the decimal int→string used
     by the real class-ID filename builder) found 5 sites — NONE inside FUN_0070e810.
  3. The pins cited as the "re-verification" (0x70C40E `PUSH ".vfs"`, 0x70C742
     `CALL FUN_00972df0`) belong to **FUN_0070c680**, not FUN_0070e810. The
     class-ID→"<classID>.vfs" mechanism exists and IS byte-pinned — in FUN_0070c680
     (pins 0x70C3FC/0x70C405/0x70C40E/0x70C742/0x70C71E, all QC-verified).
- FAILURE MECHANISM: the §15 comparison re-verified the MECHANISM in the correct
  function (FUN_0070c680) but stamped the PRIOR CLAIM's FUNCTION-LEVEL attribution
  (FUN_0070E810) CONFIRMED with mismatched evidence; the contradicting dump was
  already persisted in the package but not consulted for the filename construction.
- AFFECTED: BLAST_RADIUS item 6 verdict; EVIDENCE_INDEX §S8 row; the §15 record of
  JOIN R1 PE_MASTER_REVIEW claim 5. NOT affected: this run's primary chain (routing
  via FUN_0070c680 is fully byte-pinned and QC-reproduced; see §5).
- CORRECTION (for the final regeneration; not applied by QC — QC does not modify
  executor evidence): narrow item 6 to: "the class-ID→'<classID>.vfs' open mechanism
  is CONFIRMED in FUN_0070c680 (byte-pinned); JOIN R1 claim 5's attribution of that
  mechanism to FUN_0070E810 is CONTRADICTED at function level (FUN_0070E810 builds a
  'textures'+'.vfs' filename; DECOMP/DISASM_FUN_0070e810.txt + string 0xA86858);
  verdict: PRIOR_CLAIMS_NARROWED (mechanism confirmed, function attribution
  corrected), second lead-correction of the §B lead alongside the FUN_00959090
  correction." EVIDENCE_INDEX §S8 row must be updated accordingly.
- REVALIDATION PREDICATE (machine-checkable): bytes at 0x70E4AC == `68 58 68 A8 00`
  (PUSH 0xA86858); E8 rel32 at 0x70E866 targets 0x70E470; no E8 site of FUN_0040e900
  lies within [0x70E810, 0x70E928]; DECOMP_FUN_0070e810.txt contains "textures".
  (All four verified true by QC.)

### **P2-2 — EXECUTOR INCIDENT: forbidden-path write outside OUTPUT_ROOT (`__pycache__` inside the JOIN R1 package); self-repaired in-run; QC verifies the repair COMPLETE and the disclosure honest**

- EVENT (disclosed by executor at `06_REPORT\HANDOFF.md` process note 1): the first
  execution of `03_SCRIPTS\s3_crossval_vfs_common.py` imported JOIN R1's
  `04_TOOLS\vfs_common.py` without `sys.dont_write_bytecode`, causing CPython to
  create `docs\audits\PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928\04_TOOLS\__pycache__\vfs_common.cpython-312.pyc`
  — a write into a pre-existing READ-ONLY untracked group (contract §0: the 5 groups
  "must remain byte-identical").
- QC REPAIR VERIFICATION (duty 9): full recursive sweep of the JOIN R1 package:
  0 `*.pyc` files, 0 `__pycache__` directories, 228 files total (matches the
  executor's claim); latest write in the group = 2026-09-30 22:52:33 (predates the
  run); 10-file spot re-hash against JOIN R1's own `06_REPORT\MANIFEST_SHA256.csv`
  (incl. `04_TOOLS\vfs_common.py`, `06_REPORT\PE_MASTER_REVIEW.md`,
  `03_COUNTERCHECKS\AMEND_R2\AMEND_R2_ID2_MEMBERSHIP_20002_48.json`): 10/10 SHA+size
  MATCH. The patched script (`sys.dont_write_bytecode = True`, line 22) is present
  and was re-run without recreating the artifact (CROSSVALIDATION_vfs_common.json
  regenerated 2026-10-02T12:14:53Z — manifest-consistent).
- DISPOSITION: a real contract process violation (P2 by incident class:
  write outside OUTPUT_ROOT into a byte-identity-protected group), fully repaired,
  fully disclosed, no evidence damage, no impact on any claim. The disclosure is
  honest and complete (cause, artifact, repair, re-verification, prevention).
  Severity P2 stands in the QC record so the violation remains visible in the
  verdict trail; the repair is verified complete.

### **P3-1 — PASS15_GHIDRA_DUMP.json self-declares a non-existent generator script**

- SOURCE: `01_RAW\GHIDRA_ROUTING\PASS15_GHIDRA_DUMP.json` field `generator` =
  `03_SCRIPTS/s3_ghidra_routing_pass15.py`. No such file exists in `03_SCRIPTS`
  (inventory checked); the actual pass-15 Jython script is
  `03_SCRIPTS\s5_consumer_census_pass15.py` (read fully by QC).
- SKUTEK/EFFECT: provenance-label defect only (§17 "each artifact states its
  generator"); the census content itself is sound and was independently reproduced
  by QC (202/202; 2 candidates).
- CORRECTION: fix the `generator` field to `03_SCRIPTS/s5_consumer_census_pass15.py`
  in the final regeneration.
- REVALIDATION: `Test-Path 03_SCRIPTS\s3_ghidra_routing_pass15.py` == False;
  `Test-Path 03_SCRIPTS\s5_consumer_census_pass15.py` == True.

### **P3-2 — RELEVANT_XREFS.json self-declares a non-existent generator script**

- SOURCE: `01_RAW\RELEVANT_XREFS.json` field `generator` =
  `03_SCRIPTS/write_relevant_xrefs.py` — not present anywhere in the package (grep
  verified); the artifact is a manual consolidation of the PASS dumps (its own
  note says so, and `02_ANALYSIS\DESTINATION_CONSUMER_CENSUS.json` says
  "+ this consolidation").
- EFFECT: derived-number provenance chain (§17) references a non-persisted step.
  Load-bearing edges in the artifact were INDEPENDENTLY re-derived by QC's own
  call-edge census (all match: see QC4 row) — no content defect found.
- CORRECTION: replace the generator field with the true provenance ("manual
  consolidation of 01_RAW\GHIDRA_ROUTING\*_GHIDRA_DUMP.json, executor session") in
  the final regeneration.
- REVALIDATION: `Test-Path 03_SCRIPTS\write_relevant_xrefs.py` == False.

### **P3-3 — RECORD_FRAMING_SUMMARY.json aggregate census key `distinct_u16_at_payload_08` is mislabeled (contains u16@payload+04 values)**

- SOURCE: `03_SCRIPTS\s1_framing_census.py` lines 195/220: the set named
  `u8_vals` collects `row["u16_at_payload_04"]` (the record-id B component, values
  1..190) but is emitted under key `distinct_u16_at_payload_08` in
  `01_RAW\RECORD_FRAMING_SUMMARY.json`.
- EFFECT: the aggregate census does not actually aggregate the flags field; a
  reader of the summary alone would be misled about +0x08. The PER-ROW data
  (`RECORD_FRAMING.jsonl` `u16_at_payload_08` = 128 for all rows) is correct, and
  the REPORT claim "flags 0x80 … in 1,366/1,366 records" is TRUE — QC re-derived
  it from raw VFS bytes (QC1: `{0x80: 1366}`), so no claim is affected.
- CORRECTION: rename the key (e.g. `distinct_u16_at_payload_04`) and add a correct
  `distinct_u16_at_payload_08: {"0x80": 1366}` aggregate in the final regeneration.
- REVALIDATION: recompute the histogram from the raw VFS (QC1 result).

### **P3-4 — HANDOFF package file count is off by one**

- SOURCE: `06_REPORT\HANDOFF.md` line 26: "Package file count: 363 files (362
  covered by MANIFEST_SHA256.csv + the manifest itself …)".
- MEASURED (QC5): the manifest has 363 data rows; files outside `04_QC` = 364
  (363 manifest-covered + the manifest). The manifest itself is PERFECTLY consistent
  with disk (0 missing, 0 stale; 14/14 spot re-hash OK) — only the HANDOFF's two
  numbers (363/362) are off by one against its own manifest.
- CORRECTION: final regeneration should state 364 (363 covered + manifest).
- REVALIDATION: count manifest data rows (363) + 1.

### **P3-5 — s5_tlv_walk_census.py counter `tag11_value_matches_plus30_count` is tautological**

- SOURCE: `03_SCRIPTS\s5_tlv_walk_census.py` lines 132–135: inside the
  `if val_off == 0x30:` branch the comparison result is discarded (`pass`) and the
  counter increments unconditionally — and the compared value is read at the same
  offset the walk just verified, so the check could not fail by construction.
- EFFECT: the TLV_WALK_CENSUS.json field `tag11_value_matches_plus30_count` (1366)
  carries no information. NOT load-bearing: the real predicate
  `field_30_is_tag11_value_count` (tag-0x11 value offset == 0x30) is computed
  correctly, and QC1 re-derived it independently (1366/1366).
- CORRECTION: remove the tautological counter (or make it a genuine independent
  re-read comparison) in any future regeneration; harmless to the verdict now.

### Disclosed limitations (not defects; recorded for completeness)

- **L-1 (read-census detection window):** the "0 static tag-0x11 readers" census
  scans the 0x20 bytes of instructions preceding each of the 202 call sites
  (PASS15; getter contexts 0x18 bytes in PASS14) for an immediate 0x11. A tag
  immediate pushed further than 0x20 bytes before a call would escape detection.
  The search rule IS recorded, the census IS labeled bounded, and global
  exhaustiveness is explicitly UNVERIFIED (V2-012) — no overclaim. QC reproduced
  the 202-site denominator independently.
- **L-2 (routing path-prefix link):** the byte-pinned routing chain proves
  class-20002's class object opens `itoa(20002)+".vfs"` via FUN_0070c680→FUN_00972df0;
  the PATH PREFIX argument is runtime data (FUN_00703e80 passes caller-supplied
  paths; "Data\Parameters\" exists @0xA97E58 but is not byte-pinned in-run). The
  physical-file identity of the opened target rests on the byte-pinned filename
  construction + uniqueness (QC verified exactly one 20002.vfs exists in the entire
  pcg_install: `Data\Parameters\20002.vfs`) + the exact structural match of the
  parser's consumption profile (56-B payloads, ver=1, base=0x80, crc=0 gate,
  6-entry TLV + zero tail) with the pinned file. CONFIRMED remains defensible on this
  chain; QC records the unpinned path-prefix link as a residual that the final
  report could state explicitly.

---

## 3. Gate-strength audit (S0–S8 as implemented/emitted)

| GATE | PREDICATE AS EMITTED | QC ASSESSMENT |
|---|---|---|
| S0 INPUT_IDENTITY | exact HEAD + EXE size/SHA + VFS size/SHA match, fail-closed (00_CONTROL\PREFLIGHT.md) | STRONG, PASS. QC re-measured all four identities independently: all MATCH. No default-success path. |
| S1 RECORD_FRAMING | in-run walk byte 0→EXACT EOF; `stop_pos == file_size` AND `16+Σstrides == file_size` machine-checked; record count with derivation; anchored boundaries recorded; NC-FRAMING executed and falsifies | PASS. QC1 independently re-derived the walk (grammar incl. stride rule confirmed by exact-EOF; base read from the physical header field, matching the client's index-builder stride rule) and the invariants (stop 174864 == size; stride-sum check TRUE). Executor NC1–NC4 detected + NC5 honestly recorded non-discriminating; QC's own NCQ1b/c/d additionally falsify and NCQ1e shows no spurious failure. Any framing uncertainty: none found. |
| S2 FIELD_ANCHOR | per-record bounds assertions machine-checkable; RAW/width/endianness/value recorded with HYPOTHESIS_DERIVED vs RAW provenance; census denominator == N | PASS. FIELD_BYTE_ANCHOR.json carries the assertions (both anchors both-true; all_records_bounds_true) — QC re-verified bounds_ok 1366/1366 from raw bytes; anchors agree byte-for-byte incl. full payload hex; width/endianness upgraded to RAW_MEASUREMENT only after the client-read pin (V2-009 discipline followed; the census rows still carry the HYPOTHESIS_DERIVED label with the upgrade documented — acceptable). Defect P3-3 (mislabeled aggregate key) noted; no claim affected. |
| S3 ROUTING | §8 outputs present; CLIENT_READ allowed only if 20002_VFS_ROUTED_TO_GENERIC_PARSER ≥ PLAUSIBLE with byte-level routing evidence | PASS. GENERIC_PARSER_IDENTIFIED=YES (FUN_00726900 family, per-class descriptor schema via FUN_0070c180 — QC verified the lookup semantics from the in-package decomp + pins); routing = CONFIRMED on a byte-pinned, FILE-SPECIFIC chain (class-ID 20002 imm @0x73A441 → registry case @0x73C8C1 → itoa+".vfs" construction in FUN_0070c680 (pins 0x70C3FC/0x70C405/0x70C40E) → open @0x70C742 → per-record seek/read @0x971B14 → parse via FUN_00726900 @0x70DC53) — NOT a generic +0x30 hit; the §B trap (generic parser + a displacement coincidence) was avoided, and the §B lead's wrong parser family was corrected (see §5). QC independently reproduced every routing edge by call-edge census. Residual L-2 (path prefix) recorded. |
| S4 CLIENT_READ | every claimed instruction byte-pinned (bytes at FILE_OFFSET == recorded ORIGINAL_BYTES, machine-verifiable); full §9 chain fields; decompiler text never sufficient | PASS. QC2 re-read ALL 45 pins from the pinned EXE with its own VA→RVA→FO conversion: 45/45 match (0 mismatched); the two headline instructions' conversions verified explicitly; the read/store window hand-decoded (pure copy confirmed — no conditional consumes the value between load and store; the only branches test cursor flag/limit, and the error path stores 0, i.e. fail-closed, not value-conditional). All §9 keys present in FIELD_TO_DESTINATION_TRACE.md. |
| S5 CONSUMER_CENSUS | scopes/counts/unresolved-lists per §10; V2-012 exhaustiveness wording | PASS. Scopes recorded (write: FUN_0075f660 callers — QC census: exactly 1; read: 202 descriptor-lookup sites — QC census: exactly 202, reproducing the denominator independently; + getter/serialization families in PASS14). STATIC_WRITE_SITES_FOUND=1 consistent (single store @0x0041255A on the single dispatch path). "0 static tag-0x11 readers" is bounded-census-based with 2 candidate false-positives examined (parse-loop register tag; the 0x8AEAD5 state byte with actual tag 0x2/class 24017) — both verified in PASS15 contexts. Wording: ONLY_DIRECT_WRITER_FOUND / bounded read census / global UNVERIFIED — exactly as evidenced. Limitation L-1 recorded. |
| S6 MECHANISM_SEMANTICS | KEY_ROLE/LOOKUP_CONTAINER/RESULT_TYPE/RESULT_CONSUMER if a lookup; FIELD_IDENTITY vs OBSERVED_OPERATION vs FINAL_SEMANTIC_ROLE separated; §13 control if mechanism proposed | PASS. No lookup at the traced instructions — N/A documented with the measured precondition (QC hand-decode confirms: no map probe, no equality test, no branch on the value; the value flows load→store unmodified). The three axes are reported separately (FIELD_IDENTITY=CONFIRMED structural; OBSERVED_OPERATION=CONFIRMED pure copy; FINAL_SEMANTIC_ROLE=UNVERIFIED with bounded wording). §13 controls executed (see S-rows) with NC-VALUE N/A justified by §13's no-invention rule. |
| S7 WORDING_HONESTY | no §2-forbidden label without in-run byte proof; STATIC_ONLY; runtime NOT_TESTED; PRIOR_EVIDENCE labels; id2 CONTEXT ONLY; no significance/exhaustiveness overclaims | PASS. QC swept REPORT.md, HANDOFF.md, EVIDENCE_INDEX.md and all 02_ANALYSIS files: every occurrence of id2/template/model/resource/instance/coordinate/pointer/offset/foreign-key wording is either a meta-discussion of the forbidden-label discipline, an explicit denial, or PRIOR_EVIDENCE context — none is applied to the payload+0x30 value. STATIC_ONLY present (REPORT header + every 02_ANALYSIS header); RUNTIME=NOT_TESTED stated; the id2-domain observation cited as CONTEXT ONLY matching AMEND_R2's own no-significance framing (QC read the AMEND_R2 artifact: offset 48, 1364/1366, non-members 1014/1015 value 0, semantic_reference=UNVERIFIED — correctly quoted, nothing promoted). No exhaustiveness overclaim found. |
| S8 PACKAGE_COMPLIANCE | all §17 artifacts exist; REPORT carries all §18 fields; git delta == only the package + 5 byte-identical groups; HEAD unchanged; 0 commits; 0 staged; no client launch; manifest census documented | PASS WITH FINDINGS (P3-4 count off-by-one; P2-2 incident noted). All §17 artifacts exist (QC EVIDENCE_INDEX census: 20/20 cited artifacts on disk; all directories present). All §18 fields present key-by-key in REPORT.md (QC checked each against the contract list, incl. the FN-2 anchor-field resolution: singular keys = ANCHOR_PRIMARY, ANCHOR_ZERO in secondary keys — clearly labeled). Git at QC end: HEAD == origin/master == BASE_SHA; exactly 6 untracked groups; ZERO staged; ZERO commits. No Entropia.exe launch evidence anywhere in the package (all evidence static; no runtime-capture artifacts; no Entropia process alive at QC time). Manifest census documented (363 rows + self-exclusion + 04_QC exclusion; manifest↔disk perfect). |

---

## 4. Risk-probe results (dispatched probes)

### 4.1 tag→slot mapping ("slot 21"): BYTE-DERIVED, not label-derived
- Chain verified from bytes: descriptor registration `PUSH 0x11` @0x76171E (`6A 11`) →
  FUN_0070cbc0 computes field index = tag+4 via `ADD ECX,4` @0x70CBF6 (`83 C1 04`) —
  QC re-derived the argument position (arg1 = the tag: caller pushes 0xC0(arg3)/0x1(arg2)/0x11(arg1);
  after SUB ESP,0x10+PUSH ESI (+0x14) and one intervening push, `[ESP+0x1C]` == arg1) —
  stored into the descriptor object; parse side reads it via `MOV ECX,[EAX+8]` @0x726A0E and
  computes the destination via `LEA ECX,[EDX+ECX*4]` @0x726A14 from
  `MOV EDX,[EBP+0x40]` @0x726A11. Slot 21 == 0x15 == 0x11+4; +0x54 == 21×4.
  The 22-slot array size is byte-consistent: FUN_0070d990 allocates
  `((classObj[0x8C]-classObj[0x88])>>4)+4` u32s = 18+4 = 22 for the 18 descriptors
  (count 0x12 set by FUN_0070e2f0(0x12,0) in FUN_0073d1f0, verified in the in-package
  decomp); instance size 0x58 (operator_new(0x58) in FUN_0073a490, in-package decomp).
  All pins QC-verified (45/45).
- VERDICT: "slot 21" is byte-derived end-to-end.

### 4.2 "pure copy, no comparison/lookup" at 0x00412553/0x0041255A: CONFIRMED
- QC hand-decode of the 18-byte pinned window @0x412540 (PASS13_DISASM_FUN_00412540.txt
  + QC2 direct bytes):
  `80 79 11 00` CMP byte [ECX+0x11],0 / `74 23` JZ err / `8B 41 0C` MOV EAX,[ECX+0xC]
  (cursor.offset) / `8D 50 04` LEA EDX,[EAX+4] / `3B 51 08` CMP EDX,[ECX+8]
  (cursor.limit) / `77 18` JA err / `8B 11` MOV EDX,[ECX] (cursor.base) /
  `8B 04 10` THE READ / `8B 54 24 04` MOV EDX,[ESP+4] (dest ptr) / `89 02` THE STORE.
  Between load and store there is exactly one instruction and it loads the
  destination pointer. Every conditional in the window tests CURSOR STATE
  (flag/bounds), never the loaded value. The error path stores 0 (fail-closed
  default, value-independent). The TLV loop's neighboring checks (descriptor type
  @0x726A08, flags bit0 @0x75F687, mode-1 tail @0x726A87) are on schema/structure
  values, not on the +0x30 value. CONFIRMED — OBSERVED_OPERATION = pure copy stands.

### 4.3 ArkParameterArmor RTTI chain: BYTE-PROVEN (QC's own chain walk)
- vtable 0xA86FE0 → [-1] = COL 0xAA8B00 → COL+0xC = TD 0xB8DBC0 → TD+8 name =
  `.?AV?$ArkObjectClassImpl@VArkParameterArmor@@$0EOCC@@@` (class-object vtable;
  $0EOCC@ = 20002 by the MSVC nibble rule, calibrated in-binary by
  $0EOCG@ = 0x4E26 = 20006 = ArkParameterCommon — both strings found 2× by QC's own
  census at the executor's exact file offsets).
- instance vtable 0xA878BC → COL 0xAA9F18 → TD 0xB8EE20 → name = `.?AVArkParameterArmor@@`;
  slots [+0..+0x14] = [0x761510, 0x8E0010, 0x9154A0, 0x7263E0, 0x8E0110, 0x726340],
  matching the census; slot +0xC (the mode-1 nested reader) = FUN_007263e0 as claimed.
- imm32 0x4E22 census: 3 sites, identical offsets to the executor's (0x73819A,
  0x73A442, 0x73FBCC); the registration site 0x73A441 `PUSH 0x4E22` → FUN_0070cf80
  (classID → this[+8]) → filename via FUN_0070c680 — the class-ID ↔ file-name ↔ RTTI
  correlation is byte-consistent. VERDICT: class 20002 = ArkParameterArmor CONFIRMED
  at the RTTI/string level (independently).

### 4.4 EnvironmentZones attribution of FUN_00959090: EVIDENCE-BASED (QC-verified)
- Evidence basis (all independently reproduced by QC): the string "EnvironmentZones"
  @VA 0xA9808C (.rdata) with exactly ONE code reference in the whole .text —
  `PUSH 0xA9808C` @0x958DCE inside FUN_00958d90 (the string ctor, in-package decomp
  agrees); caller chain (QC call-edge census): FUN_0094e890 → (0x94EA9C) →
  FUN_0094e470 → (0x94E4D2) → FUN_0094e1d0 → (0x94E1FC/0x94E3B7) →
  FUN_0094dfc0/FUN_0094e390; FUN_0094dfc0 → (0x94E05A) → FUN_0094b9e0 → (0x94B9EF)
  → FUN_00958d90; the record loop FUN_0094bd30 → (0x94BDAD) → FUN_00959090; the array
  append FUN_0094d9b0 ← (0x94E2EB). RELEVANT_XREFS.json's edges match QC's census
  exactly.
- The family's cursor grammar (QC counted from the in-package dumps
  DECOMP_FUN_0094bd30.txt + DISASM_FUN_00959090.txt): FUN_0094bd30 reads 12 B
  (FUN_00412430) + 2×u32, FUN_00959090 reads 3×12 B + 7×4 B = 64 B →
  **84 cursor bytes total** — the executor's "84 cursor bytes" figure is
  byte-supported, and equals the EnvironmentZones.vfs payload size (84 B,
  per JOIN R1's T1 census), NOT 20002.vfs's 56 B. The incompatibility claim stands.

### 4.5 CRC-gate-skip: RE-DERIVED FROM QC's OWN WALK
- All 1,366 record crc fields == 0 (QC1 census, raw bytes). The gate instructions
  (`TEST EAX,EAX` @0x971B4A `85 C0`; `JZ +0x22` @0x971B4C `74 22`) are byte-pinned
  (QC2) — with crc==0 the comparison branch is skipped for every record of this
  file. CONFIRMED.

---

## 5. Canon-conflict description (JOIN R1 PE_MASTER_REVIEW claim 5) — described, NOT resolved by rewording history

JOIN R1 claim 5 (standing historical text, `06_REPORT\PE_MASTER_REVIEW.md` line 35,
advisory MASTER_ACCEPTED there): "The class-parameter file channel: FUN_0070E810
builds `<classID>.vfs` from a numeric class ID, opens via FUN_00972DF0 base=0x80,
cursor-parses {param_set_id, record_key, fixed fields} into 0x58-B array records via
FUN_0094D9B0 → CONFIRMED at code level (pins: C7 44 24 1C 80 00 @0x70E841;
'.vfs' @0xA86820; 83 42 04 58 @0x94D9F5)."

Physical facts (same pinned EXE in both runs; QC byte-verified):
1. **FUN_0070E810 is the textures-file opener**: it builds
   `param_1 + "textures" + ".vfs"` (string 0xA86858; concats 0x401FD0/0x401E70;
   open @0x70E8B6 with {1, 0x80, 8}). No itoa, no class-ID immediate. JOIN R1's OWN
   persisted decompilation (G1_DECOMP_0070e810.txt) says the same — the historical
   claim is contradicted by its own package's evidence and by this run's dump.
2. **The `<classID>.vfs` mechanism lives in FUN_0070c680**: MOV EAX,[ECX+8]
   (classID) @0x70C3FC → itoa FUN_0040e900 @0x70C405 → PUSH ".vfs" @0x70C40E →
   open @0x70C742 → reader at classObj+0x84 @0x70C71E (all QC-verified pins).
3. **The FUN_0094E1D0→FUN_0094BD30+FUN_00959090→FUN_0094D9B0 array family is the
   EnvironmentZones.vfs loader** (see §4.4): 84-byte cursor grammar == 84-B
   EnvironmentZones payloads; the 0x58-B array elements (operator_new(0x58) in
   FUN_0094e610; append pin @0x94D9F5 — real bytes, QC re-measured) belong to THIS
   family, not to the 20xxx parameter records.
4. **The 20002.vfs records** are parsed by the class-property TLV machinery
   (FUN_00726900 → FUN_0075f660 → FUN_004129c0 → FUN_00412540), into 0x58-B
   ArkParameterArmor INSTANCES (a size coincidence with the 0x58-B zone-array
   elements — different machinery, different provenance).

Therefore JOIN R1 claim 5 conflated three separate mechanisms under one chain
attribution. The current run CORRECTED part 3 (FUN_00959090 family → EnvironmentZones;
recorded as a lead correction — legitimate: the contract §B marked the lead
LEADS_TO_REVERIFY, NOT TRUTH, and no historical text was rewritten). The current run
did NOT correct parts 1–2 and instead stamped them "PRIOR_CLAIMS_CONFIRMED"
(BLAST_RADIUS item 6) — P2-1 above. QC reports the conflict precisely; per the
dispatch instruction, history is NOT reworded: any retraction/supersession edge
against the JOIN R1 package (a completed, accepted run) requires PE-MASTER's
separate disposition. The current run's PRIMARY chain is unaffected: 20002.vfs
routing runs through FUN_0070c680 (byte-pinned, QC-reproduced), not through
FUN_0070E810.

---

## 6. __pycache__ incident verification (duty 9)

See P2-2. Summary: forbidden-path write occurred (executor-disclosed); repair
VERIFIED COMPLETE by QC (0 .pyc / 0 __pycache__ dirs / 228 files / 10-10 SHA
spot-checks vs JOIN R1's own manifest / all mtimes predate the run); disclosure
HONEST (cause, artifact path, repair, re-verification, prevention patch all
recorded in HANDOFF.md process note 1). Recorded as a QC finding at P2 severity
because the violation class (write outside OUTPUT_ROOT into a byte-identity-protected
group) is material per contract §0/§5, even though fully repaired.

---

## 7. Taxonomy / status-algebra check

- RUN_STATUS = `CONSUMER_REACHED_ROLE_STRONGLY_SUPPORTED` — a §12 terminal value; the
  run maps it explicitly: the CONSUMER (the destination field: the instance's tag-0x11
  property slot) was REACHED with a byte-pinned end-to-end chain (routing CONFIRMED,
  read CONFIRMED, store CONFIRMED), and the ROLE ("record's tag-0x11 armor-parameter
  property copied into slot 21, exposed to the generic property machinery") is
  STRONGLY_SUPPORTED by RTTI + schema + parse evidence. The three claim axes are kept
  SEPARATE and not flattened: FIELD_IDENTITY = CONFIRMED (structural, byte-proven —
  QC re-verified the structural chain), OBSERVED_OPERATION = CONFIRMED (pure copy —
  QC hand-decode), FINAL_SEMANTIC_ROLE = UNVERIFIED (§3 baseline NOT lifted; bounded
  wording; no gameplay semantics claimed). The package explains exactly what was
  reached and what stays unverified (REPORT lines 80–81; SEMANTIC_ASSESSMENT §RUN_STATUS).
- WORLD_INSTANCE_TO_MODEL_EDGE = NOT_TESTED (per evidence — no edge claimed/tested) ✓;
  PLACEMENT_XYZ_RECOVERED = NO ✓; DOWNSTREAM_CONSUMER_IDENTIFIED = NO with the bounded
  census honestly separating "write path unique" from "read side runtime-tag-driven,
  global exhaustiveness UNVERIFIED" ✓.
- Claim statuses use only the §4 vocabulary; QC found no status inflation
  (no CONFIRMED without in-run byte evidence on the primary chain; the one
  mis-verification is the §15 prior-claim comparison, P2-1).
- INDEPENDENT_QC = QC_PENDING in REPORT.md as required (executor leaves it; this
  report is the QC round's output; the field is filled only in the final
  regeneration after PE-MASTER's verdict).

---

## 8. Coverage (QC reading/verification modes)

FULL READ (QC): RUN_CONTRACT.md (all 213 lines); 00_CONTROL\PREFLIGHT.md,
FORMALIZER_NOTES.md, CONTRACT_FREEZE.json; 06_REPORT\REPORT.md, HANDOFF.md,
EVIDENCE_INDEX.md; 01_RAW\CLIENT_READ_BYTES.json (all 45 pins), FIELD_BYTE_ANCHOR.json,
TLV_WALK_CENSUS.json, ROUTING_CENSUS_RAW.json, RELEVANT_XREFS.json,
CROSSVALIDATION_vfs_common.json; all 7 files of 02_ANALYSIS (VFS_TO_PARSER_TRACE.md,
FIELD_TO_DESTINATION_TRACE.md, CONSUMER_TRACE.md, NEGATIVE_CONTROLS.md,
SEMANTIC_ASSESSMENT.md, BLAST_RADIUS.md, DESTINATION_CONSUMER_CENSUS.json);
executor scripts s1_framing_census.py, s4_byte_pins.py, s5_tlv_walk_census.py,
s5_consumer_census_pass15.py, s3_exe_census.py, s3_crossval_vfs_common.py,
make_manifest.py, s3_ghidra_routing_pass14.py; Ghidra dumps (full):
PASS13_DISASM_FUN_00412540.txt, PASS13_DISASM_FUN_0070cbc0.txt,
PASS10_DISASM_FUN_00726900.txt, PASS10_DECOMP_FUN_0070d990.txt,
PASS12_DECOMP_FUN_004129c0.txt, PASS11_DECOMP_FUN_0070c180.txt,
PASS3_DECOMP_FUN_00958d90.txt, PASS2_DECOMP_FUN_0094e470.txt,
PASS3_DECOMP_FUN_0094e610.txt, PASS4_DECOMP_FUN_0073d1f0.txt,
PASS4_DECOMP_FUN_0070e470.txt, PASS4_DECOMP_FUN_0094b910.txt,
PASS3_DECOMP_FUN_00703e80.txt, DECOMP_FUN_0070e810.txt, DISASM_FUN_0070e810.txt,
DECOMP_FUN_0094bd30.txt, DISASM_FUN_00959090.txt, PASS5_DECOMP_FUN_00761540.txt,
PASS4_DECOMP_FUN_0073a490.txt; JOIN R1 (read-only): PE_MASTER_REVIEW.md (claim-matrix
region), G1_DECOMP_0070e810.txt, G2_FUN_00959090_DECOMP.txt,
AMEND_R2_ID2_MEMBERSHIP_20002_48.json.

PROGRAMMATIC FULL PARSE + RECOMPUTE (QC): RECORD_FRAMING.jsonl (all 1366 rows parsed
and compared field-by-field against QC's own walk); RECORD_FRAMING_SUMMARY.json (all
scalar/census fields extracted and re-derived from raw bytes); PASS15_GHIDRA_DUMP.json
(all 202 sites + both candidates); MANIFEST_SHA256.csv (all 363 rows; 14 spot
re-hashes SHA+size); JOIN R1 MANIFEST (10 spot re-hashes); EVIDENCE_INDEX (all 20
cited artifacts existence-checked).

SPOT: RECORD_FRAMING_SUMMARY.json's long sorted-values array (verified by independent
recomputation: 142 distinct, min/max) rather than row-by-row visual reading; PASS14
getter-family dump (conclusions re-derived via QC's independent call-edge census and
the pinned getter tags); the 202 PASS15 call-site contexts (only the 2 candidates
read; the count and candidate detection independently reproduced).

NOT_CHECKED (explicit; none load-bearing):
- 03_SCRIPTS drivers not read: s1_explore_framing.py, s1_explore_payloads.py,
  s3_ghidra_routing.py, s3_ghidra_routing_pass2..pass13.py, pass16.py (13 files).
  Justification: their outputs are the persisted dumps; every load-bearing number
  derived from those outputs was INDEPENDENTLY recomputed by QC from the pinned
  bytes (framing, pins, call edges, censuses), so no unchecked load-bearing
  component remains.
- 00_CONTROL\PREFLIGHT_EXPECTED.md, AUTHORIZATION_RECORD.md, SOURCE_IDENTITY.md
  (formalization-side controls; S0 identity was re-measured independently by QC and
  the gate does not depend on QC reading these transcriptions).
- PASS14_GHIDRA_DUMP.json full decompilation texts (see SPOT).
- The remaining ~180 PASS15 call-site contexts beyond the 2 candidates.
- templates.vfs id2-domain membership NOT re-scanned (the current run made no new
  membership claim — CONTEXT ONLY per S7; the raw basis (zeros at 1014/1015) was
  re-derived by QC).
- Runtime behavior: not tested by design (STATIC_ONLY); QC also launched nothing
  (no Entropia/ghidra processes at QC end; no runtime artifacts in the package).
- Remote git state: origin/master verified locally as HEAD (`git rev-parse
  origin/master`); no network fetch performed (not required by §8, which pins
  HEAD/local equality; no push/remote claims are made by this run).

UNCHECKED LOAD-BEARING COMPONENTS: NONE. (Per the coverage algebra: primary-chain
components = framing (FULL, recomputed), pins (FULL 45/45), routing edges (FULL,
census-reproduced), TLV grammar (FULL, recomputed), destination derivation (FULL,
byte-derived), RTTI (FULL, byte-proven), census denominators (FULL, reproduced),
wording (FULL sweep), manifest (FULL parse + 14 spot re-hashes), incident (FULL
sweep + 10 spot re-hashes).)

---

## 9. Verdict justification

- **P2-1** (BLAST_RADIUS item 6 mis-verification): material §15 defect — a prior
  claim's function-level attribution is stamped CONFIRMED on mismatched evidence
  while the package's own dump contradicts it; must be corrected in the final
  regeneration; primary chain unaffected.
- **P2-2** (__pycache__ incident): material process violation, fully repaired and
  honestly disclosed; repair verified complete; recorded so the violation remains
  visible; no claim impact.
- **P3-1/P3-2** (generator-name provenance defects): labeling only; content
  independently reproduced.
- **P3-3** (mislabeled aggregate census key): per-row data correct; claims
  unaffected; QC re-derived the true aggregate.
- **P3-4** (HANDOFF count off-by-one): transcription; manifest itself consistent.
- **P3-5** (tautological counter): non-load-bearing field; real predicate correct.

The primary result of the run — payload+0x30 of a 20002.vfs record is the tag-0x11
(4-byte, LE) property value of the record's 6-entry TLV block, read by the client at
VA 0x00412553 and stored (pure copy) into value-array slot 21 (tag+4) of the
ArkParameterArmor instance (class 20002, RTTI byte-proven), exposed to the generic
runtime-tag-driven property machinery with no static tag-0x11 reader in the bounded
202-site census — is INDEPENDENTLY REPRODUCED at every load-bearing link by this QC.
RUN_STATUS = CONSUMER_REACHED_ROLE_STRONGLY_SUPPORTED is supported; the semantic
axis correctly remains UNVERIFIED.

QC_VERDICT = **PASS_WITH_FINDINGS** (0×P0, 0×P1, 2×P2, 5×P3; findings P2-1 and
P3-1..P3-4 require corrections in the final regeneration; P2-2 is verified-repaired;
P3-5 cosmetic).

NEXT_PARENT_ACTION (advisory, for PE-MASTER): accept the primary trace; require the
final-regeneration corrections for P2-1 (BLAST_RADIUS item 6 + EVIDENCE_INDEX row
narrowing) and P3-1..P3-5 (labels/counters); record the JOIN R1 claim-5 canon
conflict (§5) for PE-MASTER's separate disposition regarding the historical package;
then the independent ChatGPT Desktop post-audit per contract §19.
