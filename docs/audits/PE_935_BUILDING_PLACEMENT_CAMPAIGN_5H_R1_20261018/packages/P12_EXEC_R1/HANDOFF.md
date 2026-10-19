# P12 HANDOFF — out-of-window targets for parent admission (NOT read by P12)

All VAs below are outside the admitted region 0x006C27A0-0x006C2830 (end-exclusive). P12 derived **zero**
claims from any of them. Priority ordering is the executor's recommendation for any future admission.

## Priority 1 — direct semantic edges of the P12 verdict

| VA | What it is (from in-window call/branch rows only) | Why it matters |
|---|---|---|
| **0x0043A550** | callee taking the table DWORD (sole pushed arg, callee-pops) and returning the ECX argument for the registry lookup 0x0072F580; called at L648049/L648077 | The key-type edge: decides what the table DWORDs ARE (resource ID / handle / index). Smallest decisive next admission (P12-B1). Cited idiom context: P06 §4.1 element #6, P04 callsite 0x0067C8A8. |
| **0x0070ED80** | callee with 1 pushed DWORD arg (0x1F at L648037 / 0x20 at L648063), ECX=this at call; returns pointer whose word fields +0x0E (body 1) / +0x0C (body 2) are read as the column index | Identifies the column-selector object and the meaning of args 0x1F/0x20 (P12-B3). |
| **0x006B22D0** | thiscall on the producer's this, no stack args, returns the row index; called 2× per body, first return EAX dead (L648040/L648044, L648066/L648070) | Row-index semantics; iterator-advance hypothesis P12-H1 (UNVERIFIED) lives here (P12-B4). |
| **0x0072F580** | the terminal lookup both producers call (L648051/L648079); bridge standing: templates.vfs RB-tree keyed lookup | Only needed if the bridge attribution is challenged (P12-B2); large body expected. |

## Priority 2 — body 2 completion (10-byte window suffices)

| VA | What it is | Why it matters |
|---|---|---|
| **0x006C2830 / 0x006C2831** | body 2's terminal rows (stack-forced POP+RET-class tail; opcodes not claimed) | Would upgrade body 2's return from STRONGLY_SUPPORTED to CONFIRMED. |
| **0x006C2832** | body 2's bound-fail arm target (JNC at L648068/0x006C2809) | Body 2's fail return value is currently NOT claimed; shape-parallel with body 1's 0xBA5800 is UNVERIFIED. A ~0x10-byte window covers the arm. |

## Priority 3 — family and prior-package leftovers

| VA | What it is | Why it matters |
|---|---|---|
| 0x006C2700, 0x006C2750 | sibling producer-family entries BEFORE the window (incidentally displayed by the navigation over-display; not read, no claims) | If the family shares the 0x0043A550→0x0072F580 tail (plausible, UNVERIFIED), the [EDI+0x8] object exposes a getter family over adjacent tables (0xA855D0, 0xA85778 visible in the over-display as VA mentions only). |
| 0x006C2840, 0x006C2870, 0x006C28A0, 0x006C28F0 | further family entries AFTER the window (same disclosure status) | Same as above; 0x006C28A0+ region also contains loop-shaped code (displayed, not read). |
| 0x006B4120, 0x006B6CB9+, 0x006B6C9F.., enclosing head <0x006B6C1B | P11 HANDOFF leftovers, unchanged, still unadmitted and unread by P12 | Pump consumer / enclosing loop structure (P12-B9). |

## Data barriers (no admission can fix under campaign rules)

- Table contents at **0xA857C8 / 0xA85804** and sentinel object at **0xBA5800**: not in the saved text
  corpus; recovering values would require EXE/.data access = FORBIDDEN. Parent may check the catalog for
  prior saved exports documenting .data around 0xA85xxx / 0xBA5800 (P12 did not open files beyond the
  pinned source and cited reports).

## Over-display disclosure (for the parent's ledger)

The boundary-location navigation search incidentally displayed rows outside the region
(0x006C2700-0x006C2796, 0x006C2830-0x006C28FF terminal output). P12's extract contains only the 48
in-window rows; all claims cite in-window lines only. The displayed sibling VAs are listed above so the
parent can weigh them in future admission decisions; their instruction details are deliberately NOT
re-quoted here.
