# -*- coding: utf-8 -*-
"""
GENERATOR: 00_CONTROL/cleanup_verify_identities.py
RUN_ID: PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914
PURPOSE: G0/G10/G11 fail-closed identity verification at cleanup start.
  - Entropia.exe SHA256+SIZE pin assert (BEFORE any byte read beyond the hash itself)
  - Entropia PE optional-header byte dump (AUD-F4 evidence -> 01_RAW/ENTROPIA_PE_OPTIONAL_HEADER_DUMP.txt)
  - LINK30 historical artifacts byte-identity (BEFORE record -> 01_RAW/IDENTITY_VERIFICATION_AT_START.txt)
  - FIRSTCALL package 7-file hash census (read+hash ONLY, no modification)
  - GB112 oracle: NiMain.lib pin assert + Gb112_eval one-level census
MODE: STATIC-ONLY. The client binary is NEVER executed. Read-only file access.
EXECUTED AS:
  D:\\Eudoria_Reconstruction\\10_Scripts\\python_env\\python.exe -B cleanup_verify_identities.py
  (workdir 00_CONTROL/ of this package)
TOOLCHAIN PROVENANCE: interpreter + capstone measured dynamically (recorded in output).
OUTPUTS: 01_RAW/ENTROPIA_PE_OPTIONAL_HEADER_DUMP.txt, 01_RAW/IDENTITY_VERIFICATION_AT_START.txt
INPUT IDENTITIES: fail-closed pins loaded from 00_CONTROL/SOURCE_IDENTITIES.json (never hand-typed here).
"""
import hashlib
import json
import os
import struct
import sys
import datetime

PKG_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CTRL = os.path.join(PKG_ROOT, "00_CONTROL")
RAW = os.path.join(PKG_ROOT, "01_RAW")
REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"

SELF_PATH = os.path.abspath(__file__)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def self_sha256():
    return sha256_file(SELF_PATH)


