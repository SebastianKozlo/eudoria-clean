# B2 — jeremv42/DaocNavMesh: nifs.csv + fixtures.csv → world matrix → load NIF

- Repo: https://github.com/jeremv42/DaocNavMesh (cloned read-only 2026-09-13; ONLY code reading, never executed)
- Commit SHA (master HEAD at clone): **206c3287770eb55ad56d3477a052375c49393281**
- Language: C++20 + glm; license BSD-3-Clause; repo created 2024-04-21 (per GitHub API), last push 2025-08-04.

## nifs.csv (ID→filename) + fixtures.csv parsing — VERBATIM CODE

File: `src/daoc/world/Zone.cpp`

```cpp
85:  auto nifs_csv = parse_csv(*find_file(game.fs, "nifs.csv"));
86:  for (int i = 2; i < nifs_csv.size(); ++i)
87:      nifs[std::stoi(nifs_csv[i][0])] = nifs_csv[i][2];   // nif ID -> filename
88:  auto fixtures_csv = parse_csv(*find_file(game.fs, "fixtures.csv"));
89:  for (int i = 2; i < fixtures_csv.size(); ++i)
90:  {
91:      auto const &row = fixtures_csv[i];
94:      glm::vec3 translation(std::stof(row[3]), std::stof(row[4]), std::stof(row[5]));  // XYZ
95:      if (row[11] == "1")
96:          translation.z = this->get_ground_height(translation);                       // on-ground flag
97:      float scale = std::stof(row[7]);                                                // scale
98:      if (std::fabs(scale) > 0.00001f)
99:          scale = scale / 100;
102:     auto rotation = glm::rotate(glm::mat4(1), std::stof(row[6]) / 180.f * std::numbers::pi_v<float>, glm::vec3(0, 0, 1));  // angle
103:     if (row.size() > 16)
104:         rotation = glm::rotate(glm::mat4(1), std::stof(row[15]), glm::vec3(std::stof(row[16]), std::stof(row[17]), -std::stof(row[18])));  // axis-angle
106:     _add_fixture(
107:         Fixture{
108:             .zone = this,
109:             .id = std::stoi(row[0]),           // fixture ID
110:             .nif_id = std::stoi(row[1]),       // NIF ID
111:             .world = glm::mat4(1),
112:             .collide = row[8] != "0",          // collision flag
113:             .collide_radius = std::stoi(row[9]),
114:             .unique_id = std::stoi(row[14]),   // unique ID
115:         },
116:         translation, rotation, scale);
```

## WORLD MATRIX composition — VERBATIM CODE (Zone.cpp L122-128)

```cpp
122: void Zone::_add_fixture(Fixture &&fixture, glm::vec3 const &translation, glm::mat4 const &rotation, float scale)
123: {
124:     glm::mat4x4 world = glm::mat4x4(1);
125:     world = glm::translate(world, translation);
126:     world *= rotation;
127:     world = glm::scale(world, glm::vec3(scale, -scale, scale));
128:     fixture.world = world;
```

Per-fixture world matrix = T × R × S (glm column-vector convention: scale applied first to the vertex, then rotation, then translation). NOTE: **scale Y is NEGATED** (`glm::vec3(scale, -scale, scale)`) — a Y-flip.

## Zone offset application method — VERBATIM CODE (Zone.cpp L218-244, Zone::visit)

```cpp
220: auto world = glm::mat4(1);
221: world = glm::translate(world, glm::vec3(this->offset_x * 8192, this->offset_y * 8192, 0));
...
239: for (auto &fix : this->fixtures)
240: {
241:     auto meshes = fix.get_meshes(game);
242:     for (auto m : meshes)
243:         visitor(*m, world * fix.world);
```

**ORDER CORRECTION vs the audited claim**: the claim wrote "translation × rotation × scale × zone offset". The code composes per-fixture world = T×R×S (L124-127) and applies the zone offset SEPARATELY at traversal time as the OUTERMOST factor: final = T_zone × (T × R × S) (L221+L243). The zone offset is NOT a trailing factor after scale — as a trailing factor it would be scaled/rotated by R and S. The mechanism: zone offset added in world space by pre-multiplication.

## load NIF — VERBATIM CODE (Zone.cpp L197-215, Fixture::get_meshes)

```cpp
197: auto nif_stream = zone->find_nif(game.fs, nif_it->second);
204: auto nif = Niflib::ReadNifTree(*nif_stream);
206: if (Niflib::TryExtractMesh(nif, glm::mat4(1), m.vertices, m.indices))
```

## tree_clusters (parallel path) — `src/daoc/world/TreeCluster.cpp`

```cpp
11: auto file_csv = fs.open("zones/trees/tree_clusters.mpk/tree_clusters.csv");
...
21: auto key = row[0];       // cluster name
23: auto nif = row[1];       // tree NIF
24: for (auto i = 2; i < row.size(); i += 3)
28:     auto pos = glm::vec3(-std::stof(row[i + 0]), -std::stof(row[i + 1]), std::stof(row[i + 2]));  // local XYZ triplets
```

Cluster expansion into per-tree fixtures: Zone.cpp L137-162 (fixture ids `id*100000+i`, ground-snap Z).
