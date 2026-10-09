# FINAL REPORT — PE_935_TEMPLATE_4057_CONSUMER_CHAIN_R1_20261009

- **RUN_CLASS**: BOUNDED_STATIC_CONSUMER_CENSUS
- **RECORDS**: **STATIC_ONLY — the client never ran in this run.** No runtime,
  no dynamic instrumentation, no network. Every finding below is labeled with its
  evidence maturity level (IDENTITY / BYTE_OBSERVATION / STRUCTURE / RELATION).
  No MECHANISM and no RUNTIME claims are made.
- **Era / binary**: PCG/EU 9.3.5 client, `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe`
  (8,015,872 B). SHA256 measured before AND after all work:
  `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31` — identical to
  the expected value. Image base 0x00400000, no ASLR. All addresses below are VAs.
- **Tooling**: Ghidra 11.2.1 PUBLIC headless, REUSED project `LANDMARK4057`
  (`99_Audits\PE_935_LANDMARK4057_GHIDRA_SCRATCH_20261003\proj`, disclosed in
  PREREGISTRATION.md §6; its imported sandbox EXE re-hashed this run = expected
  SHA256; auto-analysis from the prior run, `-noanalysis`). Census cross-checked
  by an independent disassembler-free raw-byte scan (own PE mapper, calibrated on
  two canon byte anchors). Scripts + hashes: see EVIDENCE_INDEX.md.
- **Human authorization**: "kontynuuj szukanie budynków i ich lokalizacji" (2026-10-09).

## 1. Subject re-pins (prior labels re-verified at exact VAs — never inherited)

| Subject | VA | Re-pin result (evidence) |
|---|---|---|
| FUN_0043A550 | 0x0043A550 | **IDENTITY + STRUCTURE**: singleton getter, 119 B. Reads `DAT_00BA1824` (`A1 24 18 BA 00` @0x0043A571); if 0 → `operator_new(0x18)` via FUN_0095d3c4 @0x0043A57C (body CLOSED), constructor FUN_0052a260 @0x0043A596 (body CLOSED), store `A3 24 18 BA 00` @0x0043A59B; failure path stores 0 @0x0043A5B2. Success and already-exists paths RET with EAX = the singleton; the alloc-failure path stores 0 and RETs with EAX = 0 (NULL). |
| FUN_0072F580 | 0x0072F580 | **IDENTITY + STRUCTURE**: registry lookup, 46 B, `__thiscall(this = 0x18-byte map object, 1 stack dword key)`. Calls FUN_004d1430(this,&out,&key) @0x0072F590 (prior-canon generic STL RB-tree mapfind; body NOT re-decoded). Found → returns `node+0x14` (`83 C0 14` @0x0072F59E) = the map value of an (int-key, value) pair. Not-found (out == this) → returns fixed `.data` sentinel pointer 0x00BA5800 (`B8 00 58 BA 00` @0x0072F5A5). |
| DAT_00BA1824 | 0x00BA1824 | **IDENTITY + BYTE_OBSERVATION**: Ghidra symbol `DAT_00ba1824`, undefined4, value 0x0, located in the zero-initialized `.data` tail (no file bytes; BSS-like). ALL references in the binary: exactly 3, all inside FUN_0043A550 (1 READ @0x0043A571, 2 WRITE @0x0043A59B/0x0043A5B2). Dual-method agreement (raw absolute scan 3 operand hits ↔ Ghidra 3 instruction refs). The prior "registry tree referenced only inside the getter" statement is CONFIRMED by this run's own measurements. |

Note: FUN_0072F580 does NOT call FUN_0043A550 itself. The consumer chain is a
**pair pattern**: every measured caller calls the getter first, then passes the
returned singleton as `this` to the lookup (see §3).

## 2. Reference census (per class, both functions — G1)

All classes enumerated with method + result. Machine-readable form with full
method statements: `CALLER_CENSUS.json → targets → reference_classes`; agreement
raw data: `01_RAW\CENSUS_AGREEMENT.json`.

