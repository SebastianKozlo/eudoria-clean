#!/usr/bin/env python3
r"""
parse_coff_vtable.py -- Deterministic COFF (.obj) vtable extractor for the
PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1 audit.

Reads MSVC COFF object files (i386), locates `??_7<Class>@@6B@` vtable symbols
and maps each vtable slot to its relocated symbol name via the section
relocation table. Pure stdlib (struct only). Deterministic: same input file ->
same JSON output.

Usage:
  python parse_coff_vtable.py <file.obj> [--classes NiNode,NiAVObject] [--out out.json]

Evidence usage:
  - D:\gamebyroengine\extracted\gb12_build\build\NiMain\NiNode.obj (GB 1.2.2.6 compiled oracle)
  - output JSON -> 03_EVIDENCE/

COFF facts used:
  - IMAGE_FILE_HEADER: 20 bytes (Machine u16, NumberOfSections u16,
    TimeDateStamp u32, PtrToSymbolTable u32, NumberOfSymbols u32,
    SizeOfOptionalHeader u16, Characteristics u16)
  - Section header: 40 bytes (Name[8], PhysicalAddress/VirtualSize u32,
    VirtualAddress u32, SizeOfRawData u32, PointerToRawData u32,
    PointerToRelocations u32, PointerToLinenumbers u32,
    NumberOfRelocations u16, NumberOfLinenumbers u16, Characteristics u32)
  - Symbol record: 18 bytes + aux records (Name u8[8] -- if first u32 == 0 then
    next u32 is string-table offset; Value u32, SectionNumber i16, Type u16,
    StorageClass u8, NumberOfAuxSymbols u8)
  - Relocation entry size auto-detected (8 or 10 bytes; validated against
    symbol count + sane i386 reloc types).
  - IMAGE_REL_I386_DIR32 == 6, IMAGE_REL_I386_DIR32NB == 7, REL32 == 20.
"""
import argparse
import json
import struct
import sys


def read_coff(path):
    with open(path, "rb") as f:
        data = f.read()
    return read_coff_bytes(data)


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
            "index": i + 1,
            "name": name,
            "raw_ptr": rawptr,
            "raw_size": rawsize,
            "rel_ptr": relptr,
            "n_rel": nrel,
        })
        off += 40
    # symbol table (aux records skipped by advancing both index and offset).
    # NOTE: relocation SymbolTableIndex values reference SLOT indices
    # (0..NumberOfSymbols-1, aux slots included), so the returned list is
    # slot-indexed: slots occupied by aux records hold None.
    strtab_base = symptr + nsyms * 18
    symbols = [None] * nsyms
    real = []
    idx = 0
    symoff = symptr
    while idx < nsyms:
        rec = data[symoff: symoff + 18]
        if len(rec) < 18:
            break
        zero, stroff = struct.unpack_from("<II", rec, 0)
        if zero == 0:
            start = strtab_base + stroff
            end = data.index(b"\x00", start) if start < len(data) else len(data) - 1
            name = data[start:end].decode("ascii", "replace")
        else:
            name = rec[0:8].rstrip(b"\x00").decode("ascii", "replace")
        value, secnum, typ, storage, naux = struct.unpack_from("<IhHBB", rec, 8)
        sym = {
            "index": idx,
            "name": name,
            "value": value,
            "section": secnum,
            "type": typ,
            "storage_class": storage,
            "n_aux": naux,
        }
        symbols[idx] = sym
        real.append(sym)
        symoff += 18 * (1 + naux)
        idx += 1 + naux
    return data, sections, symbols, real


def detect_reloc_entry_size(data, sections, nsyms):
    """Validate that reloc entries are the PE/COFF fixed 10-byte layout
    (DWORD VirtualAddress, DWORD SymbolTableIndex, WORD Type). Returns 10 on
    validation success, raises on malformed content (fail-closed)."""
    for s in sections:
        if s["n_rel"] == 0:
            continue
        p = s["rel_ptr"]
        for i in range(s["n_rel"]):
            base = p + i * 10
            if base + 10 > len(data):
                raise ValueError("reloc table overrun in section %s" % s["name"])
            symidx = struct.unpack_from("<I", data, base + 4)[0]
            rtype = struct.unpack_from("<H", data, base + 8)[0]
            if symidx >= nsyms:
                raise ValueError("reloc symbol index %d >= nsyms %d in section %s"
                                 % (symidx, nsyms, s["name"]))
            if rtype > 32:
                raise ValueError("implausible reloc type %d in section %s"
                                 % (rtype, s["name"]))
    return 10


def relocs_for_section(data, s, entry_size):
    out = []
    p = s["rel_ptr"]
    for i in range(s["n_rel"]):
        base = p + i * entry_size
        rva, symidx = struct.unpack_from("<II", data, base)
        rtype = struct.unpack_from("<H", data, base + 8)[0]
        out.append({"offset_in_section": rva, "symbol_index": symidx,
                    "type": rtype})
    return out


def find_vtable_symbol(symbols, classname):
    """Return symbol for ??_7<class>@@6B@ (the MSVC vftable decoration)."""
    target = "??_7%s@@6B@" % classname
    for sym in symbols:
        if sym is not None and sym["name"] == target:
            return sym
    return None


