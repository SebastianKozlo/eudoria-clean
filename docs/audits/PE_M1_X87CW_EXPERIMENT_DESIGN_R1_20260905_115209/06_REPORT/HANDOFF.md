# HANDOFF — PE_M1_X87CW_EXPERIMENT_DESIGN_R1_20260905_115209

## The mandatory handoff block

    AUDIT_OUTPUT_ROOT      = D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_EXPERIMENT_DESIGN_R1_20260905_115209\
    FINAL_REPORT_PATH      = D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_EXPERIMENT_DESIGN_R1_20260905_115209\06_REPORT\00_FINAL_REPORT.md
    PRIMARY_EVIDENCE_PATHS = D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_EXPERIMENT_DESIGN_R1_20260905_115209\05_ANALYSIS\EXPERIMENT_DESIGN.md
                             + 05_ANALYSIS\COMPOSITION_RECORD.md + 05_ANALYSIS\DESIGN_CHECKLIST.md
                             + 03_STATIC\CANON_EXTRACTS.md + 01_RAW\pre_run_locks_hashes.json
                             + 00_CONTROL\RUN_MANIFEST.json + artifact_index.csv
                             + the repo mirror docs\audits\PE_M1_X87CW_EXPERIMENT_DESIGN_R1_20260905_115209\
    BASE_SHA / HEAD_SHA    = 642bc123fe036a4cda1d08fafcbbabecb646a160 / <recorded in the final handoff message after the push — this mirror commit's SHA>
    PUSH_STATUS            = PUSHED (the authoritative BASE/HEAD/PUSH values are delivered in the run's final handoff message)
    RUN_STATUS             = DESIGN_COMPLETE
    HARD_STOP_REASON       = NONE
    NEXT_GATE              = the PE-MASTER design review -> the human's GO runtime

## The outcome for the reviewer

The design is composed and complete (W1-W6, all checklist items A1-A16). ZERO runtime was executed; ZERO new static claims were made; the GAP CHECK found NO canon gaps (every design need maps to a cited canon fact or a bounded execution-phase check). The runtime execution is separately gated: PE-MASTER reviews THIS package first; the human's explicit "GO runtime" starts the execution run (a fresh RUN_ID per the reuse rule), which follows EXPERIMENT_DESIGN.md W3 verbatim and classifies its outcome per W5.

## The review focus (suggested)

1. W2's read-point choice (the site-local primary; the chain-entry fallbacks; the init-vs-site disambiguation) — does the reviewer agree the site-local read alone answers the P0 under both init conditions?
2. W3's N=10-hit policy + the bounded window + the honest manual-session reality (the measured x32dbg GUI blocker).
3. W5.1's RC honesty bound (the closure is complete only if RC measures nearest-even; otherwise the RC dimension opens as its own sub-item — no silent pass).
4. W4's class set (7 classes; signatures + dispositions) against the §14 taxonomy.
5. The COMPOSITION_RECORD map (C1-C22, E1-E5) — the reviewer's own spot-checks against the pinned canon.
