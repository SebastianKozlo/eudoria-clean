# ABI_FIELD_MAP — PE2003_ISO_MODEL_BINDING_VALUE_ORIGIN_STATIC_R5_20261025

RUN_ID: PE2003_ISO_MODEL_BINDING_VALUE_ORIGIN_STATIC_R5_20261025 | BUILD: ISO2003NOV_PE_5_1_0_0 | DATE: 2026-10-25
PROVENANCE: jobs/A01/RESULT.md (attempt 2, R5-A01-002) + jobs/A01/data/ABI_FIELD_MAP_R5_A01.json + jobs/A01/data/SCRATCH_SLOT_TRACE.md; niezależnie re-derywowane przez QC1 (probe_log.txt). Companion strict: ABI_FIELD_MAP_R5_A01.json (frozen job artifact).

## 1. Łańcuch i ABI (wszystkie krawędzie zmierzone w A01, byte-proven)

```
0x4578E0 factory (thiscall: ecx=this, 6 stack args a1..a6, ret 0x18)   [frame E0]
  ├─ 0x4ADE7C operator new(0x100)  [cdecl; add esp,4 @0x457903 (83 c4 04) — przywraca frame do E0-0x14]
  ├─ 0x46E870 entity ctor (ecx=alloc; stack arg = this−8 = M) → [E]=0x65C060, [E+0x48]=0x65C05C, [E+0xF8]=0, [E+0xFC]=M
  └─ call [vt+0x1c] @0x457951 (ff 50 1c) → 0x65C07C = 0x46E990 WRITER (this=E; a1..a6 1:1)
       ├─ 0x51D730 (forwarduje a1..a6; byte[E+0xDC]=1 dirty)
       │    └─ 0x5531F0 (forwarduje a1,a2,a4,a5,a6 — 5 args, ret 0x14)
       │         ├─ store a3 → [E+0x54] @0x553217 (89 56 54)  PO inner call (edx=[esp+0x10]=a3)
       │         └─ 0x555170 (stores a1,a2; forwarduje a4,a5,a6)
       │              ├─ store a1 → [E+0x40] @0x555191 (89 46 40)
       │              ├─ store byte(a2) → [E+0x44] @0x555194 (88 4e 44; cl @0x55518D — LOW BYTE ONLY)
       │              └─ 0x555270 dispatcher:
       │                   ├─ [vt+4]   @0x55527C (ff 50 04) ← a4 → 0x5552C0
       │                   ├─ [vt+8]   @0x555288 (ff 52 08) ← a5 → 0x5552E0
       │                   ├─ [vt+0xc] @0x555294        ← const 0x6C6664 → 0x555300
       │                   ├─ [vt+0x10]@0x5552A0 (ff 50 10)← a6 → 0x555320
       │                   └─ [vt+0x14]@0x5552AC        ← const 0x6C6664 → 0x555350
       ├─ lazy-create 0x46E9C4..0x46E9D2: I=[E+0x40] (0x553220), push I, push 0 → 0x457980 → 0x473E90 → [E+0xF8]
       └─ first-translation 0x46F0A0 @0x46EA62: args = (scale·f[E+4], scale·f[E+8], scale·f[E+0xC]), scale=[0x65B648]
```

E = writer entry this; vt = 0x65C060. NOTE: PA shorthand "factory→51D730" pomija jeden hop — [vt+0x1c] target = WRITER 0x46E990 (byte-verified), który woła 51D730; mapa argumentów nietknięta.

## 2. Cele virtual setterów (z bajtów obrazu, oba vtable identyczne)

| Slot | Target | ABI | Zachowanie ciała |
|---|---|---|---|
| vt+0x04 | 0x5552C0 | thiscall, 1 stack arg = ptr do vec3, ret 4 | kopiuje 12B z *arg do [this+4] |
| vt+0x08 | 0x5552E0 | j.w. | kopiuje 12B do [this+0x10] |
| vt+0x10 | 0x555320 | j.w. | kopiuje 12B do [this+0x28], potem call 0x524370 |
| vt+0x0c | 0x555300 | j.w. (arg = const 0x6C6664) | kopiuje 12B do [this+0x1c] |
| vt+0x14 | 0x555350 | j.w. | kopiuje 12B do [this+0x34] + call 0x524370 |

