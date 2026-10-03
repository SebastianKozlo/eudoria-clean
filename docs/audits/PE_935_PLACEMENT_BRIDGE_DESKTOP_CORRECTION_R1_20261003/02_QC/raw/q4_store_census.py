#!/usr/bin/env python
"""QC-F4 store census (PE-935 placement bridge desktop correction R1 targeted QC).

Independent recount of historical session tool-call census values.
Method (MY OWN, disclosed):
  - open C:/Users/User/.local/share/opencode/opencode.db READ-ONLY (URI mode=ro)
  - inspect the parts table schema
  - count, per session_id, the part rows whose data JSON has type == 'tool'
    (one part row of type 'tool' = one tool invocation; this matches the
    natural per-invocation unit of an OpenCode session store)
  - also print total part rows per session and the session title/created_at
    for identification
"""
import sqlite3
import json
import sys

DB = "file:C:/Users/User/.local/share/opencode/opencode.db?mode=ro"

SESSIONS = [
    "ses_eff63660cffeJE8ariHPxOW4KQ",   # executor (claimed 125+23=148 total)
    "ses_eff4f9ba2ffe54l7YQDmBq294P",   # fresh QC (claimed 109)
    "ses_eff40a7ffffex6TtoVQEAWrKmX",   # focused re-QC (claimed 69)
    "ses_eff335334ffekauyuLGpNeRUxP",   # persistence (claimed 55, not a census value)
    "ses_eff20857cffeai93HfqGMdWPT8",   # service restore (claimed 112, not a census value)
    "ses_eff65ce0dffehQR2H4VAoaJOIv",   # parent (info only)
]

def main():
    con = sqlite3.connect(DB, uri=True)
    cur = con.cursor()
    print("STORE = C:/Users/User/.local/share/opencode/opencode.db (mode=ro)")
    tabs = [r[0] for r in cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    print("TABLES =", tabs)
    # schema of likely tables
    for t in tabs:
        if "part" in t or "session" in t:
            cols = cur.execute("PRAGMA table_info(%s)" % t).fetchall()
            print("SCHEMA %s: %s" % (t, [(c[1], c[2]) for c in cols]))
    # session identification
    sestab = None
    for t in tabs:
        if t in ("session", "sessions"):
            sestab = t
            break
    if sestab:
        for sid in SESSIONS:
            row = cur.execute(
                "SELECT id, title, directory, parent_id, time_created FROM %s WHERE id = ?" % sestab,
                (sid,)).fetchone()
            print("SESSION %s -> %s" % (sid, row))
    # part census
    parttab = None
    for t in tabs:
        if "part" in t and "message" not in t:
            parttab = t
            break
    if parttab is None:
        parttab = "part" if "part" in tabs else None
    if parttab is None:
        print("NO PART TABLE FOUND")
        return
    print("PART_TABLE =", parttab)
    for sid in SESSIONS:
        total = cur.execute(
            "SELECT COUNT(*) FROM %s WHERE session_id = ?" % parttab,
            (sid,)).fetchone()[0]
        tool_rows = cur.execute(
            "SELECT data FROM %s WHERE session_id = ?" % parttab,
            (sid,)).fetchall()
        n_tool = 0
        n_badjson = 0
        types = {}
        for (d,) in tool_rows:
            try:
                obj = json.loads(d)
                t = obj.get("type")
                types[t] = types.get(t, 0) + 1
                if t == "tool":
                    n_tool += 1
            except Exception:
                n_badjson += 1
        print("SESSION %s: TOTAL_PARTS=%d TOOL_PARTS=%d BADJSON=%d TYPES=%s"
              % (sid, total, n_tool, n_badjson, sorted(types.items(), key=lambda x: -x[1])[:6]))
    con.close()

if __name__ == "__main__":
    main()
