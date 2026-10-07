"""qc_ind_controls_replica.py — PE-MASTER-AUDITOR independent QC, part 4.

INDEPENDENT REPLICA of the four §9 controls (dispatch item 5). NOT a re-run of
the executor's qc_controls.py: the checkers below are re-implemented here
from the CONTROL_RESULTS.json predicates, using my own PE reads and my own
instruction decoding. Each control must show: clean PASS -> mutated FAIL on the
SAME checker with the correct cause. Real inputs marked POLICY_ONLY where the
rejection is evidence-absence only.
"""
import struct

EXE_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
with open(EXE_PATH, "rb") as f:
    EXE = f.read()

e_lfanew = struct.unpack_from("<I", EXE, 0x3C)[0]
coff = e_lfanew + 4
nsec = struct.unpack_from("<H", EXE, coff + 2)[0]
opt = coff + 20
opt_size = struct.unpack_from("<H", EXE, coff + 16)[0]
image_base = struct.unpack_from("<I", EXE, opt + 28)[0]
sectab = opt + opt_size
SECTIONS = []
for i in range(nsec):
    o = sectab + 40 * i
    vs, va, rs, rp = struct.unpack_from("<IIII", EXE, o + 8)
    SECTIONS.append((va, vs, rs, rp))


def rd(va, n):
    rva = va - image_base
    for v, vs, rs, rp in SECTIONS:
        if v <= rva < v + max(vs, rs):
            return EXE[rp + (rva - v):rp + (rva - v) + n]
    raise ValueError(hex(va))


def fail_closed_check(ok, label):
    print(("PASS " if ok else "FAIL ") + label)


# ------------------------------------------------------------------ CTRL_1
# The §6 evidence-leg classifier (my own implementation).
def ctrl1(ev):
    legs = [ev.get("resource_derived_contained_model", False),
            ev.get("typed_containment", False),
            ev.get("exact_wrapper_used_as_child", False),
            ev.get("positive_consumer_proof", False)]
    adj_only = ev.get("model_adjacency_only", False)
    if adj_only and not all(legs):
        return False, "REJECT_MODEL_ADJACENCY_ONLY"
    if all(legs):
        return True, "all four legs present"
    return False, "missing legs: " + str(sum(1 for l in legs if not l))


clean1 = ctrl1({"resource_derived_contained_model": True, "typed_containment": True,
                "exact_wrapper_used_as_child": True, "positive_consumer_proof": True})
mut1 = ctrl1({"model_adjacency_only": True, "object_class": "NiControllerSequence"})
real1 = ctrl1({"resource_derived_contained_model": True, "typed_containment": False,
               "exact_wrapper_used_as_child": False, "positive_consumer_proof": False})
ctrl1_ok = clean1[0] is True and mut1[0] is False and real1[0] is False and "REJECT_MODEL_ADJACENCY_ONLY" == mut1[1]
fail_closed_check(ctrl1_ok,
                  "QC-J1-CTRL_1-replica: clean PASS + adjacency-only(NiControllerSequence) FAIL "
                  f"+ real child FAIL (missing 3 legs -> POLICY_ONLY evidence-absence) on MY OWN classifier: "
                  f"clean={clean1}, mut={mut1}, real={real1}")

# ------------------------------------------------------------------ CTRL_2
# Containment predicate: the writer's STORE must target the declared child-field
# offset (+0x68 of ESI) and the source READ must be [eax+4]. My own byte decode.
def ctrl2(store_va, read_va):
    sb = rd(store_va, 3)
    rb = rd(read_va, 3)
    # store: 89 /r -> mov r/m32, r32; ModRM mod=01 reg rm=ESI; disp8 == 0x68
    store_ok = (sb[0] == 0x89 and (sb[1] >> 6) == 1 and (sb[1] & 7) == 6 and sb[2] == 0x68)
    # read: 8B /r -> mov r32, r/m32; ModRM mod=01 reg=EDI rm=EAX; disp8 == 4
    read_ok = (rb[0] == 0x8B and (rb[1] >> 6) == 1 and ((rb[1] >> 3) & 7) == 7 and (rb[1] & 7) == 0 and rb[2] == 4)
    return store_ok and read_ok, f"store@0x{store_va:08X}={'OK' if store_ok else 'BAD'}({' '.join('%02X' % x for x in sb)}); read@0x{read_va:08X}={'OK' if read_ok else 'BAD'}({' '.join('%02X' % x for x in rb)})"


clean2 = ctrl2(0x006C67E2, 0x006C67BE)   # real writer pair
mut2 = ctrl2(0x006C7008, 0x006C67BE)    # the +0x6C foreign-field store (real EXE bytes of another field)
ctrl2_ok = clean2[0] is True and mut2[0] is False
fail_closed_check(ctrl2_ok,
                  f"QC-J2-CTRL_2-replica: clean (real writer 89 7E 68 + read 8B 78 04) PASS -> mutated (foreign store 89 46 6C = +0x6C field) FAIL, cause = store offset no longer the declared +0x68 containment field: clean={clean2}, mut={mut2}")

# ------------------------------------------------------------------ CTRL_3
# Provenance predicate: the accessor must READ [ecx+0x68] (any ModRM form whose
# effective displacement is +0x68 with base ECX and destination EAX).
def ctrl3(va):
    b = rd(va, 6)
    if b[0] != 0x8B:
        return False, f"accessor {' '.join('%02X' % x for x in b)} not a mov reg,[r/m]"
    m = b[1]
    mod = m >> 6
    reg = (m >> 3) & 7
    rm = m & 7
    if mod == 1:
        disp = b[2]
    elif mod == 2:
        disp = struct.unpack_from("<I", b, 2)[0]
    else:
        return False, f"accessor {' '.join('%02X' % x for x in b)} does not read [ecx+0x68]"
    if reg == 0 and rm == 1 and disp == 0x68:
        return True, "accessor reads [ecx+0x68] == the producer-written field"
    return False, f"accessor {' '.join('%02X' % x for x in b)} does not read [ecx+0x68] (reads [ecx+{disp:#x}])"


