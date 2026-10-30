# LAB External Post-Audit Notice R1 — PE2003 Gamebryo Local Toolkit Asset Bridge Lab R1

RUN_ID (this corrections run): PE2003_ROSETTA_GAMEBRYO_BRIDGE_CORRECTIONS_R1_20261030 (2026-10-30)
ADDITIVE NOTICE for: PE2003_GAMEBRYO_LOCAL_TOOLKIT_ASSET_BRIDGE_LAB_R1_20261030
This notice is ADDITIVE: every file of the original lab run package — including
REPORT_PUBLIC.md and PUBLICATION_MANIFEST.csv — is untouched. Nothing in the historical
package was edited, retracted in place, or deleted; corrections live in this notice and in
the new reference namespace cited below.

## External post-audit verdict

The independent Desktop post-audit of the lab run issued:
**PARTIAL_PASS_WITH_MATERIAL_CORRECTIONS**. The lab's executed achievements stand
(stock-engine SDK_CONTROL_RENDERED, PE_ASSET_PARSED, adapted loads, texture re-attachment
mechanism, launcher controls); the material corrections below are now recorded and
executable. Advisory pre-qualification context applies (PE-MASTER
PROVISIONAL_UNTIL_QUALIFIED; publication is not scientific acceptance; canonical gate
effect of the lab and of these corrections: NONE).

## The six GBL findings and this run's corrections

**GBL-1 — Texture era ("real 2003 textures") — REJECTED.**
All 31 texture-lineage rows trace to the EU_LATER-era Textures.bnt (RE evidence only), not
Jan2003 Textures.ark members and not PCG9.3.5. SAME_ERA_WITH_PE42 = FALSE. Bounded
per-member comparison vs the CD Jan-2003 Textures.ark: 16/24 byte-identical, 8/24
byte-different, 0 absent; per-member era for the 8 byte-different members is
NOT_ESTABLISHED (pixel identity not evaluated). Corrected wording:
"EU_LATER Textures.bnt; RE evidence only; never silently Jul-2003 truth."

**GBL-2 — Blanket "lossless" fidelity — scoped.**
RGB is preserved through the lab chain (hash-verified on all 31 rows), but variable alpha
is lost for 2/24 textures (126773: 5212/16384 non-255 alpha pixels; 126775: 2580/8192) at
the 24-bpp BMP re-encode, and the GPU path is alpha-less end-to-end (X8R8G8B8; forced-
opaque 0xFF000000 load; D3DTSS_ALPHAOP=D3DTOP_DISABLE). Corrected wording: "RGB lossless;
alpha lost for 2/24 (126773, 126775); GPU format X8R8G8B8 alpha-less."

**GBL-3 — Transform fidelity of rendered instances — corrected.**
The harness world builder (MatFromTransform) fed a row-vector device an untransposed
rotation, computing R^T(s·p)+t (measured deviations 3.0–9.0 units on 4 executed cases); the
view builder (MatFromCameraWorld) wrote the basis as rows, so the eye did not reach the
view origin (|view(eye)| = 18.977674), and additionally built X = norm(U×F) = −col2,
mirroring the view X axis relative to the engine's own kRight (second bug found in the
corrections run). The projection matrix is CORRECT (matches D3DXMatrixPerspectiveFovLH).
The claim is corrected to "API-identity only" for the historical path; a corrected
portable adapter now reproduces the ground truth on 8/8 gates with the wrong-transpose
mutant failing as the required negative control. No corrected-harness render was executed.

**GBL-4 — NiArk graph bypass "world geometry preserved" implication — PROVEN BROKEN.**
The bypass-splice copies each spliced child's local payload verbatim without composing the
removed node's transform: world = W_parent·L_child instead of W_parent·L_billboard·L_child.
All 7 NiArkBillboardNode graph nodes in 296445 carried non-identity transforms
(position deltas 4941.8–11291.1 magnitude units plus dropped 180°-Z rotations); the lab's
own engine recount independently corroborates all 7 quads collapsed at (0, 0, −534.634).
Verdict: PROVEN_BROKEN_FOR_7_OF_7. Related corrections: the 7 orphan NiZBufferProperty
blocks were node-level properties of the removed billboards (the surviving quads inherit
nothing; depth only via device-global states, with D3DRS_CULLNONE masking the 180°
orientation flip); UV-animation inertia was caused by the untextured PLAN_B render path,
NOT by block removal (the UV controller chain survived, remapped); 0 NiArk blocks were
left as NULL (the nulls are pre-existing exporter child slots of the root node).

**GBL-5 — Process and ledger integrity of the lab run — corrected.**
The experiment ledger was rewritten by fix helpers, so its "append-only" claim is false
(encoding defect at line 19: cp1252 bytes vs the complete JSON remainder;
INTEGRITY_PARTIAL at CURRENT_SEALED_BYTES=PASS). The launch cap was exceeded: 36 startup
markers in 32 log files = strong lower-bound evidence; exact total UNKNOWN. The reported QC
counter read 54858 was a misread (it had mixed 296445 sizes); the corrected counter read is
55304 = 56535 − (84 + 1056 + 91). The "brak exit6" finding was false: iExit=6 is present.
The lab's claimed file count "16+1" was wrong: recount = SCI 18 rows + manifest = 19 files;
author = 13+1 = 14.

**GBL-6 — Publication manifest completeness and path hygiene — corrected.**
The lab's PUBLICATION_MANIFEST.csv enumerated 1 row while 3 paths had changed; this
corrections run's publication manifest enumerates EVERY changed path, including the single
newest-first AUDIT_ENTRYPOINT.md row. Hygiene: 5 absolute private filesystem paths were
removed from the published code (grep-gate zero, verified by two independent
implementations); the G8 three cross-check now resolves its dependency portably (bare
specifier + module-relative walk-up; honest SKIP if unresolvable) — it was executed against
three@0.185.0 in the working root and honestly SKIPs in a bare checkout.

## Where the executable corrections live

New reference namespace (added by this corrections run; nothing pre-existing was
modified): `src/pe2003/rosetta/bridges/gamebryoReference/` —
niTransformAdapter.mjs (corrected world/view/camera math, explicit handedness, NaN/Inf
rejection), rosettaReferenceRegistry.mjs (strict era-scoped lookup; ISO 5.1.0.0 queries are
REJECTED, never substituted), FORMAT_LOSS_MATRIX.json (11 capability rows with evidence
pointers), TEXTURE_ERA_RECORD.json (per-member era comparison), CLAIM_CORRECTIONS.json
(6 additive corrections, old wording preserved verbatim), ROSETTA_INTEGRATION_MAP.json
(record-level integration state; runtime_enabled=false for every record) — plus
tests/bridge/rosettaRegistry.test.mjs (8/8 gates PASS, re-executed). The namespace is
REFERENCE ONLY: no runtime code imports it yet (INTEGRATION_PENDING). Nothing in it is
ISO_5_1_0_0 primary-target truth; era is identity, never a fallback.

Old lab REPORT_PUBLIC.md: untouched (its historical wording is superseded additively by
this notice and by CLAIM_CORRECTIONS.json, which preserves the old wordings verbatim).
PE2003_WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED;
CANONICAL_GATE_EFFECT=NONE.
