# D1, D2, D3 — Dawn of Light (DOLSharp) + WarEmu create-object packets

All repos cloned read-only 2026-09-13; ONLY code reading — never compiled, never executed.

## D1 — Dawn-of-Light/DOLSharp (DAoC server emulator)

- Repo: https://github.com/Dawn-of-Light/DOLSharp ("Dawn of Light (DOL) - Dark Age of Camelot (DAOC) Server Emulator", C#, GPL-2.0, 136 stars)
- Commit SHA (master HEAD at clone): **776619f88d2d5ce52f09ab956194fd519a41f985**

### NPC creation packet — VERBATIM CODE

File: `GameServer/packets/Server/PacketLib168.cs`, method `SendNPCCreate(GameNPC npc)` (L1038-1120), opcode `NPCCreate = 0xDA` (`IPacketLib.cs` L127):

```csharp
1058: pak.WriteShort((ushort) npc.ObjectID);
1059: pak.WriteShort((ushort) speed);
1060: pak.WriteShort(npc.Orientation.InHeading);   // Heading
1061: pak.WriteShort((ushort) npc.Position.Z);    // Z
1062: pak.WriteInt((uint) npc.Position.X);        // X
1063: pak.WriteInt((uint) npc.Position.Y);        // Y
1064: pak.WriteShort(speedZ);
1065: pak.WriteShort(npc.Model);                  // Model
1066: pak.WriteByte(npc.Size);
1067: pak.WriteByte(npc.GetDisplayLevel(...));
```

Claimed "Heading→Z→X→Y→Model" sequence: CONFIRMED (fields in exactly this order; a `speed` short precedes Heading and `speedZ` sits between Y and Model; then Size/Level/flags/name/guild).

### Which object classes are handled by create packets (D1 census)

`GameServer/packets/Server/IPacketLib.cs` create-family + implementations:
- `SendNPCCreate(GameNPC)` — opcode `NPCCreate = 0xDA` (L127) — NPCs/mobs.
- `SendObjectCreate(GameObject)` — opcode `ObjectCreate = 0xD9` (L126) — PacketLib168.cs L917-979: handles `GameStaticItem` (emblem), `GameKeepBanner`, `GameStaticItemTimed`, `WorldInventoryItem` (items on ground), `IDoor` (door payload appended), plus flags/realm/model/name. These are DYNAMIC/interactive objects, NOT static city geometry.
- `SendPlayerCreate(GamePlayer)` — opcode `PlayerCreate = 0xD4` (L123).
- `SendMovingObjectCreate(GameMovingObject)` — opcode `MovingObjectCreate = 0x12` (L43) (siege weapons).
- `SendHouse(House)` — opcode `HouseCreate = 0xD1` (L120) — PacketLib168.cs L3693-3716: HouseNumber, Z, X, Y, Orientation, PorchRoofColor, emblem flags, Emblem, Model (byte), RoofMaterial, WallMaterial, DoorMaterial, TrussMaterial, PorchMaterial, WindowMaterial, name. This IS a network-placed building — but it is the PLAYER HOUSING system (dynamic purchasable houses in the housing region), NOT the authored static world.

**D1 RESOLUTION**: NPC create packet carries world transform + model ID runtime — CONFIRMED. Object classes: NPC, player, moving object, interactive GameObjects (static items/inventory items/doors/banners), player-housing houses. **Static city buildings are NOT in the server packet family** — in DAoC the static world is in the CLIENT's own zone data (the same nifs.csv/fixtures.csv corpus verified in group B).

## D2 — WarEmu/WarEmu (WAR emulator)

- Repo: https://github.com/WarEmu/WarEmu ("Warhammer Online Emulator 1.4.8", C#, 129 stars, default branch "update")
- Commit SHA (update HEAD at clone): **3e69ff657325e93cbe0a3955c56cdba6bdac5c5e** (branch tip; HEAD commit dated 2014-08-26)

### Opcodes — VERBATIM CODE

File: `WorldServer/NetWork/Opcodes.cs`
```csharp
88: F_CREATE_STATIC = 0x71,
89: F_CREATE_MONSTER = 0x72,
```

### F_CREATE_STATIC composition — VERBATIM CODE

File: `WorldServer/World/Objects/GameObject.cs`, method `SendMeTo(Player)` (L72-109):

```csharp
74:  PacketOut Out = new PacketOut((byte)Opcodes.F_CREATE_STATIC);
75:  Out.WriteUInt16(Oid);                       // OID
76:  Out.WriteUInt16(0);
78:  Out.WriteUInt16((UInt16)Spawn.WorldO);      // WorldO
79:  Out.WriteUInt16((UInt16)Spawn.WorldZ);       // WorldZ
80:  Out.WriteUInt32((UInt32)Spawn.WorldX);       // WorldX
81:  Out.WriteUInt32((UInt32)Spawn.WorldY);       // WorldY
82:  Out.WriteUInt16((ushort)Spawn.DisplayID);    // DisplayID
84-101: Unk shorts/bytes, loot flag (|4), Unk4
103: Out.WritePascalString(Name);
```

