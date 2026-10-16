# Postaudyt wrappera kursora PE 9.3.5 — 2026-10-16

**Werdykt: PARTIAL_PASS.** Lokalny relay C/O/B pozostaje potwierdzony warunkowo na zadanym entry i jawnych modelach ABI. Handoff nie uzasadnia jednak twierdzeń „budżety w limicie”, „maskowanie było szumem dekompilera” ani ogólnego „kwalifikator fail-closed”. Do znanego otwartego defektu zapisu F1 dochodzą dwa materialne ustalenia: dodatkowy niepoliczony pełny odczyt EXE i błędna interpretacja bypass EAX. Nowy audyt nie zmienia zamrożonego runu ani kanonicznych gate.

## 1. Co zbadano i jak

Badany run: `D:\Eudoria_Reconstruction\99_Audits\PE_935_PARAMETER_CURSOR_UPSTREAM_WRAPPER_R1_20261016`.

Podstawa kontraktowa: `outputs/PARAMETER_CURSOR_UPSTREAM_WRAPPER_PROMPT_R1_20261016/OPENCODE_PARAMETER_CURSOR_UPSTREAM_WRAPPER_R1.md`, 25 252 B, SHA256 `F0EA823C650953FAFA4D2524538332258573D49F6B2AE6A7D0879B199435F7C2`. INPUT_PINS: 6 186 B, SHA256 `E6F46702F9BE6821282C40B1F1C3479E523CFDF0BB9384D547C32D8C08BE3B65`.

Odczytano raport, handoff, evidence, budżety, source-reads, cały ledger i wszystkie 19 entries, zapisane dekodury A/B, roster, pięć końcowych wyników controls oraz ich kod i zachowane wcześniejsze wersje. Procesowa analiza objęła pełne `run_common`, t00/t02/t09/t10, różnice controls v1→v2→v3 i wskazane ścieżki t03–t07. Pełny census/re-hash obejmuje wszystkie pliki pakietu; nie jest deklaracją semantycznego przeglądu każdej linii każdego narzędzia.

Własny verifier `measure.py` niezależnie porównuje zapisane A/B/roster z oboma zapisanymi buforami, przelicza siedem celów z raw i parsuje PE z odwracalnej pochodnej zapisanego nagłówka. **Nie uruchomiono dekodera ani starych narzędzi.** To niezależne sprawdzenie zapisanych rekordów i arytmetyki, nie nowa niezależna dekodura x86 ani dowód działania runtime.

Wszystkie ścieżki wejściowe tego verifiera mają whitelistę dwóch korzeni. Ścieżki absolutne z ledgeru są odrzucane przed I/O. Cztery takie referencje pominięto jawnie. Pliki obu badanych pakietów pozostały byte-identyczne w census przed/po. Nie było zapisu do repo, EXE ani zamrożonego outputu.

## 2. Naruszenie zakresu przez ten audyt

**AUDIT-SCOPE-01: audyt nie spełnił własnego warunku ZERO ORIGINAL EXE READS.** Verifier podagenta procesowego złożył `Path(root) / absolute_input_path`. Na Windows wybiera to ścieżkę absolutną. Następnie `read_bytes()` odczytał oryginalny `Entropia.exe` dla wejść attempts 0003/0004/0005: **3 × 8 015 872 = 24 047 616 B**. Błąd wykryto i zgłoszono; dalszych odczytów oryginału zaniechano.

Nie było zapisów, dekodowania, analizy regionów ani wykonania klienta. Wyniki tych trzech odczytów **wyłączono z materiału dowodowego**. Nie używamy ich do potwierdzenia obecnego SOURCE_UNCHANGED ani przypięcia EXE. Finding o historycznym ukrytym hash-pass zidentyfikowano i przekazano wcześniej, wyłącznie na podstawie zachowanego kodu i ledgeru. To dwa odrębne zdarzenia: dodatkowy odczyt badanego runu i trzy późniejsze błędne odczyty audytu.

Dokładny wadliwy fragment verifiera, zakres i kolejność ujawnienia zachowano w `AUDIT_RAW.zip/review/wrapper_process_review.md`. Własny `measure.py` zawiera pre-I/O odmowę ścieżek zewnętrznych. Ponowne poprawne sprawdzenie zapisanych records nie cofa naruszenia. AUDIT_PROCESS_STATUS = SCOPE_VIOLATED_DISCLOSED; wiarygodność merytorycznych ustaleń należy oceniać w podanym saved-records scope. Następnego eksperymentu nie wykonano.

## 3. Integralność pakietu i retencja

