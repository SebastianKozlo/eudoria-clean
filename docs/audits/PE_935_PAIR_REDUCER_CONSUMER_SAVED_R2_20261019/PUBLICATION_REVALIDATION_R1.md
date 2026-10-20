# PUBLICATION_REVALIDATION_R1 — PE_935_PAIR_REDUCER_CONSUMER_SAVED_R2_20261019

ADDITIVE REVALIDATION SIDECAR (historical files and the old 00_PUBLICATION/PUBLICATION_MANIFEST.csv
are preserved byte-identical; the old manifest is SUPERSEDED for current verification by
00_PUBLICATION/PUBLICATION_MANIFEST_V2.csv added by this same commit).

Revalidation facts (source: the independent deep postaudit
PE_935_PAIR_REDUCER_CONSUMER_DEEP_POSTAUDIT_R1_20261019):
1. The old 00_PUBLICATION/PUBLICATION_MANIFEST.csv (60 rows) mismatches the committed blob of
   00_PUBLICATION/EXCLUDED_ARTIFACTS.csv: expected 3864 B / 8E2F7A6C5D4409F525347DDC4E1D2EF0D9E49EEE72D8486AEAB290EA70FD2624,
   actual 3860 B / D91369C0ED079BA41E40E0BD27C114087794B9BD74B690A098FD06E76D50AFD6.
2. The old manifest omits 00_PUBLICATION/PUBLICATION_ALLOWLIST.csv and
   00_PUBLICATION/REDACTION_MAP.md.
3. The sealed local root currently has 78 physical files (76 manifest rows + manifest +
   CONTROL/EP_ROW.txt written after the local seal) — the local bijection claim FAILS for the
   current root; pinned as INHERITED_NONPASS in the successor run's guard; no source byte
   repaired; the science rows remain hash-valid.
4. QC adjudication: 16 findings (15 ACCEPTED + 1 PARTIALLY_ACCEPTED), not 14/13+1 as older texts said.
5. Standing science limitations (see POSTAUDIT_NOTICE.md and the deep postaudit):
   CALL EAX at 006C2A63; selected-position erase + zero-after ≠ whole-range remove-zero;
   004D1430 unproven constructor; saved RTTI permitted; compaction/indirect-call/RTTI barriers preserved.