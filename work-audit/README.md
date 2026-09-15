# WORK-AUDIT ? independent zero-trust audit reports (auditor artifacts, NOT project canon)

This branch (`audit/work-audit-reports`) collects the working artifacts of the
**WORK-AUDIT** role: an independent, zero-trust auditor of the executor runs of the
Eudoria Reconstruction / PE_935 project (repo: `SebastianKozlo/eudoria-clean`, main
branch: `master`). Every report here was produced by re-executing verifications
against the physical evidence (byte reads, own parsers, re-hashing, own disassembly,
live git), never by trusting the audited delivery's narrative.

Each file carries a WORK-AUDIT provenance header. These are auditor work products:
they do not modify, supersede or constitute the project's canon, and the project's
own packages under `docs/audits/` on `master` remain the authoritative record.

Verdict taxonomy used in the reports (Polish): POTWIERDZONY CALKOWICIE /
POTWIERDZONY CZESCIOWO / ODRZUCONY / NIEROZSTRZYGNIETY (fully confirmed /
partially confirmed / refuted / inconclusive).

## Index of audits

| Directory | Subject | Verdict (see each REPORT.md) |
|---|---|---|
| `audyt-eu935-position-construction-6465019` | completion of an interrupted audit of run PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913 | see REPORT.md |
| `audyt-935-scenefeeder-census-20260914-0900` | publication + closure-message claims of the PE_935_SCENEFEEDER_SLOT_CENSUS run | see REPORT.md |
| `audyt-935-pub-persist-20260914-0648` | publication + PE_MASTER_REVIEW claims audit (LINK30 lineage) | see REPORT.md |
| `audyt-935-link30-identity-20260914-1101` | run PE_935_SCENEFEEDER_LINK30_IDENTITY_R1 (BASE 1a490ee -> HEAD 3644e5a, 34 paths) | see REPORT.md |
| `audyt-auditor-md-flow-20260914` | meta-audit: full read of D:\auditor.md (17,849 lines; the ChatGPT/Codex Desktop independent-auditor conversation) | see REPORT.md |
| `audyt-pe935-slot17-oracle-minicheck-20260914-1515` | run PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1 (3644e5ac..5290e79): 23-claim matrix, 18 confirmed / 3 refuted / 2 unconfirmed; own byte checks 77/77, own COFF re-derivation of the GB112/GB12 vtables from the physical .lib/.obj, rizin cross-disassembly; findings F1 (P2) + F2-F7 (P3) | POTWIERDZONY CZESCIOWO (science results upheld; documentation defects found) |
| `audyt-preloop-cleanup-formalize-20260914-1600` | FORMALIZE delivery of PE_935_PRELOOP_INTEGRATED_CLEANUP_R1: 13/13 claims confirmed incl. the F-FORM-1 census discrepancy and the F-FORM-2 capstone/PYTHONPATH experiment, both reproduced by the auditor; includes an own-gap correction (a GB12 prose-table defect missed by the previous audit) | POTWIERDZONY CALKOWICIE |

## Publication hygiene

- Published on a dedicated branch; `master` untouched; single path-limited commit
  adding only `work-audit/`.
- Excluded from publication: `__pycache__/`, `*.pyc`, and a vendored third-party
  capstone copy (`pylibs/`) found in one audit working directory ? binaries and
  bytecode caches do not belong in an audit report archive.
