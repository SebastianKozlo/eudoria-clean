# REPORT - PE_935_OWNER_R_JOIN_OPENCODE_SAVED_R1_20261021

RUN: bounded saved-only research run OWNER B/R ATTACHMENT, launched from a legal foreground receipt (CLI 1.18.18, scoped nask-glm medium); OUTPUT_ROOT fresh, created by saved_guard start. All statuses PENDING_EXTERNAL_POSTAUDIT.

## Model gate (real, runtime-captured)

- Coordinator: ses_ea20efac2ffeNM7Vc6ypcMxhs5, agent pe-master, model glm-5-3, provider nask-glm, version 1.18.18, PE_ROLE=SCIENCE_COORDINATOR.
- TOOL_SMOKE: ses_ea20c08d9ffe10igaO97UN1x02 (parent=coordinator, finish=stop, 1 completed tool), model glm-5-3-default; smoke input SHA256 independently re-measured by the child via tool: DAC385592D413A184F352DBD64AD9C504EDC2C4B67AE84E74378B79C9365F752; T1-T4 all matching; nonce ORJ_OC_20261021_721AE9.
- MODEL_PROBE (auditor role evidence): ses_ea20bae56ffeyZMWXA0IJ2ibKX (finish=stop, 0 tools), model glm-5-3-default.
- Scoped merged registry verified via CLI `opencode models nask-glm --verbose`: glm-5-3 and glm-5-3-default active with reasoningEffort=medium; glm-5-3-high/max exist but nothing selects them. REQUEST_EFFORT=NOT_OBSERVED, SERVER_EFFECTIVE_EFFORT=UNKNOWN.
- saved_guard check PASS (authoring 148+1 files, 2365 pinned inputs). start --proof PASS -> event 000001_START.

## ETAP A - reader/getter mechanics (CONFIRMED)

- B=entryECX preserved to EBX; R_load=M32[B+0xC] into EDI at 00527AB7; R_call==R_load within span (no EDI/ECX write between load and CALL 0085BFA0; no intervening call). Guards: R nonzero, member B+0x10 nonzero, float member updates.
- OUT_local = caller 0x34-byte (13-DWORD) frame block (LEA EAX,[ESP+0xC] = ESP0-0x34), pushed as the getter's sole stack arg; getter epilogue RET 0x4 cleans it (row 1171004).
- Getter chain: P_provider=M32[R+0x2C] (0085BFA6), VT=M32[P] (0085BFA9), F_slot24=M32[VT+0x24] (0085BFAB), T_slot = value RETURNED by CALL EAX (0085BFB5); 12 floats read from [T_slot+0x00..0x2C].
- Frame closure (decisive): 0x0096CB20 ends RET 0x24 (row 1500231) -> callee-cleans model row-proven; epilogue balance (POP EDI/POP ESI/ADD ESP,0xa0/RET 0x4) forces ESP=ESPe-0xa8 at 0085C06A, so [ESP+0xac]=[ESPe+4]=OUT pointer; EAX never overwritten afterwards => U_getter==OUT_local pointer at the STATIC pointer level. Cdecl virtual-callee countermodel doubly falsified (return-address corruption). Residual: the opaque virtual CALL EAX callee-cleans inference is arithmetic necessity, not a row of that callee; no runtime pointer-equality capture.
- Output block: 13 dwords at [OUT+0x00..0x30] (9 REP MOVSD + four tail stores incl. FLD1 -> 1.0f at +0x30); caller copies 13 dwords from U_getter to DST_copy=R+0x30 (REP MOVSD ECX=0xD).

## ETAP B - bounded +0xC census and construction upstream

- Literal MOV dword [GPR+0xC] census in preregistered ranges 00527000..00529000 and 0085B100..0085B800: exactly 7 candidates (NAV002, event 000007). Qualification (J006..J011 + QC003/QC004): 0085B1CD = construction-time ZERO-INIT of the constructed object field (base ctor 0085B1B0 writes vtable 0xA91E4C +0, 0 +4, arg +8, 0 +0xC, 0 +0x10; ESI=entry ECX; EBX=0); the other six are stack/frame stores (two SEH logging-shape zeros, two EBP argument slots, one ESP staging). 7th candidate 0085B652 not opened (cap of 6 windows). NO nonzero owner-field writer in the literal census - scoped negative, not a global absence claim.
- Construction chain: alloc 0x128 (0095D3C4) -> derived ctor 00528E50 (vtable 0xA7DCB0 per pinned prior hexdump; calls base ctor 0085B1B0) -> registration 00856190 on singleton 004154F0; registration head gates on [EDI+0x74], container ops, and invokes virtual slot0 on the registered object; NO visible [EDI+0xC] store in the head.
- Reader caller (single direct caller 0048EE31): B = retval of 004123D0 (trivial deref, pinned prior decomp) on stack slot X0+0x70; the nonzero gate rows 4696-4698 check the SAME slot. CORRECTED per QC004-F1 (ESP shift): the visible 0085B840 wrapper (rows 4692-4693) built a DIFFERENT slot (X0+0x74); the B-source wrapper's construction lies before the admitted window and is UNRESOLVED.

## ETAP C - R origin and placement relevance

