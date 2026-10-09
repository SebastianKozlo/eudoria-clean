# HANDOFF — PE_935_CAND4_006C9700_PLUS4_RESIDUAL_POST_AUDIT_CORRECTION_R1_20261008

The contract §8 mandatory final response, with ACTUAL measured values.
(Persistence-phase handoff; the terminal chat handoff to PE-MASTER restates
the SHA facts that cannot be embedded in this commit's own files.)

```text
RUN_ID
  = PE_935_CAND4_006C9700_PLUS4_RESIDUAL_POST_AUDIT_CORRECTION_R1_20261008
  (RUN_CLASS RECORDS_AND_QC_MACHINERY_CORRECTION; correction-only;
  RUN_SCOPE = EXACTLY THREE DESKTOP P2 + ONE REC-W P3)

BASE_SHA
  = 0b94c487ba11869b811aada188bfabaf8972728a
  (verified at preflight: LOCAL_HEAD == origin/master == actual remote
  master, live ls-remote, no fuzzy comparison; re-verified immediately
  before commit per contract §7(h))

RESULTING_SHA / REMOTE_SHA
  = recorded at the terminal handoff per contract — not embedded in this
  commit's files (a commit cannot contain its own SHA; the same rule the
  repo's HEAD row applies). The terminal handoff to PE-MASTER states both.

PERSISTENCE_STATUS
  = this handoff is written BEFORE the commit; the gates->commit->push
  sequence follows per contract §7(i). If any persistence gate failed, the
  honest state would be BLOCKED_UNPUBLISHED per contract §8 — the recorded
  technical result is PASS, so the expected terminal state is ONE ordinary
  commit + fast-forward push + actual-remote re-verification == RESULTING_SHA.
  (CORRECTION_VERDICT and PERSISTENCE_SAFETY are kept separate; both PASS
  here.)

LOCAL / ORIGIN / ACTUAL-REMOTE EQUALITY
  = at preflight and immediately before commit: git rev-parse HEAD ==
    git rev-parse origin/master == git ls-remote origin refs/heads/master
    == 0b94c487ba11869b811aada188bfabaf8972728a (all three equal; measured,
    not assumed). After push: LOCAL_HEAD == origin/master == actual remote
    master == RESULTING_SHA (re-verified live). No
    reset/amend/rebase/cherry-pick/force-push/auto-merge at any point.

SCOPE AND ALLOWED-PATH DIFF
  = exactly ONE ordinary commit containing ONLY:
    (a) every physical file under docs/audits/PE_935_CAND4_006C9700_PLUS4_RESIDUAL_POST_AUDIT_CORRECTION_R1_20261008/
    (the OUTPUT_ROOT allowlist — 80 files at commit time incl. this
    handoff and the manifest generated LAST);
    (b) the narrow AUDIT_ENTRYPOINT.md amendments (one new newest-first run
    row + the line-32 annotation extension inside the existing
    HISTORICAL_REFERENCE annotation).
    NO other path is staged, modified, deleted or committed. The six foreign
    untracked paths recorded at preflight remain untouched and uncommitted.
    git status after commit shows only those foreign untracked paths.

DISPOSITIONS (contract §8)
  P2-A = CORRECTED — half-open [VA,VA+n) VA intervals with whole
    pre-validation (integer-not-bool, 0<=VA<2**32, n>0, VA+n<=2**32;
    underflow separate); per-section ANY-intersection rule (>1 intersecting
    section => REJECTED_INVALID_INPUT/QC_REJECT even if one fully contains);
    single section must cover the whole request; RAW_BACKED whole-range in
    ONE section's SizeOfRawData AND physically in file; VIRTUAL_BSS;
    raw->BSS crossing controlled FAIL; no fabricated zeros; valid boundaries
    VA=0xFFFFFFFF,n=1 and VA=0xFFFFFFFE,n=2 read correct bytes (NOT
    over-rejected); VA=0xFFFFFFFE,n=4 / VA=0x100000000,n=4 INVALID; Desktop
    overlap cases (0x0040104F / 0x0040106F, n=4) controlled-reject; one-byte
    intersection rejects; real-EXE pin 0x006E8FA5,n=3 -> 89 46 04; BSS
    0x00BA1100/0x00BA73BC -> VIRTUAL_BSS; base+0x7FFFFFFF retained RELABELED
    UNMAPPED. Executor POST 39/39; PRE false-RAM_BACKED falsifiers reproduced
    with byte parity on BOTH historical implementations (immutable 00_PRE/).
  P2-B = CORRECTED — staged constructor boundary checks before every
    unpack_from/slice (e_lfanew, COFF, SizeOfOptionalHeader, Magic, ImageBase,
    section table); truncations 0x98/0x99/0xB4/0xB7 -> controlled
    ControlledReadError/QCReadError at the exact stage (PRE: raw struct.error
    escapes, messages byte-identical with the Desktop); probes 0x9A
    (ImageBase stage), 0xB8/0x190 (section-table stage), 0x1C0 (CONSTRUCTED);
    positive intact control all fixture fields match (section table 0x178).
  P2-C = CORRECTED (records) — retraction (a): R_W_SEPARATENESS ->
    SCOPED_STRUCTURAL_FACT (R/W construction evidence preserved; the
    unsupported later-T part removed); retraction (b): the SOURCE_RUN
    FD-C2/SL-9 active 'R != T' superseded (RS-2); explicit new unknown rows
    T_NOT_EQUAL_W_AT_LATER_USE = NOT_ESTABLISHED_WITHIN_BOUND and
    R_NOT_EQUAL_T_AT_LATER_USE = NOT_ESTABLISHED_WITHIN_BOUND (neither
    equality NOR inequality established); all old T==P/heap-origin/WITHIN
    overclaims remain superseded with zero active standing; floor 17 /
    bodies 5 / edge budget 12 -> ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL and
    ORIGINAL_SCOPE_COMPLIANCE = FAIL; exact counts UNRESOLVED;
    RETROACTIVE_PRIOR_AUTHORIZATION = NO; HISTORICAL_FIRST_QC_PRE =
    LOST_OR_NOT_AVAILABLE disclosed (RS-8); RS-3 census 10 locations — the
    last one (entrypoint line 32) closed by THIS persistence phase (F-QC-1).
  P3 REC-W = CORRECTED — new production gate RECW:W_RECORD_IDENTITY
    (canonical module-internal registry 'W_CTOR_CALL_AT_006CB836' <->
    0x006CB836, non-mutatable, independent of the fixture JSON; structural
    1 definition/0 assignments/0 JSON-writes + behavioral confirmation);
    PRE through the ORIGINAL checker's NORMAL loader path: wrong-callsite
    mutant 86/86 FALSE PASS (Desktop expectation reproduced); W2
    RECORD_ID-only 86/86 false pass (fixed-address QC did NOT catch it —
    honest negative); W3 generality 86/86 false pass; POST: W1/W2/W3 each
    FAIL exactly on RECW:W_RECORD_IDENTITY (86/87; 80 historical + 6 original
    RECW PASS; no rescue paths); clean 87/87; denominator honestly 87.

EXACT PRODUCTION/QC CLEAN BASELINES
  = production v2 clean gate 87/87 PASS (80 historical + 6 RECW + 1
    identity; every row enumerated); clean scratch copy through the normal
    loader path 87/87; QC's own QCPEv2 Desktop-case suite 18/18; QC's own
    80-ID re-execution 80/80; QC clean re-execution 87/87 via both loader
    paths; PE-MASTER's own gate execution 87/87 (all rows enumerated).

PRE/POST MUTANT FAILURES AND CONTROL PASS COUNTS
  = PRE (immutable 00_PRE/, original machinery): W1 86/86 gate PASS (false
    pass; fixed-address QC MISMATCH_DETECTED); W2 86/86 gate PASS (false
    pass; fixed-address QC MATCH_NO_MISMATCH — honest negative); W3 86/86
    gate PASS (false pass; QC MISMATCH_DETECTED); the four Desktop P2-A
    mapper false-passes and four P2-B truncation escapes reproduced with
    byte parity on BOTH historical implementations.
    POST (v2): W1 86/87 gate FAIL, fail_ids = [RECW:W_RECORD_IDENTITY];
    W2 86/87 gate FAIL, fail_ids = [RECW:W_RECORD_IDENTITY]; W3 86/87 gate
    FAIL, fail_ids = [RECW:W_RECORD_IDENTITY]; in each the historical 80 and
    the six original RECW PASS and no SHA-mismatch/missing-file/unrelated-pin
    failure rescues the verdict; MC1-MC5 each FAIL exactly its anchor; MC6
    all 87 anchor gates PASS; the three W-record JSON mutation gates flip
    exactly their own gate with the identity gate PASS; P2-A boundary
    controls 39/39 case-PASS; P2-B truncations/probes controlled at the
    exact stages; prior RAW/BSS controls preserved.

HISTORICAL 80-ID REGRESSION + SEPARATELY COUNTED NEW IDS
  = 80/80 PASS, complete required ID set (EXE_IDENTITY + 57 PIN + 16 REL32
    + 3 RTTI + 3 STR, no duplicates), tables element-identical to BOTH the
    historical PROVENANCE checker (4/4) and the SOURCE_RUN successor (4/4);
    separately counted: RECW old 6/6; NEW identity check 1/1
    (RECW:W_RECORD_IDENTITY); total 87/87; separate denominators 80/6/1 = 87
    (TARGET_FORMULA stays schema-required, NOT a separate gate).

QC DUTIES AND LIMITATIONS
  = QC_ORIGIN = pe-master-auditor fresh-context internal QC, internal to
    PE-MASTER (NOT an independent Desktop post-audit; NOT executor
    self-review). QC_VERDICT = PASS — 10 recorded duties (D1 18/18 P2-A
    incl. Desktop PRE parity byte-identical; D2 9/9 P2-B; D3 P3 mutant
    re-executions W1/W2/W3 -> exactly the identity gate, clean 87/87 both
    loader paths, identity-oracle non-mutatability structural+behavioral;
    D4 own W byte pin read E8 75 F0 02 00 / +0x2F075 / 0x006FA8B0 with a
    direct file-slice crosscheck at offset 0x2CB836; D5 own 80/80
    re-execution; D6 P2-C records re-adjudication; D7 the RS-3 10-location
    census + entrypoint dependent-location verification; D8 MAPPER spot
    verification 0 disagreements; D9 REGRESSION spot verification agrees;
    D10 PRE immutability 0 mismatches + 4 superseded POST stamps preserved).
    QC repair round 1/1 used ONLY on the QC's own tooling (2 disclosed
    fixes; attempts preserved in QC_ATTEMPTS_LOG.md; zero executor artifacts
    modified). LIMITATIONS (explicit): no new RE/disassembly of any kind;
    forbidden bodies NOT opened (FUN_007B79B0 / FUN_007B7930 / FUN_006B2310
    — the &R+8 write-effects GAP stays a GAP); the EXE never executed
    (STATIC_ONLY); not every JSON field of every PRE/POST raw was
    individually re-executed (hash-verified + load-bearing rows re-executed);
    the external Desktop post-audit of the resulting SHA is NOT this QC.

ORIGINAL SOURCE-PACKAGE IMMUTABILITY CENSUS
  = SOURCE_RUN docs/audits/PE_935_CAND4_006C9700_PLUS4_POST_AUDIT_CORRECTION_R1_20261008/
    22/22 byte-identical at BASE (physical Git tree comparison AND
    working-tree hashing; manifest blob 60e8318e90a76e6d0a85365d9080a89f33bdd1bf
    verified); git diff 0b94c48 -- <SOURCE_RUN> empty; the historical
    PROVENANCE package and checker unchanged; the whole-repo diff of this
    commit is exactly OUTPUT_ROOT/** + AUDIT_ENTRYPOINT.md (verified against
    BASE before commit); THIS package census 75 files pre-persistence
    (executor 66 + QC 9) measured physically, never assumed.

MANIFEST FILE AND EXACT VERIFIED ROWS
  = MANIFEST_SHA256.csv, generated LAST (after ALL writes incl. the
    entrypoint amendments), self-exclusion documented: scope = every
    physical file under OUTPUT_ROOT EXCEPT the manifest itself PLUS
    AUDIT_ENTRYPOINT.md; repo-relative; one row per path. MEASURED census:
    80 physical package files -> 79 package rows + 1 entrypoint row = 80
    manifest rows; verified missing=0, extra=0, duplicate=0, size mismatch=0,
    SHA mismatch=0 (bijection PASS).

UNRESOLVED F-1..F-5 AND NEW FINDINGS
  = F-1..F-5 source backlog unchanged and kept OPEN (not material to the
    corrections). NEW findings of THIS run: NONE material beyond the
    corrected five; F-QC-1 (the entrypoint line-32 'R!=T' annotation
    extension) EXECUTED in THIS persistence phase; executor/QC disclosed
    process items (runner case-design defects; QC self-tooling fixes) are
    disclosed, preserved negative evidence, not open defects;
    HISTORICAL_FIRST_QC_PRE = LOST_OR_NOT_AVAILABLE disclosed (RS-8).

RETRACT/SUPERSESSION EFFECTS
  = RS-1: the SOURCE_RUN matrix's R_W_SEPARATENESS 'T != W' part retracted
    (construction evidence preserved as SCOPED_STRUCTURAL_FACT); RS-2: the
    SOURCE_RUN ledger FD-C2/SL-9 ACTIVE 'R != T stays' superseded — with the
    entrypoint line-32 annotation extension the LAST dependent location is
    closed (all 10 RS-3 census locations now resolved); RS-4: all old
    T==P/heap-origin/WITHIN overclaims remain superseded, zero active
    standing; the SOURCE_RUN files themselves remain byte-identical
    READ_ONLY history (standing use withdrawn, files never edited).

COMPLIANCE
  = ORIGINAL_SCOPE_COMPLIANCE = FAIL (preserved; floor 17 / bodies 5 / edge
    budget 12; exact counts UNRESOLVED — NO exact counts established);
    ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL; RETROACTIVE_PRIOR_AUTHORIZATION
    = NO; SCIENCE_NEW = 0 (NEW_PCG_FUNCTION_BODIES = 0;
    NEW_PCG_SCIENCE_EDGE_INTERPRETATIONS = 0).

EXTERNAL POST-AUDIT STATUS
  = NEW_DESKTOP_POST_AUDIT = NOT_PERFORMED (the independent ChatGPT Desktop
    post-audit of the RESULTING SHA is a later human-authorized action; not
    self-declared by this run).

NEXT_EXPERIMENT_AUTHORIZED
  = NO

HARD_STOP
  = YES
```

## Persistence-phase file census (this commit)

```text
package files written by earlier phases (executor 66 + QC 9)   : 75
PE_MASTER_REVIEW.md (persistence phase, verbatim)              :  1
FINAL_REPORT.md (persistence phase)                             :  1
EVIDENCE_INDEX.md (persistence phase)                           :  1
HANDOFF.md (this file)                                         :  1
MANIFEST_SHA256.csv (generated LAST)                           :  1
                                                               ----
physical package files at commit time                          : 80
+ AUDIT_ENTRYPOINT.md (repo root, two narrow amendments)       :  1
                                                               ----
changed-path census of the commit                              : 81
```

## Governance standing after this run

MASTER_ACCEPTED_ADVISORY (internal advisory; ADVISORY_PRE_QUALIFICATION;
CANONICAL_GATE_EFFECT = NONE). This correction run does not qualify any
milestone, does not promote any record to canonical standing, and authorizes
nothing further. Standing ceilings preserved verbatim (FINAL_REPORT.md §9).
HARD_STOP = YES after this persistence phase.
