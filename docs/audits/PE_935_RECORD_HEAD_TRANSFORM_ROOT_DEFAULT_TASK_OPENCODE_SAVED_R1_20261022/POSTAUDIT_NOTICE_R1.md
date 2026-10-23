# POSTAUDIT_NOTICE_R1 (additive; this file does not modify any existing file of this run)

The independent external post-audit of 2026-10-23
(PE_935_RECORD_HEAD_TRANSFORM_ROOT_DEFAULT_TASK_DEEP_POSTAUDIT_R1_20261023)
delivered corrections RH-A01..RH-A07 to this run's package:

- RH-A01: the 0096CDD0 x87 guard was inverted by the executor; fall-through = LT (|v0^2-K|<eps), JP CE6C = GE/masked-unordered; the full output branch beyond 0096CF00 was not examined; Euler/axes interpretation remains hypothesis.
- RH-A02: the 0085CDE0 vcall payload is 48B = 9 transposed DWORD + 3 DWORD at +0x24/+0x28/+0x2C; the 13th input dword belongs to the conditional 13-DWORD cache at X+0x30; standard 3x4/translation-column convention NOT established.
- RH-A03: 13/25B wire advance and defaults=1.0/scale were unproven while 00412430/0040DE60 were unopened. [Successor run 20261023: saved bodies recovered; wire=12B CONFIRMED; 13/25B and 1.0-default REFUTED for those bodies.]
- RH-A04: the B1A tail after two POPs belongs to the same passed block (arg+0x24/0x28/0x2C/0x30), not a separate buffer.
- RH-A05: the reported 10/7/2 task totals were wrong (actual 11/8/3); the two skipped owner-family callsites 005284AC (row 181601) and 00528A00 (row 182002) were the priority continuation.
- RH-A06: failed length reads count toward exposures; packet union = 518 unique rows; at least 14 semantic body units were used, not 12.
- RH-A07: the observer expected PUBLICATION_RESULT.json while the executor wrote PUBLICATION_RECEIPT.json - exact cause of the terminal false-negative; the canonical receipt filename is PUBLICATION_RESULT.json; publication manifests must carry per-file path,size_bytes,sha256.

Science verdict of the predecessor run stands as PARTIAL_PASS_WITH_MATERIAL_CORRECTIONS (process PARTIAL_NONCOMPLIANT_WITH_ACCOUNTING_ERRORS). This notice is additive; the sealed predecessor package is unchanged. Local positives preserved: record -> 00527AB0 -> D_apply -> X=[D+4] -> 0085CDE0 -> pointer[X+2C] slot5 delegation, conditional cache52B at X+0x30, sister 00861030.
