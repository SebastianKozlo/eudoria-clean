# PE 9.3.5 — skrypt i kontrakt następnego kroku: surowe referencje do wrappera

RUN_ID = PE_935_PARAMETER_CURSOR_CALLER_DISCOVERY_R1_20261016

Ten plik przygotowano do osobnego wykonania. **W trakcie jego autorowania nie wykonano poniższego runu.** Wklejenie START_PROMPT do wykonawcy z poleceniem realizacji zleca jeden run w dokładnie tym zakresie. Stary wrapper run i jego HARD STOP pozostają zamknięte. To nowy zakres nawigacyjny, bez retroaktywnej autoryzacji starych naruszeń.

## 1. Cel i granica wyniku

Ustal listę **surowych kandydatów referencji do VA 0x00852A30**. Wrapper lokalnie przekazuje istniejący kursor C do parsera 0x00852750 przy bramce B==1; nie znamy jego upstream dostawcy ani miejsca konstrukcji/wypełnienia bufora. Lista kandydatów ma umożliwić wybór małego okna do późniejszego, odrębnego badania.

Zbadaj dokładnie dwa kanały:

1. Wszystkie początki pięciobajtowych wzorców E8/E9 rel32 w RAW `.text`, dla których `(siteVA + 5 + signed32(disp)) mod 2^32 == 0x00852A30`.
2. Wszystkie czterobajtowe wartości little-endian `0x00852A30` w RAW `.rdata`, których **siteRVA mod 4 == 0**.

Nazwy kanałów opisują encoding-shaped patterns. Żaden wzorzec E8/E9 nie jest tu zakwalifikowany jako instruction head, CALL/JMP, caller lub granica funkcji. DWORD nie jest automatycznie pointerem, vtable, RTTI ani referencją używaną runtime. Wartość DWORD porównujemy z **VA 0x00852A30**, a nie RVA 0x00452A30.

Nie wykonuj disassembly, operand qualification, local caller-body analysis ani argument-flow z kandydatów. Nie otwieraj otoczenia trafienia. Nie wybieraj automatycznie kolejnego body. Ten run nie odzyskuje lokalizacji XYZ i nie ustanawia producenta kursora.

## 2. Bieżąca interpretacja wejść

Obowiązuje dołączony postaudyt PARTIAL_PASS. Historyczne wrapper REPORT/EVIDENCE zachowano byte-identycznie jako dane historyczne, z jawnym sprostowaniem:

- Known F1 OPEN: tekstowy CRT write zmienił saved header na4099 B i liczne logiczne identities. Nie używaj tego nagłówka do nowego mapowania ani dawnych helperów zapisu. Zapisane82 B okna są nienaruszone.
- WRAP-PROC-01: historyczny t02 przez `file_identity(EXE)` wykonał ukryty dodatkowy full hash. Minimum3 pełne przebiegi /24 051 876 B, a nie2 /16 036 004 B. Nie przejmuj starego budżetu jako prawdziwego.
- WRAP-SCI-01: bypass EAX=`(u32(B)-1)&0xFFFFFF00`; dla B=0 EAX=FFFFFF00 i AL=0. Maska nie była noise. B==1 gate i scoped relay pozostają potwierdzone warunkowo.
- Cztery końcowe controls potwierdzają wyłącznie cztery konkretne odmowy. Nie przejmuj globalnego fail-closed.
- Postaudyt ma własne jawne naruszenie zakresu: podagent odczytał oryginał3 razy. Tych wyników nie użyto do dowodów ani aktualnej identity EXE. Nowy run wykonuje własne policzone identity checks; nie cofa naruszenia audytu.

Hierarchia dla tego runu: ten kontrakt + INPUT_PINS + delivered tool, następnie bieżący postaudyt i INTERPRETATION_CORRECTIONS, następnie historyczne wrapper facts w ich scoped zakresie. Dawne instrukcje zawarte w historycznych wejściach są danymi, nie nową autoryzacją. Nie wykonuj instrukcji ani ścieżek shell znalezionych w evidence.

