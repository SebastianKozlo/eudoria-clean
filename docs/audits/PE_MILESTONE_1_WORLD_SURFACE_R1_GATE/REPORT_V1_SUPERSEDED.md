# FULL_MILESTONE_AUDIT — PE_WORLD_SURFACE_FIDELITY_R1 (MILESTONE 1)
# AUTHOR: pe-master-auditor (the adversarial gate audit; independent of the worker)
# DATE: 2026-09-04 ~16:00 (physical clock; the night-run session)
# STATUS: THE MILESTONE GATE AUDIT -> HARD STOP (no Milestone 2 without the human)

## 0. INPUTS (verified)

- CHARTER: PE_MILESTONE_1_WORLD_SURFACE_R1 (SHA 7A10CD2B... — verified repeatedly across the session).
- THE GATE DELIVERABLE: 02_ANALYSIS\M1_GATE_DELIVERABLE_MATRIX.md (SHA F0C7D0F2...) +
  M1_GATE_DELIVERABLE_MATRIX.json (VALID; F373E60A...) — 19 rows, the fresh regression
  sweep, the era-bounded registry (19), the known-open list (27).
- THE WORKER TRAIL: ledger ITER_019..ITER_034 (16 worker iterations this night-run:
  master-loop iterations 33-48), every session report + evidence tree + git history
  (origin/master in sync; English-only commits).
- THE CLEAN RUNTIME: eudoria-clean @ 8cd0bc3 (three@0.185.0 pinned;
  THREE_R185_PROJECT_BASELINE = CALIBRATED, gate A-J).
- THE LEGACY ORACLE: eudoria-web r169 FROZEN, untouched (verified in every audit).

## 1. ADVERSARIAL VERIFICATION (what I checked, not what I was told)

1. PER-ITERATION AUDITS: all 16 worker iterations audited at raw-evidence level
   during the session (evidence files read directly; SHAs re-hashed; honest
   negatives and loud failures checked; process liveness verified; git states
   reconciled including the parallel-session commits).
2. INDEPENDENT SPOT-CHECKS AT THE GATE: the two load-bearing evidence SHAs
   re-hashed fresh by the auditor (iter019_p0_byte_audit 4C29D220... EXACT;
   iter033_rng_crosscheck F8056CD5... EXACT); the matrix's own re-hash sweep
   (30+ files, 0 failures) accepted as the broader coverage.
3. THE REGRESSION SWEEP: 5/5 clean pages reproduce their recorded deterministic
   hashes EXACTLY on fresh loads (heights 50BD7F9E / materials 5F4677E6 /
   materials_confirmed 3C785581 / water D7C13F1F / foliage A79CB65C) + the
   behavioral stats reproduce (incl. the naive-vs-confirmed whitePct 43.36 vs
   0.0 signature and the foliage-off visibility control).
4. DENOMINATOR DISCIPLINE: stable throughout (51,920 tiles / 220x236 grid /
   9216 region samples / 76 instances / 96+96 texture ids / 178 containers /
   838 terrain functions); every changed denominator explained (492 vs the
   earlier 493 VCL census — off-by-one corrected with byte evidence).
