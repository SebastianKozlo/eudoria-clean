# R10 REPORT - PE2003_ISO_RECORD_CONSUMER_X_PRODUCER_STATIC_R10_20261026
Sealed (UTC): 2026-10-27T06:52:27.146263+00:00
Mode: STATIC_ONLY, corpus ISO2003NOV_PE_5_1_0_0, flat image section1.bin SHA256 D43A23B9EFCFC9BC4092B38FA3C73499DE7DE7B03B20F34478B9E81EE8893631 (base 0x401000, 2939409 B).
Models: 296445.nif, 218757.nif. Goal chain resource->instance->authentic transform->frame: OPEN for both.

## Executive summary
R10 executed the R9-corrected strongest tests: the direct record(E,M) consumer 5257C0 (C-route) and the nearest producer of [E+0x14] (X-route). Both routes advanced with byte-level evidence; no per-model placement join was reached (models remain NOT_OBSERVED_IN_BOUNDED_SEARCH in the ISO tree; P1 confirmed no local .ark candidate archives in the contracted directories; era of the 26 VFS files remains UNRESOLVED).

## C-route (record consumer 5257C0) - results
1. ENTRY ABI (Q1-verified): 5257C0 = thiscall(this=receiver_0x70, A1=[esp0+4], A2=[esp0+8]); forwards (this, A1, A2) to 0x52B750 at 0x5257EE.
2. 0x52B750 body (decode 0x52B750..0x52B7D0, closed ret 8 at 0x52B7C4; Q2-verified): stores this+0x0C = A1 = the WHOLE record(E,M) (store 89 4e 0c at 0x52B77D, ecx=A1) and this+0x08 = [A1+8] = M (8b 51 08 at 0x52B77A -> 89 46 08 at 0x52B784, consistent with record ctor 533740: rec+4=E, rec+8=M). E is NOT copied (this+4/+0x14/+0x18/+0x1C zeroed). No retention of A1 visible in the closed body.
3. Back in 5257C0 (Q1-verified): reads [this+0xC]=record, then [record+8]=M, passes M to 0x534F00 at 0x525874; result (EDI) iterated with stride 0x24 (entry fields +0x1C/+0x20; per-entry alloc 0x10). vptr of receiver_0x70 = 0x65E5B4 (FACT: c7 06 b4 e5 65 00 at 0x525865).
4. 0x534F00 (closed, ret at 0x534F83; cdecl, M on stack) = SEH wrapper: ctor helper16B 0x4474F0, ctor container A 0x534C40, core 0x4475C0(helper16B, M, &A), dtors, returns ESI. NOT a vtable wrapper on M.
5. Core 0x4475C0 (closed): dispatches M via the helper vtable slot +0x10: call [edx+0x10] at 0x4475EF (edx = helper vptr), M as argument; returns NULL or *(dword*)begin (front).
6. Helper ctor 0x4474F0 (closed) sets vptr 0x65BCE4; slots: [vt+0x08]=0x447C90, [vt+0x10]=0x447B20 (actual M reader), [vt+0x14]=0x447C80. 0x447B20 body NOT decoded (frontier).
=> M is passed as an argument to reader 0x447B20 through a 16-byte dispatch helper; the returned collection is iterated by the 0x70 receiver with 0x24-stride entries. M itself remains UNCLASSIFIED (not proven node/model/resource).

