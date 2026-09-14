# -*- coding: utf-8 -*-
# decode_adhoc.py - ad-hoc decode helper for this run.
# Usage: python decode_adhoc.py <va_hex> [max_bytes_hex]
# STATIC-ONLY. Dumps function body disasm from the physical EXE.

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pe935_core as core

pe = core.PE(core.EXE_PATH)
va = int(sys.argv[1], 16)
mx = int(sys.argv[2], 16) if len(sys.argv) > 2 else 0x200
end, body = pe.func_body(va, maxb=mx)
print("FUN_%08X end=%s size=%d" % (va, hex(end) if end else "-", len(body)))
print(pe.disasm_lines(va, len(body)))
