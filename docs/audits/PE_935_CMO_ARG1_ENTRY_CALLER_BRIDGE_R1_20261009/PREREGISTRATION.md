# PREREGISTRATION — PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009

```text
RUN_ID = PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009
RUN_CLASS = BOUNDED_STATIC_ARGUMENT_PROVENANCE
PREREGISTRATION_STATUS = WRITTEN_BEFORE_SCIENCE
WRITTEN_AFTER = PREFLIGHT PASS (contract identity, git triple, worktree, OUTPUT_ROOT absence, EXE identity, 8 required input identities — see INPUT_IDENTITIES.md)
WRITTEN_BEFORE = any code-window extraction, disassembly or interpretation
REPOSITORY_ROOT = D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean
BASE_SHA = ce75b7b3ee0b7b87c1f0a03bc79167169aed71a0
```

## P1. Actual authorization (recorded before science)

- Contract file (authoritative task definition):
  `C:\Users\User\Documents\ChatGPT\PE\PE_CMO_ENTRY_CALLER_BRIDGE_PROMPT_REVIEW_20261009\OPENCODE_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_REVISED_20261009.md`
  SIZE=23187, SHA256=773C1310A2CB02B365068EE2D9C684A97765E4D416E30B415B8672D8CC09FF07.
  Verified byte-for-byte with Get-FileHash BEFORE any other action. The contract alone authorizes
  nothing (`CONTRACT_STATUS = PREPARED_REQUIRES_SEPARATE_HUMAN_DISPATCH`).
- Actual dispatch: a separate human-authorized worker assignment received in this OpenCode session
  (2026-10-09, executor agent `pe-reconstruction`, model `nask-glm/glm-5-2`, host WinDev2407Eval with
  WSL distro `PE-AI`). The dispatch identifies the contract by exact path, byte size and SHA256 and
  authorizes exactly this one run `PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009`.
- Scope granted to THIS worker by the dispatch (production package only):
  PREREGISTRATION.md, INPUT_IDENTITIES.md, WINDOW_IDENTITIES.json + raw disassembler text per
  window, ENTRY_FRAME_LEDGER.csv, CALLER_STACK_LEDGER.csv, BRIDGE_PROVENANCE.json, CLAIM_MATRIX.csv,
  `03_SCRIPTS/run_frame_bridge.py` (location choice: `03_SCRIPTS/`, documented here), CONTROL_RESULTS.json,
  ARTIFACT_CONTROL_RESULTS.json, SUPERSESSION_AND_STANDING.md — all only under OUTPUT_ROOT.
- Explicitly NOT this worker's (per dispatch): `qc_frame_bridge.py` + `QC_RESULTS.json` + `QC_REPORT.md`
  (separate fresh-QC worker/session); `FINAL_REPORT.md` / `PE_MASTER_REVIEW.md` / `EVIDENCE_INDEX.md` /
  `HANDOFF.md` / manifest / AUDIT_ENTRYPOINT.md row / any stage/commit/push (later parent phases).
  NO_NESTED_TASKS: no agent is spawned by this worker; fresh QC is left to the separate session and is
  recorded here as NOT_PERFORMED_BY_THIS_WORKER — never invented, never faked.
- No commit, no push, no AUDIT_ENTRYPOINT.md write, no modification of any file outside OUTPUT_ROOT.
  Standing lack of general static-placement authorization is NOT lifted by this dispatch; it grants only
  this bounded static experiment, no milestone authority, no follow-up experiment.

## P2. The one bounded question (§1 verbatim intent)

At the already recorded CALL 0x004C47C1, what supplies the first explicit stack argument of
FUN_00528E50, and is that same pointer value forwarded as arg1 of FUN_0085B1B0 at CALL 0x00528E8D?

Two fixed windows establish one bridge. Phase A relates the old source slot to the derived-constructor
entry frame. Only after clean Phase A qualifies may Phase B establish one upstream delivery. STOP before
tracing the contents or earlier producer of the pointed-to area.

Kept strictly separate: source-slot address, value read from that slot, prepared argument-slot address,
LEA-computed address, pointee contents, receiver ECX, semantic role. Address equality alone does not
prove memory-value preservation. No assumption of position, NiPoint3, world instance, building, network
packet, model or XYZ. No OpenMW/Gamebryo research or loading in this run.

