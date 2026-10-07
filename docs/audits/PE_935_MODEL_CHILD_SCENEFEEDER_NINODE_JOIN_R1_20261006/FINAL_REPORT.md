# FINAL_REPORT — PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006

RUN_CLASS: BOUNDED STATIC_RE · Era: PCG 9.3.5 · MODE: STATIC-ONLY (klient nigdy nie
działa; no client launch, no runtime, no network, no payload/VFS/BNT/NIF opening).
Executor: pe-reconstruction (PE-MASTER direct dispatch, NO_NESTED_TASKS).
BASE_SHA 24f45e0108b922c26ff584fee9ef7749de0390b6 (== origin/master == actual remote,
verified at preflight: fetch query 2026-10-06T22:49:05-07:00, all three SHAs equal).
EXE: D:\Eudoria_Reconstruction\pcg_install\Entropia.exe = 8,015,872 B /
SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (re-verified at
preflight, inside every analysis tool via fail-closed import, and at QC time).
No Ghidra project used: GHIDRA_PROJECT_USED = NONE (byte-level analysis only: own PE
mapper + capstone 5.0.7 + independent rel32 arithmetic; no program database created
or published).

---

## 1. The one question and the answer

**QUESTION (contract §0):** czy na jednej zbadanej ścieżce PCG 9.3.5 wynik o
fizycznie ustanowionym pochodzeniu model/resource zostaje związany jako visual child
z dokładnie tym samym NiNode pointerem, który pochodzi z badanego SceneFeeder+0x30?

**ANSWER — SCIENCE OUTCOME = PARENT_FOUND_CHILD_UNRESOLVED.**

1. A JOIN SITE was found and byte-proven on ONE examined path — the
   ArkClientLocalDynamic construction chain (FUN_006A3930):
   - the SF is created by the same factory as the SF island's (FUN_005247C0
     @0x006A39ED, stored at [ACLD+0x18] @0x006A39F6);
   - an ArkModelManagerMain (new 0x130 -> FUN_006C0D50 @0x006A3A77, class vtable
     canon from the prior bridge run) is created and passed to the SF-class method
     FUN_0050A310 @0x006A3A9D;
   - FUN_0050A310 stores the manager at [SF+0x20] @0x0050A3AC, derives a child
     object via FUN_006C66D0(manager) @0x0050A3AF, and at 0x0050A3E9..0x0050A3F7
     calls NiNode vtable slot 41 with receiver = **[SF+0x30]** — the EXACT NiNode
     pointer of that path's SF instance — and arguments (child, 0).
   - NiNode vtable slot 41 = FUN_007B5810; its body was byte-proven against the
     Gb12 NiNode::AttachChild fingerprint (the run's ONE oracle mechanism):
     child NULL-guard, refcount inc [child+4] (x2), an AttachParent-shaped call on
     the child passing the parent (direct call FUN_007BF470 — body NOT decoded),
     children-array insertion into the m_kChildren object at NiNode+0xC8
     (base +0xCC / alloc +0xD0 / used +0xD4 — consistent with the independent
     slot-17 GetObjectByName canon), both AddFirstEmpty and append-with-growth
     branches present, refcount dec (x2) with zero-destroy via the child's vtable
     slot 1. JOIN_OPERATION_STATUS = STRONGLY_SUPPORTED (NOT CONFIRMED: the PCG
     engine generation is not era-exact with the oracle — the same status ceiling
     as the slot-17 canon — and the AttachParent-shaped inner body is undecoded).
2. PROOF B (EXACT_PARENT) = CONFIRMED for the examined ACLD-path SF instance
   (receiver provenance byte-traced; no ECX clobber between the [SF+0x30] load and
   the virtual call). SCOPE: this is an SF of the SAME class (SceneFeederObject,
   vtable 0x00A7D458) and the SAME creation chain (FUN_005247C0 ->
   FUN_00509330 -> [SF+0x30] = new NiNode) as the contract's SF island — but a
   DIFFERENT INSTANCE from the SF-island's CMO+0xC0 holder. On the SF-island's own
   CMO path, NO model-child join was found in the examined chain (see 3).
3. PROOF A (CHILD_PROVENANCE) = UNRESOLVED. The child is ONE getter away from the
   ArkModelManagerMain (FUN_006C66D0 — NOT decoded; the function budget was
   exhausted at 8/8). The manager's own model/resource provenance was NOT traced
   to a physically established model/resource operation on this path. No
   CONFIRMED_MODEL_DERIVED claim is made. PROOF D (VISUAL_ROLE) = UNRESOLVED (no
   physical visual-role proof; per the binding anchor constraints, a resource-derived
   child may be VFX — a separate proof is required and was not performed).
4. INSTANCE_MODEL_NODE_JOIN = **NOT_ESTABLISHED** (A, D unresolved; C
   STRONGLY_SUPPORTED; the status algebra does not average up). RUNTIME_JOIN_OBSERVED
   = NO (always, static-only).
5. Separately established (its own status, no join promotion):
   SAME_INSTANCE_TRANSFORM_RELATION = CONFIRMED_STATIC (path-conditional): on the
   SF-island CMO-ctor path, FUN_00509850 (called @0x00529050 with the SF as
   receiver) applies the SF position/rotation/scale to the SAME-INSTANCE SF+0x30
   NiNode's m_kLocal (translate +0x5C..0x64 = pos x100, rotation 9 dwords
   SF+0x4C -> +0x38, scale |SF+0x70| -> +0x68). Per the binding constraints,
   child relation ≠ transform application — this is recorded as a transform
   relation, NOT a child binding.

