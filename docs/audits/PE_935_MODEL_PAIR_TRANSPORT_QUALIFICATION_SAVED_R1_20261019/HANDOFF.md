# HANDOFF — run PE_935_MODEL_PAIR_TRANSPORT_QUALIFICATION_SAVED_R1_20261019

Zwrot do PE-MASTER (rodzic) / przyszłych runów:
- Mechanizm pair-transport: H1 CONFIRMED (synchroniczne collect→sort→dedupe→project; global sink 0xBA45E8); H2 REJECTED w łańcuchu; H3 ograniczone do domeny par (nieznana semantyka).
- CALLBACK 008BD720 przypięty immediate w 006C3FB0 (callsite 006C3F50).
- MEMBER_VIEW: 0040B070=param+0x14; provenance same-aggregate-declared, program-identity UNVERIFIED.
- PAIR_FRAME_TO_PROJECTED: NOT_ESTABLISHED (rodzeństwo w jednym kontenerze — nowy fakt).
- Kontener: 3 stackowe w 006C4060 (statyczne tablice id 0xA855F0/0xA858B8/0xA858C0) + global 0xBA45E8 (final sink).
- Konsumenci: 006C3D40 sort, 006C2C90 dup-find, 006C2C50 (opaque), 006C36B0→0xBA45E8; dalsze — open edge za 006C4160.
- Fallback SceneFeeder: odrzucony (PIVOT_RECORD.json).
- Następny krok (przyszły kontrakt): dokończenie 006C4060 i konsumenci globala 0xBA45E8; ewentualnie 006C29D0 (transform pary→DWORD). Nowy eksperyment na oryginale/runtime: NIEAUTORYZOWANY.
- Budżety actuals: 21/24 ciał, 419/4800 wierszy, 26/160 CALL, 22/24 warianty, 15/1000 body-lines.