# R14 external postaudit notice (additive; R15 advisory follow-up)

This notice is an ADDITIVE postaudit follow-up published together with the R15 package (PE2003_ISO_FETCH_TABLE_KEY_RESOURCE_PRODUCER_STATIC_R15_20261029). All R14 files in this folder are byte-untouched; this is the only new file. Nothing here is a scientific acceptance; the R15 findings are advisory and era-labelled (ISO2003NOV_PE_5_1_0_0, section1.bin, SHA256 D43A23B9EFCFC9BC4092B38FA3C73499DE7DE7B03B20F34478B9E81EE8893631).

1. FALSIFIED in R15 (advisory): the R14-era premise "receiver = entry" for the fetch-array walk. The R15 re-derivation shows the receiver at 0x564978 (symbolically `mov esi,[esi+0x1C]`) is the CHAIN sub-object of the entry, not the entry itself.
2. FALSIFIED / SUPERSEDED in R15 (advisory): the earlier "0xC-byte elements" premise. The element stride of the fetch-record array is 0x20; the +0x0C cell is a sub-object offset within the 0x20-byte entry, not an element size.
3. CONFIRMED in R15 (advisory): the R14 fetch-manager chain (R14-A05) stands — the R15 S->U->A->B->C->D owner chain (0x46F1A0 with U=[S+0x78], A=[U+0x34], B=[A+8], C=[B+0x1C], D=[C+8]) is consistent with and extends the R14 manager findings; the pair-table mechanics (head/end at entry +0x0C/+0x10, {compare_object, record} pairs, holder at +0x18) are re-derived and upheld.

See the R15 public report (pe2003/research/PE2003_ISO_FETCH_TABLE_KEY_RESOURCE_PRODUCER_STATIC_R15_20261029/REPORT.md) for the full sanitized claims matrix and the READY frontier. R14 verdicts as published remain the R14 record; the two falsified premises above are superseded by the R15 advisory evidence.
