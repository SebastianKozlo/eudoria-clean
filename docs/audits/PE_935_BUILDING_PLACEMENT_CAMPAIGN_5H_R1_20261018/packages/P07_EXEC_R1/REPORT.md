# P07 REPORT (DIRECT_ANALYST_FALLBACK by PE-MASTER)
Attribution: parent fallback per CONTRACT section 4 after two incomplete child executions (attempt 1 preserved CONTRACT.json, RUN_STARTED.json, tools, 4 extracts; attempt 2 added nothing). Extracts verified (headers carry source SHA, admission ID, listing line numbers; spot line-parity checks passed).
## Scoped result
(a) 745BF0 = keyed map-lookup helper (4-DWORD key incl. constant 4; callee 745A70 performs the actual read; success returns *[EAX]; fail path exits window at 0x00745C40). NO VFS-record-fed source in-window (scoped negative). id2/tag-6 hypothesis NOT confirmed in-window - moved to 745A70.
(b) ALL THREE imm32 sites register the SAME callback 0x008BD720. 0x006B6C9D is the {0x66,A}-forming pump: valid check 72FCE0 -> A-read getter 7CE1E0 (bridge-CONFIRMED [ECX+0x08]) -> const 0x66 pair build 43C700 -> callback registration via 40B070 -> enqueue via 43E5B0. 006C3F98 and 006D44A4 register the same callback via 40B070 + 006C3640 (second enqueue path).
## Position in the campaign
{0x66,A} request formation CONFIRMED at instruction level in the model-side pump adjacent to the CAND4 factory cluster. Missing consumer edge = bodies 0040B070/0043E5B0/006C3640 + callback invocation census. This is the transport side of MODEL_INSTANCE_BINDING; VFS->slot merge question open at 745A70.
## Counters
4 bodies / 148 extract rows (vs 133 reserved - loop-tail overshoot disclosed) / 10 CALL / 4 candidates.
## Standing
WORLD_XYZ_RECOVERED=NO, HISTORICAL_PLACEMENT=NOT_ESTABLISHED, CURSOR_SOURCE_MEDIUM=UNKNOWN, CANONICAL_GATE_EFFECT=NONE.
