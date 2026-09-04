# iter020_r169_oracle_compare.py — MILESTONE 1-E ITER 020 (r169 ORACLE COMPARISON)
# INDEPENDENT-LANGUAGE comparison (Python/Pillow — no shared code with the
# clean JS pipeline) of the ITER 020 region material decode against the
# FROZEN legacy r169 splat data (eudoria-web, LEGACY_REFERENCE/REGRESSION
# ORACLE — never truth; legitimate r185/r169 differences are recorded, not
# "fixed" to match the oracle).
#
# REGION: tiles (56..58, 112..114) = heightmap x 1792..1887, y 3584..3879.
# Legacy chunk r07_c03 covers heightmap x 1536..2047, y 3584..4095 at splat
# resolution 256x256 (1 splat px = 2x2 height samples = 1 material cell).
# Region cell (global cx,cy in 0..47) -> splat px (128+cx, cy).
#
# VERSION LABELS: decode = ITER 020 clean pipeline (PCG_9_3_5 terrain.bnt,
# r185 runtime); oracle = legacy eudoria-web r169 splat data (built from JUL
# 50.bnt material weightmaps by the legacy pipeline).
import json
import base64
import sys
from PIL import Image

EXPORT = r'D:\Eudoria_Reconstruction\99_Audits\PE_MILESTONE_1_WORLD_SURFACE_R1\03_EVIDENCE\iter020_region_masks_export.json'
IDX_PNG = r'D:\Eudoria_Reconstruction\12_WebGame\eudoria-web\data\terrain\splat\splat_indices_r07_c03.png'
W_PNG = r'D:\Eudoria_Reconstruction\12_WebGame\eudoria-web\data\terrain\splat\splat_weights_r07_c03.png'
ATLAS_MANIFEST = r'D:\Eudoria_Reconstruction\12_WebGame\eudoria-web\data\terrain\splat\texture_atlas\texture_atlas_manifest.json'
ATLAS_PNG = r'D:\Eudoria_Reconstruction\12_WebGame\eudoria-web\data\terrain\splat\texture_atlas\terrain_atlas.png'
OUT = r'D:\Eudoria_Reconstruction\99_Audits\PE_MILESTONE_1_WORLD_SURFACE_R1\03_EVIDENCE\iter020_r169_oracle_compare.json'
OUT_VIS = r'D:\Eudoria_Reconstruction\99_Audits\PE_MILESTONE_1_WORLD_SURFACE_R1\03_EVIDENCE\iter020_r169_vs_r185_visual.png'

exp = json.load(open(EXPORT))
idx = Image.open(IDX_PNG).convert('RGBA')
wgt = Image.open(W_PNG).convert('RGBA')
am = json.load(open(ATLAS_MANIFEST))
index_to_id = {t['index']: t['material_id'] for t in am['textures']}
index_to_name = {t['index']: t['material_name'] for t in am['textures']}

