# F5 DISPOSITION — W7 (FIRSTCALL package: process HOLD + supersession QC comparison)

RUN_ID: PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914 · Era: PCG_9_3_5 · MODE: STATIC-ONLY.

## 1. F5_PROCESS_STATUS (the human's OPTION C decision, recorded verbatim-faithful)

**F5_PROCESS_STATUS = PARKED_UNAUTHORIZED_ATTEMPT** (human decision OPTION C, 2026-09-14).

The FIRSTCALL run (PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914) started before the
authorization gate. The violation history stands. The package is never completed, never
retro-authorized, never deleted, its science never adopted as an evidence source, never
published; it stays untracked on disk untouched (verified this run: untracked, all files
byte-identical to the formalizer census — §2 below). Any future reference to its measured
facts is a QC comparison only (§3), never an adoption.

## 2. FIRSTCALL package census re-verification (read + hash ONLY; no modification)

Re-hashed at cleanup start by this run's own script
(00_CONTROL/cleanup_verify_identities.py; raw: 01_RAW/IDENTITY_VERIFICATION_AT_START.txt
§4). All 7 files MATCH the 00_CONTROL/SOURCE_IDENTITIES.json pins (formalizer census =
disk truth: 6 content files + 1 .pyc = 7 files, plus 3 EMPTY directories 02_ANALYSIS /
03_EVIDENCE / 06_REPORT — each verified empty):

| relpath | size | SHA256 (re-measured == pin) |
|---|---|---|
| 00_CONTROL/RUN_CONTRACT.md | 12443 | 9E0006030D078E71F4D9609371F6BA27CDEB936BA63ABD8D5EE5F9DAAEEC8882 |
| 00_CONTROL/SOURCE_IDENTITIES.json | 2037 | 088A4EE4766B37C6B80B55643A2610F9FBA1C44C29E707A2B137DCA881F8DBB2 |
| 00_CONTROL/run_state.json | 7125 | D7F7428827B459256F23A4CFEDC77D5CB8DD5B40061D4F6D52C6A1C5F7A14F65 |
| 00_CONTROL/slot17_core.py | 10615 | 02D58F8B642E1952AA4E3A5A538998C1FDFEDCB17A7B798AB481ADE9AF6CAF4D |
| 00_CONTROL/slot17_run.py | 26646 | C4802B2A1B7E1FBFF8258A993B2CB36D0707025F345B4460106D7EDA444CB2C3 |
| 00_CONTROL/__pycache__/slot17_core.cpython-312.pyc | 12520 | FF8344BFC9BDA545AA466DD0A45DCFA67D377CEBDE8C8146EA79F147792D3FE9 |
| 01_RAW/SLOT17_BODY_RAW.txt | 5577 | 2EABC45F81738039DA6C876C411301EFCE0CD0744BB6CF0077C740A455A9C2F1 |

Disk walk total: 7 files (== pin). ZERO modifications by this run.

## 3. Supersession comparison (QC comparison ONLY — FIRSTCALL is NOT adopted as evidence)

Per-fact consistency table: FIRSTCALL's measured facts (its 01_RAW/SLOT17_BODY_RAW.txt,
read-only) vs the SLOT17 package's INDEPENDENT re-measurements (READ-ONLY sources:
01_RAW/ENTROPIA_007B5390_DISASM.txt, 02_ANALYSIS/ENTROPIA_SLOT17_FINGERPRINT.md,
02_ANALYSIS/GETOBJECTBYNAME_FINGERPRINT.md, 03_EVIDENCE/ENTROPIA_RTTI_CHAIN_PROBE.json).

