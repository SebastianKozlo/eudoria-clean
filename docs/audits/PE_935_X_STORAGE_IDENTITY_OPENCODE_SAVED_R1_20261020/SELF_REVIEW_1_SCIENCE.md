# SELF_REVIEW_1 - pointer flow / ABI / aliasing / countermodels

Findings and dispositions:
1. FOUND (P2 CORRECTNESS): CLAIMS v1 XSI-17 cited source row 1166141 (MOV [ESP+0x78],0x1) which is not part of the [ESP+0x7c/0x80/0x84] vector trio. FIXED as CLAIMS v2 with ERRATA; original bytes preserved in CLAIMS_v1.json.
2. CHECKED: ECX last-definition chain at 00858240 - direct row flow, no intervening EAX/ECX redefinition between 0085821e CALL result, 00858226 cache, 0085822a CMP and 0085823e MOV ECX,EAX. No alternative register source visible in admitted rows.
3. CHECKED: ESP offset algebra for the D410 arg and C3B0 args (reads at ESP-8 compensated by +0x8 in displacement): recomputed manually; consistent.
4. CHECKED: shifted-ESP writes to the frame cell (SUB ESP,8 windows): only [ESP+0x3c] writes could hit the cell; both such writes occur at base ESP before the first SUB ESP,8 (0085c691). No other aliasing window found.
5. CHECKED: countermodels - allocator aliasing (A==X value) retained UNKNOWN; [ESP+0x18] reload instead of EAX refuted by direct MOV ECX,EAX row; PUSH ECX at 0085824f carrying D410 result refuted (ECX caller-saved, no relation proven; result captured via EAX->ESI).
6. LIMITATION (accepted): DF=0 and absence of live aliasing are static assumptions; runtime confirmation excluded by contract (saved sources only). XSI-08/XSI-09 stay STRONGLY_SUPPORTED, not CONFIRMED.
7. LIMITATION (accepted): 0x80/0x68 are allocator REQUESTS; allocator semantics not opened. All wording uses request-size language; XSI-04 phrase size requests softened by A_TO_X countermodel note.
8. CHECKED: XSI-13 census wording limited to direct CALL sites in the pinned listing; indirect/jump-based entries not claimed.