| Sprawdzenie | Wynik |
|---|---:|
| Manifest: wiersze / fizyczne pliki | 124 / 125 |
| Łączne fizyczne bajty | 566 173 |
| Missing / extra / duplicate / size-hash mismatch | 0 / 0 / 0 / 0 |
| Piny wejściowe + INPUT_PINS + kontrakt | 14/14 zgodnych |
| Strict JSON/JSONL | 63/63 poprawnych |
| Ledger / osobne attempt entries | 19 / 19 |
| Zgodność prefix size/SHA ledgeru | 19/19 |
| Semantyczna zgodność entry.json z linią ledgeru | 19/19 |
| Główne tool SHA względem zachowanego kodu | 19/19 |
| Standing kontrakt→EVIDENCE | 22/22, dokładna zgodność |

Manifest: SIZE **11 863**, SHA256 **`25EC0FB6253D16D836F886AC97FAD8C59899CE04E34FE867FADA8FF704D63558`**. Self-exclusion manifestu jest jedynym wyłączeniem. Liczba „124/124” w handoff odnosi się do wierszy, a nie wszystkich fizycznych plików. Ostateczny census mieści się w 128 plikach / 8 MiB.

W 97 sprawdzonych referencjach input/output/capture 41 tożsamości dyskowych odbiega od zapisanej tożsamości logicznej. Każdą z tych 41 rozbieżności wyjaśnia odwrócenie znanej translacji CRT CRLF. Osiem payloadów `_incoming` ma zachowane kopie `attempts/NNNN/payload_input.*`; nie uznano ich za utracone. Nie używano odwrócenia jako cichej naprawy oryginałów.

`artifact_index.csv` jest jawnym snapshotem sprzed końcowego append do ledgeru. Jedyny różniący się finalnie wpis to ATTEMPT_LOG.jsonl. To ujawniona granica snapshotu, a końcowy manifest obejmuje właściwy finalny ledger; nie traktujemy tego jako nieujawnionego naruszenia manifestu.

## 4. Nowe materialne ustalenie WRAP-PROC-01 (P2): odczyty EXE ponad limit

`tools/t02_hash_exe.py:31–37` wykonuje pełny streaming hash EXE. Następnie linia 49 robi `rc.file_identity(exe_rel_cfg)`. Zachowane `run_common.py:88–91` wywołuje stąd `sha256_file`, którego linie 42–50 **ponownie czytają cały EXE**. To nie martwa gałąź: attempt 0003 ma status OK, zgodny główny tool SHA i wypełnioną input identity. `t09_close.py:58–64` wykonuje kolejny pełny odczyt przy zamknięciu.

| Miara badanego runu | Deklarowane | Ustanowione minimum z kodu i records | Limit |
|---|---:|---:|---:|
| Pełne odczyty EXE | 2 | **3** | 2 |
| Łączne bajty oryginału | 16 036 004 | **24 051 876** | 16 036 004 |
| Pominięte bajty | 0 | **8 015 872** | 0 |

Równanie: `3×8015872 + 4096 + 2×82 = 24051876`. Mówimy „co najmniej”, ponieważ analizowany ślad nie jest zewnętrznym OS trace wszystkich I/O. Już jawny retained-code path przekracza kontrakt. Metadata/hash identity też jest odczytem oryginału; etykieta helpera nie wyłącza go z budżetu. F1 dotyczy zapisu i nie wyjaśnia tego odczytu.

`SOURCE_READS.json`, `BUDGET_USED.json`, REPORT oraz HANDOFF zaniżają bilans. Utrzymanie PARTIAL było właściwe, ale ich argument „wszystkie budżety w limicie” jest błędny. Nie ma potrzeby nowego odczytu EXE, aby odtworzyć to ustalenie. Historyczne hash-equality w saved records można cytować wyłącznie jako historyczny wynik narzędzia; ten audyt nie poświadcza obecnej tożsamości oryginału.

## 5. Nowe materialne ustalenie WRAP-SCI-01 (P2): maska bypass jest rzeczywista

`REPORT.md:23` i `EVIDENCE.json` w `/provenance_rows/3/finding` oraz `/pseudo_vs_bytes_disclosures/0` błędnie nazywają pseudo `(B−1)&0xFFFFFF00` szumem dekompilera. Handoff powtarza to jako poprawne wycofanie.

Zapisane bajty pokazują:

```text
0x00852A64  0F B6 C3   MOVZX EAX,BL
0x00852A67  83 E8 01   SUB EAX,1
0x00852A6A  74 08      JE parser_path
... bypass ...
0x00852A6E  32 C0      XOR AL,AL
```

