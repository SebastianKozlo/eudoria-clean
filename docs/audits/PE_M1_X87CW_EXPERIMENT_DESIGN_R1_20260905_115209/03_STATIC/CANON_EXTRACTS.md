# CANON EXTRACTS — the load-bearing static facts this design composes from

**RUN_ID:** PE_M1_X87CW_EXPERIMENT_DESIGN_R1_20260905_115209
**STATUS:** VERBATIM EXTRACTS ONLY. Every item below is quoted (or faithfully paraphrased with the exact field name) from a SHA-locked pinned input. ZERO new static analysis was performed in this run. The full pointer (file + SHA256 + field/line) for each extract is given; the composition mapping is in `05_ANALYSIS\COMPOSITION_RECORD.md`.

---

## X1. The three QWORD constants + their consuming instructions

**Source:** `D:\Eudoria_Reconstruction\99_Audits\PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439\03_STATIC\CONSTANT_ADDRESS_LOCK.json` — SHA256 `6F4A9A6ED2E26F18C59AEB88F571374B73647C80FE19F65D5F0B6466A8D80304` — field `three_qword_constants` (entries 1 and 2; entry 3 quoted for chain context).

### X1.1 — the RNG divisor path

> `"symbol": "_DAT_00a7d7a8", "va": "0xa7d7a8", "section": ".rdata", "file_offset": "0x67d7a8", "bytes_le": "00 00 00 00 C0 FF DF 40", "value_f64": 32767.0, "value_f64_ok": true, "instruction_va": "0x98ce5a", "instruction_file_offset": "0x58ce5a", "instruction_bytes": "DC 35 A8 D7 A7 00", "opcode_decode": "FDIV qword ptr [0x00a7d7a8]", "operand_references_va": true, "role": "the rand01 divisor"`

- The FDIV site: **instruction VA 0x0098CE5A**, bytes `DC 35 A8 D7 A7 00`, consuming the .rdata QWORD at VA 0x00A7D7A8 = **32767.0 f64** (file-backed; bytes `00 00 00 00 C0 FF DF 40`).

### X1.2 — the position divisor path

> `"symbol": "_DAT_00a8c758", "va": "0xa8c758", "section": ".rdata", "file_offset": "0x68c758", "bytes_le": "00 00 00 00 E0 FF EF 40", "value_f64": 65535.0, "value_f64_ok": true, "instruction_va": "0x95b2bc", "instruction_file_offset": "0x55b2bc", "instruction_bytes": "DD 05 58 C7 A8 00", "opcode_decode": "FLD qword ptr [0x00a8c758]", "operand_references_va": true, "role": "the u16 position divisor"`

- The FLD site: **instruction VA 0x0095B2BC**, bytes `DD 05 58 C7 A8 00`, consuming the .rdata QWORD at VA 0x00A8C758 = **65535.0 f64** (file-backed; bytes `00 00 00 00 E0 FF EF 40`).

### X1.3 — the node-scale multiplier (chain context; the third byte-locked site)

> `"symbol": "_DAT_00a980d0", "va": "0xa980d0", "bytes_le": "00 00 00 40 E1 7A 14 3F", "value_f64": 7.812499825377017e-05, "instruction_va": "0x95b347", "instruction_bytes": "DC 0D D0 80 A9 00", "opcode_decode": "FMUL qword ptr [0x00a980d0]", "role": "the node-scale multiplier (float32(1/12800) widened)"`

## X2. The section mapping (why the VAs are file-backed)

**Source:** `...\03_STATIC\PE_SECTION_MAP.json` — SHA256 `C5688A5300C4119FD22EA74FD0D739B1E6DFCC77D112C910395061FF1ED11804`

> `"image_base": "0x400000", "machine": "0x14c", "n_sections": 5`
> `"coincidence_note": ".text and .rdata have raw_offset == rva in this binary, which is WHY the naive mapping happened to work for every .rdata constant in the census"`
> `"mapping_rule": "VA -> RVA = VA - image_base; find the section with rva <= RVA < rva + virtual_size; file offset EXISTS only when RVA - rva < raw_size"`

- Both pinned instruction sites and both constant slots live in `.text`/`.rdata` (file-backed sections). The design's breakpoint VAs are image VAs; the execution procedure verifies the loaded module base against image_base 0x00400000 before placing breakpoints (a runtime check — see W3; no static ASLR claim is made).

