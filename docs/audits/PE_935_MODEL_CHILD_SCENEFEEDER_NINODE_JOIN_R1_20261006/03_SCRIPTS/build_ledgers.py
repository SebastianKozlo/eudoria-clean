"""Build the four ledgers (csv.DictWriter, fixed headers) + schema validation.
PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006.
"""
import csv, json, os, sys

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006"

def write_csv(path, header, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow(r)

def validate_csv(path, header):
    with open(path, "r", encoding="utf-8", newline="") as f:
        rd = csv.reader(f)
        rows = list(rd)
    errs = []
    if rows[0] != header:
        errs.append(f"header mismatch: {rows[0]} != {header}")
    ids = set()
    for i, r in enumerate(rows[1:], start=2):
        if len(r) != len(header):
            errs.append(f"row {i}: width {len(r)} != {len(header)}")
        for j, c in enumerate(r):
            if c is None or c == "":
                errs.append(f"row {i} col {header[j]}: null/missing")
    return errs

# ---------------- FUNCTION_BUDGET.csv ----------------
FH = ["FN_ID", "VA_RANGE", "STATUS", "CHARGE_BASIS", "NEW_SEMANTICS_ESTABLISHED", "PRIOR_SCOPE_NOTE"]
fn_rows = [
    {"FN_ID": "FUN_008BD720", "VA_RANGE": "0x008BD720..0x008BD724", "STATUS": "NEW_DETAIL_1_OF_8",
     "CHARGE_BASIS": "full body read (4 B) of a VA pinned but never decoded",
     "NEW_SEMANTICS_ESTABLISHED": "lea eax,[ecx+0x18]; ret — a 4-byte accessor returning &obj+0x18, NOT a completion handler body; the {0x66,A} scheduler 'callback' pin (bridge E3) is an accessor",
     "PRIOR_SCOPE_NOTE": "bridge E3 pinned the VA only; no body was recorded"},
    {"FN_ID": "FUN_00528E50", "VA_RANGE": "0x00529020..0x00529072 (continuation)", "STATUS": "NEW_DETAIL_2_OF_8",
     "CHARGE_BASIS": "new semantics of a known function beyond the recorded pin scope",
     "NEW_SEMANTICS_ESTABLISHED": "CMO ctor tail: 3 further SF method calls — FUN_00509510(&[CMO+0x5C]) @0x0052902F, FUN_00509070(&[CMO+0x50]) @0x0052903E, FUN_00509850(0.0f, flag) @0x00529050; ctor extent ends 0x00529072 (ret 0x10)",
     "PRIOR_SCOPE_NOTE": "MICRO_R1/LINK30 recorded prologue, +0x74 chain, SF factory, [CMO+0xC0] store, FUN_005094C0 call"},
    {"FN_ID": "FUN_00509510", "VA_RANGE": "0x00509510..0x00509566", "STATUS": "NEW_DETAIL_3_OF_8",
     "CHARGE_BASIS": "never decoded in any read prior package",
     "NEW_SEMANTICS_ESTABLISHED": "SF SetRotation-like: triple -> SF+0x74/0x78/0x7C; conversion pair FUN_00437F70+FUN_0048BAC0 -> 9-dword block -> SF+0x4C; [SF+0x28]=1",
     "PRIOR_SCOPE_NOTE": "none (called at 0x0052902F discovered this run)"},
    {"FN_ID": "FUN_00509070", "VA_RANGE": "0x00509070..0x00509091", "STATUS": "NEW_DETAIL_4_OF_8",
     "CHARGE_BASIS": "never decoded in any read prior package",
     "NEW_SEMANTICS_ESTABLISHED": "SF setter: triple -> SF+0x80/0x84/0x88 (the triple exposed by vtable slot 4)",
     "PRIOR_SCOPE_NOTE": "none"},
    {"FN_ID": "FUN_00509850", "VA_RANGE": "0x00509850..0x005099BB", "STATUS": "NEW_DETAIL_5_OF_8",
     "CHARGE_BASIS": "never decoded in any read prior package",
     "NEW_SEMANTICS_ESTABLISHED": "SF update: flags SF+0x24..0x27 gate; [SF+0x20] model-manager object calls FUN_006C0EC0/ED0/FA0/FB0; SAME-INSTANCE TRANSFORM APPLICATION: SF pos x100 -> NiNode+0x5C/+0x60/+0x64, rotation 9 dwords SF+0x4C -> NiNode+0x38, scale |SF+0x70| -> NiNode+0x68; then FUN_007BF500([SF+0x30], caller-float, 1)",
     "PRIOR_SCOPE_NOTE": "none (called at 0x00529050 discovered this run)"},
    {"FN_ID": "FUN_007BF500", "VA_RANGE": "0x007BF500..0x007BF575", "STATUS": "NEW_DETAIL_6_OF_8",
     "CHARGE_BASIS": "never decoded in any read prior package",
     "NEW_SEMANTICS_ESTABLISHED": "update-like operation on the NiNode receiver: builds a 16-byte local from [this+0x24..0x34]; virtual call this->vtable[19] (0x007B47D0) with (float,1); conditional virtual call on [this+0x24] object vtable[45] (0x007B4550); NO children-array access (+0xCC/+0xD4 untouched) — REJECTED as an attach operation",
     "PRIOR_SCOPE_NOTE": "none"},
    {"FN_ID": "FUN_0050A310", "VA_RANGE": "0x0050A310..0x0050A453+", "STATUS": "NEW_DETAIL_7_OF_8",
     "CHARGE_BASIS": "never decoded in any read prior package",
     "NEW_SEMANTICS_ESTABLISHED": "SF visual/model-manager install (this=SF): old [SF+0x20] detach path (NiNode vtable[42] call + dtor); [SF+0x20]=new ArkModelManagerMain @0x0050A3AC; child=FUN_006C66D0(manager) @0x0050A3AF; JOIN SITE @0x0050A3E9..0x0050A3F7: receiver=[SF+0x30] (the exact examined NiNode), NiNode vtable slot 41 call with (child,0)",
     "PRIOR_SCOPE_NOTE": "none (found via the SF-cluster +0x20 census and the bridge R09 prior decompile of its caller FUN_006A3930)"},
    {"FN_ID": "FUN_007B5810", "VA_RANGE": "0x007B5810..0x007B58F2", "STATUS": "NEW_DETAIL_8_OF_8",
     "CHARGE_BASIS": "oracle identity probe (the join operation's PCG candidate) — full body read",
     "NEW_SEMANTICS_ESTABLISHED": "NiNode::AttachChild counterpart (STRONGLY_SUPPORTED): F1 NULL-guard child; F2 refcount inc [child+4] (x2); F3 direct call FUN_007BF470(child=ecx, parent=stack arg) — AttachParent-shaped, inner body NOT decoded; F4 children-array insertion: m_kChildren object @NiNode+0xC8 (base +0xCC, alloc +0xD0, used +0xD4 — consistent with the slot-17 GetObjectByName canon); bFirstAvail=1 -> FUN_007B55E0 AddFirstEmpty; else append-with-growth FUN_00788570 (grow) + FUN_007790D0 (set-at-index); F5 refcount dec (x2) with zero-destroy via child vtable slot 1",
     "PRIOR_SCOPE_NOTE": "none"},
]
write_csv(os.path.join(PKG, "FUNCTION_BUDGET.csv"), FH, fn_rows)

# ---------------- EDGE_LEDGER.csv ----------------
EH = ["EDGE_ID", "CALLSITE_VA", "EDGE", "STATUS", "LOAD_BEARING_FOR", "PROOF_ARTIFACT"]
edge_rows = [
    {"EDGE_ID": "E1", "CALLSITE_VA": "0x0052902F", "EDGE": "FUN_00528E50 -> FUN_00509510 (this=[CMO+0xC0]=SF, arg=&[CMO+0x5C])", "STATUS": "NEW_EDGE_1_OF_6",
     "LOAD_BEARING_FOR": "CMO-path SF initialization (no join at this edge)", "PROOF_ARTIFACT": "01_RAW/FUN_00528E50_CONTINUATION.txt; 01_RAW/FUN_509x_SF_METHODS.txt"},
    {"EDGE_ID": "E2", "CALLSITE_VA": "0x0052903E", "EDGE": "FUN_00528E50 -> FUN_00509070 (this=SF, arg=&[CMO+0x50])", "STATUS": "NEW_EDGE_2_OF_6",
     "LOAD_BEARING_FOR": "CMO-path SF initialization (no join at this edge)", "PROOF_ARTIFACT": "01_RAW/FUN_00528E50_CONTINUATION.txt; 01_RAW/FUN_509x_SF_METHODS.txt"},
    {"EDGE_ID": "E3", "CALLSITE_VA": "0x00529050", "EDGE": "FUN_00528E50 -> FUN_00509850 (this=SF, args=(0.0f, flag))", "STATUS": "NEW_EDGE_3_OF_6",
     "LOAD_BEARING_FOR": "the SF-update entry (leads to CAND-1/CAND-2 examinations and the transform-application proof)", "PROOF_ARTIFACT": "01_RAW/FUN_00528E50_CONTINUATION.txt; 01_RAW/FUN_00509850_FULL.txt"},
    {"EDGE_ID": "E4", "CALLSITE_VA": "0x00509972", "EDGE": "FUN_00509850 -> FUN_007BF500 (this=[SF+0x30] NiNode, args=(caller-float, 1))", "STATUS": "NEW_EDGE_4_OF_6",
     "LOAD_BEARING_FOR": "CAND-1 rejection (no child argument; no children-array access)", "PROOF_ARTIFACT": "01_RAW/FUN_007BF500_DECODE.txt"},
    {"EDGE_ID": "E5", "CALLSITE_VA": "0x006A3A9D", "EDGE": "FUN_006A3930 -> FUN_0050A310 (this=[ACLD+0x18]=SF, arg=ArkModelManagerMain)", "STATUS": "NEW_EDGE_5_OF_6",
     "LOAD_BEARING_FOR": "the model-manager install into the SF (leads to the join site CAND-4)", "PROOF_ARTIFACT": "01_RAW/FUN_006A3930_CHAIN_REPIN.txt; 01_RAW/FUN_0050A310_DECODE.txt"},
    {"EDGE_ID": "E6", "CALLSITE_VA": "0x0050A3F7", "EDGE": "FUN_0050A310 -> NiNode vtable slot 41 = FUN_007B5810 (this=[SF+0x30] NiNode, args=(child=FUN_006C66D0(manager) result, 0))", "STATUS": "NEW_EDGE_6_OF_6",
     "LOAD_BEARING_FOR": "THE JOIN SITE: parent byte-proven = the exact examined-path SF+0x30 NiNode; operation = AttachChild-shaped conditional children-array insertion (STRONGLY_SUPPORTED)", "PROOF_ARTIFACT": "01_RAW/FUN_0050A310_DECODE.txt; 01_RAW/FUN_007B5810_ORACLE_BYTE_PROOF.txt"},
]
write_csv(os.path.join(PKG, "EDGE_LEDGER.csv"), EH, edge_rows)

# ---------------- CANDIDATE_LEDGER.csv ----------------
CH = ["CANDIDATE_ID", "JOIN_SITE_VA", "PARENT_SOURCE", "PARENT_STATUS", "CHILD_SOURCE", "CHILD_PROVENANCE", "CHILD_ROLE", "JOIN_OPERATION", "JOIN_OPERATION_STATUS", "PATH_CONDITIONS", "WRAPPER_DEPTH", "IDENTITY_BREAK_FOUND", "STATUS", "REJECTION_REASON", "PHYSICAL_EVIDENCE"]
cand_rows = [
    {"CANDIDATE_ID": "CAND-1-CMO-PATH-7BF500-CALL", "JOIN_SITE_VA": "0x00509972",
     "PARENT_SOURCE": "FUN_00509850 @0x0050996C mov ecx,[ebp+0x30] (SF+0x30 NiNode of the CMO-ctor-path SF instance)",
     "PARENT_STATUS": "CONFIRMED_EXACT_SCENEFEEDER_PLUS_30",
     "CHILD_SOURCE": "NONE — no child object participates in this call (args: float, 1)",
     "CHILD_PROVENANCE": "UNRESOLVED (no child argument exists)", "CHILD_ROLE": "UNRESOLVED",
     "JOIN_OPERATION": "FUN_007BF500(this=NiNode, float, 1): builds a 16-byte local from [this+0x24..0x34]; virtual call this->vtable[19] (0x007B47D0); conditional virtual call on [this+0x24] via its vtable[45] (0x007B4550); NO children-array access",
     "JOIN_OPERATION_STATUS": "REJECTED",
     "PATH_CONDITIONS": "flags SF+0x24..0x27 window; [SF+0x28]==1 branch (first call form) or the else-path (second call form 0x005099AE); bl(flag arg)==0 in both",
     "WRAPPER_DEPTH": "1",
     "IDENTITY_BREAK_FOUND": "YES — the site has no child identity at all (not a child binding)",
     "STATUS": "REJECTED",
     "REJECTION_REASON": "REJECTED_NO_CHILD_ARGUMENT_AND_NO_CHILDREN_ARRAY_ACCESS (update-like operation on the NiNode; +0xCC/+0xD4 untouched)",
     "PHYSICAL_EVIDENCE": "01_RAW/FUN_00509850_FULL.txt; 01_RAW/FUN_007BF500_DECODE.txt"},
    {"CANDIDATE_ID": "CAND-2-CMO-PATH-TRANSFORM-WRITE", "JOIN_SITE_VA": "0x00509913",
     "PARENT_SOURCE": "FUN_00509850 @0x005098FA/0x00509931 mov eax/edi,[ebp+0x30] (SF+0x30 NiNode, CMO path)",
     "PARENT_STATUS": "CONFIRMED_EXACT_SCENEFEEDER_PLUS_30",
     "CHILD_SOURCE": "N/A — a transform write, no child object",
     "CHILD_PROVENANCE": "UNRESOLVED (no child)", "CHILD_ROLE": "UNRESOLVED",
     "JOIN_OPERATION": "m_kLocal write into the NiNode: translate=[SF+0x34..0x3C](+SF+0x40..0x48 conditional)x100 -> NiNode+0x5C/0x60/0x64; rotation 9 dwords from SF+0x4C -> NiNode+0x38; scale |SF+0x70| -> NiNode+0x68",
     "JOIN_OPERATION_STATUS": "REJECTED",
     "PATH_CONDITIONS": "[SF+0x20]!=NULL gates FUN_006C0EC0/ED0; [SF+0x28]==1 gates the transform write; bit test of [SF+0x2C]>>4 bit0 gates the +0x40..0x48 offset add",
     "WRAPPER_DEPTH": "1",
     "IDENTITY_BREAK_FOUND": "YES — transform application is not a child relation (binding anchor-constraint honored)",
     "STATUS": "REJECTED",
     "REJECTION_REASON": "TRANSFORM_APPLICATION_NOT_CHILD_BINDING (recorded separately as SAME_INSTANCE_TRANSFORM_RELATION=CONFIRMED_STATIC)",
     "PHYSICAL_EVIDENCE": "01_RAW/FUN_00509850_FULL.txt"},
    {"CANDIDATE_ID": "CAND-3-SF-CTOR-EXTRADATA-REGISTRATION", "JOIN_SITE_VA": "0x005094A2",
     "PARENT_SOURCE": "FUN_00509330 @0x00509494 mov ecx,[ebp+0x30] (SF+0x30 NiNode, in the SF ctor)",
     "PARENT_STATUS": "CONFIRMED_EXACT_SCENEFEEDER_PLUS_30",
     "CHILD_SOURCE": "FUN_0064B1E0 ctor result: SceneFeederObjectExtraData (vtable 0x00A83274; key at [obj+0x10] = the CMO+0x74 key)",
     "CHILD_PROVENANCE": "UNRESOLVED as model/resource (the child is the instance-key metadata carrier, not a model operation result)",
     "CHILD_ROLE": "NON_MODEL (NiExtraData family metadata; no visual role)",
     "JOIN_OPERATION": "FUN_007B6A80([SF+0x30], 'ArkSceneFeeder' literal 0x00A7D444, ExtraData) — AddExtraData-like front-end (STRONGLY_SUPPORTED per prior canon); final storage callee FUN_007B68B0 NOT_CHECKED (DEFERRED_LEAD per contract §3)",
     "JOIN_OPERATION_STATUS": "STRONGLY_SUPPORTED",
     "PATH_CONDITIONS": "allocations succeed; holder branch; the ExtraData chain is conditional on the ctor path",
     "WRAPPER_DEPTH": "0",
     "IDENTITY_BREAK_FOUND": "NO (same ExtraData object flows to the registration)",
     "STATUS": "REJECTED",
     "REJECTION_REASON": "NON_MODEL_CHILD_METADATA_NOT_VISUAL (re-pinned prior canon PA2; no new analysis performed)",
     "PHYSICAL_EVIDENCE": "01_RAW/REPIN_ANCHOR_WINDOWS.txt (PA2a/b/c)"},
    {"CANDIDATE_ID": "CAND-4-ACLD-PATH-SLOT41-ATTACH", "JOIN_SITE_VA": "0x0050A3F7",
     "PARENT_SOURCE": "FUN_0050A310 @0x0050A3E9 mov ecx,[esi+0x30]; esi=SF @0x0050A313; the SF was created by FUN_005247C0 in FUN_006A3930 @0x006A39ED and stored at [ACLD+0x18] @0x006A39F6 (ArkClientLocalDynamic ctor)",
     "PARENT_STATUS": "CONFIRMED_EXACT_SCENEFEEDER_PLUS_30 (the examined ACLD-path SF instance — same class (vtable 0x00A7D458) and same creation chain (FUN_005247C0->FUN_00509330->[SF+0x30]=NiNode) as the SF-island; SCOPE NOTE: a DIFFERENT INSTANCE from the SF-island's CMO+0xC0 holder — for the CMO instance no join was found in the examined chain)",
     "CHILD_SOURCE": "FUN_006C66D0(ArkModelManagerMain) result: @0x0050A3AF (call) -> eax -> edi @0x0050A3B7; the manager created in FUN_006A3930 @0x006A3A77 (new 0x130 -> FUN_006C0D50, vtable=ArkModelManagerMain per bridge W02 canon) and installed at [SF+0x20] @0x0050A3AC",
     "CHILD_PROVENANCE": "UNRESOLVED — the child is one getter away from the model manager; FUN_006C66D0 NOT decoded (function budget exhausted at 8/8); the manager's model/resource provenance NOT physically established on this path",
     "CHILD_ROLE": "UNRESOLVED — no physical visual-role proof; the follow-up calls FUN_007BF900/FUN_007BF630 on the child are NiMain-cluster methods (noted, not decoded); per binding constraint: resource-derived child may be VFX — separate proof required",
     "JOIN_OPERATION": "NiNode vtable slot 41 = [0x00A8CCF4+0xA4] = FUN_007B5810, called with (child=edi, 0): NULL-guard child; refcount inc [child+4] x2; direct call FUN_007BF470(child, parent) (AttachParent-shaped; body NOT decoded); children-array insertion into m_kChildren @NiNode+0xC8 (base +0xCC / alloc +0xD0 / used +0xD4 — matches the slot-17 GetObjectByName canon); bFirstAvail arg==0 -> append-with-growth branch (FUN_00788570 grow + FUN_007790D0 set-at-index); refcount dec x2 with zero-destroy via child vtable slot 1 — the Gb12 NiNode.cpp:52 AttachChild fingerprint (oracle identities re-measured MATCH)",
     "JOIN_OPERATION_STATUS": "STRONGLY_SUPPORTED (F1/F2/F4/F5 matched by bytes; F3 present as a direct call with undecoded body; PCG engine generation not era-exact with the oracle — same status ceiling as the slot-17 canon; NOT CONFIRMED)",
     "PATH_CONDITIONS": "FUN_006A3930: template-registry lookup (FUN_0043A550 + FUN_0072F580 + validity FUN_0072FCE0) must succeed; SF creation success ([ACLD+0x18]!=0); new(0x130)+FUN_006C0D50 success; FUN_006C66D0(manager) result !=0; in FUN_0050A310: [SF+0x30]!=0 @0x0050A32B; old [SF+0x20] (if any) goes through the detach path (NiNode vtable[42] FUN_007B5A00 + dtor); FUN_006C0F90 check -> [SF+0x2C] bit1; FUN_006C10B0 value -> FUN_0050A1E0(SF, child, value)",
     "WRAPPER_DEPTH": "2 (FUN_006A3930 -> FUN_0050A310 -> slot-41 edge); the child's next wrapper FUN_006C66D0 NOT traversed (budget)",
     "IDENTITY_BREAK_FOUND": "NO at the traversed depth (edi is the same pointer passed at 0x0050A3F7); the provenance to a physically established model/resource operation is NOT closed — the unresolved boundary is exactly the child's origin",
     "STATUS": "EXAMINED_UNRESOLVED (the positive candidate shape: parent + operation established; child provenance/role unresolved within budget)",
     "REJECTION_REASON": "NONE (not rejected; unresolved within bound)",
     "PHYSICAL_EVIDENCE": "01_RAW/FUN_0050A310_DECODE.txt; 01_RAW/FUN_007B5810_ORACLE_BYTE_PROOF.txt; 01_RAW/FUN_006A3930_CHAIN_REPIN.txt; 01_RAW/SF20_WRITER_CENSUS.txt (NiNode vtable dump slot 41)"},
]
write_csv(os.path.join(PKG, "CANDIDATE_LEDGER.csv"), CH, cand_rows)

# ---------------- CLAIM_MATRIX.csv ----------------
MH = ["CLAIM_ID", "CLAIM", "STATUS", "EVIDENCE", "WHY_NON_CIRCULAR"]
claim_rows = [
    {"CLAIM_ID": "CL-01", "CLAIM": "PA1 re-pin: SF ctor stores the FUN_007B6000 result at [SF+0x30]; the object is NiNode (vtable 0x00A8CCF4 @0x007B6041)", "STATUS": "CONFIRMED (re-pin of prior canon)", "EVIDENCE": "01_RAW/REPIN_ANCHOR_WINDOWS.txt PA1a/PA1b", "WHY_NON_CIRCULAR": "raw EXE bytes re-read this run from the hash-pinned file; matches LINK30/MICRO_R1 records independently"},
    {"CLAIM_ID": "CL-02", "CLAIM": "PA2 re-pin: ExtraData chain FUN_0064B1E0 + FUN_007B6A80([SF+0x30],'ArkSceneFeeder',obj) @0x005094A2", "STATUS": "CONFIRMED (re-pin; helper role STRONGLY_SUPPORTED per prior canon)", "EVIDENCE": "01_RAW/REPIN_ANCHOR_WINDOWS.txt PA2a/b/c", "WHY_NON_CIRCULAR": "raw bytes vs NIRTTI/ENGINE_COMPARISON pinned reports"},
    {"CLAIM_ID": "CL-03", "CLAIM": "PA3 re-pin: FUN_0050A050 slot-3 primary path reads [SF+0x30] and dispatches NiNode vtable+0x44 (slot 17)", "STATUS": "CONFIRMED (re-pin)", "EVIDENCE": "01_RAW/REPIN_ANCHOR_WINDOWS.txt PA3a/PA3b", "WHY_NON_CIRCULAR": "raw bytes vs SLOT_CENSUS/LINK30/SLOT17 records"},
    {"CLAIM_ID": "CL-04", "CLAIM": "PA4 re-pin: CMO ctor [CMO+0x74] key -> FUN_005247C0 -> [CMO+0xC0]=SF; SF re-received -> FUN_005094C0", "STATUS": "CONFIRMED (re-pin)", "EVIDENCE": "01_RAW/REPIN_ANCHOR_WINDOWS.txt PA4a/b/c/d", "WHY_NON_CIRCULAR": "raw bytes vs MICRO_R1/LINK30 records"},
    {"CLAIM_ID": "CL-05", "CLAIM": "CH1 re-pin: emitter FUN_006C3F50 {0x66,A} pair stores + scheduler entry FUN_006C3640 with callback imm 0x008BD720 @0x006C3FB0", "STATUS": "CONFIRMED (re-pin)", "EVIDENCE": "01_RAW/REPIN_ANCHOR_WINDOWS.txt CH1a/CH1b", "WHY_NON_CIRCULAR": "raw bytes vs bridge E3 record"},
    {"CLAIM_ID": "CL-06", "CLAIM": "FUN_008BD720 = lea eax,[ecx+0x18]; ret (4-byte accessor) — NOT a completion handler body", "STATUS": "CONFIRMED (NEW #1)", "EVIDENCE": "01_RAW/FUN_008BD720_DECODE.txt", "WHY_NON_CIRCULAR": "own capstone decode of raw bytes from the hash-pinned EXE; extent by terminal ret + int3 padding"},
    {"CLAIM_ID": "CL-07", "CLAIM": "The CMO ctor calls three further SF methods after FUN_005094C0: FUN_00509510, FUN_00509070, FUN_00509850", "STATUS": "CONFIRMED (NEW #2)", "EVIDENCE": "01_RAW/FUN_00528E50_CONTINUATION.txt", "WHY_NON_CIRCULAR": "raw bytes; call targets recomputed from rel32"},
    {"CLAIM_ID": "CL-08", "CLAIM": "FUN_00509850 applies the SF position/rotation/scale to the SAME-INSTANCE SF+0x30 NiNode's m_kLocal (translate+0x5C, rotation+0x38, scale+0x68)", "STATUS": "CONFIRMED (NEW #5) — recorded as SAME_INSTANCE_TRANSFORM_RELATION=CONFIRMED_STATIC (path-conditional); explicitly NOT a child binding", "EVIDENCE": "01_RAW/FUN_00509850_FULL.txt", "WHY_NON_CIRCULAR": "x87 register/stack tracing instruction-by-instruction; NiNode field layout cross-checked against slot-17 canon (m_kLocal+0x38/translate+0x5C/scale+0x68)"},
    {"CLAIM_ID": "CL-09", "CLAIM": "FUN_007BF500 (called on the SF+0x30 NiNode by FUN_00509850) performs NO children-array write and takes NO child argument — not an attach", "STATUS": "CONFIRMED (NEW #6, negative)", "EVIDENCE": "01_RAW/FUN_007BF500_DECODE.txt", "WHY_NON_CIRCULAR": "full body decode; +0xCC/+0xD4 absence measured over the whole extent"},
    {"CLAIM_ID": "CL-10", "CLAIM": "FUN_0050A310 (this=SF, called from FUN_006A3930 with the ArkModelManagerMain) installs the manager at [SF+0x20] @0x0050A3AC and calls NiNode vtable slot 41 on [SF+0x30] with (FUN_006C66D0(manager) result, 0) @0x0050A3F7", "STATUS": "CONFIRMED (NEW #7, bytes)", "EVIDENCE": "01_RAW/FUN_0050A310_DECODE.txt; 01_RAW/FUN_006A3930_CHAIN_REPIN.txt", "WHY_NON_CIRCULAR": "raw bytes both sides of the edge; the SF receiver provenance chain byte-pinned ([ACLD+0x18] <- FUN_005247C0 result; esi=SF; [esi+0x30])"},
    {"CLAIM_ID": "CL-11", "CLAIM": "FUN_007B5810 (NiNode vtable slot 41) = NiNode::AttachChild counterpart (NULL-guard + refcount pair + children-array insertion + zero-destroy protocol)", "STATUS": "STRONGLY_SUPPORTED (NEW #8, oracle byte proof; NOT CONFIRMED — engine generation not era-exact; FUN_007BF470 body undecoded)", "EVIDENCE": "01_RAW/FUN_007B5810_ORACLE_BYTE_PROOF.txt", "WHY_NON_CIRCULAR": "the fingerprint prediction comes from the externally-pinned Gb12 source (identity re-measured MATCH vs the earlier research); the PCG side is measured from EXE bytes; children-array offsets cross-checked against the independently established slot-17 canon"},
    {"CLAIM_ID": "CL-12", "CLAIM": "PROOF B (EXACT_PARENT) at CAND-4: the join-site parent receiver is the exact [SF+0x30] NiNode of the examined ACLD-path SF instance", "STATUS": "CONFIRMED (scoped: the ACLD-path instance; NOT the SF-island CMO instance)", "EVIDENCE": "01_RAW/FUN_0050A310_DECODE.txt @0x0050A3E9; 01_RAW/FUN_006A3930_CHAIN_REPIN.txt", "WHY_NON_CIRCULAR": "receiver register provenance byte-traced: [ACLD+0x18]->ecx->esi->[esi+0x30]->ecx at the virtual dispatch"},
    {"CLAIM_ID": "CL-13", "CLAIM": "PROOF A (CHILD_PROVENANCE) at CAND-4: the child's model/resource origin", "STATUS": "UNRESOLVED (FUN_006C66D0 undecoded — budget boundary 8/8; the manager's model-resource provenance untraced)", "EVIDENCE": "budget boundary; 01_RAW/FUN_0050A310_DECODE.txt shows the child = FUN_006C66D0(manager) result", "WHY_NON_CIRCULAR": "no claim made beyond the measured getter call; the boundary is recorded as the run's primary open edge"},
    {"CLAIM_ID": "CL-14", "CLAIM": "PROOF D (VISUAL_ROLE) at CAND-4: the child's visual/model role", "STATUS": "UNRESOLVED", "EVIDENCE": "none produced (budget); the child receives NiMain-cluster calls FUN_007BF900/FUN_007BF630 after the join (noted, undecoded)", "WHY_NON_CIRCULAR": "no role inferred from names/labels per binding constraints"},
    {"CLAIM_ID": "CL-15", "CLAIM": "INSTANCE_MODEL_NODE_JOIN (the run's question)", "STATUS": "NOT_ESTABLISHED", "EVIDENCE": "A=UNRESOLVED, B=CONFIRMED(scoped), C=STRONGLY_SUPPORTED, D=UNRESOLVED — the status algebra does not average up", "WHY_NON_CIRCULAR": "each component provenance separately byte-measured or explicitly left unresolved"},
    {"CLAIM_ID": "CL-16", "CLAIM": "RUNTIME_JOIN_OBSERVED", "STATUS": "NO (always, static-only run)", "EVIDENCE": "n/a", "WHY_NON_CIRCULAR": "the client never ran"},
    {"CLAIM_ID": "CL-17", "CLAIM": "WORLD_XYZ_RECOVERED", "STATUS": "NO", "EVIDENCE": "n/a", "WHY_NON_CIRCULAR": "unchanged governance status"},
    {"CLAIM_ID": "CL-18", "CLAIM": "STATIC_BUILDING_CHANNEL", "STATUS": "NOT_ESTABLISHED", "EVIDENCE": "n/a", "WHY_NON_CIRCULAR": "unchanged governance status"},
    {"CLAIM_ID": "CL-19", "CLAIM": "HISTORICAL_INSTANCE_DATA_RECOVERED", "STATUS": "NO", "EVIDENCE": "n/a", "WHY_NON_CIRCULAR": "unchanged governance status"},
    {"CLAIM_ID": "CL-20", "CLAIM": "CANONICAL_GATE_EFFECT / NEXT_EXPERIMENT_AUTHORIZED", "STATUS": "NONE / NO", "EVIDENCE": "n/a", "WHY_NON_CIRCULAR": "unchanged governance status"},
]
write_csv(os.path.join(PKG, "CLAIM_MATRIX.csv"), MH, claim_rows)

# ---------------- schema validation ----------------
results = {}
for path, hdr in [(os.path.join(PKG, "FUNCTION_BUDGET.csv"), FH),
                  (os.path.join(PKG, "EDGE_LEDGER.csv"), EH),
                  (os.path.join(PKG, "CANDIDATE_LEDGER.csv"), CH),
                  (os.path.join(PKG, "CLAIM_MATRIX.csv"), MH)]:
    errs = validate_csv(path, hdr)
    results[os.path.basename(path)] = {"errors": errs, "pass": len(errs) == 0}
    print(os.path.basename(path), "PASS" if not errs else f"FAIL {errs}")

# duplicate candidate ids
with open(os.path.join(PKG, "CANDIDATE_LEDGER.csv"), encoding="utf-8", newline="") as f:
    rd = csv.DictReader(f)
    ids = [r["CANDIDATE_ID"] for r in rd]
dups = [x for x in set(ids) if ids.count(x) > 1]
print("candidate id duplicates:", dups if dups else "NONE")

with open(os.path.join(PKG, "03_SCRIPTS", "ledger_build_results.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump({"schema_validation": results, "candidate_id_duplicates": dups}, f, indent=2)
    f.write("\n")
print("done")
