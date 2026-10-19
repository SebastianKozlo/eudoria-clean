# P12 REPORT — C1 final discriminator: the worklist producers (Front C)

Run: PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018 | Package: P12 | Executor: pe-reconstruction (child, NO_NESTED_TASKS)
Admission: Abff4b58618ac | Region 0x006C27A0-0x006C2830 (end-exclusive; 48 rows, source lines L648033-L648080, VA 0x006C27A0-0x006C282F) | Hard stop 2026-10-19T01:10:00Z respected (all stamps real clock).

## Scoped result

**VERDICT: the worklist is REGISTRY-FED.** Bodies 0x006C27A0 and 0x006C27F0 are same-family keyed-table
producers whose success path terminates in the campaign-standing object-resolution idiom
`PUSH table_DWORD; CALL 0x0043A550; MOV ECX,EAX; CALL 0x0072F580` — and **returns the 0x0072F580 product**
(body 1: CONFIRMED at its in-window RET; body 2: STRONGLY_SUPPORTED, terminal epilogue out-of-window,
stack-forced POP+RET-class tail). Per bridge standing (cited, not re-derived), 0x0072F580 is the
templates.vfs RB-tree keyed lookup — the **definition registry**.

**Where the value comes from — the three options discriminated (CLAIMS P12-C8a/C8b):**

1. **Registry walk: YES (success path).** Both producers *call the registry lookup* and return its result.
   The RB-tree walk itself lives inside the out-of-window callee; in-window evidence is the call chain.
2. **Container data: REJECTED as the return source; ACCEPTED as the KEY source.** Each body reads one DWORD
   from a global, row-indexed table — body 1: `M32[0xA857C8 + (w1 + idx1*10)*4]`, body 2:
   `M32[0xA85804 + (w2 + idx2*15)*4]` — where the column word `w` comes from a field (+0x0E/+0x0C) of the
   object returned by 0x0070ED80(arg 0x1F/0x20), unsigned-bounded (<10/<15, MOVSX+JNC: negative words take
   the fail arm), and the row index `idx` is returned by 0x006B22D0(this). That DWORD never reaches the
   return register: it is the sole visible argument to 0x0043A550, whose return becomes ECX for 0x0072F580.
3. **Other: partial.** Body 1's bound-fail arm returns the constant 0xBA5800 (sentinel-shaped; semantics
   UNKNOWN). Body 2's fail arm jumps to 0x006C2832, **out-of-window — its return value is NOT claimed**
   (shape-parallel with body 1 is UNVERIFIED; premise preserved).

**P11 edge closure:** P11 left open "whether the producers internally consult the definition registry —
the exact two admission candidates." Decided in-window: **YES, via CALL 0x0072F580.** The full C1 chain now
reads: `[EDI+0x8] object state` → `0x006B22D0 row index` + `0x0070ED80 column word` → **global table DWORD**
(0xA857C8 / 0xA85804) → `0x0043A550` key transform → **templates.vfs RB-tree lookup 0x0072F580** → worklist
element (append-staged per P11) → buffer-full arm → `{0x66,A}` pump 0x006B6C9D (P07 standing). The getter
0x007CE1E0 and all pump/callback machinery (0x0072FCE0, 0x0043C700, 0x0040B070, 0x0043E5B0, 0x006C3640,
0x008BD720) are **absent** from the 48 rows (scoped negative, window-bounded).

**Premise compliance:** the registry here is a DEFINITION registry — the worklist elements are definition-
source products, **not** instance records (definition registry ≠ instance source, preserved). The two
bodies' shape-identity was not used to transfer semantics (each body's facts derive from its own rows);
the P06/P04 idiom match is corroboration, not proof.

## Micro-findings kept honest

- **Dead first call:** in each body the first `0x006B22D0` return EAX is overwritten before any use
  (P12-C7). Iterator-advance hypothesis P12-H1 = UNVERIFIED (callee out-of-window).
- **Stack-balance ABI (P12-C5, STRONGLY_SUPPORTED):** 0x0070ED80 and 0x0043A550 each take exactly one
  pushed DWORD and pop it themselves — forced by the fixed `POP EDI/POP ESI/RET` epilogues balancing on
  both body-1 arms and body 2's in-window `POP EDI`.
- **Receiver plumbing (P12-C11):** ECX=this at every 0x0070ED80 call (`MOV ESI,ECX` is copy-only);
  this = the [EDI+0x8] value per cited P11.
