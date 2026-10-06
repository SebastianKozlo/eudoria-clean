# QC_REPORT_INTERNAL — PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_QC_INTERNAL_R1_20261006

```text
RUN_ID             = PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_QC_INTERNAL_R1_20261006
PARENT_DISPATCH    = PE-MASTER direct dispatch (INTERNAL_QC worker: pe-master-auditor)
                      NO_NESTED_TASKS · STATIC-ONLY · fresh context
QC_SCOPE           = INDEPENDENT_INTERNAL_QC_INSTANCE_KEY_RESOURCE_EDGE_MICRO (LOAD_BEARING depth)
AUDITED_PACKAGE    = docs/audits/PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006/ (28 files)
REPO               = D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean @ BASE 3921dbe2a43a9181f8a50fa5242d8586c85896b6
                      (HEAD unchanged; package untracked pre-persistence; entrypoint unedited)
EXE                = D:\Eudoria_Reconstruction\pcg_install\Entropia.exe
                      8,015,872 B / SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (re-verified 2x)
CONTRACT           = .../OPENCODE_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006.md
                      11,823 B / SHA256 57A731683EE32E6FC43CCEC42664B03D4DC7FBA2138009B8BF7A0A8E634BABB6 (re-verified)
QC_VERDICT         = QC_PASS_WITH_FINDINGS
```

## 1. Verdict and its basis

**QC_VERDICT = QC_PASS_WITH_FINDINGS.**

Every load-bearing scientific claim of the executor package that this QC was
required to check was independently re-derived from the pinned EXE with a different
engine (PowerShell/.NET byte scans + own PE walk + own MSVC RTTI walk) and MATCHED:
the getter pin, the complete E8/E9/dword census, all claimed rel32 call targets,
the receiver chains, the insert-body resource-family negative, the RTTI class
identities (including `.?AVClientMovableObject@@` by own byte read), the budget
accounting, and the manifest bijection (27/27 rows re-hashed: zero mismatches).
The QC gate scripts' predicates (CTRL_A/B/C) genuinely bind to physical EXE bytes
— a mutated expectation/in-memory copy FAILS from a real byte mismatch, not from
manifest or Git state. My own executed negative controls (NC1-NC3, incl. an
independent re-run of the CTRL_C falsifier) all PASS.

Two findings are material provenance/evidence-integrity defects (F1, F2 — both P1)
that must be repaired in the package **before the persistence phase publishes it**;
three are P3 wording/documentation nits (F3-F6) and one is a P3 observation (F7).
None of them falsifies a scientific claim; the science is TRUE as verified, but the
package as it stands would publish (a) a governance record whose pinned KROK-0
identity no longer matches the file, and (b) ledger citations pointing at raw
evidence windows that were never persisted.

This verdict is the independent internal QC result. It is NOT MASTER_ACCEPTED, NOT
a milestone closure, and leaves PE_MASTER = PROVISIONAL_UNTIL_QUALIFIED,
CANONICAL_GATE_EFFECT = NONE, external Desktop post-audit NOT_PERFORMED/NOT_CHECKED.

## 2. Own counters vs declared (all MATCH unless noted)

