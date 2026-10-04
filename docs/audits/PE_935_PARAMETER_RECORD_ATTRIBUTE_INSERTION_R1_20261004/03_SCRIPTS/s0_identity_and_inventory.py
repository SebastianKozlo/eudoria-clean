# s0_identity_and_inventory.py
# RUN: PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004
# Purpose: (1) verify the pinned input identities (Entropia.exe, templates.vfs);
# (2) complete physical inventory of Data\Parameters (all files: name, size, SHA256,
#     numeric-basename classification; explicit 20006.vfs presence check).
# READ-ONLY against all corpus files. Writes only inside the run package.
import sys, os, hashlib, csv, json, re
sys.dont_write_bytecode = True

RUN = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004"
PARAM_DIR = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters"
EXE_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

EXPECT_EXE_SHA = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
EXPECT_EXE_SIZE = 8015872
EXPECT_TPL_SHA = "BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77"
EXPECT_TPL_SIZE = 560788

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()

def main():
    out = {}
    # 1) EXE identity
    exe_size = os.path.getsize(EXE_PATH)
    exe_sha = sha256_file(EXE_PATH)
    out["exe"] = {"path": EXE_PATH, "size": exe_size, "sha256": exe_sha,
                  "size_match": exe_size == EXPECT_EXE_SIZE,
                  "sha_match": exe_sha == EXPECT_EXE_SHA}
    # 2) Complete inventory of Data\Parameters
    files = sorted(os.listdir(PARAM_DIR))
    rows = []
    total_files = 0; total_vfs = 0; numeric_vfs = 0
    present_20006 = False
    for name in files:
        full = os.path.join(PARAM_DIR, name)
        if not os.path.isfile(full):
            out.setdefault("non_file_entries", []).append(name)
            continue
        total_files += 1
        size = os.path.getsize(full)
        sha = sha256_file(full)
        is_vfs = name.lower().endswith(".vfs")
        if is_vfs:
            total_vfs += 1
        base = name[:-4] if is_vfs else os.path.splitext(name)[0]
        m = re.fullmatch(r"\d+", base)
        numeric = bool(m)
        if is_vfs and numeric:
            numeric_vfs += 1
        if base == "20006":
            present_20006 = True
        rows.append({"filename": name, "relative_path": "Data\\Parameters\\" + name,
                     "size_bytes": size, "sha256": sha,
                     "is_vfs": is_vfs, "numeric_basename": base if numeric else "non-numeric"})
    out["inventory"] = {
        "total_parameter_files": total_files,
        "total_vfs_files": total_vfs,
        "numeric_vfs_count": numeric_vfs,
        "subdirectories": 0,
        "20006_vfs_present": present_20006,
        "all_files_are_vfs": total_files == total_vfs,
    }
    # 3) templates.vfs pin
    tpl_row = [r for r in rows if r["filename"].lower() == "templates.vfs"][0]
    out["templates_vfs"] = {"size_match": tpl_row["size_bytes"] == EXPECT_TPL_SIZE,
                            "sha_match": tpl_row["sha256"] == EXPECT_TPL_SHA,
                            **tpl_row}
    # write CSV inventory (committed artifact)
    csv_path = os.path.join(RUN, "PARAMETER_FILE_INVENTORY.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["relative_path", "filename", "size_bytes", "sha256",
                    "is_vfs", "numeric_basename"])
        for r in rows:
            w.writerow([r["relative_path"], r["filename"], r["size_bytes"],
                        r["sha256"], r["is_vfs"], r["numeric_basename"]])
    raw_path = os.path.join(RUN, "01_RAW", "S0_IDENTITY_AND_INVENTORY.json")
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(json.dumps({"exe_ok": out["exe"]["size_match"] and out["exe"]["sha_match"],
                      "tpl_ok": out["templates_vfs"]["size_match"] and out["templates_vfs"]["sha_match"],
                      "inventory": out["inventory"]}, indent=2))

if __name__ == "__main__":
    main()
