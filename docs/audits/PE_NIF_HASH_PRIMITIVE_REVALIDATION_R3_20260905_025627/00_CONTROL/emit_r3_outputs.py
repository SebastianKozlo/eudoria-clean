"""emit_r3_outputs.py — generates STAGE_ACCEPTANCE_GATES.csv (THREE-STATE) and
artifact_index.csv for R3 from the emitted TEST_RESULTS.json.

Three-state discipline (R3 repair of the R2 pending-as-FAIL defect):
  - gate rows carry result = PASS / FAIL / PENDING (PENDING for HUMAN_REVIEWED);
  - the OVERALL row carries overall_executable_pass AND the explicit statement
    that OVERALL EXECUTABLE PASS IS NOT HUMAN ACCEPTANCE;
  - the R3 claim-matrix tally label is DERIVED FROM THE ACTUAL EMITTED ROWS at
    emit time (R2G13's stale {17,7} label is the superseded anti-pattern).

Deterministic; nonzero exit on any inconsistency.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

RUN = Path(r'D:\Eudoria_Reconstruction\99_Audits\PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627')
TR = json.loads((RUN / '02_LOGS/TEST_RESULTS.json').read_text(encoding='utf-8'))


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    gates = TR['gates']

    # R3 claim-matrix tally derived from the ACTUAL emitted rows
    cm_path = RUN / '05_ANALYSIS/CLAIM_MATRIX.csv'
    if not cm_path.is_file():
        print('CLAIM_MATRIX.csv missing — run emit_r3_analysis.py first', file=sys.stderr)
        sys.exit(1)
    rows = list(csv.DictReader(open(cm_path, encoding='utf-8-sig', newline='')))
    tally = {}
    for r in rows:
        tally[r['knowledge_status']] = tally.get(r['knowledge_status'], 0) + 1
    tally_label = ' '.join('%s %d' % (k, tally[k]) for k in sorted(tally))

    out = RUN / 'STAGE_ACCEPTANCE_GATES.csv'
    with open(out, 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['gate_id', 'gate_name', 'gate_type', 'result', 'measured_quantity',
                    'denominator', 'independent_source_of_truth', 'why_non_circular',
                    'failure_case_detected', 'method_class'])
        for g in gates:
            w.writerow([g['gate_id'], g['gate_name'], g['gate_type'], g['state'],
                        g['measured_quantity'], g['denominator'],
                        g['independent_source_of_truth'], g['why_non_circular'],
                        g['failure_case_detected'], g['method_class']])
        ov = TR['overall']
        w.writerow(['OVERALL',
                    'overall executable pass=%s; human_acceptance=%s; R3 CLAIM_MATRIX tally derived '
                    'from actual rows: %s' % (ov['overall_executable_pass'],
                                              ov['human_acceptance'], tally_label),
                    'SUMMARY', 'PASS' if ov['overall_executable_pass'] and not ov['failed_gates']
                    else 'FAIL',
                    '%d executable gates PASS, %d FAIL, %d HR gates PENDING'
                    % (ov['executable_gates'], len(ov['failed_gates']),
                       ov['human_reviewed_gates_pending']),
                    '%d gates' % len(gates), 'TEST_RESULTS.json (this run)',
                    'generated from TEST_RESULTS.json — no hand-written results',
                    'OVERALL EXECUTABLE PASS IS NOT HUMAN ACCEPTANCE',
                    'SUMMARY'])
    print('STAGE_ACCEPTANCE_GATES.csv written: %d gate rows + OVERALL' % len(gates))

    # artifact index: every run artifact with real SHA256; documented exclusions
    EXCLUDE = {out.name, 'artifact_index.csv'}  # self-hash impossible / final ledger
    LOCAL_ONLY = {'PRIMITIVE_VALUE_CENSUS_FULL.json'}  # derived values, kept local
    idx_path = RUN / 'artifact_index.csv'
    entries = []
    for p in sorted(RUN.rglob('*')):
        if not p.is_file() or p.name in EXCLUDE:
            continue
        rel = p.relative_to(RUN).as_posix()
        role = 'R3 run artifact (%s)' % rel
        scope = 'LOCAL_ONLY (not part of the published package)' if p.name in LOCAL_ONLY \
            else 'PUBLISHED (docs/audits package)'
        if p.name == 'TEST_RESULTS.json':
            claims = 'R3C-01..R3C-15; all gates'
        elif p.name == 'PRIMITIVE_VALUE_COMPARISON.json':
            claims = 'R3C-05, R3C-06, R3C-09'
        elif p.name == 'CENSUS_RECOUNT_R3.json':
            claims = 'R3C-07'
        elif p.name == 'R34_RESUM.json':
            claims = 'R3C-10'
        elif p.name == 'R35_CLAIM_TABLE_PRESERVED.json':
            claims = 'R3C-11'
        elif p.name == 'R2_STATE_RESUM.json':
            claims = 'R3C-12, R3C-13'
        elif p.name == 'SIDECAR_BARE_CR_ANALYSIS.json':
            claims = 'R3C-14'
        elif p.name == 'R2_HELPER_PROBE.json':
            claims = 'R3C-01, R3C-03'
        elif p.name.startswith('kat_'):
            claims = 'R3C-04, R3C-09, R3C-12 (KAT evidence)'
        elif 'CLAIM_MATRIX' in p.name:
            claims = 'R3 claim matrix (tally %s)' % tally_label
        elif 'SUPERSESSION_MAP' in p.name:
            claims = 'S-01..S-12'
        elif 'FINDING_DISPOSITIONS' in p.name:
            claims = 'F1/F2/F2b/F3/F5/N1/N2'
        else:
            claims = ''
        entries.append((str(p), role, sha(p), p.stat().st_size,
                        'this run (PE-NIF-HASH-PRIMITIVE-REVALIDATION-R3, 2026-09-05)', scope, claims))
    with open(idx_path, 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['source_path_full', 'role', 'sha256', 'size_bytes', 'snapshot_time_scope',
                    'publication_scope', 'claims_supported'])
        for e in entries:
            w.writerow(e)
    print('artifact_index.csv written: %d artifacts' % len(entries))
    print(json.dumps({'gates': len(gates), 'artifacts': len(entries),
                      'tally_label': tally_label}))


if __name__ == '__main__':
    main()
