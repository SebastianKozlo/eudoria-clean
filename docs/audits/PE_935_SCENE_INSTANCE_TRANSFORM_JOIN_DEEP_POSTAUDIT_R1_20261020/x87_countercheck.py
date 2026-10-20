"""Synthetic rational interpreter of admitted C130 listing. Opaque helper outputs are inputs.
Not a runtime oracle; finite rational test values do not model IEEE rounding/NaNs.
"""
import json,re
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).parent
RUN=ROOT.parent/'PE_935_SCENE_INSTANCE_TRANSFORM_JOIN_SAVED_R1_20261019'
rows=[]
for s in (RUN/'P02_EXTRACT').read_text().splitlines():
 m=re.match(r'^\d+\|([0-9a-f]{8})\s+(\S+)(?:\s+(.*))?$',s)
 if m:rows.append((int(m[1],16),m[2],m[3] or ''))
def run(factor):
 E=0x800000;R=0x100000;OUT=0x300000
 reg=dict(ESP=E,ECX=R,ESI=0x44444444,EAX=0,EDX=0);mem={E+4:OUT,E+8:F(factor)};fp=[];peak=0;steps=[];helper=0;captured=None
 O=[F(1),F(2),F(3)];C=[F(101),F(202),F(303)];A=[F(11),F(22),F(33)];B=[F(41),F(52),F(63)]
 for i,x in enumerate(O):mem[R+0x54+4*i]=x
 def address(s):
  inside=re.search(r'\[(.*)\]',s)[1].strip();m=re.fullmatch(r'([A-Z]+)(?:\s*\+\s*(0x[0-9a-f]+))?',inside);assert m,s
  return reg[m[1]]+int(m[2] or '0',0)
 def value(s):
  s=s.strip()
  if '[' in s:return mem[address(s)]
  if s in reg:return reg[s]
  if s.startswith('ST'):return fp[int(s[2:])]
  return int(s,0)
 for va,op,args in rows:
  aa=[s.strip() for s in args.split(',')]
  if op=='MOV':
   v=value(aa[1])
   if '[' in aa[0]:mem[address(aa[0])]=v
   else:reg[aa[0]]=v
  elif op=='LEA':reg[aa[0]]=address(aa[1])
  elif op in ['SUB','ADD']:
   assert aa[0]=='ESP';reg['ESP']+=int(aa[1],0)*(1 if op=='ADD' else -1)
  elif op=='PUSH':
   v=value(aa[0]);reg['ESP']-=4;mem[reg['ESP']]=v
  elif op=='POP':reg[aa[0]]=mem[reg['ESP']];reg['ESP']+=4
  elif op=='FLD':fp.insert(0,F(value(args)))
  elif op=='FLDZ':fp.insert(0,F(0))
  elif op in ['FST','FSTP']:
   if '[' in args:mem[address(args)]=fp[0]
   else:fp[int(args[2:])]=fp[0]
   if op=='FSTP':fp.pop(0)
  elif op in ['FADD','FSUB','FMUL']:
   v=F(value(args));fp[0]=fp[0]+v if op=='FADD' else fp[0]-v if op=='FSUB' else fp[0]*v
  elif op in ['FMULP','FADDP','FSUBP']:
   i=int(aa[0][2:]);fp[i]=fp[i]*fp[0] if op=='FMULP' else fp[i]+fp[0] if op=='FADDP' else fp[i]-fp[0];fp.pop(0)
  elif op=='FXCH':
   i=int(args[2:]) if args else 1;fp[0],fp[i]=fp[i],fp[0]
  elif op=='CALL':
   target=int(args,0)
   if target==0x85BFA0:
    ptr=mem[reg['ESP']]
    for i,x in enumerate([F(i) for i in range(9)]+C+[F(1)]):mem[ptr+i*4]=x
    reg['EAX']=ptr;reg['ESP']+=4
   elif target==0x96CD10:
    ptr=mem[reg['ESP']];vals=A if helper==0 else B
    for i,x in enumerate(vals):mem[ptr+4*i]=x
    steps.append(dict(helper='stored' if helper==0 else 'fresh',this_address=hex(reg['ECX']),out_address=hex(ptr)))
    helper+=1;reg['ESP']+=4
   elif target==0x96D7C0:
    p2=mem[reg['ESP']];p1=mem[reg['ESP']+4]
    captured=dict(L2=[mem[p2+4*i] for i in range(3)],L1=[mem[p1+4*i] for i in range(3)]);reg['ESP']+=8
   else:raise AssertionError(hex(target))
  elif op=='RET':assert not fp and reg['ESP']==E and reg['EAX']==OUT
  else:raise AssertionError((hex(va),op,args))
  peak=max(peak,len(fp))
 assert helper==2 and captured
 assert captured['L1']==[o+F(factor)*(c-o) for o,c in zip(O,C)]
 assert captured['L2']==[a+F(factor)*(b-a) for a,b in zip(A,B)]
 return dict(factor=str(factor),L1=list(map(str,captured['L1'])),L2=list(map(str,captured['L2'])),fpu_at_ret=len(fp),peak=peak,helper_bindings=steps,result='PASS')
tests=[run(F(0)),run(F(1)),run(F(1,4))]
# Separate-object countermodel: the ctor zero at B+2C cannot entail R+2C=0.
mem={0x10000+0xC:0x20000,0x10000+0x2C:0,0x20000+0x2C:0x30000,0x30000:0x40000,0x40000+0x24:0x50000}
assert mem[0x10000+0x2C]!=mem[mem[0x10000+0xC]+0x2C]
# Provider identity and returned float storage need not be the same address.
provider=mem[0x20000+0x2C];virtual_target=mem[mem[provider]+0x24];returned_buffer=0x60000
assert provider!=returned_buffer and virtual_target==0x50000
x=dict(scope='Synthetic arithmetic and pointer counterexamples, never executes original instructions or game runtime.',x87_primary_reference='https://cdrdv2-public.intel.com/774492/325383-sdm-vol-2abcd.pdf',semantics='FSUBP ST(i),ST0 subtracts ST0 from old ST(i), then pops.',endpoint_formula='L2=A+S*(B-A), A=first helper output from R+30 stored transform; B=second helper output from fresh transform; formula conditional on helper out writes and ABI.',tests=tests,pointer_countermodels={'B_plus_2C_not_R_plus_2C':'PASS','provider_not_returned_buffer':'PASS'},limits=['Finite rational arithmetic; rounding, NaNs, exceptions, FP control word and runtime helper behavior unverified.','Frozen report u/v symbols must be bound explicitly before comparing endpoint formula.'])
with (ROOT/'COUNTERCHECKS.json').open('x',encoding='utf-8') as f:json.dump(x,f,indent=2);f.write('\n')
print(json.dumps(x,indent=2))
