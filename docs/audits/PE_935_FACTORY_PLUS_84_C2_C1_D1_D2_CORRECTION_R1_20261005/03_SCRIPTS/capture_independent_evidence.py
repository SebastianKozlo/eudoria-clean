# capture_independent_evidence.py
# RUN: PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005
# Independent-evidence capture for the synthetic fixtures ONLY:
#   (1) GNU objdump (WSL, GNU Binutils for Debian 2.44) raw disassembly of
#       every synthetic fixture used by this run's falsifiers and controls
#       (NEW-G, NEW-F, A1/A2/B/C/D/E, the H1 16-bit rm table, the H2
#       grouped-opcode positive/negative controls, the P2-2 decoder unit
#       vectors, and THIS RUN's D1 fixtures: the two 0F 73 /4 negative
#       forms, the six contract legal controls and the D1 downstream
#       falsifier stream);
#   (2) the VERBATIM BASE (THREE-P2) commit message (immutable history; this
#       run's supersession ledger quotes it - history is never edited).
# The production decoder is NEVER its own source of truth: every expected
# instruction boundary below is locked from the D1 contract + the ISA
# reference BEFORE the corrected decoder's D1 behaviour is evaluated
# against these records (the fixtures' expected values are fixed in this
# file; objdump is run to capture the raw oracle; the corrected decoder is
# then checked AGAINST these - never the reverse).
# Outputs: 01_RAW/D1_INDEPENDENT_ORACLE_RECORDS.json,
#          01_RAW/BASE_COMMIT_MESSAGE_VERBATIM.txt (--out/--out-cm overrides).

import argparse
import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

RUN = (r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
       r"\PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005")
REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
BASE_SHA = "9d31a82b6589f46e9ca6c75c6e323b433c1ebf92"
TMP = r"C:\Users\User\AppData\Local\Temp\opencode\d1d2_oracle"

