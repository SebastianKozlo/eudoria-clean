# SELECTION — PE_GAMEBRYO_ORACLE_TOOL_R1_20261003
# TEST-CORPUS PREREGISTRATION (rules fixed by the formalizer BEFORE any
# oracle execution; the executor fills ONLY the T1-T5 rows and the lock
# record, then hash-locks this file)

## 1. Fixed selection rules (preregistered; NEVER result-driven)

- **T1 = 218757.nif** — fixed by the human order (the 218757 probe asset).
- **T2** = the mechanically SMALLEST 10.1.0.0 NIF in the Models.bnt corpus
  (by payload size).
- **T3** = the mechanically LARGEST-BLOCK-COUNT 10.1.0.0 NIF (by
  num_blocks; structurally different from T2 by construction).
- **T4** = the mechanically SMALLEST 4.1.0.12 NIF in the Models.bnt corpus.
- **T5** = the overall SMALLEST NIF in Models.bnt by payload size (ANY
  version), EXCLUDING T1, T2 and T4; if the smallest is one of those, the
  next distinct smallest is taken.

**Mechanical** means derivable ONLY from the pinned prior version census
artifact + the Models.bnt index (below), WITHOUT looking at any oracle
result, any GAMEBRYO_ORACLE_TOOL output, any original-tool run, or any
semantic judgement about file content. Selection is computed BEFORE the
first oracle execution on ANY of T1-T5 and is NEVER revised afterwards
except by a recorded, evidence-backed protocol-violation finding.

### Tie-breaks (fixed now, deterministic)

- T2/T4/T5 (min payload size): if two candidates have equal size, the one
  with SMALLER num_blocks wins; if still tied, the lexicographically
  smallest `name` wins.
- T3 (max num_blocks): if tied, the LARGER payload size wins; if still
  tied, the lexicographically smallest `name` wins.
- Candidate EXCLUSION (mechanical, recorded): a candidate that is absent
  from the Models.bnt index, or whose manifest size disagrees with the
  Models.bnt index size for the same name, is EXCLUDED and the next
  candidate per the rule is taken; every exclusion is recorded in the
  selection evidence with its reason.

## 2. Pinned mechanical basis (identities fixed by the formalizer 2026-10-03)

| Basis artifact | Identity |
|---|---|
| Per-file version census (PRIMARY basis: per-file `version`, `size`, `num_blocks`, `sha256`) | `docs/nif/corpus/pcg953_nif_manifest.csv` — 2,827,906 B — SHA256 `2BE0DEFC9C09FF26371528A4601C10216AC3013717A244EB0652169123989B59` — 5,596 logical rows (Import-Csv; NOT 5,612 physical lines — embedded newlines in quoted fields); version distribution 4,838 x 10.1.0.0 + 757 x 4.1.0.12 + 1 x 4.0.0.2 |
| Audited per-entry BNT census (cross-check: per-entry `offset`, `size_stored`, `sha256_stored`) | `docs/audits/PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915/01_RAW/NIF_VERSION_CENSUS.csv` — SHA256 `962B10ABCB38F98A14F18950E66E30E65B835648D810B62979DFA8517960585D` — 5,596 entries |
| Container authority | `D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt` — 395,412,868 B — pinned SHA256 `C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0` (the executor RE-HASHES it fail-closed before use; on mismatch: HARD STOP, no selection) |

Rules of use:
1. Selection candidates come from the per-file census (manifest) filtered
   by the fixed rules above; every selected candidate MUST cross-check
   against the Models.bnt index (same name present, same size) before it
   is final. The Models.bnt index is parsed from the physical Models.bnt
   by the executor (the pinned audited index facts: index_start
   395,262,727, entry_count 5,596 — reference values from the interrupted
   run's EXTRACT_PROVENANCE.json, UNVERIFIED_REFERENCE; the executor
   re-derives them from the physical file).
2. The manifest is a PRIOR audited project artifact (frozen R61 parser
   lineage) — it is NOT an output of the new oracle, so using it does not
   violate result-independence. The NEW GAMEBRYO_ORACLE_TOOL must not be
   used for selection in any way.
3. The manifest must be parsed with a real CSV parser (embedded newlines;
   see PREFLIGHT section 5). The executor re-verifies the manifest SHA256
   before selection; on mismatch against the pin above, selection HALTS
   and the discrepancy is returned to PE-MASTER (the basis may have
   changed under us).
4. NIF version for each selected T is re-read from the EXTRACTED file's
   own header (not copied from the manifest) when the rows are filled.
5. `manifest_2003.csv` (docs/nif/corpus/) is the 2003-era corpus — WRONG
   ERA for this run's T-corpus; NEVER a selection source here.

## 3. T1-T5 rows (EXECUTOR FILLS — then hash-locks this file)

