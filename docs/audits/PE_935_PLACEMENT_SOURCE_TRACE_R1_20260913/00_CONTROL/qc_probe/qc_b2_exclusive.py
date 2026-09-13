# qc_b2_exclusive.py — B2: czy wszyscy setter-callerzy czytaja transformy z systemu atrybutow?
import sys, os, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qc_pe import load
pe = load()
data = pe.data

ATTR_FUNCS = {
    0x00846840: 'FUN_00846840 attr-pos-fetch',
    0x008492C0: 'FUN_008492c0 attr-float-read',
    0x00845360: 'FUN_00845360 attr-float-get',
    0x008452D0: 'FUN_008452d0 attr-int-get',
    0x00854720: 'FUN_00854720 attr-triple',
    0x00843D60: 'FUN_00843d60 walker-init',
    0x0085B840: 'FUN_0085b840 walker',
    0x008544D0: 'FUN_008544d0 resolver',
    0x00844020: 'FUN_00844020 attr-check',
    0x00845F70: 'FUN_00845f70 attr-SET',
}
OTHER_FUNCS = {
    0x0072F580: 'FUN_0072f580 template-lookup',
    0x004926E0: 'FUN_004926e0 avatar-id',
    0x006B22D0: 'FUN_006b22d0 getter C',
    0x007CE1E0: 'FUN_007ce1e0 getter A',
    0x00746550: 'FUN_00746550 getter B',
    0x0048ADA0: 'FUN_0048ada0 getter D',
    0x00730700: 'FUN_00730700 ctor rekordu',
    0x00730F60: 'FUN_00730f60 init',
    0x00730F90: 'FUN_00730f90 setter pos',
    0x00730FB0: 'FUN_00730fb0 setter rot',
    0x00730FD0: 'FUN_00730fd0 setter 2p',
    0x004148F0: 'FUN_004148f0 rejestracja',
    0x00457930: 'FUN_00457930 rejestracja nazwa',
    0x004C5580: 'FUN_004c5580 deriver',
}

SETTER_CALLER_FUNCS = [
    ('FUN_0050bed0', 0x0050BED0), ('FUN_00457cd0', 0x00457CD0), ('FUN_00459270', 0x00459270),
    ('FUN_00442190', 0x00442190), ('FUN_00447630', 0x00447630), ('FUN_004b3a00', 0x004B3A00),
    ('FUN_0043a200', 0x0043A200), ('FUN_004c47f0', 0x004C47F0), ('FUN_0046e790', 0x0046E790),
    ('FUN_00488920', 0x00488920), ('FUN_0067bc90', 0x0067BC90), ('FUN_0067ccd0', 0x0067CCD0),
    ('FUN_00567170', 0x00567170), ('FUN_005b5f90', 0x005B5F90), ('FUN_00567770', 0x00567770),
]

def body_of(va, maxb=0x8000):
    off = pe.va2off(va)
    if off is None: return va, b''
    end = off
    while not (data[end] == 0xCC and data[end+1] == 0xCC and data[end+2] == 0xCC):
        end += 1
        if end - off > maxb: break
    return va, data[off:end]

print('%-14s %-8s %-s' % ('funkcja', 'rozmiar', 'wywolania (atrybutowe vs inne)'))
for name, va in SETTER_CALLER_FUNCS:
    bv, body = body_of(va)
    attr_calls = []
    other_calls = []
    for i in range(len(body)-5):
        if body[i] == 0xE8:
            rel = struct.unpack_from('<i', body, i+1)[0]
            t = bv + i + 5 + rel
            if t in ATTR_FUNCS:
                attr_calls.append(ATTR_FUNCS[t].split()[0])
            elif t in OTHER_FUNCS:
                other_calls.append(OTHER_FUNCS[t].split()[0])
    print('%-14s %6d B  ATTR: %-60s INNE: %s' % (name, len(body), ','.join(sorted(set(attr_calls))) or '-', ','.join(sorted(set(other_calls))) or '-'))