# Every synthetic fixture oracle-checked this run. EXPECTED_* values are
# locked from the D1 contract + the ISA reference BEFORE the corrected
# decoder is evaluated; the production decoder is then checked AGAINST
# these (never the reverse).
FIXTURES = [
    # (name, hex, expected_boundaries_human, role)
    ("NEW_G_66_0F_84_je_rel16", "66 0F 84 00 00 B8 00 E8 01 00 00 00 C3",
     "je rel16 +0..+5 (5 B); mov eax,0x1e800 +5..+10; add [eax],al +10..+12; ret +12",
     "P2-2 NEW-G falsifier (REPRODUCED this run): the C2 decoder measured the first instruction as 7 and fabricated a CALL edge from the E8 at +7"),
    ("JCC_REL32_0F_84", "0F 84 00 00 00 00",
     "je rel32 +0..+6 (6 B)", "P2-2 unit: unprefixed near Jcc rel32"),
    ("JCC_66REL16_0F_84", "66 0F 84 00 00",
     "je rel16 +0..+5 (5 B)", "P2-2 unit: 66 0F 84 rel16"),
    ("JCC_66REL16_0F_8F", "66 0F 8F 00 00",
     "jg rel16 +0..+5 (5 B)", "P2-2 unit: 66 0F 8F rel16 (whole 0x80..0x8F class)"),
    ("E8_REL32", "E8 01 00 00 00",
     "call rel32 +0..+5 (5 B)", "P2-2 unit: ordinary E8 rel32 positive form"),
    ("E8_66_REL16", "66 E8 01 00",
     "callw rel16 +0..+4 (4 B)", "P2-2 unit: existing 66 E8 rel16 case"),
    ("SHUFPS_0F_C6_ib", "0F C6 C0 E8 00",
     "shufps xmm0,xmm0,0xe8 +0..+4 (4 B)", "P2-2 unit: existing 0F C6 /r ib case"),
    ("ADDR16_67_8B_06", "67 8B 06 84 00 90",
     "mov eax,[0x84] (16-bit addr) +0..+5 (5 B)", "P2-2 unit: existing 67-address-size case"),
    ("NEW_F_anchor_conflict", "B8 00 E8 01 00 00 00 90 CC",
     "mov eax,0x1e800 +0..+5; add [eax],al +5..+7; nop +7; int3 +8",
     "P2-1 NEW-F falsifier (REPRODUCED this run, cached + uncached): anchor A covers the E8 at +2 as immediate data; anchor B lands exactly at +2 -> ANCHOR_CONFLICT"),
    ("A1_B8_CC_CC_E8_imm", "B8 CC CC E8 00 00 00 00 C3",
     "mov eax,0xe8cccc +0..+5; ...", "AF2 counterexample A1 (REPRODUCED this run)"),
    ("A2_B8_C3_CC_E8_imm", "B8 C3 CC E8 00 00 00 00 C3",
     "mov eax,0xe8ccc3 +0..+5; ...", "AF2 counterexample A2 (REPRODUCED this run)"),
    ("B_0F_C6_shufps_imm8", "0F C6 C0 E8 00 00 00 00 C3",
     "shufps +0..+4; ...", "AF2 counterexample B (REPRODUCED this run)"),
    ("C_67_8B_06_disp16", "67 8B 06 E8 00 90 C3",
     "mov eax,[0xe8] +0..+5; nop +5; ret +6", "AF2 counterexample C (REPRODUCED this run)"),
    ("D_66_E8_rel16", "66 E8 01 00 90 C3",
     "callw +0..+4; nop +4; ret +5", "AF2 counterexample D (REPRODUCED this run)"),
    ("E_positive_real_call", "B8 01 00 00 00 E8 05 00 00 00 C3",
     "mov eax,1 +0..+5; call 0xf +5..+10; ret +10", "AF2 counterexample E (positive control, REPRODUCED this run)"),
    # H1: the complete 16-bit addressing rm table (67 prefix) - REPRODUCED this run
    ("H1_MOD0_RM0", "67 8B 00", "mov eax,[bx+si] (3 B)", "H1 rm table: rm=0 mod=0"),
    ("H1_MOD0_RM1", "67 8B 01", "mov eax,[bx+di] (3 B)", "H1 rm table: rm=1 mod=0"),
    ("H1_MOD0_RM2", "67 8B 02", "mov eax,[bp+si] (3 B)", "H1 rm table: rm=2 mod=0"),
    ("H1_MOD0_RM3", "67 8B 03", "mov eax,[bp+di] (3 B)", "H1 rm table: rm=3 mod=0"),
    ("H1_MOD0_RM4", "67 8B 04", "mov eax,[si] (3 B)", "H1 rm table: rm=4 mod=0"),
    ("H1_MOD0_RM5", "67 8B 05", "mov eax,[di] (3 B)", "H1 rm table: rm=5 mod=0"),
    ("H1_MOD0_RM6", "67 8B 06 34 12", "mov eax,ds:0x1234 (5 B)", "H1 rm table: rm=6 mod=0 [disp16]"),
    ("H1_MOD0_RM7", "67 8B 07", "mov eax,[bx] (3 B)", "H1 rm table: rm=7 mod=0 [BX] - the H1 defect (C2 said [BP])"),
    ("H1_MOD1_RM0", "67 8B 40 05", "mov eax,[bx+si+0x5] (4 B)", "H1 rm table: rm=0 mod=1"),
    ("H1_MOD1_RM1", "67 8B 41 05", "mov eax,[bx+di+0x5] (4 B)", "H1 rm table: rm=1 mod=1"),
    ("H1_MOD1_RM2", "67 8B 42 05", "mov eax,[bp+si+0x5] (4 B)", "H1 rm table: rm=2 mod=1"),
    ("H1_MOD1_RM3", "67 8B 43 05", "mov eax,[bp+di+0x5] (4 B)", "H1 rm table: rm=3 mod=1"),
    ("H1_MOD1_RM4", "67 8B 44 05", "mov eax,[si+0x5] (4 B)", "H1 rm table: rm=4 mod=1"),
    ("H1_MOD1_RM5", "67 8B 45 05", "mov eax,[di+0x5] (4 B)", "H1 rm table: rm=5 mod=1"),
    ("H1_MOD1_RM6", "67 8B 46 05", "mov eax,[bp+0x5] (4 B)", "H1 rm table: rm=6 mod=1 [BP+disp]"),
    ("H1_MOD1_RM7", "67 8B 47 05", "mov eax,[bx+0x5] (4 B)", "H1 rm table: rm=7 mod=1 [BX+disp] - the H1 defect"),
    ("H1_MOD2_RM0", "67 8B 80 34 12", "mov eax,[bx+si+0x1234] (5 B)", "H1 rm table: rm=0 mod=2"),
    ("H1_MOD2_RM6", "67 8B 86 34 12", "mov eax,[bp+0x1234] (5 B)", "H1 rm table: rm=6 mod=2 [BP+disp16]"),
    ("H1_MOD2_RM7", "67 8B 87 34 12", "mov eax,[bx+0x1234] (5 B)", "H1 rm table: rm=7 mod=2 [BX+disp16] - the H1 defect"),
    # H2: grouped-opcode positive controls (carried)
    ("H2_BA_REG4_BT", "0F BA E0 05", "bt eax,0x5 (4 B)", "H2 positive: 0F BA /4 BT r,imm8"),
    ("H2_BA_REG5_BTS", "0F BA 6D 00 05", "bts [ebp+0x0],0x5 (5 B)", "H2 positive: 0F BA /5 BTS m,imm8 (memory form legal)"),
    ("H2_BA_REG4_MEM", "0F BA 25 78 56 34 12 05", "bt [0x12345678],0x5 (8 B)", "H2 positive: 0F BA /4 BT [disp32],imm8"),
    ("H2_71_REG2_PSRLW", "0F 71 D0 02", "psrlw mm0,0x2 (4 B)", "H2 positive: MMX 0F 71 /2"),
    ("H2_71_REG4_PSRAW", "0F 71 E2 02", "psraw mm2,0x2 (4 B)", "H2 positive: MMX 0F 71 /4"),
    ("H2_71_REG6_PSLLW", "0F 71 F0 02", "psllw mm0,0x2 (4 B)", "H2 positive: MMX 0F 71 /6"),
    ("H2_72_REG2_PSRLD", "0F 72 D0 02", "psrld mm0,0x2 (4 B)", "H2 positive: MMX 0F 72 /2"),
    ("H2_72_REG6_PSLLD", "0F 72 F0 02", "pslld mm0,0x2 (4 B)", "H2 positive: MMX 0F 72 /6"),
    ("H2_73_REG2_PSRLQ", "0F 73 D0 02", "psrlq mm0,0x2 (4 B)", "H2 positive: MMX 0F 73 /2"),
    ("H2_73_REG6_PSLLQ", "0F 73 F0 02", "psllq mm0,0x2 (4 B)", "H2 positive: MMX 0F 73 /6"),
    ("H2_66_71_REG2_PSRLW_XMM", "66 0F 71 D0 02", "psrlw xmm0,0x2 (5 B)", "H2 positive: SSE2 66 0F 71 /2"),
    ("H2_66_71_REG4_PSRAW_XMM", "66 0F 71 E2 02", "psraw xmm2,0x2 (5 B)", "H2 positive: SSE2 66 0F 71 /4"),
    ("H2_66_71_REG6_PSLLW_XMM", "66 0F 71 F0 02", "psllw xmm0,0x2 (5 B)", "H2 positive: SSE2 66 0F 71 /6"),
    ("H2_66_72_REG2_PSRLD_XMM", "66 0F 72 D0 02", "psrld xmm0,0x2 (5 B)", "H2 positive: SSE2 66 0F 72 /2"),
    ("H2_66_72_REG6_PSLLD_XMM", "66 0F 72 F0 02", "pslld xmm0,0x2 (5 B)", "H2 positive: SSE2 66 0F 72 /6"),
    ("H2_66_73_REG6_PSLLQ_XMM", "66 0F 73 F3 03", "psllq xmm3,0x3 (5 B)", "H2 positive: SSE2 66 0F 73 /6"),
    ("H2_66_73_REG3_PSRLDQ", "66 0F 73 DB 03", "psrldq xmm3,0x3 (5 B)",
     "H2 positive: SSE2 66 0F 73 /3 PSRLDQ (mod=3) - must NOT be misreported as reserved"),
    ("H2_66_73_REG7_PSLLDQ", "66 0F 73 FB 03", "pslldq xmm3,0x3 (5 B)",
     "H2 positive: SSE2 66 0F 73 /7 PSLLDQ (mod=3) - must NOT be misreported as reserved"),
    # H2: grouped-opcode negative controls (reserved/invalid -> oracle (bad))
    ("H2_BA_REG0_BAD", "0F BA C0 05", "(bad)", "H2 negative: 0F BA /0 reserved"),
    ("H2_BA_REG1_BAD", "0F BA C1 05", "(bad)", "H2 negative: 0F BA /1 reserved"),
    ("H2_BA_REG2_BAD", "0F BA C2 05", "(bad)", "H2 negative: 0F BA /2 reserved"),
    ("H2_BA_REG3_BAD", "0F BA C3 05", "(bad)", "H2 negative: 0F BA /3 reserved"),
    ("H2_71_REG1_BAD", "0F 71 C8 02", "(bad)", "H2 negative: 0F 71 /1 reserved"),
    ("H2_71_REG3_BAD", "0F 71 D8 02", "(bad)", "H2 negative: 0F 71 /3 reserved"),
    ("H2_71_REG5_BAD", "0F 71 E8 02", "(bad)", "H2 negative: 0F 71 /5 reserved"),
    ("H2_71_REG7_BAD", "0F 71 F8 02", "(bad)", "H2 negative: 0F 71 /7 reserved"),
    ("H2_73_REG3_NO66_BAD", "0F 73 D8 02", "(bad)", "H2 negative: 0F 73 /3 without 66 reserved (PSRLDQ requires 66)"),
    ("H2_73_REG7_NO66_BAD", "0F 73 F8 02", "(bad)", "H2 negative: 0F 73 /7 without 66 reserved (PSLLDQ requires 66)"),
    ("H2_66_71_REG1_BAD", "66 0F 71 C8 02", "(bad)", "H2 negative: 66 does not legalize 0F 71 /1"),
    ("H2_MMX_71_REG2_MEM", "0F 71 00 02", "(bad)", "H2 negative: MMX imm-shift memory form (mod!=3) invalid"),
    ("H2_MMX_72_REG2_MEM", "0F 72 00 02", "(bad)", "H2 negative: MMX imm-shift memory form (mod!=3) invalid"),
    ("H2_MMX_73_REG2_MEM", "0F 73 00 02", "(bad)", "H2 negative: MMX imm-shift memory form (mod!=3) invalid"),
    ("H2_66_71_REG2_MEM", "66 0F 71 00 02", "(bad)", "H2 negative: SSE2 imm-shift memory form (mod!=3) invalid"),
    ("H2_66_73_REG3_MEM_BAD_FIXED", "66 0F 73 5B 00 03", "(bad)", "H2 negative: 66 0F 73 /3 PSRLDQ memory form (mod!=3) invalid"),
    ("H2_66_73_REG7_MEM_BAD_FIXED", "66 0F 73 7B 00 03", "(bad)", "H2 negative: 66 0F 73 /7 PSLLDQ memory form (mod!=3) invalid"),
    ("H2_F3_71_BAD", "F3 0F 71 D0 02", "(bad)", "H2 negative: F3-prefixed imm-shift group - no legal form"),
    ("H2_F2_71_BAD", "F2 0F 71 D0 02", "(bad)", "H2 negative: F2-prefixed imm-shift group - no legal form"),
    # ---- D1 (THIS RUN): the 0F 73 /4 defect pair + the six contract legal
    # controls + the downstream falsifier stream. Expected verdicts locked
    # from the D1 contract + the ISA reference BEFORE the corrected decoder
    # is evaluated (Desktop post-audit
    # PE_935_F84_C2_C1_DESKTOP_POST_AUDIT_20261005 finding D1). ----
    ("D1_NEG_73_4_E0", "0F 73 E0 02", "(bad)",
     "D1 NEGATIVE: 0F 73 /4 mod=3 WITHOUT 66 is reserved (no PSRADQ exists; "
     "MMX 73 = /2,/6 only) - the THREE-P2 decoder ACCEPTED it (decoded "
     "length 4)"),
    ("D1_NEG_73_4_E0_66", "66 0F 73 E0 02", "data16 (bad)",
     "D1 NEGATIVE: 66 0F 73 /4 mod=3 WITH 66 is reserved (SSE2 73 forms are "
     "/2,/3,/6,/7 only) - the THREE-P2 SSE2 branch RETAINED /4 (decoded "
     "length 5)"),
    ("D1_POS_71_4_E0", "0F 71 E0 02", "psraw mm0,0x2 (4 B)",
     "D1 legal control: /4 STAYS legal for 0F 71 (mod=3)"),
    ("D1_POS_72_4_E0", "0F 72 E0 02", "psrad mm0,0x2 (4 B)",
     "D1 legal control: /4 STAYS legal for 0F 72 (mod=3)"),
    ("D1_POS_73_2_D0", "0F 73 D0 02", "psrlq mm0,0x2 (4 B)",
     "D1 legal control: 0F 73 /2 PSRLQ register form stays legal"),
    ("D1_POS_73_6_F0", "0F 73 F0 02", "psllq mm0,0x2 (4 B)",
     "D1 legal control: 0F 73 /6 PSLLQ register form stays legal"),
    ("D1_POS_66_73_3_D8", "66 0F 73 D8 02", "psrldq xmm0,0x2 (5 B)",
     "D1 legal control: 66 0F 73 /3 PSRLDQ mod=3 stays legal (NOT misreported as reserved)"),
    ("D1_POS_66_73_7_F8", "66 0F 73 F8 02", "pslldq xmm7,0x2 (5 B)",
     "D1 legal control: 66 0F 73 /7 PSLLDQ mod=3 stays legal (NOT misreported as reserved)"),
    ("D1_DOWNSTREAM_FALSIFIER", "0F 73 E0 02 E8 05 00 00 00 C3",
     "(bad) at +0; objdump recovery disassembly after (bad) is NOT treated "
     "as execution evidence",
     "D1 downstream falsifier stream: the invalid initial instruction must "
     "STOP justified sequential decoding (the production boundary outcome "
     "is measured separately in 01_RAW/D1_BOUNDARY_FALSIFIER.json)"),
]


