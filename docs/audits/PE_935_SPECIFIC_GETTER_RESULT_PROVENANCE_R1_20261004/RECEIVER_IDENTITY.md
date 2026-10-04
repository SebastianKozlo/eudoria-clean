# RECEIVER_IDENTITY — PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004

EXACT_RECEIVER_IDENTITY = STRONGLY_SUPPORTED (structural chain byte-pinned;
the concrete runtime object is runtime state; one boundary function
FUN_00747970 was surface-identified only — not decoded within the budget).

## The receiver chain (all edges machine-verified)

1. **The entity** — FUN_004C5480's arg1, delivered by FUN_004C5580's arg1,
   which the builder FUN_00567770 passes at its call site @0x005678BA.
   Within FUN_004C5480: MOV EDI,[ESP+0x30] @0x004C54A5 (EDI = entity).

2. **The resolved receiver** — FUN_00843DD0(entity, &L) @0x004C54B2:
   `MOV ECX,[ECX+4]; TEST ECX,ECX; JE→zero; PUSH &L; CALL FUN_00747970(
   [entity+4], &L); MOV ECX,[EAX]; *out = ECX`. So:
   - if [entity+4] == NULL → resolved = 0 (getter path then feeds pair
     {20006, 0} to the selector; the class component is still resolved —
     the selector caches per RECEIVER KEY, and a NULL receiver is a
     legitimate key value);
   - else resolved = the object returned through FUN_00747970 on the
     entity's [+4] child. FUN_00747970 was NOT decoded this run (budget);
     its semantic label (e.g. "get owner/avatar/scene node") is UNKNOWN.

3. **The pair {CLASS_SELECTOR=0x4E26=20006, resolved receiver}** — built at
   0x004C54C2/0x004C54CA and resolved by FUN_00703B80 @0x004C54CE
   (singleton FUN_00415470 @0x00703B88 → FUN_00703D70 @0x00703B8F →
   FUN_0073C870(20006) @0x00703D7D → [0x00BA590C] factory →
   FUN_0070E100(factory, receiver) @0x00703D8F).

4. **The class component (class_obj)** — the PER-RECEIVER 20006-class object:
   - 0x58 bytes (allocator FUN_0073B8C0, alloc PUSH 0x58; ctor
     FUN_007374C0: calls FUN_00735E70(class_obj, factory, arg) then sets
     vtable 0x00A86F2C);
   - [class_obj+4] = THE FACTORY (MOV [EBX+4],ESI @0x0070D9A5);
   - [class_obj+0x40] = a 12-entry, 4-byte-element VALUE TABLE
     (ids 0..11; init FUN_00412C50; entries written at creation with
     traits defaults);
   - cached per receiver in the factory's map at +0x0C, keyed by the
     receiver POINTER value (FUN_004D1430 key = *(u32*)&receiver);
   - creation paths: FUN_0070DE10 → (a) FUN_0070DCF0 record-read early
     creator (manager mode 1/2 + factory+0x84 stream) or (b)
     FUN_0070D990 defaults + factory+0x80 delegate bind (vtable[1]).

5. **The getter's exact receiver** — MOV ECX,[EAX+4] @0x004C551C reads
   [class_obj+4] = **THE 20006 FACTORY OBJECT**:
   - 0x118 bytes; vtable 0x00A870C4; singleton slot 0x00BA590C;
     lazy init (0x0073E2C7..0x0073E355): alloc 0x118 → ctor
     FUN_0073B820 (registers 0x4E26 via FUN_0070CF80; vtable store
     `C7 06 C4 70 A8 00` @0x0073B89B) → store @0x0073E303 →
     FUN_0070E2F0(f,8,0) → FUN_007374F0(f) (the 8-slot array) →
     FUN_0070C150 → FUN_0070BF10 (success flag).
   - [factory+0x88]/[+0x8C] = the 16-byte ATTRIBUTE-SLOT array (the class
     schema); [+0xD8/+0xE8/+0xF8/+0x108] = the four fixed members
     (attribute ids 0..3); [+0x0C] = per-receiver cache map; [+0x24] =
     critsec; [+0x80] = bind delegate (NULL at init); [+0x84] = record
     stream (NULL at init); [+0xA0] = name string (from .rdata 0x00A7957B).

## Why STRONGLY_SUPPORTED and not CONFIRMED

- Every edge from the entity to the getter receiver is byte-pinned.
- The one un-decoded boundary: FUN_00747970 (the [entity+4] resolver). Its
  semantics (what the resolved receiver IS) is not established, so the
  receiver's SEMANTIC identity is structural, not named.
- The receiver's CONCRETE runtime object (which entity instance triggers the
  audited path) is runtime state — unobservable in a STATIC-ONLY run.

## The tag-6 getter receiver vs the class component — not the same object

Per the C2-corrected layered identity (preserved): the CLASS_SELECTOR 20006
resolves the per-receiver CLASS COMPONENT (class_obj); the PROPERTY_TAG 6
getter's receiver is [class_obj+4] = the FACTORY (the class-level schema
holder). The audited getter therefore reads a CLASS-DEFINED attribute
definition (slot 6 on the factory) but takes the VALUE from the per-receiver
component's value table (table[10] on class_obj). Both facts are byte-pinned
(@0x004C551C and @0x004C553C/0x004C553F respectively).