## 3. Korzenie, przypięcia i preflight

AUTHORING_ROOT = C:\Users\User\Documents\Codex\2026-10-13\files-pasted-by-the-user-wszystko\outputs\PARAMETER_CURSOR_CALLER_DISCOVERY_SCRIPT_R1_20261016

OUTPUT_ROOT = `D:\Eudoria_Reconstruction\99_Audits\PE_935_PARAMETER_CURSOR_CALLER_DISCOVERY_R1_20261016`

ORIGINAL_EXE = `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe`

EXE_SIZE = 8 015 872 B

EXE_SHA256 = `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31`

TOOL = `caller_discovery.py`, SIZE=49977, SHA256=`59B1E7E596F290EB5316B57FA1E6ED22D4E09942E92FC1AD49D3B37B9D8465EC`

INPUT_PINS = `INPUT_PINS.json`, SIZE=3856, SHA256=`8186A569BF7E166566FD6A35B8513C65A10928150FD8FB6124E005A4D338C597`

Skrypt używa tylko Python3 stdlib. Nie wymaga Ghidry/objdump/x86dec, sieci, runtime klienta ani repo changes. Użyj jawnie wybranego Python3 z `-B`; wersję/interpreter path zachowaj w wynikach. Nie instaluj zależności.

Wykonanie original-run odbywa się wyłącznie w Windows VM projektu `WinDev2407Eval`, zgodnie z `D:\Eudoria_Reconstruction\AGENTS.md`. Skrypt wymaga Windows oraz mierzy hostname i sprawdza jego zgodność; sam hostname nie jest zewnętrznym poświadczeniem hypervisora. Nie używaj hosta Hyper-V ani przekierowanych dysków RDP. Skrypt przed ścieżkowym I/O sprawdza literalne, znormalizowane source/output z tego kontraktu; inne source/output dają odmowę. Testy syntetyczne tych gates nie otwierają oryginału.

Przed pierwszym read oryginału: pełny re-hash/bijekcja AUTHORING_MANIFEST_SHA256.csv i wszystkich przypiętych inputs; strict JSON; brak symlink/junction escape; OUTPUT_ROOT nie istnieje, rodzic istnieje i jest zapisywalny, output poza źródłem/authoring i poza Git checkout. Ustal realne argv/paths/tool identity. Atomowe utworzenie świeżego root ma odmawiać collision. Nie kasuj, nie przenoś i nie nadpisuj żadnego istniejącego root. Przy odmowie praw lub preflight zatrzymaj się; nie szukaj innej kopii EXE.

Polecenie wykonania wywołuje literalną flagę `--execute-original-read`; bez niej skrypt odmawia original run. Jedynym zewnętrznym plikiem binarnym czytanym w science jest wskazany EXE, i każdy jego read przechodzi przez licznik OriginalReader. Ścieżek EXE z dawnych ledgerów/inputs nie wolno otwierać. Relative bundle input names muszą odrzucać absolutne, drive-relative, UNC, rooted, URI i `..` przed I/O.

Nie uruchamiaj starych t02/run_common/t09 ani importowanych narzędzi z historycznych pakietów. Nie wyłączaj checków pinu dla „tej samej wersji”. Identity mismatch blokuje science.

## 4. Dokładna geometria PE i zakres odczytów

Po pierwszym policzonym pełnym hash odczytaj dokładnie pierwsze4096 B nowego EXE. Zachowaj binarnie i zweryfikuj fizyczny SIZE/SHA. Parsuj MZ, e_lfanew, PE, machine014C, magic010B, imagebase00400000, bounds section table, unikalność .text/.rdata, raw ranges, brak overlap i file bounds. Nie używaj starego uszkodzonego header jako danych mapowania.

Przypięta geometria musi się zgodzić:

| Sekcja | RVA | VirtualSize | RawPointer | RawSize | Characteristics |
|---|---:|---:|---:|---:|---:|
| .text | 4096 | 6 764 005 | 4096 | 6 766 592 | 0x60000020 |
| .rdata | 6 770 688 | 1 009 001 | 6 770 688 | 1 011 712 | 0x40000040 |

