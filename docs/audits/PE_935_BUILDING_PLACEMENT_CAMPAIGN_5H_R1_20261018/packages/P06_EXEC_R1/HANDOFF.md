# HANDOFF — P06 (Front C) to PE-MASTER
# PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018 / packages / P06_EXEC_R1

## Status block

```text
RUN_ID            = PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018
PACKAGE_ID        = P06 (Front C)
RUN_STATUS        = COMPLETED_WITH_PROCEDURAL_INCIDENT (INCIDENT-P06-I1, disclosed below)
ADMISSION_ID      = A912213023006
QC_ORIGIN         = SELF_CHECK (executor's own; independent QC is the parent's separate phase)
HARD_STOP_REASON  = none (final closure at real-clock 2026-10-18T22:27:52.985Z+;
                    package hard stop 23:15:00Z not reached, ~47 min margin)
DEADLINE          = respected
CLOCKS            = RUN_STARTED 22:21:29.355Z real clock; 3 estimated stamps in first
                    writes corrected to values bounded by real readings (disclosed in
                    REPORT.md 6.9 and MANIFEST.json)
BUDGETS           = rows 92/98 OK; CALL 11/14 OK; candidates 4/4 OK; bodies 3-in-window vs 2 reserved (DEVIATION, window-contained, disclosed)
```

## ANSWER (a) — thunk 0x008BD720 dispatch result (for parent admission)

**THERE IS NO DISPATCH TARGET VA.** The complete body of 0x008BD720 (admitted window
0x008BD720-0x008BD740) is:

```
008bd720  LEA EAX,[ECX + 0x18]
008bd723  RET
```

No JMP, no CALL. It is not a dispatching thunk: it is a side-effect-free leaf that
returns the interior pointer `ECX + 0x18` to its caller (writes nothing, reads only
ECX). Evidence: EXTRACT_SUBREGION_A_008BD720_008BD740.txt rows 1-2 (pinned-listing
lines 1282626-1282627), verbatim re-read from the pinned source. Evidence level:
CONFIRMED (listing-level; body fully in-window). The "dispatches to target" premise is
REJECTED_WITH_EVIDENCE.

Consequence for the designed experiment: the {0x66,A} chain cannot continue through a
callee — it continues CONSUMER-SIDE: (i) which of the 3 imm32 registration sites
(006B6D05, 006C3FB0, 006D44E8 — navigation only, NOT read) stores the callback into
the {0x66,A} scheduler queue, and (ii) what consumes the returned &req+0x18 pointer.
Recorded for admission, not read: also 22 direct CALL sites of 008BD720 (full list in
REPORT.md section 9). The bridge's callback-imm32 pin (cited standing) is consistent
with a pointer-resolver callback shape.

## ANSWER (b) — slot-consumer 0x00848EA0 semantics table (in-window evidence only)

| Element | In-window semantics |
|---|---|
| Frame | MSVC SEH prologue; handler imm 0x00A28300 (recorded, NOT read); __try scope (trylevel 0/-1) wraps the 0x00844660->0x0043A550->0x0072F580 lookup chain |
| Consumes | FIRST STACK ARGUMENT (MOV EDI,[ESP+0x80]) = the slot(-container) object; the function is NOT thiscall-on-the-slot (wires ECX=EDI per call); provenance = sole in-listing caller 0x004E55F7 (NOT read) |
| Slot interface (in-window, all direct calls, class NOT_ESTABLISHED) | 0x00745540(slot,1)->bool (kind-of-slot flag; FALSE -> 0x00848FEC outside window); 0x00745BF0(slot)->ptr, null-checked (the id2/property channel ENTRY — the read is inside the callee: class-20006 tag-6 hypothesis UNVERIFIED here); 0x00745690(slot,0)->float st0 |
| Direct field reads | NONE in-window (all field access delegated to callees or on the out-of-window flag-2 path at >=0x00848FEC, where the bridge places the {u16@+0xC, float@+0x10} stores) |
| Does | flag-1 TRUE: P=0x00745BF0(slot); L=0x00843D60(&local,P); obj1=0x00844660(L); obj2=0x0043A550(obj1); EBP=0x0072F580(obj2) [keyed lookup label inherited]; local op 0x008E0110(&frame58); guard 0x0072FCE0(EBP)->bool; 0x0072FE30(EBP, buf1, buf2, buf3) fills three 12-byte float3 out-buffers (zero-init in-window); t=0x00745690(slot,0); R=0x006C1F90(ptr_a, ptr_b, ptr_c, t) (4 cdecl dwords) -> EAX -> 12-byte float triple |
| Produces (in-window) | the 12-byte float triple copied into frame locals; then JMP 0x00848FC6 (epilogue OUTSIDE window). Bridge's "store to slot+0x00" + "loop over 3 slots" live in the OUT-of-window regions (epilogue/flag-2) — inherited standing, NOT re-derived |
| In-window writes | FS:[0] + frame locals ONLY; no heap/global write in-window (callee aliasing unresolved = honest boundary) |
| Data sources (complete census) | arg1 (caller 0x004E55F7, unread); float const [0x00A7B25C]; MSVC cookie [0x00B9D8D0]; FS:[0]; returns of 11 unadmitted callees |

