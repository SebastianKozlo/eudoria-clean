# t07_roster.py — PATH_A/PATH_B comparison and merged INSTRUCTION_ROSTER build.
# Parses the saved PATH_A objdump text (continuation lines merged as bytes of the
# previous instruction, never new heads), loads the saved PATH_B sweep, compares
# heads/lengths/raw byte-by-byte, recomputes every branch/call target from the
# RECORDED raw bytes (TARGET_SOURCE=ARITHMETIC_FROM_RECORDED_RAW; the pinned library
# records no imm for unprefixed E8/E9 and for Jcc/JMP), compares against the PATH_A
# printed operand, derives bounded encoding facts (push/mov reg-reg/ret cleanup/
# indirect call form), emits decode/ab_comparison.json + decode/INSTRUCTION_ROSTER.json.
import sys, os, re, json, traceback
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_common as rc

TOOL_REL = "tools/t07_roster.py"

REGS32 = ["EAX", "ECX", "EDX", "EBX", "ESP", "EBP", "ESI", "EDI"]
REGS8 = ["AL", "CL", "DL", "BL", "AH", "CH", "DH", "BH"]
JCC = {0x70: "JO", 0x71: "JNO", 0x72: "JB", 0x73: "JAE", 0x74: "JE", 0x75: "JNE",
       0x76: "JBE", 0x77: "JA", 0x78: "JS", 0x79: "JNS", 0x7A: "JP", 0x7B: "JNP",
       0x7C: "JL", 0x7D: "JGE", 0x7E: "JLE", 0x7F: "JG"}
REG_TOKENS = set(REGS32) | set(REGS8) | set(["EIP"])

head_re = re.compile(r"^\s*([0-9a-fA-F]+):\s+((?:[0-9a-fA-F]{2}[ \t]+)*[0-9a-fA-F]{2})(?:\s+(\S.*))?$")
cont_re = re.compile(r"^\s+((?:[0-9a-fA-F]{2}[ \t]+)*[0-9a-fA-F]{2})(?:\s+(\S.*))?$")

def parse_path_a(text, win_start):
    rows = []
    skipped = []
    cont_lines = 0
    for raw_line in text.splitlines():
        line = raw_line.rstrip("\r")
        mh = head_re.match(line)
        if mh:
            va = int(mh.group(1), 16)
            bytestr = mh.group(2)
            txt = mh.group(3) or ""
            # label lines like "852a30 <.data>:" do not match (bytes group fails).
            if rows and va == rows[-1]["va_int"] and not rows[-1]["text"]:
                # wrapped continuation carrying the same address: merge, not a new head
                rows[-1]["bytes"].extend(int(b, 16) for b in bytestr.split())
                rows[-1]["text"] = (rows[-1]["text"] + " " + txt).strip()
                cont_lines += 1
                continue
            rows.append({"va_int": va, "bytes": [int(b, 16) for b in bytestr.split()],
                         "text": txt.strip()})
            continue
        mc = cont_re.match(line)
        if mc and rows:
            rows[-1]["bytes"].extend(int(b, 16) for b in mc.group(1).split())
            if mc.group(2):
                rows[-1]["text"] = (rows[-1]["text"] + " " + mc.group(2).strip()).strip()
            cont_lines += 1
            continue
        if line.strip():
            skipped.append(line.strip())
    for r in rows:
        r["offset_in_window"] = r["va_int"] - win_start
        r["length"] = len(r["bytes"])
        r["raw_hex"] = " ".join("%02x" % b for b in r["bytes"])
    return rows, skipped, cont_lines

def s8(b):
    return b - 256 if (b & 0x80) else b

def s32(v):
    return v - (1 << 32) if (v & 0x80000000) else v

