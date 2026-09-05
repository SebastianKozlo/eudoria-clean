# -*- coding: utf-8 -*-
"""app_content.py — annotation-file content builders for the
PE_NIF_R3_PROPOSAL_APPLICATION_R1 driver.

The 13 annotation entries embed the map's verbatim new_text payloads, the
verbatim superseded old fragments (from the hash-pinned map_defs.py), the
evidence_pointer and lineage_ref fields (from TARGET_MAP.json), and the
byte-identity hashes of the referenced historical files. All payloads are
passed in by apply_r1.py — nothing is hand-transcribed here.
"""

MAP_SHA = "D3F043F2167C1BD0EDBC9C4F7957D5FD31AF37C8296848DEEB9350DDA7699628"
FIXED_SHA = "65DC552806C2C2A1E27A7ABDB227B4CCF09A8C2A473BC6A9628655298A88DE27"


def ledger_header(run_id, ts):
    return (
        "# CORRECTION LEDGER — superseded-wording record for frozen audit artifacts\n"
        "\n"
        "> STANDING CONTRACT (file created by %s on %s; authority: the human\n"
        "> HR-R3-3 GO relayed via PE-MASTER; map: TARGET_MAP.json SHA256 %s):\n"
        "> historical/frozen audit artifacts are NEVER edited. When a review\n"
        "> supersedes wording inside such an artifact, the supersession is recorded\n"
        "> HERE as a new entry: the historical file stays byte-identical (SHA256\n"
        "> re-hashed before and after the recording run, both trees: the local\n"
        "> 99_Audits tree and the repo mirror), the entry quotes the superseded\n"
        "> wording verbatim with its location, and carries the corrected wording\n"
        "> (verbatim), the evidence pointer and the lineage reference.\n"
        "> Operation kind: LEDGER-ENTRY (TARGET_MAP.json operations_legend:\n"
        "> \"historical file preserved byte-identical; entry records superseded\n"
        "> wording\"). APPEND-ONLY: existing entries are never modified or deleted;\n"
        "> authorized application runs append below the last entry. A repo/local\n"
        "> byte-identical pair is maintained (SYNC hashes recorded per run).\n"
        "\n---\n"
        % (run_id, ts, MAP_SHA))


def rules_header(run_id, ts):
    return (
        "# STANDING RULES — audit-methodology rules adopted by proposal application\n"
        "\n"
        "> STANDING CONTRACT (file created by %s on %s; authority: the human\n"
        "> HR-R3-3 GO relayed via PE-MASTER; map: TARGET_MAP.json SHA256 %s):\n"
        "> this file carries STANDING-RULE texts (TARGET_MAP.json operations_legend:\n"
        "> \"new standing text; no superseded file wording\") adopted via authorized\n"
        "> proposal application. Each entry embeds the rule text VERBATIM (the map's\n"
        "> new_text payload), its evidence pointer and lineage reference.\n"
        "> APPEND-ONLY: existing rules are never modified or deleted; authorized\n"
        "> runs append below the last entry. A repo/local byte-identical pair is\n"
        "> maintained (SYNC hashes recorded per run).\n"
        "\n---\n"
        % (run_id, ts, MAP_SHA))


def policies_header(run_id, ts):
    return (
        "# STANDING POLICIES — acceptance/policy guards adopted by proposal application\n"
        "\n"
        "> STANDING CONTRACT (file created by %s on %s; authority: the human\n"
        "> HR-R3-3 GO relayed via PE-MASTER; map: TARGET_MAP.json SHA256 %s):\n"
        "> this file carries STANDING-POLICY texts (TARGET_MAP.json\n"
        "> operations_legend: \"acceptance/policy guard; anchor fragment verifies\n"
        "> the referenced historical wording\"). Where an entry references historical\n"
        "> wording, the anchor fragment is verified READ-ONLY (present exactly-once\n"
        "> at the recorded location in the hash-stable historical file). Each entry\n"
        "> embeds the policy text VERBATIM (the map's new_text payload), its\n"
        "> evidence pointer and lineage reference. APPEND-ONLY: existing policies\n"
        "> are never modified or deleted; authorized runs append below the last\n"
        "> entry. A repo/local byte-identical pair is maintained (SYNC hashes\n"
        "> recorded per run).\n"
        "\n---\n"
        % (run_id, ts, MAP_SHA))


def _claims_str(claims):
    return ", ".join(claims) if isinstance(claims, list) else str(claims)


def render_entry(eid, kind, title, claims, new_text, old_frag, old_span,
                 evidence, lineage, new_text_source, hist_rel,
                 hist_sha_before, hist_sha_after, trees_equal, run_id,
                 extra_lines=None):
    """Render ONE annotation entry (markdown). Payloads embedded verbatim."""
    b = []
    b.append("## Entry %s — %s\n" % (eid, title))
    b.append("- operation: %s" % kind)
    b.append("- applied_by: %s (authority: HR-R3-3 GO relayed via PE-MASTER;"
             " TARGET_MAP.json SHA256 %s, edit %s)" % (run_id, MAP_SHA, eid))
    b.append("- claims: %s" % _claims_str(claims))
    if hist_rel is not None:
        b.append("- historical file (NOT edited; byte-identical before == after"
                 " this run): 99_Audits\\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054\\%s"
                 % hist_rel)
        b.append("- repo mirror (NOT edited): docs/audits/"
                 "PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054/%s"
                 % hist_rel.replace("\\", "/"))
        b.append("- historical file SHA256 before == after: %s (repo mirror SHA256"
                 " EQUAL: %s)" % (hist_sha_before, trees_equal))
    if old_frag is not None:
        if kind == "STANDING-POLICY":
            label = (("referenced historical wording (anchor; verified"
                      " read-only at lines %d-%d of the historical file)"
                      % old_span) if old_span else
                     "referenced historical wording (anchor; verified read-only)")
        else:
            label = (("superseded wording (verbatim; at lines %d-%d of the"
                      " historical file)" % old_span) if old_span else
                     "superseded wording (verbatim)")
        b.append("- %s:\n" % label)
        b.append(old_frag)
        b.append("")
    b.append("- %s (TARGET_MAP.json new_text, verbatim):\n"
             % ("corrected wording" if kind == "LEDGER-ENTRY" else
                ("standing text" if kind == "STANDING-RULE" else
                 ("standing policy text" if old_frag is None
                  else "standing policy text")))) 
    b.append(new_text)
    b.append("")
    b.append("- evidence_pointer: %s" % evidence)
    b.append("- lineage_ref: %s" % lineage)
    b.append("- new_text_source: %s" % new_text_source)
    if kind == "STANDING-POLICY" and old_frag is not None:
        b.append("- anchor verification (this run): the anchor fragment above was"
                 " verified READ-ONLY — present EXACTLY-ONCE at the recorded"
                 " location in the historical file whose SHA256 was re-hashed"
                 " before and after this run (%s == %s; both trees EQUAL: %s)"
                 % (hist_sha_before, hist_sha_after, trees_equal))
    if extra_lines:
        b.extend(extra_lines)
    b.append("\n---\n")
    return "\n".join(b) + "\n"
