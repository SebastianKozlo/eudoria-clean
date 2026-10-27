# CLAIMS - R10
| ID | Claim | Evidence | Status |
|---|---|---|---|
| C1-ABI | 5257C0 thiscall(this=recv0x70, A1, A2); forwards to 52B750(this,A1,A2) | JW window rows + Q1 recompute | CONFIRMED (window) |
| C2-BIND | 52B750: this+0xC=A1(whole record), this+8=[A1+8]=M | decode 0x52B750..0x52B7D0; Q2 verify | CONFIRMED (window) |
| C1-VT | vptr recv0x70 = 0x65E5B4; 10 virtual slots; +0x30 area is float data | store at 0x525865 + raw dump; Q1 byte-verify | CONFIRMED |
| C1-LIST | 5257C0 passes M to 534F00; result iterated stride 0x24 (+0x1C/+0x20) | JW window + tail decode | CONFIRMED (window); list semantics INFERENCE |
| C3-WRAP | 534F00 = cdecl SEH wrapper, core 0x4475C0(helper16B, M, &A) | decode 0x534F00..0x534F83 closed | CONFIRMED (window) |
| C4-DISP | 0x4475C0 dispatches M via helper vtable slot +0x10; front-or-NULL result | decode 0x4475C0..0x447680 closed; Q2 verify | CONFIRMED (window) |
| C5-READER | helper vtable=0x65BCE4; [vt+0x10]=0x447B20 = M reader; +0x08=0x447C90 | ctor 0x4474F0 closed + blob dwords; Q2 verify | CONFIRMED (identity); 0x447B20 semantics OPEN |
| X1-REG | vt+30 call at 0x564A44: receiver=[bucket_entry+0x18], arg1=E(edi), arg2=0 | R8 M03 window + Q1 independent | CONFIRMED (window) |
| X-NEG | no dword 0x451730/0x451710 in whole flat image => no vtable direct entry | root dword-scan (X2-RAWSCAN) | BOUNDED NEGATIVE (direct dwords only) |
| X-CENSUS | 451730: 9 direct callers; 451710: 10; only adjacent pair in wrapper 0x4021E0 | root rel32 scan | CONFIRMED |
| X3-WRAP | 0x4021E0 builder: S=edi=this; E=alloc(0x78)+ctor 0x451430; single caller 0x4019EB | decode 0x4021E0..0x402421 + census | CONFIRMED (window); setter run beyond window raw-hex grounded, decode-verified only to 0x402421 |
| X3-FIX | 451730 at 0x40248A arg = [S+0x68]; run 451700..451990 over S+0x5C..0x70 | Q2 P2 recompute of raw bytes | CONFIRMED (raw bytes); CORRECTS root misattribution |
| X4-VT | E class vtable=0x65BDB4; [vt+0x30]=0x447C90; ctor 0x451430 | decode 0x451430..0x4514C0 + blob dwords; Q2 verify | CONFIRMED |
| X-IDENT | E(wrapper) == E(564890 flow)? X==owner? M type? | no edge found | UNVERIFIED |
| P1-VFS | 26/26 VFS hash-covered by M2_7_2; era/source UNRESOLVED | manifest SHA cited in P1 RESULT | CONFIRMED (coverage); era UNRESOLVED |
| P1-ARCH | no PE_PCG*/FullDat*/Dat*_*.ark in contracted local scope; PE_Terrain missing | metadata-only sweep with recorded limits | BOUNDED NEGATIVE |
| M-CLASS | M is a node/model/resource | none | UNVERIFIED (do not promote) |
