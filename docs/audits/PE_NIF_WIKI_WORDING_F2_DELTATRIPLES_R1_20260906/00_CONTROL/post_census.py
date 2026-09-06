# Post-edit census: forbidden phrases over ALL docs/nif/**, RUN-B applied-text assertions,
# collateral hash census (all 15 files before==after for non-targets).
import sys, io, hashlib, os, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = "docs/nif"
files = []
for dirpath, _, names in os.walk(ROOT):
    for n in sorted(names):
        files.append(os.path.join(dirpath, n))
files.sort()
print(f"TOTAL_FILES_UNDER_docs/nif = {len(files)}")

FORBIDDEN = ["77 types", "77 distinct block types", "delta triples"]
print("\n=== FORBIDDEN-PHRASE CENSUS (all docs/nif/**, byte-exact) ===")
fp_fail = False
for phrase in FORBIDDEN:
    pb = phrase.encode("utf-8")
    total = 0
    per_file = {}
    for p in files:
        with open(p, "rb") as f:
            c = f.read().count(pb)
        if c:
            per_file[p] = c
            total += c
    status = "PASS(0)" if total == 0 else f"FAIL({total})"
    if total: fp_fail = True
    print(f"  [{phrase}] hits={total} {status} {('in ' + str(per_file)) if per_file else ''}")

print("\n=== RUN-B APPLIED-TEXT ASSERTIONS (each must be exactly 1x) ===")
def count_in(path, s):
    with open(path, "rb") as f:
        return f.read().count(s.encode("utf-8"))

RUNB = [
    ("docs/nif/09-semantics.md", "9 \u00d7 f32 trailing values; grouping and semantic role UNVERIFIED"),
    ("docs/nif/09-semantics.md", "334 classifier-real spans do not fit the tested VARIABLE-K model"),
    ("docs/nif/10-containers-corpus.md", "every validator at 100%"),
]
rb_fail = False
for path, s in RUNB:
    c = count_in(path, s)
    status = "PASS(1x)" if c == 1 else f"FAIL({c}x)"
    if c != 1: rb_fail = True
    print(f"  {path} :: [{s[:60]}...] count={c} {status}")

print("\n=== NEW-FRAGMENT EXACTLY-ONCE RE-ASSERT ===")
NEWF = [
    ("docs/nif/02-block-registry.md", "## Full registry (76 types observed in 9.3.5; counts = 9.3.5 / 2003 where known)"),
    ("docs/nif/10-containers-corpus.md", "(5596/5596 PASS, block census 76 types)"),
    ("docs/nif/09-semantics.md", "[9 \u00d7 f32 trailing values \u2014 grouping into triples is an OPEN HYPOTHESIS, not an established structure (see the uniform-block wording above)]"),
]
for path, s in NEWF:
    c = count_in(path, s)
    print(f"  {path} new-anchor count={c} {'PASS(1x)' if c==1 else 'FAIL'}")

print("\n=== COLLATERAL HASH CENSUS (post-edit, all docs/nif/**) ===")
for p in files:
    with open(p, "rb") as f:
        h = hashlib.sha256(f.read()).hexdigest()
    print(f"  {h}  {p}")

print(f"\nOVERALL: forbidden={'FAIL' if fp_fail else 'PASS'} runb_assert={'FAIL' if rb_fail else 'PASS'}")
sys.exit(0 if (not fp_fail and not rb_fail) else 2)
