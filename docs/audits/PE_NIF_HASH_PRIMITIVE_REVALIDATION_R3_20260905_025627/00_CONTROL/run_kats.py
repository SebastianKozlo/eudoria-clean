"""run_kats.py — executable known-answer test runner (R3 prompt item 3 + item 5).

One invocation = one primitive set; process exit code is 0 iff every asserted
predicate of that set passes, nonzero (1) otherwise. The revalidation driver
(revalidate_r3.py) invokes this as a subprocess per set and captures ACTUAL
exit codes — negative controls must exit nonzero, corrected sets must exit 0.

Sets:
  corrected              — stage-local corrected primitives vs zlib oracle +
                           published constants + incremental/streaming identity.
  r2_literal_python      — exact-int Python transcription of the two R2 helper
                           declarations, run against THE SAME predicates: must
                           FAIL (negative control: unchanged R2 helpers).
  wrong_value_controls   — deliberately wrong-value implementations (aggregate
                           zero-match preserving) against the same predicates:
                           must FAIL (negative control proving value-identity
                           gates are required).
  three_state_corrected  — PENDING/PASS/FAIL distinct through the corrected
                           serializer: must PASS.
  three_state_r2_coercion— R2 run_gates.py bool(ok) coercion against the same
                           three-state predicates: must FAIL (pending-as-false
                           serialization detected).
  oracle_self_vectors    — the oracles' own published known vectors: must PASS.

Usage: python run_kats.py --set <name> --out <json path>
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r3_primitives as rp  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--set', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()

    payload = {'set': args.set}
    exit_code = 0

    if args.set == 'corrected':
        res = rp.run_kat('corrected')
        payload.update(res)
        payload['oracle_self_vectors'] = rp.check_published_constants()
        if not res['all_pass'] or not all(c['pass'] for c in payload['oracle_self_vectors']):
            exit_code = 1
    elif args.set == 'r2_literal_python':
        res = rp.run_kat('r2_literal_python')
        payload.update(res)
        payload['expected_outcome'] = 'FAIL (negative control: unchanged R2 helper semantics)'
        exit_code = 0 if res['all_pass'] else 1  # nonzero exit == control detected
    elif args.set == 'wrong_value_controls':
        res = rp.run_kat('wrong_value_controls')
        payload.update(res)
        payload['expected_outcome'] = 'FAIL (negative control: wrong values must not pass value identity)'
        exit_code = 0 if res['all_pass'] else 1
    elif args.set == 'three_state_corrected':
        cases = [(None, 'PENDING'), (True, 'PASS'), (False, 'FAIL')]
        checks = [{'input': 'None' if k is None else str(k), 'expected': v,
                   'actual': rp.three_state(k), 'pass': rp.three_state(k) == v} for k, v in cases]
        payload['cases'] = checks
        payload['all_pass'] = all(c['pass'] for c in checks)
        if not payload['all_pass']:
            exit_code = 1
    elif args.set == 'three_state_r2_coercion':
        # The SAME three-state predicates applied to R2's bool(ok) coercion:
        # pending (None) must NOT serialize as FAIL — R2's coercion does.
        cases = [
            {'predicate': "serialize(None) == 'PENDING'", 'actual': rp.bool_coerce(None),
             'expected': 'PENDING', 'pass': rp.bool_coerce(None) == 'PENDING'},
            {'predicate': "serialize(True) == 'PASS'", 'actual': rp.bool_coerce(True),
             'expected': 'PASS', 'pass': rp.bool_coerce(True) == 'PASS'},
            {'predicate': "serialize(False) == 'FAIL'", 'actual': rp.bool_coerce(False),
             'expected': 'FAIL', 'pass': rp.bool_coerce(False) == 'FAIL'},
        ]
        payload['cases'] = cases
        payload['all_pass'] = all(c['pass'] for c in cases)
        payload['expected_outcome'] = 'FAIL (negative control: pending-as-false serialization must be detected)'
        exit_code = 0 if payload['all_pass'] else 1
    elif args.set == 'oracle_self_vectors':
        checks = rp.check_published_constants()
        payload['oracle_self_vectors'] = checks
        payload['all_pass'] = all(c['pass'] for c in checks)
        if not payload['all_pass']:
            exit_code = 1
    else:
        print('unknown set ' + args.set, file=sys.stderr)
        sys.exit(2)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=1) + '\n', encoding='utf-8')
    print(json.dumps({'set': args.set, 'all_pass': payload.get('all_pass'),
                      'exit_code': exit_code}))
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
