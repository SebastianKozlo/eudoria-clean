# REPORT (sanitized public projection) — PE_935_OWNER_SLOT1_MINCAP_WRITER_SOURCE_DEFAULT_TASK_OPENCODE_STATIC_R1_20261023

RUN_ID = PE_935_OWNER_SLOT1_MINCAP_WRITER_SOURCE_DEFAULT_TASK_OPENCODE_STATIC_R1_20261023
RUN_STATUS = COMPLETED_SCIENCE_QC_SEALED_PUBLISHED
TASK_ACTUAL_COUNT = 11
ROOT_SESSION = ses_e95b00276ffek009Rr9H9QjCVS
CLIENT_MEDIUM_ATTESTATION = DEFAULT_PREFLIGHT: nask-glm/glm-5-3, client reasoningEffort=medium, thinking=enabled, client_config_medium=true (all 11 roles)
REQUEST_EFFORT = NOT_OBSERVED
SERVER_EFFECTIVE_EFFORT = UNKNOWN
STOP/LENGTH/FAILED/RETRIES/ORPHANS = 10 stop / 1 length (W01 attempt1 FAILED_NO_DELIVERED_ARTIFACT, retried per ladder) / 0 orphans
QC_SCOPE = fresh QSCI (science) + fresh QACCOUNT (accounting); see QC_FINDINGS.json
CANONICAL_GATE_EFFECT = NONE

## 1. Authorized minimal static capture (EXECUTED, once)

One controlled helper-driven read of the pinned original client binary (pin: 8,015,872 bytes; SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31): exactly 21 reads (two full-file hash passes, one 4096-byte header window, four 4-byte DWORD cells), total 16,035,856 bytes == declared cap; both hashes equal the pin. Derived cell results (no raw dumps in this projection):
- BASE table (base 0x00A91E4C): VT+4 entry (cell VA 0x00A91E50) holds 0x0095D4FA; slot-3 control (0x00A91E58) holds 0x0085B6A0 == pin.
- DERIVED table (base 0x00A7DCB0): VT+4 entry (cell VA 0x00A7DCB4) holds 0x00528380; slot-3 control (0x00A7DCBC) holds 0x005278A0 == pin.
The source was NOT reopened after the closing hash; all further analysis used the saved capture plus the pinned saved disassembly (H5). Evidence limits: two equal hashes are not an atomic snapshot; source stability during acquisition is a premise; the capture proves STATIC file content, not any runtime vtable observation.

## 2. Actual new findings (the missing VT+4 frontier is closed)

1. BASE VT+4 = 0x0095D4FA: in the pinned saved disassembly this is a single-instruction indirect-jump thunk forwarding through a .rdata pointer cell (0x00A75378) with two sibling thunks adjacent; the forwarding cell content was NOT read (identity UNKNOWN). HBR-A03 confirmed: the address is even; the prior REJECTED-as-code-pointer classification had no basis; the saved prior artifact S4B records this same target in three other vtable contexts (14 hits); the base table is absent from S4B.
2. DERIVED VT+4 = 0x00528380: a thiscall method of the derived-table class with null-guards on two sub-object members and an enum gate; it is a WRITER that self-caches into its own fields at offsets 0x104..0x124 — two float-triples copied from out-arg buffers filled by two producer callees (0x0085C0C0, 0x0085C280), three floats from three other callees, plus five tail stores including three dwords sourced from globals (0x00BA921C-family). Role assessment: PLAUSIBLE self-cache update/refresh handler; NOT a world transform claim. Both exit paths return with a 0x8 stack cleanup.
3. VALUE_PRODUCER: both producer callees return the caller's out-arg buffer and forward through virtual slots on the sub-object at this+0x2c; the ULTIMATE float provenance remains UNKNOWN behind the runtime-vptr barrier (saved-only scope).
4. CTOR LINK (the decisive closed edge): the constructor 0x00528E50 (prior canon chain: creator 0x004C46C0 -> ctor 0x00528E50) stores an immediate vtable pointer whose value is EXACTLY 0x00A7DCB0 — the base of the captured derived table (0x00A7DCB4-4 = 0x00A7DCBC-0xC = 0x00A7DCB0). Therefore the class built by the creator->ctor chain has the captured derived table as its STATIC vtable (construction-level binding; runtime dispatch NOT_OBSERVED). The base table (0x00A91E4C) was never observed stored in this run — its class remains UNKNOWN.

