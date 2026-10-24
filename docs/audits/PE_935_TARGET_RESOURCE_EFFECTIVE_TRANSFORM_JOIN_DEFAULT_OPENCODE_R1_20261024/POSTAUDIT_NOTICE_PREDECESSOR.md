# POSTAUDIT NOTICE — poprzednik PE_935_INSTANCE_DATA_TRANSLATION_JOIN_DEFAULT_OPENCODE_R1_20261024

Ten notice jest addytywną korektą publicznej publikacji poprzednika (commit 8ed9f5c33d7db883223454732b475f9d1b28a638), wykonaną zgodnie z kontraktem R1_20261024. Historia poprzednika nie została przepisana; jego publikacja pozostaje na swoim commicie.

## Wiążące korekty postaudytu Desktop (ITR-A01..A12) przyjęte jako baseline tego runu
1. ITR (proces): poprzedni proces NIE był compliant w zakresie dozwolonych odczytów EXE (3 pełne zdarzenia hashowania vs limit 2; raportowane 5) i limitów ekspozycji pojedynczych jobów. Historyczne limity nie zostały skorygowane wstecz.
2. ITR (census): pełny indeks poprzednika = 78 wierszy + indeks = 79 plików; root ses_e932c02e4ffeTibiREck6qR6zU; 23 natywne Task (19 prób workerów, 4 QC), 21 stop / 2 length.
3. ITR (wektory): pierwszy wektor = rec+0x38 → def+0x08 → B+0x44/48/4C; drugi = rec+0x44 → def+0x14 → B+0x5C/60/64 (+kopia B+0x68..0x70). Creator może warunkowo podnieść trzecią składową pierwszej trójki (H>u2, ordered).
4. ITR (selector): word[F+0x44] = record+0x34; writer znany (parser 0074543D, default 00745448, zero-init 00745378); otwarte było preservation — ten run domknął je bounded (M5).
5. ITR (ABI): 004154F0 RET C3 (nie RET 4); 0085B3E0 RET 8; przy spełnionych przesłankach F+0x54 = record+0x44 (nie record+0x3C).
6. ITR (creator): clamp H nie jest bezwarunkowym verbatim — potwierdzone i doprecyzowane w tym runie (kierunek: v1.z := H iff H > v1.z ordered strict GT).
7. ITR (math): _CIcos/_CIsin rozpoznane w saved imports; K i epsilon niezweryfikowane (utrzymane).
8. ITR (tożsamość): S_ctor vs S_later=M32[B+0x10] bez dowodu tożsamości (pozostaje UNKNOWN).
9. ITR (T): T=M32[B+0xC0] ma dokładnie jeden wskazany dereference; zapis trójki i delta/norm nie ustanawiają world position.

## Zachowany i rozszerzony postęp (ten run)
- T = M32[B+0xC0] = instancja SceneFeederObject — domknięty łańcuch akwizycji (CONFIRMED); arg4 ctor = stała 1 (nie model_id).
- Mapa pól transformacyjnych T (writery + readerzy +0x34; bounded negative readera +0x4C).
- H = wartość z providera pod [mgr+0] (manager 0x8C @0x00BA12E8), nie obliczana w 00853A80; terrain-height = PLAUSIBLE.
- Selector: writer→reader preservation bounded CONFIRMED.

## Status algebra
- WORLD_XYZ_RECOVERED = NO; HISTORICAL_PLACEMENT = NOT_ESTABLISHED.
- Model-instance join = PARTIAL (bez zmiany względem poprzednika; brakujące krawędzie sprecyzowane w FIRST_MISSING_EDGE).
- Niniejsza nauka = REPORTED_PENDING_EXTERNAL_POSTAUDIT; CANONICAL_GATE_EFFECT = NONE.
