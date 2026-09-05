# NEXT_PROMPT — formalized direction for PE-NIF-HASH-PRIMITIVE-REVALIDATION-R3

Formalization record under the three-tier relay/formalization workflow (browser
run auditor designs direction → master auditor formalizes → executor executes).
The direction below was relayed from the external post-audit
PE_NIF_R2_POST_AUDIT_20260905_025627 (verdict REVALIDATION_REQUIRED) via
00_CONTROL/OPENCODE_REVALIDATION_PROMPT.md (SHA256
662d4c522a570d210549618bfee7d27acbc0253f39034c005c2678bde389d35c, verified by
gate R3G1) and was EXECUTED by pe-reconstruction in THIS run. It is recorded
here as the run-local formal charter (intent, paths, gates, restrictions), per
the convention that each published package carries its own 00_CONTROL record.

```text
RUN_ID        = PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627
EXECUTOR      = pe-reconstruction (implementation agent)
P0            = HASH_PRIMITIVE_VALUE_IDENTITY_BEFORE_AGGREGATE_ACCEPTANCE
ITER/MILESTONE= EU935-M2 contribution; NO milestone advancement
SCOPE         = one bounded revalidation/repair package; no new research
```

## Intent

Repair, without executing any historical driver and without touching any
read-only source, exactly what the external post-audit flagged: (F1) the two
defective R2 Node hash primitives and the aggregate-concealment mechanism;
(F2) the morph-residual and 21-claim summary overstatements; (F3) the
pending-as-fail gate serialization and the stale R2G13 tally label; (F5) the
implicit sidecar bare-CR policy — while PRESERVING every accepted physical
result (era join, nine-zero + CRC-subset census, 12/12 byte-lossless sidecars)
and superseding only unsupported method assurances.

## Resolved paths (as executed)

- AUDIT_OUTPUT_ROOT = D:\Eudoria_Reconstruction\99_Audits\PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627 (created fresh; collision-checked nonexistence)
- FINAL_REPORT_PATH = ...\06_REPORT\00_FINAL_REPORT.md
- PRIMARY_EVIDENCE_PATHS = ...\01_RAW\PRIMITIVE_VALUE_COMPARISON.json; ...\02_LOGS\TEST_RESULTS.json; ...\05_ANALYSIS\CLAIM_MATRIX.csv
- Publication = docs/audits/PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627/ in SebastianKozlo/eudoria-clean (master), local clone D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean

## Work items (all nine executed — see 02_LOGS/TEST_RESULTS.json gate mapping)

1. Defect reproduction from the ACTUAL bytes of the hash-pinned R2 source
   (extracted literal declarations executed; counterexamples tested, not
   assumed) — R3G3a/R3G3b/R3G6b.
2. Corrected stage-local primitives with explicit definitions (RFC1950 adler
   s1=1/s2=0 mod 65521; RFC9923 fnv exact multiply mod 2^32) — no shared-tool or
   R2 edits — 00_CONTROL/r3_primitives.py.
3. Executable known-answer tests BEFORE corpus aggregation, with independent
   oracles (zlib AND exact-integer/BigInt references) and oracle self-vectors
   — R3G4/R3G5 (enforced ordering; nonzero-exit abort).
4. Per-entry function VALUE comparison across both hash-pinned Models.bnt
   corpora keyed by era+file+candidate input identity, covering Adler(name),
   Adler(payload), FNV(name) and proportionately all ten census candidates;
   match-count tables only AFTER the identity pass; no payload bytes
   published — R3G9join/R3G9/R3G10 + 01_RAW/PRIMITIVE_VALUE_COMPARISON.json.
5. Negative controls that MUST fail (unchanged R2 helpers; deliberately
   wrong-value implementations preserving aggregate zero-match counts;
   pending-as-false serialization) with ACTUAL captured exit codes and failed
   predicates; corrected code passes the same predicates — R3G6a/R3G7a/R3G7b/
   R3G8a/R3G8b.
6. Nine-zero/CRC-subset recount with corrected primitives (physical result
   unchanged; 20/20 agreement with R2 aggregates and R36 historical); R2G8 +
   affected C2-B/C2-E method claims and report/handoff wording superseded
   without erasing history — R3G11 + SUPERSESSION_MAP.csv S-03..S-08.
7. The two bounded non-research inconsistencies repaired: R34 per-span re-sum
   (334/62/272 + counterexamples; no promotion of alternative fits; no
   all-21-at-100% claim) and three-state PENDING/PASS/FAIL preservation through
   gate function/JSON/CSV/report with the R2G13 tally derived from actual rows
   (16/8) — R3G12/R3G13/R3G15/R3G16.
8. The accepted 12/12 byte-lossless sidecars preserved; bare-CR policy stated
   explicitly and mapped fields independently compared under that policy
   (R39 row 10 dual-policy evidence; NOT raw-byte loss; no migration) — R3G14.
9. Finding dispositions + claim matrix + supersession map + corrected proposals
   ONLY + negative/positive test evidence + source hashes + command logs; each
   PASS records MEASURED_QUANTITY/DENOMINATOR/INDEPENDENT_SOURCE_OF_TRUTH/
   WHY_NON_CIRCULAR/FAILURE_CASE_DETECTED; source-inspection vs physical
   recomputation vs historical re-sum kept separate (method_class labels) —
   05_ANALYSIS/* + 02_LOGS/*.

## Restrictions honored (READ-ONLY)

Original game files, all historical run directories, R2, wiki/docs/nif,
canonical/vault/index, PE_AUTO_LOOP, shared tools/scripts, runtime code: all
READ-ONLY and re-verified by hash where used as evidence. No game/Ghidra
launch, no morph-boundary research, no leaf/XYZ, no MAPRE or milestone
promotion, no automatic wiki application, no nested agents, no stopping of the
concurrent M1-gate writer (untracked
docs/audits/PE_MILESTONE_1_WORLD_SURFACE_R1_GATE/ excluded from staging).

## Publication protocol (as executed)

Explicit-path staging only (no blanket add), commit of ONLY this run's package,
push WITHOUT force, remote commit/ancestry + package blob parity verified,
BASE_SHA captured (f37ba25468a39d9c89c7b01e106fab3215db7e4c at run start), the
final publication HEAD_SHA reported in the handoff (a commit cannot embed its
own hash). On any unsafe condition: EXTERNAL_AUDIT_INCOMPLETE with the exact
blocker.

## HARD STOP

After the corrected published package + handoff. Wait for independent
revalidation before proposals are applied. No next milestone, no unbounded
loop.
