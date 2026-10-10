"""PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009 - Work Package B.

Combiner: merges this phase's synthetic-control and negative-control internal
results into the contract-required artifact 01_SDK/SYNTHETIC_AND_NEGATIVE_CONTROLS.json.
Own code of this run (not reused from Desktop). Reads only this run's internal
JSONs; writes one combined JSON; changes nothing else.
"""
import json
from pathlib import Path

SDK_OUT = Path(r'D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits'
               r'\PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009\01_SDK')

neg = json.loads((SDK_OUT / 'negative_control_details_internal.json').read_text(encoding='utf-8'))
syn = json.loads((SDK_OUT / 'synthetic_control_details_internal.json').read_text(encoding='utf-8'))

# --- synthetic section: expected (preregistered) vs actual ---
synthetic_cases = []
for r in syn['results']:
    synthetic_cases.append({
        'case': r['case'],
        'preregistration_locator': '01_SDK/PREREGISTRATION_SDK_PHASE.md section 3',
        'expected_probe_world_translation': r['expected_probe_world_translation'],
        'expected_derivation': r['expected_derivation'],
        'expected_visits': r['expected_visits'],
        'actual_exit_code': r['exit_code'],
        'timeout': r['timeout'],
        'observed_probe_world_translation': r.get('observed_probe_world_translation'),
        'observed_visits': r.get('visit_count'),
        'observed_visits_match_expected': r.get('observed_visits_match_expected'),
        'observed_camera_local_translate_via_trans_flag':
            r.get('camera_local_translate_via_trans_flag'),
        'reported_summary': r.get('reported_summary'),
        'fixture_local_only': r['fixture_local_only'],
        'raw_stdout': r['stdout_raw_path'],
        'raw_stderr': r['stderr_raw_path'],
        'command': r['command'],
        'cwd': r['cwd'],
        'child_env_delta_class': r['child_env_delta_class'],
        'special_label': r.get('diagnostic_label') or r.get('special'),
        'result': ('PASS' if r.get('pass_') else
                    ('TIMEOUT_MEASURED' if r.get('timeout') else 'FAIL')),
    })

# --- negative section: intended vs actual, with mutation bytes ---
negative_cases = []
for m, case in zip(neg['mutations'], neg['negative_cases']):
    negative_cases.append({
        'case': m['case'],
        'preregistration_locator': '01_SDK/PREREGISTRATION_SDK_PHASE.md section 4',
        'fixture_local_only': m['fixture_local_only'],
        'length': m['length'],
        'length_vs_base': m['length_vs_base'],
        'changed_offsets': m['changed_offsets'],
        'changed_byte_pairs_original_vs_new': m['changed_byte_pairs'],
        'header_line_original': m['header_line_original'],
        'header_line_new': m['header_line_new'],
        'intended_failure': m['intended_failure'],
        'intended_failure_class': ('SOURCE_PREDICTED cause (stock binary prints only '
                                   'the generic message)'),
        'actual_exit_code': case['exit_code'],
        'actual_timeout': case['timeout'],
        'actual_stderr': case['stderr_text'],
        'actual_stdout_size': case['stdout_size'],
        'raw_stdout': case['stdout_raw_path'],
        'raw_stderr': case['stderr_raw_path'],
        'command': case['command'],
        'child_env_delta_class': case['child_env_delta_class'],
        'actual_matches_preregistered_expectation': (
            case['exit_code'] == 1 and case['stderr_text'].strip() == 'Error loading stream.'
            if m['case'] != 'SYNTH_EMPTY_SCENE' else
            case['exit_code'] == 0 and
            case['stderr_text'].strip() == 'No top-level file objects.'),
    })

missing_case = next(c for c in neg['negative_cases'] if c['case'] == 'MISSING_INPUT')
missing = {
    'case': 'MISSING_INPUT',
    'preregistration_locator': '01_SDK/PREREGISTRATION_SDK_PHASE.md section 4 (N5)',
    'fixture': missing_case['input'],
    'fixture_exists': False,
    'intended_failure': 'NiFile open failure (NiStream.cpp:647-653, FILE_NOT_LOADED)',
    'actual_exit_code': missing_case['exit_code'],
    'actual_stderr': missing_case['stderr_text'],
    'raw_stdout': missing_case['stdout_raw_path'],
    'raw_stderr': missing_case['stderr_raw_path'],
}

empty = next(c for c in negative_cases if c['case'] == 'SYNTH_EMPTY_SCENE')

out = {
    'run_id': 'PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009',
    'phase': 'SDK_QUALIFICATION (Work Package B)',
    'artifact': 'SYNTHETIC_AND_NEGATIVE_CONTROLS.json',
    'preregistration': {
        'file': '01_SDK/PREREGISTRATION_SDK_PHASE.md',
        'written_before_execution': True,
        'expected_values_derived_from': 'SDK source (NiTransform composition, NiStream gates,'
                                        ' NiSceneGraphPrinter traversal) + pinned Desktop '
                                        'reports as comparison inputs',
    },
    'synthetic_transform_controls': {
        'count': len(synthetic_cases),
        'expected_registered_before_execution': True,
        'observation_probe': syn['observation_probe_scope'],
        'all_pass': all(c['result'] == 'PASS' for c in synthetic_cases),
        'cases': synthetic_cases,
    },
    'negative_sdk_copy_inputs': {
        'count': len(negative_cases),
        'mutation_base': ('fresh LOCAL_ONLY copies of OBJECT.NIF '
                          '(1eaeef364ccb84a32a3cd53a91f7b301177e00b15381357cdd96a97c4aa89511); '
                          'SDK originals never modified (verified post-run)'),
        'cases': negative_cases,
    },
    'missing_file_case': missing,
    'empty_scene_case': {
        'record': empty,
        'classification': ('empty scene + exit 0 is NOT a populated scene inspection; '
                           'per preregistered gate rule an inspection counts as populated '
                           'only with exit 0 AND >=1 numbered visit AND nonzero Total '
                           'Object Count; this case has 0 visits and no summary'),
    },
    'original_inputs_unchanged_after_all_runs': {
        'printer_exe': 'fd693af2d713c021b959fc7506200173435307c8fccc24ccd5851dfceb241c7c (re-verified post-run by independent process)',
        'dlls_and_samples': 're-verified post-run by independent process: 7/7 unchanged',
    },
}
(SDK_OUT / 'SYNTHETIC_AND_NEGATIVE_CONTROLS.json').write_text(
    json.dumps(out, indent=2) + '\n', encoding='utf-8')
print(json.dumps({
    'synthetic_all_pass': out['synthetic_transform_controls']['all_pass'],
    'synthetic_cases': [c['case'] + '=' + c['result'] for c in synthetic_cases],
    'negative_cases': [c['case'] + ' exit=' + str(c['actual_exit_code']) +
                       ' match=' + str(c['actual_matches_preregistered_expectation'])
                       for c in negative_cases],
}, indent=2))
