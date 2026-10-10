"""PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009 - Work Package B.

Six synthetic NIF 10.1.0.0 graph controls loaded by the ORIGINAL Gamebryo SDK
SceneGraphPrinter (headless).

LINEAGE DISCLOSURE - THIS IS REUSED CODE, NOT AN INDEPENDENT IMPLEMENTATION:
Adapted copy of the Desktop script
  C:\\Users\\User\\Documents\\ChatGPT\\PE\\PE_GAMEBRYO_PLACEMENT_MECHANISMS_LOCAL_RESEARCH_20261009\\native_transform_probe.py
  (5945 B, SHA256 b003e3c4c49d16da534de8a230cbe7585086016e8bd2dcba7b1bff2d41db107b,
   identity re-verified in this run's INPUT_IDENTITIES.json).
Adaptations by this run (serialization logic intentionally kept byte-identical
to the validated Desktop generator so results stay comparable):
  1. Fixtures written to LOCAL_ONLY_ROOT\\01_SDK_fixtures\\synthetic\\ (own
     synthetic content; kept out of the repo package, referenced by path+SHA).
  2. Raw stdout/stderr -> <repo package>\\01_SDK\\raw\\; results ->
     <repo package>\\01_SDK\\synthetic_control_details_internal.json.
  3. Per-run provenance recorded (argv, cwd, child env delta, timeout).
  4. EXPECTED values are the ones THIS RUN preregistered in
     01_SDK\\PREREGISTRATION_SDK_PHASE.md, derived by this executor from the
     SDK transform-composition source (NiTransform.inl:15-24,
     NiAVObject_Win32.cpp:22-31), with derivations recorded per case.
  5. Camera visit block additionally parsed for the LOCAL Translate (-trans,
     local getter) so local-vs-world is measured, not assumed.
  6. Registered traversal prediction for TWO_PARENTS_LAST_LINK_WINS: 4 visits.
  7. Tool identity verified before and after all runs.

NiCamera is an observation probe ONLY: NiCamera::UpdateWorldBound sets the
world-bound CENTER to the world TRANSLATION (NiCamera.cpp:267-270). That
equivalence is a property of NiCamera in this SDK and is NOT generalized to
arbitrary geometry. TWO_PARENTS_LAST_LINK_WINS is a deliberately conflicting
graph diagnostic, not a valid authoring recommendation.

No PE assets, no client, no GUI, no SDK-original writes.
"""
import ctypes
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess

GB = Path(r'D:\gamebyroengine\extracted\Gb12_Source')
EXE = GB / 'Tools/DeveloperTools/SceneGraphPrinter/Win32/VC71/SceneGraphPrinter.exe'
RUNTIME = Path(r'D:\gamebyroengine\extracted\Gb112_tools_setup')
OUT_ROOT = Path(r'D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits'
                r'\PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009')
SDK_OUT = OUT_ROOT / '01_SDK'
RAW = SDK_OUT / 'raw'
LOCAL = Path(r'D:\Eudoria_Reconstruction\99_Audits'
             r'\PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009'
             r'\01_SDK_fixtures\synthetic')
LOCAL.mkdir(parents=True, exist_ok=True)
TIMEOUT_S = 30
IDENTITY = [1, 0, 0, 0, 1, 0, 0, 0, 1]
RZ90 = [0, -1, 0, 1, 0, 0, 0, 0, 1]
NULL = 0xffffffff


