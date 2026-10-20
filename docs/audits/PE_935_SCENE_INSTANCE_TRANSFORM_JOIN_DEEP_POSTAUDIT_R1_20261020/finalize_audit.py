import csv,hashlib,io,json,subprocess
from pathlib import Path
ROOT=Path(__file__).parent;BASE=ROOT.parent
RUN=BASE/'PE_935_SCENE_INSTANCE_TRANSFORM_JOIN_SAVED_R1_20261019'
AUTH=BASE/'PE_935_SCENE_INSTANCE_TRANSFORM_JOIN_AUTHORING_R1_20261019'
REPO=Path(r'D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean')
def write(n,x):
 with (ROOT/n).open('x',encoding='utf-8',newline='\n') as f:f.write(x if isinstance(x,str) else json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def pin(p):
 b=Path(p).read_bytes();return dict(size_bytes=len(b),sha256=hashlib.sha256(b).hexdigest().upper())
errors=[];valid=0;public=[]
for p in sorted(RUN.rglob('*.json')):
 try:json.loads(p.read_text(encoding='utf-8-sig'));valid+=1
 except json.JSONDecodeError as e:errors.append(dict(path=p.relative_to(RUN).as_posix(),line=e.lineno,column=e.colno,message=e.msg))
for e in errors:
 path='docs/audits/'+RUN.name+'/packages/'+e['path'];b=subprocess.check_output(['git','show','f38349322ee32932583d73d43c7605d31f991fd7:'+path],cwd=REPO)
 try:json.loads(b.decode('utf-8-sig'))
 except json.JSONDecodeError as z:public.append(dict(path=path,line=z.lineno,column=z.colno,message=z.msg))
write('ARTIFACT_SCHEMA_CHECK.json',dict(valid_json_files=valid,invalid_json_files=errors,public_json_errors=public,source_hashes_can_match_invalid_JSON=True))
config=Path(r'C:\Users\User\.config\opencode\opencode.jsonc');cfg=json.loads(config.read_text(encoding='utf-8-sig'));roles=[]
for n in ['pe-master','pe-reconstruction','pe-master-auditor']:
 p=Path(r'D:\Eudoria_Reconstruction\.opencode\agents')/(n+'.md');roles.append(dict(role=n,path=str(p),**pin(p),model_line=next(l for l in p.read_text().splitlines() if l.startswith('model:'))))
write('MODEL_PREFERENCE_FINDING.json',dict(config_path=str(config),config_pin=pin(config),safe_model_map={k:dict(reasoningEffort=v.get('options',{}).get('reasoningEffort'),display_name=v.get('name')) for k,v in cfg['provider']['nask-glm']['models'].items()},roles=roles,required_future_model='nask-glm/glm-5-3-default',required_future_effort='medium',configuration_changed=False,secrets_included=False,official_reference='https://docs.opencode.ai/docs/agents/'))
write('NAVIGATION_ONLY_NEXT_COST.json',dict(scope='New structural navigation only, no new semantic body analysis',candidates=[dict(begin='0x0085ACD0',end_exclusive='0x0085AD10',store_site='0x0085ACE9',rows=26,calls=1,displacement='0x0C'),dict(begin='0x0085BD80',end_exclusive='0x0085BEE0',store_site='0x0085BE70',rows=125,calls=8,displacement='0x2C')],identity='Neither site qualified for actual B/R yet.'))
write('HANDOFF.md','AUDIT_VERDICT=REQUIRE_CORRECTIONS\nSCIENCE=PARTIAL_PASS_WITH_MATERIAL_IDENTITY_CORRECTIONS\nLOCAL_ROOT=108FILES_HASH_BIJECTION_PASS\nJSON_SCHEMA=FAIL_2_CLAIMS\nPUBLICATION=MASTER_PRESENT_OLD_REPAIRS_PASS_NEW_CSV_SCHEMA_FAIL\nNEXT=qualify0085ACE9 and0085BE70, separate B/R/P/T, enforce default/medium\nWORLD_XYZ_RECOVERED=NO\nCANONICAL_GATE_EFFECT=NONE\nNo next experiment, push or configuration change performed.\n')
write('STAGE_ACCEPTANCE_GATES.csv','gate,result,evidence\nSource108_files,PASS,INTEGRITY.json\nCatalog1560,PASS,EXTERNAL_RECHECK.json\nAdmission11_parity,PASS,ADMISSION_RECHECK.json\nJSON_schema,FAIL_FINDING,ARTIFACT_SCHEMA_CHECK.json\nPublication_old_V2s,PASS,PUBLICATION_RECHECK.json\nPublication_new_CSV,FAIL_FINDING,PUBLICATION_RECHECK.json\nSynthetic_x87_endpoints3,PASS,COUNTERCHECKS.json\nPointer_counterexamples2,PASS,COUNTERCHECKS.json\nNo_canonical_promotion,PASS,HANDOFF.md\n')
write('AUDIT_QA.json',dict(science_review='B/R/P/T independently reconstructed;99-row rational interpreter3endpoint factors,2pointer countermodels.',process_review='108files,5childmanifests,1560pins,11exactselections,13eventlinks; finalJSON parsed;66changedGitblobs read and3manifestsets checked.',own_checker_history='Two partial checker outputs retained under versions. Final publication check distinguishes SHA256/Gitblob schemas and records malformed rows. Administrative precheck corrected publication path mapping packages/ before writing artifacts.',limits=['No original game/runtime','No new semantic body openings; writer sites navigation only','No complete P09 owner census','No FP rounding/control-state model','No independently retrieved historical child telemetry']))
integrity=json.loads((ROOT/'INTEGRITY.json').read_text());pins=integrity['run']['files']+integrity['authoring']['files'];external=json.loads((AUTH/'SAVED_TEXT_CATALOG.json').read_text())['files'];bad=[]
for e in pins+external:
 if pin(e['path'])!=dict(size_bytes=e['size_bytes'],sha256=e['sha256']):bad.append(e['path'])
assert not bad;write('FINAL_COMPLETE_RECHECK.json',dict(files_checked=len(pins)+len(external),errors=[],all_unchanged=True))
s=io.StringIO();w=csv.writer(s,lineterminator='\n');w.writerow(['path','role'])
for p in sorted(ROOT.rglob('*')):
 if p.is_file():w.writerow([p.relative_to(ROOT).as_posix(),'AUDIT_ARTIFACT'])
write('artifact_index.csv',s.getvalue())
files=sorted(p for p in ROOT.rglob('*') if p.is_file());s=io.StringIO();w=csv.writer(s,lineterminator='\n');w.writerow(['path','size_bytes','sha256'])
for p in files:
 z=pin(p);w.writerow([p.relative_to(ROOT).as_posix(),z['size_bytes'],z['sha256']])
write('MANIFEST_SHA256.csv',s.getvalue());print(json.dumps(dict(rows=len(files),files=len(files)+1,manifest=pin(ROOT/'MANIFEST_SHA256.csv'),invalid_local_json=len(errors),invalid_public_json=len(public)),indent=2))
