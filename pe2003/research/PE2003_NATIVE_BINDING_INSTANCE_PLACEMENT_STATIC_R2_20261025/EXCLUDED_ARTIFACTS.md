# EXCLUDED_ARTIFACTS — PE2003_NATIVE_BINDING_INSTANCE_PLACEMENT_STATIC_R2_20261025

Excluded from this public projection (remain private in D:\Eudoria_Reconstruction per the sanitization contract):

- **B02a_DECODE_ANNOTATED.txt** (44 148 B, SHA256 B88E7D45F6315E8000428FA39999ADC253FDB88C09A3FBD7F060C8957928BEAB) — root-excluded BEFORE this publication: annotated decoded DLOB bytecode dump (decoded bytecode listing).
- **P01_NIF_BLOCK_MAP.csv** (15 720 B, SHA256 CC9A1D7B81D6DFBA0D38B7196D5A0E8ECD6904575C2B36E9C75E9A1BA559C753) — root-excluded BEFORE this publication: per-block derived NIF data.
- All game data: ISO/installers, EXE/DLL images, ARK/NIF/BNT/BVI members, textures, DLOB plaintexts/decoded corpus files, raw disassembly dumps/trace listings (EXE identity cited by SHA256 only).
- Raw worker evidence: per-job Ghidra projects/decompiles, byte dumps, scan logs (WORK_ROOT).
- Internal process material: ADMISSION_EVENTS ledger, BUDGET_LEDGER, INPUT_PINS, prompt/contract texts, model DB/session material, tools.

Sanitization scan (executed before commit over all 38 allowlist files, this run):
- UTF-8 validity: 38/38 PASS.
- Sealed MANIFEST_SHA256.csv bijection for the 37 copied rows: 37/37 size+SHA256 PASS (MANIFEST_SHA256.csv itself is self-excluded by design).
- Long-hex scan (>=64 hex chars): all hits adjudicated = uppercase SHA256 hash identities (allowed) — zero raw-data hex blocks.
- Byte-sequence scan (spaced hex groups): all hits adjudicated = isolated 10-13-byte instruction-encoding citations each tied to an explicit VA or file offset (structural byte-check metadata of the same class as previously published projections); zero contiguous byte dumps or bytecode listings; longest run 13 bytes.
- Credential/secret scan: 0 hits.
- Result: 0 additional files excluded beyond the two root-excluded above.

Allowed here (and only this): analysis text, function names, VAs, instruction-encoding citations with pinned sites, size/SHA256 identities of pinned inputs, offset constants, census denominators, verdicts.

Publication manifest bijection: PUBLICATION_MANIFEST.csv (repo root) covers every path changed by this commit (self-excluded); every blob re-verified SIZE+SHA256 against the manifest before push.