## 3. Science terminal

WRITER_OBSERVED = YES (0x00528380; direct stores; saved-disassembly evidence level; code bytes NOT revalidated against the original)
WRITER_SITE = this+0x104..0x124 self-cache of the dispatching object, plus tail fields this+0xd2/0x9e/0xd4/0xd8/0xdc
WRITER_PHASE = update/refresh [PLAUSIBLE]; not ctor
VALUE_PRODUCER = 0x0085C0C0/0x0085C280 -> opaque virtual dispatch on [this+0x2c]; ultimate provenance UNKNOWN
CTOR_RETURN_VALUE_STATUS = UNKNOWN
RECEIVER_JOIN = NOT_ESTABLISHED (HBR-A01 preserved)
REGISTER_LOOKUP_JOIN = STATIC_CLASS_VTABLE_BINDING_ESTABLISHED (construction level; runtime NOT_OBSERVED)
MAP_KEY_AND_FLAG_CONTRACT = prior canon preserved, not re-derived
X_PROVENANCE = UNKNOWN
INSTANCE_ROOT_ROLE = UNKNOWN
RESOURCE_INSTANCE_JOIN = UNKNOWN
TRANSFORM_SOURCE = UNKNOWN
PHYSICAL_SOURCE_MEDIUM = UNKNOWN
SOURCE_CAPTURE_STATUS = STATIC_CAPTURE_PASS (1 attempt, 21 reads, 16,035,856 bytes, 2/2 hashes == pin)
ORIGINAL_ACTUAL_READ_BYTES = 16035856
SLOT3_CONTROLS = 2/2 PASS
STATIC_SLOT1_TARGETS = 0x0095D4FA (BASE, thunk) / 0x00528380 (DERIVED, writer)
TARGET_BODY_AVAILABILITY = 2/2 in pinned saved disassembly
DIRECT_STORES = 14 (9 mid-body + 5 tail)
RECEIVER_PRESERVATION = CONDITIONAL (HBR-A01)
BRANCH_RELEVANCE = WORLD_INSTANCE_RELEVANCE UNKNOWN; MODEL_RESOURCE_BINDING UNKNOWN; BUILDING_ROLE NOT_ESTABLISHED; HISTORICAL_TRANSFORM_PROVENANCE NOT_ESTABLISHED
FIRST_MISSING_EDGE = runtime vptr dispatch on [this+0x2c] (producer chain); secondary: the base-table thunk forwarding cell 0x00A75378 (4 bytes, .rdata) NOT_READ

WORLD_XYZ_RECOVERED = NO
HISTORICAL_PLACEMENT = NOT_ESTABLISHED
CURSOR_SOURCE_MEDIUM = UNKNOWN

## 4. Fresh-QC caveat (binding on this report)

Fresh QSCI independently recomputed the capture rows and verified the packet instructions, BUT it could not re-hash the original (reopen forbidden): the hashes are recorded claims and source stability during acquisition remains a premise; instruction verification is at SAVED-disassembly level (code bytes not revalidated); the creator->ctor chain is prior canon used as premise; RECEIVER_JOIN stays NOT_ESTABLISHED. Full reservations in QC_FINDINGS.json.

## 5. Process summary

One capture attempt (21 reads / 16,035,856 bytes == cap); 4 analyzed bodies (cap 48); 4 reference queries (cap 32); exposure metrics LOWER_BOUND/APPROX (no COMPLETE_WITHIN_BOUND claimed); 11 native tasks (9 workers + 2 fresh auditors; 10 stop / 1 length; parent/model parity verified from the read-only DB census). Deviations PD-1 (read-before-ADMIT, disclosed) and PD-2 (one failed worker attempt, charged and retried per ladder) are recorded in the sealed ledger; wording corrections QS-1/QS-2 from fresh QSCI were applied before seal. Sanitization: this projection contains only our own conclusions and provenance pins — no raw capture bytes, no raw header dump, no read ledger, no disassembly listings, no SDK text, no prompts, no model outputs, no DB, no local configs. Local sealed package (76 files, manifest pin 1AC466225AD9EFC6B8551EAE1F35AD426D3C53BDA0BD4BE880DBA2A94DEF0937) remains read-only on disk.

Science, integrity, process and publication carry separate verdicts; publication is not canonical acceptance. New evidence reported for external postaudit; no self-promotion of canon.