## P3. Exact code scope (absolute; §4)

| Window | Half-open VA interval | Bytes | Raw offset | SHA256 (pinned, to re-verify) |
|---|---|---:|---:|---|
| A | [0x00528E50,0x00528E92) | 66 | 1216080 / 0x128E50 | F8735567340CD3BE2F6B64B4BBC2BE292487E97B6184758CA408E6FF1CE78E85 |
| B | [0x004C4792,0x004C47C6) | 52 | 804754 / 0x0C4792 | B59E16DC116F4CE0438A1E92BC6B2CBC33FAB0B19FABC24CB3A29C911C1EFB6A |

```text
UNIQUE_ORIGINAL_CODE_BYTES_ANALYZED_MAX = 118   (A 66 + B 52 = exactly 118)
AUTHORIZED_PARTIAL_CODE_WINDOWS_MAX = 2
COMPLETE_FUNCTION_BODIES_TO_OPEN = 0
NEW_CALLEE_BODIES = 0
TARGET_CALLSITES = {0x004C47C1, 0x00528E8D}
INCIDENTAL_OPAQUE_CALLSITE = 0x004C4797 → 0x0095D3C4  (opaque: no body, no heap-origin claim,
  no allocator-wide semantics; record the normal ABI-compatible return condition; if unsupported,
  retain conditional/unresolved WITHOUT opening it)
UPSTREAM_BEYOND_WINDOW_B = 0
OTHER_CALLSITES_OR_XREF_CENSUS = 0
FIELD_SEMANTIC_PROMOTIONS = 0
RUNTIME / NETWORK / MODEL / VFS_BNT_NIF_RE = 0
```

Method rules preregistered:
- These are two PARTIAL windows with three visible CALL instructions. Every interpreted instruction and
  all three callsite roles are recorded; scope is never hidden under RAW/prior-repin labels.
- Whole-file hashing and PE header/section-table reads are allowed for identity/mapping only; physical
  bytes read for metadata are separated from interpreted code bytes.
- Both complete intervals must map to unique RAW-backed ranges (no ambiguous/BSS mapping). Boundary
  provenance comes from the pinned raw offsets above and is cross-checked against the pinned historical
  instruction streams (F00528E50_CTOR_MOBJ.txt, F004C46C0_CREATE.txt — input records only). Function
  starts are NEVER inferred from CC/RET padding or E8 searches.
- Disassembler: WSL GNU objdump (GNU Binutils for Debian) 2.44, raw-binary mode
  (`objdump -D -b binary -m i386 -M intel --adjust-vma=<window VA>`), actual name/version/command/
  return status/raw output persisted per case. No new decoder, no analysis platform.
- A small symbolic replay for these instructions/controls is permitted: `03_SCRIPTS/run_frame_bridge.py`
  (location choice: 03_SCRIPTS/). It consumes objdump tool output and actual bytes; no handwritten
  listing is ever represented as tool output. Unsupported instruction/operand/control flow or unresolved
  alias → controlled UNRESOLVED/FAIL; the expected result is never filled in; no universal verifier.
- The old top-level QC with hidden EXE access is not run. Historical production register_definitions is
  NOT a complete reaching-definition history and does not serve as one here.

## P4. Preregistered hypotheses (to DERIVE from the physical bytes — these are expectations to test, not conclusions)

### H-A (Phase A — window A entry frame and value preservation; straight-line path within the window)

- HA1 ESP chain: with E = symbolic ESP at entry 0x00528E50, the decoded stream yields
  PUSH −1; PUSH handler; PUSH previous FS:[0] → E−0x0C; SUB ESP,0x1C → E−0x28; PUSH EBX; PUSH ESI;
  PUSH EDI; PUSH cookie → E−0x38; S = ESP at 0x00528E76 = E−0x38; source-slot address S+0x3C = E+4
  (the entry first stack-argument slot). FS:[0] stores and LEA do not adjust ESP; the cookie
  computation changes a value, not the push width.
- HA2 preservation of the entry-slot value: no write in [0x00528E50, 0x00528E84) touches [E+4]
  (pushes write below E; a [ESP+0x10] write stays below E; the FS:[0] write targets the TIB segment
  chain head, not the stack); every write is examined, no unexamined alias is silently assumed safe.
