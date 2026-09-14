# HANDOFF.md — PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914 (executor return to PE-MASTER)

Executor: pe-reconstruction · Direct PE-MASTER dispatch · NO_NESTED_TASKS honored (no agents,
no loop-state changes, no gate waivers, no milestone actions). STATIC-ONLY: the client never
ran; engine-execution layer ABSENT. Publication NOT performed (separate step:
pe-master-auditor after PE-MASTER adjudication). Repo untouched (zero git mutations; only
read-only identity measurements).

## RUN_STATUS

**RUN_STATUS = B — 6/6 SceneFeederObject vtable slots decoded from the physical EXE; exactly
one slot (slot 3, FUN_0050A050) reads the corrected position SF+0x34..0x3C and copies the
triple to the caller's out buffer WITHOUT passing it into any call; slot 1 hands out &pos by
address; no slot passes position values into a call; no bridge claim made;
TRANSFORM_TO_MODEL stays NOT_DEMONSTRATED.**

- FINAL_REPORT_PATH: `D:\Eudoria_Reconstruction\99_Audits\PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914\06_REPORT\REPORT.md`
- PRIMARY_EVIDENCE_PATHS:
  - `01_RAW/SLOT_DISASSEMBLY.txt` (full disassembly of all 6 bodies — primary decode evidence)
  - `01_RAW/VTABLE_AND_SLOTS.txt` (physical vtable dump + own RTTI walk + slot map)
  - `01_RAW/POSITIVE_CONTROL_005094C0.txt` (window re-derivation: PASS)
  - `02_ANALYSIS/SCENEFEEDER_SLOT_CENSUS.csv` (the mandatory 6/6 census)
  - `02_ANALYSIS/ONE_HOP_FLOW.md` (minimal dataflows, stop-at-first-call)
- HARD_STOP_REASON: NONE (BASE_DRIFT, SOURCE_IDENTITY_FAIL, RUN_INVALID all not triggered)

## GATES

G1-SOURCE **PASS** (SHA e7785430…, size 8015872, i386/PE32/0x00400000 — own fail-closed S0).
G2-VTABLE **PASS** (own RTTI walk: vtable-4 -> COL 0x00AA12B8 -> TD 0x00B78834 ->
`.?AVSceneFeederObject@@`; vtable 0x00A7D458 in .rdata has EXACTLY 6 slots = the six contract
functions; extent ends at the `dPVS` data dword).
G3-COMPLETE-SLOT-CENSUS **PASS** (6/6 rows, all 19 columns, allowed vocabulary only).
G4-POSITION-ACCESS **PASS** (slot 3 value reads with raw instructions + in-run pointer
provenance via slot 1; slot 1 raw `lea` bytes; negatives fully evidenced).
G5-ONE-HOP-FLOW **PASS (vacuous)** (no position value enters any call; zero
MODEL/NiAVObject/ArkModelResourceInstanceRef/TRANSFORM_TO_MODEL/CANDIDATE_MODEL_BRIDGE
claims; callees not decoded — stop rule).

POSITIVE_CONTROL **PASS** — measured bytes at 0x005094C0:
`8B 44 24 04 8B 10 89 51 34 8B 50 04 89 51 38 8B 40 08 89 41 3C C6 41 28 01 C2 04 00` —
byte-exact vs contract-expected; 9/9 semantic checks PASS (arg-triple -> this+0x34/0x38/0x3C,
flag this+0x28=1, ret 4).

## THE FULL 6-SLOT CENSUS (inline; authoritative copy: 02_ANALYSIS/SCENEFEEDER_SLOT_CENSUS.csv)

