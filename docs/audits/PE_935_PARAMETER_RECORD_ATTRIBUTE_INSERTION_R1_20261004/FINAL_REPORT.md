# FINAL_REPORT — PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004

RUN_ID: PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004
RUN_CLASS: LOAD_BEARING | MODE: STATIC-ONLY (client never launched; raw byte reads +
manual x86 decode only; no Ghidra this run) | Executor: pe-reconstruction
(PE-MASTER bounded worker contract; NO_NESTED_TASKS).

## THE ONE QUESTION AND THE ANSWER

Can ONE concrete physical record from ONE chosen Data\Parameters\*.vfs in PCG 9.3.5 be
carried through PHYSICAL RECORD BYTES → CLIENT PARSER → REAL KEY + REAL VALUE →
IDENTIFIABLE RECEIVER/CONTAINER → ATTRIBUTE INSERTION/UPDATE — and, only if that exists,
READ OF THAT SAME VALUE by the placement-builder path?

**YES for the first half — CONFIRMED, byte-pinned end-to-end for one concrete record:**
templates.vfs record id2=16083 (file offset 560,212) is parsed by the client loader
(reader FUN_0072FA30 → per-record read FUN_00971AD0 → parse FUN_00730C90) into the
real key id2=16083 and the real value {B=0, A=410620, C=0, D_f32=0.49950098991394043,
list1=[], list2=[], f11=0}, which is INSERTED as the pair {key@node+0x10,
value@node+0x14} into the RB-tree registry rooted at DAT_00BA1824 (lazy singleton
FUN_0043A550; insert FUN_0072F8D0 → node alloc FUN_0072F7F0 (0x44 B) → pair init
FUN_0072F740 → canonical copy FUN_005670A0).
PARSER_TO_RUNTIME_VALUE_SEAM = CONFIRMED. (S1 reached. This does NOT mean
PLACEMENT_CARRIER_CONFIRMED.)

