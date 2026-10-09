#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""qc_stack_replay.py — PE_935_CMO_ARG1_SINGLE_CALLSITE_PROVENANCE_R1_20261009

The fresh-context pe-master-auditor QC worker's OWN independent symbolic
replay + control re-run for the bounded arg1-provenance micro-run.

INDEPENDENCE STATEMENT (honest):
  * This script does NOT import, copy or invoke the executor's
    03_SCRIPTS/run_stack_controls.py. It shares NO code with it.
  * It does NOT take the executor's ledger, measured facts or verdicts as
    its source of truth. Its ONLY expectation source is the frozen
    human-authorized contract (sections 4/5/6), independently translated
    into the checks below.
  * SAME disassembler as the executor (GNU objdump 2.44 via WSL): sharing a
    mature disassembler is NOT cross-implementation disassembler QC. The
    independent dimensions are: own byte read of the authorized window from
    the physical EXE; own PE header parse and VA->offset mapping; own
    objdump invocations and raw capture; own parser — which additionally
    cross-validates every decoded instruction's byte column against the
    physical fixture bytes (a byte-level check the executor's parser does
    not perform); own symbolic replay implementation; own synthetic mutant
    fixtures built from the QC's own window read; own negative controls.
  * The contract's six cases do not exercise the fail-closed path
    (executor's own F6 note: "fail-closed path unexercised by design").
    The QC therefore adds two NEGATIVE CONTROLS of its own (not part of the
    12 contract analysis outcomes):
      NC1_FAILCLOSED — an unsupported instruction (cmpxchg) inside the
        window MUST trigger a controlled FAIL_CLOSED, never a fabricated
        source;
      NC2_TARGET_MISMATCH — one rel32 byte mutated so the recomputed call
        target becomes 0x0085B1C0: the QC's baseline call-target
        expectation MUST FAIL on it (liveness/falsifiability of the QC's own
        predicate), while the recompute-vs-objdump internal consistency
        check still passes.

BOUNDS: reads from the EXE only (a) PE headers/section metadata for the
mapping, (b) the authorized 28-byte window at file offset 1216118, (c) full
identity hashes. No other EXE bytes. The client never runs (STATIC_ONLY).
W3's first two bytes are NOT read. No callee body. No upstream tracing.

WRITES: nothing into the repository. Fixtures live only in the QC's own OS
temp directory OUTSIDE Git and are removed at the end. Results are printed
as JSON to stdout. Run with: python3 -B qc_stack_replay.py (WSL).
"""

import hashlib
import json
import os
import platform
import re
import struct
import subprocess

QC_RUN_TAG = "QC_PE_935_CMO_ARG1_20261009"
EXE = "/mnt/d/Eudoria_Reconstruction/pcg_install/Entropia.exe"
EXE_SIZE = 8015872
EXE_SHA = "e7785430e81dffe648ce8f5312414b17bc9fce61389689a22f753765d5280f31"

TEMP = "/mnt/c/Users/User/AppData/Local/Temp/opencode/QC_935_CMO_ARG1_20261009"

WIN_VA = 0x00528E76
WIN_END = 0x00528E92
WIN_LEN = 28
WIN_OFF = 1216118
WIN_SHA = "64102bc06987d31b9610b43602b7f777a73219ff9209f554241ee52080b923a2"
# Contract section 3 identity pin (hypothesis bytes, to be MEASURED):
WIN_PIN = ("8B F1 89 74 24 10 8B 44 24 44 8B 4C 24 40 "
           "8B 7C 24 3C 50 51 57 8B CE E8 1E 23 33 00")
CALLEE_PIN = 0x0085B1B0

REG32 = {"eax", "ebx", "ecx", "edx", "esi", "edi", "ebp", "esp"}
ALLOWED_MNEMONICS = {"mov", "push", "call", "sub", "nop"}  # straight-line set


class Blocked(Exception):
    """Hard identity failure -> BLOCKED (before science)."""


class FailClosed(Exception):
    """Controlled analysis boundary -> UNRESOLVED/FAIL, never fabrication."""


def sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def hx(v):
    return "0x%08X" % v


def esp_expr(off):
    if off == 0:
        return "S"
    return ("S+0x%X" % off) if off > 0 else ("S-0x%X" % (-off))


# ------------------------------------------------------------ own PE mapping
def pe_map():
    with open(EXE, "rb") as f:
        head = f.read(0x2000)
    if head[:2] != b"MZ":
        raise Blocked("no MZ signature")
    lfanew = struct.unpack_from("<I", head, 0x3C)[0]
    if head[lfanew:lfanew + 4] != b"PE\x00\x00":
        raise Blocked("no PE signature")
    machine = struct.unpack_from("<H", head, lfanew + 4)[0]
    if machine != 0x14C:
        raise Blocked("machine != 0x14C")
    nsec = struct.unpack_from("<H", head, lfanew + 6)[0]
    optsz = struct.unpack_from("<H", head, lfanew + 20)[0]
    magic = struct.unpack_from("<H", head, lfanew + 24)[0]
    if magic != 0x10B:
        raise Blocked("not PE32 (magic != 0x10B)")
    image_base = struct.unpack_from("<I", head, lfanew + 24 + 28)[0]
    rva = WIN_VA - image_base
    tab = lfanew + 24 + optsz
    hits = []
    secs = []
    for i in range(nsec):
        s = head[tab + 40 * i: tab + 40 * (i + 1)]
        if len(s) < 40:
            raise Blocked("section table truncated")
        name = s[:8].rstrip(b"\x00").decode("ascii", "replace")
        vsz = struct.unpack_from("<I", s, 8)[0]
        sva = struct.unpack_from("<I", s, 12)[0]
        rsz = struct.unpack_from("<I", s, 16)[0]
        raw = struct.unpack_from("<I", s, 20)[0]
        secs.append({"name": name, "virtual_address": sva,
                     "virtual_size": vsz, "raw_size": rsz,
                     "raw_pointer": raw})
        if sva != 0 and sva <= rva < sva + max(vsz, rsz):
            hits.append({"name": name, "section_virtual_address": sva,
                         "section_raw_pointer": raw,
                         "computed_file_offset": rva - sva + raw})
    if len(hits) != 1:
        raise Blocked("window RVA covered by %d sections (need exactly 1)"
                      % len(hits))
    hit = hits[0]
    if hit["computed_file_offset"] != WIN_OFF:
        raise Blocked("computed offset %d != pinned offset %d"
                      % (hit["computed_file_offset"], WIN_OFF))
    return {"machine": "0x14C (i386)", "image_base": image_base,
            "window_rva": rva, "section": hit["name"],
            "section_virtual_address": hit["section_virtual_address"],
            "section_raw_pointer": hit["section_raw_pointer"],
            "computed_file_offset": hit["computed_file_offset"],
            "expected_file_offset": WIN_OFF, "mapping_match": True,
            "covering_sections": len(hits), "sections": secs}


# ------------------------------------------------------- own fixture factory
def build_fixtures(win):
    """Build the six contract cases + two QC negative controls.

    Mutation byte sets come from the CONTRACT section 5 table (shared
    pre-registered input). Original bytes at each mutation offset are
    verified against the QC's OWN window read before mutating, and each
    finished fixture is verified to differ from baseline ONLY at the
    declared offsets.
    """
    if " ".join("%02X" % b for b in win) != WIN_PIN:
        raise Blocked("QC window bytes differ from the contract pin bytes")

    def mk(name, changes, desc):
        b = bytearray(win)
        for off, old, new in changes:
            if b[off] != old:
                raise Blocked("%s: byte at offset %d is %02X, expected %02X"
                              % (name, off, b[off], old))
            b[off] = new
        m = bytes(b)
        if len(m) != WIN_LEN:
            raise Blocked("%s: fixture length %d" % (name, len(m)))
        diff = [i for i in range(len(win)) if win[i] != m[i]]
        if diff != sorted(c[0] for c in changes):
            raise Blocked("%s: byte deltas %s != declared %s"
                          % (name, diff, sorted(c[0] for c in changes)))
        return {"name": name, "bytes": m,
                "changes": [{"offset": o, "original": "%02X" % a,
                             "mutated": "%02X" % n} for o, a, n in changes],
                "diff_offsets_vs_baseline": diff, "description": desc}

    o = lambda va: va - WIN_VA  # noqa: E731
    return [
        mk("BASELINE", [],
           "no change (the authorized original 28 bytes)"),
        mk("M1_PUSH_ORDER",
           [(o(0x00528E89), 0x51, 0x57), (o(0x00528E8A), 0x57, 0x51)],
           "0x00528E89..8A: 51 57 -> 57 51 (push order swap; last push "
           "supplies the ECX value loaded @0x00528E80 from [S+0x40])"),
        mk("M2_ESP_BEFORE_READ",
           [(o(0x00528E78), 0x89, 0x83), (o(0x00528E79), 0x74, 0xEC),
            (o(0x00528E7A), 0x24, 0x04), (o(0x00528E7B), 0x10, 0x90)],
           "0x00528E78..7B: 89 74 24 10 -> 83 EC 04 90 (sub esp,4; nop; "
           "loads then execute with ESP=S-4)"),
        mk("M3_EDI_DEFINITION_REMOVED",
           [(o(0x00528E85), 0x7C, 0x4C)],
           "0x00528E84..87: 8B 7C 24 3C -> 8B 4C 24 3C (load defines ECX, "
           "not EDI; push edi has no in-window definition)"),
        mk("M4_RECEIVER_ONLY",
           [(o(0x00528E8C), 0xCE, 0xCF)],
           "0x00528E8B..8C: 8B CE -> 8B CF (mov ecx,edi; receiver channel "
           "only; arg1 stack delivery unchanged)"),
        mk("M5_SOURCE_DISPLACEMENT",
           [(o(0x00528E87), 0x3C, 0x38)],
           "0x00528E84..87: 8B 7C 24 3C -> 8B 7C 24 38 (EDI/arg1 derive "
           "from [S+0x38]; stack deltas and receiver as baseline)"),
        mk("NC1_FAILCLOSED",
           [(o(0x00528E7C), 0x8B, 0x0F), (o(0x00528E7D), 0x44, 0xB0),
            (o(0x00528E7E), 0x24, 0xD8), (o(0x00528E7F), 0x44, 0x90)],
           "0x00528E7C..7F: 8B 44 24 44 -> 0F B0 D8 90 (cmpxchg bl,al; "
           "nop): an instruction OUTSIDE the supported straight-line set — "
           "the QC replay MUST return a controlled FAIL_CLOSED, never a "
           "fabricated source (QC negative control, not a contract case)"),
        mk("NC2_TARGET_MISMATCH",
           [(o(0x00528E8E), 0x1E, 0x2E)],
           "0x00528E8E: rel32 first byte 0x1E -> 0x2E (call target "
           "recomputes to 0x0085B1C0 != pinned 0x0085B1B0): the QC's own "
           "call-target expectation MUST FAIL on it (QC negative control, "
           "not a contract case)"),
    ]


# ------------------------------------------------------- own objdump handling
def objdump_version():
    p = subprocess.run(["objdump", "--version"], capture_output=True,
                       text=True, timeout=30)
    return p.stdout.splitlines()[0].strip()


def run_objdump(fixture_path):
    cmd = ["objdump", "-D", "-b", "binary", "-m", "i386", "-M", "intel",
           "--adjust-vma=0x528e76", fixture_path]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    return {"returncode": p.returncode, "stdout": p.stdout,
            "stderr": p.stderr, "command": " ".join(cmd)}


def parse_objdump(raw, fixture_bytes):
    """The QC's OWN parser for objdump raw-binary output.

    Differences from the executor's parser, by construction:
      * splits the line on TAB (objdump's actual field separator) instead
        of a whitespace regex;
      * cross-validates EVERY decoded instruction's byte column against the
        physical fixture bytes at the instruction's window offset (the
        executor trusts the byte column);
      * computes instruction length from the cross-validated byte tokens;
      * fail-closes on '(bad)' marks, non-contiguous streams, wrong
        start/end boundaries, or non-hex byte tokens.
    """
    insns = []
    for line in raw.splitlines():
        if ":" not in line:
            continue
        head, _, rest = line.partition(":")
        hs = head.strip()
        if not re.fullmatch(r"[0-9a-fA-F]+", hs):
            continue
        va = int(hs, 16)
        segs = [s for s in rest.split("\t") if s.strip() != ""]
        if len(segs) < 2:
            continue
        toks = segs[0].split()
        for t in toks:
            if not re.fullmatch(r"[0-9a-fA-F]{2}", t):
                raise FailClosed("non-hex byte token %r in byte column"
                                 % t)
        text = " ".join(" ".join(segs[1:]).split())
        if "(bad" in text:
            raise FailClosed("objdump marked an undecodable instruction: "
                             "%r" % text)
        b = bytes(int(t, 16) for t in toks)
        # byte-column cross-validation against the physical fixture bytes
        off = va - WIN_VA
        if (off < 0 or off + len(b) > len(fixture_bytes)
                or fixture_bytes[off:off + len(b)] != b):
            raise FailClosed("objdump byte column disagrees with fixture "
                             "bytes @%s" % hx(va))
        parts = text.split(None, 1)
        insns.append({"va": va, "len": len(b), "bytes": b, "text": text,
                      "mnem": parts[0],
                      "ops": parts[1].strip() if len(parts) > 1 else ""})
    if not insns:
        raise FailClosed("objdump produced no instruction lines")
    if insns[0]["va"] != WIN_VA:
        raise FailClosed("decode does not start at 0x00528E76 (got %s)"
                         % hx(insns[0]["va"]))
    for a, b2 in zip(insns, insns[1:]):
        if a["va"] + a["len"] != b2["va"]:
            raise FailClosed("non-contiguous instruction stream @%s"
                             % hx(b2["va"]))
    if insns[-1]["va"] + insns[-1]["len"] != WIN_END:
        raise FailClosed("decode does not end exactly at 0x00528E92 (got "
                         "%s)" % hx(insns[-1]["va"] + insns[-1]["len"]))
    return insns


# ---------------------------------------------------- own symbolic replay
MEM_ESP = re.compile(r"^DWORD PTR \[esp([+-]0x[0-9a-fA-F]+)?\]$")


def mem_disp(operand):
    m = MEM_ESP.match(operand)
    if not m:
        return None
    return 0 if m.group(1) is None else int(m.group(1), 16)


def split_operands(ops):
    out, depth, cur = [], 0, ""
    for ch in ops:
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
        if ch == "," and depth == 0:
            out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur.strip())
    return out


def replay(insns):
    """The QC's OWN symbolic replay. S = the UNKNOWN ESP at 0x00528E76.

    Fail-closed on every instruction outside the supported straight-line
    set. Register definitions are snapshotted AT PUSH TIME (correct
    reaching-definition semantics by construction). Distinguishes the
    loaded VALUE from the ADDRESS of its source slot and from the
    ARGUMENT SLOT the value is copied into.
    """
    esp = 0
    rstate = {}          # reg -> definition record (last write wins)
    defs_history = []     # ALL definition events in order (no collapsing)
    writes = []
    loads = []
    pushes = []
    slots = {}            # esp offset -> content expression
    deltas = []
    rows = []
    calls = []

    for ins in insns:
        va, mn, ops = ins["va"], ins["mnem"], ins["ops"]
        delta = 0
        kind = None
        dst = ""
        srcv = ""
        slot_addr = ""
        note = ""
        if mn not in ALLOWED_MNEMONICS:
            raise FailClosed("unsupported mnemonic %r @%s (outside the "
                             "window's allowed straight-line set)"
                             % (mn, hx(va)))
        if mn == "mov":
            a = split_operands(ops)
            if len(a) != 2:
                raise FailClosed("mov with %d operands @%s"
                                 % (len(a), hx(va)))
            d, s = a
            s_disp = mem_disp(s)
            d_disp = mem_disp(d)
            if d in REG32 and s_disp is not None:
                eff = esp + s_disp
                rec = {"expr": "MEM(%s)@%s" % (esp_expr(eff), hx(va)),
                       "def_va": va, "def_insn": ins["text"],
                       "kind": "LOAD", "src_reg": None,
                       "src_slot": esp_expr(eff)}
                rstate[d] = rec
                defs_history.append(dict(reg=d, **rec))
                loads.append({"va": hx(va), "dst": d,
                              "esp_at_load": esp_expr(esp),
                              "slot": esp_expr(eff)})
                kind = "REG_LOAD"
                dst = d.upper()
                srcv = rec["expr"]
                slot_addr = esp_expr(eff)
                note = ("value loaded from source slot; ESP at load = %s"
                        % esp_expr(esp))
            elif d in REG32 and s in REG32:
                sr = rstate.get(s)
                rec = {"expr": sr["expr"] if sr else s.upper() + "_ENTRY",
                       "def_va": va, "def_insn": ins["text"],
                       "kind": "COPY", "src_reg": s,
                       "src_slot": (sr["src_slot"] if sr else None)}
                rstate[d] = rec
                defs_history.append(dict(reg=d, **rec))
                kind = "REG_COPY"
                dst = d.upper()
                srcv = rec["expr"]
                note = "register copy from %s" % s.upper()
            elif d_disp is not None and s in REG32:
                eff = esp + d_disp
                sr = rstate.get(s)
                vexpr = sr["expr"] if sr else s.upper() + "_ENTRY"
                writes.append({"va": hx(va), "addr": esp_expr(eff),
                               "value": vexpr, "src_reg": s})
                kind = "MEM_WRITE"
                dst = "[%s]" % esp_expr(eff)
                srcv = vexpr
                note = "in-window memory write to %s" % esp_expr(eff)
            else:
                raise FailClosed("unsupported mov form @%s: %s"
                                 % (hx(va), ins["text"]))
        elif mn == "push":
            a = split_operands(ops)
            if len(a) != 1 or a[0] not in REG32:
                raise FailClosed("unsupported push form @%s: %s"
                                 % (hx(va), ins["text"]))
            reg = a[0]
            delta = -4
            esp += delta
            sr = rstate.get(reg)
            val = sr["expr"] if sr else reg.upper() + "_ENTRY"
            slots[esp] = val
            pushes.append({"va": hx(va), "reg": reg, "slot_off": esp,
                           "slot": esp_expr(esp), "value": val,
                           "def_at_push": dict(sr) if sr else None})
            kind = "PUSH"
            dst = "[%s]" % esp_expr(esp)
            srcv = val
            note = "push %s -> prepared stack slot %s" % (
                reg.upper(), esp_expr(esp))
        elif mn == "sub":
            a = split_operands(ops)
            if (len(a) != 2 or a[0] != "esp"
                    or not re.fullmatch(r"0x[0-9a-fA-F]+", a[1])):
                raise FailClosed("unsupported sub form @%s: %s"
                                 % (hx(va), ins["text"]))
            imm = int(a[1], 16)
            delta = -imm
            esp += delta
            kind = "ESP_ADJ"
            dst = "ESP"
            srcv = esp_expr(esp)
            note = "sub esp,%s" % a[1]
        elif mn == "nop":
            kind = "NOP"
            note = "no effect"
        elif mn == "call":
            b = ins["bytes"]
            if len(b) != 5 or b[0] != 0xE8:
                raise FailClosed("call @%s is not a 5-byte E8 rel32 form"
                                 % hx(va))
            esp_before = esp
            delta = -4
            esp += delta
            nxt = va + 5
            slots[esp] = "RET@%s" % hx(nxt)
            rel = struct.unpack("<i", b[1:5])[0]
            target = nxt + rel
            obj_target = int(ops, 16) if re.fullmatch(
                r"0x[0-9a-fA-F]+", ops) else None
            calls.append({"va": va, "esp_before_call_off": esp_before,
                          "next_va": nxt, "rel32": rel,
                          "rel32_hex": "%08X" % (rel & 0xFFFFFFFF),
                          "recomputed_target": target,
                          "objdump_target": obj_target,
                          "bytes": b})
            kind = "CALL"
            dst = "[%s]" % esp_expr(esp)
            srcv = "RET@%s" % hx(nxt)
            note = "return-address push by CALL; target %s" % hx(target)
        deltas.append(delta)
        rows.append({"va": hx(va), "bytes": ins["bytes"].hex(" ").upper(),
                     "text": ins["text"], "esp_delta": delta,
                     "esp_after": esp_expr(esp), "kind": kind, "dst": dst,
                     "src_or_value": srcv, "source_slot_address": slot_addr,
                     "note": note})

    if len(calls) != 1:
        raise FailClosed("expected exactly one CALL, got %d" % len(calls))
    call = calls[0]
    if call["va"] != insns[-1]["va"]:
        raise FailClosed("CALL is not the final instruction")

    esp_before_call = call["esp_before_call_off"]
    esp_entry = esp_before_call - 4

    def arg(n):
        off = esp_entry + 4 * n
        rec = {"entry_slot": esp_expr(off),
               "content": slots.get(off, "UNWRITTEN_BY_IN_WINDOW_PUSH")}
        p = next((x for x in pushes if x["slot_off"] == off), None)
        if p is None:
            rec.update({"delivered_by": "NO_IN_WINDOW_PUSH",
                        "push_va": None, "register": None,
                        "value_expression": None, "in_window_def": None,
                        "status": "SLOT_CONTENT_UNRESOLVED"})
            return rec
        rec.update({"delivered_by": "push %s" % p["reg"],
                    "push_va": p["va"], "register": p["reg"],
                    "value_expression": p["value"]})
        d = p["def_at_push"]
        if d is not None:
            rec["in_window_def"] = {
                "va": hx(d["def_va"]), "instruction": d["def_insn"],
                "source_kind": d["kind"], "source_register": d["src_reg"],
                "source_slot": d["src_slot"],
                "value_expression": d["expr"]}
            rec["status"] = "IN_WINDOW_REACHING_DEFINITION_ESTABLISHED"
        else:
            rec["in_window_def"] = None
            rec["status"] = "UNRESOLVED_UPSTREAM"
        return rec

    ec = rstate.get("ecx")
    receiver = {"channel": "ECX (thiscall receiver; separate from arg1)"}
    if ec is not None:
        receiver.update({"def_va": hx(ec["def_va"]),
                         "instruction": ec["def_insn"],
                         "source_register": ec["src_reg"],
                         "value_expression": ec["expr"],
                         "source_slot": ec["src_slot"]})
    else:
        receiver.update({"def_va": None, "instruction": None,
                         "source_register": None,
                         "value_expression": "ECX_ENTRY",
                         "source_slot": None,
                         "status": "NO_IN_WINDOW_DEFINITION"})

    facts = {
        "instruction_count": len(insns),
        "instructions": [{"va": hx(i["va"]), "len": i["len"],
                          "bytes": i["bytes"].hex(" ").upper(),
                          "text": i["text"]} for i in insns],
        "esp_at_window_start": "S",
        "esp_deltas_by_instruction": deltas,
        "esp_before_call": esp_expr(esp_before_call),
        "esp_at_callee_entry": esp_expr(esp_entry),
        "arg1": arg(1),
        "arg2": arg(2),
        "arg3": arg(3),
        "receiver": receiver,
        "pushes": [{"va": p["va"], "reg": p["reg"], "slot": p["slot"],
                    "value": p["value"],
                    "def_va_at_push": (hx(p["def_at_push"]["def_va"])
                                       if p["def_at_push"] else None),
                    "source_slot_at_push": (p["def_at_push"]["src_slot"]
                                            if p["def_at_push"] else None)}
                   for p in pushes],
        "loads": loads,
        "in_window_memory_writes": writes,
        "register_definitions_full_history": defs_history,
        "call": {"va": hx(call["va"]),
                 "bytes": call["bytes"].hex(" ").upper(),
                 "rel32_signed_decimal": call["rel32"],
                 "rel32_hex": call["rel32_hex"],
                 "next_va": hx(call["next_va"]),
                 "recomputed_target": hx(call["recomputed_target"]),
                 "objdump_target": (hx(call["objdump_target"])
                                    if call["objdump_target"] is not None
                                    else None),
                 "recompute_vs_objdump_match":
                     call["objdump_target"] == call["recomputed_target"]},
        "window_first_va": hx(insns[0]["va"]),
        "window_last_end": hx(insns[-1]["va"] + insns[-1]["len"]),
        "straight_line_no_branches": all(
            i["mnem"] in ALLOWED_MNEMONICS for i in insns),
    }
    return facts, rows


# ------------------- own expectation encoding (contract sections 4/5/6) ----
def qc_expectations(case, f):
    """The QC's OWN translation of the contract's expected discriminating
    results (contract section 5 table + section 4/6 hypothesis). NOT taken
    from the executor's implementation."""
    a1, a2, a3 = f["arg1"], f["arg2"], f["arg3"]
    checks = []

    def chk(field, exp, got):
        checks.append({"field": field, "expected": exp, "measured": got,
                       "match": exp == got})

    if case in ("BASELINE", "NC2_TARGET_MISMATCH"):
        chk("instruction_count", 10, f["instruction_count"])
        chk("insn_vas",
            ["0x00528E76", "0x00528E78", "0x00528E7C", "0x00528E80",
             "0x00528E84", "0x00528E88", "0x00528E89", "0x00528E8A",
             "0x00528E8B", "0x00528E8D"],
            [i["va"] for i in f["instructions"]])
        chk("insn_lens", [2, 4, 4, 4, 4, 1, 1, 1, 2, 5],
            [i["len"] for i in f["instructions"]])
        chk("window_last_end", "0x00528E92", f["window_last_end"])
        chk("call_recomputed_target", "0x0085B1B0",
            f["call"]["recomputed_target"])
        chk("call_recompute_vs_objdump", True,
            f["call"]["recompute_vs_objdump_match"])
        chk("esp_deltas", [0, 0, 0, 0, 0, -4, -4, -4, 0, -4],
            f["esp_deltas_by_instruction"])
        chk("esp_before_call", "S-0xC", f["esp_before_call"])
        chk("esp_at_callee_entry", "S-0x10", f["esp_at_callee_entry"])
        chk("arg1_entry_slot", "S-0xC", a1["entry_slot"])
        chk("arg1_push_va", "0x00528E8A", a1["push_va"])
        chk("arg1_register", "edi", a1["register"])
        chk("arg1_value_expression", "MEM(S+0x3C)@0x00528E84",
            a1["value_expression"])
        chk("arg1_in_window_def_va", "0x00528E84", a1["in_window_def"]["va"])
        chk("arg1_source_slot", "S+0x3C", a1["in_window_def"]["source_slot"])
        chk("arg1_status", "IN_WINDOW_REACHING_DEFINITION_ESTABLISHED",
            a1["status"])
        chk("receiver_source_register", "esi",
            f["receiver"]["source_register"])
        chk("receiver_value_expression", "ECX_ENTRY",
            f["receiver"]["value_expression"])
        chk("mem_writes",
            [{"va": "0x00528E78", "addr": "S+0x10"}],
            [{"va": w["va"], "addr": w["addr"]}
             for w in f["in_window_memory_writes"]])
        chk("loads_esp_at_load", ["S", "S", "S"],
            [l["esp_at_load"] for l in f["loads"]])
        chk("push_slots", ["S-0x4", "S-0x8", "S-0xC"],
            [p["slot"] for p in f["pushes"]])
        chk("arg2_register", "ecx", a2["register"])
        chk("arg2_source_slot", "S+0x40", a2["in_window_def"]["source_slot"])
        chk("arg3_register", "eax", a3["register"])
        chk("arg3_source_slot", "S+0x44", a3["in_window_def"]["source_slot"])
    elif case == "M1_PUSH_ORDER":
        chk("instruction_count", 10, f["instruction_count"])
        chk("arg1_push_va", "0x00528E8A", a1["push_va"])
        chk("arg1_register", "ecx", a1["register"])
        chk("arg1_status", "IN_WINDOW_REACHING_DEFINITION_ESTABLISHED",
            a1["status"])
        chk("arg1_in_window_def_va", "0x00528E80",
            a1["in_window_def"]["va"])
        chk("arg1_source_slot", "S+0x40", a1["in_window_def"]["source_slot"])
        chk("original_edi_source_claim_not_retained", True,
            a1["in_window_def"]["source_slot"] != "S+0x3C")
        chk("arg2_register", "edi", a2["register"])
        chk("arg2_in_window_def_va", "0x00528E84",
            a2["in_window_def"]["va"])
        chk("arg2_source_slot", "S+0x3C", a2["in_window_def"]["source_slot"])
        chk("receiver_source_register", "esi",
            f["receiver"]["source_register"])
        chk("esp_before_call", "S-0xC", f["esp_before_call"])
        chk("esp_at_callee_entry", "S-0x10", f["esp_at_callee_entry"])
        chk("arg1_entry_slot", "S-0xC", a1["entry_slot"])
        chk("call_recomputed_target", "0x0085B1B0",
            f["call"]["recomputed_target"])
    elif case == "M2_ESP_BEFORE_READ":
        chk("instruction_count", 11, f["instruction_count"])
        chk("arg1_register", "edi", a1["register"])
        chk("arg1_status", "IN_WINDOW_REACHING_DEFINITION_ESTABLISHED",
            a1["status"])
        chk("arg1_in_window_def_va", "0x00528E84",
            a1["in_window_def"]["va"])
        chk("arg1_source_slot", "S+0x38", a1["in_window_def"]["source_slot"])
        chk("esp_before_call", "S-0x10", f["esp_before_call"])
        chk("esp_at_callee_entry", "S-0x14", f["esp_at_callee_entry"])
        chk("arg1_entry_slot", "S-0x10", a1["entry_slot"])
        chk("loads_esp_at_load", ["S-0x4", "S-0x4", "S-0x4"],
            [l["esp_at_load"] for l in f["loads"]])
        chk("mem_writes", [],
            [{"va": w["va"], "addr": w["addr"]}
             for w in f["in_window_memory_writes"]])
        chk("receiver_source_register", "esi",
            f["receiver"]["source_register"])
        chk("call_recomputed_target", "0x0085B1B0",
            f["call"]["recomputed_target"])
    elif case == "M3_EDI_DEFINITION_REMOVED":
        chk("instruction_count", 10, f["instruction_count"])
        chk("arg1_register", "edi", a1["register"])
        chk("arg1_status", "UNRESOLVED_UPSTREAM", a1["status"])
        chk("arg1_in_window_def", None, a1["in_window_def"])
        chk("arg1_value_expression", "EDI_ENTRY", a1["value_expression"])
        chk("arg2_register", "ecx", a2["register"])
        chk("arg2_in_window_def_va", "0x00528E84",
            a2["in_window_def"]["va"])
        chk("arg2_source_slot", "S+0x3C", a2["in_window_def"]["source_slot"])
        chk("receiver_source_register", "esi",
            f["receiver"]["source_register"])
        chk("esp_before_call", "S-0xC", f["esp_before_call"])
        chk("esp_at_callee_entry", "S-0x10", f["esp_at_callee_entry"])
        chk("arg1_entry_slot", "S-0xC", a1["entry_slot"])
        chk("call_recomputed_target", "0x0085B1B0",
            f["call"]["recomputed_target"])
    elif case == "M4_RECEIVER_ONLY":
        chk("instruction_count", 10, f["instruction_count"])
        chk("receiver_source_register", "edi",
            f["receiver"]["source_register"])
        chk("receiver_def_va", "0x00528E8B", f["receiver"]["def_va"])
        chk("receiver_value_expression", "MEM(S+0x3C)@0x00528E84",
            f["receiver"]["value_expression"])
        chk("receiver_value_expression_same_as_arg1", True,
            f["receiver"]["value_expression"] == a1["value_expression"])
        chk("arg1_register", "edi", a1["register"])
        chk("arg1_status", "IN_WINDOW_REACHING_DEFINITION_ESTABLISHED",
            a1["status"])
        chk("arg1_in_window_def_va", "0x00528E84",
            a1["in_window_def"]["va"])
        chk("arg1_source_slot", "S+0x3C", a1["in_window_def"]["source_slot"])
        chk("arg1_entry_slot", "S-0xC", a1["entry_slot"])
        chk("arg1_push_va", "0x00528E8A", a1["push_va"])
        chk("esp_before_call", "S-0xC", f["esp_before_call"])
        chk("esp_at_callee_entry", "S-0x10", f["esp_at_callee_entry"])
        chk("channels_distinct", True,
            f["receiver"]["channel"].startswith("ECX")
            and a1["entry_slot"] == "S-0xC")
        chk("esp_deltas", [0, 0, 0, 0, 0, -4, -4, -4, 0, -4],
            f["esp_deltas_by_instruction"])
    elif case == "M5_SOURCE_DISPLACEMENT":
        chk("instruction_count", 10, f["instruction_count"])
        chk("arg1_register", "edi", a1["register"])
        chk("arg1_status", "IN_WINDOW_REACHING_DEFINITION_ESTABLISHED",
            a1["status"])
        chk("arg1_in_window_def_va", "0x00528E84",
            a1["in_window_def"]["va"])
        chk("arg1_source_slot", "S+0x38", a1["in_window_def"]["source_slot"])
        chk("arg1_value_expression", "MEM(S+0x38)@0x00528E84",
            a1["value_expression"])
        chk("receiver_source_register", "esi",
            f["receiver"]["source_register"])
        chk("esp_before_call", "S-0xC", f["esp_before_call"])
        chk("esp_at_callee_entry", "S-0x10", f["esp_at_callee_entry"])
        chk("arg1_entry_slot", "S-0xC", a1["entry_slot"])
        chk("esp_deltas", [0, 0, 0, 0, 0, -4, -4, -4, 0, -4],
            f["esp_deltas_by_instruction"])
    else:
        raise FailClosed("unknown case %s" % case)
    return checks


def qc_signature(f):
    a1 = f["arg1"]
    return {
        "instruction_count": f["instruction_count"],
        "arg1_register": a1["register"],
        "arg1_status": a1["status"],
        "arg1_source_slot": (a1["in_window_def"]["source_slot"]
                             if a1["in_window_def"] else None),
        "esp_before_call": f["esp_before_call"],
        "esp_at_callee_entry": f["esp_at_callee_entry"],
        "arg1_entry_slot": a1["entry_slot"],
        "receiver_source_register": f["receiver"]["source_register"],
        "mem_write_addrs": [w["addr"] for w in f["in_window_memory_writes"]],
    }


# ------------------------------------------------------------------- main
def main():
    out = {"qc_run_tag": QC_RUN_TAG,
           "run_id": "PE_935_CMO_ARG1_SINGLE_CALLSITE_PROVENANCE_R1_20261009",
           "qc_origin": "pe-master-auditor fresh-context internal QC "
                        "(internal to PE-MASTER; NOT an independent "
                        "Desktop post-audit)",
           "independence_statement": {
               "same_disassembler_as_executor": True,
               "shared_objdump_is_NOT_cross_implementation_decoder_qc": True,
               "own_byte_read": True, "own_pe_mapping": True,
               "own_objdump_invocations": True,
               "own_parser_with_fixture_byte_cross_validation": True,
               "own_symbolic_replay_implementation": True,
               "own_mutant_fixtures": True,
               "own_negative_controls": True,
               "executor_code_imported": False,
               "expectation_source": "frozen contract sections 4/5/6 "
                                     "(independently translated by the QC)"},
           "tool": {"name": "GNU objdump",
                    "version": objdump_version(),
                    "python": platform.python_version(),
                    "uname": " ".join(platform.uname())}}

    # 1. EXE identity BEFORE (own full re-hash)
    sz = os.path.getsize(EXE)
    if sz != EXE_SIZE:
        raise Blocked("EXE size %d != %d" % (sz, EXE_SIZE))
    sha_b = sha_file(EXE)
    if sha_b != EXE_SHA:
        raise Blocked("EXE SHA256 mismatch BEFORE: %s" % sha_b)
    out["exe"] = {"size": sz, "sha256_before": sha_b}

    # 2. PE mapping (own)
    out["pe_mapping"] = pe_map()

    # 3. Window read (own; ONLY the authorized 28 bytes at 1216118)
    with open(EXE, "rb") as f:
        f.seek(WIN_OFF)
        win = f.read(WIN_LEN)
    if len(win) != WIN_LEN:
        raise Blocked("short window read: %d" % len(win))
    wsha = hashlib.sha256(win).hexdigest()
    whex = " ".join("%02X" % b for b in win)
    if wsha != WIN_SHA:
        raise Blocked("window SHA256 mismatch: %s" % wsha)
    if whex != WIN_PIN:
        raise Blocked("window bytes differ from the contract pin")
    out["window"] = {"va_start": hx(WIN_VA), "va_end_exclusive":
                     hx(WIN_END), "size": WIN_LEN, "file_offset": WIN_OFF,
                     "bytes_hex": whex, "sha256": wsha,
                     "expected_sha256": WIN_SHA, "identity_match": True,
                     "pin_bytes_match": True,
                     "note": "QC own read; W3 first two bytes (offsets "
                             "1216116..1216117) NOT read (DOC-1)"}

    # 4. Fixtures + runs
    fixtures = build_fixtures(win)
    os.makedirs(TEMP, exist_ok=True)
    cases_out = []
    facts_by_case = {}
    sig_by_case = {}
    raw_by_case = {}
    cleanup = []

    for fx in fixtures:
        name = fx["name"]
        path = os.path.join(TEMP, "qc_%s.bin" % name.lower())
        with open(path, "wb") as f:
            f.write(fx["bytes"])
        fsha = sha_file(path)
        cleanup.append({"path": path, "sha256": fsha})
        if len(fx["bytes"]) != WIN_LEN:
            raise Blocked("fixture %s length %d" % (name, len(fx["bytes"])))
        od = run_objdump(path)
        if od["returncode"] != 0:
            raise Blocked("objdump failed on %s: %s" % (name, od["stderr"]))
        raw_by_case[name] = od["stdout"]

        entry = {"case": name, "temp_path": path, "size_bytes": WIN_LEN,
                 "sha256": fsha, "is_synthetic": name != "BASELINE",
                 "byte_changes": fx["changes"],
                 "diff_offsets_vs_baseline": fx["diff_offsets_vs_baseline"],
                 "description": fx["description"],
                 "objdump_command": od["command"],
                 "objdump_returncode": od["returncode"],
                 "objdump_stderr": od["stderr"].strip(),
                 "objdump_raw_output": od["stdout"]}

        try:
            insns = parse_objdump(od["stdout"], fx["bytes"])
            facts, rows = replay(insns)
            status = "OK"
            err = None
        except FailClosed as e:
            facts = None
            rows = None
            status = "FAIL_CLOSED"
            err = str(e)
        entry["analysis_status"] = status
        entry["analysis_error"] = err

        if status == "OK":
            checks = qc_expectations(name, facts)
            all_match = all(c["match"] for c in checks)
            sig = qc_signature(facts)
            facts_by_case[name] = facts
            sig_by_case[name] = sig
            differs = None
            if name == "BASELINE":
                verdict = ("BASELINE_QUALIFIED" if all_match
                           else "BASELINE_MISMATCH_HONEST_FAILURE")
            elif name in ("M1_PUSH_ORDER", "M2_ESP_BEFORE_READ",
                          "M3_EDI_DEFINITION_REMOVED", "M4_RECEIVER_ONLY",
                          "M5_SOURCE_DISPLACEMENT"):
                differs = sig != sig_by_case.get("BASELINE")
                verdict = ("CONTROL_PASS" if (all_match and differs)
                           else "CONTROL_FAIL")
            elif name == "NC2_TARGET_MISMATCH":
                tgt = next(c for c in checks
                           if c["field"] == "call_recomputed_target")
                verdict = ("NC_PASS_TARGET_FALSIFIER_LIVE"
                           if (not tgt["match"]
                               and tgt["measured"] == "0x0085B1C0")
                           else "NC_FAIL")
            entry["checks"] = checks
            entry["all_checks_match"] = all_match
            entry["signature"] = sig
            entry["differs_from_baseline"] = differs
            if name == "BASELINE":
                entry["qc_ledger_rows"] = rows
            if name == "NC2_TARGET_MISMATCH":
                entry["nc2_call_target_check"] = next(
                    c for c in checks
                    if c["field"] == "call_recomputed_target")
                entry["nc2_recompute_vs_objdump_check"] = next(
                    c for c in checks
                    if c["field"] == "call_recompute_vs_objdump")
        else:
            if name == "NC1_FAILCLOSED":
                verdict = ("NC_PASS_FAIL_CLOSED_LIVE"
                           if "unsupported mnemonic" in err
                           else "NC_FAIL")
            else:
                verdict = ("UNRESOLVED_WITHIN_BOUND_HONEST_FAILURE"
                           if name == "BASELINE" else "CONTROL_FAIL")
            entry["checks"] = None
            entry["all_checks_match"] = False
            entry["signature"] = None
            entry["differs_from_baseline"] = None
        entry["verdict"] = verdict
        cases_out.append(entry)

    out["cases"] = [
        {k: v for k, v in e.items() if k != "objdump_raw_output"}
        for e in cases_out]
    out["objdump_raw_output_by_case"] = raw_by_case
    out["baseline_facts"] = facts_by_case.get("BASELINE")

    # 5. EXE identity AFTER (own full re-hash)
    sha_a = sha_file(EXE)
    if sha_a != EXE_SHA:
        raise Blocked("EXE SHA256 mismatch AFTER: %s" % sha_a)
    out["exe"]["sha256_after"] = sha_a
    out["exe"]["identity_match_after"] = True

    # 6. Cleanup ONLY the QC's own temp fixtures
    for c in cleanup:
        os.remove(c["path"])
    out["temp_cleanup"] = {"note": "only QC-created fixture files were "
                                  "removed; nothing staged; nothing "
                                  "written into the repository",
                           "files": cleanup}

    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    try:
        main()
    except Blocked as e:
        print("BLOCKED: %s" % e)
        raise SystemExit(3)
