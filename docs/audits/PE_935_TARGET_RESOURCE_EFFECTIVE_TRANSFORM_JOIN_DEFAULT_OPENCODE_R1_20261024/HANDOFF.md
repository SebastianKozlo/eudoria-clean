# HANDOFF — PE_935_TARGET_RESOURCE_EFFECTIVE_TRANSFORM_JOIN_DEFAULT_OPENCODE_R1_20261024

AUDIT_OUTPUT_ROOT = D:/Eudoria_Reconstruction/99_Audits/PE_935_TARGET_RESOURCE_EFFECTIVE_TRANSFORM_JOIN_DEFAULT_OPENCODE_R1_20261024
FINAL_REPORT_PATH = AUDIT_OUTPUT_ROOT/REPORT.md
PRIMARY_EVIDENCE_PATHS = PACKETS/ (18 plików, source SHAs w nagłówkach), JOBS/*/RESULT.md, QC/EVIDENCE_SNAPSHOT_PRE_QC.txt
RUN_STATUS = COMPLETED; HARD_STOP_REASON = none (terminal kampanii osiągnięty w granicach kontraktu)

## Stan nauki (do przejęcia)
1. T=M32[B+0xC0] = SceneFeederObject — CONFIRMED (łańcuch akwizycji domknięty bajtowo; patrz REPORT §1).
2. Mapa pól transformacyjnych T domknięta po stronie writerów (REPORT §2); reader +0x4C = bounded negative.
3. H = wartość z providera pod [mgr+0] (manager 0x8C @0xBA12E8), NIE obliczana w 00853A80; clamp v1.z=max(v1.z,H) przy ordered GT.
4. Creator arg4 ctor = stała 1 (nie model_id) — domknięte.
5. Selector: writer→reader preservation potwierdzone bounded; kierunek H potwierdzony counter-checkiem mastera.

## Najlepszy frontier (FME — pierwszy brakujący brzeg)
A. Reader bloku T+0x4C (36B): przeszukać konsumentów SFO poza vtable (targeted: callsite'y 00509510/0096CDD0 → konsumenci 0048BAC0-rodziny; NIE census wszystkich vtable).
B. Klasa providera H: vtable obiektu instalowanego pod [mgr+0] — zlokalizować writer mgr+0 (zapis runtime-install providera) z zapisanych okien; identyfikacja klasy providera rozstrzygnie terrain-height.
C. Klasa linka SFO+0x30 (ctor 007B6000, obiekt 0x118) — next-test z SCENEFEEDER_SLOT_CENSUS REPORT.
D. Model-resource join: payload+0x0C typed sub-object (type tag +0x20==3) + blok 004C49BF + lookupy 004C4981/004C4A9D.
E. Path B 0096CDD0 (bajty ≥0x0096CE9F) + wartości K/eps.

## Zakazy przenoszone
ZERO nowych odczytów EXE/assetów/cache/NIF bez odrębnego autoryzowanego harmonogramu. Saved sources only. WORLD_XYZ_RECOVERED=NO do pełnego dowodu autentycznej instancji i wartości.
