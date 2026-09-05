# FULL_MILESTONE_AUDIT V2 (RE-JUDGMENT) — PE_WORLD_SURFACE_FIDELITY_R1 (MILESTONE 1)
# AUTHOR: pe-master-auditor
# DATE: 2026-09-04 ~18:00 (physical clock; the correction series complete)
# SUPERSEDES: the V1 audit (its PASS verdict was REJECTED by the human independent
#   audit — ledger ENTRY #10 — and is retained as history, superseded, never deleted)
# STATUS: THE GATE RE-JUDGMENT -> HARD STOP -> THE HUMAN + CHATGPT DECIDE

## 0. THE CORRECTION SERIES (what happened after the rejection)

The human's independent audit REJECTED the V1 PASS on a byte-proven critical
error + independent gaps. The mandated correction series (iterations 49-51):

1. **ITER_049 (ledger ITER_035) — the FLOAT64 operand lock (foliage)**: all
   three flagged constants byte-verified from the original Entropia.exe
   (32767.0 FDIV QWORD / 65535.0 FLD QWORD / 0.00007812499825377017 FMUL
   QWORD — the worker's "0.0 statically" + "32768.0" + "2.0f" were the LOW
   DWORDs of 8-byte doubles); the full arithmetic census (17 functions /
   51 FPU instructions; 6 FSTP-DWORD f32 points); the fix (constants f64-
   locked, Math.fround at the binary's rounding points); the ANTI-CIRCULAR
   revalidation (the reference derives constants FROM the binary extraction
   + the ORIGINAL VCL records: 76/76 bit-exact; the human's 9719 vector
   PASS; the OLD circular reference now FAILS 76/76 — the demonstrative
   negative proving the old validation was assumption-circular); the fresh
   deterministic render 8770AAA0 (delta root-caused; the terrain path
   contributed zero delta). Rows 10/11 re-judged: RNG CONFIRMED on the
   byte-locked basis; DISTRIBUTION = mechanism-confirmed + the cell content
   explicitly RECONSTRUCTION-ONLY.
2. **ITER_050 (ledger ITER_036) — the float-constant lock sweep (ALL chains)**:
   the census of every milestone-cited float constant (79 exe VAs + 57 .fx
   tokens + 5 immediates, all byte-locked; the width re-derivation agrees
   with the frozen findings 71/71); the 7 dangers resolved (4 corrected at
   code — the materials_confirmed noise tables used inexact JS literals
   float32-widened; 3 OK; 1 carried) + the RNG draw discovery (the engine's
   exact construction (state & 0xFFFFFFFFFFFF)/2^48 — superseding the
   documented variant; [P4] reduced to the seed only); the revalidation
   2048/2048 bit-exact (the old chain FAILS 2048/2048); the fresh render
   EA4411B5; the regression 4/4 MATCH; **THE ERROR CLASS CLOSED MILESTONE-WIDE**.
3. **ITER_051 (ledger ITER_037) — the ORIGINAL-DIRECT SINGLE-MODEL WITNESS**
   (the decision-#3 requirement the human flagged as missing): the clean NIF
   reader (NifModelReader.js) parses the witness model 457485 from the era
   Models.bnt bytes (loud failures, no fallback); the R61 frozen-python
   cross-validation EXACT (575 leaves / 281 float-hex / 16/16 blocks /
   0 mismatches; byte-identical texture RGBA via two independent decoders);
   the chain demonstrated END-TO-END (Models.bnt -> NIF v10.1.0.0 -> NiTriShape
   16v/8t/2-UV -> NiTexturingProperty -> **NiArkTextureExtraData 457490 — the
   era binds textures via the Ark system; 0/10 candidates contain
   NiSourceTexture (a NEW engine fact)** -> resolveTexture -> TGA2 A32 ->
   deterministic render 381A80C4, 3/3 loads, the ?model-off control differs);
   the regression 5/5 MATCH; the witness-MATRIX next-steps recorded NOT
   executed (the witness rule: one model FIRST).

## 1. THE AUDITOR'S CORRECTIONS TO THE RECORD (demotions stand)

Per ledger ENTRY #10 and the auditor's independent byte verification (the
three constants + the QWORD opcodes DC 35 / DD 05 / DC 0D — confirmed
personally from the original binary, file offsets 0x67D7A8/0x68C758/0x6980D0):
- The V1 audit's PASS verdict: SUPERSEDED (the audit failed to re-derive
  decompilation arithmetic — the recorded LESSON: load-bearing arithmetic
  claims require independent operand-width + constant re-derivation at audit
  time; the 76/76 validation was accepted without checking that the
  validator derived its constants independently).
