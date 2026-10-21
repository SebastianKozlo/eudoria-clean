# SELF_REVIEW_1 - pointer/frame/lifetime/CFG (AUTHOR_SELF_CHECK_NOT_INDEPENDENT)

PASS_WITH_DOCUMENTED_RESIDUALS.

1. Pointer levels: B/R_load/R_call/P_provider/VT/F_slot24/T_slot/U_getter/OUT_local/DST_copy/W_attach are declared separately in SYMBOL_BINDINGS.json. No level was equated without row proof: R_call==R_load is row-proven within span; U_getter==OUT_local is row-proven at static level under labeled balance-necessity inferences (virtual CALL EAX cleanup, 0096CF80 net-0). T_slot vs U_getter: distinct at static level (EAX at return = OUT pointer, rows 1170983+; T_slot consumed at rows 1170935-1170960); runtime aliasing formally open (noted).
2. Frame maps re-derived independently by three parties (coordinator, W001/W002/W003R workers, QC001/QC002 reviewers) with byte-exact arithmetic; one ESP-shift error in the B-source attribution (ORJ-08) was caught by QC004 and corrected (CORRECTIONS_APPLIED CA-1). The same error class was actively hunted: the correction validates the adversarial QC design.
3. Lifetime: construction zero (row 1169775) vs reader nonzero requirement (rows 180900-180931 guard) brackets the open attach window; recorded as ATTACH_DEF_USE gap, not narrated away. T_slot lifetime bounded to getter body. EDI/EBX preservation across the getter closed by full-body row coverage (PUSH/POP pairs, zero writes).
4. CFG: guards and conditional float updates recorded with rows; no inference from gaps (e.g., no claim that the getter writes OUT before row 1170983); "missing intervening paths remain unresolved" discipline enforced in every packet.
5. Residuals kept open: virtual callee cleanup class (balance-necessity only); 0096CF80 interior; derived ctor body; B-source wrapper construction (post-correction); runtime pointer equality (no capture).
6. Own-error retention: ORJ-04 source_row typo (1180000) caught and fixed before claims validation; ORJ-11 STRUCTURAL-ref schema issue caught pre-seal and converted to the predecessor's ADMITTED+premises pattern.
