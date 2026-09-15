# WORK-AUDIT (audytor: Work-Audit, audyt: audyt-pe935-slot17-oracle-minicheck-20260914-1515) - plik audytora, NIE jest czescia pracy wykonawcy.
# PROMPT_KONTYNUACJA V2 - zintegrowany cleanup/persistence run (decyzja human z 2026-09-14).
# V1 (ABI_PREFIX_R2) pozostaje w PROMPT_KONTYNUACJA.md jako spec ODL/OZONY - nie uruchamiac bez eksplicytnej decyzji.

=== 8< === CUT HERE === 8< ===

RUN ORDER (direct PE-MASTER dispatch; executor pe-reconstruction; publication per project
discipline; NO_NESTED_TASKS)

RUN_ID: PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914
RUN_CLASS: PROCESS/PERSISTENCE - master-mutating BY HUMAN AUTHORIZATION, limited to the
  enumerated scope below. This authorization OVERRIDES the default no-master-mutation rule
  for this run ONLY. STATIC-ONLY: no client runs, no oracle code runs.

## Context (why this run exists)

The knowledge line is verified and standing: SceneFeeder cached XYZ / SF+0x30 -> NiNode ->
slot 17 0x007B5390 (recursive named lookup, STRONGLY_SUPPORTED_GETOBJECTBYNAME) ->
returned NiAVObject* -> +0x90 = m_kWorld.m_Translate.x. The independent audit
(audyt-pe935-slot17-oracle-minicheck-20260914-1515) re-verified every load-bearing number
from physical files and found 1xP2 + 6xP3 documentation/provenance defects. The live state
is split: master = a7a6c75 (LINK30 AMEND_R2), the accepted mini-check = 5290e79 on branch
audit/pe935-ninode-slot17-gb-oracle-minicheck-r1. This run converges both into ONE correct
current master, with all audit findings dispositioned, BEFORE any further RE.

## A. STATE INTAKE (fail-closed; EVERY observation timestamped - audit AUD-F6/F7 discipline)

A1. BASE: live origin/master at run start (expected a7a6c756...; verify local == remote ==
    ls-remote with timestamps; record any concurrent-session movement explicitly, separate
    "at run start" vs "at publication" statements in every document).
A2. SLOT17 branch: audit/pe935-ninode-slot17-gb-oracle-minicheck-r1 @ 5290e79, local and
    remote equal; the package = exactly 35 paths (re-run the census yourself).
A3. Untracked census (hash-only, DO NOT read contents):
    docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/ (the LINK30-R2 F5 HOLD subject)
    + experiments/ - file list + SHA256 census for the record.
A4. Pins re-measured: Entropia.exe E7785430..., NiMain.lib FF4519AF..., the six gb12 .obj
    and Gb12_Source pins (copy the R1 pin list; every hash re-measured at run start).

## B. SLOT17 PACKAGE AMENDMENTS (documented errata; project amendment discipline:
   AMEND_LOG with before/after quotes + byte-identical .pre proofs in 00_CONTROL/PRE_EDIT/;
   01_RAW and 03_EVIDENCE files UNTOUCHED; MANIFEST_SHA256.csv regenerated at the end;
   the original 5290e79 state stays forever reachable via the audit branch)

AUD-F1 [P2] HANDOFF.md: replace the unqualified "OBSERVED_MASTER_SHA ... local master and
    live remote master observed equal to BASE_SHA; no drift" with the timestamped truth:
    run-start observation (14:31 local, master=3644e5a) + at-publication state
    (local master=a7a6c75 - concurrent LINK30 AMEND_R2 commit 14:40:54, NOT this run).
AUD-F2 [P3] HANDOFF.md: per-directory census corrected to 03_EVIDENCE=16 / 06_REPORT=4
    (total 35 incl. manifest).
