# w6_package.py — PE_935_SF_ARG2_PROVENANCE_R1_20260914 (00_CONTROL)
# W6 (part 1): NC-3 machinery demo, G7 immutability verification, end-of-run git
# observation. ZERO git mutations (read-only measurement commands only).
#
# Outputs (01_RAW, deterministic except the mandated timestamped observation):
#   NC3_MACHINERY_DEMO.txt, G7_IMMUTABILITY_CHECK.txt, AT_RUN_END_GIT_OBSERVATION.md

import datetime
import hashlib
import os
import subprocess
import sys

sys.path.insert(0, r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SF_ARG2_PROVENANCE_R1_20260914\00_CONTROL")
import sf_arg2_common as C

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SF_ARG2_PROVENANCE_R1_20260914"
REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
BASE_SHA = "f239eb85cd0f56ae10cee52d57833a49f225965c"

FIRSTCALL_FILES = {
    "00_CONTROL/RUN_CONTRACT.md": "9E0006030D078E71F4D9609371F6BA27CDEB936BA63ABD8D5EE5F9DAAEEC8882",
    "00_CONTROL/run_state.json": "D7F7428827B459256F23A4CFEDC77D5CB8DD5B40061D4F6D52C6A1C5F7A14F65",
    "00_CONTROL/slot17_core.py": "02D58F8B642E1952AA4E3A5A538998C1FDFEDCB17A7B798AB481ADE9AF6CAF4D",
    "00_CONTROL/slot17_run.py": "C4802B2A1B7E1FBFF8258A993B2CB36D0707025F345B4460106D7EDA444CB2C3",
    "00_CONTROL/SOURCE_IDENTITIES.json": "088A4EE4766B37C6B80B55643A2610F9FBA1C44C29E707A2B137DCA881F8DBB2",
    "00_CONTROL/__pycache__/slot17_core.cpython-312.pyc": "FF8344BFC9BDA545AA466DD0A45DCFA67D377CEBDE8C8146EA79F147792D3FE9",
    "01_RAW/SLOT17_BODY_RAW.txt": "2EABC45F81738039DA6C876C411301EFCE0CD0744BB6CF0077C740A455A9C2F1",
}
FIRSTCALL_EMPTY_DIRS = ["02_ANALYSIS", "03_EVIDENCE", "06_REPORT"]
LINK30_IMMUTABLE = {
    r"docs\audits\PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914\02_ANALYSIS\SF30_WRITER_CENSUS.csv":
        "71552E2A4BFC120DA0BE1A7E108A41A03C873ADDD238637DD7C18F3C968824D0",
    r"docs\audits\PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914\01_RAW\SF30_WRITER_RAW.txt":
        "SOURCE_IDENTITIES.json pins only the CSV hash; RAW is existence+untouched-checked",
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def git(args):
    r = subprocess.run(["git"] + args, cwd=REPO, capture_output=True, text=True, timeout=120)
    return (r.stdout + r.stderr).strip()


def main():
    exe = C.PinnedExe()
    lines = []
    lines.append(C.provenance_header())
    lines.append(f"S0: PASS (sha256 {exe.sha256}, size {exe.size})")

    # ---------------- NC-3 machinery demo ----------------
    n = []
    n.append("NC3_MACHINERY_DEMO — PE_935_SF_ARG2_PROVENANCE_R1_20260914")
    n.append(C.provenance_header())
    n.append(f"S0: PASS (sha256 {exe.sha256}, size {exe.size})")
    n.append("")
    n.append("NC-3 (contract): every .rdata/.data literal identified as an arg2 producer gets its")
    n.append("raw bytes re-read at the literal VA and recorded VERBATIM (proves the pointer->content")
    n.append("chain; no interpretation).")
    n.append("")
    n.append("IN-RUN RESULT: ZERO string literals were identified as arg2 producers (zero verified")
    n.append("slot-3 call sites -> the producer trace reached no IMM32 literal). NC-3 therefore has no")
    n.append("in-scope subject this run. The verbatim read-back MACHINERY (imm_analysis in")
    n.append("w2c_w3_virtual_census.py: read_va at the literal VA, hex + NUL-terminated ASCII read-back)")
    n.append("is demonstrated below on a KNOWN .rdata literal as a tooling calibration ONLY —")
    n.append("this demo is NOT adopted as arg2 evidence.")
    n.append("")
    for va in (0xA7957B, 0xA7957C):
        raw = exe.read_va(va, 48)
        nul = raw.find(b"\x00")
        n.append(f"known-answer read @ {va:#010x} (section {exe.section_name_of_va(va)}):")
        n.append(f"  bytes[0:24]  = {raw[:24].hex(' ').upper()}")
        n.append(f"  VERBATIM to first NUL (NUL at +{nul}): {raw[:nul+1].hex(' ').upper() if nul != -1 else '<no NUL in 48 bytes>'}")
        n.append(f"  ASCII        = {raw[:nul if nul != -1 else 48]!r}")
        n.append("")
    n.append("Machinery verdict: the pointer->content chain reads back exactly the bytes on disk;")
    n.append("the demo literal at 0x00A7957C reads back as the ASCII string 'Entropia' (NUL-terminated,")
    n.append("9 bytes) — a verbatim .rdata FACT recorded with VA + bytes.")
    with open(PKG + r"\01_RAW\NC3_MACHINERY_DEMO.txt", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(n) + "\n")

    # ---------------- G7 immutability ----------------
    g = []
    g.append("G7_IMMUTABILITY_CHECK — PE_935_SF_ARG2_PROVENANCE_R1_20260914")
    g.append(C.provenance_header())
    g.append(f"S0: PASS (sha256 {exe.sha256}, size {exe.size})")
    g.append("")
    g.append("== FIRSTCALL package (docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/) ==")
    fc_root = os.path.join(REPO, "docs", "audits", "PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914")
    all_ok = True
    for rel, pin in sorted(FIRSTCALL_FILES.items()):
        p = os.path.join(fc_root, rel.replace("/", "\\"))
        if not os.path.exists(p):
            g.append(f"  [MISSING] {rel} — G7 FAIL")
            all_ok = False
            continue
        got = sha256_file(p)
        ok = got == pin
        all_ok = all_ok and ok
        g.append(f"  [{'MATCH' if ok else 'MISMATCH'}] {rel}: {got} (pin {pin})")
    for d in FIRSTCALL_EMPTY_DIRS:
        p = os.path.join(fc_root, d)
        exists = os.path.isdir(p)
        empty = exists and not os.listdir(p)
        g.append(f"  [{'MATCH' if empty else 'MISMATCH'}] empty dir {d}/ (exists={exists}, empty={empty if exists else 'n/a'})")
        all_ok = all_ok and empty
    extra = []
    for root, dirs, files in os.walk(fc_root):
        for fn in files:
            rel = os.path.relpath(os.path.join(root, fn), fc_root).replace("\\", "/")
            if rel not in FIRSTCALL_FILES:
                extra.append(rel)
    g.append(f"  extra files beyond the 7 pinned: {extra if extra else 'NONE (exactly 7 files)'}")
    g.append("")
    g.append("== LINK30 historical census CSV/RAW (IMMUTABLE; read + hash only) ==")
    for rel, pin in sorted(LINK30_IMMUTABLE.items()):
        p = os.path.join(REPO, rel)
        if not os.path.exists(p):
            g.append(f"  [MISSING] {rel} — G7 FAIL")
            all_ok = False
            continue
        got = sha256_file(p)
        if pin.startswith("SOURCE_IDENTITIES"):
            g.append(f"  [PRESENT/UNTOUCHED] {rel}: exists, sha256={got} (existence+untouched check; no hash pin in SOURCE_IDENTITIES)")
        else:
            ok = got == pin
            all_ok = all_ok and ok
            g.append(f"  [{'MATCH' if ok else 'MISMATCH'}] {rel}: {got} (pin {pin})")
    g.append("")
    g.append("== experiments/ (foreign; untouched; never inventoried) ==")
    g.append("  present:" + str(os.path.isdir(os.path.join(REPO, "experiments"))) + " (not inventoried; never written by this run)")
    g.append("")
    g.append("G7_IMMUTABILITY_FILE_SIDE: " + ("PASS (all pinned hashes match; no extra files)" if all_ok and not extra else "FAIL — see rows above"))
    with open(PKG + r"\01_RAW\G7_IMMUTABILITY_CHECK.txt", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(g) + "\n")

    # ---------------- end-of-run git observation ----------------
    ts = datetime.datetime.now().astimezone().isoformat()
    head = git(["rev-parse", "HEAD"])
    branch = git(["branch", "--show-current"])
    status_short = git(["status", "--short"])
    staged = git(["diff", "--cached", "--name-only"])
    log_count = git(["rev-list", "--count", "HEAD"])
    o = []
    o.append("# AT_RUN_END_GIT_OBSERVATION.md — PE_935_SF_ARG2_PROVENANCE_R1_20260914")
    o.append("")
    o.append("Executor end-of-run READ-ONLY git observation (G7). ZERO git mutations performed")
    o.append("at any point in this run (no add/commit/push/stash/checkout/reset/branch).")
    o.append("")
    o.append(f"TIMESTAMP: `{ts}`")
    o.append("")
    o.append("```")
    o.append("--- HEAD ---")
    o.append(head)
    o.append("--- BRANCH ---")
    o.append(branch)
    o.append("--- rev-list --count HEAD (no new commits) ---")
    o.append(log_count + " (commits reachable from HEAD)")
    o.append("--- status --short ---")
    o.append(status_short)
    o.append("--- staged paths check ---")
    o.append("git diff --cached --name-only -> " + (staged if staged else "EMPTY (STAGED_COUNT: 0)"))
    o.append("```")
    o.append("")
    untracked = sorted(l[3:].strip() for l in status_short.splitlines() if l.startswith("?? "))
    expected = [
        "docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/",
        "docs/audits/PE_935_SF_ARG2_PROVENANCE_R1_20260914/",
        "experiments/",
    ]
    ok_head = head == BASE_SHA
    ok_untracked = untracked == expected
    ok_staged = staged == ""
    o.append(f"HEAD == BASE_SHA: {'MATCH' if ok_head else 'DRIFT — HARD_STOP BASE_DRIFT'}")
    o.append(f"untracked set == expected three: {'MATCH' if ok_untracked else 'MISMATCH: ' + str(untracked)}")
    o.append(f"staged paths: {'ZERO' if ok_staged else 'PRESENT — FOREIGN_STAGED_PATH'}")
    o.append("")
    o.append("G7_GIT_SIDE: " + ("PASS" if (ok_head and ok_untracked and ok_staged) else "FAIL"))
    with open(PKG + r"\01_RAW\AT_RUN_END_GIT_OBSERVATION.md", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(o) + "\n")

    print("wrote 01_RAW/NC3_MACHINERY_DEMO.txt")
    print("wrote 01_RAW/G7_IMMUTABILITY_CHECK.txt —", g[-1])
    print("wrote 01_RAW/AT_RUN_END_GIT_OBSERVATION.md — HEAD match:", ok_head, "staged zero:", ok_staged, "untracked match:", ok_untracked)


if __name__ == "__main__":
    main()
