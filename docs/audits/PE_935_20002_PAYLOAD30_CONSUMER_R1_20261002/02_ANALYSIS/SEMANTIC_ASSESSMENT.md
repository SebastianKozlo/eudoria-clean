# SEMANTIC_ASSESSMENT — PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002

STATIC_ONLY; RUNTIME=NOT_TESTED. Statuses from the contract taxonomy
(CONFIRMED|STRONGLY_SUPPORTED|PLAUSIBLE|UNVERIFIED|REJECTED). The three axes are
reported SEPARATELY per §12.
Correction state: DESKTOP_CORRECTION_R1 (the OBSERVED_OPERATION instructions below are
the SELECTED reader's; the RUN_STATUS is corrected to CONSUMER_UNREACHED per the
branch-selection correction; see 06_REPORT\AMEND_LOG_DESKTOP_CORRECTION_R1.md).

## FIELD_IDENTITY = CONFIRMED (structural identity; byte-proven)

The value at payload+0x30 of a 20002.vfs record is, structurally:

- the VALUE of the TLV entry with **tag 0x11 (tag ID 17)** — the LAST of the six property
  entries present in every record of the file (1366/1366 machine-verified);
- a 4-byte scalar per the class-20002 property schema (descriptor for tag 0x11 =
  {type 1, flags 0xC0, field 21}, byte-pinned registration at 0x76170F..0x761727);
- the payload of a record belonging to the parameter file of class 20002, whose
  registered client class object is **ArkObjectClassImpl<class_ArkParameterArmor,20002>**
  (RTTI-confirmed in the pinned binary).

"Structural parse closure is not semantic closure": this identity says WHAT slot the
value is, not what it MEANS.

## OBSERVED_OPERATION = CONFIRMED (instruction-level, byte-pinned — SELECTED reader)

The client operation on the value is a **pure copy (opaque propagation)**:
1. 4-byte little-endian load from the record payload at offset 0x30
   (`MOV EAX, dword [EDX+EAX*1]` @ VA 0x00977807, bytes 8B 04 10, in FUN_009777F0 — the
   SELECTED type-1 scalar reader of the generic property parser, reached through the
   proven virtual branch: descriptor+0 != NULL -> [vtable+0x14] slot -> 0x009777F0; the
   reader object's RTTI class is ArkRTTraitsInt);
2. store into the freshly constructed ArkParameterArmor instance's value-array
   slot 21 (`MOV [EDX], EAX` @ 0x00977810, bytes 89 02; destination address =
   instance->[+0x40] + (tag 0x11 + 4)*4 = value_array+0x54);
3. the instance is then registered in the class instance map by record id.

No comparison, arithmetic, branch, lookup, or transformation is applied to the value
at any traced instruction. The width (4) and endianness (LE) of the field are RAW
measurements from the selected client instruction (x86 dword load).

(The pre-correction text pinned the read to FUN_00412540 @0x00412553 / store
@0x0041255A. Those instructions are byte-correct but belong to the NON-SELECTED
FALLBACK path, reachable only when descriptor+0 == NULL — which is not the tag-ID-17
state. Superseded as the observed-operation attribution; preserved as labeled fallback
evidence in 01_RAW\DESKTOP_CORRECTION_R1\FALLBACK_PATH_RECORD.json.)

## FINAL_SEMANTIC_ROLE = UNVERIFIED (bounded wording below)

Bounded wording: "the payload+0x30 value is a per-record 4-byte scalar property value
(TLV tag 0x11) of the ArkParameterArmor / class-20002 parameter records; the client
copies it into the corresponding ArkParameterArmor instance's property slot 21, where
it is exposed to the client's generic property-read machinery. WHICH gameplay
behavior (if any) consumes this property at runtime, and what the property represents
in game semantics, was NOT established in this bounded run."

Status: **UNVERIFIED** — the epistemic baseline (§3:
20002_VFS_PAYLOAD_PLUS_30_FINAL_SEMANTIC_ROLE = UNVERIFIED) is NOT lifted, because:

- no in-run evidence identifies the property's game meaning (no reader with a static
  tag-0x11 immediate was identified within the 202-site bounded census; runtime
  consumers are tag-variable-driven and outside the bounded census);
- the §2-forbidden semantic labels (id2, template ID, resource ID, model ID, NIF ID,
  object ID, instance ID, world-placement ID, network ID, foreign key, pointer,
  offset, coordinate, world-instance->model edge) were NOT applied: none is
  re-established from in-run evidence. Numerical coincidences (e.g., the prior
  AMEND_R2 observation that 1,364/1,366 of these values are members of the
  templates.vfs id2 domain) remain CONTEXT ONLY (membership count; no significance
  language; id2-domain correlation stays CANDIDATE / UNVERIFIED — numeric-domain
  overlap is not semantic proof; see 02_ANALYSIS\BLAST_RADIUS.md).

## KEY_ROLE / LOOKUP_CONTAINER / RESULT_TYPE / RESULT_CONSUMER (§11)

Not applicable: the traced mechanism is NOT a lookup. The value does not enter any
map, registry, or container as a key at the traced instructions — it is stored as a
property value in the instance's own slot array. (The instance ITSELF is keyed by
record id in the class map, but that key is the record id, not the +0x30 value.)

## RUN_STATUS

CONSUMER_UNREACHED — the destination field (the ArkParameterArmor instance's tag-0x11
property slot 21) was reached and is byte-proven (the branch-selection correction
proves the selected reader chain: routing CONFIRMED; the selected client read
CONFIRMED; the store CONFIRMED), but NO downstream consumer of the slot was
identified: within the inspected 202 direct descriptor-lookup sites and the
documented limited context window, no tag-ID-17 downstream reader was identified;
full downstream static data-flow, aliases, indirect calls and global writer/read
completeness remain UNVERIFIED; further static resolvability is NOT_ESTABLISHED.
The GAMEPLAY semantic role remains UNVERIFIED (per the separate FINAL_SEMANTIC_ROLE
axis), and no world/model/placement edge is claimed or demonstrated.

(The pre-correction RUN_STATUS = CONSUMER_REACHED_ROLE_STRONGLY_SUPPORTED is
SUPERSEDED by this correction: it treated the destination slot as "the consumer"
under a path-selection claim that the Desktop post-audit falsified. The slot is the
destination field, not the downstream consumer; the downstream-consumer question is
honestly answered NO — see 06_REPORT\AMEND_LOG_DESKTOP_CORRECTION_R1.md.)
