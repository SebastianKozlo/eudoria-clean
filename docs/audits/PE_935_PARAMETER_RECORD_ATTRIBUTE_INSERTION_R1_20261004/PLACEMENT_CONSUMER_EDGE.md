# PLACEMENT_CONSUMER_EDGE — PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004 (PHASE F)

## The ONE question

Is the SAME inserted value — the registry value object that RECORD_A's parse created and
the insert stored ({key 16083 → value at node+0x14}) — actually read by the previously
established placement-builder path (per the contract: "FUN_00567770 via FUN_00567C50 and
the related established attribute-reader path where applicable")?

## Chain-1: RECORD_A's object IS read with a byte-pinned STATIC key by a placement-record constructor

```
FUN_005B6370 (attribute-flag-gated: FUN_00844020 checks 0x976/0xDDB/0xDCD with ECX=ESI
  — the established attribute-flag reader, byte-verified: MOV ECX,[ECX+4]; the tree find)
  └─ PUSH 0x3ED3 @0x005B6597            ← THE STATIC KEY = 16083 = RECORD_A's id2
     CALL FUN_005B5F90 @0x005B659C      (id2 pushed as param_1 → EBX)
        ├─ PUSH EBX; CALL FUN_0043A550 @0x005B5FE8   ← THE SAME REGISTRY (DAT_00BA1824)
        ├─ MOV ECX,EAX; CALL FUN_0072F580 @0x005B5FEF  ← THE SAME LOOKUP, key 16083,
        │    returns node+0x14 == THE OBJECT BUILT FROM RECORD_A'S PARSE (lookup identity:
        │    same registry root, same key domain, same key value)
        └─ PUSH EAX; LEA ECX,[local]; CALL FUN_005670A0 @0x005B5FFC
             ← FULL-FIELD READ of RECORD_A's object: id2, B, A, C, D_f32, list1, list2, f11
             copied field-by-field into the constructor's local
then FUN_00730F60/FUN_00730F90/FUN_0096C630/FUN_00730FB0/FUN_00797280(record, 16083)
→ FUN_004148F0 → FUN_00457930 (registration) → FUN_0050A690(...) [post-registration
consumer; its ECX provenance is stack-state-dependent and left UNRESOLVED this run —
non-load-bearing] → FUN_00567030 (update-queue push family)
```
FUN_005B5F90 constructs PLACEMENT RECORDS (the same record family/setters/registration/
queue-push as the named builder FUN_00567770; the BRIDGE R1 canon names
FUN_00567170/FUN_005B5F90/FUN_00567770 together as "the placement-construction
machinery"). Every edge above is byte-pinned and QC-verified (QC-9).

**But FUN_005B5F90 is NOT "FUN_00567770 via FUN_00567C50"** — it is a sibling
constructor driven by FUN_005B6370. Per the contract's warning ("Do not assume every
reader of the parameter system feeds this builder"), no claim is made that FUN_005B5F90
feeds FUN_00567770.

## Chain-2: the contract's named family — three byte-pinned structural findings

### 2a. The named builder FUN_00567770 itself reads the SAME registry — with a RUNTIME key

```
FUN_00567770 (builder)
  └─ CALL FUN_004C5580 @0x005678BA   (census-verified: 10 call sites; this one in the builder)
      ├─ FUN_004C5480(param_1) @0x004C55B5 (exactly 1 call site)
      │   └─ [C2-corrected layered identity — CLASS_SELECTOR vs PROPERTY_TAG; the prior
      │      "reads the entity's 0x4E26-PROPERTY value = the id2" wording conflated two
      │      distinct identities:]
      │      1. exact receiver: tree resolve CALL FUN_00843DD0 @0x004C54B2
      │         (instruction start C1/P3-corrected — @0x004C54AD was mid-stream);
      │         MOV EAX,[EAX] @0x004C54B7 (the resolved receiver);
      │      2. CLASS_SELECTOR 20006: pair built with the constant 0x4E26 (=20006):
      │         MOV [ESP+0x1C],0x4E26 @0x004C54C2 (C7 44 24 1C 26 4E 00 00) +
      │         MOV [ESP+0x20],EAX @0x004C54CA (the exact receiver), resolved by the
      │         wrapper CALL FUN_00703B80 @0x004C54CE — a CLASS-SELECTOR-20006
      │         resolve operation, NOT a property-tag fetch of 20006;
      │      3. branch predicate: the normal branch is gated by the flag-0xD82
      │         alternative (PUSH 0xD82 @0x004C54DC → FUN_00844020 @0x004C54E4) —
      │         the alternative/fallback branch is preserved as SEPARATE/UNKNOWN;
      │      4. PROPERTY_TAG 6 getter on the audited normal branch:
      │         exact receiver MOV ECX,[EAX+4] @0x004C551C; PUSH 6 (6A 06)
      │         @0x004C551F; CALL FUN_0070C180 @0x004C5523 (rel32 byte-verified) →
      │         returned descriptor/variant (null-check TEST ECX,ECX @0x004C552B;
      │         predicate CMP ECX,1 @0x004C552F; value read MOV EAX,[EAX+8]
      │         @0x004C5539 on the measured branch);
      │      5. the returned RUNTIME VALUE — the id2 key used below. NOT every getter
      │         result comes from the normal tag-6 branch (see 3).
      ├─ CALL FUN_0043A550 @0x004C55D2 (THE SAME REGISTRY)
      ├─ MOV ECX,EAX; CALL FUN_0072F880 @0x004C55D9 (lookup-with-copy, this run's decode:
      │    mapfind(key) → node+0x14 or default 0x00BA5800 → FUN_0072FCE0 validity
      │    (id2≠0 && (A≠0||B≠0||C≠0)) → FUN_0072F7A0(out, template) = FULL-FIELD COPY
      │    of the registry object into the caller's buffer)
      └─ the copied object lands in the builder's local ([ESP+0x80]-region); the builder
         then reads its B via FUN_00746550 ([ECX+4]) @0x005678C9
```
So the builder's own call tree READS the same container with the same lookup family and
copies the full value object — **but the lookup KEY is a runtime value** (the value
returned by the class-selector-20006 / property-tag-6 getter on the exact receiver and
branch — a SPECIFIC getter result, not any 20006-family constant). Whether the runtime
key ever equals 16083 is NOT statically
provable. (The all-encodings imm32 scan found NO static 0x3ED3 anywhere inside
FUN_00567770/FUN_00567C50 — the only static 0x3ED3 is the Chain-1 PUSH.)

### 2b. The named driver FUN_00567C50's own tree reaches a STATIC-KEY registry read — on a DISJOINT key set

```
FUN_00567C50 (driver; called by the three established drives: FUN_00514EF0(virtual)/
  FUN_0058DB50/FUN_005B72C0 — census: call sites 0x00515345/0x0058E0B7/0x005B7567)
  ├─ CALL FUN_00567770 @0x0056836C (the builder — verified)
  └─ CALL FUN_00567B40 @0x00567D24 and @0x00567D54 (the capacity-gated queue push,
      called with D as the argument — the established ERRATA_R4 canon, byte-verified)
      └─ FUN_00567B40 branch (A-getter == FUN_00844130 filter result; capacity logic):
          FUN_00844130 (attribute-family transform filter) + FUN_00566100 (position reader)
          → CALL FUN_00567170 @0x00567C3E (EXACTLY 1 caller)
              └─ FUN_00567170: registry lookup with a STATIC key selected from
                 {0x3BDB=15323, 0x3BD9=15321, 0x3A40=14912, 0x3A47=14919, 0x3BDA=15322}
                 (MOV-imm32 sites @0x005671E1/0x00567273/0x005672D2/0x00567303/0x00567339 —
                 byte-pinned; note: 0x3A40=14912 is a completeness addition to the
                 historical E9 key list) → CALL FUN_0072F580 @0x0056736D →
                 CALL FUN_005670A0 @0x0056737A (FULL-FIELD READ of the looked-up object)
```
So the named driver's own call tree DOES read registry objects with byte-pinned static
keys — but that key set is DISJOINT from RECORD_A's key 16083 (and all five records
exist in the file — container-level census fact; not analyzed as records).

## Verdict (anti-over-claim, family-faithful)

- The same-value READ is byte-pinned CONFIRMED on Chain-1 — but on a placement-record
  constructor (FUN_005B5F90) OUTSIDE the contract's named family.
- Inside the named family: the mechanism (same registry, same lookup family, same value
  layout, full-object copy) is byte-pinned CONFIRMED, but the specific-record key
  identity is runtime-dependent (2a) or targets a disjoint record set (2b).
- Therefore:

**PLACEMENT_CONSUMER_EDGE = STRONGLY_SUPPORTED** (not CONFIRMED)
**PHYSICAL_RECORD_TO_PLACEMENT_ATTRIBUTE = NOT_ESTABLISHED**

No S2 is claimed. Even a hypothetical S2 would NOT prove world instance / static
placement / XYZ / model association (contract).

## FIRST_MISSING_EDGE

**INSERTED_VALUE_TO_PLACEMENT_CONSUMER** — specifically [C2-corrected wording]: the
provenance of the RUNTIME KEY at the named builder's lookup, i.e. the producer of the
SPECIFIC RUNTIME VALUE returned by the class-selector-20006 (CLASS_SELECTOR 0x4E26 =
20006, pair @0x004C54C2 → FUN_00703B80 @0x004C54CE) / property-tag-6 (PROPERTY_TAG 6,
PUSH 6 @0x004C551F → CALL FUN_0070C180 @0x004C5523) getter on the EXACT receiver and
branch whose result is consumed as the FUN_0072F880 lookup key. Can that specific value
ever be fed from a physical record (RECORD_A's id2 16083 in particular)? If yes,
Chain-2a closes to CONFIRMED for the named family; if not, the named family's registry
read stays confirmed-as-mechanism but never record-keyed statically.

## NEXT EXPERIMENT (recommendation ONLY — designed, NOT executed)

[C2-corrected experiment identity — supersedes "Decode the WRITERS of the 0x4E26
(20006-family) property value", which chased a conflated identity.] Trace the
producer/provenance of the SPECIFIC RUNTIME VALUE returned by the
class-selector-20006 / property-tag-6 getter (FUN_004C5480 → pair 0x4E26 @0x004C54C2
→ FUN_00703B80 @0x004C54CE → exact receiver → branch predicate → PUSH 6 @0x004C551F
→ FUN_0070C180 @0x004C5523) on the exact receiver and branch whose result is consumed
as the FUN_0072F880 lookup key. Allowed provenance outcomes (OPEN taxonomy, no forced
physical-vs-network binary): PHYSICAL_RECORD_DERIVED | CONSTANT_INITIALIZATION |
LOCAL_COMPUTED | CACHE_PROVIDER | MESSAGE_DERIVED | FALLBACK_BRANCH | UNKNOWN.
Alternative/fallback branches (e.g. the flag-0xD82 path) are preserved as
SEPARATE/UNKNOWN — do NOT assume all getter results come from the normal tag-6 branch.
This is the single experiment that addresses FIRST_MISSING_EDGE directly.
(Also observed, RAW_OCCURRENCE_ONLY, no consumer role claimed: the imm32 0x3ED3/0x3ED2
appear in a property-machinery idiom at 0x0050F383/0x0050F2F3 inside the 0x0050Fxxx
CWO-handler-region function — `MOV [ESP+0x1C],0x3ED3` + CALL FUN_0042EAD0 — a possible
second lead for the same experiment; it must not be treated as a registry key without
parser proof.)