- W_attach (nonzero writer of owner+0xC): NOT_ESTABLISHED in admitted scope. Construction zero is CONFIRMED (row 1169775); the reader requires R nonzero (rows 180900-180901); no nonzero store exists in the literal census, the construction/registration windows, or the qualified upstream. NOT proven absent.
- R origin: NOT_ESTABLISHED. Ranked frontier: (1) derived ctor 00528E50 body post-base-chain stores (cheapest next admission); (2) virtual slot0 target at 008561EB (GA3 saved dataset zero-hit for 0x00A7DCB0 - needs a saved nonliteral reference representation); (3) new preregistered literal census ranges; (4) runtime watchpoint (out of scope).
- GA3: three complete zero-hit scans (0x00A7DCB0, 0x00A91E4C, 0x00527AB0; census_complete=true; events 000017-000022) - scoped zeros for the single pinned saved dataset.
- Provider identity (P/VT/F/T_slot): UNKNOWN; no class/instance identity claimed. No model-instance join. PLACEMENT_RELEVANCE: NO_FOR_NOW.

## Claims and QC

- CLAIMS.json ORJ-01..ORJ-11: 6 CONFIRMED (incl. scoped negative ORJ-06 covering the six opened candidates; ORJ-11 GA3 dataset-scoped negative), 1 STRONGLY_SUPPORTED (ORJ-08 corrected per QC004-F1), 2 UNVERIFIED/NOT_ESTABLISHED (ORJ-09, ORJ-10). All PENDING_EXTERNAL_POSTAUDIT.
- Workers: W001 (72 rows), W003R (64), W004 (85) DELIVERED inline-only (0 tool parts, glm-5-3-default, finish=stop). W003 length-failed (empty; retried smaller as W003R per contract). W002: generation-1 answer delivered but prompt-parity broken by a trailing-newline transport artifact; the exact-byte generation-2 retry hit finish=length; explicit DIRECT_ANALYST fallback declared per contract, with W002 question content fully covered by the delivered W003R and independently reviewed by QC002 (gen1 answer retained as parity-unverified auxiliary material).
- Fresh QC (pe-master-auditor, inline-only; generation-2 exact-parity redelivery after a self-detected ROLE_PROMPT_PARITY seal failure - all gen1 dispatches lost one trailing newline in transport, QC003 gen1 additionally contained a paraphrase; see CORRECTIONS_APPLIED CA-6): QC001 (72 rows) PASS_WITH_NOTED_GAPS (gaps closed by coverage: getter epilogue RET 0x4 row, full getter body, DF=0 premise); QC002 (64 rows) PASS - ORJ-04/ORJ-05 upheld with independent full ESP-chain re-derivation, cdecl countermodel doubly rejected; QC003 (85 rows) QC_PARTIAL - ORJ-07/08/09/10 PASS, ORJ-06 CORRECTIONS (7th candidate now explicitly named NOT_OPENED_CAP, CA-5); QC004 CORRECTIVE (64 rows incl. all five rejected candidates + wrapper-this row 4692) QC_PASS; the gen1 QC004 found the MATERIAL correction QC004-F1 (ESP shift in the B-source attribution), applied to ORJ-08 and OWNER_CANDIDATES.json (CA-1), and its arithmetic was independently re-confirmed by the gen2 W004 worker (same slot identity for the gate and the B-source deref).

## Budgets

Charged: 53/64 body reservations, 484/10000 listing rows (union 484), 38/400 CALL charges, 26/64 candidate reservations. GA3: 3/8 scans, 0/32 matches. Nav: 6 metadata requests. Incidents: 0. W003 length-failure recorded (no exposure; retry within contract).

## Coverage

Checked fully: all 14 admitted extracts (row-complete reads by coordinator; worker/QC sub-spans contiguous); 4 worker + 4 QC answers (byte-dumped from DB, parity-checked); 3 GA3 zero-hit scans re-derived by reference_probe.verify_events; census NAV results with event pins. NOT CHECKED (explicit): derived ctor 00528E50 body; 0085B840/008544D0/0096B760/0096CF80/00856190-post-head bodies; virtual slot targets (slot+0x24 provider, slot0 registration hook); 7th census candidate 0085B652; sibling getter callers; any runtime behavior; any original game bytes.

## Conclusion

The owner reader/getter mechanics chain is now row-closed: B -> R=[B+0xC] (nonzero-gated) -> P=[R+0x2C] -> VT/F_slot24 -> T_slot (12 floats) -> 13-dword block (incl. 1.0f) into caller OUT -> copy to R+0x30; U_getter==OUT_local at static pointer level. The P0 attach question resolves to a DATA_BARRIER: the field is zero-initialized at construction and its nonzero writer is NOT in the preregistered literal census nor in the admitted construction/registration/upstream windows. FIRST_MISSING_EDGE: the nonzero store site for owner+0xC, ranked: derived ctor body 00528E50 > new preregistered census ranges > saved nonliteral reference representation (slot0 target of vtable 0xA7DCB0) > runtime watchpoint.

WORLD_XYZ_RECOVERED=NO
HISTORICAL_PLACEMENT=NOT_ESTABLISHED
CURSOR_SOURCE_MEDIUM=UNKNOWN
CANONICAL_GATE_EFFECT=NONE
All statuses PENDING_EXTERNAL_POSTAUDIT. Publication (sanitized, additive) follows seal; publication is not scientific acceptance.
