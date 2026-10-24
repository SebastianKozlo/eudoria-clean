# Reconstruction roadmap — PE 2003 frontier

RUN_ID: PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3_20261024.
Sanitized public projection of FRONTIER.json / FIRST_MISSING_EDGE.json.
Ordered by priority; item (a) is the FIRST_MISSING_EDGE.

## (a) Dynamic capture of a real model open — FIRST MISSING EDGE

Definition → open for a live instance. The static surface is exhausted
(0 direct callers verified 3×; 0 qualified virtual dispatch sites among
5776 indirect CALL sites / 576 444 instructions). Next method: runtime
instrumentation of the open slots (facade vtable 0x5E796C slots +8..+0x14
and/or open_nif 0x520EE0 / open_bvi 0x520D80) with the client running against
any reachable session, logging the id of every open call. Expected value:
closes the E20 edge for BOTH target models (they share it), potentially
catching live opens of 296445.nif / 218757.nif and the instance ids that
request them.

## (b) Live orientation source

Who supplies the real 9 floats to FUN_005030c0 param_5 (all static callsites
pass 0/unresolved)? Decompile/trace the supplier, or watch scene node
+0x2C..+0x4C writes at runtime. Closes the last UNVERIFIED transform edge
(W3-11). Co-dependent with (a) on a running session.

## (c) Server-side instance data model

The client parses+links the .obj bytecode but has no 0x7700xxxx interpreter
(E19); the attach-resource macro is byte-verified in both definitions.
Confirming the server-side execution model would complete the
definition→open edge from the other side. Server binary / session capture
analysis.

## (d) PCG demo NSIS payload recovery

PE_PCG.exe (157 629 853 B, SHA256 F74BE3AC…) extraction is BLOCKED at NSIS
data block #40 (0x1D7A238) with 40/40 clean parsed blocks. Recovery or an
alternative extraction path would verify/falsify that the PCG demo carries
the same ARK corpus as the PE42 install (its outer ZIP member already tests
PASS).

## (e) Terrain 50.bnt era split decode

TWO versions exist (PE42 8E43CD14… / 116 528 920 B vs other copy
A6E59EE0… / 118 016 977 B). Decode BOTH with the BNT/BUNT/TDF pipeline and
diff, to determine which terrain corpus belongs to the Jan-2003 COT client
era. Prerequisite for ANY future world-position calibration (anchor problem,
see world-data-and-placement.md). Requires explicit authorization under the
corpus extraction rules.

## Standing

- Status of the published campaign: ADVISORY_PENDING_EXTERNAL_POSTAUDIT;
  CANONICAL_GATE_EFFECT=NONE.
- The dynamic items (a)-(c) require an authorized runtime campaign; (d)/(e)
  are corpus work independent of a live session.
