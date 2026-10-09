# ROOT_CAUSE — PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009

Finding under correction: CMO-C1 / P2 (independent Desktop post-audit of
PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009). All values below are
MEASURED by this run's PRE (`00_PRE/PRE_COUNTEREXAMPLES.json`), not quoted.

## 1. The defect, in one sentence

Both bounded x86-32 decoders of the historical package index the 32-bit GPR
table with the byte-alias index when building the writes/reads sets of
register-direct `MOV r/m8,r8` (opcode 0x88), so every HIGH byte alias
(AH, CH, DH, BH) is attributed to the WRONG parent register — concretely, a
`mov ch, bl` (88 DD) is recorded as writing EBP instead of ECX — and the
ECX-clobber scan that guards the value chain therefore cannot see a CH/CL-class
clobber of ECX; only the low-alias quarter of the alias space is correct, and
only BY COINCIDENCE.

## 2. Exact code locations (measured source, immutable)

### 2.1 Historical executor decoder — `repin_write_provenance.py` (34043 B / 45120C91…)

File: `docs/audits/PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009/03_SCRIPTS/repin_write_provenance.py`

The tables (module level):

```python
REGS = ["eax", "ecx", "edx", "ebx", "esp", "ebp", "esi", "edi"]   # line 47
R8   = ["al", "cl", "dl", "bl", "ah", "ch", "dh", "bh"]           # line 48
```

`R8` is NOT parallel to `REGS`: `R8[4..7]` (ah, ch, dh, bh) belong to parents
`REGS[0..3]` (eax, ecx, edx, ebx), but the decoder treats the R8 index as a
REGS index.

The defect sits in the `elif b0 == 0x88:` branch of `decode_instruction`
(source lines 161-175). The register-direct destination writes-set
(source line 174) and the byte-source reads-set (source line 175):

```python
            else:
                ins["writes"].add(REGS[mr["rm"]])     # line 174 — WRONG for rm=4..7
            ins["reads"].add(REGS[mr["reg"]])         # line 175 — WRONG for reg=4..7
```

For the ModRM byte `0xDD` of `mov ch, bl`: mod=11, reg=3 (BL source),
rm=5 (CH destination). The operand STRINGS stay correct
(`ins["dst"] = R8[mr["rm"]]` = "ch", `ins["src"] = R8[mr["reg"]]` = "bl",
text `mov ch, bl`), but the writes-set adds `REGS[5] = "ebp"` — the
contract's exact example: the CH operand (rm=5) treated as REG[5]=EBP in the
writes-set. A CH source on the other side is likewise recorded as reading
EBP (PRE matrix case H-0305: `mov bl, ch` measured `reads=["ebp"]`).

### 2.2 Historical QC decoder — `qc_remeasure.py` (31970 B / 4E5426AE…)

File: `docs/audits/PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009/03_SCRIPTS/qc_remeasure.py`

Same table non-parallelism (`GPR` line 88, `GPR8` line 89). The defect sits in
the `elif b0 == 0x88:` branch of `my_decode` (source lines 202-216). The
register-direct writes-set (source lines 214-215):

```python
                out["dst"] = GPR8[mr["rm"]]
                out["writes"].add(GPR[mr["rm"]] if mr["rm"] < 4
                                  else GPR[mr["rm"]])   # lines 214-215 — NO-OP
                                                        # conditional: both arms
                                                        # are GPR[mr["rm"]]
```

The `if mr["rm"] < 4 else` conditional is a no-op — both arms add
`GPR[mr["rm"]]`, so CH (rm=5) again writes `GPR[5] = "ebp"`. Additionally the
register-direct byte SOURCE parent is never added to `reads` at all (line 216
sets the `src` STRING only): a second, distinct defect facet — the QC reads-set
is MISSING the byte-source parent in every register-direct 0x88 case
(PRE-measured: 0/64 cases record the source parent).

### 2.3 The downstream consumer that turns the defect into a false PASS

The historical ECX-clobber scan (executor `main()` source lines 444-446;
QC `main()` nested `writers_between`, source lines 497-499, called at
line 509) lists writers of "ecx" in the reaching-definition interval
(0x0085B24B, 0x0085B27A). Because the CH mutant is filed under "ebp", the scan
returns [] — the historical provenance guard cannot see the clobber.

## 3. PRE-measured reproduction (this run; historical implementations,
## AST-extracted, top-level never executed)

| Case | Implementation | Mutation-site decode (measured) | ECX scan (verbatim historical scan) |
|---|---|---|---|
| PRE-EX-CLEAN | executor | `D9 E8` `fld1`, writes=[] | [] (TRUE no-clobber) |
| PRE-QC-CLEAN | QC | `D9 E8` `fld1`, writes=[] | [] (TRUE no-clobber) |
| PRE-EX-CH (88 DD) | executor | dst `ch`, src `bl`, text `mov ch, bl`, **writes=["ebp"]**, reads=["ebx"] | **[] (FALSE EMPTY — false PASS)** |
| PRE-QC-CH (88 DD) | QC | dst `ch`, src `bl`, **writes=["ebp"]**, reads=[] (source parent missing) | **[] (FALSE EMPTY — false PASS)** |
| PRE-EX-CL (88 D9) | executor | dst `cl`, writes=["ecx"] (low-alias coincidence) | DETECTED @0x0085B24D |
| PRE-QC-CL (88 D9) | QC | dst `cl`, writes=["ecx"] (coincidence) | DETECTED @0x0085B24D |

