# MODEL_CASE_218757
Model: 218757.nif — DWA warianty fizycznie rozdzielone:
- wariant 2003: 56535 B, NetImmerse 4.1.0.12, SHA256 C13D08736D7E778803E20A3105067448007F32D15290AF168F836CD99248AD98 — wyłącznie w COT Jan 2003 Models.ark (wszystkie kopie F660D055).
- wariant późniejszy: 57316 B, Gamebryo 10.1.0.0, SHA256 3E8A22C2213202207E374B55CD65B2C3BE039CCDD1E8D01A07FCAF44DE12CF36 — pcg_install/pcg915/EU2008 Models.bnt.

## Stan wiedzy po R4
- Kontrakt zachowany: późniejszy wariant NIE zastępuje wariantu 2003 (korekta C01 potwierdziła: EU 2008 trzyma wyłącznie wariant późniejszy).
- SOURCE_SPECIFIC_ISO_MODELS: UNKNOWN (jak dla 296445; brak lokalnej jednostki modelowej wydania ISO).
- templates.vfs referuje ID (u32@88848), era UNKNOWN.

## Łańcuch klienta 5.1.0.0: jak w MODEL_CASE_296445 (COMMON mechanism; per-model def 5.1 niedostępny — brak Models.ark 5.1.0.0; NIE wolno zamykać joinu przez podstawienie def z innej ery).
- Transformacje model-local wariantu 2003: 12 NiNode zero/identity + 14 NiTriShape (7 nonzero T), skale 82/82=1.0 — NIE world placement.

## Następne kroki: jak 296445 (wspólny mechanizm); dodatkowo wariant 2003 istnieje tylko w jednym korpusie — priorytet backup/dowolne dodatkowe źródła COT-era.
