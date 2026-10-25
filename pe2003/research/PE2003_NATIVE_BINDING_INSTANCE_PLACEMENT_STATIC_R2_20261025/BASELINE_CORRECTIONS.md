# BASELINE CORRECTIONS — R1 dispositions carried into R2 closing

RUN_ID: PE2003_NATIVE_BINDING_INSTANCE_PLACEMENT_STATIC_R2_20261025 | Authoring: 2026-10-25T11:18:13Z
Policy: frozen R1 is NOT modified; corrections are additive; per governing postaudit SP-A01..09 (REPORT.md SHA256 1946EABA..., re-verified MATCH).

## A. Accepted R1 measurements (value preserved)

- NIF model data, DLOB getter definitions, headers, EXTN tables and raw literal counts of R1 retain value (postaudit preamble; SP-A03: literal census reproduced by the postaudit's own all-offset census).
- 1936-file scanned corpus after 12-byte u32LE = exact literal census (not a full reference graph) — used as such by J02 (bounded negative with explicit residual).
- R1 attach-chain leads (ext 30298/33521, EXTN#23) — independently re-derived TRUE by B02a (lead-A/lead-B CONFIRMED with own decoder).

## B. Retracted / corrected R1 overclaims

1. **"missing .obj for 2202/768/382"** → **FILE_CLASS_PRESENT** (namespace error: ext ids are METHOD ids inside owner class files; raw members byte-identical in Scripts.ark; decoded counterparts in the pinned 1936-row corpus). [B01_OWNER_CLASSIFICATION.csv; QC VC-19/20/21/22]
2. **R1-V8 "EBX=param_1 (obj 0xFC)"** in FUN_005068f0 owner-chain → at the owner-chain sites EBX = arg2 = the SceneInstancePair; the 0xFC object arrives via arg1 as pointer-to-slot (deref @0x506cee). [J01b corrections_to_prior]
3. **R1 "FUN_004fe250→FUN_00503b90" as a FUN_00506780 caller** → NOT a caller (REF census: exactly 2 callers: 0x505870, 0x505aa0). [J01b corrections_to_prior]
4. **R1 "def→getter 51F6E0(id=...)"** phrasing → MECHANISM HYPOTHESIS at J02 static level, not a byte-verified edge (resource-open family byte-verified as mechanism; connecting edge not statically reachable — no literal anchors). [J02 native_qualification]
5. **R1 SELF_POSITIONING_FALSIFIED / ZERO_POSITIONAL_CONSTANTS / branches_exhausted / NETWORK_ONLY** → not carried (postaudit SP-A01/02/05 dispositions; standing is SOURCE_UNKNOWN / INSTANCE-LEVEL join STILL_AMBIGUOUS / LOCAL_SOURCE_EXHAUSTED=NO).

## C. In-run premise corrections (see CORRECTION_LEDGER.json for full records)

- J01a: SizeOfRawData 0xF0 → 0xF000 (attempt2; beyond-raw conclusion unchanged; QC VC-18).
- J01b (frozen, superseded downstream — cite P01/J04 for X-class facts): X=0x28B → X=0x28; X+0x14 "no static writer" → writer FUN_005b5380 @0x5b5433; node+0x2C "stored quat" → 3x3 rotation matrix (converted by FUN_00545030).
- B02a (frozen, defect visible): 4508 getter DYN rec f1/f2 transposition — J02 correction correct (QC VC-23).
- V18's "3x TEN SAM dword [SP+36]" → PUSHV_SPoff reads three DIFFERENT locals ([S1+8]=0, [S1+4]=root.prop(33505), [S1+0]=root) — re-derived by B02a, not copied.

## D. Still-open R1 hypotheses (unchanged by R2 evidence)

- record[6]/struct-0x48 network mechanism exists and is now precisely qualified (cursor writes its own wire struct; the transform channel reaches FUN_005030c0 on vt-0x5E2A3C nodes) — but its object-identity join to models 296445/218757 remains STILL_AMBIGUOUS (R2-C31; decisive edge = registry+0x3C root identity).
- HOSTCALL case ids for 4652/4653 (runtime binder data) remain runtime-bound; static residual scoped in BLK-R2-03.
