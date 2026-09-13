# F2, F4 — XeNTaX backup: xennex (2007 BNT2) + sinkillerj (2020 recreate-the-old-world)

- Source: **XeNTaX community backup** — https://github.com/XeNTaXBackup/XeNTaXBackup.github.io ("XeNTaX's Public Backup"; forum.xentax.com is dead since ~2018; this backup is the community scrape published Oct 2023)
- Backup repo commit SHA (main HEAD at clone, 2026-09-13): **2c6074a1bcb085e77f527fcf620620a4ee1e76da**
- Retrieval: git clone (read-only; --filter=blob:none sparse), files read from the working tree; thread files under `markdown/`
- Read date: 2026-09-13
- Provenance caveat: the original xentax.com URLs are dead; these are scrape-preserved posts with metadata (username, join date, post datetime). The original forum thread IDs: 2446 and 21558.

## F2 — xennex: "Problem mit Entropia Universe Archive" (thread 2446)

File: `markdown/Problem mit Entropia Universe Archive_2446.md`

Post #1 — Username: **xennex** (rank: beginner; joined 2006-10-06; 27 posts) — **Post datetime: 2007-01-24T16:14:54+00:00** — VERBATIM (German):

> Ich habe ein Problem mit dem Archiv mit Entropia Universe. Teilweise kann iich das Archiv schon lesen.
>
> ```
> Int32 (4) Startoffset
> Char  (4) Header (BNT2)
> //Gehe zu Startoffset
>   Int32 (4) anzahl der Dateien
> // Wiederholung anzahl der dateien
>   Char  (x) Dateiname (Solange wiederholen bis chr=10)
>   int32 (4) Dateigröße
>   int32 (4) Dateioffset
>   int64 (8) Unbekannt
> // Ende Wiederholung anzahl der dateien
> Byte  (x) Datei
> ```
>
> Das Problem besteht darin das ich nicht weiß wofür der Int64 wert steht, dachte erste das es eine Datei ID stimmt aber nicht, weill ich schon versucht habe eine andere datei zu ersetzen und mit dieser ID zu schreiben und das Spiel stürz[t] ab kann mir da einer helfen?

Post #2 — xennex — **Post datetime: 2007-01-25T08:46:55+00:00** — VERBATIM (English):

> ok, i try in english.
> i have a proplem with the game archive Entropia Universe, can extract but not replace(the game crash).
> here is the gamearchive description
>
> ```
> int32 (4) Start offset
> char  (4) Header (BNT2)
> //go to startoffset
>   int32 (4) number of files
> // for each file
>   char  (x) filename (do while not char=10)
>   int32 (4) file size
>   int32 (4) file offset
>   int64 (8) unknown
> // End loop
> byte  (x) File data
> ```
>
> the problem is that i don't known what the int64 value is(Not file ID).
> can anyone help me?

### F2 claim check
- Structure [int32 StartOffset]["BNT2"][int32 numberOfFiles][name until chr=10 (0x0A)][int32 size][int32 offset][int64 UNKNOWN]: **CONFIRMED VERBATIM** (both posts).
- "author experimented with int64 as ID, client crashed after swap": **CONFIRMED** — post #1: tried the int64 as file ID, replaced a file and wrote with that ID → the game crashed ("das Spiel stürzt ab"); post #2: "can extract but not replace(the game crash)", "i don't known what the int64 value is(Not file ID)".
- Dates 2007-01-24/25: **CONFIRMED** (post metadata in the backup).
- The preserved thread shows NO ANSWER (only xennex's two posts in the backup file).
- LIMITATION: XeNTaX is dead; this is a community-scrape copy (post metadata embedded), not the live forum; the scrape preserves the posts verbatim as of the 2023 backup snapshot.

## F4 — sinkillerj: "Classic Entropia Universe Models (Gamebryo NIF)" (thread 21558)

File: `markdown/Classic Entropia Universe Models (Gamebryo NIF)_21558.md`

Post #1 — Username: **sinkillerj** (rank: ultra-n00b; joined 2008-08-17; 7 posts) — **Post datetime: 2020-01-03T04:06:44+00:00** — VERBATIM:

> I've been exploring the files of the old Entropia Universe (Before the drastic redesign and switch to CryEngine) after finding the archive here: https://archive.org/details/EntropiaUniverse180208
>
> Ultimately my goal is to **decode the game enough to recreate the old world**. Dragon Unpacker has no problem with the BNT archives, and the textures are easy as they are simply a mix of TGA and DDS disguised as DAT, but the model and terrain formats have been giving me some trouble and thus i come to the experts here.
>
> These are in NIF format which is a pretty widely used Gamebryo format, but NifSkope refuses to open them due to the unknown block type **NiArkAnimationExtraData**.
>
> As for the terrain I've no idea where to begin, it appears to be in chunks of **TDF** files, but this may be proprietary as i can find no info online.

Post #3 — shakotay2 (MEGAVETERAN) — 2020-01-03T08:35:14 — VERBATIM (relevant part):

> There's a handful of NifSkope versions. This one is from 2010 iirc: [screenshot CEU-nif.png — a CEU NIF loaded in old NifSkope]
> (There's unknown ints in the NiArkAnimationExtraData node, yes.)

Post #4 — sinkillerj — **Post datetime: 2020-01-04T01:29:26+00:00** — VERBATIM:

> I tried the version of NifSkope from your screenshot and sure enough it can handle the files fine, who woulda thought that ancient versions would be the solution...
>
> Edit: For those jumping down this rabbit hole **any version of NifSkope 1 appears to work, including the seemingly latest 1.2.0 Alpha 2**, some files stil have issues that will need to be resolved but for the most part it works quite well: [link to niftools/nifskope v1.2.0-alpha.2 nightly]
>
> Now I just need to look more into how the terrain works. If anyone wants to take a stab at it here is one of the **TDF** files: [drive.google.com link]
>
> As well as one of the **TEZ** files from **TerrainEditZones**, though this seams minor as there are not many of them compared to the terrain chunks, and **I'm not quite sure how they correlate yet**: [drive.google.com link]

### F4 claim check
- "decode the game enough to recreate the old world" quote: **CONFIRMED VERBATIM** (post #1).
- Had BNT/textures/NIF/terrain: **CONFIRMED** — Dragon Unpacker opened BNT; textures = TGA/DDS "disguised as DAT"; models = NIF; terrain = TDF chunks.
- Stuck on NiArkAnimationExtraData: **CONFIRMED** — modern NifSkope refused due to the unknown block; old NifSkope 1.x (2010-era, incl. 1.2.0a2) "can handle the files", "some files still have issues".
- Stuck on TDF/TEZ: **CONFIRMED** — "I've no idea where to begin" (terrain), thread ends with "I'm not quite sure how they correlate yet" (TEZ vs terrain chunks).
- Date January 2020: **CONFIRMED** (2020-01-03/04).
- Thread content in the backup: 4 posts (sinkillerj #1, Bigchillghost #2 [image only], shakotay2 #3, sinkillerj #4).
- LIMITATION: same backup-provenance caveat as F2; the 4 posts are what the scrape preserved; the original thread may have had more posts not captured. No placement/protocol/runtime RE is present in the preserved posts (consistent with the audited claim that this predecessor ended at asset extraction/viewing).