- "FOLIAGE_FULLY_PROCEDURAL_ZERO_SERVER_RNG": stays DEMOTED to "the local
  spawn-loop chain is decoded; the cell-content origin remains open".
- The matrix rows 10/11: re-judged per ITER_049 (CONFIRMED on the byte-locked
  basis / mechanism-confirmed with RECONSTRUCTION-ONLY content labels).

## 2. THE HONEST LIMITS (stated explicitly — NOT promoted)

1. **The regression sweep (5/5) compares OUR OWN recorded runtime, NOT the
   original client.** An original-client comparison requires a server (the
   emulator/protocol track = post-M1, human-gated). This is a MILESTONE-SCOPE
   LIMIT, stated as such — the deterministic-reproducibility claim stands;
   the historical-visual-parity claim is NOT made.
2. **The water page datum [P-DATUM]**: the engine level 10.0f is in the
   GLOBAL-FIELD datum; the field-vs-tile georeferencing is UNPINNED ([P3b],
   the measured contradiction preserved as evidence). The page's 0.0
   demonstrative control stays labeled.
3. **The foliage cell-content origin**: the placementHash/round(density)
   stand-in + the cell-stream origin + the per-location climate choice =
   RECONSTRUCTION-ONLY (labeled; no historical-truth claims).
4. **The patcher-delivered world-data grids** (65x65 climate / 129x129
   details): MISSING locally (the 178-container census; the client fetch is
   local-only + init-halts on miss) — [P1]/[P2] era-bounded placeholders;
   acquisition = a patcher-updated era container or a runtime capture (post-M1).
5. **The witness MATRIX is NOT executed** (one model proven original-direct
   per the witness rule; the matrix = the next work package if the human
   directs it).

## 3. THE GATE RE-JUDGMENT

With the correction series complete (the FLOAT64/FLOAT32 class closed
milestone-wide; the anti-circular method established; the original-direct
witness delivered; all reconstruction items labeled), the auditor's PROPOSED
verdict:

**MILESTONE_1 = PARTIAL_PASS_CORRECTED** — the four gates (A/B/C/D) +
M1-E stand at evidence-verified statuses with the honest limits above; the
V1 overclaims are demoted; the deliverable matrix (as corrected by
ITER_049/050) + this V2 re-judgment + the ledger = the gate package.

THE DECISION IS THE HUMAN'S (+ the ChatGPT independent review):
- ACCEPT the corrected state and CLOSE Milestone 1 (with the honest limits
  as the recorded boundary); or
- DIRECT the remaining work packages (the witness matrix; the georef pin;
  the patcher-era container hunt; the cell-stream origin) as gate blockers;
  or
- Any other disposition.

The ChatGPT review package: this file + the corrected matrix
(02_ANALYSIS\M1_GATE_DELIVERABLE_MATRIX.md as amended by iter035/036) +
ledger ENTRY #10 + ITER_035/036/037 (the corrections) + the V1 audit
(superseded, for the record).

## 4. HARD STOP

The loop stops at the gate again. NO Milestone 2 without the human.

— pe-master-auditor, at the re-judgment, 2026-09-04.
