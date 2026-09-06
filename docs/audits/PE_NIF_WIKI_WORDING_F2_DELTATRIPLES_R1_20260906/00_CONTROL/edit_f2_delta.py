# Byte-safe exactly-once anchor replacement for RUN PE_NIF_WIKI_WORDING_F2_DELTATRIPLES_R1_20260906
# Reads files as BYTES, UTF-8-encodes fragments, enforces exactly-once old anchor,
# replaces, verifies 0x old / 1x new, writes bytes back. No fuzzy matching.
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

EDITS = [
    ("docs/nif/02-block-registry.md",
     "## Full registry (77 types observed in 9.3.5; counts = 9.3.5 / 2003 where known)",
     "## Full registry (76 types observed in 9.3.5; counts = 9.3.5 / 2003 where known)"),
    ("docs/nif/10-containers-corpus.md",
     "(5596/5596 PASS, block census 77 types)",
     "(5596/5596 PASS, block census 76 types)"),
    ("docs/nif/09-semantics.md",
     "[9 \u00d7 f32 delta triples]",
     "[9 \u00d7 f32 trailing values \u2014 grouping into triples is an OPEN HYPOTHESIS, not an established structure (see the uniform-block wording above)]"),
]

results = []
fail = False
for path, old, new in EDITS:
    with open(path, "rb") as f:
        data = f.read()
    ob = old.encode("utf-8")
    nb = new.encode("utf-8")
    n_old = data.count(ob)
    print(f"ANCHOR {path}")
    print(f"  old_occurrences={n_old} old_hex_len={len(ob)}")
    if n_old != 1:
        print("  RESULT=ANCHOR_NOT_UNIQUE -> HARD STOP, no write for this file")
        fail = True
        results.append((path, "ANCHOR_NOT_UNIQUE", n_old))
        continue
    data2 = data.replace(ob, nb, 1)
    n_old_after = data2.count(ob)
    n_new_after = data2.count(nb)
    if n_old_after != 0 or n_new_after != 1:
        print(f"  post-replace check FAILED old={n_old_after} new={n_new_after}")
        fail = True
        results.append((path, "POSTCHECK_FAIL", (n_old_after, n_new_after)))
        continue
    with open(path, "wb") as f:
        f.write(data2)
    print(f"  RESULT=APPLIED new_occurrences={n_new_after} old_occurrences_after=0")
    results.append((path, "APPLIED", 1))

print("SUMMARY:", "ALL_APPLIED" if not fail else "HARD_STOP")
for r in results:
    print(" ", r)
sys.exit(0 if not fail else 2)
