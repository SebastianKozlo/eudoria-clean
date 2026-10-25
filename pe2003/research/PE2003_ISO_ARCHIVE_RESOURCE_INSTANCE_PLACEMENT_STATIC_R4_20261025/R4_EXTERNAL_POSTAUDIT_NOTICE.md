# R4_EXTERNAL_POSTAUDIT_NOTICE — resolved corrections confirmed in R5

RUN_ID context: PE2003_ISO_ARCHIVE_RESOURCE_INSTANCE_PLACEMENT_STATIC_R4_20261025 (this folder, frozen) /
PE2003_ISO_MODEL_BINDING_VALUE_ORIGIN_STATIC_R5_20261025 (successor closing wave).
DATE: 2026-10-25. STATUS: ADDITIVE NOTICE — all pre-existing files in this R4 folder are byte-untouched.

This notice records ONLY the corrections from the R4 external postaudit that were RESOLVED and
confirmed by the R5 static closing wave (image ISO2003NOV_PE_5_1_0_0 section1.bin, SHA256
D43A23B9EFCFC9BC4092B38FA3C73499DE7DE7B03B20F34478B9E81EE8893631, VA = 0x401000 + blob_offset).
It is NOT a copy of any PA draft: it lists the resolved corrections only, with the R5 evidence base.
Theses that remain disputed or unresolved are explicitly marked as such.

## Resolved corrections (R4 postaudit item -> R5 resolution)

1. **entity+0x40 = ID for the SFO (R4-A01).** RESOLVED — CONFIRMED_FOR_MEASURED_SCOPE. I = [E+0x40]
   is written by a1 (store `89 46 40` @0x555191) and pushed to the lazy-create lookup, which receives
   the LITERAL 0 as the record index K (byte-proven `push 0` @0x46E9D0) and therefore selects SUB[0].
   I != K is upheld (separate argument slots, byte-proven); K != 0 EXISTS in the re-bind method
   0x46ECA0, which takes its record selector K from the message. ID lands at SFO+4 via 0x473E90
   (push 0x7C byte-proven); record lands at SFO+0x78.

2. **No demonstrated NIF ROOT -> record join (R4-A02).** UPHELD — maintained UNVERIFIED. The R5 waves
   J01-J05 kept the gap open; the name -> ROOT -> map -> SFO loop is NOT closed statically in
   section1.bin. Lanes (a) container-readers [obj+0xBC] and (c) [SUB+0x18] vt+4 provider are
   measured-closed-negative (lane (c) statically dead in-image: flag=0 hardcoded); lane (d) member
   +0x18 measured non-key-contributing at the 52A130 edge. Open lanes: (b) residual-14 `call
   [reg+0x3C]` + wrapper 0x498B80 inner (key 0x19A), (d-res) post-52A130 flow 0x526CFA+, (e) PE
   sections outside section1.bin. Per-model binding certificates: CONDITIONAL_OPEN (both models).

3. **Renderer 0x4DD421 = DrawIndexedPrimitive (COM vt+0x11C, 5 args), NOT a transform sink (R4-A03).**
   UPHELD. record+0x14/+0x2C/+0x30 are NOT XYZ at this call; the transform-sink interpretation is
   REJECTED. R5 added no new renderer measurement and did not rehabilitate the renderer-as-applier
   thesis; the countermodel stands.

4. **Typed factory arguments a1..a6 (R4-A04 family).** RESOLVED — CONFIRMED_FOR_MEASURED_SCOPE, with
   two theses REJECTED. Measured chain: factory 0x4578E0 (thiscall, 6 stack args, ret 0x18) ->
   writer 0x46E990 via [vt+0x1c] @0x457951 -> 0x51D730 -> 0x5531F0 -> 0x555170 -> 0x555270:
   a1 -> [E+0x40] (I); a2 -> byte [E+0x44] (low byte only); a3 -> flags [E+0x54] (not forwarded to
   0x555170; bit0 consumed @0x46E9E4); a4/a5/a6 -> vec3-copy transform dispatches [vt+4]/[vt+8]/
   [vt+0x10] -> 0x5552C0/0x5552E0/0x555320. The axis-label interpretations x,y,z,rx,ry,rz are
   REJECTED (no consumer/frame evidence; KONTRAZ upheld). A4_UNUSED is REJECTED (a4 is live). The
   stale-A6 thesis is RESOLVED as REJECTED at this callsite: the scratch slot [E+0x18] (a6 incoming
   home) is written at 0x46EA02 with dword [E+4] (`89 44 24 1c`, ESP=E-0x04) and read at 0x46EA55
   (`d9 44 24 28`, ESP=E-0x10) — the SAME absolute slot; the dominant definition at the read is the
   [E+4] store. First-translation 0x46F0A0 receives (scale*f[E+4], scale*f[E+8], scale*f[E+0xC]),
   scale = [0x65B648] — no axis labels.

