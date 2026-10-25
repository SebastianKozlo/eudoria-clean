# REPRODUCTION — PE2003_MODEL_INSTANCE_PLACEMENT_STATIC_R1_20261024

How an independent auditor can reproduce the main results (all inputs hash-pinned in the private package INPUT_RECHECK.json / EXTERNAL_DEPENDENCY_MANIFEST.csv; binary = PE2_unpacked_out.exe 2207744 B, SHA256 56178993692A7409C896398089E482EDDF96177666BACB91A8CC1A638D9A0650, imagebase 0x400000):

1. UDP transport: at 0x5BFEE9 read call-through IAT (socket(2,2,17)); at 0x5BF918 the sole recvfrom call; CMP EAX,0x11 @0x5BF929 = min-length gate, not a type. Ordinals per wine ws2_32.spec (the V3 misread = shifted ordinal table — remap documented).
2. Definition registry: FUN_005977b0 loop over message records (stride 0x1C); FUN_00441280 insert into RB-tree @GCE+0x10064; FUN_00454300 executor (exactly 2 E8 callsites: 0x597914 immediate, 0x44aa03 in drainer FUN_0044a910).
3. HOSTCALL pump: bytes at 0x458182: MOV ECX,[EBP-30]; MOV EAX,[EBX+4]; MOV [ECX+14],EDI; CALL [EDX+0xC] — VM SP publish + receiver-vtable dispatch.
4. Dispatch B table: decode binary-search/jump tables at 0x485260 (379 cases; positive control 0x3C89 -> FUN_004b59f0 ScriptInsert; case 0x10a -> FUN_004b1bd0 translation writer (x,y,z x100.0f, ADD EDI,0x50 idiom); case 0xdc -> orientation (rep movsd 9 dwords -> +0x2C)).
5. Root placement (record[6] entities): struct 0x48 parsed with ntohl (ws2_32 ord 14 via [0x5E2474]); entity ctor FUN_004889c0 (vt 0x5E4628); FUN_005030c0 @0x5030C0: FLD [ESP+0x44]; ADD EAX,0x50; 3x FMUL [0x5E412C] (= 00 00 C8 42 = 100.0f); MOV [EAX]/[EAX+4]/[EAX+8]; rotation 9x FLD -> node+0x2C (transposed).
6. Corpus negatives: binary LE-dword scan of all 1936 decoded .obj.dec members for 4508/4057/296445/296446/218757/218758 (self-only hits; known-hit control: 4652 must yield ~2744 hits in 1364 files — if zero, the scanner is broken — this control caught one broken ASCII scanner during QC).
7. EXTN fixups: parse PFIX/EXTN of 4508/4057 (.obj.dec): code_offset == operand-slot offset (opcode_off+4); bijection 10==10 / 8==8; ATTACH slot 0x0C60 (4508) / 0x08EC (4057) -> {30298, hash 0x53AA64FE, code_offset 1016} in def 1796.
8. TDF residues: chunk-chain grammar post-inflate ([count][len][data]...) over the 75 walk-fail members: all decode with exact EOF consistency; chunk types {2 (masks), 3 (gradient weights, new), 6, 9, 10}.

Tools: private per-job parsers (hash-gated, SHA assert before reads) in the campaign WORK_ROOT; Ghidra 11.2.1 headless on per-job fresh projects. Prior-run decoder grammar reused for corpus parsing only (reviewed before use).
