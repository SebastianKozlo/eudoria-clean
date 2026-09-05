#!/usr/bin/env python3
# -*- coding: ascii -*-
# compose_registry_v4_1.py - W1 of PE_M1_GATE_V4_1_REGISTRY_RESIDUAL_R1_20260905_110528:
# compose the registry fields for BOTH entries (P-RNG-DIV, P-POS-SCALE) per the
# iter035 byte locks - in the V4 md AND json. Fail-loud: verifies the current
# live SHAs == the pre-edit pins BEFORE touching anything; verifies the edit is
# BOUNDED (only the two registry entries in the JSON; only the two registry
# lines in the MD); verifies the exact round-trip format (indent=1, CRLF,
# trailing newline).
#
# Composition contract (PE-MASTER ORDERED_WORK item 2, verbatim field texts):
#   missing (P-RNG-DIV)   : "NONE for the divisor (byte-locked 32767.0 f64 @0x00A7D7A8, iter035; the historical open-item record follows)"
#   missing (P-POS-SCALE) : "NONE for the divisor (byte-locked 65535.0 f64 @0x00A8C758, iter035; the historical open-item record follows)"
#   why (both, ONE mandated text, quoted-hypothesis disproof):
#         "the pre-iter035 hypothesis 'reads 0.0 statically (runtime-initialized)' was DISPROVEN by the byte lock - the slot is file-backed .rdata (bytes 00 00 00 00 C0 FF DF 40 [32767.0 f64]; 65535.0: 00 00 00 00 E0 FF EF 40)"
#   resume_path (both)    : "NONE for the divisor; runtime tracing remains relevant only to the actual-CW question"
#   Every composed field labeled "composed in V4.1".
# WHY THE TYPED RECORDS: the mandated why text quotes the retired hypothesis
# verbatim ("reads 0.0 statically (runtime-initialized)") - a phrase the V4.1
# semantic gate forbids in LIVE fields and permits ONLY in records explicitly
# typed as retraction/supersession (NEXT_PROMPT W2(b)). The why field therefore
# IS a typed SUPERSESSION record carrying the mandated statement verbatim, and
# the old open-item triple is kept as a typed RETRACTION record (the mandated
# "historical open-item record" - typed historical context, NOT live status).
# The live MD layer renders the composed fields WITHOUT the retired wording
# (the R2-established architecture: retired wordings live ONLY in typed JSON
# records; the MD stays clean).
import copy
import hashlib
import json
import os
import sys