| Class | FUN_0072F580 | FUN_0043A550 | Method |
|---|---|---|---|
| C1 direct CALL rel32 | **25 callsites / 23 unique callers** | **35 callsites / 32 unique callers** | dual: Ghidra `getReferencesTo` isCall-filtered AND raw E8 rel32 scan of .text; **VA sets identical, 0 disagreements**; every raw candidate is a defined Ghidra instruction |
| C2 tail call / thunk JMP rel32 | 0 | 0 | raw E9 rel32 scan of the whole .text raw range |
| C3 indirect / computed calls | 0 static paths | 0 static paths | Ghidra computed-flags (none) + whole-file absolute VA scan (0 hits) → no immediate-carrying path exists; register/computed-only targeting is statically non-enumerable (NOT_CHECKED, reason recorded) |
| C4 address-taken refs | 0 | 0 | raw 4-byte LE scan of the ENTIRE file (all sections incl. .tls, .rsrc) |
| C5 data references | 0 (Ghidra non-call refs = 0) | 0 | C4 subset + Ghidra non-call refs |
| C6 vtable slots | 0 | 0 | C4/C5 .rdata pointer-run heuristic (no hits at all to apply it to) |
| C7 callbacks (incl. .tls) | 0 | 0 | whole-file absolute scan covers .tls callback table |
| C8 thunks | 0 | 0 | covered by C2 |
| C9 jump tables | 0 | 0 | x86 jump tables store absolute code VAs; the absolute scan would find any |
| C10 other Ghidra ref types | none (all refs are `UNCONDITIONAL_CALL`) | none (same) | exhaustive verbatim dump in `01_RAW\C2_SUBJECT_REPINS.json` |

**Static reachability statement (STRUCTURE, bounded)**: within what static
analysis can see, both functions are reachable ONLY by direct CALL rel32 from
defined code. NO_DIRECT_XREF != DEAD_CODE is respected (QH-007): absence of
indirect classes is a measured census fact here, not a liveness claim.

## 3. Direct-caller census and in-budget windows (G2)

