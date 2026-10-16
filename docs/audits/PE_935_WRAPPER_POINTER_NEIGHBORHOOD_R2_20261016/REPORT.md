# PE_935_WRAPPER_POINTER_NEIGHBORHOOD_R2_20261016 — FINAL REPORT

RUN_ID = PE_935_WRAPPER_POINTER_NEIGHBORHOOD_R2_20261016
MODE = ONE_BOUNDED_READ_ONLY_RUN | ERA = PCG_9_3_5
BASE_SHA (repo HEAD at start) = 6ba8f7d83894a649fdf2fab1b9ba2d7cb5d3c314
GENERATED = 2026-10-16T16:06:44.203878+00:00

## 1. RUN_STATUS

COMPLETE_WITHIN_BOUND (single run; 1 correction round of 2 — the §3-mandated S7 conflict investigation layer;
v1 outputs preserved; hard stop after this run).
SOURCE_UNCHANGED = YES (2 full streaming SHA256 passes, both == pin E7785430...F31).
NO repo modification, NO commit/push, NO nested agents. Falsifiers 14/14 PASS.

## 2. Input identity and budget

- ORIGINAL_EXE = D:\Eudoria_Reconstruction\pcg_install\Entropia.exe; SIZE = 8015872 B; SHA256 = E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (pass 1 == pass 2 == pin).
- EXE byte budget: 2x full hash (16,031,744) + 1x PE header (4,096) + 2x window (256) + 1x RAW .text
  (6,766,592) = 22,802,688 B == MAX_TOTAL_ORIGINAL_BYTES (exactly at budget; no third window read on any
  condition; no helper/verifier EXE hashing; .text SHA256 computed IN-PASS during the single .text read).

## 3. SCIENCE A — the 128-B neighborhood of 0x00A91CFC (question 1)

- Window VA [0x00A91CC0,0x00A91D40) -> RVA [0x00691CC0,0x00691D40) -> file [6888640,6888768) = [0x00691CC0,0x00691D40) — verified mechanically
  from the freshly parsed PE header (MZ, machine 014C, magic 010B, imagebase 0x400000; .text RVA 4096
  VSize 6764005 RawPtr 4096 RawSize 6766592 char 0x60000020; .rdata RVA 6770688 VSize 1009001 RawPtr
  6770688 RawSize 1011712 char 0x40000040; bounds/overlap/file-bounds checks clean).
- Dual independent reads: WINDOW_READ1.bin / WINDOW_READ2.bin — 128/128 bytes equal (SHA256 3F6F536316E8DABF4FE1C807B0352291AC1B5700957F00548B2678431EA1CFB0 both).
- MANDATORY CONTROL: DWORD index 15 @ 0x00A91CFC = 0x00852A30 — PASS (matches the contract pin and the R1
  wrapper identity).

### 3.1 Full 32-DWORD roster

