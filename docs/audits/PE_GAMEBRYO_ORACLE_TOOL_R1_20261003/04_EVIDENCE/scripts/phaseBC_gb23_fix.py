#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PE_GAMEBRYO_ORACLE_TOOL_R1_20261003 - E1 fix: GB_2.3 Wise-setup bounded extraction.
The SDK setup is a Wise installer; 7z lists its file table FLAT with UPPERCASE
8.3 names. Extract ONLY the oracle-relevant class headers/libs by short name,
normalize into sandbox\gb23\sdk\Include, then rebuild the GB_2_3 index rows and
evidence pack. Bounded: no whole-setup extraction, no demos/docs/tools."""
import hashlib, json, os, re, subprocess

SBX = r"D:\Eudoria_Reconstruction\99_Audits\PE_GAMEBRYO_ORACLE_TOOL_R1_20261003\sandbox"
OUT = os.path.join(SBX, "phaseBC")
SEVEN = r"C:\Program Files\7-Zip\7z.exe"
G23 = os.path.join(SBX, "gb23")
SDKSETUP = os.path.join(G23, "GbEvaluationSDKSetup.exe")
LISTING = os.path.join(OUT, "gb23_sdksetup_listing.txt")

WANT = {
    "NIVERSION.H": "NiVersion.h",
    "NISTREAM.H": "NiStream.h", "NISTREAM.INL": "NiStream.inl",
    "NIBINARYSTREAM.H": "NiBinaryStream.h",
    "NIOBJECT.H": "NiObject.h",
    "NIOBJECTNET.H": "NiObjectNET.h", "NIOBJECTNET.INL": "NiObjectNET.inl",
    "NIAVOBJECT.H": "NiAVObject.h", "NIAVOBJECT.INL": "NiAVObject.inl",
    "NINODE.H": "NiNode.h", "NINODE.INL": "NiNode.inl",
    "NIGEOMETRY.H": "NiGeometry.h", "NIGEOMETRYDATA.H": "NiGeometryData.h",
    "NITEXTURINGPROPERTY.H": "NiTexturingProperty.h",
    "NISOURCETEXTURE.H": "NiSourceTexture.h",
    "NIPIXELDATA.H": "NiPixelData.h",
    "NITIMECONTROLLER.H": "NiTimeController.h",
    "NICONTROLLERSEQUENCE.H": "NiControllerSequence.h",
    "NIKEYFRAMECONTROLLER.H": "NiKeyframeController.h",
    "NITRANSFORMCONTROLLER.H": "NiTransformController.h",
    "NIBOUND.H": "NiBound.h", "NIBOUND.INL": "NiBound.inl",
    "NIBOXBV.H": "NiBoxBV.h", "NISPHEREBV.H": "NiSphereBV.h",
    "NIBOUNDINGVOLUME.H": "NiBoundingVolume.h",
    "NIVIEWERSTRINGS.H": "NiViewerStrings.h", "NIVIEWERSTRINGS.CPP": "NiViewerStrings.cpp",
    # core cpp probes (expected mostly absent in a binary SDK)
    "NISTREAM.CPP": "NiStream.cpp", "NIAVOBJECT.CPP": "NiAVObject.cpp",
    "NINODE.CPP": "NiNode.cpp", "NIOBJECT.CPP": "NiObject.cpp",
    "NIBOUND.CPP": "NiBound.cpp", "NIBOXBV.CPP": "NiBoxBV.cpp", "NISPHEREBV.CPP": "NiSphereBV.cpp",
    "NIBOUNDINGVOLUME.CPP": "NiBoundingVolume.cpp",
}

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest().upper()

# 1. parse listing for available names + sizes
txt = open(LISTING, encoding="utf-8", errors="replace").read()
entries, cur = [], {}
for line in txt.splitlines():
    if line.startswith("Path = "):
        if cur.get("Path"):
            entries.append(cur)
        cur = {"Path": line[7:]}
    elif line.startswith("Size = ") and cur.get("Path"):
        cur["Size"] = line[7:]
    elif line.startswith("Folder = ") and cur.get("Path"):
        cur["Folder"] = line[9:]
if cur.get("Path"):
    entries.append(cur)
avail = {}
for e in entries:
    avail.setdefault(e["Path"].upper(), []).append(e.get("Size", "?"))

ni_cpp = sorted({p for p in avail if re.match(r"^NI[A-Z0-9_]*\.CPP$", p)})
nimain_libs = sorted({p for p in avail if re.match(r"^NIMAIN.*\.LIB$", p)})
res = {"ni_cpp_entries_in_setup": ni_cpp, "nimain_lib_entries": nimain_libs,
       "want_present": {}, "want_absent": [], "extracted": {}}

# 2. extract wanted names
flat = os.path.join(G23, "sdk_flat")
norm = os.path.join(G23, "sdk", "Include")
os.makedirs(flat, exist_ok=True)
os.makedirs(norm, exist_ok=True)
for short, proper in sorted(WANT.items()):
    if short not in avail:
        res["want_absent"].append(short)
        continue
    res["want_present"][short] = avail[short]
    r = subprocess.run([SEVEN, "e", "-y", "-o" + flat, SDKSETUP, short],
                       capture_output=True)
    got = os.path.join(flat, short)
    if os.path.exists(got):
        dst = os.path.join(norm, proper)
        open(dst, "wb").write(open(got, "rb").read())
        res["extracted"][short] = {"proper": proper, "size": os.path.getsize(dst),
                                   "sha256": sha256_file(dst), "sevenzip_exit": r.returncode}

# 3. also record NiMain lib identity (extract first NIMAIN*.LIB entries, bounded 3)
libdir = os.path.join(G23, "sdk_libs")
os.makedirs(libdir, exist_ok=True)
librows = []
for short in nimain_libs[:3]:
    r = subprocess.run([SEVEN, "e", "-y", "-o" + libdir, SDKSETUP, short], capture_output=True)
    p = os.path.join(libdir, short)
    if os.path.exists(p):
        librows.append({"short_name": short, "size": os.path.getsize(p), "sha256": sha256_file(p),
                        "sevenzip_exit": r.returncode})
res["nimain_lib_rows"] = librows

# 4. GB23 metadata into result (ini etc. already in iso_root)
for name in ["GbEvaluationSetup.ini", "Gb23EvaluationDisk01.txt", "license.txt", "readme.txt"]:
    p = os.path.join(G23, "iso_root", name)
    if os.path.exists(p):
        res["meta_" + name] = open(p, "rb").read().decode("windows-1252", "replace")[:1200]

# 5. rebuild index rows for GB_2_3 + evidence pack
CLASS_FUNCS = ["LoadBinary", "SaveBinary", "RegisterLoader", "RegisterStreamables",
               "CreateObject", "LinkObject", "PostLinkObject"]
idx_path = os.path.join(OUT, "source_oracle_index.json")
rows = json.load(open(idx_path, encoding="utf-8"))
rows = [r for r in rows if r["version_category"] != "GB_2_3"]
for proper in sorted(set(WANT.values())):
    p = os.path.join(norm, proper)
    if os.path.exists(p):
        txtf = open(p, "rb").read().decode("windows-1252", "replace")
        funcs = [f for f in CLASS_FUNCS if f in txtf]
        rows.append({"version_category": "GB_2_3", "class_file": proper,
                     "rel_path": "sdk\\Include\\" + proper, "size": os.path.getsize(p),
                     "sha256": sha256_file(p), "functions_present": funcs,
                     "note": "extracted from GB_2.3.iso GbEvaluationSDKSetup.exe (Wise table, flat 8.3 names)"})
for lr in librows:
    rows.append({"version_category": "GB_2_3", "class_file": "NiMain.lib",
                 "rel_path": "sdk_libs\\" + lr["short_name"], "size": lr["size"],
                 "sha256": lr["sha256"], "functions_present": [],
                 "note": "GB23 Wise-table lib (short name identity)"})
json.dump(rows, open(idx_path, "w", encoding="utf-8"), indent=1)

# 6. GB_2_3 evidence pack (headers; functions extracted where declared)
def numbered(lines):
    return ["%04d: %s" % (i + 1, ln) for i, ln in enumerate(lines)]

def dump_full(path, label, pack):
    if not os.path.exists(path):
        pack.append("!! MISSING %s" % label)
        return
    lines = open(path, "rb").read().decode("windows-1252", "replace").splitlines()
    pack += ["", "======== FULL %s (%s) sha256=%s size=%d ========" %
             (label, path, sha256_file(path), os.path.getsize(path))]
    pack += numbered(lines)

def dump_funcs(path, label, patterns, pack):
    if not os.path.exists(path):
        pack.append("!! MISSING %s" % label)
        return
    lines = open(path, "rb").read().decode("windows-1252", "replace").splitlines()
    pack += ["", "======== FUNCS %s (%s) sha256=%s size=%d ========" %
             (label, path, sha256_file(path), os.path.getsize(path))]
    i = 0
    while i < len(lines):
        ln = lines[i]
        if any(p in ln for p in patterns) and not ln.lstrip().startswith(("//", "*", "/*")):
            pack.append("%04d: %s" % (i + 1, ln))
        i += 1

pack = ["# EVIDENCE PACK GB_2_3 (headers only - binary SDK; generated by phaseBC_gb23_fix.py)"]
dump_full(os.path.join(norm, "NiVersion.h"), "NiVersion.h", pack)
dump_full(os.path.join(norm, "NiViewerStrings.h"), "NiViewerStrings.h", pack)
dump_full(os.path.join(norm, "NiViewerStrings.cpp"), "NiViewerStrings.cpp", pack)
dump_funcs(os.path.join(norm, "NiStream.h"), "NiStream.h", ["Version", "Load", "Save"], pack)
dump_funcs(os.path.join(norm, "NiAVObject.h"), "NiAVObject.h",
           ["SetTranslate", "SetRotate", "SetScale", "UpdateWorldData", "LoadBinary", "UpdateWorldBound"], pack)
dump_funcs(os.path.join(norm, "NiAVObject.inl"), "NiAVObject.inl", ["SetTranslate", "SetRotate", "SetScale"], pack)
dump_funcs(os.path.join(norm, "NiNode.h"), "NiNode.h", ["AttachChild", "DetachChild", "SetAt", "LoadBinary"], pack)
dump_funcs(os.path.join(norm, "NiNode.inl"), "NiNode.inl", ["AttachChild", "DetachChild", "SetAt"], pack)
dump_full(os.path.join(norm, "NiBound.h"), "NiBound.h", pack)
dump_full(os.path.join(norm, "NiBound.inl"), "NiBound.inl", pack)
dump_funcs(os.path.join(norm, "NiBoundingVolume.h"), "NiBoundingVolume.h",
           ["LoadBinary", "SaveBinary", "CreateFromStream", "CreateFromData", "WorldBound"], pack)
dump_funcs(os.path.join(norm, "NiBoxBV.h"), "NiBoxBV.h", ["LoadBinary", "SaveBinary", "WorldBound"], pack)
dump_funcs(os.path.join(norm, "NiSphereBV.h"), "NiSphereBV.h", ["LoadBinary", "SaveBinary", "WorldBound"], pack)
dump_funcs(os.path.join(norm, "NiObjectNET.h"), "NiObjectNET.h",
           ["LoadBinary", "SaveBinary", "LinkObject", "PostLinkObject", "RegisterStreamables"], pack)
dump_funcs(os.path.join(norm, "NiObject.h"), "NiObject.h",
           ["LoadBinary", "SaveBinary", "Stream", "CreateObject", "LinkObject", "PostLinkObject", "RegisterStreamables"], pack)
outp = os.path.join(OUT, "evidence_GB_2_3.txt")
open(outp, "w", encoding="utf-8", newline="\n").write("\n".join(pack))
res["pack"] = {"path": outp, "lines": len(pack), "bytes": os.path.getsize(outp)}
json.dump(res, open(os.path.join(OUT, "gb23_fix_result.json"), "w", encoding="utf-8"), indent=1)

print("GB23 fix done. extracted=%d absent=%d ni_cpp_in_setup=%d nimain_libs=%s" %
      (len(res["extracted"]), len(res["want_absent"]), len(ni_cpp), nimain_libs[:4]))
print("absent:", res["want_absent"])
print("pack:", res["pack"])
print("index_rows_total:", len(rows))
