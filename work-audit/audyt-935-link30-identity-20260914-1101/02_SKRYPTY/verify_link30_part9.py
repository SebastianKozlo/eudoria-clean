# WORK-AUDIT part9: own forbidden-label census over FULL package + UTF-8 validity + loop-state search
import os, sys
PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914"
def rep(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(detail) if detail else ""))
NEG = ("NOT_DEMONSTRATED", "not made", "no ", "NOT ", "not ", "remains", "zero", "Zero", "forbidden", "FORBIDDEN", "negative", "claim-context", "FORBIDDEN_CLAIMS", "sanctioned", "census", "detector")
hits = []
claim_ctx = []
for root, dirs, files in os.walk(PKG):
    for f in files:
        p = os.path.join(root, f)
        rel = os.path.relpath(p, PKG)
        if p.endswith((".md", ".txt", ".csv", ".json", ".py")):
            try:
                t = open(p, encoding="utf-8", errors="replace").read()
            except Exception:
                continue
            for ln, line in enumerate(t.splitlines(), 1):
                if "MODEL_BRIDGE_CONFIRMED" in line or "TRANSFORM_TO_MODEL" in line:
                    has_neg = any(m in line for m in NEG)
                    hits.append((rel, ln, has_neg, line.strip()[:100]))
                    if not has_neg:
                        claim_ctx.append((rel, ln, line.strip()[:160]))
print("total label occurrences (full 33-file package incl. qc/REVIEW):", len(hits))
print("claim-context (no negative/machinery marker):", len(claim_ctx))
for c in claim_ctx:
    print("  CLAIM?:", c)
rep("K1 zero claim-context forbidden labels in FULL package", len(claim_ctx) == 0)
# UTF-8 validity of the 4 regenerated evidence files
bad_utf = []
for rel in ("02_ANALYSIS/SF30_PROVENANCE.md", "01_RAW/POSITIVE_CONTROL_0050A050.txt",
            "01_RAW/SF30_WRITER_RAW.txt", "01_RAW/SF30_RTTI_RAW.txt"):
    p = os.path.join(PKG, rel.replace("/", os.sep))
    try:
        open(p, encoding="utf-8").read()
    except UnicodeDecodeError as ex:
        bad_utf.append((rel, str(ex)))
rep("K2 the 4 regenerated evidence files are valid UTF-8", not bad_utf, bad_utf)
# UTF-8 BOM check (REPORT/HANDOFF docs)
import codecs
for rel in ("06_REPORT/REPORT.md", "06_REPORT/HANDOFF.md"):
    p = os.path.join(PKG, rel.replace("/", os.sep))
    raw = open(p, "rb").read(4)
    print("   BOM", rel, ":", raw[:3].hex())