| slot_index | function_va | function_name | body_start | body_end | reads_sf30 | reads_sf34 | reads_sf38 | reads_sf3c | writes_sf34 | writes_sf38 | writes_sf3c | takes_position_address | position_to_call | call_va | call_target | receiver | classification | evidence_ref |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0050A460 | FUN_0050A460 | 0050A460 | 0050A47E | N | N | N | N | N | N | N | N | N | (none) | (none) | (none) | NO_RELEVANT_ACCESS | SLOT_DISASSEMBLY#SLOT0 — deleting dtor shell; 0x50A463 call 0x50A240 (dtor body, not decoded); 0x50A470 call 0x95D42A = MSVCR80 operator delete (one-hop thunk resolve); zero window refs |
| 1 | 005090A0 | FUN_005090A0 | 005090A0 | 005090A4 | N | N | N | N | N | N | N | Y | N | (none) | (none) | (none) | NO_RELEVANT_ACCESS | SLOT_DISASSEMBLY#SLOT1 — lea eax,[this+0x34]; ret: ADDRESS-OF only, no value read (convention documented; address exposure carried by takes_position_address=Y) |
| 2 | 005090B0 | FUN_005090B0 | 005090B0 | 005090B4 | N | N | N | N | N | N | N | N | N | (none) | (none) | (none) | NO_RELEVANT_ACCESS | SLOT_DISASSEMBLY#SLOT2 — lea eax,[this+0x74]: outside window |
| 3 | 0050A050 | FUN_0050A050 | 0050A050 | 0050A0AA | Y | Y | Y | Y | N | N | N | N | N | 0050A064 | [SF+0x30 link]->vtable[+0x44] slot 17 (dynamic; class unknown in this run) | SF+0x30 link object (class unknown in this run) | MIXED | SLOT_DISASSEMBLY#SLOT3 + ONE_HOP_FLOW#slot-3 — primary: link read + virtual call (no position values involved); fallback: self-vcall vtable[1] (=slot1) -> reads X/Y/Z 0x50A090/98/9E -> copies to caller arg1 buffer 0x50A096/9B/A1; NO position value enters any call |
| 4 | 005090C0 | FUN_005090C0 | 005090C0 | 005090C7 | N | N | N | N | N | N | N | N | N | (none) | (none) | (none) | NO_RELEVANT_ACCESS | SLOT_DISASSEMBLY#SLOT4 — lea eax,[this+0x80]: outside window |
| 5 | 00509580 | FUN_00509580 | 00509580 | 00509598 | N | N | N | N | N | N | N | N | N | (none) | (none) | (none) | NO_RELEVANT_ACCESS | SLOT_DISASSEMBLY#SLOT5 — reads [this+0x18] (outside window); calls 0x4150F0/0x8B71D0 carry no window-field data; callees not decoded |

## PACKAGE_CENSUS

19 files, 120461 bytes total, MANIFEST_SHA256.csv = 18 rows (every file
except the manifest itself; no self-row; zero missing; zero duplicate paths). One transient
`__pycache__` (Python import side-effect) was REMOVED before manifesting — it is not part of
the package.

## NEXT_SEAM / NEXT TEST

NEXT_SEAM = NONE (status B; no position-to-call exists). The ONE next test (REPORT.md §6):
SF+0x30 LINK IDENTITY + SLOT-17 DECODE — writer-scan of [SF+0x30], RTTI-identify the stored
link object class, decode its vtable slot 17 ([vtable+0x44], the exact virtual target invoked
at 0x0050A064) down to the first call; max outcome label CANDIDATE_MODEL_BRIDGE; STATIC-ONLY.

## ENTRYPOINT_ROW_DRAFT (executor does NOT edit AUDIT_ENTRYPOINT.md; publication is separate)

