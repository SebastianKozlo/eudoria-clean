#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PE_GAMEBRYO_ORACLE_TOOL_R1_20261003 - Batch E1 phaseBC_evidence.py
Executor: pe-reconstruction. MODE: STATIC / LOCAL / READ-ONLY on originals.

Does:
  A2. Bounded GB_2.3 extraction: small metadata files + GbEvaluationSDKSetup.exe
      (listing first; then ONLY the Include / NiMain / NiSystem / NiCollision /
      NiAnimation source subtrees needed for version gates + pipeline reading;
      never the whole ISO, never the demos/docs/tools installers).
  A3. SOURCE_ORACLE_INDEX build: every s4 class file (order section 4 list) per
      GB version tree, with path, size, SHA256, and which s4 functions appear.
  B/C. Evidence packs: line-numbered extracts (whole small files, targeted
      functions from large files) for VERSION_SUPPORT / NIF_LOAD_PIPELINE /
      TRANSFORM_SEMANTICS / BOUNDING_VOLUME_SEMANTICS.

All outputs to sandbox. No writes into D:\gamebyroengine or pcg_install.
"""
import hashlib, json, os, re, subprocess

RUN = "PE_GAMEBRYO_ORACLE_TOOL_R1_20261003"
SBX = r"D:\Eudoria_Reconstruction\99_Audits\PE_GAMEBRYO_ORACLE_TOOL_R1_20261003\sandbox"
OUT = os.path.join(SBX, "phaseBC")
os.makedirs(OUT, exist_ok=True)
SEVEN = r"C:\Program Files\7-Zip\7z.exe"
GB = r"D:\gamebyroengine"
ISO23 = os.path.join(GB, "GB_2.3.iso")
G23 = os.path.join(SBX, "gb23")

R = {"run_id": RUN, "stage": "phaseBC_evidence", "gb23": {}, "index_rows": 0, "packs": {}, "notes": []}


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest().upper()


def read_text(p):
    b = open(p, "rb").read()
    for enc in ("utf-8-sig", "utf-8", "windows-1252"):
        try:
            return b.decode(enc)
        except UnicodeDecodeError:
            continue
    return b.decode("windows-1252", "replace")


def run7z(args):
    r = subprocess.run([SEVEN] + args, capture_output=True)
    return r.returncode, r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace")


# ============================================================ A2: GB_2.3 bounded extraction
os.makedirs(os.path.join(G23, "iso_root"), exist_ok=True)
for name in ["GbEvaluationSetup.ini", "Gb23EvaluationDisk01.txt", "license.txt", "readme.txt", "autorun.inf"]:
    rc, _, _ = run7z(["e", "-y", "-o" + os.path.join(G23, "iso_root"), ISO23, name])
    R["gb23"]["extract_" + name] = {"exit": rc, "size": os.path.getsize(os.path.join(G23, "iso_root", name)) if os.path.exists(os.path.join(G23, "iso_root", name)) else None}

SDKSETUP = os.path.join(G23, "GbEvaluationSDKSetup.exe")
if not os.path.exists(SDKSETUP):
    rc, _, _ = run7z(["e", "-y", "-o" + G23, ISO23, "GbEvaluationSDKSetup.exe"])
    R["gb23"]["sdksetup_extract_exit"] = rc
R["gb23"]["sdksetup_size"] = os.path.getsize(SDKSETUP) if os.path.exists(SDKSETUP) else None
R["gb23"]["sdksetup_sha256"] = sha256_file(SDKSETUP) if os.path.exists(SDKSETUP) else None

gb23_paths = []
if os.path.exists(SDKSETUP):
    rc, so, se = run7z(["l", "-slt", SDKSETUP])
    open(os.path.join(OUT, "gb23_sdksetup_listing.txt"), "w", encoding="utf-8").write(so)
    R["gb23"]["sdksetup_listing_exit"] = rc
    cur = {}
    for line in so.splitlines():
        if "=" in line:
            k, _, v = line.partition("=")
            k = k.strip(); v = v.strip()
            if k == "Path":
                if cur.get("Path"):
                    gb23_paths.append(cur)
                cur = {"Path": v}
            elif k in ("Size", "Attributes"):
                cur[k] = v
    if cur.get("Path"):
        gb23_paths.append(cur)
    R["gb23"]["sdksetup_entries"] = len(gb23_paths)

    # derive bounded extraction dirs from listing
    want_dirs = set()
    pat_interest = re.compile(
        r"(Include/NiVersion\.h$"
        r"|/(NiMain|NiSystem|NiCollision|NiAnimation)/"
        r"(NiStream|NiBinaryStream|NiObject|NiObjectNET|NiAVObject|NiNode|NiGeometry|NiGeometryData"
        r"|NiTexturingProperty|NiSourceTexture|NiPixelData|NiTimeController|NiControllerSequence"
        r"|NiKeyframeController|NiTransformController|NiBound|NiBoxBV|NiSphereBV|NiBoundingVolume"
        r"|NiVersion|NiViewerStrings)\.(cpp|h|inl)$)")
    for e in gb23_paths:
        pl = e["Path"].replace("\\", "/")
        if pat_interest.search(pl):
            want_dirs.add(os.path.dirname(pl))
    # drop dirs that are inside another wanted dir (prefix containment)
    drops = set()
    for a in want_dirs:
        for b in want_dirs:
            if a != b and (b + "/").startswith(a + "/"):
                drops.add(b)
    want_dirs -= drops
    R["gb23"]["want_dirs"] = sorted(want_dirs)
    if want_dirs:
        args = ["x", "-y", "-o" + os.path.join(G23, "sdk"), SDKSETUP] + [d + "/*" for d in sorted(want_dirs)]
        rc, so, se = run7z(args)
        open(os.path.join(OUT, "gb23_sdk_extract_log.txt"), "w", encoding="utf-8").write(so + "\n--STDERR--\n" + se)
        R["gb23"]["sdk_extract_exit"] = rc
    else:
        # fallback: no exploded paths - record what the setup actually contains
        R["gb23"]["sdk_extract_exit"] = None
        R["notes"].append("GB23 SDK setup listing had no exploded source paths; top entries: " +
                          "; ".join(e["Path"] for e in gb23_paths[:25]))
        # try cabs/msi one more bounded level
        containers = [e["Path"] for e in gb23_paths if re.search(r"\.(cab|msi)$", e["Path"], re.I)]
        R["gb23"]["containers_in_setup"] = containers[:20]
        if containers:
            rc, so, se = run7z(["e", "-y", "-o" + os.path.join(G23, "sdk_containers"), SDKSETUP] + containers[:6])
            R["gb23"]["container_extract_exit"] = rc
            cdir = os.path.join(G23, "sdk_containers")
            for cf in sorted(os.listdir(cdir))[:6] if os.path.isdir(cdir) else []:
                rc2, so2, _ = run7z(["l", "-slt", os.path.join(cdir, cf)])
                open(os.path.join(OUT, "gb23_container_listing_" + cf + ".txt"), "w", encoding="utf-8").write(so2)
                for line in so2.splitlines():
                    if line.startswith("Path = "):
                        pl = line[7:].replace("\\", "/")
                        if pat_interest.search(pl):
                            want_dirs.add(os.path.dirname(pl))
            if want_dirs:
                for cf in sorted(os.listdir(cdir))[:6] if os.path.isdir(cdir) else []:
                    rc, so, se = run7z(["x", "-y", "-o" + os.path.join(G23, "sdk"), os.path.join(cdir, cf)] +
                                       [d + "/*" for d in sorted(want_dirs)])
                R["gb23"]["want_dirs_after_container"] = sorted(want_dirs)

# dump GB23 metadata file contents
meta = {}
for name in ["GbEvaluationSetup.ini", "Gb23EvaluationDisk01.txt", "license.txt", "readme.txt"]:
    p = os.path.join(G23, "iso_root", name)
    if os.path.exists(p):
        meta[name] = read_text(p)
R["gb23"]["metadata_contents"] = meta

# ============================================================ A3 + B/C: trees
CLASS_FILES = [
    "NiStream.cpp", "NiStream.h", "NiStream.inl",
    "NiBinaryStream.cpp", "NiBinaryStream.h",
    "NiObject.cpp", "NiObject.h",
    "NiObjectNET.cpp", "NiObjectNET.h", "NiObjectNET.inl",
    "NiAVObject.cpp", "NiAVObject.h", "NiAVObject.inl",
    "NiNode.cpp", "NiNode.h", "NiNode.inl",
    "NiGeometry.cpp", "NiGeometry.h", "NiGeometryData.cpp", "NiGeometryData.h",
    "NiTexturingProperty.cpp", "NiTexturingProperty.h",
    "NiSourceTexture.cpp", "NiSourceTexture.h",
    "NiPixelData.cpp", "NiPixelData.h",
    "NiTimeController.cpp", "NiTimeController.h",
    "NiControllerSequence.cpp", "NiControllerSequence.h",
    "NiKeyframeController.cpp", "NiKeyframeController.h",
    "NiTransformController.cpp", "NiTransformController.h",
    "NiBound.cpp", "NiBound.h", "NiBound.inl",
    "NiBoxBV.cpp", "NiBoxBV.h",
    "NiSphereBV.cpp", "NiSphereBV.h",
    "NiBoundingVolume.cpp", "NiBoundingVolume.h",
    "NiVersion.h", "NiViewerStrings.cpp", "NiViewerStrings.h",
    "NiMain.lib",
]
FUNC_NAMES = ["LoadBinary", "SaveBinary", "RegisterLoader", "RegisterStreamables",
              "CreateObject", "LinkObject", "PostLinkObject"]

TREES = [
    ("GB_1_2", os.path.join(GB, "extracted", "Gb12_Source")),
    ("GB_2_6", os.path.join(GB, "extracted", "Gb26_src")),
    ("GB_1_1_2", os.path.join(GB, "Gamebryo 1.1.2 Evaluation")),
    ("GB_2_3", os.path.join(G23, "sdk")),
]

index_rows = []
for ver, root in TREES:
    if not os.path.isdir(root):
        R["notes"].append("tree missing: " + ver + " " + root)
        continue
    found = {}
    for dp, dns, fns in os.walk(root):
        for fn in fns:
            if fn in CLASS_FILES:
                found.setdefault(fn, []).append(os.path.join(dp, fn))
    for base in CLASS_FILES:
        for full in sorted(found.get(base, [])):
            rel = full[len(root):].lstrip("\\")
            sz = os.path.getsize(full)
            sha = sha256_file(full)
            funcs = []
            if base.lower().endswith((".cpp", ".h", ".inl")) and sz < 3_000_000:
                try:
                    txt = read_text(full)
                    funcs = [f for f in FUNC_NAMES if f in txt]
                except Exception as ex:
                    R["notes"].append("read fail %s: %s" % (full, ex))
            note = ""
            if base == "NiMain.lib":
                if "VC71" in rel and "ReleaseLib" in rel:
                    note = "representative VC71 ReleaseLib lib"
                elif rel.startswith("NiMain.lib"):
                    note = "flat tree root lib"
                elif "build" in rel:
                    note = "our build output lib (OUR_TOOL lineage)"
                else:
                    continue  # bound lib index to representative rows
            index_rows.append({
                "version_category": ver, "class_file": base, "rel_path": rel,
                "size": sz, "sha256": sha, "functions_present": funcs, "note": note})
R["index_rows"] = len(index_rows)
with open(os.path.join(OUT, "source_oracle_index.json"), "w", encoding="utf-8") as f:
    json.dump(index_rows, f, indent=1)

# duplicate-hash detection between CoreLibs headers and SDK Include mirrors (GB_1_2)
gb12 = [r for r in index_rows if r["version_category"] == "GB_1_2"]
bymap = {}
for r in gb12:
    bymap.setdefault(r["sha256"], []).append(r["rel_path"])
R["gb12_duplicate_hash_groups"] = {k: v for k, v in bymap.items() if len(v) > 1}

# ============================================================ B/C: evidence packs
def numbered(lines, a, b):
    return ["%04d: %s" % (i + 1, lines[i]) for i in range(a, min(b, len(lines)))]

def extract_functions(path, patterns, max_span=700):
    try:
        lines = read_text(path).splitlines()
    except Exception as ex:
        return ["!! read fail %s: %s" % (path, ex)]
    out, i, n = [], 0, len(lines)
    while i < n:
        ln = lines[i]
        if any(p in ln for p in patterns) and "(" in ln and not ln.lstrip().startswith(("//", "*", "/*")):
            start = i
            # signature may begin on an earlier line (return type); walk back at most 2 lines
            if start > 0 and lines[start - 1].strip() and not lines[start - 1].strip().endswith((";", "}", "{")) and re.match(r"^[A-Za-z_]", lines[start - 1]):
                start -= 1
            j = i + 1
            end = None
            while j < n and j - start < max_span:
                if lines[j].startswith("}"):
                    end = j
                    break
                j += 1
            if end is None:
                end = min(i + 80, n - 1)
            out.append("")
            out.append("---- function extract %s lines %d-%d ----" % (os.path.basename(path), start + 1, end + 1))
            out.extend(numbered(lines, start, end + 1))
            i = end + 1
            continue
        i += 1
    return out

def dump_full(path, label, pack, header=None):
    if not os.path.exists(path):
        pack.append("!! MISSING %s (%s)" % (label, path))
        return
    lines = read_text(path).splitlines()
    pack.append("")
    pack.append("======== FULL %s (%s) sha256=%s size=%d ========" %
                (label, path, sha256_file(path), os.path.getsize(path)))
    if header:
        pack.append("---- " + header)
    pack.extend(numbered(lines, 0, len(lines)))

def dump_funcs(path, label, patterns, pack):
    if not os.path.exists(path):
        pack.append("!! MISSING %s (%s)" % (label, path))
        return
    pack.append("")
    pack.append("======== FUNCS %s (%s) sha256=%s size=%d ========" %
                (label, path, sha256_file(path), os.path.getsize(path)))
    pack.extend(extract_functions(path, patterns))

def find_one(root, name):
    hits = []
    for dp, dns, fns in os.walk(root):
        if name in fns:
            hits.append(os.path.join(dp, name))
    return hits

def build_pack(ver, root):
    pack = ["# EVIDENCE PACK %s root=%s generated by phaseBC_evidence.py (%s)" % (ver, root, RUN)]
    v = ver
    # version identity
    for cand in (os.path.join(root, "SDK", "Win32", "Include", "NiVersion.h"),):
        dump_full(cand, "NiVersion.h_SDK_Win32_Include", pack)
    for p in sorted(find_one(root, "NiVersion.h")):
        dump_full(p, "NiVersion.h", pack)
    for p in sorted(find_one(root, "NiViewerStrings.cpp")):
        dump_full(p, "NiViewerStrings.cpp", pack)
    if not find_one(root, "NiViewerStrings.cpp"):
        for p in sorted(find_one(root, "NiViewerStrings.h")):
            dump_full(p, "NiViewerStrings.h", pack)
    # P2 core
    for p in sorted(find_one(root, "NiObject.cpp")):
        dump_full(p, "NiObject.cpp", pack, header="s4 NiObject + P2 GroupID evidence")
    for p in sorted(find_one(root, "NiBinaryStream.cpp")):
        dump_full(p, "NiBinaryStream.cpp", pack)
    # stream pipeline
    for p in sorted(find_one(root, "NiStream.cpp")):
        dump_funcs(p, "NiStream.cpp",
                   ["::Load(", "::Save(", "ReadHeader", "WriteHeader", "Version",
                    "LoadBinary", "SaveBinary", "RegisterLoader", "RegisterStreamables", "FindLinkID"], pack)
    for p in sorted(find_one(root, "NiStream.h")):
        dump_funcs(p, "NiStream.h", ["Version", "Load", "Save"], pack)
    # transforms
    for p in sorted(find_one(root, "NiAVObject.cpp")):
        dump_funcs(p, "NiAVObject.cpp",
                   ["SetTranslate", "SetRotate", "SetScale", "UpdateWorldData",
                    "LoadBinary", "SaveBinary", "UpdateWorldBound", "UpdateControllers", "SetSelectiveUpdate"], pack)
    for p in sorted(find_one(root, "NiAVObject.inl")):
        dump_full(p, "NiAVObject.inl", pack, header="s14 SetTranslate/SetRotate/SetScale inline contracts")
    for p in sorted(find_one(root, "NiAVObject.h")):
        dump_funcs(p, "NiAVObject.h", ["SetTranslate", "SetRotate", "SetScale", "UpdateWorldData", "LoadBinary"], pack)
    for p in sorted(find_one(root, "NiNode.cpp")):
        dump_funcs(p, "NiNode.cpp", ["AttachChild", "DetachChild", "SetAt", "LoadBinary", "SaveBinary", "UpdateWorldBound", "UpdateDownwardPass"], pack)
    for p in sorted(find_one(root, "NiNode.inl")):
        dump_full(p, "NiNode.inl", pack)
    # objectNET
    for p in sorted(find_one(root, "NiObjectNET.cpp")):
        dump_funcs(p, "NiObjectNET.cpp", ["LoadBinary", "SaveBinary", "LinkObject", "PostLinkObject", "RegisterStreamables", "SetName", "SetExtraData", "AddController"], pack)
    # geometry + textures + controllers
    for p in sorted(find_one(root, "NiGeometry.cpp")):
        dump_funcs(p, "NiGeometry.cpp", ["LoadBinary", "SaveBinary"], pack)
    for p in sorted(find_one(root, "NiGeometryData.cpp")):
        dump_funcs(p, "NiGeometryData.cpp", ["LoadBinary", "SaveBinary"], pack)
    for p in sorted(find_one(root, "NiTexturingProperty.cpp")):
        dump_funcs(p, "NiTexturingProperty.cpp", ["LoadBinary", "SaveBinary"], pack)
    for p in sorted(find_one(root, "NiSourceTexture.cpp")):
        dump_funcs(p, "NiSourceTexture.cpp", ["LoadBinary", "SaveBinary"], pack)
    for p in sorted(find_one(root, "NiPixelData.cpp")):
        dump_funcs(p, "NiPixelData.cpp", ["LoadBinary", "SaveBinary"], pack)
    for p in sorted(find_one(root, "NiTimeController.cpp")):
        dump_funcs(p, "NiTimeController.cpp", ["LoadBinary", "SaveBinary", "SetTarget"], pack)
    for p in sorted(find_one(root, "NiControllerSequence.cpp")):
        dump_funcs(p, "NiControllerSequence.cpp", ["LoadBinary", "SaveBinary", "SetTarget"], pack)
    for p in sorted(find_one(root, "NiKeyframeController.cpp")):
        dump_funcs(p, "NiKeyframeController.cpp", ["LoadBinary", "SaveBinary", "SetTarget"], pack)
    for p in sorted(find_one(root, "NiTransformController.cpp")):
        dump_funcs(p, "NiTransformController.cpp", ["LoadBinary", "SaveBinary", "SetTarget"], pack)
    # bounds
    for p in sorted(find_one(root, "NiBound.cpp")):
        dump_full(p, "NiBound.cpp", pack)
    for p in sorted(find_one(root, "NiBound.h")):
        dump_full(p, "NiBound.h", pack)
    for p in sorted(find_one(root, "NiBound.inl")):
        dump_full(p, "NiBound.inl", pack)
    for p in sorted(find_one(root, "NiBoxBV.cpp")):
        dump_funcs(p, "NiBoxBV.cpp", ["LoadBinary", "SaveBinary", "CreateFromData", "WorldBound", "CopyWorld", "SetToWorld"], pack)
    for p in sorted(find_one(root, "NiSphereBV.cpp")):
        dump_funcs(p, "NiSphereBV.cpp", ["LoadBinary", "SaveBinary", "CreateFromData", "WorldBound", "CopyWorld", "SetToWorld"], pack)
    for p in sorted(find_one(root, "NiBoundingVolume.cpp")):
        dump_funcs(p, "NiBoundingVolume.cpp", ["LoadBinary", "SaveBinary", "CreateFromData", "WorldBound", "CreateFromStream"], pack)
    for p in sorted(find_one(root, "NiBoundingVolume.h")):
        dump_funcs(p, "NiBoundingVolume.h", ["LoadBinary", "SaveBinary", "CreateFromStream", "CreateFromData", "WorldBound"], pack)
    outp = os.path.join(OUT, ("evidence_%s.txt" % v))
    open(outp, "w", encoding="utf-8", newline="\n").write("\n".join(pack))
    R["packs"][v] = {"path": outp, "lines": len(pack), "bytes": os.path.getsize(outp)}

for ver, root in TREES:
    if os.path.isdir(root):
        build_pack(ver, root)
    else:
        R["packs"][ver] = {"path": None, "missing_root": root}

R["completed_utc"] = __import__("datetime").datetime.utcnow().isoformat() + "Z"
with open(os.path.join(OUT, "phaseBC_result.json"), "w", encoding="utf-8") as f:
    json.dump(R, f, indent=1)
print("phaseBC done. index_rows=%d gb23_sdksetup_entries=%s gb23_want_dirs=%s" %
      (R["index_rows"], R["gb23"].get("sdksetup_entries"), R["gb23"].get("want_dirs")))
for k, v in R["packs"].items():
    print("PACK", k, v)
for n in R["notes"][:12]:
    print("NOTE", n[:200])