Claimed "OID, WorldO, WorldZ, WorldX, WorldY, DisplayID…": CONFIRMED (with a zero UInt16 between OID and WorldO, then unknown fields, flags, name).

### F_CREATE_MONSTER composition — VERBATIM CODE

File: `WorldServer/World/Objects/Creature.cs`, method `SendMeTo(Player)` (L142-204):

```csharp
146: PacketOut Out = new PacketOut((byte)Opcodes.F_CREATE_MONSTER);
147: Out.WriteUInt16(Oid);                        // OID
148: Out.WriteUInt16(0);
150: Out.WriteUInt16((UInt16)Heading);            // Heading
151: Out.WriteUInt16((UInt16)WorldPosition.Z);    // WorldPosition.Z
152: Out.WriteUInt32((UInt32)WorldPosition.X);    // WorldPosition.X
153: Out.WriteUInt32((UInt32)WorldPosition.Y);    // WorldPosition.Y
154: Out.WriteUInt16(0); // Speed Z
156: Out.WriteUInt16(Spawn.Proto.Model1);         // Model1
157: Out.WriteByte((byte)Spawn.Proto.MinScale);   // MinScale
158: Out.WriteByte(Level);                        // Level
159: Out.WriteByte(Faction);                     // Faction
161-171: Emote, Unks, Title, quest-state bytes
201: Out.WriteStringBytes(Name);
```

Claimed "OID, Heading, WorldPosition.Z/X/Y, SpeedZ, Model1, MinScale, Level, Faction": CONFIRMED exactly.

### Return of Reckoning post quotability (D2, part 2) — UNVERIFIED, documented attempts

Claimed URL: https://www.returnofreckoning.com/forum/viewtopic.php?p=15035
Attempts (2026-09-13):
1. Live fetch → HTTP 403 (forum bot protection)
2. Wayback `web/2024/` → 404
3. Wayback `web/2/` (nearest capture) → 404
4. Wayback availability API → HTTP 429 (rate limit)
5. Wayback CDX API (`cdx/search/cdx?url=...viewtopic.php?p=15035`) → EMPTY result (zero captures of this URL)
6. Playwright real-browser fetch → ECONNREFUSED (no browser endpoint available)
7. Bing web search for the thread title → no RoR results returned

=> The RoR post itself is NOT quotable from this environment; any claim about its content (packet logs from live servers, structures RE'd without original server code) remains UNVERIFIED.

## D3 (CRITICAL) — What F_CREATE_STATIC actually creates, from the code

**What the code SHOWS:**
- `GameObject : Unit` (`GameObject.cs` L12) is the ONLY sender of F_CREATE_STATIC in the repo (single grep hit).
- The class carries: loot generation (`LootsMgr.GenerateLoot`, `Looted`, `RELOOTABLE_TIME`, loot flag bit 4 in the packet), quest interaction (`QUEST_USE_GO`), Tok unlocks, Faction/Rank/Level from `Spawn.Proto` (L33-43), script attachment (`ScrInterface.AddScript(Spawn.Proto.ScriptName)`).
- The embedded real-packet hex comment (L57-70) decodes the name to **"Empire Bar Door"** — a DOOR object.
- Spawn data source: `GameObject_spawn : DataObject` with `[DataTable(TableName = "gameobject_spawns", DatabaseName = "World")]` (`Common/Database/World/GameObjects/GameObject_spawn.cs` L28-30) — spawns come from the EMULATOR'S OWN WORLD DATABASE, not from client files and not authored at runtime by the packet.
- Object-class census in `WorldServer/World/Objects/`: Object : Point3D → Unit : Object → Creature/Player; Object → GameObject / Door (empty stub) / ChapterObject / PQuestObject / Item. None of these is a city-building placer.

**What the code does NOT show:**
- No code path composes or transmits static city/building geometry. The packet name "F_CREATE_STATIC" means "static (non-moving, non-monster) interactive object" — the name does NOT prove the packet places whole cities.
- No evidence that WAR's authored static world comes from the server: the client renders static geometry itself; the emulator spawns interactive/dynamic entities from its DB.
- NPC/monster creation via F_CREATE_MONSTER proves nothing about a parallel path for buildings.

**D3 RESOLUTION**: F_CREATE_STATIC creates DB-driven interactive world objects (doors, lootable props, quest objects — per class logic and the embedded door example). It does NOT demonstrate network placement of static city geometry. The network-create precedent applies to DYNAMIC entities (and, in DAoC, player housing); it does NOT support network-first for authored static buildings — consistent with the DAoC client-side fixtures.csv finding (group B).