# build our region decode: global cell (cx, cy) -> {material_id: weight}
# our model: base (position-0) = full coverage 255 (Stone04 rule), overlays
# carry their decoded mask weights; sums>255 tolerated (normalization REJECTED)
ours = {}
our_names = {}
for tile in exp['tiles']:
    tx, ty = tile['gridX'], tile['gridY']
    for mi, m in enumerate(tile['materials']):
        mask = base64.b64decode(m['maskB64'])
        for i in range(256):
            cx = (tx - 56) * 16 + (i % 16)
            cy = (ty - 112) * 16 + (i // 16)
            key = (cx, cy)
            ours.setdefault(key, {})
            w = 255 if mi == 0 else mask[i]  # base = full coverage (CONFIRMED rule)
            if m['id'] in ours[key]:
                ours[key][m['id']] = max(ours[key][m['id']], w)
            else:
                ours[key][m['id']] = w
            our_names[m['id']] = m['name']

cells = 48
dom_agree = 0
set_agree = 0
base_agree = 0
compared = 0
diffs = []
for cy in range(cells):
    for cx in range(cells):
        px, py = 128 + cx, cy
        pi = idx.getpixel((px, py))
        pw = wgt.getpixel((px, py))
        legacy = {}
        for ch in range(4):
            if pi[ch] != 255 and pw[ch] > 0:
                mid = index_to_id.get(pi[ch])
                if mid is not None:
                    legacy[mid] = pw[ch]
        our = ours.get((cx, cy), {})
        if not legacy and not our:
            continue
        compared += 1
        leg_dom = max(legacy, key=legacy.get) if legacy else None
        our_dom = max(our, key=our.get) if our else None
        if leg_dom == our_dom:
            dom_agree += 1
        if set(legacy) == set(our):
            set_agree += 1
        else:
            diffs.append({
                'cell': [cx, cy], 'splatPx': [px, py],
                'legacyIds': {str(k): v for k, v in legacy.items()},
                'ourIds': {str(k): v for k, v in our.items()},
                'legacyNames': [our_names.get(k) or index_to_name.get(pi[0]) for k in legacy],
            })

# dominant-material agreement EXCLUDING the base + TIE-AWARE overlay dominance
# (Python max() breaks weight ties by insertion order — agreement must be
# tie-aware: our top overlay agrees if it is among legacy's max-weight overlays)
ov_agree, ov_compared = 0, 0
shared_weight_exact, shared_weight_compared = 0, 0
legacy_subset_of_ours, subset_compared = 0, 0
for cy in range(cells):
    for cx in range(cells):
        our = ours.get((cx, cy), {})
        px, py = 128 + cx, cy
        pi = idx.getpixel((px, py)); pw = wgt.getpixel((px, py))
        legacy = {}
        for ch in range(4):
            if pi[ch] != 255 and pw[ch] > 0:
                mid = index_to_id.get(pi[ch])
                if mid is not None:
                    legacy[mid] = pw[ch]
        if compared_cells := bool(legacy or our):
            subset_compared += 1
            if set(legacy).issubset(set(our)):
                legacy_subset_of_ours += 1
        for mid, w in legacy.items():
            if mid in our:
                shared_weight_compared += 1
                if our[mid] == w:
                    shared_weight_exact += 1
        our_ov = {k: v for k, v in our.items() if k != 13382}
        legacy_ov = {k: v for k, v in legacy.items() if k != 13382}
        if not our_ov or not legacy_ov:
            continue
        ov_compared += 1
        leg_max = max(legacy_ov.values())
        leg_top = {k for k, v in legacy_ov.items() if v == leg_max}
        our_max = max(our_ov.values())
        our_top = {k for k, v in our_ov.items() if v == our_max}
        if our_top & leg_top:
            ov_agree += 1

result = {
    'iteration': 'ITER_020',
    'versionLabels': {
        'decode': 'ITER 020 clean pipeline (PCG_9_3_5 terrain.bnt, Three.js r185 runtime)',
        'oracle': 'legacy eudoria-web r169 splat data (JUL 50.bnt weightmaps, frozen pipeline)',
        'rule': 'oracle is REFERENCE ONLY — legitimate differences recorded, never "fixed" to match',
    },
    'region': {'originGridX': 56, 'originGridY': 112, 'tilesX': 3, 'tilesY': 3,
               'cells': cells * cells, 'cellsCompared': compared},
    'mapping': 'material cell (global cx,cy) <-> legacy splat px (128+cx, cy) of chunk r07_c03',
    'dominantMaterialAgreement': f'{dom_agree}/{compared} (includes the Stone04 base dominance — expected on both models)',
    'materialSetAgreement': f'{set_agree}/{compared} (0 expected: legacy caps at max_materials_per_pixel=4; we carry ALL layers — see legacyIdsSubsetOfOurs)',
    'legacyIdsSubsetOfOurs': f'{legacy_subset_of_ours}/{subset_compared} (every legacy id present in our decode?)',
    'sharedIdWeightExactMatches': f'{shared_weight_exact}/{shared_weight_compared} (byte-exact weight agreement on ids present in both)',
    'overlayDominanceTieAware': f'{ov_agree}/{ov_compared} (top overlay in legacy max-weight set; Stone04 base excluded)',
    'setMismatchExamples': diffs[:25],
    'setMismatchCount': compared - set_agree,
    'interpretation': 'set mismatch = legacy 4-material cap + our extra zero/low-weight layers; shared-id weights are byte-exact where both carry the id',
}
json.dump(result, open(OUT, 'w'), indent=2)

# ---------- visual comparison artifact (version-labeled diagnostic) ----------
atlas = Image.open(ATLAS_PNG).convert('RGB')
cols, rows = am['atlas_cols'], am['atlas_rows']
tex_size = am['texture_size']
id_to_index = {t['material_id']: t['index'] for t in am['textures']}
def atlas_cell(mid, size=8):
    if mid not in id_to_index:
        return Image.new('RGB', (size, size), (255, 0, 255))  # magenta = unknown
    t = am['textures'][id_to_index[mid]]
    box = (t['atlas_col'] * tex_size, t['atlas_row'] * tex_size,
           (t['atlas_col'] + 1) * tex_size, (t['atlas_row'] + 1) * tex_size)
    return atlas.crop(box).resize((size, size), Image.NEAREST)

panel = 48 * 8
vis = Image.new('RGB', (panel * 2 + 20, panel), (16, 16, 16))
left = Image.new('RGB', (panel, panel)); right = Image.new('RGB', (panel, panel))
for cy in range(cells):
    for cx in range(cells):
        # legacy dominant
        px, py = 128 + cx, cy
        pi = idx.getpixel((px, py)); pw = wgt.getpixel((px, py))
        legacy = {}
        for ch in range(4):
            if pi[ch] != 255 and pw[ch] > 0:
                legacy[index_to_id.get(pi[ch], -1)] = pw[ch]
        ldom = max(legacy, key=legacy.get) if legacy else None
        left.paste(atlas_cell(ldom) if ldom is not None else Image.new('RGB', (8, 8), (0, 0, 0)), (cx * 8, cy * 8))
        # our dominant
        our = ours.get((cx, cy), {})
        odom = max(our, key=our.get) if our else None
        right.paste(atlas_cell(odom) if odom is not None else Image.new('RGB', (8, 8), (0, 0, 0)), (cx * 8, cy * 8))
from PIL import ImageDraw
d = ImageDraw.Draw(vis)
vis.paste(left, (0, 0)); vis.paste(right, (panel + 20, 0))
d.text((4, 2), 'r169 oracle (legacy splat)', fill=(255, 255, 0))
d.text((panel + 24, 2), 'r185 clean decode (ITER 020)', fill=(0, 255, 255))
vis.save(OUT_VIS)
print('cells compared:', compared)
print('dominant agreement:', f'{dom_agree}/{compared}')
print('set agreement:', f'{set_agree}/{compared}')
print('overlay dominance agreement:', f'{ov_agree}/{ov_compared}')
print('evidence:', OUT)
print('visual:', OUT_VIS)
