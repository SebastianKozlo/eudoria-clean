# CORRECTED_STATUS_ALGEBRA.md — PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011

The DA-1 correction replaces the old one-label-per-entry census with a disjoint
**state-vector algebra**. Every declared entry carries exactly one record:

```json
{
  "entryIndex": <stable identity, NOT the name>,
  "name": "<declared name (may be duplicated)>",
  "disposition": "<one of the disjoint named labels below>",
  "admitted": <bool>          // reservation was made (refunded on PARSE_FAILED)
  "payloadRead": <bool>       // a verified payload buffer was obtained
  "analysisStarted": <bool>   // analyzeBlob actually ran for this entry
  "analysisStatus": "<NOT_ANALYZED | COMPLETED | PARTIAL | ANALYSIS_ERROR>"
}
```

## State lattice (per declared entry)

```
DECLARED ──┬─> FILTERED_REGEX | FILTERED_EXTENSION | ENTRY_TOO_LARGE | TOO_SMALL
           │    (admitted=false, payloadRead=false, analysisStarted=false, NOT_ANALYZED)
           ├─> OVER_BUDGET  (admission refused: SYNTHETIC_INPUTS/SCANNED_BYTES; or the
           │                 analysis-capable LAYOUT budget was already exhausted before
           │                 the read — the payload is then NOT readEntry-decoded)
           │    (admitted=false, payloadRead=false, analysisStarted=false, NOT_ANALYZED)
           ├─> PARSE_FAILED (admitted=true [refunded], payloadRead per reader outcome,
           │                 analysisStarted=false, NOT_ANALYZED)
           └─> PAYLOAD_READ (intermediate execution state; finalized to one of:)
                ├─> SCANNED   (analysisStarted=true; analysisStatus=
                │              COMPLETED — analysis ran without its own exhaustion stop;
                │              PARTIAL — its analysis hit a budget stop mid-run;
                │              ANALYSIS_ERROR — analyzeBlob threw)
                └─> OVER_BUDGET (the shared LAYOUT budget was exhausted by an earlier
                                 entry's analysis before this one's turn: the whole
                                 tail is accounted with analysisStarted=false,
                                 analysisStatus=NOT_ANALYZED — the loop never breaks
                                 after the first stopped entry)
```

## File-level records (outside the entry lattice)

- `parseStatus=INPUT_TOO_LARGE` / `UNSUPPORTED`: no invented entry count
  (`declaredEntryCount=null`), no entry dispositions.
- `parseStatus=NOT_OPENED_BUDGET` (file never opened at a retained-candidates stop):
  `declaredEntryCount` is the literal `UNKNOWN_ENTRY_COUNT` string — no catalog is
  invented for a container that was not read; `censusOk=null` (no claim made).

## Derived counters (re-derived from the vectors, never trusted from a field)

- `scannedPayloadCount` = count of `analysisStarted=true` — an admission or a read
  NEVER counts as a performed scan.
- `admittedCount`, `payloadReadCount`, `analysisStatusCounts{NOT_ANALYZED, COMPLETED,
  PARTIAL, ANALYSIS_ERROR}` — separate units (declared entries vs payloads vs
  candidate rows remain separate units).
- `censusOk` (per container) is computed by the **exported `censusGate()`**:
  1. parseStatus must be OK; declaredEntryCount must be a known integer equal to the
     disposition total (sum check);
  2. no duplicate entryIndex;
  3. SCANNED ⇒ analysisStarted=true ∧ payloadRead=true ∧ admitted=true ∧
     analysisStatus ∈ {COMPLETED, PARTIAL, ANALYSIS_ERROR};
  4. non-SCANNED ⇒ analysisStarted=false; OVER_BUDGET ⇒ analysisStatus=NOT_ANALYZED;
  5. recorded `scannedPayloadCount`/`payloadReadCount`/`admittedCount` must equal the
     re-derived counts.
  A mutant that flips a not-analyzed entry to SCANNED **while keeping the sum**
  violates (3) and is refused by the SAME gate that computed the published censusOk.

## Request/refusal algebra (DA-3, section E obligation)

- `layoutAttempts` = REQUESTS, including the one refused at the limit: at a limit of
  60 the run reports 61 requests = **60 executed layout evaluations + 1 refused
  request** (`layoutRefusals=1`). This is never a claim of 61 performed evaluations;
  the refusal record itself names "executed evaluations: 60". `layoutsAdmitted` counts
  admitted layouts separately; `candidatesBeforeCap/candidatesEmitted/capTruncated`
  separate found vs emitted candidates.
- Effective limits: `Budget` constructor AND `analyzeBlob` use-time validation
  (finite safe integers, all five limits ∈ [1, canonical ceiling]); contradictory
  `budgetThresholds` next to a valid supplied Budget → fail-closed refusal;
  non-instanceof budget objects supply NOTHING (canonical ceilings apply);
  a NaN limit throws `INVALID_CONFIGURATION` (never serialized as a valid `null`).
- Distinct-record algebra (DA-2): `MAX_RETAINED_CANDIDATES` bounds the simultaneously
  live DISTINCT records across `found`/per-call candidate lists and `allRows` — the
  forwarded row IS the candidate object (the same object in two arrays counts ONCE);
  a new object with the same fields counts SEPARATELY; CSV/JSON text, indexes,
  configuration and per-axis statistics are NOT candidate records.
