#!/usr/bin/env python3
r"""coff_disasm_symbol.py -- Deterministic symbol-targeted capstone
disassembler for MSVC i386 COFF .obj members and .lib archives, for the
PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1 audit.

Purpose:
  1. Disassemble compiled Gamebryo oracle functions (e.g. the protected
     NiAVObject constructor, NiNode::GetObjectByName) directly from
     D:\gamebyroengine .obj/.lib build products (READ ONLY).
  2. Relocation-annotated output: call/jmp targets are resolved to MSVC
     symbol names via the section relocation table -- giving compiled-code
     behavioral fingerprints independent of header/source reasoning.

Pure stdlib (struct) + capstone 5.x (measured 5.0.7). Deterministic: same
input -> same output.

Usage:
  coff_disasm_symbol.py <file.obj|file.lib> --symbol <decorated-or-prefix>
      [--member-prefix X] [--max 0x400] [--out out.txt]
  For .lib archives, --member-prefix selects members whose name contains the
  substring (e.g. /2822). The first symbol whose name STARTS WITH the given
  prefix is disassembled.
"""
import argparse
import struct
import sys

import capstone


def read_coff_bytes(data):
    if len(data) < 20:
        raise ValueError("file too small for COFF header")
    (machine, nsec, tds, symptr, nsyms, optsize, chars) = struct.unpack_from(
        "<HHIIIHH", data, 0)
    if machine != 0x014C:
        raise ValueError("not an i386 COFF file (machine=0x%04X)" % machine)
    sections = []
    off = 20 + optsize
    for i in range(nsec):
        name = data[off:off + 8].rstrip(b"\x00").decode("ascii", "replace")
        (physaddr, vaddr, rawsize, rawptr, relptr, lineptr, nrel, nline,
         schars) = struct.unpack_from("<IIIIIIHHI", data, off + 8)
        sections.append({
            "index": i + 1, "name": name, "raw_ptr": rawptr,
            "raw_size": rawsize, "rel_ptr": relptr, "n_rel": nrel,
        })
        off += 40
    strtab_base = symptr + nsyms * 18
    symbols = [None] * nsyms
    idx = 0
    symoff = symptr
    while idx < nsyms:
        rec = data[symoff: symoff + 18]
        if len(rec) < 18:
            break
        zero, stroff = struct.unpack_from("<II", rec, 0)
        if zero == 0:
            start = strtab_base + stroff
            end = data.index(b"\x00", start)
            name = data[start:end].decode("ascii", "replace")
        else:
            name = rec[0:8].rstrip(b"\x00").decode("ascii", "replace")
        value, secnum, typ, storage, naux = struct.unpack_from("<IhHBB", rec, 8)
        symbols[idx] = {"index": idx, "name": name, "value": value,
                        "section": secnum, "type": typ,
                        "storage_class": storage, "n_aux": naux}
        symoff += 18 * (1 + naux)
        idx += 1 + naux
    return data, sections, symbols


def relocs_for_section(data, s):
    out = []
    p = s["rel_ptr"]
    for _ in range(s["n_rel"]):
        rva, symidx = struct.unpack_from("<II", data, p)
        rtype = struct.unpack_from("<H", data, p + 8)[0]
        out.append({"offset_in_section": rva, "symbol_index": symidx,
                    "type": rtype})
        p += 10
    return out


