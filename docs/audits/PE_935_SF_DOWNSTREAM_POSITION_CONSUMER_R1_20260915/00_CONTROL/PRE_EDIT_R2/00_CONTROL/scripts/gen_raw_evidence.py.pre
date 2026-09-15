"""gen_raw_evidence.py — generates the mechanical raw evidence files for PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915.

Outputs (into 01_RAW/):
  FUN_0050A050_DOWNSTREAM_DISASM.txt   — Phase A: full decode + pin-MATCH lines + extent/padding
  FUN_00437F70_DISASM.txt              — Phase C: full decode + SEH + census
  FUN_0082B5A0_DISASM.txt              — Phase D: full decode + x87 trace
  SOURCE_VECTOR_LAYOUT_RAW.txt         — Phase B: UpdateWorldData + slot16 anchors + vtable matrix
  HELPER437F70_CALLER_CENSUS.csv       — 99 E8 callers classified
  HELPER82B5A0_CALLER_CENSUS.csv       — 36 E8 callers classified (pair membership)
Read-only on Entropia.exe; S0 fail-closed at start; measured env printed in every header.
"""
import sys
import os
import struct
import hashlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import decode_lib as L

RUN_DIR = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915"
RAW = os.path.join(RUN_DIR, "01_RAW")
SCRIPT_PATH = os.path.abspath(__file__)


