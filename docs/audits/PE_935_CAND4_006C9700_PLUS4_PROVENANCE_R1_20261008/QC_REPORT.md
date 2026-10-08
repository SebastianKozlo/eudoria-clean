# QC_REPORT — PE_935_CAND4_006C9700_PLUS4_PROVENANCE_R1_20261008

**QC_RUN_ID** = PE_935_CAND4_006C9700_PLUS4_PROVENANCE_R1_20261008_INTERNAL_QC_R1
**QC_ORIGIN** = pe-master-auditor **fresh-context internal QC** under direct PE-MASTER
dispatch (contract §6). This is NOT a Desktop post-audit
(NEW_DESKTOP_POST_AUDIT = NOT_PERFORMED) and is NOT independent of PE-MASTER —
it is the run's internal QC phase. QC_VERDICT (bottom) is an internal-QC
result, NOT MASTER_ACCEPTED and NOT milestone closure.
**Worker** = pe-master-auditor session (fresh context; first contact with this
package was this dispatch). Executor of the audited package = pe-reconstruction
(executor phase; QC_ORIGIN for that phase = NOT_PERFORMED_BY_EXECUTOR — honestly
recorded by the executor; verified).
**Inputs** = contract OPENCODE_FUN006C9700_PLUS4_MICRORUN_R2.md (read in full,
336 lines; SIZE 17487 / SHA256 A6ABFE5E155F3FBAECDCC52E9D9A5E2B18D4286E67192C1C6717B3899EA2B20C —
measured MATCH by the QC before any package read), the 22-file package (ALL
read in full by the QC), and the physical EXE (full re-measure below).
**BASE/REPO** = LOCAL_HEAD == origin/master == EXPECTED_BASE_SHA
97823c6180b0a35a8f5c43e45c29076d48208bee (re-measured by the QC; the package
is untracked, unstaged; zero tracked changes; foreign untracked paths untouched
— consistent with the executor's SOURCE_STATE §8).

---

## 1. Method

1. **Identity gates first**: contract SIZE+SHA256 measured before reading;
   physical EXE fully re-measured (fail-closed) BEFORE any byte use:
   `Entropia.exe` = **8,015,872 B / SHA256
   E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31** — MATCH
   with the pinned identity in the task, the contract §2.5 and the package.
2. **Full package read**: all 22 files read to EOF (list in §8/§9); no file
   was taken from memory or summary.
3. **Independent implementation**: the QC wrote its own PE32 mapper
   (`qc_independent_check.py`; `QCPE`), which — unlike the executor's
   `OwnPE` — distinguishes RAW from the virtual zero-init tail
   (`VIRTUAL_BSS`); own fail-closed identity; own pin reads; own rel32/rel8
   arithmetic (call_va + 5 + int32; branch + 2 + int8); own RTTI chain walk;
   own string reads. **No disassembler was used by the QC** — instruction
   identities were verified from the byte encodings (opcode/modrm arithmetic),
   which is an implementation lineage DISJOINT from the executor's capstone.
4. **Corruption controls re-run**: the QC's OWN corruption bytes (different
   from the executor's) on in-memory copies + the same PRODUCTION gate
   (checker_plus4.run_checks) + the QC's own independent pin gate; direct
   file-offset MC6 variants; physical EXE SHA256 re-measured after all
   controls (unchanged).
5. **Adjudication layers**: claim matrix CL-1..CL-22, ledger rows, ceilings
   and budgets re-adjudicated by content (not just sums) from the raw
   evidence + QC measurements; machine-readable record in
   `00_CONTROL_INTERNAL_QC/QC_RESULTS.json`.

## 2. Real origin / session / independence lineages

| layer | lineage |
|---|---|
| **bytes** | QC's own PE32 mapping + own fail-closed EXE identity + own reads of the physical EXE. Expected values taken from the raw claims in the package and the QC task list, then compared byte-for-byte. No report/CSV/JSON was used as a byte source. |
| **decoder** | NONE used by the QC. The executor's capstone 5.0.7 decode was checked AGAINST THE PHYSICAL BYTES, not against a second decode; the QC verified instruction encodings by hand (opcode/modrm) — the same facts the executor's MANUAL_ENCODING_CROSSCHECK records, re-derived independently. |
| **dataflow** | QC re-derived the return-path/branch algebra from the physical bytes (15/15 rel8, 19/19 rel32 own recomputes). Claim adjudication is the QC worker's own (fresh context). |
| **scope adjudication** | QC enumerated every callsite of the four opened bodies from the byte-verified hex (12 charged + 9 RAW = complete census of the opened extents) and re-adjudicated every ledger row's CONTENT (interpretation text, NOT_COUNTED_REASONs, charges, extents). |

Independent-evidence hierarchy honored: original bytes + independent
measurements > independently generated evidence > project derivatives >
reports > summaries > memory. The QC's own byte reads are the top tier; the
executor's package artifacts are audited objects, never QC inputs.

## 3. Anchor recheck table (own mapping, own byte read; full machine table in QC_RESULTS.json)

26 load-bearing anchors re-measured from the physical EXE — **26/26 MATCH,
0 mismatches**. Key rows:

| anchor | VA | measured | expected | verdict |
|---|---|---|---|---|
| CAND-4 caller callsite → FUN_006C9700 | 0x006C6FFC | E8 FF 26 00 00 | E8 FF 26 00 00 (rel32 +0x26FF) | MATCH (own rel32 → 0x006C9700) |
| store [manager+0x6C] | 0x006C7008 | 89 46 6C | 89 46 6C | MATCH |
| installer [R+4]→T load | 0x006C67BE | 8B 78 04 | 8B 78 04 | MATCH |
| installer T→[manager+0x68] | 0x006C67E2 | 89 7E 68 | 89 7E 68 | MATCH |
| ADD [EDI+4],EBX pin | 0x006C67E7 | 01 5F 04 | 01 5F 04 | MATCH (ADD, not INC) |
| EBX=1 establisher | 0x006C67C9 | BB 01 00 00 00 | BB 01 00 00 00 | MATCH (MOV, not INC) |
| new(0x10) size push | 0x006C97B9 | 6A 10 | 6A 10 | MATCH (R = 16 B ≠ W = 0xC) |
| ctor call rel32 → FUN_006E8F70 | 0x006C97D8 | E8 93 F7 01 00 | — | MATCH (own recompute 0x006C97DD+0x1F793 = 0x006E8F70) |
| ctor return-this | 0x006E9014 | 8B C6 | 8B C6 | MATCH |
| pump return R | 0x006C9808 | 8B C6 | 8B C6 | MATCH |
| **THE [R+4] writer** | 0x006E8FA5 | 89 46 04 | 89 46 04 | MATCH |
| ctor addref [P+4],ecx | 0x006E8FAF | 01 48 04 | 01 48 04 | MATCH |
| [R+0]=S store (no vptr) | 0x006E8F9D | 89 06 | 89 06 | MATCH |
| slot pre-clear | 0x006C95A0 | C7 06 00 00 00 00 | same | MATCH |
| slot = P swap-in | 0x006C9651 | 89 3E | 89 3E | MATCH |
| setter addref [P+4],ebx | 0x006C9657 | 01 5F 04 | 01 5F 04 | MATCH |
| setter → FUN_007B79B0 | 0x006C9631 | E8 7A E3 0E 00 | — | MATCH (own recompute → 0x007B79B0) |
| hist. FUN_006FA8B0(W,R) prior record | 0x006CB836 | E8 75 F0 02 00 | E8 75 F0 02 00 | MATCH — the CORRECTED transcription is the physically true one (rel32 +0x2F075 → 0x006FA8B0); the executor's caught-and-disclosed first-draft error (E8 35…) is confirmed as corrected |

Additionally: **19/19 rel32** (12 counted-edge targets + RAW arith + 5
prior-scope re-pins) and **15/15 rel8 branch targets** independently
recomputed — zero mismatches. All four body windows (0x11C / 0xB8 / 0xFF /
0x60 bytes) byte-identical to the physical EXE. RTTI W chain independently
re-walked: vtable 0x00A864B8 → COL 0x00AA7770 (sig 0) → TD 0x00B8CAC4 →
`.?AVArkModelResourceInstanceRef@@` — correctly used for W only, never for R.
Strings re-read: "Geowater:0" @0x00A85DA4, "ArkTexture" @0x00A859F8,
"ArkAnimation" @0x00A8547C, empty string @0x00A7957B — all MATCH.

## 4. Claim adjudication (CLAIM_MATRIX CL-1..CL-22 — content, not shape)

**All 22 claims ACCEPTED as within their evidence class** (machine table:
QC_RESULTS.json → claim_matrix_readjudication). Highlights of the classic
error-class hunt (all negative — no violations found):

- **R+4/T+4 base confusion: NONE.** R+4 (writer 89 46 04, base ESI=R) and
  T+4 (installer incref 01 5F 04 @0x006C67E7, base EDI=T) are kept on
  separate bases; the T==P alias (CL-13) is PROVEN by dataflow (this run's
  measured store + the prior-record installer load on the same base R),
  explicitly adjudicated as roles from two recorded callers — NOT one
  observed execution. Wording verified.
- **Assumed alias: NONE.** CL-13/HP-3 cite the store and the load
  byte-measured; the R!=T/R!=W differences are size-verified (0x10 vs 0xC).
- **Class-by-name / nearby-RTTI: NONE.** CL-7 verified by the QC's own
  enumeration: the ctor's ONLY R-base stores are 89 06 ([R+0]=S — an
  argument POINTER), 89 46 04 ([R+4]=P — an argument pointer) and TWO ZERO
  immediates (C7 07 00 00 00 00 → R+8; C7 46 0C 00 00 00 00 → R+0xC). A vptr
  store would require a non-zero vtable immediate — none exists in the
  construction dataflow. R's class name UNKNOWN is therefore CONFIRMED as a
  byte-verified negative, not an assumption. W's RTTI name is never
  transferred to R (CTRL_A/CTRL_C upheld).
