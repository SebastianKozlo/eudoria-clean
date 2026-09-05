# PE_MASTER_REVIEW — the RUN-1..RUN-4 package verdict + the x87 CW design review
# Persisted VERBATIM per the three-tier operating model (§22.5) by pe-master-auditor.
# Scope: the RUN-1..4 package (RUN-1 = the governance commit 642bc12 [no run dir];
# RUN-2 = the TESTAI runtime sync [no repo dir; the sync record = the SHA verification
# in this verdict]; RUN-3 = this run dir; RUN-4 = PE_LOOP_CALIBRATION_R1_20260905_120600).
# This file is placed in BOTH run dirs (RUN-3, RUN-4) — append-only; no old file edited.

OD PE-MASTER (główny audytor — werdykt paczki RUN-1..RUN-4):MASTER_ACCEPTED — pełny
audyt z dysku potwierdził: RUN-2 sync 6/6 (moje hashe IDENTICAL; AGENTS.md/opencode.json
nietknięte), RUN-4 kalibracja (19 plików/917170 B; 776 claims = 41 MATCH + 3 SUPERSEDED +
0 MISMATCH + 638 external + 94 unknown; write-ahead przez 3 dispatche; oba defekty
detektora naprawione jawnie; V4.json == 003056AC moje), governance scope czysty.
DESIGN REVIEW x87 CW (RUN-3) = MASTER_ACCEPTED — DESIGN APPROVED (adresy i
bajty zgodne z moimi niezależnymi odczytami; site-local read = słuszny;
interwencje jawne; W4 kompletne; NOT_EXECUTED dotrzymane). G1 = SPEŁNIONE.

=== HUMAN GO RUNTIME (this relay = the human's explicit GO — cytat autoryzacji) ===

KROK A (natychmiast, automatyczne): zbuduj OPERATOR KIT dla wykonania x87 CW:
  1. Fresh RUN_ID: PE_M1_X87CW_EXECUTION_R1_<ts> + własne drzewo runu
     (99_Audits + mirror); design package = pinned input (re-hash WSZYSTKICH
     pinów na starcie — standing rule).
  2. Sandbox wg designu W3.1: portable x32dbg (pin 822028F0) + working copy
     Entropia.exe + pcg_install prerequisites (Data\ + DLL-e + configi);
     hash pre-verify E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31
     / 8,015,872 B — fail-closed ABORT przy niezgodności, PRZED jakimkolwiek
     uruchomieniem. Oryginał pcg_install NIGDY nie uruchamiany.
  3. Operator checklist (krok po kroku z W3.2-W3.5): spawn → module-base check
     (0x00400000 albo delta) → BP1 0x0098CE5A + BP2 0x0095B2BC hardware
     (pre-verify bajtów DC 35 A8 D7 A7 00 / DD 05 58 C7 A8 00) → init CW
     (aux read C) → N=10 hits/site: FPU-panel CW + JSONL linia + screenshot
     per hit → cross-site agreement → liveness §14 (terminate + niezależny
     dowód OS + ACTIVE_ORPHANED) → bounded window 30 min.
  4. Puste szablony: 04_RUNTIME\cw_capture.jsonl + SESSION_LOG.txt +
     JSONL validator (skrypt sprawdzający linie przy ingest).
  5. Zakaz: NIE symuluj pomiaru, NIE uruchamiaj klienta sam (manual GUI =
     operator człowiek; automation blocker honest). Twoja rola = KIT gotowy
     + komendy + walidator.
KROK B (po ręcznym pomiarze przez człowieka): ingest JSONL (validator), zbuduj
  raport z exact verdict string: MEASURED-PC53 / MEASURED-PC64 /
  MEASURED-PC24-DEFECT / OPEN-<class> (+ RC honesty bound: RC≠nearest-even →
  osobny sub-item, NO silent pass); pakiet + jeden path-limited commit + push
  + remote SHA verify → raport do PE-MASTER (przez człowieka) → mój post-audit.
KROK C (równolegle, czysto biurowe): persistnij mój werdykt RUN-1..4 (ten blok)
  jako PE_MASTER_REVIEW.md w run dirach (append-only; bez edycji starych plików).
ZAKAZY bez zmian: żadne M2; żadne payloady; jeden run = jeden commit;
  runtime = TYLKO ten kit x87 CW (nic poza designem).

EXECUTION RECORD (pe-master-auditor, this session):
- KROK A EXECUTED (commit 83c89b4, pushed, remote verified): the kit built by
  pe-master-auditor directly (the Task tool is denied in this session per the
  operating model; the KROK A mandate = a bounded assignment executed by the
  orchestrator). RUN_STATUS = OPERATOR_KIT_READY: the sandbox hash-verified
  (verify PASS 20/20), the operator checklist composed verbatim from the
  approved design W3, the validator fail-closed-PROVEN (the self-test rejected
  the 3 invalid fixture classes), the templates empty, ZERO runtime executed
  by the builder. The x32dbg-source note: the design's literal path
  (D:\x64dbg\release\x32\) does not exist on disk; the pin-identical portable
  (822028F0...) located at the C3_X32DBG calibration tree + re-verified before
  and after the copy — THE PIN IS THE BINDING IDENTITY (documented in
  KIT_COMPOSITION_RECORD.md).
- KROK B = PENDING the human operator's manual session (the next human act).
- KROK C EXECUTED (this file; placed in docs/audits/
  PE_M1_X87CW_EXPERIMENT_DESIGN_R1_20260905_115209/ + docs/audits/
  PE_LOOP_CALIBRATION_R1_20260905_120600/ + the local trees; append-only).