## X3. The chain functions — EXACTLY what the V4 matrix states

**Source:** `D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE\GATES\M1_GATE_DELIVERABLE_MATRIX_V4.json` — SHA256 `003056AC0210A7E0C33F304232F2F366D45D4E94B04D9984FA03B62D06CB4A95` — row 10 (`FOLIAGE_DISTRIBUTION`) field `knowledge`; row 11 (`FOLIAGE_SEED/RNG`) fields `knowledge`, `implementation`, `limitations`; known-open list item 7; `honest_limits_binding` item 2. (MD mirror: `M1_GATE_DELIVERABLE_MATRIX_V4.md` — SHA256 `EC04FC471C55450DF060E5E3441A92584BB0CB7C4C63ED1E223C20F0BE732552` — ROW 10 at line 134, ROW 11 at line 146, the open item at line 322, the binding limit at line 334.)

### X3.1 — row 10 knowledge (verbatim, the FOLIAGE_DISTRIBUTION chain):

> "FUN_0098fe00 procedural grid (subdivision 0..4 -> steps 1/2/4/8/16; INTEGER-ONLY per the iter035 census; 24B cells; density = *(cell+8)>>3); FUN_00990810 stored cell records {u16 x, u16 y, u32 id}; FUN_0095b180 spawn loop: nodeX/Y = f32(u16 / 65535.0 f64) = node-local fractions [0,1] (the _DAT_00a8c758 QWORD; node+0x5C/0x60); nodeScale = f32(|value * 0.00007812499825377017|) = float32(1/12800)-widened = 10737418/2^37 (the _DAT_00a980d0 QWORD; node+0x68); the u32 model bind at node+0x64; rotation IDENTITY = the RE-faithful absence; the spawn default level 1; Math.fround at the six binary FSTP-DWORD points; 76/76 bit-exact; CELL CONTENT RECONSTRUCTION-ONLY."

