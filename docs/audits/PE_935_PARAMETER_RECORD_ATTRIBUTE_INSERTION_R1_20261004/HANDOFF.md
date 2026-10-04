# HANDOFF — PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004

Executor: pe-reconstruction (PE-MASTER bounded worker contract; NO_NESTED_TASKS;
STATIC-ONLY — the client never ran; no Ghidra; raw byte reads + manual x86 decode only).
This is the return-to-parent handoff. The run was RESUMED: the first session's final
return arrived empty at PE-MASTER with a partial package on disk (Phase A + raw windows
only, nothing committed); this session completed the run from that state per the
parent's resume order — Phase A re-verified (not redone), the analysis finished, all
package files written, and the publication executed as assigned.

## Result in one paragraph

YES to the first half of the question, CONFIRMED byte-pinned for ONE concrete record:
templates.vfs record id2=16083 (file offset 560,212, payload 28 B, header
{id=16083,size=28,ver=1,crc 0x82A125AB}) is carried PHYSICAL RECORD BYTES → CLIENT
PARSER (reader FUN_0072FA30, path from the byte-pinned string "Parameters\templates.vfs"
@0x00A86D30; per-record read FUN_00971AD0; parse FUN_00730C90 — this run's own field
decode, destinations confirmed against the established getter anchors) → REAL KEY
(id2=16083) + REAL VALUE {B=0, A=410620, C=0, D_f32=0.49950098991394043, list1=[],
list2=[], f11=0} → IDENTIFIABLE RECEIVER (the RB-tree registry, root DAT_00BA1824, lazy
singleton FUN_0043A550) → ATTRIBUTE INSERTION (FUN_0072F8D0 → FUN_0072F7F0 0x44-B node
→ FUN_0072F740 pair {key@node+0x10, value@node+0x14} → FUN_005670A0 canonical full-object
copy). PARSER_TO_RUNTIME_VALUE_SEAM = CONFIRMED (S1; NOT placement recovery). The
placement-consumer half is STRONGLY_SUPPORTED, NOT CONFIRMED: RECORD_A's object IS
read back with the byte-pinned STATIC key PUSH 0x3ED3 (=16083, the record's own id2) by
the placement-record constructor FUN_005B5F90 (full-field copy FUN_005670A0 of every
field the parse wrote) — but that constructor is a SIBLING of the contract's named
family; the named builder FUN_00567770 reads the SAME registry via its deriver
FUN_004C5580→FUN_004C5480 ([C2-corrected identity] the runtime value returned by the
class-selector-20006 (CLASS_SELECTOR 0x4E26=20006, pair @0x004C54C2 → FUN_00703B80) /
property-tag-6 (PROPERTY_TAG 6, PUSH 6 @0x004C551F → FUN_0070C180 @0x004C5523) getter
on the exact receiver and branch) → FUN_0072F880 with a
RUNTIME key (value identity for RECORD_A not statically provable); and the named driver
FUN_00567C50's own tree (→ FUN_00567B40 queue push → FUN_00567170) reads registry
objects with byte-pinned static keys {15321,15322,15323,14912,14919} — DISJOINT from
RECORD_A's key. FIRST_MISSING_EDGE = INSERTED_VALUE_TO_PLACEMENT_CONSUMER ([C2-corrected]
the provenance of the specific runtime value returned by the class-selector-20006 /
property-tag-6 getter and consumed as the FUN_0072F880 lookup key). NEW_FUNCTION_COUNT=11/20; records 2/2; VFS 1/1;
inventory COMPLETE (27 files, all .vfs, 19 numeric, 20006.vfs ABSENT). SELF_CHECK
QC_VERDICT = QC_PASS (8/8 gates; S5_QC_CHECKS.json).

## Status block

