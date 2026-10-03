# RETRACTIONS / SUPERSESSIONS / BLAST RADIUS — PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z

## Retraction made BY THIS RUN (affects this run's own earlier framing only —
no historical package claim is retracted by this run's evidence)

R-1 (executor self-correction, in-run, disclosed):
- RETRACTED: the initial interpretation (carried while reading lead
  packages, and visible in early analysis notes) that FUN_006CB020 builds a
  "named MODEL instance" 0x110 B — the decompilation of FUN_007796D0 (O03)
  shows the 0x110 object's ctor writes NiControllerSequence::vftable (an
  animation-sequence holder keyed "<id>__<name>").
- BLAST RADIUS: this run's E5 wording only (corrected in
  TRACE_EDGE_BLOCKS.md before finalization). HISTORICAL packages that used the
  "named instance" phrase (STATIC_INSTANCE_TRACE S-B) described the same
  object as "instancja nazwana 0x110 B o nazwie <id>__<name>" — the byte
  facts (0x110 size, name format, registration) are unaffected; only the
  CLASS identity is now pinned more precisely. No historical claim is
  retracted by me; flagging for adjudication is NOT required (the historical
  text did not assert a class identity).

## Supersessions (this run's results vs prior canon — none contradict;
all extend or re-pin)

S-1: 20002_PAYLOAD30_CONSUMER record-0 anchor — RE-PINNED byte-exact
    (payload+0x30 = BB 2E 00 00 = 11963). Supersedes nothing; revalidates.
S-2: JOIN R1 id2-domain observation (1,364/1,366) — REPRODUCED with an
    independent implementation (C1). No status change (stays
    CANDIDATE/UNVERIFIED per AMEND-R2 F3 wording).
S-3: NINODE_SLOT17 slot-17 anchor (0x007B5390) — RE-PINNED from raw bytes
    (vtable 0x00A8CCF4 located from ctor imm32). No status change.
S-4: NINODE_SLOT17 slot-27 "rep movsd x13" descriptive detail — NOT
    reproduced inside this run's 512-B probe window (1 consecutive rep movsd
    found; UpdateWorldData SHAPE confirmed by the +0x38/+0x6C offsets and
    parent-pointer read). Recorded as a probe-window discrepancy. This is NOT
    a retraction of that run's evidence (their window was theirs); if their
    exact window is desired, it should be re-derived in a run that reads the
    full function — flagged as adjudication-optional, LOW priority.

## Blast radius statement

- No material counterexample against any historical claim was produced by
  this run. All historical anchors used (20002 record 0 bytes; 296445.nif
  index offset; slot 17 VA; placement-record field offsets) re-pinned
  CONSISTENT.
- The largest interpretive delta is R-1 (NiControllerSequence identity), which
  adds precision rather than contradicting any published claim.
- No canonical gate, qualification, or milestone status is touched
  (CANONICAL_GATE_EFFECT = NONE).
