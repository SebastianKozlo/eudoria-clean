#!/usr/bin/env python3
# QC-R3 Q5: wording + dependency sweep of the CURRENT (post-correction) package state
# against correction-contract §5/§7 wording requirements and the high-risk-word audit.
import json, os, re

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002"
QC_DIR = os.path.join(PKG, "04_QC", "QC_R3_DESKTOP_CORRECTION")

CORRECTED_DOCS = [
    "06_REPORT/REPORT.md", "06_REPORT/EVIDENCE_INDEX.md", "06_REPORT/HANDOFF.md",
    "02_ANALYSIS/FIELD_TO_DESTINATION_TRACE.md", "02_ANALYSIS/CONSUMER_TRACE.md",
    "02_ANALYSIS/SEMANTIC_ASSESSMENT.md", "02_ANALYSIS/NEGATIVE_CONTROLS.md",
    "02_ANALYSIS/BLAST_RADIUS.md", "02_ANALYSIS/VFS_TO_PARSER_TRACE.md",
    "02_ANALYSIS/DESTINATION_CONSUMER_CENSUS.json",
]

res = {"q": "Q5_wording_sweep", "status_checks": {}, "forbidden_phrases": {},
       "conventions": {}, "report_s18_keys": {}, "counts": {}, "high_risk_words": {},
       "manifest_stale_statement": None, "historical_sections": {}}

def load(rel):
    p = os.path.join(PKG, *rel.split("/"))
    with open(p, "r", encoding="utf-8-sig") as f:
        return f.read()

docs = {rel: load(rel) for rel in CORRECTED_DOCS}

# ---------- 1. mandated statuses in the current state ----------
status_checks = {}
for rel, txt in docs.items():
    checks = {}
    for key, val in [("RUN_STATUS", "CONSUMER_UNREACHED"),
                     ("DEST_FIELD_IDENTIFIED", "YES"),
                     ("DOWNSTREAM_CONSUMER_IDENTIFIED", "NO"),
                     ("FINAL_SEMANTIC_STATUS", "UNVERIFIED"),
                     ("WORLD_INSTANCE_TO_MODEL_EDGE", "NOT_TESTED"),
                     ("PLACEMENT_XYZ_RECOVERED", "NO")]:
        pat = re.compile(re.escape(key) + r"\s*=\s*(\S+)")
        m = pat.search(txt)
        if m:
            checks[key] = {"found": m.group(1), "ok": m.group(1).startswith(val)}
        else:
            checks[key] = {"found": None, "ok": None, "note": "key not present (not required in every doc)"}
    # the bounded §5 wording (exact or equivalent) present?
    bounded = ("202 direct descriptor-lookup sites" in txt and
               ("no tag-ID-17 downstream reader was identified" in txt or
                "no tag-0x11 reader was identified" in txt or
                "no statically-coded tag-0x11 reader was identified" in txt))
    checks["bounded_wording_present"] = {"found": bounded}
    # any CONTRADICTORY (old) status in the current text NOT labeled historical/superseded?
    bad_status = []
    for m in re.finditer(r"RUN_STATUS\s*=\s*(\S+)", txt):
        if not m.group(1).startswith("CONSUMER_UNREACHED"):
            # check the surrounding 200 chars for a historical/superseded label
            ctx = txt[max(0, m.start()-260):m.end()+260]
            labeled = any(w in ctx.lower() for w in ["superseded", "historical", "superse"])
            bad_status.append({"at": m.group(0), "labeled_historical_or_superseded": labeled})
    checks["run_status_noncurrent_mentions"] = bad_status
    status_checks[rel] = checks
res["status_checks"] = status_checks

# ---------- 2. forbidden over-broad phrase forms in the CURRENT corrected docs ----------
# (HANDOFF carries an explicitly-labeled historical section; occurrences INSIDE that
#  section are classified historical, not current.)
forbidden = {
    "no_static_reader_exists": [
        r"no\s+static\s+reader\s+exists",
        r"no\s+statically[- ]coded\s+tag[- ]0x11\s+reader\s+exists",
        r"no\s+static\s+tag[- ]0x11\s+reader\s+exists",
    ],
    "reads_are_runtime_tag_driven": [
        r"reads\s+are\s+runtime[- ]tag[- ]driven",
        r"the\s+read\s+side\s+is\s+runtime[- ]tag[- ]driven",
    ],
    "static_only_cannot_close": [r"static[- ]only\s+cannot\s+close"],
    "runtime_is_required": [r"runtime\s+is\s+required"],
}
def handoff_historical_span(txt):
    i = txt.find("ORIGINAL DELIVERY NOTICE (historical")
    return (i, len(txt)) if i >= 0 else None

