# F02 — VCL CORPUS / DECODER REVALIDATION

RUN_ID: EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926 (02_ANALYSIS)

## 1. THE CLAIM CHAIN UNDER TEST

1. Historical census (m1_iter032k_vcl_columns.py, TSV-line based): 492 nonempty
   lines; numeric_rows_12cols = 491; 3 "special" tab-rows (3.vcl ntok 17, 9.vcl
   ntok 29, 9.vcl ntok 18); distinct models 256.
2. Documentation chain: "492 engine records from 32 .vcl chunks = 491 lines of 12
   numeric tokens + the 9.vcl 29-token line contributing a SECOND (continuation)
   record" (VegetationClimateDecoder.js header, pre-edit) + "the text is numeric
   throughout — verified by the census over all 492 records" (ibid.) + V4 row 7
   VALIDATION "the '493' lead corrected to 492" + V4 row 7 IMPLEMENTATION
   "reproduces the audited 491-line + 9.vcl continuation census exactly".
3. Desktop claim (GC-F02, P1): the chain is false — the raw stream = 493 groups;
   the current decoder = 31/32 files + 472 records + 25.vcl throws; the historical
   chain dropped the comma line.

## 2. INDEPENDENT RE-DERIVATION (this run's own probes)

Corpus: VegetationClimates.bnt re-hashed fresh = 7B858401C3EEBDA574DF4B4517E7FB2A
8149C283885F27187682AA1239C745F4 (25,346 B). BNT2 trailer parse (the historical
generator's rules): 32 .vcl entries, index consumed exactly.

CENSUS (03_EVIDENCE/F02_VCL_CENSUS.json; probe r1_f02_vcl_census.mjs; node
v22.22.0):

| quantity | value | vs Desktop |
|---|---|---|
| files | 32 | MATCH |
| nonempty TSV lines | 492 | MATCH |
| whitespace tokens | 5,916 | (= 493 x 12) |
| groups of 12 | 493 (integer total) | MATCH |
| groups fully numeric | 492 | MATCH |
| comma tokens | 6 (all in 25.vcl group 9) | MATCH |
| whole-file decoder successes | 31 | MATCH |
| whole-file decoder failures | 1 (25.vcl) | MATCH |
| records returned by successful files | 472 | MATCH |
| distinct model ids, raw TSV col0 | 256 | MATCH |
| distinct model ids, decoder-returned | 246 | (Desktop: 246) MATCH |
| ids lost with 25.vcl | 10 | — |
| first bad token payload offset | 447 ("0,2", group 9, col 1) | MATCH byte-exactly |
| bad-token offsets | 447, 451, 455, 470, 475, 481 | MATCH all six |

25.vcl payload: offset 17286, size 1030, SHA256 re-hashed =
89ACABE78A812F344F03F5FEB48BECA529D9B2545682CD77505675C21B513E45 (pin MATCH,
re-derived from raw bytes). The comma line = the 10th nonempty line of 25.vcl
(0-based index 9), 12 whitespace tokens:

`545504 | 0,2 | 0,8 | 1,1 | 12 | 50 | 10 | 5 | 0,01 | 0,1 | 0 | 0,1`

(six comma tokens; the model-id slot col0 = "545504" is itself numeric — the
row still cannot pass a 12-numeric check because of col1).

THE 9.VCL "29-TOKEN LINE" ADJUDICATED: the historical "29-token" is the TAB-split
field count (12 numeric + 5 EMPTY fields + 12 numeric = 29 fields); in the
WHITESPACE token stream the same line = 24 tokens = 2 records (12+12). Both
numbers are true in their own tokenizations; the whitespace stream (the engine's
operator>> semantics per the iter032 decompile) sees 24. Special lines corpus-wide
reproduced exactly: 3.vcl = 17 tab fields / 12 ws tokens; 9.vcl = 29 / 24;
9.vcl = 18 / 12.

THE HISTORICAL GENERATOR BEHAVIOR (re-run proof): a byte-identical copy of
m1_iter032k_vcl_columns.py (SHA256 202FE509... == historical original, proven)
was executed with ONLY the OUT line patched (one-line diff recorded; run copy
SHA256 6DC0067D... — AMEND_R1 QC-P3-3 note: the RUN copy's spurious UTF-8 BOM
was stripped, so it is now byte-identical to the historical original except
that single OUT line) against the hash-pinned corpus, output redirected to THIS
package (03_EVIDENCE/F02_ITER032K_RERUN_vcl_columns.json). Result:
numeric_rows_12cols = 491; total_rows_alltokens = 492; special rows 3;
distinct models 256 — the historical output REPRODUCED exactly. The historical
iter032_vcl_columns.json is byte-untouched (SHA before == after ==
A62D9473D6D6D82C97595CEECCBCB915490F95A2B0F14750DBC03075A6526789). The float(t)
ValueError path (lines 76-84) SILENTLY SKIPS the failing row (ok=False; break; no
error record; the row is simply not appended) — the comma line is dropped from
numeric_rows_12cols with NO accounting anywhere.

THE EXACT DEFECT: the raw whitespace stream has 493 groups; the comma group is a
FULL 12-token group; the TSV-line route silently dropped it; the historical
narrative "492 engine records" matches NEITHER the raw stream census (493 groups)
NOR the current decoder's behavior (31/32 files + 472 records + 1 unsupported
file). The "the '493' lead corrected to 492" sentence in V4 row 7 got the
direction wrong: 493 is the true raw GROUP count; "492" is the artifact of a
TSV-line census that silently skipped the comma line. (The coincidence that
492 = 493 − 1 is exactly the dropped group.)