Vtable: 0x65C060 (entity, ctor 0x46E870) i 0x65EC90 (transform-node, ctor 0x5551A0) — te SAME cele setterów na +4/+8/+0xc/+0x10/+0x14. Blob offsets: 0x25B064/0x25DC94 (+4) itd.

## 3. Layout obiektu (strukturalny, BEZ etykiet semantycznych per KONTRAZ)

+0 vt; +4, +0x10, +0x1c, +0x28, +0x34 — pięć grup vec3 (ctor 0x5551A0 inicjuje z globali 0x6C6664/0x6C6668/0x6C666C); +0x40 dword (a1=I); +0x44 byte (a2); +0x54 dword flags (a3); +0xDC dirty byte (51D730); +0xF8 cached product (writer).

## 4. Scratch-slot [E+0x18] — pełna chronologia ESP

E = entry ESP writera 0x46E990 (wartości bezwzględne zależne od caller-a; wszystkie różnice względne do E):

- WRITE 0x46EA02 `89 44 24 1c` (ESP=E−0x04: pojedynczy prolog `push esi` @0x46E998=56; call 51D730 czyści własne kopie ret 0x18): store do [ESP+0x1c]=[E+0x18] = wejściowy slot home a6. Wartość = dword [esi+4] ([E+4] — pierwsza składowa vec3 zapisanego chwilę wcześniej przez 0x5552C0 z *a4).
- Interwenty 0x46EA06..0x46EA54: zapisy TYLKO do [esi+0xF8], [E−0x08], [E−0x0c], [E−0x04]; callees dostają ESP ≤ E−0x08. NIC nie pisze [E+0x18].
- READ 0x46EA55 `d9 44 24 28` (ESP=E−0x10 po `sub esp,0xc` @0x46EA3B=83 ec 0c): [ESP+0x28]=[E−0x10+0x28]=[E+0x18] — TEN SAM absolutny slot.
- **DOMINUJĄCA DEFINICJA @0x46EA55 = store 0x46EA02 ([E+4], reinterp. jako float, skalowane). "Stale A6" REJECTED (measured scope: każda ścieżka przechodzi przez 0x46EA02 przed 0x46EA55).**
- Corroboracja: wariant writera 0x46EB20 (ret 8) powtarza idiom na home slocie arg2 (write 0x46EB3D → [E'+0x08]; read 0x46EB8A `fld [esp+0x18]` @ESP=E'−0x10 → [E'+0x08]).

## 5. Statusy per argument (CONFIRMED_FOR_MEASURED_SCOPE)

a1→[E+0x40]; a2→byte[E+0x44] (low byte only — precyzja względem PA); a3→flags [E+0x54] (dead-arg dla 0x555170; zapisuje sam 0x5531F0; bit0 konsumowany @0x46E9E4→[product+0x20]); a4→[vt+4]; a5→[vt+8]; a6→[vt+0x10]. A4_UNUSED REJECTED (upheld). Negative control fabryki: wszystkie 6 argów czytane i pushowane (a6 @0x457927 pierwszy, a1 @0x457946 ostatni); własne odczyty [esp+0x2c]/[esp+0x28] rozstrzygają się na a6/a5 TYLKO przez `add esp,4` @0x457903 (kontrmodel frame-mis-read obalony bajtami).

## 6. Granice

(i) standardowa dyscyplina stosu x86 (callees nie piszą powyżej entry ESP) — założenie potrzebne i wystarczające dla dominacji scratch-slotu; (ii) VA=0x401000+blob_offset (provenance R3, SHA MATCH attempt 1); (iii) odczyty vtable w granicach pliku (0x25B060/0x25DC90 < 0x2CD5A1); (iv) zmierzony JEDEN target dispatch vt+0x1c (vtable 0x65C060) — inne podklasy ⇒ statusy scoped, nie globalne; (v) brak etykiet osi/semantyki a1..a6 (KONTRAZ upheld).
