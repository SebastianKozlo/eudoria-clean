# C3 — openmw-trav docs: Overview of Lua scripting (mwdialogue-bindings branch)

- URL: https://openmw-trav.readthedocs.io/en/mwdialogue-bindings/reference/lua-scripting/overview.html
- Read date: 2026-09-13 (live fetch, HTTP 200)
- Document: "Overview of Lua scripting", OpenMW version 0.49.0, core.API_REVISION: 62
- Provenance note: openmw-trav.readthedocs.io hosts the "mwdialogue-bindings" branch docs of the GitLab project trav55/openmw (an OpenMW fork/branch doc set), per the page's "Edit on GitLab" link: https://gitlab.com/trav55/openmw/blob/mwdialogue-bindings/docs/source/reference/lua-scripting/overview.rst — NOT the primary openmw.readthedocs.io domain.

## VERBATIM QUOTES (section "Basic concepts")

> **Game object**
> Any object that exists in the game world and has a specific location. Player, actors, items, and statics are game objects.
>
> **Record**
> Persistent information about an object. Includes starting stats and **links to assets, but doesn't have a location**. Game objects are **instances of records**. Some records (e.g. a unique NPC) have a single instance, some (e.g. a specific potion) may correspond to multiple objects.

> Note
> Don't be confused with MWSE terminology. In MWSE game objects are "references" and records are "objects".

## Claim verification notes

- Base record contains asset links without location: CONFIRMED verbatim ("Includes starting stats and links to assets, but doesn't have a location").
- Instance has location: CONFIRMED verbatim ("Any object that exists in the game world and has a specific location").
- Additional verified detail: the page explicitly notes the MWSE/OpenMW terminology inversion (OpenMW "game object" == MWSE "reference"; OpenMW "record" == MWSE "object") — a caution for cross-referencing C2 and this row.
- Limitation: docs of one engine's scripting model (OpenMW 0.49 Lua); a RESEARCH PATTERN for definition/instance separation, NOT a mandatory architecture of all Gamebryo games, NOT evidence for Entropia.