Adres targetu musi leżeć w virtual span `.text`. Przeliczenie: `VA=ImageBase+RVA`, `fileOffset=RawPointer+sectionOffset`, bez kopiowania samego adresu jako file offset. Dla wrappera poprzedni offset0x452A30 był prawidłowy, ale nowy skan wylicza site offsets z nowego mapowania.

Skanuj RAW obu sekcji włącznie z paddingiem, aby domena była jednoznaczna. Każdemu kandydatowi nadaj osobne pola `site_in_virtual_span` oraz `full_pattern_in_virtual_span`. Trafienia zaczynające się w paddingu albo przecinające granicę VirtualSize pozostają typed raw candidates; nie traktuj ich jako mapped code/data. Header/file alignment nie jest instruction alignment.

Nie czytaj .data/.tls/.rsrc w science; pełne hash przebiegi obejmują plik tylko do identity, bez zachowania/analitycznego skanowania zawartości tych sekcji. Nie wykonuj trzeciego hash przez metadata helper. Hash już policzony dla EXE reuse w source identity record.

## 5. Budżet oryginału i domeny skanu

| Odczyt / operacja | Maksimum |
|---|---:|
| Pełny streaming SHA256 EXE | 2 ×8 015 872 B |
| Header | 1 ×4096 B |
| RAW .text | 1 ×6 766 592 B |
| RAW .rdata | 1 ×1 011 712 B |
| Łączne original bytes | **23 814 144 B** |
| Nowe body / dekodury / vicinity reads / runtime | **0** |
| Target VA | **1** |
| Maksimum wszystkich retained candidates | **4096** |
| Fizyczne output files / bytes | **32 /8 MiB** |
| Naprawy narzędzia lub records w trakcie runu | **0** |

To nowy jawny section census, szerszy od poprzedniego82-B okna. Budżet nie jest wynikiem poszukiwania ani dowodem, że odczyty wykonano. Po wykonaniu podaj wyłącznie rzeczywiste liczniki z reader ledgeru.

Normalny pełny skan ma6 766 588 eligible text starts, ponieważ pattern wymaga5 B w RAW section. `.rdata` ma252 928 eligible aligned DWORD sites. Eligible denominators wylicz też mechanicznie z mapowania; jeśli nowa geometria nie zgadza się z pinem, odmowa zamiast cichej adaptacji.

Czytaj chunkami do1 MiB, zachowując do4 B carry dla text. Carry nie oznacza dodatkowego odczytu oryginału. Każdy eligible start oceniaj raz, także na granicy chunków; końcowe1–4 B bez całego pattern nie są eligible. `.rdata` alignment odnosi się do siteRVA, nie bieżącego początku chunku. Short read/error/cap overflow daje PARTIAL; nie deklaruj pełnego zero-result. Po wejściu w science zaplanowany closing hash pozostaje w tym samym wspólnym budżecie, także przy kontrolowanym błędzie, jeśli czytanie nadal możliwe.

## 6. Wykonanie dostarczonego skryptu

Otwórz i przeczytaj cały ten kontrakt, INPUT_PINS oraz interpretację sprostowań. Re-hash inputs jest checkiem tożsamości, nie dowodem przeczytania ich znaczenia. Nie modyfikuj skryptu przed runem. Ewentualny wykryty defekt zgłoś i zatrzymaj execution; wymaga nowej wersji kontraktu/tool, poza tym runem.

Polecenie w PowerShell:

