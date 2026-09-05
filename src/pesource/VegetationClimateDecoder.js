// VegetationClimateDecoder.js — M1 ITER 047 (ledger ITER_033, Gate C wiring).
// Canonical .vcl climate decoder for the PESourceMount layer.
//
// SOURCE FORMAT (CONFIRMED, iter032 RE evidence — Entropia.exe 9.3.5.6746):
//   The .vcl payload is TSV TEXT. The engine builds ArkVegetationClimate objects
//   from the payload string via a stringstream (FUN_004072d0) and
//   FUN_0083a7d0 = THE TSV PARSER: a stream loop reading 12 VALUES PER RECORD
//   (the 12-value stack copy loop, `for (iVar3 = 0xc; iVar3 != 0; iVar3--)`),
//   appending 0x30 (48-byte) records to the climate's row vector — 12 values
//   x 4 bytes = the 48-byte engine record layout. FUNCTION_IDENTITY = CONFIRMED;
//   OBSERVED_OPERATION = CONFIRMED; FINAL_SEMANTIC_ROLE = CONFIRMED (the VCL
//   TSV parser; iter032_findings stage 2).
//
//   The engine reads a FLAT NUMERIC TOKEN STREAM (C++ operator>> semantics):
//   whitespace (tab/CR/LF/space) separates tokens; line boundaries are NOT
//   record boundaries. This reproduces the audited census exactly: 492 engine
//   records from 32 .vcl chunks = 491 lines of 12 numeric tokens + the 9.vcl
//   29-token line contributing a SECOND (continuation) record — 12+12 numeric
//   tokens on one line (iter032_vcl_columns.json).
//
// COLUMN SEMANTICS (census-measured, iter032_vcl_columns.json; cols 6..11
// UNVERIFIED — carried raw, never silently interpreted):
//   col0  model id (int, 256 distinct across the corpus; the GetModel
//         type-0x66 fetch id space — FUN_0094b1d0, iter017b 255/256 resolve)
//   col1  density (0..330, 82 distinct, median 0.6 — role PLAUSIBLE)
//   col2  per-model scale min (0.2..4)
//   col3  per-model scale max (0.5..6; corr(col2,col3)=0.449)
//   col4  per-model elevation band min (0..1000)
//   col5  per-model elevation band max
//   col6..col11 UNVERIFIED (candidates: slope restrictions, jitter, LOD
//         weights, per-axis scale variation — iter032 bound 4)
//
// The per-column VALUE TYPES (int vs float at the FUN_0083a5b0 extractor level)
// are UNVERIFIED (iter032 bound 4); this decoder keeps every value as a JS
// number (the text is numeric throughout — verified by the census over all
// 492 records) and does NOT force a type.

export const VCL_VALUES_PER_RECORD = 12;       // FUN_0083a7d0 12-value loop
export const VCL_ENGINE_RECORD_BYTES = 0x30;   // 48 = 12 * 4 (engine row stride)

/**
 * decodeVclPayload — canonical .vcl text payload -> 12-value records.
 * LOUD failures only (no silent skip): a non-numeric token or a trailing
 * partial record throws; the caller surfaces it.
 * @param {Uint8Array} payload raw .vcl entry bytes (ASCII text)
 * @returns {{records: number[][], recordCount: number, text: string,
 *            valuesPerRecord: number, engineRecordBytes: number}}
 */
export function decodeVclPayload(payload) {
  if (!payload || payload.byteLength === 0) {
    throw new Error('[VegetationClimateDecoder] empty .vcl payload');
  }
  let text = '';
  try {
    text = new TextDecoder('ascii').decode(payload);
  } catch (err) {
    throw new Error(`[VegetationClimateDecoder] payload is not ASCII text: ${err.message}`);
  }
  // FUN_0083a7d0 stream semantics: any whitespace run separates values.
  const tokens = text.split(/\s+/).filter((t) => t.length > 0);
  if (tokens.length === 0) {
    throw new Error('[VegetationClimateDecoder] no numeric tokens in payload');
  }
  const records = [];
  for (let i = 0; i + VCL_VALUES_PER_RECORD <= tokens.length; i += VCL_VALUES_PER_RECORD) {
    const rec = new Array(VCL_VALUES_PER_RECORD);
    for (let c = 0; c < VCL_VALUES_PER_RECORD; c++) {
      const v = Number(tokens[i + c]);
      if (!Number.isFinite(v)) {
        throw new Error(
          `[VegetationClimateDecoder] non-numeric token "${tokens[i + c]}" at record ` +
          `${records.length} col ${c} — LOUD (the engine stream would fail here too)`);
      }
      rec[c] = v;
    }
    records.push(rec);
  }
  if (tokens.length % VCL_VALUES_PER_RECORD !== 0) {
    throw new Error(
      `[VegetationClimateDecoder] token count ${tokens.length} is not a multiple of ` +
      `${VCL_VALUES_PER_RECORD} — trailing partial record, LOUD`);
  }
  return {
    records,
    recordCount: records.length,
    text,
    valuesPerRecord: VCL_VALUES_PER_RECORD,
    engineRecordBytes: VCL_ENGINE_RECORD_BYTES,
  };
}
