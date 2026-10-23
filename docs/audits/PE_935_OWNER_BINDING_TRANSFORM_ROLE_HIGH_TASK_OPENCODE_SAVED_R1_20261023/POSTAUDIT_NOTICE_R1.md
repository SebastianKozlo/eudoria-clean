# POSTAUDIT_NOTICE_R1.md — additive notice for PE_935_OWNER_BINDING_TRANSFORM_ROLE_HIGH_TASK_OPENCODE_SAVED_R1_20261023

This run (PE_935_OWNER_SLOT1_MINCAP_WRITER_SOURCE_DEFAULT_TASK_OPENCODE_STATIC_R1_20261023) accepts and applies the external HBR postaudit findings HBR-A01..HBR-A06 to the predecessor package (this folder). The predecessor's sealed artifacts remain byte-untouched; this notice is additive.

- HBR-A01 ACCEPTED: RECEIVER_JOIN is kept NOT_ESTABLISHED everywhere in the new run; store/reload value preservation remains CONDITIONAL; the opaque CALL between store and reload is not resolved by any new evidence; REGISTER_LOOKUP_JOIN in the new run is scoped to a STATIC construction-level class-vtable binding only (ctor store == captured table base, exact equality), never a runtime claim.
- HBR-A02 ACCEPTED: the TEST AL consumption claim is not reused; the slot-5 result dependency remains UNKNOWN past the intervening callee.
- HBR-A03 RESOLVED BY NEW EVIDENCE: the minimal static capture confirms the base-table VT+4 cell (0x00A91E50) actually holds 0x0095D4FA; the address is even; the prior REJECTED-as-code-pointer classification is retired as unjustified; the saved prior artifact S4B records this target in three other vtable contexts; the code identity of the target beyond the saved one-line thunk remains UNVERIFIED.
- HBR-A04 ACCEPTED: prior-body availability acknowledged; per-run not-read is never reported as data absence.
- HBR-A05 ACCEPTED: budgets are not reset between waves; all attempts/failures charged; exposure metrics reported as LOWER_BOUND/APPROX.
- HBR-A06 ACCEPTED: raw tool stdout handled via subprocess (shell=False) with UTF-8 JSON re-dump; a failed terminal-consistency version is preserved as TERMINAL_CONSISTENCY.json.failed.txt.

Science consequence: the predecessor's saved-only VT+4 DATA_BARRIER is now closed for both candidate tables by the authorized minimal static capture; the world/instance relevance questions remain open exactly as before (WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED).