RUN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(RUN_ROOT, "01_RAW")
REPO_GATE = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE"
V4_JSON = os.path.join(REPO_GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V4.json")
V4_MD = os.path.join(REPO_GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V4.md")

PIN_V4_JSON = "11FB16B0A175CE183F5C46E734737921DBA0BA72CD975C447CF197C2046F9C58"
PIN_V4_MD = "5B90D2C43B3B0D9E5D9CBB05A387557862A61647D1A29F437F6F18416A744ACD"

LABEL = "composed in V4.1"
WHY_STATEMENT = (LABEL + ": the pre-iter035 hypothesis 'reads 0.0 statically (runtime-initialized)'"
                 " was DISPROVEN by the byte lock - the slot is file-backed .rdata"
                 " (bytes 00 00 00 00 C0 FF DF 40 [32767.0 f64]; 65535.0: 00 00 00 00 E0 FF EF 40)")
RESUME = LABEL + ": NONE for the divisor; runtime tracing remains relevant only to the actual-CW question"
MD_WHY_RENDERING = (LABEL + ": the pre-iter035 runtime-zero-initialization hypothesis was DISPROVEN by"
                    " the byte lock - the slot is file-backed .rdata (bytes 00 00 00 00 C0 FF DF 40"
                    " [32767.0 f64]; 65535.0: 00 00 00 00 E0 FF EF 40) - the retired hypothesis wording"
                    " is carried ONLY by the typed SUPERSESSION record (the why field) in the V4.1 JSON,"
                    " and the historical open-item record (the old missing/why/resume) ONLY by the typed"
                    " RETRACTION record in the V4.1 JSON (both = historical context, NOT live status;"
                    " this live MD layer carries none of it)")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def dump_exact(doc):
    """the exact on-disk format: json.dumps(indent=1) + CRLF + trailing newline."""
    return (json.dumps(doc, indent=1, ensure_ascii=True) + "\n").replace("\n", "\r\n").encode("ascii")


def composed_entry(old):
    """compose one registry entry per the byte-locks; era_statement + v4_status UNTOUCHED."""
    ph = old["placeholder"]
    if ph.startswith("P-RNG-DIV"):
        missing = LABEL + ": NONE for the divisor (byte-locked 32767.0 f64 @0x00A7D7A8, iter035; the historical open-item record follows)"
        supersedes = "_DAT_00a7d7a8 reads 0.0 statically (runtime-initialized)"
        sources = ("the iter035 byte locks (CONSTANT_ADDRESS_LOCK + PE_SECTION_MAP; _DAT_00a7d7a8, FDIV QWORD @0x0098CE5A)"
                   " + the PE-MASTER R2 post-audit re-read of the pinned Entropia.exe bytes")
        hist = {"record_type": "RETRACTION (explicitly typed; the historical open-item record kept as historical context, NOT live status)",
                "missing": "the exact RNG normalization divisor",
                "why": "_DAT_00a7d7a8 reads 0.0 statically (runtime-initialized)",
                "resume_path": "runtime tracing (separate authorization)"}
    elif ph.startswith("P-POS-SCALE"):
        missing = LABEL + ": NONE for the divisor (byte-locked 65535.0 f64 @0x00A8C758, iter035; the historical open-item record follows)"
        supersedes = "_DAT_00a8c758 reads 0.0 statically (runtime-initialized)"
        sources = ("the iter035 byte locks (CONSTANT_ADDRESS_LOCK + PE_SECTION_MAP; _DAT_00a8c758, FLD QWORD @0x0095B2BC)"
                   " + the PE-MASTER R2 post-audit re-read of the pinned Entropia.exe bytes")
        hist = {"record_type": "RETRACTION (explicitly typed; the historical open-item record kept as historical context, NOT live status)",
                "missing": "the u16->world position divisor",
                "why": "_DAT_00a8c758 reads 0.0 statically (runtime-initialized)",
                "resume_path": "runtime tracing"}
    else:
        raise SystemExit("compose_registry_v4_1: unexpected placeholder %r" % ph)
    why = {"record_type": "SUPERSESSION (explicitly typed; " + LABEL + "; the only permitted carrier of the retired hypothesis wording)",
           "composed_in": "V4.1",
           "statement": WHY_STATEMENT,
           "supersedes": supersedes,
           "sources": sources}
    return {"placeholder": ph,
            "missing": missing,
            "why": why,
            "resume_path": RESUME,
            "historical_open_item_record": hist,
            "era_statement": old["era_statement"],
            "v4_status": old["v4_status"]}


def main():
    # fail-loud preconditions: the current live SHAs == the pre-edit pins
    sha_json, sha_md = sha256_file(V4_JSON), sha256_file(V4_MD)
    if sha_json != PIN_V4_JSON:
        raise SystemExit("HARD STOP: V4 json pre-edit SHA mismatch (%s)" % sha_json)
    if sha_md != PIN_V4_MD:
        raise SystemExit("HARD STOP: V4 md pre-edit SHA mismatch (%s)" % sha_md)

    # ---- the JSON composition
    with open(V4_JSON, "r", encoding="ascii", newline="") as f:
        original_doc = json.load(f)
    original_bytes = open(V4_JSON, "rb").read()
    if dump_exact(original_doc) != original_bytes:
        raise SystemExit("HARD STOP: the V4 json round-trip format is not exact - refusing to edit")
    new_doc = copy.deepcopy(original_doc)
    reg = new_doc["era_bounded_registry_v4"]
    old_entries = {}
    for idx in (11, 13):
        old_entries[idx] = reg[idx]
        reg[idx] = composed_entry(reg[idx])
    new_bytes = dump_exact(new_doc)
    # bounded-diff proof: line-by-line, the changes confined to the two entries
    old_lines = original_bytes.split(b"\r\n")
    new_lines = new_bytes.split(b"\r\n")
    if len(old_lines) != len(new_lines):
        # the composed entries add lines (the typed records); verify the structural containment instead
        pass
    # verify byte-identity of everything OUTSIDE the two entries:
    old_reg = original_doc["era_bounded_registry_v4"]
    new_reg_others = [e for i, e in enumerate(new_doc["era_bounded_registry_v4"]) if i not in (11, 13)]
    old_others = [e for i, e in enumerate(old_reg) if i not in (11, 13)]
    if json.dumps(old_others, sort_keys=True) != json.dumps(new_reg_others, sort_keys=True):
        raise SystemExit("HARD STOP: the composition leaked outside the two registry entries")
    for k, v in original_doc.items():
        if k == "era_bounded_registry_v4":
            continue
        if json.dumps(v, sort_keys=True) != json.dumps(new_doc[k], sort_keys=True):
            raise SystemExit("HARD STOP: the composition leaked into top-level key %r" % k)
    # the 17 untouched entries + every other top-level key verified identical.
    with open(V4_JSON, "wb") as f:
        f.write(new_bytes)

    # ---- the MD composition (the two registry lines; everything else byte-identical)
    md_bytes = open(V4_MD, "rb").read()
    lines = md_bytes.split(b"\r\n")
    md_old_rng = (b"- **P-RNG-DIV (foliage_system)** - missing: the exact RNG normalization divisor | "
                  b"why: _DAT_00a7d7a8 reads 0.0 statically (runtime-initialized) | "
                  b"resume: runtime tracing (separate authorization)")
    md_old_pos = (b"- **P-POS-SCALE (foliage_system)** - missing: the u16->world position divisor | "
                  b"why: _DAT_00a8c758 reads 0.0 statically (runtime-initialized) | "
                  b"resume: runtime tracing")
    md_new_rng = ("- **P-RNG-DIV (foliage_system)** - missing: " + LABEL +
                  ": NONE for the divisor (byte-locked 32767.0 f64 @0x00A7D7A8, iter035; the historical open-item record follows)"
                  " | why: " + MD_WHY_RENDERING +
                  " | resume: " + RESUME).encode("ascii")
    md_new_pos = ("- **P-POS-SCALE (foliage_system)** - missing: " + LABEL +
                  ": NONE for the divisor (byte-locked 65535.0 f64 @0x00A8C758, iter035; the historical open-item record follows)"
                  " | why: " + MD_WHY_RENDERING +
                  " | resume: " + RESUME).encode("ascii")
    hits_rng = [i for i, ln in enumerate(lines) if ln == md_old_rng]
    hits_pos = [i for i, ln in enumerate(lines) if ln == md_old_pos]
    if len(hits_rng) != 1 or len(hits_pos) != 1:
        raise SystemExit("HARD STOP: the MD registry lines were not found exactly once (%r / %r)" % (hits_rng, hits_pos))
    lines[hits_rng[0]] = md_new_rng
    lines[hits_pos[0]] = md_new_pos
    new_md_bytes = b"\r\n".join(lines)
    # bounded-diff proof: exactly 2 lines differ
    diff_count = sum(1 for a, b in zip(md_bytes.split(b"\r\n"), new_md_bytes.split(b"\r\n")) if a != b)
    if diff_count != 2 or len(md_bytes.split(b"\r\n")) != len(new_md_bytes.split(b"\r\n")):
        raise SystemExit("HARD STOP: the MD diff is not exactly 2 lines (got %d)" % diff_count)
    with open(V4_MD, "wb") as f:
        f.write(new_md_bytes)

    # ---- the composition record (01_RAW)
    record = {
        "run_id": "PE_M1_GATE_V4_1_REGISTRY_RESIDUAL_R1_20260905_110528",
        "work_item": "W1 - compose the registry fields for P-RNG-DIV + P-POS-SCALE per the iter035 byte locks",
        "sources": "the iter035 byte locks (CONSTANT_ADDRESS_LOCK + PE_SECTION_MAP) + the historical open-item record (kept as the typed historical context, NOT live status) - zero new forensics",
        "pre_edit_shas": {"M1_GATE_DELIVERABLE_MATRIX_V4.json": sha_json, "M1_GATE_DELIVERABLE_MATRIX_V4.md": sha_md},
        "post_edit_shas": {"M1_GATE_DELIVERABLE_MATRIX_V4.json": sha256_file(V4_JSON),
                           "M1_GATE_DELIVERABLE_MATRIX_V4.md": sha256_file(V4_MD)},
        "composed_fields": {
            "P-RNG-DIV": {"missing": reg[11]["missing"], "why": reg[11]["why"], "resume_path": reg[11]["resume_path"],
                          "historical_open_item_record": reg[11]["historical_open_item_record"]},
            "P-POS-SCALE": {"missing": reg[13]["missing"], "why": reg[13]["why"], "resume_path": reg[13]["resume_path"],
                            "historical_open_item_record": reg[13]["historical_open_item_record"]},
        },
        "bounded_diff_proof": {
            "json": "the 17 other registry entries + every other top-level key verified IDENTICAL (content-equal dump comparison); the only change = the two composed entries",
            "md": "exactly 2 lines differ (the P-RNG-DIV + P-POS-SCALE registry lines); line count unchanged",
        },
        "typed_record_design": ("the mandated why text quotes the retired hypothesis verbatim; the V4.1 gate permits that phrase ONLY in typed retraction/supersession records, so the why field IS a typed SUPERSESSION record (the mandated statement verbatim) and the old open-item triple is kept as a typed RETRACTION record (the mandated 'historical open-item record follows'); the live MD layer renders the composed fields WITHOUT the retired wording (the R2-established architecture: retired wordings live ONLY in typed JSON records)"),
        "script_sha256": sha256_file(os.path.abspath(__file__)),
    }
    with open(os.path.join(RAW, "composition_record_v4_1.json"), "w", encoding="ascii", newline="") as f:
        json.dump(record, f, indent=1)
        f.write("\n")
    print("W1 JSON : %s -> %s" % (sha_json, record["post_edit_shas"]["M1_GATE_DELIVERABLE_MATRIX_V4.json"]))
    print("W1 MD   : %s -> %s" % (sha_md, record["post_edit_shas"]["M1_GATE_DELIVERABLE_MATRIX_V4.md"]))
    print("W1 composition record -> 01_RAW\\composition_record_v4_1.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
