"""Independent saved-evidence audit. No game-file or runtime operations."""
import csv, hashlib, json, pathlib, re, subprocess
from collections import Counter

OUT=pathlib.Path(__file__).parent
BASE=pathlib.Path(r'D:\Eudoria_Reconstruction')
RUN=BASE/'99_Audits/PE_935_MODEL_PAIR_TRANSPORT_QUALIFICATION_SAVED_R1_20261019'
AUTHOR=BASE/'99_Audits/PE_935_MODEL_PAIR_TRANSPORT_QUALIFICATION_AUTHORING_R1_20261019'
REPO=BASE/'12_WebGame/eudoria-clean'
SHA='45fe1c22c64445127bd68c412e9fa2103425ee0b'

def pin(p):
 b=p.read_bytes();return {'size_bytes':len(b),'sha256':hashlib.sha256(b).hexdigest().upper()}
def put(n,x):
 with (OUT/n).open('x',encoding='utf-8') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n')
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def tree(root):
 rows=list(csv.DictReader((root/'MANIFEST_SHA256.csv').open(encoding='utf-8-sig',newline='')))
 names=[r['path'] for r in rows]; errors=[]
 if len(names)!=len(set(n.casefold() for n in names)):errors.append('duplicate/case alias')
 for r in rows:
  p=pathlib.PurePosixPath(r['path'])
  if p.is_absolute() or '..' in p.parts or ':' in r['path'] or '\\' in r['path'] or r['path']=='MANIFEST_SHA256.csv':
   errors.append('bad path '+r['path']);continue
  target=root/r['path']
  if not target.is_file() or pin(target)!={'size_bytes':int(r['size_bytes']),'sha256':r['sha256'].upper()}:errors.append('mismatch '+r['path'])
 physical={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
 extra=physical-set(names)-{'MANIFEST_SHA256.csv'};missing=set(names)-physical
 return {'root':str(root),'rows':len(rows),'physical_files':len(physical),'errors':errors,'extra':sorted(extra),'missing':sorted(missing),'ok':not(errors or extra or missing),'manifest':pin(root/'MANIFEST_SHA256.csv')}

def main():
 roots=[RUN]+[p.parent for p in sorted(RUN.rglob('MANIFEST_SHA256.csv')) if p.parent!=RUN]
 integrity=[tree(p) for p in roots]
 put('INTEGRITY.json',{'trees':integrity,'all_ok':all(x['ok'] for x in integrity),'source_pins':[{'path':str(p),**pin(p)} for p in sorted(RUN.rglob('*')) if p.is_file()]})
 external=load(AUTHOR/'SAVED_TEXT_CATALOG.json')['files'];bad=[]
 for row in external:
  p=pathlib.Path(row['path'])
  if p.suffix.lower() not in ['.py','.ps1','.md','.txt','.c','.json','.jsonl','.csv']:raise ValueError('unauthorized file type')
  if not p.is_file() or pin(p)!={'size_bytes':row['size_bytes'],'sha256':row['sha256']}:bad.append(str(p))
 put('EXTERNAL_RECHECK.json',{'checked':len(external),'errors':bad,'writes':0})
 events=[];prev='0'*64;chain=[];totals=Counter()
 for p in sorted((RUN/'CONTROL/EVENTS').glob('*.json')):
  e=load(p);events.append(e)
  chain.append({'file':p.name,'sequence_ok':e['seq']==len(events),'previous_hash_ok':e['previous_sha256']==prev})
  prev=pin(p)['sha256']
  if e['action']=='ADMIT':totals.update(e['payload']['counts'])
 admits=[e for e in events if e['action']=='ADMIT']
 sources={e['payload']['request']['source_path']:pathlib.Path(e['payload']['request']['source_path']).read_text(encoding='utf-8-sig').splitlines() for e in admits}
 extracts=[];union={};occurrences=0;allcalls=set();matches={}
 for p in sorted(RUN.rglob('extracts/*.txt')):
  text=p.read_text(encoding='utf-8-sig');source=re.search(r'^# LOCAL ONLY; source=(.+)$',text,re.M).group(1)
  admission=re.search(r'^# admission=(.+)$',text,re.M).group(1)
  numbered=[(int(m.group(1)),m.group(2)) for line in text.splitlines() if (m:=re.match(r'^(\d+)\|(.*)$',line))]
  wrong=[i for i,s in numbered if sources[source][i-1]!=s]
  inst=[(i,s) for i,s in numbered if re.match(r'^[0-9a-fA-F]{8}\s+',s)]
  for i,s in inst:
   va=int(s[:8],16)
   if va in union and union[va]!=s:raise ValueError('conflicting rows')
   union[va]=s
   if re.match(r'^[0-9a-fA-F]{8}\s+CALL\b',s):allcalls.add(va)
  occurrences+=len(inst)
  selected='\n'.join(f'{i}|{s}' for i,s in numbered).encode()
  selected_sha=hashlib.sha256(selected).hexdigest().upper()
  event=next(e for e in admits if e['payload']['admission_id']==admission)
  bounds=event['payload']['request'].get('regions',[])
  bound_ok=all(any(int(b['va_begin'],16)<=int(s[:8],16)<int(b['va_end_exclusive'],16) for b in bounds) for _,s in inst)
  extracts.append({'path':str(p.relative_to(RUN)),'rows':len(numbered),'instruction_rows':len(inst),'source_line_mismatch':wrong,'admission_id':admission,'selected_hash_ok':selected_sha==event['payload']['selected_lines_sha256'],'bounds_ok':bound_ok})
  matches[admission]=selected_sha
 idx=list(csv.reader((RUN/'artifact_index.csv').open(encoding='utf-8-sig',newline='')));index_bad=[]
 for r in idx:
  if len(r)!=3 or not (RUN/r[0]).is_file() or pin(RUN/r[0])!={'size_bytes':int(r[1]),'sha256':r[2].upper()}:index_bad.append(r[0])
 put('RAW_AND_CONTROL_RECHECK.json',{'events':dict(Counter(e['action'] for e in events)),'chain':chain,'reservations':dict(totals),'extracts':extracts,'all_10_admits_bound':len(matches)==len(admits)==10,'physical_listing_row_occurrences':occurrences,'unique_instruction_va':len(union),'unique_call_sites':len(allcalls),'body_charge_no_refund_minimum':totals['bodies']+2,'candidate_charge_no_refund':totals['candidates'],'body_reason':'20 reserved, P08 4 observed vs 2 reserved; do not refund P09 3 to 2','root_index_rows':len(idx),'root_index_mismatches':index_bad})
 git=lambda *a:subprocess.check_output(['git','-C',str(REPO),*a])
 changed=git('diff-tree','--no-commit-id','--name-only','-r',SHA).decode().splitlines()
 manifests=[n for n in changed if n.endswith('/00_PUBLICATION/PUBLICATION_MANIFEST.csv')]
 pub=[]
 for name in manifests:
  raw=git('show',SHA+':'+name).decode('utf-8-sig');rr=list(csv.DictReader(raw.splitlines()));pub.append({'manifest':name,'fieldnames':list(rr[0]) if rr else [],'rows':len(rr),'data':rr})
 put('PUBLICATION_METADATA.json',{'commit':SHA,'parent':git('rev-parse',SHA+'^').decode().strip(),'remote_master':git('ls-remote','origin','refs/heads/master').decode().strip(),'changed_paths':changed,'publication_manifests':pub,'entrypoint_numstat':git('diff-tree','--no-commit-id','--numstat','-r',SHA,'--','AUDIT_ENTRYPOINT.md').decode().strip(),'main_status':git('status','--porcelain=v1').decode().splitlines()})
 print(json.dumps({'integrity_all_ok':all(x['ok'] for x in integrity),'external_checked':len(external),'external_errors':len(bad),'unique_instructions':len(union),'calls':len(allcalls),'events':dict(Counter(e['action'] for e in events)),'no_refund_body_charge':totals['bodies']+2,'index_bad':index_bad,'changed_paths':len(changed)}))

if __name__=='__main__':main()
