#!/usr/bin/env python3
# rawscan.py — ERRATA G2: niezależny generator odtwarzający RAWSCAN_CORRECT_HITS.json
# runu R1 CO DO OFFSETÓW (zbiory (plik, offset) identyczne).
#
# Zakres: WSZYSTKIE pliki pcg_install\Data (1,818 plików, 2,384,417,861 B — census
# zweryfikowany w ERRATA). Wzorce:
#   u32LE: 296445, 296446, 126740, 126741, 278453, 278454
#   ASCII : "296445" oraz "B_Eu_Slum_Building" (ten drugi dla pełnej równości
#           artefaktu R1 — R1 zawiera tę serię; zakres kontraktu pokrywa serię
#           u32 + ASCII 296445, seria B_Eu_Slum_Building dodana dla reprodukcji 1:1)
#
# DYSCYPLINA WZORCA (nauczka z retrakcji §7 runu R1): każdy wzorzec binarny jest
# budowany przez struct.pack z ASECJĄ konwersji odwrotnej PRZED użyciem.
#
# BRAMKA G2 (assert w skrypcie): wygenerowane zbiory (plik, offset) == RAWSCAN_CORRECT_HITS.json
# runu R1, per seria wzorca, dokładnie.
import os, struct, json, hashlib

DATA = r"D:\Eudoria_Reconstruction\pcg_install\Data"
R1 = r"D:\Eudoria_Reconstruction\09_Research\PE_296445_NIF_ORIGIN_PLACEMENT_R1_20260912"
ERR = r"D:\Eudoria_Reconstruction\09_Research\PE_296445_NIF_ORIGIN_PLACEMENT_R1_ERRATA_R1_20260912"

# --- budowa wzorców z asercją konwersji odwrotnej PRZED użyciem ---
# KLUCZE WEWNETRZNE ROZŁĄCZNE ("u32:xxx"/"ascii:xxx") — pary <u32 id> i <ASCII id>
# muszą być skanowane NIEZALEŻNIE (nauczka: scalenie {**u32, **ascii} nadpisuje
# wzorzec u32LE bajtami ASCII dla tych samych kluczy — złapane przez bramkę G2).
U32_IDS = [296445, 296446, 126740, 126741, 278453, 278454]
scan_patterns = {}
for i in U32_IDS:
    p = struct.pack("<I", i)
    assert struct.unpack("<I", p)[0] == i, f"reverse-conversion assertion FAILED for {i}"
    scan_patterns[f"u32:{i}"] = p
for k in ["296445", "B_Eu_Slum_Building"]:
    p = k.encode("ascii")
    assert p.decode("ascii") == k, f"reverse-conversion assertion FAILED for ascii {k}"
    scan_patterns[f"ascii:{k}"] = p

CHUNK = 1 << 22  # 4 MiB
OVERLAP = 64     # > max(len(pattern)) - 1, bezpieczny margines

def scan_file(path, patterns):
    """Zwraca dict pattern_key -> [(offset,)] dla pliku; skan chunkowy z zakładką."""
    out = {k: [] for k in patterns}
    size = os.path.getsize(path)
    base = 0
    tail = b""
    with open(path, "rb") as f:
        while True:
            chunk = f.read(CHUNK)
            if not chunk:
                break
            buf = tail + chunk if tail else chunk
            start_of_buf = base - len(tail)
            for k, p in patterns.items():
                pos = buf.find(p)
                while pos != -1:
                    off = start_of_buf + pos
                    # wyklucz duplikaty z zakładki: trafienie musi zaczynać się w bieżącym chunku
                    if off not in out[k] and off >= base - (len(tail) if base > 0 else 0):
                        if not out[k] or out[k][-1] != off:
                            out[k].append(off)
                    pos = buf.find(p, pos + 1)
            # zachowaj zakładkę; trafienia w zakładce zostaną ponownie znalezione — dedup po sortowaniu
            tail = buf[-(OVERLAP):] if len(buf) > OVERLAP else b""
            base += len(chunk)
    return out

def dedup_sort(hits):
    # deduplikacja po (file, offset) — zakładka chunkowa może teoretycznie powielić trafienie
    for k in list(hits.keys()):
        seen = set(); lst = []
        for e in hits[k]:
            key = (e["file"], e["offset"])
            if key not in seen:
                seen.add(key); lst.append(e)
        hits[k] = lst
    return hits

# --- skan całego korpusu ---
u32_hits = {str(i): [] for i in U32_IDS}
ascii_hits = {"296445": [], "B_Eu_Slum_Building": []}
nfiles = 0; total_bytes = 0
for dp, dn, fns in os.walk(DATA):
    for fn in sorted(fns):
        p = os.path.join(dp, fn)
        rel = os.path.relpath(p, DATA)  # Windows: backslash — zgodnie z formatem R1
        nfiles += 1; total_bytes += os.path.getsize(p)
        fh = scan_file(p, scan_patterns)
        for k, offs in fh.items():
            if not offs:
                continue
            kind, _, name = k.partition(":")
            target = u32_hits if kind == "u32" else ascii_hits
            for off in offs:
                target[name].append({"file": rel, "offset": off})

u32_hits = dedup_sort(u32_hits)
ascii_hits = dedup_sort(ascii_hits)
repro = {"u32": u32_hits, "ascii": ascii_hits}

# --- porównanie z RAWSCAN_CORRECT_HITS.json R1 ---
r1 = json.load(open(os.path.join(R1, "03_SEARCH", "RAWSCAN_CORRECT_HITS.json")))

def series_set(d, key):
    return set((e["file"], e["offset"]) for e in d.get(key, []))

gate_results = {}
overall = True
for series in sorted(set(list(r1["u32"].keys()) + list(repro["u32"].keys()))):
    a = series_set(r1["u32"], series); b = series_set(repro["u32"], series)
    ok = a == b
    overall &= ok
    gate_results[f"u32:{series}"] = {"identical": ok, "r1_count": len(a), "repro_count": len(b),
                                     "missing_in_repro": sorted(a - b), "extra_in_repro": sorted(b - a)}
for series in sorted(set(list(r1["ascii"].keys()) + list(repro["ascii"].keys()))):
    a = series_set(r1["ascii"], series); b = series_set(repro["ascii"], series)
    ok = a == b
    overall &= ok
    gate_results[f"ascii:{series}"] = {"identical": ok, "r1_count": len(a), "repro_count": len(b),
                                       "missing_in_repro": sorted(a - b), "extra_in_repro": sorted(b - a)}

assert overall, f"G2 FAIL: {json.dumps(gate_results, indent=1)}"

# --- zapis ---
json.dump(repro, open(os.path.join(ERR, "02_EVIDENCE", "RAWSCAN_REPRO.json"), "w"), indent=1)
gate = {
    "G2_rawscan_reproduction": "PASS — zbiory (plik, offset) identyczne per seria",
    "scanned_files": nfiles, "scanned_bytes": total_bytes,
    "patterns_u32le": sorted(str(i) for i in U32_IDS),
    "patterns_ascii": ["296445", "B_Eu_Slum_Building"],
    "pattern_discipline": "struct.pack('<I') + asercja struct.unpack przed użyciem (nauczka §7 R1)",
    "series": gate_results,
}
json.dump(gate, open(os.path.join(ERR, "02_EVIDENCE", "G2_GATE_RESULTS.json"), "w"), indent=1)
print(f"G2 PASS: {nfiles} files, {total_bytes} bytes scanned")
for k, v in gate_results.items():
    print(f"  {k}: identical={v['identical']} count={v['r1_count']}")
