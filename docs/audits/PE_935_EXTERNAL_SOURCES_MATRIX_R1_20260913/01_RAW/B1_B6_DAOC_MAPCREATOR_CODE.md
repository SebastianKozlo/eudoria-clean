# B1, B6 — Merec/DAoC-MapCreator: nifs.csv + fixtures.csv + Treemap.csv + tree_clusters.csv

- Repo: https://github.com/Merec/DAoC-MapCreator (cloned read-only 2026-09-13; ONLY code reading, never executed)
- Commit SHA (master HEAD at clone): **073a5940128be0e3f3bb57df0468d946b560c7f1**
- Language: C# (.NET WinForms); author: Stefan Schäfer <merec@merec.org>, Copyright 2017, GPL-2 (file headers)
- README changelog 2017-10-01: "Replaced my Niflib.NET with https://github.com/dol-leodagan/niflib.net"

## B1: nifs.csv then fixtures.csv — VERBATIM CODE

File: `MapCreator/Classes/MapCreation/Fixtures/FixturesLoader.cs`

```csharp
75:  List<string> nifsCsvRows = DataWrapper.GetFileContent(zoneConf.CvsMpk, "nifs.csv");
76:  List<string> fixturesRows = DataWrapper.GetFileContent(zoneConf.CvsMpk, "fixtures.csv");
```

nifs.csv parsing (fields[0]=NifId, fields[1]=TextualName, fields[2]=Filename, fields[5]=Color), lines 84-96:
```csharp
91:  nifRow.NifId = Convert.ToInt32(fields[0]);
92:  nifRow.TextualName = fields[1];
93:  nifRow.Filename = fields[2];
```

fixtures.csv parsing — ALL CLAIMED FIELD INDICES VERBATIM (lines 99-125):
```csharp
105: fixtureRow.Id = Convert.ToInt32(fields[0]);          // [0] fixture ID
106: fixtureRow.NifId = Convert.ToInt32(fields[1]);       // [1] NIF ID
107: fixtureRow.TextualName = fields[2];                  // [2] textual name
108: fixtureRow.X = Convert.ToDouble(fields[3], provider); // [3] X
109: fixtureRow.Y = Convert.ToDouble(fields[4], provider); // [4] Y
110: fixtureRow.Z = Convert.ToDouble(fields[5], provider); // [5] Z
111: fixtureRow.A = Convert.ToInt32(fields[6]);           // [6] angle
112: fixtureRow.Scale = Convert.ToInt32(fields[7]);       // [7] scale
113: fixtureRow.OnGround = (Convert.ToInt32(fields[11]) == 1) ? true : false;  // [11] on-ground
114: fixtureRow.Flip = (Convert.ToInt32(fields[12]) == 1) ? true : false;      // [12] flip
116: if (fields.Length > 15)
117: {
118:   fixtureRow.Angle3D = Convert.ToDouble(fields[15], provider);  // [15] 3D angle
119:   fixtureRow.AxisX3D = Convert.ToDouble(fields[16], provider); // [16] axis X
120:   fixtureRow.AxisY3D = Convert.ToDouble(fields[17], provider); // [17] axis Y
121:   fixtureRow.AxisZ3D = Convert.ToDouble(fields[18], provider); // [18] axis Z
122: }
```

Transform application (2D map rendering): `MapCreator/Classes/MapCreation/Fixtures/DrawableFixture.cs`
- L163: `Scale = ((FixtureRow.Scale / 100f) * ZoneConf.LocScale);`
- L165: `double angle = 360d * FixtureRow.AxisZ3D - FixtureRow.A;`
- L172-176: rotation matrix (Z-axis only — this is a 2D map renderer, NOT a 3D world compositor)
- L87-91: OnGround → Z overwritten from heightmap; Z then used for draw order.

## B6: Treemap.csv + tree_clusters.csv — VERBATIM CODE (same file, lines 127-174)

```csharp
130: string treeMpk = string.Format("{0}\\zones\\trees\\treemap.mpk", ...);
131: string treeClusterMpk = string.Format("{0}\\zones\\trees\\tree_clusters.mpk", ...);
133: List<string> treesCsvRows = DataWrapper.GetFileContent(treeMpk, "Treemap.csv");
134: List<string> treeClusterCsvRows = DataWrapper.GetFileContent(treeClusterMpk, "tree_clusters.csv");
```

TreeClusterRow parsing — local XYZ triplets of tree instances inside the cluster (lines 151-174):
```csharp
157: TreeClusterRow treeClusterRow = new TreeClusterRow();
158: treeClusterRow.Name = fields[0];
159: treeClusterRow.Tree = fields[1];
160: treeClusterRow.TreeInstances = new List<SharpDX.Vector3>();
161: for (int i = 2; i < fields.Length; i = i + 3)
162: {
165:   float x = Convert.ToSingle(fields[i], provider);
166:   float y = Convert.ToSingle(fields[i + 1], provider);
167:   float z = Convert.ToSingle(fields[i + 2], provider);
170:   treeClusterRow.TreeInstances.Add(new SharpDX.Vector3(x, y, z));
```

Tree-cluster instance application (FixturesLoader.cs L390-415): for each cluster tree instance, base-tree polygons are offset by the LOCAL instance XYZ (X negated in code: `newPolygon.Vectors[i].X -= tree.X; Y += tree.Y; Z += tree.Z`, L408-410).

## Nuance recorded (B6 LIMITATION)

- Tree data files (treemap.mpk / tree_clusters.mpk) are SEPARATE archives from the per-zone nifs/fixtures CSVs (zones\trees\ is a global path).
- HOWEVER: trees/clusters are still INSTANTIATED in the world via fixtures.csv rows (fixture NIF filename matched against tree tables — `fixture.IsTree`/`IsTreeCluster`, FixturesLoader.cs L374-375, L390-392). So: tree MODEL + cluster LOCAL offsets = separate tables; cluster WORLD placement still comes from a fixture row. This refines "osobna ścieżka drzew od fixtures": separate data source, partially shared placement path.
