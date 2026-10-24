# World data and placement — PE 2003 corpus

RUN_ID: PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3_20261024.

## Headline result

**TRANSFORM_SOURCE = NETWORK_RUNTIME_ONLY.**
**AUTHENTIC_INSTANCE_COUNT (offline) = 0** for both target models.
**PLACEMENT_VERDICT = MECHANISM_CONFIRMED_LOCATIONS_NOT_RECOVERABLE_FROM_LOCAL_2003_CORPUS.**

The spawn/transform mechanism is byte-confirmed (see
object-and-transform-pipeline.md); the historical locations are not in the
local 2003 corpus. Every negative below carries its real denominator
(a negative without a denominator is not a result).

## Local placement-source negatives (with denominators)

| Source | Denominator | Result |
|---|---|---|
| Install file census | 711 extracted files: 5 data containers (Models/Textures/Scripts/Volumes.ark + Terrain\50.bnt) + 650 sound files + data.ini (60 B export metadata) + 14 non-data files (FileList) | NO instance cache/seed/state file exists in the install |
| Volumes.ark | 831/831 members scanned (unaligned, LE+BE, plus [id+floats] pattern) | 0 id hits, 0 instance rosters; .bvi = model-LOCAL collision volumes only |
| Scripts.ark | 1936/1936 decoded DLOB corpus (R10 canon) + the two target definitions parsed to EOF | OBJECT_TYPE_DEFINITION only; zero positional floats (f32-window hits are ASCII mesh names); static placement records NOT_EXISTS byte-evidenced corpus-wide |
| Models.ark | 2492 members | local model payloads only; NIF-internal transforms are model-local (not world placement) |
| World-data containers | no Parameters dir; 24007.vfs ABSENT from the PE42 install (checked); no anchor tables | no world anchor exists locally |

## Mechanism (CONFIRMED)

Instance population is network-fed at runtime: frame type 0x06 chain
(dispatcher FUN_005bc5a0 → parser FUN_00528a40 → avatar spawn → scene attach).
The client's runtime instance roster (FUN_00503940 lookup / FUN_00502E80
insert) is populated only from network frames.

## Axis / units calibration status

- Wire/storage-level units and axes are answered: position = 3 × f32
  LITTLE-ENDIAN inside a BIG-ENDIAN envelope; storage multiplier ×100.0
  (0x42C80000) at scene attach; orientation = 3×3 row-major row-vector (v·M).
- World-axis/meters conversion is **UNANSWERABLE with local data**: there is
  no anchor (zero authentic instance values), so a meters conversion is
  FORBIDDEN, and world-coordinate claims about float-looking values are not
  made. Terrain is not decoded (two 50.bnt versions catalogued only), so no
  terrain-based anchor exists either.
- Cross-era caution (era discipline): 9.3.5-era world relations were used
  only as oracles; no cross-era ID/offset/VA/instance transfer.

## Consequences for reconstruction

- Authentic historical locations of 296445 / 218757 can be recovered only via
  a dynamic capture of a live session (open of the model for a real instance
  + its transform values) or via server-side data — see
  reconstruction-roadmap.md frontier items (a)/(c).
- Any placement of these models in the modern reconstruction viewer is
  modern/invented by definition and must not be labeled historical.
