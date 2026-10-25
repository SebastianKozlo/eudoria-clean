# MODEL_CASE_296445
Model: 296445.nif (wariant 2003: 108876 B, NetImmerse 4.1.0.12, SHA256 656795D8B3DDDF8F9192EE41C4710D592894860F6959B53B2C08036977E7B862)

## Stan wiedzy po R4
- Wariant 2003 byte-identical w 4 korpusach lokalnych: COT Jan 2003 Models.ark (F660D055...), pcg_install Models.bnt (C950A8C2...), pcg915 Models.bnt (4878C016...), EU 2008 Models.bnt (1322ADF2...). Wszystkie eralabel DIFFERENT corpus vs ISO 5.1.0.0 (wariant przetrwał jako legacy member).
- Wydanie ISO 5.1.0.0: payload NIE zawiera archiwum modeli; jednostka PE_PCG.ark (Download.data) nieobecna lokalnie i bez konsumenta w korpusie binarnym; ClientLoader 5.1.0.0 pobiera FullDat_%d.ark/Dat%d_%d.ark wg wersji.
- SOURCE_SPECIFIC_ISO_MODELS: UNKNOWN — nie udowodniono, że ten wariant pochodzil z PE_PCG.ark wydania ISO ani z FullDat/Dat.

## Łańcuch klienta 5.1.0.0 (COMMON, per-model join otwarty)
mount models.ark (0x45ED7D) -> member-open 0x59E2D0 (lowercased filename) -> loader .nif 0x42E990/ROOT 0x423280 -> fabryka 0x4578E0 (6 arg x,y,z,rx,ry,rz) -> SFO writer 0x46E990 -> sinki x100/Euler/scale. Proveniencja wartości: UNVERIFIED (indirect dispatch). Transformacje model-local w samym NIF: 19 NiNode + 30 NiTriShape + 7 Billboard, skale 82/82=1.0 — NIE world placement.

## Następne kroki (ranking)
1. [renderer+0x28] identity + entry-set producer — dynamic trace poza statyką; wymaga decyzji człowieka o kampanii dynamicznej.
2. Pozyskanie PE_PCG.ark / FullDat 5.1.0.0 z archiwów zewnętrznych (wymaga autoryzacji człowieka — kampania statyczna nie pobiera plików gry).
3. templates.vfs (era UNKNOWN) — dekodowanie strukturalne; referencje 296445@96552.