def classify_and_target(va_int, brow, raw):
    op = brow["opcode_hex"]
    op2 = brow["opcode2_hex"]
    opv = int(op, 16) if op else None
    op2v = int(op2, 16) if op2 else None
    L = brow["length"]
    rel16 = brow["rel16"]
    def rel_target(rel, base):
        return ("0x%08X" % ((va_int + base + rel) & 0xFFFFFFFF))
    if rel16:
        # 66-prefixed near branch: imm recorded by the library (imm_width=2)
        rel = brow["imm_signed"]
        base = L
        kind = "CALL_REL16" if opv in (0xE8,) else ("JMP_REL16" if opv in (0xE9,) else "JCC_REL16")
        return kind, rel_target(rel, base), "LIBRARY_RECORDED_IMM16"
    if opv == 0xE8:
        rel = s32(int.from_bytes(bytes(raw[1:5]), "little"))
        return "CALL_REL32", rel_target(rel, L), "ARITHMETIC_FROM_RECORDED_RAW"
    if opv == 0xE9:
        rel = s32(int.from_bytes(bytes(raw[1:5]), "little"))
        return "JMP_REL32", rel_target(rel, L), "ARITHMETIC_FROM_RECORDED_RAW"
    if opv == 0xEB:
        rel = s8(raw[1])
        return "JMP_REL8", rel_target(rel, L), "ARITHMETIC_FROM_RECORDED_RAW"
    if opv is not None and 0x70 <= opv <= 0x7F:
        rel = s8(raw[1])
        return "JCC_REL8_%s" % JCC[opv], rel_target(rel, L), "ARITHMETIC_FROM_RECORDED_RAW"
    if opv == 0x0F and op2v is not None and 0x80 <= op2v <= 0x8F:
        rel = s32(int.from_bytes(bytes(raw[2:6]), "little"))
        return "JCC_REL32_%s" % JCC[0x70 + (op2v - 0x80)], rel_target(rel, L), "ARITHMETIC_FROM_RECORDED_RAW"
    if opv == 0xFF and brow["reg"] == 2 and brow["mod"] == 3:
        return "CALL_INDIRECT_REGISTER", None, "INDIRECT_FORM_NO_DIRECT_TARGET"
    if opv == 0xFF and brow["reg"] == 4 and brow["mod"] == 3:
        return "JMP_INDIRECT_REGISTER", None, "INDIRECT_FORM_NO_DIRECT_TARGET"
    return "OTHER", None, None

def encoding_facts(brow, raw):
    op = brow["opcode_hex"]
    opv = int(op, 16) if op else None
    mod, reg, rm = brow["mod"], brow["reg"], brow["rm"]
    f = {}
    if opv is None:
        return f
    if 0x50 <= opv <= 0x57:
        f["push_register"] = REGS32[opv - 0x50]
        f["fact_source"] = "DERIVED_FROM_OPCODE_50_PLUS_R"
    if 0x58 <= opv <= 0x5F:
        f["pop_register"] = REGS32[opv - 0x58]
        f["fact_source"] = "DERIVED_FROM_OPCODE_58_PLUS_R"
    if mod == 3:
        if opv == 0x8B:
            f["mov_dst"] = REGS32[reg]; f["mov_src"] = REGS32[rm]
            f["fact_source"] = "DERIVED_FROM_MODRM_REG_RM_MOD3"
        elif opv == 0x89:
            f["mov_src"] = REGS32[reg]; f["mov_dst"] = REGS32[rm]
            f["fact_source"] = "DERIVED_FROM_MODRM_REG_RM_MOD3"
        elif opv == 0x8A:
            f["mov_dst8"] = REGS8[reg]; f["mov_src8"] = REGS8[rm]
            f["fact_source"] = "DERIVED_FROM_MODRM_REG_RM_MOD3"
        elif opv == 0x88:
            f["mov_src8"] = REGS8[reg]; f["mov_dst8"] = REGS8[rm]
            f["fact_source"] = "DERIVED_FROM_MODRM_REG_RM_MOD3"
        elif opv in (0x01, 0x03, 0x08, 0x0A, 0x29, 0x2B, 0x31, 0x33, 0x39, 0x3B, 0x85):
            f["reg_field_register"] = REGS32[reg]
            f["rm_field_register"] = REGS32[rm]
            f["modrm_reg_reg_form"] = True
            f["fact_source"] = "DERIVED_FROM_MODRM_REG_RM_MOD3"
    if opv == 0xC2:
        v = int.from_bytes(bytes(raw[1:3]), "little")
        f["ret_imm16_raw"] = v
        f["ret_cleanup_bytes"] = v
        f["ret_cleanup_source"] = "DERIVED_FROM_RECORDED_RAW"
    if opv == 0xFF and reg == 2 and mod == 3:
        f["call_indirect_register"] = REGS32[rm]
        f["fact_source"] = "DERIVED_FROM_MODRM_FF_2_MOD3"
    if opv == 0x68:
        f["push_imm32_raw"] = int.from_bytes(bytes(raw[1:5]), "little")
        f["fact_source"] = "DERIVED_FROM_RECORDED_RAW"
    if opv == 0x6A:
        f["push_imm8_signed"] = s8(raw[1])
        f["fact_source"] = "DERIVED_FROM_RECORDED_RAW"
    return f

