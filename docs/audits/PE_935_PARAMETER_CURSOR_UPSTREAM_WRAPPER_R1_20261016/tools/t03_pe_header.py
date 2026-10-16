# t03_pe_header.py — the single permitted PE32 header read (<=4096 B) and MECHANICAL
# window-to-file-offset mapping. The offset is derived from the parsed section table,
# never copied from any expected value. Checks: MZ/PE magic, machine, ImageBase,
# unique RAW-backed coverage of the whole 82-B window, file bounds, no overlap with
# any other section's raw range, no BSS, no wraparound. Writes
# buffers/pe_header_first4096.bin and records/pe32_mapping.json. Critical mismatch
# halts science (exit 2).
import sys, os, struct, traceback
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_common as rc

TOOL_REL = "tools/t03_pe_header.py"

def main():
    argv = list(sys.argv)
    t_start = rc.utcnow_iso()
    a = rc.parse_simple_args(argv, ["--config", "--attempt"])
    cfg = rc.load_config(a["--config"])
    root = cfg["_output_root_abs"]
    attempt_id = a["--attempt"]
    tool_abs = os.path.abspath(__file__)
    exe_path = cfg["original_exe"]["path"]
    win_start = int(cfg["window"]["start_va"], 16)
    win_end_ex = int(cfg["window"]["end_exclusive_va"], 16)
    win_size = cfg["window"]["size_bytes"]
    status = "OK"
    exit_code = 0
    err = ""
    result = {}
    inputs_meta = []
    outputs_meta = []
    try:
        rc.new_attempt_dir(root, attempt_id)
        HEADER_BYTES = cfg["budgets"]["MAX_HEADER_BYTES"]
        with open(exe_path, "rb") as f:
            header = f.read(HEADER_BYTES)
        header_read = len(header)
        if header_read != HEADER_BYTES:
            raise rc.CriticalMismatch("header read short: %d" % header_read)
        inputs_meta.append({"path": exe_path, "size_bytes": header_read,
                            "sha256": rc.sha256_bytes(header),
                            "note": "first %d bytes (the one permitted header read)" % HEADER_BYTES})
        checks = {}
        if header[0:2] != b"MZ":
            raise rc.CriticalMismatch("DOS magic MZ absent")
        checks["dos_magic_mz"] = True
        e_lfanew = struct.unpack_from("<I", header, 0x3C)[0]
        if e_lfanew + 24 > header_read:
            raise rc.CriticalMismatch("e_lfanew out of header buffer")
        if header[e_lfanew:e_lfanew + 4] != b"PE\x00\x00":
            raise rc.CriticalMismatch("PE magic absent")
        checks["pe_magic"] = True
        machine = struct.unpack_from("<H", header, e_lfanew + 4)[0]
        nsec = struct.unpack_from("<H", header, e_lfanew + 6)[0]
        size_opt = struct.unpack_from("<H", header, e_lfanew + 20)[0]
        opt_magic = struct.unpack_from("<H", header, e_lfanew + 24)[0]
        image_base = struct.unpack_from("<I", header, e_lfanew + 52)[0]
        checks["machine_is_i386_0x14c"] = (machine == 0x14C)
        checks["optional_magic_pe32_0x10b"] = (opt_magic == 0x10B)
        if machine != 0x14C:
            raise rc.CriticalMismatch("machine is not i386: 0x%04X" % machine)
        if opt_magic != 0x10B:
            raise rc.CriticalMismatch("optional header magic is not PE32: 0x%04X" % opt_magic)
        sec_table_off = e_lfanew + 24 + size_opt
        if sec_table_off + 40 * nsec > header_read:
            raise rc.CriticalMismatch("section table extends beyond header buffer")
        sections = []
        for i in range(nsec):
            off = sec_table_off + 40 * i
            name = header[off:off + 8].rstrip(b"\x00").decode("ascii", "replace")
            vsize = struct.unpack_from("<I", header, off + 8)[0]
            vaddr = struct.unpack_from("<I", header, off + 12)[0]
            rsize = struct.unpack_from("<I", header, off + 16)[0]
            rptr = struct.unpack_from("<I", header, off + 20)[0]
            sections.append({"name": name, "virtual_size": vsize, "virtual_address": vaddr,
                             "size_of_raw_data": rsize, "pointer_to_raw_data": rptr})
        window_rva = win_start - image_base
        checks["window_rva_positive_no_wraparound"] = (0 < window_rva < 0xFFFFFFFF and
                                                       window_rva + win_size > window_rva)
        if not checks["window_rva_positive_no_wraparound"]:
            raise rc.CriticalMismatch("window RVA arithmetic invalid")
        candidates = []
        for s in sections:
            raw_lo = s["pointer_to_raw_data"]
            raw_hi = raw_lo + s["size_of_raw_data"]
            va_lo = s["virtual_address"]
            va_hi = va_lo + s["size_of_raw_data"]
            if s["size_of_raw_data"] > 0 and s["pointer_to_raw_data"] != 0 and \
               va_lo <= window_rva and (window_rva + win_size) <= va_hi:
                candidates.append(s)
        checks["unique_raw_backed_covering_section"] = (len(candidates) == 1)
        if len(candidates) != 1:
            raise rc.CriticalMismatch("raw-backed covering sections: %d (need exactly 1)" % len(candidates))
        sec = candidates[0]
        file_offset = window_rva - sec["virtual_address"] + sec["pointer_to_raw_data"]
        file_size = os.path.getsize(exe_path)
        checks["within_file_bounds"] = (file_offset + win_size <= file_size and file_offset >= 0)
        if not checks["within_file_bounds"]:
            raise rc.CriticalMismatch("window raw range beyond file bounds")
        # overlap check: no OTHER section raw range may intersect [file_offset, file_offset+win_size)
        overlaps = []
        for s in sections:
            if s is sec or s["size_of_raw_data"] == 0:
                continue
            lo = s["pointer_to_raw_data"]
            hi = lo + s["size_of_raw_data"]
            if lo < file_offset + win_size and hi > file_offset:
                overlaps.append(s["name"])
        checks["no_other_section_raw_overlap"] = (len(overlaps) == 0)
        if overlaps:
            raise rc.CriticalMismatch("raw overlap with sections: %s" % overlaps)
        checks["not_bss"] = (sec["pointer_to_raw_data"] != 0 and sec["size_of_raw_data"] >= win_size)
        hb = rc.atomic_write_bytes(root, "buffers/pe_header_first4096.bin", header)
        outputs_meta.append(hb)
        mapping = {
            "generated_by_tool": "t03_pe_header.py",
            "pass": "header_read_1_of_1",
            "header_read_bytes": header_read,
            "header_buffer_sha256": hb["sha256"],
            "e_lfanew": e_lfanew,
            "machine": "0x%04X" % machine,
            "number_of_sections": nsec,
            "optional_header_magic": "0x%04X" % opt_magic,
            "image_base": "0x%08X" % image_base,
            "sections": sections,
            "window": {"start_va": cfg["window"]["start_va"],
                       "end_exclusive_va": cfg["window"]["end_exclusive_va"],
                       "size_bytes": win_size},
            "window_rva": "0x%08X" % window_rva,
            "covering_section": sec,
            "derived_file_offset_hex": "0x%08X" % file_offset,
            "derived_file_offset_decimal": file_offset,
            "derivation": "file_offset = window_rva - covering_section.virtual_address + covering_section.pointer_to_raw_data (parsed from the PE32 section table in the saved header buffer; mechanically derived, not copied)",
            "checks": checks,
            "file_size_bytes": file_size,
            "status": "OK"
        }
        mapping["generated_utc"] = rc.utcnow_iso()
        mj = rc.atomic_write_bytes(root, "records/pe32_mapping.json", rc.strict_dumps(mapping).encode("utf-8"))
        outputs_meta.append(mj)
        result = {"header_read_bytes": header_read, "machine": "0x%04X" % machine,
                  "image_base": "0x%08X" % image_base, "sections": nsec,
                  "covering_section": sec["name"],
                  "derived_file_offset": "0x%08X" % file_offset,
                  "checks": checks, "status": "OK",
                  "outputs": [hb["path"], mj["path"]]}
        status = "OK"
        exit_code = 0
        t_end = rc.utcnow_iso()
    except SystemExit as e:
        raise e
    except rc.CriticalMismatch as e:
        status = "CRITICAL_MISMATCH"
        exit_code = 2
        err = "CriticalMismatch: %s" % e
        result = {"error": err, "status": status}
        t_end = rc.utcnow_iso()
    except BaseException as e:
        status = "FAILED"
        exit_code = 1
        err = "%s: %s" % (type(e).__name__, e)
        result = {"error": err, "traceback": traceback.format_exc()}
        t_end = rc.utcnow_iso()
    stdout_text = rc.compact_dumps({"tool": TOOL_REL, "attempt": attempt_id, "status": status,
                                   "exit": exit_code, "result": result})
    entry = {"attempt_id": attempt_id, "tool": TOOL_REL,
             "tool_sha256": rc.sha256_file(tool_abs),
             "config": rc.file_identity(cfg["_config_abs"], "RUN_CONFIG.json"),
             "argv": argv, "kind": "PE32_HEADER_READ_AND_MAPPING",
             "t_start_utc": t_start, "t_end_utc": t_end,
             "status": status, "exit_code": exit_code,
             "inputs": inputs_meta, "outputs": outputs_meta, "result": result}
    if err:
        entry["error"] = err
    outs, prefix = rc.finalize(root, attempt_id, entry, stdout_text, "" if status == "OK" else err)
    print(stdout_text)
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