## 2. What was examined (budgets: 8/8 functions, 6/6 edges, 4/4 candidates, 1/1 oracle)

Two examined paths, from the declared anchors (PRE_REGISTERED_ANCHORS.md):

**PATH 1 — the SF-island CMO-ctor path (parent side):** PA1–PA4 re-pinned from the
EXE (all MATCH prior canon). NEW: the CMO ctor continuation (after the pinned
FUN_005094C0 callsite) calls three further SF methods: FUN_00509510 (rotation-like
setter: triple -> SF+0x74/0x78/0x7C + a converted 9-dword block -> SF+0x4C),
FUN_00509070 (setter: triple -> SF+0x80/0x84/0x88), and FUN_00509850 (the SF update).
FUN_00509850 was fully decoded: it operates on the [SF+0x20] model-manager object
via the 0x6C-family methods (FUN_006C0EC0/ED0/FA0/FB0), applies the transform to the
SF+0x30 NiNode's m_kLocal (SAME_INSTANCE_TRANSFORM_RELATION above), and then calls
FUN_007BF500 on the NiNode with (caller-float, 1). FUN_007BF500 was decoded: an
update-like operation (vtable[19] virtual call; a conditional virtual call on
[this+0x24] via its vtable[45]) with NO child argument and NO children-array
access — REJECTED as an attach (candidate CAND-1). The transform write itself was
examined and REJECTED as a join (CAND-2: transform application is not a child
binding). The SF-ctor ExtraData registration (re-pinned PA2) was re-classified for
the ledger: CAND-3 = NON_MODEL_CHILD (metadata; not visual).

