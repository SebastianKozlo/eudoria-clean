# VERSION_SUPPORT — PE_GAMEBRYO_ORACLE_TOOL_R1_20261003 (Batch E1, Phase B)

MODE: STATIC / source-derived only. No loader was executed in E1 (executed-loader
observations are Batch E2). Every claim below cites source file + line + SHA256 of
the cited file. Statuses use the closed set {SUPPORTED, REJECTED, PARTIAL, UNKNOWN}.
"Should support" statements are absent by construction (contract s5 / G-VER-1).

## 1. GB_1_2 — Gamebryo 1.2.2 (source tree `D:\gamebyroengine\extracted\Gb12_Source`)

**Engine identity (evidence):** `SDK\Win32\Include\NiVersion.h`
(2,503 B, SHA256 `0F4734C150AB78CC265B65FB21FF122A00EE724866E06424266317E73D940351`)
lines 18-21: `GAMEBRYO_MAJOR_VERSION 1`, `GAMEBRYO_MINOR_VERSION 2`,
`GAMEBRYO_PATCH_VERSION 2`, `GAMEBRYO_BUILD_VERSION 0`, build date 08-06-2005;
`CoreLibs\NiSystem\NiVersion.h` (2,503 B, SHA256
`326D013616AF74DD867147ED96EFA702F5D9E5BD5C707DCFC0C282580547DD7A`) lines 18-21:
1.2.2.**6**, build date 19-06-2006. The tree therefore carries two patch levels of
the same 1.2.2 lineage (SDK headers older than CoreLibs) — both define
`NIF_MAJOR_VERSION CONCAT(1,0)`=10, `NIF_MINOR_VERSION 2` (NiVersion.h lines 41-44
in both variants) → **NIF written by GB 1.2.2 = 10.2.0.0**.

- **MIN_NIF_VERSION_SUPPORTED = 3.3.0.11** — `CoreLibs\NiMain\NiStream.cpp`
  (38,458 B, SHA256 `E955C36EBBB442029E00BE8A154726741B8454A607F2DC043F1FD542B009DC25`)
  lines 42-43: `const unsigned int NiStream::ms_uiNifMinVersion = NiStream::GetVersion(3, 3, 0, 11);`
- **MAX_NIF_VERSION_SUPPORTED = 10.2.0.0** — same file lines 44-46:
  `ms_uiNifMaxVersion = NiStream::GetVersion(NIF_MAJOR_VERSION, NIF_MINOR_VERSION, NIF_PATCH_VERSION, NIF_INTERNAL_VERSION);`
- **SUPPORTED VERSION TABLE (read range):** NIF 3.3.0.11 .. 10.2.0.0 inclusive;
  user-defined version range 0.0.0.0..0.0.0.0 (lines 47-50), read only when file
  version >= 10.0.1.8 (LoadHeader line 335).
