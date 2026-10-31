# BVI_STRUCTURE — Stage D (PE_WORLD_R2_PLACEMENT_SOURCE_R1_20261031)

Era: PCG_9_3_5. Źródło: `D:\Eudoria_Reconstruction\pcg_install\Data\Volumes\Volumes.bnt`
(SHA256 = 6AD8BA3C…BAC09, zweryfikowany). Kontener: BNT2 (trailer `[u32 index_start]["BNT2"]`;
indeks `[u32 count][count × {nazwa\0A, u32 packed, u32 offset, u32 c, u32 d}]`;
round-trip pełny do traileru; c == d dla każdego wpisu — zgodne z konwencją CRC32×2).
Payloady: NIESKOMPRESOWANE (raw bytes @offset, packed_size bajtów; wysokie entropie typowych
f32 potwierdzają brak zlib; brak nagłówka 02 00 00 FF).

## Census rodzajów (pełny korpus 1865 plików; 01_RAW/CORPUS_HEADER_CENSUS.json)

| Rodzina | Kryterium nagłówka | Liczba | Walidacja strukturalna |
|---|---|---|---|
| TYPE0 — lista prymitywów 36 B | `00 00` + u16 LE count @+2 | **1686** | 4 + count×36 == packed_size: **1686/1686 PASS, 0 mismatch** |
| TYPE1 — siatka (mesh) | u32 LE @+0 == 1 | **164** | blok wierzchołków 12+vc×12+4 ≤ packed: **164/164 PASS** |
| INNE/UNCLASSIFIED | np. `01 00 05 00`, `01 00 0d 00` | **15** (0.80%) | nagłówek poza obiema rodzinami — NIE zdekodowane w tym runie (denominator jawny) |

## TYPE0 — rekord 36 B = 9 × f32 LE (przykład: 506044.bvi, 4 rekordy; 105624.bvi, 1 rekord; 506237.bvi, 70 rekordów)

| Offset w rekordzie | Szerokość | Etykieta | Semantyka |
|---|---|---|---|
| +0..+11 (f1..f3) | 3 × f32 LE | OBSERVED (wartości) / HYPOTHESIS (znaczenie) | trójka 1 — hipotezy: punkt/kotwica prymitywu; NIE ustalone (patrz ALTERNATIVE_HYPOTHESES w PLACEMENT_CLASSIFICATION.md) |
| +12..+23 (f4..f6) | 3 × f32 LE | OBSERVED (wartości) / HYPOTHESIS | trójka 2 — hipotezy: drugi punkt / rozmiar / wektor; NIE ustalone |
| +24..+27 (f7) | f32 LE | OBSERVED | 15,760/21,818: dokładnie 0.0; w 6,058 pozostałych: wartości kątowe (max abs = π/2) i szumy ≤1e-9 — kąt w radianach (HYPOTHESIS: oś X) |
| +28..+31 (f8) | f32 LE | OBSERVED | 0.0/−0.0 w 15,778/21,818; w 6,040: dominują π (524×), ±π/4, π/36 — kąt w radianach (HYPOTHESIS: oś Y) |
| +32..+35 (f9) | f32 LE | OBSERVED | dominują: −0.0 (12,699×), ±π/2, ±π, ±π/4, ±π/9, ±π/6… — kąt w radianach (HYPOTHESIS: oś Z) |

Pomiar pełnokorpusowy (1686 plików, 21,818 rekordów): **01_RAW/TYPE0_FIELD_STATS.json**
(generator tools/field_stats.py). Ograniczenie jawne: większość wartości f7–f9 leży na
siatce wielokrotności π/36, ale występują pojedyncze wartości siatkie (−0.015121, 0.003562,
−1.569051 ≈ π/2 − 0.0017) — kwantyzacja SILNELY_SUPPORTED, nie bezwyjątkowa. Trójka
(f7,f8,f9) jako rotacja Euler prymitywu = HYPOTHESIS (wartości kątowe OBSERVED;
przypisanie osi HYPOTHESIS).

Klasyfikacja przestrzeni pól f1–f6 (V2-009 — wynik, nie założenie):
**UNDETERMINED per-rekord; ale klatka wspólna świata ODRZUCONA pomiarem** — zakresy
f1–f6 silnie klastrowane per-plik (506044: [−526, +1265]; 506237: [−25, +33];
105624: [−0.55, +1.73]) — niespójne ze współdzieloną klatką świata (patrz Stage E).

## TYPE1 — siatka (przykład: 584781.bvi, 190,690 B)

| Offset | Pole | Etykieta |
|---|---|---|
| +0 | u32 LE = 1 (słowo typu) | OBSERVED (164/164 plików typu 1) |
| +4 | u32 LE (0x10010 w 584781; znaczenie nieznane) | HYPOTHESIS (metadane/nagłówek sub-formatu) |
| +8 | u32 LE vertex_count (584781: 2104) | OBSERVED (walidowane blokiem) |
| +12 | vcount × f32 LE ×3 — wierzchołki | OBSERVED (wartości; zakres 584781: [−57.6, +52.5]) / HYPOTHESIS: współrzędne lokalne siatki kolizyjnej |
| +12+vc×12 | u32 LE tri_count (584781: 926) | OBSERVED |
| po nim | tcount × 3 × u32 LE — indeksy trójkątów; wszystkie < vcount; wzorce triangle-soup (sekwencja 0,1,2…71, potem 71,72,69,73,74,75,75,76,73…) | OBSERVED |
| za blokiem trójkątów | **OGON NIEZDEKODOWANY** — 584781: 154,314 B (80.9% pliku) zaczynają się od f32 (−3.383, −3.267, 12.757, 1.0) i zawierają powtórzenia 4-bajtowe; NIE rozstrzygnięte w tym runie (budget) | HYPOTHESIS/UNRESOLVED — jawny RESUME_POINT |

## Kontrole negatywne (G3) — wykonane na OBU dekoderach (01_RAW/DECODE_A.json, DECODE_B.json)
- (a) wrong-endian (BE): FAIL A (4/4) i FAIL B (4/4) — rzeczywiste komunikaty w JSON.
- (b) truncated (połowa, dla type1: 24,000 B < vertex block): FAIL A (4/4) i FAIL B (4/4).
- (c) wrong-width (type0: rekord 72 B; type1: wierzchołki f64/24 B): FAIL A (4/4) i FAIL B (4/4).
- Linie dekoderów niezależne: A = structure-first (licznik w nagłówku); B = content/statistics-driven
  (grid solver z dywizybilności + spójności wzorca; vcount ze skanu f32-run, nie z nagłówka).
  Wspólna tabela pól: BRAK (dokumentacja lineage w nagłówkach skryptów).

## Zgodność A/B (01_RAW/AB_AGREEMENT.json)
4/4 próbki both_ok; **0 rozbieżności** pól: count (4,1,70; vcount 2104 scan-vs-header),
wszystkie f32 rekordów type0 (675 pól), vertex_f32_first9, tri_first15, tail_bytes — identyczne.
Zapisana dwuznaczność solvera B: dla plików type0 istnieje też pod-grid 12 B (12 | 36) —
odrzucany przez kalibrację korpusową B i spójność wzorca intra=24; jawne w stride_solutions.