clean3 = ctrl3(0x006C66D0)
mut3 = ctrl3(0x006C0EE0)  # REAL foreign accessor bytes (mov eax,[ecx+0x120])
ctrl3_ok = clean3[0] is True and mut3[0] is False
fail_closed_check(ctrl3_ok,
                  f"QC-J3-CTRL_3-replica: clean (real getter 8B 41 68) PASS -> mutated (real foreign-field accessor 8B 81 20 01 00 00 = [ecx+0x120]) FAIL, cause = correct bytes of a foreign field do not qualify as provenance of THIS getter: clean={clean3}, mut={mut3}")

# ------------------------------------------------------------------ CTRL_4
# §7 preservation predicate over the caller window 0x0050A3B7..0x0050A3F8:
# head = mov edi,eax; NO EDI-writing instruction before push edi; push edi present.
# My own fixed-size decoder for the window's opcode set.
REGS = ["EAX", "ECX", "EDX", "EBX", "ESP", "EBP", "ESI", "EDI"]


def decode_window(code, base):
    ins = []
    p = 0
    while p < len(code):
        va = base + p
        op = code[p]
        writes = []
        if op == 0x8B:
            m = code[p + 1]
            mod, reg, rm = m >> 6, (m >> 3) & 7, m & 7
            if mod == 3:
                n = 2
                writes.append(REGS[reg])
            else:
                disp = {0: 4 if rm == 5 else 0, 1: 1, 2: 4}[mod]
                n = 2 + (1 if rm == 4 else 0) + disp
                writes.append(REGS[reg])
        elif op == 0x83:
            m = code[p + 1]
            mod, rm = m >> 6, m & 7
            disp = 0 if mod == 3 else {0: 4 if rm == 5 else 0, 1: 1, 2: 4}[mod]
            n = 2 + (1 if (mod != 3 and rm == 4) else 0) + disp + 1  # + imm8
        elif op == 0x84:
            n = 2
        elif op in (0x74, 0x75, 0xEB):
            n = 2
        elif op == 0xE8:
            n = 5
        elif op in (0x50, 0x51, 0x52, 0x53, 0x55, 0x56, 0x57):
            n = 1
        elif op == 0x6A:
            n = 2
        elif op == 0xFF:
            m = code[p + 1]
            mod, rm = m >> 6, m & 7
            disp = 0 if mod == 3 else {0: 4 if rm == 5 else 0, 1: 1, 2: 4}[mod]
            n = 2 + (1 if (mod != 3 and rm == 4) else 0) + disp
        elif op == 0x0F:
            n = 6  # jcc rel32 in this window
        else:
            raise NotImplementedError(f"op {op:02x} @0x{va:08x}")
        ins.append((va, n, writes))
        p += n
    return ins


def ctrl4(code, base):
    ins = decode_window(code, base)
    if not (code[0] == 0x8B and code[1] == 0xF8):
        return False, "chain head missing (not mov edi,eax)"
    edi_writes = [i for i in ins[1:] if "EDI" in i[2]]
    if edi_writes:
        return False, f"EDI clobbered at 0x{edi_writes[0][0]:08x}"
    if code[0x3F] != 0x57:  # push edi @0x0050A3F6
        return False, "push edi @0x0050A3F6 missing"
    return True, "chain intact: mov edi,eax; no EDI write before push edi; push edi present"


WIN_VA, WIN_LEN = 0x0050A3B7, 0x42
clean_code = bytearray(rd(WIN_VA, WIN_LEN))
clean4 = ctrl4(clean_code, WIN_VA)
mut_code = bytearray(rd(WIN_VA, WIN_LEN))
off = 0x0050A3DD - WIN_VA
mut_code[off:off + 6] = bytes([0x8B, 0x3D, 0xD0, 0xD8, 0xB9, 0x00])  # synthetic EDI clobber (same as the run's fixture)
mut4 = ctrl4(mut_code, WIN_VA)
ctrl4_ok = clean4[0] is True and mut4[0] is False and "clobber" in mut4[1]
fail_closed_check(ctrl4_ok,
                  f"QC-J4-CTRL_4-replica: clean (real window) PASS -> mutated (synthetic 8B 3D D0 D8 B9 00 @0x0050A3DD = mov edi,[0x00B9D8D0]) FAIL, cause = an EDI write between head and push edi breaks the return->final-child relation: clean={clean4}, mut={mut4}")

# window decoder sanity: my clean walk must reproduce the exact instruction boundaries
ins = decode_window(bytes(clean_code), WIN_VA)
starts = [i[0] for i in ins]
expect_starts = [0x0050A3B7, 0x0050A3B9, 0x0050A3BE, 0x0050A3C0, 0x0050A3C2, 0x0050A3C6,
                0x0050A3C8, 0x0050A3CC, 0x0050A3CF, 0x0050A3D4, 0x0050A3D6, 0x0050A3D7,
                0x0050A3D8, 0x0050A3DD, 0x0050A3E3, 0x0050A3E4, 0x0050A3E9, 0x0050A3EC,
                0x0050A3EE, 0x0050A3F4, 0x0050A3F6, 0x0050A3F7]
fail_closed_check(starts == expect_starts,
                  f"QC-J5-CTRL_4-window-boundaries: my fixed decoder's instruction starts == the record's listing: {'MATCH' if starts == expect_starts else 'MISMATCH'}")

print()
print("PART4 DONE (all four control replicas executed on my own byte reads)")
