# B3, B4, B5 — OpenDAoC-BuildNav + daoctocrysis + kinship analysis

## B3 — OpenDAoC/OpenDAoC-BuildNav (independent fixtures.csv reader)

- Repo: https://github.com/OpenDAoC/OpenDAoC-BuildNav (cloned read-only 2026-09-13; ONLY code reading, never executed)
- Commit SHA (master HEAD at clone): **291149188c0a67db00357f84518cf7b0309ffbb9**
- Language: C# (.NET); license GPL-3.0; org repo created 2025-02-23, last push 2026-07-18.
- README (VERBATIM, first lines): "A fork of the [buildnav tool](https://github.com/thekroko/uthgard-opensource/tree/master/pathing/buildnav) from the [uthgard-opensource repository](https://github.com/thekroko/uthgard-opensource), originally created by [thekroko](https://github.com/thekroko)."

### fixtures.csv parsing — VERBATIM CODE

File: `Client/ZoneExporter/Zone2Obj.cs` (method ExportNifs)

```csharp
184: using TextReader fixtureCsv = new StreamReader(ClientData.FindCSV(Zone, "fixtures.csv"));
...
195: int fixid = int.Parse(fixture[0], CultureInfo.InvariantCulture);
196: int nifid = int.Parse(fixture[1], CultureInfo.InvariantCulture);
197: string name = fixture[2];
199: float x = float.Parse(fixture[3], CultureInfo.InvariantCulture);
200: float y = float.Parse(fixture[4], CultureInfo.InvariantCulture);
201: float z = float.Parse(fixture[5], CultureInfo.InvariantCulture);
202: float a = (float)(short.Parse(fixture[6], CultureInfo.InvariantCulture) / 180f * Math.PI);  // rotation
203: float scale = float.Parse(fixture[7], CultureInfo.InvariantCulture);
210: bool collide = fixture[8] != "0";
211: int radius = int.Parse(fixture[9], CultureInfo.InvariantCulture);
212: bool ground = fixture[11] == "1";
218: bool flip = fixture[12] == "1";
224: int uniqueid = int.Parse(fixture[14]);
231: if (fixture.Length > 16)
233:     a3d = float.Parse(fixture[15], CultureInfo.InvariantCulture);   // axis-angle
234-236: ax, ay, az = fixture[16..18];
```

### Transform built BEFORE adding the NIF — VERBATIM CODE (L239-269)

```csharp
239: Matrix4 worldMatrix = Matrix4.Identity;
240: worldMatrix *= Matrix4.CreateScale(new Vector3(scale, -scale, scale));
241: if (a3d != null)
242:     worldMatrix *= Matrix4.CreateFromAxisAngle(new Vector3(ax, ay, -az), a3d.Value);
243: else
244:     worldMatrix *= Matrix4.CreateRotationZ(a);
246: worldMatrix *= Matrix4.CreateTranslation(new Vector3(x, y, z) + Zone.OffsetVector);
...
269: AddModelToObj(nifs[nifid], worldMatrix, ["collide", "collidee", "collision"], true, fixtureId: fixid);
```