| idx | VA | raw4 LE | value | value-section | classification | prior |
|---|---|---|---|---|---|---|
| 0 | 0x00A91CC0 | 50d78400 | 0x0084D750 | .text | POINTER_TO_text | PRIOR |
| 1 | 0x00A91CC4 | c0c28400 | 0x0084C2C0 | .text | POINTER_TO_text | PRIOR |
| 2 | 0x00A91CC8 | 01000000 | 0x00000001 | - | SUB_IMAGE_VALUE | PRIOR |
| 3 | 0x00A91CCC | 0830ab00 | 0x00AB3008 | .rdata | POINTER_TO_rdata | PRIOR |
| 4 | 0x00A91CD0 | b0068500 | 0x008506B0 | .text | POINTER_TO_text | PRIOR |
| 5 | 0x00A91CD4 | fad49500 | 0x0095D4FA | .text | POINTER_TO_text | PRIOR |
| 6 | 0x00A91CD8 | fad49500 | 0x0095D4FA | .text | POINTER_TO_text | PRIOR |
| 7 | 0x00A91CDC | 5030ab00 | 0x00AB3050 | .rdata | POINTER_TO_rdata | PRIOR |
| 8 | 0x00A91CE0 | b0068500 | 0x008506B0 | .text | POINTER_TO_text | PRIOR |
| 9 | 0x00A91CE4 | d0068500 | 0x008506D0 | .text | POINTER_TO_text | PRIOR |
| 10 | 0x00A91CE8 | d0068500 | 0x008506D0 | .text | POINTER_TO_text | PRIOR |
| 11 | 0x00A91CEC | 01000000 | 0x00000001 | - | SUB_IMAGE_VALUE | PRIOR |
| 12 | 0x00A91CF0 | 00008041 | 0x41800000 | - | OUTSIDE_IMAGE | PRIOR |
| 13 | 0x00A91CF4 | 9c30ab00 | 0x00AB309C | .rdata | POINTER_TO_rdata | PRIOR |
| 14 | 0x00A91CF8 | 500c8500 | 0x00850C50 | .text | POINTER_TO_text | PRIOR |
| 15 | 0x00A91CFC | 302a8500 | 0x00852A30 | .text | POINTER_TO_text | PRIOR |
| 16 | 0x00A91D00 | e430ab00 | 0x00AB30E4 | .rdata | POINTER_TO_rdata | PRIOR |
| 17 | 0x00A91D04 | 802b8500 | 0x00852B80 | .text | POINTER_TO_text | PRIOR |
| 18 | 0x00A91D08 | 10018e00 | 0x008E0110 | .text | POINTER_TO_text | PRIOR |
| 19 | 0x00A91D0C | 70678200 | 0x00826770 | .text | POINTER_TO_text | PRIOR |
| 20 | 0x00A91D10 | 01000000 | 0x00000001 | - | SUB_IMAGE_VALUE | PRIOR |
| 21 | 0x00A91D14 | 3031ab00 | 0x00AB3130 | .rdata | POINTER_TO_rdata | PRIOR |
| 22 | 0x00A91D18 | 902c8500 | 0x00852C90 | .text | POINTER_TO_text | PRIOR |
| 23 | 0x00A91D1C | 602d8500 | 0x00852D60 | .text | POINTER_TO_text | PRIOR |
| 24 | 0x00A91D20 | 01000000 | 0x00000001 | - | SUB_IMAGE_VALUE | PRIOR |
| 25 | 0x00A91D24 | 0ad7233d | 0x3D23D70A | - | OUTSIDE_IMAGE | PRIOR |
| 26 | 0x00A91D28 | 00401c47 | 0x471C4000 | - | OUTSIDE_IMAGE | PRIOR |
| 27 | 0x00A91D2C | 00000000 | 0x00000000 | - | ZERO | NEW |
| 28 | 0x00A91D30 | 182d4454 | 0x54442D18 | - | OUTSIDE_IMAGE | NEW |
| 29 | 0x00A91D34 | fb210940 | 0x400921FB | - | OUTSIDE_IMAGE | NEW |
| 30 | 0x00A91D38 | 182d4454 | 0x54442D18 | - | OUTSIDE_IMAGE | NEW |
| 31 | 0x00A91D3C | fb21f93f | 0x3FF921FB | - | OUTSIDE_IMAGE | NEW |

Structure narrative (series, zeros, gaps, candidate boundaries):
- slots 0-1: .text pointers — tail of the ArkPortalCellGraph vtable that STARTS at 0x00A91CB4 (BEFORE the
  window; out of scan domain).
- slot 2: 1 (small integer). slot 3: .rdata COL-class pointer 0x00AB3008 -> candidate vtable head at slot 4
  (MSVC RTTI vtable-4 layout HYPOTHESIS supported by prior GA3/S4 structure; NOT proven here).
- slots 4-6: candidate vtable of an unnamed class: .text pointer + 2x 0x0095D4FA (prior GA3 labels _purecall).
- slot 7: COL 0x00AB3050 (ArkPortalIdGenerator); slots 8-12: IdGenerator vtable region (.text, .text, 1, float).
- slot 13: COL 0x00AB309C (ArkPortalCell); slots 14-15: Cell vtable head [0x00850C50, 0x00852A30] — slot 15 is
  the R1-decoded parameter-cursor wrapper (body [0x00852A30,0x00852A82), relay CONDITIONAL_ON_ABI_MODEL;
  CALLER_DISCOVERY R1: no direct .text E8/E9 callers — reached virtually).
- slot 16: COL 0x00AB30E4 (ArkPortalResourceItem); slots 17-20: Item vtable region (.text x3, 1).
- slot 21: COL 0x00AB3130 (ArkPortalPortal); slots 22-26: Portal vtable region (.text x2, 1, float x2).
- slots 27-31 (no prior documentation): 27=0x00000000 (ZERO); 28=0x54442D18 (OUTSIDE_IMAGE); 29=0x400921FB (OUTSIDE_IMAGE); 30=0x54442D18 (OUTSIDE_IMAGE); 31=0x3FF921FB (OUTSIDE_IMAGE)

