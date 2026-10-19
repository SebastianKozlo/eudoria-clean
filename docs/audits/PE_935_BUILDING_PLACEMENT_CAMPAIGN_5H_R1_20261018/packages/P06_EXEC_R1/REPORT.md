# P06 (Front C) — EXECUTOR REPORT
# PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018

- RUN_ID: `PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018`
- PACKAGE: P06, Front C (definition/resource -> instance-record connection)
- ROLE: pe-reconstruction (bounded executor; no delegation)
- RUN_STARTED (real clock): 2026-10-18T22:21:29Z — PACKAGE_HARD_STOP: 2026-10-18T23:15:00Z
- ADMISSION: A912213023006 (parent-granted; recorded in CONTRACT.json)
- SOURCE PIN: `GHIDRA_H5_VTABLE2.txt` (saved listing, 50,780,146 B, 1,743,929 lines),
  SHA256 `642CC29A01B8AD6F783E82E14DA4A61FA00BA6A3EC6DF98EDFF28AC25CC1D8DB`
  — verified twice (pre-extraction, package close). Address search = navigation;
  semantic read restricted to the two admitted subregions.
- RUN_STATUS: **COMPLETED_WITH_PROCEDURAL_INCIDENT** (INCIDENT-P06-I1: one unforeseen
  in-window body, disclosed; see Incident section).

## 1. Assignment (from P06.json, SHA-verified)

(a) What does the {0x66,A} request scheduler callback thunk `0x008BD720` dispatch to?
Report the exact jump/call target VA; DO NOT read the target region.
(b) Slot-consumer `0x00848EA0`: slot-object class semantics, which fields/property it
reads (bridge hypothesis: class-20006 property tag 6), what it does with them, where its
data comes from; does any VFS-record-fed channel reach it in-window (FAMILY-P/T merge)?

## 2. Method

1. CONTRACT.json SHA256 verified (`5239C441...4891905`).
2. RUN_STARTED.json materialized FIRST (22:21:29Z) with real clock.
3. Source pin hashed and verified before any semantic read.
4. Context docs (bridge run 06_REPORT: DRAFT_FINAL_REPORT.md L95-214, AMEND_LOG_R1.md
   full, HANDOFF.md full, PE_MASTER_REVIEW.md grep-only) read for CITATION ONLY —
   their standing was not re-derived.
5. Address navigation (grep of the pinned listing) located both bodies:
   0x008BD720 @ listing line 1282626; 0x00848EA0 @ listing line 1145803.
6. A run-local, read-only extractor (`tools/extract_p06_subregions.py`) streamed the
   pinned file and emitted ONLY lines whose parsed VA falls inside
   [0x008BD720, 0x008BD740) ∪ [0x00848EA0, 0x00848FC4) — end-exclusive, per
   CONTRACT §6. No out-of-region content was extracted or read.
7. Extracts cross-checked by direct re-read of the same source lines with the Read tool
   (subregion A: 4/4 rows verbatim; subregion B: first/last rows spot-checked verbatim).
8. In-window decode performed; all out-of-window control targets, callees and caller
   VAs recorded but NOT read.

## 3. FINDING A — the "thunk" 0x008BD720 dispatches to NOTHING

Admitted window 0x008BD720-0x008BD740 (end-exclusive) contains exactly 4 listed
instruction rows:

```
source_line | VA       | instruction
1282626     | 008bd720 | LEA EAX,[ECX + 0x18]
1282627     | 008bd723 | RET
1282628     | 008bd730 | MOV AL,byte ptr [ECX + 0x64]     <- separate body (INCIDENT-P06-I1)
1282629     | 008bd733 | RET
```

**Answer to (a): there is NO dispatch target VA.** The body of 0x008BD720 is exactly
`LEA EAX,[ECX + 0x18]; RET` — two instructions, 4 bytes, no JMP, no CALL. It is not a
dispatching thunk; it is a side-effect-free leaf getter that returns the interior
pointer `ECX + 0x18` to its caller (evidence_level: CONFIRMED, listing-level; the body
is fully contained in the admitted window; the question's "dispatch" premise is
REJECTED_WITH_EVIDENCE).