def identity(p):
    b = p.read_bytes()
    return {'path': str(p), 'size_bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def u32(*v):
    return struct.pack('<' + 'I' * len(v), *v)


def f32(*v):
    return struct.pack('<' + 'f' * len(v), *v)


def string(s):
    b = s.encode('ascii')
    return u32(len(b)) + b


def av(name, t, r, s):
    # Group ID, NiObjectNET fields, then NiAVObject; no extras/controllers/properties.
    return (u32(0) + string(name) + u32(0, NULL) + struct.pack('<H', 0) +
            f32(*t) + f32(*r) + f32(s) + u32(0, NULL))


def node(name, t=(0, 0, 0), r=IDENTITY, s=1, children=()):
    return {'type': 'NiNode', 'name': name, 'translation': list(t), 'rotation': list(r),
            'scale': s, 'children': list(children)}


def camera(name='Probe', t=(1, 2, 3), s=1):
    return {'type': 'NiCamera', 'name': name, 'translation': list(t), 'rotation': IDENTITY,
            'scale': s}


def serialize(objects):
    types = ['NiNode', 'NiCamera']
    b = (b'Gamebryo File Format, Version 10.1.0.0\n' + u32(0x0a010000, 0, len(objects)) +
         struct.pack('<H', len(types)) + b''.join(string(t) for t in types) +
         b''.join(struct.pack('<H', types.index(o['type'])) for o in objects) + u32(0))
    offsets = []
    for o in objects:
        offsets.append(len(b))
        b += av(o['name'], o['translation'], o['rotation'], o['scale'])
        if o['type'] == 'NiNode':
            b += u32(len(o['children']), *o['children']) + u32(0)
        else:
            b += (struct.pack('<H', 0) + f32(-.5, .5, .5, -.5, 1, 100) + b'\x00' +
                  f32(0, 1, 1, 0, 1) + u32(NULL, 0, 0))
    return b + u32(1, 0), offsets


# Expected values PREREGISTERED in 01_SDK/PREREGISTRATION_SDK_PHASE.md section 3
# (derived by this executor from NiTransform composition source; consistent with
# the pinned Desktop report used as comparison input).
cases = [
    {'case': 'IDENTITY_PARENT',
     'objects': [node('Root', children=[1]), camera()],
     'expected': [1, 2, 3],
     'derivation': 'world = I * (1,2,3); T = 0 + 1*(I*(1,2,3))',
     'expected_visits': 2},
    {'case': 'TRANSLATED_PARENT',
     'objects': [node('Root', t=(100, 200, 300), children=[1]), camera()],
     'expected': [101, 202, 303],
     'derivation': 'T = (100,200,300) + 1*(I*(1,2,3))',
     'expected_visits': 2},
    {'case': 'ROTATED_SCALED_PARENT',
     'objects': [node('Root', t=(100, 200, 300), r=RZ90, s=2, children=[1]), camera()],
     'expected': [96, 202, 306],
     'derivation': 'T = (100,200,300) + 2*(Rz90*(1,2,3)) = (100,200,300)+2*(-2,1,3)',
     'expected_visits': 2},
    {'case': 'THREE_LEVEL_SOCKET',
     'objects': [node('WorldRoot', t=(100, 200, 300), r=RZ90, s=2, children=[1]),
                 node('Socket', t=(10, 20, 30), s=.5, children=[2]), camera()],
     'expected': [58, 221, 363],
     'derivation': 'Socket world T=(100,200,300)+2*(Rz90*(10,20,30))=(60,220,360); '
                   'Probe T=(60,220,360)+1*(Rz90*(1,2,3))=(58,221,363)',
     'expected_visits': 3},
    {'case': 'LEAF_SCALE_SEPARATE',
     'objects': [node('Root', t=(100, 200, 300), children=[1]), camera(s=9)],
     'expected': [101, 202, 303],
     'derivation': 'leaf scale s=9 does not enter its own translate composition: '
                   'T = (100,200,300)+1*(I*(1,2,3))',
     'expected_visits': 2},
    {'case': 'TWO_PARENTS_LAST_LINK_WINS',
     'objects': [node('Root', children=[1, 2]),
                 node('ParentA', t=(100, 0, 0), children=[3]),
                 node('ParentB', t=(0, 200, 0), children=[3]), camera()],
     'expected': [1, 202, 3],
     'derivation': 'second AttachChild detaches the camera from ParentA '
                   '(NiAVObject::AttachParent, NiAVObject.cpp:62-69) -> parent=ParentB: '
                   'T = (0,200,0)+1*(I*(1,2,3))',
     'expected_visits': 4,
     'special': 'Deliberate conflicting-parent DIAGNOSTIC, not a valid authoring pattern.'},
]

before = identity(EXE)
env = os.environ.copy()
env['PATH'] = str(RUNTIME) + ';' + env.get('PATH', '')
old = ctypes.windll.kernel32.SetErrorMode(0x0001 | 0x0002 | 0x8000)
results = []
try:
    for c in cases:
        data, offsets = serialize(c['objects'])
        p = LOCAL / (c['case'] + '.nif')
        p.write_bytes(data)
        command = [str(EXE), '-in', str(p), '-trans', '-bs', '-mem']
        out = RAW / (c['case'] + '.stdout.txt')
        err = RAW / (c['case'] + '.stderr.txt')
        r = {'case': c['case'], 'command': command, 'cwd': str(LOCAL),
             'child_env_delta': {'PATH': '+' + str(RUNTIME) + ';<inherited PATH>'},
             'child_env_delta_class': 'CHILD_PROCESS_PATH_DLL_EXPOSURE',
             'timeout_s': TIMEOUT_S,
             'fixture_local_only': identity(p),
             'serialized_body_offsets': offsets,
             'expected_probe_world_translation': c['expected'],
             'expected_derivation': c['derivation'],
             'expected_visits': c['expected_visits'],
             'special': c.get('special'),
             'stdout_raw_path': str(out), 'stderr_raw_path': str(err)}
        try:
            proc = subprocess.run(command, cwd=str(LOCAL), env=env, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, timeout=TIMEOUT_S,
                                  creationflags=subprocess.CREATE_NO_WINDOW, check=False)
        except subprocess.TimeoutExpired:
            r.update(timeout=True, pass_=False, exit_code=None)
            results.append(r)
            continue
        out.write_bytes(proc.stdout)
        err.write_bytes(proc.stderr)
        text = proc.stdout.decode('cp1252', errors='replace')
        match = re.search(r'(\d+) - NiCamera:<Probe>[^\n]*\n(.*?)(?=\n\s*\d+ - |\Z)', text, re.S)
        center = re.search(r'World Bound: C <([^>]+)>', match[2]) if match else None
        local_tr = re.search(r'Translate: <([^>]+)>', match[2]) if match else None
        addr = re.search(r'<0x([0-9A-Fa-f]+)>', match[0]) if match else None
        observed = [float(x) for x in center[1].split(',')] if center else None
        visits = re.findall(r'^\s*\d+ - .*$', text, re.M)
        summary = re.search(r'Total Object Count: (\d+), Tree Depth: (\d+)', text)
        ok = (proc.returncode == 0 and observed == c['expected'])
        r.update(exit_code=proc.returncode, timeout=False,
                 observed_probe_world_translation=observed,
                 camera_local_translate_via_trans_flag=(
                     [float(x) for x in local_tr[1].split(',')] if local_tr else None),
                 camera_address=addr[1] if addr else None,
                 camera_traversal_depth=int(match[1]) if match else None,
                 visit_count=len(visits),
                 reported_summary=([int(summary.group(1)), int(summary.group(2))]
                                  if summary else None),
                 printed_hierarchy=visits,
                 stderr=proc.stderr.decode('cp1252', errors='replace'),
                 observed_visits_match_expected=(len(visits) == c['expected_visits']),
                 pass_=ok, synthetic_not_PCG=True)
        if 'special' in c:
            r['diagnostic_label'] = ('conflicting two-parent graph - DIAGNOSTIC ONLY, '
                                     'not normal authoring practice')
        results.append(r)
        if proc.returncode != 0:
            break
finally:
    ctypes.windll.kernel32.SetErrorMode(old)

after = identity(EXE)
result = {
    'run_id': 'PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009',
    'phase': 'SDK_QUALIFICATION (Work Package B)',
    'tool_identity_before': before,
    'tool_unchanged': after == before,
    'results': results,
    'passed': sum(1 for x in results if x.get('pass_')),
    'executed': len(results),
    'registered': len(cases),
    'observation_probe_scope': (
        'Only these synthetic NiCamera probes. Camera world-bound CENTER equals '
        'world TRANSLATION by NiCamera::UpdateWorldBound source identity '
        '(NiCamera.cpp:267-270); no general bound-center/position equivalence is '
        'claimed for arbitrary geometry.'),
    'flags': ['-trans', '-bs', '-mem'],
    'client_executed': False,
    'gui_executed': False,
    'pe_data_read': False,
}
(SDK_OUT / 'synthetic_control_details_internal.json').write_text(
    json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'passed': result['passed'], 'executed': len(results),
                  'tool_unchanged': result['tool_unchanged'],
                  'cases': [{k: r.get(k) for k in
                             ('case', 'exit_code', 'expected_probe_world_translation',
                              'observed_probe_world_translation',
                              'camera_local_translate_via_trans_flag',
                              'visit_count', 'observed_visits_match_expected', 'pass_')}
                            for r in results]}, indent=2))