| # | Item | Executor declared | My own measurement | Match |
|---|------|------------------|-------------------|-------|
| 1 | Getter bytes @0x00414130 | `8B 41 74 C3` (+ RET/CC boundary) | `8B 41 74 C3 CC CC CC CC CC CC CC CC CC CC CC CC`; window @0x00414120 matches; decode verified | YES |
| 2 | E8 census in .text | 6 hits (list) | 6 hits — identical VAs/file-offsets/rel32 signed values/bytes | YES |
| 3 | E9 JMP thunks / absolute dwords | 0 / 0 | 0 / 0 (whole file) | YES |
| 4 | E8-pattern outside .text | 0 | 0 | YES |
| 5 | Ghidra references to getter | exactly 6, all UNCONDITIONAL_CALL, all PROVEN_EXACT starts | set equality: my census set == in-package Ghidra reference set (6==6, identical VAs); my raw streams byte-identical to the Ghidra listings | YES |
| 6 | rel32 target recomputations | MATCH everywhere | all 25+ claimed sites recomputed by me: all MATCH (QC_MEASUREMENTS M3) | YES |
| 7 | RTTI identities | 3 calibration + `.?AVGameClient@@` + `.?AVSceneFeederObjectExtraData@@` + 1 honest NOT-A-CLASS-VTABLE | all reproduced by own walk incl. `.?AVClientMovableObject@@` (COL 0x00AA17CC / TD 0x00B79958); string @0x00A7D444 = "ArkSceneFeeder" (matches the Ghidra decompile) | YES |
| 8 | Receiver chain (CTRL_B E1-E4) | 8B F1 / C7 06 B0 DC A7 00 / 8B CE / E8 52 B1 EE FF | byte-verified at 0x00528E76 / 0x00528EA2 / 0x00528FD2 / 0x00528FD9 + key PUSH 50 + E8 DA B7 FF FF -> 0x005247C0 + 89 86 C0 00 00 00 store | YES |
| 9 | SF ctor key/holder stores | [SF+0x14]=key @0x00509372..7E; [SF+0x8C]=holder; [SF+0x30] NiNode; refcount++ | byte-verified: 8B 44 24 50 / 89 45 14 / 8B 4C 24 4C / 89 8D 8C 00 00 00 / 83 40 04 01 / 6A 14 | YES |
| 10 | Budget-boundary edge | E8 50 1D 14 00 @0x0050948B -> FUN_0064B1E0; E8 D9 D5 2A 00 @0x005094A2 -> FUN_007B6A80 | byte-verified by my own read (the cited own-byte window is MISSING from the package — F2); Ghidra decompile corroborates | YES (content) / NO (citation) |
| 11 | FUN_0064B1E0 probe content | 26-B body: 56 8B F1 E8->0x007C8780 8B 44 24 08 89 46 10 C7 06 74 32 A8 00 RET 4; vtable -> `.?AVSceneFeederObjectExtraData@@` | byte-verified exactly; RTTI walk reproduced; body is 26 B; probe window is MISSING from the package (F2) | YES (content) / NO (citation) |
| 12 | FUN_004157B0 vtable store | C7 06 18 9F A7 00 @0x004157B7 -> 0x00A79F18 | byte-verified; RTTI `.?AVGameClient@@` reproduced; window MISSING from the package (F2) | YES (content) / NO (citation) |
| 13 | CTRL_C clean (resource-family E8s in insert body) | ZERO | my own census: 0 (all 6 body E8s enumerated: 0x00413440 / 0x00414130 / 0x00856090 / 0x00854D90 / 0x00413450 x2) | YES |
| 14 | Budget | 6 COUNTED (getter, ctor, FUN_005247C0, FUN_00509330, FUN_00856190, FUN_00401360) + FUN_0064B1E0 DISCLOSED_OVER_BUDGET_PROBE + FUN_004157B0 BOUNDED_CLASSIFICATION_PROBE; hops=2 (3rd edge recorded stop); shortlist=3 | ledger recount confirms exactly this; probe is genuinely NON-LOAD-BEARING for the outcome (see §4) | YES |
| 15 | Manifest | 27 rows, self-excluded, entrypoint-row exclusion documented | 27/27 re-hashed: 0 size/SHA mismatches, 0 extra, 0 missing; 28 physical files | YES |
| 16 | Governance verbatim | human instruction saved VERBATIM before science | content consistent point-by-point with the dispatch description and contract identity (SHA/size verified); byte-identity vs the KROK-0 pinned state cannot be established (F1) | PARTIAL (F1) |

## 3. Findings

### **F1 (P1) — GOVERNANCE_DECISION.md: dwa niespójne piny tożsamości; nieujawniona edycja po pomiarze KROK 0 (+25 B)**