**The placement-consumer half is STRONGLY_SUPPORTED, not CONFIRMED:**
- RECORD_A's object IS read back with a byte-pinned STATIC key (PUSH 0x3ED3 = 16083 =
  RECORD_A's id2) inside a placement-record constructor: FUN_005B6370 (attribute-flag
  gates) → FUN_005B5F90 → same registry FUN_0043A550 → same lookup FUN_0072F580
  (key 16083) → FUN_005670A0 full-field copy (id2, B, A, C, D_f32, list1, list2, f11
  — every field RECORD_A's parse wrote). Lookup identity: same registry root, same key
  domain, same key VALUE, same lookup function. But FUN_005B5F90 is a SIBLING
  constructor — NOT the contract's named family ("FUN_00567770 via FUN_00567C50").
- The named builder FUN_00567770 itself reads the SAME registry (via its deriver
  FUN_004C5580 @0x005678BA → FUN_004C5480: the entity's 0x4E26-property id2 →
  FUN_0072F880 lookup-with-copy → full value copy into the builder's local) — with a
  RUNTIME key whose value identity for RECORD_A is NOT statically provable.
- The named driver FUN_00567C50's own tree (→ FUN_00567B40 queue push → FUN_00567170)
  reads registry objects with byte-pinned STATIC keys {15321, 15322, 15323, 14912,
  14919} — a record set DISJOINT from RECORD_A's key.
- Therefore PLACEMENT_CONSUMER_EDGE = STRONGLY_SUPPORTED;
  PHYSICAL_RECORD_TO_PLACEMENT_ATTRIBUTE = NOT_ESTABLISHED. No S2 claimed.

## Negative/control record

RECORD_B = record id2=4508 (offset 96,496): same grammar/insertion; its established
consumer is the model-request EMITTER (FUN_006C3F50 — E3, re-verified) — a different
receiver path; NO static 4508 key exists (all 3 imm32 hits are ESP/struct
displacements; 0 PUSH sites). The control discriminates inserted-vs-statically-looked-up.

## TERMINAL FIELDS (exact)

```text
BASE_SHA = 780cc4e442ec2bef7e4e0880b9ffee22a39e302c
HEAD_SHA = (this publication commit; discover: git log -1 -- docs/audits/PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004)
PARAMETER_INVENTORY = COMPLETE
TOTAL_PARAMETER_FILES = 27
TOTAL_VFS_FILES = 27
NUMERIC_VFS_COUNT = 19
20006_vfs = ABSENT
SELECTED_FILE = Data\Parameters\templates.vfs
SELECTED_FILE_REASON = strongest code-side filename->reader->parser linkage among the
  contract-allowed named VFS files (byte-pinned "Parameters\templates.vfs" string
  @0x00A86D30 + PUSH @0x0072FAAC; FUN_00730C90/FUN_0072F8D0 each have EXACTLY 1 call
  site = this reader loop); prior tracked BRIDGE R1 corroboration reproduced by an
  independent walk; non-circular (see SELECTED_FILE.md)
DETAILED_VFS_COUNT = 1
DETAILED_RECORD_COUNT = 2
NEW_FUNCTION_COUNT = 11
RECORD_BOUNDARY = CONFIRMED
RECORD_KEY_VALUE_DECODE = CONFIRMED
RECEIVER_IDENTITY = CONFIRMED
CONTAINER_ROLE = DEFINITION_REGISTRY
PARSER_TO_RUNTIME_VALUE_SEAM = CONFIRMED
PLACEMENT_CONSUMER_EDGE = STRONGLY_SUPPORTED
PHYSICAL_RECORD_TO_PLACEMENT_ATTRIBUTE = NOT_ESTABLISHED
WORLD_INSTANCE_SEMANTIC = NOT_ESTABLISHED
MODEL_JOIN_EXECUTED = NO
POSITION_RECOVERY_GOAL = OUT_OF_SCOPE
WORLD_XYZ_RECOVERED = NO
NETWORK_PLACEMENT_PROVEN = NO
0xB9_POSITION_DESERIALIZER = NO_FOR_AUDITED_HISTORICAL_PATH
F3_EXECUTED = NO
F4_EXECUTED = NO
F1_F2_ORACLE_MODIFIED = NO
FIRST_MISSING_EDGE = INSERTED_VALUE_TO_PLACEMENT_CONSUMER
CANONICAL_GATE_EFFECT = NONE
NEXT_RUN_EXECUTED = NO
```

## Forbidden-overclaim census (contract QC-11)

WORLD_XYZ_RECOVERED=NO; MODEL_JOIN_EXECUTED=NO (A=410620 recorded as a decoded value
only; no Models.bnt join attempted); NETWORK_PLACEMENT_PROVEN=NO;
STATIC_INSTANCE_CONFIRMED=NOT_ESTABLISHED; no ALL_20XXX/ALL_24XXX generalization is
made anywhere (decode coverage was intentionally narrow: 1 file, 2 records);
SELECTED_RECORD_TO_ATTRIBUTE_INSERTION is ESTABLISHED (for RECORD_A); no movable→static
transfer; 0xB9 untouched; the templates registry is a DEFINITION_REGISTRY — reaching
it is NOT placement recovery.

## FIRST_MISSING_EDGE + the ONE recommended next experiment (designed, NOT executed)

FIRST_MISSING_EDGE = INSERTED_VALUE_TO_PLACEMENT_CONSUMER, precisely: the provenance
of the RUNTIME KEY at the named builder's lookup (FUN_004C5480's 0x4E26/20006-family
property value → FUN_0072F880). Recommended experiment: decode the WRITERS of the
0x4E26-property value (the property-write counterparts of the FUN_00703B80/FUN_0042EAD0
machinery) and determine whether that id2 is ever fed from a physical record — if yes,
the named-family chain closes to CONFIRMED; if network/runtime-only, the named family's
registry read is confirmed-as-mechanism but never record-keyed statically.
(Adjacent RAW_OCCURRENCE_ONLY lead, no role claimed: imm32 0x3ED3/0x3ED2 in the
property idiom at 0x0050F383/0x0050F2F3, function NOT decoded this run.)

## Evidence index

- `PARAMETER_FILE_INVENTORY.csv` — complete Phase A inventory (27 files, SHA256 each).
- `01_RAW/S0_IDENTITY_AND_INVENTORY.json` — identity verifications + counts.
- `01_RAW/S2_EXE_WINDOWS.json` — 25 raw EXE windows + 22-target rel32 caller censuses +
  PUSH-imm32 scans.
- `01_RAW/S3_MORE_WINDOWS.json` — 12 further windows (driver, queue push, property
  machinery, node creator, validity check, constructor bodies).
- `01_RAW/S4_RECORD_ANCHOR_AND_SCANS.json` — RECORD_A/RECORD_B machine-measured
  anchors (offsets, payload hex, SHA256s, re-parsed fields, boundary checks) +
  all-encodings imm32 scans + the reader string verification.
- `01_RAW/S5_QC_CHECKS.json` — the 8 QC gates, all PASS.
- `SELECTED_FILE.md`, `RECORD_A.md`, `RECORD_B.md`, `PARSER_CHAIN.md`,
  `RECEIVER_INSERTION_CHAIN.md`, `PLACEMENT_CONSUMER_EDGE.md`, `QC_REPORT.md`,
  `INPUT_IDENTITIES.md`, `HANDOFF.md`.
- `03_SCRIPTS/s0..s5` — the bounded instruments (all read-only vs originals;
  sys.dont_write_bytecode; PE mapper reads the section table).

## Honest boundaries

1. The verdicts are STATIC-ONLY (no runtime observation of any lookup occurring).
2. FUN_0050A690's ECX provenance (FUN_005B5F90's post-registration consumer of the
   local template copy) is UNRESOLVED (stack-state-dependent; non-load-bearing).
3. The header crc field's checking semantics were not investigated.
4. The parse-layout ambiguity in the prior E1 wording was resolved by this run's own
   byte decode + getter/anchor cross-checks (documented in PARSER_CHAIN.md).
5. RESUMED RUN: the previous session's final return arrived empty at PE-MASTER; this
   session continued the partial disk state per the parent's resume order; Phase A was
   re-verified, not redone.
