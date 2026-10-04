# ALTERNATIVE_BRANCH — PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004

MAX_ALTERNATIVE_BRANCHES_ANALYZED = 1 (used): the flag-0xD82 alternative of
FUN_004C5480. Kept SEPARATE from the audited normal-branch semantics; no
claim about the alternative's value provenance is merged into the normal
branch's verdicts.

## The branch predicate (byte-pinned)

```
PUSH 0xD82            @0x004C54DD   (68 82 0D 00 00)
MOV ECX,EDI           @0x004C54E2   (this = the ORIGINAL entity, arg1)
CALL FUN_00844020     @0x004C54E4   (the established attribute-flag reader)
TEST AL,AL            @0x004C54E9
JE 0x004C5518         @0x004C54EB   ← flag NOT set → THE AUDITED NORMAL BRANCH
```

FUN_00844020 (narrow recheck of the prior-package-established reader:
`8B 49 04; 85 C9; ...; 50; CALL tree-find; 84 C0; ...`) resolves the entity's
flag 0xD82. Flag CLEAR (AL==0) → normal branch. Flag SET (AL!=0) → the
alternative below.

## The alternative path (bounded decode)

```
0x004C54ED: LEA EDX,[ESP+0x14]; MOV ECX,EDI
0x004C54F4: CALL FUN_00843DD0     (receiver tree resolve — SAME function as
                                    the pre-selector resolve)
0x004C54F9: PUSH EAX
0x004C54FA: CALL FUN_007292F0     (surface read only: takes the resolved
                                    receiver; internally PUSHes 0x23D6=9174
                                    and calls a further helper — NOT decoded)
0x004C54FF: ADD ESP,4
0x004C5502: TEST AL,AL
0x004C5504: JNE 0x004C5518        ← SUB-OUTCOME 1: joins THE AUDITED NORMAL
                                     BRANCH (the tag-6 getter + value-table
                                     key derivation THEN RUNS on this path)
0x004C5506: MOV ECX,EDI; CALL FUN_004123D0   (8B 01 C3 — returns [entity])
0x004C550D: PUSH EAX; CALL FUN_00843340      (SEH function — NOT decoded)
0x004C5513: ADD ESP,4
0x004C5516: JMP 0x004C5550        ← SUB-OUTCOME 2: the function RETURNS
                                     FUN_00843340's result (ESI=EAX at the
                                     convergence point 0x004C5550), i.e. a
                                     DIFFERENT template source that NEVER
                                     consults the tag-6 getter, the value
                                     table, or FUN_0072F880.
```

## Bounded findings

1. The alternative is NOT a single semantics: it has two sub-outcomes.
   - Sub-outcome 1 (FUN_007292F0 TRUE) CONVERGES with the audited normal
     branch — so SOME flag-0xD82-set executions still derive the lookup key
     through the audited tag-6 chain. The normal-branch verdicts therefore
     describe the shared key-derivation segment, not only the flag-clear
     population.
   - Sub-outcome 2 (FUN_007292F0 FALSE) bypasses the entire audited chain and
     returns FUN_00843340([entity]) directly as the "template object".
2. FUN_007292F0's embedded constant 0x23D6 (= 9174) is recorded
   RAW_OCCURRENCE_ONLY (locator discipline; no registry/record role claimed;
   the function was not decoded).
3. FALLBACK_BRANCH_PROVENANCE (the descriptor-invalid path @0x004C5549, also
   reached from the normal branch itself): CALL FUN_00977780 → `MOV EAX,
   0x00BA9374; RET` → MOV EAX,[EAX] @0x004C554E reads [0x00BA9374] — the
   .data VIRTUAL TAIL with ZERO direct .text writers (census in
   01_RAW/S5_CREATOR_DECODE.json) → NULL → FUN_004C5580 aborts at
   JE 0x004C5AB6. Classification: STATIC_FALLBACK (a permanently-zero static
   object; produces NO lookup key, only a NULL getter result).
4. No deeper decode of FUN_007292F0 / FUN_00843340 / FUN_004123D0 was
   performed (budget); their value provenance remains UNKNOWN/NOT_ANALYZED
   beyond the surface reads recorded here.
