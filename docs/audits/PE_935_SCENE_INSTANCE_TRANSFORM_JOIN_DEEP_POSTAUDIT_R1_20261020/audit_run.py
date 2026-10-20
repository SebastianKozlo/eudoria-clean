"""Independent audit of generated saved text and Git blobs; no original game access."""
import csv,hashlib,io,json,re,subprocess
from pathlib import Path,PureWindowsPath
from datetime import datetime,timezone
ROOT=Path(__file__).parent;BASE=ROOT.parent
RUN=BASE/'PE_935_SCENE_INSTANCE_TRANSFORM_JOIN_SAVED_R1_20261019'
AUTH=BASE/'PE_935_SCENE_INSTANCE_TRANSFORM_JOIN_AUTHORING_R1_20261019'
REPO=Path(r'D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean')
COMMIT='f38349322ee32932583d73d43c7605d31f991fd7'
def sha(b):return hashlib.sha256(b).hexdigest().upper()
def pin(p):
 b=Path(p).read_bytes();return dict(size_bytes=len(b),sha256=sha(b))
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(n,x):
 with (ROOT/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n')
def tree(root):
 rows=list(csv.DictReader((root/'MANIFEST_SHA256.csv').read_text(encoding='utf-8-sig').splitlines()));seen=set();errors=[];pins=[]
 for r in rows:
  n=r['path'].replace('\\','/');pp=PureWindowsPath(n)
  assert not pp.drive and not pp.root and ':' not in n and all(t not in ('','.','..') for t in n.split('/'))
  assert n.casefold() not in seen and n!='MANIFEST_SHA256.csv';seen.add(n.casefold());p=root/n;x=pin(p);pins.append(dict(path=str(p),**x))
  if x!=dict(size_bytes=int(r['size_bytes']),sha256=r['sha256'].upper()):errors.append(n)
 actual={p.relative_to(root).as_posix().casefold() for p in root.rglob('*') if p.is_file()};extra=sorted(actual-seen-{'manifest_sha256.csv'});missing=sorted(seen-actual)
 return dict(root=str(root),rows=len(rows),physical_files=len(actual),extra=extra,missing=missing,hash_errors=errors,pass_=not(extra or missing or errors),manifest=pin(root/'MANIFEST_SHA256.csv'),files=pins)
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)
def main():
 snap={str(p):pin(p) for r in [RUN,AUTH] for p in r.rglob('*') if p.is_file()}
 save('INTEGRITY.json',dict(utc=datetime.now(timezone.utc).isoformat(),run=tree(RUN),authoring=tree(AUTH),children=[tree(p.parent) for p in sorted(RUN.glob('*/MANIFEST_SHA256.csv'))]))
 cat=load(AUTH/'SAVED_TEXT_CATALOG.json')['files'];errs=[]
 for e in cat:
  if pin(e['path'])!=dict(size_bytes=e['size_bytes'],sha256=e['sha256']):errs.append(e['path'])
 assert not errs;save('EXTERNAL_RECHECK.json',dict(count=len(cat),errors=errs,scope='Hash-only, not semantic body coverage.'))
 totals={k:0 for k in ['bodies','instructions','calls','candidates','document_lines']};prev='0'*64;events=[];selections=[];listing_rows=set();calls=set();docrows=set();decoded_doc_calls=set();sources={}
 for p in sorted((RUN/'CONTROL/EVENTS').glob('*.json')):
  e=load(p);assert e['seq']==len(events)+1 and e['previous_sha256']==prev;prev=pin(p)['sha256'];events.append(dict(file=p.name,action=e['action'],utc=e['utc'],hash=prev))
  if e['action']!='ADMIT':continue
  v=e['payload'];q=v['request'];src=q['source_path'];ls=sources.setdefault(src,Path(src).read_text(encoding='utf-8-sig').splitlines())
  if q['kind']=='listing':
   rg=[(int(x['va_begin'],16),int(x['va_end_exclusive'],16)) for x in q['regions']]
   wanted=[(i,s) for i,s in enumerate(ls,1) if (m:=re.match(r'^([0-9A-Fa-f]{8})\s{2,}(.*)$',s)) and any(a<=int(m[1],16)<b for a,b in rg)]
  else:wanted=[(i,ls[i-1]) for i in range(q['line_begin'],q['line_end_exclusive'])]
  actual=[(int(s.split('|',1)[0]),s.split('|',1)[1]) for s in (RUN/(q['package_id']+'_EXTRACT')).read_text().splitlines() if re.match(r'^\d+\|',s)]
  assert actual==wanted;assert sha('\n'.join(f'{i}|{s}' for i,s in wanted).encode())==v['selected_lines_sha256']
  for k in totals:totals[k]+=v['counts'][k]
  for i,s in wanted:
   if q['kind']=='listing':
    listing_rows.add((src,i));m=re.match(r'^([0-9a-fA-F]{8})\s+CALL\b',s)
    if m:calls.add(int(m[1],16))
   else:
    docrows.add((src,i));m=re.match(r'^([0-9a-fA-F]{8})\s+[0-9a-fA-F]+\s+call\b',s,re.I)
    if m:decoded_doc_calls.add(int(m[1],16))
  selections.append(dict(package=q['package_id'],source=src,kind=q['kind'],counts=v['counts'],source_parity=True,selected_lines_sha256=v['selected_lines_sha256']))
 stop=load(RUN/'CONTROL/EVENTS/000013_STOP.json')
 save('ADMISSION_RECHECK.json',dict(events=events,selections=selections,reserved=totals,incident_debits={k:0 for k in totals},charged=totals,unique_listing_rows=len(listing_rows),unique_listing_call_vas=len(calls),unique_document_lines=len(docrows),decoded_document_call_vas=len(decoded_doc_calls),all_visible_call_union=len(calls|decoded_doc_calls),budget_note='Guard document_body rows charge document_lines and body reservations but CALL count=0. 35 is listing-only CALL census, not all visible calls in admitted decoded documents. Logical-owner correctness is a separate obligation.'))
 # Publication bytes: all actual committed blobs, each manifest self-excludes only itself.
 specs=[('PE_935_SCENE_INSTANCE_TRANSFORM_JOIN_SAVED_R1_20261019','PUBLICATION_MANIFEST.csv'),('PE_935_PAIR_REDUCER_CONSUMER_SAVED_R2_20261019','PUBLICATION_MANIFEST_V2.csv'),('PE_935_MODEL_PAIR_TRANSPORT_DEEP_POSTAUDIT_R1_20261019','PUBLICATION_MANIFEST_V2.csv')];pubs=[]
 for name,mname in specs:
  prefix='docs/audits/'+name;paths=git('ls-tree','-r','--name-only',COMMIT,'--',prefix).decode().splitlines();matches=[p for p in paths if p.endswith('/'+mname)];assert len(matches)==1;mp=matches[0]
  data=list(csv.reader(git('show',COMMIT+':'+mp).decode('utf-8-sig').splitlines()));header=data.pop(0);rr=data;seen=set();errors=[];schema_errors=[];recovered=[]
  for raw in rr:
   n=raw[0];assert n and n.casefold() not in seen;seen.add(n.casefold());full=n if n.startswith('docs/') else prefix+'/'+n;b=git('show',COMMIT+':'+full)
   if len(raw)!=len(header):
    schema_errors.append(dict(path=n,columns=len(raw),expected=len(header)))
    assert len(header)==5 and len(raw)==4 and raw[1]=='','Unexpected malformed schema'
    size,h=raw[2:];recovered.append(n)
   else:
    r=dict(zip(header,raw));size=r.get('blob_size_bytes',r.get('size_bytes',r.get('size')));h=r.get('git_blob_sha1',r.get('sha256'))
   actualhash=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\x00'+b).hexdigest() if len(h)==40 else sha(b)
   if len(b)!=int(size) or actualhash.lower()!=h.lower():errors.append(full)
  actual={p[len(prefix)+1:].casefold() for p in paths};selfname=mp[len(prefix)+1:].casefold();extra=sorted(actual-seen-{selfname});missing=sorted(seen-actual)
  pubs.append(dict(root=prefix,manifest=mp,header=header,rows=len(rr),physical_files=len(paths),hash_errors=errors,schema_errors=schema_errors,recovery_only_for_independent_blob_check=recovered,extra=extra,missing=missing,pass_=not(errors or schema_errors or extra or missing)))
 parent=git('rev-parse',COMMIT+'^').decode().strip();changed=git('diff-tree','--no-commit-id','--name-only','-r',COMMIT).decode().splitlines();screen=[]
 for p in changed:
  b=git('show',COMMIT+':'+p)
  if b'\x00' in b or p.lower().endswith(('.bin','.exe','.nif','.ark','.vfs','.bnt')):screen.append(p)
 save('PUBLICATION_RECHECK.json',dict(commit=COMMIT,parent=parent,live_remote=git('ls-remote','origin','refs/heads/master').decode(),changed_paths=len(changed),paths=changed,entrypoint_numstat=git('diff',parent,COMMIT,'--numstat','--','AUDIT_ENTRYPOINT.md').decode().strip(),manifests=pubs,screen_flags=screen,scope='All66 changed Git blobs read; all3 public manifest sets independently rehashed.'))
 after={p:pin(p) for p in snap};assert after==snap
 save('FINAL_SOURCE_RECHECK.json',dict(files=len(snap),errors=[],unchanged=True))
 print(json.dumps(dict(run=tree(RUN)['pass_'],catalog=len(cat),totals=totals,document_calls=len(decoded_doc_calls),visible_call_union=len(calls|decoded_doc_calls),publication=pubs),indent=2))
if __name__=='__main__':main()
