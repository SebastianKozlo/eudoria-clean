# PROPOSED_DOC_CORRECTIONS — PE-NIF-CLAIM-EVIDENCE-LOCK-R1
# STATUS: PROPOSALS ONLY. Nothing below has been applied. The existing repo,
# wiki, runs and canon are UNCHANGED by this round. An authorized applier
# (post-audit) must review, then apply. Each item cites the claim-matrix row
# (05_ANALYSIS/CLAIM_MATRIX.csv) and the raw evidence.

## P1 — docs/nif/09-semantics.md (wiki target @ 077b8a4, SHA bb22d518...)

### P1-1 (C-R32-03, CE-1): L55
- OLD: "The slot VOCABULARY itself is now closed — 40 slots with a perfect f1
  enum (ITER-32, next section)"
- NEW: "The slot VOCABULARY itself is now closed — 40 slots mapping onto 9
  distinct f1 type-codes; the mapping is zero-exception for the 8 named slots
  and holds for ANIM in 985/1,157 entries (ITER-32, next section)"

### P1-2 (C-R32-03): L70-73
- OLD: "...AND in entry f1 (a perfect 1:1 enum): BASE=0, DARK=1, DETAIL=2,
  GLOSS=3, GLOW=4, BUMP=5, DECAL0=6, ENVIRONMENT=9, ANIM=11."
- NEW: "...AND in entry f1 (a zero-exception type-code enum for the 8 named
  slots: BASE=0, DARK=1, DETAIL=2, GLOSS=3, GLOW=4, BUMP=5, DECAL0=6,
  ENVIRONMENT=9; ANIM slots carry 11 in 985/1,157 entries — the 172
  exceptions are 142 x f1=0 and 30 x f1=4, late v4 frames)."

### P1-3 (C-R32-01): L84-86 (ANIM bullet — add the exception sentence)
- APPEND after "…(1,157/1,157 auxiliary-verified)": "; f1=11 in 985/1,157 of
  these entries (142 x f1=0, 30 x f1=4 — the same late-v4-frame population)."

### P1-4 (C-R38-03D): L146+ (mode section heading area)
- PREPEND to the mode bullet: "Evidence-graded (ITER-38): census CONFIRMED
  (1,274 records); mode-orthogonal-to-params CONFIRMED (41076.nif twin
  pair); state-binding STRONGLY_SUPPORTED; `single` ≈ one-shot PLAUSIBLE;
  runtime semantics open." — replacing the ungraded "Readings:" framing.

### P1-5 (C-R34-06, CE-11): L180-181 + L190-192
- OLD: "[9 × f32 position deltas]"
- NEW: "[9 × f32 delta triples — grouping structural; target quantity
  UNVERIFIED (position vs other; the 3-states-×-XYZ reading is an open
  hypothesis)]"
- OLD: "with k per-record ∈ {2,3,4} — byte-exact on 86.2% of real-record
  spans (ITER-34)"
- NEW: "with k per-record variable (parser takes the smallest k in 1..8 whose
  weight prefix sums ≈1; observed k ∈ {1,2,3,4} on 9.3.5 exact examples —
  k=1 concentrated in 574845.nif bi=69, possibly smallest-k misparses of k=2 —
  and k ∈ {1..5} on 2003) — byte-exact on 2,093/2,427 classifier-real spans
  (86.2%; the 'real-record' class is a hypothesis-aligned classifier) and
  3,186/6,167 all fit spans (ITER-34)"

### P1-6 (C-R36-04, CE-5): L208
- OLD: "**d==c ⟺ the file has not changed since registration** (61.42% in
  9.3.5 / 60.80% in 2003)"
- NEW: "**d==c is consistent with the file being unchanged since its last
  registration** (61.42% in 9.3.5 / 60.80% in 2003; the biconditional is not
  established — CRC collisions, byte-restoration and unobserved registering
  events are not excluded)"

### P1-7 (C-R29-02, CE-9): L219-220
- OLD: "**The importer exporter-string = the ORIGINAL toolchain version
  (ITER-29)**"
- NEW: "**The importer exporter-string is corpus-confirmed as one of 4
  toolchain names; the reading that it records the ORIGINAL exporter and
  survives NIF version up-conversion is STRONGLY_SUPPORTED (ITER-29)** — an
  era/provenance hint, not an observed re-export event"

## P2 — docs/nif/10-containers-corpus.md (SHA 0b197ed4...)

### P2-1 (C-R36-04, CE-5): L23
- OLD: "registration; d==c ⟺ unchanged since registration.**"
- NEW: "registration; d==c is consistent with unchanged-since-registration
  (biconditional not established — see ch09 note).**"

### P2-2 (C-R35-03, CE-6): L121-125
- OLD: "**Conclusion (CONFIRMED): the NIF extension formats are era-stable at
  the byte level — across a half-decade corpus gap every byte-exact grammar
  reproduces at 100% and the rare-family and importer pattern censuses are
  count-identical. The era drift is CONTENT (which directive/effect names and
  which records appear), never GRAMMAR.**"
- NEW: "**Conclusion (CONFIRMED at the tested scope): in the 21 tested grammar
  claims on the 2003 and 9.3.5 Models.bnt corpora (5,426/5,426 + 5,596/5,596
  parse closure; note 5,208/5,422 shared files are byte-identical across
  eras), every byte-exact grammar reproduced at 100% and the rare-family and
  importer pattern censuses were count-identical. All drift observed in the
  tested claims was CONTENT (which directive/effect names and which records
  appear); no grammar-level drift was found. No claim is made about untested
  claims, other archives, or other versions.**"