| T | Source container | Asset name/id | Payload offset (B) | Payload size (B) | Extracted local SHA256 | NIF version (from file header) | Mechanical selection reason |
|---|---|---|---|---|---|---|---|
| T1 | D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt (re-hashed this run: SHA256 C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0, 395,412,868 B, PIN MATCH) | 218757.nif (fixed by human order) | 116,223,520 | 57,316 | 3E8A22C2213202207E374B55CD65B2C3BE039CCDD1E8D01A07FCAF44DE12CF36 | 10.1.0.0 (header line "Gamebryo File Format, Version 10.1.0.0"; num_blocks from header = 66) | FIXED BY HUMAN ORDER (not mechanical). Index entry 781, name_file_offset 395,283,797; all interrupted-run UNVERIFIED_REFERENCE cross-checks MATCH (offset/size/sha256/header/num_blocks). |
| T2 | D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt (same re-hash as T1) | 533021.nif | 76,840,444 | 537 | 9CFF776D204AEC7B64377DD365AC11A71C9DCFA4A00A5905E642EE7420D5DC28 | 10.1.0.0 (header line "Gamebryo File Format, Version 10.1.0.0"; num_blocks from header = 6) | min size 10.1.0.0 = 537 B over 4,838 candidates; tie-break applied: 547226.nif is also 537 B with equal num_blocks 6, lexicographically smallest name wins (533021 < 547226); no exclusions. |
| T3 | D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt (same re-hash as T1) | 496633.nif | 101,046,525 | 2,068,670 | 4DBCC7311884C453CBBB2255C1592994A225088D1D9BBB47D2D0C287580B7369 | 10.1.0.0 (header line "Gamebryo File Format, Version 10.1.0.0"; num_blocks from header = 1,288) | max num_blocks 10.1.0.0 = 1,288 blocks over 4,838 candidates (unique maximum, no tie); no exclusions. |
| T4 | D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt (same re-hash as T1) | 223534.nif | 59,511,426 | 948 | 81CB4D8D1ABC166C8384FCBD8CDAC4D93FE9D925BCF79FF7E6DFAC13D1000BE0 | 4.1.0.12 (header line "NetImmerse File Format, Version 4.1.0.12"; num_blocks from header = 10) | min size 4.1.0.12 = 948 B over 757 candidates; no tie, no exclusions. |
| T5 | D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt (same re-hash as T1) | 547226.nif | 110,752,130 | 537 | D7F2A02CC86FBFAEFF10FFEA285E0A7A5BB7745494E888F79239D84D73E5F8DB | 10.1.0.0 (header line "Gamebryo File Format, Version 10.1.0.0"; num_blocks from header = 6) | overall min size over 5,593 candidates (all 5,596 minus T1/T2/T4 names) = 537 B; the equal-size candidate 533021.nif is T2 and excluded by rule; next distinct = 547226.nif; no exclusions by cross-check. |

Required per-T values (all mandatory, none may stay PENDING after lock):
container path; asset name/id; payload offset within the container;
payload size; SHA256 of the EXTRACTED local copy (in THIS run's sandbox);
NIF version string read from the extracted file's header; the mechanical
reason quoting the rule and the measured extremum (e.g. "min size 10.1.0.0
= N bytes over 4,838 candidates; tie-breaks not needed / applied: ...").
Record also the candidate-pool sizes used (e.g. "4,838 x 10.1.0.0"), any
exclusions with reasons, and the exact basis artifact hashes used at
selection time.

Reference cross-check values for T1 (from the interrupted run, read-only,
UNVERIFIED_REFERENCE — the executor re-derives all of them from the
physical Models.bnt): entry_index 781; name_file_offset 395,283,797;
payload offset 116,223,520; size 57,316; stored payload SHA256
3E8A22C2213202207E374B55CD65B2C3BE039CCDD1E8D01A07FCAF44DE12CF36; header
"Gamebryo File Format, Version 10.1.0.0"; num_blocks 66. The old
interrupted-run sandbox copy (`...PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003\sandbox\218757.nif`)
may be used ONLY as a cross-check; T1 is RE-EXTRACTED FRESH from Models.bnt
into THIS run's sandbox.

## 4. Lock protocol (binding, G-SEL-1)

1. The executor fills the T1-T5 rows (section 3) — and NOTHING else in this
   file — during batch E1, BEFORE the first oracle execution on ANY of
   T1-T5.
2. The executor then computes SHA256 of this file in its filled state
   (SELECTION_LOCK_SHA256) and records it — with a UTC timestamp, the
   executor identity and the basis artifact hashes actually used — in a
   SEPARATE file `04_EVIDENCE/SELECTION_LOCK.json` (this file itself is
   NOT edited after lock; appending the hash here would change the hash).
3. SELECTION_LOCK.json's creation time MUST precede the creation time of
   the FIRST oracle output on any T (raw evidence creation order must be
   consistent with the lock; G-SEL-1 is FAIL if the order is violated or
   unverifiable).
4. After the lock, this file is IMMUTABLE for the rest of the run. Any
   post-lock edit (other than a PE-MASTER-dispatched correction with a
   recorded protocol-violation finding) = G-SEL-1 FAIL.
5. The run MANIFEST_SHA256.csv must contain this file with a hash equal to
   SELECTION_LOCK_SHA256 (byte identity of the locked state).

## 5. Payload discipline (binding)

- ALL T payloads stay LOCAL_ONLY in THIS run's sandbox
  (`D:\Eudoria_Reconstruction\99_Audits\PE_GAMEBRYO_ORACLE_TOOL_R1_20261003\sandbox\`);
  extraction provenance per T recorded in `04_EVIDENCE/EXTRACT_PROVENANCE.json`
  (container identity + re-hash, index entry used, offset/size, extracted
  SHA256, method).
- ONLY identity metadata (name/id, offset, size, SHA256, version) enters
  the repo/package — never payload bytes (G-PAYLOAD-1).
- Modified/corrupted copies created for controls stay in the sandbox and
  are never published.