def main():
    lines = []

    def rec(s=""):
        lines.append(s)
        print(s)

    # ---- toolchain provenance (dynamically measured) ----
    rec("=== TOOLCHAIN PROVENANCE (measured) ===")
    rec("interpreter: %s" % sys.executable)
    rec("python version: %s" % sys.version.split()[0])
    try:
        import capstone
        rec("capstone.__version__: %s" % capstone.__version__)
        rec("capstone.__file__: %s" % capstone.__file__)
    except Exception as e:  # pragma: no cover
        rec("capstone import FAILED: %r" % (e,))
    rec("generator: %s" % SELF_PATH)
    rec("generator SHA256: %s" % self_sha256())
    rec("executed as: python.exe -B cleanup_verify_identities.py (workdir 00_CONTROL/)")
    rec("timestamp: %s" % datetime.datetime.now().isoformat())

    with open(os.path.join(CTRL, "SOURCE_IDENTITIES.json"), "r", encoding="utf-8") as f:
        SID = json.load(f)

    failures = []

    def assert_pin(label, measured, expected):
        ok = measured == expected
        rec("%s: measured=%s expected=%s -> %s" % (label, measured, expected, "MATCH" if ok else "MISMATCH"))
        if not ok:
            failures.append(label)
        return ok

    # ---- 1. Entropia.exe fail-closed identity (BEFORE any other byte is read) ----
    rec("")
    rec("=== 1. Entropia.exe fail-closed identity ===")
    exe_path = SID["PRIMARY_BINARY"]["path"]
    exe_size = os.path.getsize(exe_path)
    exe_sha = sha256_file(exe_path)
    assert_pin("Entropia.exe SIZE", exe_size, SID["PRIMARY_BINARY"]["expected_size_bytes"])
    assert_pin("Entropia.exe SHA256", exe_sha, SID["PRIMARY_BINARY"]["expected_sha256"])
    if failures:
        rec("HARD_STOP: Entropia.exe identity mismatch — no further byte reads.")
        write_outputs(lines, pe_dump=None)
        sys.exit(2)

    # ---- 2. PE optional header byte dump (AUD-F4) ----
    rec("")
    rec("=== 2. Entropia.exe PE optional header (own byte read; AUD-F4) ===")
    pe = {}
    with open(exe_path, "rb") as f:
        hdr = f.read(0x400)
        pe["e_lfanew"] = struct.unpack_from("<I", hdr, 0x3C)[0]
        pe["pe_sig"] = hdr[pe["e_lfanew"]:pe["e_lfanew"] + 4]
        coff = pe["e_lfanew"] + 4
        machine, nsec = struct.unpack_from("<HH", hdr, coff)
        size_opt = struct.unpack_from("<H", hdr, coff + 16)[0]
        chars = struct.unpack_from("<H", hdr, coff + 18)[0]
        opt = coff + 20  # == e_lfanew + 0x18
        pe["opt_start"] = opt
        magic = struct.unpack_from("<H", hdr, opt)[0]
        image_base = struct.unpack_from("<I", hdr, opt + 0x1C)[0]
        sect_align = struct.unpack_from("<I", hdr, opt + 0x20)[0]
        dll_chars = struct.unpack_from("<H", hdr, opt + 0x46)[0]
        pe.update(machine=machine, nsections=nsec, size_opt=size_opt, coff_chars=chars,
                  magic=magic, image_base=image_base, section_alignment=sect_align,
                  dll_characteristics=dll_chars)
        # section table
        sect_table = opt + size_opt
        sections = []
        for i in range(nsec):
            off = sect_table + 40 * i
            name = hdr[off:off + 8].rstrip(b"\x00").decode("ascii", "replace")
            vsize, vaddr, rsize, rptr = struct.unpack_from("<IIII", hdr, off + 8)
            sections.append((name, vsize, vaddr, rsize, rptr))
    f4 = SID["AUDIT_F4_PE_HEADER_PINS"]
    assert_pin("e_lfanew (file offset 0x3C)", pe["e_lfanew"], int(f4["e_lfanew_at_file_offset_0x3C"], 16))
    assert_pin("PE signature", pe["pe_sig"].hex().upper(), "50450000")
    assert_pin("optional header start (e_lfanew+0x18)", pe["opt_start"], int(f4["optional_header_start"], 16))
    rec("optional header magic: measured=0x%04X expected=%s -> %s" % (
        pe["magic"], f4["optional_header_magic"], "MATCH" if pe["magic"] == 0x10B else "MISMATCH"))
    if pe["magic"] != 0x10B:
        failures.append("opt magic")
    assert_pin("ImageBase dword @opt+0x1C", pe["image_base"], int(f4["image_base_dword_at_opt_plus_0x1C"], 16))
    assert_pin("SectionAlignment dword @opt+0x20", pe["section_alignment"], int(f4["section_alignment_dword_at_opt_plus_0x20"], 16))
    assert_pin("DllCharacteristics word @opt+0x46", pe["dll_characteristics"], int(f4["dll_characteristics_word_at_opt_plus_0x46"], 16))

    pe_dump = []
    pe_dump.append("=== ENTROPIA.EXE PE OPTIONAL HEADER DUMP (raw byte evidence, AUD-F4) ===")
    pe_dump.append("RUN_ID: PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914")
    pe_dump.append("GENERATOR: 00_CONTROL/cleanup_verify_identities.py (SHA256 %s)" % self_sha256())
    pe_dump.append("COMMAND: D:\\Eudoria_Reconstruction\\10_Scripts\\python_env\\python.exe -B cleanup_verify_identities.py")
    pe_dump.append("INPUT: D:\\Eudoria_Reconstruction\\pcg_install\\Entropia.exe")
    pe_dump.append("  SIZE=%d SHA256=%s (fail-closed pin asserted BEFORE this dump)" % (exe_size, exe_sha))
    pe_dump.append("MODE: STATIC-ONLY (never executed); own byte read via struct, no third-party PE parser.")
    pe_dump.append("TIMESTAMP: %s" % datetime.datetime.now().isoformat())
    pe_dump.append("")
    pe_dump.append("e_lfanew (u32 @ file 0x3C)        = 0x%08X" % pe["e_lfanew"])
    pe_dump.append("PE signature @e_lfanew            = %s" % pe["pe_sig"].hex().upper())
    pe_dump.append("COFF Machine                     = 0x%04X (0x014C = i386)" % pe["machine"])
    pe_dump.append("COFF NumberOfSections            = %d" % pe["nsections"])
    pe_dump.append("COFF SizeOfOptionalHeader       = 0x%04X" % pe["size_opt"])
    pe_dump.append("optional header start            = e_lfanew+0x18 = 0x%08X" % pe["opt_start"])
    pe_dump.append("optional header Magic            = 0x%04X (0x10B = PE32)" % pe["magic"])
    pe_dump.append("dword @opt+0x1C (ImageBase)     = 0x%08X" % pe["image_base"])
    pe_dump.append("dword @opt+0x20 (SectionAlign)  = 0x%08X" % pe["section_alignment"])
    pe_dump.append("word  @opt+0x46 (DllCharacter)  = 0x%04X" % pe["dll_characteristics"])
    pe_dump.append("")
    pe_dump.append("SECTION TABLE (derived facts only; no payload bytes):")
    pe_dump.append("name       VirtualSize   VirtualAddr(RVA)   SizeOfRawData   PointerToRawData")
    for (name, vsize, vaddr, rsize, rptr) in sections:
        pe_dump.append("%-10s 0x%08X    0x%08X        0x%08X      0x%08X" % (name, vsize, vaddr, rsize, rptr))
    pe_dump.append("")
    pe_dump.append("AUD-F4 CONCLUSION (executor's own derivation): the standard IMAGE_OPTIONAL_HEADER32")
    pe_dump.append("layout holds: ImageBase is at OptionalHeader+0x1C and reads 0x00400000. The SLOT17")
    pe_dump.append("entropia_rtti_probe.py docstring claim of a '+4 shifted' ImageBase read is factually")
    pe_dump.append("wrong (REJECTED_WITH_EVIDENCE); erratum recorded in 02_ANALYSIS/SLOT17_ERRATA.md.")

    # ---- 3. LINK30 historical artifacts (BEFORE record) ----
    rec("")
    rec("=== 3. LINK30 historical artifacts byte-identity (BEFORE) ===")
    lk = SID["LINK30_HISTORICAL_ARTIFACTS"]
    csv_path = os.path.join(REPO, lk["census_csv"]["path_relative"].replace("/", os.sep))
    raw_path = os.path.join(REPO, lk["raw_txt"]["path_relative"].replace("/", os.sep))
    assert_pin("SF30_WRITER_CENSUS.csv SIZE", os.path.getsize(csv_path), lk["census_csv"]["measured_size_bytes"])
    assert_pin("SF30_WRITER_CENSUS.csv SHA256", sha256_file(csv_path), lk["census_csv"]["expected_sha256"])
    assert_pin("SF30_WRITER_RAW.txt SIZE", os.path.getsize(raw_path), lk["raw_txt"]["measured_size_bytes"])
    assert_pin("SF30_WRITER_RAW.txt SHA256", sha256_file(raw_path), lk["raw_txt"]["expected_sha256"])

    # ---- 4. FIRSTCALL package 7-file census (read + hash ONLY) ----
    rec("")
    rec("=== 4. FIRSTCALL package census (read+hash ONLY; NOT an evidence source) ===")
    fc = SID["FIRSTCALL_UNAUTHORIZED_PACKAGE"]
    fc_root = os.path.join(REPO, fc["path_relative"].replace("/", os.sep))
    measured_files = 0
    for entry in fc["files"]:
        p = os.path.join(fc_root, entry["relpath"].replace("/", os.sep))
        sz = os.path.getsize(p)
        sh = sha256_file(p)
        measured_files += 1
        assert_pin("FIRSTCALL %s SIZE" % entry["relpath"], sz, entry["size_bytes"])
        assert_pin("FIRSTCALL %s SHA256" % entry["relpath"], sh, entry["sha256"])
    rec("FIRSTCALL content+pyc file count measured: %d (pin: %d)" % (measured_files, fc["file_count_total_measured"]))
    if measured_files != fc["file_count_total_measured"]:
        failures.append("FIRSTCALL count")
    for d in fc["empty_directories"]:
        dp = os.path.join(fc_root, d)
        entries = os.listdir(dp) if os.path.isdir(dp) else None
        rec("FIRSTCALL dir %s: exists=%s entries=%s (pin: EMPTY)" % (d, os.path.isdir(dp), entries))
        if entries != []:
            failures.append("FIRSTCALL dir %s not empty" % d)
    all_on_disk = []
    for root, dirs, files in os.walk(fc_root):
        for fn in files:
            all_on_disk.append(os.path.relpath(os.path.join(root, fn), fc_root))
    rec("FIRSTCALL disk walk total files: %d" % len(all_on_disk))
    if len(all_on_disk) != 7:
        failures.append("FIRSTCALL walk count %d != 7" % len(all_on_disk))

    # ---- 5. GB112 oracle ----
    rec("")
    rec("=== 5. GB112 oracle identity ===")
    nl = SID["GB112_ORACLE"]["nimain_lib"]
    assert_pin("NiMain.lib SIZE", os.path.getsize(nl["path"]), nl["expected_size_bytes"])
    assert_pin("NiMain.lib SHA256", sha256_file(nl["path"]), nl["expected_sha256"])
    gb = SID["GB112_ORACLE"]["gb112_eval_dir"]["path"]
    one = sorted(os.listdir(gb))
    rec("Gb112_eval one-level census: %s (pin: ['Documentation'])" % one)
    if one != ["Documentation"]:
        failures.append("Gb112_eval census")
    doc = sorted(os.listdir(os.path.join(gb, "Documentation")))
    rec("Gb112_eval/Documentation entries: %s" % doc)
    rec("Gb112_eval/Documentation census match: %s" % (doc == sorted(
        [e["name"] for e in SID["GB112_ORACLE"]["gb112_eval_dir"]["documentation_dir_entries_measured"]])))

    # ---- verdict ----
    rec("")
    rec("=== VERDICT ===")
    if failures:
        rec("PIN MISMATCHES (%d): %s" % (len(failures), failures))
        rec("RUN_STATUS: HARD_STOP required on mismatches of Entropia identity; other mismatches = findings.")
    else:
        rec("ALL PIN CHECKS MATCH. G0 identity components verified at cleanup start.")
    write_outputs(lines, pe_dump)
    return 1 if failures else 0