| # | FIRSTCALL measured fact | SLOT17 independent re-measurement | Consistent? | Strictly subsumed? |
|---|---|---|---|---|
| 1 | calibration RTTI: SF vtable 0x00A7D458 -> COL 0x00AA12B8 -> TD 0x00B78834 -> `.?AVSceneFeederObject@@` PASS | SF RTTI chain re-derived in the SLOT_CENSUS/LINK30 runs (SF vtable 0x00A7D458); SLOT17 independently re-measured the NiNode chain (below) with the same method (COL@vtable-4, TD@COL+0xC, name@TD+8) | YES | YES (SLOT17 re-measured with its own probe + the method family is shared) |
| 2 | NiNode RTTI walk: vtable 0x00A8CCF4 -> COL 0x00AAEEC8 -> TD 0x00B936C8 -> `.?AVNiNode@@` PASS | ENTROPIA_RTTI_CHAIN_PROBE.json + ENTROPIA_SLOT17_FINGERPRINT.md: primary NiNode vtable VA 0x00A8CCF4, MSVC RTTI `.?AVNiNode@@`, base chain NiAVObject -> NiObjectNET -> NiObject -> NiRefObject; PLUS the NiRTTI (second RTTI system) static-initializer proof and slot-2 GetRTTI decode | YES | YES (SLOT17 additionally proved the NiRTTI side + slot 2) |
| 3 | slot17 dword [0x00A8CCF4+0x44] = 0x007B5390 PASS | `[vtable+0x44] (slot 17) = 0x007B5390 (re-measured, target_slot17.match = true)` (ENTROPIA_SLOT17_FINGERPRINT.md) | YES | YES |
| 4 | the 6 SF slot-3 dispatch pins byte-exact @0x0050A057..0x0050A064 (8bf1 / 8b4e30 / 8b11 / 50 / 8b4244 / ffd0) PASS | The dispatch window re-measured in the SLOT_CENSUS run (published census input); SLOT17 fingerprints carry the same pins consistently | YES | YES |
| 5 | body decode 0x007B5390: push ebx; mov ebx,[esp+8]; push edi; push ebx; mov edi,ecx; first call @0x007B5399 E8 rel32 target 0x007BF220 (stop at first call) | ENTROPIA_007B5390_DISASM.txt: IDENTICAL instruction sequence from the same entry (53; 8B 5C 24 08; 57; 53; 8B F9; E8 82 9E 00 00 call 0x7bf220) — AND the decode continues through the FULL extent (test eax; child-array loop [edi+0xD4]/[edi+0xCC]; recursive virtual dispatch via [child->vtable+0x44]; first-match-or-NULL; ret 4 @0x007B53DE) | YES | YES (FIRSTCALL stopped at the first call by design; SLOT17 decoded the full extent + neighbors + vtable prefix) |
| 6 | first-call target prologue 0x007BF220: NULL-guards (arg [esp+4] and [ecx+0xC]); byte-pair strcmp ladder; ret 4 | ENTROPIA_SLOT17_FINGERPRINT.md helper section: helper 0x007BF220 opened from the true entry, full extent 0x007BF220..0x007BF270; (a) NULL-guards the argument, (b) reads the name member at this+0x0C, (c) INLINED byte-pair strcmp (2-bytes-per-iteration compare ladder), `ret 4` @0x007BF26D | YES | YES (SLOT17 additionally classified the helper as the self-name-check of base NiAVObject::GetObjectByName semantics) |

**Verdict: consistency = 6/6 facts consistent; strict subsumption = 6/6** (every FIRSTCALL
measured fact is re-measured independently and consistently in the SLOT17 package, which
additionally decoded the full function extent, the neighbors, the vtable prefix, the
NiRTTI static initializer, and the two-oracle comparison). No inconsistency found.

## 4. F5_SCIENCE_STATUS

**F5_SCIENCE_STATUS = SUPERSEDED_SCIENTIFICALLY_BY
PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1_20260914** (commit
5290e79e0dc469c70605f35c125d7b727f9f7a6b). The process status (§1) is unaffected by this
scientific supersession: the violation history stands, the package remains
PARKED_UNAUTHORIZED_ATTEMPT, untracked, untouched, never adopted as an evidence source,
never published.