def a_operand_target(text):
    toks = text.replace(",", " ").split()
    if len(toks) >= 2:
        mn, tok = toks[0], toks[-1]
        if tok.upper() in REG_TOKENS:
            return ("INDIRECT_REGISTER", tok.upper())
        t = tok.lower()
        if t.startswith("0x"):
            t = t[2:]
        if re.fullmatch(r"[0-9a-f]+", t):
            return ("DIRECT", "0x%08X" % int(t, 16))
    return (None, None)

def main():
    argv = list(sys.argv)
    t_start = rc.utcnow_iso()
    a = rc.parse_simple_args(argv, ["--config", "--attempt"])
    cfg = rc.load_config(a["--config"])
    root = cfg["_output_root_abs"]
    attempt_id = a["--attempt"]
    tool_abs = os.path.abspath(__file__)
    win_start = int(cfg["window"]["start_va"], 16)
    win_size = cfg["window"]["size_bytes"]
    expected_parser = int(cfg["window"]["downstream_expected_target_va"], 16)
    helper_hint = int(cfg["window"]["opaque_helper_hint_va"], 16)
    status = "OK"
    exit_code = 0
    err = ""
    result = {}
    inputs_meta = []
    outputs_meta = []
    try:
        rc.new_attempt_dir(root, attempt_id)
        pa_abs = rc.resolve_in_root(root, "decode/PATH_A_SWEEP.txt")
        pb_abs = rc.resolve_in_root(root, "decode/PATH_B_SWEEP.json")
        with open(pa_abs, "r", encoding="utf-8") as f:
            pa_text = f.read()
        with open(pb_abs, "r", encoding="utf-8") as f:
            pb = rc.strict_loads(f.read())
        inputs_meta.append(rc.file_identity(pa_abs, "decode/PATH_A_SWEEP.txt"))
        inputs_meta.append(rc.file_identity(pb_abs, "decode/PATH_B_SWEEP.json"))
        a_rows, skipped, cont_lines = parse_path_a(pa_text, win_start)
        b_rows = pb["instructions"]
        # duplicate VA check before mapping (both sides)
        a_vas = [r["va_int"] for r in a_rows]
        b_vas = [int(r["va"], 16) for r in b_rows]
        dup_a = len(a_vas) != len(set(a_vas))
        dup_b = len(b_vas) != len(set(b_vas))
        comparisons = []
        disagreements = []
        n = min(len(a_rows), len(b_rows))
        for i in range(n):
            ar = a_rows[i]
            br = b_rows[i]
            same_va = (ar["va_int"] == int(br["va"], 16))
            same_len = (ar["length"] == br["length"])
            same_raw = (ar["raw_hex"] == br["raw_hex"])
            ok = same_va and same_len and same_raw
            if not ok:
                disagreements.append({"index": i, "a": {"va": "0x%08X" % ar["va_int"], "length": ar["length"], "raw_hex": ar["raw_hex"]},
                                      "b": {"va": br["va"], "length": br["length"], "raw_hex": br["raw_hex"]},
                                      "same_va": same_va, "same_length": same_len, "same_raw": same_raw})
            comparisons.append(ok)
        count_mismatch = (len(a_rows) != len(b_rows))
        roster_rows = []
        target_agreements = []
        for i in range(n):
            ar = a_rows[i]
            br = b_rows[i]
            va_int = ar["va_int"]
            raw = ar["bytes"]
            kind, target, tsrc = classify_and_target(va_int, br, raw)
            a_kind_tok, a_tok = a_operand_target(ar["text"])
            tgt = None
            if kind.endswith("REL32") or kind.endswith("REL8") or kind.endswith("REL16") or kind.startswith("JCC") or kind.startswith("CALL_REL") or kind.startswith("JMP_REL"):
                tgt = {"value": target, "source": tsrc,
                       "path_a_operand_kind": a_kind_tok, "path_a_operand": a_tok,
                       "agreement": (a_kind_tok == "DIRECT" and a_tok is not None and target is not None and int(a_tok, 16) == int(target, 16))}
                target_agreements.append(tgt["agreement"])
            elif kind in ("CALL_INDIRECT_REGISTER", "JMP_INDIRECT_REGISTER"):
                tgt = {"value": None, "source": "INDIRECT_FORM_NO_DIRECT_TARGET",
                       "path_a_operand_kind": a_kind_tok, "path_a_operand": a_tok,
                       "agreement": (a_kind_tok == "INDIRECT_REGISTER"),
                       "form_register": br.get("ea_text") if br.get("memop") else (REGS32[br["rm"]] if br.get("rm") is not None and br.get("mod") == 3 else None)}
                target_agreements.append(tgt["agreement"])
            else:
                tgt = None
            hints = {}
            if target is not None:
                tv = int(target, 16)
                hints["is_call_to_expected_parser_0x00852750"] = (tv == expected_parser and kind.startswith("CALL"))
                hints["is_call_to_helper_0x0040DE60"] = (tv == helper_hint and kind.startswith("CALL"))
            roster_rows.append({
                "index": i, "va": "0x%08X" % va_int,
                "offset_in_window": ar["offset_in_window"],
                "length": ar["length"], "raw_hex": ar["raw_hex"],
                "path_a_text": ar["text"], "path_b_fields": br,
                "kind": kind, "target": tgt,
                "encoding_facts": encoding_facts(br, raw),
                "hint_flags": hints})
        full_agree = (not disagreements and not count_mismatch and not dup_a and not dup_b
                      and all(comparisons) and all(target_agreements)
                      and len(target_agreements) == sum(1 for r in roster_rows if r["target"] is not None))
        coverage = {"a_rows": len(a_rows), "b_rows": len(b_rows),
                    "a_last_end_offset": (a_rows[-1]["offset_in_window"] + a_rows[-1]["length"]) if a_rows else None,
                    "b_barrier": pb["barrier"], "b_reached_window_end_exactly": pb["reached_window_end_exactly"],
                    "window_size_bytes": win_size}
        comp = {"heads_compared": n,
                "start_length_raw_agreement": "%d/%d" % (sum(1 for c in comparisons if c), n),
                "targets_compared": len(target_agreements),
                "target_agreement": "%d/%d" % (sum(1 for t in target_agreements if t), len(target_agreements)),
                "disagreements": disagreements,
                "count_mismatch": count_mismatch,
                "duplicate_va_a": dup_a, "duplicate_va_b": dup_b,
                "continuation_lines_merged": cont_lines,
                "skipped_non_instruction_lines": skipped,
                "coverage": coverage,
                "target_source_note": "every branch/call target recomputed as (VA+length+signed_rel) mod 2^32 from the recorded raw bytes (TARGET_SOURCE=ARITHMETIC_FROM_RECORDED_RAW for unprefixed E8/E9/Jcc/JMP; LIBRARY_RECORDED_IMM16 for 66-prefixed rel16) and compared against the PATH_A printed operand; this is NOT two independent full operand-semantics verifications",
                "full_agreement": full_agree}
        comp["generated_utc"] = rc.utcnow_iso()
        o1 = rc.atomic_write_bytes(root, "decode/ab_comparison.json", rc.strict_dumps(comp).encode("utf-8"))
        roster = {"run_id": cfg["run_id"], "window": "[0x%08X,0x%08X)" % (win_start, win_start + win_size),
                  "rows": len(roster_rows), "unique_instruction_starts": len(roster_rows),
                  "provenance": "PATH_A (objdump 2.44, sweep 1) and PATH_B (pinned x86dec, sequential from offset 0) independently; merged one row per VA by t07; targets recomputed from recorded raw bytes",
                  "instructions": roster_rows}
        roster["generated_utc"] = rc.utcnow_iso()
        o2 = rc.atomic_write_bytes(root, "decode/INSTRUCTION_ROSTER.json", rc.strict_dumps(roster).encode("utf-8"))
        outputs_meta.extend([o1, o2])
        status = "FULL_AGREEMENT" if full_agree else "DISAGREEMENT"
        exit_code = 0 if full_agree else 1
        result = {"a_rows": len(a_rows), "b_rows": len(b_rows), "heads_compared": n,
                  "target_agreement": comp["target_agreement"],
                  "start_length_raw_agreement": comp["start_length_raw_agreement"],
                  "continuation_lines_merged": cont_lines,
                  "full_agreement": full_agree, "status": status,
                  "outputs": [o1["path"], o2["path"]],
                  "unique_instruction_starts_vs_limit": "%d/%d" % (len(roster_rows), cfg["budgets"]["MAX_UNIQUE_INSTRUCTION_STARTS"])}
        t_end = rc.utcnow_iso()
    except SystemExit as e:
        raise e
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
             "argv": argv, "kind": "AB_COMPARISON_AND_ROSTER",
             "t_start_utc": t_start, "t_end_utc": t_end,
             "status": status, "exit_code": exit_code,
             "inputs": inputs_meta, "outputs": outputs_meta, "result": result}
    if err:
        entry["error"] = err
    outs, prefix = rc.finalize(root, attempt_id, entry, stdout_text, "" if status != "FAILED" else err)
    print(stdout_text)
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