Na bypass EAX wynosi dokładnie `(u32(B)−1)&0xFFFFFF00`. Dla B=0 jest to **0xFFFFFF00**; dla B=2…255 — 0. AL jest zerowane we wszystkich bypassach, ale zerowanie AL nie zeruje górnych 24 bitów EAX. B=1 przechodzi do parsera; nie ma wtedy lokalnego bypass return.

To ustalenie dotyczy wzorca EAX, bez awansu do konkretnego typu zwrotnego C. Nie obala bramki B==1 ani relay. Należy skorygować interpretację w nowym dokumencie wejściowym; zamrożonego EVIDENCE/REPORT nie edytujemy. Poprzednie pseudo pozostaje tylko nawigacją, lecz ta konkretna maska zgadza się z bajtami.

## 6. Znane F1 (P2, OPEN): bajtowa tożsamość zapisów

`run_common.atomic_write_bytes` używa `os.open(... O_CREAT|O_EXCL|O_WRONLY)` bez `O_BINARY`. Na użytej platformie translacja CRT rozszerza LF do CRLF. Zwracana identity opisuje bufor w pamięci, nie ponownie zmierzony plik na dysku.

Nagłówek na dysku ma **4099 B**, SHA256 `2190840B26FDE4BA368326990246C24BA96F8E8C9C8603B9690A71FED69B0E29`. Wyłącznie w pamięci `replace(b'\r\n',b'\n')` daje 4096 B i SHA256 `636B01A25A9DE410781805D67AE1149FA64DF3D26C5C4FDE7D2D9EBCABC5A5C0`, zgodny z historycznym logicznym pinem. Z tej jawnej pochodnej odczytano sekcje PE; nie zapisano jej jako naprawionego oryginalnego artefaktu.

Oba okna `[0x00852A30,0x00852A82)` mają po **82 B** i są identyczne: SHA256 `43134E71A4C84F7F06972F9EDC3C6BDC8A29A5FCBCF27E6D95252FE5B2D30B5C`. Ten defekt zapisu nie zmienił ich bajtów. Fizyczny manifest pozostaje poprawny; nie przywraca to zgodności logicznych identities z dyskiem.

Drobne WRAP-DOC-01 (P3): `QC.json/findings/F1/affected_artifacts/window_buffers` ma 63-cyfrowy skrócony digest, bez końcowego `C`. Bufory i inne wiążące references mają pełny 64-cyfrowy hash; to literówka, nie kolejna różnica bajtów.

## 7. Co pozostaje potwierdzone w wrapperze

Zapisane A/B i roster pokrywają całe 82 B: **37 instrukcji**, ciągłe head/raw/length, **7 poprawnych celów arytmetycznych**. CALL `0x00852A77` ma raw `E8 D4 FC FF FF`, nextVA `0x00852A7C`, displacement −0x32C, target **0x00852750**.

- C pochodzi z `[entryESP+4]` i trafia do ESI; po dwóch pushach `[ESP+0xC]` oznacza ten slot. Sam RET4 nie dowodzi całkowitej liczby parametrów.
- O pochodzi z entry ECX i trafia do EDI. PUSH EDI@0x00852A3D zapisuje wcześniejsze EDI wywołującego. `MOV ECX,EDI` przy transferze ustanawia zapis operacji, a zachowanie wartości przez opaque helper wymaga modelu ABI.
- B jest odczytane jako u8 z `[C.data+C.offset]`; valid/size są osobnymi strażnikami. `offset+1` działa modulo 2^32, a JA jest unsigned; nie ustanawia globalnej OOB/no-wrap safety.
- Valid-fail nie czyta bufora i nie zeruje valid. Size-fail zapisuje BL=0 do valid. Read-success przechodzi przez opaque helper. BL/ESI/EDI preservation jest warunkowe; rzeczywiste efekty helpera na pamięci pozostają nieustalone.
- Gate do parsera to B==1. W oknie nie ma wykazanej konstrukcji ani wypełniania kursora. Wniosek **relay** ma zakres tego okna, entry i modeli, bez twierdzenia o całej funkcji w każdym możliwym kontekście.

Nie ustalono medium FILE/NETWORK/VFS, roli budynku, powiązania modelu 218757, tożsamości instancji świata ani XYZ. Nauka tego szwu nie usuwa tych braków.

## 8. Kontrole, korekty i granice kwalifikatora