forbidden_hits = {}
for rel, txt in docs.items():
    hist_span = handoff_historical_span(txt) if rel == "06_REPORT/HANDOFF.md" else None
    hits = []
    for cls, pats in forbidden.items():
        for pat in pats:
            for m in re.finditer(pat, txt, re.I):
                in_hist = bool(hist_span and hist_span[0] <= m.start() < hist_span[1])
                # labeled historical in surrounding context?
                ctx = txt[max(0, m.start()-300):m.end()+300]
                labeled = "historical" in ctx.lower() or "superseded" in ctx.lower() or "delivery-time" in ctx.lower()
                hits.append({"class": cls, "phrase": m.group(0), "offset": m.start(),
                             "in_explicitly_labeled_historical_section": in_hist or labeled,
                             "context": txt[max(0, m.start()-120):m.end()+160].replace("\n", " ")})
    forbidden_hits[rel] = hits
res["forbidden_phrases"] = forbidden_hits

# ---------- 3. conventions ----------
conv = {}
# "tag ID 17" usage vs "17th property/descriptor" in current state
for rel, txt in docs.items():
    hist_span = handoff_historical_span(txt) if rel == "06_REPORT/HANDOFF.md" else None
    cur = txt if not hist_span else txt[:hist_span[0]]
    ordinal_hits = [m.group(0) for m in re.finditer(r"17th\s+(property|descriptor)", cur, re.I)]
    conv[rel] = {"tag_id_17_count_cur": len(re.findall(r"tag\s+ID\s+17", cur)),
                 "ordinal_17th_in_current_section": ordinal_hits}
res["conventions"] = conv

# one-caller scoping
one_caller = {}
for rel, txt in docs.items():
    hits = []
    for m in re.finditer(r"ONE_DIRECT_CALLER_FOUND|exactly\s+1\s+caller|exactly one caller", txt):
        ctx = txt[max(0, m.start()-200):m.end()+260]
        scoped = ("censused machinery" in ctx) or ("NOT global" in ctx) or ("within the censused" in ctx)
        hits.append({"match": m.group(0), "properly_scoped": scoped})
    one_caller[rel] = hits
res["one_caller_scoping"] = one_caller

# ---------- 4. REPORT.md §18 key census ----------
report = docs["06_REPORT/REPORT.md"]
s18_keys = ["RUN_ID", "BASE_HEAD", "STATIC_ONLY", "RUNTIME_EXECUTION_PERFORMED",
            "EXE_IDENTITY_MATCH", "VFS_IDENTITY_MATCH", "SOURCE_SHA256",
            "RECORD_ORDINAL_OR_PHYSICAL_ID", "RECORD_FRAME_START", "RECORD_PAYLOAD_START",
            "RECORD_PAYLOAD_LENGTH", "FIELD_FILE_OFFSET", "PAYLOAD_PLUS_30_RAW_BYTES",
            "PAYLOAD_PLUS_30_DECODED_VALUE", "20002_VFS_TO_PARSER_ROUTING",
            "CLIENT_READ_IDENTIFIED", "READ_FUNCTION", "READ_INSTRUCTION_VA",
            "READ_INSTRUCTION_RVA", "READ_INSTRUCTION_FILE_OFFSET",
            "DEST_FIELD_IDENTIFIED", "DEST_STRUCTURE", "DEST_FIELD_OFFSET",
            "DOWNSTREAM_CONSUMER_IDENTIFIED", "OBSERVED_OPERATION",
            "STATIC_READ_SEARCH_SCOPE", "STATIC_WRITE_SEARCH_SCOPE",
            "UNRESOLVED_ALIASES", "UNRESOLVED_INDIRECT_CALLS", "UNINSPECTED_PATHS",
            "FIELD_IDENTITY_STATUS", "FINAL_SEMANTIC_ROLE", "FINAL_SEMANTIC_STATUS",
            "WORLD_INSTANCE_TO_MODEL_EDGE", "PLACEMENT_XYZ_RECOVERED",
            "NEGATIVE_CONTROL_STATUS", "INDEPENDENT_QC", "RUN_STATUS",
            "Q1_STATUS_CHANGED", "PE_MASTER_QUALIFICATION_CHANGED", "GATE_B_CHANGED",
            "M1_CHANGED", "M2_CHANGED", "M3_CHANGED", "COMMIT", "PUSH"]
