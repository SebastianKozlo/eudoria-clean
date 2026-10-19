"""Explicit adapters for the legacy manifest schemas; no repair of source files."""
from pathlib import Path
import json,hashlib
R=Path(r'D:\Eudoria_Reconstruction\99_Audits\PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018')
A=Path(__file__).parent
def pin(p):
 b=p.read_bytes();return {'size_bytes':len(b),'sha256':hashlib.sha256(b).hexdigest().upper()}
def check(p):
 m=json.loads(p.read_text(encoding='utf-8-sig'));rows=None;schema=None
 for k in ['artifacts','files','entries','artifact_census','package_files']:
  if isinstance(m.get(k),list):rows=m[k];schema=k;break
 assert rows is not None,p
 names=[];errors=[];unhashed=[];self_meta=[];good=0
 for x in rows:
  n=next((x[k] for k in ['path','relative_path','name','file','artifact'] if k in x),None)
  if n=='MANIFEST.json' and x.get('self_excluded'):
   self_meta.append(x);continue
  assert n,p
  n=n.replace('\\','/');names.append(n);h=x.get('sha256',x.get('sha'));z=x.get('size_bytes',x.get('bytes',x.get('size')))
  if h is None or z is None:unhashed.append(n);continue
  f=p.parent/n;actual=pin(f)
  if actual!={'size_bytes':int(z),'sha256':h.upper()}:errors.append({'path':n,'expected':{'size_bytes':z,'sha256':h},'actual':actual})
  else:good+=1
 actual_names={q.relative_to(p.parent).as_posix() for q in p.parent.rglob('*') if q.is_file()}
 return {'schema_adapter':schema,'data_rows':len(names),'self_metadata_rows':len(self_meta),'hashed_rows_passed':good,'hash_mismatches':errors,'unhashed_rows':unhashed,
  'physical_files':len(actual_names),'extra':sorted(actual_names-set(names)-{'MANIFEST.json'}),'missing':sorted(set(names)-actual_names),
  'duplicate_names':len(names)-len(set(names)),'case_aliases':len(names)-len({n.casefold() for n in names}),'manifest_identity':pin(p)}
out={p.parent.relative_to(R).as_posix():check(p) for p in sorted(R.rglob('MANIFEST.json')) if p.parent!=R}
result={'schema_note':'Names/file/artifact aliases are explicit adapters, not source errors. First generic scan diagnostics retained separately. QC P03 has roles-only inventory and cannot verify its own four files.',
 'nested_count':len(out),'results':out,'hash_mismatches_total':sum(len(x['hash_mismatches']) for x in out.values()),'unhashed_rows_total':sum(len(x['unhashed_rows']) for x in out.values())}
with (A/'NESTED_MANIFEST_RECHECK.json').open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
old=(A/'INTEGRITY.json').read_bytes()
with (A/'CHECKER_DIAGNOSTICS_V1.json').open('xb') as f:f.write(old)
integrity=json.loads(old);integrity['nested']=out;integrity['checker_revision']={'previous_bytes_retained':'CHECKER_DIAGNOSTICS_V1.json','previous_sha256':hashlib.sha256(old).hexdigest().upper(),'cause':'The first generic scanner did not support all source schemas; schema diagnostic was not a hash-mismatch claim. This pre-seal correction uses explicit adapters in recheck_nested.py.'}
(A/'INTEGRITY.json').write_text(json.dumps(integrity,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'nested':len(out),'hash_mismatches':[(n,x['hash_mismatches']) for n,x in out.items() if x['hash_mismatches']],
 'unhashed':[(n,x['unhashed_rows']) for n,x in out.items() if x['unhashed_rows']],
 'coverage_errors':[(n,x['extra'],x['missing']) for n,x in out.items() if x['extra'] or x['missing']]},ensure_ascii=False,indent=2))