def objdump_records():
    os.makedirs(TMP, exist_ok=True)
    version = subprocess.run(["wsl", "-e", "sh", "-c", "objdump --version"],
                             capture_output=True, text=True)
    records = {
        "run": "PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005",
        "oracle_tool": "GNU objdump (WSL, Debian)",
        "oracle_version_raw": version.stdout.strip().splitlines()[:2],
        "oracle_scope_note": ("INDEPENDENT oracle for SYNTHETIC FIXTURES ONLY; "
                              "the production decoder is never its own source "
                              "of truth; this run's D1 expected boundaries were "
                              "locked from the D1 contract + the ISA reference "
                              "BEFORE the corrected decoder's D1 behaviour was "
                              "evaluated; the real-EXE re-derivations of the "
                              "QC gates use the production decoder (the "
                              "established Q2/Q3 pattern, disclosed)"),
        "fixtures": [],
    }
    for name, hx, expected, role in FIXTURES:
        b = bytes.fromhex(hx.replace(" ", ""))
        path = os.path.join(TMP, name + ".bin")
        with open(path, "wb") as f:
            f.write(b)
        wpath = "/mnt/c" + path.replace("\\", "/")[2:]
        cmd = 'objdump -D -b binary -m i386 -M intel "%s"' % wpath
        out = subprocess.run(["wsl", "-e", "sh", "-c", cmd],
                             capture_output=True, text=True)
        records["fixtures"].append({
            "name": name, "bytes": hx, "role": role,
            "expected_boundaries": expected,
            "command_line": "wsl -e sh -c \"%s\"" % cmd,
            "raw_stdout": out.stdout,
            "raw_stderr": out.stderr, "returncode": out.returncode,
        })
    return records


def capture_commit_message():
    msg = subprocess.check_output(
        ["git", "-C", REPO, "log", "-1", "--format=%B", BASE_SHA],
        ).decode("utf-8", errors="replace")
    return msg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(RUN, "01_RAW", "D1_INDEPENDENT_ORACLE_RECORDS.json"))
    ap.add_argument("--out-cm", default=os.path.join(RUN, "01_RAW", "BASE_COMMIT_MESSAGE_VERBATIM.txt"))
    args = ap.parse_args()
    rec = objdump_records()
    with open(args.out, "w", newline="\n", encoding="utf-8") as f:
        json.dump(rec, f, indent=1)
    cm = capture_commit_message()
    with open(args.out_cm, "w", newline="\n", encoding="utf-8") as f:
        f.write(cm)
    print("oracle fixtures=%d base_commit_message_bytes=%d" % (len(rec["fixtures"]), len(cm)))


if __name__ == "__main__":
    main()
