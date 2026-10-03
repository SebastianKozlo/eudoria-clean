#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PE_GAMEBRYO_ORACLE_TOOL_R1_20261003 - E1 inventory CSV generator.
(a) SOURCE_ORACLE_INDEX.csv from source_oracle_index.json
(b) TOOLCHAIN_MATRIX.csv grouped from the exe census
(c) archive listing item counts (printed for the corpus inventory CSV)
"""
import csv, json, os, re

SBX = r'D:\Eudoria_Reconstruction\99_Audits\PE_GAMEBRYO_ORACLE_TOOL_R1_20261003\sandbox'
PKG = r'D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_GAMEBRYO_ORACLE_TOOL_R1_20261003'

# ---------- (a) SOURCE_ORACLE_INDEX.csv ----------
rows = json.load(open(os.path.join(SBX, 'phaseBC', 'source_oracle_index.json'), encoding='utf-8'))
outp = os.path.join(PKG, '01_INVENTORY', 'SOURCE_ORACLE_INDEX.csv')
with open(outp, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['version_category', 'class_file', 'rel_path', 'size_bytes', 'sha256', 's4_functions_present', 'note'])
    for r in rows:
        w.writerow([r['version_category'], r['class_file'], r['rel_path'], r['size'], r['sha256'], ';'.join(r['functions_present']), r['note']])
percat = {}
for r in rows:
    percat[r['version_category']] = percat.get(r['version_category'], 0) + 1
print('SOURCE_ORACLE_INDEX.csv rows=%d per_version=%s' % (len(rows), percat))

# ---------- (b) TOOLCHAIN_MATRIX.csv ----------
j = json.load(open(os.path.join(SBX, 'phaseA', 'inventory_data.json'), encoding='utf-8'))
TOOL_PAT = re.compile(r'^(SceneViewer_DX\d|SceneGraphPrinter|sgp|NifConvert|AnimationTool|AssetViewer|SceneDesigner|PhysXNifViewer|PhysXNifViewer_DLL|PhysXSceneGraphPrinter|NSFParserUtility|MatchPal|NiFontCreator|TGAQuant|ToolPluginBatch|ToolPluginTestbed)\.exe$', re.I)

def vcat(p):
    if p.startswith('extracted\\Gb12_Source') or p.startswith('extracted\\gb12_build'):
        return 'GB_1_2'
    if p.startswith('extracted\\Gb26_src') or p.startswith('extracted\\Gb26'):
        return 'GB_2_6'
    if p.startswith('Gamebryo 1.1.2 Evaluation'):
        return 'GB_1_1_2'
    return 'UNKNOWN_GAMEBRYO'

groups = {}
for e in j['exes']:
    base = os.path.basename(e['rel_path'])
    if TOOL_PAT.match(base):
        groups.setdefault(base.lower(), []).append(e)
out_rows = []
for key in sorted(groups):
    lst = groups[key]
    name = os.path.basename(lst[0]['rel_path'])
    by_ver = {}
    for e in lst:
        by_ver.setdefault(vcat(e['rel_path']), []).append(e)
    for ver, sub in sorted(by_ver.items()):
        rep = sorted(sub, key=lambda e: ('VC71' not in e['rel_path'], e['rel_path']))[0]
        out_rows.append([name, ver, ' | '.join(x['rel_path'] for x in sub),
                         rep['sha256'], rep['size'],
                         'company=%s product=%s file_version=%s product_version=%s' % (
                             rep['pe_company'], rep['pe_product'], rep['pe_file_version'], rep['pe_product_version']),
                         'NOT_TESTED (E1 static inventory; execution attempts are E2)', ''])

arch_rows = [
    ['SceneViewer_DX8/DX9.exe (prebuilt, VC71)', 'GB_1_2',
     r'ARCHIVE-INTERNAL: gamebryo_1.2.7z -> gamebryo_1.2\Tools\SceneViewer\Application\VC71\SceneViewer_DX8.exe (335,872 B) + SceneViewer_DX9.exe (335,872 B)',
     'archive+internal path (not extracted by E1)', 335872,
     'archive label gamebryo_1.2 (listing dates 2004-11-09)',
     'NOT_TESTED (E1; E2 may extract)', 'GB 1.2 prebuilt tool package'],
    ['AnimationTool_PC.cab / AssetViewer_PC.cab / Dev_Tools_PC.cab / SceneDesigner_PC.cab', 'GB_2_6',
     r'ARCHIVE-INTERNAL: GameBryo2.6.7z (root) + ALREADY EXTRACTED: extracted\Gb26\*.cab (same cabs)',
     'extracted cab files enumerated in dir census; per-cab SHA256 NOT_TESTED in E1 (see notes)', None,
     'archive label GameBryo2.6 (listing dates 2008-10-21)',
     'NOT_TESTED (E1; E2 extracts cabs if needed)',
     r'also mirrored in C:\Users\User\AppData\Local\Temp\opencode\gb_tools_inventory\ (read-only reference)'],
    ['SceneViewerDX8.dll / SceneViewerDX9.dll (SDK ToolPlugins)', 'GB_1_1_2',
     r'ARCHIVE-INTERNAL: Gamebryo 1.1.2 Evaluation.zip -> SDK\Win32\ToolPlugins\Lib\VC6 + VC71; EXTRACTED: installed tree SDK\Win32\ToolPlugins',
     'zip+internal path; installed copy covered by dir census', None,
     'zip listing dates 2004-04-27', 'NOT_TESTED (E1)', ''],
    ['GbEvaluationToolsSetup.exe (GB 2.3 toolset installer)', 'GB_2_3',
     'ARCHIVE-INTERNAL: GB_2.3.iso (182,166,094 B, 2007-04-25)',
     'ISO sha256 AF3391BF959672A1740C2BD6EAE5C4D944E557D6FEAE338B8E5128EB3F4482F4; installer NOT extracted in E1', 182166094,
     'ISO label Gb23EvaluationDisk01.txt + GbEvaluationSetup.ini',
     'NOT_TESTED (E1; E2 bounded extraction if needed)', ''],
    ['Tool MFC sources (SceneViewer/AnimationTool/DeveloperTools: SceneGraphPrinter, NifConvert, NiFontCreator, NSFParserUtility, TGAQuant, MatchPal, ToolPluginBatch, ToolPluginTestbed)', 'GB_1_2',
     r'EXTRACTED: extracted\Gb12_Source\Tools\{SceneViewer,AnimationTool,DeveloperTools\*} full MFC tool source trees',
     'source trees readable in place; representative file hashes in exe census', None,
     'Gb12_Source = Gamebryo 1.2.2 source (CoreLibs NiVersion.h sha 326D0136: 1.2.2.6, build 2006-06-19)',
     'NOT_TESTED (E1; E2 build/run attempts)', 'prebuilt tool exes also in-tree (see exe rows)'],
]
out_rows += arch_rows
outp = os.path.join(PKG, '01_INVENTORY', 'TOOLCHAIN_MATRIX.csv')
with open(outp, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['tool', 'version_category', 'physical_locations', 'representative_identity', 'rep_size_bytes', 'version_fields', 'builds_runs_status', 'notes'])
    for r in out_rows:
        w.writerow(r)
print('TOOLCHAIN_MATRIX.csv rows=%d (exe groups=%d)' % (len(out_rows), len(groups)))

# ---------- (c) archive listing item counts ----------
print('---- ARCHIVE LISTING COUNTS ----')
for fn in sorted(os.listdir(os.path.join(SBX, 'listings'))):
    if not fn.endswith('.txt') or fn.startswith('err_'):
        continue
    p = os.path.join(SBX, 'listings', fn)
    raw = open(p, 'rb').read()
    try:
        txt = raw.decode('utf-16')
    except Exception:
        txt = raw.decode('utf-8', 'replace')
    lines = [l for l in txt.splitlines() if re.match(r'^\d{4}-\d{2}-\d{2} ', l)]
    d = sum(1 for l in lines if re.search(r'D\.\.\.\.', l[:30]))
    print('%s entries=%d files=%d dirs=%d' % (fn, len(lines), len(lines) - d, d))
