"""Synthetic arithmetic/countermodels, not execution of the game or its code."""
import json,pathlib,hashlib,subprocess
ROOT=pathlib.Path(__file__).parent
BASE=pathlib.Path(r'D:\Eudoria_Reconstruction')
RUN=BASE/'99_Audits/PE_935_MODEL_PAIR_TRANSPORT_QUALIFICATION_SAVED_R1_20261019'
REPO=BASE/'12_WebGame/eudoria-clean'

def put(n,x):
 with (ROOT/n).open('x',encoding='utf-8') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n')
def main():
 # B is ESP after the cookie PUSH at 006C407C. It is an abstract reference, not a captured runtime address.
 sp=0;rows=[]
 for lea,off,site in [(0x6C4095,0x1C,0x6C40A3),(0x6C40A8,0x24,0x6C40B2),(0x6C40B7,0x2C,0x6C40C1)]:
  pointer=sp+off;rows.append({'lea_va':hex(lea),'esp_minus_B':sp,'operand_offset':off,'result_minus_B':pointer,'callsite':hex(site)})
  sp-=8 # two pushes; audited callee exits are RET without immediate
 assert [r['result_minus_B'] for r in rows]==[0x1C]*3
 # Deferred caller cleanup: 24 collection bytes + 8 sort bytes + 8 equality-scan bytes.
 sp-=8;sort_args={'begin_minus_B':-24+0x34,'end_minus_B':-24+0x38}
 dup_args={'begin_minus_B':sp+0x3C,'end_minus_B':sp+0x40}
 sp-=8;sp+=0x28;assert sp==0
 assert sort_args=={'begin_minus_B':0x1C,'end_minus_B':0x20} and dup_args==sort_args
 # At 006C36BF three register pushes precede [ESP+1C].
 receiver_arg_offset=-12+0x1C;assert receiver_arg_offset==0x10
 copied_context_last=(0xAABBCC00&0xFFFFFF00)|1;assert copied_context_last!=1
 # In 006C36B0, S is function-entry ESP. Track only admitted stack instructions.
 # Three saved-register pushes, then four argument pushes for 006C29D0.
 sdelta=-12
 sdelta-=4;arg3_address=sdelta+0x20
 sdelta-=4;arg2_address=sdelta+0x28
 sdelta-=4;zero_byte_address=sdelta+0x20
 sdelta-=4;this_address=sdelta+0x38;cursor_slot=sdelta+0x2C
 assert (arg3_address,arg2_address,zero_byte_address,this_address,cursor_slot)==(0x10,0x14,0x8,0x1C,0x10)
 put('STACK_REDERIVATION.json',{'scope':'symbolic normal-exit x86 stack arithmetic on already admitted extracts','premise':'Normal returns and conventional stack/nonvolatile-register contract at opaque call boundaries; not a runtime capture','B_definition':'ESP immediately after PUSH EAX @006C407C','collection_pointer_expressions':rows,'init_header_slots_minus_B':[0x1C,0x20,0x24],'result':'one shared 3-DWORD header, not three separately constructed containers','sort_inputs':sort_args,'adjacent_scan_inputs':dup_args,'after_ADD_ESP_28_minus_B':sp,'sink_in_006C36B0':{'entry_ESP_name':'S','ESI_read_at':'006C36BF','entry_offset':receiver_arg_offset,'one_based_arg':4,'literal_at_caller':'0x00BA45E8'},'context_last_dword':{'write':'M8[B+0x34]=1 at 006C4125','copy':'M32[B+0x34] -> EBP -> sixth copied DWORD','proved':'low byte equals 1; upper 24 bits not fixed by admitted stores','counterexample':hex(copied_context_last)},'call_006C29D0':{'callee_this':'S+0x1C','arg2':'S+0x14','arg3':'S+0x10','arg4':0,'cursor_slot':'S+0x10','cursor_slot_contents':'EDI, current pair address, stored @006C36DD','arg1':'M32[S+8] after M8[S+8]=0; semantic role unknown','warning':'arg3 points to a stack slot containing the current pair pointer; it is not directly the pair pointer'}})
 # A synchronous producer can also populate requests; unanalysed transform has unknown effects.
 queue=[];visible=[]
 for pair in [(0x66,42),(7,99)]:
  queue.append({'request':pair});visible.append(len(queue))
 table_address=0xA855F0;table_memory={table_address:1};constant_pointer=table_address
 table_memory[table_address]=9
 tests=[{'id':'CM1','name':'deferred pushes make three LEAs alias','pass':len(set(r['result_minus_B'] for r in rows))==1},
 {'id':'CM2','name':'sink is arg4, not arg5','pass':receiver_arg_offset==0x10},
 {'id':'CM3','name':'byte 1 does not establish DWORD 1','pass':copied_context_last==0xAABBCC01},
 {'id':'CM4','name':'synchronous collect/project can coexist with opaque enqueue effects','pass':len(queue)==len(visible)==2},
 {'id':'CM5','name':'no-refund budget counts 20 reserved plus 2 overflow as 22','pass':20+max(4-2,0)==22},
 {'id':'CM6','name':'current pair reaches opaque callee through pointer-to-pointer stack slot','pass':arg3_address==cursor_slot==0x10},
 {'id':'CM7','name':'immediate table address alone does not establish immutable contents or their domain','pass':constant_pointer==table_address and table_memory[constant_pointer]==9}]
 put('COUNTERMODELS.json',{'origin':'synthetic analyst models; no original program execution','tests':tests,'all_pass':all(t['pass'] for t in tests)})
 meta=json.loads((ROOT/'PUBLICATION_METADATA.json').read_text(encoding='utf-8'));sha=meta['commit'];manifest_rows={};errors=[]
 git=lambda *a:subprocess.check_output(['git','-C',str(REPO),*a])
 for m in meta['publication_manifests']:
  for r in m['data']:
   old=manifest_rows.get(r['path'])
   if old is not None and old!=r:errors.append('conflicting duplicate '+r['path'])
   manifest_rows[r['path']]=r
   b=git('show',sha+':'+r['path'])
   if len(b)!=int(r['size_bytes']) or hashlib.sha256(b).hexdigest().upper()!=r['sha256'].upper():errors.append('blob mismatch '+r['path'])
 expected=set(manifest_rows)|{m['manifest'] for m in meta['publication_manifests']}
 if expected!=set(meta['changed_paths']):errors.append('changed path coverage')
 source_count=0
 for public in meta['changed_paths']:
  for name in ['PE_935_MODEL_PAIR_TRANSPORT_QUALIFICATION_SAVED_R1_20261019','PE_935_BUILDING_PLACEMENT_5H_DEEP_POSTAUDIT_R1_20261019']:
   prefix='docs/audits/'+name+'/'
   if public.startswith(prefix):
    p=BASE/'99_Audits'/name/public.removeprefix(prefix)
    if p.is_file():
     source_count+=1
     if git('show',sha+':'+public)!=p.read_bytes():errors.append('source identity mismatch '+public)
 put('PUBLICATION_REHASH.json',{'commit':sha,'unique_manifested_paths':len(manifest_rows),'changed_paths':len(meta['changed_paths']),'self_excluded_public_manifests':len(meta['publication_manifests']),'source_files_byte_compared':source_count,'errors':errors,'ok':not errors,'main_checkout_tracked_changes':any(not x.startswith('??') for x in meta['main_status'])})
 print(json.dumps({'countermodels':len(tests),'all_pass':all(t['pass'] for t in tests),'public_rows':len(manifest_rows),'source_byte_compared':source_count,'public_errors':len(errors)}))
if __name__=='__main__':main()
