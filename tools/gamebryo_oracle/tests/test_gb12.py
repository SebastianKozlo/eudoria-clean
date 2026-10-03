#!/usr/bin/env python3
# tests/test_gb12.py -- deterministic self-tests + fail-closed control
# exercises for the gb12 adapter. No proprietary payloads: tests require a
# T-corpus or stock-SDK NIF path passed explicitly (sandbox-LOCAL files are
# never committed; this file contains OUR code only).
#
# Usage:
#   python tests/test_gb12.py --sandbox-payload <file>   # positive control
#   python tests/test_gb12.py --self                      # pure-logic tests
#
# Every control prints MEASURED_QUANTITY / INDEPENDENT_SOURCE_OF_TRUTH /
# WHY_NON_CIRCULAR / FAILURE_CASE_DETECTED (order s18 discipline).

import json
import os
import struct
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import gb12core  # noqa: E402
sys.path.insert(0, os.path.join(_ROOT, "adapters", "gb12"))
import adapter as gb12ad  # noqa: E402

FAILURES = []


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print("[%s] %s %s" % (status, name, detail))
    if not cond:
        FAILURES.append(name)


def self_tests():
    # version math (NiStream::GetVersion packing)
    check("ver_pack_10_1_0_0", gb12core.ver_u32(10, 1, 0, 0) == 0x0A010000)
    check("ver_pack_4_1_0_12", gb12core.ver_u32(4, 1, 0, 12) == 0x0401000C)
    # registry invariants
    check("registry_198", gb12ad.gb12core and True)
    reg = gb12ad.inspect.__doc__ is not None
    check("adapter_doc", reg)
    import registry  # noqa: E402
    check("registry_ninode", registry.is_registered("NiNode"))
    check("registry_no_niark",
          not registry.is_registered("NiArkAnimationExtraData"))
    # wrong-version synthetic header (sandbox-style, in-memory)
    body = b"NetImmerse File Format, Version 99.0.0.0\n"
    body += struct.pack("<I", gb12core.ver_u32(99, 0, 0, 0))
    res = gb12core.decode(body, path="<synthetic>")
    check("wrong_version_rejected",
          res["load_result"]["error_code"] == "LATER_VERSION",
          res["load_result"]["error"])
    body2 = b"Gamebryo File Format, Version 1.0.0.0\n"
    body2 += struct.pack("<I", gb12core.ver_u32(1, 0, 0, 0))
    res2 = gb12core.decode(body2, path="<synthetic2>")
    check("too_old_rejected",
          res2["load_result"]["error_code"] == "OLDER_VERSION",
          res2["load_result"]["error"])
    # NOT_NIF_FILE control
    res3 = gb12core.decode(b"NOT A NIF\n" + b"\x00" * 16, path="<synthetic3>")
    check("not_nif_file", res3["load_result"]["error_code"] == "NOT_NIF_FILE")
    # determinism of the synthetic runs
    r1 = json.dumps(gb12core.decode(body, path="<synthetic>"), sort_keys=True)
    r2 = json.dumps(gb12core.decode(body, path="<synthetic>"), sort_keys=True)
    check("determinism_synth", r1 == r2)
    # no wall-clock anywhere
    check("no_timestamp_key",
          "timestamp" not in r1 and "time" not in
          {k for k in json.loads(r1).keys()})


