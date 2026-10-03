# SOURCE_ORDER_DERIVATION — independent expected behavior for the F1 fix

RUN: PE_GAMEBRYO_ORACLE_F1_RTTI_CORRECTION_R1_20261003
QC DISCIPLINE: this derivation is made from the PINNED SOURCE BYTES ONLY
(D:\gamebyroengine\extracted\Gb12_Source\CoreLibs\NiMain\NiStream.cpp,
SHA256 E955C36EBBB442029E00BE8A154726741B8454A607F2DC043F1FD542B009DC25,
re-verified at run start) and hand-built fixtures. The corrected adapter code
is NOT a source of truth for this document. The fixtures were built from the
same pinned canon (see 01_FIXTURES/build_fixtures.py header); fixtures A and B
came out BYTE-IDENTICAL to the Desktop auditor's independently built
synthetic_valid_node.nif (48B24BB5...) and unused_unregistered_rtti.nif
(BEDE862D...), which cross-validates the layout derivation twice.

## 1. The pinned source algorithm (NiStream.cpp L412-449)

```cpp
bool NiStream::LoadRTTI()
{
    unsigned short usRTTICount;
    NiStreamLoadBinary(*this, usRTTICount);          // (a) u16 count

    CreateFunction* ppfnCreate = new CreateFunction[usRTTICount];

    unsigned int i;
    for (i = 0; i < usRTTICount; i++)
    {
        char aucRTTI[MAX_RTTI_LEN];
        LoadRTTIString(aucRTTI);                      // (b) read ONE name
        bool bFound = ms_pkLoaders->GetAt(aucRTTI, ppfnCreate[i]);
        if (!bFound)                                  // (c) factory check
        {
            RTTIError(aucRTTI);                       //     "<name>: cannot
            delete[] ppfnCreate;                      //      find create
            return false;                             //      function."
        }
    }

    for (i = 0; i < m_kObjects.GetAllocatedSize(); i++)
    {
        unsigned short usRTTI;
        NiStreamLoadBinary(*this, usRTTI);            // (d) per-object index
        assert(usRTTI < usRTTICount);
        NiObject* pkObject = ppfnCreate[usRTTI]();
        m_kObjects.Add(pkObject);
    }
    ...
    return true;
}
```

Call site (LoadStream L506-526): `bNew = GetFileVersion() >= 5.0.0.1`;
`if (bNew) { if (!LoadRTTI()) return false; }` — a false return fails the
WHOLE Load() before LoadObjectGroups, before any LoadBinary body loop, before
links, before the footer.

## 2. Derived control flow (what any faithful port MUST do)

1. Read u16 `usRTTICount`.
2. For i in 0..count-1, IN TABLE ORDER:
   a. read name i (u32 length + bytes);
   b. registry/factory check name i;
   c. **the FIRST miss aborts everything**: error is the miss name; NOTHING
      after it (later names, ALL object indices, groups, bodies, footer) is
      read; the verdict is fail-closed REJECTED.
3. Only if EVERY table entry is registered: read one u16 type index per
   header-declared object (`m_kObjects.GetAllocatedSize()` == header
   uiObjects), in object order, and instantiate.
4. Consequences, each directly readable from the control flow:
   - an UNUSED table entry (referenced by no object) is still validated at
     step 2 — the object indices do not exist yet at that point;
   - the FIRST miss is determined by TABLE order; object order is irrelevant
     to the verdict and to the error name;
   - a truncated later name (EOF inside step 2 at j > miss) is NEVER reached
     when an earlier miss exists — the earlier factory miss is the verdict;
   - a truncated/incomplete object-index list is NEVER reached when a table
     miss exists — same rule;
   - the per-object reference histogram/census is a step-3 artifact and
     CANNOT substitute for the step-2 table validation.

## 3. Per-fixture expected verdicts (ordinary, fail-closed mode)