- **VERSION COMPARISON LOGIC** — `NiStream::LoadHeader`, NiStream.cpp lines
  303-336 (verbatim, line-numbered):
  ```
  0303: bool NiStream::LoadHeader()
  0304: {
  0305:     // read NIF file header
  0306:     const int iLineCount = 128;
  0307:     char acLine[iLineCount];
  0308:
  0309:     m_pkIstr->GetLine(acLine, iLineCount);
  0310:
  0311:     if (strstr(acLine, "File Format") == NULL)
  0312:     {
  0313:         m_uiLastError = NOT_NIF_FILE;
  0314:         strcpy(m_acLastErrorMessage, "Not a NIF file");
  0315:         return false;
  0316:     }
  0317:
  0318:     NiStreamLoadBinary(*this, m_uiNifFileVersion);
  0320:     if (m_uiNifFileVersion <  ms_uiNifMinVersion)  { ... "NIF version is too old."; return false; }
  0327:     if (m_uiNifFileVersion > ms_uiNifMaxVersion)   { ... "Unknown NIF version."; return false; }
  0335:     if (m_uiNifFileVersion >= GetVersion(10, 0, 1, 8)) { NiStreamLoadBinary(*this, m_uiNifFileUserDefinedVersion); }
  0356:     NiStreamLoadBinary(*this, uiObjects);  // block count
  ```
  Comparison is a plain packed-u32 integer range test
  (`GetVersion(maj,min,patch,int)` = `maj<<24|min<<16|patch<<8|int`,
  `GetVersionFromString` NiStream.cpp lines 1167-1201). The header text line must
  contain `"File Format"` — this accepts both `"Gamebryo File Format, Version ..."`
  and `"NetImmerse File Format, Version ..."` (T4's actual header).
- **FAILURE BEHAVIOR:** `Load()` returns false; `m_uiLastError` set to one of
  {STREAM_OKAY, FILE_NOT_LOADED, NOT_NIF_FILE, OLDER_VERSION, LATER_VERSION,
  NO_CREATE_FUNCTION} (declared `CoreLibs\NiMain\NiStream.h`, 9,921 B, SHA256
  `0EF7F74F2119FED09E88C5047D11D4FE7204F020B5CCD988BE7A1AE2881F82BD`, enum lines
  250-258); error string via `GetLastErrorMessage()`. Unknown class at LoadRTTI →
  `RTTIError` → `LoadRTTI()` returns false → load fails (NiStream.cpp lines
  415-449: `bFound = ms_pkLoaders->GetAt(aucRTTI, ppfnCreate[i]); if (!bFound) { RTTIError(aucRTTI); ... return false; }`).

**P1 reconciliation (pin: "Gb12 NiVersion.h ms_uiNifMaxVersion = 10.2.0.0"):**
VALUE MATCH, LOCATION SUPERSEDED. `ms_uiNifMaxVersion` is *defined in
NiStream.cpp lines 44-46* from the `NIF_*_VERSION` macros of NiVersion.h (lines
41-44); the value 10.2.0.0 reproduces exactly from source. The pin's wording
placed the constant in NiVersion.h; the constant itself lives in NiStream.cpp
(declared NiStream.h line 288 `static const unsigned int ms_uiNifMaxVersion;`).
Both claims recorded (H4 discipline satisfied — same value, corrected location).

**P2 reconciliation (pin: "Gb12 NiObject.cpp per-block GroupID engine range
5.0.0.6 <= v < 10.1.0.114"):** EXACT MATCH. `CoreLibs\NiMain\NiObject.cpp`
(6,377 B, SHA256 `B137FE42126F496A37E7627061FF968256A6DA87D912784865609E2122FE470E`)
lines 134-143 (verbatim):
```
0134: void NiObject::LoadBinary (NiStream& stream)
0136:     if (stream.GetFileVersion() >= NiStream::GetVersion(5, 0, 0, 6) &&
0137:         stream.GetFileVersion() < NiStream::GetVersion(10, 1, 0, 114))
0139:         unsigned int uiID;
0140:         NiStreamLoadBinary(stream, uiID);
0141:         SetGroup(stream.GetGroupFromID(uiID));
```

## 2. GB_2_6 — Gamebryo 2.6.0 (flat source tree `D:\gamebyroengine\extracted\Gb26_src`)

**Engine identity (evidence):** `NiVersion.h` (3,595 B, SHA256
`36BEAD880811F96B67E76734056A6B608FACC1A013F9D7139FDC018A7D0C0A57`) lines 18-25:
GAMEBRYO 2.6.0.0, build 20-10-2008 (Emergent copyright 1996-2008);
`NIF_MAJOR_VERSION CONCAT(2,0)`=20, `NIF_MINOR_VERSION 6` (lines 41-42) →
**NIF written = 20.6.0.0**.

- **MIN_NIF_VERSION_SUPPORTED = 10.1.0.114** — `NiStream.cpp` (64,363 B, SHA256
  `72781EEB0E22D42152E04FADD498EA30292D1807E5C60378F08BFD8563693BA2`) lines 48-49:
  `const unsigned int NiStream::ms_uiNifMinVersion = NiStream::GetVersion(10, 1, 0, 114);`
- **MAX_NIF_VERSION_SUPPORTED = 20.6.0.0** — same file lines 50-52.
- **SUPPORTED VERSION TABLE (read range):** NIF 10.1.0.114 .. 20.6.0.0.
- **VERSION COMPARISON LOGIC** — `NiStream::LoadHeader`, NiStream.cpp lines
  374-407: identical `"File Format"` string test (lines 380-387), identical
  `< ms_uiNifMinVersion` / `> ms_uiNifMaxVersion` integer range test (lines
  395-407); plus endian handling absent in 1.2: header read forced little-endian
  (lines 389-391) and a serialized endianness flag when version >= 20.0.0.3
  (lines 412-415), `ENDIAN_MISMATCH` error path (lines 417-425).
- **FAILURE BEHAVIOR:** same false-return + OLDER_VERSION/LATER_VERSION error
  codes as GB 1.2 (`NiStream.h`, 13,419 B, SHA256
  `DCBB5DD3664B5DD105A535071787997023EC385102A18418D82310AFE1B7EF45`).
  Unknown-class handling differs: `LoadRTTIHelper::ParseRTTINameAndArgs`
  (NiStream.cpp lines 630-683) + `SKIPPABLE_MASK = 0x8000` (NiStream.h line 363)
  allow unknown classes to be **skipped (NULL placeholder)** when the file version
  >= 20.2.0.5 and the skippable bit is set (lines 655-677); for older file
  versions an unregistered class still fails the load (lines 663-668).

**GB 1.2 vs GB 2.6 per-block GroupID difference (1.x vs 2.x, explicit):**
GB 2.6 `NiObject.cpp` (7,088 B, SHA256
`F25499D8C91281B49A3BFF61AEB801B7A09948DA63DA5D2292D5701077AFDA5E`) lines 150-158:
GroupID u32 read when `stream.GetFileVersion() < NiStream::GetVersion(10, 1, 0, 114)`
— **no lower bound** (GB 1.2 requires `>= 5.0.0.6` too, GB 2.6 dropped the lower
check). For NIF 10.1.0.0 both read the GroupID; for NIF 4.1.0.12 GB 1.2 reads it,
GB 2.6 rejects the file before reaching it.

## 3. GB_1_1_2 — Gamebryo 1.1.2 Evaluation (installed tree, BINARY SDK)

**Engine identity (evidence):** `SDK\Win32\Include\NiVersion.h` (1,166 B, SHA256
`67C9C745142D217A3A7F95BEFD4E7B0D098BEEF3973CC7375DD808EBD9D15249`) lines 18-21:
`NI_MAJOR_VERSION 10`, `NI_MINOR_VERSION 1`, `NI_PATCH_VERSION 0`,
`NI_INTERNAL_VERSION 0` (NDL copyright 1996-2004) → **GB 1.1.2 identifies/writes
NIF 10.1.0.0** — the same NIF version as the PCG 9.3.5 corpus header
("Gamebryo File Format, Version 10.1.0.0", see 04_EVIDENCE/EXTRACT_PROVENANCE.json).

- **MIN/MAX_NIF_VERSION_SUPPORTED = UNKNOWN (binary-only):** `SDK\Win32\Include\NiStream.h`
  (8,961 B, SHA256 `DF8057C664B3544457867544DF81F716938EC9DF412E165CC7678F6EB6FA620C`)
  lines 261-264 declare `ms_uiNifMinVersion/ms_uiNifMaxVersion` as `static const
  unsigned int` members — the VALUES are compiled into `NiMain.lib` (no .cpp in
  the installed SDK; GB112 SDK cpp census = 0 files). No source claim is possible.
- **SUPPORTED VERSION TABLE:** UNKNOWN (headers declare the same LoadHeader /
  LoadStream / LoadRTTI / RTTIError pipeline as GB 1.2 — NiStream.h lines
  161-185, 249-270 — but the gate constants are not source-visible).
- **VERSION COMPARISON LOGIC:** NOT_AVAILABLE_IN_SOURCE (binary lib only);
  structure implied by GB 1.2 lineage is recorded as UNVERIFIED, not claimed.
- **FAILURE BEHAVIOR:** error enum {STREAM_OKAY, FILE_NOT_LOADED, NOT_NIF_FILE,
  OLDER_VERSION, LATER_VERSION, NO_CREATE_FUNCTION} declared NiStream.h lines
  250-258 — same vocabulary as GB 1.2.

**P4 record (canon pin):** installed SDK lib
`SDK\Win32\Lib\VC71\ReleaseLib\NiMain.lib` = 3,073,590 B, SHA256
`FF4519AFD2475D9A6E71A35E5DB6B0F5A0B7E9E86EC3662C6A340DA19BA06597` —
**prefix FF4519AF and size MATCH the P4 pin (CONFIRMED this run).** Full lib
census (37 hashed NiMain.lib copies across trees) in sandbox
`phaseA\inventory_data.json` `libs` array.

## 4. GB_2_3 — Gamebryo 2.3.0 Evaluation (GB_2.3.iso, BINARY SDK)

**Engine identity (evidence):** `GB_2.3.iso` → `GbEvaluationSDKSetup.exe`
(187,899,445 B, SHA256
`69F84692D8BF857D607B30C6748F18B8FDEA857D43B63C56B4E63619E74C015E` — computed
this run; ISO itself SHA256
`AF3391BF959672A1740C2BD6EAE5C4D944E557D6FEAE338B8E5128EB3F4482F4`). The ISO's
`Gb23EvaluationDisk01.txt` reads "Gamebryo 2.3 Evaluation Disk 1" and
`GbEvaluationSetup.ini` sets `Label = Gamebryo 2.3 Evaluation Disk 1`
(extracted to sandbox this run). The setup is a **Wise installer** whose 7z file
table (4,642 entries) exposes UPPERCASE 8.3-style names; bounded per-name
extraction recovered `NiVersion.h`
(3,438 B, SHA256 `DFCCD6ECA8D48B984B1931D0A983E758A37167CCCBCF742143B6555CBFB81D39`)
lines 18-24: GAMEBRYO **2.3.0.0**, build 24-04-2007; lines 41-44:
`NIF_MAJOR_VERSION CONCAT(2,0)`=20, `NIF_MINOR_VERSION 3`, **`NIF_INTERNAL_VERSION 9`**
→ **NIF written = 20.3.0.9**. Lib names `NIMAIN23VC71D/R/S.LIB` encode "23" + VC71
configs.

- **MIN/MAX_NIF_VERSION_SUPPORTED = UNKNOWN (binary-only):** recovered
  `NiStream.h` (11,033 B, SHA256
  `532FEE68C565204230A93E5874A185806AABAB103C6B2D156CC274B6EFB6104D`) lines
  314-317 declare `ms_uiNifMin/MaxVersion` as static const; the SDK setup's Wise
  table contains **0 `NI*.CPP` core entries** (binary SDK — CoreLibs source not
  shipped in the evaluation). No source value claim is possible.
- **SUPPORTED VERSION TABLE:** UNKNOWN from source. The 2.x pipeline shape is
  header-evidenced (NiStream.h: `LoadHeader` L210, `LoadStream` L212,
  `LoadRTTI` L231, `LoadObjectSizeTable` L220, `LoadFixedStringTable` L238,
  `SetSelectiveUpdateFlagsForOldVersions` L226).
- **VERSION COMPARISON LOGIC:** NOT_AVAILABLE_IN_SOURCE (binary lib only).
- **FAILURE BEHAVIOR:** NOT_AVAILABLE_IN_SOURCE.

## 5. G-VER-2 — the NIF 10.1.0.0 / 4.1.0.12 question (per version)

| GB version | NIF 10.1.0.0 | NIF 4.1.0.12 | Evidence class |
|---|---|---|---|
| GB_1_2 (1.2.2) | **SUPPORTED (version gate, source)** — 3.3.0.11 <= 10.1.0.0 <= 10.2.0.0; GroupID read per block (P2); executed-loader confirmation = E2 | **SUPPORTED (version gate, source)** — same range; < 4.1.0.0 conditionals exercised in LoadBinary paths | NiStream.cpp L42-46, L303-336; NiObject.cpp L134-143 |
| GB_2_6 (2.6.0) | **REJECTED (source)** — 10.1.0.0 < ms_uiNifMinVersion 10.1.0.114 → OLDER_VERSION "NIF version is too old." | **REJECTED (source)** — below min | NiStream.cpp L48-52, L395-401 |
| GB_1_1_2 (1.1.2) | **UNKNOWN** — engine identifies as NIF 10.1.0.0 itself, but the read range is compiled into NiMain.lib (binary) | **UNKNOWN** (same) | NiVersion.h L18-21; NiStream.h L261-264 (declarations only) |
| GB_2_3 (2.3.0) | **UNKNOWN** — read range compiled into NIMAIN23VC71R.lib (binary) | **UNKNOWN** | NiVersion.h (recovered) L18-24; NiStream.h L314-317 |

**FULL vs PARTIAL for GB_1_2 + NIF 10.1.0.0 (source-level statement):** the
version gate accepts; every block-type LoadBinary implementation is present in
source for the standard Gamebryo classes; unknown/unregistered RTTI class names
FAIL the whole load (RTTIError path, fail-closed, not skip). The PCG 9.3.5 corpus
contains MindArk-custom block types (project canon: NiArk* classes in 10.1.0.0
files); **source-derived prediction (not an executed result): a 10.1.0.0 file
containing NiArk* blocks will fail GB 1.2 LoadRTTI unless those loaders are
registered** — E2 must test exactly this on T1/T2/T3/T5. Until the executed-loader
runs exist, GB_1_2 10.1.0.0 support stays **SUPPORTED (source) / NOT_TESTED
(execution)** — no FULL/PARTIAL execution verdict is claimed in E1.

**T-corpus object-coverage basis:** per-file block mixes are in the manifest
`block_histogram` column (docs/nif/corpus/pcg953_nif_manifest.csv, SHA256
`2BE0DEFC9C09FF26371528A4601C10216AC3013717A244EB0652169123989B59`, re-hashed
this run); the five selected payloads with re-read headers are in
04_EVIDENCE/EXTRACT_PROVENANCE.json.

## 6. Source availability summary (era-separated)

| GB version | SOURCE (.cpp CoreLibs) | HEADERS | LIBS | TOOLS |
|---|---|---|---|---|
| GB_1_2 | FULL (Gb12_Source CoreLibs + SDK) | yes | yes (multi-config) | sources + prebuilt exes |
| GB_2_6 | FULL (Gb26_src flat) | yes | yes (6 lib variants) | prebuilt exes (AnimationTool, AssetViewer, SceneDesigner, SceneGraphPrinter, PhysXNifViewer...) |
| GB_1_1_2 | NO (binary SDK; 0 cpp) | yes | yes (VC6/VC71 configs; P4 pin lib) | tool sources in the ZIP + prebuilt exes installed |
| GB_2_3 | NO (binary SDK; 0 NI*.cpp in Wise table) | yes (recovered from SDK setup) | yes (NIMAIN23VC71D/R/S) | installer only (not extracted in E1) |
