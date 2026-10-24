# EXCLUDED_ARTIFACTS (not published, with reasons)
- SCRIPT_REGISTRATION_ROSTER.csv (full): per-member SHA256 of decoded script plaintexts — derived corpus metadata of decrypted scripts; not published (decrypted-script corpus privacy rule). Counts and rules published in summaries.
- DECODER key blob (0x1C0 B @0x610478) and any decode-capable key material: never in any output, private by rule.
- Raw Ghidra decompilations/listings, scan dumps (JB1_*.txt, ghidra_*.json, decomp_*.c), DLOB hex streams: raw listings/dumps excluded; analyses and byte proofs summarized in reports.
- Preview frames/screenshots, extracted NIF/BVI payloads, sandbox (705-file install closure incl. junctioned game data): game-derived bytes stay local.
- Ghidra projects (jb1/jc1/jd1/qc1), WORK_ROOT evidence trees, trace artifacts: workspace-local.
- Full BASELINE_DISPOSITION/NORMALIZED/REPLAY_REVALIDATED/CHECKER outputs: published notice summarizes dispositions; normalized rows contain verbatim frozen-run material — the frozen source runs remain the authoritative copies.
