# QC_AUDIT.md — G14 FRESH INDEPENDENT QC — PE_935_SF_ARG2_PROVENANCE_R1_20260914

- **QC session:** pe-master-auditor (fresh session; NOT the formalizer; NOT the executor;
  no participation in the formalization or execution of this run)
- **Parent:** PE-MASTER loop `2ed038db-5d2e-4e7e-b679-2d29bf57501a` (EU935-M1, Phase 2)
- **QC date:** 2026-09-14 · **RUN_CLASS:** MATERIAL (targeted QC depth: load-bearing claims
  + census machinery + gates)
- **Method:** all load-bearing claims re-measured from the pinned EXE with the QC session's
  OWN implementations (no executor code reused for measurement); full read of every
  package file and every generator; the executor's scripts additionally RE-EXECUTED from a
  byte-safe path-patched copy to prove repeatability/determinism. Counter-check scripts live
  OUTSIDE the project tree (`C:\Users\User\AppData\Local\Temp\opencode\qc_arg2_r1\`,
  labeled `AUDITOR_COUNTERCHECK_*`); ZERO git mutations by the QC session; this file is the
  QC session's ONLY write inside the package.
- **Interpreter used by the QC:** `D:\Eudoria_Reconstruction\10_Scripts\python_env\python.exe`
  (Python 3.12.7) with `-B`; capstone 5.0.7 (measured, same site-packages).

## G14 VERDICT

# **QC_PASS_WITH_FINDINGS**

One P1 report-layer denominator defect (must be corrected before persistence; it does not
flip any gate outcome or science status), one P2 census-machinery defect (latent; zero
outcome impact this run), three P3 documentation/precision notes. Every load-bearing
claim — the W1 ABI chain, all three censuses, the receiver-proof outcomes, the
FUN_006FAB80 forwarding-thunk trail, the shared-slots P1, the immutability pins, the gates'
measured quantities — REPRODUCES from my own independent measurements.

---

## 1. Identity / immutability (QC checklist 1) — PASS

| Item | Executor claim | My own measurement | Verdict |
|---|---|---|---|
| Entropia.exe SHA256 | E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 | identical (own hashlib) | MATCH |
| Entropia.exe size | 8015872 | 8015872 | MATCH |
| PE32 sanity | machine 0x014C, magic 0x010B, image_base 0x00400000; sections .text vaddr 0x1000 vsize 0x6735E5 raw 0x674000 etc. | identical (own PE parse) | MATCH |
| HEAD at QC time | BASE_SHA f239eb85cd0f56ae10cee52d57833a49f225965c | `git rev-parse HEAD` == f239eb85cd0f56ae10cee52d57833a49f225965c == origin/master == live ls-remote | MATCH |
| Untracked set | exactly {FIRSTCALL pkg, this package, experiments/} | exactly those three; STAGED_COUNT 0 | MATCH |
| AT_RUN_START / AT_RUN_END observations | present, read-only, HEAD==BASE both times | present on disk, consistent with my own re-measurement; run-start 16:49 vs run-end 17:08, zero mutations start==end | MATCH |
| FIRSTCALL package | 7/7 pinned hashes + 3 empty dirs + no extra files | **7/7 re-hashed MATCH** (own hashlib); 02_ANALYSIS/03_EVIDENCE/06_REPORT empty; extra files 0 | MATCH |
| LINK30 immutable census | SF30_WRITER_CENSUS.csv hash MATCH; SF30_WRITER_RAW.txt present | CSV re-hashed == 71552E2A4BFC120DA0BE1A7E108A41A03C873ADDD238637DD7C18F3C968824D0; RAW present | MATCH |
| experiments/ | untouched, never inventoried | present; untouched by this run | MATCH |
| Git mutations | NONE | my session: zero mutations (read-only git); HEAD/status/staged identical before and after QC | MATCH |

## 2. W1 ABI chain (QC checklist 2) — PASS, fully reproduced from my own byte reads

My own read of the 33 byte positions 0x0050A050..0x0050A0A7 (plus the padding window):

- `mov eax,[esp+8]` @0x0050A050 = **8B 44 24 08** (the arg2 def) → `test eax,eax` (85 C0)
  → NULL-branch `je 0x50A087` — the claimed eax chain to `push eax` @0x0050A060 = **50**
  reproduces byte-exactly.
- Dispatch window: 8B F1 @0x0050A057; 8B 4E 30 @0x0050A05B; 8B 11 @0x0050A05E;
  8B 42 44 @0x0050A061; FF D0 @0x0050A064 — NC-1 pins 9/9 byte-exact (0 PIN_MISMATCH),
  my measurement agrees.
- **ret 8 (C2 08 00) at BOTH ret sites**: @0x0050A084 and @0x0050A0A7 — measured by me.
- Fallback pins: 8B 16 @0x0050A087; 8B 42 04 @0x0050A089; 8B CE @0x0050A08C;
  FF D0 @0x0050A08E; X/Y/Z reads 8B 10 / 8B 50 04 / 8B 40 08 @0x0050A090/98/9E;
  out copies 89 11 / 89 51 04 / 89 41 08 @0x0050A096/9B/0A1 — all byte-exact.
- Primary-path E8 targets: 0x0050A075 → 0x437F70 and 0x0050A07C → 0x82B5A0 (verified
  rel32; G6: these appear only as decoded call targets, never analyzed downstream).
- Extent end 0x0050A0AA: padding **CC CC CC CC CC CC** (6 bytes) completing to the
  16-aligned 0x0050A0B0; adjacent-start bytes 56 8B F1 80 7E 24 00 75 10 E8 02 F5 FF FF
  B0 01; adjacent start corroborated by exactly {E8@0x0044CC41, E9@0x0044CC92,
  E9@0x0044CD64} (my own lattice scan); imm32 refs to 0x0050A0B0 = 0. The iterative
  terminal+padding boundary derivation is correct (first ret 0x0050A084 is NOT the end:
  non-CC bytes follow AND internal branches target 0x0050A087).
- B.2 permitted value check: dword [0x00A8CCF4+0x44] == 0x007B5390 — MATCH (value read
  only; slot 17 was NOT decoded — G6 held).

**ARG2_ABI CONFIRMED is supported.**

## 3. Census machinery (QC checklist 3) — PASS, all denominators reproduced by my own scans

- **E8 census:** my own full-.text byte scan (0x00401000..0x00A75000, 6,766,592 B):
  **156,829** E8 byte occurrences; **0** E8 / 0 E9 / 0 EB targets == 0x0050A050.
  CAL-2 known answer: FUN_005247C0 → exactly **7** sites
  {0x0044D625, 0x0044D677, 0x0044D6C8, 0x00528FE1, 0x0067B8A4, 0x0067C864, 0x006A39ED} —
  identical set. SF ctor FUN_00509330 → exactly {0x0047D043, 0x0052480F} (B.3 pin MATCH).
- **imm32 census:** my own whole-file scan for LE dword 0x0050A050: **exactly 1 hit**,
  file offset 0x0067D464 = VA **0x00A7D464**, section .rdata; NC-4: dword == 0x0050A050.
  CAL-1: LE dword 0x00A7D458 → exactly 2 hits, VAs 0x00509369 / 0x0050A26B, inside the
  store instructions `mov [ebp],0xA7D458` @0x00509366 (C7 45 00 58 D4 A7 00) and
  `mov [esi],0xA7D458` @0x0050A269 (C7 06 58 D4 A7 00) — both byte-verified.
  **FUN_0050A050 is vtable-addressed ONLY — the channel is exclusively virtual: CONFIRMED.**
- **Pattern denominators (my own byte scans):** P1 `call [reg+0xC]` = **1** (the site
  0x005B0163 `FF 55 0C`, a frame call — NOT_A_VTABLE_CALL); P1J = 0; P2 = 0;
  P3 `mov dst,[base+0xC]` pre-check = **7,106**; P3 after the follow-check = **217**
  (my own re-implementation of the declared ≤3-non-control-interstitial rule reproduces
  the set); slot-17-form cross-check `FF 52 44` = 0. Total candidates **218**.

## 4. Receiver-proof machinery (QC checklist 4) — PASS

- `01_RAW/VIRTUAL_CALLSITE_CENSUS.csv`: **237 lines = header + 218 candidate rows
  (P1=1, P3=217) + 18 M1_FLOW rows** — verified by direct parse.
- Outcomes: **211 INSUFFICIENT_PROOF / 5 REJECTED_NOT_SF / 2 NOT_A_VTABLE_CALL /
  0 PROVEN** — verified by direct count.
- **Mechanical row validation:** I decoded every one of the 218 candidate rows at its VA
  (own capstone) and re-derived pattern bytes, the base column, the instruction text and
  the follow-check: **0 bad rows**. Evidence-instruction spot-checks (pop esi @0x4056F0;
  `mov ecx,[esi+0x28]` @0x47D808; `mov ecx,[edi+0x160]` @0x7B96D1; `mov ecx,[esi+0x30]`
  @0x804908; `call 0x7d0b40` @0x78CBD9) — all byte-exact.
- **NC-2 discrimination (REJECTED rows) — my own RTTI walks:** 0x007AC2F0 is a vtable
  slot function of `.?AVNiD3DHLSLPixelShader@@` + `.?AVNiD3DPixelShader@@` (slot 14; my
  membership scan); 0x007F1D70 of `.?AVNiBMPReader@@` / `.?AVNiBoundingVolume@@` /
  `.?AVNiSGIReader@@`; the vtable loads (e.g. `mov eax,[esi]` 8B 06 @0x007AC44A) and
  slot-3 loads (8B 50 0C @0x007AC450) byte-verified. The census demonstrably rejects
  non-SF receivers — NC-2 PASS.
- **NOT_A_VTABLE_CALL rows:** my own 48-byte backward-window decode of 0x004198C1 and
  0x005B0163 confirms no vtable load into the base register — honest classifications.
- **CAL-3:** my own backward-chain enumeration at 0x00529020 resolves the last def of
  ECX in every chain to `mov ecx,[esi+0xC0]` @0x0052901A (8B 8E C0 00 00 00) → the
  tracer's PROVEN_HOLDER_0xC0 calibration reproduces.
- **Method-1 holder route:** per-offset read counts reproduce EXACTLY (my own scan,
  correct signed-disp8 semantics): +0x04 = 12,535; +0x0C = 5,957; +0x10 = 2,615;
  +0x14 = 2,841; +0x18 = 1,761; "+0xC0" bucket = 196 (see P2-QC for what that 196
  really contains). My own clobber-aware flow re-derivation over the same enumeration
  finds **exactly the same 18 flows** (same read sites, same offsets; no extra, no
  missing), and my own ABI disposition of all 18 reproduces **17 ABI_INCOMPATIBLE**
  (my measured effective-arg counts match every row: 3×2-arg/not-thiscall,
  1×0-arg/thiscall, 7×1-arg/thiscall, 6×4-arg/not-thiscall) + **1
  ABI_COMPATIBLE_2ARG_THISCALL** at the FUN_006FAB80 read @0x006FAB80.
- **FUN_006FAB80 (own decode):** bytes @0x006FAB80 =
  `8B 49 14 / D9 44 24 04 / 8B 54 24 08 / 8B 01 / 8B 40 0C / 52 / 51 / D9 1C 24 / FF D0 /
  C2 08 00` — a forwarding thunk: receiver = [this+0x14], arg1 (float @ [esp+4])
  re-pushed via fld/fstp reserve-slot idiom, **arg2 ([esp+8]) forwarded verbatim via
  `push edx`**, call slot 3 of the held object's vtable, `ret 8`. B.5 padding before the
  entry (CC-run completing at the 16-aligned start) verified. **Vtable memberships (my
  own whole-file dword scan + RTTI walk): EXACTLY the 10 claimed classes**
  (ArkAnimationAlpha / AnimatedTexture / Color / Cyclic / CyclicLinear / CyclicSin /
  Derivatives / Predefined / ArkModelResourceInstanceRef / ArkRefObject). The E8/E9
  lattice mis-attribution claim is real: 0x006FAB20 IS the closest lattice start below
  the call and 0x006FAB80 is NOT a lattice target (vtable-only function).
- **Closest-candidate trail (ARG2_ANALYSIS §1.2):** ctor @0x006FABA0 verified — vtable
  store 0xA864C0 (ArkAnimationPredefined), `mov [eax+0x14],ecx` (the held-object store),
  refcount increment on the held object (`mov edx,1; add [ecx+4],edx`), float write at
  +0x24 (`fstp dword [eax+0x24]`); E8 callers of the ctor == the 6 claimed sites
  {0x006FAFC7, 0x006FB092, 0x006FB409, 0x006FB5CD, 0x006FE9E8, 0x006FFA87}; the
  container-side contrast is real (`mov ecx,[esi+0x24]` @0x0044D66A feeding the
  SF-factory call @0x0044D677 → 0x005247C0, and `mov [esi+0x10],eax` @0x0044D680).
- **Machinery metadata:** function-start lattice (distinct E8/E9 targets) = **44,875**;
  RTTI vtable→class entries = **1,904**; vtable-slot function map = **6,713** functions —
  all reproduced by my own implementations.

## 5. SF-vtable shared-slots P1 (QC checklist 5) — PASS

My own walk (string → TD → COLs → vtable): `.?AVArkAudioObjectInterface@@` vtable
**0x00A7D42C** slots 11..15 = {0x50A460, 0x5090A0, 0x5090B0, 0x50A050, 0x5090C0} ==
SF vtable 0x00A7D458 slots 0..4 (my own read of both vtables). The SF RTTI chain
reproduces: vtable-4 → COL 0x00AA12B8 → signature **0**, COL+0x0C = **0x00B78834 (a
full VA, not an RVA)** → TD → `.?AVSceneFeederObject@@`. **P1-2 (shared slots) and
P1-3 (pointer-based RTTI COLs, signature 0) are CONFIRMED.**

## 6. NC/CAL verification (QC checklist 6) — PASS

NC-1 9/9 byte-exact (my reads, §2); NC-2 5 real rejections with verified class proofs
(§4); NC-3 no in-scope subjects (zero verified sites) — machinery demo literal
`Entropia` @0x00A7957C reads back as 45 6E 74 72 6F 70 69 61 00 (verified by me);
NC-4 MATCH (§3); CAL-1 PASS, CAL-2 PASS, CAL-3 PASS (§3–4). All calibrations use
published known answers and are tooling-only; none was adopted as run evidence.

## 7. Gates / REPORT / HANDOFF consistency (QC checklist 7) — PASS with the P1-QC caveat

- W6: package = **30 files**; MANIFEST_SHA256.csv = **29 rows** (no self-row, no
  duplicates; **all 29 re-hashed MATCH** by me); SCRIPT_SHA256.csv = **7/7 re-hash
  MATCH**; EVIDENCE_INDEX.csv covers every derived artifact with generator + generator
  hash pointers (two cosmetic notes below); 0 `__pycache__`/`.pyc` in the package; no
  binary payloads (only .rdata string FACTS).
- **Determinism PROVEN by re-execution:** I copied all 7 scripts, patched ONLY the
  output-path constant (byte-safe patch), and re-ran them with the canonical interpreter:
  all **9 deterministic artifacts reproduce BYTE-IDENTICAL**
  (FUN_0050A050_DISASM.txt, CENSUS_E8_DIRECT.txt, CENSUS_IMM32_0050A050.txt,
  B3_PIN_REVERIFICATION.txt, VIRTUAL_CALLSITE_CENSUS.csv, ARG2_PRODUCER_TRACE.txt,
  IDENTITY_VERIFICATION.txt, NC3_MACHINERY_DEMO.txt, G7_IMMUTABILITY_CHECK.txt).
  (An initial DIFFERS was my own harness artifact — PowerShell read the UTF-8-no-BOM
  scripts as Windows-1252 and mojibake'd em-dashes in string literals; byte-safe patching
  resolved it. Not a package defect.)
- **G3/G4 NOT_APPLICABLE is honest and correct:** the emptiness (zero verified sites →
  zero producers; zero identified values) is the MEASURED census outcome, which I
  reproduced independently; a vacuous PASS would overstate.
- **G5/G6 held:** zero semantic promotions (all four statuses' evidence trails are
  independent; hypotheses labeled as hypotheses everywhere I checked); slot-17 NOT
  re-identified (only the permitted value check — verified in the code and bytes);
  TRANSFORM_TO_MODEL / MODEL_BRIDGE untouched = NOT_DEMONSTRATED; no model/NIF corpus
  work; the disclosed bounded receiver-class discrimination reads are census-necessary
  value/entry reads within the declared bound.
- **W5 delta:** SCIENCE_STATUS_DELTA.csv status_before values match the standing matrix
  rows exactly ("arg2 ABI" = `partially observed revalidate-pending`; "arg2 provenance" =
  UNVERIFIED; "arg2 semantic role" = UNVERIFIED; "arg2 value class" = NEW). Statuses-after
  are consistent with the measured evidence.
- **Falsifiers:** the three disclosed in-run corrections are corroborated: (1) the
  lattice mis-attribution is real and measurable (0x006FAB20 vs the B.5 start 0x006FAB80);
  (2) the clobber example exists exactly as described (`mov ecx,[esi+0x160]` @0x007B93B9
  before the vtable load @0x007B93C8 and slot-3 call @0x007B93D4 in the 0x007B93D3
  region) and the FIXED accumulator reproduces the 18-flow outcome; (3) the corrected
  iterative boundary rule is the one implemented and it agrees with the published extent.
  The P1=1 denominator cross-check (FF 52 44 = 0) reproduces.

## 8. Hygiene (QC checklist 8) — PASS

Deterministic scripts (sorted output; wall-clock only inside the two mandated
timestamped observation files — proven by byte-identical re-run); `-B` everywhere
(zero pyc/pycache in the package); provenance headers (interpreter + capstone measured)
in every raw artifact and every script header; no payloads; script-computed hashes only
(both hash registries re-verified).

---

## FINDINGS

### **P1-QC-1 (report layer; must fix before persistence): the method-1 aggregate "23,671 holder reads" is arithmetically wrong — the true enumeration is 25,905**

- **Sources:** `06_REPORT/REPORT.md` line 22 (ARG2_PROVENANCE cell: "23,671 holder-offset
  reads"), `06_REPORT/HANDOFF.md` line 9, `06_REPORT/STAGE_ACCEPTANCE_GATES.csv` G2
  MEASURED_QUANTITY ("method-1: 23671 holder-offset reads"), `02_ANALYSIS/ARG2_ANALYSIS.md`
  line 92, and the executor's delivery notice.
- **Contradicted quantity:** the package's OWN raw evidence
  (`01_RAW/ARG2_PRODUCER_TRACE.txt` lines 28–33) enumerates +0x04: 12,535; +0x0C: 5,957;
  +0x10: 2,615; +0x14: 2,841; +0x18: 1,761; +0xC0: 196 → **sum = 25,905**, not 23,671.
  My independent scan reproduces all six per-offset counts exactly, so the RAW is right
  and the summary aggregate is wrong (I could not derive 23,671 from any real subset).
- **Effect:** a wrong measured-quantity statement in four package documents including
  inside the G2 gate row. NOT outcome-bearing: the flows (18), the ABI dispositions
  (17+1), the 0-PROVEN result and all other denominators reproduce exactly, and the
  error direction is conservative (MORE reads enumerated than stated — the exhaustion
  bound is strengthened, not weakened). No status or gate outcome flips.
- **Correction:** replace "23,671" with "25,905" (or "25,905 enumerated positions; see
  per-offset raw") in the four documents (and in any future delivery-notice restatement).
- **Revalidation predicate:** sum the six per-offset counts from
  ARG2_PRODUCER_TRACE.txt lines 28–33 == 25,905; my recount (correct signed-disp8
  semantics) == the same six counts.

### **P2-QC-1 (census machinery, latent; zero outcome impact this run): the method-1 "+0xC0" bucket conflates `[base+0xC0]` (disp32) reads with `[base−0x40]` (disp8 0xC0) reads — disp8 sign extension is not applied; the ebp-base exclusion is not applied to the disp32 form**

- **Source:** `00_CONTROL/w2c_w3_virtual_census.py` method-1 enumeration (mod=01 with
  disp8 byte == 0xC0 treated as "+0xC0"; the mod=10 disp32 == 0xC0 case does not
  exclude ebp-base); the raw label "mov reg,[base+0xc0] reads (base != esp/ebp, non-SIB):
  196" (`01_RAW/ARG2_PRODUCER_TRACE.txt` line 33).
- **My measurement:** the 196 = **78 true `[base+0xC0]` disp32 reads (of which 3 have
  ebp base)** + **118 `[base−0x40]` reads** (disp8 0xC0 sign-extends to −0x40). Both
  sub-counts verified by my own scan with correct sign handling.
- **Effect this run:** NONE on outcomes — zero of the 18 flows came from this bucket,
  and I additionally scanned all 118 `[base−0x40]` sites: none flows into a genuine
  slot-3 vcall, so there is no missed and no false channel. The defect is latent: in
  another binary/context a `[base−0x40]` read could be mis-treated as an SF-holder
  candidate channel, and the label misstates what was counted.
- **Correction:** sign-extend disp8 in the enumeration; keep `[base−0x40]` out of the
  +0xC0 bucket (or record it as its own bucket); apply the esp/ebp-base exclusion to the
  disp32 form; re-label the raw line.
- **Revalidation predicate:** bucket split 78 / 118 / 3 reproduces; no change to the 18
  flows or the 17+1 dispositions.

### **P3-QC-1 (documentation typo): EVIDENCE_INDEX.csv CENSUS_IMM32 row cites the CAL-1 ctor-store hit as "0x00509368" — the raw and my scan give 0x00509369**

- **Source:** `03_EVIDENCE/EVIDENCE_INDEX.csv` row 11 ("hits at 0x00509368/0x0050A26B
  operand positions"); the raw (`CENSUS_IMM32_0050A050.txt`) and my own scan: the imm32
  operand of `C7 45 00 58 D4 A7 00` @0x00509366 sits at VA 0x00509369. Off-by-one in the
  index row only. **Correction:** 0x00509369. No other content affected.

### **P3-QC-2 (observation, no defect): FUN_006FAB80 occupies different slot positions across its 10 vtables**

- My membership scan records it at slots 2/4/6/7/11/13/15 across the class vtables (two
  vtables contain it twice) — normal multiple-inheritance thunk sharing. The executor's
  claim ("shared slot function of 10 RTTI classes") is confirmed as stated and never
  asserted a single slot position; recorded here so no later reader assumes one.

### **P3-QC-3 (wording precision): ARG2_ANALYSIS §1.2 describes the held-object refcount increment as `add [ecx+4],1`; the actual instruction is `add [ecx+4],edx` with `mov edx,1` immediately before**

- Bytes @0x006FABA0 region: `BA 01 00 00 00` (mov edx,1) + `74 03` + `01 51 04`
  (add [ecx+4],edx). Semantically identical (adds 1); the prose is a paraphrase, the raw
  decode carries the true bytes. No action required beyond noting the exact form.

### **P3-QC-4 (cosmetic): EVIDENCE_INDEX.csv indexes 2 of the 7 scripts as artifact rows (sf_arg2_common.py, s0_runstart.py); the other 5 generators appear only via SCRIPT_SHA256.csv and the generator columns of their outputs**

- No hash is missing (SCRIPT_SHA256.csv covers 7/7, all re-verified) and every derived
  artifact has its generator recorded. Asymmetry only.

## What was NOT fabricated — the honest negative bound is real

The 0-PROVEN outcome is a genuine property of the data within the declared bound: the
censuses ran (byte-identical re-execution), the denominators are real (my independent
recounts match the raw exactly), the receiver-proof rule demonstrably discriminates
(5 verified non-SF rejections), and the single ABI-compatible channel (FUN_006FAB80) is
correctly recorded as an UNPROVEN-receiver forwarding-thunk family rather than promoted.

## FULL_READ_LOG

All 30 package files read in full by the QC session: 00_CONTROL (RUN_CONTRACT.md,
SOURCE_IDENTITIES.json, GIT_OBSERVATIONS_AT_FORMALIZE.md, SCRIPT_SHA256.csv, and all 7
scripts incl. sf_arg2_common.py read to EOF); 01_RAW (all 12 artifacts); 02_ANALYSIS
(ARG2_ANALYSIS.md, SCIENCE_STATUS_DELTA.csv); 03_EVIDENCE (README.md,
EVIDENCE_INDEX.csv); 06_REPORT (REPORT.md, HANDOFF.md, STAGE_ACCEPTANCE_GATES.csv,
MANIFEST_SHA256.csv). Also read: the standing SCIENCE_STATUS_MATRIX.csv arg2 rows
(cleanup R1 package), AUDIT_ENTRYPOINT.md, and the pinned FIRSTCALL/LINK30 files (hashed).

## NOT_CHECKED

- The client was never executed (STATIC-ONLY; also forbidden for the QC).
- The pre-fix (falsifier) intermediate outputs are not preserved in the package and were
  not re-executed; the falsifier claims are corroborated by mechanism + final-state
  reproduction + the cited bytes (0x006FAB20 lattice start; 0x007B93B9 clobber) rather
  than by diffing the pre-fix artifacts.
- The second ArkAnimationAlpha vtable 0x00AA7BB0's RTTI walk was not independently
  re-derived (not needed for any claim — the class membership is confirmed via 0x00A8663C).
- w6_manifest.py was not re-executed; the equivalent verification (re-hashing all 29
  manifest rows + 7 script rows) was performed instead.
- The published prior-run records (SLOT_CENSUS / LINK30 / SLOT17 GB oracle reports) were
  used as pin sources only; their internal science was not re-audited here (out of this
  QC's scope; their packages are immutable and hash-pinned).

## QC-side artifacts

Counter-check scripts + logs (AUDITOR_COUNTERCHECK_A..E.py, countercheck_*_log.txt,
byte-safe re-run tree) persist outside the project tree at
`C:\Users\User\AppData\Local\Temp\opencode\qc_arg2_r1\`. The QC session performed ZERO
git mutations; HEAD == f239eb85cd0f56ae10cee52d57833a49f225965c before and after the QC;
staged paths 0; the untracked set is unchanged. This QC_AUDIT.md is the QC session's only
write inside the package (it is intentionally NOT covered by the executor's
MANIFEST_SHA256.csv, which freezes the executor's 30-file deliverable).

## NEXT STEP FOR PE-MASTER

Adjudicate. If the correction route is chosen, the P1-QC-1 fix (23,671 → 25,905 in
REPORT.md / HANDOFF.md / STAGE_ACCEPTANCE_GATES.csv G2 / ARG2_ANALYSIS.md) plus the two
P3 wording fixes can be carried by a small amendment (the raws stay untouched); on
PE-MASTER's adjudication, pe-master-auditor will persist the verdict + authorized
corrections and publish (G15) per the standing family convention.
