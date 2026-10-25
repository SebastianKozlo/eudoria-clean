# MODEL INSTANCE PLACEMENT STATIC R2 — CLOSING REPORT

RUN_ID: PE2003_NATIVE_BINDING_INSTANCE_PLACEMENT_STATIC_R2_20261025
Closing authoring wave (exclusive-create): 2026-10-25T11:18:13Z (tool: python datetime UTC)
Author: pe-master-auditor under PE-MASTER direct order (CLOSING/AUTHORING mode; documents only; no new science; no frozen artifact modified)
Inputs: SCIENCE_ROOT B01_*/J01a_*/J01b_*/B02a_*/J02_*/P01_*/P02_*/J03_*/J04_* artifacts + QC/ dir; WORK_ROOT ledgers + jobs (read-only); AUTHORING_ROOT CONTRACT.md §10–11 + INPUT_PINS.json; governing postaudit D:/Eudoria_Reconstruction/99_Audits/PE2003_STATIC_PLACEMENT_DESKTOP_POSTAUDIT_R1_20261025/REPORT.md (SP-A01..09; SHA256 1946EABABD402BEAC7C7CCFDDD22FC640816A2D84535F97A629ABA3CA30DCBA4, re-verified MATCH in INPUT_RECHECK.json).

## 1. VERDICT

**CAMPAIGN_SCOPE_SETTLED (static depth reached) — science verdict per job family PASS; overall standing UNCHANGED and carried exactly:**

- **WORLD_XYZ_RECOVERED = NO** — no world placement of 296445/218757 recovered; no LOCAL→WORLD promotion anywhere.
- **HISTORICAL_PLACEMENT = NOT_ESTABLISHED.**
- **SOURCE = UNKNOWN** — neither local nor network exclusivity proven.
- **Object-instance network→model join = STILL_AMBIGUOUS** with exact missing edges (§5; CLAIMS R2-C31).
- **FAMILY-LEVEL join = ESTABLISHED** (loader create-fn 0x4077F0 and network writer FUN_005030c0 both target the vt 0x5E2A3C class; byte-verified installs 0x407896 / 0x405bdf — QC VC-03/VC-04 TRUE).
- **CANONICAL_GATE_EFFECT = NONE; ADVISORY_PENDING_EXTERNAL_POSTAUDIT.**
- **PE2003_LOCAL_SOURCE_EXHAUSTED = NO** (precise frontier in FRONTIER.md / BACKLOG.json).
- QC verdict for the run: **QC_PARTIAL** (QC_PE2003..._F1; 37 verification items all TRUE; rationale below).

Main B/J/P questions were resolved to the available static depth and sensible alternatives were checked (postaudit "next experiment" B/J/P executed: B01/B02a/J01a/J01b/J02/P01/P02/J03/J04); remaining edges are precisely scoped, not waived.

## 2. WHAT THIS RUN ESTABLISHED (claim matrix summary — full matrix in CLAIMS.json, 46 claims)

Tool-computed status counts (from CLAIMS.json): CONFIRMED 29, STRONGLY_SUPPORTED 6, UNVERIFIED 8, REJECTED 3 (PLAUSIBLE 0). Every claim cites its artifact + evidence; every CONFIRMED has an evidence pointer (self-review check, §8).

**B — binding / ID space (B01, B02a)**
- EXTN→executed-target mechanism fully qualified: chunk tables → def fields (+0x50/+0x54, +0x1c code, PFIX/DYN) → superclass resolve pass → EXTN bind pass FUN_00453e20 ADDS resolved values into code words → VM executes patched bytecode. Native fallback (manager+0x1C binder vcall `ff 55 08` @0x453F1B) exists for owner-1 native/builtin ids only (B01_RESOLVER_FLOW.json).
- **R1 "missing .obj for 2202/768/382" corrected to FILE_CLASS_PRESENT** — namespace error; raw members PROVEN byte-identical in Scripts.ark (2202.obj/768.obj/382.obj header offsets 1032200/4990079/2602823; CRC+SHA re-derived by QC VC-19/20/21/22).
- ext 33521 target CLOSED: 2202 DYN#0 code@532 (hash byte-equal to 1796 EXTN#23).
- 4508/4057 attach chain fully decoded (COMMON plumbing): per-part loop → ext 30298 → 1796@1016 → dispatch slot → ext 33521 → 2202@532; EXTN bijection 10/10 + 8/8, zero unmatched; 0 unknown opcodes (1419 items). Per-model data lives OUTSIDE the chain.

