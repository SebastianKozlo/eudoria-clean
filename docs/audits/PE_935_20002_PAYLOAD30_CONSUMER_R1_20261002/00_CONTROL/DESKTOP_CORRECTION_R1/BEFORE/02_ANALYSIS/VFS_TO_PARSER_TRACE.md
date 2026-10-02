# VFS_TO_PARSER_TRACE — PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002

STATIC_ONLY. The client was never launched (RUNTIME_EXECUTION_PERFORMED=NO).
Binary: D:\Eudoria_Reconstruction\pcg_install\Entropia.exe (SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31, EU 9.3.5.6746).
Data: D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\20002.vfs (SHA256 C3899C3E88D72CE12CEF9B8A4F5E73B26632BB1A3207C950FF2BC40FD9C94AC4, 174,864 B).
Every load-bearing VA below is byte-pinned in `01_RAW\CLIENT_READ_BYTES.json` (45/45 pins OK; bytes read back from the pinned physical EXE at the recorded FILE_OFFSETs).

## §8 ROUTING EDGE — TARGET_PATH=20002.vfs

### 1. Class identity for 20002 (encoding verified in-run)
- 20002 decimal == 0x4E22; LE u32 bytes `22 4E 00 00` (verified: the same bytes open every record payload of 20002.vfs at payload+0).
- MSVC mangling rule (nibbles a..p = 0..15, MSB first): 20002 = 0x4E22 -> `$0EOCC@`. Calibration in the SAME binary: `$0EOCG@` = 0x4E26 = 20006 = `ArkParameterCommon` (matches prior evidence).
- RTTI type-name strings (byte-pinned excerpts at fo 0x78EDE4 / 0x78D89C):
  - `?$ArkObjectImpl@$0EOCC@VArkParameterArmor@@VArkObjectClassInterface@@V2@@@`
  - `?$ArkObjectImpl@$0EOCG@VArkParameterCommon@@VArkObjectClassInterface@@V2@@@`
- **Class 20002 = ArkParameterArmor** (RTTI name; status CONFIRMED at the string/RTTI level).

### 2. imm32 census (in-run, own scanner: 01_RAW\ROUTING_CENSUS_RAW.json)
- imm32 `22 4E 00 00` in .text: 3 sites — 0x73819A (FUN_00738150 -> calls FUN_00703b80), **0x73A442 (FUN_0073a3f0, the registration ctor: `PUSH 0x4E22` @0x73A441 -> `CALL FUN_0070cf80` @0x73A44D)**, 0x73FBCC (FUN_0073fa30 -> calls FUN_00703b80).
- ASCII "20002": 0 hits. The filename is built at runtime via itoa (see 3c).

