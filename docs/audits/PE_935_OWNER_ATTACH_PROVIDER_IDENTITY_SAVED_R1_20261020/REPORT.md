# REPORT — OWNER ATTACH / PROVIDER IDENTITY — SAVED R1

RUN_ID: PE_935_OWNER_ATTACH_PROVIDER_IDENTITY_SAVED_R1_20261020
MODE: SAVED_ONLY_ADAPTIVE_RESEARCH_DEFAULT_GLM_WITH_FRESH_QC_AND_PUBLICATION
MODEL: primary/worker/QC all nask-glm/glm-5-3-default, reasoningEffort=medium (MODEL_DEFAULT_GATE.json, measured session metadata; SERVER_HONORS_EFFORT=UNKNOWN). No HIGH/MAX session used.
Corpus: SAVED_TEXT_CATALOG (GHIDRA_H5_VTABLE2.txt, H5 sha256 642CC29A01B8AD6F783E82E14DA4A61FA00BA6A3EC6DF98EDFF28AC25CC1D8DB) only. Zero game-file stat/hash/read, zero runtime, zero scripts of prior runs executed.

## Main results

1. **B→R attach (Etap A, P01): NOT at 0085ACE9.** The candidate store+C @0085ACE9 is a **stack local zero-init** (ESP-relative, after SUB ESP,8 + PUSH ESI + PUSH EDX), zeroing an 8-byte pair passed by address as an out-buffer arg to CALL 00730F00 inside 0085ACD0 (ECX=ARG1). Not an object-field write; candidate rejected for this body (scoped negative).
2. **R→P provider store (Etap B, P02–P04): NOT at 0085BE70.** 0085BD80 is a stream-deserialization method whose this (OBJ) is a **stack-local temporary** of the 0048EDxx stream-loader (constructed at [ESP+0x18] by CALL 0085BBE0 @0048EDDF, passed via cdecl adapter 0085BF00(reader,OBJ) — its sole caller at 0048EDF7). Store+2C@0085BE70 copies a 3-dword global constant (float-like trio, [0x00BA921C..0x00BA9224]) into OBJ+0x28/+0x2C/+0x30. OBJ ≠ R (stack temp vs persistent owner field); the chain is definitively not the R+0x2C provider writer.
3. **New negative (P05):** store+2C@0085C0A7 is a float slot of a full 13-dword transform write at [EAX..EAX+0x30] (9-dword REP MOVSD + 3 floats + FLD1); EAX=[ESP+0xAC], receiver identity unknown; not a provider pointer store.
4. **NEW STRONG POSITIVE CANDIDATE (P06–P08): the 0085CD17 provider store.** In a large serialize function (entry before 0085C780, not yet opened): ESI=[ESP+0x34]; factory call [obj[ESI+0x28]] vtable slot+0x18 → **MOV [ESI+0x2C],EAX** @0085CD17 — the first store+2C with genuine object-pointer provenance. The stored object is used as a vtable receiver with slots +0xAC (float getter), +0xB0 (3-float out), +0x4C/+0x50 (results consumed as int). The containing function is a serializer (CALL EDI float→double writes, TEST EAX,0x207 error checks; EBX = outer saved object with child-pointer array [EBX+0x50/+0x54]).
5. **Join ESI==R: NOT_ESTABLISHED** — the serialize function entry and the initialization of [ESP+0x34] are outside all admitted windows. This is the run's FIRST_MISSING_EDGE. If the join later succeeds, the chain becomes: B→R (per frozen prior P01), R+0x28 factory owner → slot+0x18 → P stored at R+0x2C (0085CD17), P → VT, VT+0x24 → F, CALL F → T — with the provider slots +0xAC/+0xB0 (+0x4C/+0x50) as additional P-method evidence.
6. T (retval of CALL F, floats read from EAX after call @0085BFB5) origin: still opaque from this run (0085BFA0 target body not re-opened; no new evidence). RETURN_T_ORIGIN=UNKNOWN.

## Incidents (process, honest accounting)

- INC1 (P02): parent displayed operand rows of 3 unadmitted bodies during census (0085BF00/0085BF20/0085BF50 + 0085BD80 tail) → INCIDENT_DEBIT 3 bodies; region later admitted properly as P03. PARTIAL_NONCOMPLIANT recorded, interpretation was stopped, no retroactive legalization.
- INC2 (P07): parent displayed operand rows of the unadmitted serialize-part [0085C912,0085CA01) while locating the entry → INCIDENT_DEBIT 1 body; region admitted properly as P08. PARTIAL_NONCOMPLIANT recorded.
- Worker dispatch: P01 succeeded on first retry (initial attempt + both P02 attempts stalled empty — operational anomaly, per contract not a science violation; P02+P03..P08 analyzed by PARENT_DIRECT with attribution in each RUN_STARTED.json).

## Status lines

WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; CURSOR_SOURCE_MEDIUM=UNKNOWN; CANONICAL_GATE_EFFECT=NONE.
SCIENCE_VERDICT: PARTIAL_PASS — two commissioned store-site candidates qualified (negative, decidable); one new strong positive provider-store candidate found; B→R→P chain not yet closed (missing entry binding edge).
