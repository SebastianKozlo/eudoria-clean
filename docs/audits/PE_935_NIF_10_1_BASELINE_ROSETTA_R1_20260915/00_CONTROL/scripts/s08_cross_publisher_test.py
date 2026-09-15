"""s08_cross_publisher_test.py — run the FROZEN world-slice decoder on
non-MindArk 10.1.0.0 files (EE2 samples + Gamebryo 1.1.2 SDK samples).

Contract §14: game-specific samples usable only after byte-verified version.
All files here verified 10.1.0.0 by header (s02-class logic).

If the SAME frozen decoder achieves full-file closure on EE2/SDK files, the
Entropia world-slice layouts == the standard Gamebryo 10.1 layouts (same
writer family), strengthening STANDARD_10_1_* classifications.
"""
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from s06_world_slice_validator import (  # noqa: E402
    WorldSliceValidator, ArkBlockError)
from s04_nifxml_baseline import Unresolved  # noqa: E402

SAMPLES = [
    r'D:\Eudoria_Reconstruction\04_External_References\reference_only'
    r'\blender_niftools\todo\old_nifs\ee2\lodtest.nif',
    r'D:\Eudoria_Reconstruction\04_External_References\reference_only'
    r'\blender_niftools\todo\old_nifs\ee2\lodtest-skinned.nif',
    r'D:\gamebyroengine\extracted\gb112_known_good\BABYLENGUIN.NIF',
    r'D:\gamebyroengine\extracted\gb112_known_good\DESTROYERBOT.NIF',
    r'D:\gamebyroengine\extracted\gb112_known_good\ROCKY.NIF',
]

SUPPORTED = set('''NiNode NiTriShape NiTriShapeData NiTexturingProperty
NiMaterialProperty NiAlphaProperty NiZBufferProperty NiStencilProperty
NiVertexColorProperty NiSpecularProperty NiShadeProperty NiDitherProperty
NiFogProperty NiSourceTexture NiPixelData NiTextureEffect NiPointLight
NiSpotLight NiDirectionalLight NiAmbientLight NiStringExtraData
NiIntegerExtraData NiBooleanExtraData NiArkAnimationExtraData
NiArkImporterExtraData NiArkTextureExtraData NiArkViewportInfoExtraData
NiArkShaderExtraData NiCollisionData NiSortAdjustNode NiBillboardNode
NiArkBillboardNode'''.split())


def read_header_types(data):
    nl = data.index(b'\x0A')
    hs = data[:nl].decode('ascii', 'replace')
    pos = nl + 1
    ver, = struct.unpack('<I', data[pos:pos + 4])
    pos += 4
    if ver != 0x0A010000:
        return hs, ver, None, None, None
    uv, = struct.unpack('<I', data[pos:pos + 4])
    pos += 4
    nb, = struct.unpack('<I', data[pos:pos + 4])
    pos += 4
    nbt, = struct.unpack('<H', data[pos:pos + 2])
    pos += 2
    names = []
    for _ in range(nbt):
        ln, = struct.unpack('<I', data[pos:pos + 4])
        pos += 4
        names.append(data[pos:pos + ln].decode('ascii'))
        pos += ln
    return hs, ver, nb, names, None


def sequential_decode(v, data):
    """Decode a standard-types-only 10.1 file WITHOUT the Ark search:
    header + GroupID+block xN + TopObjects + EOF-exact. This tests the
    FROZEN schema layouts (the hypothesis) on non-MindArk files."""
    cur = Cursor_ = None
    from s06_world_slice_validator import Cursor
    cur = Cursor(data)
    hdr = v.parse_header(cur)
    blocks = []
    for i in range(hdr['num_blocks']):
        tname = hdr['types'][hdr['idx'][i]]
        start = cur.pos
        gid = cur.u32()
        if gid != 0:
            raise ValueError(f'block {i} GroupID={gid}')
        if tname not in v.dec.s.objects:
            raise ValueError(f'unsupported type {tname}')
        blk = v.dec.decode_block(cur, tname)
        blk['__type__'] = tname
        blk['__start__'] = start
        blocks.append(blk)
    ntop = cur.u32()
    tops = [cur.i32() for _ in range(ntop)]
    eof_ok = cur.pos == len(data)
    return {'blocks': blocks, 'tops': tops, 'eof_ok': eof_ok,
            'num_blocks': hdr['num_blocks']}


def main():
    v = WorldSliceValidator()
    out = []
    for path in SAMPLES:
        if not os.path.exists(path):
            out.append({'file': path, 'status': 'MISSING'})
            continue
        data = open(path, 'rb').read()
        hs, ver, nb, names, _ = read_header_types(data)
        if ver != 0x0A010000:
            out.append({'file': os.path.basename(path), 'status':
                        f'NOT_10_1({ver:08X})'})
            continue
        unsupported = [t for t in names if t not in SUPPORTED]
        try:
            res = sequential_decode(v, data)
            out.append({'file': os.path.basename(path),
                        'types': names, 'unsupported_types': unsupported,
                        'status': ('CLOSURE_OK' if res['eof_ok'] else
                                   'EOF_MISMATCH'),
                        'blocks': res['num_blocks'],
                        'tops': len(res['tops'])})
        except (Unresolved, struct.error, ValueError, TypeError,
                IndexError) as ex:
            out.append({'file': os.path.basename(path),
                        'types': names, 'unsupported_types': unsupported,
                        'status': f'FAIL:{str(ex)[:100]}'})
    for r in out:
        print(json.dumps(r))
    with open(r'D:\Eudoria_Reconstruction\99_Audits'
              r'\PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915\02_WORK'
              r'\CROSS_PUBLISHER_TEST.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=1)


if __name__ == '__main__':
    main()
