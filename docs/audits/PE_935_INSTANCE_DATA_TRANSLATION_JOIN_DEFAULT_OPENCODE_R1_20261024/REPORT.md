# REPORT — INSTANCE DATA / TRANSLATION / RESOURCE JOIN (DEFAULT/MEDIUM)

RUN_ID: PE_935_INSTANCE_DATA_TRANSLATION_JOIN_DEFAULT_OPENCODE_R1_20261024
ROOT_SESSION: PE_MASTER_INTERACTIVE_TUI_THIS_SESSION (exact CLI session id not exposed to tooling; no parent_id fabricated)
ERA: PE_EU_9_3_5_SAVED_ONLY_PLUS_LIMITED_EXE_RDATA_VTABLE_READ (§9-compliant, see EXE_READ_LEDGER)
MODEL: nask-glm default/medium for root and all children; REQUEST_EFFORT=NOT_OBSERVED; SERVER_EFFECTIVE_EFFORT=UNKNOWN.

## Main question
Record -> instance -> model/resource -> actual translation: close several consecutive hops of the historical building-instance chain in one campaign.

## Science results (claims N1-N13 in CLAIMS.json; per-claim evidence there)

1. PARSER AND FRAME (A01): parser 007453D0 has exactly ONE caller — 004C47F0 @004C483D; the stream object {base,end,cursor,valid} is a caller argument from the dispatch chain (004B18D0 -> 004574F0(ESI=cursor) -> 004C47F0). Record >= 0x5D B: +0x00 u32 id, +0x04 method-field, +0x0C embedded sub-stream, +0x34 u16, +0x38 vec3#1 (12B), +0x44 vec3#2 (12B), +0x50/+0x54 u32, +0x58 f32, +0x5C u8; per-field bounds gate, default+invalidate on failure. Selector [F+0x44] (creator arg2): NO_DEF_IN_WINDOW (004C4952..004C4A01, 76 rows); rec+0x04 in {20020,20024,24009} gates the unseen 004C49BF block (B03).
2. BOTH 12B FIELDS (A02): independent, byte-exact: rec+0x38 -> def+0x08 (setter 00730F90, getter 00746560); rec+0x44 -> def+0x14 (setter 00730FB0, getter 0040B070 stateless address-return).
3. TARGET AND CONSUMERS (A03): target_this = M32[B+0xC0] (one dereference); 005094C0 = verbatim vec3 store (target+0x34..0x3C + dirty +0x28); 00509510 = verbatim copy (target+0x74..0x7F) + relay 0096CDD0 -> 36B block (target+0x4C..0x6F); wrapper path: &B+0x44 -> 005094C0, &B+0x50 -> 00509070, &B+0x5C -> 00509510.
4. MATH (A04): 0096CDD0 = rotation-triple -> rotation-shaped 3x3 matrix builder (|x0^2-1|<=eps single-axis fast path; angle-addition general branch; 0095da1c/0095da28 identity UNVERIFIED; Euler-vs-quaternion UNRESOLVED).
5. CLASS B (A05/A05b/A05c/A05d/A05e): wrapper class B: ctor 00528E50 installs vtable 0x00A7DCB0 (after base-init 0085B1B0, base vtable 0x00A91E4C); record object at [B+0x10]; managed target at [B+0xC0]; vtable slots (EXE §9 read): +0x24=00528300, +0x28=00528320, +0x2C=00528340. def+0x14 additionally copied to B+0x11C (positional delta use, NOT orientation).
6. RECORD->TRANSFORM CHAIN (B02): PROVEN_ON_SHOWN_DATAFLOW: in base-init 0085b1b0, def vec1 -> B+0x44/0x48/0x4C [SHOWN]; def vec2 -> B+0x5C/0x60/0x64 [SHOWN] (+duplicate 0x68..0x70 via stateless getter); then wrappers -> consumers: TRANSLATION_CANDIDATE (verbatim, axis/units UNKNOWN) / SCALE_CANDIDATE / ORIENTATION (rotation-triple). Parser-rec->def edge INHERITED_FROM_PIN (QF2); creator->ctor hop INFERRED (QF3).
7. INSTANCE/MODEL JOIN (B03): PARTIAL: record id (rec+0x00) is BOTH the 008544D0 lookup key (payload -> holder-class-UNKNOWN object +0x00; payload = class-B candidate) AND the factory-record id (00853A50 verbatim store -> creator 004C46C0 @004C4952) — per-instance creation keyed by id. Missing: L1 manager identity (E2), L2 payload=model-root (lead: payload+0x0C typed sub-object [+0x20]==3), L3 unseen continuation (004C4981/004C4A9D), L4 rec+0x50 interior, L6 0085B84F. The 4508->A296445->296445.nif precedent: NOT shown on this chain (neither confirmed nor refuted as destination).
8. RECORD SOURCE (C01/C02/C03): static chain network dispatch -> message cursor -> 004C47F0 -> parser [SHOWN]; queue->cursor bridge NOT_ESTABLISHED (bounded negative: purge walker 008329a0 is a deallocator, not a dispatcher; indirect dispatch/wait-side consumer/multi-stage re-push not excluded). MEMORY_RECORD = RUNTIME_PARSED_FROM_MESSAGE_CURSOR; PHYSICAL_SOURCE_MEDIUM of VALUES = NOT_ESTABLISHED (materialization != origin).
9. CACHE/PROVENANCE (D01 pinned via T01; D03): cache plaintext 180; English Strings part0 3949 members (u32 count-prefix; R13 skipped ID1); CRC32 3949/3949; roundtrip 3949/3949; 180 joins; unresolved UTF8 IDs 3196/4135/4136; EXACT_CACHE_ERA=UNVERIFIED (candidate EU2008/9.2.2.2 REPORTED_ONLY; tree EXE is a different binary; copy dates non-dating; later-than-9.3.5 NOT_SUPPORTED).

## QC
QSCI_A = QC_PARTIAL (QF1-QF7 applied); QCI_B = QC_PARTIAL (QB1-QB6 applied; INC-5 relocation); QCI_C = PASS; QACCOUNT = QC_PARTIAL (F1-F5 bookkeeping fixed). All QC fresh contexts, independent session GLMs.

## Failed / empty attempts
A01b attempt1 and A04 attempt1 returned empty results; both retried successfully; no STOP_JOB remained.

## Incidents (all disclosed)
INC-1 A01a rows 214/180; INC-2 A03 H5 286/140; INC-3 A05b ~790/150; INC-4 C02 findstr ~500 (00838f9b/00839d90 candidates flagged for re-derivation); INC-5 B03 wrote to authoring root (evidence relocated; authoring tree restored). No retroactive cap changes; global caps far from exhausted.

## Verdicts
SCIENCE_VERDICT = PARTIAL_PASS_WITH_PROVEN_RECORD_TO_TRANSFORM_DATAFLOW_AND_HONEST_BOUNDED_NONPASSES
PROCESS_VERDICT = COMPLIANT_WITH_DISCLOSED_INCIDENTS (bookkeeping corrections applied after QACCOUNT)
WORLD_XYZ_RECOVERED = NO
HISTORICAL_PLACEMENT = NOT_ESTABLISHED
EXACT_CACHE_ERA = UNVERIFIED
REPORTED_PENDING_EXTERNAL_POSTAUDIT = yes (this publication is not canonical acceptance)
CANONICAL_GATE_EFFECT = NONE

## Frontier
See FRONTIER.json: #1 payload class/model-root join; #2 queue->cursor bridge (with re-derivation caveat); #3 selector [F+0x44] / rec+0x04 gate semantics.
