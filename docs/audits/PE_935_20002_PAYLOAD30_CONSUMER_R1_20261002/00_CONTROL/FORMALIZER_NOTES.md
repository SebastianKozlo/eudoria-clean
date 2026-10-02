# FORMALIZER_NOTES — PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002

Genuine ambiguities/gaps observed by the pe-master-auditor formalizer session in the
PE-MASTER dispatch spec (2026-10-02), recorded ONLY — NO resolutions invented here.
Where the executor must choose, the executor records the choice + evidence basis in the
run artifacts. These notes do NOT modify the contract; RUN_CONTRACT.md is frozen as
transcribed.

FN-1 (§13) — control-name shorthand "NC-ANCHOR"
The §13 minimum feasible set defines exactly four controls: NC-FRAMING, NC-ANCHOR-ADJ,
NC-RECORD, NC-VALUE. The closing paragraph ("If NO mechanism is reached: ... still
execute NC-FRAMING, NC-ANCHOR (feasible part), NC-RECORD and the routing-discrimination
controls.") references "NC-ANCHOR", which is not a defined control name. It is not stated
whether "NC-ANCHOR (feasible part)" means the feasible part of NC-ANCHOR-ADJ (the
adjacent-displacement control), nor what that feasible part is when no client read is
pinned (e.g. extraction/decode of +0x2C/+0x34 under the same rule, without the
instruction-level destination comparison). Not resolved by the formalizer.

FN-2 (§18 vs §7) — singular REPORT record fields vs the two anchored records
§7 deterministically defines TWO anchored records (ANCHOR_PRIMARY, ANCHOR_ZERO) plus the
FIELD_CENSUS. §18 requires singular REPORT.md keys (RECORD_ORDINAL_OR_PHYSICAL_ID,
RECORD_FRAME_START, RECORD_PAYLOAD_START, RECORD_PAYLOAD_LENGTH, FIELD_FILE_OFFSET,
PAYLOAD_PLUS_30_RAW_BYTES, PAYLOAD_PLUS_30_DECODED_VALUE). The spec does not state which
anchored record populates the singular §18 fields. Not resolved by the formalizer; the
executor must state which anchored record populates them and where the other anchored
record's equivalent values are recorded.

FN-3 (dispatch) — no timebox specified
The dispatch specifies no execution timebox/deadline for the executor run. The formalizer
did not invent one. Any timebox is PE-MASTER's to set at executor dispatch.
