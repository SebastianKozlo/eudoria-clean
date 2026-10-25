# VALUE_ORIGIN_MAP — PE2003_ISO_MODEL_BINDING_VALUE_ORIGIN_STATIC_R5_20261025

RUN_ID: PE2003_ISO_MODEL_BINDING_VALUE_ORIGIN_STATIC_R5_20261025 | BUILD: ISO2003NOV_PE_5_1_0_0 | DATE: 2026-10-25
PROVENANCE: jobs/A01/D01/D02/D03/D04/J01/J02/J03/J05 RESULT; companion strict: SOURCE_PROVENANCE.json. Kompanion ról: OBJECT_AND_ID_MAP.md, ROLE_LEDGER.json.

## 1. Pytanie kampanii

Skąd biorą się wartości a1..a6 fabryki 0x4578E0 (entity transform-setter) — i czy łańcuch wartości domyka się od komunikatów/NIF do entity/SFO?

## 2. Świadectwa źródeł wartości (zmierzone)

### 2.1 Wiadomości (handler 51C930/51C880 family) — potwierdzone dla kluczy/selektorów, NIE dla a1..a6
- **47CFB0 → 45DE90/45D5F0** (record creation): entity-id, selektor K, klucz wizualny pochodzą z komunikatu (J01 S8/S9/S10).
- **47DFB0** (visual-key handler): klucz wizualny = argument komunikatu → 45E2A0 → 473E50 → 46F1A0 → 52A130 (J01 S10).
- **0x47B8A0** (caller 527A00/527BC0): string klucza = msg_arg1; separator ':' (strchr-like [0x65A24C] runtime ptr); flaga = [msg_arg2]≠0 (create/release typu-7); receiver chain 4579E0(msg_arg0 id)→54FD40→W→46EC60→P (J03).
- **0x4859A0** (caller 498B80): arg1=[msg_arg0] (deref), arg2=string z msg_arg2 (ctor [0x65A6AC]); forwarded verbatim do [[inner]vt+0x3C] — potencjalny open-by-name z nazwą z komunikatu (J03 caller B).
- **0x47E0E0 (call site 0x47E13E → 526AE0)**: skan bufora na ':' (cmp cl,0x3a); 526AE0 woła 52A130(edx=wynik 457C80(this), ecx=wartość ze stosu caller-a [push ebx @0x47E128], 0) — args handler-local (J05 T8/T9).
- Werdykt: **strumień komunikatów jest potwierdzonym źródłem kluczy i selektorów**; NIE zmierzono żadnej krawędzi komunikat→a1..a6.

### 2.2 Lazy-create (K=0, I=[E+0x40])
Writer 0x46E990 po łańcuchu setterów: I=[E+0x40] (fresh, getter 0x553220), push I, push LITERAL 0 (byte-proven `push 0` @0x46E9D0), call 0x457980(M,0,I) → 451210(O,0) → 45DE20 (vector-at-index [O+0x10]) → 473E90 → [E+0xF8]=P. K=0 to LITERAL, niezależny od a1..a6; I to jedyny writer-generated lookup input (D01 §6 re-derived).

### 2.3 Init 45D5F0 (init-set) i 45DE90 (on-demand)
Jedyne 3 zmierzone in-image witryny 477FC0 (0x45D6A6/0x45D7BF w 45D5F0; 0x45DF00 w 45DE90) = cały łańcuch tworzenia rekordów; 477FC0 hardkoduje flag=0 → gałąź provider [[SUB+0x18] vt+4] statycznie martwa → [rec+0x38]=NULL przy każdym in-image utworzeniu (J05). LOCAL CODE dla dwóch domyślnych rekordów nie ustala źródła całej populacji (kontrakt §8 upheld).

### 2.4 Config-literals (VFS initializer 0x45E4F0)
'textures.ark'/'models.ark'/'musdef.bnt'/'parameters2.bnt'/'strings2.bnt', ścieżki '\models\'/'\sounds\', wzorce X+'.nif'/'.dds'/'.tga' — STAŁE literalne config, doklejane przez 0x565C90/0x565A60 (wszystkie refy z tej funkcji). Człon "name" ze stałych tabeli konfiguracyjnej — NIE z komunikatu, NIE per-model. Funkcja nie zasila 52A130/564890 żadną zmierzoną krawędzią (J02 T1/T2).