POINTER_ARRAY_SHAPE = PLAUSIBLE_POINTER_ARRAY_SHAPE (at most; NEVER VTABLE_CONFIRMED automatically).
No target pointed to by any read DWORD was opened (no pointer-following).

## 4. SCIENCE B — raw .text references to the 32 slot addresses (question 2)

Single full read of RAW .text (6,766,592 B; in-pass SHA256 DA6F04A0FFEC0EBB312AD69AEAC79457914AE97B2DB5185C31B4CBB5589D1F09); chunked scan CHUNK=1,048,576, CARRY=3
(logical carry; NOT an additional read); eligible starts 6766589 evaluated; NO alignment requirement;
MAX_HITS=4096.

- TOTAL_RAW_HITS = 13; census_complete = True; chunked-vs-unchunked cross-check identical = True
- spans: FULL_VIRTUAL_SPAN 13; CROSSES_VIRTUAL_SIZE_END 0; RAW_PADDING_ONLY 0
- QUALIFICATION = RAW_ADDRESS_OCCURRENCE_UNQUALIFIED for every hit (no disassembly, no body expansion, no
  Ghidra, no argument-flow).

| ord | slot | slot VA | hit VA | span | axis A |
|---|---|---|---|---|---|
| 1 | 4 | 0x00A91CD0 | 0x008506BA | FULL_VIRTUAL_SPAN | NEW_RAW_CANDIDATE |
| 2 | 8 | 0x00A91CE0 | 0x008506FC | FULL_VIRTUAL_SPAN | NEW_RAW_CANDIDATE |
| 3 | 14 | 0x00A91CF8 | 0x00851EB7 | FULL_VIRTUAL_SPAN | NEW_RAW_CANDIDATE |
| 4 | 12 | 0x00A91CF0 | 0x00851F36 | FULL_VIRTUAL_SPAN | NEW_RAW_CANDIDATE |
| 5 | 14 | 0x00A91CF8 | 0x0085213D | FULL_VIRTUAL_SPAN | NEW_RAW_CANDIDATE |
| 6 | 17 | 0x00A91D04 | 0x00852ACB | FULL_VIRTUAL_SPAN | NEW_RAW_CANDIDATE |
| 7 | 17 | 0x00A91D04 | 0x00852B3A | FULL_VIRTUAL_SPAN | NEW_RAW_CANDIDATE |
| 8 | 22 | 0x00A91D18 | 0x00852BE2 | FULL_VIRTUAL_SPAN | NEW_RAW_CANDIDATE |
| 9 | 22 | 0x00A91D18 | 0x00852DD1 | FULL_VIRTUAL_SPAN | NEW_RAW_CANDIDATE |
| 10 | 22 | 0x00A91D18 | 0x00852E8C | FULL_VIRTUAL_SPAN | NEW_RAW_CANDIDATE |
| 11 | 25 | 0x00A91D24 | 0x00853522 | FULL_VIRTUAL_SPAN | NEW_RAW_CANDIDATE |
| 12 | 26 | 0x00A91D28 | 0x00853C1D | FULL_VIRTUAL_SPAN | NEW_RAW_CANDIDATE |
| 13 | 25 | 0x00A91D24 | 0x00891561 | FULL_VIRTUAL_SPAN | NEW_RAW_CANDIDATE |

### 4.1 S7 preregistered controls (contract §3) — formal result + §3-mandated investigation

- S7-C1 (ArkPortalCell, slot 14): preregistered expected start 0x00851EBF -> census: NOT FOUND at expected position (formal PRIOR_EVIDENCE_CONFLICT); investigation: pattern byte-confirmed at the S7 va anchor 0x00851EB7 with post-bytes matching -> S7 evidence CONFIRMED, expectation arithmetic was the error
- S7-C2 (ArkPortalCell, slot 14): preregistered expected start 0x00852145 -> census: NOT FOUND at expected position (formal PRIOR_EVIDENCE_CONFLICT); investigation: pattern byte-confirmed at the S7 va anchor 0x0085213D with post-bytes matching -> S7 evidence CONFIRMED, expectation arithmetic was the error
- S7-C3 (ArkPortalResourceItem, slot 17): preregistered expected start 0x00852AD3 -> census: NOT FOUND at expected position (formal PRIOR_EVIDENCE_CONFLICT); investigation: pattern byte-confirmed at the S7 va anchor 0x00852ACB with post-bytes matching -> S7 evidence CONFIRMED, expectation arithmetic was the error
- S7-C4 (ArkPortalResourceItem, slot 17): preregistered expected start 0x00852B42 -> census: NOT FOUND at expected position (formal PRIOR_EVIDENCE_CONFLICT); investigation: pattern byte-confirmed at the S7 va anchor 0x00852B3A with post-bytes matching -> S7 evidence CONFIRMED, expectation arithmetic was the error

