# RUN-B RE-VERIFICATION: extract the 3 docs/nif REPLACE new_texts from TARGET_MAP.json
# and count each FULL text in its live target file (expect 3x found, each exactly 1x).
import sys, io, json, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

TM = "docs/audits/PE_NIF_R3_PERSISTENCE_AND_TARGETMAP_R1_20260905_101203/05_ANALYSIS/TARGET_MAP.json"
with open(TM, "rb") as f:
    tm_bytes = f.read()
print("TARGET_MAP.json sha256 =", hashlib.sha256(tm_bytes).hexdigest().upper())
tm = json.loads(tm_bytes.decode("utf-8"))

# The docs/nif REPLACE edits (operation REPLACE + target_file under docs/nif)
replaces = []
for prop in tm["proposals"]:
    for ed in prop["edits"]:
        if ed["operation"] == "REPLACE" and isinstance(prop.get("target_file"), str) and prop["target_file"].startswith("docs/nif"):
            replaces.append((prop["proposal_id"], ed["edit_id"], prop["target_file"], ed["new_text"]))

print(f"docs/nif REPLACE edits in TARGET_MAP = {len(replaces)}")
ok = 0
for pid, eid, tf, new_text in replaces:
    with open(tf, "rb") as f:
        data = f.read()
    c = data.count(new_text.encode("utf-8"))
    status = "FOUND(1x)" if c == 1 else f"NOT-1x({c}x)"
    if c == 1: ok += 1
    print(f"  {pid}/{eid} -> {tf}: full new_text count={c} {status}")

print(f"RESULT: {ok}/{len(replaces)} found" if replaces else "RESULT: no docs/nif REPLACE edits found")
sys.exit(0 if ok == len(replaces) and ok == 3 else 2)
