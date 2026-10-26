# POINTER AND VALUE SOURCE MAP — R9
| VA | rola | status | dowod |
|----|------|--------|-------|
| 0x6b6648 | statyczny klucz Blowfish (64 B, uzyty 448 bit) | CONFIRMED_BYTES | push @0x505c76/7b; blob w obrazie |
| 0x6b6b10/0x6b7b10 | tablice S/P pi Blowfish | CONFIRMED (QC2: 1024/1024, 18/18 bajt-dokladne) | obraz |
| 0x520620/0x520fa0 | Initialize/key expansion Blowfish | CONFIRMED | A2+QC2 |
| 0x520AD0 | Blowfish DECRYPT (lancuch 8B, P[17]->P[1]) | CONFIRMED | A2+QC2 |
| 0x505ba0 | glowica funkcji otwarcia strumienia .ark | CONFIRMED | A3 (SEH prolog) |
| 0x45c9b6 | jedyny caller 0x505ba0; okolicy "/Scripts/" | CONFIRMED_BYTES (call rel32); funkcja nadrzedna CANDIDATE | root scan |
| 0x505E60 | ingest zdekodowanych chunkow; entry SEH | CONFIRMED | A1/A3 |
| 0x564890/0x564ab0 | fetch E / thunk | CONFIRMED | M1/A4/QC3 |
| 0x451730 | setter [E+0x14]=owner (produkcja X) | CONFIRMED | QC3 |
| 0x52a17f | odczyt X=M32[E+0x14] | CONFIRMED | QC3 |
| 0x417600 | get-or-create M (mapa, global [0x6c3a70]) | CONFIRMED | A3/A4 |
| 0x533740 | ctor rekordu (E weak, M strong, vtbl 0x65e648) | CONFIRMED | A5/QC3 |
| 0x46f207->0x473c90->0x451200->0x44f050 | lancuch ownera | CONFIRMED | M1/QC1 |
| templates.vfs @96532 | cell 4508 (296445,296446, f32 124.941) | CONFIRMED_BYTES; era UNKNOWN; value-source CANDIDATE | I2/QC2 |
| templates.vfs @88828 | cell 4057 (218757,218758, f32 21.2574) | CONFIRMED_BYTES; era UNKNOWN; value-source CANDIDATE | I2/QC2 |
Braki: vtable M; 0x5257c0 (konsument rekordu w 46F1A0); CODE->VM 0x508290/0x50A340; 0x520ee0; epilog 0x505ba0 (ret 8 UNVERIFIED_IN_WINDOW); glowica funkcji 0x45c9b6.