- HA3 EDI preservation: no write to EDI in [0x00528E86, 0x00528E8A) after the load at 0x00528E84.
- HA4 delivery at CALL 0x00528E8D (hardware return-address push): ESP_before_base_CALL = S−0x0C
  (three net pushes after S); ESP_at_callee_entry = S−0x10; callee arg1 slot = [S−0x0C] (the PUSH EDI
  slot); callee arg1 value = the value loaded from [E+4] on this path; receiver ECX of the callee
  derives from the entry receiver through ESI (separate channel, not the arg1 channel).
- Expected falsifiers (control-coded): wrong SUB delta (M1), wrong source displacement (M2), any
  write aliasing [E+4] or [S+0x3C], EDI clobber, wrong CALL target, decode failure.
- Stop rule: if clean A cannot establish entry-argument/value identity → STOP SCIENCE;
  B analysis = NOT_PERFORMED (with reason); reports/safe persistence only. Expected rejections of
  synthetic A hypotheses do not invalidate a correctly qualified original A.

### H-B (Phase B — window B, ONLY after clean A qualifies)

- HB1 T relation: T = ESP at 0x004C47AF. Under the stated normal ABI-compatible opaque-return
  condition (callee 0x0095D3C4 pops exactly its return address and returns with EAX set; PUSH 0x128
  before, ADD ESP,4 after), T equals ESP at the B-window start. The callee stays opaque: no body, no
  heap-origin claim, no allocator-wide semantics. If the condition cannot be supported, it remains
  conditional/unresolved without opening the callee.
- HB2 flags: flags survive from TEST EAX,EAX (0x004C47A3) to JE 0x004C47C8 (0x004C47AD) — no
  flag-writing instruction intervenes — so the branch condition is precisely EAX==0. The JE target
  0x004C47C8 lies OUTSIDE window B and is never opened or interpreted.