- **Static-possibility-as-observed: NONE.** "A static path is NOT an observed
  execution" is carried in the trace, the ledgers and FINAL_REPORT; the
  old-release branch is correctly described as existing-but-not-executed on
  the recorded first-install path.
- **Refcount-vs-INC mislabeling: NONE.** BB 01 00 00 00 (MOV ebx,1) + 01 5F
  04 (ADD [base+4],reg) verified from encodings at all sites; no INC claim
  anywhere.
- **Oracle promoted to PCG status: NONE.** CL-16/CL-17 stay PRIOR/cited;
  CL-19 preserves all 13 standing statuses verbatim; CL-20/CL-15 report
  THIS run's measured resolutions ([R+4]=P pointer; H-2 relation) as run-local
  measured results for the parent's adjudication — which is exactly the
  contract's preserve-until-the-evidence-concerns-exactly-that-claim rule;
  no top-level promotion is claimed anywhere.

## 5. Ledger re-adjudication (row content, not only sums)

- **Bodies 4/6 — HONEST.** B-1..B-4 windows byte-verified; extent proofs
  re-pinned (ret C3 @0x006C981B; ret 8 @0x006E9027; ret 8 x2
  @0x006C962E/@0x006C966C; B-4 PARTIAL cut 0x007B7A0F). The
  RAW_WINDOW_OVERFLOW neighbors are displayed raw and NOWHERE interpreted
  (QC full-read confirms); the not-opened list with reasons is accurate.
