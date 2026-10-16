# -*- coding: utf-8 -*-
"""Runner: p935_run.py --phase <name>. Appends an attempt record per phase."""
import sys, os, json, time, argparse, traceback
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p935_core as C
import p935_phases1 as P1
import p935_phases2 as P2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", required=True)
    args = ap.parse_args()
    phases = {
        "preflight": P1.phase_preflight,
        "prereg": P1.phase_prereg,
        "falsify": P1.phase_falsify,
        "hashpass1": lambda: P1.phase_hashpass(1),
        "pemap": P1.phase_pemap,
        "window_roster": P1.phase_window_roster,
        "textscan": P1.phase_textscan,
        "hashpass2": lambda: P1.phase_hashpass(2),
        "analyze": P2.phase_analyze,
        "conflict_investigation": P2.phase_conflict_investigation,
        "evidence": P2.phase_evidence,
        "report": P2.phase_report,
        "qc": P2.phase_qc,
        "manifest": P2.phase_manifest,
    }
    fn = phases.get(args.phase)
    if fn is None:
        print(json.dumps({"phase": args.phase, "status": "UNKNOWN_PHASE"}))
        sys.exit(2)
    t0 = time.time()
    rec = {"ts": C.utcnow(), "phase": args.phase, "argv": sys.argv[1:],
           "tool": os.path.abspath(__file__), "python": sys.version.split()[0]}
    code = 0
    try:
        fn()
        rec["status"] = "OK"
    except SystemExit as e:
        code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
        rec["status"] = "EXIT_%d" % code
        raise
    except Exception as e:
        code = 1
        rec["status"] = "FAIL"
        rec["error"] = "%s: %s" % (type(e).__name__, str(e))
        rec["traceback_tail"] = traceback.format_exc().splitlines()[-6:]
        raise
    finally:
        rec["duration_ms"] = int((time.time() - t0) * 1000)
        rec["exit_code"] = code
        try:
            C.append_jsonl(C.ATTEMPT_LOG, rec)
        except Exception:
            pass
    sys.exit(code)


if __name__ == "__main__":
    main()
