# POSTAUDIT_NOTICE — SCENE_INSTANCE_TRANSFORM_JOIN_SAVED_R1_20261019

An independent deep postaudit (PE_935_SCENE_INSTANCE_TRANSFORM_JOIN_DEEP_POSTAUDIT_R1_20261020, published in this commit) issued REQUIRE_CORRECTIONS for this run:
1. The receiver-field reclassification ([receiver+0x2C] as direct 12-float data address) is RETRACTED: the provider chain must keep B (owner ECX in caller 00527AB0), R=M32[B+0xC] (receiver 0085BFA0), P=M32[R+0x2C], VT=M32[P], F=M32[VT+0x24], T=retval CALL F as SEPARATE symbols; floats are read from T after the call @0085BFB5, and P=T is neither assumed nor excluded.
2. The constructor 0085B1B0 (via 007345C0(B+0x14)) zeroes B+0x2C; it proves nothing about R+0x2C absent B==R (not demonstrated). Owner-side methods 0085B3E0/0085B6A0 are not thereby attributed to R.
3. The "corpus-blocked" data barrier of this run was PREMATURE (denominator = 11 admitted windows, not the corpus).
4. Two CLAIMS.json files of this run's packages (P02_CONTINUATION, P03_DISPATCHER) contain literal JSON syntax errors; they remain published byte-identical as history and are superseded by CLAIMS_CORRIGENDUM.json (this commit). The local sealed originals stay unedited.
5. The old PUBLICATION_MANIFEST.csv has 3 metadata rows of 4 columns under a 5-column header; corrected uniformly as PUBLICATION_MANIFEST_V2.csv (this commit). Earlier 23/65-row manifests are compliant and untouched.
Follow-up run: PE_935_OWNER_ATTACH_PROVIDER_IDENTITY_SAVED_R1_20261020 (this commit) applied these corrections and qualified both commissioned store-site candidates.
