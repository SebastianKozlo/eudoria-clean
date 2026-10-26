# R7 — Model root value-source static reconstruction (ISO 5.1.0.0)

RUN_ID: PE2003_ISO_MODEL_ROOT_VALUE_SOURCE_STATIC_R7_20261025
Campaign: PE2003, wave R7 — model root value-source static reconstruction
Mode: STATIC_ONLY (no game execution, zero runtime; disassembly of pinned
bytes as data only)

---

## Section RUN (identity, provenance, environment)

- Client: ISO PC Gamer Nov 2003, Project Entropia client 5.1.0.0.
- Code source: flat blob `section1.bin`
  (SHA256 D43A23B9EFCFC9BC4092B38FA3C73499DE7DE7B03B20F34478B9E81EE8893631,
  2,939,409 B, image base 0x401000, flat-blob mapping), the UNPACKED FLAT
  IMAGE of the ISO PC Gamer Nov 2003 client PE.exe 5.1.0.0
  (962,560 B, SHA256 46B68741568D09664D8B0152E19FF765DFD562A8FF4BE32664E867971D55BB32;
  NRV2D/UPX unpack in R3/I02a; OEP RVA 0xADFC2).
  PE2_unpacked_out.exe
  (SHA256 56178993692A7409C896398089E482EDDF96177666BACB91A8CC1A638D9A0650,
  2,207,744 B) is a SEPARATE corpus: the PE42 3.4.3.1 unpacked client,
  pinned in R7 as a COMPARISON input only — NOT the identity source of
  section1.bin. Analysis era: ISO 5.1.0.0 (contract-compliant).
- Unpack provenance and input pins: preflight read-only verification
  1058/1058 PASS (author bijection 15 rows PASS); pinned R4 decoder inputs
  reused read-only (`.asm` bodies and the R4 record/source map).
- Model/effort client: nask-glm/glm-5-3 DEFAULT/MEDIUM for root and all
  native children; REQUEST_EFFORT=NOT_OBSERVED;
  SERVER_EFFECTIVE_EFFORT=UNKNOWN.
- Authority status: ADVISORY_PRE_QUALIFICATION. All statements are
  era-labelled to the 5.1.0.0 ISO static image.

## Section SCIENCE (results)

### 1. Corrected vtable map (boundaries, no table splicing)

- D (vtable 0x65CBEC, ctor-qualified, store after base ctor): slot +8 is
  0x4AF430, an intrusive doubly-linked-list walker over `this+0x2C0`
  (list header at `this+0x2BC`; 12-byte POD nodes {payload, next, prev},
  no vtable on nodes). Per node a virtual predicate (slot +4) runs; on a
  match the payload's virtual slot +8 PRODUCES the object here called Nd
  and returns it without retention in the walker body.
- W (vtable 0x65B3F0, slot +8 = 0x423280, typed NiPixelData ancestral
  walk) — R6 baseline boundary maintained. R7 confirms the W semantics do
  NOT transfer to D: D slot +8 returns an interned descriptor, not
  NiPixelData (R6-A02 upheld and strengthened positively).
- H holder (vtable 0x65E5D4, ctor 0x52B750) and its caller F
  (0x5257C0, derived vtable 0x65E5B4); wrapper W12B (vtable 0x65E648,
  ctor 0x533740); temporary global collector (vtable 0x65B024, 16 B,
  37 slots at +0xC); buffered binary file stream (vtable 0x65BAA8,
  ctor 0x43C490); list payload family (A: 0x65CE5C, B: 0x65CE4C, common
  base 0x65BA1C); Nd interned descriptor (vtable 0x65AB84, ctor 0x40E320,
  size 0x48B); R per-TYPE record template (vtable 0x65C3A0, size 0x5C);
  P ctor table 0x65C0DC (4 qualified entries) with 0x65C0EC a SEPARATE
  base-dtor table (R6 boundary maintained; new R7 observation: the
  destructor of the F-caller receiver installs vptr 0x65C0EC and releases
  the lazy slot — supports S==P, see below).
- A file-stream classification: 0x43C490 is a buffered binary file stream
  (open modes read/write/append binary); 0x2800 is the byte size of the
  I/O buffer allocation. The earlier "pixel" reading of the 2800 constant
  is downgraded to "I/O buffer; pixel content UNKNOWN".

### 2. Symbols (kept separate; no merges)

- E = return value of the entity lookup; R = return value of the
  record-template lookup = [SFO+0x78] (per-TYPE record template, chosen
  by a pure array INDEX K with bounds check, no string key);
  P = SFO (cached E+0xF8) holds R at +0x78, the instance ID from [E+0x40]
  at [SFO+4], and the lazy holder H at [P+0x10] (allocation 0x70,
  refcount +0x2C).
- H chain (each link CONFIRMED from bytes; whole chain
  STRONGLY_SUPPORTED): the F-caller method of class S builds A1 through a
  factory (new 12-byte wrapper) whose ctor 0x533740 returns `this`, so
  A1 == W (wrapper, vtable 0x65E648): +4 stores the first argument
  (no AddRef), +8 stores the second argument M WITH AddRef. M is the
  result of a virtual acquisition (slot 2) on a temporary global
  collector. The H ctor 0x52B750 stores W at [H+0xC] and M at [H+8];
  the F caller stores H at [S+0x10] and increments the refcount.