def dump_vtable(data, sections, symbols, classname, reloc_entry_size):
    sym = find_vtable_symbol(symbols, classname)
    if sym is None:
        return {"class": classname, "found": False}
    secnum = sym["section"]
    sec = None
    for s in sections:
        if s["index"] == secnum:
            sec = s
            break
    if sec is None:
        return {"class": classname, "found": True, "symbol": sym["name"],
                "error": "bad section number %d" % secnum}
    rels = relocs_for_section(data, sec, reloc_entry_size)
    by_off = {}
    for r in rels:
        by_off.setdefault(r["offset_in_section"], []).append(r)
    base = sym["value"]
    slots = []
    off = base
    while off in by_off:
        rs = sorted(by_off[off], key=lambda r: r["type"])
        names = []
        for r in rs:
            si = r["symbol_index"]
            if 0 <= si < len(symbols) and symbols[si] is not None:
                names.append(symbols[si]["name"])
            else:
                names.append("<bad symbol slot %d>" % si)
        slots.append({"slot": len(slots), "offset": off,
                      "reloc_types": [r["type"] for r in rs],
                      "symbols": names})
        off += 4
    return {
        "class": classname,
        "found": True,
        "symbol": sym["name"],
        "section": sec["name"],
        "section_index": secnum,
        "value_in_section": base,
        "slot_count": len(slots),
        "slots": slots,
    }


def iter_ar_members(archive_bytes):
    """Yield (member_name, member_bytes) for MS COFF archive (lib) members.
    Skips the special linker ('/') and long-name ('//') members."""
    if archive_bytes[:8] != b"!<arch>\n":
        raise ValueError("not an AR archive")
    longnames = b""
    off = 8
    n = 0
    while off + 60 <= len(archive_bytes):
        hdr = archive_bytes[off:off + 60]
        rawname = hdr[0:16].decode("ascii", "replace")
        size = int(hdr[48:58].decode("ascii", "replace").strip())
        start = off + 60
        body = archive_bytes[start:start + size]
        off = start + size + (size & 1)
        n += 1
        if rawname.startswith("/") and rawname.strip("/") == "":
            # symbol-index member(s); first '/' may also be longname table '//'
            if rawname == "//" or (rawname.rstrip(" ") == "//"):
                longnames = body
            continue
        name = rawname.rstrip(" ")
        if name.endswith("/"):
            name = name[:-1]
        # long name: '/NN' -> offset into longnames table
        if name.startswith("/") and name[1:].isdigit():
            stroff = int(name[1:])
            end = longnames.index(b"\n", stroff) if stroff < len(longnames) else -1
            if end > -1:
                name = longnames[stroff:end].decode("ascii", "replace").rstrip("\x00")
        yield (name, body)


def parse_object_result(path_label, data, classes=None, all_vtables=False):
    """Parse one COFF object and return the JSON-ready result dict."""
    data, sections, symbols, real = read_coff_bytes(data)
    entry_size = detect_reloc_entry_size(data, sections, len(symbols))
    result = {
        "file": path_label,
        "machine": "0x014C (i386)",
        "n_symbol_slots": len(symbols),
        "n_real_symbols": len(real),
        "n_sections": len(sections),
        "reloc_entry_size": entry_size,
        "vtables": [],
    }
    if all_vtables:
        classes = sorted({s["name"][4:].split("@")[0] for s in real
                           if s["name"].startswith("??_7") and "@@6B@" in s["name"]})
    for c in classes or []:
        result["vtables"].append(dump_vtable(data, sections, symbols, c,
                                              entry_size))
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("obj")
    ap.add_argument("--classes", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--all-vtables", action="store_true")
    ap.add_argument("--archive-member", default="",
                    help="inside .lib archives: substring filter for member name")
    ap.add_argument("--extract-dir", default="",
                    help="inside .lib archives: write each member containing a "
                         "wanted vtable to <dir>/<class>_<slot>.obj")
    args = ap.parse_args()
    with open(args.obj, "rb") as f:
        blob = f.read()
    results = []
    if blob[:8] == b"!<arch>\n":
        # archive (.lib): scan members, dump requested vtables from each
        classes = [c.strip() for c in args.classes.split(",") if c.strip()]
        wanted = set("??_7%s@@6B@" % c for c in classes)
        member_seq = 0
        if args.extract_dir:
            import os
            if not os.path.isdir(args.extract_dir):
                os.makedirs(args.extract_dir)
        for name, body in iter_ar_members(blob):
            member_seq += 1
            if args.archive_member and args.archive_member.lower() not in name.lower():
                continue
            if len(body) < 20 or struct.unpack_from("<H", body, 0)[0] != 0x014C:
                continue
            try:
                _, _, symbols, real = read_coff_bytes(body)
            except Exception:
                continue
            names = {s["name"] for s in real if s is not None}
            hit = names & wanted
            if args.all_vtables or hit:
                r = parse_object_result("%s::%s" % (args.obj, name), body,
                                        classes=classes, all_vtables=args.all_vtables)
                results.append(r)
                if args.extract_dir and hit:
                    for cls in sorted(hit):
                        clsname = cls[4:].split("@")[0]
                        path = os.path.join(args.extract_dir,
                                           "%s_%04d.obj" % (clsname, member_seq))
                        with open(path, "wb") as g:
                            g.write(body)
        final = {
            "file": args.obj,
            "archive": True,
            "n_members_scanned": sum(1 for _ in iter_ar_members(blob)),
            "member_results": results,
        }
        text = json.dumps(final, indent=1)
    else:
        r = parse_object_result(args.obj, blob,
                                classes=[c.strip() for c in args.classes.split(",") if c.strip()],
                                all_vtables=args.all_vtables)
        text = json.dumps(r, indent=1)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
