# GATE-C FINDINGS REVALIDATION REPORT — FINAL REPORT
# EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926

**RUN_ID**: EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926
**Executor**: pe-reconstruction (PE-MASTER-dispatched correction run; NO_NESTED_TASKS)
**RUN_CLASS**: LOAD_BEARING; **RUN_TYPE**: GATE_C_FINDINGS_CORRECTION_REVALIDATION
**Execution class**: STATIC-ONLY — the client never ran; zero GPU/physical-console
experiments; zero renders; no patching of any original binary; no new corpus.
**Repo**: D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean. PRE-PERSISTENCE: no
git add / commit / push / staging. HEAD at start == at end ==
`cc747dfbf75d3c89c80bd8cccd33d6546fbfa36d` (== origin/master == remote).
**Package**: docs/audits/EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926/

## 1. HUMAN DECISION BLOCK (what needs the human NOW)

1. Relay THIS package to ChatGPT Desktop for the SECOND Gate-C deep post-audit
   (GATE_C_STATUS = REQUIRES_INDEPENDENT_DESKTOP_REAUDIT; the first audit
   returned MILESTONE_POST_AUDIT_REJECTED with findings F01-F06 — this package
   is the bounded correction/revalidation).
2. Separately decide the PE-MASTER qualification Q1 (the committed
   PE_MASTER_QUALIFICATION_Q1.md remains ABSENT; canonical Gate-B authority is
   BLOCKED under the current POM §12 until the human executes/grades Q1 or
   amends the contract).
3. Nothing else is requested. This package issues NO MILESTONE_CLOSED, NO
   MILESTONE_POST_AUDIT_PASS, NO M2 authorization. Gate D = HUMAN_PENDING.

## 2. STATE DELTA (before -> after)

- BEFORE: the standing M1 package (EU935_M1_FULL_MILESTONE_AUDIT_R1_20260916 at
  cc747df) declared V4.1 reconciliation 19/19 with 0 contradictions, Gate A
  PASS, Gate B PASS (advisory), and carried the six Desktop-identified defects:
  the ZERO-PRIMARY premise (F01), the 492-census/decoder-coverage mislabel
  (F02), the NIF figures in terrain positions (F03), the merged "exhaustive"
  negative language (F04), the unconditional exactness wording + the shortened
  origin formula (F05), and the Gate-B advisory/canonical conflation (F06).
- AFTER: all six findings independently REPRODUCED from physical sources; the
  false premises RETRACTED (2 load-bearing correction edges NEW-F01/NEW-F02 +
  4 housekeeping edges NEW-P3A/P3B/P3C/P3D = 6 new edges total; NEW-P3C is a
  chronology-clarification edge, no claim retracted); the
  V4.1 delta re-dispositioned (19/19: 1 CONTRADICTION_FOUND at row 7; 2 CORRECTED;
  2 NARROWED; 14 UNCHANGED); the unresolved set re-dispositioned (39/39: 1
  STATUS_REVALIDATION at C7; 6 NEW_CORRECTION_EDGE; 32 NO_CHANGE); the two
  authorized source files corrected with a proven zero behavior change
  (src/pesource/VegetationClimateDecoder.js comment-only;
  src/peworld/PEFoliageCore.js comment lines + ONE documentation-metadata
  string (FOLIAGE_OPERAND_LOCK.exactness) — no executable change); the gates
  re-adjudicated: Gate A = REVALIDATION_REQUIRED (old PASS not
  inherited), GATE_B_SCIENTIFIC_PACKAGE_STATUS = REVALIDATION_REQUIRED,
  GATE_B_CANONICAL_AUTHORITY_STATUS = BLOCKED, Gate C =
  REQUIRES_INDEPENDENT_DESKTOP_REAUDIT, Gate D = HUMAN_PENDING.

## 3. WHAT THIS RUN DID (method)

Read Desktop's GATEC package as CLAIMS; re-derived every load-bearing number
from physical sources with THIS run's own probes (03_EVIDENCE/scripts/r1_*.mjs;
node v22.22.0 = the repo runtime) and a byte-proven re-run of the historical
python census generator (the verbatim copy SHA == historical
202FE509E097F12E074D54B3D4923B789C6CCB7C35E7A5A9E5AF2DE740E8911F; the executed
RUN copy differs ONLY in the OUT line; the historical output file verified
byte-identical before/after: A62D9473...). Re-hashed every pin
(00_CONTROL/BASELINE_PIN.md; all MATCH). Then adjudicated per the run contract.
Where this run's recomputation differs from Desktop, the difference is
reported, not forced (see §11 NOT_CHECKED + the trace total-row delta).

