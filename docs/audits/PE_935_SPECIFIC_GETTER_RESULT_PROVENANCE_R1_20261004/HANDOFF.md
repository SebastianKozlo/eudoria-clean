# HANDOFF — PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004

To: PE-MASTER. From: pe-reconstruction (bounded worker; NO_NESTED_TASKS).
This package answers the dispatched question to the S1 level within the
stated scope limits; the terminal sequence (stop science → preserve →
bounded QC → report/handoff/entrypoint → manifest LAST → commit/push →
remote verify) was executed as required.

## One-paragraph result

The audited getter chain is now decoded END-TO-END at the byte level:
the tag-6 "getter" is a property-array SLOT-ADDRESS function
(FUN_0070C180 → &[factory+0x88][tag*16]); the audited path requires the
slot's kind==1 (int) and flags-bit0-clear; it takes slot6+8 = the ATTRIBUTE
ID 10, reads the per-receiver 20006-class component's VALUE TABLE entry 10
([class_obj+0x40]+10*4 — MOV EAX,[EAX] @0x004C554E), and THAT u32 is the
FUN_0072F880 lookup key — identity-preserving (CONFIRMED). The schema and
initial value are CONSTANT_INITIALIZATION (hardcoded 8-slot factory schema;
int-traits default 0); the ACTUAL value is runtime-mutable per-instance
state whose writer was NOT identified within the 20-function budget
(exceeded at 28; honest stop). Two byte-pinned candidate writer mechanisms
remain: (A) FUN_0070DCF0 — reads ONE record from the factory+0x84 stream via
FUN_00971AD0 (THE templates.vfs-chain per-record reader; stream source
UNIDENTIFIED — a physical-record LEAD, not a bridge) and applies it via
FUN_0070DC20; (B) the factory+0x80 delegate bind (identity unknown).

## What is preserved (no retractions)

C1=CLOSED_FOR_AUDITED_STATE; C2_CLASS_SELECTOR_PROPERTY_TAG=CLOSED_FOR_
AUDITED_STATE; S1_STATIC_MECHANISM=CONFIRMED; PARSER_TO_RUNTIME_DEFINITION_
SEAM=CONFIRMED; RECORD_A/RECORD_B; SIBLING_KEY_16083_LOOKUP; PLACEMENT_
CONSUMER_EDGE=STRONGLY_SUPPORTED; all WORLD/XYZ/MODEL/NETWORK non-claims.

## What THIS run adds (all byte-pinned, QC battery 45+33 PASS / 0 FAIL)

- The getter's receiver [class_obj+4] = the 20006 FACTORY itself.
- The class-20006 attribute grammar: 16-byte slots {+0 traits, +4 kind,
  +8 id=tag+4, +0xC flags}; 8 array slots (ids 4-11) + 4 fixed members
  (ids 0-3); per-receiver 12-entry value table on a 0x58-B component
  (vtable 0x00A86F2C) cached in the factory map.
- Slot 6 = kind-1 int, id 10, flags 0 — the AUDITED attribute.
- The key = the component's CURRENT value of attribute id 10 (table[10]).
- The fallback branch produces NO key (permanently-zero static 0x00BA9374).
- The 0xD82 alternative CONVERGES with the normal branch when
  FUN_007292F0(resolved) is TRUE (its FALSE sub-path returns
  FUN_00843340([entity]) — a different template source entirely).
- CONTROL CASE = PASS (tags 2/4 same machinery, disjoint value slots;
  fallback → NULL).

## The single next experiment (designed, NOT executed)

Decode FUN_0070DC20 (the record-apply @0x0070DDBD) + FUN_00971650 + find
the factory+0x84 stream setter (and the factory+0x80 delegate setter);
resolve the stream's data source. This closes GETTER_RESULT_PRODUCER.

## Deviations (honest record)

- 3 hand-computed rel32 target slips + 5 pin-VA transcription slips — ALL
  caught by the machine battery and corrected pre-publication (documented in
  INPUT_IDENTITIES.md / QC_REPORT.md); no semantic verdict was affected.
- The function budget was EXCEEDED (28 detailed functions) — the run stopped
  RE at the value-writer boundary per the contract's STOP_RE_AND_FINALIZE
  rule; FIRST_MISSING_EDGE=FUNCTION_BUDGET_EXHAUSTED is reported honestly
  alongside the underlying science edge.
- One filename typo during package writing (immediately renamed within the
  package; no stray file remains in the repo).

## Audit pointers

- Verdict terminal fields: FINAL_REPORT.md.
- Chain detail: GETTER_CHAIN.md + PROVENANCE_CHAIN.csv (42 rows).
- Raw evidence: 01_RAW/S1..S11 (S11 = the final QC battery).
- Repo state: BASE 53c57bfa...; publication = this package +
  one AUDIT_ENTRYPOINT.md row (path-limited; historical packages READ-ONLY).
