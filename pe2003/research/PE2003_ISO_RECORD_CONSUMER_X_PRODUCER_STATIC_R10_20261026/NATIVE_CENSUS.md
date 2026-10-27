# NATIVE_CENSUS - R10 (final as of seal; post-seal PUB totals live in REC)
All children: nask-glm/glm-5-3, depth 1, max 2 active, NO_NESTED_TASKS observed (no grandchild tasks attempted).
| # | job | attempt | role | native task id | result |
|---|---|---|---|---|---|
| 1 | C1 | 1 | research | ses_e83fb90b3ffew9mBcuBin3uvWK | EMPTY return (length-class; no files written) |
| 2 | X1 | 1 | research | ses_e83fb5d78ffevwiJ1pkEwb3CWa | COMPLETE (RESULT+EARLY) |
| 3 | C1 | 2 | research | ses_e83f8847cffelEO5yZqhVJotHL | EMPTY return (no files) |
| 4 | Q1 | 1 | QC | ses_e83f2b3d0ffeBubOOXEfuJcEHr | QC PASS (A=X1, B=C1 fallback) |
| 5 | C2 | 1 | research | ses_e83faf57ffeYopqdA8ePaOPIy | COMPLETE |
| 6 | X2 | 1 | research | ses_e83f9ba5ffe6lFYvPHfXgt06a | COMPLETE |
| 7 | X3 | 1 | research | ses_e83ea7aa1ffeJMR66jRlphS8Sn | COMPLETE (window partial, marked) |
| 8 | P1 | 1 | research | ses_e83ea6252ffew7bSIY1ntky0KK | COMPLETE |
| 9 | X4 | 1 | research | ses_e83e7aa5effewakZvYd13jm | COMPLETE |
| 10 | C3 | 1 | research | ses_e83e79ca9ffea6wIQph5k2eyc0 | COMPLETE |
| 11 | C4 | 1 | research | ses_e83e5c0dcffe4TvLVJSHgwWrl1 | COMPLETE |
| 12 | C5 | 1 | research | ses_e83e47dfeffeeSfJxOVVHheyvK | COMPLETE |
| 13 | Q2 | 1 | QC (closing) | ses_e83e3626affexVwqoUobonJnNW | QC_PASS + P2 finding (accepted, corrected) |
Native attempts: 13 charged, 13 executed (11 COMPLETE, 2 empty length-class failures: C1 a1/a2).
Root fallbacks (separate activities, no native IDs): C1 record-consumer analysis after 2 empty attempts (jobs/C1/attempt_2/ROOT_FALLBACK.md, independently QC-passed by Q1); all bounded_decode executions and raw scans executed by root under admissions (C1-DECODE, C2-DECODE, X3-RAWSCAN, X3-DECODE, X4-RAWSCAN, X4-DECODE, C3-DECODE, C4-DECODE, C5-DECODE, C1-RAWSCAN, X2-RAWSCAN a1/a2); PUB publication mechanics by root under PUB-CLOSING-a1 (no fictional extra native task).
