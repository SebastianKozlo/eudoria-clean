# AUTHORIZATION_RECORD — PE_935_CAND4_006C9700_PLUS4_RESIDUAL_POST_AUDIT_CORRECTION_R1_20261008

## 1. The real human authorization (source: the human's direct instruction)

This bounded correction run was authorized by the human's DIRECT dispatch of
the frozen contract file to OpenCode (the pe-reconstruction worker phase
under PE-MASTER). The authorization instrument is the contract file itself:

```text
path    = C:\Users\User\Downloads\OPENCODE_PLUS4_RESIDUAL_CORRECTION_R1_20261008.md
size    = 23137 bytes
sha256  = 2634BA31C4002B636E6AF659D2EB51313C18CB2ED3B7FEB000AA2303042C6969
lines   = 172 (LF-terminated; file ends with LF)
read    = IN FULL before any work; measured identity recorded in
          INPUT_IDENTITIES.md §0
modified= NO — the contract file was not touched by this run
```

The contract states (§0): "The human authorizes ONLY THIS ONE correction run
if and when this complete contract is deliberately dispatched to OpenCode."
The complete contract was dispatched; the run is therefore authorized for
exactly its frozen scope:

```text
RUN_SCOPE = EXACTLY THREE DESKTOP P2 + ONE REC-W P3; correction-only
  P2-A  partial section overlap + PE32 32-bit address boundaries (§2)
  P2-B  truncated/malformed PE optional header constructor boundary (§3)
  P2-C  pointer-identity / dependent claim retraction records (§4)
  P3    REC-W canonical wrong-callsite identity gate (§5)
```

## 2. Authority and phase split

- The human's authorization covers the WHOLE bounded run including the
  parent's persistence steps enumerated in contract §7(h)–(i): ONE ordinary
  commit, fast-forward push and actual remote re-verification, strictly
  allowlisted to NEW files under OUTPUT_ROOT plus the narrow
  AUDIT_ENTRYPOINT.md amendments (one newest-first run row + the
  scope-corrected standing annotation of the immediately preceding source
  row).
- THIS executor phase (pe-reconstruction) performed the corrections, tests,
  PRE/POST evidence and records ONLY. It staged NOTHING, committed NOTHING,
  pushed NOTHING and did NOT edit AUDIT_ENTRYPOINT.md (those are the
  parent's later phases under the same one-run authorization).
- The independent ChatGPT Desktop post-audit of the resulting SHA is a
  LATER, EXTERNAL action (contract §0; NEW_DESKTOP_POST_AUDIT =
  NOT_PERFORMED); no external acceptance is self-declared by this run.

## 3. Hard boundaries honored (contract §0 — all NEGATIVE confirmations)

```text
new science                = NONE (NEW_SCIENCE_EXECUTED = NO)
Ghidra / new xrefs / new client bodies = NONE
FUN_007B79B0 continuation  = NOT touched; FUN_007B7930 = NOT touched;
FUN_006B2310               = NOT touched (body never opened; the &R+8
                            write-effects GAP stays a GAP)
transform / runtime / network RE = NONE
placement/XYZ research     = NONE (WORLD_XYZ_RECOVERED = NO)
Gamebryo/OpenMW research   = NONE (GAMEBRYO_OPENMW_RESEARCH_IN_SCOPE = NO)
generalized PE framework  = NONE (the v2 checker stays a bounded
                            range-safe read layer; GENERAL_PE_MAPPER_
                            CORRECTNESS = NOT_ESTABLISHED)
NEW_PCG_FUNCTION_BODIES   = 0
NEW_PCG_SCIENCE_EDGE_INTERPRETATIONS = 0
no second run, no milestone qualification, no next-experiment
authorization (NEXT_EXPERIMENT_AUTHORIZED = NO; HARD_STOP = YES)
```

## 4. Permission limits (what this run may NEVER do)

Modify the frozen contract; modify any historical audit package (all
READ_ONLY — the SOURCE_RUN 22-file census re-verified unchanged after all
controls); modify the physical EXE (verified unchanged before AND after);
mutate the source ACTIVE_CORRECTED_PINS.json (mutant records live only in
isolated scratch fixture JSON files under 00_PRE/scratch/ and
00_POST/scratch/); commit proprietary PCG payloads beyond small
pins/provenance; expand scope beyond the three P2 + one P3; run a second
correction run; authorize retroactively (RETROACTIVE_PRIOR_AUTHORIZATION =
NO); perform the fresh-context internal QC (parent's separate phase — no
self-review is labeled independent).

## 5. Era and corpus labels

Every physical fact cited in this package belongs to the PCG 9.3.5 client
image (D:\Eudoria_Reconstruction\pcg_install\Entropia.exe, 8015872 B,
SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31).
MindArk written consent covers technical analysis, migration, conversion
and non-commercial reconstruction; no public distribution of assets; the
EXE stays local-only and is never committed.
