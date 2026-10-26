# R6 External Postaudit Notice — R1 (issued by R7)

RUN_ID: PE2003_ISO_MODEL_ROOT_VALUE_SOURCE_STATIC_R7_20261025
This is an ADDITIVE notice placed next to the historical R6 report
(PE2003_ISO_LOADER_VTABLE_INSTANCE_JOIN_STATIC_R6_20261025). The R6 files
are byte-untouched; nothing in the R6 package is edited or retracted
silently.

The R7 static wave confirmed, corrected and maintained the following R6
statements (evidence class in brackets):

1. **E / R owner identity — CORRECTED.** The R6-era merged reading is not
   maintainable: E (return value of the entity lookup), R (return value of
   the record-template lookup, stored at [SFO+0x78]) and P (the SFO
   instance, cached E+0xF8) are SEPARATE symbols. Bit-level equality of E
   and R was never proven and is neither assumed nor denied. R is a
   per-TYPE record template chosen by a pure array index; the per-INSTANCE
   side is SFO. [CONFIRMED from bytes]
2. **W / D override — CORRECTED.** The typed NiPixelData ancestral-walk
   semantics of the W wrapper table do NOT transfer to the D singleton
   table. The R7 decode shows D slot +8 is a list walker that returns an
   INTERNED DESCRIPTOR (get-or-create intern pattern, integer-only
   identity record), not NiPixelData. The D-side constant 2800 is the
   I/O buffer size of a buffered binary file stream; pixel content
   UNKNOWN. [CONFIRMED from bytes]
3. **Ancestry-vs-graph — MAINTAINED (untouched).** The distinction that the
   pixel-path selection walks the class ancestry of one selected object,
   not the entire object graph, is upheld. [maintained]
4. **P / base vtable — MAINTAINED + new observation.** 0x65C0DC remains the
   qualified P ctor table (4 entries) and 0x65C0EC a separate base-dtor
   table; no splicing into P slots. New R7 observation: the destructor of
   the F-caller receiver installs vptr 0x65C0EC and releases the lazy
   slot, supporting S==P==SFO — held at PLAUSIBLE; the 0x65C0EC to
   0x65C0DC binding is NOT byte-proven. [maintained + PLAUSIBLE]
5. **Mutable global — MAINTAINED (untouched).** Runtime-initialized globals
   are zero in the static image; roles are resolved via registration
   evidence, not absence. [maintained]
6. **Premature R6 stop — CORRECTED.** The R6 stop is classified
   NONCOMPLIANT_PREMATURE_STOP: the then-backlog was attainable, in-scope
   and budget-feasible with no blocker. R7 executed those edges (D
   override, H initializer chain, R source, NAME producer) to their
   honest budget boundary. [process correction]

**Confirmed in R7 (from bytes):** E/R/P separation; D slot +8 interned
descriptor; the H origin chain link-by-link (holder ctor, unique caller,
wrapper ctor with AddRef on the acquired object M); R per-TYPE template
identity with the map correction that the E+0x40 field is an ID (not a
template index); NAME = [A+4] as a pointer to a large object consumed by a
direct call (not the earlier-assumed vtable slot).

**Plausible (not promoted):** S==P==SFO; the semantics of the acquired
object M (manager/registry/root reading; the virtual acquisition target
was not opened).

**Unknown:** filename-vs-ID for NAME; per-model binding for 296445/218757;
the runtime content of the interned descriptors.

**Still open after R7:** the NAME consumer (filename-vs-ID, model
binding), transform writers, the promotion of S==P, per-model values and
frames. All five remaining ready edges are documented and
candidate-budget-exhausted (INC-001).

Full R7 report:
`pe2003/research/PE2003_ISO_MODEL_ROOT_VALUE_SOURCE_STATIC_R7_20261025/PUBLIC_REPORT_R7.md`

Status carried: PE2003_WORLD_XYZ_RECOVERED=NO;
PE2003_HISTORICAL_PLACEMENT=NOT_ESTABLISHED;
SOURCE_SPECIFIC_ISO_MODELS=UNKNOWN; PE2003_LOCAL_SOURCE_EXHAUSTED=NO;
CANONICAL_GATE_EFFECT=NONE; EXTERNAL_POSTAUDIT=PENDING.
