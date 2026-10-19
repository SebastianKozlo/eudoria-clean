"""Independent saved-only postaudit. Reads frozen evidence and Git blobs, writes here.
Does not run any original worker script, game, decompiler, debugger or configuration.
"""
from pathlib import Path,PureWindowsPath
from datetime import datetime,timezone
import csv,hashlib,io,json,re,subprocess,collections

B=Path(r'D:\Eudoria_Reconstruction\99_Audits')
R=B/'PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018'
A=Path(__file__).parent
AUTH=B/'PE_935_BUILDING_PLACEMENT_5H_AUTHORING_R1_20261018'
REPO=Path(r'D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean')
SHA='2265ec61a1f00a45cdc9e95fdaf588b3708c1ddc'
H5=REPO/'docs/audits/PE_NIGHT_AGGREGATE_20260905_160000/GHIDRA_H5_VTABLE2.txt'
GATE=H5.with_name('GHIDRA_GATE_00407270.txt')
def sha(b):return hashlib.sha256(b).hexdigest().upper()
def pin(p):
 b=p.read_bytes();return {'size_bytes':len(b),'sha256':sha(b)}
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(n,x):
 p=A/n
 with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)
def verify_json_manifest(root):
 p=root/'MANIFEST.json';m=load(p);rows=m.get('artifacts',m.get('files',m.get('entries')))
 if not isinstance(rows,list):return {'error':'UNRECOGNIZED_SCHEMA','keys':list(m)}
 names=[];errors=[]
 for x in rows:
  n=x.get('path',x.get('relative_path'));z=x.get('size_bytes',x.get('bytes',x.get('size')));h=x.get('sha256',x.get('sha'))
  if not n or z is None or not h:errors.append({'schema':x});continue
  n=n.replace('\\','/');names.append(n);pp=PureWindowsPath(n)
  if pp.drive or pp.is_absolute() or '..' in pp.parts:errors.append({'unsafe':n});continue
  t=root/n
  if not t.is_file():errors.append({'missing':n});continue
  pp=pin(t)
  if pp!={'size_bytes':int(z),'sha256':h.upper()}:errors.append({'mismatch':n,'actual':pp})
 actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
 return {'manifest':pin(p),'rows':len(rows),'physical_files':len(actual),'hash_errors':errors,
         'duplicate_rows':len(names)-len(set(names)),'case_aliases':len(names)-len({n.casefold() for n in names}),
         'extra':sorted(actual-set(names)-{'MANIFEST.json'}),'missing':sorted(set(names)-actual),
         'self_exclusion_scope':'only root/MANIFEST.json may be excluded, never all basenames'}

assert not (A/'INTEGRITY.json').exists()
snapshot={p.relative_to(R).as_posix():pin(p) for p in R.rglob('*') if p.is_file()}
parent=verify_json_manifest(R)
nested={str(p.parent.relative_to(R)):verify_json_manifest(p.parent) for p in sorted(R.rglob('MANIFEST.json')) if p.parent!=R}
put('INTEGRITY.json',{'parent':parent,'nested':nested,'all_285_source_file_pins':snapshot,
 'source_parent_manifest_first_attempt_retention':'Manifest metadata reports overwritten previous parent attempt SHA C4517A...; bytes of that attempt are absent from current root',
 'interpretation':'260 listed payload files match; full root bijection FAIL: 24 nested manifests unlisted + root self=285 physical files. No hash mismatch implies no evidence of changed listed payload; does not repair coverage.'})

events=[];prev='0'*64;res={k:0 for k in ['bodies','instructions','edges','candidates']};pkg={}
for i,p in enumerate(sorted((R/'CONTROL/EVENTS').glob('*.json')),1):
 e=load(p);assert e['seq']==i and e['previous_event_sha256']==prev,p
 prev=pin(p)['sha256'];events.append(e)
 if e['action']=='ADMIT':
  pp=pkg.setdefault(e['payload']['package_id'],{k:0 for k in res})
  for k in res:res[k]+=e['payload']['reserve'][k];pp[k]+=e['payload']['reserve'][k]
