# EVIDENCE PROVENANCE RULES - EU935_M1_FULL_MILESTONE_AUDIT_R1_20260916

- Physical payloads (original executables, DLLs, BNT/ARK/VFS/NIF/TGA corpora,
  installers, ProcMon traces) are NEVER copied into Git. They stay LOCAL-ONLY
  under `D:\Eudoria_Reconstruction` and the repo working tree.
- LOCAL-ONLY sources are represented in this package by identity metadata only:
  path, era, size, SHA256, source era, and the reproduction method (see
  00_CONTROL/SOURCE_INDEX.md and 03_EVIDENCE/EVIDENCE_INDEX.csv).
- Historical run packages under `docs/audits/` are READ-ONLY for this run:
  this audit reads and cites them; it does not modify, overwrite, or absorb
  them. The single exception is the authorized §19 housekeeping touch on
  `AUDIT_ENTRYPOINT.md` (exactly one verdict cell + one row; PRE_EDIT evidence
  preserved at 00_CONTROL/AUDIT_ENTRYPOINT.md.pre).
- Evidence hierarchy applied: original bytes + independent measurements >
  independently generated evidence > project derivatives > reports > summaries
  > memory. A generated JSON validating another output of the same flawed
  generator is circular; generator lineage was inspected per claim.
- Every hash in EVIDENCE_INDEX.csv for a repo file was computed at this
  persistence by pe-master-auditor; physical-source hashes are PE-MASTER's
  fresh session re-hashes persisted verbatim (with the row-6 stub recomputed
  and byte-verified at this persistence per the contract's explicit
  instruction).
