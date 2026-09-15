"""gen_manifest.py — builds EVIDENCE_INDEX.csv, SCRIPT_SHA256.csv, MANIFEST_SHA256.csv (L12 self-exclusion),
and 03_EVIDENCE/README.md for PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915.
Run AFTER all other package files (incl. AT_RUN_END_GIT_OBSERVATION.md) exist.
"""
import os
import sys
import hashlib
import time

RUN_DIR = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915"
SCRIPTS = os.path.join(RUN_DIR, "00_CONTROL", "scripts")
EVID = os.path.join(RUN_DIR, "03_EVIDENCE")
REPORT = os.path.join(RUN_DIR, "06_REPORT")
MANIFEST = os.path.join(REPORT, "MANIFEST_SHA256.csv")


def sha256_of(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest().upper()


def iter_package_files():
    for root, dirs, files in os.walk(RUN_DIR):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for fn in sorted(files):
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, RUN_DIR).replace("\\", "/")
            yield rel, full


def main():
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    # --- SCRIPT_SHA256.csv (00_Control/scripts/*; includes this script — its hash, not a self-hash of the CSV)
    script_rows = []
    for fn in sorted(os.listdir(SCRIPTS)):
        full = os.path.join(SCRIPTS, fn)
        if os.path.isfile(full) and not fn.endswith((".pyc",)):
            script_rows.append((fn, sha256_of(full), os.path.getsize(full)))
    with open(os.path.join(RUN_DIR, "00_CONTROL", "SCRIPT_SHA256.csv"), "w", encoding="utf-8") as f:
        f.write("script_name,sha256,size_bytes\n")
        for n, h, s in script_rows:
            f.write("%s,%s,%d\n" % (n, h, s))

    # --- 03_EVIDENCE/README.md — AMEND (QC P1-2 root-cause fix): written BEFORE the evidence index so the
    # index row for README.md captures the FINAL file. The original ordering wrote the index first, so the
    # README row captured the pre-rewrite state (the stale-row defect QC found).
    with open(os.path.join(EVID, "README.md"), "w", encoding="utf-8") as f:
        f.write("""# 03_EVIDENCE — PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915

Evidence index: EVIDENCE_INDEX.csv (every package file -> role + SHA256 + size, generated %s UTC).
EXCLUSIONS (documented): EVIDENCE_INDEX.csv excludes its own row (self-hash impossible) and
06_REPORT/MANIFEST_SHA256.csv (written after the index in the same generation pass; the manifest covers it).
Manifest: 06_REPORT/MANIFEST_SHA256.csv (SHA256 of every package file; the manifest itself is excluded
per the L12 self-exclusion rule — a manifest cannot contain its own hash).
GENERATION ORDER (amended per QC P1-2): SCRIPT_SHA256.csv -> README.md -> EVIDENCE_INDEX.csv ->
MANIFEST_SHA256.csv, so the index's README.md row reflects the final README bytes.

Evidence discipline applied in this run (contract EVIDENCE QUALITY):
- Every load-bearing PASS cites a MEASURED_QUANTITY with an INDEPENDENT_SOURCE_OF_TRUTH (capstone decode of
  Entropia.exe physical bytes) and an explicit WHY_NON_CIRCULAR chain (instruction-address def-use, not prose).
- FAILURE_CASE_DETECTED = YES (4 executed negative controls; 01_RAW/NEGATIVE_CONTROL_RAW.txt).
- No runtime execution of the client (STATIC-ONLY); no oracle used as primary proof (QH-012).
- All raw files carry measured provenance headers (python 3.12.7 / capstone 5.0.7 / generator script SHA256 /
  source SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31).
- Correction pass (fresh-QC findings P1/P2/P3): 00_CONTROL/PRE_EDIT/ holds byte-exact pre-edit copies of every
  amended file; amendments are logged in 00_CONTROL/AMEND_LOG_R1.md; the triple write-census channels are
  enumerated in 01_RAW/ORIGIN_TRIPLE_WRITE_CENSUS_RAW.txt (census_triple_writes.py).
- Correction run PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915 (origin mutability): 00_CONTROL/PRE_EDIT_R2/
  holds byte-exact pre-edit copies of every AMEND-14+ amended file; the write-through of the getter-returned
  singleton pointer is measured in 01_RAW/ORIGIN_SINGLETON_WRITE_THROUGH_CENSUS.csv (writer site 0x458E27;
  pre-registered N=16 window); the corrected status algebra is 02_ANALYSIS/ORIGIN_STATUS_CORRECTION.md;
  generator prose no longer carries science conclusions (measurement/status separation).
""" % ts)

    # --- EVIDENCE_INDEX.csv
    evidence_map = {
        "00_CONTROL/RUN_CONTRACT.md": "Authoritative contract (formalizer; executor READ-ONLY; SHA256 verified at dispatch: EEF4C898...AAC3E)",
        "00_CONTROL/SOURCE_IDENTITIES.json": "Formalizer-measured source/repo/boot identities (executor re-verified S0 at run start)",
        "00_CONTROL/SCRIPT_SHA256.csv": "SHA256 of all run-local generator scripts",
        "00_CONTROL/AMEND_LOG_R1.md": "Correction log: 2 pre-completion entries + correction-pass entries (QC findings) + origin-mutability correction entries (AMEND-14+, RUN PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915); .pre/new SHA pairs; named lessons",
        "00_CONTROL/CORRECTION_CONTRACT_ORIGIN_MUTABILITY_R1.md": "Origin-mutability correction run contract (persisted verbatim before any package edit)",
        "00_CONTROL/scripts/census_triple_writes.py": "Correction-pass census generator (P1-1): channel-enumerated write census of the origin triple ([T.10] amended by the origin-mutability correction)",
        "00_CONTROL/scripts/decode_lib.py": "Shared PE loader (S0 fail-closed) + capstone decode/census helpers",
        "00_CONTROL/scripts/gen_raw_evidence.py": "Generates the mechanical raw disasm/census files (Phases A-D); origin-mutability correction removed hardcoded science conclusions from its emitted prose",
        "00_CONTROL/scripts/gen_manifest.py": "Builds this evidence index + manifest (L12 self-exclusion; README written before the index per QC P1-2)",
        "00_CONTROL/scripts/patch_utf8.py": "One-shot UTF-8 encoding patch helper (documented in AMEND_LOG_R1.md AMEND-2)",
        "00_CONTROL/scripts/sprov.py": "NEW (origin-mutability correction): symbolic S_PTR provenance engine + callee-head classifier + ret-convention measurer",
        "00_CONTROL/scripts/probe_origin_setter.py": "NEW (origin-mutability correction): falsifier + setter 0x458D90 full decode + esp ledger + caller decode",
        "00_CONTROL/scripts/census_write_through.py": "NEW (origin-mutability correction): provenance-aware write-through census over all direct E8 callers of 0x437F70",
        "00_CONTROL/scripts/census_setter_reach.py": "NEW (origin-mutability correction): static reachability census of the setter chain (channels, extents, RTTI)",
        "00_CONTROL/scripts/probe_output_formula.py": "NEW (origin-mutability correction): independent re-derivation of the 0x82B5A0 output formula (K bits, ret 8)",
        "01_RAW/AT_RUN_START_GIT_OBSERVATION.md": "SECTION 1 formalizer (immutable) + SECTION 2 executor run-start git/S0 measurement",
        "01_RAW/AT_RUN_END_GIT_OBSERVATION.md": "Executor run-end git verification (HEAD unchanged; untracked census; zero mutations) + correction-pass appendix",
        "01_RAW/CORRECTION_RUN_GIT_OBSERVATION.md": "NEW (origin-mutability correction): correction-run git observation (BASE SHA match; untracked inventory; zero git mutations)",
        "01_RAW/FUN_0050A050_DOWNSTREAM_DISASM.txt": "PHASE A: 36/36 pin MATCH (count amended per QC P2-2); extent; stack/arg mapping for both helpers; def-use answer; pseudo-C",
        "01_RAW/FUN_00437F70_DISASM.txt": "PHASE C: helper1 = origin-singleton getter; SEH (amended per QC P3-3); IAT callee IDs; 10 questions (lifetime prose amended by the origin-mutability correction)",
        "01_RAW/FUN_0082B5A0_DISASM.txt": "PHASE D: helper2 = scaled-subtract converter; bit-exact constants; exact x87 trace; 7 questions (zero-origin simplification amended to conditional)",
        "01_RAW/SOURCE_VECTOR_LAYOUT_RAW.txt": "PHASE B: +0x90 world translate proof; world-vs-local; vtable matrix; SF ctor anchors; [B.2] excerpt extended per QC P3-1",
        "01_RAW/HELPER437F70_CALLER_CENSUS.csv": "99 E8 callers of 0x437F70 classified (pair membership + next-instruction shape; the original instrument's write-through coverage claim is retracted by the origin-mutability correction)",
        "01_RAW/HELPER82B5A0_CALLER_CENSUS.csv": "36 E8 callers of 0x82B5A0 with pair membership (non-pair rows amended per QC P2-4)",
        "01_RAW/HELPER82B5A0_CALLER_CENSUS.txt": "Human-readable 0x82B5A0 census companion (prose amended per QC P2-4)",
        "01_RAW/END_TO_END_VALUE_FLOW_RAW.txt": "PHASE E: per-component formulas; triple write-census channels (enumerated per QC P1-1; E.3 wording amended by the origin-mutability correction); fallback dataflow; UNKNOWNs",
        "01_RAW/ORIGIN_TRIPLE_WRITE_CENSUS_RAW.txt": "CORRECTION-PASS CENSUS (P1-1): channel-enumerated write census of the origin triple ([T.10] + residuals amended by the origin-mutability correction: measurement verdict + status pointers) + P2/P3 fact-verification annex",
        "01_RAW/ORIGIN_SETTER_458D90_DISASM.txt": "NEW (origin-mutability correction): falsifier reproduction at 0x458E27 + setter 0x458D90 full decode + esp ledger + chain ABI + caller FUN_00458E50 + recounts",
        "01_RAW/ORIGIN_SINGLETON_WRITE_THROUGH_CENSUS.csv": "NEW (origin-mutability correction): write-through census rows over 99 boundary-verified direct callers of 0x437F70 (N=16 + N=8 views; writer site 0x458E27)",
        "01_RAW/ORIGIN_SINGLETON_WRITE_THROUGH_RAW.txt": "NEW (origin-mutability correction): census method + per-site windows/events + mechanical aggregates + instrument validation",
        "01_RAW/ORIGIN_SETTER_CALLER_CENSUS.csv": "NEW (origin-mutability correction): channel census rows (E8/E9/imm32/vtable/extents) for the setter-chain subject functions",
        "01_RAW/ORIGIN_SETTER_REACHABILITY_RAW.txt": "NEW (origin-mutability correction): both reported branches re-derived; true static chain; boundary proofs; RTTI walk; anchor discrepancy reports",
        "01_RAW/OUTPUT_FORMULA_REVALIDATION_RAW.txt": "NEW (origin-mutability correction): independent 0x82B5A0 formula re-derivation (K bits BITMATCH; ret 8)",
        "01_RAW/FALLBACK_PRIMARY_COMPARISON.txt": "Five contract questions: fallback vs primary (origin-condition wording amended by the origin-mutability correction)",
        "01_RAW/NEGATIVE_CONTROL_RAW.txt": "MANDATORY negative control: 4 executed controls; FAILURE_CASE_DETECTED=YES; Control 4 SUPERSEDED by counterexample 0x458E27 (appended block)",
        "02_ANALYSIS/SOURCE_VECTOR_LAYOUT.md": "PHASE B analysis + H1 verdict",
        "02_ANALYSIS/HELPER_OPERATIONS.md": "PHASE C/D analysis + H2/H3 verdicts (origin-mutability status corrected by the origin-mutability correction)",
        "02_ANALYSIS/OUTPUT_VALUE_RELATION.md": "G6/G7 analysis (general formula scale(W)-S; zero-origin simplification conditional)",
        "02_ANALYSIS/POSITION_SEMANTICS.md": "PHASE F analysis + G9/G11-G14 + H4/H5 verdicts (100:1 claims conditionalized by the origin-mutability correction)",
        "02_ANALYSIS/ORIGIN_STATUS_CORRECTION.md": "NEW (origin-mutability correction): corrected origin-singleton status algebra with per-status measured quantity, evidence, non-circularity, failure case",
        "02_ANALYSIS/SCIENCE_STATUS_DELTA.csv": "All 11 status-algebra dimensions (K hex amended per QC P3-2; origin rows amended by the origin-mutability correction)",
        "03_EVIDENCE/README.md": "This evidence directory guide",
        "03_EVIDENCE/EVIDENCE_INDEX.csv": "This index",
        "06_REPORT/REPORT.md": "Final report (primary question answer; findings; boundaries; QC P1/P2 corrections applied)",
        "06_REPORT/HANDOFF.md": "Executor handoff (schema-conformant return; QC P2-2/P2-3 corrections applied)",
        "06_REPORT/STAGE_ACCEPTANCE_GATES.csv": "G0..G17 honest statuses (G2/G6 rows amended per QC P2-2/P1-1)",
        "06_REPORT/MANIFEST_SHA256.csv": "SHA256 manifest (L12 self-exclusion)",
    }
    with open(os.path.join(EVID, "EVIDENCE_INDEX.csv"), "w", encoding="utf-8") as f:
        f.write("evidence_path,role_in_run,sha256,size_bytes\n")
        for rel, full in iter_package_files():
            rel_fwd = rel.replace("\\", "/")
            # Self-exclusion (L12 rationale): the index cannot contain its own hash (the file is being written);
            # 06_REPORT/MANIFEST_SHA256.csv is written AFTER this index in the same run (order artifact) and is
            # covered by the manifest itself; both exclusions are documented in 03_EVIDENCE/README.md.
            if rel_fwd == "03_EVIDENCE/EVIDENCE_INDEX.csv" or rel_fwd == "06_REPORT/MANIFEST_SHA256.csv":
                continue
            role = evidence_map.get(rel, "package file")
            f.write("%s,\"%s\",%s,%d\n" % (rel, role, sha256_of(full), os.path.getsize(full)))

    # --- MANIFEST_SHA256.csv (L12 self-exclusion: no row for MANIFEST_SHA256.csv itself)
    rows = []
    for rel, full in iter_package_files():
        rel_fwd = rel.replace("\\", "/")
        if rel_fwd == "06_REPORT/MANIFEST_SHA256.csv":
            continue  # L12 self-exclusion
        rows.append((rel_fwd, sha256_of(full), os.path.getsize(full)))
    with open(MANIFEST, "w", encoding="utf-8") as f:
        f.write("path,sha256,size_bytes\n")
        for r, h, s in rows:
            f.write("%s,%s,%d\n" % (r, h, s))
    print("manifest rows:", len(rows))
    print("scripts:", [r[0] for r in script_rows])


if __name__ == "__main__":
    main()
