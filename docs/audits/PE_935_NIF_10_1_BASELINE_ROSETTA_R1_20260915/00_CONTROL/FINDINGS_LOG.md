# FINDINGS_LOG — PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915

Append-only working findings log (executor). Final polished versions go to 02_ANALYSIS/*.

## F-01 (S0/S1) BNT2 structure physically verified (2026-09-15)
- Footer last-8: DirOffset u32 LE + "BNT2". Physical: DirOffset=395262727.
- Index at DirOffset: NumEntries u32 = 5596 (physical). Entry: name ASCII + 0x0A + 16B {size,offset,field_c,field_d}.
- Last entry ("16175.nif" [QC AMEND-005: fixed typo "175.nif"; bytes
  unchanged]): size=27971, offset=395234756; offset+size == DirOffset EXACT.
- Entry0 "505775.nif": offset=0, size=306034; entry1 offset=306034 (contiguous).
- PRIOR KNOWLEDGE SOURCE: Dragon UnPACKer BNT2Entry (skill) — treated as hypothesis, now physically verified on live bytes; full walk with fail-closed invariants pending (s01).

## F-02 (§4) Entropia NIF 10.1.0.0 header layout — ENGINE GROUND TRUTH (2026-09-15)
Physical (entry0 505775.nif, PCG 9.3.5 Models.bnt):
- @0 HeaderString: "Gamebryo File Format, Version 10.1.0.0\n" — 0x0A-terminated, NO length prefix (39 bytes)
- @39 Version u32 LE = 0x0A010000
- @43 User Version u32 = 0  [cond: >= 10.0.1.8]
- @47 Num Blocks u32 = 103
- @51 Num Block Types u16 = 13
- @53 Block Types: 13× SizedString (u32 len + chars): NiNode, NiArkAnimationExtraData, NiArkImporterExtraData, NiArkTextureExtraData, NiTexturingProperty, NiTextureEffect, NiArkViewportInfoExtraData, NiMaterialProperty, NiZBufferProperty, NiTriShape, NiTriShapeData, NiAlphaProperty, NiPointLight
- @323 Block Type Index: u16 × NumBlocks (206B for 103)
- @529 Num Groups u32 = 0  [cond: >= 5.0.0.6]
- @533 Block 0 GroupID u32 = 0  ← per-block, part of NiObject::LoadBinary
- @537 Block 0 (NiNode) Name SizedString "Scene Root"

ENGINE SOURCE (D:\gamebyroengine\extracted\Gb12_Source\CoreLibs\NiMain\NiStream.cpp — Gamebryo 1.2 source):
- NiStream::LoadHeader: GetLine(HeaderString) → Version u32 → UserVersion u32 (file >= 10.0.1.8) → NumBlocks u32.
- NiStream::LoadRTTI (file >= 5.0.0.1): u16 RTTI count → LoadRTTIString×count (u32 len + chars) → u16 type index per object.
- NiStream::LoadObjectGroups (file >= 5.0.0.6): u32 NumGroups → u32 size per group.
- NiObject::LoadBinary (NiObject.cpp L134): reads u32 GroupID if file version >= 5.0.0.6 AND < 10.1.0.114. ← per-block GroupID
- NiStream::LoadTopLevelObjects: after all blocks: u32 NumTopObjects + u32 LinkID each.

## F-03 (§4) BASELINE CONFLICT #1 — GroupID version condition (2026-09-15)
- Modern nif.xml (0.10.0.0): NiObject "Group ID" field `since="10.1.0.114"` ("Always zero.")
- Historical nif.xml (0.7.1.1): NO GroupID field at all in NiObject.
- Engine source (Gamebryo 1.2): GroupID for 5.0.0.6 <= version < 10.1.0.114 — INVERTED vs modern schema for 10.1.0.0.
- Physical adjudication (5 independent 10.1.0.0 files, 3 publishers):
  - EE2 lodtest.nif + lodtest-skinned.nif (Empire Earth II, non-MindArk): GroupID present (=0)
  - Gamebryo 1.1.2 SDK samples BABYLENGUIN.NIF / DESTROYERBOT.NIF / ROCKY.NIF / BABYLENGUIN.KF: GroupID present (=0)
  - Entropia PE_101358/PE_11710/PE_508947 + corpus files: GroupID present (=0)
- VERDICT: public schemas (all pinned variants) FAIL to model per-block GroupID for 10.1.0.0; engine + physical bytes agree. Baseline for this run = engine-source framing.
- NOTE: NiflySharp (104d79f) NiHeader reads only NumGroups after array → would misalign blocks on real 10.1.0.0 files. Its 10.1.0.0 support is untested against real Gamebryo-1.x-era files.

## F-04 (§4) External oracles pinned locally (2026-09-15)
- nif.xml variants (5 distinct): nifxml modern 0.10.0.0 (SHA D6B76A83..., 565041B, == byroredux legacy copy), nifxml_historical 0.7.1.1 (SHA 1D5C8E58..., 401093B, == pyffi copy), NifSkope 2.0 (2018-02-22) bundled (0DCE5092..., 466952B), NiflySharp bundled (752C7978..., 570454B), fo76utils build (880C3167..., 667577B).
- NiflySharp source: ousnius-NiflySharp-104d79f (C# implementation).
- Gamebryo engine source: Gb12_Source (Gamebryo 1.2 full source) + Gamebryo 1.1.2 Evaluation SDK (D:\gamebyroengine\) + gb112_known_good sample NIFs.
- EE2 10.1.0.0 samples: blender_niftools todo/old_nifs/ee2/lodtest.nif, lodtest-skinned.nif.
- Also available: pyffi source, blender_niftools (0305c8d), openmw 0.51.0, openmw-nif, pynifly, byroredux, f4ref_to_blender.
- Historical nif.xml 10.1.0.0 version entry EXPLICITLY LISTS "Entropia Universe" as a 10.1.0.0 title.

## F-05 (§1 probe) SOLDIER.NIF (SDK sample) = 10.0.1.18 (0x0A000112) — a 10.0.1.x variant exists in SDK; not in PCG corpus expectation (watch during census).

## F-06 Header+block framing for 4.1.0.12 / 4.0.0.2 (from engine + schema, to verify on physical bytes during census):
- line + version u32 + NumBlocks u32; block types INLINE (SizedString before each block, no RTTI table — file < 5.0.0.1); NO GroupID (4.1 < 5.0.0.6); no groups.

## F-07 (§8/§9) NiArkImporterExtraData v10 tail = 41 BYTES (2026-09-15)
- Closure-confirmed 2,343/2,343 slice blocks (+ witness 457485.nif dump): name + u32(=8) + SS version + 41B = 13B header + 7×f32 (bbox 6 + pad 0.0).
- Matches HIST schema stub (UnknownBytes[13]+UnknownFloats[7]=41). WIKI 38B claim SUPERSEDED: the parser's 38+3 split re-attributes the tail pad's last 3 bytes to ArkTexture's "3 unknown zero bytes" (bit-compatible).
- Importer int1 = 8 in ALL slice blocks. Version strings (slice): Gamebryo_1_1 ×2,302 / 4.1.0.12 ×36 / 4.0.0.2 ×5.

## F-08 (§8/§9) ArkTexture entry ref = BLOCK LINK (2026-09-15)
- 10,610 refs → NiTexturingProperty; 1,105 → NiTextureEffect (ENVIRONMENT-slot pairing f1=9); +3 NiNode + 24 garbage (anomaly family).
- HIST schema's "Texturing Property Ref" role CONFIRMED; docs/nif/08 "slot/purpose index" label SUPERSEDED.

## F-09 (§8/§9) ArkTexture count = (field2>>8)&0xFFFFFF in 99.0% (2026-09-15)
- 2,319/2,343 slice blocks formula==closure-truth; 24-block variant family deviates (17× count=1/field2=0 via field1; 7× count=3 via numfield; f1=15 ×24 / 0x1000000 ×3 entries).
- NEW OPEN FINDING; prior "4,838/4,838 PERFECT" claim SUPERSEDED. Parser (JS, no fallback) would mis-read the 24 blocks → PARSER_GAP row.

## F-10 (§8/§9) Width-identical split ambiguities resolved to BASELINE labels (2026-09-15)
- NiTexturingProperty header 4B = ApplyMode u32 (enum {0,2} observed; TextureCount=7 constant ×7,088) — wiki's 2×u16 = alternative split of the same bytes.
- NiVertexColorProperty 10B = flags u16 + VertMode u32 + LightMode u32 (schema closure 2,544/2,544); the wiki u16×3+u32 "PE ext" = width-identical alternative; "PE-SPECIFIC" attribution SUPERSEDED (ambiguity disclosed, not semantically resolved).
- NiGeometryData "numUvSets u16" ≡ u8 count + u8 ExtraVectorsFlags (bit-identical: low6=count, bit4=tangents; flags=0 ×8,206 / 48 ×377).
- TexDesc 32B "raw transform" = Translation/Tiling TexCoord + WRotation f32 + TransformType u32 + CenterOffset TexCoord; "trailing u32==0" = NumShaderTextures==0.

## F-11 (§10) Closure + holdout discipline (2026-09-15)
- World slice (2,363 files, 32 supported types): TRAIN 1,876/1,890 (99.3%); HOLDOUT 467/473 (98.7%); hypothesis_sha frozen 6DB2F1E3...; 20 PARSE_BLOCKED recorded with reasons.
- 0 out-of-range refs; NaN/Inf fail-closed; TopObjects root = block0 NiNode in 2,343/2,343 closed files; per-block GroupID==0 everywhere.

## F-12 (§14) Cross-publisher closure (2026-09-15)
- EE2 lodtest.nif (non-MindArk 10.1.0.0): FULL CLOSURE with the same frozen layouts (7 blocks + footer).
- EE2-skinned/SDK samples fail only at types absent from the Entropia corpus (skin/PSys/strips/camera...). The Entropia world slice == standard Gamebryo 10.1.

## F-13 (§15) Parser audit verdicts (2026-09-15)
- NifModelReader.js: 8 PARSER_MATCHES_STANDARD; 4 unverified width-identical assumptions; 2 bit-compatible mis-attributions (38+3); 1 defect-class finding (ArkTexture count formula, 24-block family, no fallback in the JS reader); witness-scope limits by design.
- Recommended separate runs: PE_935_NIF_PARSER_TEXTURECOUNT_24BLOCK_CORRECTION_R1 (+ minor relabel ride-along; REPORT-ONLY held — no src/ changes made).

## F-14 (§CORRECTION, 2026-09-15, PE-MASTER-adjudicated correction batch, AMEND-009) RETRACTION of F-09: the "24-block ArkTexture variant family" is a DECODER CANDIDATE-ORDER ARTIFACT, not a corpus fact
- RETRACTS: F-09's variant family as a corpus fact; the "formula==closure-truth in 2,319/2,343 (99.0%)" verdict; the slice-level supersession of the prior wiki "4,838/4,838 PERFECT" claim; F-09's 17/7 description (superseded by the byte-verified 18+6 split below). F-09 above is retained as a historical entry of this append-only log.
- MECHANISM (byte-confirmed): s06 orders ArkTexture entry-count candidates (A,'numfield'), (B,'field1'), ((C>>8)&0xFFFFFF,'field2>>8'), (C&mask), (0,'zero') and deduplicates them BY VALUE; when the true count is reached only by a later candidate, a wrong earlier candidate can close the file first by consuming the NEXT block's GroupID+name bytes as fake "entries" (the elastic ArkViewportInfo ext search then absorbs the remainder). The run's own NEGATIVE_CONTROL_RAW "residual honesty notes" anticipated exactly this artifact class.
- RE-DERIVATION EVIDENCE (s12_arktexture_zero_count_rederivation.py; 01_RAW/ARKTEXTURE_ZERO_COUNT_REDERIVATION.csv 38 rows + 01_RAW/ARKTEXTURE_FAKE_ENTRIES_RETRACTED.csv 27 rows; all rows signature-verified gid=0+len+canonical name and type-index agreement NiArkViewportInfoExtraData/"ArkViewportInfo"):
  - 32 in-slice ZERO-COUNT blocks ((C>>8)&0xFFFFFF == 0): 25× header (3,1,0,0) + 7× (3,0xFFFFFF00,0xFF,0) by raw byte scan over all 4,838 v10.1 payloads [note: the QC summary's 24/8 signature split differs by one file; the per-block CSV rows are authoritative]. The bytes right after each 13B header are the NEXT BLOCK's start (zero entries). 18 were mis-parsed by the frozen decoder (accepted count=1 via field1); 8 closed consistently (accepted count=0 = formula); 6 live in files the frozen decoder blocks (FAIL:EOF; subset of the 20 PARSE_BLOCKED).
  - 6 further deviation blocks (accepted != formula) with TRUE count 1 or 2 = formula: 386950/386951/386590 (C=0x100; one real entry "*_0_BASE", ref=7) and 488579/493785/490489 (C=0x200; two real entries Box02_*_BASE / Box01_*_BASE). The frozen decoder accepted count=3 via numfield on all 6 (consuming the viewport block's start as fake entries 2-3).
  - The 24 deviation blocks ARE the complete "variant family" of F-09 (24 total stands; its 17/7 split superseded by 18 zero-count + 6 count-1/2).
- CORRECTED FORMULA VERDICT: (field2>>8)&0xFFFFFF == TRUE entry count in 100% IN-SLICE: 2,319 direct (accepted==formula) + 24 re-derived (this correction) = 2,343/2,343 frozen-decoder closures; the QC independent decoder: 2,361/2,363; union = every one of the 2,363 slice files closes under at least one of the two decoders with formula==true count. The prior wiki claim "4,838/4,838 PERFECT" is NOT superseded at slice level — it is CONFIRMED in-slice; corpus-wide outside the slice (2,475 files) remains an OPEN item (raw scan observes 1,790 further zero-count-signature ArkTexture blocks outside the slice, 1,101 of them already byte-consistent with zero-entries+viewport-next; verification deferred; prior claim uncontradicted).
- FAKE-ENTRY ATTRIBUTION (27 entries; ARKTEXTURE_FAKE_ENTRIES_RETRACTED.csv): ALL recorded anomalies were artifacts of the 24 mis-parsed blocks: 24× OOR ref 1886872937 (= ASCII "iewp" of "ArkViewportInfo"), 3× NiNode ref (ref=0 -> block 0 "Scene Root"; fake 3rd entry of 386950/386951/386590), f1=15 ×24 (= len("ArkViewportInfo")), f1=16777216 ×3, f2=1449882177 ×24 (= ASCII "ArkV"). After retraction the TRUE ArkTexture entry-ref targets are NiTexturingProperty 10,610 + NiTextureEffect 1,105 (NEVER polluted — every fake ref went OOR or to NiNode), 0 NiNode, 0 OOR; TRUE f1 domain exactly the prior claim {0,1,2,3,4,5,6,9} (11,715 true entries); TRUE f2 domain {-1: 10,226, 0: 1,489}.
- INSTRUMENT note: the frozen TRAIN/HOLDOUT/ALL results (1,876/1,890; 467/473; 2,343/2,363) are UNCHANGED (closure byte consumption identical); 24 of the 2,343 "closure OK" files carry a mis-attributed ArkTexture/ArkViewportInfo boundary (file structure totals unchanged; semantic attribution corrected by this entry). Decoder-instrument hardening note for future runs: order count candidates field2>>8-FIRST or validate the next-block signature at the entry boundary — this is an INSTRUMENT-ordering note, not a parser defect (see the parser verdict below).
- PARSER VERDICT (supersedes F-13's defect-class row and PARSER_GAP_MATRIX row 7): the JS/R61 formula (field2>>>8)&0xFFFFFF reads ALL these blocks CORRECTLY (formula == true count in-slice 100%); there is NO 24-block parser defect; the recommended run PE_935_NIF_PARSER_TEXTURECOUNT_24BLOCK_CORRECTION_R1 is WITHDRAWN (false premise — no family exists in-slice to investigate; the fallback idea is unnecessary; how R61 passes those files = it reads the correct count).

## F-15 (§CORRECTION, 2026-09-15, AMEND-009) F-08 update — ArkTexture entry-ref attribution after F-14
- F-08's core finding STANDS, now cleaner: the ArkTexture entry ref = BLOCK LINK to NiTexturingProperty (10,610 refs) / NiTextureEffect (1,105 refs; ENVIRONMENT-slot f1=9 pairing) — confirmed byte-wise by PE-MASTER on 505775.nif (entry "Box01_1_BASE" ref=4 -> block#4 = NiTexturingProperty) and by this run's re-derivation (all real refs target NiTexturingProperty/NiTextureEffect; 0 out-of-range after retraction).
- The F-08 qualifiers "+3 NiNode + 24 garbage (anomaly family)" are RETRACTED as decoder artifacts (F-14): all 3 NiNode refs and all 24 garbage/OOR refs came from fake entries of the 24 mis-parsed blocks; ZERO real NiNode-targeting or out-of-range refs exist in the slice.
- The docs/nif/08 "slot/purpose index" mislabel supersession STANDS (LIVE_DOC_IMPACT_MATRIX row 13 SUPERSEDE unchanged).

## F-16 (§CORRECTION, 2026-09-15, PE-MASTER-adjudicated correction batch, AMEND-010) F-03 NOTE retraction — NiflySharp does NOT misalign on real 10.1.0.0 files
- RETRACTS the F-03 NOTE sentence "NiflySharp (104d79f) NiHeader reads only NumGroups after array → would misalign blocks on real 10.1.0.0 files" (the analysis had stopped at the header reader). F-03's own text above is retained byte-unchanged per the append-only discipline.
- ACTUAL NiflySharp behavior (ousnius-NiflySharp-104d79f, NiflySharp\NiflySharp\NiObject.cs L61-62, Sync): `if (stream.Version.FileVersion >= NiFileVersion.V10_0_0_0 && stream.Version.FileVersion < NiFileVersion.V10_1_0_114) stream.Sync(ref groupId);` — 10.1.0.0 IS inside the range; EVERY block deserializes its own per-block u32 groupId after the header; no misalignment on real 10.1.0.0 files. (NiHeader reading only NumGroups at header level is CORRECT engine behavior — the per-block u32 is consumed per-block, exactly like the engine's NiObject::LoadBinary.)
- RESIDUAL (separate note, not a 10.1 problem): NiflySharp's per-block groupId range starts at V10_0_0_0 whereas the ENGINE (Gamebryo 1.2 NiObject.cpp L134-143) reads GroupID for 5.0.0.6 <= v < 10.1.0.114 — the two differ only for 5.0.0.6..9.x files (NiflySharp would skip the per-block u32 there; out of this run's 10.1.0.0 scope).
- UNAFFECTED: F-03's verdict row (engine range 5.0.0.6<=v<10.1.0.114; physical presence; modern mis-version since=10.1.0.114; historical omission) and conflict C-01's core — CONFIRMED. The hedge "untested against real Gamebryo-1.x-era files" stays as a test-gap note.

## F-17 (§CORRECTION, 2026-09-15, PE-MASTER-adjudicated correction batch, AMEND-014) F-12 cross-publisher wording correction — BABYLENGUIN.NIF nonzero GroupID
- F-12's sentence "EE2-skinned/SDK samples fail only at types absent from the Entropia corpus" (historical entry above, byte-unchanged per the append-only discipline) is FALSE for one sample: BABYLENGUIN.NIF (Gamebryo 1.1.2 SDK, 10.1.0.0) fails this run's decoder at block 7 GroupID=479309 — a NONZERO engine GroupID in a non-PE 10.1.0.0 file.
- READING: positive realism evidence for the GroupID field (the per-block u32 carries real engine values outside PE; PE files have NumGroups=0 hence always 0, so the run's gid==0 closure invariant is PE-scoped BY DESIGN — a decoder intended for non-PE 10.1 files must accept nonzero GroupIDs).
- Corrected wording applied in REPORT §2.4, FIELD_VALIDATION_RAW cross-publisher row, STAGE_ACCEPTANCE_GATES G6 note (AMEND-012). F-12's core verdict (the Entropia world slice IS standard Gamebryo 10.1; EE2 lodtest closure) is UNAFFECTED.

