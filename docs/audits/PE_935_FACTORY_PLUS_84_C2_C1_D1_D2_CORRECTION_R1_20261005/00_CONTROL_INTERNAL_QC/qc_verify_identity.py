# QC verification script 2: quotecheck, manifest re-hash, identity pins, PINS triple-check
# RUN_ID: PE_935_QC_INTERNAL_20261005 (worker: pe-master-auditor, fresh context)
# Reads ONLY. Writes nothing.
import json, csv, hashlib, ast, re, os, sys, subprocess

sys.dont_write_bytecode = True

REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
PKG = os.path.join(REPO, "docs", "audits",
                  "PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005")
BASE_SHA = "9d31a82b6589f46e9ca6c75c6e323b433c1ebf92"

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest().upper()

print("=== A. Identity pins ===")
exe = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
sz = os.path.getsize(exe)
sh = sha256_file(exe)
print("EXE size:", sz, "(declared 8015872)", "match:", sz == 8015872)
print("EXE sha256:", sh)
print("EXE sha match:", sh == "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31")

drep = r"C:\Users\User\Documents\ChatGPT\PE\PE_935_F84_C2_C1_DESKTOP_POST_AUDIT_20261005\REPORT.md"
sz2 = os.path.getsize(drep)
sh2 = sha256_file(drep)
print("Desktop report size:", sz2, "(declared 15535)", "match:", sz2 == 15535)
print("Desktop report sha256:", sh2)
print("Desktop sha match:", sh2 == "31AA87BC7C38089C7F648B5C749E196D80C4C6ED37823A96D5379CF84E78E61E")

# contract file itself
contract = r"C:\Users\User\Documents\ChatGPT\PE\F84_C2_C1_D1_D2_PROMPT_REVIEW_20261005\OPENCODE_F84_C2_C1_D1_D2_CORRECTION_COMPLETE_20261005.md"
print("Contract size:", os.path.getsize(contract), "sha:", sha256_file(contract))

print()
print("=== B. Source manifest pin (BASE package) ===")
sm = os.path.join(REPO, "docs", "audits",
                 "PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005",
                 "COMMITTED_PACKAGE_MANIFEST_SHA256.csv")
print("source manifest size:", os.path.getsize(sm), "(declared 5613)")
print("source manifest sha:", sha256_file(sm))
print("sha match:", sha256_file(sm) == "A407694EC96BBDDE8A8CE2E1D5808BACF39762017EE80B9A8A03D5AC6125897E")

print()
print("=== C. Independent supersession quotecheck (own parser) ===")
led = open(os.path.join(PKG, "SUPERSESSION_LEDGER.md"), encoding="utf-8").read()
records = re.findall(r"^## (S-(?:D1|D2|CM|AUD)-\d+)", led, re.M)
print("record headers:", records, "count:", len(set(records)))
excerpt_lines = [l for l in led.splitlines() if "ORIGINAL_EXCERPT" in l and "`" in l]
print("excerpt lines:", len(excerpt_lines))
current_src = None
fails = []
checked = 0
for line in led.splitlines():
    if line.startswith("- SOURCE_FILE: "):
        current_src = line[len("- SOURCE_FILE: "):].strip().strip("`")
    elif "ORIGINAL_EXCERPT" in line and "`" in line and current_src:
        a = line.find("`"); b = line.rfind("`")
        if b > a:
            excerpt = line[a+1:b]
            sp = current_src
            if not os.path.isabs(sp):
                sp = os.path.join(REPO, sp)
            try:
                src_content = open(sp, encoding="utf-8").read()
                ok = excerpt in src_content
            except OSError:
                ok = False
            checked += 1
            if not ok:
                fails.append((current_src, excerpt[:100]))
print("excerpts checked:", checked, "failures:", len(fails))
for f in fails:
    print("  FAIL:", f)

print()
print("=== D. Manifest bijection + full re-hash (38 rows) ===")
man = os.path.join(PKG, "COMMITTED_PACKAGE_MANIFEST_SHA256.csv")
with open(man, encoding="utf-8-sig", newline="") as f:
    mrows = list(csv.DictReader(f))
print("manifest rows:", len(mrows))
print("manifest columns:", list(mrows[0].keys()))
# physical files under PKG
phys = []
for root, dirs, files in os.walk(PKG):
    for fn in files:
        full = os.path.join(root, fn)
        rel = os.path.relpath(full, REPO).replace("\\", "/")
        phys.append(rel)
phys_set = set(phys)
print("physical files under PKG (incl. this QC dir):", len(phys))
# manifest declared set
man_set = set()
man_map = {}
for r in mrows:
    rel = r.get("path") or r.get("rel_path") or r.get("file")
    man_set.add(rel)
    man_map[rel] = r
missing = man_set - (phys_set | {"AUDIT_ENTRYPOINT.md"})
extra = (phys_set - man_set) - {os.path.relpath(man, REPO).replace("\\", "/")}
print("manifest paths missing on disk:", missing)
print("disk files not in manifest (excl. manifest itself):")
for e in sorted(extra):
    print("   ", e)
size_mm = []
sha_mm = []
for r in mrows:
    rel = r.get("path") or r.get("rel_path") or r.get("file")
    dsize = int(r.get("size_bytes") or r.get("size") or 0)
    dsha = (r.get("sha256") or "").strip().upper()
    if rel == "AUDIT_ENTRYPOINT.md":
        full = os.path.join(REPO, "AUDIT_ENTRYPOINT.md")
    else:
        full = os.path.join(REPO, rel.replace("/", os.sep))
    asize = os.path.getsize(full)
    asha = sha256_file(full)
    if asize != dsize:
        size_mm.append((rel, dsize, asize))
    if asha != dsha:
        sha_mm.append((rel, dsha, asha))
