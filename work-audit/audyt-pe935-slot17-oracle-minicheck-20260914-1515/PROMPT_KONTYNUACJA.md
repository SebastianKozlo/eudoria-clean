# WORK-AUDIT (audytor: Work-Audit, audyt: audyt-pe935-slot17-oracle-minicheck-20260914-1515) - plik audytora, NIE jest czescia pracy wykonawcy.
# PROMPT DO KONTYNUACJI - do przekazania wykonawcy (pe-reconstruction) w nowej sesji.
# Oparte na: werdykt PE_MASTER_REVIEW SLOT17 R1 (MASTER_ACCEPTED, advisory), wlasnym audycie
# (REPORT.md, 77/77 bajt, re-derwacja COFF) oraz NEXT_EXPERIMENT z werdyktu.
# Nota dla human: ponizszy prompt jest w jezyku projektowym (EN) zgodnie z konwencja runow.

=== 8< === CUT HERE === 8< ===

RUN ORDER (direct PE-MASTER dispatch -> executor pe-reconstruction, NO_NESTED_TASKS)

RUN_ID: PE_935_NINODE_ABI_PREFIX_R2_20260914
RUN_CLASS: MATERIAL (bounded static mini-check, sequel to
  PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1_20260914, verdict B).
STATIC-ONLY: the Entropia client never runs. Era oracle code never runs.

## Purpose and single research question family

R1 established (MASTER_ACCEPTED advisory, my re-audit confirms every load-bearing number):
- Entropia NiNode primary vtable 0x00A8CCF4 has 47 slots; slot 17 (+0x44) = 0x007B5390 =
  recursive named-object lookup, STRONGLY_SUPPORTED_GETOBJECTBYNAME (status B).
- Measured ABI prefix: slot 0 vector deleting dtor, slot 1 scalar deleting dtor thunk,
  slot 2 GetRTTI -> +1 slot shift vs BOTH pinned oracles (GB112 GetRTTI@1, GB12 GetRTTI@1).
- Anchors consistent with the +1 shift: slot 16 ApplyTransform-shaped, slot 17
  GetObjectByName-shaped, slot 18 SetSelectiveUpdateFlags-shaped, slot 27 UpdateWorldData
  (GB112 slots 15/16/17/26).
- Slots 3..15 were NOT decoded - explicitly the reason the status is B, not A.

THIS RUN closes that gap or falsifies the model - both outcomes are results:

Q1: Decode, from physical Entropia.exe bytes ONLY (fail-closed SHA pin), the behavioral
    identity of vtable slots 3..15 (thirteen slots, +0x0C..+0x3C) of the NiNode vtable at
    0x00A8CCF4: one bounded decode per slot (signature/args from ret-n and arg use; return
    class; distinctive instruction patterns; RTTI/NiRTTI where applicable). No downstream
    traversal beyond one callee per slot when needed for classification (stop rule as in R1).
Q2: Test the +1-shift alignment model slot-by-slot: predicted identity for Entropia slot N
    (N in 3..15) = GB112 slot N-1 = GB12 slot N-2, with the GB12->GB112 delta being the
    source-proven GetGroup/SetGroup virtualization (GB12 slots 13/14). Produce a per-slot
    MATCH / MISMATCH / UNKNOWN table (02_ANALYSIS CSV). The model is FALSIFIED if any slot
    in 3..15 is structurally incompatible with the predicted method family; report
    falsification as a first-class result (it would mean Entropia carries extra virtuals in
    the prefix and the +1-shift model must be revised).
Q3: PRE-DECLARED PROMOTION CRITERION (decide BEFORE measuring, so the verdict cannot drift):
    FUNCTION_IDENTITY for slot 17 stays B unless ALL of:
      (a) all thirteen slots 3..15 decode as the predicted families with zero MISMATCH;
      (b) the full prefix 0..18 then forms a measured, contiguous ABI alignment;
      (c) a HUMAN-ADJUDICATED generation decision: even (a)+(b) do not establish era-exactness
          (Entropia has 47 slots vs 32/34 and a +0x14 class-tail delta); promotion to A
          additionally requires an era-exact oracle, which is OUTSIDE this run's pin.
    In other words: this run can at most upgrade the evidence quality of the alignment model;
    the B->A promotion requires the generation question, which is a separate, human-gated run.
Q4: Secondary (bounded): for each decoded slot, record the recursion/self-dispatch offset if
    the method recurses (expected: own slot +0x4*N) - these are cheap ABI anchors.

## Pinned identities (fail-closed; re-measure every one at run start and inside every script)

- Entropia.exe  D:\Eudoria_Reconstruction\pcg_install\Entropia.exe
  SIZE 8015872  SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31
- GB112 oracle  D:\gamebyroengine\Gamebryo 1.1.2 Evaluation\SDK\Win32\Lib\VC71\ReleaseLib\NiMain.lib
  SIZE 3073590  SHA256 FF4519AFD2475D9A6E71A35E5DB6B0F5A0B7E9E86EC3662C6A340DA19BA06597
