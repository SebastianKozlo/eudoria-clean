#!/usr/bin/env python3
# -*- coding: ascii -*-
# v4_manifest_claims.py - the per-claim provenance compositions (independent
# truth / why_non_circular / failure_case / dependencies), composed FROM THE
# V4 FIELDS (never from the old matrix's carried fields). Key: row number ->
# the four provenance fields.

CLAIM_PROVENANCE = {
 1: {
  "independent_source_of_truth": "the ORIGINAL 50.bnt/terrain.bnt bytes re-decoded by a SECOND minimal parser (tools/p0_byte_audit.js - no shared code); the FROZEN r169 oracle chunk (built from JUL-identical source tiles by the independent legacy pipeline); the audit-accepted iter002 full-map SHA record",
  "why_non_circular": "the byte-audit parser shares no code with the runtime decoder; the oracle chunk was built by a different pipeline from independently-extracted bytes; the full-map SHA is compared against a frozen prior acceptance record, not against this run's own output",
  "failure_case_detected": "any sample mismatch at any of the 9x1024 height samples, any oracle-chunk divergence, or a full-map SHA != 3DC16D52... would FAIL the row",
  "dependencies": ["ROW 2 (the grid decode feeds the tile addressing)", "ROW 18 (the mount layer)"]
 },
 2: {
  "independent_source_of_truth": "the full-corpus walk counts the exact consumption 51,920/51,920 against the BUNT/BNT2 footers themselves; the era-validation walks all 58,451 PCG entries; the denominator checks run in-browser on the assembled image",
  "why_non_circular": "the denominators are counted from the physical container footers, not from the decoder's own bookkeeping; the in-browser checks consume the assembled product, not the counters",
  "failure_case_detected": "any walk failure, any consumption != 51,920, or a wrong assembled denominator (7040x7552) would FAIL",
  "dependencies": ["ROW 1", "ROW 18"]
 },
 3: {
  "independent_source_of_truth": "the engine constants are read from the decompiled/disassembled binary at cited VAs (FUN_0082b790, FUN_009478e0, the ArkHeightTree root size key) - static code facts, not runtime self-reports; the renders are compared against the heights oracle of rows 1-2",
  "why_non_circular": "the constants come from static RE of the pinned binary (Entropia.exe SHA E7785430...), independent of the runtime implementation that consumes them",
  "failure_case_detected": "a vtable/root-size reading that contradicts the renders, or a render divergence vs the heights oracle, would FAIL; the [P3b] georef contradiction is recorded, not resolved",
  "dependencies": ["ROW 1", "ROW 2"]
 },
 4: {
  "independent_source_of_truth": "the INDEPENDENT DataView-level parser (iter020 64/64, iter021 95 records); the JUL oracle tile lists (iter008b); the 838/838 terrain-range consumer census (the consumers located by function, not by claim)",
  "why_non_circular": "the record-decode comparison uses a byte-level parser with no shared code; the consumer-role claim comes from an exhaustive function census, not from the decoder's assumptions",
  "failure_case_detected": "any record decode divergence, any unconsumed tail byte, or a located consumer that contradicts the masks' vertex-color-bake role would FAIL",
  "dependencies": ["ROW 1", "ROW 5", "ROW 18"]
 },
 5: {
  "independent_source_of_truth": "the frozen M3-2-R1 provenance manifest (an INDEPENDENT resolution pipeline); the M3-4 witness-set intersection (disjoint); the four-era byte-identity measurements",
  "why_non_circular": "the resolution chain is compared against a manifest built by a different pipeline; the disjoint witness set proves the id spaces do not overlap (non-circular by set-theoretic evidence)",
  "failure_case_detected": "any SHA mismatch vs the frozen manifest, any silent cross-era fallback, or a missing LOUD NOT_FOUND would FAIL",
  "dependencies": ["ROW 4", "ROW 18"]
 },
 6: {
  "independent_source_of_truth": "the HLSL byte-extracted from the ORIGINAL materials.vfs (SHA-pinned artifact 5AE4AF81...); the producer FUN_00939c40 decompiled + disasm-pinned; the palette alpha values {45,62,85} byte-matched on the DATA side; the noise constants byte-derived from the EXE through the section-derived map; the 13 fail-closed negative controls (8/8 noise + 5/5 witness mutations FAIL, clean copies PASS)",
  "why_non_circular": "the constants are read from the binary bytes (not from the JS implementation); the thresholds are confirmed on both the code and the data side; the gate's fail-closedness is PROVEN by the mutation fixtures, not asserted",
  "failure_case_detected": "any bit mismatch in the 2048-entry re-check, any negative control that PASSES, or a saturation signature != 0.0% on the worked example would FAIL",
  "dependencies": ["ROW 4", "ROW 18"]
 },
 7: {
  "independent_source_of_truth": "the loader positives are string/RTTI facts of the pinned binary (fresh Ghidra project, sandbox SHA-pinned, ~250 functions); the VCL census re-derived from the ORIGINAL VegetationClimates.bnt (SHA 7B858401...)",
  "why_non_circular": "the RTTI chain is file-side deterministic; the census counts (32 .vcl / 492 rows / 256 ids) come from the original BNT, not from the decoder's own records",
  "failure_case_detected": "a census count divergence, a loader-string absence contradiction, or a BNT2 framing failure would FAIL",
  "dependencies": ["ROW 8", "ROW 9", "ROW 18"]
 },
 8: {
  "independent_source_of_truth": "the SINGLE ORIGINAL-DIRECT WITNESS reads ORIGINAL Models.bnt/Textures.bnt bytes (container SHAs C950A8C2.../61ACD13B... pinned); the STRICT witness gate compares payloadSize + per-block index + offsets + payload SHAs against the oracle extract (16/16); the repaired gate demonstrably FAILS on 5/5 witness mutations",
  "why_non_circular": "the witness gate's oracle side (iter037_oracle_extract.json) and observed side are independent reads; the missing-payloadSize fallback that previously compared oracle-vs-oracle is now a FAIL by construction (fail_closed_gates.json)",
  "failure_case_detected": "a dropped block, a wrong payloadSize, a corrupt block index, or a texture payload SHA mismatch would FAIL (all demonstrated by the mutation fixtures)",
  "dependencies": ["ROW 7", "ROW 10", "ROW 18"]
 },
 9: {
  "independent_source_of_truth": "the correlations + the disjointness measured from the ORIGINAL records (both id sets); the .tez geometry census both eras (1015/1020 records)",
  "why_non_circular": "the measurements read the original data, not the generator's interpretation; the disjointness is computed from both id spaces independently",
  "failure_case_detected": "an id-space overlap, or a .tez-climate alignment stronger than near-random, would contradict the disjointness/absence claims and be recorded as a failure",
  "dependencies": ["ROW 7", "ROW 10"]
 },
 10: {
  "independent_source_of_truth": "the ANTI-CIRCULAR reference (constants FROM the binary extraction, records FROM the ORIGINAL VegetationClimates.bnt, its own implementation) recomputing all 76 instances; the OLD shared-assumption reference demonstrably FAILING 76/76 (the negative); the exhaustive real-domain re-proof with the platform-validated oracle (229,376 + 229,376 checks)",
  "why_non_circular": "the reference shares NO constants with the page (they are re-derived from the binary bytes) and NO records (they come from the original BNT); the demonstrative negative proves the old validation was assumption-circular",
  "failure_case_detected": "any bit mismatch in any of the 76 instances' f32/u32/position fields, or any engine-vs-JS mismatch on the real-domain checks, would FAIL",
  "dependencies": ["ROW 9", "ROW 11", "ROW 18"]
 },
 11: {
  "independent_source_of_truth": "the INDEPENDENT python reference written from the Ghidra decompiles (not the JS); the MSVC LCG constants identified against an external public reference and matched by the binary's own bytes; the human's byte-proven vector (RNG 9719: /32767 = 0.2966093935972167...) as a BUILT-IN test; the platform-cross-validated oracle (443,141 platform + 20,000 f80-exactness = 463,141 TOTAL, 0 mismatches); THIS run's PC24 double measurement (the REAL anchor 14,104/229,376 and the SYNTHETIC anchor 103,073/1,245,184 both exact)",
  "why_non_circular": "the reference's constants are byte-derived from the binary (the CONSTANT_ADDRESS_LOCK), its records from the original BNT, and its implementation is its own; the PC24 sensitivity is measured by two independent implementations with exact agreement",
  "failure_case_detected": "any state0/samplerValue/scale mismatch across the 76 instances, any engine-vs-JS mismatch on the exhaustive domains, or a PC24 anchor divergence (real != 14,104 or synthetic != 103,073) would FAIL (the anchors are the run's fail-closed controls)",
  "dependencies": ["ROW 10", "ROW 7"]
 },
 12: {
  "independent_source_of_truth": "the exhaustive container/string census (denominators explicit: 53 containers, 2,217 files); the dual-era byte-extraction of the 0x3eb technique (SHA 857dea6e... BOTH eras)",
  "why_non_circular": "the census is a negative-proof over the physical corpus; the technique bytes are extracted independently in both eras and hash-compared",
  "failure_case_detected": "a located dedicated water container, or a JUL-vs-9.3.5 technique SHA divergence, would FAIL the claims",
  "dependencies": ["ROW 4", "ROW 13", "ROW 15"]
 },
 13: {
  "independent_source_of_truth": "the full-corpus dual-era walk (0 failures); the frozen iter008b census counts reproduced EXACTLY as the independent re-derivation; the consumer RE (FUN_00934890 -> FUN_00953340 in the LOD ring builder)",
  "why_non_circular": "the component census recomputes from the raw material records; the JUL counts equal an independently-frozen prior census",
  "failure_case_detected": "any walk failure or a count divergence vs the frozen census would FAIL",
  "dependencies": ["ROW 4", "ROW 12"]
 },
 14: {
  "independent_source_of_truth": "the engine constant read at its VA (_DAT_00a7b128 = bytes 00 00 20 41); the three-path unit-consistency triangle; the 51,920-tile crosstab that REFUTED the naive zero-marker",
  "why_non_circular": "the constant is a static binary fact; the refutation is measured on the full corpus, not on the page's own behavior",
  "failure_case_detected": "a crosstab that supported 'zero = water', or a constant byte divergence, would FAIL/REJECT the claims",
  "dependencies": ["ROW 3", "ROW 12"]
 },
 15: {
  "independent_source_of_truth": "the dual-era resolution + decode (iter023); the four-era byte-identity (PCG==JUL==EU==CD, 5/5); the 178-container census negative for waves/sky",
  "why_non_circular": "the byte-identity is measured across four independent corpora; the missing-plane-texture claim is a census negative, not a runtime observation",
  "failure_case_detected": "a located waves/sky texture, or a four-era payload divergence, would FAIL",
  "dependencies": ["ROW 12", "ROW 5"]
 },
 16: {
  "independent_source_of_truth": "the byte-faithful extraction from BOTH eras (SHA 857dea6e... each); the JUL-vs-9.3.5 record comparison (same offset/size/SHA - era-stable)",
  "why_non_circular": "the constants are read from the technique bytes, not from the page implementation",
  "failure_case_detected": "any constant divergence vs the extracted technique, or a JUL-vs-9.3.5 byte divergence, would FAIL",
  "dependencies": ["ROW 12", "ROW 15"]
 },
 17: {
  "independent_source_of_truth": "the disasm-pinned RE chain (FUN_009512a0 <- FUN_009516f0 stores); the .fx semantic + state macros from the original 1Ark.fx/25ArkLight.fx includes (the include-id rule verified over all referenced numbers)",
  "why_non_circular": "the wind chain is proven from the binary's own instructions; the .fx semantics come from the shipped include files",
  "failure_case_detected": "a store-site reading that contradicts the chain, or an include-id mismatch, would FAIL",
  "dependencies": ["ROW 12", "ROW 16"]
 },
 18: {
  "independent_source_of_truth": "the full-map SHA reproduction == the frozen iter002 acceptance; the 175/175 agreement with the independent M3-2-R1 pipeline; the era-validation walk (58,451 entries, 448,384 tail records); the SHA-enforced KNOWN_HASHES at mount",
  "why_non_circular": "the mount's products are compared against acceptance records produced by other pipelines; the KNOWN_HASHES enforcement makes any corpus substitution a LOUD failure",
  "failure_case_detected": "any mount of a corpus with a non-matching SHA, any walk failure, or a full-map SHA divergence would FAIL",
  "dependencies": ["ROW 1", "ROW 2", "ROW 4", "ROW 5", "ROW 7"]
 },
 19: {
  "independent_source_of_truth": "the 5/5 regression sweep vs the RECORDED deterministic hashes (produced by the prior sessions, re-verified on fresh headless-Chromium loads); the offline bit-exact re-checks of the 76/2048/16 recorded results with the repaired method (constants byte-derived from the EXE)",
  "why_non_circular": "the recorded hashes come from the prior sessions' probes (not from this run's code); the offline re-checks recompute with constants read from the binary bytes rather than the page's",
  "failure_case_detected": "any fresh-load hash divergence vs the recorded value, or any bit mismatch in the 76/2048/16 re-checks, would FAIL",
  "dependencies": ["all rows 1-18 (the integration consumer)"]
 }
}
