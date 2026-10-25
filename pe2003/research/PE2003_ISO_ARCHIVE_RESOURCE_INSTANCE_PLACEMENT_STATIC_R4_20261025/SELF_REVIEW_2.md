# SELF_REVIEW_2 (root, przed seal — druga faza samoaudytu)
1. Które zdanie wysokiej pewności polega tylko na wygenerowanym output? Liczniki budżetowe (job-reported, QC-spot-checked) — oznaczone PARTIALLY_MEASURED w BUDGET_LEDGER.
2. Predykat słabszy niż brzmi? G-SEAL asserts manifest bijection — wykonywane teraz; G-A04 covers corpus-scope absence, nie global absence — prosa REPORT trzyma "w przypiętym korpusie".
3. Czy spłaszczyłem stany? Nie: RUN_ACCEPTED_WITH_ERRATA (QC verdict) to nie MILESTONE_PASS; kampania statyczna nie promuje się do placement closure. EXTERNAL_POSTAUDIT=PENDING.
4. Czy późniejszy commit mógł usunąć wynik? N/A (nie-git korpus audytowy; seal przez manifest + przyszły sanitizowany commit).
5. Czy następna akcja jest wykonywalna na żywych celach? HANDOFF wskazuje dokładne warunki; kampania dynamiczna i pozyskanie PE_PCG.ark wymagają decyzji człowieka — nie sfabrykowałem autoryzacji.
6. Claim poza osobiście audytowanym zakresem? Nie twierdzę weryfikacji pełnej semantyki entry typów 0..8 (UNVERIFIED); Ghidra cross-check LOW (4 zawieszone próby udokumentowane).
7. Pozostaje NOT_CHECKED: pełny dekód 135 TYPE_ONLY (zachowany limitation); konsument Download.data poza korpusem (UNVERIFIED, nie sfabrykowany).
SELF_FINDINGS_DETECTED = 1 (punkt 1 budżety) -> SELF_FINDINGS_RESOLVED_IN_FINAL_DRAFT = 1 (oznaczone PARTIALLY_MEASURED w BUDGET_LEDGER przed publikacją).
