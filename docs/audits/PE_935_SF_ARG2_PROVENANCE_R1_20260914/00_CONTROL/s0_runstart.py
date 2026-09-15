# s0_runstart.py — PE_935_SF_ARG2_PROVENANCE_R1_20260914 (00_CONTROL)
# G0: AT_RUN_START git observation (timestamped, mandated) + fail-closed EXE
# identity verification. ZERO git mutations — read-only measurement commands only
# (rev-parse / branch / ls-remote / status / worktree list / diff --cached).
#
# Outputs:
#   01_RAW/AT_RUN_START_GIT_OBSERVATION.md  (timestamped observation file)
#   01_RAW/IDENTITY_VERIFICATION.txt       (deterministic S0 record)
#
# Run with: python -B s0_runstart.py   (canonical interpreter)

import datetime
import subprocess
import sys

sys.path.insert(0, r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SF_ARG2_PROVENANCE_R1_20260914\00_CONTROL")
import sf_arg2_common as C

REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SF_ARG2_PROVENANCE_R1_20260914"
BASE_SHA = "f239eb85cd0f56ae10cee52d57833a49f225965c"


def git(args):
    r = subprocess.run(
        ["git"] + args, cwd=REPO, capture_output=True, text=True, timeout=120
    )
    return (r.stdout + r.stderr).strip()


def main():
    ts = datetime.datetime.now().astimezone().isoformat()

    # ---------------- S0 fail-closed identity ----------------
    s0_lines = []
    s0_lines.append("IDENTITY_VERIFICATION — PE_935_SF_ARG2_PROVENANCE_R1_20260914 (S0 fail-closed)")
    s0_lines.append(C.provenance_header())
    exe = C.PinnedExe()  # raises on any mismatch -> no downstream
    s0_lines.append("S0_RESULT: PASS")
    s0_lines.append(f"exe_path      : {exe.path}")
    s0_lines.append(f"size_measured : {exe.size} (pin {C.PIN_SIZE})")
    s0_lines.append(f"sha256_measured: {exe.sha256}")
    s0_lines.append(f"sha256_pin    : {C.PIN_SHA256_UPPER}")
    s0_lines.append(f"machine       : {exe.machine:#06x} (pin 0x014C)")
    s0_lines.append(f"opt_magic     : 0x010B (PE32, pin)")
    s0_lines.append(f"image_base    : {exe.image_base:#010x} (pin 0x00400000)")
    s0_lines.append("sections:")
    for s in exe.sections:
        s0_lines.append(
            f"  {s['name']:<8} vaddr={s['vaddr']:#010x} vsize={s['vsize']:#010x} "
            f"rawptr={s['rawptr']:#010x} rawsize={s['rawsize']:#010x}"
        )
    with open(PKG + r"\01_RAW\IDENTITY_VERIFICATION.txt", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(s0_lines) + "\n")

    # ---------------- AT_RUN_START git observation ----------------
    head = git(["rev-parse", "HEAD"])
    branch = git(["branch", "--show-current"])
    origin_master = git(["rev-parse", "origin/master"])
    ls_remote = git(["ls-remote", "origin", "refs/heads/master"])
    status_short = git(["status", "--short"])
    worktree_list = git(["worktree", "list"])
    remote_v = git(["remote", "-v"])
    staged = git(["diff", "--cached", "--name-only"])

    lines = []
    lines.append("# AT_RUN_START_GIT_OBSERVATION.md — PE_935_SF_ARG2_PROVENANCE_R1_20260914")
    lines.append("")
    lines.append("Recorded by pe-reconstruction (executor) at run start, under PE-MASTER loop")
    lines.append("`2ed038db-5d2e-4e7e-b679-2d29bf57501a` (EU935-M1, Phase 2). READ-ONLY observation —")
    lines.append("the executor performed ZERO git mutations (no add/commit/push/stash/checkout/reset/branch).")
    lines.append("")
    lines.append(f"Repo: `{REPO}` · expected HEAD (BASE_SHA) = `{BASE_SHA}`.")
    lines.append("")
    lines.append(f"TIMESTAMP: `{ts}`")
    lines.append("")
    lines.append("```")
    lines.append("--- HEAD ---")
    lines.append(head)
    lines.append("--- BRANCH ---")
    lines.append(branch)
    lines.append("--- origin/master (local cached ref) ---")
    lines.append(origin_master)
    lines.append("--- remote -v ---")
    lines.append(remote_v)
    lines.append("--- ls-remote origin refs/heads/master ---")
    lines.append(ls_remote)
    lines.append("--- status --short ---")
    lines.append(status_short)
    lines.append("--- worktree list ---")
    lines.append(worktree_list)
    lines.append("--- staged paths check ---")
    lines.append("git diff --cached --name-only -> " + (staged if staged else "EMPTY (STAGED_COUNT: 0)"))
    lines.append("```")
    lines.append("")
    lines.append("## EXPECTED vs OBSERVED")
    lines.append("")
    lines.append("| Item | Expected | Observed | Verdict |")
    lines.append("|---|---|---|---|")
    v1 = "MATCH" if head == BASE_SHA else "MISMATCH -> HARD_STOP BASE_DRIFT"
    lines.append(f"| HEAD | {BASE_SHA} | {head} | {v1} |")
    v2 = "MATCH" if branch == "master" else "MISMATCH"
    lines.append(f"| Branch | master | {branch} | {v2} |")
    v3 = "MATCH" if origin_master == BASE_SHA else "MISMATCH -> HARD_STOP BASE_DRIFT"
    lines.append(f"| origin/master (local ref) | == BASE_SHA | {origin_master} | {v3} |")
    live = ls_remote.split()[0] if ls_remote.split() else "<EMPTY>"
    v4 = "MATCH" if live == BASE_SHA else "MISMATCH -> HARD_STOP BASE_DRIFT"
    lines.append(f"| Live remote (ls-remote origin refs/heads/master) | == BASE_SHA | {ls_remote} | {v4} |")
    untracked = sorted(
        l[3:].strip() for l in status_short.splitlines() if l.startswith("?? ")
    )
    expected_untracked = [
        "docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/",
        "docs/audits/PE_935_SF_ARG2_PROVENANCE_R1_20260914/",
        "experiments/",
    ]
    v5 = (
        "MATCH"
        if untracked == expected_untracked
        else f"MISMATCH -> observed set {untracked}"
    )
    lines.append(
        f"| Untracked set | exactly {expected_untracked} | {untracked} | {v5} |"
    )
    v6 = "MATCH (zero staged)" if staged == "" else "MISMATCH -> HARD_STOP FOREIGN_STAGED_PATH"
    lines.append(f"| Staged paths | none | {'EMPTY' if staged == '' else staged} | {v6} |")
    lines.append("")
    lines.append("## EXECUTION DECISION")
    ok = all(x.startswith("MATCH") for x in (v1, v2, v3, v4, v5, v6))
    lines.append("")
    if ok:
        lines.append("G0 git side: PASS — no HARD_STOP armed. Proceed to W1.")
    else:
        lines.append("G0 git side: FAIL — HARD_STOP condition present. Report to PE-MASTER; no downstream.")
    lines.append("")
    with open(
        PKG + r"\01_RAW\AT_RUN_START_GIT_OBSERVATION.md", "w", encoding="utf-8", newline="\n"
    ) as f:
        f.write("\n".join(lines) + "\n")

    print("S0:", s0_lines[1] if len(s0_lines) > 1 else "?")
    print("S0_RESULT: PASS (identity)")
    print("git G0:", "PASS" if ok else "FAIL")
    print("wrote 01_RAW/IDENTITY_VERIFICATION.txt")
    print("wrote 01_RAW/AT_RUN_START_GIT_OBSERVATION.md")
    if not ok:
        sys.exit(2)


if __name__ == "__main__":
    main()
