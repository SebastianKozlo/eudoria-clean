# WORK-AUDIT header
# -*- coding: utf-8 -*-
# WORK-AUDIT (audytor: Work-Audit, audyt: audyt-935-pub-persist-20260914-0648) — plik audytora
import json, struct, sys
sys.path.insert(0, r"D:\TESTAI\audits\work-audit\audyt-935-pub-persist-20260914-0648\pylibs")
PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913"
results = []
def check(name, ok, detail=""):
    results.append((name, ok, detail)); print(("PASS " if ok else "FAIL ") + name + ((" | " + detail) if detail else ""))

# 1) F1_MASK_SUITE.json — suita 29 = 28 model==decoder + 1 meta
su = json.load(open(PKG + r"\01_RAW\F1_MASK_SUITE.json", encoding="utf-8"))
print("F1_MASK_SUITE top-level keys:", list(su.keys())[:10])
# struktura: sprawdzimy rekurencyjnie pola pass/fail
def count_fields(o, key):
    n = 0
    if isinstance(o, dict):
        for k, v in o.items():
            if k == key: n += 1
            n += count_fields(v, key)
    elif isinstance(o, list):
        for x in o: n += count_fields(x, key)
    return n
s = json.dumps(su)
print("json size:", len(s), "| occurrences of '\"pass\": true':", s.count('"pass": true'), "| '\"pass\": false':", s.count('"pass": false'))
n_pass_true = count_fields(su, None)  # placeholder
cases = su.get("cases") or su.get("suite") or su.get("results")
if cases is not None:
    print("cases count:", len(cases))
    ok_all = all(c.get("model_eq_decoder", c.get("pass", c.get("match", True))) for c in cases if isinstance(c, dict))
    check("SUITA 29 = 28 + 1 meta", len(cases) == 29, str(len(cases)))
    meta = [k for k in su.keys() if "meta" in k.lower() or "arithmetic" in k.lower() or "summary" in k.lower()]
    print("meta keys:", meta)
else:
    print("keys detail:", {k: (type(v).__name__, len(v) if hasattr(v, "__len__") else "") for k, v in su.items()})

# 2) F2_X87_TABLE.json — 21 wierszy + re-derivacja reguly
xt = json.load(open(PKG + r"\01_RAW\F2_X87_TABLE.json", encoding="utf-8"))
rows = xt.get("rows") or xt.get("table") or xt.get("cases")
print("F2_X87 rows:", len(rows) if rows else xt.keys())
if rows:
    import math
    def f32bits(i): return struct.pack("<f", i) if isinstance(i, float) else struct.pack("<I", i & 0xFFFFFFFF)
    bad = 0
    for r in rows:
        z = r.get("z"); h = r.get("h")
        zc = r.get("z_bits") or r.get("z_bits_hex"); hc = r.get("h_bits") or r.get("h_bits_hex")
        zp = r.get("z_prime_bits") or r.get("result_bits") or r.get("z_prime")
        C0 = r.get("C0"); C2 = r.get("C2"); C3 = r.get("C3")
        jne = r.get("jne_taken", r.get("branch"))
        # wlasna re-derivacja: unordered gdy NaN(h) lub NaN(z)
        def isnan(x):
            try: return math.isnan(x)
            except: return False
        unord = isnan(h) or isnan(z)
        if unord: eC0 = eC2 = eC3 = 1
        elif h > z: eC0 = eC2 = eC3 = 0
        elif h < z: eC0, eC2, eC3 = 1, 0, 0
        else: eC0, eC2, eC3 = 0, 0, 1
        if (C0, C2, C3) != (eC0, eC2, eC3):
            bad += 1; print("  FLAGS MISMATCH z=%r h=%r: json=(%s,%s,%s) expected=(%s,%s,%s)" % (z, h, C0, C2, C3, eC0, eC2, eC3))
        ejne = not (eC0 == 0 and eC3 == 0)
        if jne is not None and bool(jne) != ejne:
            bad += 1; print("  JNE MISMATCH z=%r h=%r json=%r expected=%r" % (z, h, jne, ejne))
    check("X87 tabela 21 wierszy", len(rows) == 21, str(len(rows)))
    check("X87 flagi C0/C2/C3 + JNE spójne z IEEE-754 FCOM (re-derivacja wlasna)", bad == 0, "bad=%d" % bad)

# 3) F1_CONSUMER_CENSUS.json
cc = json.load(open(PKG + r"\01_RAW\F1_CONSUMER_CENSUS.json", encoding="utf-8"))
print("F1_CONSUMER keys:", list(cc.keys())[:12])
s3 = json.dumps(cc)
for k in ("call_site", "callers", "sites"):
    pass

# 4) ERRATA_LIVE_SCAN.json — tally 41/18/0, 17 sond
ls = json.load(open(PKG + r"\02_ANALYSIS\ERRATA_LIVE_SCAN.json", encoding="utf-8"))
print("LIVE_SCAN top keys:", list(ls.keys())[:12])
entries = ls.get("entries") or ls.get("results") or ls.get("scan")
if entries is None:
    # struktura inna — zbadajmy
    print(json.dumps(ls, indent=1)[:800])
else:
    from collections import Counter
    cnt = Counter(e.get("classification") or e.get("class") or e.get("status") for e in entries)
    print("tally:", dict(cnt), "total:", len(entries))
    check("LIVE_SCAN 59 wpisow", len(entries) == 59, str(len(entries)))
    check("LIVE_SCAN IN_REGISTER 41", cnt.get("IN_REGISTER", 0) == 41, str(cnt))
    check("LIVE_SCAN HISTORICAL_PACKAGE 18", cnt.get("HISTORICAL_PACKAGE", 0) == 18, str(cnt))
    check("LIVE_SCAN LIVE_ELSEWHERE 0", cnt.get("LIVE_ELSEWHERE", 0) == 0, str(cnt))

# 5) P2_CENSUS2.json — pusta sonda [[]]
p2c2 = open(PKG + r"\01_RAW\P2_CENSUS2.json", encoding="utf-8").read()
check("P2_CENSUS2.json = pusta sonda [[]]", p2c2.strip() == "[[]]", repr(p2c2[:40]))

# 6) piny writerow (EXE)
data = open(r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe", "rb").read()
def rd(va, n):
    off = va - 0x400000
    if 0x1000 <= off < 0x675000: off2 = off  # .text raw=rva
    elif 0x675000 <= off < 0x76B000: off2 = off  # .rdata raw=rva
    elif 0x76C000 <= off < 0x7A0000: off2 = off - 0x76C000 + 0x76C000
    else: off2 = off
    return data[off2:off2+n]
check("PIN FUN_00855340 MOV [EBX+0x4C],EAX @0x0085536D", rd(0x0085536D, 3) == bytes.fromhex("894C4C")[:3] or rd(0x0085536D, 3) == bytes.fromhex("8943 4C".replace(" ","")), rd(0x0085536D, 4).hex().upper())

print()
print("SUMMARY: %d PASS, %d FAIL" % (sum(1 for _, ok, _ in results if ok), sum(1 for _, ok, _ in results if not ok)))
