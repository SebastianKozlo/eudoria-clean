# Jednocelowy census RAW odniesień

RUN_ID = PE_935_PARAMETER_CURSOR_CALLER_DISCOVERY_R1_20261016
PUBLICATION_STAGE = PRE_PUBLICATION (status wymaga terminalnego freeze PASS)
RUN_STATUS = COMPLETE_WITHIN_BOUND
SCIENCE_RESULT = RAW_INBOUND_REFERENCE_CENSUS_COMPLETE

Target: 0x00852A30.
Zachowane kandydaty RAW: 1.
Census zakresu RAW: ukończony.

Skan obejmuje E8/E9 rel32 na każdym bajcie .text z dostępnymi 5 bajtami oraz
DWORD równy targetowi na wyrównanych do 4 B RVA w .rdata. Arytmetyka rel32 jest modulo 2^32.
RAW padding i pełny span w VirtualSize są jawnie rozróżnione dla każdego kandydata.
Kandydat nie dowodzi głowicy instrukcji, callsite, funkcji caller, producenta kursora ani roli świata.
Brak dopasowań nie dowodzi braku callerów programu; pośrednie referencje i inne encodingi są poza zakresem.
Nie wykonano decode ani odczytu bodies. Nie zapisano całego EXE ani sekcji.

SOURCE_UNCHANGED = YES_IN_TWO_COUNTED_HASH_PASSES_AND_SIZE_CHECKS
Limit odczytów: 23814144 B; ledger obejmuje także pełne hashe i nagłówek.
Manifest jest ostatnim zapisem. Jego fizyczny census i identity zostają zwrócone wyłącznie na stdout CLI.
Log wewnętrzny nie jest capture stdout/stderr procesu systemowego.

Rzeczywiste oryginalne reads: 23814144 B;
konserwatywny debit: 23814144 B.

.text: eligible evaluated=6766588; expected from mapping=6766588; retained=0; full span=0; crossing=0; raw padding=0.
.rdata: eligible evaluated=252928; expected from mapping=252928; retained=1; full span=1; crossing=0; raw padding=0.

Standing dziedziczony z przypiętego inputs/STANDING.json:

```ini
FIELD_SEMANTICS = UNVERIFIED_EXCEPT_SCOPED_WIDTH_AND_ADDRESS_FACTS
CURSOR_SOURCE_MEDIUM = UNKNOWN
CURSOR_CONSTRUCTION_OR_FILL_UPSTREAM = NOT_ESTABLISHED
ACTUAL_ADVANCE_HELPER_EFFECTS = NOT_ESTABLISHED
ACTUAL_VIRTUAL_CALLEE_TARGET = NOT_ESTABLISHED_UNLESS_DIRECTLY_EVIDENCED_IN_SCOPE
ACTUAL_VIRTUAL_CALLEE_EFFECTS = NOT_ESTABLISHED
ALLOCATION_RETURN_EQUALS_INITIALIZATION_RETURN = NOT_ESTABLISHED
STATIC_BUILDING_ROLE = NOT_ESTABLISHED
MODEL_218757_TO_THIS_PARSER_INSTANCE = NOT_ESTABLISHED
MODEL_218757_TO_CMO_JOIN = NOT_ESTABLISHED
WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED
HISTORICAL_PLACEMENT = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
PREDECESSOR_PROCESS_TERMINAL = PARTIAL
RETROACTIVE_AUTHORIZATION = NO
CANONICAL_GATE_EFFECT = NONE
REPOSITORY_MODIFIED = NO
COMMIT_PUSH = NOT_PERFORMED
EXTERNAL_POSTAUDIT_OF_THIS_RUN = PENDING
NEXT_EXPERIMENT_AUTHORIZED = NO
NEXT_MILESTONE_AUTHORIZED = NO
HARD_STOP = YES
```

FIRST_MISSING_EDGE = kwalifikacja instruction/data reference oraz przepływu C w osobno wybranym małym oknie.
HARD_STOP = YES
