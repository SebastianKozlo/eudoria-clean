# P11 HANDOFF — to PE-MASTER (parent)

Run: PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018 | Package: P11 | Front C | RETRY 1 of 1 | no delegation
Worker root: D:\Eudoria_Reconstruction\99_Audits\PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018\packages\P11_EXEC_R1

## RUN_STATUS

COMPLETE. All contract §12 artifacts materialized in the package root. Prior-session files CONTRACT.json
(sha256 369059f6cbd181033b10d84c8276c28e4cf539cba392354c69cdfef2c9f191a0) and RUN_STARTED.json
(sha256 8c0203a31cedbfcc3987a0c6f80f271749bb55ad5d35cdf59fa84be7b07aca7d) preserved byte-identical.
Retry marker RUN_STARTED_RETRY1.json materialized at 2026-10-18T23:36:51Z (real clock). Package hard stop
2026-10-19T00:55:00Z respected; run completed well before stop.

## PRIMARY_EVIDENCE_PATHS

- EXTRACT_REGION_006B6C1B_006B6C9D.txt (sha256 cda76004453d5ca7a6390e6bee969079168c2e25f58c0e9a4d8838c61987cfae)
- CLAIMS.json (P11-C1..C8 with evidence/premises/countermodel/evidence_level + 3 unclaimed hypotheses)
- SOURCE_PINS.json (contract + source pin + context doc hashes, all verified)
- MEMORY_AND_IDENTITY.json | COUNTERS.json | BARRIER_BACKLOG.json | REPORT.md | GATES.json |
  artifact_index.csv | MANIFEST.json (self-excluded, LAST)

## WORKLIST PROVENANCE RESULT (the one question)

In-window (45 rows, CONFIRMED-as-instruction): the element list built by bodies 0x006B6C1B/0x006B6C5C is a
STACK-LOCAL DWORD-stride append buffer (cursor [ESP+0x38], bound [ESP+0x3c], pending slot [ESP+0x14]).
Its elements are the return values of two method calls on the CONTAINER FIELD [EDI+0x8] of an object of
unknown (out-of-window) provenance: producers 0x006C27A0 (stage A) and 0x006C27F0 (stage B), each wrapped by
a helper call 0x006B4120 (stack-temp this at [ESP+0x48]; args incl. incoming ECX, &[ESP+0x20], &[ESP+0x58], 1, 1).
Of the three offered provenance options (registry / template objects / container field), only **container
field** is supported in-window. Registry or template-object provenance for the elements is UNDECIDABLE
in-window — it lives entirely inside the two producer bodies (the 2 admission candidates). Scoped negative:
zero global/absolute memory references and zero registry-machinery calls inside the window.

## SCOPED RESULT (pump driver)

The {0x66,A}-forming pump 0x006B6C9D (P07-C3) is entered from 0x006B6C88 JZ exactly when the stage-B append
finds cursor == bound: within the window the pump is the OVERFLOW/FALLBACK ARM of the stack-local append state
machine — its TRIGGER is not the definition registry (CONFIRMED-as-instruction). The pump's A-DATA source
(keyed templates.vfs RB-tree lookup -> [record+0x08] read) remains STANDING_INHERITED from P07-C3 + bridge,
cited and NOT re-proven here (pump body out-of-window; only its entry row 0x006B6C9D PUSH 0x1 is in-window,
being the region's declared last row). The worklist feed itself is [EDI+0x8]-producer-fed with no in-window
registry access. Stashed-but-unappended element at [ESP+0x14] is a candidate pump input (hypothesis P11-H1,
unclaimed).

## OUT-OF-WINDOW TARGETS — exact VAs, RECORDED FOR PARENT ADMISSION, NOT READ

1. **0x006C27A0** — stage-A producer (method on [EDI+0x8]). Priority 1: decides worklist element provenance.
2. **0x006C27F0** — stage-B producer (method on [EDI+0x8]). Priority 1. (VA delta from producer A = 0x50;
   one admission window may cover both.)
3. **0x006B4120** — helper, called twice (this=[ESP+0x48]; incoming ECX arg = stage-A cursor on the
   A→B overflow path). Priority 2.
4. **0x006B6CB9** — stage-B append-success exit (JMP target from 0x006B6C9B). Priority 2: enclosing flow /
   possible loop latch.
5. **0x006B6C9F..** — pump body continuation after the in-window entry row (already covered by P07-C3
   standing; re-admission only if [ESP+0x14]-consumption proof is wanted).
6. **Enclosing function head < 0x006B6C1B** (VA unlocated in-window; not read) — would resolve EDI identity,
   buffer initialization, EBP role, loop structure.

## ACTUAL COUNTERS

bodies 2/2 (reserved 2) | instruction rows 45/60 (rows 632937–632981; no overshoot) | CALL 4/8 (distinct
targets 3: 0x006B4120 ×2, 0x006C27A0, 0x006C27F0) | candidates 2/2 (producers) | branches 6 (JZ ×4,
JMP ×2; out-of-window branch targets: 0x006B6CB9) | memory census: 16 stack-slot accesses, 2 [EDI+0x8]
reads, 2 indirect stores, 0 global refs | unforeseen in-window bodies 0 | incidents 0 | hypotheses recorded
not claimed 3.

## PRECISE REMAINING EDGE

Producer semantics: what 0x006C27A0/0x006C27F0 return and from where (registry walk vs container data vs
other) — the single discriminator for "is the worklist registry-fed". Secondarily: EDI/[EDI+0x8] container
class, helper 0x006B4120 role, buffer identity ([ESP+0x3c] static-capacity vs dynamic-end), EBP role,
loop-vs-straight-line, and whether the pump consumes [ESP+0x14]. Recommended next admission: 0x006C27A0 +
0x006C27F0 (one window; delta 0x50), then the enclosing function head.

## PREMISES (preserved, cited per claim)

identical names/shapes do not prove common semantics | definition registry != instance source |
no direct caller != exclusively virtual | scoped negatives keep window bounds.

## CHILD SCOPE ONLY

No nested task, no milestone action, no gate waiver, no repo/config/skill writes, no EXE/payload/Ghidra work,
no out-of-window reads. This handoff returns evidence to PE-MASTER for admission decisions and audit.
