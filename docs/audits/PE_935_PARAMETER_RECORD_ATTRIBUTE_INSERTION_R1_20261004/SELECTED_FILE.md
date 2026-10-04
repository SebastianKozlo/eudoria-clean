# SELECTED_FILE — PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004

## SELECTED_FILE

`Data\Parameters\templates.vfs` (physical: `D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs`,
560,788 B, SHA256 BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77).

## Selection space (contract-constrained)

The contract's OUT_OF_SCOPE list excludes detailed analysis of "all 20xxx VFS; all 24xxx VFS",
so the selection space is the 8 NAMED Data\Parameters files:
AmbientAudioZones.vfs, EnvironmentZones.vfs, hierarchy.vfs, materials.vfs, sids.vfs,
templates.vfs, textures.vfs, videos.vfs.

## SELECTION_REASON (evidence-driven, ranked by the contract's own criteria)

1. **Strongest exact code-side linkage between the file identity and the known
   Data\Parameters loader/parser path**: the reader FUN_0072FA30 builds the access path
   from the .rdata string `"Parameters\templates.vfs"` @VA 0x00A86D30 (raw bytes verified
   this run; PUSH of the string VA at 0x0072FAAC), opens the file, and walks the file's
   own id index; the parse target FUN_00730C90 has EXACTLY ONE call site in the whole
   binary (0x0072FBA5, inside this reader loop — this run's rel32 census), and the
   registry insert FUN_0072F8D0 likewise has EXACTLY ONE call site (0x0072FBE5, the same
   loop). No other named VFS file has any established filename→reader→parser linkage in
   the pinned corpus.
2. **Strongest direct filename/open/parser provenance**: the filename string is the
   byte-pinned link between the physical file name and the reader (verified: 24-char
   string + NUL at 0x00A86D30; PUSH @0x0072FAAC; path-build call FUN_00401E70 @0x0072FAB7).
3. **Prior accepted-package corroboration (independent, non-circular)**: the tracked
   BRIDGE R1 package byte-pinned the same chain (E1) and its C1 census walked 5,438
   records to exact EOF — reproduced this run by an independent decoder (below).

## ALTERNATIVES_NOT_SELECTED

- `sids.vfs`, `materials.vfs`, `hierarchy.vfs`, `EnvironmentZones.vfs`,
  `AmbientAudioZones.vfs`, `textures.vfs`, `videos.vfs`: no established
  filename→reader→parser linkage in the pinned 9.3.5 evidence base (the older skill notes
  about sids/EnvironmentZones contents belong to a different corpus era and are not
  code-side parser proof for PCG 9.3.5). Selecting any of them would violate the
  "defensible parser/open linkage" requirement.
- The 19 numeric VFS files (18× 20xxx + 24007): excluded by the contract's explicit
  OUT_OF_SCOPE ("all 20xxx VFS; all 24xxx VFS"); inventory-verified only.
- `SELECTED_FILE=NONE` was considered and rejected: a defensible candidate exists (above).

## WHY_SELECTION_IS_NON_CIRCULAR

- The selection criterion (byte-pinned filename→reader→parser linkage) is established by
  PRIOR TRACKED PACKAGES (BRIDGE R1 E1) and re-verified this run from the pinned EXE
  bytes with this run's own PE mapper — it does not depend on this run's decoder choices.
- This run's own independent walk of the physical file (5,438 records, EOF-exact,
  framing: 16-byte header {id,size,ver,crc} + size-byte payload + 36-byte block
  alignment; payload id2 echoes header id in 5,438/5,438 records) reproduces the prior
  census numbers without using the client binary at all.
- The record choice (RECORD_A = id2 16083) is driven by CODE-side evidence only:
  the byte-pinned hardcoded key PUSH 0x3ED3 @0x005B6597 → CALL FUN_005B5F90
  (a placement-record constructor that looks the key up in the registry this run
  proves the record populates). The record's existence at id2=16083 in the file was then
  verified physically — the code evidence precedes and is independent of the record bytes.

## After-selection discipline

No switch of the selected file was made at any point. Detailed RE was confined to
templates.vfs and to exactly two of its records (RECORD_A id2=16083, RECORD_B id2=4508).
