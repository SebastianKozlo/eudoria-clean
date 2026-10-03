# NOT CHECKED — PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003

Executor: pe-reconstruction. STATIC_ONLY. Items below were NOT measured this
run, with reasons. None is load-bearing for the run's verdicts; each is bounded
out either by the falsifier STOP (S2) or by scope discipline.

## Stopped by the falsifier (contract §12/§24 — landmark path terminated)

```text
N-01  Phases 6-11 as landmark path: template->A bridge at THIS call-site,
      resource request/resolution, runtime NIF open, world-instance identity,
      transform producer/semantics, scene/world edge, XYZ recovery. NOT
      EXECUTED: the falsifier fired; the call-site has no template path.
N-02  Search for OTHER call-sites pushing 4057 (EXE-wide immediate scan).
      NOT DONE — contract §9 forbids whole-EXE scans "na wypadek" and §31
      forbids immediately hunting another call-site (separate future
      experiment if ever authorized).
N-03  The 0x008D-0x008F family beyond the directly-dependent callees measured
      (g2/g3): e.g. FUN_008DF1E0, FUN_008DF9A0, FUN_008E04E0, FUN_008E2AB0,
      FUN_00890D30, FUN_0092B490, FUN_0092B390, FUN_008DFAE0, FUN_008DF290,
      FUN_008268A0, FUN_00822970, FUN_00826840, FUN_008C3580 — only their call
      presence inside measured windows is recorded; bodies not decoded.
N-04  FUN_00824C70 (0x98-manager singleton ctor), FUN_008216F0 (sids string
      reader), FUN_00413DA0 (sids map insert; composite-key part-1 semantics),
      FUN_00401E70 (VFS path open) — the map the key {section,4057} resolves in
      is identified mechanically; its loader/ctor internals are not.
N-05  The contents of the FUN_00826A50 table (DAT_00b95954[0] = key part 1 =
      "section object"); the section/subsystem semantics of key part 1.
N-06  The display-text/localization layer beyond the identifier string: the
      measured chain resolves id -> identifier ('S_REPAIR_UI_CLEAR_TOOLTIP');
      how identifiers become rendered UI text (further localization stages)
      was NOT traced.
N-07  RTTI chain walks (vtable-4 -> COL -> TD) for 0x00A7A948
      (ArkUI::Component), ArkRepairUI vtable / ArkRepairUI_Impl Type
      Descriptor: the labels are Ghidra RTTI-analyzer readings of the binary's
      own RTTI symbols (STRONGLY_SUPPORTED); no independent byte-walk was run.
      R1 AMEND NOTE: QC's independent chain walks (04_QC/TARGETED_QC_REPORT.md
      Q6) now CONFIRM all three chain-walk facts (store vtable 0x00A7A948 =
      '.?AVComponent@ArkUI@@'; unwind vtable 0x00A80704 = '.?AVArkRepairUI@@';
      gate TD = '.PAVArkRepairUI_Impl@@' pointer-form). Executor + QC agree on
      the chain-walk facts; class BEHAVIORAL identity remains exactly as before
      (not upgraded to behavioral semantics). This N-07 row remains an honest
      record of the EXECUTOR's own run scope.
N-08  The [ESP+0xC8] owner object's exact class (no vtable store of its own was
      measured; identified only as the ArkRepairUI-path owner that receives
      FUN_008DFCD0/008E7B80/008F0780 calls).
N-09  FUN_0059BE70's siblings (FUN_0059ba40, FUN_004d9dc0, FUN_004143f0,
      FUN_0042bc30, FUN_008df860(0x411), FUN_008df290, FUN_008df1e0,
      FUN_00595b40) — caller context recorded only.
N-10  The sids.vfs CRC field of its single container record is 0 (CRC disabled
      at container level) — no CRC claim made for sids.vfs; the sids ENTRY
      parse validation is the exact-closure + count match (SIDS_ENTRY_PARSE).
N-11  Whether OTHER sids ids collide with other templates id2 values (only the
      anchored/sibling series were censused, per bounded scope).
N-12  The 2003-era corpus (01_Original_Files) — wrong era; not used, not opened.
N-13  Any dynamic/runtime/network work — NONE (STATIC_ONLY enforced; no client
      launch, no instrumentation, no network).
N-14  Ghidra auto-analysis coverage outside the measured path (undefined-code
      regions, thunks) — not relevant to any claim; all claims are anchored on
      defined instructions byte-verified against the physical EXE.
N-15  Gamebryo oracle mechanisms: 0 new (NEW_GAMEBRYO_ORACLE_MECHANISMS_MAX=0);
      existing canon read as context only.
N-16  The deeper history of the deferred lead (who produced the 4057/0x0059AB12
      candidate in the earlier local conversation) — not evidence either way;
      out of scope.
```

## Budget-relevant counts

```text
NEW_PCG_FUNCTIONS_DETAILED = 18 (FUN_00599d30; g2: 008dfcd0, 008f0780, 008e7b80,
  008df3f0, 008df310; g3: 00414170, 00821bb0, 008dfb70, 008f01c0, 0059be70;
  g4: 00821760, 008221c0; g5: 00826a50, 00415670, 00823c10, 00821fb0;
  g6: 00821e70) — limit 60 NOT exceeded.
NEW_PHYSICAL_RECORDS_DETAILED = 2 (templates.vfs record 4057; sids.vfs
  single-record payload parsed + entry 4057 dump) — limit 2 NOT exceeded
  (record 4508 was a calibration re-pin of an existing canon anchor).
NEW_MODEL_RESOURCE_INDEX_RECORDS = 4 (Models.bnt: 296445.nif calibration,
  218757.nif; Volumes.bnt: 296446.bvi calibration, 218758.bvi) — limit 4 NOT
  exceeded.
```
