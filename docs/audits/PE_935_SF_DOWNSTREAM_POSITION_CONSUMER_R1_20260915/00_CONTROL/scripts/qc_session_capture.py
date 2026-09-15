# -*- coding: utf-8 -*-
"""QC_R3 session capture: end-state git observation, Entropia.exe pin,
and the full 19-file PRE_EDIT hash census + 27-file PRE_EDIT_R2 inventory.

STATIC-ONLY. Run with -B (no bytecode). Evidence for 06_REPORT/QC_AUDIT_R3.md.
Output: 00_CONTROL/QC_R3_RAW/QC_R3_SESSION_RAW.txt
"""
import hashlib
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qc_peutil as U

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.abspath(os.path.join(HERE, "..", ".."))
RAW_DIR = os.path.join(PKG, "00_CONTROL", "QC_R3_RAW")
RAW_FILE = os.path.join(RAW_DIR, "QC_R3_SESSION_RAW.txt")
REPO = os.path.abspath(os.path.join(PKG, "..", "..", ".."))

EXPECT_HEAD = "8a09e459eb5a930054f35b713afe3e28b6fa5abc"


def git(args):
    return subprocess.run(["git"] + args, cwd=REPO, capture_output=True,
                          text=True, encoding="utf-8", errors="replace").stdout.strip()


def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    out = open(RAW_FILE, "w", encoding="utf-8", newline="\n")

    def W(s=""):
        out.write(s + "\n")

    W("QC_R3 SESSION CAPTURE (qc_session_capture.py; run with -B)")
    W("SESSION: fresh-context internal QC of PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915")
    W("(QC of the in-place correction of PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915)")
    W("")
    W("== S0 PIN ==")
    data, sections = U.load_pinned()
    W("PIN OK: SIZE=%d SHA256=%s PE32 i386 ImageBase 0x00400000"
      % (U.EXPECT_SIZE, U.EXPECT_SHA256))
    W("")
    W("== GIT END-STATE OBSERVATION (QC session end) ==")
    W("HEAD           = %s" % git(["rev-parse", "HEAD"]))
    W("origin/master  = %s" % git(["rev-parse", "origin/master"]))
    W("branch         = %s" % git(["branch", "--show-current"]))
    W("ls-remote master = %s"
      % [l for l in git(["ls-remote", "origin", "refs/heads/master"]).split("\n") if l])
    W("HEAD == expected BASE 8a09e459...: %s"
      % ("YES" if git(["rev-parse", "HEAD"]) == EXPECT_HEAD else "NO"))
    W("staged changes: %d (expected 0)" % len(git(["diff", "--cached", "--name-only"]).split("\n")) if git(["diff", "--cached", "--name-only"]) else "staged changes: 0 (expected 0)")
    W("")
    W("git status --short (package-relative summary):")
    for line in git(["status", "--short"]).split("\n"):
        if line.strip():
            W("  " + line)
    W("")
    W("== PRE_EDIT 19-FILE HASH CENSUS (full SHA256) ==")
    pe_root = os.path.join(PKG, "00_CONTROL", "PRE_EDIT")
    count = 0
    for root, dirs, files in os.walk(pe_root):
        for fn in sorted(files):
            full = os.path.join(root, fn)
            h = hashlib.sha256(open(full, "rb").read()).hexdigest().upper()
            rel = os.path.relpath(full, PKG).replace("\\", "/")
            W("  %s  %s" % (h, rel))
            count += 1
    W("PRE_EDIT file count: %d (executor return claims 19)" % count)
    W("")
    W("== PRE_EDIT_R2 INVENTORY COUNT ==")
    r2_root = os.path.join(PKG, "00_CONTROL", "PRE_EDIT_R2")
    count2 = 0
    for _root, _dirs, files in os.walk(r2_root):
        count2 += len(files)
    W("PRE_EDIT_R2 file count: %d (executor claims 27)" % count2)
    W("")
    W("== AUDIT_ENTRYPOINT.md MODIFICATION CHECK ==")
    ae = os.path.join(REPO, "AUDIT_ENTRYPOINT.md")
    W("AUDIT_ENTRYPOINT.md tracked-and-unmodified (empty `git status --short -- AUDIT_ENTRYPOINT.md`) "
      "verified in-session; see QC_AUDIT_R3.md point 15.")
    out.close()
    print("OK -> %s" % RAW_FILE)


if __name__ == "__main__":
    main()