def disasm_symbol(data, sections, symbols, sym_prefix, max_bytes,
                  stop_at_ret=False):
    target = None
    for sym in symbols:
        if sym is not None and sym["name"].startswith(sym_prefix):
            target = sym
            break
    if target is None:
        return None, "symbol not found: %s*" % sym_prefix
    secnum = target["section"]
    sec = None
    for s in sections:
        if s["index"] == secnum:
            sec = s
            break
    if sec is None:
        return target, "symbol section %d not found" % secnum
    start = sec["raw_ptr"] + target["value"]
    rels = relocs_for_section(data, sec)
    by_off = {}
    for r in rels:
        by_off.setdefault(r["offset_in_section"], []).append(r)

    lines = []
    lines.append("SYMBOL: %s" % target["name"])
    lines.append("SECTION: %s (#%d) value_in_section=0x%X -> file 0x%X"
                 % (sec["name"], secnum, target["value"], start))
    code = data[start:start + max_bytes]
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    end_off = None
    for ins in md.disasm(code, 0):
        raw = " ".join("%02X" % b for b in ins.bytes)
        # section-relative offset of this instruction
        rel_off = target["value"] + ins.address
        ann = ""
        if rel_off in by_off:
            names = []
            for r in by_off[rel_off]:
                si = r["symbol_index"]
                if 0 <= si < len(symbols) and symbols[si] is not None:
                    names.append(symbols[si]["name"])
            ann = "  ; reloc -> " + ", ".join(names)
        lines.append("%04X  %-21s %-7s %s%s"
                     % (ins.address, raw, ins.mnemonic, ins.op_str, ann))
        if ins.mnemonic in ("ret", "retn"):
            nxt = start + ins.address + ins.size
            if stop_at_ret or data[nxt] in (0xCC, 0x90):
                end_off = ins.address + ins.size
                break
    lines.append("(stop%s)" % (" at +%X" % end_off if end_off else " at cap"))
    return target, "\n".join(lines)


def iter_ar_members(archive_bytes):
    if archive_bytes[:8] != b"!<arch>\n":
        raise ValueError("not an AR archive")
    longnames = b""
    off = 8
    while off + 60 <= len(archive_bytes):
        hdr = archive_bytes[off:off + 60]
        rawname = hdr[0:16].decode("ascii", "replace")
        size = int(hdr[48:58].decode("ascii", "replace").strip())
        start = off + 60
        body = archive_bytes[start:start + size]
        off = start + size + (size & 1)
        if rawname.rstrip(" ") == "//":
            longnames = body
            continue
        if rawname.strip("/").strip(" ") == "":
            continue
        name = rawname.rstrip(" ")
        if name.endswith("/"):
            name = name[:-1]
        if name.startswith("/") and name[1:].isdigit():
            stroff = int(name[1:])
            if stroff < len(longnames):
                nl = longnames.find(b"\n", stroff)
                nul = longnames.find(b"\x00", stroff)
                ends = [e for e in (nl, nul) if e >= 0]
                end = min(ends) if ends else len(longnames)
                name = longnames[stroff:end].decode("ascii", "replace").rstrip("\x00")
            else:
                name = name + "(bad-longname-off)"
        yield (name, body)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("obj")
    ap.add_argument("--symbol", required=True)
    ap.add_argument("--member-prefix", default="")
    ap.add_argument("--max", default="0x400")
    ap.add_argument("--stop-at-ret", action="store_true")
    ap.add_argument("--quiet-members", action="store_true",
                    help="archive mode: only print members where the symbol "
                         "was found (defined, section != 0)")
    ap.add_argument("--out", default="")
    args = ap.parse_args()
    max_bytes = int(args.max, 16)
    with open(args.obj, "rb") as f:
        blob = f.read()
    blocks = []
    if blob[:8] == b"!<arch>\n":
        found_any = False
        for name, body in iter_ar_members(blob):
            if args.member_prefix and args.member_prefix not in name:
                continue
            if len(body) < 20 or struct.unpack_from("<H", body, 0)[0] != 0x014C:
                continue
            try:
                data, sections, symbols = read_coff_bytes(body)
            except Exception:
                continue
            target, res = disasm_symbol(data, sections, symbols,
                                        args.symbol, max_bytes,
                                        stop_at_ret=args.stop_at_ret)
            if target is not None and target["section"] != 0:
                found_any = True
                blocks.append("=== MEMBER %s ===" % name)
                blocks.append(res)
        if not found_any:
            blocks.append("symbol not found in any scanned member")
    else:
        data, sections, symbols = read_coff_bytes(blob)
        target, res = disasm_symbol(data, sections, symbols, args.symbol,
                                    max_bytes, stop_at_ret=args.stop_at_ret)
        blocks.append(res)
    text = "\n".join(blocks) + "\n"
    if args.out:
        with open(args.out, "w", encoding="utf-8") as g:
            g.write(text)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
