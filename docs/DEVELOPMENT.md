# DEVELOPMENT — how a new RE result feeds the Rosetta pipeline

This is the standing recipe. It is the same flow every finding in
`KNOWLEDGE_COVERAGE.csv` went through. Follow it in order; do not skip the negative
controls — a capability without a falsification attempt is not a capability.

## 1. Pin the source (era + hash)

Register the era and its container hashes in `src/pesource/PEProvenance.js`
(`ERAS.<NAME>`, `KNOWN_HASHES['<era>:<container>']`). Era = physical source + label.
If a file is byte-identical with another era's copy, record it as a **byte coincidence**,
never an alias. The mount boundary verifies the hash and **refuses on mismatch** — that
gate is the point, don't route around it.

## 2. Decode with the era's format module

`PESourceMount` maps era → required archive format (BUNT vs BNT2 vs ArkVFS). Add/extend
the format module in `src/pesource/` (e.g. `BuntArchive.js`). Derive field offsets from
an **audited fixture** — never blind ±4 probes (the material-tail +56 lesson: legacy
TMF1.7's +52 was a misassignment that survived because nobody byte-verified the ramp).
If practical, dual-decode: an independent extraction script vs the repo decoder, and
require 0 mismatches (that is how +56 was locked).

## 3. Emit IR

Decoders produce intermediate representation only (census, hierarchy, TRS, materials,
geometry samples). The browser pages import the decoder modules — **there is no second
parser**. If a format version is not implemented, the reader loud-fails (see the 4.1
gate); do not add a lenient fallback.

## 4. Fixture + unit gates (node)

Generate a fixture (e.g. `src/peworld/IsoMaterialsFixture.js`), write a unit test
script that runs in node and emits a JSON verdict (pattern: `w05_unit_test.mjs` →
`W05_UNIT_TEST.json`). Gates must include **negative controls** (a wrong-offset decode
must fail; a mutant adapter must fail; a hash mismatch must refuse).

## 5. Browser proof (CDP)

Write a headless-Chrome probe that loads the real page and evaluates deterministic
gates (pattern: `w14_browser_probe.mjs` → `W14_BROWSER_PROOF.json`): REVISION check, 0
fatal errors, toggle pixel-difference tests, HUD/badge text assertions. Canvas pixel
statistics substitute for visual review when the session cannot view images — label
screenshots `NOT_VISUALLY_REVIEWED` if so.

## 6. Consumer

Only now wire the IR into runtime code (`src/peworld/*`, `terrain/*.js`). HUD/badge
must state the evidence mode per layer (STRICT_ISO / REFERENCE / ENGINEERING_PREVIEW)
and the source (archive + SHA prefix). If a claim is not on the HUD, it is not claimed.

## 7. Fold into the Rosetta registry

Append a knowledge record to
`src/pe2003/rosetta/bridges/gamebryoReference/KNOWLEDGE_RECORDS_CAMPAIGN_R1.json`
(additive; the J4-hash-gated adapter modules and the frozen J5 records stay
byte-identical). Record shape: `knowledge_record` / `source_build` / `source_hash` /
`claim_status` / `limitation` / `consumer_code_api` / `executed_test_ids` /
`evidence_pointer` / `runtime_enabled`.

## 8. Update the honesty surfaces

- `docs/KNOWLEDGE_COVERAGE.csv` — one row per finding: code → test → consumer.
- `docs/CAPABILITY_MATRIX.json` — the domain's status can only move up with new
  evidence (never from ambition).
- The relevant `docs/*.md` page(s).

## Standing rules

- **Fail-closed**: terminal verbatim errors for unknown data; no partial IR; no
  default-success.
- **Era discipline**: never substitute across eras; REFERENCE items carry the label
  everywhere (HUD, docs, records).
- **Honest animation**: never claim animation from controller presence — measure TRS
  deltas at t0/t1.
- **Oracle discipline** (engine or otherwise): bounded launches, PID/exit ledger,
  exclusive outputs, timeouts, no orphans; oracle data displayed as REFERENCE is never
  presented as a JS parse.
- **Tests re-run live**: the registry gate re-executes the adapter suite; the mutant
  negative control is mandatory — a suite that passes with the mutant present is itself
  broken.
