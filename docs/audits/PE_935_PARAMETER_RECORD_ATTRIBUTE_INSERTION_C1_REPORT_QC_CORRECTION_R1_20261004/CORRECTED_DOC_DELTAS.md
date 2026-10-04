# CORRECTED_DOC_DELTAS — PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_C1_REPORT_QC_CORRECTION_R1_20261004

Per-file delta record for the narrowly corrected R1 package docs
(`docs/audits/PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004/`). Every
change below is one of the ordered C1/C2/P3 corrections only; nothing else in the
package was touched. BEFORE quotes are verbatim from parent commit
`4c1205342abd1b051f72fab9932532b1f0ed86fe` (the original evidence of each mistake is
preserved there and in git history — nothing was deleted). The full machine diff of
this correction is reproducible with
`git diff 4c12053 <this commit> -- docs/audits/PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004`.

Files changed (8): FINAL_REPORT.md, HANDOFF.md, PARSER_CHAIN.md, PLACEMENT_CONSUMER_EDGE.md,
QC_REPORT.md, RECEIVER_INSERTION_CHAIN.md, RECORD_A.md, RECORD_B.md.
Files NOT changed: 01_RAW/* (all five JSONs), 03_SCRIPTS/* (all six scripts),
PARAMETER_FILE_INVENTORY.csv, SELECTED_FILE.md, INPUT_IDENTITIES.md,
COMMITTED_PACKAGE_MANIFEST_SHA256.csv (R1 historical manifest — the record of the
R1 publication's file states; the corrected files' new identities are in THIS
package's manifest).

## PARSER_CHAIN.md (C1 + P3)

1. BEFORE: "Fast-path pattern per field: bounds check ...; a flag-checked slow path
   (`CMP [ESI+0x11],BL`) handles the other cursor mode and stores the same value to
   the SAME destination (both paths verified)."
   AFTER: normal-path pattern (flag gate + bounds + read + store + FUN_0040DE60 with
   its byte-decoded flag-zero-on-exceed behavior), then the C1-CORRECTED failure-path
   description: ZERO-WRITE to the same destination on flag/bounds failure
   (MOV [EDI],EBX @0x00730CC3; MOV [EDI+8],EBX @0x00730CF0; MOV [EDI+4],EBX
   @0x00730D1E; MOV [EDI+0xC],EBX @0x00730D4C; D via FLDZ @0x00730D7A + FSTP
   @0x00730D7C; no cursor advance; flag re-cleared), explicitly SUPERSEDING the
   same-value claim as FALSE.
2. BEFORE: "Destinations (verified in QC-7 by re-parsing RECORD_A/RECORD_B raw bytes
   and matching the established historical anchors):"
   AFTER: "Destinations ([C1-corrected verification claim] byte-verified against the
   pinned-EXE store instructions by the correction package's
   CLIENT_DESTINATION_MAPPING_CHECK ... The R1 QC-7 gate verified only the PAYLOAD
   FIELD VALUES at fixed file offsets (PAYLOAD_FIELD_DECODE_CHECK) — it did NOT read
   these destination instructions; the independent Desktop post-audit proved that a
   deliberate A/B destination swap in this table still passes it ... which retracts
   the prior claim that QC-7 verified the destinations)".
3. Table rows (P3 instruction starts):
   BEFORE "MOV [EDI+0x04],EAX @0x00730D16" → AFTER "MOV [EDI+0x04],EAX @0x00730D14";
   BEFORE "MOV [EDI+0x0C],EAX @0x00730D36" → AFTER "MOV [EDI+0x0C],EAX @0x00730D42";
   BEFORE "FLD [EDX+EAX] @0x00730D6D; FSTP [EDI+0x10] @0x00730D70" → AFTER
   "FLD [EDX+EAX] @0x00730D69; FSTP [EDI+0x10] @0x00730D70".
4. Added note block under the table documenting the three instruction-start
   corrections with byte encodings (89 47 04 / 89 47 0C / D9 04 10) and that the
   A→+0x08 / B→+0x04 PAIRING itself is unchanged; only the automatic-verification
   claim is retracted.

## RECORD_A.md (P3)

1. Decode-table rows: BEFORE "@0x00730D16" → AFTER "@0x00730D14" (B store);
   BEFORE "@0x00730D36" → AFTER "@0x00730D42" (C store);
   BEFORE "FLD [EDX+EAX]; FSTP [EDI+0x10] @0x00730D6F" → AFTER
   "FLD [EDX+EAX] @0x00730D69; FSTP [EDI+0x10] @0x00730D70".
2. Added [C1/P3 correction] bullet noting the corrected starts, the byte encodings,
   the unchanged destination pairing, and the pointer to the C1 correction package.

## QC_REPORT.md (C1 + C2 + P3)

1. QC-7 row: BEFORE "Parser raw↔decoded roundtrip: ... re-parsed from raw bytes with
   the byte-decoded destinations ..." → AFTER "PAYLOAD_FIELD_DECODE_CHECK
   ([C1-corrected name and scope; formerly mislabeled 'Parser raw↔decoded roundtrip'
   — it does NOT read the client's destination instructions]): ... SCOPE LIMIT (C1):
   the payload→template-field DESTINATION mapping is NOT verified by this gate — it
   is verified by the correction package's CLIENT_DESTINATION_MAPPING_CHECK
   (pinned-EXE store instructions + A/B mutation falsifier)".
2. QC-8 row: BEFORE "node size 0x44 @0x0072F825" → AFTER "node size 0x44 @0x0072F822
   (C1/P3-corrected from @0x0072F825 — the in-run script already pinned the bytes at
   0x0072F822; the doc row's address was wrong)"; added "(MOV EAX,0x00BA5800 starts
   @0x0072F5A5 — C1/P3-corrected from @0x0072F5A8)".
3. QC-9 row: BEFORE "0x4E26 store @0x004C54C2" → AFTER "class-selector 0x4E26 store
   @0x004C54C2 (C2-corrected role label: CLASS_SELECTOR constant, not a property id)".
4. QC-10 row: BEFORE "PUSH 0x119C sites = 0 → no static 4508 lookup key" → AFTER
   the measured-scan-scope wording (PUSH 0x119C sites = 0 in the performed scan;
   computed/indirect/runtime-produced 4508 keys NOT excluded; no absence claim beyond
   the measured scan).
5. ANTI-CIRCULARITY #1 FAILURE_CASE: BEFORE "a wrong destination pairing would have
   broken the RECORD_B anchor match (detected by QC-7 if so)" → AFTER the honest
   counterexample record (the Desktop proved the swap passes QC-7; QC-7 never reads
   the destination instructions) and the new detection duty assigned to the
   correction package's CLIENT_DESTINATION_MAPPING_CHECK + mutation falsifier.
6. ANTI-CIRCULARITY #4: BEFORE "the 0x4E26 store instruction + the property-machinery
   call targets" → AFTER "the class-selector 0x4E26 store instruction + the
   class-selector-resolve (FUN_00703B80 @0x004C54CE) and property-tag-6-getter
   (PUSH 6 @0x004C551F → FUN_0070C180 @0x004C5523) call targets ([C2-corrected
   layering: CLASS_SELECTOR 0x4E26=20006 vs PROPERTY_TAG 6 ...])".
7. Deviations note 7 added: the C1/C2/P3 correction of record pointing at this
   package's supersession ledger, explicitly noting the R1 raw JSON evidence was
   NOT altered.

## RECEIVER_INSERTION_CHAIN.md (P3)

1. Receiver pointer provenance bullet: BEFORE "The reader loop fetches the registry
   via FUN_0043A550 and keeps it at [ESP+0x3C] (MOV ECX,[ESP+0x3C] @0x0072FBD4 before
   the insert call @0x0072FBE5)." → AFTER the [C1/P3-corrected] wrapper→loader
   provenance: FUN_00452490 (CALL FUN_0043A550 @0x00452490 → MOV ECX,EAX @0x00452495
   → tail JMP FUN_0072FA30 @0x00452497); the loader PRESERVES the incoming ECX
   (MOV [ESP+0x38],ECX @0x0072FA6B — byte-verified, with the Desktop's @0x0072FA6C
   identified as the ModRM byte) and recovers it before the insert; the loader does
   NOT itself call the singleton (no FUN_0043A550 call site inside FUN_0072FA30,
   E8 census); "The same singleton feeds every OTHER consumer censused this run".
2. Node-size line: BEFORE "(`MOV [EBP-0x14],0x44` @0x0072F825 in FUN_0072F7F0 ...)"
   → AFTER "(`MOV [EBP-0x14],0x44` @0x0072F822 in FUN_0072F7F0 ...; C1/P3-corrected
   instruction start — @0x0072F825 was mid-instruction; the R1 QC script's byte check
   already read C7 45 EC 44 at 0x0072F822)".
3. Lookup default: BEFORE "miss default `MOV EAX,0x00BA5800` @0x0072F5A8" → AFTER
   "miss default `MOV EAX,0x00BA5800` @0x0072F5A5 — C1/P3-corrected instruction
   start; @0x0072F5A8 was the operand byte".

## PLACEMENT_CONSUMER_EDGE.md (C2 + P3)

1. Chain-2a block: BEFORE "reads the entity's 0x4E26-PROPERTY value = the id2:
   FUN_00843DD0 @0x004C54AD (tree resolve; MOV ECX,[ECX+4] + find)
   MOV [ESP+0x1C],0x4E26 @0x004C54C2 ← the 20006-family property id
   CALL FUN_00703B80 @0x004C54CE (property machinery via FUN_00415470)
   → returns the id2 (null-checked; flag 0xD82 path also present)" → AFTER the
   C2-corrected five-step layered chain: (1) exact receiver (resolver CALL
   FUN_00843DD0 @0x004C54B2 — corrected start; MOV EAX,[EAX] @0x004C54B7);
   (2) CLASS_SELECTOR 20006 (0x4E26 pair @0x004C54C2 + receiver @0x004C54CA,
   resolved by the wrapper CALL FUN_00703B80 @0x004C54CE — a CLASS-SELECTOR-20006
   resolve operation, NOT a property-tag fetch of 20006); (3) branch predicate with
   the flag-0xD82 alternative preserved SEPARATE/UNKNOWN (PUSH 0xD82 @0x004C54DC →
   FUN_00844020 @0x004C54E4); (4) PROPERTY_TAG 6 getter on the audited normal
   branch (MOV ECX,[EAX+4] @0x004C551C; PUSH 6 (6A 06) @0x004C551F; CALL
   FUN_0070C180 @0x004C5523 → descriptor/variant null-check TEST ECX,ECX
   @0x004C552B; predicate CMP ECX,1 @0x004C552F; value read MOV EAX,[EAX+8]
   @0x004C5539); (5) the returned RUNTIME VALUE — with the explicit caveat that NOT
   every getter result comes from the normal tag-6 branch.
2. Verdict paragraph: BEFORE "**but the lookup KEY is a runtime value** (the entity's
   0x4E26-property id2)" → AFTER "... (the value returned by the
   class-selector-20006 / property-tag-6 getter on the exact receiver and branch —
   a SPECIFIC getter result, not any 20006-family constant)".
3. FIRST_MISSING_EDGE: BEFORE "(FUN_004C5480's 0x4E26-property id2 → FUN_0072F880):
   who WRITES the 0x4E26-property value on the entity ..." → AFTER the C2-corrected
   wording: the provenance of the SPECIFIC RUNTIME VALUE returned by the
   class-selector-20006 / property-tag-6 getter on the EXACT receiver and branch.
4. NEXT EXPERIMENT: BEFORE "Decode the WRITERS of the 0x4E26 (20006-family) property
   value — the property-write counterparts of the FUN_00703B80/FUN_0042EAD0
   property machinery — and determine their data sources." → AFTER the C2-corrected
   specific-getter-result provenance experiment with the OPEN taxonomy
   (PHYSICAL_RECORD_DERIVED | CONSTANT_INITIALIZATION | LOCAL_COMPUTED |
   CACHE_PROVIDER | MESSAGE_DERIVED | FALLBACK_BRANCH | UNKNOWN) and the
   SEPARATE/UNKNOWN fallback-branch preservation. RAW_OCCURRENCE_ONLY note kept
   unchanged.

## FINAL_REPORT.md (C2 + P3)

1. Builder-chain bullet: BEFORE "(via its deriver FUN_004C5580 @0x005678BA →
   FUN_004C5480: the entity's 0x4E26-property id2 → FUN_0072F880 ...)" → AFTER the
   C2-corrected identity (the runtime value returned by the class-selector-20006 /
   property-tag-6 getter on the exact receiver and branch).
2. Negative-control paragraph: BEFORE "NO static 4508 key exists (all 3 imm32 hits
   are ESP/struct displacements; 0 PUSH sites)" → AFTER the measured-scan-scope
   wording (zero PUSH-imm32 0x119C sites in the performed scan; 3 imm32 occurrences
   classified as displacement operands; computed/indirect/runtime 4508 keys NOT
   excluded; the control still discriminates within the measured classes).
3. FIRST_MISSING_EDGE + recommended experiment section: BEFORE "(FUN_004C5480's
   0x4E26/20006-family property value → FUN_0072F880). Recommended experiment:
   decode the WRITERS of the 0x4E26-property value ..." → AFTER the C2-corrected
   specific-getter-result provenance with the OPEN taxonomy and the
   SEPARATE/UNKNOWN fallback-branch caveat.
   NOT changed: TERMINAL FIELDS block, the S1 verdict text, forbidden-overclaim
   census, evidence index, honest boundaries.

## HANDOFF.md (C2 + P3)

1. Result paragraph: BEFORE "(the entity's 0x4E26-property id2) → FUN_0072F880" and
   "FIRST_MISSING_EDGE = ... (the 0x4E26-property-key provenance)" → AFTER the
   C2-corrected layered identity and the specific-getter-result provenance wording.
2. Next experiment: BEFORE "Decode the WRITERS of the 0x4E26 (20006-family) property
   value — the property-write counterparts of the FUN_00703B80/FUN_0042EAD0
   machinery — to determine the provenance of the runtime id2 key ..." → AFTER the
   C2-corrected specific-getter-result provenance with the OPEN taxonomy and the
   fallback-branch caveat. Adjacency lead kept.
3. Boundaries honored: BEFORE "no proprietary payload committed (originals
   represented by era, path, size, SHA256, offsets, bounded window hashes)" →
   AFTER the C1/P3-corrected census: no complete original proprietary
   binary/payload FILES committed; bounded original byte windows / payload excerpts
   used as forensic evidence ARE present (RECORD_A/B payload hex, bounded EXE
   windows in 01_RAW); no NEW proprietary payload beyond those bounded evidence
   excerpts.

## RECORD_B.md (P3)

1. Control item 3: BEFORE heading "**No static key**: ... The PUSH-imm32 scan found
   ZERO `PUSH 0x119C` sites. No placement-construction function looks up key 4508
   statically — the discriminating contrast ..." → AFTER heading "**Measured 4508
   scan scope** ([C1/P3-corrected wording — supersedes the heading 'No static key'
   and its broad absence claim]": zero PUSH-imm32 sites in the performed scan; the 3
   imm32 occurrences classified as displacement operands; SCOPE LIMIT:
   computed/indirect/runtime-produced 4508 keys NOT excluded; NO absence claim
   beyond the measured scans; the discriminating contrast stands, as measured.
2. Control verdict: BEFORE "...is read on the model-request path (runtime-keyed) and
   NOT by any placement-construction lookup with a static key" → AFTER "...within
   the censused machinery and the measured scan classes, is read on the model-request
   path (runtime-keyed) and NOT by any censused placement-construction lookup with a
   static key".

## Verification of the deltas

Every corrected statement above is byte-verified from the pinned Entropia.exe by
03_SCRIPTS/qc_targeted.py (01_RAW/QC_TARGETED.json TQ2/TQ3/TQ4/TQ5/TQ6) and the
wording is verified by TQ7/TQ8/TQ9; the A/B mutation falsifier
(01_RAW/QC_MUTATION_AB_SWAP.json) proves the new CLIENT_DESTINATION_MAPPING_CHECK
fails on the swapped documentation mapping while the raw VFS values stay unchanged.