**J — binding → model → instance (J01a, J01b, J02, J03, J04)**
- DAT_A=FUN_005c27a0 (empty no-op), DAT_B=FUN_00561ee0 (forwarder to quaternion normalizer FUN_005541e0); writers = 15 lazy-init clone installers into the 20-slot fn-ptr table (beyond-raw BSS, SR 0xF000); receivers = fresh record buffers in FUN_005068f0.
- Model ids 296445/296446/218757/218758 present ONLY as DYN getters (STOREI literals), consumers cross the DYN dispatch boundary → **(e) MISSING_EDGE**; honest bounded negative: 13 target ids, 0 foreign raw hits in 1936 corpus files + EXE.
- [X+8] NIF root = NiNode block-0, vt 0x5E2A3C byte-pinned (create-fn 0x4077F0; loader registry 0x619E78; 3403 sites / 100 pairs census).
- GCE attach path byte-verified CLOSED (registry+0x3C AddChild; 69/69 byte checks). owner+0x1C writer+semantics pinned (FUN_005b3cf0 @0x5b3d09, value=FUN_00403e80(arg)); NOT the GCE hash registry; exact class OPEN.
- Part objects are VM objects — DISJOINT from the C++ node family (CM2 CONFIRMED).

**P — transform / authentic values (P01, P02)**
- X = 0x28 bytes; +0x6C/+0x70 live on the owner class 0x78 (vt 0x5EBBEC) and are **NIF_FILE_LOCAL** (NIF block reader FUN_005b38c0 region overwrites ctor defaults −1.0f from the file stream).
- NIF local transforms all identity (31/31 NiNode transforms across both files) — **no local placement data in the two NIF files**.
- node+0x2C = 3x3 rotation matrix; P01 MISSING_EDGE resolved by P02: writer = FUN_005030c0, network-reachable, writes translation (×100.0f) + matrix on vt-0x5E2A3C-class 0x130 objects.
- The network cursor mechanism itself (0x5bbca5 target) is DISJOINT (0x48 record[6] wire struct).

## 3. MANDATORY DISCLOSURES (per QC findings P1-1/P2-1/P2-2/P2-3/P3)

1. **(P2-1) B01 admission-trail gap.** B01's child admission events died with the dead prior session (ADMISSION_EVENTS starts at A1/ROOT_TAKEOVER; no B01 events). Compensation, verified: root A1-CC independent countercheck (seq=4: ark members, decoded pins, EXE key bytes — all PASS) and post-hoc admin HANDOFF synthesized by the J01a child on root order (WORK/jobs/B01/HANDOFF.md). The B01 science artifacts' load-bearing claims were independently counterchecked by root and later by QC (VC-19..22).
2. **(P2-3) J01b supersession map.** J01b_RECEIVER_FLOW.json (frozen, SHA256 25874C25EC1DFC02E47FCFF9F678EFFB6F94D32986A0DF2B58711E2AD1EF466E) claims X=0x28B owner-of-fields, X+0x14-no-writer and node+0x2C-quat — **superseded by P01** (X=0x28; fields on owner class 0x78 vt 0x5EBBEC; +0x2C=3x3 rotation matrix) **and J04** (X+0x14 writer = FUN_005b5380 @0x5b5433). J01b's flow/read-site claims (fld sites @0x506aab/0x506af0, executor semantics, COMMON verdict) **remain standing**. A reader citing J01b alone would take superseded facts as current canon — cite P01/J04 for X-class facts.
3. **(P2-2) LOC deviation.** P01 tool LOC 878 > 800 hard cap — disclosed at closure (seq=17 KNOWN DEVIATION), tools hash-pinned, not trimmed post-hoc. **MASTER disposition: ACCEPTED_AS_DEVIATION** (recorded in BUDGET_LEDGER P01 entry). Hand prose 181 ≤ 400.
4. **(P1-1) Budget ledger.** BUDGET_LEDGER contains an additive completion block (2026-10-25T11:12:45Z) enumerating every dispatch unit incl. dead attempts (spent keys: A1, B01, J01, A1-CC, J01a, J01b, B02_dead, B02a, J02, P01, P02, J03, J04, QC1; native_task_accounting: prior 4 + this 12 = 16 dispatches; dead_infra 3; family A2/B5/J7/P3/Q1). **SEMANTIC_BUDGET_COMPLIANCE remains UNVERIFIED (SP-A09)** — bodies/instruction exposures are not fully aggregated; the ledger's own note: "own aggregate UNMEASURED never yields budget PASS".
5. **(P3-1/2/3) VA errata (additive; frozen artifacts unmodified).**
   - The push-0x28 sites are actually **0x521b78 / 0x5b7256** (bytes `6a 28`); the VAs cited in P01 (0x521b94, 0x5b7272) are the ctor CALL sites, both targeting FUN_005b5110 (QC P3-2; premise CONFIRMED).
   - LEA +0x6C: instruction `8d 57 6c` starts at **0x5b3ca9** (0x5b3cab is the disp byte); +0x70 at 0x5b3cb9 (QC P3-1).
   - Census convention: J02 model-id `file_off` values (0x298/0x244/0x1C8/0x174) point at the id **operand dword**; the 12-byte instruction starts 4 bytes earlier (0x294/0x240/0x1C4/0x170) (QC P3-3). Future byte checks must cite the instruction start VA.