Consequences for the designed-but-not-executed bridge experiment #1 ("decode
FUN_008BD720 + the type-0x66 provider chain down to the NIF load"):

- The chain CANNOT continue through a callee of 0x008BD720 — it has none.
- When the scheduler invokes the pinned callback, the whole observable effect is
  "return &arg+0x18". The continuation is CONSUMER-SIDE: the code that calls this
  callback and uses the returned pointer, and/or the +0x18 sub-object of the
  request object.
- The bridge premise "0x008BD720 is the {0x66,A} request's callback (imm32 pin)" is
  inherited (cited, not re-derived) and is CONSISTENT with the body: an imm32-pinned
  pointer-returning accessor is a plausible scheduler callback shape (the scheduler
  resolves a handler/record at +0x18 of the request object). This package does NOT
  establish which object that is.
- Navigation (address search only, no caller region read): in the pinned listing
  0x008BD720 is called directly from 22 sites and loaded as an immediate at 3 sites
  (registration-shaped): `006B6D05 MOV EBX,0x8bd720`, `006C3FB0 MOV EBX,0x8bd720`,
  `006D44E8 MOV EDI,0x8bd720`. These 25 VAs are recorded in the Navigation Appendix
  for future admission; none was read. 0x008BD720 is NOT exclusively virtual — it has
  22 direct callers AND is address-taken (premise honored with evidence).

The precise remaining edge for the {0x66,A} chain: identify which registration site
belongs to the {0x66,A} scheduler and what consumes the returned &req+0x18 pointer.
See BARRIER_BACKLOG.json BARRIER-P06-1.

## 4. FINDING B — slot-consumer 0x00848EA0 semantics

Admitted window 0x00848EA0-0x00848FC4 (end-exclusive) contains 88 instruction rows,
VAs 0x00848EA0..0x00848FC2, contiguous with no undefined-byte gaps. All 88 VA deltas
match standard x86 encoding lengths for the listed mnemonics (encoding-consistency
control, section 6.3).

### 4.1 Semantics table (in-window evidence only)

