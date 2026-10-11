# QC report — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010

Reviewer origin: **SELF_REVIEW** (the executor's own fresh pass over the final
artifacts; NOT an independent Desktop audit — INDEPENDENT_DESKTOP_POST_AUDIT
stays PENDING).

## Checked
- Corpus accounting: 5,596 = index = catalog = extentOrder bijection (gate 1).
- Parse: 5,589 PASS / 7 FAIL with reasons kept (never relabeled).
- Ranking: monotonic extent DESC, UNKNOWN last, stable ties, coverage per
  metric (gate 4).
- Texture chain: controls verified + honest states (gate 5); checkerboard is
  visible PARTIAL, never TEXTURED_EXACT.
- Animation: original-key witnesses + browser loop/pause/scrub evidence
  (gates 6, 8); PSys/morphs honestly labeled.
- API: 17 negative probes truthful (gate 7); read-only loopback.
- Sweep: 5,589 OK + 7 SKIPPED_KNOWN_FAIL, LRU held at 6 (gate 9).
- Memory: A/B/A bounded (gate 10).
- Regressions: 218757.nif + 457485.nif parse PASS with validation OK (gate 11);
  protected files (PecNif10Reader.js, NifModelReader.js) byte-identical.
- Browser: LOAD/PIXEL/INTERACTION all pass with asset-discriminating pixel
  census (screenshots under PRIVATE_OUTPUT_ROOT, not committed).

## Known limitations (visible, not hidden)
See KNOWLEDGE_GAPS.md — 7 parse failures, property-controller application
partial, PSys/morph unresolved, JPEG/TGA-other unsupported.

## Protected-file identity
- src/pecompat/PecNif10Reader.js: sha256 in gate11 record (unchanged).
- src/pesource/NifModelReader.js: sha256 in gate11 record (unchanged).
- Old compat files: untouched (git status shows no compat/* modifications
  other than the NEW pcg935-* + server-pcg935-viewer.mjs).