6. **(P3-4/5/6) Count/format conventions.** BUDGET_LEDGER "owner_rows: 7" counts CSV rows incl. header (6 classified data rows); seq=14 prose says "12 B02a/data files" but enumerates 11 and the directory contains 11 (all re-hashed, zero drift); ADMISSION_EVENTS.jsonl is a single strict-JSON object with an events[] wrapper, not JSON-lines.
7. **B02 dead attempts & J02 seq=14 incident.** B02 attempts 1+2 were infra-dead (zero artifacts); per attempt-cap the job was split to B02a with lineage (leads recovered from the dead sessions were treated UNTRUSTED and independently re-derived). During J02, the first run of the copied decoder executed unpatched and re-wrote 11 B02a/data files — deterministically **byte-identical** (all hashes match HANDOFF pins; QC VC-34 re-verified all 11); the incident is recorded at seq=14.

## 4. QC VERDICT AND ITS LIMITS

QC_RUN_ID QC_PE2003_NATIVE_BINDING_INSTANCE_PLACEMENT_STATIC_R2_20261025_F1 → **QC_PARTIAL** (started/finished 2026-10-25T11:08:34Z..11:20:00Z, tool-measured). All 37 independently re-derived verification items TRUE (QC_VERIFIED_CLAIMS.csv); corrections handled honestly (immutability + hash pins + downstream supersession verified); no forbidden overclaim wording found; WORLD_XYZ_RECOVERED=NO and family-level join limits maintained everywhere. QC_PARTIAL, not QC_PASS, because of P1-1 (budget coverage at QC time), P2-1, P2-2 and the explicit NOT_CHECKED load-bearing components (Ghidra decompilation correctness; J03 3403-site census re-derivation; J02 1936-file corpus scan re-run; opencode.db census; NIF block-map re-parse) — coverage algebra forbids QC_PASS (control 15 / L11). This closing carries every QC-mandated disclosure; the closing docs themselves are administrative, not new science, so the QC verdict for the science stands unchanged.

## 5. STILL_AMBIGUOUS — exact missing edges (not strengthened, not waived)

1. registry+0x3C root identity — whether owner+0x1C / the [X+8] NIF root is (or is under) the registry+0x3C tree (FUN_00468980 chain not followed) — the decisive instance-join edge;
2. class/ctor of the object stored at owner+0x1C (= FUN_00403e80(arg) of an unidentified cursor-array class; 190 indirect [reg+0x10] sites);
3. binder-patched HOSTCALL case ids binding def-ids 4652/4653 to native factories (runtime data; static residual = HOSTCALL case registration table);
4. ctx+0x50 append method (not load-bearing for the verdict).