| # | Element | In-window instructions (VA) | Semantics (evidence level) |
|---|---------|------------------------------|----------------------------|
| 1 | Entry / SEH | `PUSH -0x1; PUSH 0xa28300; MOV EAX,FS:[0x0]; PUSH EAX; SUB ESP,0x5c; ...; MOV FS:[0x0],EAX` (00848ea0-00848ec1) | MSVC SEH prologue; handler 0x00A28300 recorded, NOT read (CONFIRMED idiom) |
| 2 | Slot object | `MOV EDI,[ESP+0x80]` (00848ec7) | first stack argument; the function is NOT thiscall-on-the-slot — it receives the object by stack and wires ECX=EDI per call (CONFIRMED) |
| 3 | Flag query | `PUSH 0x1; MOV ECX,EDI; CALL 0x00745540; TEST AL,AL; MOV ECX,EDI; JZ 0x00848fec` (00848ed2-00848edf) | boolean kind-of-slot predicate 0x00745540(slot,1); FALSE -> 0x00848FEC (OUTSIDE window; recorded, not read). TRUE falls through to the chain below (CONFIRMED; matches bridge AMEND-4 flag-1 semantics) |
| 4 | Const vec | `FLD [0x00a7b25c]; PUSH ESI; FST/FST/FSTP -> [ESP+0x20/0x24/0x28]` (00848ee5-00848ef4) | a 3-float frame buffer initialized to (c,c,c), c = float const @0x00A7B25C (.data; value not read) (CONFIRMED stores; role idiom-level) |
| 5 | id2/property entry | `CALL 0x00745bf0; TEST EAX,EAX; JZ 0x00848fc6` (00848ef8-00848eff) | pointer getter on the slot object; NULL -> early exit to epilogue 0x00848FC6 (OUTSIDE window). THIS is the in-window entry of the bridge's id2/class-20006-tag-6 channel — the read itself is inside the callee, NOT in-window (CONFIRMED structure; property content NOT_CHECKED) |
| 6 | Lookup chain | `PUSH EAX; LEA ECX,[ESP+0x5c]; CALL 0x00843d60; MOV ECX,EAX; MOV [ESP+0x78],0x0; CALL 0x00844660; PUSH EAX; CALL 0x0043a550; MOV ECX,EAX; CALL 0x0072f580; LEA ECX,[ESP+0x58]; MOV EBP,EAX; MOV [ESP+0x78],0xffffffff` (00848f05-00848f31) | object-resolution chain 0x00843D60(&local,P) -> 0x00844660 -> 0x0043A550 -> 0x0072F580 -> EBP; `__try`-guarded (trylevel local [ESP+0x78]: 0 during the chain, -1 after) (CONFIRMED structure; "keyed lookup by id2" label inherited from bridge, cited) |
| 7 | Local op | `CALL 0x008e0110` with ECX=&[ESP+0x58] (00848f39) | call on a frame local; callee NOT read (address known to parent contract §5 A2 as "actual slot 008E0110" — no new claim here) |
| 8 | Guard | `MOV ECX,EBP; CALL 0x0072fce0; TEST AL,AL; JZ 0x00848fc4` (00848f3e-00848f47) | boolean predicate on the resolved object; FALSE -> 0x00848FC4 (OUTSIDE window, recorded) (CONFIRMED structure) |
| 9 | Payload read | `FLDZ` + 7 zero-stores; `PUSH/PUSH/PUSH; MOV ECX,EBP; CALL 0x0072fe30` (00848f49-00848f74) | three 12-byte float3 frame buffers, zero-initialized in-window, passed as out-params to 0x0072FE30(EBP,...) (CONFIRMED out-param idiom; the bridge's "3xvec3 list2 payload" provenance label is INHERITED standing, cited — the payload path goes through the unadmitted lookup chain) |
| 10 | Float param | `FLD [0x00a7b25c]` + const stores; `PUSH ESI; MOV ECX,EDI; CALL 0x00745690; PUSH ECX; FSTP [ESP]` (00848f79-00848f94) | float getter 0x00745690(slot, 0), result consumed as x87 st0 via the push-float idiom; another (c,c,c) const-vec store group (CONFIRMED idiom) |
| 11 | Compose | `LEA EAX,[ESP+0x20]; PUSH EAX; LEA ECX,[ESP+0x48]; PUSH ECX; LEA EDX,[ESP+0x70]; PUSH EDX; CALL 0x006c1f90; ...; ADD ESP,0x10` (00848f97-00848fbe) | 0x006C1F90(3 pointers + 1 float) — cdecl, 4 dwords, caller-cleans; returns EAX -> 12-byte float triple (bridge label: lerp; inherited, cited) (CONFIRMED call shape; semantics inherited) |
| 12 | Produce | `MOV ECX,[EAX]; MOV [ESP+0x2c],ECX; MOV EDX,[EAX+0x4]; MOV [ESP+0x30],EDX; MOV EAX,[EAX+0x8]; MOV [ESP+0x24],EAX; JMP 0x00848fc6` (00848fab-00848fc2) | the 12-byte result triple is copied into frame locals; control leaves via JMP to epilogue 0x00848FC6 (OUTSIDE window). The bridge's "store to slot+0x00" and the "R08 loop over 3 slots" live in the OUT-OF-WINDOW regions (epilogue / flag-2 machinery) — inherited standing, NOT re-derived here (CONFIRMED in-window flow; post-window disposition NOT_CHECKED) |

### 4.2 Answer to "which fields/property it reads"

In-window, 0x00848EA0 directly reads NO object field of the slot object. Its complete
in-window interface to the slot object is three direct (non-virtual) calls:
`0x00745540(this,1) -> bool`, `0x00745BF0(this) -> ptr (null-checked)`,
`0x00745690(this,0) -> float (st0)`. The per-slot `{u16@+0xC, float@+0x10}` accesses
attributed by the bridge to the FUN_00745540(2) path are NOT in this window — the
flag-1-false branch jumps to 0x00848FEC, i.e. beyond the window end (VARIANT V4,
rejected). The class-20006 property tag 6 hypothesis is therefore UNVERIFIED by this
package: the property read, if it exists, is inside 0x00745BF0 and deeper (outside
the admitted window). The slot object's CLASS is NOT_ESTABLISHED in-window (no vtable
deref, no RTTI, no ctor; the 0x00745xxx same-family call shape is noted but proves
nothing about class identity — premise preserved).

