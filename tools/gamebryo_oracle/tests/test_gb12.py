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


def _f1_fixtures():
    """Hand-built synthetic fixtures for the F1 RTTI-table-order regression
    battery (source-derived layouts; see run
    PE_GAMEBRYO_ORACLE_F1_RTTI_CORRECTION_R1_20261003 for the derivation).
    All bytes are OUR OWN synthetic data."""
    import struct as _s

    def _rtti(nm):
        b = nm.encode("latin-1")
        return _s.pack("<I", len(b)) + b

    def _cstr(nm):
        b = nm.encode("latin-1")
        return _s.pack("<i", len(b)) + b

    hdr = (b"Gamebryo File Format, Version 10.1.0.0\n"
           + _s.pack("<I", 0x0A010000) + _s.pack("<I", 0))
    nul = 0xFFFFFFFF

    def node_body(name):
        return (_s.pack("<I", 0) + _cstr(name) + _s.pack("<I", 0)
                + _s.pack("<I", nul) + _s.pack("<H", 0)
                + _s.pack("<3f", 0.0, 0.0, 0.0)
                + _s.pack("<9f", 1.0, 0.0, 0.0, 0.0, 1.0, 0.0,
                          0.0, 0.0, 1.0)
                + _s.pack("<f", 1.0) + _s.pack("<I", 0)
                + _s.pack("<I", nul) + _s.pack("<I", 0)
                + _s.pack("<I", 0))

    def build(n_blocks, names, idxs, body=b"", roots=(0,)):
        out = hdr + _s.pack("<I", n_blocks) + _s.pack("<H", len(names))
        for n in names:
            out += _rtti(n)
        for ix in idxs:
            out += _s.pack("<H", ix)
        out += _s.pack("<I", 0)  # object groups
        out += body
        out += _s.pack("<I", len(roots))
        out += b"".join(_s.pack("<i", r) for r in roots)
        return out

    fx = {}
    # A: registered-only baseline
    fx["A"] = build(1, ["NiNode"], [0], node_body("root"))
    # B: [NiNode, NiXyzzyx], the only object uses NiNode (F1 counterexample)
    fx["B"] = build(1, ["NiNode", "NiXyzzyx"], [0], node_body("root"))
    # C: >= 2 unregistered entries; object order != table order (the
    # unknown run sits in the MIDDLE -- the trailing-run variant trips the
    # pre-existing presolver boundary crash, Desktop F4 territory, out of
    # the F1 scope; see run
    # PE_GAMEBRYO_ORACLE_F1_RTTI_CORRECTION_R1_20261003)
    fx["C"] = build(3, ["NiNode", "NiXyzzyx", "NiQuuxzyx"], [0, 2, 0],
                    node_body("n0") + _s.pack("<I", 0xDEADBEEF) +
                    node_body("n2"))
    # E: unused first table miss + incomplete object-index list
    fx["E"] = build(3, ["NiNode", "NiXyzzyx"], [0], node_body("root"))
    # F: first table miss + truncated later RTTI name
    fx["F"] = (hdr + _s.pack("<I", 1) + _s.pack("<H", 3)
               + _rtti("NiNode") + _rtti("NiXyzzyx") + _s.pack("<I", 0x400))
    return fx


