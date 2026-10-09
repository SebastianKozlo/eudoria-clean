# PREREGISTRATION — PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009

Written BEFORE the correction, per contract section 4/5/6 and the delegation order
("PREREGISTRATION.md: the correction plan, PRE design, POST control list C1-C6 and
falsifiers, established BEFORE the correction (write it first)").

## 0. Run identity

- RUN_ID = `PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009`
- RUN_CLASS = `MACHINERY_AND_CONTROL_CORRECTION` (correction-only; zero new science)
- CONTRACT = `C:\Users\User\Documents\ChatGPT\PE\PE_CMO_C1_HIGH_BYTE_CORRECTION_PROMPT_20261008\OPENCODE_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009.md`
  — 16623 B / SHA256 `61AAA55854942A22085F3767A7D64512248EDFAE3A7B9BB54A5CBE36F36D3981`
  — identity verified MATCH before any run work (executor phase, this run).
- EXPECTED_BASE_SHA = `34fc34749464de3e05527088ed46be9e215f1964` (git triple verified in preflight).
- SOURCE PACKAGE (READ-ONLY, immutable) = `docs/audits/PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009/`
- OUTPUT_ROOT = `docs/audits/PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009/` (absent at preflight; created only after preflight PASS).
- TARGET = `Entropia.exe` (PCG_9_3_5), 8015872 B / SHA256 `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31`
  (measured at preflight; will be rehashed after all EXE-touching work).
- EXE ACCESS POLICY: read-only; ONLY re-pinning of the existing approved windows
  (W1 [0x0085B1A8,0x0085B290), W2 [0x00746560,0x00856564)… precisely [0x00746560,0x00746564),
  W3 [0x00528E74,0x00528EA8), the two RTTI chains 0x00A7DCB0 / 0x00A91E4C). No new bodies.

## 1. The defect under correction (pre-registered hypothesis, from the contract)

Both historical x86-32 decoders of the source package mishandle register-direct
`MOV r/m8,r8` (opcode 0x88) byte-register ALIASES in the writes/reads sets: the
byte-alias index (R8/GPR8: al,cl,dl,bl,ah,ch,dh,bh) is used directly as the index
into the 32-bit register table (REGS/GPR: eax,ecx,edx,ebx,esp,ebp,esi,edi).

Pre-registered exact locations (line numbers per the measured source files):

- `03_SCRIPTS/repin_write_provenance.py` (executor decoder), the `elif b0 == 0x88:`
  branch: `ins["writes"].add(REGS[mr["rm"]])` and `ins["reads"].add(REGS[mr["reg"]])`
  (measured source lines 161-175; the writes line is 174, the reads line is 175).
- `03_SCRIPTS/qc_remeasure.py` (QC decoder), the `elif b0 == 0x88:` branch:
  `out["writes"].add(GPR[mr["rm"]] if mr["rm"] < 4 else GPR[mr["rm"]])` — a NO-OP
  conditional (both arms identical) — measured source lines 202-216 (writes at
  214-215); additionally the register-direct byte SOURCE is never added to reads
  at all (missing, not merely wrong).

Predicted concrete behavior for the contract's counterexample `88 DD`
(mod=11, reg=3 = BL source, rm=5 = CH destination):

- Historical executor decode: text `mov ch, bl` (dst/src STRINGS correct),
  `writes = {"ebp"}` (WRONG — REGS[5]=ebp instead of CH's parent ECX),
  `reads = {"ebx"}` (BL parent EBX — correct only BY COINCIDENCE of the low alias).
- Historical QC decode: dst `ch`, src `bl` strings, `writes = {"ebp"}` (WRONG),
  `reads = {}` (source parent missing entirely).
- Therefore the historical ECX-clobber scan over the reaching-definition interval
  (0x0085B24B,0x0085B27A) returns [] on the CH mutant — a FALSE EMPTY list — and any
  provenance gate built on it would FALSE-PASS (the component-level false PASS of
  finding CMO-C1).
- Predicted historical behavior for `88 D9` (CL, a LOW alias): writes
  `{"ecx"}` — correct BY COINCIDENCE — clobber DETECTED. This asymmetry (CL detected,
  CH missed) is the signature of the alias-index defect.
- Predicted blast radius (to be measured, PRE section 6): of the 64-case alias
  matrix, only destination aliases 0-3 have correct parents in the historical
  writes-sets; destinations 4-7 (AH,CH,DH,BH) map to esp,ebp,esi,edi (wrong);
  likewise for source aliases in the executor reads-set; the QC register-direct
  reads-set records no source parent in any of the 64 cases.

Why the defect was invisible in the historical run (pre-registered): the examined
224-byte window's only physical 0x88 instructions are the four memory-form
`88 9E 9C/9D/9E/9F 00 00 00` (`mov [esi+0x9c..0x9f], bl`) plus
`66 89 9E A0 00 00 00` (16-bit). Their byte source BL is a LOW alias whose parent
(EBX) coincides with REGS[3]; no high-byte alias and no register-direct 0x88 form
exists physically in the window, so the historical executor's writes/reads happened
to be correct for every physical instruction decoded. The defect is LATENT and is
exposed only by the synthetic high-byte counterexample (the Desktop post-audit's
finding, reproduced by this run's PRE).

## 2. PRE design (contract section 5; before the fix; immutable 00_PRE/)

Method: AST EXTRACTION of the historical implementations — the historical scripts
are NEVER executed at top level and NEVER imported as modules (their module-level
code performs sys.path insertion + an external import (executor) and full-EXE load +
package-wide file scans (QC main); their main() writes into the historical package,
which must not happen).

Extracted (by name, from the parsed AST; completeness verified against the
functions' free-name sets at run time):

- From `repin_write_provenance.py`: module constants REGS, R8, R16; class
  DecodeError; functions `_modrm`, `_fmt_mem`, `decode_instruction`,
  `linear_decode_window`, `hexs`.
- From `qc_remeasure.py`: module constants GPR, GPR8, GPR16; classes QcDecodeError,
  MyPE; functions `my_modrm`, `_mem_str`, `my_decode`, `linear_decode`, `hx`;
  PLUS the nested scan helper `writers_between` (AST-extracted from inside main()).
- The executor's historical ECX-clobber scan is an inline comprehension in main()
  (source lines 444-446: `[i["va"] for i in ins_list if 0x0085B24B < i["va"] <
  0x0085B27A and "ecx" in i["writes"]]`) — transcribed VERBATIM into the PRE driver
  with a programmatic byte-for-byte verification against those source lines,
  recorded in the PRE evidence.
- The QC's historical ECX scan call (source lines 508-509:
  `writers_between(0x0085B24B, 0x0085B27A - 1, "ecx")`) is likewise transcribed
  verbatim and programmatically verified against the source lines.

PRE cases (all on in-memory copies; the physical EXE file is never modified, never
rehashed as if it were the original):

| Case | Input | Decoder | Expected (falsifier) |
|---|---|---|---|
| PRE-EX-CLEAN | physical 224-B window [0x0085B1B0,0x0085B290) | historical executor | 64 insns, end 0x0085B290, D9 E8 @0x0085B24D, ECX scan [] (TRUE no-clobber) |
| PRE-QC-CLEAN | physical window (via AST-extracted MyPE over the in-memory EXE image) | historical QC | same |
| PRE-EX-CH | window copy, `88 DD` @0x0085B24D | historical executor | writes={"ebp"} (F-PRE-1), scan [] (F-PRE-2), 64 insns, end exact (F-PRE-7) |
| PRE-QC-CH | in-memory full-EXE copy mutated at the 0x0085B24D file offset | historical QC | writes={"ebp"}, reads={} (F-PRE-3), scan [] (F-PRE-4) |
| PRE-EX-CL | window copy, `88 D9` @0x0085B24D | historical executor | writes={"ecx"} (coincidence), scan DETECTED @0x0085B24D (F-PRE-6) |
| PRE-QC-CL | in-memory EXE copy, `88 D9` | historical QC | same |
| PRE-HIST-MATRIX | 64 synthetic `88 /r` mod=11 cases | BOTH historical decoders | blast-radius census: dest 4-7 parents wrong; executor src 4-7 parents wrong; QC register-form source parent absent in all 64 |

Falsifiers (a falsified expectation stops the correction as REQUIRE_CORRECTIONS
honesty, not as a pass):

- F-PRE-1/F-PRE-3: if a historical decoder reports the CH parent as ECX (correct),
  the CMO-C1 defect does NOT exist in that decoder and the correction for it is
  void — report honestly.
- F-PRE-2/F-PRE-4: if a historical ECX scan DETECTS the CH clobber, no false PASS
  exists — CMO-C1 is void for that decoder.
- F-PRE-5: if the physical clean window shows any ECX clobber in
  (0x0085B24B,0x0085B27A) or does not decode 64 insns to exactly 0x0085B290, the
  window identity premise fails — BLOCK.
- F-PRE-6: if `88 D9` is NOT detected as an ECX clobber by a historical decoder,
  the low-alias coincidence premise fails — investigate before correcting.
- F-PRE-7: if any mutant decode raises, or yields != 64 instructions, or does not
  end exactly at 0x0085B290, the length-preservation premise (2-byte mutation in a
  2-byte slot) fails — BLOCK.
- W1 byte-identity gate: this run's own physical W1 read must equal the committed
  W1 hex in the source CONTROL_RESULTS.json — else the EXE/window premise fails —
  BLOCK.

PRE outputs (immutable once written): `00_PRE/PRE_COUNTEREXAMPLES.json` (all cases,
inputs' identities, raw decode records at the mutation site, wrong writes/reads
values, scan lists, verbatim-transcription verification records) and
`00_PRE/PRE_SHA256_INDEX.csv`.

## 3. Correction plan (contract section 4)

Corrected successor: `03_SCRIPTS/corrected_executor_decoder.py` — successor of the
historical executor decoder (repin_write_provenance.py's x86_minidec_r1). Explicit
mapping recorded in the script header and in INPUT_IDENTITIES.md:

- OLD_EXECUTOR_SCRIPT = `docs/audits/PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009/03_SCRIPTS/repin_write_provenance.py` (34043 B / 45120C91AD6A94A79C56E9B06F1C035481FB99D3017688E7F589732BEC6EE931) — immutable, not edited.
- CORRECTED_EXECUTOR_SCRIPT = `03_SCRIPTS/corrected_executor_decoder.py` (this
  package; hash measured and recorded at POST run time).

Fix (opcode 0x88 only): the byte-alias parent map AL→EAX, CL→ECX, DL→EDX, BL→EBX,
AH→EAX, CH→ECX, DH→EDX, BH→EBX. Three properties distinguished per byte operand:
(1) exact byte-register operand name (dst/src strings, preserved unchanged);
(2) parent general-purpose register (writes/reads sets now carry the correct
parent for ALL EIGHT aliases, both destination and source, both register and
memory forms); (3) width/bit-range actually written or read (width=8; low aliases
[0,8), high aliases [8,16); a partial-byte write CLOBBERS the parent for
reaching-definition purposes but is NOT a full 32-bit overwrite — recorded
explicitly as partial-write bit ranges, never as a 32-bit overwrite).

Preserved unchanged: instruction lengths; ModRM/SIB interpretation; destination
and source strings; text rendering; all other supported opcode behavior
(0x50-0x57 push, 0x89 incl. 66-prefix 16-bit, 0x8B, 0x8D, 0x33, 0xC7, 0xD9, 0xE8);
fail-closed DecodeError on unsupported opcodes. The decoder stays a bounded
window decoder — NOT a general x86 emulator/disassembler. An unsupported
instruction in a required control produces a controlled failure result with
preserved evidence (demonstrated in POST AUX-1), never a silent acceptance.

NOT claimed by this correction: GENERAL_X86_DECODER_CORRECTNESS and
GENERAL_UNSUPPORTED_FORM_FAIL_CLOSED (both remain NOT_ESTABLISHED beyond the
window's opcode set and the 0x88 alias fix).

Successor scan + provenance machinery (same-lineage, corrected):

- `scan_writers_interval` — successor of the historical main() ECX-writers
  comprehension (lines 444-446), generalized to (reg, lo_excl, hi_excl) with the
  identical interval semantics `lo_excl < va < hi_excl`.
- `value_provenance_gate` — the SAME production provenance predicate for clean and
  mutant analyses: byte pins at 0x0085B1DA (8B 7C 24 14, EDI:=arg1),
  0x0085B24B (8B CF, ECX:=EDI), 0x0085B27A (E8 E1 B2 EE FF, call) with rel32
  recomputation to 0x00746560, accessor pin 8D 41 08 C3 @0x00746560,
  0x0085B27F (8B 08), 0x0085B281 (89 4E 44); EDI-writer scan (0x0085B1DA,0x0085B24B];
  ECX-writer scan (0x0085B24B,0x0085B27A); conclusion CORE_VALUE_SOURCE=[arg1+8] /
  COPY_FROM_MEMORY. The gate contains NO hard-coded mutant expectation: a mutant
  differing from clean ONLY in the two bytes at 0x0085B24D must fail the gate
  through the ECX reaching-definition scan alone (all pins, rel32 and accessor
  checks still passing) — that asymmetry is the proof the failure is causal.

## 4. POST control list (contract section 6) and falsifiers

Driver: `03_SCRIPTS/run_alias_controls.py` (python -B) → `00_POST/POST_COUNTEREXAMPLES.json`,
`00_POST/POST_SHA256_INDEX.csv`, `CONTROL_MATRIX.csv`, `REGRESSION_RESULTS.json`.

- C1 clean baseline (physical window): DECODE PASS; INSTRUCTION_COUNT=64;
  DECODE_END=0x0085B290; D9 E8 @0x0085B24D pinned; ECX_CLOBBER_AT_MUTATION_SITE=NO;
  provenance gate PASS; CORE_VALUE_SOURCE=[arg1+8].
  Falsifier: any of these failing on the physical bytes.
- C2 CH mutant (in-memory `88 DD` @0x0085B24D): DECODE PASS; 64 insns; end
  0x0085B290; OPERAND=CH; WRITES_PARENT=ECX; reads={EBX} (BL parent); bit ranges
  dst [8,16) src [0,8); width 8; CLOBBER_SCAN=DETECTED @0x0085B24D;
  VALUE_PROVENANCE_GATE=FAIL.
  Falsifier F-C2: the gate failure MUST be the broken ECX reaching-definition —
  if the gate instead fails via a changed SHA, missing file, mismatched pin or
  decoder exception, C2 FAILS (the failure-reason decomposition per check is
  recorded; every non-scan check must PASS on the mutant).
- C3 CL control (in-memory `88 D9`): ECX clobber detected @0x0085B24D; WRITES_PARENT
  = ECX; same provenance gate FAIL (same reason decomposition; F-C2 applies
  identically).
- C4 alias matrix: the COMPLETE 8x8 matrix for opcode 0x88, mod=11 — all eight
  register-direct byte DESTINATIONS x all eight byte SOURCES (AH/CH/DH/BH on both
  sides): 64 distinct 2-byte instruction cases (`88 C0|src<<3|dst`) per decoder,
  decoded under x86-32 rules and verified against an INDEPENDENT reference table
  written inside run_alias_controls.py that does NOT import the production
  decoder's mapping helper. Per case: exact destination operand; correct parent;
  writes-set == {parent}; width 8; NO false write to an unrelated parent; exact
  source operand; source parent; reads-set == {source parent}; bit ranges low
  [0,8) / high [8,16); length 2; partial-write clobbers-parent-but-not-full-32-bit
  distinction preserved. Units reported separately: 64 cases (executor
  implementation, this phase), 64 outcomes measured; the corrected QC
  implementation's 64 outcomes are the fresh-QC worker's phase
  (corrected_qc_decoder.py + QC_RESULTS.json — NOT part of this executor phase);
  the full 128-outcome two-implementation total completes in the QC phase.
  Destination coverage 8/8 and source coverage 8/8 (each alias exercised as
  destination AND as source; testing all destinations against only BL is
  insufficient and is not done).
  Falsifier: any of the 64 cases failing any per-case check.
- C5 unrelated-parent negatives (in-memory mutants at 0x0085B24D): `88 DF`
  (mov bh,bl) → EBX; `88 DC` (mov ah,bl) → EAX; `88 CE` (mov dh,cl) → EDX;
  `88 F7` (mov bh,bh) → EBX. Per case: writes-set == the correct parent (NOT
  EDI/ECX/ESP/EBP/ESI misattributions); ECX clobber scan must NOT report ECX
  modified; provenance gate must remain PASS (the pointer's required dependencies
  untouched; a byte READ of a parent, e.g. the CL source in 88 CE, is not a write
  and must not trigger the writer-scan).
  Falsifier: any negative case reporting ECX as modified, or attributing the write
  to a wrong parent.
- C6 historical scientific regression (physical EXE, read-only, no new bodies):
  store `89 4E 44` @0x0085B281; caller target 0x0085B1B0 (rel32 recompute from
  0x00528E8D); accessor target 0x00746560 (rel32 recompute from 0x0085B27A) +
  accessor bytes 8D 41 08 C3; MovableObject + ClientMovableObject RTTI identities
  (vtables 0x00A91E4C / 0x00A7DCB0, COL 0x00AB33D0 / 0x00AA17CC, TD 0x00B7997C /
  0x00B79958, names); clean 64-instruction decode + exact boundary 0x0085B290
  with the CORRECTED decoder; the full corrected instruction table equal to the
  historical executor table for ALL 64 instructions (va/len/bytes/text/writes/reads
  — the fix must be invisible on the physical window); original receiver chain
  (ESI:=this @0x0085B1B7, base vtable stamp @0x0085B1C1, ESI-writer scan empty)
  and value-source chain (EDI:=arg1 @0x0085B1DA, ECX:=EDI @0x0085B24B, ECX/EDI
  writer scans empty, CORE_VALUE_SOURCE=[arg1+8]); the relevant existing source
  pin sets within the approved windows re-verified (boundary C3+CC CC CC, entry,
  vtable stamps, zero-init triple, copy triple, caller pins — the sibling stores
  +0x48/+0x4C byte-pinned ONLY, NO analysis per section 9); the J3 statuses
  carried verbatim (documented, not re-derived).
  Core result must remain CORE_RECEIVER_VALUE_CHAIN = PRESERVED_CONFIRMED_STATIC_CONDITIONAL
  (no promotion beyond the original static scope).
  Falsifier: any pin mismatch, any instruction-table divergence, any gate flip on
  the clean physical bytes.
- AUX-1 (auxiliary, contract section 4's controlled-failure requirement): an
  unsupported opcode at the mutation site (in-memory `0F B0` @0x0085B24D) must
  produce a controlled DecodeError-based DECODE=UNSUPPORTED_FAIL_CLOSED record
  with preserved evidence (exception class + message + VA), never a silent
  acceptance. (Not a required C-control; demonstrates the fail-closed property.)

## 5. Scope boundaries (contract section 9 — hard)

```
NEW_PCG_FUNCTION_BODIES = 0
NEW_PCG_SCIENCE_EDGES = 0
NEW_FIELD_SEMANTIC_INTERPRETATIONS = 0
NEW_RUNTIME_WORK = 0
NEW_NETWORK_RE = 0
NEW_PLACEMENT_RE = 0
NEW_MODEL_RE = 0
NEW_GAMEBRYO_OPENMW_RESEARCH = 0
```

No upstream arg1 chain; no sibling-store analysis (+0x48/+0x4C byte pins only);
no world coordinates / position units / building identities / coordinate frames /
placement messages; no Gamebryo/OpenMW research. A negative QC result is not
permission to expand. The EXE is read only to re-pin existing approved windows.

## 6. Phase exclusions (delegation; not defects)

- `03_SCRIPTS/corrected_qc_decoder.py`, `QC_RESULTS.json`, `QC_REPORT.md` — the
  fresh-QC worker's own independent corrected implementation and records
  (NOT written in this executor phase).
- `PE_MASTER_REVIEW.md`, `FINAL_REPORT.md`, `EVIDENCE_INDEX.md`, `HANDOFF.md`,
  `MANIFEST_SHA256.csv` — parent phases.
- NO AUDIT_ENTRYPOINT.md writes; NO stage/commit/push in this phase (persistence
  is the parent's per the delegation).

## 7. Pre-registered evidence outputs (this executor phase)

```
PREREGISTRATION.md            (this file — written first)
INPUT_IDENTITIES.md           (preflight census, measured)
ROOT_CAUSE.md                 (exact locations + blast radius, PRE-measured)
00_PRE/PRE_COUNTEREXAMPLES.json
00_PRE/PRE_SHA256_INDEX.csv
03_SCRIPTS/run_pre_counterexamples.py
03_SCRIPTS/corrected_executor_decoder.py
03_SCRIPTS/run_alias_controls.py
00_POST/POST_COUNTEREXAMPLES.json
00_POST/POST_SHA256_INDEX.csv
CONTROL_MATRIX.csv
REGRESSION_RESULTS.json
SUPERSESSION_AND_STANDING.md
```

## 8. Acceptance gates (contract section 11 — restated; correction accepted ONLY if)

1. PRE reproduces the false PASS in BOTH old decoders (executor + QC).
2. POST correctly maps CH to ECX in the corrected executor decoder (the corrected
   QC decoder is the QC worker's gate).
3. POST reaches the actual clobber/provenance predicate (F-C2 decomposition).
4. Clean retains no CH-related false positive.
5. CL and the complete destination/source alias matrix pass their expected controls.
6. Unrelated-parent negatives pass.
7. Original client bytes and source chain remain unchanged (EXE rehash; source
   package files rehash; git tree clean outside OUTPUT_ROOT).
8. No new science interpretation is introduced.
9. The independent QC reproduces the decisive failure case (QC worker phase).
10. Documentation does not overclaim mutation coverage (DOC-2 wording honored).
11. Full manifest/allowed-paths/historical-immutability checks pass (parent phase;
    executor-phase self-checks recorded in the handoff census).

If any material correction gate fails: `CORRECTION_VERDICT = REQUIRE_CORRECTIONS`.
Corrected decoding alone is never sufficient.

**WORKS != UNDERSTOOD. STOP BEFORE SCOPE EXCEED. ONE CORRECTION RUN ONLY.**