- **Edges 12 counted + 9 RAW — HONEST and COMPLETE.** The QC enumerated every
  call instruction in the four opened extents from the byte-verified hex:
  pump 8 callsites (E1..E8), ctor 5 (E9, E10, R-1..R-3), setter 5 (E11, E12,
  R-4..R-6), P-getter head 3 (R-7..R-9) — 12 + 9 = complete census; **no 13th
  unit exists**, so the 12/12 limit was never exceeded. Every
  NOT_COUNTED_REASON is genuine: no interpretation hides behind a RAW label;
  R-3's receiver fact is explicitly declared body-dataflow (not a callee
  claim); R-7/R-8 explicitly REFUSE to transfer the operator-new identity
  from prior canon to the getter's site; R-4/R-5/R-6 make no claim about
  their sites. **STOP_BEFORE_EXCEED at the FUN_007B79B0 boundary is real**:
  the continuation was not decoded, and no claim is made past the window cut.
  E12 is honestly charged for the off-CAND-4 variant interpretation. The
  prior-scope re-pins (0x006C6FFC, 0x006C7049, 0x006CB7CF, 0x006CB81B,
  0x006CB836) are byte re-reads without new callsite interpretation —
  correctly uncharged.
- **Writers 2/4 — HONEST.** PW-1/PW-2 byte-verified; PW-3 correctly NOT a
  writer (the boundary row). The later-overwrite negative (CL-10) matches the
  QC's own [x+4]-write enumeration of the opened bodies (PW-1 is the only
  R+4 destination; all others are refcount ops on base P/old).
- **Hops 3/3 — HONEST.** Each hop cites byte-verified instructions; prior
  manager stores are explicitly not charged; HP-3 is a legitimate
  interpreted role-transition (adjudication of two recorded flows); no 4th
  hop exists in the package.
