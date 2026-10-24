# AGENTS.md — PE2003 public research rules

Adapted from the private PE2003 program rules (sanitized: no private corpus
paths; concrete paths are parameters, not constants).

## Primary target

Project Entropia 2003 (CD-era, "Commercial Open Trial", client 4.02.0000).
Do not automatically return to the 9.3.5-era client; 9.3.5 results may be
used only as explicitly-labeled oracles, never as 2003 proof.

## Rules

1. Every build/asset corpus requires its own physical provenance (hash,
   source, extraction path). Names and mtimes are not provenance.
2. Model-instance-transform-source joins are proven per model, separately.
   COMMON findings do not close a model-specific join (no cross-model
   promotion).
3. Era discipline: no cross-era ID/offset/VA/instance transfer. A manifest row
   from a mixed corpus is a locator, not an era proof.
4. Game data, keys, raw listings, authoring prompts and databases stay
   private. The public projection lives only under `pe2003/` and is
   sanitized (hashes/offsets/own code allowed; payloads, dumps and secrets
   forbidden).
5. Standing of published material: ADVISORY_PENDING_EXTERNAL_POSTAUDIT,
   CANONICAL_GATE_EFFECT=NONE. Publication is not scientific acceptance.
6. Workers write only within their job WRITE_ALLOWLIST. One writer owns the
   shared repo/index at a time.
7. Evidence taxonomy (exact vocabulary):
   CONFIRMED / STRONGLY_SUPPORTED / PLAUSIBLE / UNVERIFIED / REJECTED.
   A negative with a denominator is a result; UNAVAILABLE is not NO.
8. Tools published under `pe2003/tools/` must take all corpus paths as
   parameters (argv/config) — never hard-coded private paths — and must not
   embed secrets or game payloads.
9. Each research run keeps: report, gates, artifact manifest, handoff, and an
   explicit list of what was NOT published and why.
