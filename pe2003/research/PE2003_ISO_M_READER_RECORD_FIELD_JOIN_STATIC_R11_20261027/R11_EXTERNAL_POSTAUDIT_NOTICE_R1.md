# R11 external postaudit notice R1 (additive; published by R12)

This notice is ADDITIVE: no R11 file, manifest row or ENTRYPOINT line is modified by this change. R11's published history is NOT rewritten; its bytes stand as published. This notice records the R12 static findings that falsify or supersede specific R11 statements, so that downstream readers do not carry them forward as standing evidence.

## Scientific corrections from R12 (STATIC_ONLY, same image: section1.bin SHA256 D43A23B9...3631)

1. Receiver-claim falsification: 0x402650 is a 4-byte getter (it computes &S+0x1C and returns with a plain ret) and CANNOT consume the ".cfg" string; the actual receiver-qualified ".cfg" consumer is 0x401260 (stack ledger from the saved S6 rows).
2. The population S at callsite 0x401140 = CONFIRMED configuration (the filename builder `<member S+0x1C>+".cfg"`); the constants 1024/768/32/30000 remain hints only; E_builder = instance data; the S/E_builder populations are pushed away from placement (E_fetch untouched).
3. 0x52F290's return value is its receiver: the R11 residual "return value = same fresh 0x3C block" is resolved NEGATIVELY; the 0x3C subobject lives at receiver+0x08.
4. 0x447B20 is closed as a structural visitor; the bounded "query/detach-style" reading of R11 is superseded as a whole-function role (the releases are refcount cleanup of temporaries); the class identities remain open (runtime-initialized nodes).

## Process note

R11's post-seal PUBQC write into the science-tree jobs area (144 files vs 143 expected) is preserved as history; the ambiguity was partly contract wording. R12 and later runs route all post-seal publication QC exclusively to the receipt root and re-verify the sealed science tree after publication. No R11 file is modified by this notice.

Advisory; CANONICAL_GATE_EFFECT=NONE.