5. **Static barriers formalized (R4-A06 direction).** APPLIED. R5 replaced runtime-necessity
   declarations with formal BARRIER statements: residual-14 `call [reg+0x3C]` sites with
   runtime-selected receivers (strongest 0x498C50 via wrapper 0x498B80; second 0x56FA46
   switch-dispatch arm), runtime receiver classes ([inner_vt+0x50] lookup; RTTI descriptors
   0x6C3898/0x6C3A0C runtime-init; descriptor 0x6C3940 zero in image), and PE sections outside
   section1.bin (wrapper vtable, import [0x65A1A8], service [0x6C4F20]). Status
   UNRESOLVED_IN_BOUNDED_STATIC_PASS applied consistently; LOCAL_SOURCE_EXHAUSTED = NO.

6. **Literal absence does not prove consumer absence (R4-A05).** APPLIED — SCOPED_NEGATIVE (literals
   only). The literals '296445'/'218757' are absent from section1.bin, but name-assembly exists
   ('.nif' @0x6B0304 with consumers @0x42E995/0x45F098; '.dds' @0x6B12C4 with 2 consumers
   0x45F0D4/0x4B61E4; VFS initializer 0x45E4F0 registers archive names and extension patterns from
   config literals), so runtime-built names remain possible. No global consumer-absence claim.

7. **UPX CLDLLPatcher static-unverifiability claim.** REJECTED as an impossibility claim. The
   postaudit thesis that CLDLLPatcher is "statically unverifiable" was rejected as a claim of
   impossibility: a bounded static unpack of the patcher image remains permissible methodology.
   In R5 the patcher interior was NOT analyzed (not required by any R5 load-bearing claim) and the
   patcher was NOT executed — this notice rejects only the impossibility inference, it does not
   assert any new CLDLLPatcher finding.

## Disputed / unresolved theses (explicitly marked, NOT resolved by this notice)

- MODEL-INSTANCE JOIN (ROOT from open-by-name 0x423280 -> record 0x5C / SFO / visual map as a
  common pointer): UNVERIFIED with formal BARRIER; the countermodel (message-borne model name ==
  open-by-name key at runtime) survives UNREFUTED with zero measured instances on the closed lanes.
- a1..a6 upstream origin: UNBOUND/UNRESOLVED (SCOPED_NEGATIVE over all bounded receiver-constrained
  forms + BARRIER); the real factory caller (slot-0 dispatch on M+0x08 with 6 pushes) was not
  found in the entire measured static scope.
- SOURCE_SPECIFIC_ISO_MODELS = UNKNOWN; WORLD_XYZ_RECOVERED = NO; HISTORICAL_PLACEMENT =
  NOT_ESTABLISHED; CANONICAL_GATE_EFFECT = NONE.

Evidence base: the sanitized R5 closing package at
`pe2003/research/PE2003_ISO_MODEL_BINDING_VALUE_ORIGIN_STATIC_R5_20261025/` (REPORT.md, CLAIMS.json
C01-C18, ABI_FIELD_MAP.md, OBJECT_AND_ID_MAP.md, ROLE_LEDGER.json,
MODEL_BINDING_CERTIFICATES_FINAL.json, VALUE_ORIGIN_MAP.md, SOURCE_PROVENANCE.json,
CORRECTION_DISPOSITION.md, FRONTIER.md, RESEARCH_BACKLOG.json). Publication is NOT scientific
acceptance; ADVISORY_PENDING_EXTERNAL_POSTAUDIT.