```text
RUN_ID = PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004
RUN_STATUS = COMPLETE (S1 CONFIRMED; placement-consumer edge STRONGLY_SUPPORTED)
HARD_STOP_REASON = contract terminal state after the single authorized question;
  the recommended next experiment is DESIGNED_NOT_EXECUTED
BASE_SHA = 780cc4e442ec2bef7e4e0880b9ffee22a39e302c
HEAD_SHA = (this publication commit; discover: git log -1 -- docs/audits/PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004)
REMOTE_STATE = actual remote master == 780cc4e at start, re-verified immediately
  before the commit, and == local HEAD == origin/master after the push (verified live)
AUDIT_OUTPUT_ROOT = docs/audits/PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004/
FINAL_REPORT_PATH = <root>/FINAL_REPORT.md
PRIMARY_EVIDENCE_PATHS =
  <root>/01_RAW/S4_RECORD_ANCHOR_AND_SCANS.json  (RECORD_A/B anchors + imm32 scans + string pin)
  <root>/01_RAW/S2_EXE_WINDOWS.json              (25 windows + 22-target censuses + PUSH scans)
  <root>/01_RAW/S3_MORE_WINDOWS.json             (12 further windows)
  <root>/01_RAW/S5_QC_CHECKS.json                (8/8 QC gates PASS)
  <root>/RECORD_A.md, RECORD_B.md, PARSER_CHAIN.md, RECEIVER_INSERTION_CHAIN.md,
  <root>/PLACEMENT_CONSUMER_EDGE.md, SELECTED_FILE.md, QC_REPORT.md
CANONICAL_GATE_EFFECT = NONE; M1_CLOSED = NO; NEXT_EXPERIMENT_AUTHORIZED = NO
```

## For the fresh-context QC (suggested falsification targets)

1. Re-walk templates.vfs with an independent framing (e.g., the candidate-scan method:
   ver==1 + payload-id2 echo) and re-derive RECORD_A's offset 560,212 without the
   36-quantum rule — the two methods must agree (they did in-run).
2. Re-derive the FUN_00730C90 destinations from raw bytes and re-parse RECORD_A/B —
   the A/B destination pairing is the historical wording trap (A must land at +0x08).
3. Try to rescue CONFIRMED for the named family: search for any static 16083 key
   inside FUN_00567770/FUN_00567C50 (this run's scans found none — PUSH sites: 1 total
   @0x005B6597; all-encodings: 2 total, both outside the family).
4. Check the DISJOINTNESS claim: FUN_00567170's 5 MOV-imm32 key sites vs RECORD_A's
   16083 — no overlap (byte addresses listed in PLACEMENT_CONSUMER_EDGE.md).

## Next experiment (proposal ONLY — not authorized, not executed)

[C2-corrected experiment identity — supersedes "Decode the WRITERS of the 0x4E26
(20006-family) property value", which chased a conflated identity.] Trace the
producer/provenance of the SPECIFIC RUNTIME VALUE returned by the
class-selector-20006 (CLASS_SELECTOR 0x4E26=20006, pair @0x004C54C2 → FUN_00703B80
@0x004C54CE) / property-tag-6 (PROPERTY_TAG 6, PUSH 6 @0x004C551F → FUN_0070C180
@0x004C5523) getter on the exact receiver and branch whose result is consumed as the
FUN_0072F880 lookup key at FUN_00567770 (FIRST_MISSING_EDGE). Allowed provenance
outcomes (OPEN taxonomy, no forced physical-vs-network binary): PHYSICAL_RECORD_DERIVED
| CONSTANT_INITIALIZATION | LOCAL_COMPUTED | CACHE_PROVIDER | MESSAGE_DERIVED |
FALLBACK_BRANCH | UNKNOWN. Alternative/fallback branches (e.g. the flag-0xD82 path)
remain SEPARATE/UNKNOWN — do NOT assume all getter results come from the normal tag-6
branch. Adjacency lead (RAW_OCCURRENCE_ONLY): the 0x3ED3/0x3ED2 property-idiom sites
@0x0050F383/0x0050F2F3 (undecoded function; no role claimed).

## Boundaries honored

STATIC_ONLY; no client launch; no runtime instrumentation; no model join; no XYZ;
no 20xxx/24xxx detailed analysis (inventory-verified only); no second VFS; no third
record; 11/20 new functions; historical packages read-only; foreign untracked groups
untouched; [C1/P3-corrected proprietary-byte census — supersedes "no proprietary
payload committed"] no complete original proprietary binary/payload FILES were
committed; bounded original byte windows / payload excerpts used as forensic evidence
ARE present in this package (RECORD_A/B payload hex, bounded EXE windows in 01_RAW);
no NEW proprietary payload beyond those bounded evidence excerpts; originals
otherwise represented by era, path, size, SHA256, offsets, bounded window hashes;
AUDIT_ENTRYPOINT.md: one factual row added in
the SAME publication commit; manifest regenerated LAST (self-excluded; bijection over
the committed package files).