print("size mismatches:", size_mm)
print("sha mismatches:", sha_mm)
dups = len(man_set) != len([r for r in mrows])
print("duplicate rows:", len(mrows) - len(man_set))

print()
print("=== E. AUDIT_ENTRYPOINT.md untouched (vs BASE blob) ===")
r = subprocess.run(["git", "-C", REPO, "diff", BASE_SHA, "--", "AUDIT_ENTRYPOINT.md"],
                   capture_output=True)
print("diff vs BASE empty:", r.stdout == b"" and r.stderr == b"")
ep_sha = sha256_file(os.path.join(REPO, "AUDIT_ENTRYPOINT.md"))
print("entrypoint sha256 (current):", ep_sha)
blob = subprocess.run(["git", "-C", REPO, "rev-parse", BASE_SHA + ":AUDIT_ENTRYPOINT.md"],
                      capture_output=True, text=True).stdout.strip()
print("entrypoint blob at BASE:", blob)

print()
print("=== F. PINS triple-check: BASE blob AST vs on-disk script PINS vs EXPECTED_PIN_REGISTRY ===")
base_pkg = "docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005"
src = subprocess.run(["git", "-C", REPO, "show", f"{BASE_SHA}:{base_pkg}/03_SCRIPTS/c1_pin_ledger.py"],
                     capture_output=True).stdout
print("BASE c1_pin_ledger blob sha (content):", hashlib.sha256(src).hexdigest().upper())
print("declared source_file_sha256: 757225FEBD2C3E7B13A779199C123CB664481B189672B3A007EBDC1B39222D47")
tree = ast.parse(src.decode("utf-8"))
pins_ast = None
for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name) and t.id == "PINS":
                pins_ast = ast.literal_eval(node.value)
print("PINS from BASE blob:", len(pins_ast), "type:", type(pins_ast).__name__)
if isinstance(pins_ast, dict):
    items = pins_ast
else:
    items = {e[0]: e[1:] for e in pins_ast}
print("PINS keys sample:", list(items)[:3])
# normalize BASE PINS to {claim_id: {va, role, expect_bytes, expect_ea, expect_imm}}
def norm_entry(cid, entry):
    # entry is a tuple like (va_int_or_str, role, bytes, ea, imm) or dict; introspect
    if isinstance(entry, dict):
        return entry
    return tuple(entry) if isinstance(entry, tuple) else entry
# Compare with EXPECTED_PIN_REGISTRY
reg = json.load(open(os.path.join(PKG, "EXPECTED_PIN_REGISTRY.json"), encoding="utf-8-sig"))
reg_pins = {p["claim_id"]: p for p in reg["pins"]}
print("registry pins:", len(reg_pins))
# structural compare: claim ids
base_ids = set(items.keys())
reg_ids = set(reg_pins.keys())
print("claim id sets equal:", base_ids == reg_ids)
if base_ids != reg_ids:
    print("  only in BASE:", sorted(base_ids - reg_ids)[:5])
    print("  only in REG:", sorted(reg_ids - base_ids)[:5])
# compare a sample entry shape
sample = list(items.items())[0]
print("BASE PINS sample entry:", sample[0], "=>", sample[1])
# registry entry for same
print("REG entry:", reg_pins[sample[0]])
# on-disk new c1_pin_ledger PINS
newsrc = open(os.path.join(PKG, "03_SCRIPTS", "c1_pin_ledger.py"), encoding="utf-8-sig").read()
ntree = ast.parse(newsrc)
npins = None
for node in ast.walk(ntree):
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name) and t.id == "PINS":
                npins = ast.literal_eval(node.value)
print("on-disk NEW PINS identical to BASE PINS:", npins == pins_ast)

print()
print("=== G. Independent forbidden-phrase sweep ===")
forbidden = ["ASSIGNED_OBJECT_VTABLE = NONE", "NON-POLYMORPHIC", "non-polymorphic",
             "vtable_store_found", "all methods direct-called", "0xA4 bytes (280)",
             'declared_families\\": 10', "declared_families = 10",
             "re-derives every C1-JSON pin field", "re-derived field-by-field",
             "promotion-safe", "safe for promotion", "underclaim-only",
             "H2_GROUP_OPCODES = CORRECTED_FAIL_CLOSED_VALIDITY",
             "the repair is COMPLETE for the three P2 + H1 + H2",
             "No defect was found that could not be fixed",
             "for every pin where semantically applicable",
             "complete H2 closure", "complete Q2 JSON closure",
             "unrestricted dependent reuse", "no remaining blocker"]
for sf in ("FINAL_REPORT.md", "HANDOFF.md", "INPUT_IDENTITIES.md",
           "SUPERSESSION_LEDGER.md", "QC_REPORT.md"):
    content = open(os.path.join(PKG, sf), encoding="utf-8").read()
    hits = []
    for ph in forbidden:
        for m in re.finditer(re.escape(ph), content):
            line_start = content.rfind("\n", 0, m.start())
            line = content[line_start:m.end()]
            if sf == "SUPERSESSION_LEDGER.md" and ("ORIGINAL_EXCERPT" in line or "DEFECT" in line
                                                   or "historical" in line.lower()):
                continue
            hits.append((ph, m.start()))
    print(sf, "-> real hits:", hits)
