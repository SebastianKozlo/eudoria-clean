# SUPERSESSION.md — PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011

## What is superseded

The historical PRE identity **generator** of run
`PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011`
(`docs/audits/PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011/PRE/gen_pre_identity.mjs`,
git blob `9c57e2bc9c75e596d76cea9d8200cb31808c2719`) is **superseded as an identity
GATE** by `tools/placement_probe/verify_inputs.mjs` +
`docs/audits/PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011/PRE/verify_inputs_runner.mjs`.

## Why (limited supersession, precisely stated)

1. The historical generator wrote `verdict: 'PASS'` as a **string literal** in the
   object it produced (see `PRE/PRE_MEASUREMENTS.json` → `PA2_LITERAL_PASS_GATE.literalVerdictLines`).
   It recorded `expected` and `measured`, but the verdict was never computed from a
   comparison. A literal PASS therefore **proved no effective gate existed**: with a
   mutated input it would still have reported PASS.
2. The historical `PRE/INPUT_IDENTITIES.json` of that run does contain measured
   identities that MATCH the pins — this run does not dispute the historical measured
   values and does NOT claim that a wrong input was historically used.
3. The historical run additionally mentioned a manual identity check. That manual
   check remains **UNVERIFIED**: there is no recorded evidence either way about
   exactly which bytes it measured or when, so no claim is made about it.

## What replaces it and how

- `tools/placement_probe/verify_inputs.mjs`: 16 **frozen expected** size/SHA256 pins
  (constants copied from the human-authorized INPUT_PINS.json whose own identity was
  verified in this run's fail-closed BOOT), **separate measurement**, and a
  **conditional** verdict: `MISSING | SIZE_MISMATCH | SHA_MISMATCH | MATCH` per pin;
  the aggregate verdict is `PASS` only when all 16 match, else
  `BLOCKED_INPUT_IDENTITY`.
- `PRE/verify_inputs_runner.mjs` actually invokes the gate in the REAL sequence —
  after implementation and BEFORE POST/qualification — and gates all downstream
  work: after a BLOCKED verdict, ZERO downstream analysis/correction/ref-reservation
  calls happen (spy-proven; see `POST/IDENTITY_GATE_LIVE_RECEIPT.json` and
  `POST/IDENTITY_GATE_COUNTERCHECKS.json`).
- Mutant verification on PRIVATE copies with UNCHANGED expected pins: clean → PASS
  (16/16, exit 0); same-size-wrong-SHA → BLOCKED (exit 3); wrong-size → BLOCKED;
  missing → BLOCKED. Every mutant's `downstreamCallsAfterGate` is all-zero, and no
  mutant performs a real GitHub write.

## What is NOT superseded

- The historical package `938aa946` stays READ_ONLY and preserved (37/37 blobs
  unchanged; `PRE/SOURCE_PACKAGE_FREEZE.json`), including the old generator, the old
  verdicts and the old timestamps.
- The historical measured identities are not retracted; only the GATE VALUE of the
  literal PASS is superseded.