## 4. PER-FINDING VERDICTS (full records: 01_RAW/FINDINGS.csv; analyses: 02_ANALYSIS/F0*.md)

- **F01 PRIMARY_DEVICE — REPRODUCED.** DISPLAY_DEVICE_PRIMARY_DEVICE = 0x4
  confirmed from the LOCAL installed SDK wingdi.h (a stronger source class than
  Desktop's web citation; pinned SHA D3A5E8BF...); the historical `& 2` =
  MULTI_DRIVER. Recomputed from the raw StateFlags: DISPLAY1 0x04000005 =
  ATTACHED+PRIMARY+REMOTE -> PRIMARY=True **1/6, NOT zero** (old predicate 0/6);
  all six adapters REMOTE. Status before: the ZERO-PRIMARY premise standing in
  M1-CL-20/X87_RUNTIME_AUDIT/CLOSURE_GATE_MATRIX-Gate-A/entrypoint/N-3/N-13;
  after: RETRACTED (edge NEW-F01). Corrected x87 disposition (A-E): A. foliage-
  site CW = UNMEASURED (no contrary evidence: the 0x027F datum is the loader-
  phase Win32 default comparison value, not a site measurement); B. client exit
  -1 = CONFIRMED, independently re-derived from the existing ProcMon trace
  (1 PID 12976; 2,193 Entropia.exe rows; exactly ONE Process Exit "Exit Status:
  -1"; ZERO ddraw/d3d8/d3d9 Load Image rows; HardwareInformation.MemorySize =
  NAME NOT FOUND); C. display environment observed facts STAND; D. CAUSE CLASS:
  ENVIRONMENT_BLOCKED -> UNKNOWN (ordering is not causality; reserved DeviceKey
  is not malfunction evidence; EXACT_BOOT_REJECTION_PREDICATE = UNKNOWN); E. the
  AV/EAX debugger-artifact supersession PRESERVED (N-9/N-13).
- **F02 VCL CORPUS/DECODER — REPRODUCED.** 32 files / 492 nonempty TSV lines /
  5,916 whitespace tokens = **493 groups of 12** (492 fully numeric + the
  25.vcl comma group); 25.vcl group 9 = six comma tokens (first "0,2" @payload
  byte 447, col 1; offsets 447/451/455/470/475/481); the CURRENT canonical
  decoder over the ORIGINAL bytes: **31/32 files + 472 records + 25.vcl THROWS**
  (UNSUPPORTED_BY_CURRENT_DECODER); raw ids 256 -> decoder ids 246 (10 lost);
  the "29-token line" = TAB-split 29 fields vs whitespace 24 tokens = 2 records.
  The historical 492-chain defect demonstrated by the generator re-run:
  numeric_rows_12cols = 491 with the comma line SILENTLY skipped (float()
  ValueError, no error record) — "492" matches neither 493 (raw) nor 472+1
  (decoder). Status before: the comment claims standing; after: CONTRADICTION_
  FOUND at V4 row 7 (edge NEW-F02); the authorized comment corrections applied
  with a PROVEN ZERO behavior change (31/1/472 + the identical exception pre/
  post edit). Original-client locale/comma/failure semantics = UNVERIFIED (§6.4/
  §6.5 honored; no comma normalization; fail-closed preserved).
- **F03 TERRAIN vs NIF DENOMINATORS — REPRODUCED (mis-scope).** 24,474/24,508 =
  99.8613% traced to PE_M1_935_BINDING_CHAIN_REVALIDATION_R1 (eabf6cf): the K1
  ARKTEXTURE ID TABLE over 5,596 NIF models (mesh -> texturing-property slot ->
  ArkTexture; dangling 34); 80.40% = 19,705/24,508 own-file name-anchoring
  (PE_935_TEXANCHOR_CENSUS_R1, c380a26; OBSERVED class; CI [79.90,80.90]).
  Both = NIF/MODEL TEXTURE resource-binding domain — NOT terrain texels/
  layers/palette/selectors/masks/layout. Disposition: retained as a clearly-
  labeled NIF/MODEL TEXTURE CROSS-REFERENCE; removed from terrain-coverage
  positions; the height A/B separation (global RGB field model vs TDF u16)
  recorded with BRIDGE_STATUS = UNKNOWN. TERRAIN TEXTURE LAYOUT = NOT RECOVERED.
- **F04 NEGATIVE-SEARCH SCOPE — REPRODUCED.** Denominators re-derived and
  matched: Parameters 27; Textures 8,381 entries (0 hits); 26 local containers /
  179,774 entries / 70 size hits (= 69 compressed TDF + 1 NIF; the historical
  scripts' ACTUAL predicates re-read); the iter029 known-ID line = 178 scanned =
  89 BNT2 + 82 VFS + 7 ARK (429259 present in 4 containers; 432502/459344 = 0).
  SYNTHETIC DETECTOR CONTROLS: raw u8 4,225/16,641 B DETECTED; RGB 12,693/49,941
  B, RGBA 16,918/66,582 B and zlib 317/27 B all MISSED by both historical
  predicates (Desktop's expected fixture sizes re-derived exactly). Corrected
  language: index enumeration under explicit predicates = valid; arbitrary-
  encoding absence = NOT proven; omitted classes carry NOT_DETECTED_UNDER_
  THESE_PREDICATES + UNKNOWN. No unrestricted decompression campaign.
- **F05 EXACTNESS + ORIGIN PRECISION — REPRODUCED.** The unconditional
  BIT-EXACT wording corrected in-code (comment lines + ONE documentation-
  metadata string (FOLIAGE_OPERAND_LOCK.exactness) — no executable/behavior
  change) to the CONDITIONAL form (x87 PC in
  {53,64} + RC = nearest-even; PC=24 measured DIFFERENT 14,104/229,376 real +
  103,073/1,245,184 synthetic) with the FOUR-WAY separation: BYTE-LOCKED
  OPERANDS = CONFIRMED (the three QWORDs re-read from the EXE this run; SHA
  re-verified E7785430...); MODEL EXACTNESS = CONDITIONAL; ORIGINAL-CLIENT
  RUNTIME PARITY = UNVERIFIED/UNMEASURED; HISTORICAL INPUTS = NOT RECOVERED;
  PLACEMENT 1:1 = NOT CLAIMED. Origin precision control (W=5, S=0):
  f32(5*f32(0.01)) = 0.04999999701976776 (0x3d4ccccc) vs f32(5*0.01) =
  0.05000000074505806 (0x3d4ccccd) — DISTINCT; K = f32(0.01) WIDENED
  (0x3c23d70a), NOT binary64 0.01 (0x3F847AE147AE147B); the typed formula
  restored in the successor contract content. ORIGIN_PERMANENT_ZERO and
  unconditional W*0.01 NOT resurrected.
- **F06 GATE B AUTHORITY — REPRODUCED.** `PE_MASTER_QUALIFICATION_Q1.md` DOES
  NOT EXIST in the committed repo (git ls-files '*QUALIFICATION*' = 0; git log
  --all --diff-filter=A = empty; the only *QUALIF* artifact = the x87cw harness
  notepad qualification_notepad_v2 — a debugging context log). PE_MASTER_STATUS
  = PROVISIONAL_UNTIL_QUALIFIED (POM §12 re-read). THREE separate variables:
  SCIENTIFIC_PACKAGE_READINESS = REVALIDATION_REQUIRED; ADVISORY_PE_MASTER_
  DISPOSITION = MASTER_ACCEPTED (advisory) recorded with
  CANONICAL_GATE_EFFECT=NONE; CANONICAL_GATE_AUTHORITY_READINESS = BLOCKED. No
  Q1 self-award/execution; POM not modified; the relay not reinterpreted as
  qualification; governance deficiency did NOT trigger a science rerun.

## 5. CORRECTED / UNCHANGED CLAIM COUNTS

- Retracted/corrected carried claims: 2 load-bearing (the ZERO-PRIMARY premise;
  the 492-census/decoder-coverage comment chain) + 3 housekeeping corrected (the
  terrain.bnt fresh-pin history claim; the witness-matrix scope wording; the
  stale OPEN_LIMITS=16 summaries) + the PROGRESS_STATE phase-7 chronology
  clarification (NEW-P3C: preserved-as-checkpoint, not a retracted claim) + the
  downstream-contract §1/§5/§6 content (successor-corrected; the historical
  file untouched; not an edge). CLAIM count vs EDGE count kept explicit and
  separate: claims = 2 load-bearing corrected + 3 housekeeping corrected + 1
  chronology clarification; edges = 6 (NEW-F01, NEW-F02, NEW-P3A, NEW-P3B,
  NEW-P3C, NEW-P3D; 01_RAW/RETRACTION_SUPERSESSION_DELTA.csv = 9 PRIOR
  preserved + 6 NEW).
- Unchanged claim families (verified unaffected): the terrain height/grid/
  material/water chains; the foliage MECHANISM claims (loader/RTTI; spawn-loop;
  RNG identity — the demo consumes the fully-numeric 0.vcl, byte-unchanged);
  the BYTE-LOCKED operands + the six rounding points (re-read from the binary
  this run); the PC24 sensitivity counts; the 463,141 cross-validation; all
  measured negative counts; the witness/falsification + georef queue verdicts;
  the retraction canon (9 prior edges preserved verbatim).

## 6. V4.1 DELTA SUMMARY (19/19; see 01_RAW/V4_1_DELTA.csv)

14 UNCHANGED + 2 NARROWED (rows 5, 19) + 2 CORRECTED (rows 9, 18) +
1 CONTRADICTION_FOUND (row 7). The 3 prior SUPERSEDED_WITH_VALID_EDGE
relationships (rows 3, 8, 14) all stand. **19/19 PRESENT is NOT 19/19
SCIENTIFICALLY ACCEPTED** — both quantities recorded: 19/19 present; 18/19
accepted-as-standing after correction; 1/19 (row 7) carries the contradiction on
its census chain (its loader/RTTI/source-graph claims remain CONFIRMED).

## 7. UNRESOLVED DELTA SUMMARY (39/39; see 01_RAW/UNRESOLVED_DELTA.csv)

32 NO_CHANGE + 6 NEW_CORRECTION_EDGE (A3/A4/A18/B4/C4/C5 — the F04
negative-language narrowing) + 1 STATUS_REVALIDATION (C7 — the x87 item: the
honest BLOCKED-UNKNOWN survives but its supporting record must be rebuilt on
true premises). F01/F02 are NOT hidden as ordinary inherited unknowns — they
remain separately visible as contradictions/corrections in FINDINGS.csv and
RETRACTION_SUPERSESSION_DELTA.csv.

## 8. CURRENT STATUS LINES (the corrected standing state)

- **x87**: A. FOLIAGE-SITE CW = UNMEASURED; B. CLIENT EXIT -1 = CONFIRMED
  (re-derived from the trace); C. DISPLAY OBSERVED FACTS = STAND (all-remote;
  1/6 primary; MemorySize NAME NOT FOUND); D. CAUSE CLASS = UNKNOWN
  (EXACT_BOOT_REJECTION_PREDICATE = UNKNOWN); E. AV/EAX supersession preserved.
  The CONDITIONAL arithmetic model + PC24 sensitivity unchanged.
- **VCL coverage**: raw corpus = 493 whitespace groups of 12 (492 numeric + 1
  comma group); current decoder = 31/32 files / 472 records / 25.vcl =
  UNSUPPORTED_BY_CURRENT_DECODER; original-client semantics for 25.vcl =
  UNVERIFIED; no parser behavior change.
- **Terrain texture**: the NIF figures re-labeled cross-reference; terrain
  texture layout NOT recovered; palette/details/masks/blend chains unchanged;
  432502/459344 MISSING (patcher-delivered) with the F04-scoped negative.
- **Cellstream/climate**: honest BLOCKED-UNKNOWN on the corrected basis —
  index enumeration under explicit predicates = YES (27/8,381/26/179,774/178);
  arbitrary-encoding detection = NO.
- **Origin/georef**: out[i] = f32(f32(W[i] * (double)(float)0.01) - S[i]);
  INITIAL S=0 evidence-backed; MUTATION_CHANNEL_EXISTS evidence-backed;
  SETTER_EXISTS evidence-backed; ACTUAL NONZERO MUTATION IN A HISTORICAL
  SESSION = UNVERIFIED; engine-side keying BLOCKED-UNKNOWN (unchanged).

## 9. GATES (see 01_RAW/GATE_REVALIDATION.csv; PE-MASTER final-adjudicates)

- GATE_A_STATUS = **REVALIDATION_REQUIRED** (the old PASS is not inherited: the
  x87 P0's supporting record contained the false ZERO-PRIMARY premise; the
  corrected-evidence rebuild is prepared by this package and must be
  post-audited before PASS can be re-awarded — the literal POM permits an
  honest BLOCKED-UNKNOWN without measuring CW, so Gate A remains REACHABLE).
- GATE_B_SCIENTIFIC_PACKAGE_STATUS = **REVALIDATION_REQUIRED**;
  GATE_B_CANONICAL_AUTHORITY_STATUS = **BLOCKED** (Q1 absent; two separate
  variables; the advisory MASTER_ACCEPTED recorded separately with
  CANONICAL_GATE_EFFECT=NONE).
- GATE_C_STATUS = **REQUIRES_INDEPENDENT_DESKTOP_REAUDIT** (this run cannot
  award Gate C to its own correction).
- GATE_D_STATUS = **HUMAN_PENDING**.

## 10. MODIFICATION CONTROL (the §9 record)

- BASE_SHA = CURRENT_HEAD = cc747dfbf75d3c89c80bd8cccd33d6546fbfa36d (no
  commits; verified at run end).
- TRACKED_DIFF_PATHS = exactly: AUDIT_ENTRYPOINT.md (+1/-0: one new row, all
  existing rows byte-preserved), src/peworld/PEFoliageCore.js (comment-only
  (PEFoliageCore.js additionally: the one exactness metadata string — no
  executable change)), src/pesource/VegetationClimateDecoder.js
  (comment-only). Byte-exact diffs:
  03_EVIDENCE/DIFF_*.patch + 01_RAW/MODIFIED_PATHS.csv.
- UNTRACKED_PATHS = this package + the 2 pre-existing roots (unchanged).
- AUTHORIZED_CHANGED_PATHS = the 3 tracked paths above; UNAUTHORIZED_CHANGED_
  PATHS = **0** (verified). PARSER_BEHAVIOR_CHANGE_WITH_HISTORICAL_PROOF = 0
  occurrences. Historical packages and raw evidence untouched (the historical
  iter032_vcl_columns.json SHA verified identical before/after the re-run).

## 11. NOT_CHECKED (honest limits)

- No Ghidra re-verification of the FUN_0083a7d0 decompile (the iter032 evidence
  cited as standing; no new RE authorized).
- The ProcMon CSV total-row delta vs the historical quote is ROOT-CAUSED
  (AMEND_R1, 03_EVIDENCE/F01_TRACE_LINECOUNT_ERRATUM.json): 282,192 = the
  CR-sensitive count of this run's original F01 line reader (282,060
  LF-terminated lines + 133 embedded lone CR bytes inside quoted Detail fields
  = 282,193 counted lines -> 282,192 "data rows"); 282,059 = the CORRECT LF
  data-row count — the historical quote in N-2 STANDS. Byte census re-derived
  independently: LF = 282,060, lone CR = 133 (both MATCH PE-MASTER's
  independent counts); a quote-aware RFC4180 parse returns 282,059 data rows;
  the per-client load-bearing facts all reproduce exactly and are unaffected.
- The 200xx.vfs interiors beyond the size census remain NOT_CHECKED (the
  historical run's own bound).
- live_test_record.json records pid=10824 while the trace's only client PID is
  12976 — a historical-package provenance inconsistency, recorded (not
  load-bearing for the exit fact).
- The R61 frozen parser, the 838-function consumer census, the 463,141 platform
  trials and the historical renderer runs were NOT re-executed (their sources
  read + pins verified; not within the bounded reproduction scope).

## 11.5 INTERNAL_QC (fresh-context pe-master-auditor, READ-ONLY)

QC_PASS_WITH_FINDINGS — 0×P0/P1/P2, 7×P3 (all confirmed by PE-MASTER and fixed
by AMEND_R1; the correction list in 00_CONTROL/AMEND_LOG_R1.md).

MANIFEST: 48 rows / 49 package files / self_excluded=YES / missing=0 / stale=0
(re-hashed after AMEND_R1/R2/R3; PE-MASTER re-verification pending its final audit).

## 12. HANDOFF

See 06_REPORT/HANDOFF_TO_DESKTOP_REAUDIT.md. RUN_STATUS = COMPLETE.
HARD_STOP: no next-milestone work, no Viewer, no M2 — the next step is the
independent Desktop re-audit, then the human's closure decision (Gate D).
