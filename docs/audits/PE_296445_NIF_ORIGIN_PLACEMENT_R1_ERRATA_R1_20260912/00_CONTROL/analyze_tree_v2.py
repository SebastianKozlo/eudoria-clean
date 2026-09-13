#!/usr/bin/env python3
# analyze_tree_v2.py — POPRAWIONA kopia instrumentu analyze_tree.py z runu R1 (ERRATA, grupa B).
#
# BUG R1 (audyt zewnętrzny F2, adjudykowany przez PE-MASTER):
#   R1 00_CONTROL\analyze_tree.py, funkcja compute(): zapisywała world[i] = cur,
#   czyli transformację RODZICA, a dopiero potem liczyła w = compose(cur, local)
#   i przekazywała w dzieciom. Geometria była przekształcana przez world[mesh]
#   — z POMINIĘCIEM WŁASNEJ transformacji mesha.
#
# KONWENCJA POPRAWNA (ta wersja):
#   world[i] = parent_world ∘ local_i  (z WŁASNĄ transformacją obiektu),
#   parent korzenia (blok 0) = identity.
#
# BRAMKA G1 (wartości oczekiwane podwójnie zweryfikowane: audyt zewnętrzny probe.json
# + rekomputacja PE-MASTER — to jest bramka REPRODUKCJI, assertowana tutaj, nie wpisana
# na sztywno do wyników):
#   G1a: dokładnie 14 z 30 meshy zmienia world_T względem TRANSFORM_TABLE.csv runu R1
#        (16 pozostałych identycznych — kontrola negatywna).
#   G1b: bbox globalny złożonej geometrii = min (-2500.0, -2500.0, ~-1.27e-08)
#        do max (2500.0, 2500.0, 15620.0); tolerancja 1e-4 bezwzględna.
#        (ujemne Z ~ -1.27e-08 to epsilon numeryczny kompozycji, nie przesunięcie)
#   G1c: mesh #66 B_Eu_b047_glowsak:0 world_T == (401.14190673828125,
#        -1611.4522705078125, -368.0000305175781) (równość co do f64 z JSON-a).
#   G1d (krzyżowa): wszystkie 14 skorygowanych world_T zgodne z probe.json audytora
#        (tolerancja 1e-6 bezwzględna; niezależna lineage obliczeń).
#
# WEJŚCIA (READ-ONLY):
#   R1 01_RAW\BLOCKMAP_V2.json        — parsowanie 155 bloków (niezmienione, poprawne)
#   R1 02_ANALYSIS\TRANSFORM_TABLE.csv — tabela R1 (world_T do porównania; SUPERSUMOWANE)
#   probe.json audytora zewnętrznego   — wiersze krzyżowe (wartości oczekiwane)
# WYJŚCIA (NOWY katalog ERRATA):
#   01_CORRECTED\TRANSFORM_TABLE_CORRECTED.csv
#   01_CORRECTED\TREE_MESHES_CORRECTED.json
#   01_CORRECTED\TREE_ANALYSIS_CORRECTED.txt
#   02_EVIDENCE\G1_GATE_RESULTS.json
import json, struct, hashlib, os, sys, csv, math

ERR = r"D:\Eudoria_Reconstruction\09_Research\PE_296445_NIF_ORIGIN_PLACEMENT_R1_ERRATA_R1_20260912"
R1  = r"D:\Eudoria_Reconstruction\09_Research\PE_296445_NIF_ORIGIN_PLACEMENT_R1_20260912"
PROBE = r"C:\Users\User\Documents\ChatGPT\PE\audit-296445-placement-r1\probe.json"

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

B = json.load(open(os.path.join(R1, "01_RAW", "BLOCKMAP_V2.json")))
blocks = B["blocks"]
N = len(blocks)

