# MODEL_218757_CONTINUITY — PE_935_CMO_ARG1_BR_C1_LEAF_QC_PROVENANCE_CORRECTION_R1_20261009

**RECORDS ONLY.** This file is a compact continuity map built from the
pinned prior Desktop report and preserved bridge records ONLY. In THIS run
no new asset, function, model, instance, archive or code region was opened
to populate it (scope fence; the two-leaf machinery correction and the two
window replays are unrelated to these facts). Every fact below carries its
origin; **writing a fact into Git does not independently confirm or promote
it.**

```text
MODEL_CONTINUITY_ORIGIN = PRIOR_EVIDENCE_RECORDS_ONLY
```

## 1. Compact map (as fixed by the contract)

```text
PCG definition 4057 -> model 218757 -> visual/world-instance join UNKNOWN

unknown producer -> value at T+0x10 at read time
                 -> [arg1+8] -> MovableObject+0x44

connection between these chains = NOT_ESTABLISHED
historical building XYZ = NOT_RECOVERED
```

## 2. Fact register (prior evidence, not re-executed this run)

| # | Fact (as recorded by prior evidence) | ERA/BUILD | EVIDENCE_ORIGIN | SOURCE_PATH / HASH | Status | REEXECUTED_THIS_RUN |
|---|---|---|---|---|---|---|
| 1 | Physical template record 4057 in `pcg_install/Data/Parameters/templates.vfs` (record header offset 88792, version 1, payload length 28, CRC32 79E7AC62 recompute-match) has resource fields: payload+4 = 218757 (model), payload+8 = 218758 (paired volume); payload+0x10 = 0x41AA0F28 (float reading 21.257400512695312; unit/semantics NOT established; NOT a building position) | PCG 9.3.5 | prior Desktop measurement | `PE_MODEL_218757_PLACEMENT_CASE_RESEARCH_20261009\REPORT.md` / AE4F6A932D50097D6A7AF93EC3C2F2D5020A1DC60A37F97A764137BFFD4CC12F section 4 | PRIOR_DESKTOP_MEASUREMENT_NOT_REEXECUTED_THIS_RUN; a definition/resource relation, NOT a world instance or location | no |
| 2 | The displayed GLB `218757_complete_textured.glb` (511452 B / D58D7534998260734DAFBF44CF3096C897D4D9C43533BA1E3FC408CA4BB9818F) is tied to the OLDER 2003 ARK payload: NIF 4.1.0.12, 56535 B / C13D08736D7E778803E20A3105067448007F32D15290AF168F836CD99248AD98; both ARK copies byte-identical (F660D055B4B9471B3B6E16B07F5368DBD6F2208DAB6B51BB9BDB9942BD73EA62); ark_export_report prefix c13d08736d7e7788, 62 blocks, 14 shapes, 1130 vertices, 526 triangles, 9 textures | 2003 CD / ARK (for the GLB) | prior Desktop measurement | same REPORT.md section 2 | PRIOR_DESKTOP_MEASUREMENT_NOT_REEXECUTED_THIS_RUN | no |
| 3 | The PCG 9.3.5 corpus contains the SAME NUMBER as a DIFFERENT payload: NIF 10.1.0.0, 57316 B / 3E8A22C2213202207E374B55CD65B2C3BE039CCDD1E8D01A07FCAF44DE12CF36, 66 blocks per pinned prior decode (Models.bnt payload offset 116223520; older corpus BNT_Models offset 57504982) | PCG 9.3.5 | prior Desktop measurement (prior adapter record for block counts) | same REPORT.md section 2 | PRIOR_DESKTOP_MEASUREMENT_NOT_REEXECUTED_THIS_RUN; **no build/identity/instance/placement transfer between the two variants** | no |
| 4 | Viewer Bounds approximately [2500, 1250, 3350] = the GLB POSITION accessor extent (min (-1100, -100.00001525878906, -1850) to max (1400, 1150, 1500)); viewer recentering (viewer.js L214-220) and Bounds printing (L532-562) are PRESENTATION; not world XYZ, not proven metres | 2003 CD / ARK (GLB export) | prior Desktop measurement | same REPORT.md section 1 | PRIOR_DESKTOP_MEASUREMENT_NOT_REEXECUTED_THIS_RUN | no |
| 5 | Older-variant root NiNode "Scene Root" has translation (0,0,0), identity rotation, scale 1 (transform at NIF offset 83); PCG-variant root prefix (boundary 448 per prior adapter record; transform at offset 496) likewise translation (0,0,0)/identity/scale 1. Zero root translation establishes only that field's value; it does NOT prove the file cannot carry placement information, nor that missing placement must arrive by network | 2003 ARK + PCG 9.3.5 | prior Desktop measurement (prefix reads; no full 4.1 decoder; no custom NiArk ExtraData decoding) | same REPORT.md section 3 | PRIOR_DESKTOP_MEASUREMENT_NOT_REEXECUTED_THIS_RUN | no |
| 6 | Mesh names in the older payload include B_Outpost_me01_Ext_main, _bigdoors, _sign, _vent03 — justifies treating the asset as an outpost-part model; does NOT identify Port Atlantis, any specific outpost or any one historical instance | 2003 ARK | prior Desktop measurement | same REPORT.md section 3 | PRIOR_DESKTOP_MEASUREMENT_NOT_REEXECUTED_THIS_RUN | no |
| 7 | The prior 27-file Parameters scan (top-level PCG Data/Parameters *.vfs, 14825 outer records, 0 CRC failures, all walks closed at EOF) searched ONLY exact little-endian u32 sequences 218757 / 218758 / 4057 on payload alignments: 218757 -> one hit (template 4057 payload+4); 218758 -> one hit (same payload+8); 4057 -> three hits (own ID in template; hierarchy context `[477, 2437, 4057]` with NO established geographic semantics; sids string ID `4057 -> S_REPAIR_UI_CONFIRM_REPAIR`, a DIFFERENT namespace, not a building reference) | PCG 9.3.5 | prior Desktop measurement | same REPORT.md section 4 | PRIOR_DESKTOP_MEASUREMENT_NOT_REEXECUTED_THIS_RUN; its negative does NOT prove absence of local placement or a network-only source (bounded to literal u32 refs; other keys/encodings/directories/messages/cache/runtime structures/indirect references not examined) | no |
| 8 | Independent current chain (preserved bridge records, commit a7b1dc0/2ac7cfa era): under AS1-AS5 and EAX!=0, ADDRESS(T+8) is delivered as arg1 of FUN_00528E50 at CALL 0x004C47C1 AND as arg1 of FUN_0085B1B0 at CALL 0x00528E8D (CROSS_CALL_POINTER_VALUE_IDENTITY = CONFIRMED_STATIC_CONDITIONAL); T = ESP at 0x004C47AF (NOT the older R/P/T/W symbol); prior constructor evidence reads [arg1+8] into MovableObject+0x44; substituting that same pointer gives LOAD ADDRESS T+0x10 at load time; contents, producer, numeric type and field semantics remain UNRESOLVED | PCG client binary (windows A [0x00528E50,0x00528E92), B [0x004C4792,0x004C47C6), STATIC_ONLY) | preserved committed bridge + correction records | `docs/audits/PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009/` (35 files at BASE a7b1dc0) + `docs/audits/PE_935_CMO_ARG1_BR_C1_ARTIFACT_VALIDATION_CORRECTION_R1_20261009/` (20 files); windows re-verified by SHA this run only as gate replays | PRESERVED_CONFIRMED_STATIC_CONDITIONAL (pointer-value identity only); POINTEE_CONTENTS_PROVENANCE = UNRESOLVED_UPSTREAM; FIELD_SEMANTICS = UNVERIFIED | no (the two pinned windows were replay/verify only within the machinery correction; no new body/xref/pointee opened) |
| 9 | Relationship of the CMO/arg1 chain to definition 4057, model 218757, a specific scene object or any world instance | — | preserved records | contract section 5 + the two records above | **NOT_ESTABLISHED** — no confirmed edge between the two chains may be drawn | no |