- **Exact source:** `01_RAW/GovernanceWriteTime.txt` (pin: 6,299 B, SHA256
  `A953107598F7553C8DE5926EE7FA690920117E34923977B728F065AC073741A6`, file
  LastWriteTime 2026-10-05 23:54:05.874, measured_at 23:54:08.342) vs the current
  physical `GOVERNANCE_DECISION.md` (6,324 B, SHA256
  `96B80022C5819AE0781B978053CB076C12B918C9E377D4CDB8569BBADD808E3A`,
  LastWriteTime 23:54:12) vs `COMMITTED_PACKAGE_MANIFEST_SHA256.csv` row
  `GOVERNANCE_DECISION.md` (6,324 B / 96B80022... — pins the CURRENT bytes).
- **Contradicted claim:** GOVERNANCE_DECISION.md's FILE_WTIME_VERIFICATION section
  presents GovernanceWriteTime.txt as the "independent re-measurement performed
  immediately after the write" identity of this file; the file changed (+25 B)
  4 seconds AFTER that measurement, and no package text discloses the edit.
- **Failure mechanism:** two identity pins of the same file, recorded at two
  different times, both presented as valid, with the intermediate edit neither
  disclosed nor content-preserved anywhere. The KROK-0 byte state (6,299 B) cannot
  be reconstructed from the package, so a byte-identity proof of the VERBATIM
  human-instruction block against the KROK-0 state is impossible from the package
  alone (L10/L13: SOURCE_FILE vs MANIFEST_IDENTITY split; report->physical chain).
- **Effect/blast radius:** governance provenance only. No science claim depends on
  the delta. Mitigations found: (a) the edit (mtime 23:54:12) still precedes the
  first science artifact (pe935k_core.py, 23:56:13), so "written BEFORE science"
  holds for the final state; (b) the verbatim block is internally consistent with
  the contract identity (path + SHA `57A73168...` + size 11,823 B — all verified
  by me), the PE-MASTER dispatch characterization (DA1 present-exception, one run,
  allowlist, prohibitions, two-phase persistence instruction), and the actually
  executed package state; (c) the manifest correctly pins the current bytes.
- **Required correction (pre-persistence, by the persistence phase/executor):**
  add a disclosed amendment (in GOVERNANCE_DECISION.md or an adjacent addendum
  record) stating: initial write 23:54:05.874 (6,299 B / A9531075...), a subsequent
  edit at 23:54:12 (+25 B -> 6,324 B / 96B80022...) performed still before science,
  its exact content delta, and an explicit statement whether the VERBATIM block was
  touched (with a re-pin of the final file). Do NOT alter GovernanceWriteTime.txt
  (it is an honest measurement of the earlier state) and do NOT rewrite the
  historical content.
- **Revalidation predicate:** the amendment's pinned SHA == physical file at the
  persistence-phase manifest regeneration; the regenerated manifest pins the
  amended file; no further unexplained mtime/hash drift.

### **F2 (P1) — Cytowane okna surowe `SF_ctor_tail`, `F0064B1E0_head`, `F004157B0_head` nie istnieją w 01_RAW/BYTE_WINDOWS.txt (zerwany łańcuch własnych bajtowych dowodów)**

