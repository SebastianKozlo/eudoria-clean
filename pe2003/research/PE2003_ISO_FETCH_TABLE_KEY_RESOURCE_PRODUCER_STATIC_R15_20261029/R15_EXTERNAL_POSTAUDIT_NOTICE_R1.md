# R15 External Postaudit Notice (additive, R15 files byte-untouched)

This notice is the additive public record of the external Desktop postaudit of R15 (PE2003_R15_DESKTOP_POSTAUDIT_R1_20261029) and of the R16 campaign's disposition of its findings. No historical file or commit was edited; the R15 publication commit 476bb5bc1c21c8d706ad71959314f85255660a71 remains the published record for R15.

Postaudit verdict: REQUIRE_CORRECTIONS / PARTIAL_PASS_WITH_MATERIAL_CORRECTIONS. Material findings and their R16 dispositions:
- A01 (stack-frame error in the C2 key-origin claim): ACCEPTED. The K key at 0x47E062 reads [T+0x10], not the helper out-slot; the O-cache write is not the definition of K. R16 additionally falsified the residual 'incoming arg2' reading: [T+0xC]/[T+0x10] are two LOCAL slots of the enclosing function (entry 0x47DFB0, thiscall, sub esp,8), and K_slot is written inside the function prolog at 0x47DFC8; the K value chain M32[M32[M32[M32[0x6C62F4]+0x18]+4]] is established to the singleton root 0x6C62F4 with a byte-confirmed producer->global identity (ctor 0x5003C0). The [G1+0x18] writer remains an open, scope-bounded negative (four producer scopes exhausted; next operand: producer-singleton head <0x500A00).
- A02 (AL tail): ACCEPTED, already satisfied by saved TABLEPROD a8/TYPEPROD a3; R16 reused it without re-decoding.
- A03 (5651D0 range-copy role): ACCEPTED; reused from TABLE1 a3/a4.
- A04 (11 raw E8 hits unqualified; Dprime==D INCONCLUSIVE): ACCEPTED; R16 resolved Dprime==D as REJECTED (CM-A confirmed: receiver = fresh 0x45E450 object on [manager-0x450190+0x1C], not an S-chain element) and kept the raw cluster unqualified.
- A05 (0x5257C0 consumer, not world-instance): upheld; no world-instance claim made in R16.
- A06 (census/provenance counters): upheld; R16 reconciles reservations vs actuals explicitly (ACTUAL_RECONCILIATION) and used the canonical MANIFEST_SHA256.csv name.
- A07 (packet_read operand loss): ACCEPTED; R16 saved reads honored operands/op_str and no old-format packet was re-read.
- A08 (range incident; no automatic full-campaign freeze for a bounded range overread; keep every check attempt separate): ACCEPTED as contract policy for R16 (LOCAL_BRANCH_HOLD discipline; no such incident occurred in R16).
- A09 (closing receipts, UTF16LE gate file, custom manifest name): ACCEPTED; R16 used UTF-8 receipts, the MANIFEST_SHA256.csv name, and preserved every NONPASS.
Standing after R16: both model case certificates (296445/218757) remain OPEN; WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; LOCAL_SOURCE_EXHAUSTED=NO; CANONICAL_GATE_EFFECT=NONE; EXTERNAL_POSTAUDIT=PENDING.
