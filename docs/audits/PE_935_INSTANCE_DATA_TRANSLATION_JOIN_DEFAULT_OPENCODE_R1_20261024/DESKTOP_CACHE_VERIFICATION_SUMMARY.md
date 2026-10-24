# DESKTOP_CACHE_VERIFICATION_SUMMARY — R1 20261024

Source: independently verified checker package PE_935_CACHE_STRINGS_INDEPENDENT_RECHECK_DESKTOP_R1_20261023 (RESULT.json SHA256 CB53DC4C35851A7B6BF3D20CC97D118178B3E4B8FFE0860F25E4117621B33C5D == authoring pin; re-verified this run by T01 without repeating the decryption).

- Cache 24007.vfs is PLAINTEXT (ArkVFS02; not encrypted): 180 records x 256 B.
- English Strings /1/0.bnt part0: 3949 members. The index starts with a u32 count (= 3949) that the old parser R13 mistook for a filename prefix — R13 therefore skipped member ID 1 (1.str) and published 3948. Correction incorporated: 3949 members.
- CRC32 control: 3949/3949 entries pass; roundtrip re-encryption reproduces ciphertext 3949/3949.
- 180/180 cache-name joins consistent with the old export.
- Unresolved: strict UTF-8 fails for members 3196, 4135, 4136 (not a blanket validity claim).
- Scope: part0 only; NOT all 15 archives verified.
- Era/cache provenance: UNVERIFIED (see DESKTOP_POSTAUDIT_SUMMARY and PROCESS_SUMMARY; D03: EXACT_CACHE_ERA=UNVERIFIED; candidate EU2008/9.2.2.2 REPORTED_ONLY).

No decryption keys, no full plaintext strings, no raw cache bytes are published.