## 6. PROCESS ACCOUNTING (from NATIVE_TASK_CENSUS.json; ledger-carried)

16 native dispatches (prior session 4: B01 a1 dead / B01 a2 emit / J01 a1 partial / J01 a2 dead; this session 12: J01a, J01a-fix, J01b, B02 a1+a2 dead, B02a, J02, P01, P02, J03, J04, QC1) of 96; dead infra attempts 3 (B02×2 + J01 attempt2); attempt-cap PASS (splits with lineage, no 3rd identical retry); root+children modelID=glm-5-3, zero high (SP-A06 respected); SP-A09 carried as UNVERIFIED.

## 7. INDEXES

- STAGE_ACCEPTANCE_GATES.csv — per-job gate table (B01/J01a/J01b/B02a/J02/P01/P02/J03/J04 G1+G2, all PASS with explicit non-pass classes, artifact SHA256s tool-computed).
- artifact_index.csv / MANIFEST_SHA256.csv — full bijection of SCIENCE_ROOT at seal (manifest LAST-but-one, self-excluded; SCIENCE_STOP.json written LAST and pins the manifest hash).
- EXTERNAL_DEPENDENCY_MANIFEST.csv — every external input with SHA256 (EXE, Scripts.ark + members, NIFs, decoded corpus files used, pinned R1/R2 artifacts, tools); INPUT_RECHECK.json — 36/36 rechecks MATCH at closing.
- BASELINE_CORRECTIONS.md, CORRECTION_LEDGER.json — R1 dispositions and in-run corrections.

## 8. SELF-REVIEWS

Two genuine independent passes (SELF_REVIEW_1.md, SELF_REVIEW_2.md) over the closing docs: claim-matrix vs prose consistency, every-CONFIRMED-has-evidence-pointer (programmatic check: 29/29 pass), no LOCAL→WORLD promotion, STILL_AMBIGUOUS not strengthened. Issues found and fixed before finalization: (SR1-F1) erratum-ID cross-reference inconsistency — docs cited "R2-E01/R2-E03" while CORRECTION_LEDGER used only "R2-CLR-09"; resolved by adding named errata sub-ids (R2-E01/E02/E03) to the R2-CLR-09 entry; (SR1-F2) a wrong artifact-name reference ("B02a_CONTAINER") in LOCAL_SOURCE_COVERAGE.csv corrected to B02a_CHAIN_DECODE.json (container_parse); (SR2-F1) EXTERNAL_DEPENDENCY_MANIFEST.csv was missing the preflight_readonly.py tool row used by the A1 baseline — added with live re-hash; (SR2-F2) the overclaim-term scan produced hits only as RETRACTION labels in BASELINE_CORRECTIONS.md §B.5 (quoted R1 overclaim names being retracted) — reviewed in context, no assertion of those claims.

## 9. STANDING OF THE SCIENCE (final, carried exactly)

WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; SOURCE_UNKNOWN (neither local nor network exclusivity proven); object-instance network→model join STILL_AMBIGUOUS with the exact missing edges above; FAMILY-LEVEL join established (0x4077F0 and FUN_005030c0 both target vt 0x5E2A3C; installs 0x407896/0x405bdf byte-verified); NIF local transforms all identity (31/31) — no local placement data in the two NIF files; +0x6C/+0x70 fields NIF_FILE_LOCAL; R1 "missing .obj" corrected to FILE_CLASS_PRESENT; DAT_A no-op / DAT_B quaternion-normalizer forwarder; 15 lazy-init clone installers; attach chain 4508/4057→1796→2202 fully decoded, bijection 10/10+8/8, COMMON plumbing; model ids as DYN getters with cross-dispatch consumers = MISSING_EDGE and the honest bounded negative (13 ids, 0 foreign raw hits in 1936 files + EXE). CANONICAL_GATE_EFFECT=NONE; ADVISORY_PENDING_EXTERNAL_POSTAUDIT; PE2003_LOCAL_SOURCE_EXHAUSTED=NO.

Publication (sanitized commit+FF push to eudoria-clean) is a SEPARATE later assignment; this report and seal do not publish anything.
