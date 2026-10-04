# QC_REPORT — PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004

QC_SCOPE = SELF_CHECK_FUN_0070DC20_TABLE10_WRITER (targeted SELF_CHECK; no
independent-QC claim). MODE: STATIC-ONLY. The battery is
03_SCRIPTS/s5_qc_battery.py -> 01_RAW/S5_QC_BATTERY.json: **92 pin checks,
0 failures** (call-target recomputations, byte pins at exact VAs, branch
target recomputations, IAT-name resolutions, EXE hash).

## Gate-by-gate verdicts

### Q1 — base + EXE identity: PASS
- local HEAD == origin/master == actual remote master ==
  2bfb0f23c5b438eef7a8af47a963260d1df193b1 (rev-parse after fetch +
  ls-remote; re-verified again immediately before commit).
- EXE: 8,015,872 B / SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31
  (machine-verified at S1 and again at S5).

### Q2 — exact call target + function extent: PASS
- CALL @0x0070DDBD: bytes `E8 5E FE FF FF`, machine-computed target
  0x0070DC20 == pinned target.
- FUN_0070DC20 extent 0x0070DC20..0x0070DCF0: prologue pin
  `83 EC 10 53`; BOTH exits `C2 0C 00` (@0x0070DCE2 fail, @0x0070DCED
  success); next-function prologue `6A FF 68 28 C7 A0 00` @0x0070DCF0.

### Q3 — argument/receiver structural identity: PASS
- Caller argument construction @0x0070DDB3 (`6A 02 8D 44 24 18 50 57 8B CE`)
  machine-verified; FUN_0070DCF0 RET 4 (thiscall, 1 stack arg = receiver).
- Callee arg loads pinned: arg1 receiver `8B 5C 24 18` @0x0070DC24,
  arg2 cursor `8B 44 24 24` @0x0070DC46, arg3 mode `8B 54 24 28`
  @0x0070DCA0; this=factory `8B F1` @0x0070DC2D; RET 0xC == 3 args.

### Q4 — same-component identity: PASS
- Creation: FUN_0070DC20 -> FUN_0070D990 @0x0070DC3F; component vtable
  store 0x00A86F2C @0x007374DC; factory->class_obj+4 @0x0070D9A5; 12-entry
  table (+4 count @0x0070D9BB; vector ctor @0x0070D9C9 -> 0x00412C50).
- Insert: factory+0x0C map `8D 4E 0C` @0x0070DC71; key slot = receiver
  `89 5C 24 18` @0x0070DC74; value slot = class_obj `89 7C 24 1C`
  @0x0070DC78; CALL FUN_0092B660 @0x0070DC7C.
- Getter-side lookup of the SAME map: `8D 7E 0C` @0x0070E11E; CALL
  FUN_004D1430 @0x0070E124 (target machine-verified); node value
  `8B 68 14` @0x0070E131.
- SAMENESS: same factory singleton (ctor reads [0x00BA590C]), same map
  member (+0x0C), same receiver key, inserted value == written object.

### Q5 — attribute-id selection: PASS
- Schema: slot-6 SLOT_ADD args @0x0073758D (`50 6A 00 6A 00 6A 01 6A 06`),
  call @0x00737598 -> FUN_0070CBC0; ID = TAG+4 via `83 C1 04` @0x0070CBF6;
  traits singleton vtable store @0x00977A68 (0x00A9C670 into 0x00BA937C).
- Loop: tag read `0F B7 3C 08` @0x007269E7; slot getter CALL @0x00726A03
  -> FUN_0070C180 (in-range lea `C1 E0 04 03 81 88 00 00 00` @0x0070C1D3;
  default `B8 08 51 BA 00` @0x0070C1DF); kind gate `83 78 04 00`
  @0x00726A08; id load `8B 48 08` @0x00726A0E.

### Q6 — exact write destination: PASS
- table ptr `8B 55 40` @0x00726A11; dest lea `8D 0C 8A` @0x00726A14;
  arg pushes `51 56` + `8B C8` @0x00726A17-19; dispatch CALL @0x00726A1B
  -> 0x0075F660 (machine-computed; the executor's hand target 0x0075F65C
  was WRONG and was corrected by the battery — disclosed deviation).
- Dispatcher: traits load `8B 08` @0x0075F662; vtable slot 5 `8B 40 14`
  @0x0075F676; virtual call `FF D0` @0x0075F67B; RET 8 @0x0075F684.
- Traits vtable slot 5 dword @0x00A9C684 == 0x009777F0 (and slot 1 ==
  0x009777E0) machine-read from .rdata.
- Writer: READ `8B 04 10` @0x00977807; STORE `89 02` @0x00977810; advance
  CALL -> FUN_0040DE60 @0x00977812; fail-path zero store
  `C7 00 00 00 00 00` @0x0097781E; RET 8 @0x00977817.

### Q7 — table[10] identity (independently recomputed BOTH sides): PASS
- WRITER SIDE (from the schema-writer path, NOT from the getter claim):
  tag 6 imm `6A 06` @0x00737594; id = tag+4 (`83 C1 04` @0x0070CBF6) = 10;
  dest = [class_obj+0x40] + 10*4 (lea scale pinned @0x00726A14); store
  @0x00977810.
