# TRANSFORM PROVENANCE — PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003

Executor: pe-reconstruction. STATIC_ONLY.

## 1. Status

```text
WORLD_TRANSFORM_SOURCE = UNKNOWN   (contract §29 vocabulary; the value is
                                     also NOT_APPLICABLE to the measured path)
TRANSFORM_SEMANTIC_ROLE = UNVERIFIED
PLACEMENT_XYZ_RECOVERED = NO
PLACEMENT_X / Y / Z = UNKNOWN
ROTATION_RECOVERED = NO
```

## 2. Why there is no transform provenance to classify

Contract Phase 9 (transform source) executes ONLY if runtime-object identity is
established (Phase 8), which requires the template→model bridge (Phase 6), which
requires the template-id consumer PASS (Phase 5). The mandatory falsifier fired
(TEMPLATE_ROLE_TEST.md): 4057 does not reach any proven template-id consumer;
STOP S2 terminated the landmark construction branch. No runtime world instance,
no construction→transform path, and no transform producer exist on the measured
path.

## 3. What values actually flow on the measured path (E10 discipline)

The 4057 dataflow carries NO floating-point triples at any measured step. The
values on the path are: integers (ids, count, section selector), pointers
(singletons, map nodes, stack objects), and STLPort basic_string data
(the resolved string `S_REPAIR_UI_CLEAR_TOOLTIP` + its fallback). No
three-float operation, no NiTransform-shaped copy, no position setter, and no
known transform target field appears anywhere in the 18 measured functions
(01_RAW/G1..G6 listings). Per the E10 lesson, no spatial semantics were
attributed — and none could be, since no candidate triple was observed.

## 4. What the UI-side store is NOT

The terminal store FUN_008DFB70 writes into an ArkUI::Component-family temp
object (vtable 0x00A7A948 store @0x008DFBD0) — a UI component container, not a
NiAVObject/NiNode: no m_kLocal/m_kWorld-shaped fields (+0x38/+0x6C per NINODE
canon), no UpdateWorldData-shaped propagation, no refcount-pair AttachChild
shape (the record-bridge E7 negative-control family). No scene/world insertion
edge is claimed from this machinery (CONTROL-5).