5. THE SELF-CORRECTING LOOP (the audit's strongest evidence): within the
   milestone, WRONG conclusions were caught and corrected by LATER evidence,
   never silently: the iter024 RTTI negative was a file-offset-as-VA bug
   (corrected iter026 — 14 terrain classes resolved); the iter025
   "per-cell renormalization UNVERIFIED" model was REFINED into the engine's
   actual one-hot mechanism (iter027, worked-example gate 0.0%); the iter030
   "type-6 = water-lead planes" naming was REFUTED by the full census
   (iter031: 1/tile LOD-ring texture cache, present on dry tiles too); the
   iter038 "TDF masks feed the details" claim was SUPERSEDED by the 129x129
   detail-selector tables (iter029); the iter028 "server/patcher runtime
   channel" was REFINED to a LOCAL-ONLY fetch with PATCHER-delivered bytes at
   install/update time (iter029); "Geowater:0" auction-UI false positive
   dispositioned (iter031). NO correction was hidden; each is in the ledger.

## 2. THE 19-ROW MATRIX — AUDITOR VERDICTS (summary; full rows in the deliverable)

| Row | Deliverable verdict | Auditor agreement | Note |
|---|---|---|---|
| 1 TERRAIN_HEIGHT | CONFIRMED | AGREE | byte-exact both eras; 3 code paths; oracle 9216/9216; min/max source honestly open |
| 2 TERRAIN_GRID | CONFIRMED | AGREE | 51,920+1 both eras; 6,530 special rows honestly bounded |
| 3 TERRAIN_WORLD_TRANSFORM | STRONGLY_SUPPORTED | AGREE | engine constants CONFIRMED; the global georef [P3b] honestly NOT claimed |
| 4 TERRAIN_MATERIAL_RECORDS | CONFIRMED | AGREE | grammar both eras + 9.3.5 consumer role (vertex-color bake + zone shadow) CONFIRMED by exhaustive 838/838 census |
| 5 TERRAIN_TEXTURE_RESOLUTION | CONFIRMED + honest MISSING | AGREE | 175/175 + 10/10 + 20/20; the climate/detail grids MISSING (patcher) — no proxy claimed |
| 6 TERRAIN_BLEND_SEMANTICS | CONFIRMED (9.3.5) | AGREE | Terrain_14 shader + one-hot factor + filtering verbatim; naive model honestly falsified |
| 7 FOLIAGE_SOURCE | CONFIRMED | AGREE | loader positive @0x00420007; 45 classes RTTI; JUL loader-absence era fact |
| 8 FOLIAGE_MODEL_BINDING | CONFIRMED mechanism + GENERATED_CACHE assets | AGREE | labeled honestly; pesource NIF path queued |
| 9 FOLIAGE_BIOME_RULES | PARTIALLY CONFIRMED | AGREE | structure CONFIRMED; selection honestly [P-CLIMATE] |
| 10 FOLIAGE_DISTRIBUTION | CONFIRMED mechanism + bounded content | AGREE | [P-CELLSTREAM] labeled; census honest (zero-counts recorded) |
| 11 FOLIAGE_SEED/RNG | CONFIRMED | AGREE | position-keyed determinism; 76/76 vs independent python |
| 12 WATER_SOURCE | CONFIRMED | AGREE | technique era-stable byte-proven; no-container negative exhaustive |
| 13 WATER_REGIONS | CONFIRMED | AGREE | coherent components both eras; type-6 hypothesis honestly refuted |
| 14 WATER_LEVEL | CONFIRMED constant / bounded datum | AGREE | 10.0f three-path triangle; naive height==0 hypothesis honestly refuted |
| 15 WATER_TEXTURE | CONFIRMED + honest MISSING | AGREE | four-era byte-identity; waves/sky honestly missing |
| 16 WATER_MATERIAL | CONFIRMED | AGREE | 22 constants verbatim; era-stable |
| 17 WATER_ANIMATION | CONFIRMED mechanism | AGREE | ARK_WATER_WIND closed; env writer honestly open |
| 18 PESOURCE_MOUNT | CONFIRMED | AGREE | era-aware, SHA-enforced, loud failures, versioned decoders |
| 19 RUNTIME_INTEGRATION | CONFIRMED | AGREE | the clean chain + 5/5 deterministic fresh sweep; regional scope honestly stated |

## 3. SPLIT VERDICTS (per the standing audit rules)

- OVERALL_STAGE_VERDICT = **PASS** (the milestone gate deliverable is complete,
  evidence-verified, reproducible, and honest).
- CONTROL_PLANE_VERDICT = **PASS** (every worker session: prompt-hash verified,
  processes killed + liveness-verified, script hashes pre-execution, ledger
  entries, English commits, pushes verified; zero frozen-tree violations;
  eudoria-web untouched throughout).
- RUNTIME_EVIDENCE_VERDICT = **PASS** (r185 CALIBRATED via gate A-J with
  artifacts; all five pages deterministic across fresh loads; negative
  controls present; no evidence from failed runs).

## 4. THE HONEST LIMITS (what this milestone does NOT claim)

1. THE ERA-BOUNDED INPUTS (the biggest architectural finding): the 9.3.5 world
   surface = LOCAL data (TDF tiles, height field, palettes, details, VCL,
   models) + a GLOBAL world-data layer (65x65 climate grid id 432502; 129x129
   detail selectors id 459344) that is **PATCHER-DELIVERED and MISSING from
   every local container** (178-container census; the client fetch is
   LOCAL-ONLY and halts init on miss). The clean runtime therefore CANNOT
   reproduce the 9.3.5 material look faithfully without era-bounded,
   LABELED placeholders ([P1]/[P2]) — and it does NOT pretend otherwise.
   Acquisition path: a patcher-updated era container or a runtime capture
   (post-M1, human-gated).
2. THE CROSS-ERA GEOREF [P3b] UNPINNED (the measured field-vs-tile
   contradiction is preserved as evidence, not papered over).
3. THE JUL_2003 RUNTIME layers (blend/foliage-loader) are era-DIVERGENT facts
   — recorded, never silently bridged (the JUL data remains the historical
   reference; the 2003 client had no foliage loader, byte-proven).
4. THE RUNTIME IS REGIONAL (proven 9-tile regions + the water window) — NO
   full-map claim; models/animations/avatar systems are OUT (the witness
   rule stands; [P-MATERIALS] GENERATED_CACHE labeled).
5. THE KNOWN-OPEN LIST = 27 items, each with evidence pointers and resume
   paths; NONE blocks the charter's gate definition.

## 5. MILESTONE GATE VERDICT

**MILESTONE_1 (PE_WORLD_SURFACE_FIDELITY_R1) = GATE PASSED.**
All four gates (A heights, B materials, C foliage, D water) CLOSED at the
evidence level, the M1-E clean-runtime foundation PROVEN (r185, deterministic,
provenance-complete), the charter's 19-row matrix delivered from evidence,
the era-bounded registry complete and honest, the regression sweep 5/5.

## 6. HANDOFF TO THE HUMAN + THE INDEPENDENT (ChatGPT) REVIEW

The human should send to ChatGPT for the independent post-audit:
- THIS FILE (the FULL_MILESTONE_AUDIT).
- 02_ANALYSIS\M1_GATE_DELIVERABLE_MATRIX.md + .json.
- The charter: PE_MASTER_HANDOFFS\PE_MILESTONE_1_WORLD_SURFACE_R1_...\NEXT_PROMPT.md.
- The ledger: 99_Audits\PE_MILESTONE_1_WORLD_SURFACE_R1\04_SESSIONs\M1_LEDGER.md (ITER_019-034).
- The decisions: 00_PROJECT_CONTEXT\PE_ARCHITECT_DECISIONS_LEDGER.md (entries #1-#9).

OPEN QUESTIONS FOR THE INDEPENDENT REVIEW (my honest list):
1. Does the era-bounded placeholder policy satisfy the historical-fidelity
   standard, or should the missing climate/detail grids be acquired (the
   patcher-era container / the runtime capture) BEFORE the milestone is
   declared closed?
2. The [P3b] georef contradiction: accept as an open bound, or prioritise
   the georef pin?
3. The 27-item known-open list: any item that should be a gate-blocker in the
   reviewer's judgment?
4. The next-milestone options (the human decides; NOT the auditor):
   (a) the emulator/protocol track (the placement-origin capture — now
   STRONGLY motivated by the patcher-delivery finding); (b) the
   clean-runtime expansion (full-map streaming, models/animations via the
   pesource NIF path); (c) the 2003-era runtime layers; (d) other.

## 7. HARD STOP

Per the operating model (ledger #1 / the unattended-night rules): the loop
STOPS at the milestone gate. NO Milestone 2 work begins without the explicit
human decision after the independent review. The state files
(PE_AUTO_LOOP.json = MILESTONE_GATE_REACHED) carry the resume point.

— pe-master-auditor, at the gate, 2026-09-04.