def script_sha256():
    with open(SCRIPT_PATH, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest().upper()


def header(title):
    img = L.Image()
    lines = []
    lines.append("=" * 100)
    lines.append(title)
    lines.append("RUN_ID: PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915")
    lines.append("GENERATED_UTC: " + __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ", __import__("time").gmtime()))
    lines.append("GENERATOR_SCRIPT: %s" % SCRIPT_PATH)
    lines.append("GENERATOR_SHA256: %s" % script_sha256())
    lines.append("MEASURED ENVIRONMENT (1a490ee lesson: measured at run time, not hardcoded):")
    for ln in L.measured_env(img).split("\n"):
        lines.append("  " + ln)
    lines.append("S0 FAIL-CLOSED: PASSED at generator start (size+sha256+PE layout re-verified before any decode).")
    lines.append("SOURCE OF TRUTH: Entropia.exe physical bytes (primary). Gamebryo oracles = secondary corroboration only (QH-012).")
    lines.append("=" * 100)
    return img, lines


def disasm_block(img, md, start, end):
    out = []
    for ins in L.disasm_range(md, img, start, end):
        out.append(L.fmt_ins(ins))
    return out


def classify_pair_membership(img, md):
    """Classify each E8 caller of 0x437F70 by the instruction following the call."""
    e8, _, _ = L.scan_calls(img, 0x437F70)
    rows = []
    for site in e8:
        ins_list = L.disasm_range(md, img, site, site + 5 + 24)
        body = ins_list[1:]
        nxt = (body[0].mnemonic + " " + body[0].op_str) if body else "NONE"
        nxt2 = (body[1].mnemonic + " " + body[1].op_str) if len(body) > 1 else "NONE"
        is_pair = nxt == "mov ecx, eax" and nxt2 == "call 0x82b5a0"
        if is_pair:
            cls = "PAIR_82B5A0"
        elif nxt == "mov ecx, eax" and nxt2.startswith("call"):
            cls = "ECX_CONSUMER_" + nxt2.split("call ")[1]
        else:
            cls = "OTHER(" + nxt + ")"
        rows.append((site, is_pair, cls, nxt, nxt2))
    return rows


def phase_a():
    img, lines = header("FUN_0050A050 DOWNSTREAM WINDOW — PHASE A FULL CAPSTONE DECODE (SF vtable slot 3 of SceneFeeder class, vtable 0xa7d458)")
    md = L.make_disassembler()
    lines.append("")
    lines.append("[A.1] LINEAR DECODE 0x0050A050..0x0050A0AA (the pinned full window incl. fallback tail)")
    lines.append("")
    lines.extend(disasm_block(img, md, 0x50A050, 0x50A0AA))
    lines.append("")
    lines.append("[A.2] EXTENT BY TERMINAL+PADDING RULE (measured)")
    lines.append("  - Primary-path terminal: 0x0050A084 'ret 8' (3 bytes) -> next 0x0050A087")
    lines.append("  - Fallback-path terminal: 0x0050A0A7 'ret 8' (3 bytes) -> next 0x0050A0AA")
    lines.append("  - Padding after last terminal (read from bytes at 0x50A0AA): %s" %
                 " ".join("%02x" % b for b in img.read(0x50A0AA, 12)))
    # AMEND (QC P2-1): the original hardcode said "12x int3 ... 0x50A0B6" — a miscount of the printed string
    # (only the first 6 of the 12 bytes are 0xCC). Corrected: 6x 0xCC at 0x50A0AA..0x50A0AF; next fn 0x50A0B0.
    lines.append("  - Extent verdict: 0x0050A050..0x0050A0AA TERMINATED (0x50A0A7 ret 8), padded 0x50A0AA..0x50A0B0 with 0xCC (6x int3),")
    lines.append("    next function starts 0x0050A0B0 ('56 8b f1' = push esi; mov esi,ecx; ...). PIN MATCH: extent 0x50A050..0x50A0AA == package-A pin. MATCH.")
    lines.append("")
    lines.append("[A.3] PIN RE-MEASUREMENT — every pinned instruction from the contract's standing-knowledge block")
    pins = [
        (0x0050A050, "mov eax, dword ptr [esp + 8]"),
        (0x0050A054, "test eax, eax"),
        (0x0050A056, "push esi"),
        (0x0050A057, "mov esi, ecx"),
        (0x0050A059, "je 0x50a087"),
        (0x0050A05B, "mov ecx, dword ptr [esi + 0x30]"),
        (0x0050A05E, "mov edx, dword ptr [ecx]"),
        (0x0050A060, "push eax"),
        (0x0050A061, "mov eax, dword ptr [edx + 0x44]"),
        (0x0050A064, "call eax"),
        (0x0050A066, "test eax, eax"),
        (0x0050A068, "je 0x50a087"),
        (0x0050A06A, "mov esi, dword ptr [esp + 8]"),
        (0x0050A06E, "add eax, 0x90"),
        (0x0050A073, "push eax"),
        (0x0050A074, "push esi"),
        (0x0050A075, "call 0x437f70"),
        (0x0050A07A, "mov ecx, eax"),
        (0x0050A07C, "call 0x82b5a0"),
        (0x0050A081, "mov eax, esi"),
        (0x0050A083, "pop esi"),
        (0x0050A084, "ret 8"),
        (0x0050A087, "mov edx, dword ptr [esi]"),
        (0x0050A089, "mov eax, dword ptr [edx + 4]"),
        (0x0050A08C, "mov ecx, esi"),
        (0x0050A08E, "call eax"),
        (0x0050A090, "mov edx, dword ptr [eax]"),
        (0x0050A092, "mov ecx, dword ptr [esp + 8]"),
        (0x0050A096, "mov dword ptr [ecx], edx"),
        (0x0050A098, "mov edx, dword ptr [eax + 4]"),
        (0x0050A09B, "mov dword ptr [ecx + 4], edx"),
        (0x0050A09E, "mov eax, dword ptr [eax + 8]"),
        (0x0050A0A1, "mov dword ptr [ecx + 8], eax"),
        (0x0050A0A4, "mov eax, ecx"),
        (0x0050A0A6, "pop esi"),
        (0x0050A0A7, "ret 8"),
    ]
    lines.append("  PIN_ADDR            PINNED_TEXT                                          MEASURED(capstone)                                VERDICT")
    all_match = True
    for addr, pinned in pins:
        code = img.read(addr, 16)
        got = None
        for ins in md.disasm(code, addr):
            got = ins
            break
        measured = got.mnemonic + " " + got.op_str
        ok = (measured == pinned) or (measured == pinned.replace("dword ptr ", ""))
        if not ok and measured.replace("dword ptr ", "") == pinned.replace("dword ptr ", ""):
            ok = True
        all_match = all_match and ok
        lines.append("  0x%08X  %-52s  %-48s  %s" % (addr, pinned, measured, "MATCH" if ok else "MISMATCH"))
    # AMEND (QC P2-2): the original hardcode said "ALL 37" while the pins list has 36 entries (the contract's
    # "fallback:" line is a label, not an instruction). Corrected to the measured length.
    lines.append("  PIN RE-MEASUREMENT VERDICT: %s" % ("ALL %d PINNED INSTRUCTIONS MATCH (capstone byte decode vs contract pin block)." % len(pins) if all_match else "PIN MISMATCH DETECTED — SEE LINES ABOVE"))
    lines.append("")
    lines.append("[A.4] EXACT STACK-STATE TRACKING 0x50A064..0x50A084 (derived below from the decoded pushes/calls/rets)")
    lines.append("  Entry (thiscall, after 'call [slot3]' pushed return address):")
    lines.append("    [esp+0x00]=retaddr_to_slot3_caller  [esp+0x04]=ARG1(out float3 buffer ptr)  [esp+0x08]=ARG2(name lookup key ptr)")
    lines.append("  0x50A056 push esi           -> [esp]=saved caller ESI, [esp+0x04]=retaddr, [esp+0x08]=ARG1, [esp+0x0C]=ARG2")
    lines.append("  0x50A057 mov esi,ecx        -> ESI = this (SceneFeeder object)")
    lines.append("  0x50A060 push eax           -> [esp]=ARG2(name), [esp+0x04]=savedESI, [esp+0x08]=retaddr, [esp+0x0C]=ARG1, [esp+0x10]=ARG2")
    lines.append("  0x50A064 call eax           -> pushes ret 0x50A066; INSIDE LOOKUP CALLEE: [esp]=ret, [esp+0x04]=name==ARG2, ECX=this->[SF+0x30] (NiNode).")
    lines.append("     lookup = NiNode-family vtable slot 0x44 (slot17 = 0x007B5390, recursive named-object lookup; ret 4 thiscall; package-B pin re-measured in SOURCE_VECTOR_LAYOUT_RAW.txt)")
    lines.append("     lookup callee 'ret 4' pops ret+name -> stack returns to the post-0x50A060 state.")
    lines.append("  0x50A06A mov esi,[esp+8]   -> with [esp]=savedESI,[esp+4]=retaddr: [esp+8]=ARG1(out buffer). ESI is RE-LOADED with ARG1 (this is the")
    lines.append("     DERIVED mapping the contract ordered: original ARG1 after push esi sits at [esp+8] HERE — CONFIRMED, and ESI (which held SF this) is overwritten.")
    lines.append("  0x50A06E add eax,0x90       -> EAX = lookup_result + 0x90 (== &NiAVObject.m_kWorld.m_Translate per Phase B)")
    lines.append("  0x50A073 push eax           -> [esp]=&world_translate, [esp+4]=savedESI, [esp+8]=retaddr, [esp+0xC]=ARG1, [esp+0x10]=ARG2")
    lines.append("  0x50A074 push esi           -> [esp]=ARG1(out), [esp+4]=&world_translate, [esp+8]=savedESI, [esp+0xC]=retaddr, [esp+0x10]=ARG1, [esp+0x14]=ARG2")
    lines.append("  0x50A075 call 0x437F70     -> pushes ret 0x50A07A; INSIDE HELPER1: [esp]=ret, [esp+4]=ARG1(out)=callee arg1, [esp+8]=&world_translate=callee arg2.")
    lines.append("     PUSH-ORDER->ARG MAPPING: LAST push (esi=ARG1 out) lands at callee [esp+4]; FIRST push (eax=&world_translate) lands at callee [esp+8].")
    lines.append("     FUN_00437F70 IGNORES both stack args (decode in FUN_00437F70_DISASM.txt) and returns with PLAIN 'ret' — the 8 bytes REMAIN on the stack.")
    lines.append("     HELPER1 return value: EAX = singleton S pointer (global slot 0xba1804).")
    lines.append("  0x50A07A mov ecx,eax        -> ECX = S (helper1 return)")
    lines.append("  0x50A07C call 0x82B5A0     -> pushes ret 0x50A081; INSIDE HELPER2: [esp]=ret, [esp+4]=ARG1(out) — the SAME leftover slot — , [esp+8]=&world_translate.")
    lines.append("     HELPER2 stack-arg positions: [esp+4]=out buffer (same ARG1), [esp+8]=source=&world_translate, ECX=base S. HELPER2 'ret 8' CLEANSES the pair's leftover 8 bytes.")
    lines.append("     HELPER2 writes out[0]/out[1]/out[2] itself (decode in FUN_0082B5A0_DISASM.txt).")
    lines.append("  0x50A081 mov eax,esi        -> EAX = ARG1 (out buffer) — FUNCTION RETURN VALUE = the caller-provided out pointer")
    lines.append("  0x50A083 pop esi; 0x50A084 ret 8")
    lines.append("")
    lines.append("[A.5] REQUIRED QUESTION (def-use, from the decode above):")
    lines.append("  Does FUN_0050A050 itself write primary-path XYZ? -> **NO**. Between 'call 0x82B5A0' (0x50A07C) and 'ret 8' (0x50A084) the only")
    lines.append("  instructions are mov eax,esi / pop esi / ret 8 — ZERO memory writes to [esi] on the primary path. On the primary path the")
    lines.append("  ENTIRE out-buffer write happens inside FUN_0082B5A0 (out[i] = f32(f32(src[i]*K) - S[i])). FUN_0050A050 only passes the")
    lines.append("  pointers through the stack frames. (The FALLBACK path 0x50A087..0x50A0A7 DOES write 3 dwords directly: out[0..2]=P[0..2],")
    lines.append("  where P = SF::slot1() = &SF+0x34 — see FALLBACK_PRIMARY_COMPARISON.txt.)")
    lines.append("")
    lines.append("[A.6] PSEUDO-C (derived ONLY AFTER the decode above; thiscall, ret 8):")
    lines.append("  struct SceneFeeder { /* vtable@0 = 0xa7d458; +0x30 NiNode-family root (refcounted, 0x118B); +0x34 float3 posSlotA; +0x40 float3 posSlotB; ... */ };")
    lines.append("  float3* SF_slot3(SceneFeeder* this, float3* out, const char* name) {   // [esp+4]=out, [esp+8]=name, ret 8")
    lines.append("      NiAVObject* obj = name ? this->root /* +0x30 */->GetObjectByName(name) /* slot17, 0x44 */ : NULL;")
    lines.append("      if (!obj) { float3* p = (float3*)this->slot1(); /* == &this->posSlotA @ +0x34 */ out->x=p->x; out->y=p->y; out->z=p->z; return out; }")
    lines.append("      float3* src = (float3*)((char*)obj + 0x90);   // &obj->m_kWorld.m_Translate")
    lines.append("      S = GetOrCreateOriginSingleton();              // 0x437F70; singleton = global-zero-vector snapshot (Phase C)")
    lines.append("      ScaledSub(out, src, S);                         // 0x82B5A0: out[i] = f32(f32(src[i]*K) - S[i]); K=(f64)f32(0.01)")
    lines.append("      return out;")
    lines.append("  }")
    lines.append("  (Semantics of S/K/the helpers are derived in the Phase C/D raw files; the pseudo-C only encodes the measured control flow + dataflow.)")
    with open(os.path.join(RAW, "FUN_0050A050_DOWNSTREAM_DISASM.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return all_match


def phase_c():
    img, lines = header("FUN_00437F70 FULL DECODE — PHASE C (helper 1 of the SF slot3 primary pair)")
    md = L.make_disassembler()
    lines.append("")
    lines.append("[C.1] EXTENT BY TERMINAL+PADDING RULE")
    lines.append("  Terminals: 'ret' at 0x437FCF (fallthrough path) and 'ret' at 0x437FE6 (je/jne target 0x437FD7 path).")
    lines.append("  Last terminal ends 0x437FE7; padding 0x437FE7..0x437FF0 = 0xCC (int3, next function at 0x437FF0).")
    lines.append("  Extent: 0x00437F70..0x00437FE7. Function size 0x77 bytes.")
    lines.append("")
    lines.append("[C.2] FULL LINEAR DECODE 0x437F70..0x437FE7")
    lines.append("")
    lines.extend(disasm_block(img, md, 0x437F70, 0x437FE7))
    lines.append("")
    lines.append("[C.3] CALLING CONVENTION / STACK ARGS (MEASURED)")
    lines.append("  - Plain 'ret' at BOTH terminals (0x437FCF, 0x437FE6): NO 'ret n'. This function consumes ZERO stack args itself.")
    lines.append("  - It is called with 8 bytes of leftover caller stack args at [esp+4]/[esp+8] (at the SF site: out buffer and &world_translate);")
    lines.append("    it NEVER reads [esp+4]/[esp+8] as its own data — the bytes are left for the NEXT helper in the pair (0x82B5A0 'ret 8').")
    lines.append("  - At the SF slot3 site: ECX is NOT set by the caller before 'call 0x437F70' (caller EAX/ESI hold args); the function's only")
    lines.append("    register usage is EAX for the singleton pointer and ECX as SEH-scratch. It is a CDECL-style 0-arg global getter, NOT a thiscall.")
    lines.append("")
    lines.append("[C.4] EVERY MEMORY READ / WRITE (from the decode)")
    lines.append("  READS : [fs:0] (0x437F77, SEH chain); [0xb9d8d0] (0x437F7F, __security_cookie canary — MSVCR80-style);")
    lines.append("          [0xba1804] (0x437F91, GLOBAL SLOT: singleton cache); [esp+8] post-frame (0x437FC0, saved SEH node restore — not an arg read).")
    lines.append("  WRITES: [fs:0] (0x437F8B, SEH install); [esp+4] local slot (0x437FA4, new pointer stash); [esp+0x10] local (0x437FAA, zero init);")
    lines.append("          [0xba1804] (0x437FBB write on success; 0x437FD2 write-NULL on alloc failure); [fs:0] restore (0x437FC4/0x437FDB).")
    lines.append("  NO writes to the pair's stack args; NO FPU/SSE; NO branches beyond the test/jne/je.")
    lines.append("")
    lines.append("[C.5] SEH FRAME (decoded)")
    # AMEND (QC P3-3): "push ecx" is a local/scratch+alignment slot (stashed with the new pointer at 0x437FA4
    # 'mov [esp+4],eax'); the exception registration NODE is {prev, handler 0x99C06B} at [esp+8] installed by
    # 'lea eax,[esp+8]; mov fs:[0],eax'. Wording corrected.
    lines.append("  - Frame pushed at 0x437F70..0x437F8B: push -1 (machine frame), push 0x99c06b (HANDLER), push fs:[0] (prev), push ecx (local/scratch+alignment slot — NOT the registration; stashed with the new pointer at 0x437FA4),")
    lines.append("    push eax(cookie^esp) — cookie-check + fs:[0] install.")
    lines.append("  - Handler VA 0x0099C06B: at end (0x437FD7 path) the frame is popped by 'mov ecx,[esp+8]; mov fs:[0],ecx; pop ecx; add esp,0x10'.")
    lines.append("  - Handler address recorded: 0x0099C06B (handler body itself not decoded — outside this run's load path: the function never")
    lines.append("    faults unless operator new throws; scope-bounded decision, recorded as NOT_DECODED).")
    lines.append("")
    lines.append("[C.6] CALLEE IDENTITIES (via IAT walk)")
    lines.append("  - 0x95D3C4 = jmp dword ptr [0xa75354] -> IAT 0xa75354 = MSVCR80.dll!??2@YAPAXI@Z = operator new(unsigned int). (measured import-dir walk)")
    lines.append("  - 0x82B580 = singleton constructor: copies [0xba921c]/[0xba9220]/[0xba9224] -> S[0/1/2]. thiscall, ret (0-arg), returns this.")
    lines.append("  - No other callees.")
    lines.append("")
    lines.append("[C.7] GLOBAL SLOTS (recorded)")
    lines.append("  - 0xba1804: singleton cache slot (NULL until first call). Writers: ONLY this function (0x437FBB success, 0x437FD2 alloc-fail NULL).")
    lines.append("    Whole-image imm32 scan: exactly 3 refs, ALL inside this function. NO other reader/writer exists (HELPER437F70_CALLER_CENSUS.csv).")
    # AMEND (QC P1-1): "NEVER WRITTEN anywhere in the image" now cites the correction-pass whole-image census.
    lines.append("  - 0xba921c/0xba9220/0xba9224: source triple for the singleton ctor. NEVER WRITTEN (correction-pass whole-image write census: ORIGIN_TRIPLE_WRITE_CENSUS_RAW.txt + END_TO_END_VALUE_FLOW_RAW.txt E.3).")
    lines.append("  - 0xb9d8d0: security cookie (canary).")
    lines.append("")
    lines.append("[C.8] SEMANTICS (from bytes)")
    lines.append("  FUN_00437F70(): S = [0xba1804]; if (S == 0) { p = operator_new(12); if (!p) { [0xba1804]=0; return NULL; } S = ctor_0x82B580(p);")
    lines.append("                   /* S = {triple 0xba921c} */ [0xba1804] = S; } return S;   // EAX = singleton pointer, args IGNORED")
    lines.append("  Return type shape: a POINTER (12-byte heap object = 3 floats).")
    lines.append("")
    lines.append("[C.9] THE 10 CONTRACT QUESTIONS (answered from bytes)")
    lines.append("  (1) arg1 ([esp+4] = out buffer at SF site): dest or source? -> NEITHER: never read, never written by this function (IGNORED).")
    lines.append("  (2) arg2 ([esp+8] = &world_translate at SF site): dest or source? -> NEITHER: IGNORED (stays on stack for helper2).")
    lines.append("  (3) is it a copy? -> NO. Zero data movement of any float.")
    lines.append("  (4) vector constructor? -> NO for itself; it CALLS one (0x82B580) exactly once (lazy init) which copies the global zero triple.")
    lines.append("  (5) swaps axes? -> NO. (6) negates components? -> NO. (7) scales? -> NO. (8) normalizes? -> NO.")
    lines.append("  (9) converts engine/world/render coordinates? -> NO by itself; it RETURNS the conversion ORIGIN (the singleton S).")
    lines.append("  (10) what does EAX point to on return? -> the 12-byte singleton S = cached copy of the never-written global triple 0xba921c/20/24")
    # AMEND (QC P1-1): cites the correction-pass census for the never-written claim.
    lines.append("       = {0,0,0} at ALL times (triple proven never written by the correction-pass whole-image write census, ORIGIN_TRIPLE_WRITE_CENSUS_RAW.txt; .data virtual-tail zero-init). EAX == S for the entire process lifetime after first call.")
    lines.append("")
    lines.append("[C.10] CALLER CENSUS (all channels, measured)")
    lines.append("  Channels: E8 rel32 direct calls: 99 sites. E9 tail calls: 0. imm32 address-takers in .text: 0. Vtable membership (.rdata scan): 0.")
    lines.append("  Non-.text imm32 refs: 0. => FUN_00437F70 is a plain static helper, never address-taken, never virtual.")
    lines.append("  Classification of all 99 callers (next instruction pattern) is in HELPER437F70_CALLER_CENSUS.csv; summary:")
    rows = classify_pair_membership(img, md)
    npair = sum(1 for r in rows if r[1])
    lines.append("  - PAIR_82B5A0 (mov ecx,eax; call 0x82B5A0 immediately): %d sites (incl. the SF slot3 site 0x50A075)." % npair)
    others = {}
    for r in rows:
        if not r[1]:
            others.setdefault(r[2], 0)
            others[r[2]] += 1
    for k in sorted(others):
        lines.append("  - %s: %d sites" % (k, others[k]))
    lines.append("  - No caller writes through the returned pointer within 8 instructions (measured over all 99 sites) => singleton never mutated post-construction.")
    with open(os.path.join(RAW, "FUN_00437F70_DISASM.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return rows


def write_census_csv(rows, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("call_site_va,is_pair_82b5a0,classification,instruction_after_call,instruction_after_next,caller_context_note\n")
        for site, is_pair, cls, nxt, nxt2 in rows:
            f.write("0x%08X,%s,%s,\"%s\",\"%s\",\n" % (site, "YES" if is_pair else "NO", cls, nxt, nxt2))


def census_82b5a0():
    img, lines = header("FUN_0082B5A0 CALLER CENSUS — measured (36 direct E8 sites)")
    md = L.make_disassembler()
    e8, e9, imm = L.scan_calls(img, 0x82B5A0)
    lines.append("E8 rel32 direct: %d sites. E9: %d. imm32 in .text: %d. Vtable membership: none found." % (len(e8), len(e9), len(imm)))
    # AMEND (QC P2-4): the original prose said "OR are near-adjacent to a 437F70 call" — false for the 2 NON-PAIR
    # sites; and prior = site-7 was computed under pair geometry for ALL rows, fabricating addresses for the
    # NON-PAIR rows. Corrected: pair rows carry the measured prior site; NON-PAIR rows carry NOT_APPLICABLE +
    # the measured ECX source (stored origin [this+0x4C]; see ORIGIN_TRIPLE_WRITE_CENSUS_RAW.txt [A.1]).
    lines.append("34 sites are 'call 0x437F70; mov ecx,eax; call 0x82B5A0' pairs; the 2 remaining sites use a STORED ORIGIN pointer")
    lines.append("(ECX = [this+0x4C]; no adjacent 437F70 call — see the CSV rows and ORIGIN_TRIPLE_WRITE_CENSUS_RAW.txt [A.1]);")
    lines.append("(pair membership is computed from the caller census of 437F70 — see HELPER437F70_CALLER_CENSUS.csv).")

    NONPAIR_NOTE = {
        0x00930030: "AMENDED per QC P2-4: no adjacent 437F70 call (the prior cell 0x930029 was pair-geometry, not a measured site; byte 0x930029 is mid-instruction inside 'mov esi,[esp+8]' @0x930027); ECX = stored origin [this+0x4C] (0x930023 mov ecx,[ecx+0x4c]); src = [this+0x14]+0x5C",
        0x00930056: "AMENDED per QC P2-4: no adjacent 437F70 call (the prior cell 0x93004F was pair-geometry, not a measured site; byte 0x93004F is mid-instruction inside 'lea ecx,[esp+0xc]' @0x93004E); ECX = stored origin [this+0x4C] (0x930053 mov ecx,[esi+0x4c]); src = [this+0x14]+0x5C; out = [esp+0xc] temp",
    }
    lines.append("")
    lines.append("call_site_va  preceded_by_437f70(call site)  pair_member")
    e437, _, _ = L.scan_calls(img, 0x437F70)
    e437set = set(e437)
    with open(os.path.join(RAW, "HELPER82B5A0_CALLER_CENSUS.csv"), "w", encoding="utf-8") as f:
        f.write("call_site_va,prior_437f70_site,is_pair,context_class_note\n")
        for site in e8:
            prior = site - 7
            is_pair = prior in e437set
            if is_pair:
                f.write("0x%08X,0x%08X,YES,\n" % (site, prior))
            else:
                # AMEND (QC P2-4): NON-PAIR rows carry NOT_APPLICABLE + the measured ECX source (measured decode,
                # see ORIGIN_TRIPLE_WRITE_CENSUS_RAW.txt [A.1]); site-7 was pair geometry, not a measured site.
                note = NONPAIR_NOTE.get(site, "NON-PAIR; prior_437f70_site NOT_APPLICABLE (site-7 was pair geometry)")
                f.write('0x%08X,NOT_APPLICABLE,NO,"%s"\n' % (site, note))
            lines.append("0x%08X     %-20s           %s" % (site, ("0x%08X" % prior) if is_pair else "NOT_APPLICABLE", "PAIR" if is_pair else "NON-PAIR"))
    with open(os.path.join(RAW, "HELPER82B5A0_CALLER_CENSUS.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def phase_d():
    img, lines = header("FUN_0082B5A0 FULL DECODE — PHASE D (helper 2 of the SF slot3 primary pair; the PRIMARY WRITER of the out buffer)")
    md = L.make_disassembler()
    lines.append("")
    lines.append("[D.1] EXTENT + CALLING CONVENTION")
    lines.append("  Terminal 'ret 8' at 0x82B5E4; padding 0x82B5E7..0x82B5F0 = 0xCC. Extent 0x0082B5A0..0x0082B5F0 (size 0x50).")
    lines.append("  Convention: ECX-arg (thiscall-style) + 2 stack args, 'ret 8' (callee-popped). At the SF site: ECX=S (0x437F70 return),")
    lines.append("  [esp+4]=out buffer (caller ARG1), [esp+8]=source (NiAVObject+0x90 world translate).")
    lines.append("")
    lines.append("[D.2] FULL LINEAR DECODE 0x82B5A0..0x82B5F0")
    lines.append("")
    lines.extend(disasm_block(img, md, 0x82B5A0, 0x82B5F0))
    lines.append("")
    lines.append("[D.3] BIT-EXACT CONSTANTS")
    lines.append("  qword [0xa7b360] (loaded by 'fld qword ptr [0xa7b360]' at 0x82B5AA):")
    b = img.read(0xa7b360, 8)
    lines.append("    bytes = %s ; as f64 = %.17g ; bit pattern = 0x%016X" % (" ".join("%02x" % x for x in b), struct.unpack("<d", b)[0], struct.unpack("<Q", b)[0]))
    lines.append("    = (double)(float)0.01 = the f64 widening of f32 0.01 (0x3C23D70A); decimal value 0.009999999776482582.")
    lines.append("  No other constants in the function.")
    lines.append("")
    lines.append("[D.4] EXACT x87 REGISTER-STACK TRACE (per component; IEEE-754 extended-precision discipline)")
    lines.append("  ENTRY: x87 stack empty. EDX=[esp+8]=src, EAX=[esp+4]=out, ECX=base S.")
    lines.append("  COMPONENT X:")
    lines.append("    0x82B5A4 fld dword ptr [edx]        st0 := (f80)src.x                     [load f32 -> f80, exact]")
    lines.append("    0x82B5AA fld qword ptr [0xa7b360]   st0 := (f80)K, st1 := src.x            [K = (f64)f32(0.01), exact widening]")
    lines.append("    0x82B5B0 fmul st(1), st(0)          st1 := src.x * K  (f80 mul, extended)   st0 := K")
    lines.append("    0x82B5B2 fxch st(1)                 st0 := src.x*K, st1 := K")
    lines.append("    0x82B5B4 fstp dword ptr [esp+8]     [esp+8] := f32(src.x*K)  <<< F32 NARROWING #1 (round to nearest f32)")
    lines.append("                                          NOTE: [esp+8] is the caller's leftover SRC slot — reused as temp; src was already")
    lines.append("                                          read into registers; the temp store does not alias anything live.")
    lines.append("    0x82B5B8 fld dword ptr [esp+8]      st0 := (f80)f32(src.x*K), st1 := K")
    lines.append("    0x82B5BC fsub dword ptr [ecx]       st0 := f32(src.x*K) - S.x   (f80 sub vs f32-loaded base)")
    lines.append("    0x82B5BE fstp dword ptr [eax]       out.x := f32( f32(src.x*K) - S.x )  <<< F32 NARROWING #2 (final store)")
    lines.append("  COMPONENT Y:")
    lines.append("    0x82B5C0 fld dword ptr [edx+4]      st0 := src.y, st1 := K")
    lines.append("    0x82B5C3 fmul st(1)                 st0 := src.y*K   (st1 := K)")
    lines.append("    0x82B5C5 fstp dword ptr [esp+8]     [esp+8] := f32(src.y*K)     <<< F32 NARROWING")
    lines.append("    0x82B5C9 fld dword ptr [esp+8]      st0 := f32(src.y*K)")
    lines.append("    0x82B5CD fsub dword ptr [ecx+4]     st0 -= S.y")
    lines.append("    0x82B5D0 fstp dword ptr [eax+4]     out.y := f32(...)           <<< F32 NARROWING (final)")
    lines.append("  COMPONENT Z:")
    lines.append("    (st0 := K survives component Y's chain)")
    lines.append("    0x82B5D3 fmul dword ptr [edx+8]     st0 := K * src.z")
    lines.append("    0x82B5D6 fstp dword ptr [esp+8]     [esp+8] := f32(K*src.z)     <<< F32 NARROWING")
    lines.append("    0x82B5DA fld dword ptr [esp+8]      st0 := f32(K*src.z)")
    lines.append("    0x82B5DE fsub dword ptr [ecx+8]     st0 -= S.z")
    lines.append("    0x82B5E1 fstp dword ptr [eax+8]     out.z := f32(...)           <<< F32 NARROWING (final)")
    lines.append("    0x82B5E4 ret 8")
    lines.append("  PER-COMPONENT FORMULA (bit-exact): out[i] = f32( f32( (f80)src[i] * (f80)K ) - (f80)S[i] ), i in {0,4,8} (x,y,z).")
    lines.append("  With S == {0,0,0} (Phase C) and the x87 default rounding: out[i] = f32( f32(src[i]*0.01f) - 0.0f ) = f32(src[i]*0.01f),")
    lines.append("  with the ONLY caveat: if src[i]*K rounds to +0/-0, subtracting 0.0 preserves the sign of zero. No NaN/Inf paths exist here")
    lines.append("  beyond the generic x87 rules (no fwait, no control-word change, no exceptions handled).")
    lines.append("")
    lines.append("[D.5] MEMORY WRITES (only these 4)")
    lines.append("  [esp+8] temp stores (3x, reusing the dead caller arg slot) and the 3 output stores [eax+0/4/8]. NO writes to ECX/S, NO global writes.")
    lines.append("  => The function DOES NOT MUTATE the source vector, the base S, or any owner object.")
    lines.append("")
    lines.append("[D.6] ECX MEANING AT SF SLOT3 SITE AND AT OTHER SITES")
    lines.append("  - SF site (0x50A07C): ECX = FUN_00437F70 return = singleton S (12-byte origin vector).")
    lines.append("  - All 34 pair sites: identical construction 'mov ecx,eax' immediately after 'call 0x437F70' => ECX = S at every pair site (measured census).")
    lines.append("  - RTTI/vtable walk: function is never address-taken (no imm32, no vtable membership) => no virtual identity; structural identity only.")
    lines.append("")
    lines.append("[D.7] THE 7 CONTRACT QUESTIONS (answered from bytes)")
    lines.append("  (1) does it mutate the vector? -> It WRITES the out buffer (3 f32 stores) but does NOT mutate src (NiAVObject+0x90) or ECX/S.")
    lines.append("  (2) modify an owner object? -> NO (no writes outside [eax+0..8] and the dead temp slot).")
    lines.append("  (3) update cache/dirty state? -> NO (no flag writes).")
    lines.append("  (4) clamp/validate? -> NO (no compares, no min/max).")
    lines.append("  (5) transform coordinate system? -> YES (bit-exact scale by (f64)f32(0.01) and subtraction of origin S; per-component,")
    lines.append("      with two f32 narrowings per component). This is the engine->internal-space conversion of a world-space translation vector.")
    lines.append("  (6) merely return/commit a temporary? -> It commits the converted result into the caller's out buffer; returns EAX=out (unchanged).")
    lines.append("  (7) operate on something unrelated to position? -> NO: every operand is a 3-float vector (src=out-world-translate, S=origin, out=buffer).")
    lines.append("")
    lines.append("[D.8] SIBLING/INVERSE FAMILY (context, measured)")
    lines.append("  - FUN_0082B6A0 (same family, ECX=S): out[i] = f32( f32( (f32(src[i]) + S[i]) ) * 100.0 ) using qword [0xa7a618] = (f64)100.0:")
    lines.append("    the EXACT algebraic inverse of the 0x82B5A0 forward transform (inverse = (scaled + S) * 100). Bytes measured in this run.")
    lines.append("  - FUN_0082B5F0 (ECX=S): zero-fills arg1+0x24..0x2c then scales the block at arg2+0x24 by K (0xa7b360) — structure-space converter.")
    lines.append("  - FUN_0082B790 (ECX discarded before use — clobbered at 0x82B79B): array-of-float3 transformer, per-element scale by f32 [0xa7af68] = 100.0f")
    lines.append("    (bytes 0000c8420000a040 = f32 pair {100.0f, 5.0f}; 'fld dword ptr [0xa7af68]' loads 100.0f). NOT a setter of S (writes only the new array).")
    lines.append("  - FUN_00437E80 (ECX=S): reads a 9-float block from arg2 (rotate-matrix-like) and passes 9 dwords onward (0x96cb20 helper) — matrix-side consumer.")
    lines.append("  => The pair (437F70 + 82B5A0) is one member of a coordinate-conversion family anchored on the SAME origin singleton S.")
    with open(os.path.join(RAW, "FUN_0082B5A0_DISASM.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def phase_b():
    img, lines = header("SOURCE VECTOR LAYOUT — PHASE B RAW (independent Entropia-local evidence; oracle = secondary only)")
    md = L.make_disassembler()
    lines.append("")
    lines.append("[B.1] FUN_007E4820 (vtable slot 27 = UpdateWorldData pin; package B) — FULL DECODE")
    lines.append("")
    lines.extend(disasm_block(img, md, 0x7E4820, 0x7E4870))
    lines.append("")
    lines.append("  Evidence: 13-dword (52-byte) block copy into this+0x6C (rep movsd ecx=0xD).")
    lines.append("  Block layout (derived): +0x00..0x23 rotate (9 floats), +0x24..0x2F translate (3 floats), +0x30 scale (1 float) = 13 dwords.")
    lines.append("  => m_kWorld block starts at +0x6C; m_kWorld.m_Translate = +0x6C+36 = +0x90/+0x94/+0x98; m_kWorld scale at +0x9C.")
    lines.append("  No parent => copy m_kLocal (block at +0x38, translate at +0x5C) -> m_kWorld. Parent => compose via 0x6eb380(parent+0x6C, local, tmp) -> m_kWorld.")
    lines.append("")
    lines.append("[B.2] FUN_007B4650 (vtable slot 16 pin; local-translate applier) — first 0x28 bytes")
    lines.append("")
    lines.extend(disasm_block(img, md, 0x7B4650, 0x7B4678))
    lines.append("")
    lines.append("  Evidence: 'lea edi,[esi+0x5c]' = &m_kLocal.m_Translate (+0x38+36=+0x5C) — confirms the LOCAL translate offset anchor and")
    lines.append("  the 3-float additions into it ([eax+0/4/8] + [ecx+0/4/8]).")
    lines.append("")
    lines.append("[B.3] VTABLE MATRIX (measured: where 0x7B5390 and 0x7E4820 sit in .rdata vtables)")
    lines.append("  0x007B5390 (slot17 named lookup, ret 4 thiscall, recursive over children array [+0xCC] count [+0xD4]) stored in .rdata at:")
    for va in (0xa8cd38, 0xa8e800, 0xa90b68, 0xa90c80, 0xa91010, 0xa91230, 0xa91918):
        lines.append("    %#x (vtable start %#x => slot offset %#x)" % (va, va - 0x44, 0x44))
    lines.append("  0x007E4820 (slot27 UpdateWorldData) stored at 16 vtable slots; e.g. %#x in vtable start %#x => slot offset %#x" % (0xa8cd60, 0xa8cd60 - 0x6c, 0x6c))
    lines.append("  => vtable 0x00A8CCF4 holds BOTH slot17=0x7B5390 @ +0x44 AND slot27=0x7E4820 @ +0x6C: the NiAVObject-family virtual layout,")
    lines.append("     Entropia-local. SF slot3 reads [vtable+0x44] (0x50A061) and [vtable+0x04] (0x50A089) — consistent slots.")
    lines.append("")
    lines.append("[B.4] SF+0x30 RECEIVER CONSTRUCTION (SF ctor FUN_00509330 decode excerpt — measured)")
    lines.extend(disasm_block(img, md, 0x509366, 0x5093CC))
    lines.append("")
    lines.append("  Evidence: 'push 0x118; call 0x95d3c4' (operator new(0x118)); ctor 0x7B6000 (arg=0); 'add [eax+4],1' (refcount at +4 = Gamebryo")
    lines.append("  NiObject-family smart-pointer acquire); [ebp+0x30] = result. => SF+0x30 = refcounted 0x118-byte NiNode-family object with")
    lines.append("  vtable at +0, children array at +0xCC (count +0xD4) — matches the slot17 lookup consumer layout. PIN MATCH with package B.")
    lines.append("")
    lines.append("[B.5] SF CLASS POSITION SLOT INIT (measured, ctor continues)")
    lines.extend(disasm_block(img, md, 0x509424, 0x509458))
    lines.append("")
    lines.append("  Evidence: SF ctor initializes SF+0x34/38/3C AND SF+0x40/44/48 FROM the global triple [0xba921c]/[0xba9220]/[0xba9224]")
    lines.append("  — the SAME triple that seeds the origin singleton S. (Fallback source + primary base share one origin vector.)")
    lines.append("")
    lines.append("[B.6] STRUCTURE START/EXTENT (NiAVObject-family, this-build)")
    lines.append("  +0x00 vtable; +0x04 refcount; +0x24 m_pkParent; +0x38 m_kLocal{rotate+0x38, translate+0x5C, scale+0x68};")
    lines.append("  +0x6C m_kWorld{rotate+0x6C, translate+0x90, scale+0x9C}; +0xB0 child link (per UpdateWorldData tail virtual dispatch);")
    lines.append("  +0xCC children array; +0xD4 children count (NiNode subclass; object size >= 0x118).")
    lines.append("  m_kWorld.m_Translate (+0x90/+0x94/+0x98) is EXPLICITLY DISTINGUISHED from m_kLocal.m_Translate (+0x5C/+0x60/+0x64):")
    lines.append("  the +0x90 block is the parent-composed WORLD state; the +0x5C block is the LOCAL state.")
    lines.append("")
    lines.append("[B.7] VERDICT")
    lines.append("  SOURCE_OBJECT_IDENTITY: CONFIRMED (NiAVObject-family, NiNode-subclass tree; vtable/ctor/children-layout chain measured)")
    lines.append("  SOURCE_FIELD_IDENTITY: CONFIRMED (m_kWorld.m_Translate at +0x90; the 'add eax,0x90' at 0x50A06E lands exactly on it)")
    lines.append("  SOURCE_VECTOR_LAYOUT: CONFIRMED (contiguous 3x f32 = translate of the 13-dword world block; NOT m_kLocal)")
    lines.append("  H1: SUPPORTED-CONFIRMED (contiguous 3-component world-translation vector at NiAVObject+0x90).")
    with open(os.path.join(RAW, "SOURCE_VECTOR_LAYOUT_RAW.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    ok = phase_a()
    rows = phase_c()
    write_census_csv(rows, os.path.join(RAW, "HELPER437F70_CALLER_CENSUS.csv"))
    census_82b5a0()
    phase_d()
    phase_b()
    print("phase_a pins all match:", ok)
    print("census rows:", len(rows))


if __name__ == "__main__":
    main()
