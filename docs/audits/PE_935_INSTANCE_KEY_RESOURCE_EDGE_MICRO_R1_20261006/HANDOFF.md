# HANDOFF — PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006

## Run status

- RUN_STATUS: COMPLETE (bounded micro-run; package written; NO commit/push —
  persistence is a separate later phase per the human dispatch)
- RUN_ID: PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006 · RUN_CLASS: BOUNDED_STATIC_RE
- BASE_SHA: 3921dbe2a43a9181f8a50fa5242d8586c85896b6 (== origin/master == actual remote, verified)
- RESULTING_SHA: NONE (no commit performed in this phase)
- REMOTE_SHA: 3921dbe2a43a9181f8a50fa5242d8586c85896b6 (unchanged)
- EXE: E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 / 8,015,872 B (re-verified everywhere)

## Science result

- **OUTCOME (exact §5 string): `BOUND_REACHED`**
- Receiver identity (selected branch): the ClientMovableObject ctor this (RTTI
  `.?AVClientMovableObject@@` calibration + 4-edge byte chain, CTRL_B).
- KEY_ROLE: runtime identity — PROVEN map-identity use at the insert site
  (mgr1+0x10 hash_map, instance-key → the same instance object); identity-carrying
  pass-through on the ctor branch ([SF+0x14] → the key-carrying 0x14-B object at the
  boundary). FUN_00414130 is a SHARED +0x74 offset reader (NOT class-specific:
  6 callsites, ≥3 receiver kinds: ClientMovableObject / GameClient singleton /
  dereferenced [x]).
- RESOURCE_EDGE_STATUS: NOT_ESTABLISHED_IN_EXAMINED_PATH (no
  resource/template/model consumer reached or demonstrated anywhere in the examined
  path; the LEAD families FUN_0072F580/FUN_006C9700/FUN_006CB6F0/FUN_006CB020 are
  NOT on the examined chain).
- Resource kind/identity: **UNKNOWN**.
- First missing edge (NEXT_INPUT/EDGE): the SceneFeederObjectExtraData chain —
  FUN_0064B1E0's base ctor FUN_007C8780, FUN_007B6A80's registration semantics, and
  the consumers of ExtraData+0x10 (the carried instance key). Second-ranked lead
  (no recommendation weight): the UNRESOLVED site 0x0045A08B → FUN_00853d00
  (mgr1-family query). NEXT_EXPERIMENT_AUTHORIZED = NO; DESIGNED_NOT_EXECUTED.
- Counted functions: **6 budgeted** (FUN_00414130, FUN_00528E50, FUN_005247C0,
  FUN_00509330, FUN_00856190, FUN_00401360) + **1 disclosed over-budget probe**
  (FUN_0064B1E0, 26-B body — deviation disclosed, non-load-bearing,
  FUNCTION_LEDGER row 7 / QC_REPORT Q7) + 1 bounded classification probe
  (FUN_004157B0 head, row 8). Callsites: 6 census (4 NEW), 3 shortlisted,
  2 branches examined. Further call edges from the selected callsite: 2 (budget
  respected; the 3rd edge recorded as the boundary stop).

## Targeted QC (§5 controls)

- (a) getter offset +0x74→+0x78 mutation, EXE untouched: clean PASS → mutated FAIL — **PASS (mandatory control)**
- (b) receiver/identity edge removal (the ctor receiver chain, 4 byte-pinned edges):
  clean PASS → mutated-copy FAIL — **PASS** (the claim genuinely depends on the edge)
- (c) resource-join negative on the REAL key-to-map operation (FUN_00856190):
  map pins hold + ZERO resource-family E8s in the body + falsifier (injected fake
  E8→FUN_0072F580) DETECTED — **PASS**
- Identity/recount/boundary re-reads: EXE SHA/size MATCH (QC time), census recount
  6/6, getter boundary RET/CC confirmed. Overall: **QC_PASS** (SELF_CHECK; one
  disclosed budget deviation in Q7; no independent-QC claim; Desktop post-audit
  NOT_PERFORMED / NOT_CHECKED).

## Package census (this phase)

