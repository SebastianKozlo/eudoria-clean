# qc_b8_portals.py — WLASNY parse Portals.bnt (QC B8): indeks + payloady + 13 anchorow
# Audytor QC: PE_935_ROUND_QC_STATIC_PLACEMENT_R1_20260913. READ-ONLY na Portals.bnt.
import struct, statistics, glob
from collections import Counter

PRT_PATH = r'D:\Eudoria_Reconstruction\pcg_install\Data\Portals\Portals.bnt'
data = open(PRT_PATH, 'rb').read()
print('Portals.bnt:', PRT_PATH)
print('rozmiar pliku:', len(data))

index_start, = struct.unpack('<I', data[-8:-4])
magic = data[-4:]
print('stopka: index_start=%d magic=%r' % (index_start, magic))
assert magic == b'BNT2', 'zla stopka!'

# Naglowek licznika wpisow (QC P2-2): @index_start stoi u32 = liczba wpisow (0x114 = 276);
# wpisy zaczynaja sie @index_start+4. Parse bez naglowka wchlania licznik w nazwe 1. wpisu.
cnt_header, = struct.unpack_from('<I', data, index_start)
print('naglowek licznika @%d = %d (0x%X)' % (index_start, cnt_header, cnt_header))
assert cnt_header == 276

i = index_start + 4
entries = []
while i < len(data) - 8:
    nl = data.find(b'\n', i)
    if nl < 0: break
    name = data[i:nl].decode('ascii', 'replace')
    i = nl + 1
    size, offset = struct.unpack_from('<II', data, i)
    i += 8
    aux = struct.unpack_from('<q', data, i)[0]
    i += 8
    entries.append(dict(name=name, size=size, offset=offset, aux=aux))

print('liczba wpisow w indeksie:', len(entries))
prts = [e for e in entries if e['name'].endswith('.prt')]
print('wpisy .prt: %d ; non-.prt: %d' % (len(prts), len(entries) - len(prts)))
sizes = [e['size'] for e in prts]
print('rozmiary: min=%d mediana=%s max=%d' % (min(sizes), statistics.median(sizes), max(sizes)))
viol = [e for e in entries if e['offset'] + e['size'] > index_start]
print('naruszenia granic (offset+size>index_start): %d' % len(viol))
ids = [int(e['name'].split('.')[0]) for e in prts if e['name'].split('.')[0].isdigit()]
print('liczba id z nazw: %d ; unikalnych: %d' % (len(ids), len(set(ids))))
cnt = Counter(ids)
dups = {k: v for k, v in cnt.items() if v > 1}
print('zduplikowane id:', dups)
print('id-range: %d..%d' % (min(ids), max(ids)))
window = sorted(id for id in ids if 505000 <= id <= 510000)
print('wpisy w oknie 505000-510000: %d -> %s' % (len(window), window))
for o in (382811, 422806, 592739, 592741):
    print('  outlier %d istnieje: %s' % (o, any(e['name'] == str(o) + '.prt' for e in entries)))

anchors = {
    'template_4508': struct.pack('<I', 4508),
    'template_4752': struct.pack('<I', 4752),
    'template_2249': struct.pack('<I', 2249),
    'nif_A_296445': struct.pack('<I', 296445),
    'nif_A_126740': struct.pack('<I', 126740),
    'nif_A_278453': struct.pack('<I', 278453),
    'bvi_B_296446': struct.pack('<I', 296446),
    'paramset_20005': struct.pack('<I', 20005),
    'paramset_20006': struct.pack('<I', 20006),
    'paramset_20007': struct.pack('<I', 20007),
    'msgtype_0xB9': struct.pack('<I', 0xB9),
    'attr_0x6A4': struct.pack('<I', 0x6A4),
    'attr_0x6A8': struct.pack('<I', 0x6A8),
}
hits = {k: [] for k in anchors}
total_payload_bytes = 0
for e in prts:
    payload = data[e['offset']:e['offset'] + e['size']]
    total_payload_bytes += len(payload)
    for k, pat in anchors.items():
        idx = payload.find(pat)
        if idx >= 0:
            hits[k].append((e['name'], idx))
print()
print('total .prt bytes: %d' % total_payload_bytes)
print('=== ANCHORY (surowy skan bajtowy, wszystkie offsety) ===')
for k in anchors:
    print('  %-16s: %d trafien %s' % (k, len(hits[k]), hits[k][:4]))

allvals = set()
in_range = []
for e in prts:
    payload = data[e['offset']:e['offset'] + e['size']]
    for off in range(0, len(payload) - 3, 4):
        v = struct.unpack_from('<I', payload, off)[0]
        allvals.add(v)
        if 100000 <= v <= 460000:
            in_range.append(v)
print()
print('unikalne u32 (aligned 4B grid): %d' % len(allvals))
print('u32 w zakresie 100k-460k: %d ; przyklady: %s' % (len(in_range), sorted(set(in_range))[:12]))

print()
e382 = next(e for e in entries if e['name'] == '382811.prt')
p = data[e382['offset']:e382['offset'] + e382['size']]
print('=== probka 382811.prt (%d B) — pierwsze 96 B ===' % len(p))
for i in range(0, min(96, len(p)), 16):
    print('  %04x: %s' % (i, ' '.join('%02x' % x for x in p[i:i+16])))
print('  f32 od offsetu 8: ', [round(struct.unpack_from('<f', p, o)[0], 5) for o in range(8, 8+24, 4)])
print('  tag=%02x u16@1=%04x (claim: 0x0101) u32@4=%08x' % (p[0], struct.unpack_from('<H', p, 1)[0], struct.unpack_from('<I', p, 4)[0]))
