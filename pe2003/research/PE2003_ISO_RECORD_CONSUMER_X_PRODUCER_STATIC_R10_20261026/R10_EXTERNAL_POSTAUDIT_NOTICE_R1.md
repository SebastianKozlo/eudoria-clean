# R10_EXTERNAL_POSTAUDIT_NOTICE_R1.md — additive postaudit notice for PE2003_ISO_RECORD_CONSUMER_X_PRODUCER_STATIC_R10_20261026

This notice is ADDITIVE: no R10 file, manifest row or ENTRYPOINT line is modified by this change. R10's published history (commit 2b7595c) is NOT rewritten; its bytes stand as published. This notice records the independent external postaudit findings (R10_CORRECTIONS disposition, REQUIRE_MATERIAL_CORRECTIONS) so that downstream readers do not carry R10's superseded statements forward as standing evidence.

## Material corrections (superseded R10 statements)

1. The helper object H has observed extent AT LEAST 0x18 bytes (ctor 0x4474F0 writes a DWORD at this+14; stack frame at 0x534F00 separates H and A by 0x18) — the "16-byte helper" wording is superseded; the exact full class size remains unestablished.
2. F is an opaque pointer-or-NULL, NOT a confirmed list with stride 0x24. The consumer reads F+0x1C/F+0x20 and passes the ADDRESS F+0x24; no backedge or iteration was proven. (R11 later closed this consumer and disproved iteration for it: no backedge exists in 0x5257C0..0x5258F5.)
3. 0x447B20 is a CONFIRMED call TARGET receiving the argument M; its reader/model-reader role was NOT established. The CALL slot is at 0x4475F8 (0x4475EF is a load). (R11 qualified the body without assumed semantics: a query/detach-style operation over M's internal list; not established as a reader.)
4. CMP EAX,EAX at 0x4475D0 makes the JNE not-taken; the reserve/growth description is not the behavior of the shown reachable path.
5. The stores at 0x52B750 prove binding AT STORE TIME (this+0xC=A1; this+8=[A1+8]; byte this+0x10=A2). Field behavior, M_store==M_read equality and retention are NOT automatically confirmed; use separate symbols M_store/M_read/M_arg until bridges are proven.
6. Callback arg2 at 0x564A44 originates from local_struct+8 (zero-init) but the local escaped through opaque calls; the value at callback time is UNKNOWN.
7. 3F800000 at 0x65E5B4+30 and ten code-address-shaped first DWORDs do not establish exact vtable length, object inequality or a type-query role for the shared address 0x447C90.
8. Wrapper 0x4021E0 builds a SEPARATE population E; the call at 0x40248A takes [S+68] (not [S+64]); this writer is NOT established as the writer of the E consumed at 0x564890; E_builder != E_fetch is NOT a proven inequality (no identity bridge).
9. R10's "9/10 hits" setter census is encoding-shaped and had an off-by-one scan start; R11's corrected full-range census: exactly 9 direct call sites of 0x451730.
10. Accounting: the actual R10 child census is 13 native tasks (11 research + 2 QC); four public session IDs were transcribed incorrectly; reservations are not actual counts; >=255 instruction rows were read before admission and 626 further QC exposures were not reconciled in the reported 786 figure — this is not full compliance.

## Publication-integrity findings (R10 publication contract NON-PASS; history NOT rewritten)

- The publication manifest contained a stale self-row (manifest must never list itself).
- The ENTRYPOINT diff was 4/3 (numstat): three pre-existing lines changed instead of exactly one additive line. The historical lines are left as-is (PRE_EXISTING_OUTSIDE_NEW_DIFF); future publications add exactly one line and preserve all old bytes (the R11 publication demonstrates this).
- The public R10 report included raw instruction encodings forbidden by the publication contract. The R10 files stand as published; this notice is the corrective disclosure. The R11 public projection contains no raw encodings.

## Seal-coverage history

R10's SCI manifest covered documents only (48 WORK/REC files outside the seal); the first manifest was overwritten after a post-manifest marker write without preserving v1; stage-acceptance gates were absent and the full historical closing input recheck was not shown. Those are R10's historical gaps — today's hashes do not restore R10's historical seal. R11 avoided repeating them: all science evidence lives inside the sealed science tree, the manifest is exclusive-create as the last write, stage gates are present, and the full closing input recheck is recorded.

## Standing status

WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; LOCAL_SOURCE_EXHAUSTED=NO; CANONICAL_GATE_EFFECT=NONE. Next scope per the corrected record: 0x447B20 semantics, the full 0x5257C0 consumer, then actual [S+68]/E+0x14 provenance — executed by R11 (see the R11 report in pe2003/research/PE2003_ISO_M_READER_RECORD_FIELD_JOIN_STATIC_R11_20261027).