def mat_mul(a, b):  # 3x3 row-major
    return [[sum(a[i][k]*b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
def mat_vec(m, v):
    return [sum(m[i][k]*v[k] for k in range(3)) for i in range(3)]

def compose(parent, local):
    # world = parent_world ∘ local (zgodnie z R1 compose; R1 tylko ZAPISYWAŁ złą wartość)
    Rp, Tp, Sp = parent
    Rl, Tl, Sl = local
    R = mat_mul(Rp, Rl)
    S = Sp * Sl
    T = [mat_vec(Rp, [Tl[i]*Sp for i in range(3)])[i] + Tp[i] for i in range(3)]
    return (R, T, S)

identity = ([[1,0,0],[0,1,0],[0,0,1]], [0,0,0], 1.0)

# ---------- 1. drzewo (children) ----------
parents = {}
for b in blocks:
    for ch in b.get("children", []):
        if ch is not None:
            if ch in parents: print(f"WARN: block {ch} has multiple parents")
            parents[ch] = b["index"]

# ---------- 2. POPRAWIONA kompozycja: world[i] = parent_world ∘ local_i ----------
world = {}
def compute(i, parent_world):
    b = blocks[i]
    R = b.get("rotation", identity[0]); T = b.get("translation", identity[1]); S = b.get("scale", 1.0)
    w_i = compose(parent_world, (R, T, S))   # WŁASNA transformacja uwzględniona
    world[i] = w_i
    for ch in b.get("children", []):
        if ch is not None: compute(ch, w_i)

b0 = blocks[0]
compute(0, identity)   # root parent = identity

# ---------- 3. geometria: per-mesh bbox lokalny (surowe wierzchołki) i złożony ----------
mesh_stats = []
allmin = [1e30]*3; allmax = [-1e30]*3
rawmin = [1e30]*3; rawmax = [-1e30]*3
for b in blocks:
    if b["type"] == "NiTriShape":
        db = blocks[b["data_ref"]]
        verts = db.get("vertices", [])
        w = world[b["index"]]
        R, T, S = w
        tmin = [1e30]*3; tmax = [-1e30]*3
        rmin = [1e30]*3; rmax = [-1e30]*3
        for v in verts:
            tv = [mat_vec(R, [v[i]*S for i in range(3)])[i] + T[i] for i in range(3)]
            for i in range(3):
                tmin[i] = min(tmin[i], tv[i]); tmax[i] = max(tmax[i], tv[i])
                rmin[i] = min(rmin[i], v[i]); rmax[i] = max(rmax[i], v[i])
                allmin[i] = min(allmin[i], tv[i]); allmax[i] = max(allmax[i], tv[i])
                rawmin[i] = min(rawmin[i], v[i]); rawmax[i] = max(rawmax[i], v[i])
        mesh_stats.append({"idx": b["index"], "name": b["name"], "nverts": db["num_vertices"],
                           "ntris": db["num_triangles"], "parent": parents.get(b["index"]),
                           "local_T": b["translation"], "local_S": b["scale"],
                           "world_T": w[1], "world_S": w[2],
                           "bbox_local": [rmin, rmax], "bbox_world": [tmin, tmax],
                           "nprops": len(b.get("properties", [])), "props": b.get("properties", [])})

# ---------- 4. porównanie z tabelą R1 (world_T superseded) ----------
r1_wt = {}
with open(os.path.join(R1, "02_ANALYSIS", "TRANSFORM_TABLE.csv"), newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        r1_wt[int(row["mesh_idx"])] = json.loads(row["world_T"])

EPS_UNCH = 1e-9
changed = []
unchanged = []
for m in mesh_stats:
    old = r1_wt[m["idx"]]
    dmax = max(abs(m["world_T"][k] - old[k]) for k in range(3))
    m["world_T_r1_superseded"] = old
    m["world_T_delta_max"] = dmax
    (changed if dmax > EPS_UNCH else unchanged).append(m["idx"])

# ---------- BRAMKI G1 (assert w skrypcie) ----------
gate = {}
gate["G1a_changed_count"] = {"expected": 14, "actual": len(changed),
                             "changed_idx": changed, "unchanged_count": len(unchanged)}
assert len(mesh_stats) == 30, f"mesh count != 30: {len(mesh_stats)}"
assert len(changed) == 14, f"G1a FAIL: changed != 14 (actual {len(changed)}): {changed}"
assert len(unchanged) == 16, f"G1a FAIL: unchanged != 16 (actual {len(unchanged)})"

EXP_BMIN = [-2500.0, -2500.0, -1.2652602576768146e-08]
EXP_BMAX = [2500.0, 2500.0, 15620.0]
TOL = 1e-4
dmin = [abs(allmin[k] - EXP_BMIN[k]) for k in range(3)]
dmax_ = [abs(allmax[k] - EXP_BMAX[k]) for k in range(3)]
gate["G1b_bbox"] = {"computed_min": allmin, "computed_max": allmax,
                    "expected_min": EXP_BMIN, "expected_max": EXP_BMAX,
                    "absdiff_min": dmin, "absdiff_max": dmax_, "tolerance": TOL}
assert all(x <= TOL for x in dmin + dmax_), f"G1b FAIL: bbox out of tolerance: {allmin}..{allmax}"

gl = [m for m in mesh_stats if m["idx"] == 66][0]
EXP_GLOW = [401.14190673828125, -1611.4522705078125, -368.0000305175781]
dgl = [abs(gl["world_T"][k] - EXP_GLOW[k]) for k in range(3)]
gate["G1c_glowsak"] = {"mesh": 66, "name": gl["name"], "computed": gl["world_T"],
                       "expected": EXP_GLOW, "absdiff": dgl}
assert dgl == [0.0, 0.0, 0.0], f"G1c FAIL: glowsak world_T != expected: {gl['world_T']}"

probe = json.load(open(PROBE))
probe_rows = {r["index"]: r["correctT"] for r in probe["transforms"]["rows"]}
assert len(probe_rows) == 14, f"probe.json rows != 14"
XTOL = 1e-6
xdiffs = {}
for idx, expT in probe_rows.items():
    got = [m for m in mesh_stats if m["idx"] == idx][0]["world_T"]
    d = max(abs(got[k] - expT[k]) for k in range(3))
    xdiffs[idx] = d
    assert d <= XTOL, f"G1d FAIL: mesh {idx} world_T {got} != probe.json {expT} (diff {d})"
gate["G1d_probe_crosscheck"] = {"source": "probe.json (audyt zewnetrzny, transformacje niezalezne)",
                                "tolerance": XTOL, "max_absdiff_per_mesh": xdiffs}
assert set(probe_rows.keys()) == set(changed), f"G1d FAIL: changed set != probe set"

# importer tail (7 floatów) — ekstrema SUROWYCH tablic (fakt z R1 utrzymany)
imp = [b for b in blocks if b["type"] == "NiArkImporterExtraData"][0]
th = bytes.fromhex(imp["ark_tail_hex"])
imp_floats = [struct.unpack_from("<f", th, 13+4*k)[0] for k in range(7)]

gate["inputs"] = {
    "BLOCKMAP_V2.json": sha256_file(os.path.join(R1, "01_RAW", "BLOCKMAP_V2.json")),
    "TRANSFORM_TABLE.csv (R1, superseded world_T)": sha256_file(os.path.join(R1, "02_ANALYSIS", "TRANSFORM_TABLE.csv")),
    "probe.json (audyt zewnetrzny)": sha256_file(PROBE),
}
gate["verdict"] = "G1 PASS (a: 14/30 changed + 16 unchanged; b: bbox w tolerancji 1e-4; c: glowsak exact; d: 14/14 zgodnych z probe.json)"

# ---------- 5. zapis artefaktów ----------
with open(os.path.join(ERR, "01_CORRECTED", "TRANSFORM_TABLE_CORRECTED.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["mesh_idx", "mesh_name", "parent", "local_T", "local_S", "world_T",
                "world_T_r1_superseded", "changed_vs_r1", "bbox_local_min", "bbox_local_max",
                "bbox_world_min", "bbox_world_max", "nverts", "ntris", "props"])
    for m in mesh_stats:
        w.writerow([m["idx"], m["name"], m["parent"], m["local_T"], m["local_S"], m["world_T"],
                    m["world_T_r1_superseded"], m["idx"] in changed,
                    m["bbox_local"][0], m["bbox_local"][1], m["bbox_world"][0], m["bbox_world"][1],
                    m["nverts"], m["ntris"], m["props"]])

json.dump({"mesh_stats": mesh_stats, "orphan_blocks": [],
           "convention": "world[i] = parent_world ∘ local_i; root parent = identity (poprawka ERRATA B1)",
           "global_bbox_composed": {"min": allmin, "max": allmax},
           "raw_vertex_extremes": {"min": rawmin, "max": rawmax},
           "importer_tail_floats": imp_floats,
           "changed_meshes_vs_r1": changed, "unchanged_meshes_vs_r1": sorted(unchanged),
           "g1_gate": gate},
          open(os.path.join(ERR, "01_CORRECTED", "TREE_MESHES_CORRECTED.json"), "w"), indent=1)

lines = []
lines.append("=== SCENE TREE (children only) — world = parent∘local, root parent = identity (ERRATA v2) ===")
def ptree(i, d=0):
    b = blocks[i]
    nm = b.get("name", "")
    extra = ""
    if b["type"] == "NiTriShape":
        extra = f" -> data={b['data_ref']} tris={blocks[b['data_ref']]['num_triangles']}"
    ex = b.get("extra_data_ref")
    exs = f" extra->{ex}:{blocks[ex]['type']}" if ex is not None else ""
    ctrl = b.get("controller_ref")
    ctrls = f" ctrl->{ctrl}:{blocks[ctrl]['type']}" if ctrl is not None else ""
    wT = world[i][1] if i in world else None
    wTs = f" worldT={[round(x,4) for x in wT]}" if wT is not None else ""
    lines.append("  "*d + f"[{b['index']}] {b['type']} '{nm}' T={b.get('translation')} S={b.get('scale')}{wTs}{extra}{exs}{ctrls}")
    for ch in b.get("children", []):
        if ch is not None: ptree(ch, d+1)
for i in range(N):
    if i not in parents:
        ptree(i)
lines.append("")
lines.append("=== GLOBAL GEOMETRY BBOX (world-composed z WLASNA transformacja mesha; poprawka ERRATA B) ===")
lines.append(f"world bbox min: {allmin}")
lines.append(f"world bbox max: {allmax}")
lines.append(f"extents: {[allmax[i]-allmin[i] for i in range(3)]}  (~5000 x 5000 x 15620 j.m.)")
lines.append("NOTE: ujemne Z min (~-1.27e-08) to epsilon numeryczny kompozycji, nie przesuniecie.")
lines.append(f"raw (untransformed vertices) extremes min: {rawmin} max: {rawmax}")
lines.append("NOTE (ERRATA B4): ekstrema SUROWYCH tablic wierzcholkow pochodza z ROZNYCH ukladow lokalnych;")
lines.append("      ich min/max NIE jest bboxem sceny po zlozeniu — ogon importera odpowiada wlasnie tym ekstremom.")
lines.append("")
lines.append("=== IMPORTER TAIL FLOATS (7) ===")
lines.append(f"[u32 0][u32 0][u32 -1][u8 0xFF] + 7xf32 = {imp_floats}")
lines.append("zgodnosc bitowa z ekstremami surowych tablic: TAK (fakt R1 utrzymany); semantyka 7. floata (0.0) = UNKNOWN.")
lines.append("")
lines.append(f"=== MESH TABLE (30) — changed vs R1: {len(changed)} ===")
for m in mesh_stats:
    mark = "CHANGED" if m["idx"] in changed else "same"
    lines.append(f"[{m['idx']:3d}] {m['name']!r:28s} verts={m['nverts']:4d} tris={m['ntris']:4d} parent={m['parent']} localT={[round(x,2) for x in m['local_T']]} worldT={[round(x,3) for x in m['world_T']]} [{mark}] props={m['props']}")
lines.append("")
lines.append("=== G1 GATE (asserted in-script) ===")
lines.append(json.dumps(gate, indent=1))
lines.append("")
lines.append("=== REF CENSUS (in-refs per block) ===")
inrefs = {}
for b in blocks:
    for ch in b.get("children", []):
        if ch is not None: inrefs.setdefault(ch, []).append((b["index"], "child"))
    for pr in b.get("properties", []):
        if pr is not None: inrefs.setdefault(pr, []).append((b["index"], "property"))
    for ef in b.get("effects", []):
        if ef is not None: inrefs.setdefault(ef, []).append((b["index"], "effect"))
    if b.get("extra_data_ref") is not None: inrefs.setdefault(b["extra_data_ref"], []).append((b["index"], "extra"))
    if b.get("next_extra_data_ref") is not None: inrefs.setdefault(b["next_extra_data_ref"], []).append((b["index"], "extra_next"))
    if b.get("controller_ref") is not None: inrefs.setdefault(b["controller_ref"], []).append((b["index"], "controller"))
    if b.get("data_ref") is not None: inrefs.setdefault(b["data_ref"], []).append((b["index"], "data"))
    if b.get("skin_instance_ref") is not None: inrefs.setdefault(b["skin_instance_ref"], []).append((b["index"], "skin"))
    if b.get("target_ref") is not None: inrefs.setdefault(b["target_ref"], []).append((b["index"], "ctrl_target"))
    if b.get("uvdata_ref") is not None: inrefs.setdefault(b["uvdata_ref"], []).append((b["index"], "uvdata"))
    if b.get("source_texture_ref") is not None: inrefs.setdefault(b["source_texture_ref"], []).append((b["index"], "src_tex"))
orphans = [i for i in range(N) if i not in inrefs and i != 0]
lines.append(f"orphan blocks (no in-refs, not root): {orphans}")
missing = [(i, refs) for i, refs in inrefs.items() if not (0 <= i < N)]
lines.append(f"refs out of range: {missing}")
lines.append("")
lines.append("=== ROOT CHILDREN CENSUS (ERRATA F1) ===")
ch0 = blocks[0].get("children", [])
lines.append(f"root children slots: {len(ch0)}; -1 slots: {sum(1 for c in ch0 if c is None)}; real children: {sum(1 for c in ch0 if c is not None)}")
open(os.path.join(ERR, "01_CORRECTED", "TREE_ANALYSIS_CORRECTED.txt"), "w", encoding="utf-8").write("\n".join(lines) + "\n")

json.dump(gate, open(os.path.join(ERR, "02_EVIDENCE", "G1_GATE_RESULTS.json"), "w"), indent=1)

print("G1 PASS: changed=14, unchanged=16")
print("bbox min:", allmin)
print("bbox max:", allmax)
print("glowsak[66] world_T:", gl["world_T"])
print("artifacts written: TRANSFORM_TABLE_CORRECTED.csv, TREE_MESHES_CORRECTED.json, TREE_ANALYSIS_CORRECTED.txt, G1_GATE_RESULTS.json")