- **Exact source (citations):** `EDGE_LEDGER.csv` rows `E-E2-EXTRADATA` ("01_RAW/
  BYTE_WINDOWS.txt SF_ctor_tail"), `E-E2-REG` (same), `E-XD` ("F0064B1E0_head"),
  `E-GB2` ("F004157B0_head"); `FUNCTION_LEDGER.csv` row 4 ("F00509330_edge2_sfctor +
  SF_ctor_tail"), row 7 ("F0064B1E0_head"), row 8 ("F004157B0_head");
  `EVIDENCE_INDEX.md` (claims BYTE_WINDOWS.txt contains "FUN_00509330 (body+tail),
  ... FUN_0064B1E0 head, FUN_004157B0 head").
- **Physical counter-evidence:** `01_RAW/BYTE_WINDOWS.txt` (5,474 B) contains
  exactly the 7 windows that `03_SCRIPTS/byte_windows.py` generates; the
  F00509330 window ends at 0x0050946F — BEFORE the tail (0x0050948B/0x005094A2);
  no other package file contains the three cited windows. The "boundary probe"
  output (EVIDENCE_INDEX: "byte_windows.py + the boundary probe") was never
  persisted.
- **Skutek / blast radius:** the package's *own-byte* evidence layer (the layer
  EVIDENCE_INDEX advertises as "independent of Ghidra") is absent for: the
  budget-boundary edge record (E-E2-EXTRADATA — load-bearing for the
  BOUND_REACHED outcome's "3rd edge exists" component), the registration edge
  (E-E2-REG), the over-budget probe body (FUN_0064B1E0) and the GameClient
  classification store (FUN_004157B0). Citations in 3 ledger rows + 3 FUNCTION_LEDGER
  rows + the EVIDENCE_INDEX description are broken (L13 chain breaks at the
  source-identity step; the index misdescribes the artifact for 3 of 10 items).
- **Material mitigation (my own re-derivation):** every byte claim in those rows is
  TRUE — verified by my independent reads (QC_MEASUREMENTS M6): SF tail
  (`8B 55 14 / 52 / 8B C8 / E8 50 1D 14 00 @0x0050948B -> 0x0064B1E0 / 8B 4D 30 /
  50 / 68 44 D4 A7 00 / E8 D9 D5 2A 00 @0x005094A2 -> 0x007B6A80 / C2 0C 00
  @0x005094BC`), FUN_0064B1E0 (`56 8B F1 / E8 98 D5 17 00 -> 0x007C8780 /
  8B 44 24 08 / 89 46 10 / C7 06 74 32 A8 00 / RET 4`, 26-B body), FUN_004157B0
  (`C7 06 18 9F A7 00 @0x004157B7`). The budget-boundary edge is additionally
  corroborated inside the package by the independent tool (GHIDRA_DECOMPILES.txt
  0x00509330: `uVar4 = FUN_0064b1e0(param_1_00[5]);` and
  `FUN_007b6a80("ArkSceneFeeder",uVar4);`).
- **Required correction (pre-persistence):** persist the missing own-byte windows
  — extend `byte_windows.py` WINDOWS with `("SF_ctor_tail", 0x00509470, 0x50)`,
  `("F0064B1E0_head", 0x0064B1E0, 0x30)`, `("F004157B0_head", 0x004157B0, 0x30)`,
  regenerate BYTE_WINDOWS.txt from the pinned EXE, and re-verify the regenerated
  content against the ledger claims (my M6 dumps are the cross-check). Then correct
  the EVIDENCE_INDEX description and regenerate the manifest LAST (bijection
  re-verification is already part of the persistence flow). A citation-only fix
  (pointing at the Ghidra artifacts) is the weaker alternative and would leave the
  "own evidence independent of Ghidra" claim unbacked for these records.
- **Revalidation predicate:** BYTE_WINDOWS.txt contains the three windows with
  bytes equal to QC_MEASUREMENTS M6; every ledger CITED_PHYSICAL_SOURCE resolves to
  an existing artifact window; the regenerated manifest re-hashes clean.

### **F3 (P3) — qc_controls.py: komentarz CTRL_C błędnie opisuje miejsce iniekcji falsifiera jako "padding-safe"**

- **Source:** `03_SCRIPTS/qc_controls.py` lines ~205-210 ("overwrite a padding-safe
  spot: use the trailing RET 04 00 + padding region tail at 0x0085620C (past the
  epilogue ret) to keep the body intact").
- **Physical counter-evidence:** the injection point is `fake_at = len(body)-5` ->
  VA 0x0085620B, which OVERWRITES live epilogue bytes `83 C4 10 C2 04`
  (ADD ESP,0x10; RET 4) — it is not padding and the body is not "kept intact".
- **Skutek:** none on the control's validity (in-memory copy only, EXE untouched,
  the detector is exercised on the real predicate — my NC1 re-run confirms the
  falsifier is detected). QC_CONTROLS.json/QC_REPORT.md texts state the injection
  site accurately ("injected ... at 0x0085620B in an in-memory copy").
- **Poprawka:** one-line comment fix before persistence; re-pin the script hash in
  the regenerated manifest.

### **F4 (P3) — EDGE_LEDGER E-GB2: transkrypcja nazwy RTTI `.?AVGameClient@` (brak jednego `@`)**

- **Source:** `EDGE_LEDGER.csv` row `E-GB2`, column TARGET_OR_DESTINATION_ARITHMETIC
  ("...name .?AVGameClient@"). Raw evidence (`RTTI_PROBES.json`) and my own walk:
  `.?AVGameClient@@`. Display-level transcription defect (L10: a transcription
  error is a provenance defect even when the source is unchanged).
- **Poprawka:** fix the field; no re-measurement needed.

### **F5 (P3) — FINAL_REPORT §1.2: "ZERO calls to the resource family" — predykat obejmuje wyłącznie bezpośrednie E8**

- **Source:** FINAL_REPORT.md §1.2 ("Control CTRL_C proves the insert body contains
  ZERO calls to the resource family"). The measurement (own §8 PASS record,
  QC_REPORT Q5) is the E8-target census; the body's indirect call `FF D2`
  (0x008561EB, the vtable-dispatched deleting dtor) is outside that census. The
  pair-build bytes prove the FF D2 target is the VALUE's own vtable slot 0 — not a
  resource-family address — so the residual risk is theoretical, but the claim
  wording is broader than the predicate.
- **Poprawka:** reword to "ZERO DIRECT (E8) calls" (one-word precision edit).

### **F6 (P3) — FUNCTION_LEDGER row 4: VA cytatu `C2 0C 00 @0x005094BE` nie jest startem instrukcji**

- **Source:** FUNCTION_LEDGER.csv row 4 ("...RET 0xC; 3 stack args confirmed by
  C2 0C 00 @0x005094BE"). The RET 0xC opcode starts at 0x005094BC; 0x005094BE is
  its last byte (the extent end is consistent as an inclusive end).
- **Poprawka:** cite the start VA 0x005094BC (extent unchanged).

### **F7 (P3, observation) — FAILURE_CASE w rekordzie PASS "All-6-instruction-starts" jest przewidywanym mechanizmem, nie wykonanym falsifierem**

- FINAL_REPORT §8 describes "a mid-instruction E8 ... would have no instruction at
  the VA and be caught" — predicted, not executed (no such case existed in this
  run). Post-hoc closure: my raw census set == Ghidra reference set (6==6,
  identical VAs) is exactly the detection signal that would fire on any
  mid-instruction raw hit. No action required beyond awareness; if a future run
  wants an executed falsifier for this gate, inject a synthetic mid-instruction
  E8 in a copy and require census/references divergence.

### Observation O1 (no defect, recorded for the follow-up run)

The string at 0x00A7D444 is `ArkSceneFeeder` (my own read; also visible in
GHIDRA_DECOMPILES.txt as FUN_007B6A80's first arg). The executor honestly recorded
0x00A7D444 as NOT-A-CLASS-VTABLE (RTTI walk fails) without decoding it as a string.
This string identity is available context for the NEXT_INPUT/EDGE recommendation
(the FUN_007B6A80 registration semantics) and for the two tiny thunks at
0x0064B200/0x0064B210 (the latter returns 0x00A7D444 — a likely accessor for the
same name). No claim in the package is affected.

## 4. Budget, hops, shortlist — own recount

- FUNCTION_LEDGER rows 2-7 = `COUNTED_1_of_6` .. `COUNTED_6_of_6` (getter
  FUN_00414130, ctor FUN_00528E50, FUN_005247C0, FUN_00509330, FUN_00856190,
  FUN_00401360) — exactly 6 == TOTAL_DETAILED_FUNCTIONS_MAX. Row 8 FUN_0064B1E0 =
  `DISCLOSED_OVER_BUDGET_PROBE` (explicitly disclosed as function #7; disclosed in
  FINAL_REPORT §6 + QC_REPORT Q7). Row 9 FUN_004157B0 = `BOUNDED_CLASSIFICATION_PROBE`.
- **Is the probe genuinely non-load-bearing?** YES. The OUTCOME (`BOUND_REACHED`)
  rests on (a) the budget rule (two further edges traced: FUN_005247C0, FUN_00509330;
  the third edge recorded and the analysis stopped) and (b) the EXISTENCE of the
  third edge (E8 @0x0050948B -> FUN_0064B1E0), which is evidenced independently of
  the probe content (my byte read + the Ghidra decompile call chain). The probe's
  CONTENT (ExtraData class identity, key at +0x10) only informs the NEXT_INPUT
  recommendation; KEY_ROLE ("runtime identity") is carried by the insert-site proof
  and the no-lookup findings in the two budgeted SF functions. No 4th shortlisted
  site, no second deep branch, no function-#8 analysis — confirmed.
- Further call edges from the selected callsite: 2 (budget respected), 3rd edge
  recorded as the boundary stop — confirmed. Shortlist: 3 SHORTLISTED rows + 3
  census-classified NOT SHORTLISTED — confirmed (contract "at most THREE" sites).

## 5. QC gate predicates (dispatch item 4) — code-level verdict

- **CTRL_A** (`qc_controls.py` pin_gate/semantic_gate): mutated expectation +0x78
  FAILS against the physical byte 0x74 re-read from the EXE (byte-pin FAIL +
  semantic "disp8 mismatch"). FAIL = real measurement change; no manifest/Git
  involvement anywhere in the gate. PASS (mandatory control satisfied).
- **CTRL_B** (receiver_gate): E3 removal in an in-memory window copy FAILS the
  4-edge byte predicate re-read from the EXE. The claim "ECX at 0x00528FD9 == ctor
  this" is exactly covered by E1-E4 (prologue capture + CMO vtable store + receiver
  re-establishment + the call). PASS.
- **CTRL_C** (resource_join_negative): map pins re-read from the EXE body +
  direct-E8 census against the BASE-canon family list; the injected fake
  E8->FUN_0072F580 (in-memory) is detected. My independent NC1 re-run reproduced
  clean=0 / detected=1. PASS. (Note F5 on the FINAL_REPORT wording and F3 on the
  code comment.)

## 6. Scope / status algebra (dispatch item 7)

- **No commit** — HEAD == BASE `3921dbe2...`; the package tree is untracked;
  AUDIT_ENTRYPOINT.md unmodified vs BASE (the proposed row is in HANDOFF.md as
  instructed; the persistence phase will add it and regenerate the manifest — the
  deferral is documented in GOVERNANCE_DECISION.md, EVIDENCE_INDEX.md and the
  manifest comment line).
- **No runtime** — STATIC-ONLY corroborated: all instruments are byte readers;
  the Ghidra sandbox holds a byte-identical copy of the EXE (sandbox SHA == pin)
  and its out artifacts are SHA-identical to the package copies; no VFS/BNT/NIF/ARK
  payload appears anywhere (package-wide greps: only prohibition/scope lines); no
  0xA4 work; capstone/objdump absence disclosed in INPUT_IDENTITIES.
- **No bare except / no silent failure** — zero try/except in 03_SCRIPTS;
  fail-closed asserts in pe935k_core (size/PE identity), error-reason returns in
  the RTTI walker, exit-2 bijection verification in make_manifest, explicit
  DECOMPILE_FAILED recording in ghidra_post. No default-success flags; all
  verdicts computed from byte comparisons.
- **Status algebra** — OUTCOME = `BOUND_REACHED` (a contract §5 outcome string);
  RESOURCE_EDGE_STATUS = NOT_ESTABLISHED_IN_EXAMINED_PATH; resource kind/identity =
  UNKNOWN (not promoted); FUN_0064B1E0 lead = NON-CANONICAL (not promoted); the
  four-variable separation (FUNCTION_IDENTITY / OBSERVED_OPERATION /
  FINAL_SEMANTIC_ROLE / HISTORICAL_INPUT_AVAILABILITY) is present and filled in
  FINAL_REPORT §7 and the FUNCTION_LEDGER columns. The dispatch-required RTTI claim
  `.?AVClientMovableObject@@` is CONFIRMED by my own byte read
  (VT 0x00A7DCB0 -> COL 0x00AA17CC -> TD 0x00B79958 -> name).
- **No overclaims** — "SHARED +0x74 OFFSET READER" is covered by the 6 census sites
  with >=3 proven receiver kinds (ClientMovableObject x2, GameClient singleton x3,
  unresolved deref x1 — all byte-verified by me); the package explicitly does NOT
  claim all readers (indirect/inlining/other aliases disclosed NOT claimed —
  contract §3.1 prohibition respected in FINAL_REPORT §2, QC_REPORT Q2, HANDOFF).

## 7. COVERAGE (L11) and NOT_CHECKED

Coverage algebra: package files 28 = FULL_READ 28 + NOT_READ 0 (FULL_READ_LOG.txt);
my own executed measurements: ~50 byte-pin reads + 3 full-file scans (E8/E9/dword)
+ 6 RTTI walks + 1 string read + 27-row manifest re-hash + 3 negative controls + 4
sandbox corroboration hashes — all recorded in QC_MEASUREMENTS.txt.

**NOT_CHECKED (this QC, explicit):**
- A fresh Ghidra headless re-run (I did not re-execute analyzeHeadless; the
  in-package Ghidra outputs are corroborated by byte-identity with the sandbox
  originals + my independent byte/census/RTTI re-derivations + the census-vs-
  references set equality). Instruction-start PROVEN_EXACT rests on the in-package
  independent-tool evidence + that set equality — not on a second Ghidra engine.
- The 4 new containing-function bodies beyond the examined windows
  (FUN_00456770 / FUN_00456a10 / FUN_00456f40 / FUN_00459fd0) — matches the
  executor's own NOT_CHECKED; within my QC scope these were window-verified only.
- FUN_00853D00, FUN_004A9850, FUN_007C8780, FUN_007B6A80, FUN_009789C0 semantics
  (the executor's declared NOT_CHECKED; only their call-target VAs were recomputed).
- Indirect/virtual/inlined readers of any +0x74 anywhere (NOT_CLAIMED by the
  executor either — the absence of a claim is verified, the absence of readers is
  not established and not claimed).
- The BASE-canon resource-family ADDRESS LIST re-derivation from the historical
  packages (used as input by CTRL_C; I re-verified the census arithmetic with the
  same list, not the list's provenance).
- The verbatim human message's original bytes (not available to this QC) —
  assessed for consistency only (G18 PASS_WITH_CAVEAT; F1 for the identity chain).
- BASE historical package contents beyond the cited inputs; runtime behavior;
  Ghidra sandbox project internals; the proposed AUDIT_ENTRYPOINT row's future
  adaptation by the persistence phase.

## 8. Effect of THIS QC on the package (blast radius note for PE-MASTER)

This QC wrote ONLY new files under
`docs/audits/PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006/00_CONTROL_INTERNAL_QC/`
(qc_negative_controls.ps1, QC_MEASUREMENTS.txt, FULL_READ_LOG.txt, QC_GATES.csv,
MANIFEST_REHASH.csv, this report, and its own dir manifest). No executor file was
touched; the EXE was never modified; no commit/push was performed. **Consequence:**
the current 27-row manifest no longer enumerates every physical file under the
package (by the two-phase flow this is expected and disclosed: the persistence
phase regenerates the manifest LAST; per the BASE-precedent persistence decision
commit 3921dbe, the QC records belong in the regenerated manifest scope). The
persistence phase must also apply the pre-persistence corrections for F1/F2 (and
optionally F3-F6) BEFORE the entrypoint row, manifest regeneration, commit and push.

## 9. QC handoff block

```text
ASSIGNMENT_MODE    = INTERNAL_QC (independent fresh-context; LOAD_BEARING depth)
RUN_ID             = PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_QC_INTERNAL_R1_20261006
PARENT_LOOP_ID     = PE-MASTER dispatch of 2026-10-06 (PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006)
MILESTONE          = PE 9.3.5 reconstruction (no gate effect; CANONICAL_GATE_EFFECT = NONE)
SCOPE              = INDEPENDENT_INTERNAL_QC_INSTANCE_KEY_RESOURCE_EDGE_MICRO (STATIC-ONLY)
QC_VERDICT         = QC_PASS_WITH_FINDINGS
FINDINGS           = F1 (P1, governance identity-pin drift, pre-persistence repair required)
                      F2 (P1, three cited raw windows missing, pre-persistence repair required)
                      F3 (P3, qc_controls.py falsifier-site comment)
                      F4 (P3, E-GB2 RTTI name transcription)
                      F5 (P3, FINAL_REPORT "ZERO calls" wording vs direct-E8 predicate)
                      F6 (P3, RET VA citation ambiguity)
                      F7 (P3 observation, predicted-vs-executed FAILURE_CASE)
                      + O1 observation (ArkSceneFeeder string available for NEXT_INPUT)
FULL_READ_LOG      = 00_CONTROL_INTERNAL_QC/FULL_READ_LOG.txt (28/28 package files + contract)
NOT_CHECKED        = section 7 above (Ghidra re-run, 4 new function bodies, undeclared
                      consumer semantics, indirect/inlined +0x74 readers, BASE list
                      provenance, verbatim original bytes, BASE package contents)
FINAL_REPORT_PATH  = 00_CONTROL_INTERNAL_QC/QC_REPORT_INTERNAL.md (this file)
GATES_PATH         = 00_CONTROL_INTERNAL_QC/QC_GATES.csv (G1-G18 + NC1-NC3; FAIL: G14, G15)
MANIFEST_PATH      = 00_CONTROL_INTERNAL_QC/QC_PACKAGE_MANIFEST_SHA256.csv (self-excluded)
                      + 00_CONTROL_INTERNAL_QC/MANIFEST_REHASH.csv (executor manifest re-hash)
INPUT_HASHES       = contract 57A73168...BABB6 (11,823 B); EXE E7785430...0F31 (8,015,872 B)
FILES_CHANGED      = ONLY 00_CONTROL_INTERNAL_QC/* (7 files); nothing else; no commit
BASE_SHA           = 3921dbe2a43a9181f8a50fa5242d8586c85896b6
HEAD_SHA           = 3921dbe2a43a9181f8a50fa5242d8586c85896b6 (unchanged; no commit)
PUSH_STATUS        = NOT_PERFORMED (forbidden for this QC per dispatch)
UNRELATED_WORK     = excluded/untouched: 5x foreign PE_935_* untracked dirs + experiments/
NEXT_PARENT_ACTION = persistence phase (after applying F1/F2 pre-persistence repairs,
                      optionally F3-F6 nits): entrypoint row -> manifest LAST (include the
                      00_CONTROL_INTERNAL_QC records in scope) -> bijection/hash verification
                      -> path-limited commit -> push -> verify LOCAL == origin == actual
                      remote -> report pushed SHA; Desktop post-audit stays NOT_PERFORMED.
```

QC performed by: pe-master-auditor (PE-MASTER subordinate; fresh context; adversarial
posture — the executor runs on the same model family, so every load-bearing number
was re-derived with an independent engine rather than trusted).

PE_MASTER = PROVISIONAL_UNTIL_QUALIFIED (advisory only; this QC does not grade or
promote). Q1 / Gate-B / M1 unchanged. WORLD_XYZ_RECOVERED = NO.