- Changed paths (this run's writes): exactly the files under
  `docs/audits/PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006/` (the package:
  9 root documents + 2 CSV ledgers + 1 shortlist CSV + 01_RAW/ (10 files) +
  03_SCRIPTS/ (7 files) + COMMITTED_PACKAGE_MANIFEST_SHA256.csv). AUDIT_ENTRYPOINT.md
  NOT edited; foreign untracked paths untouched; no tracked file outside the package
  touched.
- MANIFEST_ROWS: **27** (COMMITTED_PACKAGE_MANIFEST_SHA256.csv generated LAST; scope =
  every physical file under this package minus the manifest itself; in-process
  bijection verification: zero missing/extra/duplicate/size/SHA mismatches).
  **The entrypoint row is NOT in the manifest** (the entrypoint file was not edited
  in this phase — per the human dispatch the persistence phase will add the row and
  REGENERATE the manifest including it; the bijection/hash verification must be
  repeated then).
- PHYSICAL_PACKAGE_FILE_COUNT: **28** (27 manifest rows + the manifest itself).

## p) Persistence instruction for the persistence phase

Per the human dispatch: commit/push is authorized ONLY within this contract's
allowlist; the persistence phase must (1) add the proposed AUDIT_ENTRYPOINT.md row
below (newest-first LATEST RUNS table), (2) REGENERATE the manifest including the
updated AUDIT_ENTRYPOINT.md row, (3) path-limited commit + push + verify
LOCAL_HEAD == origin/master == actual remote, (4) report the exact pushed SHA.
DA1 remains a PRESENT-ACCEPTED disclosed exception (not evidence of prior
authorization; DA2 = P3 backlog, not re-ordered).

### Proposed AUDIT_ENTRYPOINT.md row (NEW, newest-first; to be adapted by the persistence phase with the actual commit SHA discovery string)

```markdown
| (this commit; discover with `git log -1 -- docs/audits/PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006`) | PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006 (RUN_CLASS BOUNDED_STATIC_RE; BASE 3921dbe2; executor pe-reconstruction, targeted SELF_CHECK QC QC_SCOPE=SELF_CHECK_INSTANCE_KEY_RESOURCE_EDGE — no independent-QC claim; PE-MASTER direct dispatch, NO_NESTED_TASKS; two-phase flow: phase 1 = this package (NO commit by the executor), phase 2 = persistence (entrypoint row + manifest LAST + commit/push within the allowlist); STATIC-ONLY — the client never ran; EXE identity re-verified E7785430.../8,015,872 B; DA1 present-adjudication PRESENT_EXCEPTION_DISCLOSED saved verbatim in GOVERNANCE_DECISION.md) | `PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006/` | the instance-key→resource-edge micro-run: FUN_00414130 re-pinned from EXE (8B 41 74 C3 @0x00414130, mov eax,[ecx+0x74]; ret; Ghidra-confirmed body [[00414130,00414133]]) — the E8 census finds 6 direct callsites (2 BASE-published re-verified 0x00528FD9/0x008561AC + 4 NEW: 0x004569D3/0x00456BEB/0x0045723E/0x0045A08B; 0 E9-thunks, 0 address-taker dwords, Ghidra references == exactly 6, all UNCONDITIONAL_CALL, all PROVEN_EXACT instruction starts); FUN_00414130 is a SHARED +0x74 OFFSET READER, NOT class-specific: the 4 new sites' receivers are the GameClient singleton [0x00B9FE5C] (0x88 B, ctor FUN_004157B0, vtable 0x00A79F18 → RTTI .?AVGameClient@@ — DIFFERENT_OBJECT proven) or an unresolved [EBX] deref; shortlist = 3 (ctor SAME_MOVABLE_OBJECT_PROVEN selected; map-insert SAME proven in the examined CREATE chain; 0x0045A08B UNRESOLVED strongest new lead → FUN_00853d00 mgr1-family query); the selected branch traced 2 further edges: FUN_005247C0 (SF factory wrapper — NO lookup by key anywhere in the body; key passes through) → FUN_00509330 (SF ctor: [SF+0x14]=key @0x0050937E, [SF+0x8C]=holder, [SF+0x30] NiNode re-verified) — the key's next edge FUN_0064B1E0 = the 3rd further edge = BUDGET BOUNDARY → STOP (disclosed over-budget 26-byte probe: the 0x14-B object = RTTI .?AVSceneFeederObjectExtraData@@, key at +0x10, registered into the SF NiNode via FUN_007B6A80 — NON-CANONICAL LEAD, not load-bearing); the insert site = RUNTIME IDENTITY MAP (mgr1+0x10 STLport hash_map, key=[value+0x74], value=the instance itself, duplicate→deleting dtor) — the resource-join NEGATIVE (zero resource-family E8s in the body; falsifier: injected fake E8→FUN_0072F580 detected); OUTCOME = BOUND_REACHED — the key is used only for runtime identity/map operations in the examined path, NO resource/template/model consumer reached; WORLD_XYZ_RECOVERED=NO, STATIC_BUILDING_CHANNEL=NOT_ESTABLISHED, HISTORICAL_INSTANCE_DATA_RECOVERED=NO, NEXT_EXPERIMENT_AUTHORIZED=NO; NEXT_INPUT/EDGE = the SceneFeederObjectExtraData chain (FUN_007C8780 + FUN_007B6A80 + readers of ExtraData+0x10), DESIGNED_NOT_EXECUTED; QC controls (a) getter +0x74→+0x78 mutation clean PASS→FAIL, (b) receiver 4-edge chain removal clean PASS→FAIL, (c) resource-join negative with falsifier PASS; QC_PASS (SELF_CHECK; one disclosed budget deviation: the FUN_0064B1E0 26-byte boundary probe) |
```

## Honest NOT_CHECKED / UNKNOWN

- Resource kind/identity for the carried key: UNKNOWN (consumers unexamined).
- FUN_00853d00 semantics; FUN_004A9850; FUN_007C8780; FUN_007B6A80; ExtraData
  consumers; the 4 new containing-function bodies; indirect/inlined +0x74 readers
  anywhere: NOT_CHECKED.
- External Desktop post-audit: NOT_PERFORMED (until after publication).
- PE-MASTER review of this run: NOT_PERFORMED (a later separate step; the current
  handoff is the executor's own SELF_CHECK — not an independent audit).

HARD_STOP = YES (after the package; no further work authorized in this dispatch).