Composition here: S × R × T (System.Numerics row-vector convention — same effective transform as DaocNavMesh's T×R×S column-vector form: scale first, then rotation, then translation). Zone offset is ADDED INTO the translation vector: `CreateTranslation(new Vector3(x,y,z) + Zone.OffsetVector)` (L246) — a different mechanism than DaocNavMesh's pre-multiplied traversal matrix, same effective result.
NOTE: scale Y negated here too (`scale, -scale, scale`); axis-angle Z negated (`ax, ay, -az`).

nifs.csv read: `Zone2Obj.cs` L277-318 `ReadNifEntries()` — id (data[0]) → nif filename (data[2]) → loads NiFile (own NIF parser).

## B4 — mharj/daoctocrysis ("model and location data")

- Repo: https://github.com/mharj/daoctocrysis (cloned read-only 2026-09-13; ONLY code reading, never executed)
- Commit SHA (master HEAD at clone): **3e98846c51ba6ee8e065fb4b27c03c6f2adcec6e**
- Language: C++ / Qt4 + MagickWand; description (GitHub API): "Automatically exported from code.google.com/p/daoctocrysis"; repo created 2015-04-02 (Google Code era project).

### VERBATIM CODE — File: `main_window.cpp`

```cpp
226: // model and location data
227: (comment line "// model and location data" directly precedes:)
228: if (! dem_files.extract( QString("%1/zone%2").arg( ui.builddir->text() ).arg( id ),"nifs.csv") ) {
233: if (! dem_files.extract( QString("%1/zone%2").arg( ui.builddir->text() ).arg( id ),"fixtures.csv") ) {
```

(Exact quote with real line numbers: L227 is the comment `// model and location data`; L228 extracts `nifs.csv`; L233 extracts `fixtures.csv`.)

Fixture → CryEngine instance conversion (main_window.cpp L338-383, `add_nifs_to_xml`):
```cpp
339: QFile file(QString("%1/zone%2/fixtures.csv").arg( ui.builddir->text() ).arg( id ));
347: int nif_id = list.at(1).toInt(&ok, 10 );
370: // ID,NIF #,Textual Name,X,Y,Z,A,Scale
371: double x = (list.at(3).toDouble()/65536*1024)+(((region_offset_x[id.toInt()]*32)-low_x)*4);
372: double y = (list.at(4).toDouble()/65536*1024)+(((region_offset_y[id.toInt()]*32)-low_y)*4);
373: double z = list.at(5).toDouble()/64;
374: double s = (list.at(7).toDouble()/100)/nif_cgf_scale[nif_name_id];
375: Instance.setAttribute("Pos", QString("%1,%2,%3").arg(y,0,'f',3).arg(x,0,'f',3).arg(z,0,'f',3) );
376: Instance.setAttribute("Scale",QString("%1").arg(s,0,'f',3) );
```

CryEngine direction: output is a `.veg` vegetation layer XML (L267: `save_xml(QString("%1/%2.veg")...)`) with `VegetationObject`/`Instances` elements and `FileName` = converted CGF model (`nif_cgf[nif_name_id]`, L353; CGF mapping built at L120). `TODO` file contains a sample CryEngine `<VegetationObject ... FileName="objects/natural/trees/exodus pines/pine_a.cgf" ...>` — CryEngine vegetation descriptor syntax. NetImmerse→CryEngine zone conversion CONFIRMED (terrain.pcx/offset.pcx heightmap compositing + LOD dds + NIF→CGF + .veg instances).

## B5 — Implementation kinship (fork/copy analysis)

Findings:
1. **No GitHub fork relationship among the four DAoC repos** (DAoC-MapCreator, DaocNavMesh, OpenDAoC-BuildNav, daoctocrysis): different languages (C# vs C++20 vs C# vs C++/Qt), different NIF parsers (Niflib.NET wrapper vs own Niflib.hpp vs own NiFile vs none — daoctocrysis only maps names), different matrix libraries (SharpDX vs glm vs System.Numerics vs none), different eras (2014-2017 / 2024 / 2025 / 2015), different licenses (GPL-2 / BSD-3 / GPL-3 / none).
2. **OpenDAoC-BuildNav is a DECLARED FORK of thekroko/uthgard-opensource `pathing/buildnav`** (README first line, quoted above) — its lineage is the Uthgard freeshard project, NOT MapCreator. So BuildNav is not a first-hand independent implementation, but it IS independent of the other three repos in this matrix.
3. **What the repos DO share is the underlying game-data format knowledge** (nifs.csv/fixtures.csv/Treemap.csv/tree_clusters.csv field layout of the DAoC client). Their agreement on non-obvious indices ([11] on-ground, [12] flip, [14] unique_id, [15..18] axis-angle, scale/100, Y-negation) mutually corroborates the format reading. Knowledge genealogy (a later author learning the format from an earlier repo) cannot be fully excluded for DaocNavMesh (2024) vs MapCreator (2017), but the implementations are demonstrably separate code.
4. Per the contract rule ("forki i kopie kodu NIE są niezależnymi źródłami"): OpenDAoC-BuildNav must be counted as ONE lineage with uthgard-opensource buildnav (not an independent source for the format); daoctocrysis (2015, Google Code) and DAoC-MapCreator (2014-2017) and DaocNavMesh (2024) are separate lineages. For EU935 relevance, the correct independent witnesses of the DAoC client static-world format are: daoctocrysis (2015), DAoC-MapCreator (2017), DaocNavMesh (2024), uthgard-opensource/OpenDAoC-BuildNav (one lineage).

IMPORTANT: none of this transfers the DAoC FORMAT to Entropia — it is a research pattern only (see matrix LIMITATION).