All six cases decode 64 instructions ending exactly at 0x0085B290
(the 2-byte mutation is length-preserving in the 2-byte `fld1` slot).
Supplementary non-historical evidence: an EBP-writer scan over the same
interval on the CH mutant returns [0x0085B24D] — the clobber exists, it is
merely misfiled under EBP.

The false PASS, precisely: the scan that guards the ECX reaching definition
returned [] on a mutant that physically writes CH (ECX bits [8,16)); any
historical provenance conclusion built on this scan would PASS on the mutant.

## 4. Blast radius (PRE-measured historical 8x8 census, 64 cases x 2 decoders)

For the complete register-direct `88 /r` mod=11 matrix (dest 0-7 x source 0-7,
2-byte instructions, decoded under x86-32 rules against an independent
reference table):

- Historical EXECUTOR: writes parent correct in 32/64 cases (exactly the
  dest 0-3 = AL/CL/DL/BL cases — coincidence), WRONG in 32/64 (dest 4-7:
  AH→esp, CH→ebp, DH→esi, BH→edi instead of eax/ecx/edx/ebx); reads parent
  correct in 32/64 (source 0-3), WRONG in 32/64 (source 4-7 same misfiling);
  BOTH correct in exactly 16/64 (dest<=3 AND source<=3).
- Historical QC: writes parent correct 32/64 / wrong 32/64 (identical
  pattern); register-direct SOURCE parent recorded in 0/64 cases (missing in
  all 64).
- Example rows (measured): H-0503 `mov ch, bl` — EX writes ["ebp"] /
  QC writes ["ebp"]; H-0305 `mov bl, ch` — EX reads ["ebp"] (the CH SOURCE
  misfiled as an EBP read, the exact reads-side facet of CMO-C1);
  H-0707 `mov bh, bh` — EX writes ["edi"], reads ["edi"] (should be ebx/ebx).

## 5. Why the historical run did not catch it (measured fact, not excuse)

The examined 224-byte window contains exactly five 8-bit/16-bit store-class
instructions with byte/word sources: the four memory-form
`88 9E 9C/9D/9E/9F 00 00 00` (`mov [esi+0x9c..0x9f], bl`) and the
16-bit `66 89 9E A0 00 00 00` (`mov [esi+0xa0], bx`). Their byte source BL is
a LOW alias whose parent (EBX) coincides with `REGS[3]`; no high alias and no
register-direct 0x88 form exists physically in the window. The historical
executor's writes/reads were therefore coincidentally correct for every
physical instruction decoded — the defect is LATENT in the historical scope
and is exposed only by the synthetic high-byte counterexample (the Desktop
post-audit's CH mutant, reproduced independently by this run's PRE).
The historical QC additionally never recorded the BL source read of the four
physical `88 9E` stores (register-form defect facet; their base-register read
ESI was recorded), which did not affect any historical conclusion because the
historical scans only consumed WRITER sets.

## 6. The fix (contract section 4; see 03_SCRIPTS/corrected_executor_decoder.py)

- Parent map for ALL EIGHT aliases: AL→EAX, CL→ECX, DL→EDX, BL→EBX,
  AH→EAX, CH→ECX, DH→EDX, BH→EBX; applied to the writes-set (destination)
  and the reads-set (source) of opcode 0x88, in both register and memory
  forms.
- Three properties distinguished per byte operand: exact byte-register
  operand NAME (dst/src strings, preserved unchanged); PARENT general-purpose
  register (the writes/reads sets); actual WIDTH/bit-range (width=8; low
  aliases [0,8), high aliases [8,16)).
- A partial-byte write CLOBBERS the parent register for reaching-definition
  purposes but is NOT a full 32-bit overwrite — recorded explicitly via
  width/bit-range fields; the writes-set convention (parent) implements the
  clobber semantics without asserting a 32-bit overwrite.
- Preserved unchanged: instruction lengths, ModRM/SIB interpretation,
  destination strings, text rendering, all other supported opcode behavior,
  fail-closed DecodeError on unsupported opcodes (controlled failure, never
  silent acceptance). The decoder remains a bounded window decoder, NOT a
  general x86 emulator. This correction does NOT establish
  GENERAL_X86_DECODER_CORRECTNESS or GENERAL_UNSUPPORTED_FORM_FAIL_CLOSED.

## 7. Non-goals (scope)

No claim about the historical scientific result changes: the corrected decoder
must reproduce the historical 64-instruction clean decode IDENTICALLY
(verified in POST C6). No new science, no new bodies, no field semantics, no
sibling-store analysis, no arg1 upstream — see PREREGISTRATION section 5.
