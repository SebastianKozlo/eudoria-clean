# QC_PHASE_INPUTS — PE_935_CAND4_006C9700_PLUS4_PROVENANCE_R1_20261008

This directory holds the shared-ledger INPUTS for the FRESH internal QC phase (a
separate QC worker dispatched by the parent writes QC_REPORT.md and its own QC
artifacts here; this executor does NOT write QC_REPORT.md and does NOT perform the
independent QC itself — per the delegation, QC_ORIGIN for the executor phase is
NOT_PERFORMED_BY_EXECUTOR, honestly recorded). No fictional/empty evidence is
placed here; the list below is the real input set.

## Inputs the fresh QC worker must independently check (per the run contract §6)

1. RETURN/SOURCE IDENTITY re-adjudication:
   - RETURN_VALUE_TRACE.csv (the five return paths with predicates; PATH_B = R).
   - 01_RAW/FUN_006C9700_PUMP_FULL.txt (body #1 decode; raw bytes; extent proof).
   - 01_RAW/FUN_006E8F70_CTOR_R.txt (the ctor: [R+0]=S; [R+4]=P; return this).
   - 01_RAW/FUN_006C9570_SLOT_SETTER.txt (the slot setter; the CAND-4 path).
   - 01_RAW/FUN_007B79B0_P_GETTER_PARTIAL.txt (PARTIAL extent — verify NO claim is
     made past the 0x007B7A0F window cut).
2. USED BYTES + rel32: re-verify the pin table and the rel32 table against the
   PHYSICAL EXE (03_SCRIPTS/checker_plus4.py is the production gate — the QC must
   use its OWN implementation or manual arithmetic, not merely re-run the executor's
   script; the script exists for reproducibility).
3. STATUS CEILINGS: CLAIM_MATRIX.csv (CL-1..CL-22) — verify no claim exceeds its
   evidence class; especially CL-7 (no-vptr negative), CL-9 (PARTIAL source),
   CL-10 (bounded negative), CL-13 (the T==P alias — roles from two recorded
   callers + this run's measured store, NOT one observed execution), CL-15
   (RESOLVED_AS_POINTER for the CAND-4 chain), CL-19/CL-22 (standing science
   preserved; no promotions).
4. SCOPE LEDGER content (not only the sums): EDGE_ACCOUNTING_LEDGER.csv — re-adjudicate
   the 12 counted units BY ROW CONTENT (E1..E12) and the 9 RAW_VISIBLE_ONLY rows'
   NOT_COUNTED_REASONs (no analysis hidden behind RAW); FUNCTION_BODY_ACCOUNTING.csv
   (4 bodies; the RAW_WINDOW_OVERFLOW disclosure; the not-opened list);
   PLUS4_PROVENANCE.csv (2 writers used of MAX 4; PW-3 = the honest boundary);
   POINTER_LINEAGE.csv (3 hops of MAX 3).
5. CONTROLS: CONTROL_RESULTS.json — the clean pass (80/80), the mechanical
   anchor-corruption results MC1..MC6 (the SAME production gate detecting each
   corruption; the specificity control), and CTRL_A..CTRL_G (SYNTHETIC_LOGICAL_
   CONTROL — verify they match the contract §6 definitions and that no logical
   control is presented as a new physical PCG measurement).
6. Budget compliance: bodies 4/6; edges 12/12 (AT limit — verify NO 13th unit is
   hidden anywhere in the records; the body #4 RAW callsites are the exact place
   to check); writers 2/4; hops 3/3. STOP_BEFORE_EXCEED: the FUN_007B79B0 boundary
   is where the edge budget was exhausted — verify the deeper-origin UNKNOWN is
   kept honestly.
7. Process disclosures to verify: the transient first ls-remote failure (INPUT_
   IDENTITIES.md §1); the historical-caller pin transcription correction caught
   by the production gate (01_RAW/MANUAL_ENCODING_CROSSCHECK.txt item 13 — the
   corrected bytes E8 75 F0 02 00; verify against the physical EXE).

## Additional reads available to the QC (same prohibitions + budget apply)

- The pinned inputs: the two reports (identities in INPUT_IDENTITIES.md §3), the
  historical packages (READ_ONLY; 263/263 BASE-identical at preflight — re-verify),
  AUDIT_ENTRYPOINT.md rows, and the physical EXE (fail-closed identity).
- QC repetition of already-ledgered units is free; NEW units draw from the common
  budget (MAX 6 bodies / 12 edges / 4 writers / 3 hops — 4/12/2/3 already used).
- The QC worker writes QC_REPORT.md + its own artifacts into this directory
  (00_CONTROL_INTERNAL_QC/); it does NOT touch AUDIT_ENTRYPOINT.md, the manifest
  (parent phase) or any historical package.