The four preregistered expected DWORD-start positions (window_va+8 = 0x00851EBF / 0x00852145 / 0x00852AD3 /
0x00852B42) were NOT found by the census -> formal PRIOR_EVIDENCE_CONFLICT x4 on the frozen record.
§3-mandated investigation (CONFLICT_INVESTIGATION.json; already-read data only):

- The re-extractions anchored at the S7 file_offset fields show the vtable patterns EXACTLY at those anchors
  (e.g. F8 1C A9 00 at file 4529847 = VA 0x00851EB7), and the 8 post-pattern bytes match the S7 window_hex
  bytes 12..19 byte-for-byte in all four controls.
- Therefore the S7 window format is CENTERED on the pattern: S7's 'va'/'file_offset' fields ARE the raw imm32
  positions and window_hex = 8 B pre-context + pattern + 8 B post-context. The §3 formula "window start = va"
  (inherited by the frozen preregistration) is disproven by the fresh bytes.
- The census found all four S7 patterns EXACTLY at the S7 va positions (0x00851EB7 / 0x0085213D / 0x00852ACB /
  0x00852B3A) — the S7 raw evidence itself is byte-confirmed; the conflict is against the preregistered
  EXPECTATION ARITHMETIC, not against the S7 evidence.
- NO expectation massaging: the frozen counters (0 PRIOR_RAW_MATCHES on the preregistered va+8 basis)
  stand unchanged; the S7-va correspondence is a separate byte-proven fact recorded in
  CONFLICT_INVESTIGATION.json as the POST-HOC refined basis.
- GA3 xref consistency (informational byte arithmetic): every GA3 from_va paired with a census hit satisfies
  hit_va = ga3_from_va + 2 (8/8 pairs) — consistent with a 2-byte store-opcode prefix; NOT a proof of any
  instruction (no disassembly in this run).
- The S7 sites are NOT qualified as instruction heads/vptr stores.

## 5. Knowledge increment (question 3) — dual basis (frozen + investigation-refined)

FROZEN basis (preregistered prior-position set = the four window_va+8 positions; NOVELTY_ANALYSIS.json):
- TOTAL_RAW_HITS = 13; PRIOR_RAW_MATCHES = 0; NEW_RAW_CANDIDATES = 13; PRIOR_CONFLICTS = 4.

INVESTIGATION-REFINED basis (POST-HOC, byte-proven; CONFLICT_INVESTIGATION.json):
- PRIOR_RAW_MATCHES = 4 (hits exactly at the S7 va/file_offset fields); NEW_RAW_CANDIDATES = 9
  (of which 4 carry GA3 xref context at from_va+2 and 5 have NO prior documentation at any level);
  the 4 formal prereg-position conflicts stand on the record.
- NOVELTY_COMPARISON_COVERAGE: hits 13/13; roster prior-documented 27/32 (slots 0-26); undocumented [27, 28, 29, 30, 31].
- NEW_STRUCTURAL_KNOWLEDGE = NEW_STRUCTURAL_FACTS_CONFIRMED_RAW; new raw positions 13; references without ANY prior documentation
  5 (slots 12,25,26,4); newly documented window slots 27=0x00000000 (ZERO); 28=0x54442D18 (OUTSIDE_IMAGE); 29=0x400921FB (OUTSIDE_IMAGE); 30=0x54442D18 (OUTSIDE_IMAGE); 31=0x3FF921FB (OUTSIDE_IMAGE).
- NEW_SEMANTIC_KNOWLEDGE = NOT_ESTABLISHED (all hits unqualified; positive hit count != positive knowledge
  increment about client behavior).

## 6. FINAL ASSESSMENT (§10; three layers separate)