| fixture | table (order) | objects (order) | expected ordinary verdict |
|---|---|---|---|
| A `fx_A_registered_only.nif` | [NiNode] | 1 x NiNode | ACCEPTED (all stages pass) |
| B `fx_B_unused_unregistered.nif` | [NiNode, NiXyzzyx] | 1 x idx0 (NiNode) | REJECTED, RTTIError(NiXyzzyx), miss at table index 1; NiXyzzyx is UNUSED by any object — this is the F1 counterexample |
| C1 `fx_C1_trailing_unknown_run.nif` | [NiNode, NiXyzzyx, NiQuuxzyx] | idx0 (NiNode), idx2 (NiQuuxzyx) | REJECTED, RTTIError(NiXyzzyx) — TABLE order (index 1) wins even though object order meets NiQuuxzyx first. (The unknown run is TRAILING: --full-decode on this fixture trips the PRE-EXISTING presolver boundary crash, Desktop F4 territory, out of scope — recorded before AND after the fix, both exit 1) |
| C2 `fx_C2_table_vs_object_order.nif` | [NiNode, NiXyzzyx, NiQuuxzyx] | idx0 (NiNode), idx2 (NiQuuxzyx), idx0 (NiNode) — unknown run in the MIDDLE | REJECTED, RTTIError(NiXyzzyx); --full-decode keeps REJECTED + FIRST_RTTI_MISS=NiXyzzyx with full extension inspection (the standard T-corpus shape) |
| E `fx_E_incomplete_indices.nif` | [NiNode, NiXyzzyx] | header says 3, only 1 u16 index present | REJECTED, RTTIError(NiXyzzyx) — the incomplete index list is never read |
| F `fx_F_truncated_later_name.nif` | [NiNode, NiXyzzyx, <name 2: len 0x400, EOF>] | header says 1 | REJECTED, RTTIError(NiXyzzyx) — name[2] is never read |

For `--full-decode` (OUR extension, never original behavior): the extension
may continue inspection (later names, indices, bodies) but the
SOURCE_PREDICTED_VERDICT must remain REJECTED with FIRST_RTTI_MISS = the
first miss in TABLE order, and every continuation past the miss must be
explicitly labeled as extension. If the extension itself hits a parser
failure (e.g. the truncated name[2] in fixture F), that failure must be
recorded as an extension halt and must NOT mask or replace the
source-predicted verdict.

## 4. Measured pre-fix behavior (pinned code, run BEFORE any edit)

Raw records: 02_RAW_TESTS/BEFORE_FIX_*.RECORD.json (exact command, stdout,
stderr, exit code per record).

| fixture | pre-fix verdict | deviation from source |
|---|---|---|
| B | accepted=true, unregistered_types=[], exit 0 | FALSE SUCCESS: the unused unregistered NiXyzzyx entry was never checked (Desktop finding F1 reproduced exactly) |
| C1/C2 | RTTIError(NiQuuxzyx) | WRONG FIRST MISS: object-reference order, not table order |
| E | DECODE_ERROR: CLOSURE_SEARCH_FAILED (partial) | indices were read despite the earlier table miss; the object-index bytes were misinterpreted from the groups/body region |
| F | uncaught DecodeError traceback, exit 1, empty stdout | all names were read before validation; the truncated later name masked the earlier factory miss |
| C1 --full-decode | IndexError traceback in the E3 presolver (assemble -> decode_block_at(b, run_end) with run_end == n_obj for a trailing unknown run), exit 1 | PRE-EXISTING defect (Desktop F4 territory, "IndexError w presolverze"); proven pre-existing by re-running the same input under the pre-fix code via git stash; NOT an F1 regression and NOT fixed in this run |

All pre-fix behaviors contradict the pinned source control flow in
section 2. The fix must make all fixtures in section 3 behave as derived,
while preserving the registered-only baseline A.

## 5. In-run corrections of the fix implementation (honest record)

1. The first implementation of the table scan did not guard the
   first-miss assignment: under `--full-decode` the scan continues past
   the first miss (extension), and a LATER unregistered entry OVERWROTE
   first_rtti_miss (C2 full-decode reported NiQuuxzyx@2 instead of
   NiXyzzyx@1). Caught by mandatory test C; fixed with a
   `first_miss_name is None` guard; the whole after-fix battery was then
   re-captured with the final code.
2. Fixture F's first builder pass placed the truncated 3rd name OUTSIDE
   the table (count=2); it was rebuilt as count=3 with the truncated
   name INSIDE the table BEFORE any post-fix run, and the pre-fix record
   was re-captured on the corrected bytes.
3. Fixture C was split into C1 (trailing unknown run; kept as the
   permanent input documenting the pre-existing presolver boundary
   crash, out of scope) and C2 (middle unknown run; the actual test C)
   after C1's --full-decode tripped the pre-existing crash under BOTH
   the pre-fix and post-fix code.
