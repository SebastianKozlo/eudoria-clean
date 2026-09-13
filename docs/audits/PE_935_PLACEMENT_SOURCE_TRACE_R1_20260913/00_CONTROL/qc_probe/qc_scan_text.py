# qc_scan_text.py — niezalezne skany .text/.rdata (RUN A: A2, A5, A10)
import sys, os, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qc_pe import load
pe = load()

text, tsec = pe.section_bytes('.text')
text_va = pe.image_base + tsec['vaddr']
print('.text: VA 0x%08X, rozmiar 0x%X' % (text_va, len(text)))

def scan(pattern, name, results_limit=20):
    hits = []
    start = 0
    while True:
        i = text.find(pattern, start)
        if i < 0: break
        hits.append(text_va + i)
        start = i + 1
        if len(hits) > 5000: break
    print('%s: %d trafien w .text' % (name, len(hits)))
    for h in hits[:results_limit]:
        print('   0x%08X' % h)
    return hits

# A5: wzorce 4508 LE (9c 11 00 00 = 0x119C? NIE! 4508 = 0x11 0x9C? 4508 dec = 0x119C!
# 4508 = 0x119C. LE bytes: 9c 11 00 00. BE: 00 00 11 9c. 296445 = 0x4859D -> LE: 5d 85 04 00.
scan(bytes.fromhex('9c110000'), '4508 LE (9c 11 00 00)')
scan(bytes.fromhex('0000119c'), '4508 BE (00 00 11 9c)')
scan(bytes.fromhex('5d850400'), '296445 LE (5d 85 04 00)')
# kontrola: 0x119C jako disp32 w LEA ECX,[ESP+0x119C] tez = 9c 11 00 00
# A2: string CharacterPosition w calym pliku
data = pe.data
def find_str_all(s, whole_file=True):
    b = s.encode('ascii') + b'\x00'
    hits = []
    start = 0
    while True:
        i = data.find(b, start)
        if i < 0: break
        # VA z offsetu
        va = None
        for s_ in pe.sections:
            if s_['rawptr'] <= i < s_['rawptr'] + s_['rawsize']:
                va = pe.image_base + s_['vaddr'] + (i - s_['rawptr'])
                break
        hits.append((i, va))
        start = i + 1
    return hits

for s in ['CharacterPosition', 'ArkPortalCell', 'Sectors.xbc', 'Objects.pak', 'Planets.pak',
          'ArkSector', 'ArkRegion', 'ArkEntity', 'm_localTranslate', 'm_worldTranslate',
          'm_kWorldBound', 'm_bAppCulled', 'm_localRotate', 'm_worldRotate',
          'NetImmerseScene::Root', 'ArkVegetationClient::GetModel', 'm_ContainsPortals',
          'm_ContainsPortalDefinitions', 'portals.bnt', 'TerrainEditZones.bnt']:
    hits = find_str_all(s)
    print('STRING %-34s : %d trafien' % (repr(s), len(hits)))
    for off, va in hits[:6]:
        print('     off %d -> VA %s' % (off, ('0x%08X' % va) if va else '(poza sekcjami raw)'))

# A10: substring 'Sector' i 'Region' i 'Entity' (jako substringy) w .rdata
rdata, rsec = pe.section_bytes('.rdata')
rdata_va = pe.image_base + rsec['vaddr']
def substr_in_rdata(s):
    out = []
    b = s.encode('ascii')
    start = 0
    while True:
        i = rdata.find(b, start)
        if i < 0: break
        # srodowisko stringowe: poprzednie i nastepne 60 bajtow
        ctx = rdata[max(0,i-40):i+60]
        out.append((rdata_va + i, ctx))
        start = i + 1
        if len(out) > 30: break
    return out

for s in ['Sector', 'Region', 'Entity']:
    res = substr_in_rdata(s)
    print('SUBSTR %-10s w .rdata: %d trafien (limit 30)' % (s, len(res)))
    for va, ctx in res:
        txt = ''.join(chr(x) if 32 <= x < 127 else '.' for x in ctx)
        print('   0x%08X  %s' % (va, txt))

# caly plik: 'Sectors.xbc' itp.
print()
print('=== RTTI: klasa .?AV (type descriptors) zawierajace Sector/Region/Entity ===')
td_pat = b'.?AV'
i = 0
tds = []
while True:
    i = data.find(td_pat, i)
    if i < 0: break
    end = data.find(b'\x00', i)
    if end < 0 or end - i > 200: end = i + 200
    name = data[i:end].decode('ascii', 'replace')
    if any(k in name for k in ['Sector', 'Region', 'Entity']):
        tds.append(name)
    i += 1
print('TD z Sector/Region/Entity:', len(tds))
for t in tds[:40]:
    print('   ', t)
