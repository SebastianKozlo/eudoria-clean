# PE RECONSTRUCTION — KANONICZNE ZASADY

## OPENCODE MASTER AGENT (PE-MASTER)

Preferowany agent nadzoru, decyzji i orkiestracji: **pe-master**
(`.opencode\agents\pe-master.md`). Jest nadrzednym kontrolerem read-only dla
kodu projektu: bezposrednio deleguje ograniczone zadania wykonawcom, audytuje
ich wyniki z fizycznych dowodow, rozstrzyga sprzecznosci, nakazuje poprawki i
wybiera nastepny eksperyment. `pe-master-auditor` jest jego agentem
formalizacji/internal-QC i utrwalenia werdyktu, a `pe-reconstruction` oraz
agenci specjalistyczni sa wykonawcami.

Trwala pamiec projektu (czytaj na starcie sesji):

- `00_PROJECT_CONTEXT\PE_CURRENT_CHECKPOINT.md` — szybki bootstrap
- `00_PROJECT_CONTEXT\PE_WORKFLOW_RULES.md` — regululy operacyjne
- `00_PROJECT_CONTEXT\PE_MASTER_CONTEXT.md` — pelny kontekst
- `00_PROJECT_CONTEXT\PE_CANONICAL_STATE.json` — stan maszynowy
- `00_PROJECT_CONTEXT\PE_CONTEXT_SOURCES.md` — rejestr zrodel
- `00_PROJECT_CONTEXT\PE_SESSION_HANDOFF.md` — ciaglosc sesji

Dowod fizyczny (Tier 0/1) przewaza nad notatkami i INDEX.md. Nie aktualizuj
INDEX.md / PE-Vault / skills przed niezaleznym post-auditem (ChatGPT).

Backup starej konfiguracji AI: `99_Audits\PE_OPENCODE_MASTER_AGENT_BOOTSTRAP_20260901_020333\00_BACKUP\`

## Cel

Rekonstrukcja Project Entropia 2003, szczegolnie:

- BNT/TDF, Terrain_patch, Patch Manager
- geometria terenu, materialy
- render packet registration, renderer DirectX
- lokalny login/world server

## SRODOWISKO WYKONAWCZE — VM ONLY

Cala praca projektu PE odbywa sie wylacznie wewnatrz maszyny:

- Windows VM hostname: WinDev2407Eval
- Windows VM IPv4: 172.17.243.158
- Projekt: D:\Eudoria_Reconstruction / /mnt/d/Eudoria_Reconstruction
- Vault Obsidian: D:\Obsidian\PE-Vault / /mnt/d/Obsidian/PE-Vault
- WSL: PE-AI

### Wymagana izolacja

- Nie zapisuj zadnych wynikow na fizycznym laptopie
- Nie uzywaj sciezek hosta Hyper-V
- Nie korzystaj z przekierowanych dyskow RDP
- Nie tworz raportow poza VM
- Wszystkie skrypty, logi, artefakty, projekty Ghidry musza pozostac na dyskach VM

## Architektura

- Hermes = orkiestracja (zadania, zaleznosci, harmonogram, retry, statusy, handoffy)
- OpenCode = wykonanie (analiza plikow, skrypty, raporty, zmiany)
- Obsidian = pamiec kanoniczna (fakty, checkpointy, historia decyzji)
- AionUI = konsola czlowieka (reczna rozmowa, kontrola, awaryjna interwencja)
- Ghidra = statyczny reverse engineering i P-code
- x32dbg = dynamiczne breakpointy, watchpointy, pointer equality

OpenCode uzywa jednego kontrolowanego poziomu delegowania:

- PE-MASTER moze uruchamiac bezposrednich wykonawcow przez Task.
- Wykonawca zawsze zwraca wynik do PE-MASTER i nie uruchamia kolejnego agenta.
- Tylko jedna aktywna sesja PE-MASTER AUTO LOOP moze byc writerem stanu petli.
- Zadania mutujace repo sa sekwencyjne; nie wolno miec dwoch writerow naraz.

`subagent_depth = 1`

Operational clarification (night-loop repair R2): direct workers are
pe-reconstruction and pe-master-auditor. The latter may autonomously formalize,
correct assigned documents/metadata and publish an explicitly scoped package;
it does not replace PE-MASTER's independent review. Current routing is defined
by .opencode/agents/pe-master.md §13, overriding legacy workflow/skill routing
only. Scientific evidence, Q1 and human milestone-closure gates remain unchanged.

Tryby bezobslugowe: `loop 2h`, `loop 4h`, `loop 8h` lub `/pe-loop 2h|4h|8h`.
Samo `loop` oznacza 8h. Limit jest deadline'em, nie obietnica dzialania po
uspieniu VM, zatrzymaniu OpenCode albo utracie uslugi modelu.

## Statusy dowodow

CONFIRMED
STRONGLY_SUPPORTED
PLAUSIBLE
UNVERIFIED
REJECTED

## Zasady

- Kazdy run musi miec nowy RUN_ID
- Nie modyfikuj zakonczonych runow
- Kazdy run zapisuj w: 99_Audits/<RUN_ID>
- Nie deklaruj ciaglego mostu bez pointer provenance
- Nie zwiekszaj MAPRE za sama dekompilacje, liczbe plikow lub hipoteze
- Nie modyfikuj PE.exe
- Tylko jeden agent moze zapisywac aktywny projekt Ghidra
- Tylko pe-archivist moze zapisywac do Obsidian
- Poza biezacym kontraktem delegacji narzedzia (tools/, scripts/) zmienia
  pe-toolsmith. W autoryzowanym loopie PE-MASTER moze jawnie przypisac
  ograniczona zmiane tych narzedzi pe-reconstruction; wymaga ona internal QC
  i niezaleznego audytu PE-MASTER przed uzyciem jako zaufana podstawa dowodu.
- Tylko audytor moze rekomendowac zmiane MAPRE
- Rozdziel mechanical score od audited score
- Nie utozsamiaj podobnego vptr z pointer equality
- Nie uzywaj nazw klas bez dowodow
- Zasada exact pointer levels
- PRE-AUDIT -> CHECKPOINT -> EXECUTION -> AUDIT -> ARCHIVE

## Wymagane artefakty (kazdy run)

- REPORT.md
- STAGE_ACCEPTANCE_GATES.csv
- artifact_index.csv
- HANDOFF.md

## Locks

- GHIDRA_WRITE.lock — jeden agent zapisujacy Ghidra jednoczesnie
- OBSIDIAN_WRITE.lock — tylko pe-archivist
- CANONICAL_DOCS.lock — tylko pe-archivist po ACCEPTED

## Aktualny checkpoint

MAPRE: 23/30 = 76.7%
Terrain Material Pipeline: 14.8%

### Potwierdzone fakty

- record+0x00 = Terrain_patch
- Terrain_patch size = 0x130
- Terrain_patch vptr = 0x005E30CC
- FUN_00590ED0 = generic property setter
- Terrain_patch slot 8 = update, nie render
- FUN_005700E0 zapisuje entry+0x48
- FUN_005700E0 uczestniczy w rejestracji render packetow

### Otwarte krawedzie

- record+0x00 -> caller FUN_005713F0 -> FUN_005700E0 -> packet+0x48 -> packet consumer -> render item -> DrawIndexedPrimitive
- render_state+0x0C writer -> root identity -> root+0x28 -> SceneContext -> SceneContext+0x20 -> live element