AUD-F3 [P3] RUN_CONTRACT.md + SOURCE_IDENTITIES.json honesty note: explicitly list the FIVE
    files adopted from the interrupted sessions with mtimes (entropia_rtti_probe.py
    14:11:34, parse_coff_vtable.py 14:12:14, entropia_disasm_7b5390.py 14:18:25,
    coff_disasm_symbol.py 14:24:07, GB12_SOURCE_LOCATORS.md 14:26:37) vs the regenerated
    classes; remove any wording that implies "everything was regenerated".
AUD-F4 [P3] 00_CONTROL/entropia_rtti_probe.py docstring: ImageBase 0x400000 reads at the
    STANDARD IMAGE_OPTIONAL_HEADER32 offset 0x1C; DELETE the "+4 shifted relative to
    winnt.h" claim and the "+28 convention" framing (independent audit byte-parse proof);
    keep the empirical-validation sentence.
AUD-F5 [P3, verdict-side] See section C (sidecar): the PE_MASTER_REVIEW gloss "to ta sama
    zawartosc" for the Gb112_eval path issue is FALSE (Gb112_eval contains only
    Documentation; the run pinned the installed SDK path consistently) - corrected in the
    sidecar, NOT by editing the verdict.
AUD-F6/F7 [P3] REPORT.md line 5-6: the "= origin/master = live remote master" equality
    gets the same dual timestamp treatment as AUD-F1.

## C. VERDICT PERSISTENCE (the SLOT17 mini-check verdict)

C1. Persist the SLOT17 PE_MASTER_REVIEW (MASTER_ACCEPTED, ADVISORY_PRE_QUALIFICATION,
    CANONICAL_GATE_EFFECT=NONE) VERBATIM as PE_MASTER_REVIEW.md in the SLOT17 package
    (project discipline: verbatim persistence).
C2. Sidecar PE_MASTER_REVIEW_SIDECAR.md with the independent-audit dispositions:
    (i) AUD-F5: the verdict evidence-finding #2 justification "same content" is factually
    wrong; the correct statement: the run pinned and used the installed SDK path directly;
    Gb112_eval = Documentation only; conclusion (path-label cosmetic, no defect) upheld.
    (ii) AUD-F6: the verdict FINAL "origin/master=3644e5ac (brak dryfu)" was time-dependent
    and is superseded by the integrated state; see the AUD-F1 erratum for the timeline.
    (iii) pointer to the full audit: D:\TESTAI\audits\work-audit\
    audyt-pe935-slot17-oracle-minicheck-20260914-1515\REPORT.md (summary: 18 confirmed,
    3 refuted, 2 unconfirmed, 0 findings affecting the scientific result).
C3. AUDIT_ENTRYPOINT.md: LATEST RUNS row for SLOT17 R1 (+ the cleanup run itself, per the
    table convention). This is the human-authorized first AUDIT_ENTRYPOINT touch for
    SLOT17 (the R1 verdict deferred exactly this).

## D. LINK30-LINEAGE OPEN ITEMS

D1. R-EBP-INHERITED (2 census rows): from the LINK30 canonical census (post-AMEND_R2,
    3022 rows), locate the two rows with why-reason R-EBP-INHERITED; re-verify each
    row-reason against physical Entropia.exe bytes (bounded: the cited instruction pair
    per row, nothing more); write the per-row disposition note into the cleanup package.
    If a reason is WRONG -> amendment of the LINK30 census per project discipline (with
    .pre proof); if correct -> record CONFIRMED with the evidence line.
D2. LINK30-R2 F5 HOLD disposition ([HUMAN CHOICE - REQUIRED BEFORE DISPATCH]:
    [ ] OPTION A - retro-authorized bounded completion of
        PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914 per its own RUN_CONTRACT (that
        completion is a SEPARATE bounded run dispatched AFTER this cleanup, NOT inside it;
        this run only records the decision and re-censuses the untracked package),
    [ ] OPTION B - discard: archive the hash census in the cleanup package, then delete
        the untracked directory (destructive; only on the human explicit pick),
    [ ] OPTION C - keep on HOLD: record the census + the HOLD continuation in the cleanup
        package).
    Whatever the choice: NEVER silently delete or adopt untracked WIP content.