**Reading (the canon's own role assignment):** FUN_0098fe00 = the procedural GRID path (integer-only subdivision); FUN_0095b180 = the SPAWN path — the spawn loop is the consumer in which the position-divisor FLD (X1.2, @0x0095B2BC) and the node-scale FMUL (X1.3, @0x0095B347) execute, writing node+0x5C/0x60 (nodeX/Y) and node+0x68 (nodeScale).

### X3.2 — row 11 knowledge (verbatim, the FOLIAGE_SEED/RNG chain):

> "seed = ((p4*16+p5)*16+p1+p2+p3)*0x5CC7 + 0x6D7 (uint32), state = x*8^x; then the MSVC rand() LCG state*0x343FD + 0x269EC3 >> 16 & 0x7FFF (r in [0, 32767], always >= 0 - the 2^32f FADD idiom in FUN_0098ce30 is DEAD CODE); rand01 = f32(r / 32767.0) -> [0, 1] INCLUSIVE (the FSTP DWORD @0x0098CE60 = the f32 rounding BEFORE return); the sampler value = f32(rand01*(max-min)+min) (the min/max are f32 fields; FUN_0095ac30 FSTP DWORD @0x0095ACF0); the seed inputs: p1 = the packed 32-bit query position, p2 = the VIEW BAND (10/20/30), p4/p5 = the record u16 pair (POSITION-KEYED); NO global seed, NO server RNG in the LOCAL spawn loop; the seed-20030130 legacy scatter = VISUAL_RECONSTRUCTION_LEGACY (different BY CONSTRUCTION)."

### X3.3 — row 11 implementation (verbatim, the byte-locked operands):

> "the byte-locked operands: rand01 = f32(r / 32767.0 f64) [_DAT_00a7d7a8, FDIV QWORD @0x0098CE5A]; the node position fractions = f32(u16 / 65535.0 f64) [_DAT_00a8c758, FLD QWORD @0x0095B2BC]; the node scale = f32(|value * 0.00007812499825377017|) [_DAT_00a980d0, FMUL QWORD @0x0095B347]; the lerp f32 rounding at the FUN_0095ac30 FSTP DWORD."

**Reading (the canon's own path assignment):** the RNG-divisor FDIV (X1.1, @0x0098CE5A, with the FSTP DWORD f32 rounding at 0x0098CE60 immediately following) is the rand01 normalization in the RNG-next function family — the row's evidence set carries the decoded RE files `iter032_re_dec_0098cdf0_rng_seed.c` and `iter032_re_dec_0098ce30_rng_next.c` (row 11 `evidence`), and the row names FUN_0098ce30 as the function containing the dead-code FADD idiom adjacent to this arithmetic.

### X3.4 — row 11 limitations (verbatim, the open items the design targets):

> "KEEP OPEN: [P-RNG-P3] p3 = *(impl+0x24) UNVERIFIED (p3 = 0 in the reconstruction - labeled); the view-band p2 provenance (10/20/30) STRONGLY_SUPPORTED not byte-pinned; the actual-x87-CW conditionality: PC=24 breaks 14,104/229,376 = 6.15% of the REAL lerp domain AND 103,073/1,245,184 of the labeled synthetic domain (CONFIRMED by the run-side re-measurement) - the engine-parity claim is CONDITIONAL on PC in {53,64} + RC=nearest-even (the documented Win32 default CW 0x027F; the ACTUAL client CW is UNMEASURED - the falsifier = a runtime capture, NOT authorized in this run)"

### X3.5 — the known-open item (verbatim, known_open_list_v4 item 7):

> "the actual x87 control word at chain-execution time (the PC/RC conditional model's SENSITIVITY is now measured on both domains - real 14,104/229,376 and synthetic 103,073/1,245,184, the latter double-confirmed by THIS run's re-measurement - but the ACTUAL client CW remains UNMEASURED; a runtime capture is the falsifier)"

### X3.6 — the binding limit (verbatim, honest_limits_binding item 2):

> "The engine-parity arithmetic claims are CONDITIONAL on the x87 model: RC=nearest-even (the documented Win32 default; NOT a measurement of the original client) and PC in {53,64} - PC=24 measured DIFFERENT on 14,104/229,376 REAL lerp values and 103,073/1,245,184 SYNTHETIC lerp values (the latter double-confirmed by this run's re-measurement), so the condition is load-bearing; the actual control word is UNMEASURED (a runtime capture remains the falsifier - explicitly not performed, no runtime experiments)."

## X4. The PC/RC conditional model + the FLDCW chain-level fact

**Source:** `D:\Eudoria_Reconstruction\99_Audits\PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439\01_RAW\oracle_battery.json` — SHA256 `B04A3175F9E32669795D115271525E344AB823A8071171498845459D267DBFCE` — field `pcrc_conditional_model`.

### X4.1 — the PC modes compared (verbatim):

> `"PC=24_single": "the intermediate rounds to a 24-bit mantissa; the FSTP dword store is then exact -> f32(x) directly"`
> `"PC=53_double": "f32(f64(x)) - matches the DOCUMENTED Win32 process-default CW 0x027F (PC=10b double precision)"`
> `"PC=64_extended": "f32(f80(x)) - the FINIT/x87-reset default PC=11b"`

### X4.2 — the domain sensitivities (verbatim):

> `rand01_domain_r_32767: "checked": 32768, "PC24_vs_PC53_mismatches": 0, "PC53_vs_PC64_mismatches": 0`
> `position_domain_u_65535: "checked": 65536, "PC24_vs_PC53_mismatches": 0`

(The rand01 and position domains are PC-INSENSITIVE — all three PC modes agree there. The lerp/scale domains are the PC-sensitive ones; measured in the repair run, work item 2 — see X5.)

### X4.3 — the CW-modification scan facts (verbatim):

> `text_cw_bytepair_scan: "raw_d9_dd_cw_operand_pairs_in_text": 910, "caveat": "a raw byte-pair sensitivity count, NOT an instruction census (variable-length x86); an instruction-boundary walk would be required for an instruction-level claim"`
> `chain_level_static_fact: "the frozen iter035 operand census lists every FPU instruction of the 17 audited foliage-chain functions (51 instructions); NONE is FLDCW/FLDENV/FRSTOR - the audited chains do not modify the control word themselves"`

### X4.4 — the RC assumption + the unmeasured actual (verbatim):

> `"rc_assumption": "round-to-nearest-even assumed (the Win32 documented process default CW 0x027F: all exceptions masked, PC=53-bit double, RC=nearest-even). This is the PLATFORM DOCUMENTED DEFAULT, NOT a measurement of the original client."`
> `"unmeasured": "the ACTUAL runtime control word at chain-execution time (thread default + possible D3D8 FPU-mode changes if the device was created without D3DCREATE_FPU_PRESERVE) - requires an authorized runtime capture; NOT performed in this package (no runtime experiments)."`

## X5. The measured PC=24 sensitivity (the numbers the P0 resolves)

**Source:** `...\01_RAW\domain_reproof.json` — SHA256 `E654D2EF34BFF061FACF18794BE2F6A036B8BEFD847ED9308C0990F1795DEC3E` — fields `domains.lerp_scale_real`, `domains.rand01_r_32767`, `domains.positions_u16_65535`.

> `lerp_scale_real: "tag": "REAL_original_vcl_pairs", "n_pairs": 7, "lerp_checks": 229376, "lerp_engine_vs_js_mismatches": 0, "lerp_pc24_mismatches": 14104, "lerp_80bit_inexact": 0, "scale_checks": 229376, "scale_engine_vs_js_mismatches": 0, "scale_pc24_mismatches": 0`
> `rand01_r_32767: "checked": 32768, "engine_vs_js_mismatches": 0, "engine_vs_pc24_mismatches": 0`
> `positions_u16_65535: "checked": 65536, "engine_vs_js_mismatches": 0, "engine_vs_pc24_mismatches": 0`

**Reading:** under the PC=53/64 model the reconstruction is bit-exact against the 80-bit engine reference on ALL 229,376 real lerp checks + 229,376 scale checks + 32,768 rand01 + 65,536 positions (0 mismatches everywhere); under PC=24 the lerp domain diverges on **14,104 / 229,376** values (6.15%) — this is the load-bearing condition the CW measurement resolves. The synthetic-domain double-confirmation (103,073 / 1,245,184) is `pc24_synthetic_measurement.json` (SHA256 01B96D259F0FB09A6D724F8A4843938483D845736946FD73DEEBEBF4A74EA9DF; repo mirror `docs\audits\PE_M1_GATE_V4_CORRECTION_R2_20260905_101327\01_RAW\`), cited by V4 row 11 `this_run_evidence`.

## X6. The binary identity pin

**Source:** prompt §2 + CONSTANT_ADDRESS_LOCK `binary` field + offline_rechecks.json `inputs.exe`.

> `Entropia.exe — path D:\Eudoria_Reconstruction\pcg_install\Entropia.exe — SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 — 8,015,872 B — the PCG_9_3_5 client binary (read-only identity pin; never launched, never committed)`

The V4 matrix era field for rows 10/11 is `["PCG_9_3_5"]` — the measurement target is this pinned build.

## X7. The operational discipline this design inherits

- **pe-master-auditor profile §14** (REAL-RUN AUDIT SAFETY RULES; source `D:\Eudoria_Reconstruction\.opencode\agents\pe-master-auditor.md`): rule 1 control-plane != target state; rule 2 process termination requires independent proof; rule 3 the separated classes TARGET_PROCESS_EXIT / CONTROLLER_FAILURE / (session) FAILURE; rule 8 NO != UNAVAILABLE; rule 9 NOT_OBSERVED != REJECTED; rule 10 bounded capture != complete lifetime; rule 14 the ACTIVE_ORPHANED check before closure; rule 15 the machine-readable derivation chain.
- **pe-master-auditor profile §16.4** (FORECAST HEDGING): `MOST_LIKELY = strong expectation based on evidence; PLAUSIBLE = reasonable hypothesis, not yet proven; LOW_PROBABILITY = unlikely but possible. Never present a predicted cause as fact before the run proves it.`
- **pe-x32dbg-runtime skill** (source `D:\TESTAI\.opencode\skills\pe-x32dbg-runtime\SKILL.md`): the version pin (x32dbg 0.0.2.5, SHA256 822028F0...); the portable-copy discipline (run the debugger from a copy INSIDE the run tree so ini/db writes stay in allowed paths); the anti-pattern "Debugging the original binary path instead of a hash-verified sandbox copy"; the measured GUI blocker (no programmatic channel for bp-setting or log export in this environment — manual operator session, honest notes of anything not achieved); the spawn recipe (debuggee pauses at the ntdll initial system breakpoint; F9 to the entry breakpoint); breakpoint syntax `bp <VA>`; BPs set BEFORE running to entry.
