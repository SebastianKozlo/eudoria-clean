# INPUT_IDENTITIES — PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004

## Baseline identity (re-verified twice: preflight + pre-commit)

| Item | Value | Verification |
|---|---|---|
| local HEAD | 2bfb0f23c5b438eef7a8af47a963260d1df193b1 | `git rev-parse HEAD` |
| local origin/master | 2bfb0f23c5b438eef7a8af47a963260d1df193b1 | `git rev-parse origin/master` after `git fetch` |
| actual remote master | 2bfb0f23c5b438eef7a8af47a963260d1df193b1 | `git ls-remote origin master` |
| BASE_SHA (contract pin) | 2bfb0f23c5b438eef7a8af47a963260d1df193b1 | MATCH — no BASE_DIVERGENCE |
| tracked dirty paths | NONE | `git status --porcelain` shows only the 5 foreign untracked PE_935_* dirs + experiments/ + this new package |
| foreign untracked (untouched) | docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001, docs/audits/PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003, docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914, docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930, docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928, experiments/ | read-only; not staged; not in manifest |

## Pinned EXE identity (re-verified by S1 and again by S5)

| Item | Value |
|---|---|
| Path | D:\Eudoria_Reconstruction\pcg_install\Entropia.exe |
| Size | 8,015,872 bytes (matches contract pin) |
| SHA256 | E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (matches contract pin) |
| EXE_IDENTITY | PASS |
| Image base | 0x00400000 (S1) |
| Sections | .text vaddr 0x1000 rawsize 0x674000 rawptr 0x1000; .rdata vaddr 0x675000 rawsize 0xF7000 rawptr 0x675000; .data vaddr 0x76C000 rawsize 0x34000 rawptr 0x76C000 (S1) |

## Canonical predecessor packages (READ as needed; historical — READ-ONLY)

| Package | Publication commit (last commit touching path) | Role in this run |
|---|---|---|
| PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004 | 25335a28ee61fc2a8c7763f41552df85af45d067 | canonical getter chain + candidate-A shell (FUN_0070DCF0 call @0x0070DDBD); preserved states |
| PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_C1_REPORT_SCOPE_CORRECTION_R1_20261004 | 2bfb0f23c5b438eef7a8af47a963260d1df193b1 (= BASE_SHA) | GP1/GP2/GP3 scoped wording + budget-overrun discipline this run enforces |
| PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004 | 97bdf959cb742490a0e974bddf5a2dd25f93f5f7 | templates.vfs parser canon (FUN_00971AD0 reader family) — cited only; NOT opened this run |
| PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002 | 743f9fac2dd5c9e94eaba074b46903b4d3686b46 | FUN_009777F0 canon decode (READ @0x00977807, STORE @0x00977810) + traits vtable 0x00A9C670 slot 5 identification |

## Canonical facts this run re-verifies (narrow reverification, no new claims)

- FUN_0070DCF0 frame (R1): stream gate factory+0x84, cursor ctor
  FUN_0040E160(&cursor,0x80,1), record reader FUN_00971AD0 @0x0070DD75,
  advance FUN_00971650, framing skip FUN_0040DE60(&cursor,8) @0x0070DDA8,
  the call FUN_0070DC20 @0x0070DDBD with (receiver, &cursor, 2), RET 4.
- FUN_0070D990 (R1): default creator; writer idiom @0x0070DA36/
  0x0070DA3E/@0x0070DA42 (corrected encodings: `8B 44 19 08`, `8D 04 82`,
  PUSH @0x0070DA41); factory->class_obj+4 @0x0070D9A5; 12-entry table.
- FUN_0070C180 (R1): slot getter, array at factory+0x88, default
  0x00BA5108 (@0x0070C1DF), fixed-member cases factory+0xD8/+0xE8/+0xF8/
  +0x108 (tags 0x8000-0x8003).
- FUN_0040DE60 (C1 canon): cursor advance (pos += delta @0x0040DE64,
  sticky flag clear @0x0040DE6F, RET 4).
- FUN_0092B660 (R1): RB-tree insert, key @node+0x10, value @node+0x14.
- FUN_0070E100 (R1): the factory+0x0C per-receiver cache lookup.
- FUN_004D1430 (R1): generic mapfind.
- FUN_00977A50 (20002 canon): int-traits lazy singleton 0x00BA937C with
  vtable store `C7 05 7C 93 BA 00 70 C6 A9 00` @0x00977A68.
- FUN_007374F0 (R1): 8-slot schema init; slot-6 SLOT_ADD call site
  @0x0073758D/@0x00737598.
- FUN_007374C0 (R1): component ctor; vtable 0x00A86F2C store
  @0x007374DC (pin VA corrected from the R1 prose's unnumbered claim).
- Audited getter chain (R1): slot getter call @0x004C5523, id load
  @0x004C5539, table load @0x004C553C, lea @0x004C553F, element accessor
  FUN_004926E0 @0x004C5542, value load `8B 00` @0x004C554E, fallback
  helper FUN_00977780 @0x004C5549.

## Instrument identities

| Script | Output | Purpose |
|---|---|---|
| 03_SCRIPTS/s1_callsite_extent.py | 01_RAW/S1_CALLSITE_AND_EXTENT.json | EXE identity, call-site machine verification, FUN_0070DCF0 + FUN_0070DC20 windows, E8 xref census |
| 03_SCRIPTS/s2_decode_support.py | 01_RAW/S2_DECODE_SUPPORT.json | subordinate windows, caller-2 context, guard surface windows, 47 call/byte/branch pins |
| 03_SCRIPTS/s3_apply_loop_deep.py | 01_RAW/S3_APPLY_LOOP_DEEP.json | full FUN_00726900 window, FUN_0075F65C-region window, traits vtable dwords, canon windows, first battery round |
| 03_SCRIPTS/s4_writer_evidence.py | 01_RAW/S4_WRITER_EVIDENCE.json | FUN_009777F0/SLOT_ADD/insert/lookup/getter windows + corrected battery round |
| 03_SCRIPTS/s5_qc_battery.py | 01_RAW/S5_QC_BATTERY.json | final 92-pin battery, 12 QC gates, KERNEL32 IAT resolution |

All scripts are READ-ONLY against the EXE (byte reads; no writes anywhere);
no proprietary binaries/corpora are included in this package (bounded byte
windows and pin records only).
