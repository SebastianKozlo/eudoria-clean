{
  "as_of": "pre-seal",
  "charged": {
    "native_attempts": 13,
    "bodies": 14,
    "unique_rows": 786,
    "exposures": 786,
    "call_edges": 84,
    "candidates": 97,
    "doc_lines": 2600,
    "new_bytes": 643170304
  },
  "measured_actual": {
    "work_bytes": 163685,
    "sci_bytes": 16915,
    "rec_bytes": 40422
  },
  "note": "charged vector per budget_guard --status (29 ledger events, all ADMIT, includes CLOSING admissions Q2/DOC/PUB reserved); measured_actual = physical recursive sizes of WORK/SCI/REC roots pre-seal; PUB checkout bytes to be measured post-seal in REC; new_bytes reservations (PUB 600 MiB) are reserves, not usage; no reservation overrun occurred (no decode/scan exceeded its admitted caps; decoder caps all within admissions)."
}