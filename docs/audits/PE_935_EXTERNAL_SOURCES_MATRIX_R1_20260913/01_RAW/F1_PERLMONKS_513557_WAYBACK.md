# F1 — PerlMonks node 513557 (2005-12-02): binary diffing of PE BNT files

- URL: https://www.perlmonks.org/?node_id=513557
- Live fetch 2026-09-13: blocked ("Client Challenge" JS bot protection)
- Recovered via Wayback Machine: https://web.archive.org/web/20170307104849/http://www.perlmonks.org/?node_id=513557
- Wayback capture date: **2017-03-07** (1 capture of this URL)
- Node: "File reading with sysseek and sysread", by **PhilHibbs** (Hermit), posted **Dec 02, 2005 at 10:59 UTC** (node id 513557, perlquestion)
- Replies by ysth (Canon) Dec 02, 2005 — answer: open the file for READ access ("+<"), not append (">>").

## VERBATIM QUOTES (from the 2017-03-07 Wayback capture)

> I am trying to open files, seek to particular offsets, and read the byte value at that offset. My input file is the output of a number of executions of the Windows command FC /B which does a binary comparison of two files. [...]

The example input (FC /B output) — VERBATIM:

```
Comparing files C:\PROGRAM FILES\PROJECT ENTROPIA\DATA\MODELS\Models.b
+nt and C:\DATA\MODELS\MODELS.BNT
05063755: 03 43
0875CF55: BF FF
09DC0155: 00 40
0B209955: 40 00
0DE8AD55: 0A 4A
0DF4ED55: 7F 3F
Comparing files C:\PROGRAM FILES\PROJECT ENTROPIA\DATA\TERRAIN\50.bnt
+and C:\DATA\TERRAIN\50.BNT
03040155: 15 55
Comparing files C:\PROGRAM FILES\PROJECT ENTROPIA\DATA\TEXTURES\Textur
+es.bnt and C:\DATA\TEXTURES\TEXTURES.BNT
088C1355: 4C 0C
10F45955: 40 00
1155A355: 1E 5E
181FDB55: A6 E6
```

## Claim check (F1)

- Existence + date 2005-12-02: **CONFIRMED** (post header: "on Dec 02, 2005 at 10:59 UTC"; Wayback capture preserves it).
- Operations on Models.bnt / 50.bnt / Textures.bnt with concrete offsets: **CONFIRMED** — the post processes `FC /B` binary-comparison output listing hex offsets and byte pairs for all three PE archives (e.g. Models.bnt @05063755, 0875CF55, 09DC0155, 0B209955, 0DE8AD55, 0DF4ED55; 50.bnt @03040155; Textures.bnt @088C1355, 10F45955, 1155A355, 181FDB55). The author seeks to the offset and reads the byte (sysseek/sysread).
- Practical binary RE without BNT semantics: **CONFIRMED** — the thread is a pure Perl file-I/O question (why sysread returns the initialized buffer; answer: file opened in append mode ">>" instead of "+<"). ZERO BNT format semantics are discussed. The author was byte-diffing ORIGINAL game files (C:\PROGRAM FILES\PROJECT ENTROPIA\...) against their own MODIFIED copies (C:\DATA\...) — i.e., practical binary modding of the same BNT corpus, 21 years ago.
- LIMITATION: proves practical binary work on the PE BNTs in 2005; does NOT evidence any BNT format understanding, and the comparison target was the author's own modified files (modding), not format documentation.
- Wayback caveat: single capture (2017-03-07); PerlMonks live page requires JS challenge from this environment.