- **Table geometry (P12-C9, arithmetic):** row strides 10 (body 1) / 15 (body 2) DWORDs; base delta
  0xA85804−0xA857C8 = 0x3C = 60 B = body 2's row size. Whether the tables are one logical array:
  UNKNOWN. First globals in the C1 chain (P11's window had zero).
- **UNKNOWNs preserved:** this-object identity; 0x0070ED80's returned object and args 0x1F/0x20;
  0x0043A550 transform; 0x006B22D0 semantics/statefulness; table contents (data barrier — not in saved
  corpus; EXE/.data read FORBIDDEN); 0xBA5800 semantics; body 2 fail arm; enclosing loop (no back-edge
  in-window).

## Window boundary handling

Region treated as **begin-inclusive/end-exclusive** [0x006C27A0, 0x006C2830) per parent CONTRACT §6
("VA begin/end-exclusive"); this yields exactly the reserved 48 rows (L648033-L648080). Consequence: body 2's
terminal rows 0x006C2830 (POP ESI) and 0x006C2831 (RET) and its fail-arm target 0x006C2832 are
out-of-window — recorded in HANDOFF, not read; body 2's return therefore graded STRONGLY_SUPPORTED
(stack-forced), body 1's CONFIRMED. If the parent intended an inclusive end, the delta is those 1-2 rows and
no claim depends on them.

## Incidents

**One disclosed navigation over-display (process incident, no semantic use):** the boundary-location
address search (`^006c27|^006c28`, navigation per contract §2/§6) returned 166 terminal rows, i.e. wider
than the admitted region: it incidentally displayed two sibling bodies before the window
(0x006C2700, 0x006C2750), body 2's out-of-window tail/fail arm (0x006C2830-0x006C2839), and further family
entries (0x006C2840, 0x006C2870, 0x006C28A0, 0x006C28F0...). Handling: extract contains ONLY the 48
in-window rows (read-back verified verbatim); **zero claims derive from out-of-window rows**; body 2's
fail-arm value and epilogue are explicitly NOT claimed despite the incidental display; all incidentally
displayed entry VAs are listed in HANDOFF for the parent's admission ledger. No unforeseen body exists
**in-window** (0 in-window incidents; row census: exactly the 2 declared entries).

## Position in the campaign

Front C's C1 question closes at this scope: the pump's worklist is fed with registry-lookup products keyed
by global-table DWORDs — the definition-resource side of the placement chain is now connected
end-to-end at instruction level from object state to registry record: `state → table key → registry
record → worklist → {0x66,A} pump`. What remains open for MODEL_INSTANCE_BINDING is the consumer side
(P11/P07 targets: 0x006B4120, 0x006B6CB9+, pump continuation 0x006B6C9F+, 0x0043E5B0/0x006C3640 queue
consumers, callback 0x008BD720) and the key-type edge (0x0043A550). No instance edge, no world transform,
no historical values are claimed here.

## Counters (actual vs reserved)

2/2 bodies | 48/48 instruction rows (no overshoot) | 10/10 CALL (4 distinct targets: 0x0070ED80 ×2,
0x006B22D0 ×4, 0x0043A550 ×2, 0x0072F580 ×2) | 2/2 candidates | 2 JNC (1 out-of-window target
0x006C2832) | 2 RET in-window | 3 absolute constants (0xA857C8, 0xA85804, 0xBA5800) | 2 global table reads,
2 object word-field reads, 0 writes, 0 virtual calls, 0 float instructions | 0 unforeseen in-window bodies
| 1 disclosed navigation over-display incident | EXE_READ_BYTES=0, RUNTIME_ACTIONS=0.

## Standing

WORLD_XYZ_RECOVERED=NO | HISTORICAL_PLACEMENT=NOT_ESTABLISHED | CURSOR_SOURCE_MEDIUM=UNKNOWN |
CANONICAL_GATE_EFFECT=NONE. New window-scope standing: P12-C1..C12 (CLAIMS.json); inherited cited
standing unchanged: P07-C3 pump chain, P11 append-buffer/pump-entry structure, bridge 0x0072F580/0x007CE1E0.

## Evidence

Verbatim extract EXTRACT_REGION_006C27A0_006C2830.txt (sha256 0CC0F24F1066BA3BF32C5D8435B263486F2536BF4E84062BD2B48F46BDDEF640,
2435 B), built programmatically from source lines L648033-L648080 of GHIDRA_H5_VTABLE2.txt (sha256
642CC29A01B8AD6F783E82E14DA4A61FA00BA6A3EC6DF98EDFF28AC25CC1D8DB, verified before read and re-checked
after extraction; read-back verified 48/48 rows verbatim). Claim citations use source line numbers.
Context cited, not re-derived: P11 REPORT.md, P07 REPORT.md, P06 §4.1 element #6, P04 callsite table.
Clock: all stamps PowerShell [DateTime]::UtcNow.

## SELF_CHECK (executor's own — NOT independent PE-MASTER audit)

- [x] Window compliance: semantic read restricted to the 48 admitted rows; boundary located by address
      search (navigation); the wider terminal display disclosed as an incident, zero claims from it.
- [x] Counters honest: 2/2, 48/48, 10/10, 2/2 as measured; boundary arithmetic (48 = end-exclusive
      window) documented; no overshoot.
- [x] No unforeseen in-window body (both entries declared; census verified).
- [x] Out-of-window discipline: all out-of-window targets recorded with exact VAs in HANDOFF
      (callees 0x0070ED80/0x006B22D0/0x0043A550/0x0072F580; branch target 0x006C2832; tail
      0x006C2830/0x006C2831; P11 leftovers; over-displayed sibling entries); none read.
- [x] Premises preserved and cited per claim (4/4).
- [x] No forbidden action: no EXE/payload read, no new Ghidra exports, no old scripts, no frozen-root/
      config/skill/repo writes; writes only in this fresh package root.
- [x] Real clock tools for every timestamp; RUN_STARTED.json materialized FIRST; contract hash verified
      before start and copied byte-identical (re-hashed).
- [x] Honest UNKNOWNs: all listed as barriers/hypotheses; body 2 return graded STRONGLY_SUPPORTED not
      CONFIRMED; fail-arm value not claimed; no promotion of definition-registry products to instance
      records.
