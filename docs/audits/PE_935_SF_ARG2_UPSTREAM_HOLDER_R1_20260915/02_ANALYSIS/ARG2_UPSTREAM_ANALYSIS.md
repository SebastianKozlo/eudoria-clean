# ARG2_UPSTREAM_ANALYSIS.md — Phase E (G9, G10, G11) + Phase D context

RUN_ID: PE_935_SF_ARG2_UPSTREAM_HOLDER_R1_20260915
R2 CORRECTION (AMEND_LOG_R2.md; QC_AUDIT.md §2 P0-1 + §3 P2-1): the R1
"no caller" wording is qualified to "no statically-identifiable caller"
everywhere; the R1 clause "no arg2 can ever reach a live receiver" is
RETRACTED (live held receivers exist at bounded constructions); the fault
shortcut in the dispatch-candidate disposition context is dropped.
Evidence: 01_RAW/ARG2_VALUE_FLOW_RAW.txt (R2 disposition raw),
01_RAW/THUNK_CALLER_CENSUS.txt + .csv (Phase D — unchanged, QC-verified),
01_RAW/FUN_006FAB80_DISASM.txt (ABI),
01_RAW/HOLDER14_WRITER_RAW.txt ([IV-8]/[IV-9] — the receiver reality).

## Phase D outcome (prerequisite for Phase E) — UNCHANGED (QC-re-verified)

Four channels, all censused with denominators (01_RAW/THUNK_CALLER_CENSUS.txt):

1. DIRECT_E8_CENSUS: E8 byte occurrences 156,829; E9: 40,668; EB: 17,961 —
   **0** target 0x006FAB80. Lattice-verified: 0 calls, 0 jmps.
2. IMM32_ADDRESS_CENSUS: 5 whole-file occurrences — all five are the thunk's
   own vtable slot dwords (classified); nothing else in the entire file
   references the address.
3. VTABLE_MEMBERSHIP_CENSUS: 5 vtables (exactly the five expected classes),
   slot ordinal 2 in each; no membership beyond the five.
4. VIRTUAL_DISPATCH_PATTERN_CENSUS (slot ordinal 2, disp 0x08; declared
   bound: 64-byte window, <=6 interstitials — the corrected threshold after
   the prior run's <=3 miss; both the two-step `mov vt,[obj]; mov f,[vt+8];
   call f` idiom and direct `call [vt+8]` forms): **1,438 candidates** —
   PROVEN_TARGET = 0, REJECTED_TARGET_NOT_FAMILY = 5 (receivers proven
   other classes), INSUFFICIENT_PROOF = 1,433 (receivers unproven within
   the declared slice bound).

**There is no statically-identifiable caller of FUN_006FAB80.** (The census
does NOT prove the thunk is never called: 1,433 candidates remain
INSUFFICIENT_PROOF — recorded honestly, never waved through.)

## Phase E disposition (G9/G10/G11)

Phase E applies to PROVEN or strongest-bounded candidate callers ONLY. There
are no PROVEN callers. The strongest-bounded candidates are the 5 REJECTED
rows — byte-re-verified in ARG2_VALUE_FLOW_RAW.txt [E3]: each receiver
class's own slot-2 function (e.g. 0x0083FA60 for the MaPanel* classes) is !=
the thunk, so those sites are not thunk callers at all;
ArkVegetationObservable has NO slot-2 entry (vtable extent = 1 slot; the
dword at the slot-2 position is 0x566B7241 = ASCII "ArkV" — string data
after the vtable, R2 per QC P3-3).

- **G9 = PASS via NOT_APPLICABLE** (no proven caller exists; the
  strongest-bounded candidates are dispositioned with byte evidence).
- **ARG2_PROVENANCE = NOT_DEMONSTRATED.** No statically-identifiable call
  site exists to carry any arg2 value to the thunk. R2 CORRECTION: the R1
  justification "the held field itself is NULL at all constructions, so no
  arg2 can ever reach a live receiver" is RETRACTED — live held receivers
  (the FloatValue-family channel children) exist at bounded constructions;
  what stands is the empty caller set itself (QC C15).
- **ARG2_VALUE_CLASS = NOT_DEMONSTRATED** (honest negative; no STRING or
  other value class is claimed anywhere).
- **G10 = PASS with honest NOT_DEMONSTRATED.**
- **ARG2_FINAL_SEMANTIC_ROLE = UNVERIFIED** — a valid gate outcome per the
  contract's string/name evidence rule. **G11 = PASS.**

## arg1/arg2 ABI contract (re-measured, for the record)

- arg1: [esp+4] -> x87 fld/fstp roundtrip -> receiver [esp+4] (bit-preserving
  for pointers-as-dwords, normals, denormals; sNaN quieting not guaranteed).
- arg2: [esp+8] -> mov edx -> push edx -> receiver [esp+8] (verbatim dword).
- Receiver ABI: thiscall; this = [this+0x14] in ECX; ret 8.
- The Phase A discriminator (arg1 as out-buffer POINTER vs FLOAT VALUE) is
  **unresolvable at this seam**: no statically-identifiable caller exists to
  pass either form.
  For the record: the hypothetical SceneFeederObject consumer
  (FUN_0050A050) uses arg1 as an OUT float3 buffer pointer and arg2 as a
  NULL-tested name pointer (validated as SF infrastructure only — it is not
  exercised via this seam; and the R2 receiver-identity result shows the
  actual bounded receivers' slot-3 targets are 0x006FFF00/0x009154A0, whose
  signatures were not derived — out of scope).

## Dispatch-candidate disposition context (R2 correction of the residue reading)

The 1,433 INSUFFICIENT_PROOF dispatch candidates keep their honest status:
none is proven family, none proven a thunk dispatch. The R1 context clause
"all family objects carry held=NULL so a dispatch would fault" is RETRACTED
(AMEND_LOG_R2 R2-5): live family objects with non-NULL held exist on the
bounded normal construction paths, and a slot-2 dispatch on such an object
would forward to the child's slot-3 (0x006FFF00/0x009154A0) — it would NOT
fault. The census numbers themselves stand (0 PROVEN / 5 REJECTED / 1,433
INSUFFICIENT_PROOF).

## Hypotheses H4/H5 dispositions

- H4 ("the forwarded arg2 has a traceable upstream source within a bounded
  caller window"): **REJECTED** — the caller set is not merely bound-exhausted
  but EMPTY across all four channels (no statically-identifiable caller).
- H5 ("arg2 semantic role can potentially be narrower than generic
  string/name"): **UNVERIFIED** — no arg2 value exists to classify; the
  producer-source test list (11 classes from the contract) is dispositioned
  NOT_DEMONSTRATED row-by-row in the raw.