**FAMILY-P/T merge answer (scoped):** NO VFS-record-fed channel is visible IN-WINDOW
(CONFIRMED scoped negative; CONTROL-P06-N1). The merge question remains OPEN, narrowed
to exactly: (1) property provenance inside 0x00745BF0 (class-20006 tag-6 read),
(2) the class-20006 property-tag-6 WRITERS (bridge proposal 2), (3) slot-object
provenance at caller 0x004E55F7. Per the contract's own cost-benefit note, the writer
census is worth it only if (1) shows record-backed provenance — P06 found no file-fed
channel in-window, so (1) is the cheapest next discriminator.

## INCIDENT (procedural, disclosed)

INCIDENT-P06-I1: admitted window A contained an UNFORESEEN second body 0x008BD730
(`MOV AL,byte ptr [ECX+0x64]; RET`) not declared in body_entries. Per CONTRACT section 6:
reported, extract preserved, NO claims built on it, no region beyond the admitted VA
ranges opened, counters show 3 in-window bodies vs 2 reserved. Parent adjudicates.

## Actual counters (vs reserved)

bodies 3-in-window / 2 declared / 2 used-for-claims (reserved 2 — deviation disclosed);
rows 92 = A 4 + B 88 (reserved 98); CALL sites 11, all direct, 0 indirect (reserved 14);
unique call targets 11; candidate variants 4/4 (V1 dispatch-thunk REJECTED,
V2 pointer-leaf CONFIRMED, V3 in-window-VFS REJECTED, V4 flag-2-in-window REJECTED).
Out-of-window targets recorded NOT read: control 0x00848FEC/0x00848FC4/0x00848FC6;
callees 0x00745540, 0x00745BF0, 0x00843D60, 0x00844660, 0x0043A550, 0x0072F580,
0x008E0110, 0x0072FCE0, 0x0072FE30, 0x00745690, 0x006C1F90; data 0x00A28300,
0x00A7B25C, 0x00B9D8D0; callers (navigation) 22 CALL sites + 3 imm32 sites of
008BD720, 1 CALL site (004E55F7) of 00848EA0.

## Precise remaining edge (smallest next admissions)

1. {0x66,A} chain continuation: the three ~0x20-byte windows around 006B6D05 /
   006C3FB0 / 006D44E8 (which one registers 0x008BD720 into the {0x66,A} scheduler
   queue?) — and note the bridge C10 byte-pin may already localize the imm32 site
   (check parent's bridge C10 artifacts before admitting).
2. Property provenance: body of 0x00745BF0 (the id2/class-20006-tag-6 read).
3. Slot-object provenance: caller region of 0x004E55F7 (check bridge C2 census first).
4. Optional completeness: 0x00848EA0 epilogue/flag-2 at 0x00848FC4-0x00849040ish
   (store-to-slot+0x00 + loop + return construction; bridge standing currently
   carries these).

## Standing (unchanged by this package)

PLACEMENT_XYZ_RECOVERED=NO; world-instance identity NOT_ESTABLISHED;
CURSOR_SOURCE_MEDIUM=UNKNOWN; templates.vfs = DEFINITION registry only within censused
machinery; no standing promoted; MODEL_INSTANCE_BINDING unchanged.

## Paths

- FINAL_REPORT_PATH: D:\Eudoria_Reconstruction\99_Audits\PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018\packages\P06_EXEC_R1\REPORT.md
- HANDOFF_PATH: this file
- PRIMARY_EVIDENCE_PATHS:
  - EXTRACT_SUBREGION_A_008BD720_008BD740.txt (SHA256 E1557D0AAD625525C35548307D8FFBE90F1040FD14222A2014896707CF544CC2)
  - EXTRACT_SUBREGION_B_00848EA0_00848FC4.txt (SHA256 AC82259C022A70A8C86643AEA7BF6EA4C103413220C452768259D819EE9A274F)
  - CLAIMS.json, COUNTERS.json, MEMORY_AND_IDENTITY.json, BARRIER_BACKLOG.json, GATES.json
- MANIFEST: MANIFEST.json (written LAST, self-excluded)
- Child scope only: no parent CONTROL touched, no other package touched, no repo/Git
  operations, no publication (not assigned to this package).