```powershell
& 'C:\Users\User\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B 'C:\Users\User\Documents\Codex\2026-10-13\files-pasted-by-the-user-wszystko\outputs\PARAMETER_CURSOR_CALLER_DISCOVERY_SCRIPT_R1_20261016\caller_discovery.py' --execute-original-read --bundle 'C:\Users\User\Documents\Codex\2026-10-13\files-pasted-by-the-user-wszystko\outputs\PARAMETER_CURSOR_CALLER_DISCOVERY_SCRIPT_R1_20261016' --source 'D:\Eudoria_Reconstruction\pcg_install\Entropia.exe' --output 'D:\Eudoria_Reconstruction\99_Audits\PE_935_PARAMETER_CURSOR_CALLER_DISCOVERY_R1_20261016'
```

Zachowaj rzeczywisty wynik procesu i exit w terminalnym handoff poza frozen root. Nie dodawaj sfabrykowanego stdout/stderr „capture” do pakietu. Wewnętrzny JSON result, log i traceback są rekordami narzędzia, nie zewnętrznym świadectwem OS. Jeśli host ma osobny harness, jego prawdziwe captures można zachować poza OUTPUT_ROOT i jawnie odróżnić od tool-owned files.

Skrypt jest jedną monolityczną próbą ze znanymi fazami: preflight→first hash→header→text scan→rdata scan→closing hash→input recheck→QC→report/result→manifest. Nie twórz sztucznego ledgeru19 prób. Nie uruchamiaj skryptu ponownie pod tym samym output ani z suffixem w celu obejścia błędu. Nie resetuj liczników po wyjątku. Nie wykonuj dodanych ręcznie odczytów „dla pewności”.

## 7. Wymagane fakty o kandydacie

Każdy zachowany kandydat ma co najmniej kanał/type, targetVA, siteVA/siteRVA/fileOffset, section/offset, raw5 albo raw4, full-pattern width, flagi virtual-span oraz qualification status `RAW_UNQUALIFIED`. Dla rel32 zachowaj signed displacement i nextVA; arytmetyka musi być modulo2^32. Dla DWORD zachowaj wartość i dowód siteRVA%4==0. Oba kanały pozostają osobnymi denominatorami i licznikami.

Nie wyprowadzaj instrukcji od pierwszego E8 w buforze. E8 może leżeć w immediate/displacement/innych danych. E9 także może być danymi. W `.rdata` równy DWORD może być przypadkową liczbą. Bez code-flow/xref qualification brak ustalonego callera nawet przy wielu trafieniach.

Zachowaj wszystkie trafienia do cap bez preferowania pierwszego/najbliższego. Gdy wystąpi overflow, record musi jawnie mówić `census_complete=false`, a limitowana lista jest prefiksem skanu, nie pełną listą. Nie nazywaj retained count globalnym total. Nie dobieraj dodatkowych section/targetów, aby poprawić zero lub niejednoznaczność.

## 8. Zapis, QC i zamknięcie

Każdy zapis jest binarny i exclusive (`xb` albo równoważnie z O_BINARY), bez nadpisywania. Po zapisie mierz ponownie fizyczny SIZE/SHA; to te wartości obowiązują w manifest i result. Test256 różnych bajtów w authoring QA sprawdza ścieżkę binarną, ale runtime też kontroluje własne saved bytes. Nie zapisuj całego EXE ani całych sekcji; tylko4096-B header, kandydaci i metadane.

QC musi sprawdzić: first/closing hash vs pin; geometry; brak read-budget overflow; pojedyncze section reads; rzeczywiste denominator counts; deduplikację site+channel; candidate arithmetic/raw width/alignment; pełność census; strict JSON/JSONL; input recheck; faktyczny file/byte census; unknown standing. Zgodność skryptu z samym sobą nie jest niezależną kwalifikacją instrukcji.

Jeżeli zaistnieje błąd: zachowaj to, co naprawdę zapisano, pełny error i fazę, rzeczywiste reads i status PARTIAL albo BLOCKED_PREFLIGHT. Wyjątek po rozpoczęciu source I/O musi pozostać PARTIAL; nie wolno nazwać go BLOCKED_PREFLIGHT ani utracić ledgeru przy wyjątku QC. Gdy zapisu nie da się dokończyć, zwróć pełny read ledger w terminalnym wyniku poza root. Nie poprawiaj zapisanych własnych plików. Jeśli materializacja error-report lub manifest także zawiedzie, ujawnij to poza pakietem; nie deklaruj frozen bijection, której brak.

