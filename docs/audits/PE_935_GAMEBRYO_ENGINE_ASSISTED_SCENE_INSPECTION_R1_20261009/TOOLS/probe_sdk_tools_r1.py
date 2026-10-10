"""PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009 - Work Package B.

SDK tools probe (positive controls + negative inputs + missing-file + empty scene).

LINEAGE DISCLOSURE - THIS IS REUSED CODE, NOT AN INDEPENDENT IMPLEMENTATION:
This script is an ADAPTED COPY of the Desktop script
  C:\\Users\\User\\Documents\\ChatGPT\\PE\\PE_GAMEBRYO_SCENE_TOOLS_DEEP_CHECK_20261009\\probe_tools.py
  (6551 B, SHA256 f475e0589f07576bb903af2eb8bfc5a794314dd811661b048b5dd403b600d2d6,
   identity re-verified in this run's INPUT_IDENTITIES.json).
Adaptations by this run (all other logic intentionally kept identical so results
stay comparable with the Desktop run):
  1. Output locations moved to THIS run's package:
     - raw stdout/stderr -> <repo package>\\01_SDK\\raw\\
     - result JSONs -> <repo package>\\01_SDK\\
     - mutated/negative fixtures -> LOCAL_ONLY_ROOT\\01_SDK_fixtures\\ (SDK-derived
       payload bytes stay OUT of the repo package; referenced by path+SHA only).
  2. Visit-line parser fixed to accept BOTH PrintID forms: objects print
     `:<name>` only when NiObjectNET-derived (NiSceneGraphPrinter.cpp:63-75);
     NiTimeController derives from NiObject, NOT NiObjectNET (NiTimeController.h:26),
     so controller visit lines have no `:<name>` token. (Desktop disclosed its
     first parser missed that form.)
  3. Per-run provenance recorded (argv, cwd, child env delta, timeout).
  4. Mutation records extended: original bytes AND new bytes (not just offsets).
  5. EMPTY_SCENE case added by THIS RUN (own minimal NIF 10.1.0.0 generator:
     header + version + user version + count 0 + type count 0 + group count 0 +
     top-level count 0). Desktop's empty-scene fixture lives in its frozen
     directory and is not touched.
  6. Exe/DLL/sample identities re-verified before AND after all runs.

No PE client, no PE assets, no GUI tools, no SDK-original writes.
"""
import collections
import ctypes
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import sys

GB = Path(r'D:\gamebyroengine\extracted\Gb12_Source')
TOOL = GB / 'Tools/DeveloperTools/SceneGraphPrinter/Win32/VC71/SceneGraphPrinter.exe'
RUNTIME = Path(r'D:\gamebyroengine\extracted\Gb112_tools_setup')
OUT_ROOT = Path(r'D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits'
                r'\PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009')
SDK_OUT = OUT_ROOT / '01_SDK'
RAW = SDK_OUT / 'raw'
LOCAL_ROOT = Path(r'D:\Eudoria_Reconstruction\99_Audits'
                  r'\PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009\01_SDK_fixtures')
TIMEOUT_S = 30  # preregistered per-process hang-detection timeout
FLAGS = ['-trans', '-extra', '-prop', '-geom', '-bs', '-mem']  # all flags from inspected CLI source


