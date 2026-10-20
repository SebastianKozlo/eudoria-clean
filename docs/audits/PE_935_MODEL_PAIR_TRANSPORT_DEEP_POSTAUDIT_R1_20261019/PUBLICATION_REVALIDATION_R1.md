# PUBLICATION_REVALIDATION_R1 — PE_935_MODEL_PAIR_TRANSPORT_DEEP_POSTAUDIT_R1_20261019

ADDITIVE REVALIDATION SIDECAR (nothing in this directory was modified by this commit; the
historical files and the old manifests are preserved byte-identical and are SUPERSEDED for
current verification by 00_PUBLICATION/PUBLICATION_MANIFEST_V2.csv added by this same commit).

Revalidation facts (source: the independent deep postaudit
PE_935_PAIR_REDUCER_CONSUMER_DEEP_POSTAUDIT_R1_20261019, REPORT.md SHA256
11B5BE7AE2B1850C7BEF4B43990A26F0F6B25D027E5A18F40847AA1831243BC2 at manifest level):
1. The old 00_PUBLICATION/PUBLICATION_MANIFEST.csv (19 rows) mismatches the committed blob of
   00_PUBLICATION/EXCLUDED_ARTIFACTS.csv: expected 574 B / 2C30E4E2DB1B5F3CFD5DB6E2ED35FC50DCAD4BBB586AC5EEA79907FA750AAF4A,
   actual 570 B / 93E87EF822106788C0E9546C70838282C549F6426EF5BEBE2AD8D69005FB474D.
2. The old manifest omits two physically published metadata files:
   00_PUBLICATION/PUBLICATION_ALLOWLIST.csv and 00_PUBLICATION/REDACTION_MAP.md.
3. The local sealed source root of the qualified run has 78 physical files vs 77
   manifest-defined (extra CONTROL/EP_ROW.txt created after the local seal) — pinned as
   INHERITED_NONPASS; the source-science hashes remain valid; the local bijection claim FAILS
   for the current root and is NOT repaired.
4. QC adjudication had 16 findings (15 ACCEPTED_FINDING + 1 PARTIALLY_ACCEPTED); older
   reports/terminal/commit text said 14 and 13+1.
5. Limitations preserved: 006C2A63 is CALL EAX (statically resolved target 00823C10), not an
   E8 direct call; consumer compaction erases an opaque-selected position and zeroes strictly
   after it (not proven whole-range remove-zero); 004D1430 not proven a constructor; saved
   RTTI is contract-permitted (missing runtime does not close static paths); LINK30 R3
   census 2 PROVEN / 620 POSSIBLE / 3021 REJECTED (not universal preservation).