def write_outputs(lines, pe_dump):
    ts = datetime.datetime.now().isoformat()
    label = "END" if (len(sys.argv) > 1 and sys.argv[1].upper() == "END") else "START"
    head = [
        "=== IDENTITY VERIFICATION AT CLEANUP %s (raw record) ===" % label,
        "RUN_ID: PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914",
        "GENERATOR: 00_CONTROL/cleanup_verify_identities.py (SHA256 %s)" % self_sha256(),
        "COMMAND: D:\\Eudoria_Reconstruction\\10_Scripts\\python_env\\python.exe -B cleanup_verify_identities.py%s"
        % ("" if label == "START" else " END"),
        "TIMESTAMP: %s" % ts,
        "POLICY: pins loaded from 00_CONTROL/SOURCE_IDENTITIES.json; measurements from disk.",
        "POLICY: FIRSTCALL/LINK30/SLOT17 inputs are READ-ONLY (read+hash only, never modified).",
        "POLICY (END record): byte-identity before == after for LINK30 CSV/RAW and FIRSTCALL",
        "  is the G9/G11 invariant; this record re-measures AFTER the executor's work.",
        "",
    ]
    with open(os.path.join(RAW, "IDENTITY_VERIFICATION_AT_%s.txt" % label), "w", encoding="utf-8") as f:
        f.write("\n".join(head + lines) + "\n")
    if pe_dump is not None:
        with open(os.path.join(RAW, "ENTROPIA_PE_OPTIONAL_HEADER_DUMP.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(pe_dump) + "\n")


if __name__ == "__main__":
    sys.exit(main())