- BYTE_FACT_STATUS = CONFIRMED
- POINTER_ARRAY_SHAPE_STATUS = PLAUSIBLE_POINTER_ARRAY_SHAPE
- KNOWN_VTABLE_COMPATIBILITY = COMPATIBLE_WITH_PRIOR_RTTI_VTABLE_HEADS_AND_R1_WRAPPER (after §3 investigation: roster 27/27 prior-confirmed; S7 byte-confirmed at its own va anchors; the 4 formal prereg-position conflicts stand on the record as a §3 window-format misreading, not as an S7 contradiction)
- RAW_REFERENCE_CENSUS_STATUS = COMPLETE
- NOVELTY_STATUS = NEW_STRUCTURAL_FACTS_CONFIRMED_RAW (dual basis: frozen 0/13/4; refined 4 prior / 9 new / 4 formal conflicts)
- CURSOR_PRODUCER_STATUS = NOT_ESTABLISHED (unchanged; slot-15 raw references: none found; any would be unqualified)
- WORLD_INSTANCE_STATUS = NOT_ESTABLISHED
- ADVISORY_ASSESSMENT_ONLY = GO_PORTAL_ROSETTA (assessment only, NOT executed): 5 raw occurrence(s) of window slot address(es) have NO prior documentation at any level — slot 4 (0x00A91CD0) @ 0x008506BA; slot 12 (0x00A91CF0) @ 0x00851F36; slot 25 (0x00A91D24) @ 0x00853522; slot 26 (0x00A91D28) @ 0x00853C1D; slot 25 (0x00A91D24) @ 0x00891561. Each is a concrete falsifiable edge: a separate bounded decode run could qualify the exact instruction at that position (candidate edges include the unnamed-class vtable-store region near 0x008506BA and the raw occurrences at 0x00851F36 / 0x00853522 / 0x00891561 / 0x00853C1D).

Layer A. CLIENT_KNOWLEDGE_COVERAGE: byte-confirmed .rdata window = portal-family vtable/RTTI region
(CellGraph tail, unnamed-class candidate, IdGenerator, Cell with the parameter-cursor wrapper at slot 15,
ResourceItem, Portal) + 5 newly documented slots + a COMPLETE raw census of .text occurrences of all 32
slot addresses (unqualified).
Layer B. RECONSTRUCTION_IMPLEMENTATION_COVERAGE: NOT_APPLICABLE (pure static RE; nothing implemented).
Layer C. HISTORICAL_GAME_RECOVERY_COVERAGE: NO (no historical instance/transform evidence in scope).

Verbatim standing (unchanged): CURSOR_SOURCE_MEDIUM=UNKNOWN; CURSOR_CONSTRUCTION_OR_FILL_UPSTREAM=
NOT_ESTABLISHED; STATIC_BUILDING_ROLE=NOT_ESTABLISHED; WORLD_INSTANCE_IDENTITY=NOT_ESTABLISHED;
WORLD_XYZ_RECOVERED=NO.

## 7. Findings and severity

- FINDING-1 (INFO): window slots 0-26 CONFIRM prior GA3/S14/R1 documentation byte-for-byte (0 content conflicts).
- FINDING-2 (INFO): slots 27-31 newly documented (raw values; unqualified).
- FINDING-3 (MAJOR, process/expectation): the §3 preregistered S7 expected positions (window_va+8) were NOT
  found; §3-mandated investigation proved the S7 window format is CENTERED on the pattern (S7 va = raw imm32
  position) — a window-format misreading shared by the contract §3 and the frozen preregistration; the census
  found all 4 S7 patterns exactly at the S7 va positions and the S7 post-pattern bytes match byte-for-byte.
  Formal result: 4 PRIOR_EVIDENCE_CONFLICTs stand on the frozen record; NO massaging; dual-basis novelty
  reported (frozen 0/13/4; refined 4/9 with 4 formal conflicts standing).
- FINDING-4 (INFO): raw census: 13 occurrences of slot addresses in .text; on the refined basis 4
  match the S7-documented positions, 4 more carry GA3 xref context (from_va+2), and 5 have NO prior
  documentation at any level (slots 12,25,26,4) — candidate new edges, all unqualified.
- FINDING-5 (INFO): 1 correction round used (§3 investigation layer; v1 analysis outputs preserved
  byte-untouched; no additional EXE reads; no counter resets). Budgets exactly at limit; falsifiers
  14/14.

## 8. Process

SELF_QC (QC.json) != INDEPENDENT_QC. Manifest written LAST; after it only read-only re-hash + bijection.