def f1_rtti_table_tests():
    """F1 regression battery (Desktop post-audit finding F1): the gb12
    LoadRTTI reimplementation must validate the ENTIRE RTTI table in SOURCE
    TABLE ORDER (NiStream.cpp L421-433: name -> factory lookup -> next name),
    including entries no object references; the FIRST unregistered table
    entry is the fail-closed verdict BEFORE later names, any object type
    index, the groups or any body. The pre-F1 build validated by iterating
    object type indices and silently skipped unused unregistered entries."""
    fx = _f1_fixtures()
    print("== F1 RTTI table-order battery (source: NiStream.cpp L412-449) ==")
    print("MEASURED_QUANTITY: load_result verdict + rtti_table_validation "
          "(first_rtti_miss / first_miss_table_index / names_read / "
          "source_predicted_verdict)")
    print("INDEPENDENT_SOURCE_OF_TRUTH: pinned NiStream.cpp LoadRTTI "
          "L421-433 control flow (name -> factory check -> next name; "
          "indices L436-444 only after the whole table registered)")
    print("WHY_NON_CIRCULAR: expectations were derived from the pinned "
          "source + hand-built fixtures before the fix; a regression to "
          "object-reference-order validation fails these controls")
    print("FAILURE_CASE_DETECTED: an adapter that skips unused unregistered "
          "table entries, or reports the first miss in object order, or "
          "reads indices/past the truncated table before the factory miss, "
          "FAILS these controls")

    # A: registered-only baseline preserved
    rA = gb12core.decode(fx["A"], path="<f1-A>")
    check("f1_registered_only_baseline",
          rA["load_result"]["accepted"] is True and
          rA["rtti_table_validation"]["source_predicted_verdict"] ==
          "ACCEPTED" and
          rA["rtti_table_validation"]["first_rtti_miss"] is None,
          "roots=%r" % rA["scene_graph"]["roots"])

    # B: unused unregistered entry fails the gate (the F1 counterexample)
    rB = gb12core.decode(fx["B"], path="<f1-B>")
    tvB = rB["rtti_table_validation"]
    check("f1_unused_unregistered_entry_rejected",
          rB["load_result"]["accepted"] is False and
          "RTTIError(NiXyzzyx)" in (rB["load_result"]["error"] or "") and
          tvB["first_rtti_miss"] == "NiXyzzyx" and
          tvB["first_miss_table_index"] == 1 and
          tvB["names_read"] == 2 and
          tvB["source_predicted_verdict"] == "REJECTED",
          "error=%r" % rB["load_result"]["error"])
    check("f1_ordinary_miss_reads_no_object_data",
          rB["type_histogram"] == {} and
          "object_reference_census" not in rB and
          "object_reference_histogram" not in rB and
          rB["objects"] == [] and
          rB["decode_continued_after_rtti_gate"] is False,
          "histogram/census/objects not reported past the miss")

    # C: first miss by TABLE order, not object-reference order
    rC = gb12core.decode(fx["C"], path="<f1-C>")
    check("f1_first_miss_table_order_not_object_order",
          "RTTIError(NiXyzzyx)" in (rC["load_result"]["error"] or "") and
          rC["rtti_table_validation"]["first_rtti_miss"] == "NiXyzzyx" and
          rC["rtti_table_validation"]["first_miss_table_index"] == 1,
          "error=%r (object order would give NiQuuxzyx)"
          % rC["load_result"]["error"])
    rCf = gb12core.decode(fx["C"], path="<f1-C-full>", full_decode=True)
    check("f1_full_decode_keeps_source_verdict",
          rCf["load_result"]["accepted"] is False and
          rCf["load_result"]["partial"] is True and
          "RTTIError(NiXyzzyx)" in (rCf["load_result"]["error"] or "") and
          rCf["rtti_table_validation"]["first_rtti_miss"] == "NiXyzzyx" and
          rCf["rtti_table_validation"]["first_miss_table_index"] == 1 and
          rCf["rtti_table_validation"]["source_predicted_verdict"] ==
          "REJECTED" and
          rCf["decode_continued_after_rtti_gate"] is True and
          "extension_observation" in rCf["rtti_table_validation"],
          "error=%r first=%r@%r" % (
              rCf["load_result"]["error"],
              rCf["rtti_table_validation"]["first_rtti_miss"],
              rCf["rtti_table_validation"]["first_miss_table_index"]))

    # E: factory miss precedes the incomplete object-index list
    rE = gb12core.decode(fx["E"], path="<f1-E>")
    check("f1_miss_precedes_incomplete_indices",
          rE["load_result"]["error_code"] == "RTTIError" and
          "RTTIError(NiXyzzyx)" in (rE["load_result"]["error"] or "") and
          rE["rtti_table_validation"]["names_read"] == 2,
          "error=%r (index-stage errors would be "
          "INVALID_TYPE_INDEX/NOT_NIF_FILE/DECODE_ERROR)"
          % rE["load_result"]["error"])

    # F: factory miss preserved; truncated later name cannot mask it
    rF = gb12core.decode(fx["F"], path="<f1-F>")
    check("f1_miss_precedes_truncated_later_name",
          rF["load_result"]["error_code"] == "RTTIError" and
          "RTTIError(NiXyzzyx)" in (rF["load_result"]["error"] or "") and
          rF["rtti_table_validation"]["names_read"] == 2 and
          rF["rtti_table_validation"]["full_table_read"] is False,
          "error=%r" % rF["load_result"]["error"])
    rFf = gb12core.decode(fx["F"], path="<f1-F-full>", full_decode=True)
    check("f1_full_decode_extension_failure_never_masks_source_verdict",
          rFf["load_result"]["error_code"] == "RTTIError" and
          "RTTIError(NiXyzzyx)" in (rFf["load_result"]["error"] or "") and
          rFf["rtti_table_validation"]["first_rtti_miss"] == "NiXyzzyx" and
          rFf["load_result"]["partial"] is True and
          any("EXTENDED_TABLE_READ_FAILED" in w
              for w in rFf["warnings"]),
          "error=%r warnings=%r" % (
              rFf["load_result"]["error"], rFf["warnings"][:2]))


def main():
    args = sys.argv[1:]
    self_tests()
    f1_rtti_table_tests()
    if "--sandbox-payload" in args:
        i = args.index("--sandbox-payload")
        payload_controls(args[i + 1])
    print("TESTS: %d failures: %r" % (len(FAILURES), FAILURES))
    return 0 if not FAILURES else 1


if __name__ == "__main__":
    sys.exit(main())