**PATH 2 — the ArkClientLocalDynamic construction path:** reached from the declared
SF-creation-container census (LINK30 C9 listed FUN_006A3930 among the 5 SF holders;
its full decompile is prior BASE evidence — the bridge R09). Byte re-pins of its
chain: the SF factory call, [ACLD+0x18] store, the SF SetPosition/Rotation calls
(FUN_005094C0 @0x006A3A2D, FUN_00509510 @0x006A3A43), new(0x130) + FUN_006C0D50
(ArkModelManagerMain ctor) @0x006A3A77, FUN_006C8B20/BB0, and
FUN_0050A310(SF, manager) @0x006A3A9D. FUN_0050A310 was decoded (NEW #7) over its
288-byte window 0x0050A310..0x0050A42F — NOT the full function. The true extent,
measured by the independent internal QC, is 0x0050A310..0x0050A45C (terminal
ret 0x4 @0x0050A459 + int3 padding); the undecoded tail 0x0050A42B..0x0050A45C holds
only flag stores, a FUN_005095C0 call and the return epilogues — NO join-bearing
content (per the QC measurement). FUNCTION_BUDGET.csv keeps the honest continuation
notation "0x0050A310..0x0050A453+" for this row. Every join-bearing item — the SF's
visual/model-manager install ([SF+0x20]=manager, child=FUN_006C66D0(manager),
old-manager detach via NiNode vtable slot 42 + dtor) and THE JOIN SITE (the NiNode
vtable slot 41 call with (child, 0) on [SF+0x30]) — lies INSIDE the decoded window.
FUN_007B5810 (slot 41) was decoded
(NEW #8) as the oracle byte proof (see 1.1/1.1c above). This path also performs a
templates.vfs registry lookup (FUN_0043A550 + FUN_0072F580 + validity FUN_0072FCE0)
before creating the SF — the same registry family as the resource island — but the
child's connection to a MODEL/RESOURCE RESULT remains unestablished.

**The resource-island side (CH1/CH2):** the {0x66=MODEL, A} emitter chain was
re-pinned (CH1 MATCH: lookup -> getter A -> pair stores -> scheduler entry
FUN_006C3640 with callback immediate 0x008BD720 @0x006C3FB0). NEW #1: FUN_008BD720
decodes as `lea eax,[ecx+0x18]; ret` — a 4-byte accessor, NOT a completion handler
body. The completion chain past the scheduler entry was NOT followed (budget
boundary — see §4 open edges).

## 3. The four proofs (CAND-4, the strongest candidate)

| proof | status | basis |
|---|---|---|
| A CHILD_PROVENANCE | UNRESOLVED | the child = FUN_006C66D0(ArkModelManagerMain) result; the getter and the manager's model/resource provenance are NOT decoded/traced (budget boundary) |
| B EXACT_PARENT | CONFIRMED (scoped to the examined ACLD-path SF instance; same class/chain as the SF island; NOT the CMO instance) | receiver provenance byte-proven: [ACLD+0x18] SF -> ESI -> [ESI+0x30] -> ECX at the virtual dispatch; no ECX clobber |
| C JOIN_OPERATION | STRONGLY_SUPPORTED | FUN_007B5810 = NiNode::AttachChild counterpart by the Gb12 fingerprint (F1/F2/F4/F5 byte-matched; F3 present as a direct call, body undecoded); children-array layout cross-checked against the independent slot-17 canon |
| D VISUAL_ROLE | UNRESOLVED | no physical visual-role proof; the child receives NiMain-cluster follow-up calls (FUN_007BF900/FUN_007BF630) — noted, undecoded |

INSTANCE_MODEL_NODE_JOIN = NOT_ESTABLISHED (requires A, B, D confirmed + C
establishing the conditional operation on their exact values — not met).
RUNTIME_JOIN_OBSERVED = NO. SAME_INSTANCE_TRANSFORM_RELATION = CONFIRMED_STATIC
(separate status; CMO path; no join promotion).

## 4. Honest open edges (the bounded next inputs — NOT authorized by this run)

1. FUN_006C66D0 (the child getter from the ArkModelManagerMain) + the child's
   provenance chain toward a physically established model/resource operation —
   the primary open edge for proof A.
2. The child's visual role (proof D) — e.g., the FUN_007BF900/FUN_007BF630 calls on
   the child, or the manager's model-request path.
3. FUN_007BF470 (the AttachParent-shaped inner step) — to raise C from
   STRONGLY_SUPPORTED toward CONFIRMED_STATIC_CONDITIONAL.
4. The resource island's completion chain: the scheduler entry FUN_006C3640 and
   the type-0x66 provider — untouched this run (FUN_008BD720's accessor identity
   redirects that lead: the "callback" slot is an accessor, so the completion
   handler is reached through the scheduler entry, not by decoding 0x008BD720).
5. Whether the SF-island's CMO instance ever receives a model child (no join found
   in the examined CMO chain; FUN_0050A310's callers other than FUN_006A3930 were
   NOT censused — the CMO could install a manager through a different path).

## 5. Governance statuses (unchanged)

WORLD_XYZ_RECOVERED = NO · HISTORICAL_INSTANCE_DATA_RECOVERED = NO ·
STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED · CANONICAL_GATE_EFFECT = NONE ·
NEXT_EXPERIMENT_AUTHORIZED = NO · no Q1/Gate-B/M1/M2 changes. Negative/partial
results are publishable; publication (by the persistence phase) is not acceptance.
FINAL_EXTRADATA_STORAGE = NOT_CHECKED (FUN_007B68B0 remained a DEFERRED_LEAD; the
join resolution did not require it — the dependency statement in
PRE_REGISTERED_ANCHORS.md §DEFERRED_LEAD was not triggered).

## 6. Phase boundary (per the dispatch)

This executor's phase = SCIENCE + TARGETED QC + PACKAGE. No AUDIT_ENTRYPOINT.md edit
(proposed newest-first row in HANDOFF.md), NO commit, NO push — persistence belongs
to PE-MASTER after its own audit and fresh internal QC. The final MANIFEST_SHA256.csv
was generated LAST over the physical package files EXCLUDING itself; the
AUDIT_ENTRYPOINT.md row is EXPLICITLY OUT of this phase's manifest scope (the
persistence phase will regenerate the manifest together with the entrypoint row).
PERSISTENCE_STATUS = PREPARED_NOT_PERSISTED; RESULTING_SHA = NONE (this phase).

