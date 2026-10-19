# P11 REPORT — C1 pump upstream (Front C, RETRY 1 of 1)

Run: PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018 | Package: P11 | Executor: pe-reconstruction (child, no delegation)
Attempt: RETRY 1 of 1 — prior session materialized only CONTRACT.json + RUN_STARTED.json (both preserved byte-identical, sha256 369059f6… / 8c0203a3…; retry marker RUN_STARTED_RETRY1.json at 2026-10-18T23:36:51Z, real clock).

## Scoped result

**The worklist is a stack-local, DWORD-stride append buffer, and its elements come from a container field.**
Bodies 0x006B6C1B (stage A, source rows 632937–632958) and 0x006B6C5C (stage B, rows 632959–632980) are
shape-identical append stages. Each stage: helper call 0x006B4120 on a stack temp ([ESP+0x48]) → producer method
call on **[EDI+0x8]** (stage A: 0x006C27A0; stage B: 0x006C27F0) → produced EAX stashed to pending slot
[ESP+0x14] → bounded append into the local list (cursor [ESP+0x38], bound [ESP+0x3c]; store `[ECX],EAX`,
stride `ADD ECX,0x4`) when cursor != bound; equality redirects control (A→B re-init via JZ 0x006B6C47;
B→pump entry via JZ 0x006B6C88).

**Pump entry condition (CONFIRMED-as-instruction):** the {0x66,A}-forming pump 0x006B6C9D (P07-C3) is entered
exactly when the stage-B append finds cursor == bound — the pump is the overflow/fallback arm of this append
state machine, not a per-element registry walker. The stage-B success exit JMP 0x006B6CB9 leaves the window
(recorded, not read). Window's last row is the pump entry instruction 0x006B6C9D PUSH 0x1 (declared in-region);
continuation ≥0x006B6C9F not read.

**Registry question, split answer:**
1. **Pump trigger** = the local append state machine — in-window this is "another source" than the registry
   (CONFIRMED-as-instruction).
2. **Pump A-data** = per standing (P07-C3 + bridge, cited not re-derived): keyed lookup on the templates.vfs
   RB-tree definition registry → [record+0x08] A-read → {0x66,A} pair → enqueue. Out-of-window here.
3. **Worklist feed** = [EDI+0x8] producer methods with **zero in-window registry access**: the 45-row window
   contains zero global/absolute memory references and zero calls to any known registry/pump machinery VA
   (no 0x0072F580, 0x007CE1E0, 0x0043C700, 0x0040B070, 0x0043E5B0, 0x006C3640, 0x008BD720) — scoped
   negative, window-bounded.

So, of the question's three provenance options (registry / template objects / container field), the in-window
evidence supports only **container field [EDI+0x8]** (via two out-of-window producers). Whether those producers
internally consult the definition registry is **undecidable in-window** — they are the exact two admission
candidates. Premise preserved: even a registry-backed producer finding would make the registry a DEFINITION
source of elements, not an instance source; the PUSH 0x1 mirror between stage entries and the pump entry is
treated as shape only (no "third twin stage" claim; hypothesis P11-H2 unclaimed).

Micro-unknowns kept honest: EBP's role (skip-slot marker compared against cursor; store skipped, cursor still
advances — behavior CONFIRMED-as-instruction, EBP value UNKNOWN); EDI object identity UNKNOWN; helper 0x006B4120
role UNKNOWN (receives incoming ECX, which on the stage-B-from-A path is the stage-A cursor); loop vs
straight-line enclosing flow UNKNOWN (no back-edge in-window).

## Position in the campaign

Front C closes its C1 question at window scope: the worklist feeding the pump machinery is a stack-local append
buffer whose element source is the [EDI+0x8] container (producer semantics behind barrier). The pump's registry
consumption remains P07-C3/bridge standing; P11 adds the missing structural fact that the pump is the full-buffer
fallback arm, which constrains any future pump/consumer model: {0x66,A} formation is entered on buffer-full, with
the just-produced-but-unappended element stashed at [ESP+0x14] (pump-input hypothesis P11-H1, unclaimed).
Out-of-window targets for parent admission recorded in HANDOFF.md: 0x006C27A0, 0x006C27F0 (priority 1),
0x006B4120, 0x006B6CB9, 0x006B6C9F.., enclosing function head (< 0x006B6C1B, VA unlocated).

## Counters (actual vs reserved)

2/2 bodies | 45/60 instruction rows (no overshoot; rows 632937–632981) | 4/8 CALL (distinct targets 3:
0x006B4120 ×2, 0x006C27A0, 0x006C27F0) | 2/2 candidates (producers) | 6 branch instructions (JZ ×4, JMP ×2;
1 out-of-window branch target 0x006B6CB9) | 0 unforeseen in-window bodies, 0 incidents | memory census: 16
stack-slot accesses, 2 object-field reads ([EDI+0x8] ×2), 2 indirect stores, 0 global refs.

## Standing

WORLD_XYZ_RECOVERED=NO | HISTORICAL_PLACEMENT=NOT_ESTABLISHED | CURSOR_SOURCE_MEDIUM=UNKNOWN |
CANONICAL_GATE_EFFECT=NONE. New standing at window scope: P11-C1..C8 (see CLAIMS.json);
STANDING_INHERITED unchanged (P07-C3, bridge).

## Evidence

Verbatim extract EXTRACT_REGION_006B6C1B_006B6C9D.txt (sha256 cda76004453d5ca7a6390e6bee969079168c2e25f58c0e9a4d8838c61987cfae),
built programmatically from source lines 632937–632981 of GHIDRA_H5_VTABLE2.txt (sha256 642CC29A…, verified
before read; admission ID Ae2bd704a017c) and read-back verified. Claim citations in CLAIMS.json use source line
numbers. Clock: all stamps PowerShell [DateTime]::UtcNow; hard stop 2026-10-19T00:55:00Z respected.

## SELF_CHECK (executor's own — NOT independent PE-MASTER audit)

- [x] Window compliance: semantic read restricted to the 45 admitted rows; boundary location by grep
      (^006b6c1b, ^006b6c9d) = navigation only; 15-line format header peek (no code semantics).
- [x] Counters honest: 2/2, 45/60, 4/8, 2/2 reported as measured; one in-run arithmetic slip
      (stack-slot census 26→16) caught and corrected before finalization.
- [x] No unforeseen in-window body: 45 rows, all inside the two declared stages + the declared in-region
      pump entry row; 0 incidents.
- [x] Out-of-window discipline: 5 out-of-window targets recorded with exact VAs, none read.
- [x] Premises preserved and cited per claim (4/4).
- [x] No forbidden action: no EXE/payload read, no new Ghidra exports, no old scripts, no frozen-root/
      config/skill/repo writes; writes only in the package root.
- [x] Real clock tools for every timestamp; retry marker materialized; original two files preserved
      byte-identical (hashes recorded in SOURCE_PINS.json).
- [x] Honest UNKNOWNs: producer semantics, EDI identity, helper role, EBP role, loop structure, pump input —
      all recorded as barriers/hypotheses, none promoted.