- GETTER SIDE (R1 canon chain, independently re-pinned): slot getter CALL
  @0x004C5523 -> FUN_0070C180; id load `8B 40 08` @0x004C5539; table load
  `8B 4E 40` @0x004C553C; lea `8D 0C 81` @0x004C553F; element accessor
  CALL @0x004C5542 -> FUN_004926E0; value load `8B 00` @0x004C554E;
  fallback CALL @0x004C5549 -> FUN_00977780.
- MEETING POINT: both sides compute the identical storage expression
  [class_obj+0x40] + id*4 with id from the same schema descriptor (slot 6).
  The writer-side id-10 derivation never consulted the getter-side claim.

### Q8 — source-operand boundary correctly stopped: PASS
- The immediate source operand is pinned: u32 at [cursor.base+cursor.pos]
  READ @0x00977807 (RECORD_FIELD through the record cursor).
- The battery contains NO stream/VFS/file/network provenance instruments;
  the factory+0x84 stream setter was NOT traced; ULTIMATE_VALUE_SOURCE
  stays UNKNOWN (contract stop honored).

### Q9 — control discrimination: PASS
- Same loop body for all tags; id = tag+4; tag 2 -> &table[6], tag 6 ->
  &table[10], tag 7 -> &table[11] (schema pins @0x0073758D/@0x007375A2
  + pattern-search-unique tag-2 block, S5 Q9). Same traits writer
  (kind 1 int) for tags 2 and 6 — identity discrimination isolated from
  the value machinery.

### Q10 — function-budget hard pre-check: PASS
- FUNCTION_LEDGER.csv complete: 8 entries, each with count_before recorded
  BEFORE the detailed analysis; every entry entered with count_before < 8;
  count never exceeded 8; NO 9th detailed decode performed.
- NEW_FUNCTION_COUNT = 8 (== MAX, not >). Two canon functions
  (FUN_009777F0, FUN_0070CBC0) were COUNTED conservatively because this
  run derived new semantic details beyond their canon pins; all other
  prior-canon functions were narrow reverifications only (pin-level; no new
  semantic claims) and are listed as such in INPUT_IDENTITIES.md.

### Q11 — forbidden-scope census: PASS (all NO)
factory+0x84 setter trace NO; templates.vfs opened NO; RECORD_A NO;
candidate-B delegate decode NO; FUN_00843340 NO; model 194013 NO; NIF NO;
world XYZ NO; client run NO; network trace NO. (The battery's Q11 census
is enforced by construction: the instruments contain no such code paths.)

### Q12 — preserved canonical states: PASS
GETTER_RESULT_TO_LOOKUP_KEY=PRESERVED_CONFIRMED; CLASS_SELECTOR_20006 /
PROPERTY_TAG_6 / audited normal path PRESERVED (not reopened);
IMMEDIATE_VALUE_STORAGE=PER_RECEIVER_COMPONENT_VALUE_TABLE (preserved;
now with the immediate writer identified);
ULTIMATE_VALUE_SOURCE=UNKNOWN; FILE_DERIVED_VALUE_EXCLUDED=NO;
RECORD_A_RELATION=NOT_ESTABLISHED; DEFAULT_CREATION_PATH_INITIAL_VALUE=0;
C1=PRESERVED_CLOSED; C2=PRESERVED_CLOSED;
S1_STATIC_MECHANISM=PRESERVED_CONFIRMED; GP1/GP2/GP3 scoped wording
preserved (this run's claims are phrased within those scopes).

## Battery error-detection record (why the battery is not decorative)

During the run the battery detected and forced correction of:
1. guard-pair rel32 hand-computation slip (0x0040D440/0x0040D450 ->
   actual 0x00413440/0x00413450);
2. a 4-byte tokenization drift inside the 320-byte FUN_00726900 window that
   displaced the loop call-site VAs (the "0x0040DE5C/0x0070C17C targets"
   were artifacts of reading call bytes at wrong VAs — the direct-VA probe
   resolved them to padding/previous-function tails and the TRUE calls at
   0x007269EF/0x00726A03/0x00726A1B);
3. the traits-dispatch target hand-slip (0x0075F65C -> 0x0075F660);
4. several pin-VA off-by-1/2/4 slips (schema call @0x00737598, tag imm
   @0x00737594, ctor vtable @0x007374DC, slotget default @0x0070C1DF,
   cursor pins @0x0040DE64/@0x0040DE6F, lookup lea @0x0070E11E,
   dispatcher pins @0x0075F6E5/@0x0075F6E8, d990 push @0x0070DA41);
5. an 8-byte-stride import-walk bug (fixed to 4-byte thunks; KERNEL32
   FirstThunk base 0x675060 resolved the guard pair to
   EnterCriticalSection/LeaveCriticalSection, hints 152/593).
All corrections are visible in the S2..S5 JSON records; the FINAL battery
is 92/92 PASS against the corrected pin set.

QC_RESULT = PASS (92/92 machine pins; 12/12 gates PASS; self-check scope).
