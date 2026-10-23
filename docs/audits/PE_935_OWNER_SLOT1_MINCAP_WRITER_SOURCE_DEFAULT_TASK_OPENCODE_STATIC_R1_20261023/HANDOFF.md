# HANDOFF (sanitized public projection) — PE_935_OWNER_SLOT1_MINCAP_WRITER_SOURCE_DEFAULT_TASK_OPENCODE_STATIC_R1_20261023

TASK_ACTUAL_COUNT = 11
ROOT_SESSION = ses_e95b00276ffek009Rr9H9QjCVS
RUN_STATUS = COMPLETED (science, fresh QC, two master self-reviews, seal, sanitized publication with remote verify)
SCIENCE_VERDICT = PARTIAL_PASS_WITH_CLEAR_EDGE_CLOSURE
PROCESS_VERDICT = PARTIAL_NONCOMPLIANT (disclosed deviations; permitted retry is not a violation)

## Closed in this run
- Missing VT+4 edge of both candidate tables, resolved by a one-shot minimal static capture: BASE 0x0095D4FA (indirect-jump thunk; forwarding cell NOT_READ), DERIVED 0x00528380 (writer method).
- Writer chain: 0x00528380 self-caches two float triples and three floats (this+0x104..0x124) plus tail fields; producers 0x0085C0C0/0x0085C280 forward through an opaque virtual dispatch on [this+0x2c] (runtime-vptr barrier).
- Static class binding: ctor 0x00528E50 stores EXACTLY 0x00A7DCB0 = the captured derived-table base => the writer belongs (statically) to the class built by creator 0x004C46C0 -> ctor 0x00528E50 (construction level; runtime NOT_OBSERVED).

## One best missing edge
FIRST_MISSING_EDGE = the runtime vptr of the [this+0x2c] producer dispatch — decides whether the cached values are world/transform data or internal state. Requires runtime observation OR a new explicitly authorized minimal static contract (e.g., the sub-object class vtable via its constructor store). Secondary: the 4-byte .rdata forwarding cell 0x00A75378 identifies the base-table VT+4 target. NO original-binary access without a NEW explicit authorization.

## Preserved premises
HBR-A01..A06 fully preserved (see the additive POSTAUDIT_NOTICE_R1.md in the predecessor package). Invariants: WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; CURSOR_SOURCE_MEDIUM=UNKNOWN; CANONICAL_GATE_EFFECT=NONE; static table content is not runtime receiver identity.

## Resume instruction
1. Work from the sealed saved artifacts only; the original was not reopened after the closing hash.
2. Next P0: saved-only identification of the [this+0x2c] sub-object class vtable; only then consider a new minimal static-read authorization.
3. The sealed local package is read-only; the canonical publication receipt lives in the run's RECEIPT root (outside the repo).

## Fresh-QC caveat
As in REPORT.md: hashes are recorded claims (no QC re-hash); saved-disassembly-level verification; creator->ctor is prior canon; RECEIVER_JOIN NOT_ESTABLISHED.
