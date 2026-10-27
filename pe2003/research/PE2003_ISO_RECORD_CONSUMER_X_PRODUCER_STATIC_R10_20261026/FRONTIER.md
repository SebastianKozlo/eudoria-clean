# FRONTIER (LIVE_FRONTIER_QUEUE) - R10 checkpoint
Ready significant edges (priority order; all STATIC_ONLY-legal):
1. DECODE 0x447B20 (M reader, [0x65BCE4+0x10]): closes the C-route mechanism record->M->reader->collection. Cost ~48 rows. Highest information gain.
2. DECODE wrapper tail 0x402421..0x4024C0 + qualify the full setter run (451700..451990 receivers/args) - finishes the E-builder map; X origin [S+0x68] already pinned.
3. DECODE 0x4019EB context (single caller of the wrapper) - S provenance (what S is; whether the 564890-flow E can be a product of this lineage).
4. Qualify 0x447C90 (shared query helper; appears in vtables 0x65E5B4/0x65BDB4/0x65BCE4 at +0x08/+0x30 slots) - probable RTTI/type-query; would separate registration vs query interpretations of vt+0x30 at 0x564A44.
5. E(wrapper) -> E(564890) identity edge: requires an explicit callsite/dataflow path from the 0x4019EB lineage into the 564890 flow; absent today.
6. 451730 remaining 8 callsites (populations of [E+0x14] writes beyond the wrapper).
7. VFS era resolution for the 26 campaign VFS files (P1 open item; needs a new bounded assignment).
8. X.vt+8 (M producer for the X-side M) - blocked on X class/vptr (X origin [S+0x68] known for wrapper population only).
Resume instruction (R11): start from FRONTIER items 1 and 2 in one bounded wave; pinset unchanged; new AUDIT_OUTPUT_ROOT with new RUN_ID per contract.