- GB12 oracles  the six gb12_build .obj + Gb12_Source pins exactly as in R1
  (00_Control/SOURCE_IDENTITIES.json of R1 is INPUT; re-hash every pin yourself).
- Base: current origin/master at run start (record exact BASE_SHA + timestamp).
- INPUT-ONLY facts (from the R1 package on branch
  audit/pe935-ninode-slot17-gb-oracle-minicheck-r1, commit 5290e79): vtable VA 0x00A8CCF4,
  slot values, +0xCC/+0xD4 children offsets, slot 27/16/18 decodes, NiRTTI static init,
  GB112/GB12 maps. NEVER re-derive from untracked WIP; every Entropia claim must be
  re-measured from physical bytes by THIS run's own scripts.

## Isolation and hygiene (audit findings folded in - mandatory)

- New isolated worktree + branch audit/pe935-ninode-abi-prefix-r2 at BASE_SHA. Master
  untouched; no AUDIT_ENTRYPOINT change; path-limited single commit of the package only,
  then push, then HARD STOP (same publication discipline as R1).
- EVERY git-state observation (ls-remote, rev-parse, status) must carry a timestamp, and the
  final HANDOFF must state observations separately for "at run start" vs "at publication",
  explicitly noting any concurrent-session master movement. (Audit F1: R1's HANDOFF said
  "local master ... no drift" which was false at publication time due to the concurrent
  LINK30 commit - do not repeat.)
- HANDOFF per-directory census must be verified against the actual file list before commit
  (R1 said 03_EVIDENCE 15 / 06_REPORT 5; reality was 16/4 - audit F2).
- If ANY file is adopted from a prior/interrupted session rather than regenerated, list it
  explicitly with mtime in the honesty note (R1 carried over 4 scripts + GB12 locators
  without saying so - audit F3).
- Correct the entropia probe docstring: ImageBase 0x400000 reads at the STANDARD
  IMAGE_OPTIONAL_HEADER32 offset 0x1C; there is no "+4 shift" (audit F4). Reuse/adapt R1
  scripts freely - they verified correct - but fix the docstring claim.
- Manifest discipline as R1 (MANIFEST_SHA256.csv over all package files except itself;
  state that the manifest file itself is the +1 unhashed file; do NOT claim "35/35" style
  phrasing without defining what is counted).

## Evidence and gates

- Evidence layout as R1: 00_CONTROL (scripts + contract + source identities),
  01_RAW (raw disasm listings), 02_ANALYSIS (per-slot identity table + alignment CSV +
  negative controls + errata if any), 03_EVIDENCE (regenerated dumps + index), 06_REPORT
  (REPORT + STAGE_ACCEPTANCE_GATES + MANIFEST + HANDOFF).
- Gates G0..G9 in the R1 structure, PLUS:
  G10_PREFIX_ALIGNMENT: the per-slot MATCH/MISMATCH/UNKNOWN table complete for 3..15;
    every MISMATCH/UNKNOWN justified with measured bytes, not narrative.
  G11_PROMOTION_INTEGRITY: the Q3 pre-declared criterion restated verbatim in the report
    and applied mechanically; no post-hoc reinterpretation of (a)/(b)/(c).
- Negative controls: at minimum, for every predicted identity that has a distinct behavioral
  signature (e.g. LoadBinary vs LinkObject vs RegisterStreamables vs SaveBinary vs IsEqual
  vs GetViewerStrings vs AddViewerStrings vs ProcessClone vs PostLinkObject vs
  GetBlockAllocationSize), one measured rejection ground for the nearest wrong candidate.

## Expected outputs

- ANSWER: per-slot identity map 3..15 + the alignment verdict (model HOLDS / FALSIFIED /
  PARTIAL with exact per-slot statuses) + updated slot-17 evidence quality statement
  (status B remains unless the Q3 criterion fires).
- OBSERVED_OPERATION per slot; no semantic-role inflation; TRANSFORM_TO_MODEL stays
  NOT_DEMONSTRATED; the SceneFeeder consumer chain stays untouched (out of scope).
- After push: HARD STOP. No next experiment without new dispatch. (Candidate for a future,
  separately-gated run: engine-generation identification - Gb26 materials exist on disk but
  are OUTSIDE this run's pinned oracle set; adding them requires a human decision.)

=== 8< === CUT HERE === 8< ===

Noty human (PL): przed przekazaniem promptu rozwa? decyzje (1) czy utrwali? najpierw werdykt
SLOT17 R1 w repo (osobny bounded persistence run: PE_MASTER_REVIEW.md + wiersz LATEST RUNS),
z uwzgl?dnieniem finding?w F5/F6 z mojego audytu; (2) czy zgadzasz si? na pre-deklarowany
kryterium promocji B->A z Q3 (wymaga human-adjudication dla generacji silnika).
