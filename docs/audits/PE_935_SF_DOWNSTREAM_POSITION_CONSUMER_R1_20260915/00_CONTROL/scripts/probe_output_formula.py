"""probe_output_formula.py — independent re-derivation of the FUN_0082B5A0 output formula
(correction run PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915, inside canonical package
PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915).

Contract Section 8: re-derive from bytes the conversion helper's arithmetic (not inherit it).
Measurements only: full decode, the K constant's bits, the ret convention, the per-component
x87 trace facts. The STATUS ALGEBRA lives in 02_ANALYSIS/ORIGIN_STATUS_CORRECTION.md.

Outputs 01_RAW/OUTPUT_FORMULA_REVALIDATION_RAW.txt.
"""
import sys
import os
import struct
import hashlib
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import decode_lib as L
import sprov as SP

RUN_DIR = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915"
RAW = os.path.join(RUN_DIR, "01_RAW")
SCRIPT_PATH = os.path.abspath(__file__)

FN = 0x82B5A0
K_VA = 0xA7B360


def script_sha256():
    with open(SCRIPT_PATH, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest().upper()


def main():
    out = []
    A = out.append
    img = L.Image()  # S0 FAIL-CLOSED before any decode
    md = L.make_disassembler()

    A("=" * 100)
    A("OUTPUT FORMULA REVALIDATION — FUN_0082B5A0 full decode + K constant bits + ret convention")
    A("RUN_ID (correction): PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915")
    A("CANONICAL PACKAGE: PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915 (in-place correction)")
    A("GENERATED_UTC: " + time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    A("GENERATOR_SCRIPT: %s" % SCRIPT_PATH)
    A("GENERATOR_SHA256: %s" % script_sha256())
    A("MEASURED ENVIRONMENT:")
    for ln in L.measured_env(img).split("\n"):
        A("  " + ln)
    A("S0 FAIL-CLOSED: PASSED at script start (size+sha256+PE layout re-verified before any decode).")
    A("PURPOSE: independent re-derivation of the scale-and-subtract arithmetic from bytes")
    A("  (contract Section 8). Measurements only; status algebra in 02_ANALYSIS/ORIGIN_STATUS_CORRECTION.md.")
    A("=" * 100)
    A("")
    A("[F.1] FULL DECODE 0x82B5A0..0x82B5F0")
    for ins in L.disasm_range(md, img, FN, 0x82B5F0):
        A("  " + L.fmt_ins(ins))
    pad = img.read(0x82B5E7, 0x10)
    n_cc = 0
    for b in pad:
        if b == 0xCC:
            n_cc += 1
        else:
            break
    A("  bytes after 'ret 8' @0x82B5E4: %s (int3 run %d; next function 0x%08X)" % (
        " ".join("%02x" % x for x in pad), n_cc, 0x82B5E7 + n_cc))
    A("")
    A("[F.2] RET CONVENTION (measured by decode)")
    ret_cache = {}
    n, det = SP.ret_convention(md, img, FN, ret_cache)
    A("  ret_n = %s (%s)" % (n, det))
    A("")
    A("[F.3] K CONSTANT AT 0x%08X (measured bits)" % K_VA)
    kb = img.read(K_VA, 8)
    ku = struct.unpack("<Q", kb)[0]
    kd = struct.unpack("<d", kb)[0]
    f32val = struct.unpack("<f", struct.pack("<f", 0.01))[0]
    widen = struct.unpack("<Q", struct.pack("<d", f32val))[0]
    A("  bytes: %s" % " ".join("%02x" % x for x in kb))
    A("  as u64 bits: 0x%016X" % ku)
    A("  as f64: %.17g" % kd)
    A("  (double)(float)0.01 reference bits: 0x%016X -> %s" % (widen, "BITMATCH" if widen == ku else "BIT MISMATCH"))
    A("  f32 0.01 bits: 0x%08X" % struct.unpack("<I", struct.pack("<f", 0.01))[0])
    A("")
    A("[F.4] PER-COMPONENT ARITHMETIC (from the decode above; ECX=S, [esp+4]=out, [esp+8]=src)")
    A("  X: 0x82B5A4 fld [edx]            st0 := src.x (f32->f80 exact)")
    A("      0x82B5AA fld qword [0x%08X]  st0 := K (f64->f80 exact); st1 := src.x" % K_VA)
    A("      0x82B5B0 fmul st(1), st       st1 := src.x * K (f80 mul)")
    A("      0x82B5B2 fxch st(1)")
    A("      0x82B5B4 fstp dword [esp+8]   [esp+8] := f32(src.x * K)   <<< f32 narrowing #1")
    A("      0x82B5B8 fld dword [esp+8]    st0 := f32(src.x * K) (re widened, exact)")
    A("      0x82B5BC fsub dword [ecx]     st0 := f32(src.x*K) - S.x   (f80 sub vs f32-loaded base)")
    A("      0x82B5BE fstp dword [eax]     out.x := f32(f32(src.x*K) - S.x)  <<< final store")
    A("  Y: 0x82B5C0..0x82B5D0: identical shape at [edx+4] / [ecx+4] / [eax+4]")
    A("  Z: 0x82B5D3..0x82B5E1: identical shape at [edx+8] / [ecx+8] / [eax+8]")
    A("  MEASURED FORMULA (per component i in {0,4,8}):")
    A("      out[i] = f32( f32( (f80)src[i] * (f80)K ) - (f80)S[i] )")
    A("  with K == (double)(float)0.01 measured bit-exact above. S is READ (fsub source operand),")
    A("  never written by this function (no store through ECX in the decode).")
    A("")
    A("[F.5] ZERO-SUBTRACTION FACT (for the special-case analysis; measured narrowing order)")
    A("  the second operand S[i] enters the f80 subtraction as an f32->f80 exact widening;")
    A("  IF S[i] == +0.0 then x - (+0.0) == x for all finite x (IEEE-754, round-to-nearest),")
    A("  with the sign-of-zero caveat: (+0.0) - (+0.0) == +0.0 and (-0.0) - (+0.0) == -0.0;")
    A("  IF S[i] == -0.0 then x - (-0.0) == x + 0.0 (which turns -0.0 into +0.0 for x == -0.0).")
    A("  These are IEEE-754 facts applied to the measured instruction sequence, not measurements")
    A("  of runtime values (STATIC-ONLY run; no runtime execution).")
    A("")
    A("MEASURED_QUANTITY: full decode of 0x82B5A0; K qword bits at 0x%08X; ret convention;" % K_VA)
    A("  per-component x87 operation sequence.")
    A("INDEPENDENT_SOURCE_OF_TRUTH: capstone 5.0.7 linear decode of Entropia.exe physical bytes")
    A("  (SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31; S0 fail-closed).")
    A("WHY_NON_CIRCULAR: decoded from bytes here; no prior package prose is imported as evidence.")
    A("FAILURE_CASE_DETECTED: N/A for this probe (measurement revalidation); the falsified")
    A("  unconditional claim 'out = W*0.01 always' is corrected by the measured S-subtraction")
    A("  above combined with the origin-mutability census (see ORIGIN_STATUS_CORRECTION.md).")

    path = os.path.join(RAW, "OUTPUT_FORMULA_REVALIDATION_RAW.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("written:", path)
    print("K bits: 0x%016X BITMATCH=%s" % (ku, widen == ku))
    print("ret_n:", n)


if __name__ == "__main__":
    main()