### 4.3 Answer to "where its data comes from" and the FAMILY-P/T merge question

Complete in-window data-source census:

1. the stack argument (slot object) — provenance: the ONLY in-listing direct caller is
   `0x004E55F7` (`CALL 0x00848ea0`, listing line 104568) — navigation only, NOT read;
   no imm32/address-taken use of 0x00848EA0 exists in the pinned instruction listing
   (data-section references cannot be seen in an instruction listing — scoped caveat);
2. float constant `[0x00A7B25C]` (static .data);
3. MSVC security cookie `[0x00B9D8D0]`;
4. `FS:[0x0]` (SEH chain);
5. return values of the 11 direct callees (all out-of-window).

**Merge answer: NO VFS-record-fed channel is visible in-window** (evidence_level:
CONFIRMED scoped negative). No file/registry/record reader, no VFS handle, no
record-array dereference appears in the admitted window. This does NOT prove
end-to-end absence — a VFS-fed channel, if real, enters through the recorded gap edges:
(i) the property provenance inside 0x00745BF0 (class-20006 tag-6 read), (ii) the
class-20006 property-tag-6 WRITERS (bridge proposal 2), (iii) the slot-object
provenance at caller 0x004E55F7. The bridge standing (cited) that templates.vfs is
consumed as a DEFINITION registry only within censused machinery is UNCHANGED; this
package did not promote it to instance-source.

## 5. INCIDENT-P06-I1 (procedural disclosure)

Window A (admitted by VA range 0x008BD720-0x008BD740) contains a second logical body at
0x008BD730: `MOV AL,byte ptr [ECX + 0x64]; RET` — a 2-instruction byte-getter leaf —
which was NOT declared in the contract body_entries. Per parent CONTRACT §6 this is
reported as an unforeseen-body incident: the extract preserves the raw content, NO
claims and NO further analysis are built on 0x008BD730, and no region beyond the
admitted VA ranges was opened. Actual counters therefore show 3 in-window logical
bodies vs 2 reserved (rows 92<=98, CALL 11<=14, candidates 4<=4 — all within reserve).
The package is marked COMPLETED_WITH_PROCEDURAL_INCIDENT for the parent to adjudicate.

## 6. Controls and self-checks (SELF_CHECK — executor's own, NOT independent audit)

6.1 Contract integrity: P06.json SHA256 matches the dispatch value. PASS.
6.2 Source pin integrity: SHA256 verified before extraction and re-verified at close;
    the extractor refuses to run on pin mismatch (it exited OK only after match). PASS.
6.3 Listing-internal encoding consistency: for all 88 window-B rows and 4 window-A
    rows, consecutive-VA deltas fit standard x86 encodings of the listed
    mnemonics/operands (e.g., `PUSH 0xa28300` 5B, `MOV EAX,FS:[0x0]` 6B, `FST [ESP+xx]`
    4B, `MOV [ESP+0x78],imm32` 8B, short `JZ` 2B vs `0F 84` 6B targets recomputable
    exactly). No undefined-byte gap inside window B; window A's inter-body gap
    (0x008BD724-0x008BD72F) is padding between declared bodies. PASS.
6.4 Extract fidelity: subregion A re-read directly from the pinned source (4/4 rows
    verbatim); subregion B spot-checked at first/last rows (verbatim). PASS.
6.5 Boundary discipline: the extractor parsed VAs and emitted ONLY in-range lines;
    every out-of-window target (3 control-flow, 11 callees, 3 data refs, 25 caller
    references) is recorded in CLAIMS/COUNTERS/HANDOFF and NONE was read. PASS.
6.6 Premise preservation: (i) identical shapes != common semantics — applied in C4;
    (ii) definition registry not promoted to instance-source — applied in C6;
    (iii) no direct caller != exclusively virtual — applied with evidence in C2
    (008BD720: 22 direct callers + 3 address-taken uses) and for 00848EA0 (1 direct
    caller, 0 in-listing address-taken uses — and the data-section caveat is stated,
    so "exclusively direct" is NOT claimed either). PASS.
