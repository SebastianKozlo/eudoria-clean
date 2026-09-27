# F05 — X87 EXACTNESS WORDING + ORIGIN CONSTANT PRECISION

RUN_ID: EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926 (02_ANALYSIS)

## 1. THE WORDING DEFECT

Desktop GC-F05 (P2): PEFoliageCore.js (header ~L38-42 + FOLIAGE_OPERAND_LOCK.exactness
~L123) stated BIT-EXACTNESS unconditionally, while the V4 HONEST LIMITS + the
downstream contract §8 carry the condition (x87 PC in {53,64} + RC = nearest-even;
the actual client CW UNMEASURED). The local declarations overclaimed. Class:
IMPLEMENTATION_COMMENT_OVERCLAIM (documentation), NOT a generator arithmetic
error under the stated model.

## 2. THE CORRECTED SEPARATION (now in the code comments + this package)

1. BYTE-LOCKED OPERANDS = CONFIRMED — the three .rdata QWORDs re-read this run
   from the original EXE bytes (probe r1_f05_precision.mjs; PE section map;
   EXE SHA256 re-verified E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F7537
   65D5280F31):
   - _DAT_00a7d7a8 = 32767.0 f64 (bytes 00 00 00 00 C0 FF DF 40)
   - _DAT_00a8c758 = 65535.0 f64 (bytes 00 00 00 00 E0 FF EF 40)
   - _DAT_00a980d0 = 0.00007812499825377017 f64 (bytes 00 00 00 40 E1 7A 14 3F)
   All match the FOLIAGE_OPERAND_LOCK byte claims.
2. ARITHMETIC MODEL EXACTNESS = CONDITIONAL on the stated model (x87 PC in
   {53,64}, RC = nearest-even): under that model the f64+Math.fround replication
   was proven BIT-EXACT vs 80-bit-then-FSTP-DWORD over the complete input
   domains (iter035; 0 mismatches). PC=24 was measured DIFFERENT (14,104/229,376
   real + 103,073/1,245,184 synthetic) — the condition is LOAD-BEARING. The
   proof is therefore NOT unconditional.
3. ORIGINAL CLIENT RUNTIME PARITY = UNVERIFIED/UNMEASURED (the actual
   foliage-site CW at chain-execution time was never measured — see F01 §5.2 A;
   no runtime experiment authorized or performed).
4. HISTORICAL FOLIAGE INPUTS = NOT RECOVERED ([P-CLIMATE] caller-selected
   climate; [P-CELLSTREAM] stand-in cell content; p3 = *(impl+0x24) UNVERIFIED ->
   0; windowWorld = the caller-supplied CURRENT_RUNTIME_CALIBRATION; the
   historical climate selection unknown; the historical cellstream origin
   unknown). FOLIAGE PLACEMENT 1:1 = NOT CLAIMED.

The authorized comment corrections implement exactly this four-way separation
(03_EVIDENCE/DIFF_PEFoliageCore.js.patch; zero executable-code change; the
exported FOLIAGE_OPERAND_LOCK.exactness metadata string now carries the
condition). The pre-existing honest bounds ([P-CLIMATE], [P-CELLSTREAM], P-RNG-P3,
P-SCALE-FIELDS, P-WINDOW) are preserved verbatim in the file.

## 3. §10 THE ORIGIN CONSTANT (typed-K precision control)

CANONICAL FORMULA (per GEOREF_ORIGIN_SCALE_AUDIT.md — CONFIRMED; preserved):

    out[i] = f32(f32(W[i] * (double)(float)0.01) - S[i])

The K constant is f32(0.01) WIDENED to f64 — NOT an unconstrained binary64
0.01 literal. The historical downstream contract §1 L11 shortened this to
`out = f32(f32(W * 0.01) - S)` — ambiguous and, read as a binary64 literal,
WRONG for at least one control:

PRECISION CONTROL (W=5, S=0; repo node v22.22.0; probe r1_f05_precision.mjs;
03_EVIDENCE/F05_PRECISION_CONTROLS.json):

| K reading | formula | f32 result (decimal) | hex bits |
|---|---|---|---|
| K = f32(0.01) widened to f64 (byte-faithful) | f32(f32(5 * (double)(float)0.01) - 0) | **0.04999999701976776** | **0x3d4ccccc** |
| K read as binary64 literal 0.01 (0x3F847AE147AE147B) | f32(f32(5 * 0.01) - 0) | **0.05000000074505806** | **0x3d4ccccd** |

DISTINCT results — Desktop's two claimed values re-derived EXACTLY (both decimal
and bit pattern). K_f32 = 0x3c23d70a (0.009999999776482582...). The successor
downstream corrections (DOWNSTREAM_CONTRACT_CORRECTIONS.md §1) restore the
`(double)(float)0.01` cast with this control cited.

## 4. ORIGIN STATUS SEPARATION (preserved; nothing resurrected)

- INITIAL S=0 = evidence-backed (the static initialization line; ORIGIN_INITIAL_ZERO
  CONFIRMED).
- MUTATION_CHANNEL_EXISTS = evidence-backed (writer 0x00458E27 — 3 f32 stores;
  re-read this run in the F05 probe context of the binary: e844f1fdff8b5424... =
  the 3-store writer pattern at the pinned address; setter FUN_00458D90:
  S := f32(-(int32)in)).
- SETTER_EXISTS = evidence-backed.
- ACTUAL NONZERO MUTATION IN A SPECIFIC HISTORICAL SESSION = UNVERIFIED
  (STATIC-ONLY; the runtime value is a later-milestone dependency).
- ORIGIN_PERMANENT_ZERO: NOT resurrected (retraction PRIOR-2 preserved).
- Unconditional W*0.01: NOT resurrected (retraction PRIOR-3 preserved; the
  successor formula keeps S and the typed K).

## 5. RESULT

Desktop GC-F05 REPRODUCED: the exactness overclaim documented and corrected
(comment-only; zero arithmetic change); the typed-K control re-derived exactly
with hex bit patterns; the four-way separation + origin status separation now
binding in the code comments and the successor contract content. V4 row 11
itself already carried the conditional model and needed no change (the row was
the correct formulation; the code comments were the defect).