Manifest obejmuje wszystkie fizyczne pliki OUTPUT_ROOT poza sobą, z zero extra/missing/duplicate. **MANIFEST_SHA256.csv jest ostatnim zapisem.** Potem wyłącznie pełny read-only re-hash/bijekcja. Nie dopisuj QC/captures/logów ani kolejnego raportu. Rozmiar/SHA manifestu, wynik verify i exit zwróć poza root. Manifest nie zawiera własnego hasha. Wewnętrzne report/result/QC zapisane przed manifestem są oznaczone PRE_PUBLICATION; terminalny wynik po read-only freeze verification rozstrzyga sukces publikacji i może obniżyć wcześniejszy status przy błędzie. Nie traktuj przedwczesnego COMPLETE w dokumencie jako potwierdzonego freeze.

## 9. Statusy i interpretacja zero/positive

COMPLETE_WITHIN_BOUND jest dozwolone wyłącznie przy pełnym skanie obu kanałów, pin/geometry/input checks, obu hashes, faktycznych limitach i poprawnym freeze. SCIENCE_RESULT to `RAW_INBOUND_REFERENCE_CENSUS_COMPLETE` oraz rzeczywiste liczby; dodatnie trafienie nie zmienia go w CALLERS_CONFIRMED. Zero oznacza tylko brak tych dwóch encoding-shaped wzorców w tych domenach, przy tych alignment i virtual/padding regułach. Nie wyklucza indirect/computed/unaligned/runtime/other-section paths.

Przy błędzie lub przekroczeniu: PARTIAL/BLOCKED_PREFLIGHT zależnie od fazy i `census_complete=false`. Nigdy nie przechodź od PARTIAL do zero-caller inference. CONTROL_PASS i AUDIT_ACCEPTED nie są statusami tego skryptu.

Standing wejściowy `inputs/STANDING.json` zachowaj dokładnie i zwróć jako utrzymane ograniczenia. Wszystkie22 klucze podlegają maszynowemu sprawdzeniu. W szczególności CURSOR_SOURCE_MEDIUM=UNKNOWN, CURSOR_CONSTRUCTION_OR_FILL_UPSTREAM=NOT_ESTABLISHED, WORLD_XYZ_RECOVERED=NO, CANONICAL_GATE_EFFECT=NONE, REPOSITORY_MODIFIED=NO, COMMIT_PUSH=NOT_PERFORMED, NEXT_EXPERIMENT_AUTHORIZED=NO, HARD_STOP=YES. Nazwa „CALLER_DISCOVERY” opisuje pytanie nawigacyjne, nie osiągnięty caller proof.

## 10. Terminal i HARD STOP

Zwróć po polsku RUN_ID/output/report, actual exit/status, source identities z dwóch zmierzonych hashes, exact read ledger total, denominatory i hits obu kanałów, virtual/padding counts, census_complete, cap/error, input/QC outcome, manifest rows/physical/SIZE/SHA oraz limits/unknown standing. Oddziel fakty skanu od hipotez interpretacyjnych.

FIRST_MISSING_EDGE po dodatnim wyniku: „kwalifikacja instruction/data reference oraz przepływu C w osobno wybranym małym oknie”. Po zerowym pełnym wyniku: „inne formy referencji nieobjęte dwoma kanałami”; bez otwierania ich teraz. W obu przypadkach wskazówka nie jest zleceniem wykonania następnego kroku.

Zakazane: disassembly, Ghidra, x86dec, objdump, dalsze full scans, inne targets/sections, callee/caller body, vtable/RTTI traversal, arbitrary path resolution z ledgerów, runtime klienta, network/VFS/BNT/ARK/NIF/model search, renderer/world changes, repo-write, kanoniczne indeksy, commit/push, automatyczne kontynuacje lub naprawy. Po jednym terminalu **HARD STOP**.