RUNTIME BEHAVIOR DEMONSTRATION: `Number("0,2")` = NaN in the repo node runtime
(Number.isFinite false) -> decodeVclPayload throws — the LOUD fail-closed path;
the input is NOT normalized. The exact current exception (reproduced):

```
[VegetationClimateDecoder] non-numeric token "0,2" at record 9 col 1 — LOUD
(the engine stream would fail here too)
```

## 3. §6.4 ORIGINAL-CLIENT SEMANTICS (reported separately; statuses only as established)

Per the existing iter032/iter035 evidence (cited, not extended):
- FUNCTION_IDENTITY of FUN_0083a7d0 = the VCL TSV parser: CONFIRMED (iter032
  findings stage 2 — the address-cited decompile; iter032_findings.json
  AF8B9000...).
- OBSERVED_OPERATION = a stream loop reading 12 values per record (the 12-value
  copy loop `for (iVar3 = 0xc; iVar3 != 0; iVar3--)`) appending 0x30 (48-byte)
  records: CONFIRMED (same evidence).
- FINAL_SEMANTIC_ROLE = the VCL TSV parser: CONFIRMED (same evidence).
- FUN_004072d0 = the stringstream constructor family feeding it (iter032).
- TOKENIZATION_SEMANTICS for the comma tokens = UNVERIFIED (no evidence shows
  what the engine's operator>> does with "0,2" — whether it parses "0" then
  fails on ",2", accepts it, or anything else).
- NUMERIC_CONVERSION_SEMANTICS = UNVERIFIED. LOCALE_SEMANTICS = UNVERIFIED.
- COMMA_DECIMAL_SEMANTICS ("0,2 means 0.2") = UNVERIFIED — NOT claimed anywhere
  in this package.
- FAILURE_HANDLING (what the engine does with 25.vcl) = UNVERIFIED — the JS
  throw proves only the JS decoder's behavior; "the original client rejects
  25.vcl" is NOT claimed from JS/Python behavior.

## 4. §6.5 STRICT PARSER-CHANGE RULE (honored)

NO behavior change was authorized or made. The existing bounded evidence does
NOT prove original-client comma/locale semantics, so the fail-closed flow,
tokenization regex, throw messages and record assembly are byte-identical
(pre/post-edit execution control: 31/1/472 + identical exception — see
MODIFIED_PATHS.csv). 25.vcl is documented =
UNSUPPORTED_BY_CURRENT_DECODER (comma tokens, group 9); the coverage deficit is
carried explicitly (V4_1_DELTA rows 7/9/18/19). NO comma->dot replacement; NO
"compatibility parsing".

RESIDUAL (recorded, not fixed): the thrown message string contains the
parenthetical "(the engine stream would fail here too)" — an UNVERIFIED
engine-behavior claim inside a behavior-locked string. Editing it would be a
behavior change (not authorized). Proposed wording for any future authorized
change: drop the parenthetical or mark it UNVERIFIED_ENGINE_CLAIM. Carried in
FINDINGS.csv open_residue.

## 5. §6.6 BLAST RADIUS (re-evaluated)

AFFECTED (see V4_1_DELTA.csv for dispositions): row 7 (CONTRADICTION_FOUND — the
old MATCH false), row 9 (denominator wording corrected), row 18 (coverage
wording corrected: "32 .vcl decode-verified" -> 31/32 + 1 unsupported),
row 19 (scope note: no full-corpus decoder PASS), M1-CL-07 measured text,
FOLIAGE_AUDIT "492 rows" (historical; successor edge), the decoder comments
(EDITED per authorization), PESourceMount.getVegetationClimate coverage claims.

NOT AFFECTED (with the reason): the climate-0 demo / 76 instances / spawn-loop
mechanism / RNG constants / conditional arithmetic model — NO physical
dependency: the demo and the iter035 validation consume 0.vcl (a fully numeric
12-record file; its bytes are unchanged and it decodes identically), the
mechanism claims are address-level RE (FUN_0098fe00/00990810/0095b180/
0098cdf0/0098ce30 decompiles), and the byte-locked operands were re-verified
this run from the EXE bytes (F05 probe). The loader/RTTI/source-graph claims of
row 7 (FUN_0041dae0, factory @0x00420007, 45 RTTI classes) are independent of
corpus tokenization. The 256 raw-id census and the 491-row correlation values
stand (their denominators are now stated accurately). Nothing here claims the
original engine loaded 492, 493 or 493-minus-one records — that number is
UNKNOWN pending engine-semantics evidence.

## 6. RESULT

Desktop GC-F02 REPRODUCED in full (every count independently re-derived and
matched; the historical chain defect demonstrated by re-running the historical
generator as a byte-identical copy). Formal CONTRADICTION_FINDING recorded at
V4 row 7; correction edges NEW-F02 in RETRACTION_SUPERSESSION_DELTA.csv; the
authorized comment-only code corrections applied with a proven zero behavior
change.