def ident(p):
    b = p.read_bytes()
    return {'path': str(p), 'size_bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def nif_table(b):
    """Reused from Desktop probe_tools.py: bounded own header/type-table parse.
    Only the two SDK header layouts used by the four positive controls."""
    p = b.index(b'\n') + 1
    version, user, count = struct.unpack_from('<III', b, p)
    if version not in (0x0a000112, 0x0a010000):
        raise ValueError('Outside registered SDK header layouts')
    p += 12
    ntypes, = struct.unpack_from('<H', b, p)
    p += 2
    types = []
    for _ in range(ntypes):
        n, = struct.unpack_from('<I', b, p)
        p += 4
        if n < 1 or n > 255 or p + n > len(b):
            raise ValueError('Invalid class name bounds')
        types.append({'name': b[p:p + n].decode('ascii'), 'name_offset': p, 'size': n})
        p += n
    indices = struct.unpack_from('<' + 'H' * count, b, p)
    if any(i >= ntypes for i in indices):
        raise ValueError('Invalid class indices')
    census = collections.Counter(types[i]['name'] for i in indices)
    return {'header': b[:b.index(b'\n')].decode('ascii'), 'version': version,
            'user_version': user, 'serialized_block_count': count,
            'types': types, 'block_class_census': dict(census)}


VISIT_RE = re.compile(
    r'^\s*(\d+) - ([A-Za-z0-9_]+)(?::<([^>]*)>)?(?:\s+<0x([0-9A-Fa-f]+)>)?\s*$')
ANY_NUMBERED_RE = re.compile(r'^\s*\d+ - ')


def parse_stdout(text):
    rows = []
    for line in text.splitlines():
        m = VISIT_RE.match(line)
        if m:
            rows.append({'depth': int(m.group(1)), 'class': m.group(2),
                         'name': m.group(3), 'address': m.group(4)})
    # "accounts for ALL numbered visits" check: any raw numbered line shape
    # that the strict parser missed would appear here.
    numbered_lines = [ln for ln in text.splitlines() if ANY_NUMBERED_RE.match(ln)]
    unaccounted = [ln for ln in numbered_lines if not VISIT_RE.match(ln)]
    summary = re.search(r'Total Object Count: (\d+), Tree Depth: (\d+)', text)
    uniq_addr = len({r['address'] for r in rows if r['address']})
    visits_with_addr = sum(1 for r in rows if r['address'])
    return {
        'numbered_visit_rows_parsed': len(rows),
        'numbered_lines_in_raw': len(numbered_lines),
        'numbered_lines_unaccounted': len(unaccounted),
        'unaccounted_examples': unaccounted[:5],
        'unique_printed_addresses': uniq_addr,
        'visits_without_address_token': len(rows) - visits_with_addr,
        'reported_summary': [int(summary.group(1)), int(summary.group(2))] if summary else None,
        'class_histogram': dict(collections.Counter(r['class'] for r in rows)),
        'depth_histogram': dict(sorted(collections.Counter(r['depth'] for r in rows).items())),
        'first_rows': rows[:10],
    }


samples = {
    'SDK_DESERT_TOWN': GB / 'Samples/ST_Applications/MOUT/Data/DesertTown/DT.NIF',
    'SDK_DESERT_GROUND': GB / 'Samples/ST_Applications/MOUT/Data/DesertTown/DT_Ground.NIF',
    'SDK_TUTORIAL_WORLD': GB / 'Samples/Tutorials/Data/Win32/WORLD.nif',
    'SDK_TUTORIAL_OBJECT': GB / 'Samples/Tutorials/Data/Win32/OBJECT.NIF',
}
DESKTOP_COMPARISON = {
    'SDK_DESERT_TOWN': {'visits': 388, 'unique_addresses': 388, 'depth': 6, 'blocks': 1226, 'header_version': '10.1.0.0'},
    'SDK_DESERT_GROUND': {'visits': 561, 'unique_addresses': 561, 'depth': 7, 'blocks': 977, 'header_version': '10.1.0.0'},
    'SDK_TUTORIAL_WORLD': {'visits': 131, 'unique_addresses': 130, 'depth': 7, 'blocks': 396, 'header_version': '10.0.1.18'},
    'SDK_TUTORIAL_OBJECT': {'visits': 17, 'unique_addresses': 16, 'depth': 5, 'blocks': 60, 'header_version': '10.0.1.18'},
}

tool_before = ident(TOOL)
dll_identities = [ident(RUNTIME / n) for n in ('MSVCP71.DLL', 'MSVCR71.DLL')]
sample_identities = {k: ident(p) for k, p in samples.items()}
tables = {k: nif_table(p.read_bytes()) for k, p in samples.items()}

# --- negative mutations: fresh LOCAL_ONLY copies of the SDK sample (never in-place) ---
base_name = samples['SDK_TUTORIAL_OBJECT']
b = base_name.read_bytes()
hdr_end = b.index(b'\n') + 1
node = next(t for t in tables['SDK_TUTORIAL_OBJECT']['types'] if t['name'] == 'NiNode')
unknown = bytearray(b)
unknown[node['name_offset']:node['name_offset'] + 6] = b'QzNode'
user_ver_off = hdr_end + 4  # OBJECT.NIF is 10.0.1.18 (>= 10.0.1.8): user version field present
userver = bytearray(b)
userver[user_ver_off] = 1
toonew = bytearray(b)
struct.pack_into('<I', toonew, hdr_end, 0x14020007)
badhdr = bytearray(b)
badhdr[0:hdr_end - 1] = b'X' * (hdr_end - 1)
# own minimal empty scene (this run's generator; layout per NiStream::LoadStream order)
empty = (b'Gamebryo File Format, Version 10.1.0.0\n' +
         struct.pack('<III', 0x0a010000, 0, 0) + struct.pack('<H', 0) +
         struct.pack('<I', 0) + struct.pack('<I', 0))

mutants = {
    'SYNTH_UNKNOWN_CLASS': (bytes(unknown), 'missing factory at LoadRTTI (source-predicted NO_CREATE_FUNCTION)'),
    'SYNTH_USER_VERSION_1': (bytes(userver), 'user-version gate (source-predicted LATER_VERSION, max allowed is 0)'),
    'SYNTH_TOO_NEW_BINARY_VERSION': (bytes(toonew), 'binary version gate (source-predicted LATER_VERSION, 20.2.0.7 > 10.2.0.0)'),
    'SYNTH_BAD_HEADER_TEXT': (bytes(badhdr), 'header text gate (source-predicted NOT_NIF_FILE)'),
    'SYNTH_EMPTY_SCENE': (empty, 'empty top-level list (source-predicted: exit 0, no top-level objects)'),
}

mutlog = []
cases = []
for k, (data, intent) in mutants.items():
    p = LOCAL_ROOT / (k + '.nif')
    p.write_bytes(data)
    diffs = [{'offset': i, 'original': b[i], 'new': data[i]}
             for i in range(min(len(b), len(data))) if i < len(b) and b[i] != data[i]]
    mutlog.append({
        'case': k,
        'base_input': (ident(base_name) if k != 'SYNTH_EMPTY_SCENE'
                       else {'note': 'no SDK base; fully synthetic minimal file authored by this run'}),
        'fixture_local_only': ident(p),
        'length': len(data),
        'length_vs_base': (len(data) - len(b)) if k != 'SYNTH_EMPTY_SCENE' else None,
        'changed_offsets': [d['offset'] for d in diffs] if k != 'SYNTH_EMPTY_SCENE' else [],
        'changed_byte_pairs': diffs if k != 'SYNTH_EMPTY_SCENE' else [],
        'header_line_original': (b[0:hdr_end - 1].decode('ascii', errors='replace')
                                  if k == 'SYNTH_BAD_HEADER_TEXT' else None),
        'header_line_new': ('X' * (hdr_end - 1) if k == 'SYNTH_BAD_HEADER_TEXT' else None),
        'intended_failure': intent,
        'synthetic_not_original_game_data': True,
        'fixture_scope': 'LOCAL_ONLY (SDK-derived copy or own synthetic; not committed to the repo)',
    })
    cases.append((k, p))

cases = [(k, samples[k], 'POSITIVE') for k in samples] + [(k, p, 'NEGATIVE_OR_EMPTY') for k, p in cases]
cases.append(('MISSING_INPUT', LOCAL_ROOT / 'DOES_NOT_EXIST_R1.nif', 'NEGATIVE_OR_EMPTY'))

env = os.environ.copy()
original_path = env.get('PATH', '')
env['PATH'] = str(RUNTIME) + ';' + original_path
old_error_mode = ctypes.windll.kernel32.SetErrorMode(0x0001 | 0x0002 | 0x8000)
results = []
try:
    for name, p, kind in cases:
        command = [str(TOOL), '-in', str(p)] + FLAGS
        out = RAW / (name + '.stdout.txt')
        err = RAW / (name + '.stderr.txt')
        r = {
            'case': name, 'kind': kind,
            'input': str(p),
            'input_identity': (ident(p) if p.exists() else {'path': str(p), 'exists': False}),
            'command': command,
            'cwd': str(LOCAL_ROOT),
            'child_env_delta': {'PATH': '+' + str(RUNTIME) + ';<inherited PATH>'},
            'child_env_delta_class': 'CHILD_PROCESS_PATH_DLL_EXPOSURE',
            'timeout_s': TIMEOUT_S,
            'stdout_raw_path': str(out), 'stderr_raw_path': str(err),
        }
        with out.open('wb') as of, err.open('wb') as ef:
            try:
                proc = subprocess.run(command, cwd=str(LOCAL_ROOT), env=env,
                                      stdout=of, stderr=ef, timeout=TIMEOUT_S,
                                      creationflags=subprocess.CREATE_NO_WINDOW, check=False)
                r['exit_code'] = proc.returncode
                r['timeout'] = False
            except subprocess.TimeoutExpired:
                r['exit_code'] = None
                r['timeout'] = True
            except OSError as ex:
                r['exit_code'] = None
                r['timeout'] = False
                r['launch_error'] = str(ex)
        text = out.read_bytes().decode('cp1252', errors='replace')
        errtext = err.read_bytes().decode('cp1252', errors='replace')
        parsed = parse_stdout(text)
        r.update(stderr_text=errtext,
                 stdout_size=out.stat().st_size, stderr_size=err.stat().st_size,
                 parsed_summary=parsed,
                 executable_identity_at_run=tool_before,
                 scope='SDK_ONLY_NOT_PCG')
        if kind == 'POSITIVE':
            comp = DESKTOP_COMPARISON[name]
            rep = parsed['reported_summary'] or [None, None]
            r['desktop_comparison'] = comp
            r['vs_desktop'] = {
                'visits_observed_vs_desktop': [rep[0], comp['visits']],
                'unique_addresses_observed_vs_desktop': [parsed['unique_printed_addresses'], comp['unique_addresses']],
                'depth_observed_vs_desktop': [rep[1], comp['depth']],
                'serialized_blocks_measured_vs_desktop': [tables[name]['serialized_block_count'], comp['blocks']],
                'counts_match_desktop': (rep[0] == comp['visits'] and
                                         parsed['unique_printed_addresses'] == comp['unique_addresses'] and
                                         rep[1] == comp['depth'] and
                                         tables[name]['serialized_block_count'] == comp['blocks']),
            }
        results.append(r)
finally:
    ctypes.windll.kernel32.SetErrorMode(old_error_mode)

tool_after = ident(TOOL)
unchanged = {
    'tool_unchanged': tool_after == tool_before,
    'tool_after': tool_after,
    'dlls_unchanged': all(ident(RUNTIME / n['path'].split('\\')[-1]) == n for n in dll_identities),
    'samples_unchanged': all(ident(samples[k]) == v for k, v in sample_identities.items()),
}

result = {
    'run_id': 'PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009',
    'phase': 'SDK_QUALIFICATION (Work Package B)',
    'tool_identity': tool_before,
    'dll_identities': dll_identities,
    'sample_identities': sample_identities,
    'own_header_table_measurements': tables,
    'mutations_and_negative_fixture_records': mutlog,
    'execution_environment': {
        'dll_exposure_class': 'CHILD_PROCESS_PATH_DLL_EXPOSURE',
        'path_prepend': str(RUNTIME),
        'system32_msvcp71_present': False,
        'system32_msvcr71_present': False,
        'printer_imports': ['MSVCP71.dll', 'MSVCR71.dll'],
        'per_process_timeout_s': TIMEOUT_S,
        'launcher_error_mode': 'SetErrorMode(SEM_FAILCRITICALERRORS|SEM_NOOPENFILEERRORBOX|SEM_NOGPFAULTERRORBOX)',
        'flags': FLAGS,
        'cwd': str(LOCAL_ROOT),
    },
    'cases': results,
    'originals_unchanged_after_runs': unchanged,
    'client_executed': False,
    'gui_executed': False,
    'global_environment_changed': False,
    'pe_data_read': False,
}
(SDK_OUT / 'SDK_EXECUTION_RESULTS.json').write_text(
    json.dumps(result, indent=2) + '\n', encoding='utf-8')
(SDK_OUT / 'negative_control_details_internal.json').write_text(
    json.dumps({'mutations': mutlog,
                'negative_cases': [r for r in results if r['kind'] == 'NEGATIVE_OR_EMPTY']},
               indent=2) + '\n', encoding='utf-8')

print(json.dumps({
    'tool_unchanged': unchanged['tool_unchanged'],
    'cases': [{'case': r['case'], 'exit_code': r.get('exit_code'), 'timeout': r.get('timeout'),
               'visits': r['parsed_summary']['numbered_visit_rows_parsed'],
               'unaccounted': r['parsed_summary']['numbered_lines_unaccounted'],
               'summary': r['parsed_summary']['reported_summary'],
               'stderr': r['stderr_text'][:60]}
              for r in results],
}, indent=2))