- NOTE (informational, optional append): changed-payload witnesses exist at
  file level — all 214 changed + 4 old-only 2003 files were parsed; family
  blocks present: animation/texture/importer in 214/214 changed files,
  shader in 9, morph in 29 (this run's scan).

## P3 — docs/nif/11-open-problems.md (SHA 5fd138f2...)

### P3-1 (C-R36-04): L24
- OLD: "d==c ⇔ unchanged since registration (c_eq_d 3,435/5,596 = 61.42%; …)"
- NEW: "d==c consistent with unchanged-since-registration (biconditional not
  established; c_eq_d 3,435/5,596 = 61.42%; …)"

### P3-2 (C-DOC-01): L80-81
- OLD: "SEMANTIC closure = PARTIAL — the table above is the complete honest
  list of what remains unknown; nothing outside that list is open."
- NEW: "SEMANTIC closure = PARTIAL — the table above is the honest list of
  what remains unknown AT THE CURRENT EVIDENCE LEVEL; claims outside this
  documentation's tested scope are neither closed nor asserted."

## P4 — docs/nif/README.md (SHA 4f976581...)

### P4-1 (C-R32-03): L82
- OLD: "NiArkTextureExtraData | CONFIRMED — 40-slot vocabulary, f1 = slot
  enum, packed field2 formula 4,838/4,838 (ITER-32)"
- NEW: "NiArkTextureExtraData | CONFIRMED — 40-slot vocabulary, f1 = slot
  type-enum (zero-exception for the 8 named slots; ANIM 985/1,157 with
  172 late-v4 exceptions), packed field2 formula 4,838/4,838 (ITER-32)"

### P4-2 (C-R38-03D): L80
- OLD: "SEMANTICS decoded (TEXT behavior records ITER-5/16; Controllers
  attachment ITER-24; viewport suite ITER-25; modes ITER-38; event registry
  ITER-7/30)"
- NEW: "SEMANTICS: census CONFIRMED; state-binding STRONGLY_SUPPORTED (TEXT
  behavior records ITER-5/16; Controllers attachment ITER-24; viewport suite
  ITER-25; modes ITER-38; event registry ITER-7/30); runtime behavior open"

### P4-3 (C-DOC-01): L3-5
- OLD: "This is the complete, evidence-based documentation of the NIF binary
  format as used by Project Entropia"
- NEW: "This is the byte-complete, evidence-graded documentation of the NIF
  binary format as used by Project Entropia (parse closure 100% on both
  Models.bnt eras; per-family semantic status in the state table below)"

## P5 — run REPORT texts (historical files are NOT edited; corrections listed for a future consolidated addendum only)

### P5-1 (C-R32-05, CE-2): R32 REPORT.md L110
- "10 of 45 carry 11" -> "9 of 45 carry 11" (raw: 3+3+1+1+1 = 9; f1=0 x22,
  f1=4 x14). DO NOT edit the historical report; record in the next wiki
  pass / correction ledger.

### P5-2 (C-R40-02, CE-7): R40 REPORT.md L106-107
- "README 4,573 → 9,182 bytes; 09-semantics 3,705 → 13,214 bytes" are
  unit-mixed sums (pre BYTES + CHAR delta); true applied byte sizes:
  9,213 / 13,326 (byte deltas 4,640 / 9,621; char deltas 4,609 / 9,509 as
  G7 verified). DO NOT edit the historical report; record in the correction
  ledger.

### P5-3 (C-R40-03, CE-8): PE_AUTO_LOOP.json L298 (WRITER-scope file — proposal only; this round does NOT write it)
- "+236 lines" = combined added lines (README +70, 09-semantics +166; net
  +225). Clarify on the next writer heartbeat as: "+236 added lines combined".

## P6 — 12 artifact_index.csv manifests
- NOT edited (historical evidence stays immutable). Normalized sidecars with
  original path + original SHA + hash verification + scope classes
  (PRE_EDIT_INPUT / POST_EDIT_OUTPUT / IMMUTABLE_SNAPSHOT / MUTABLE_POINTER /
  UNRESOLVED_ALIAS) are provided in
  05_ANALYSIS/NORMALIZED_MANIFESTS/ (12 files, all strict-CSV valid).
- The 11 malformed rows are re-derived and listed in
  01_RAW/CONTROL_R1_RESULTS.json (manifests[].strict_errors) and preserved
  row-exact in the sidecars (raw_text column).
- R40 manifest rows 14-16 (README.md / 09-semantics.md / PE_AUTO_LOOP.json):
  keep, but future manifests should label wiki targets as
  "pre-apply snapshot (READ-ONLY)" and loop files as "mutable live state".

## P7 — R32 REPORT summary wording (for the correction ledger; applies to
## any future re-statement of ITER-32)
- "The material pipeline vocabulary is now complete and closed" is CONFIRMED
  ONLY as a vocabulary-census claim; any "pipeline fully decoded" summary
  reading is REJECTED (runtime semantics of non-BASE slots + several fields
  remain open — M3-5B; R32 S7 UNVERIFIED list).