- Nd = interned key/handle/descriptor (single class; identity record of
  8 dwords plus an internal power-of-two dictionary array;
  integer-only, zero float/pixel math in the ctor — geometry/pixel
  classification REJECTED for this constructor). Producers follow a
  get-or-create intern pattern keyed by a mixed hash.
- NAME = [A+4] where A = [context+0x18] (field load, not a return value).
  The name dispatcher calls a large consumer object directly (not via the
  earlier-assumed vtable slot); NAME is a pointer to a large object, not
  a raw string. Node-name/handle semantics: PLAUSIBLE;
  filename-vs-ID: UNKNOWN.
- What connects the model to the instance: NOT established. The record
  template R is per-TYPE (selected by index K); the per-INSTANCE side is
  SFO holding R, the ID and H; the NAME consumer was not opened (budget
  exhausted, see INC-001), so no edge binds either model number to an
  instance, value or frame.

### 3. Model-binding results (both OPEN)

- 296445: availability in the ISO 5.1 corpus UNKNOWN; no asset-ID
  binding; no filename proof; no per-model instance, transform, values
  or frame. STATUS: OPEN.
- 218757: same status, OPEN. The shared mechanisms (interned descriptor,
  wrapper, M acquisition, NAME chain) do NOT close either case
  automatically; common mechanism is not per-model evidence.

## Section PROCESS

- 19 science native Tasks (D01,H01,Q1,H02,D02,H03,QC2,H04,D03,H05,D04,
  QC3,H06,H07,D05,D06,H08,N01,R01) + closing publication tasks
  (count finalized by root at publication). All parent-bound, depth 1,
  NO_NESTED_TASKS, max 2 active concurrently.
- Decode helper self-test 12/12 PASS before use; 29 admission events
  (ADMIT/DENY/CORRECTION); 22/22 EXTRACT_DONE receipts.
- QC waves: Q1 PASS (byte-overlap re-decode 108/108; two deliberately
  wrong hypotheses rejected); QC2 PASS with CORRECTIONS (stream-slot
  relabel adjudicated ACCEPTED); QC3 QC_PARTIAL with all material
  findings adjudicated (ABI correction of the factory accepted; template
  copy = 8 dwords accepted; whole-chain status held at
  STRONGLY_SUPPORTED, not promoted); QC4 final STOP_APPROVED.
- Incidents: INC-001 — candidate-reservation overrun (392 reserved vs
  370 available; root ledger under-counted per wave vs the authoritative
  event log; mechanical recount; science dispatch FREEZE; no retroactive
  cap increase). INC-002 — seal-repair (root-side; canonical record in
  the root incident ledger). H06-A — output_dir CORRECTION event
  (admission pointed at the QC3 dir; artifacts byte-identical, accepted
  as-is after comparison).

## Section INTEGRITY

- ERRATA / provenance (INC-003, corrected pre-pub): an earlier internal
  draft mislabeled section1.bin as "derived from PE2_unpacked_out.exe
  (561789...0650)". Corrected per the binding errata
  (CORRECTIONS_PRE_PUB.md / INPUT_RECHECK_v2.json): section1.bin is the
  unpacked flat image of the ISO 5.1.0.0 client PE.exe (46B687...BB32);
  PE2_unpacked_out.exe is a separate PE42 3.4.3.1 comparison corpus. The
  analysis era (ISO 5.1.0.0) was always correct; only the origin label was
  wrong. This public projection carries the corrected label only.

- Budgets (reservations vs actual): decoded rows 3326 summed over
  receipts, 3145 unique (the difference is byte-identical duplicated
  output of job H06 in two directories); candidate reservations 392 vs
  370 available = overrun 22 (INC-001, freeze applied); at stop the
  remaining ready edges each fit the row/body/call budget but require at
  least 1 candidate reservation at -22 — no further package fits.
  Closing reserve frozen before the first extraction, never increased.
- Stop class: budget enters the closing reserve (candidates) with INC-001;
  goal partially achieved; recount reproducible.
- Sealed SCIENCE_ROOT: manifest verify PASS (frozen seal; this public
  projection is derived from the sealed package read-only).
- Honest negatives: per-model binding, values, frames — NOT achieved;
  no evidence promoted above its proof level (S==P and M semantics stay
  PLAUSIBLE; filename-vs-ID and per-model binding stay UNKNOWN).

## Section PUBLICATION

- This file is a SANITIZED PUBLIC PROJECTION: conclusions, statuses,
  symbolic identities and provenance hashes only. Zero game payloads,
  zero raw byte/hex listings, zero full node float data, zero payload
  prompts/responses, zero DB/config content, zero Ghidra project data,
  zero original game values.
- An additive notice (R6_EXTERNAL_POSTAUDIT_NOTICE_R1.md) is placed next
  to the historical public R6 report; R6 files are byte-untouched.
- Publication is NOT scientific acceptance; authority is advisory.

## Final statuses

- PE2003_WORLD_XYZ_RECOVERED=NO
- PE2003_HISTORICAL_PLACEMENT=NOT_ESTABLISHED
- SOURCE_SPECIFIC_ISO_MODELS=UNKNOWN
- PE2003_LOCAL_SOURCE_EXHAUSTED=NO
- CANONICAL_GATE_EFFECT=NONE
- EXTERNAL_POSTAUDIT=PENDING