## 7. SELF_CHECK (executor's own — NOT independent PE-MASTER audit)

- [x] Full raw census where claimed: every load-bearing instruction pinned with VA +
      bytes from the hash-pinned EXE; 25 pins + 17 rel32 targets independently
      re-verified at QC (S2/S3 MATCH).
- [x] All gates honestly evaluated: the qualification gate reads the proof-chain
      structure; baseline synthetic PASS; CTRL-A/B/C rejected by their proper
      predicates; the REAL candidate FAILS (no rubber-stamping).
- [x] Meaningful negative controls: the CMO-path candidates CAND-1/CAND-2 rejected on
      measured absence (no child argument / no children-array access / transform ≠
      child); CAND-3 classified NON_MODEL; the +0xC0→+0x20 external-writer census
      returned ZERO hits (true negative, superseded by finding the writer inside the
      SF class).
- [x] Correct source/generator hashes: EXE, contract, anchor-constraints, 3 private
      reports, 2 oracle sources — all re-measured and MATCHING their pinned
      identities (INPUT_IDENTITIES).
- [x] No default-success fallback: the child provenance and visual role are recorded
      UNRESOLVED at the budget boundary; no averaging up; no synthetic promotion.
- [x] Limits respected: 8/8 functions, 6/6 edges, 4/4 candidates, 2/2 wrapper levels,
      1/1 oracle — STOPPED at the boundary; no after-the-fact exceptions.
- [x] No original file modified; no payload/VFS/BNT/NIF opened; no Gamebryo source
      copied into the repo; private scratch outside the repo (registered).
- [x] Foreign untracked groups untouched; no git staging; AUDIT_ENTRYPOINT.md NOT
      modified (the persistence phase owns the entrypoint row).
- [x] QC tooling defects found in QC round 1 (2 check-specification errors) were
      fixed in the QC script only, disclosed in QC_REPORT.md §4; no executor
      evidence was modified by QC.
