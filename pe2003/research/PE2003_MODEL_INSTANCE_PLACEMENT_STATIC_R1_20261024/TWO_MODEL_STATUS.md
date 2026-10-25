# TWO_MODEL_STATUS — PE2003_MODEL_INSTANCE_PLACEMENT_STATIC_R1_20261024

## Model 296445.nif (definition 4508, "Slum_Building_b047" family)
- Identity: 108876 B, SHA256 656795D8B3DDDF8F9192EE41C4710D592894860F6959B53B2C08036977E7B862 (PE42_EN_80553A75); resource ids 296445 (.nif) + 296446 (.bvi); DYN properties 296478 (+F8) / 296477 (+A4); getters return native property-registry keys in VM register C.
- Construction chain (byte-proven): UDP definition -> registry -> VM execution -> 'Root Model' name op -> root lookup (ext 122867, def 4652) -> 26 mesh parts (stride-256 table, ids 126743..126779) -> per-part component (ext 122888, def 4653) -> ATTACH (ext 30298, def 1796 forwarder) -> ext 33521 class 2202 [bytecode NOT in local corpus = static boundary].
- Instance: no local corpus definition instantiates it (census 1936 negative); instance creation is native get-or-create (FUN_0051f6e0) + batch ScriptInsert (case 15497) fed by VM descriptors.
- Transform: NO positional constant anywhere in its bytecode or EXTN path; world position NOT in any local static channel examined.
- WORLD_XYZ_RECOVERED = NO; HISTORICAL_PLACEMENT = NOT_ESTABLISHED (locally); PLACEMENT_VALUE_SOURCE = NOT_FOUND_IN_LOCAL_STATIC_SCOPE.

## Model 218757.nif (definition 4057, "Outpost_me01_Ext" family)
- Identity: 56535 B (2003 variant C13D08736D7E778803E20A3105067448007F32D15290AF168F836CD99248AD98; NOT the later 3E8A22C2... variant); resource ids 218757 (.nif) + 218758 (.bvi); DYN 218784 (+68) / 218783 (+14).
- Construction chain: identical mechanism; 18 mesh parts; 8 fixup slots; ATTACH ext 30298 identical (same class-2202 boundary).
- Instance/transform: same negatives as 296445 (census self-only).
- WORLD_XYZ_RECOVERED = NO; HISTORICAL_PLACEMENT = NOT_ESTABLISHED (locally); PLACEMENT_VALUE_SOURCE = NOT_FOUND_IN_LOCAL_STATIC_SCOPE.

## Mechanism recovered (shared, byte-proven)
Root placement channel EXISTS for dynamic entities (record[6] flag): message struct 0x48 -> entity class 0x118 -> FUN_005030c0 writes node translation (x,y,z x100.0f) + rotation (euler radians -> 3x3, transposed). Whether building definitions ever arrive flagged record[6] is server-side data — undecidable statically. Statics' placement therefore remains a runtime/server question (second human job's channel), NOT a local 2003 file question.