Budget: MAX 12 windows (pre-registered priority: FUN_0072F580 callers first).
The 12 windows were exactly the first 12 FUN_0072F580 callers in reference order
(all 12 also call the getter — pair pattern). Remaining 20 unique caller
functions (11 further lookup callers + 9 getter-only callers) are recorded as
**IDENTIFIED_NOT_ANALYZED** with their callsite VAs in `CALLER_CENSUS.json`.
No window was truncated (all ≤ 64 KB cap); every window's body-end rule was
verified (last instruction RET-class; next bytes = following function's
prologue; evidence in each window file's `body_end_context`).

| # | Caller | Window bounds | id-source class (feeding FUN_0072F580) | Returned-object role class |
|---|---|---|---|---|
| 1 | FUN_00511070 | 0x00511070–0x0051152B (1212 B) | IMMEDIATE_CONSTANT_BRANCH_SELECTED: 0x2DFA@0x0051121C / 0x2DF9@0x00511245, PUSH@0x0051124A | FORWARDED_TO_CALL: template→ECX→FUN_007ce1e0 @0x00511259 (body CLOSED) |
| 2 | FUN_006baa20 | 0x006BAA20–0x006BAC1A (507 B) | OBJECT_FIRST_FIELD_READ @0x006BAB25 (`8B 38`) — provenance LEAVES WINDOW (UNKNOWN, not guessed) | VALIDITY_CHECK_THEN_STORED_TO_FIELD: FUN_0072fce0 @0x006BAB4F (body CLOSED); template stored at this+0xC @0x006BAB60 (`89 7E 0C`) |
| 3 | FUN_00733490 | 0x00733490–0x00733565 (214 B) | FUNCTION_RETURN_VALUE: FUN_007376a0 @0x0073350A — provenance LEAVES WINDOW (UNKNOWN) | VALIDITY_CHECK_THEN_STORED_TO_FIELD: FUN_0072fce0 @0x00733520; template stored into 3×0x18-byte record slots @0x00733529 (`89 37`), loop @0x00733542 |
| 4 | FUN_006c26b0 | 0x006C26B0–0x006C26FA (75 B) | STATIC_RDATA_TABLE: id = dword[0x00A85608 + (A+34B)*4] @0x006C26DC | FORWARDED_AS_RETURN_VALUE (RET @0x006C26F2; out-of-range → same sentinel 0x00BA5800) |
| 5 | FUN_006c2700 | 0x006C2700–0x006C2745 (70 B) | STATIC_RDATA_TABLE: dword[0x00A855D0 + (16B+A)*4] @0x006C2727 | FORWARDED_AS_RETURN_VALUE |
| 6 | FUN_006c2750 | 0x006C2750–0x006C2796 (71 B) | STATIC_RDATA_TABLE: dword[0x00A85778 + (A+10B)*4] @0x006C2778 | FORWARDED_AS_RETURN_VALUE |
| 7 | FUN_006c27a0 | 0x006C27A0–0x006C27E6 (71 B) | STATIC_RDATA_TABLE: dword[0x00A857C8 + (A+10B)*4] @0x006C27C8 (field +0xE variant) | FORWARDED_AS_RETURN_VALUE |
| 8 | FUN_006c27f0 | 0x006C27F0–0x006C2839 (74 B) | STATIC_RDATA_TABLE: dword[0x00A85804 + (15B+A)*4] @0x006C281B | FORWARDED_AS_RETURN_VALUE |
| 9 | FUN_006c3f50 | 0x006C3F50–0x006C3FDB (140 B) | CALLER_SUPPLIED_STACK_ARG @0x006C3F53 (`8B 44 24 0C`) — provenance LEAVES WINDOW (UNKNOWN) | FORWARDED_TO_CALL_MULTIPLE: FUN_007ce1e0(0x66) @0x006C3F74, FUN_0040b070(0x8BD720) @0x006C3FB5 (bodies CLOSED); pair (0x66, result) appended to a vector arg |
| 10 | FUN_00567170 | 0x00567170–0x0056775E (1519 B) | IMMEDIATE_CONSTANT_BRANCH_SELECTED: 0x3BDA@0x00567338 (+0x3BDB/0x3BD9/0x3A47/0x3A40 on other branch paths), PUSH@0x00567365 | FORWARDED_TO_CALL: template→FUN_005670a0 @0x0056737A (body CLOSED). Window contains float ops (e.g. FLD [0x00a7d688] @0x00567324) but NONE target the template. |
| 11 | FUN_006c2840 | 0x006C2840–0x006C2864 (37 B) | STATIC_RDATA_TABLE: dword[0x00A858B4 + B*4] @0x006C284F | FORWARDED_AS_RETURN_VALUE |
| 12 | FUN_006c2870 | 0x006C2870–0x006C2894 (37 B) | STATIC_RDATA_TABLE: dword[0x00A858BC + B*4] @0x006C287F | FORWARDED_AS_RETURN_VALUE |

Index inputs for the accessor family (BYTE_OBSERVATION): A = `MOVSX` s16 field
(+0xC or +0xE) of `FUN_0070ed80(imm)`'s return (imm = 3/4/0x1F/0x20 per accessor),
B = `FUN_006b22d0(this)`; A is bounds-checked (< 34/16/10/10/15) before the
table read. All in-window callee bodies stayed CLOSED this run — only call
edges were recorded; the 12 windows contain 92 distinct non-subject call
targets and none was opened. The classification-relevant callee names
(FUN_0070ed80, FUN_006b22d0, FUN_006c2e00, FUN_006c3640, FUN_00703b80,
FUN_00728150, FUN_007376a0, FUN_004926e0, FUN_00977780, FUN_0072fce0,
FUN_007ce1e0, FUN_0040b070, FUN_005670a0, FUN_0052a260, FUN_0095d3c4,
FUN_004d1430) are the 16 cited across the classifications (14 of them among
the 92 in-window targets; FUN_0052a260 and FUN_004d1430 are callee edges of
the census subjects' own bodies — §1). `01_RAW\ID_TABLE_DUMPS.json` holds the measured table
dwords (id-ranged small integers, e.g. 11602, 15591, 16104; **no 4057**).

## 4. Answers to the two P0 sub-questions

### (a) Can any caller path carry a template id from a persisted/static source into the lookup?
**YES — STATIC_ONLY, BYTE_OBSERVATION.** 9 of 12 in-budget windows carry the
lookup key from static/persisted-in-binary sources:
- 7 windows (accessor family): ids read from `.rdata` id tables (0x00A855D0,
  0x00A85608, 0x00A85778, 0x00A857C8, 0x00A85804, 0x00A858B4, 0x00A858BC),
  indexed by runtime object state (s16 field + row index), bounds-checked,
  then pushed directly as the lookup key.
- 2 windows: branch-selected immediate constants (0x2DF9/0x2DFA in FUN_00511070;
  0x3BDB/0x3BD9/0x3BDA/0x3A40/0x3A47 in FUN_00567170).
- 3 windows carry ids whose provenance LEAVES the declared window and is
  explicitly marked UNKNOWN (caller-supplied stack arg; function-return id;
  object-first-field id) — never guessed.
- **No measured in-window id equals 4057 (0xFD9).** The registry POPULATION path
  (who inserts ids into DAT_00BA1824's map — prior canon: templates.vfs reader
  cluster) was NOT investigated this run (out of scope).

### (b) Does any caller read, write or forward a transform/position/placement-relevant field of an object derived from the returned template?
**NO transform-relevant access ESTABLISHED on the returned template object —
within the 12 in-budget windows (STATIC_ONLY); one read pattern on an
UNKNOWN-identity derived object recorded.** Zero direct field accesses (read
or write) on the returned template object in ALL 12 windows. All template
consumption is:
- pointer STORE into CALLER-owned structures (FUN_006baa20 → this+0xC;
  FUN_00733490 → this+0x14+i*0x18 record slots), and
- pointer FORWARD (return-to-caller in 8 accessors; method-call forwards to
  FUN_0072fce0 / FUN_007ce1e0 / FUN_0040b070 / FUN_005670a0).
- Recorded read pattern on a DERIVED object (FUN_006c3f50, BYTE_OBSERVATION):
  after CALL FUN_0040b070(0x8BD720) @0x006C3FB5 (receiver = the template, body
  CLOSED), the window reads [EAX+0x4] @0x006C3FBE (`8B 50 04`) and [EAX]
  @0x006C3FC1 (`8B 00`) of the FUN_0040b070 result — an object derived from
  the template by method call, identity UNKNOWN while the callee is CLOSED —
  and forwards the pair into FUN_006c3640 @0x006C3FCD. No float evidence
  in-window; the transform/position relevance of these reads is UNKNOWN, so
  no transform-relevant access is ESTABLISHED by them.
The float operations present in FUN_00567170's window do NOT target the
template. Whether any CLOSED callee reads transform/position-relevant template
fields is NOT established by this run and remains a candidate bounded
follow-up (the natural next question: decode FUN_0072fce0 — the validity method
called on the template in 2 windows — the FUN_007ce1e0 getter family, and
FUN_0040b070 whose result is field-read in-window in FUN_006c3f50).

## 5. Preserved definitions/distinctions (verbatim, all run)

- template definition 4057 -> model 218757 is a definition/resource relation, NOT a world instance.
- sids string-table id 4057 is a DIFFERENT namespace (its label is currently UNRECONCILED between prior records — not cited as resolved).
- MODEL_218757_TO_CMO_JOIN = NOT_ESTABLISHED.
- WORLD_XYZ_RECOVERED = NO.
- no CMO+0x44 -> X promotion.
- 0x0085B1B0 / 0x0095D3C4 bodies remain CLOSED this run (0x0095D3C4 appears here
  only as the operator-new-wrapper call edge inside FUN_0043A550 @0x0043A57C —
  its body was not decoded).
- no T+0x10 producer investigation in this run.

## 6. SELF_CHECK against the pre-registered gates (executor self-check — NOT an independent MASTER audit)

- **G1 CENSUS_COMPLETE: PASS (10/10 classes × 2 functions, each with method + result).**
  The only NOT_CHECKED element: the statically non-enumerable register/computed-only
  indirect-call sub-class (explicitly listed with reason in C3) — G1 remains PASS
  because the contract allows explicitly-listed NOT_CHECKED classes with reason;
  no class was silently skipped. (If the parent treats that sub-class as
  demoting, G1 = PASS_WITH_ONE_DECLARED_LIMITATION.)
- **G2 CALLER_CLASSIFIED: PASS (12/12 in-budget callers with the 4-tuple
  VA/window-bounds/id-source-class/role-class, each byte-anchored; 3 UNKNOWN
  provenance marks explicit; 0 guessed).** 20 further callers recorded
  IDENTIFIED_NOT_ANALYZED with callsites (budget respected, not exceeded).
- **G3 IDENTITY: PASS.** EXE SHA256 before == after == expected (measured both).
  Historical landmark package: 84/84 files byte-identical before vs after
  (baseline captured pre-work, re-verified post-work). Reused Ghidra project's
  sandbox EXE byte-unchanged. Zero .pyc residue created by this run (run
  scratch, package, historical landmark package — all `python` invocations
  used `-B`); pre-existing foreign untracked .pyc/__pycache__ artifacts
  elsewhere in the repo tree (cwd) predate this run and are out of scope of
  this claim.
- **G4 NO_PROMOTION: PASS.** Zero XYZ/placement/building-instance claims; zero
  runtime claims; every finding carries STATIC_ONLY + maturity labels
  (IDENTITY/BYTE_OBSERVATION/STRUCTURE/RELATION only).

Non-pass classes: none fired (no UNRESOLVED_CALLER_ROLE — the 3 UNKNOWN
provenance cases are the contract-mandated honest UNKNOWN marks inside PASS
windows; no INCONCLUSIVE_CENSUS; no BUDGET_EXHAUSTED — budget was respected
with the honest IDENTIFIED_NOT_ANALYZED census class).

## 7. Intervention ledger

- **Expected NONE (STATIC_ONLY) — actual: one tooling-cycle disclosure.** The C2
  Ghidra postscript had one bugfix cycle (Jython `Data.hasValue()` overload
  quirk); the script was re-hashed after final edit BEFORE the successful
  execution (hash history in EVIDENCE_INDEX.md; first failed run logged). No
  scientific result depends on the failed attempt; the failed run's output was
  discarded and re-measured from scratch.
- Ghidra project reuse (disclosed in PREREGISTRATION.md §6): the reused
  LANDMARK4057 project DB was re-saved by Ghidra on open/process (Ghidra
  behavior); this is a 99_Audits SCRATCH project, not a historical audit
  package; the historical package trees are byte-unchanged (verified).
- No other interventions. No input file modified. No runtime/network anything.

## 8. FULL_READ_LOG (consolidated read/closed discipline — STATIC_ONLY)

- **Physical file reads by this run's scripts**: ONLY the census binary
  `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe` (read-only; SHA256
  measured before AND after = expected, unchanged) plus the run's own JSON
  outputs. No model/asset/NIF/GLB/ARK/VFS/BNT physical reads; the string
  `Parameters\templates.vfs` was used only as an in-EXE byte anchor for the
  raw-mapper calibration, never as a file path.
- **Decoded this run (listings + decompiles)**: the 2 census subjects
  (FUN_0072F580, FUN_0043A550), the DAT_00BA1824 reference set (exactly 3
  refs, all inside FUN_0043A550), and the 12 in-budget caller windows
  (FULL_FUNCTION_FLOW_BODY; §3).
- **Stayed CLOSED (call edges recorded, bodies NOT decoded)**: all 92
  distinct non-subject in-window callee targets (§3), the census subjects'
  own callee edges FUN_004d1430 / FUN_0095d3c4 / FUN_0052a260 (§1) and
  0x0085B1B0, and the 20 IDENTIFIED_NOT_ANALYZED caller bodies (never
  opened). Classification-relevant names among these: FUN_0070ed80,
  FUN_006b22d0, FUN_006c2e00, FUN_006c3640, FUN_00703b80, FUN_00728150,
  FUN_007376a0, FUN_004926e0, FUN_00977780, FUN_0072fce0, FUN_007ce1e0,
  FUN_0040b070, FUN_005670a0 (plus the §1 subject-body edges named above).
- **Hash-read only (content not re-analyzed)**: the historical landmark
  package `PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003` (84/84
  files, SHA256 byte-identity checks before and after work) and the reused
  Ghidra scratch sandbox EXE
  (`99_Audits\PE_935_LANDMARK4057_GHIDRA_SCRATCH_20261003\Entropia.exe`,
  hash-verified before and after).
- **Ghidra project reuse** (disclosed in PREREGISTRATION.md §6): the reused
  LANDMARK4057 project DB was opened and re-saved by Ghidra on open/process
  (99_Audits scratch, not a historical package); the historical package trees
  were byte-verified unchanged.
- **Client never ran**: no runtime, no dynamic instrumentation, no network
  (STATIC_ONLY held for the whole run).
