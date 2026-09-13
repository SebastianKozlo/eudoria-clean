# 02_ANALYSIS — A. Tożsamość definicji rekordu template (CYTAT + własna weryfikacja)

RUN: PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912 | ERA: EU 9.3.5 (pcg_install)
Binarium: Entropia.exe SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (8,015,872 B)
Dane: Data\Parameters\templates.vfs SHA256 BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77 (560,788 B)

## A.1 Definicja wg kontraktu (CYTOWANA, nie re-derivowana w części semantycznej)

Kontrakt RUN (PARENT_CONTEXT z PE_296445_NIF_ORIGIN_PLACEMENT_R1): rekord template'u 4508
w pcg 9.3.5 @96,496: id=4508, f1=28, f2=1, hash=0xAFF5797C, id2=4508, A=296445 @96,516,
B=296446 @96,520, C=0, PARAM=124.941f. Kategoria 201→477→4751→4508; 296445.nif =
B_Eu_Slum_Building_b047_01.

## A.2 Własna weryfikacja bajtowa (S1/S2, narzędzia s1/s2, hashe w 00_CONTROL\*_SCRIPT_SHA256.txt)

Własny odczyt (S1_ANCHOR_RESULT.json + S2_TRUE_WALK_RESULT.json, pełny walk pliku):

| pole | wartość zmierzona | zgodność z kontraktem |
|---|---|---|
| rekord 4508 start | 96,496 (0x178F0); idx 1340 (base 16, stride 72 dla size=28) | TAK |
| id @+0x00 | 4508 (9c 11 00 00) | TAK |
| size(f1) @+0x04 | 28 | TAK |
| ver(f2) @+0x08 | 1 | TAK |
| crc32 @+0x0C | 0xAFF5797C — **zlib.crc32(payload 28 B) == pole** (S2: 0/5438 fail) | TAK |
| id2 @+0x10 | 4508 | TAK |
| **A @+0x14** | **296445** (fd 85 04 00) @96,516 | TAK |
| **B @+0x18** | **296446** (fe 85 04 00) @96,520 | TAK |
| C @+0x1C | 0 | TAK |
| PARAM @+0x20 (kontrakt: "+0x24") | **124.941f (cb e1 f9 42)** @96,528 | WARTOŚĆ TAK; offset kontraktu +4 (PROMPT_DELTA_1) |

Siblings (kontrola generyczności): 4752 @97,288 (idx 1351): A=126740, B=126741, crc=0xDFD0B0BA ok;
2249 @93,976 (idx 1305): A=278453, B=278454, crc=0xB4B87ABD ok.
**PROMPT_DELTA_2**: kontrakt podaje starty siblingów 97,294/93,982 — fizyczne starty to 97,288/93,976
(delta +6 każdorazowo). Zawartość (A/B) zgodna bajtowo z kontraktem.

## A.3 Pełna struktura bloku (NOWE, własna — S2 walk pełnego pliku)

- Nagłówek pliku: `ArkVFS02` + u32@0x08 = **base=36** + u32@0x0C = 1.
- Blok = [16-B header {id, size, ver, crc32}] + [size-B payload (crc32-gated)] + tail do stride.
- **stride = (floor((size+15)/base)+1) * base** — pełny walk 5438/5438 rekordów do EOF
  (walk_last_record_end == 560,788 == rozmiar pliku; 0 niezudokumentowanych bajtów; 0 CRC fail).
- Payload rekordu size=28 (siatka u32): [id2][A][B][C][D_f32][u16 str_count][u32-list_count_hi16][F_u32].
  - D_f32 @rec+0x20 = pole "PARAM" kontraktu (wartość 124.941 dla 4508).
  - slot @rec+0x24 = para u16: licznik listy stringów + licznik listy u32 (sub-obiekty +0x14/+0x20
    parsed-template; census: D≠0 w 5408 rekordach, slot@0x24≠0 w 2003 — D i slot@0x24 to RÓŻNE pola).
  - rekordy size>28 (np. 50, 536) niosą listy: {[u16][u16 len][nazwa][u32 100][u32 id]} —
    nazwy typu "eye_BUMP"/"calf_BASE"/"Box01_0_BASE" (avatar body parts, sloty _BASE/_BUMP).
  - Kontraktowy "PARAM f32 @+0x24": fizycznie wartość PARAM leży @+0x20; @+0x24 leży para
    liczników list. PROMPT_DELTA_1 udokumentowana (wartość i semantyka pola zgodne z kontraktem;
    adnotacja offsetu w prompcie rozbieżna o 4).

## A.4 Status

Definicja rekordu = POTWIERDZONA własnym pełnym walkiem (nie tylko cytat). CRC32-gate =
realny dyskryminator (kontrola negatywna S2: flip 1 B payloadu → AFF5797C → 3C32D977 ≠).