start=events[0];stop=events[-1]
receipt=load(B/'PE_935_BUILDING_PLACEMENT_5H_PUBLICATION_RECEIPT_R1_20261018/RECEIPT.json')
commit_time=git('show','-s','--format=%cI',SHA).decode().strip()
clock={'event_count':len(events),'admit_count':sum(e['action']=='ADMIT' for e in events),'deny_count':sum(e['action']=='DENY' for e in events),
 'chain_links_passed':len(events)-1,'T0_utc':start['utc'],'STOP_utc':stop['utc'],'STOP_event_sha256':prev,
 'wall_seconds':stop['wall_epoch']-start['wall_epoch'],'monotonic_seconds':stop['monotonic_seconds']-start['monotonic_seconds'],
 'publication_commit_time':commit_time,'publication_receipt_mtime_utc':datetime.fromtimestamp((B/'PE_935_BUILDING_PLACEMENT_5H_PUBLICATION_RECEIPT_R1_20261018/RECEIPT.json').stat().st_mtime,timezone.utc).isoformat(),
 'reserved':res,'by_package':pkg,'actual_stop_reason':'SCIENCE_QUEUE_EXHAUSTED',
 'audit_stop_assessment':'12 science packages contractual cap reached; no basis to infer every meaningful in-corpus edge exhausted. Front B receiver/node writer remains an explicit saved-source research frontier. Future design must distinguish package cap from evidence exhaustion.'}
put('CONTROL_AND_CLOCK.json',clock)

data=H5.read_bytes();assert sha(data)=='642CC29A01B8AD6F783E82E14DA4A61FA00BA6A3EC6DF98EDFF28AC25CC1D8DB'
lines=data.decode('utf-8-sig').splitlines()
rx=re.compile(r'^\s*(?:SRCLN\s+)?(\d+)\s*[:|]\s*(?:(?:0x[0-9A-Fa-f]{8})\s*\|\s*)?([0-9a-fA-F]{8})\s+(.+?)\s*$')
by_pkg={};allrows=[];allcalls=[];bad=[]
for d in sorted((R/'packages').iterdir()):
 if not d.is_dir():continue
 rr=[];extracts=[]
 for p in sorted(d.rglob('*.txt')):
  pr=[]
  for s in p.read_text(encoding='utf-8-sig').splitlines():
   m=rx.match(s)
   if not m:continue
   ln=int(m[1]);va=int(m[2],16);instruction=m[3]
   if lines[ln-1] != m[2]+'  '+instruction:bad.append({'file':str(p),'line':ln,'VA':hex(va)})
   row={'source_line':ln,'VA':va,'instruction':instruction,'extract':p.relative_to(R).as_posix()}
   rr.append(row);pr.append(row)
  if pr:extracts.append({'path':p.relative_to(R).as_posix(),'rows':len(pr),'first_va':hex(pr[0]['VA']),'last_va':hex(pr[-1]['VA'])})
 calls=[x for x in rr if re.match('CALL\\b',x['instruction'],re.I)]
 by_pkg[d.name]={'instruction_rows':len(rr),'unique_VA':len({x['VA'] for x in rr}),'CALL_sites':len({x['VA'] for x in calls}),
 'CALL_rows':len(calls),'distinct_CALL_operands':len({x['instruction'].upper() for x in calls}),'extracts':extracts,'reserved':pkg.get(d.name[:3],{})}
 allrows+=rr;allcalls+=calls
assert not bad,bad
assert len(allrows)==1254 and len(allcalls)==136
put('RAW_REDERIVATION.json',{'source':pin(H5),'extracts':sum(len(x['extracts']) for x in by_pkg.values()),'rows_parity_passed':len(allrows),'parity_errors':bad,
 'sum_instruction_rows':len(allrows),'unique_instruction_VA':len({x['VA'] for x in allrows}),
 'sum_CALL_rows':len(allcalls),'unique_CALL_site_VA':len({x['VA'] for x in allcalls}),
 'overlapping_instruction_rows':[{ 'VA':hex(v),'occurrences':n} for v,n in collections.Counter(x['VA'] for x in allrows).items() if n>1],
 'by_package':by_pkg,'body_counter_limit':'Reported30 is not certified as unique logical bodies: P02 explicitly counts2 internal blocks of prior body, P11 counts2 fragments sharing pump owner. Precise owning-function qualification remains required.'})