## E. INTEGRATION (the master-mutating part - exactly this, nothing more)

E1. Bring the AMENDED SLOT17 package into master (merge or cherry-pick the amended branch
    state; single path-limited integration commit; no mixed commits).
E2. Result: ONE correct current master containing AMEND_R2 (already there) + the amended
    SLOT17 package + the cleanup package (this run own documentation, per convention in
    docs/audits/PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914/) + the AUDIT_ENTRYPOINT
    rows. Push; verify ls-remote == local with timestamps.
E3. The audit branch audit/pe935-ninode-slot17-gb-oracle-minicheck-r1 STAYS as the
    verbatim 5290e79 historical record (do not delete).

## F. GATES

G0_STATE_INTAKE: all A items verified, fail-closed, every git observation timestamped.
G1_AMEND_INTEGRITY: every AUD-F1..F7 fix = AMEND_LOG entry + .pre byte-proof; zero
    evidence-file mutations (before/after hash census over 01_RAW + 03_EVIDENCE must be
    identical except the regenerated MANIFEST).
G2_VERBATIM_PERSISTENCE: PE_MASTER_REVIEW.md byte-verbatim; corrections ONLY in the sidecar.
G3_DISPOSITIONS: D1 per-row notes present with physical-byte evidence; D2 records the
    human choice verbatim.
G4_MASTER_INTEGRITY: post-push master = linear, one path-limited integration commit set,
    AUDIT_ENTRYPOINT consistent (rows for SLOT17 R1 + cleanup), no untracked residue
    except what D2 chose to keep.
G5_HYGIENE: no Gamebryo source/binary, no Entropia payload, no NIF/BNT payload anywhere in
    the committed set; census verified per-directory AGAINST the actual file list
    (audit AUD-F2 lesson: verify, do not reuse R1 numbers).
G6_NO_SCOPE_CREEP: no new RE, no decode of anything beyond D1 bounded checks; HARD STOP
    after the push verification.

## G. Pipeline after this run (record in HANDOFF; NOT executed by this run)

1) OpenCode QC/audit of the cleanup run ->
2) human independent post-audit ->
3) HUMAN GO ->
4) 4h AUTO LOOP (PE-MASTER). During the loop PE-MASTER weighs the DEFERRED
   PE_935_NINODE_ABI_PREFIX_R2 (slots 3..15 decode) against the more MODEL_BRIDGE-productive
   targets: arg2 provenance (who supplies the name / what names), where SF+0x30 NiNode is
   created/loaded and which NIF/model resource feeds the graph, downstream world-position
   consumer chain. THE ACCEPTED B->A CRITERION (pre-declared, locked - human decision of
   2026-09-14): even a perfect 3..15 decode yields ABI_PREFIX_ALIGNMENT=CONFIRMED while
   FUNCTION_IDENTITY stays B - STRONGLY_SUPPORTED_GETOBJECTBYNAME; BLOCKER_FOR_A =
   era/generation identity (separate human-authorized oracle experiment).

HARD STOP. No further experiment without new dispatch.

=== 8< === CUT HERE === 8< ===

Noty human (PL): (1) przed dispatchem uzupelnij [HUMAN CHOICE] w D2 (A/B/C) - bez tego run
nie moze ruszyc; (2) spec ten odtwarza Twoj zakres z rozmowy - pierwotny "przygotowany" spec
nie istnieje na dysku (grep negatywny), wiec porownaj go ze swoim zapisem; (3) pozycje D1/D2
ugruntowalem w plikach: AMEND_LOG_R2.md s5 (F5 HOLD), AMEND_LOG_R1/QC_AUDIT_R1 (R-EBP-INHERITED 2).
