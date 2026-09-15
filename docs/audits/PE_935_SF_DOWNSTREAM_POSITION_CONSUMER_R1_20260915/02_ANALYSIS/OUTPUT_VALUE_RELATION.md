# OUTPUT_VALUE_RELATION — PHASE E ANALYSIS (per-component relation; gates G6, G7)
# RUN_ID: PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915 (raw: 01_RAW/END_TO_END_VALUE_FLOW_RAW.txt)

## OUTPUT_BUFFER_LAYOUT (G7)
out is a caller-provided float3 buffer: out[0] @ +0, out[1] @ +4, out[2] @ +8 (3 contiguous f32). Both paths write
exactly these 3 dwords and return EAX == the same out pointer (primary: 0x50A081 mov eax,esi; fallback: 0x50A0A4
mov eax,ecx). FUN_0050A050's return value identity: the caller's ARG1 pointer (never the source, never a fresh
object). CONFIRMED by byte decode of both paths.

## PER-COMPONENT VALUE RELATION (G6) — primary path
out.x = f32( f32( W.x * K ) - S.x )
out.y = f32( f32( W.y * K ) - S.y )
out.z = f32( f32( W.z * K ) - S.z )
with W = named NiAVObject.m_kWorld.m_Translate (engine space), K = (double)(float)0.01, S = the origin singleton
(initial value {0,0,0} measured; AMEND, origin-mutability correction run
PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915: the OLD text said "S = {0,0,0} (proven)" as an unconditional
value claim — RETRACTED: S's initial value is measured {0,0,0}; S's mutability is a separate status
(ORIGIN_MUTATION_CHANNEL_EXISTS = CONFIRMED via writer site 0x458E27; ORIGIN_MUTATED_AT_RUNTIME/VALUE =
UNVERIFIED; status algebra: 02_ANALYSIS/ORIGIN_STATUS_CORRECTION.md; independent formula re-derivation:
01_RAW/OUTPUT_FORMULA_REVALIDATION_RAW.txt)).

REDUCED — CONDITIONAL special case (IF S == {0,0,0} (+0.0 each), bit-exact under x87 round-to-nearest,
sign-of-zero preserved; AMEND: the OLD header presented this as the unconditional reduction — conditionalized):
out.x = f32(W.x * 0.01f) ; out.y = f32(W.y * 0.01f) ; out.z = f32(W.z * 0.01f)

Each output component is a function of the SAME input component only (no cross-component terms). The relation is
line-identical, injective for the representable range, deterministic given S (K is a constant; AMEND: the OLD
text said "S is a proven-constant zero vector" — RETRACTED: S is a runtime object with a measured initial value
and a CONFIRMED static mutation channel; its runtime value is UNVERIFIED — the formula's determinism is
determinism GIVEN S, not proof of S's constancy).

## FALLBACK RELATION (in-slot control)
out[i] = P[i] (raw copy), P = SF+0x34 stored placement value (writer FUN_005094C0; ctor-seeded from the same zero
triple). No scale, no base.

## UNKNOWNs (recorded, not papered over)
- The absolute unit meaning of the scaled space ("meters"/"game units") — UNVERIFIED statically.
- Whether the fallback's stored value is already in the scaled space (coherence) — STRONGLY_SUPPORTED via the
  shared-origin ctor + inverse family + prior canon, NOT byte-proven in this window.

## G6/G7 statuses
G6_END_TO_END_VALUE_FLOW: PASS (per-component source expressions with instruction-level def-use; UNKNOWNs localized
to the two items above, both outside the measurable chain).
G7_OUTPUT_BUFFER_LAYOUT: PASS (proven layout + return identity).