6.7 No default-success fallback: question (a) resolved NEGATIVE against its own
    premise; the merge question answered as scoped-negative with explicit gap edges,
    not as a silent success. PASS.
6.8 Forbidden list: no EXE/payload/runtime access; no new Ghidra export; no old writer
    scripts (one new read-only run-local extractor); no frozen-root/config/skills/repo
    edits (all writes inside packages/P06_EXEC_R1); no publication (not assigned).
    PASS.
6.9 Real clocks: RUN_STARTED 22:21:29.355Z (Get-Date UTC); extraction and analysis
    22:21:29Z-22:27:38Z (first manifest real-clock stamp 22:27:38.348Z); final
    closure 22:27:52.985Z. DISCLOSURE: three embedded UTC stamps in the first writes
    of COUNTERS.json/GATES.json/REPORT (22:29/22:40/22:35) were estimates, not
    real-clock reads; they were corrected to values honestly bounded by the two
    adjacent real-clock readings (22:27:38.348Z, 22:27:52.985Z), and the artifact
    index + manifest were regenerated as the true final writes. Hard stop
    23:15:00Z not reached (~47 minutes margin). PASS (after correction).

## 7. Reserved vs actual counters

| Counter | Reserved | Actual | Note |
|---|---|---|---|
| bodies | 2 | 3 in-window (2 declared + 1 unforeseen) | INCIDENT-P06-I1; window-contained |
| instruction rows | 98 | 92 (A:4, B:88) | within reserve |
| CALL sites | 14 | 11 (A:0, B:11) | within reserve |
| candidate variants | 4 | 4 | exactly consumed (V1-V4, see COUNTERS.json) |

## 8. Citations (inherited standing — cited, NOT re-derived)

- `PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z/06_REPORT/DRAFT_FINAL_REPORT.md`
  L95-214: chain standing, CONTROLS_NOT_ESTABLISHED (slot-object class semantics),
  MODEL_ID_RECOVERED=YES, PLACEMENT_XYZ_RECOVERED=NO, the designed-not-executed
  discriminator text (L180-195).
- `.../06_REPORT/AMEND_LOG_R1.md` AMEND-4/AMEND-5 (normative): flag-1 vs flag-2 R08
  semantics — instruction-level CONFIRMED by this package's window (section 4.1 row 3).
- `.../06_REPORT/HANDOFF.md` L82-86: the two next-experiment proposals this package
  executed the smallest parts of; FAMILY-P/T merge wording.
- `.../06_REPORT/PE_MASTER_REVIEW.md` L29, L179 (grep-level only): callback imm32
  0x008BD720; provider-chain proposal.

## 9. Navigation appendix (address search only — NO region read)

Direct CALL sites of 0x008BD720 in the pinned listing (22):
0054F7BB, 0055000F, 00556FAD, 00556FC5, 00557030, 00557912, 0055792A, 0055794E,
005CB73A, 006B1E5A, 006B6DB9, 006C88C6, 006C88D5, 006D3BAE, 006D3BC8, 006D3BD7,
006D3CD6, 006D3CFE, 006D3D26, 006D3D3A, 006D4441, 006E68A8.
imm32 loads of 0x008BD720 (3, registration-shaped):
006B6D05 (`MOV EBX,0x8bd720`), 006C3FB0 (`MOV EBX,0x8bd720`), 006D44E8 (`MOV EDI,0x8bd720`).
Direct CALL site of 0x00848EA0 (1): 004E55F7.
Out-of-window control targets: 0x00848FEC, 0x00848FC4, 0x00848FC6.
Out-of-window callees: 0x00745540, 0x00745BF0, 0x00843D60, 0x00844660, 0x0043A550,
0x0072F580, 0x008E0110, 0x0072FCE0, 0x0072FE30, 0x00745690, 0x006C1F90.
Data refs: 0x00A28300 (SEH handler), 0x00A7B25C (float const), 0x00B9D8D0 (cookie).

All of the above are recorded for parent admission planning; none was semantically
read in this package.