> | (this commit; discover with `git log -1 -- docs/audits/PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914`) | PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914 (RUN_CLASS MATERIAL; the SceneFeederObject vtable slot census feeding the model-bridge decision; executor pe-reconstruction, direct PE-MASTER dispatch; NO_NESTED_TASKS; STATIC-ONLY — the client never ran; publication by pe-master-auditor after adjudication) | `PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914/` | The 6/6 slot census of SceneFeederObject vtable 0x00A7D458 (own RTTI walk: vtable-4 -> COL 0x00AA12B8 -> TD 0x00B78834 -> `.?AVSceneFeederObject@@`; the six contract functions ARE the complete vtable: slots 0..5 = 0x50A460/0x5090A0/0x5090B0/0x50A050/0x5090C0/0x509580; extent ends at the `dPVS` data dword): slot 0 = scalar deleting destructor (0x50A240 dtor body not decoded — stop rule; 0x95D42A = MSVCR80 operator delete via own IAT thunk resolve; zero window refs); slot 1 = POSITION-ADDRESS GETTER (`lea eax,[this+0x34]; ret`, bytes 8D 41 34 C3; takes_position_address=Y, no value read); slots 2/4 = address getters for OUT-OF-WINDOW fields +0x74/+0x80; slot 5 = reads [this+0x18] (out of window), forwards to 0x4150F0/0x8B71D0; **slot 3 = THE position reader (MIXED): GetPosition(out arg1, query arg2) — primary path (arg2!=NULL) reads the +0x30 LINK and virtually calls link->vtable[+0x44] slot 17 (0x50A064; dynamic target, class unknown; result+0x90 -> 0x437F70 -> 0x82B5A0 fill arg1), fallback path (arg2==NULL) self-vcalls vtable slot 1 (proven = the slot-1 getter) and reads X/Y/Z at SF+0x34/0x38/0x3C (0x50A090/98/9E) copying the triple to the caller's out buffer (0x50A096/9B/A1) — NO position value flows into ANY call**; positive control FUN_005094C0 re-derived byte-exact (arg triple -> this+0x34/38/3C + flag +0x28=1 + ret 4) = PASS; gates G1-G5 PASS (G5 vacuous: no position-to-call); FINAL STATUS B: slot 3 reads the position, does not send it to a call (classified MIXED: link read + position read; position sub-behavior READ-LOCAL); slot 1 exposes &pos; TRANSFORM_TO_MODEL remains NOT_DEMONSTRATED (no claim made); NEXT_SEAM = NONE; THE ONE NEXT TEST = SF+0x30 link identity (writer-scan of [SF+0x30] + RTTI of the link class + decode of its vtable slot 17 down to the first call; max label CANDIDATE_MODEL_BRIDGE) | PENDING (the PE-MASTER loop audit) |

## SELF_CHECK (executor's own, explicitly not the independent MASTER audit)

- Census completeness: 6/6 rows, all 19 columns, every disposition backed by a line in
  01_RAW/SLOT_DISASSEMBLY.txt (no report-only slots).
- Slot map derived exclusively from the physical .rdata dump (s1), independently re-derived
  inside s2 (assert slots == the six functions) — dual derivation, zero prior-report input.
- Body ends: every end has terminal RET + padding evidence + (for slots 0/3/5) independent
  next-function-start evidence (E8 callers of 0x50A480/0x50A0B0/0x5095A0); the slot-0
  over-sweep defect was caught and fixed BEFORE publication, and the corrected listing is
  the only published one.
- Negative controls: slots 0/2/4/5 are honest negatives (full listings show zero window-field
  refs); the "dPVS" extent check bounds the vtable; s3's byte-exact pattern check doubles as
  the decode-method validation (RUN_INVALID would have fired on mismatch).
- Dataflow stop rule: no callee body decoded; one-hop resolutions limited to the allowed
  classes (thunk: 0x95D42A -> MSVCR80 operator delete; function-start evidence only).
- No state mutated outside AUDIT_OUTPUT_ROOT; originals read-only; foreign untracked
  `experiments/` untouched; historical packages untouched; zero git mutations.
- Layer discipline: every claim in REPORT/ONE_HOP_FLOW carries its layer (BYTES/DISASM/ADJ);
  the one runtime-override caveat (virtual slot 1 in a derived class) is explicitly scoped to
  vtable 0x00A7D458 instances because engine execution is ABSENT.