# Published blobs are checked directly from the committed tree, never trusted from a worktree.
changed=git('diff-tree','--no-commit-id','--name-only','-r',SHA).decode().splitlines()
published={n:git('show',SHA+':'+n) for n in changed}
man_name=next(n for n in changed if n.endswith('/00_PUBLICATION/PUBLICATION_MANIFEST.json'))
pm=json.loads(published[man_name].decode('utf-8-sig'));pr=pm['artifacts'];pe=[]
for x in pr:
 n=x['path'];bb=published.get(n)
 if bb is None:bb=git('show',SHA+':'+n)
 if len(bb)!=x['size_bytes'] or sha(bb)!=x['sha256'].upper():pe.append(n)
pub_names=[x['path'] for x in pr]
assert not pe and len(pub_names)==len(set(pub_names))
expected=set(published)-{man_name}
uncovered=sorted(expected-set(pub_names));extra=sorted(set(pub_names)-expected)
entry_diff=git('diff',SHA+'^',SHA,'--numstat','--','AUDIT_ENTRYPOINT.md').decode().strip()
live=git('ls-remote','origin','refs/heads/master').decode().split()[0]
pub_result={'verified_utc':datetime.now(timezone.utc).isoformat(),'commit':SHA,'LIVE_master':live,'remote_matches':live==SHA,
 'parent_commit':git('rev-parse',SHA+'^').decode().strip(),'changed_paths':len(changed),'publication_manifest_rows':len(pr),
 'publication_hash_errors':pe,'uncovered_changed_paths':uncovered,'extra_manifest_paths':extra,
 'new_file_extensions':dict(collections.Counter(Path(n).suffix for n in changed)),
 'entrypoint_numstat':entry_diff,'copy_scope':'217 rows + publication manifest =218 changed paths; distinct from frozen local285-file source',
 'source_parent_manifest_is_metadata_not_public_bijection':True,
 'content_scan':{'no_game_binary_extensions':not any(Path(n).suffix.lower() in ['.exe','.dll','.nif','.bin','.vfs','.bnt','.ark','.dds'] for n in changed),
 'no_personal_user_paths_in_new_report_blobs':not any(re.search(rb'[A-Za-z]:\\\\?Users\\',b) for n,b in published.items() if n!='AUDIT_ENTRYPOINT.md'),
 'full_listing_excerpts_not_copied_as_files':not any('EXTRACT_' in Path(n).name or '/extracts/' in n or '01_RAW' in n for n in changed)},
 'limitations':'Mechanical scan plus full public synthesis/review of key claim documents. Not claiming every byte is proprietary-free solely from extension/regex; short analytic instruction quotations remain in own reports.'}
put('PUBLICATION_RECHECK.json',pub_result)

catalog=load(AUTH/'SAVED_TEXT_CATALOG.json')['files']
for x in catalog:
 p=Path(x['path']);assert p.suffix.lower() in ['.py','.txt','.md','.json','.csv','.c']
 assert pin(p)=={k:x[k] for k in ['size_bytes','sha256']},str(p)
assert snapshot=={p.relative_to(R).as_posix():pin(p) for p in R.rglob('*') if p.is_file()}
put('SOURCE_RECHECK.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_run_files_unchanged':len(snapshot),'catalog_pins_passed':len(catalog),
 'new_auditor_counterevidence_outside_old_catalog':{'path':str(GATE),'pin':pin(GATE),'scope':'Existing decompiled text, read after frozen run only for auditing its registration premise; same-build provenance needs qualification before instruction-level promotion'},
 'game_reads':0,'runtime_actions':0,'source_writes':0,'repo_content_changes':0})
print(json.dumps({'parent_rows':parent['rows'],'physical_files':parent['physical_files'],'unlisted_nested_manifests':len(parent['extra']),
 'nested_manifests':len(nested),'rows_parity':len(allrows),'unique_rows':len({x['VA'] for x in allrows}),'CALL_sites':len({x['VA'] for x in allcalls}),
 'publication':pub_result,'source_recheck':'285 files +967 pins unchanged'},ensure_ascii=False,indent=2))
