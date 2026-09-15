# POSITION_SEMANTICS — PHASE F ANALYSIS (caller-side semantic control; gates G9, G11-G14)
# RUN_ID: PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915
# BOUNDED per contract: no ARG2 census reopen; prior canon cited with pin checks only.

## CONTEXT CLASSES (independent, measured; >=2 required, 5 delivered)
CLASS A — SF-family sibling slot (site 0x50B0D8..0x50B0FF): same `add eax,0x90` + pair + 3-dword take-off; out
  feeds an in-function buffer and onward as [esi..esi+8] + return. Same semantic family as slot3 (world translate
  -> scaled space). (NOT used alone for promotion.)
CLASS B — position+orientation taker (site 0x438A8A..0x438AB8): pair output [edi..edi+8] consumed IMMEDIATELY
  alongside the m_kWorld ROTATE block (`add esi,0x6c`) of the SAME node — i.e. the consumer treats the pair's
  output as the position half of a world transform. Strong position-semantics evidence from an independent consumer.
CLASS C — placement-with-attributes (site 0x47CDFE..0x47CE35): node obtained via lookup chain, +0x90 translate
  through the pair, node pointer + further fields (+0x130/+0x134) gathered around it — a structure/attachment
  placement pattern (position + metadata), independent consumer context.
CLASS D — generic 3-float scaler (site 0x523C38..0x523C63): the pair applied to an inline 3-float record field
  ([ebx+8/+0xC/+0x10]) — NOT a node translate. Bounds the helper's identity: generic converter, context supplies
  the "position" meaning (NEGATIVE_CONTROL_RAW.txt Control 1).
CLASS E — in-slot fallback (0x50A087..0x50A0A7): raw copy of the stored placement value (SF+0x34) — the same
  interface returning a stored (not live-derived) value; same structure, different derivation.

PRIOR CANON (cited, pin-checked, not re-derived):
- PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914 / PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913: SF+0x34
  writer FUN_005094C0 = value copy from the placement record — pin re-measured THIS RUN (bytes match: 3-dword copy
  into +0x34/+38/+3C, dirty byte +0x28); slot1 getter FUN_005090A0 re-measured ('lea eax,[ecx+0x34]; ret').

## GATE ANSWERS
G9_CALLER_SEMANTIC_CONTROL: PASS (5 independent context classes; no single-caller promotion; Class B/C consumers
  independently corroborate position semantics; Class D bounds the helper identity).
G11_COORDINATE_SPACE: the primary output is NOT in the source's space — a 100:1 scale conversion (x0.01, origin 0)
  is CONFIRMED at the byte level (forward/inverse pair measured). The engine->internal-space direction is CONFIRMED;
  the human label of the internal space (meters vs game units) is UNVERIFIED (RUNTIME_COORDINATE_BEHAVIOR = UNVERIFIED).
G12_AXIS_MAPPING: identity permutation CONFIRMED (component i -> component i, no swap/negation); axis labels inherited
  from the shared NiPoint3 convention (label semantics UNVERIFIED statically, no runtime test permitted).
G13_UNIT_SCALE: CONFIRMED as a bit-exact numeric relation — multiply by (double)(float)0.01
  (0.009999999776482582, 0x3F847AE140000000) with two f32 narrowings per component; inverse uses
  (double)100.0. The "0.01 = cm->m" READING is PLAUSIBLE interpretation, not engine-proven.
G14_FINAL_POSITION_ROLE: STRONGLY_SUPPORTED that the SF slot3 output is a POSITION (world placement semantics):
  CONFIRMED structurally (world-translate source, float3 out, same out returned), corroborated independently by
  Classes B (position+orientation co-consumption) and C (placement-with-attributes) and by the fallback's stored
  placement value occupying the same output contract. Not CONFIRMED as an absolute (no runtime consumer trace of
  the slot3 vtable dispatch is statically enumerable) — hence STRONGLY_SUPPORTED, not CONFIRMED.

## H4 / H5 evaluation
- H4 ("output represents the named NiAVObject's world-space position, possibly after a deterministic
  convention conversion"): CONFIRMED in its full form — output = live world translate x 0.01 (a deterministic
  unit conversion), same component order; the "possibly after conversion" clause is exactly what was measured.
- H5 ("primary and fallback outputs share the same structural/coordinate semantic"): PARTIAL — structure and
  interface: CONFIRMED identical; coordinate-space coherence: STRONGLY_SUPPORTED (shared origin seeding, inverse
  family, prior canon) but not byte-proven inside the window (the stored fallback value's scale is not measurable
  in this scope fence). H5 is not rejected; its strong form is UNVERIFIED at the exact 'stored value scale' clause.