- HB3 (nonnull path, normal opaque return AND EAX!=0): the decoded stream yields
  MOV ECX,[ESP+0x50]; MOV EDX,[ESP+0x4C]; PUSH ECX; PUSH EDX; PUSH ESI (ESP=T−0x0C);
  LEA ECX,[ESP+0x14] = ADDRESS(T−0x0C+0x14) = ADDRESS(T+8), kind=ADDRESS (an address computed, not a
  value read); PUSH ECX (ESP=T−0x10; slot [T−0x10] := ADDRESS(T+8)); MOV ECX,EAX (receiver = the
  opaque call's EAX return value); CALL target == 0x00528E50 (E8 8A 46 06 00); FUN_00528E50 entry
  E = T−0x14; entry arg1 slot [E+4] = [T−0x10]; entry arg1 VALUE = ADDRESS(T+8), NOT DWORD [T+8].
- HB4 (null path, EAX==0): ZF=1 → JE taken → control exits the window at 0x004C47C8 → the constructor
  CALL is NOT reached on this path; NO fabricated delivery. No claim about what the out-of-window
  branch does; no assertion of allocation success; no fall-through continuation.
- Expected falsifiers (control-coded): LEA displacement (M3), last-push register (M4), early push order
  without arg1 change (M5 — must retain unchanged arg1 facts), JE→JMP (M6), receiver-only change (M7 —
  must retain unchanged arg1 facts), CALL rel32 (M8), LEA→MOV (M9), flag clobber between TEST/JE.

### H-BRIDGE (join; the actual question)

- Under HA1–HA4 (clean A), HB1–HB3 (clean B, nonnull path) and value preservation across the call
  (no write to [T−0x10] between PUSH ECX at 0x004C47BE and the load at 0x00528E84, checked from the
  decoded A stream): S = E−0x38 with E = T−0x14, hence [S+0x3C] = [T−0x10] — the entry first stack
  argument slot of FUN_00528E50 at CALL 0x004C47C1, containing ADDRESS(T+8), IS the source slot whose
  value is loaded into EDI at 0x00528E84 and delivered as arg1 of FUN_0085B1B0 at CALL 0x00528E8D.
- Scope of any such PASS: a POINTER_VALUE_IDENTITY across two delivery boundaries (arg1 delivery at
  the FUN_00528E50 entry; arg1 delivery at the FUN_0085B1B0 entry). It does NOT prove any value inside
  [T+8] (pointee contents), any type/lifetime beyond the examined calls, the caller's global frame
  layout, or the history of that stack area. No full signature is inferred from visible pushes; no
  claim about alternate entries/paths; delivery at entry does not require the base constructor to return.

## P5. Preregistered control matrix (12 cases; production + fresh-QC = 24 separately recorded EXPECTED outcomes)

All mutation offsets name byte positions in SYNTHETIC copies only; the EXE is never altered. Synthetic
fixtures live in an OS temp dir outside Git and are removed at the end. Identity hashes qualify ORIGINAL
inputs only; changed hashes must NOT reject synthetic controls before analysis. The same
byte → objdump → symbolic-analysis pipeline runs on every case. Expected discriminating outcomes:

| Case | Input/change | Expected discriminating result |
|---|---|---|
| A_CLEAN | Original A | S=E−0x38; source [E+4]; value preserved/delivered — or honest original analysis failure. |
| B_CLEAN_NONNULL | Original B, normal opaque return, EAX!=0 | CALL reachable; arg1 ADDRESS(T+8); receiver = return value. |
| B_CLEAN_NULL | Same original B, EAX==0 | JE taken; target CALL not reached; no fabricated delivery. |
| M1_A_FRAME | @0x00528E5E: 83 EC 1C → 83 EC 18 | S=E−0x34; later source [E+8], not entry arg1 [E+4]. |
| M2_A_SLOT | @0x00528E84: 8B 7C 24 3C → 8B 7C 24 38 | Source [E] under the original frame, not [E+4]. |
| M3_B_LEA_DISP | @0x004C47BA: 8D 4C 24 14 → 8D 4C 24 18 | arg1 ADDRESS(T+0x0C), not ADDRESS(T+8). |
| M4_B_LAST_PUSH | @0x004C47BE: 51 → 52 | arg1 is the earlier EDX load value MEM(T+0x4C), not the LEA address. |
| M5_B_EARLY_PUSH_ORDER | @0x004C47B7..B8: 51 52 → 52 51 | Earlier argument order changes; final arg1 ADDRESS(T+8) and its slot UNCHANGED; provenance not rejected merely because unrelated arguments differ. |
| M6_B_SKIP | @0x004C47AD: 74 19 → EB 19 | Unconditional exit; no delivery at the target CALL. |
| M7_B_RECEIVER_ONLY | @0x004C47BF: 8B C8 → 8B CE | Receiver becomes the T-point ESI; already-pushed arg1 and its slot remain unchanged; ESI's earlier producer remains unknown. |
| M8_B_WRONG_TARGET | @0x004C47C1: E8 8A 46 06 00 → E8 8B 46 06 00 | Actual target 0x00528E51; no valid bridge to entry 0x00528E50; wrong target NOT followed. |
| M9_B_LEA_TO_MOV | @0x004C47BA: 8D 4C 24 14 → 8B 4C 24 14 | arg1 MEM(T+8) (value read), not ADDRESS(T+8); no pointee interpretation. |

Rules: M5 and M7 must retain unchanged arg1 facts while reporting the altered other channel — a checker
that merely rejects every changed fixture is insufficient. Wrong-target/unreachable cases must reach
ACTUAL target/path predicates, not a manifest/byte-hash side failure. Baseline and all structured
results are preserved, including unexpected failures and repairs; PRE is never rewritten to match POST.
Correctly rejecting a mutated hypothesis = CONTROL_PASS, not falsification of the original client.

The fresh-QC side of the 12×2 matrix is NOT performed by this worker (dispatched to a separate
fresh-QC session); CLAIM_MATRIX.csv records its 12 expected outcomes with actual = NOT_PERFORMED_BY_
THIS_WORKER. No QC verdict is invented or issued by this production run.

### Artifact controls (§7)

- Baseline: re-read of the persisted load-bearing artifacts (WINDOW_IDENTITIES.json,
  BRIDGE_PROVENANCE.json, ENTRY_FRAME_LEDGER.csv, CALLER_STACK_LEDGER.csv) through the ordinary final
  gate must PASS first. The gate compares actual facts (instruction addresses/bytes, CALL targets, ESP
  states, ADDRESS-vs-MEM kind, entry-slot identity) to physical/replayed evidence — not only counts or
  field presence.
- AC1: a copied artifact with the clean arg1 value kind replaced, ADDRESS(T+8) → MEM(T+8), must be
  REJECTED by that same gate.
- AC2: a copied artifact with the clean entry source changed, [E+4] → [E+8], must be REJECTED by that
  same gate.
- Package hash/manifest checks are bypassed ONLY in these two isolated synthetic artifact controls
  (they test the fact predicate itself); no historical file is mutated; mutated copies live in the
  OS temp dir outside Git and are removed afterwards.

## P6. Gates (separate; no generic SCIENCE_PASS, no semantic classifier)

```text
ORIGINAL_IDENTITY          pinned identities of contract/EXE/BASE/required inputs; original window SHA256s
DECODE_COVERAGE             every window byte decoded by objdump; no gaps; exact window-boundary instruction fit
ENTRY_FRAME_VALUE_IDENTITY Phase A: E→S chain, slot equivalence, preservation (a)(b)(c), delivery facts
CALLER_PATH_AND_VALUE       Phase B: T, opaque condition, flags, LEA kind/expression, arg1 slot/value, receiver, path
CROSS_CALL_IDENTITY         the joined bridge: same pointer value across both delivery boundaries
REQUIRED_CONTROLS           12-case matrix outcomes per expected discriminating results
ARTIFACT_CONSISTENCY        baseline artifact gate PASS + AC1/AC2 rejections
```

QC_PASS (which additionally requires all 24 matrix outcomes and artifact checks) is not issued by this
worker. Science outcome is independent of QC and publication.

## P7. Conditions and stop rules

1. Phase B only after clean Phase A qualifies; otherwise B analysis = NOT_PERFORMED with reason.
2. Stop science at the first unresolved boundary; finalize rather than tracing another function.
3. No pointee contents tracing; no earlier producer of the pointed-to area; no upstream beyond
   window B; no callee bodies (0x0085B1B0 and 0x0095D3C4 stay unopened); no other callsites/xref
   census; no field semantic promotions.
4. `python -B` (no .pyc residue); temp fixtures in `C:\Users\User\AppData\Local\Temp\opencode\…`
   (outside Git), removed at the end; never staged; no proprietary payloads in outputs (persisted raw
   tool outputs are disassembly text of the two bounded windows only; no .bin window extracts committed).
5. SCIENCE_OUTCOME is exactly one of:
   ENTRY_ARG1_AND_SINGLE_CALLER_BRIDGE_ESTABLISHED /
   ENTRY_ARG1_ESTABLISHED_CALLER_BRIDGE_UNRESOLVED /
   STACK_FRAME_PROVENANCE_UNRESOLVED /
   ORIGINAL_BYTES_REJECTED_PREREGISTERED_HYPOTHESIS /
   BLOCKED (critical preflight; no scientific result).
6. Standing evidence (§2) is preserved verbatim in SUPERSESSION_AND_STANDING.md; no reinterpretation of
   the [arg1+8] → MovableObject+0x44 store; no callee re-opening; no ACLD↔CMO identity transfer;
   historical labels are not type evidence.

## P8. Toolchain (preregistered, verified available before this file was finalized)

```text
Disassembler : GNU objdump (GNU Binutils for Debian) 2.44 — WSL distro PE-AI (Debian, kernel 6.18.33.2-microsoft-standard-WSL2)
Command form : objdump -D -b binary -m i386 -M intel --adjust-vma=<window VA> <fixture.bin>
Python       : Python 3.13.5 (WSL PE-AI), invoked as python3 -B
Replay       : 03_SCRIPTS/run_frame_bridge.py (this package; bounded decoder-assisted symbolic replay;
               consumes persisted objdump text + EXE bytes; unsupported constructs → UNRESOLVED)
```

## P9. Planned evidence files (OUTPUT_ROOT only)

```text
PREREGISTRATION.md                    (this file — before science)
INPUT_IDENTITIES.md                   (preflight records incl. authorization provenance)
WINDOW_IDENTITIES.json                (window intervals, hashes, PE mapping, tool identity)
01_RAW/WINDOW_A_OBJDUMP.txt           (raw objdump output, original window A)
01_RAW/WINDOW_B_OBJDUMP.txt           (raw objdump output, original window B)
01_RAW/CONTROLS/<CASE>_OBJDUMP.txt    (raw objdump output per control case, 12 cases)
ENTRY_FRAME_LEDGER.csv                (instruction-by-instruction Phase A derivation)
CALLER_STACK_LEDGER.csv                (instruction-by-instruction Phase B derivation)
BRIDGE_PROVENANCE.json                (load-bearing claims with full evidence fields)
CLAIM_MATRIX.csv                      (12 production + 12 fresh-QC expected outcomes)
CONTROL_RESULTS.json                  (per-case structured facts + gate verdicts, production)
ARTIFACT_CONTROL_RESULTS.json         (baseline PASS + AC1/AC2 rejections)
SUPERSESSION_AND_STANDING.md          (§2 verbatim + this run's relation)
03_SCRIPTS/run_frame_bridge.py        (bounded helper)
```

---

## P10. SESSION CONTINUITY DISCLOSURE (appended by the fresh retry session, 2026-10-09)

Sections P1–P9 above were written by the FIRST executor session (which recorded
itself in P1 as model `nask-glm/glm-5-2`). That session CRASHED mid-run and
returned an EMPTY handoff. This P10 section is appended by the fresh retry
session (agent `pe-reconstruction`, model `nask-glm/glm-5-3`); the P1–P9 body is
preserved exactly as written and is NEVER rewritten to match post-science
results.

State at retry-session discovery: OUTPUT_ROOT contained exactly 3 crash-left
files — PREREGISTRATION.md (19151 B, SHA256
F36DE40AF53CEE9FE2F0F5A11A65475239E5035DE96F2FD45D4E5669E775EACC),
01_RAW/WINDOW_A_OBJDUMP.txt (1882 B, SHA256
7AABA008CFBD8BAF4CDF868BA25E3E9A014E9F732E375402553AAA3282D2C86B) and
01_RAW/WINDOW_B_OBJDUMP.txt (1557 B, SHA256
B82C5532D1E10EE3116C7E74EA72471257FA1E3A110F7BCFEA0C452B01ED99CC). The
INPUT_IDENTITIES.md referenced in the P1 "WRITTEN_AFTER" line did NOT exist on
disk (the crash preceded it).

Retry-session verification and continuation decisions (full detail in
INPUT_IDENTITIES.md §I2):

1. PREREGISTRATION.md — reviewed in full against the contract: complete and
   PRE-consistent (contract-derived hypotheses/controls only; no post-science
   result leakage). Decision: KEPT as the preregistration of record; extended
   only by THIS dated section.
2. 01_RAW/WINDOW_A_OBJDUMP.txt and 01_RAW/WINDOW_B_OBJDUMP.txt — the retry
   session re-ran its own fresh GNU objdump invocations on independently
   extracted window fixtures (physical bytes from the EXE at the pinned raw
   offsets; both SHA256s equal the contract pins) and found the persisted
   disassembly sections BYTE-IDENTICAL to its fresh outputs (23/23 and 17/17
   instruction lines; both rc 0; fixture provenance in both files correct).
   Decision: both files KEPT unchanged (sound; authorized paths). The retry
   session's own raw invocations are additionally persisted as
   01_RAW/WINDOW_A_OBJDUMP_RETRY.txt / 01_RAW/WINDOW_B_OBJDUMP_RETRY.txt.
3. Continuation: the retry re-performed the ENTIRE preflight from physical
   bytes (contract identity, git triple + live remote query, EXE hash, window
   extraction/hashes, all 8 required repo inputs, PE section mapping,
   toolchain identity) and re-derived ALL science (Phase A, Phase B, the
   bridge join, the 12-case production control matrix and the artifact gate)
   with its own pipeline (`03_SCRIPTS/run_frame_bridge.py`, decoder-assisted
   symbolic replay over GNU objdump output, fail-closed). No unverified claim
   from the crashed session is reused; the crash and the two-session origin of
   this package are disclosed here and in INPUT_IDENTITIES.md.

The crashed session's P1 model identity (`nask-glm/glm-5-2`) is preserved
above as a record of THAT session; the production science in this package was
executed by the retry session (`nask-glm/glm-5-3`). Fresh internal QC remains
NOT_PERFORMED_BY_THIS_WORKER in both sessions (separate fresh-QC worker per
dispatch).