## 3. Distinctions preserved verbatim (no promotion by recording)

- PCG 9.3.5 record 4057 -> fields 218757 (model) / 218758 (paired volume)
  is a **definition/resource relation**, not a world instance or location.
- The GLB is tied to the OLDER 2003 ARK NIF 4.1.0.12 (C13D0873...); the PCG
  same-number NIF is 10.1.0.0 (3E8A22C2...) — **no build/identity/instance/
  placement provenance transfer between them.**
- Viewer Bounds ~[2500,1250,3350] is **model extent, not world XYZ or proven
  metres**; viewer recentering is presentation; outpost-related mesh names
  do not identify a historical settlement; zero root translation does not
  prove all placement information is absent from every NIF block.
- The 27-file Parameters scan was **bounded to literal u32 references**; its
  negative does not prove absence of local placement or a network-only
  source; equal SID 4057 is a **different namespace**, not a building
  reference by itself.
- The AS1-AS5 + EAX!=0 chain: ADDRESS(T+8) -> arg1 FUN_00528E50 -> arg1
  FUN_0085B1B0; prior ctor evidence [arg1+8] -> MovableObject+0x44;
  substituting the same pointer gives load address T+0x10 at load time;
  contents/producer/numeric type/field semantics **unresolved**; T here is
  ESP at 0x004C47AF, not the older R/P/T/W symbol. No CMO+0x44 -> X
  promotion, no ACLD/CMO identity transfer, J3 supersessions kept.
- **MODEL_218757_TO_CMO_JOIN = NOT_ESTABLISHED**;
  **WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED**;
  **HISTORICAL_PLACEMENT = NOT_ESTABLISHED**;
  **WORLD_XYZ_RECOVERED = NO.**

## 4. Design-only handoff (NOT executed; NOT an authorization)

The preferred subsequent question is: **which existing, exactly pinned
writer/source supplies the value at that call path** (the producer of the
value read at [arg1+8] / the value at T+0x10 at load time) — a question
about an already-pinned writer/source on this call path, to be designed as
its own bounded micro-run with explicit window pins before any execution.
A model-side consumer question (a consumer of definition 4057 / model
218757 establishing a concrete visual object and where it receives its
initial transform) may be chosen SEPARATELY if it has a stronger physical
anchor. Neither is executed by this record; they must not be merged into
one broad run; the answer need not be a coordinate or a building; no writer
VA may be invented. OpenMW/Gamebryo/NIF methodology remains background
prior reference only — no new research, no ABI/offset transfer, no model
join claimed by this correction. NEXT_EXPERIMENT_AUTHORIZED = NO (the next
science decision follows separately published evidence and separate human
authorization).
