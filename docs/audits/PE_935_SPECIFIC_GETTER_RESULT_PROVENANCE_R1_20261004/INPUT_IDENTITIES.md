# INPUT_IDENTITIES — PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004

## Corpus

| Input | Path | Size (bytes) | SHA256 | Role |
|---|---|---|---|---|
| Entropia.exe (pinned) | D:\Eudoria_Reconstruction\pcg_install\Entropia.exe | 8,015,872 | E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 | the ONLY binary analyzed; every claim is a byte read from it; identity re-verified at run start (01_RAW/S1_CHAIN_WINDOWS.json identity block) and in the final QC battery (01_RAW/S11_QC_BATTERY.json exe_identity) |

EXE_IDENTITY = PASS (size + SHA256 both match the dispatch pin; the EXE is
PCG 9.3.5 era; no CROSS_BUILD_ORACLE semantics were imported).

## Base / repo

- BASE_SHA (dispatch pin, re-verified before any write): 53c57bfacaabe1d6cd1b5c9d16965f8394c1e61a
- At run start: local HEAD == origin/master == 53c57bfa... (git rev-parse,
  recorded in the session log); the actual-remote check is re-executed at
  persistence time (see FINAL_REPORT.md PERSISTENCE section).
- Pre-existing untracked paths at start (FOREIGN — not touched, not staged,
  not absorbed): docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/,
  docs/audits/PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003/,
  docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/,
  docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/,
  docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/,
  experiments/.
- Output root docs/audits/PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004/
  verified NON-EXISTENT at start (Test-Path False) and created fresh by this run.

## Mandatory predecessor packages (READ-ONLY; preserved, not modified)

| Package | Status this run |
|---|---|
| PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004 | read (FINAL_REPORT, PLACEMENT_CONSUMER_EDGE, PARSER_CHAIN refs); used for: registry root DAT_00BA1824, singleton FUN_0043A550, lookup FUN_0072F880/FUN_0072F580 semantics, node layout (key@+0x10, value@+0x14), RECORD_A/RECORD_B, the C2-corrected layered identity |
| ..._C1_REPORT_QC_CORRECTION_R1_20261004 | read; used for: CLASS_SELECTOR 0x4E26 vs PROPERTY_TAG 6 separation, instruction-start corrections |
| ..._C1_C1_STORE_IDENTITY_QC_R1_20261004 | read; used for: parser store-instruction oracle (FUN_00730C90 store sites), the NEXT_EXPERIMENT wording this run executes |
| PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002 (via its canon quotes in the packages above) | corroboration only: the descriptor grammar {+0 traits, +4 kind, +8 value/id, +0xC flags}, FUN_00977A50/0x00BA937C/0x00A9C670 as ArkRTTraitsInt, the tag+4 idiom @0x70CBF6 — all independently re-derived from bytes this run |

templates.vfs was NOT opened, re-measured, or used as a physical-record
bridge this run (no physical-record claim was promoted; the bridge remains
NOT_ESTABLISHED — see PRODUCER_PROVIDER_CHAIN.md).

## Instruments (all in 03_SCRIPTS/, all READ-ONLY vs originals)

| Script | Output | Purpose |
|---|---|---|
| s1_chain_windows.py | 01_RAW/S1_CHAIN_WINDOWS.json | identity + chain windows + caller censuses |
| s2_producer_windows.py | 01_RAW/S2_PRODUCER_WINDOWS.json | producer-side windows (contained the 0x004C1430 target slip — corrected in s3) |
| s3_corrected_windows.py | 01_RAW/S3_CORRECTED_WINDOWS.json | corrected windows + machine call-site verification table |
| s4_selector_and_statics.py | 01_RAW/S4_SELECTOR_AND_STATICS.json | selector machinery + statics windows |
| s5_creator_decode.py | 01_RAW/S5_CREATOR_DECODE.json | creator + writer censuses for the statics |
| s6_factory_init_and_traits_writers.py | 01_RAW/S6_FACTORY_AND_TRAITS.json | factory init + traits writer scans |
| s7_factory_ctor_and_creator.py | 01_RAW/S7_FACTORY_CTOR_AND_CREATOR.json | factory ctor, slot builder, class_obj creator windows |
| s8_slotadd_verify.py | 01_RAW/S8_SLOTADD_VERIFY.json | machine verification of SLOT_ADD/traits/init/creator call targets |
| s9_slot_layout.py | 01_RAW/S9_SLOT_LAYOUT.json | slot payload layout windows (FUN_0075F5C0/F6D0, appender, traits) |
| s10_traits_vtables.py | 01_RAW/S10_TRAITS_VTABLES.json | vtable resolution (0x00A9C670 slots; 0x00A799E4 inert) |
| s11_qc_battery.py | 01_RAW/S11_QC_BATTERY.json | final SELF_CHECK battery: 45 call checks, 33 instruction pins, JE-target arithmetic |

All scripts set sys.dont_write_bytecode=True, read the pinned EXE through a
section-table PE mapper (no offset==RVA assumption), and write only into
this package's 01_RAW/.

## In-run deviations (honest record)

1. Three hand-computed rel32 targets were WRONG and were caught by the
   machine-verification battery: 0x004C1430 → 0x004D1430 (mapfind),
   0x0073C8D0 → 0x0073C870 (selector dispatch), 0x0073E100 → 0x0070E100
   (get-or-create). All downstream analysis used the machine-verified
   targets; the s2 window at 0x004C1430 belongs to an unrelated
   destructor-shaped function and is retained in the raw record as the
   evidence of the slip.
2. Five instruction-pin VAs were transcription slips (0x0070DA5→0x0070D9A5,
   0x0070DB3A→0x0070DA36, 0x0070DB42→0x0070DA3E, 0x00977A6A→0x00977A68,
   0x0070DD25→0x0070DD28, plus the control pins 0x737539/0x737563/0x73758D)
   — all caught by the battery and corrected; the final battery is 0-FAIL.
3. One filename typo (PE_935_SPECTER_RESULT_DATAFLOW.md) was created and
   immediately renamed to GETTER_RESULT_DATAFLOW.md inside the package.
None of these deviations affected any semantic verdict; all are recorded
here and in QC_REPORT.md.
