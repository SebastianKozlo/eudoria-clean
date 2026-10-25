# TRANSFORM_SOURCE_MAP (5.1.0.0)
Sinki: 0x46F0A0 translate (receiver+0x2c/30/34 kazdy x100; const 0x65B648=0x42C80000), 0x46F0C0 Euler->matrix (receiver+0x38), 0x46F160 scale (receiver+0x6c). Renderer-side: 0x4DD421 (receiver [renderer+0x28]).

Kanaly wartości i ich statusy:
1. Argumenty fabryki 0x4578E0 (6: x,y,z,rx,ry,rz) — wejście CONFIRMED, POCHODZENIE UNVERIFIED (0 bezpośrednich xrefów; jedyna vtable 0x65BE9C slot+0; indirect dispatch).
2. Base-setter layer 0x51D730->0x5531F0->0x555170->0x555270 — wejście CONFIRMED, pochodzenie UNVERIFIED.
3. Entry record [entry+0x34] -> vcall+0x11C (pola +0x14/+0x2c/+0x30) — sink CONFIRMED, producent entry-set UNVERIFIED (file vs network vs VM statycznie nierozstrzygalne; kontrmodel plikowy sprawdzony przez QC2 i odrzucony atrybucyjnie).
4. Template records 0x5C init-set — CONFIRMED LOCAL CODE (scope: init-set).
5. Default/reset — tylko ctor-reset, NIE transform.
6. NIF model-local — REJECTED jako źródło placementu (82 bloki, skale 1.0, późne XYZ zero).
Kontrmodele odrzucone bajtowo: bbox, debug, physics, camera.
Units: mechanizm x100 CONFIRMED; semantyka jednostek (metry?) PLAUSIBLE era-labelled.
Frame/axis: nieustalona (wymaga wartości + ramy — poza zasięgiem statyki bez entry-set producenta).