## X-route (producer of [E+0x14]) - results
1. X1 (Q1-verified): in 0x564890, call [edx+0x30] at 0x564A44 receiver = [bucket_entry+0x18] (esi unmodified on the match path; bucket = [this+4]+32*(arg1&0xFF)); arg1 = edi = E (result of call [edx+4] at 0x5649BC); arg2 = 0 (local struct field, init at 0x56492A). [esp+0xC] at 0x564A2B = saved this -> owner stored to [E+0xC] by 451710 at 0x564A32 (R9 correction upheld).
2. Bounded negative (root dword-scan, whole flat image): NO dword 0x00451730 and NO dword 0x00451710 exists anywhere in the flat blob => no vtable of this image can contain either setter as a direct entry (thunk/indirection outside this negative scope). Therefore the vt+0x30 registration target is NOT 451730 in any direct-dword sense.
3. Callsite census (root rel32 scan): 451730 has 9 direct callers; 451710 has 10 (incl. 0x564A32). The ONLY adjacent-pair site is 0x402474/0x40248A inside wrapper 0x4021E0.
4. Wrapper 0x4021E0 (entry verified: prologue 6a ff 68 ...; previous fn ret 0x14 at 0x4021CC; ONLY direct caller: 0x4019EB): thiscall, edi=this=SOURCE S; builds fresh E: alloc(0x78) at 0x402230 -> ctor 0x451430 (only direct caller 0x40224A) -> esi=E; copies S fields into E through a run of setter calls (constants 0x83..0x86 and string 0x6AEE0C mixed in => builder/copy-construct, not bit-clone).
5. Setter-run correction (Q2 P2, fixes the root raw-hex misattribution): at 0x40247F call 451720 with [S+0x64]; at 0x40248A call 451730 with [S+0x68] (the earlier [S+0x64]-to-451730 attribution in the root dispatch context was wrong). The wrapper initializes E through the run 451700..451990 over successive S fields (S+0x5C..S+0x70 observed region). Hence X = M32[E+0x14] is a copy of SOURCE field [S+0x68] for this population.
6. E class vtable (X4, Q2-verified): ctor 0x451430 sets vptr 0x65BDB4 (mov [ebp],0x65BDB4 at 0x4514A0, ebp=ecx). Slots: [vt+0x2C]=0x417890, [vt+0x30]=0x447C90, [vt+0x34]=0x447C90. Since E vt+0x30 = 0x447C90 (a shared query helper, also present at slots 3/4 of vtable 0x65E5B4), the registration call on an instance of E class would reach 0x447C90, not any setter. The X1 receiver ([bucket_entry+0x18], slots +0x2C/+0x30/+0x34) is NOT proven to be E class (no edge).
7. E(wrapper-population) vs E(564890-flow): NO identity edge proven. The [E+0x14] writer population for the 564890 flow remains unqualified; candidate wrapper lineage is 0x4019EB -> 0x4021E0 (single caller), with E ctor 0x451430.
X=owner remains UNVERIFIED. X origin for the wrapper population = [S+0x68] (copy); X vtable and X.vt+8 (M producer) remain OPEN.

## P1 (metadata provenance sweep)
26/26 VFS files of the campaign corpus are hash-covered by the existing M2_7_2 manifest (independent_rehash_results.json), but their era/source binding is UNRESOLVED (corpus registry label CD_JAN_2003 is contested by ArkVFS02/R9 errata). Local archive-name sweep (top-level only, limits 200/100, no reparse traversal): [DRIVE]/ProjectEntropia (pe42_cd_jan2003/, pe42_en.exe 525581323 B, 2003-02-21), [DRIVE]/Entropia Universe (EU client files), [DRIVE]/PE_Terrain (DOES NOT EXIST), Downloads Project-Entropia-related filter (0 hits). NO PE_PCG*.ark / FullDat*.ark / Dat*_*.ark found in scope. AK-magic test not executed (no physical candidate). No game download, no build change, no full templates/ISO scan.

## Corrections issued in-run (CORRECTIONS.md)
- ROOT self-correction (Q2 P2): 451730 at 0x40248A argument = [S+0x68], not [S+0x64]; the adjacent pair is a run of 5+ setters (451700..451990), not a 2-setter pair.
- Q1 confirmed the X1 RESULT naming offset (564a3e push / 564a3a mov) and all delta arithmetic.
- Carried R9 corrections unchanged (564A32->451710->E+C; 417690 owns 4176C0; 52A215 releases M in EDI; 448-bit/full-standard cipher claim unproven; template scalar not XYZ).

## Per-model certs
296445.nif: availability=NOT_OBSERVED_IN_BOUNDED_SEARCH (carried R9; P1 adds no new source); resource->instance=OPEN (no model-specific instance); instance->transform=OPEN; transform values=NOT_ESTABLISHED; frame/units/axis=NOT_ESTABLISHED.
218757.nif: identical statuses (no per-model divergence produced by R10; C/X mechanism progress is common-mechanism only and does not close either cert).

## Honesty statements
WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; SOURCE_SPECIFIC_ISO_MODELS=NOT_OBSERVED_IN_BOUNDED_SEARCH; LOCAL_SOURCE_EXHAUSTED=NO; CANONICAL_GATE_EFFECT=NONE; advisory until external postaudit.
