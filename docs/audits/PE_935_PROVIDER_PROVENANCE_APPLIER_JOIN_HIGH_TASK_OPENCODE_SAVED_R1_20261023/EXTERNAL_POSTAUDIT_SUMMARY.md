# Zewnętrzny postaudyt SLOT1 MINCAP / WRITER SOURCE

SCIENCE_VERDICT = PARTIAL_PASS_WITH_MATERIAL_CORRECTIONS
PROCESS_VERDICT = PARTIAL_NONCOMPLIANT_WITH_ACCOUNTING_GAPS
BYTE_INTEGRITY = PASS (75 rows + manifest = 76 files)
INPUT_PINS = PASS (724)
CAPTURE_RECEIPT = PASS (saved header +4cells+21reads+16035856B; source not reopened)
PACKET_PARITY = PASS (357 rows /357uniqueVA/0mismatch to pinned H5)
NATIVE_TASKS = PASS (11;9workers/2auditors;10stop/1length;parent/prompt parity11/11;zero grandchildren)
PUBLICATION = PASS (11/11 blobs,12diffpaths,entrypoint1/0,commit4edaddebe8677dccb0894a5d4f6ac78f6e4e7282)
CANONICAL_GATE_EFFECT = NONE

MSC-A01 [P1/P2]: zachować dokładne poziomy wskaźników. B=this00528380, R_i=M32[B+0xC] na poszczególnych callsite, P_i=M32[R_i+0x2C] w producerach. Slot+0x28/+0xDC/+0x160 jest z vtable P_i, nie z B i nie z tabeli R. [B+0x2C] ma inny status i wcześniejszy zero-init przez embedded ctor B+14+18; to nie jest dowód writera [R+2C]. Reload po opaque CALL nie gwarantuje R1=R2 ani P_guard=P_value. Sformułowanie FIRST_MISSING_EDGE „[this+2C]” trzeba zastąpić obiektem/VA/czasem. To uszczegółowienie kierunku, bez negacji potwierdzonej mechaniki obu helperów.

MSC-A02 [P2]: znaleziono więcej niż sam cache. W00528380 istnieje CALL0085CDE0@005284AC z this=R; następuje PRZED odczytami C0C0/C280 do cacheB. Niezależny wcześniejszy postaudyt RECORD_HEAD już wykazał przekazanie przekształconego bloku do[[X+2C]vt+14] i warunkowy cache52B X+30. Roli world/root nadal nie dowiedziono, ale brakrelevance nie może pomijać tej istniejącej krawędzi do applier-a. Następny kontrakt powinien zestawić wejście/aplikację/odczyt/cache, zamiast wyłącznie rozwijać getter. Nie wolno od tego awansować XYZ.

MSC-A03 [P2]: enum[M32[B+C]+20]==3 nie bramkuje całego cache writera. Równość3 wybiera gałąź tworzącą macierz identity, nierówność wywołuje0096CCB0; obie dochodzą do528434 i potem applier/cache. Globalnymi strażnikami wejścia są nullB+C/B+10. Rozdziel te predykaty. Zachować14directstores self-cache/flags/globaltriple jako mechanikę H5; efekty wywołanych metod są szerszym, odrębnym pytaniem.

MSC-A04 [P2]: STATIC_CLASS_VTABLE_BINDING jest rzeczywistym wynikiem ctorstoreA7DCB0. Nie jest REGISTER_LOOKUP_JOIN. CL-7 i REPORT podstawiają tę inną kategorię pod dotychczasową nazwę, choć actualregisteredobject→lookup→call pozostaje nieudowodnione. Wprowadzić osobne pole STATIC_CLASS_VTABLE_BINDING=ESTABLISHED_AT_SAVED_CONSTRUCTION_LEVEL i REGISTER_LOOKUP_JOIN=NOT_ESTABLISHED. Podobnie „baseclassUNKNOWN w tymrunie” nie usuwa istniejącego prior0085B1B0/A91E4C. PER_RUN_NOT_READ i PRIOR_AVAILABLE nie są DATA_BARRIER.

MSC-A05 [P2]: accountingQC PASS nie obejmuje realnych rozbieżności. BODYcount4 wyklucza nawet semantycznie użyty thunk i jego2siblings; minimum7ciał, dalsi sąsiedzi wymagają osobnego rozliczenia. Pole neighbor_stubs_counted bez dodania do count nie jest rozliczeniem. WRITER_SOURCE_CHAIN ma jawnie4/3 w ledgerze; sam dopuszczony alternatywny tematC nie znosi globalnego capu tej zadeklarowanej rodziny. Jeżeli miała istnieć osobna rodzina, potrzebny jest wcześniejszy przydział, nie retoryczne wyłączenie po fakcie. Brak ADMIT QSCI/QACCOUNT w końcowym ledgerze przy realnych odczytach tych dzieci; deklaracja „admit_precedes_each_semantic_read=true” jest zbyt szeroka, już nawet PD-1 ją ogranicza. MetadataSTARTSHA zawiera literówkę, podczas gdy helper/result mają właściwy pin; zachować oryginał i addytywną korektę. Python/helperdoclines włączone do „code_exposures” mieszają jednostki; te liczby nie są wiarygodnym dolnym oszacowaniem samych x86exposures. Bez exactcapPASS. Dozwolony length/retry sam nie jest noncompliance.

MSC-A06 [P2]: capture statycznych komórek i scalar-copy obu helperów zachowane. C280 ma jednak dwa guardy ([R+24] oraz callPslot160(0x80)) i literalny zero-fallback; nie każdy powrót pochodzi z slotDC. Na activepath kopiowana jest zawartość wskaźnika zwróconego wEAX, nie automatycznie przekazanego lokalnego bufora. Tożsamość returnedpointer/localbuf pozostaje przesłanką, nie faktem. Nowa analiza ma rozdzielić zero-path/returned-storage i skutki opaqueCALL.

Zachowane: nowe static targetsBASE95D4FA/DERIVED528380,controls85B6A0/5278A0; thunkprzezA75378 nadalNOT_READ; ctorA7DCB0exactmatch; callerout-copy i mechanika14stores. SOURCE_CAPTURE_PASS zweryfikowano na zapisanych danych i ledgerze, bez ponownego otwarcia oryginału; hashy źródła nie mierzyliśmy na nowo. Nie dowiedziono runtimeVT, receiverpreservation, scene-root/modeljoin/building/history.

Następny run: jednorazowy HIGH dla mastera i nativeTask dzieci, MAX zakazany. SAVED_ONLY: bez nowego capture, także bez czytaniaA75378. Priorytety: dokładny B→R→P i writer/ctorP; oraz applier0085CDE0→Pslot14→rzeczywiste destination/source. SDKGamebryo źródłowo jako porównanie po operacji, nie ABIoracle. Powiązania world/instance/resource/history muszą być dowiedzione oddzielnie.

WORLD_XYZ_RECOVERED=NO;HISTORICAL_PLACEMENT=NOT_ESTABLISHED;CURSOR_SOURCE_MEDIUM=UNKNOWN;CANONICAL_GATE_EFFECT=NONE.