### 3. The open/routing chain (byte-pinned)
a. **FUN_0073d1f0** (the 20002 driver): `DAT_00ba5da8 = FUN_0073a3f0(new(0x118))`, then `FUN_0070e2f0(0x12, 0)` (descriptor count 0x12 = 18), `FUN_00761570(DAT_00ba5da8)` (schema registration), `FUN_0070c150()`, `FUN_0070bf10()`.
b. **FUN_0073a3f0** (the ctor): `FUN_0070cf80(this, 0x4E22, "")` (base ArkObjectClass ctor: this[2]=classID at +8; 4 trait registrations via FUN_0075f5c0(0..3)) then `*this = ArkObjectClassImpl<class_ArkParameterArmor,20002>::vftable` (0xA86FE0 store @0x73A46B).
c. **FUN_0070c680(classObj, path, flags)** (the class-VFS open; called by FUN_00703e80's class loop, whose sole caller is FUN_004b0980): if `classObj+0x84 == 0` (@0x70C6BE CMP): filename = `path + itoa(classObj->[+8]) + ".vfs"` via FUN_0070c3d0 (@0x70C3FC `MOV EAX,[ECX+8]` = the class ID; @0x70C40E PUSH 0xA86820 ".vfs"; FUN_0040e900 = the decimal int-to-string) -> `FUN_00972df0(reader, filename, ...)` @0x70C742 -> the ArkVFS reader object is stored at **classObj+0x84** (@0x70C71E). **For classObj 20002 the filename is `<path>20002.vfs`** — matching the pinned physical file `Data\Parameters\20002.vfs`.
d. **FUN_00972df0** (verified in-run, pass-1 dump): CreateFileA + GetFileSize + ReadFile 8 bytes + magic check `ArkVFS01`/`ArkVFS02`; for ArkVFS02 reads the remaining 8-byte global header; `this+0x8c` = the file's base field (0x80 for 20002.vfs).
e. **FUN_00972ad0** (index builder; verified in-run): walks the file from +16: reads 16-byte record headers {id, size, ver, crc} (FUN_00979d30 -> 4 u32 reads), checks `size != 0`, records the frame position (FUN_00417eb0 -> state+0x10), inserts id->{id,size,ver,crc,pos,base} nodes into the reader's id->node map (this+0x50) and appends the ids to the id list; advances by `FUN_00979d00 = ((size+0xF)/base + 1)*base - 0x10` — for size=56, base=128: 112 per header-read -> stride 128 (the executor framing rule confirmed at instruction level).

### 4. The per-record read path (byte-pinned)
- **FUN_0073c870** (class registry): `case 0x4E22: return DAT_00ba5da8` (@0x73C8C1 `MOV EAX,[0x00BA5DA8]`).
- **FUN_0070e100(classObj, id)**: instance-map lookup (classObj+0xC map, instance at node+0x14); on miss -> FUN_0070de10.
- **FUN_0070de10(classObj, id, &out)**: `if (state in {1,2} && classObj+0x84 != 0)` -> FUN_0070dcf0(id) [the VFS-backed create]; else the +0x80 trait-object factory path.
- **FUN_0070dcf0(classObj, id)**: `if (classObj+0x84 != 0)` (@0x70DD1A): cursor = new(0x80); `FUN_00971ad0(id, cursor, &out)`:
  - FUN_00971780 (index lookup by id) -> node; `FUN_00979d20(node)` = `[node+0x10]+0x10` = **frame_pos+16 = the PAYLOAD start**; SetFilePointer (@0x971B14 `CALL [0xA750E8]`); size = `FUN_00746550(node)` = the header size field (56); `FUN_0040e260(cursor, handle, 56)` = ReadFile 56 bytes into the cursor buffer, `cursor.limit = max(old, 56)`; `cursor.offset=0; cursor.flag=1`.
  - CRC gate: `EAX = FUN_006b22d0(node)` (the stored crc field); `TEST EAX,EAX; JZ` @0x971B4A/0x971B4C — **if the stored crc == 0 the comparison is SKIPPED**. Every record of 20002.vfs has crc field == 0 (S1 census, 1366/1366) -> the gate is inactive for this file (independently confirms the prior-evidence phrase "zeroed CRC fields / crc_gate_active=false" at instruction level).
  - id verification via FUN_00971650; then `if (cursor.limit < cursor.offset+8)` else `FUN_0040de60(8)` — **advance 8** (skipping the payload prefix {u32 class=20002, u32 record_id}); then `FUN_0070dc20(classObj, id, cursor, 2)`.
- **FUN_0070dc20(classObj, id, cursor, flags2)** (@0x70DC3F/0x70DC4B/0x70DC53): `instance = FUN_0070d990(classObj, id)`; `mode = FUN_0075d8d0(classObj, cursor)` (= constant 1); `FUN_00726900(instance, mode, cursor)`; on success register `FUN_0092b660({id, instance})` into the class instance map; else destroy.

### 5. GENERIC_PARSER_IDENTIFIED / ROUTED status
- The record parser chain (FUN_00726900 TLV loop + FUN_0075f660 + FUN_004129c0 + typed readers FUN_00412540/00412500/004099c0/...) is **GENERIC** property-parsing machinery shared by the ArkObjectClass family (the descriptor schema is per-class; FUN_0070c180 resolves per-class tables).
- **GENERIC_PARSER_IDENTIFIED = YES** (FUN_00726900 family).
- **20002_VFS_ROUTED_TO_GENERIC_PARSER = CONFIRMED** — the full chain from the class-ID 20002 registration (imm 0x4E22), through the class-object singleton (DAT_00ba5da8), the filename construction itoa(20002)+".vfs" (FUN_0070c3d0/FUN_0040e900), the ArkVFS02 open (FUN_00972df0), the index (FUN_00972ad0), the per-record seek+read (FUN_00971ad0) into FUN_00726900 is byte-pinned end-to-end (45/45 pins OK). No probabilistic or naming-only step is load-bearing.

### 6. IMPORTANT ROUTING CORRECTION vs the §B lead (LEADS_TO_REVERIFY, NOT TRUTH)
The §B lead named FUN_00959090 (0x58-byte array elements) as the candidate record-layout parser with "+0x2C/+0x30-class cursor reads". In-run verification shows that family belongs to a DIFFERENT file:
- Its open chain (FUN_0094dfc0) builds the filename from the string **"EnvironmentZones"** (FUN_0094b9e0 -> FUN_00958d90, string byte-proven) + "Data\Parameters\" + ".vfs" -> **EnvironmentZones.vfs**, with its own singletons (DAT_00ba8df4 reader / DAT_00ba8df8) and its own record loop (FUN_0094e1d0 -> FUN_0094bd30 -> FUN_00959090).
- Its element consumption profile (84 cursor bytes via 4-byte/12-byte reads) does not match 20002.vfs's 56-byte records at all.
- The 20002.vfs record parse is the class-property TLV machinery above. The contract's §8 warning ("a generic parser +0x30 hit is NOT a client-read claim without the routing edge") is hereby heeded: the FUN_00959090 lead is recorded as candidate context for a different file and plays no role in the 20002.vfs trace.

## Frames and bounds (S1 recap)
20002.vfs = 16-byte global header (magic `ArkVFS02`, base=0x80) + 1,366 records, each: 16-byte header {u32 id, u32 size=56, u32 ver=1, u32 crc=0} + 56-byte payload + alignment padding, stride 128, byte-exact EOF walk (executor implementation, cross-validated against the prior tool with FULL_BOUNDARY_AGREEMENT 1366/1366).