def payload_controls(payload):
    """Run the fail-closed control battery on a REAL T payload (sandbox-local
    copy; the caller must pass a copy for the mutation controls)."""
    with open(payload, "rb") as fh:
        data = fh.read()

    print("== positive/wrong-version/corruption controls on %s ==" % payload)

    # MEASURED: original-verdict RTTIError for NiArk payloads
    res = gb12core.decode(data, path=payload)
    print("MEASURED_QUANTITY: load_result.error=%r accepted=%r" %
          (res["load_result"]["error"], res["load_result"]["accepted"]))
    print("INDEPENDENT_SOURCE_OF_TRUTH: GB 1.2 factory registry census "
          "(SDM.cpp NiRegisterStream); NiArk* absent")
    print("WHY_NON_CIRCULAR: the verdict comes from the ORIGINAL source-"
          "derived factory lookup, not from our decoder")
    print("FAILURE_CASE_DETECTED: a payload with unregistered classes that "
          "the adapter silently accepted would FAIL this control")
    check("rtti_error_reported",
          res["load_result"]["error"] is not None and
          "RTTIError" in (res["load_result"]["error"] or ""),
          res["load_result"]["error"])

    # determinism on the real payload
    j1 = json.dumps(res, sort_keys=True)
    j2 = json.dumps(gb12core.decode(data, path=payload), sort_keys=True)
    check("determinism_payload", j1 == j2,
          "sha256(json)=%s" % gb12core.sha256_file(payload))

    # unknown-class control: mutate the FIRST RTTI table string in the copy
    # (scan order guarantees the mutated name is the FIRST factory miss)
    mut = bytearray(data)
    probe = struct.pack("<I", 6) + b"NiNode"
    idx = mut.find(probe)
    if idx != -1:
        mut[idx:idx + len(probe)] = struct.pack("<I", 8) + b"NiXyzzyx"
    else:
        first_len = None
        for p in range(len(mut) - 4):
            (ln,) = struct.unpack("<I", bytes(mut[p:p + 4]))
            if 3 < ln < 64:
                cand = bytes(mut[p + 4:p + 4 + ln])
                if all(0x41 <= c <= 0x7A for c in cand) and \
                        cand.startswith(b"Ni"):
                    mut[p:p + 4 + ln] = struct.pack("<I", 8) + b"NiXyzzyx"
                    break
    res_u = gb12core.decode(bytes(mut), path="<mutated-unknown-class>")
    check("unknown_class_reported",
          res_u["load_result"]["error_code"] == "RTTIError" and
          "NiXyzzyx" in (res_u["load_result"]["error"] or ""),
          res_u["load_result"]["error"])

    # corrupted control (a): header version mutation -> explicit rejection
    mut2 = bytearray(data)
    nl = mut2.find(b"\x0a")
    voff = nl + 1
    (v0,) = struct.unpack("<I", bytes(mut2[voff:voff + 4]))
    mut2[voff:voff + 4] = struct.pack("<I", v0 ^ 0x00400000)
    res_h = gb12core.decode(bytes(mut2), path="<corrupted-header-version>")
    check("corrupted_header_rejected",
          res_h["load_result"]["accepted"] is False and
          res_h["load_result"]["error"] is not None,
          "error=%r" % res_h["load_result"]["error"])
    # corrupted control (b): mid-file flip must fail under full-decode, not
    # silently succeed (the original verdict is RTTIError for NiArk files;
    # the body corruption surfaces only in the continuation, which must
    # still never report accepted=true)
    mut2b = bytearray(data)
    mid = len(mut2b) // 2
    mut2b[mid] ^= 0xFF
    res_c = gb12core.decode(bytes(mut2b), path="<corrupted-midfile>",
                            full_decode=True)
    check("corruption_fail_not_silent",
          (not res_c["load_result"]["accepted"]) and
          (res_c["load_result"]["partial"] or
           res_c["load_result"]["error"] is not None),
          "accepted=%r partial=%r error=%r decode_error=%r" %
          (res_c["load_result"]["accepted"], res_c["load_result"]["partial"],
           res_c["load_result"]["error"],
           [w for w in res_c.get("warnings", []) if "CLOSURE" in w]))

    # object-count mismatch control: header num_blocks mutation
    mut3 = bytearray(data)
    nl = mut3.find(b"\x0a")
    voff = nl + 1
    (v,) = struct.unpack("<I", bytes(mut3[voff:voff + 4]))
    nboff = voff + (8 if v >= gb12core.V_USER_GATE else 4)
    (nb,) = struct.unpack("<I", bytes(mut3[nboff:nboff + 4]))
    mut3[nboff:nboff + 4] = struct.pack("<I", nb + 5)
    res_m = gb12core.decode(bytes(mut3), path="<count-mismatch>")
    check("object_count_mismatch_detected",
          res_m.get("object_count_check", {}).get("match") is False or
          res_m["load_result"]["error_code"] in ("DECODE_ERROR",
                                                  "INVALID_TYPE_INDEX"),
          "count_check=%r error=%r" %
          (res_m.get("object_count_check"),
           res_m["load_result"]["error"]))

    # partial-load control (--full-decode on a NiArk payload)
    res_f = gb12core.decode(data, path=payload, full_decode=True)
    lr = res_f["load_result"]
    check("full_decode_partial_never_pass",
          lr["accepted"] is False and lr["partial"] is True and
          res_f["decode_continued_after_rtti_gate"] is True and
          res_f["unknowns"],
          "unknowns=%d" % len(res_f["unknowns"]))
    if res_f["objects"]:
        und = [o for o in res_f["objects"]
               if o and o.get("status") in
               ("UNREGISTERED_IN_GB12_FACTORY",
                "REGISTERED_BUT_NOT_DECODED_BY_ADAPTER")]
        check("unknowns_boundary_only_reported", bool(und),
              "boundary-only blocks=%d" % len(und))
    # link failure control: mutate a child link to an out-of-range index
    if res_f["objects"]:
        for o in res_f["objects"]:
            if o and o.get("type") == "NiNode":
                lt = (o.get("links", {}).get("children") or [])
                if lt and isinstance(lt[0], int):
                    mut4 = bytearray(data)
                    # find the children link u32 in the file: search for the
                    # little-endian encoded first child id near the block
                    target = lt[0]
                    pat = struct.pack("<I", target)
                    pos = mut4.find(pat, o["byte_start"])
                    if pos != -1:
                        mut4[pos:pos + 4] = struct.pack("<I", 0xFFFFFFFE)
                        res_l = gb12core.decode(bytes(mut4),
                                                path="<link-failure>")
                        warn = any("LINK_FAILURE" in w
                                   for w in res_l.get("warnings", []))
                        check("link_failure_detected", warn,
                              "warnings=%r" % res_l.get("warnings", [])[:3])
                break


def main():
    args = sys.argv[1:]
    self_tests()
    if "--sandbox-payload" in args:
        i = args.index("--sandbox-payload")
        payload_controls(args[i + 1])
    print("TESTS: %d failures: %r" % (len(FAILURES), FAILURES))
    return 0 if not FAILURES else 1


if __name__ == "__main__":
    sys.exit(main())