### 2.5 Literały stringów czytelników M-cell (D04)
"ArkClientPlayerControlledLocal" (0x6B930C, 3 hity — tylko czytelnicy), team-kick (0x6B9330), team-full (0x6B9378) + własne 1-2 stack args czytelników → sink 45B010(esi=[O+0x2C], buf, value) → binding map pod kluczem 0x4B9 w kontenerze singletonowym. Wartości tekstowe UI/team, NIE transform.

## 3. Świadectwa a1..a6 — status upstream

**UNRESOLVED (D01/D04 SCOPED_NEGATIVE + BARRIER).** Ścieżka mierzona kończy się na fabryce: [unreconstructed virtual callsite: 6 pushes, this=M+0x08] → 0x4578E0 → a1..a6 forwarded verbatim (nic nie dodaje). Domknięte negatywnie (wszystkie bounded receiver-constrained forms):
- global 0x6C4C58 → +8 → slot0: EMPTY (3 readery M-cell = stringi/producenty wartości, zero dispatchy);
- slot-22 alias 0x65BE44: ELIMINATED (D03: 37 realnych witryn +0x58 na klasach ≥23 sloty; 0x65BE44 ma 3 sloty; pointer-flow closure);
- [M+0x8C] subsystem = terminalne leaf-gettery O (D04) — args handlerów umierają tam bez dispatchy;
- registry route (singleton [0x6C62F4]): niesie 1 message id, nie 6 args; slot-1 dispatch tylko; nośnik 0x19A slots 6/7/9 = czytelnicy M-cell (byte-proven NIE callerzy fabryki).
Residual countermodel (C12): registry-consumer dispatch (slot-0 na M+0x08, 6 pushy), jmp [reg] (5435), call/jmp [reg+8] (824), receiver poza oknami, sekcje poza section1. **Brak zmierzonego dostarczyciela a1..a6; source UNKNOWN (scoped).**

## 4. Sink-side (gdzie a1..a6 lądują — potwierdzone)

E+0x40 (I), byte E+0x44, E+0x54 (flags), vec3 [this+4]/[this+0x10]/[this+0x28] w transform-node (obie vtable), dirty [E+0xDC]; first-translation 0x46F0A0 dostaje scale·f[E+4..E+0xC] (scale=[0x65B648]) — towart 46F0A0 kopiuje 3 dwordy, mnożenie w callerze (R4-A04 upheld). Brak etykiet osi/ramy (KONTRAZ): float-looking wartości NIE są world-coordinates bez consumera/ramy.

## 5. Podsumowanie statusów

| Wartość | Źródło zmierdzone | Status |
|---|---|---|
| entity-id, K selektor, klucz wizualny | komunikat (51C930/51C880 family) | CONFIRMED_FOR_MEASURED_SCOPE |
| string typu-7 / ':' wariant | komunikat (msg_arg1) | CONFIRMED_FOR_MEASURED_SCOPE |
| nazwa/context wrappera 498B80 | komunikat (msg_arg0-deref, msg_arg2) | CONFIRMED_FOR_MEASURED_SCOPE |
| lazy-create K | LITERAL 0 | CONFIRMED_FOR_MEASURED_SCOPE |
| I | a1 (store 0x555191) — upstream = a1 | CONFIRMED_FOR_MEASURED_SCOPE (downstream) |
| nazwy VFS ('.nif' itd.) | config-literals 0x45E4F0 | CONFIRMED_FOR_MEASURED_SCOPE |
| stringi czytelników M-cell | literały 0x6B93xx + własne args | CONFIRMED_FOR_MEASURED_SCOPE |
| **a1..a6 upstream** | **brak zmierzonego dostarczyciela** | **UNRESOLVED (SCOPED_NEGATIVE + BARRIER)** |
