# C1 — OpenMW documentation: World Tables (tables-world)

- URL: https://openmw.readthedocs.io/en/stable/manuals/openmw-cs/tables-world.html
- Read date: 2026-09-13 (live fetch, HTTP 200)
- Document: OpenMW stable manual, OpenMW-CS "World Tables"

## VERBATIM QUOTES

### Objects section

> This is a library of all the items, triggers, containers, NPCs, etc. in the game. There are several kinds of Record Types. [...] All Record Types contain at least a 3D model or else the player would not see them. Usually they also have a _Name_, which is what the players sees when they hover their crosshair over the object during the game.

### Instances section (THE CLAIMED TABLE)

> An instance is created every time an object is placed into a cell. While the object defines its own fundamental properties, an instance defines how and where this object appears in the world. When the object is modified, all of its instances will be modified as well.
>
> Cell — Which cell contains this instance. [...]
>
> **Object ID** — ID of the object from which this instance is created.
>
> **Pos X, Y, Z** — Position coordinates in 3D space relative to the parent cell.
>
> **Rot X, Y, Z** — Rotation in 3D space.
>
> **Scale** — Size factor applied to this instance. It scales the instance uniformly on all axes.
>
> Owner — NPC the instance belongs to. [...]
> (further fields: Soul, Faction, Faction Index, Charges, Enchantment, Coin Value, Teleport, Teleport Cell, Teleport Pos X/Y/Z, Teleport Rot X/Y/Z, Lock Level, Key, Trap, Owner Global)

## Claim verification notes

- Claimed fields present: Object ID, Pos X/Y/Z, Rot X/Y/Z, Scale — ALL CONFIRMED verbatim in the Instances table.
- Definition/instance separation explicitly stated: "While the object defines its own fundamental properties, an instance defines how and where this object appears in the world."
- Limitation: this is the OpenMW Construction Set data model for Morrowind-era content; it is documentation of ONE engine's world-editing schema, not a universal Gamebryo-era MMO standard.
