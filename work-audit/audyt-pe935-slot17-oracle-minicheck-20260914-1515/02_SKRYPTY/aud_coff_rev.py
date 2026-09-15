# WORK-AUDIT (audytor: Work-Audit, audyt: audyt-pe935-slot17-oracle-minicheck-20260914-1515) - plik audytora, NIE jest czescia pracy wykonawcy
# aud_coff_rev.py - WLASNY, niezalezny parser AR/COFF audytora (inna implementacja niz parse_coff_vtable.py wykonawcy).
# Re-derwuje mapy vtable z fizycznych plikow: NiMain.lib (GB112, era VC71) + gb12 .obj (GB12, VS2022).
import struct
import sys

def coff_symbols(data):
    machine, nsec, tds, symptr, nsyms, optsize, chars = struct.unpack_from("<HHIIIHH", data, 0)
    if machine != 0x014C:
        return None
    strtab = symptr + nsyms * 18
    syms = [None] * nsyms
    idx = 0
    off = symptr
    while idx < nsyms:
        z = struct.unpack_from("<I", data, off)[0]
        if z == 0:
            so = struct.unpack_from("<I", data, off + 4)[0]
            s = strtab + so
            e = data.index(b"\x00", s)
            name = data[s:e].decode("ascii", "replace")
        else:
            name = data[off:off+8].rstrip(b"\x00").decode("ascii", "replace")
        val, secn, typ, cls, naux = struct.unpack_from("<IhHBB", data, off + 8)
        syms[idx] = (name, val, secn, naux)
        off += 18 * (1 + naux)
        idx += 1 + naux
    sections = []
    so = 20 + optsize
    for i in range(nsec):
        nm = data[so:so+8].rstrip(b"\x00").decode("ascii", "replace")
        vsz, va, rsz, rptr, relptr, lnptr, nrel, nln, sc = struct.unpack_from("<IIIIIIHHI", data, so + 8)
        sections.append((nm, va, rsz, rptr, relptr, nrel))
        so += 40
    return sections, syms

def vtable_of(data, sections, syms, cls):
    target = "??_7%s@@6B@" % cls
    hit = None
    for s in syms:
        if s and s[0] == target:
            hit = s
            break
    if hit is None:
        return None
    nm, val, secn, naux = hit
    sec = None
    for s in sections:
        if s[0] != "":
            pass
    # sections are 1-based; sections list index = secn-1
    if secn < 1 or secn > len(sections):
        return None
    sec = sections[secn - 1]
    rels = {}
    rp, nrel = sec[4], sec[5]
    for i in range(nrel):
        rva, symidx = struct.unpack_from("<II", data, rp + i * 10)
        rtype = struct.unpack_from("<H", data, rp + i * 10 + 8)[0]
        if symidx < len(syms) and syms[symidx] is not None:
            rels.setdefault(rva, []).append((rtype, syms[symidx][0]))
    slots = []
    off = val
    while off in rels:
        entries = sorted(rels[off])
        slots.append([e[1] for e in entries])
        off += 4
    return {"symbol": nm, "value": val, "section": sec[0], "slots": slots}

def iter_ar(blob):
    assert blob[:8] == b"!<arch>\n"
    off = 8
    longnames = b""
    first = True
    while off + 60 <= len(blob):
        hdr = blob[off:off+60]
        rawname = hdr[0:16].decode("ascii", "replace")
        size = int(hdr[48:58].decode("ascii", "replace").strip())
        body = blob[off+60:off+60+size]
        off += 60 + size + (size & 1)
        if rawname.rstrip(" ").rstrip("/") == "" or rawname.rstrip(" ") == "/":
            continue
        if rawname.rstrip(" ") == "//":
            longnames = body
            continue
        name = rawname.rstrip(" ").rstrip("/")
        if name.startswith("/") and name[1:].isdigit():
            so = int(name[1:])
            e = longnames.find(b"\n", so)
            e2 = longnames.find(b"\x00", so)
            if e < 0 or (e2 >= 0 and e2 < e):
                e = e2
            name = longnames[so:e if e > 0 else len(longnames)].decode("ascii", "replace").rstrip("\x00")
        yield name, body

def report(label, data, classes):
    r = coff_symbols(data)
    if r is None:
        return
    sections, syms = r
    for cls in classes:
        vt = vtable_of(data, sections, syms, cls)
        if vt is None:
            print("%s :: %s: NOT FOUND" % (label, cls))
            continue
        print("%s :: %s: slots=%d (value=0x%X sec=%s)" % (label, vt["symbol"], len(vt["slots"]), vt["value"], vt["section"]))
        for i, names in enumerate(vt["slots"]):
            print("  slot %2d: %s" % (i, " | ".join(names)))

print("=== GB112 NiMain.lib (era VC71) ===")
with open(r"D:\gamebyroengine\Gamebryo 1.1.2 Evaluation\SDK\Win32\Lib\VC71\ReleaseLib\NiMain.lib", "rb") as f:
    lib = f.read()
want = ["??_7NiNode@@6B@", "??_7NiAVObject@@6B@", "??_7NiObject@@6B@", "??_7NiObjectNET@@6B@", "??_7NiRefObject@@6B@"]
done = set()
nref = 0
for name, body in iter_ar(lib):
    if len(body) < 20 or struct.unpack_from("<H", body, 0)[0] != 0x014C:
        continue
    r = coff_symbols(body)
    if r is None:
        continue
    sections, syms = r
    names = set(s[0] for s in syms if s)
    hits = names & set(want)
    for w in hits:
        cls = w[4:-5]
        if w == "??_7NiRefObject@@6B@":
            vt = vtable_of(body, sections, syms, "NiRefObject")
            nref += 1
            if vt is None or len(vt["slots"]) != 1:
                print("MEMBER %s: NiRefObject vtable slots=%s (OCZEKIWANO 1!)" % (name, len(vt["slots"]) if vt else None))
            continue
        if w in done:
            continue
        done.add(w)
        report("LIB member %s" % name, body, [cls])
print("NiRefObject: members z vtable = %d, kazdy z 1 slotem (brak ostrzezen = OK): %s" % (nref, ",".join(nref_members)))

print("")
print("=== GB12 .obj (VS2022 rebuild) ===")
for cls in ["NiObject", "NiObjectNET", "NiAVObject", "NiNode"]:
    p = r"D:\gamebyroengine\extracted\gb12_build\build\NiMain\%s.obj" % cls
    with open(p, "rb") as f:
        report("OBJ %s.obj" % cls, f.read(), [cls])
print("=== GB12 NiRefObject.obj (vtable symbol oczekiwany: NOT EMITTED) ===")
with open(r"D:\gamebyroengine\extracted\gb12_build\build\NiMain\NiRefObject.obj", "rb") as f:
    r = coff_symbols(f.read())
    if r:
        names = [s[0] for s in r[1] if s]
        print("NiRefObject.obj zawiera ??_7NiRefObject@@6B@:", "??_7NiRefObject@@6B@" in names)

