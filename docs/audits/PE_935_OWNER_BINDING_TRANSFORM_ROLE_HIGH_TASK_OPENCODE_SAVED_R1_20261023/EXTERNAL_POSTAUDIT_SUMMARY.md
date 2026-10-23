# Zewnętrzny postaudyt OWNER VIRTUAL SETTER / SCENE BRIDGE

SCIENCE_VERDICT = PARTIAL_PASS_WITH_MATERIAL_CORRECTIONS
PROCESS_VERDICT = PARTIAL_NONCOMPLIANT_WITH_WORKER_ARTIFACT_FORMAT_DEFECTS
BYTE_INTEGRITY = PASS (38 rows + manifest = 39 files)
INPUT_PINS = PASS (521 authoring pins + 16 discovered-entry checks)
NATIVE_TASKS = PASS (10; 8 workers + 2 auditors; all stop; parity/binding 10/10; no grandchildren)
PUBLICATION_INTEGRITY = PASS (11/11 public blobs, diff bijection and remote)
CANONICAL_GATE_EFFECT = NONE

VSB-A01 [P1]: ((q-A)+A) nie jest bezwarunkową tożsamością w arytmetyce zmiennoprzecinkowej. Getter0085B6A0 po clamp-slot wykonuje FLD qword[A7B508], FSUB ST1,ST0, FADDP i FSTP float. QC określiło to jako value-preserving bez znajomości stałej i control word. Własny dokładny model binary-round-to-nearest-even daje kontrprzykłady dla precision24/53/64: q=1, A=2^(p+2), output0. To syntetyczny kontrmodel, nie dowód wartości rzeczywistej stałej. Zatem emit-Z=min(D+40,const) NIE jest jeszcze potwierdzone; zachować z=FPU_roundtrip(clamp_slot). Kierunek ordered finite pre-roundtrip clamp jako upper bound pozostaje ważny. Unordered/NaN zachowują osobną ścieżkę, nie ogólną funkcję min.

VSB-A02 [P1/P2]: pełny predykat głównej gałęzi to type∈{3,4,5,6,7} OR ([this+0x7C]==0 AND [this+0x78]!=0). JNZ po CMP[this+7C],0 idzie do ZERO-vector path, nie do main. RESULT V01 ma błędne „+7C≠0 lub +78≠0 → main”. Raport skraca predykat do typu3..7. Odróżnić trzy wyjścia: main+nonnullD, main+nullD i zero fallback. Scalar[D+40] jest źródłem clamp-slot, ale rola height/offset/world-position pozostaje UNKNOWN.

VSB-A03 [P2]: analogia G01→PROPAGATE_WORLD nie ma rozstrzygających cech. Badany out-vector getter nie odczytuje parent world/local matrix i nie zapisuje world transform; flagi, trzy floaty i base fallback są ogólne. W localSDK faktyczna implementacja Win32 pokazuje parent-world*local. „Closest of six” bez NONE_OF_THE_ABOVE nie jest dodatnim dowodem klasy. CL-13 zawęzić do ENGINEERING_REFERENCE_ONLY / PE_OPERATION_CLASS=UNKNOWN. Generic strcmp lub podobny refcount bracket także nie identyfikuje extra-data/attach bez object-specific dataflow. SDK export NIF10.2 vs assets10.1 nie dowodzi wersji runtime PE.

VSB-A04 [P2]: slot3 inventory fields są zachowane; dodatkowo Desktop przeczytał generator (phase_b_rtti.py253..259: entries[3]) i helper extent (step4 od base), bez ich wykonywania. To potwierdza konwencję offset+0xC w saved projection, nie nowy odczyt fizycznych komórek EXE. Class/13-codepointer extent to opis wyniku skanera, nie automatycznie kompletny ABI. Brak literalnego adresu komórki VT+4 w tekście nie jest proof braku jej wartości w strukturze {table_base,entries[1]}; następny search musi być schema-aware. Actual receiver linkage nadal NOT_ESTABLISHED; brak vptr install wewnątrz consumer body sam nie jest dowodem typu ani jego braku.

VSB-A05 [P2]: L01 ma ZERO_DIRECT_STORES, lecz JMP00413440 pozostawia transitive effects UNKNOWN, dopóki nie użyto właściwego prior/ciała. „Acquire” to interpretacja, nie rozstrzygnięcie przez sam thunk. Równocześnie M01/REPORT błędnie opisują004154F0 jako transformację klucza. Prior kanon już wykazał singleton getter z plainRET, ignorujący pozostawiony PUSH. Lookup key pochodzi z pre-window stack value przekazanego PUSH; EAX gettera jest receiverem managera, nie nowym kluczem. Faktyczna równość z[B+74] nadal OPEN, lecz nie z powodu rzekomego opaque key transform.

VSB-A06 [P2]: końcowy census10/10 i root canonical formats poprawiły się. Nadal oba worker CSV są źle ucieczone: BRANCH_COVERAGE ma4wiersze szerokości6 zamiast5, CANDIDATES2wiersze13 zamiast12. PowerShell Import-Csv nie dowodzi stałej szerokości. QSCIENCE381/320 pozostaje naruszeniem; packet≤cap nie obejmuje wszystkich dodatkowych odczytów i cytatów. R1 correction jest worker re-derivation, nie nowym fresh QC wszystkich poprawionych tez. Zachować QC_PARTIAL i disclosures; nie awansować całego proofu na independent PASS.

Zachowane wyniki: saved slot3 targets0085B6A0/005278A0; derived global-triple/base-fallback mechanics; pure scalar getter00861320=[ECX+40]; out-pointer/RET4 contracts; empty-bucket tail out-pair; bounded brak qualified writera. Nie odzyskano actual VT+4 ani world-instance/resource/building identity.

WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; CURSOR_SOURCE_MEDIUM=UNKNOWN.
Nowy eksperyment PE, runtime i odczyt oryginalnych assets/EXE NIE zostały wykonane. Frozen run i repo niezmienione.
