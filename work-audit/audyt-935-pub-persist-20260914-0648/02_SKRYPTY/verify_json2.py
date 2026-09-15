# WORK-AUDIT (audytor: Work-Audit, audyt: audyt-935-pub-persist-20260914-0648) — plik audytora
# -*- coding: utf-8 -*-
# WORK-AUDIT — weryfikacja x87 (21), LIVE_SCAN (41/18/0), F1_CONSUMER
import json, struct, math
PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913"

# --- x87: pelna re-derivacja ---
xt = json.load(open(PKG + r"\01_RAW\F2_X87_TABLE.json", encoding="utf-8"))
t = xt["table"]
bad_bits, bad_flag, bad_test, bad_zp, bad_aux = 0, 0, 0, 0, 0
def isnanv(v):
    return isinstance(v, float) and math.isnan(v)
for r in t:
    zv, hv = r["z_value"], r["h_value"]
    zb = struct.unpack("<I", bytes.fromhex(r["z_bits"][2:]))[0]
    hb = struct.unpack("<I", bytes.fromhex(r["h_bits"][2:]))[0]
    ev_z = struct.unpack("<f", struct.pack("<I", zb))[0]
    ev_h = struct.unpack("<f", struct.pack("<I", hb))[0]
    # bits<->value (z aero/h side)
    if not (ev_z == zv or (isnanv(ev_z) and isnanv(zv))):
        bad_bits += 1; print("BITS z mismatch %s: ev=%r json=%r" % (r["case"], ev_z, zv))
    if not (ev_h == hv or (isnanv(ev_h) and isnanv(hv))):
        bad_bits += 1; print("BITS h mismatch %s: ev=%r json=%r" % (r["case"], ev_h, hv))
    # FCOM flagi: st0=h vs st1=z
    if isnanv(hv) or isnanv(zv):
        eC0, eC2, eC3 = 1, 1, 1
    elif hv > zv: eC0, eC2, eC3 = 0, 0, 0
    elif hv < zv: eC0, eC2, eC3 = 1, 0, 0
    else: eC0, eC2, eC3 = 0, 0, 1
    if (r["C0"], r["C2"], r["C3"]) != (eC0, eC2, eC3):
        bad_flag += 1; print("FLAGS mismatch %s: json=%s exp=%s" % (r["case"], (r["C0"],r["C2"],r["C3"]), (eC0,eC2,eC3)))
    eT = (eC0 | eC3) != 0
    if bool(r["TEST_AH_0x41_nonzero"]) != eT:
        bad_test += 1; print("TEST mismatch %s" % r["case"])
    ezp = zb if eT else hb
    azp = struct.unpack("<I", bytes.fromhex(r["zprime_bits"][2:]))[0]
    if azp != ezp:
        bad_zp += 1; print("ZPRIME mismatch %s: json=%s exp=%s" % (r["case"], hex(azp), hex(ezp)))
    if bool(r["zprime_is_z_bits"]) != (azp == zb) or bool(r["zprime_is_h_bits"]) != (azp == hb) or bool(r["h_stored_to_zslot"]) != (not eT):
        bad_aux += 1; print("AUX mismatch %s" % r["case"])
print("x87: rows=%d bad_bits=%d bad_flag=%d bad_test=%d bad_zp=%d bad_aux=%d" % (len(t), bad_bits, bad_flag, bad_test, bad_zp, bad_aux))
print("X87 VERDICT:", "PASS 21/21" if (bad_bits==0 and bad_flag==0 and bad_test==0 and bad_zp==0 and bad_aux==0 and len(t)==21) else "FAIL")
neg0 = [r for r in t if "z=-0" in r["case"] and "h=+0" in r["case"] and "bit-distinction" not in r["case"]]
if neg0: print("z=-0,h=+0 -> zprime=%s (claim: 0x80000000)" % neg0[0]["zprime_bits"])

# --- LIVE_SCAN tally ---
ls = json.load(open(PKG + r"\02_ANALYSIS\ERRATA_LIVE_SCAN.json", encoding="utf-8"))
from collections import Counter
cnt = Counter(); total = 0; sond = len(ls)
for k, entries in ls.items():
    for e in entries:
        cnt[e["class"]] += 1; total += 1
print("LIVE_SCAN: sond=%d total=%d tally=%s" % (sond, total, dict(cnt)))
print("LIVE_SCAN VERDICT:", "PASS 41/18/0 (59)" if (total==59 and cnt["IN_REGISTER"]==41 and cnt["HISTORICAL_PACKAGE"]==18 and cnt["LIVE_ELSEWHERE"]==0) else "FAIL")
# ktore sondy wskazuja AUDIT_ENTRYPOINT (edycja wymagana)
ep_sonds = [k for k, es in ls.items() if any(e["file"] == "AUDIT_ENTRYPOINT.md" for e in es)]
print("sondy z AUDIT_ENTRYPOINT:", ep_sonds)

# --- F1_CONSUMER_CENSUS ---
cc = json.load(open(PKG + r"\01_RAW\F1_CONSUMER_CENSUS.json", encoding="utf-8"))
print("F1_CONSUMER:"); print(json.dumps(cc, indent=1)[:1800])