V3 ma BASE ACCEPTED/0 i cztery wymagane odmowy /1: C1 NOT_INSTRUCTION_HEAD, C2 ROLE_OR_SLOT_MISMATCH, C3 UNJUSTIFIED_OPAQUE_PRESERVATION, C4 UNSUPPORTED_SOURCE_OR_WORLD_PROMOTION. Jest pięć końcowych wykonań kwalifikatora; licznik 0 retries dotyczy v3, nie całej historii. Zachowano v1 z błędem argv i v2 z błędem claims wrapper oraz dwa wykonane zbiory korekt. Nie ma dowodu trzeciej korekty po zamknięciu rundy 2.

**4/4 CONTROL_PASS oznacza te cztery przypadki.** `qualify()` ufa dostarczonym listom, flagom `crosses_opaque_call` i obecności proof/evidence; nie ustanawia kompletności wszystkich brakujących ról/źródeł. W C4 joint FILE+XYZ odmowa następuje już na FILE: nie dowodzi niezależnej odmowy samego XYZ ani każdej możliwej promocji. Sformułowanie handoff o ogólnym fail-closed jest za szerokie. Nie wykonywano nowej macierzy mutacji.

Wyczerpanie 2/2 rund samo nie jest odrębnym materialnym błędem ani automatycznym powodem PARTIAL dla poprawnego wyniku. Kontrakt §9 zabrania dalszych poprawek, a §11 wymaga PARTIAL przy materialnym OPEN lub przekroczeniu limitu. Tutaj istnieją F1 i nowo wykazane przekroczenie, więc PARTIAL jest merytorycznie uzasadnione. Bezpośrednio autorowany GATES.csv był ujawniony; nie nadano mu serializer timestamp, którego nie ma.

## 9. Dyspozycja i kolejny krok

Zamrożony run zachowujemy. Nowy raport supersedes wyłącznie wskazane twierdzenia w warstwie interpretacji; nie rekonstruuje brakujących historycznych times ani nie naprawia starych plików. CANONICAL_GATE_EFFECT=NONE; REPOSITORY_MODIFIED=NO; WORLD_XYZ_RECOVERED=NO.

Pierwsza brakująca krawędź nadal brzmi: **kto dostarcza C do FUN_00852A30 i gdzie konstruuje/wypełnia jego bufor?** Zanim wybierzemy małe body do analizy, potrzeba listy miejsc, które mogą odwoływać się do wrappera.

Osobno przygotowany następny pakiet zawiera skrypt oraz szczegółowy kontrakt **NAVIGATION_ONLY**. Zaplanowany future run szuka E8/E9 rel32 w RAW `.text` oraz aligned-u32 VA wrappera w RAW `.rdata`. Nie dekoduje kandydatów, nie otwiera ich otoczenia/body, nie buduje callgraph i nie ustanawia callerów. Dwa kanały surowych referencji pozwalają zebrać miejsca do następnej decyzji także wtedy, gdy nie ma direct-call pattern. Brak trafień nie wykluczy pośrednich, niealigned, computed, runtime ani innych referencji poza zakresem.

Nowy skrypt używa binarnego exclusive write z kontrolą fizycznego SIZE/SHA, centralnego licznika każdego oryginalnego read i reuse już zmierzonego full hash do metadata. To bezpośrednie środki przeciw F1 i WRAP-PROC-01. Jego testy na syntetycznych buforach nie są kwalifikacją dekodera ani wynikiem poszukiwania w EXE. **Przygotowanie pakietu nie oznacza wykonania następnego runu.**

## 10. Artefakty i kwalifikacja

`MEASUREMENTS.json` zawiera wszystkie pomiary, identities, ledger checks, jawne pominięcia absolute input paths, granice B oraz audit-scope deviation. `FINDINGS.json` rozdziela nowe ustalenia, znane F1, ograniczenia kwalifikatora i własne naruszenie audytu. `AUDIT_RAW.zip` zachowuje użyte records/kody/notatki i własny verifier; jego manifest wewnętrzny umożliwia re-hash. Główny MANIFEST_SHA256.csv obejmuje wszystkie pliki tego nowego postaudytu poza sobą.

AUDIT_VERDICT=PARTIAL_PASS; SCIENCE_RESULT=WRAPPER_CURSOR_RELAY_CONFIRMED_CONDITIONAL_ON_DECLARED_MODELS; AUDIT_PROCESS_STATUS=SCOPE_VIOLATED_DISCLOSED; HUMAN_QUALIFICATION=NOT_ESTABLISHED; CANONICAL_GATE_EFFECT=NONE; NEXT_RUN_EXECUTED=NO.
