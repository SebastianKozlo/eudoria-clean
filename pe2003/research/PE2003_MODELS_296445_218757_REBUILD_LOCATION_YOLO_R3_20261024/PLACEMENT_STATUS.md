# PLACEMENT_STATUS — historical placement of models 296445 / 218757

RUN_ID: PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3_20261024.
Detailed negatives: `docs/world-data-and-placement.md` (repo root).

## Verdict (both models)

- TRANSFORM_SOURCE = **NETWORK_RUNTIME_ONLY**
- AUTHENTIC_INSTANCE_COUNT (offline) = **0**
- PLACEMENT_VERDICT = **MECHANISM_CONFIRMED_LOCATIONS_NOT_RECOVERABLE_FROM_LOCAL_2003_CORPUS**

The spawn/transform mechanism is CONFIRMED at byte level (frame 0x06 chain);
the authentic historical locations are NOT recoverable from the local 2003
corpus. This is a mechanism result plus an exhaustive local negative — it is
NOT a "placement reconstructed" claim, and no such claim exists anywhere in
the package (QC sweep QW-05).

## Decisive negatives (denominators)

- Install census (711 files): 5 data containers + 650 sounds + data.ini
  (60 B) + 14 non-data files — no instance cache/seed/state file.
- Volumes.ark: 831/831 members scanned (LE+BE unaligned + [id+floats]) —
  0 hits; .bvi = model-LOCAL collision volumes.
- Scripts: 1936/1936 decoded corpus — static placement records NOT_EXISTS
  corpus-wide (R10 canon); both target definitions are OBJECT_TYPE_DEFINITION
  with zero positional floats.
- Models.ark: 2492 members — local payloads only; NIF-internal transforms are
  model-local.
- No world anchor: no Parameters dir, 24007.vfs ABSENT, no anchor tables,
  terrain not decoded → world-axis/meters conversion FORBIDDEN (no anchor).

## What COULD recover locations (frontier)

- Dynamic capture of a live session: open of the model for a real instance +
  its transform values (FRONTIER item a — FIRST_MISSING_EDGE; item b — live
  orientation source).
- Server-side instance data model (FRONTIER item c).

Any placement of these models in a modern viewer is modern/invented by
definition and must not be labeled historical.