- **Prohibited scope — COMPLIANT.** No decode record, pin or claim anywhere
  in the package for FUN_006C8BB0 / FUN_007B6C30 / FUN_007BF900 /
  FUN_007BF630 / FUN_007BF470 / the join implementation; no runtime evidence;
  no transform/XYZ/visual-role search; no decoder hardening; no
  AUDIT_ENTRYPOINT.md touch (HEAD and tree state confirm).

## 6. Controls re-verification

- **Clean production gate, independent re-run: 80/80 PASS** (0 fails) — the
  executor's documented clean pass is reproduced by the QC.
- **MC1 (+4 writer anchor)**: QC used its OWN corruption bytes (89 46 04 →
  **89 47 04**, different from the executor's 8B 46 04) on an in-memory
  copy; the same production gate FAILed with
  `PIN:CTOR_R4_STORE_P: @0x006e8fa5 expected 89 46 04, got 89 47 04` — the
  corruption is detected AT THE EXACT ANCHOR. PASS.
- **MC4 (ctor rel32 anchor)**: QC used its OWN bit-flip (operand byte+2
  ^= 0x02: 93 F7 **01**→**03**, different from the executor's byte+1 flip);
  own rel32 → 0x006E8D70 ≠ 0x006E8F70; the same production gate FAILed with
  `REL32:REL_PUMP_CTOR_R: rel32 +0x1f593 -> 0x006e8d70 != expected
  0x006e8f70`. PASS.
- **MC6 (specificity)**: QC corrupted TWO unpinned .rsrc bytes by DIRECT
  file offset (0x7A1100, 0x7A1200) — anchor gates stay PASS both times; and
  replayed the executor's exact VA corruption (@VA 0x00BA1100 → AA) —
  anchor gates stay PASS. The specificity conclusion holds. (See finding
  F-2 for the mapping-boundary nuance: the executor's stated VA lies in the
  .data virtual tail; its corruption lands on a .rsrc byte via the checker's
  max(vsize,rsize) mapping — the control's OUTCOME is valid, its VA label is
  the mapping artifact.)
- **CTRL_A..CTRL_G**: verified against contract §6 definitions and against
  the actual run decisions: each control's fixture uses the REAL evidence
  shape (no rubber stamps — the rejection paths are the real ones: R has no
  vptr edge; the alias T==P is accepted only in its proven form; the W name
  is not transferred; the pointer-vs-count resolution is measurement-based;
  the named-lookup receiver claim stays at call-site level; ownership stays
  ONE_REFCOUNTED_REFERENCE with the manager's separate receiver; the missing
  closure stays UNKNOWN with no promotions). All are labeled
  SYNTHETIC_LOGICAL_CONTROL and are NOT presented as new physical PCG
  measurements. PASS.
- **Physical EXE immutability**: SHA256 re-measured after all controls —
  unchanged (E7785430…F31). All corruptions were in-memory copies.

## 7. Status ceilings — verified

| ceiling | package status | QC verification |
|---|---|---|
| deeper origin of P | NOT_ESTABLISHED_WITHIN_BOUND | verified (PW-3; body #4 PARTIAL; R-7..R-9 RAW; no claim past 0x007B7A0F) |
| S/O identity | NOT_ADJUDICATED | verified (bodies unopened; no identity claim) |
| R class name | UNKNOWN (no vptr) | **verified by QC's own store enumeration** (2 arg-pointer stores + 2 zero immediates; no vtable immediate in the construction path) |
| P/T class names | UNKNOWN | verified (runtime vtable; site unopened) |
| release-on-destroy | NOT_CHECKED | verified (neighbor destructor RAW display only) |
| T downstream | NOT_ADJUDICATED | verified (no downstream trace) |
| transform owner / coordinate frame | NOT_ADJUDICATED_BY_THIS_RUN | verified (prior status preserved) |
| standing science (contract §7, 13 statuses) | preserved verbatim | compared word-for-word across CL-19 / FINAL_REPORT §14 / HANDOFF / SOURCE_STATE §5 — identical; no promotion |
| REAL_SCIENCE_AUTO_QUALIFICATION | DISABLED | respected (publication ≠ acceptance; no auto-promotion) |

## 8. Budget consumption of THIS QC

**0 new units of any class.** Bodies 4/6 (QC opened no new range — pins of
already-charged bodies only); edges 12/12 at limit (QC performed NO new
callsite interpretation — all rel32/rel8 recomputations are free
repetitions of already-charged or RAW-arith units); writers 2/4 (no new
writer hunted or found); hops 3/3 (NO new hop interpretations, per the
dispatch). Within the QC shares.

## 9. Coverage / FULL READ LOG / NOT_CHECKED

- **Full read**: the contract (336 lines) + all 22 package files to EOF
  (every 01_RAW file, all 6 ledgers/CSVs, CONTROL_RESULTS.json, both scripts,
  all 4 reports) — see the machine log in QC_RESULTS.json
  (coverage_full_read_log).
- **NOT_CHECKED by the QC (explicit)**: (a) the two pinned external reports'
  internal content — QC relied on the executor's recorded identity
  measurements (administrative inputs, not byte sources of this run's
  science); (b) the 263-file historical-package blob census was not re-hashed
  in full by the QC — instead the QC independently re-measured the
  load-bearing prior-canon bytes (installer/producer/historical-caller pins
  and rel32) from the physical EXE, all MATCH; (c) the live remote
  (ls-remote) was not re-queried by the QC worker (no publication in this
  phase; the executor's transient-failure disclosure was reviewed and is
  honestly scoped). HEAD/origin/master equality re-verified.

## 10. Open findings (none contradicts a load-bearing result)

- **F-1 (P3) — notational residue**: 01_RAW/PINS_AND_REL32.txt line 90
  contains the fragment `8B F0?` in the hist_caller_null_check row. QC
  counter-measure: physical bytes @0x006CB811 = **85 F6** (TEST ESI,ESI) —
  the cited prior record is correct; the fragment is a leftover, not a
  measurement. No effect on claims.
- **F-2 (P2) — checker mapping boundary (tooling precision; zero effect on
  this run's gates)**: `checker_plus4.OwnPE.va_to_off` uses
  `max(vsize, rsize)` without a raw-size boundary, so VAs in the .data
  zero-init tail (raw end RVA 0x7A0000, vsize end 0x7A9CE4) — e.g. VA
  0x00BA1100 (MC6) and any runtime-initialized global like 0x00BA73BC — are
  mapped onto physical file bytes of .tls/.rsrc instead of being classified
  VIRTUAL_BSS. QC counter-measurement: own section table (RSZ 0x34000 → raw
  end 0x7A0000) + own mapper returns VIRTUAL_BSS for both VAs. For THIS run
  all 80 gate checks operate on raw-backed VAs (clean 80/80 re-verified),
  so NO result is affected; MC6's conclusion (anchor gates stay PASS on
  unrelated corruption) is re-verified with direct file-offset corruptions
  AND the executor's exact VA replay. Correction for the NEXT checker
  generation: bound va_to_off by raw size; re-label MC6 as a direct
  file-offset .rsrc corruption. (This package is read-only for the QC; no
  change made.)
- **F-3 (P3) — notational arithmetic residue**: 01_RAW/PINS_AND_REL32.txt
  line 111 reads `-0x2701+... = 0x26FF rel32` for callsite 0x006C6FFC. QC
  counter-measure: physical bytes E8 FF 26 00 00; own rel32 = **+0x26FF**
  (0x006C7001 + 0x26FF = 0x006C9700 — target correct); "-0x2701" is an
  incorrect residue (would target 0x006C6900). The checker recomputes from
  the physical bytes and passes; no gate affected.

## 11. QC VERDICT

**QC_VERDICT = QC_PASS** — return/source identity, used bytes, status
ceilings and the content of the whole scope ledger independently verified:
26/26 anchors, 19/19 rel32, 15/15 rel8, 4/4 body windows, RTTI/strings,
clean 80/80, MC1/MC4 (QC's own corruptions) + MC6 (direct offsets + replay),
CTRL_A..G content checks, ledgers honest and complete (12+9 edges; 4 bodies;
2 writers; 3 hops), ceilings all hold, standing science preserved verbatim,
0 new budget units consumed. Three minor findings (F-1/F-3 P3 notation;
F-2 P2 tooling-precision with zero effect on this run's gates) are disclosed
for the parent's adjudication and the next checker generation.

*This verdict is the run's internal QC result. It is not MASTER_ACCEPTED,
not milestone closure, and does not authorize any follow-up science.
REAL_SCIENCE_AUTO_QUALIFICATION = DISABLED; publication remains the parent's
phase. The QC worker did NOT perform a Desktop post-audit
(NEW_DESKTOP_POST_AUDIT = NOT_PERFORMED).*