missing = [k for k in s18_keys if not re.search(r"(?m)^\s*" + re.escape(k) + r"\s*=", report)]
res["report_s18_keys"] = {"required_keys": len(s18_keys), "present": len(s18_keys) - len(missing),
                          "missing": missing}
# corrected §18 chain values
res["report_s18_key_values"] = {
    "READ_FUNCTION": ("FUN_009777F0" in report),
    "READ_INSTRUCTION_VA_0x977807": bool(re.search(r"READ_INSTRUCTION_VA\s*=\s*0x00977807", report)),
    "READ_INSTRUCTION_RVA_0x577807": bool(re.search(r"READ_INSTRUCTION_RVA\s*=\s*0x00577807", report)),
    "READ_INSTRUCTION_FILE_OFFSET_0x577807": bool(re.search(r"READ_INSTRUCTION_FILE_OFFSET\s*=\s*0x00577807", report)),
    "STORE_INSTRUCTION_VA_0x977810": bool(re.search(r"STORE_INSTRUCTION_VA\s*=\s*0x00977810", report)),
    "RUN_STATUS_CONSUMER_UNREACHED": bool(re.search(r"(?m)^RUN_STATUS\s*=\s*CONSUMER_UNREACHED", report)),
}

# ---------- 5. counts: fresh, distinguished, no stale digits ----------
counts = {}
for rel in ["06_REPORT/REPORT.md", "06_REPORT/HANDOFF.md", "06_REPORT/AMEND_LOG_DESKTOP_CORRECTION_R1.md"]:
    txt = load(rel)
    counts[rel] = {
        "mentions_420": txt.count("420"),
        "mentions_419_cur": len(re.findall(r"CURRENT count \(419\)|CURRENT count is the 419", txt)),
        "mentions_418_cur": len(re.findall(r"CURRENT count is the 418|CURRENT count \(418\)", txt)),
        "mentions_389": txt.count("389"),
        "mentions_364": txt.count("364"),
        "distinguishes_rows_vs_lines": ("388 file" in txt and ("391" in txt) and ("NOTE row" in txt)),
    }
res["counts"] = counts
# manifest-stale statement in REPORT
res["manifest_stale_statement"] = {
    "REPORT_states_manifest_stale_until_regeneration": ("stale" in report and "regenerat" in report),
    "HANDOFF_states_regenerated_LAST_by_persistence": ("regenerated LAST" in docs["06_REPORT/HANDOFF.md"]),
}

# ---------- 6. high-risk words over the corrected docs ----------
HIGH = [r"\bonly\b", r"\ball\b", r"\bnone\b", r"\bnever\b", r"\balways\b", r"\bglobal\b",
        r"\bexhaustiv\w*", r"\bunique\b", r"\bproves?\b", r"\bmust\b", r"\bevery\b",
        r"\bno\s+\w+\s+(?:reader|writer|consumer|path)s?\s+(?:exists|was identified)\b"]
hrw = {}
for rel, txt in docs.items():
    total = 0
    sample = []
    for pat in HIGH:
        for m in re.finditer(pat, txt, re.I):
            total += 1
            if len(sample) < 40:
                sample.append({"word": m.group(0), "context": txt[max(0, m.start()-60):m.end()+80].replace("\n", " ")})
    hrw[rel] = {"total_hits": total, "sample": sample}
res["high_risk_words"] = {k: v["total_hits"] for k, v in hrw.items()}
res["high_risk_words_details"] = hrw

out = os.path.join(QC_DIR, "QC_R3_WORDING_SWEEP_RESULT.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2)

# compact print
summary = {
    "s18": res["report_s18_keys"],
    "s18_values": res["report_s18_key_values"],
    "forbidden_current_hits": {rel: [h for h in hs if not h["in_explicitly_labeled_historical_section"]]
                               for rel, hs in forbidden_hits.items()},
    "forbidden_hist_hits_count": sum(len([h for h in hs if h["in_explicitly_labeled_historical_section"]])
                                     for hs in forbidden_hits.values()),
    "ordinal_17th_current": {rel: v["ordinal_17th_in_current_section"] for rel, v in conv.items()
                              if v["ordinal_17th_in_current_section"]},
    "counts": counts,
    "manifest_stale": res["manifest_stale_statement"],
    "high_risk_totals": res["high_risk_words"],
}
print(json.dumps(summary, indent=2))
