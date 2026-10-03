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


def _f1c1_fixtures():
    """Hand-built synthetic fixtures for the F1-C1 extension-halt regression
    battery (Desktop post-audit
    PE_GAMEBRYO_ORACLE_F1_DESKTOP_POST_AUDIT_20261003 finding F1-C1/P2; see
    run PE_GAMEBRYO_ORACLE_F1_C1_EXTENSION_HALT_R1_20261003 for the
    derivation). Byte layouts derived from the pinned source canon
    (NiStream.cpp LoadRTTI L412-449 + LoadRTTIString L1145-1153 + L70
    MAX_RTTI_LEN=256), NOT from the adapter under correction. All bytes are
    OUR OWN synthetic data; the committed package generator
    (docs/audits/PE_GAMEBRYO_ORACLE_F1_C1_EXTENSION_HALT_R1_20261003/
    01_FIXTURES/build_fixtures_c1.py) reproduces the physical files
    byte-identically (SIZE+SHA256 pins in that package)."""
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
    # third table name: source-valid declared length 127 (0 < 127 < 256),
    # incomplete payload -> LoadRTTIString cannot complete at EOF.
    third = _s.pack("<I", 127)

    def node_body(name):
        return (_s.pack("<I", 0) + _cstr(name) + _s.pack("<I", 0)
                + _s.pack("<I", nul) + _s.pack("<H", 0)
                + _s.pack("<3f", 0.0, 0.0, 0.0)
                + _s.pack("<9f", 1.0, 0.0, 0.0, 0.0, 1.0, 0.0,
                          0.0, 0.0, 1.0)
                + _s.pack("<f", 1.0) + _s.pack("<I", 0)
                + _s.pack("<I", nul) + _s.pack("<I", 0)
                + _s.pack("<I", 0))

    def truncated_table(payload):
        # 1 header block; table count 3: NiNode (registered),
        # NiDesktopFirstMissing (UNREGISTERED first miss @ index 1),
        # third name declared 127 B with only `payload` bytes behind it.
        return (hdr + _s.pack("<I", 1) + _s.pack("<H", 3)
                + _rtti("NiNode") + _rtti("NiDesktopFirstMissing")
                + third + payload)

    fx = {}
    # C1A: index-like leftover bytes ("\x02\x00" = the VALID type index 2);
    # the pre-C1-fix build consumed them as an object type index and then
    # crashed (IndexError: type_names[2] with only 2 names read).
    fx["C1A"] = truncated_table(b"\x02\x00")
    # C1B: fake-body-like leftover bytes (index + groups + NiNode body +
    # valid footer); the pre-C1-fix build reconstructed a SPURIOUS NiNode
    # object, histogram, census, groups and roots out of them.
    fx["C1B"] = truncated_table(
        _s.pack("<H", 0) + _s.pack("<I", 0) + node_body("root")
        + _s.pack("<I", 1) + _s.pack("<i", 0))
    return fx


def f1c1_extension_halt_tests():
    """F1-C1 regression battery (Desktop post-audit finding F1-C1/P2): under
    --full-decode, a DecodeError on a LATER RTTI name (after an established
    first table miss) must STOP the extension AT the table failure. After an
    incomplete table read there is NO proven boundary for the object type
    indices -- the leftover bytes of the unfinished name must NEVER be
    interpreted as indices, groups or bodies (STOP_AT_TABLE_FAILURE, not
    CONTINUE_FROM_UNKNOWN_OFFSET). The earlier source-predicted RTTIError
    verdict is preserved, the structured JSON is emitted and the CLI exits
    != 0."""
    fx = _f1c1_fixtures()
    print("== F1-C1 extension table-failure halt battery ==")
    print("MEASURED_QUANTITY: load_result verdict + rtti_table_validation "
          "(extension_halt marker / first_rtti_miss / names_read / "
          "full_table_read) + the object-side artifact keys")
    print("INDEPENDENT_SOURCE_OF_TRUTH: pinned NiStream.cpp LoadRTTI "
          "L421-433 control flow (the ORIGINAL loader aborts at the first "
          "factory miss and never reaches the later truncated name; the "
          "extension contract: no boundary proven -> no continuation)")
    print("WHY_NON_CIRCULAR: expectations were derived from the pinned "
          "source + the extension halt contract BEFORE the fix; the "
          "pre-fix behavior (traceback / spurious object) was reproduced "
          "on the same bytes and is raw-recorded in the run package")
    print("FAILURE_CASE_DETECTED: an adapter that breaks out of the name "
          "loop and continues into object indices/groups/bodies from the "
          "undetermined table boundary (losing the JSON to a traceback or "
          "fabricating objects) FAILS these controls")

    for key, cls in (("C1A", "index-like"), ("C1B", "fake-body-like")):
        # ordinary mode is UNCHANGED by F1-C1: the scan stops at the first
        # miss; the truncated later name is never read.
        ro = gb12core.decode(fx[key], path="<f1c1-%s-ordinary>" % key)
        check("f1c1_%s_ordinary_stops_at_first_miss" % key,
              ro["load_result"]["error_code"] == "RTTIError" and
              "RTTIError(NiDesktopFirstMissing)" in
              (ro["load_result"]["error"] or "") and
              ro["rtti_table_validation"]["names_read"] == 2 and
              "extension_halt" not in ro["rtti_table_validation"] and
              ro["objects"] == [] and
              "object_reference_histogram" not in ro and
              "object_reference_census" not in ro,
              "error=%r" % ro["load_result"]["error"])
        # --full-decode: the extension halts AT the table failure.
        rf = gb12core.decode(fx[key], path="<f1c1-%s-full>" % key,
                             full_decode=True)
        tv = rf["rtti_table_validation"]
        halt = tv.get("extension_halt", {})
        check("f1c1_%s_full_halt_at_table_failure" % key,
              rf["load_result"]["accepted"] is False and
              rf["load_result"]["error_code"] == "RTTIError" and
              "RTTIError(NiDesktopFirstMissing)" in
              (rf["load_result"]["error"] or "") and
              halt.get("marker") == "STOP_AT_TABLE_FAILURE" and
              halt.get("table_boundary_determined") is False and
              rf.get("extension_halt") == "STOP_AT_TABLE_FAILURE",
              "error=%r marker=%r" % (rf["load_result"]["error"],
                                      halt.get("marker")))
        check("f1c1_%s_full_keeps_source_verdict_and_table_state" % key,
              tv["first_rtti_miss"] == "NiDesktopFirstMissing" and
              tv["first_miss_table_index"] == 1 and
              tv["names_read"] == 2 and
              tv["full_table_read"] is False and
              tv["source_predicted_verdict"] == "REJECTED" and
              rf["decode_continued_after_rtti_gate"] is True and
              rf["load_result"]["partial"] is True and
              any("EXTENDED_TABLE_READ_FAILED" in w
                  for w in rf["warnings"]) and
              any("EXTENSION_HALT: STOP_AT_TABLE_FAILURE" in w
                  for w in rf["warnings"]),
              "first=%r@%r names_read=%r full=%r" % (
                  tv["first_rtti_miss"], tv["first_miss_table_index"],
                  tv["names_read"], tv["full_table_read"]))
        check("f1c1_%s_full_reads_nothing_past_table_failure" % key,
              rf["objects"] == [] and
              "object_reference_histogram" not in rf and
              "object_reference_census" not in rf and
              "object_groups" not in rf and
              rf["type_histogram"] == {} and
              rf["scene_graph"]["roots"] == [] and
              not any("EXTENDED_INSPECTION_HALTED" in w
                      for w in rf["warnings"]),
              "%s continuation: objects/histogram/census/groups/roots "
              "must be absent" % cls)
        check("f1c1_%s_marker_distinguishes_stop_vs_continue" % key,
              halt.get("continuation", "").startswith("NONE:") and
              "NOT CONTINUE_FROM_UNKNOWN_OFFSET" in
              halt.get("continuation", "") and
              halt.get("halted_at_table_index") == 2 and
              halt.get("file_type_count") == 3,
              "halt=%r" % halt)
    # the fake-body class additionally proves the crafted NiNode-like bytes
    # were NOT reconstructed into an object (the pre-fix spurious object,
    # histogram, census, groups, roots=[0] and count-match are all gone).
    rfB = gb12core.decode(fx["C1B"], path="<f1c1-C1B-full>", full_decode=True)
    check("f1c1_C1B_fake_body_not_reconstructed",
          rfB["objects"] == [] and
          "object_count_check" not in rfB and
          rfB["scene_graph"]["edges"] == [] and
          rfB["unknowns"] == [
              {"class": "NiDesktopFirstMissing",
               "status": "UNREGISTERED_IN_GB12_FACTORY"}],
          "unknowns=%r" % rfB["unknowns"])


def _f2_fixtures():
    """Hand-built synthetic fixtures for the F2 acceptance/coverage/link
    regression battery (Desktop post-audit
    C:\\Users\\User\\Documents\\ChatGPT\\PE\\
    PE_GAMEBRYO_ORACLE_TOOL_DESKTOP_POST_AUDIT_20261003 REPORT.md finding
    F2/P1; see run
    PE_GAMEBRYO_ORACLE_F2_ACCEPTANCE_COVERAGE_LINK_R1_20261003 for the
    derivation + SIZE/SHA256 pins). Byte layouts derived from the pinned
    source canon, NOT from the adapter under correction. All bytes are OUR
    OWN synthetic data; the committed package generator
    (docs/audits/PE_GAMEBRYO_ORACLE_F2_ACCEPTANCE_COVERAGE_LINK_R1_20261003/
    01_FIXTURES/build_fixtures_f2.py) reproduces the physical files
    byte-identically in the run's EXTERNAL sandbox (repo *.nif policy)."""
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

    def node_body(name, children=()):
        return (_s.pack("<I", 0) + _cstr(name) + _s.pack("<I", 0)
                + _s.pack("<I", nul) + _s.pack("<H", 0)
                + _s.pack("<3f", 0.0, 0.0, 0.0)
                + _s.pack("<9f", 1.0, 0.0, 0.0, 0.0, 1.0, 0.0,
                          0.0, 0.0, 1.0)
                + _s.pack("<f", 1.0) + _s.pack("<I", 0)
                + _s.pack("<I", nul)
                + _s.pack("<I", len(children))
                + b"".join(_s.pack("<I", c) for c in children)
                + _s.pack("<I", 0))

    def build(n_blocks, names, idxs, body, roots=(0,)):
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
    # VALID positive control: minimal fully-supported NiNode, no links
    # (byte-identical to the F1 battery fixture A)
    fx["VALID"] = build(1, ["NiNode"], [0], node_body("root"))
    # REGISTERED_BUT_NOT_DECODED counterexample: NiNode / NiCamera (MIDDLE,
    # registered but NO adapter loader) / NiNode
    nicam = _s.pack("<I", 0) + b"\xFF" * 12   # synthetic opaque body
    fx["REGNOTDEC"] = build(3, ["NiNode", "NiCamera"], [0, 1, 0],
                            node_body("n0") + nicam + node_body("n2"))
    # INVALID LINK counterexample: supported NiNode, children=[9999] with
    # n_obj=1 (out of range), structurally closed to the link phase
    fx["BADLINK"] = build(1, ["NiNode"], [0], node_body("root", (9999,)))
    return fx


def f2_acceptance_coverage_link_tests():
    """F2 regression battery (Desktop post-audit finding F2/P1): the final
    acceptance must be gated by ADAPTER_DECODE_COVERAGE and
    ADAPTER_INTEGRITY -- a REGISTERED_BUT_NOT_DECODED_BY_ADAPTER
    boundary-only placeholder is non-null but is NOT a semantic decode,
    and a LINK_FAILURE / out-of-range link must FAIL acceptance (never a
    mere warning). The four axes (SOURCE_PREDICTED_ORIGINAL_VERDICT,
    ADAPTER_DECODE_COVERAGE, ADAPTER_INTEGRITY, TOOL_VERDICT) must stay
    semantically separate; after an early RTTI halt the object-level
    counters must be null/NOT_MEASURED (never derived from RTTI table
    names -- a table entry is NOT an object reference)."""
    fx = _f2_fixtures()
    import registry  # noqa: E402  (independent factory census source)
    print("== F2 acceptance/coverage/link battery (Desktop post-audit "
          "finding F2/P1) ==")
    print("MEASURED_QUANTITY: load_result.accepted + the four F2 axes + "
          "coverage counters + integrity checks")
    print("INDEPENDENT_SOURCE_OF_TRUTH: pinned NiStream.cpp LoadStream "
          "L506-635 (link/postlink void returns discarded; unconditional "
          "return true) + GetObjectFromLinkID L245-256 (debug-only assert) "
          "+ NiTArray.inl L136-139 (unchecked GetAt) + the 198-class SDM "
          "factory census (NiCamera registered, no adapter loader) + "
          "hand-built fixtures derived BEFORE the fix")
    print("WHY_NON_CIRCULAR: expectations were derived from the pinned "
          "source semantics + the explicit F2 contract BEFORE the fix; "
          "the pre-fix false-success (accepted=true/exit 0 on both "
          "counterexamples) was reproduced on raw records on the base "
          "SHA and is preserved in the run package")
    print("FAILURE_CASE_DETECTED: an adapter that promotes accepted=true "
          "with a boundary-only REGISTERED_BUT_NOT_DECODED_BY_ADAPTER "
          "block, or leaves an out-of-range link a mere warning, or "
          "conflates a measured 0 with NOT_MEASURED, or derives "
          "object-level coverage from RTTI table names after an early "
          "halt, FAILS these controls")

    # POSITIVE CONTROL: fully-supported NiNode -> TOOL PASS, accepted
    rV = gb12core.decode(fx["VALID"], path="<f2-VALID>")
    check("f2_valid_positive_control_pass",
          rV["load_result"]["accepted"] is True and
          rV["TOOL_VERDICT"] == "PASS" and
          rV["ADAPTER_DECODE_COVERAGE"] == "COMPLETE" and
          rV["ADAPTER_INTEGRITY"] == "PASS" and
          rV["SOURCE_PREDICTED_ORIGINAL_VERDICT"] == "ACCEPTED",
          "tool=%s coverage=%s integrity=%s source=%s" % (
              rV["TOOL_VERDICT"], rV["ADAPTER_DECODE_COVERAGE"],
              rV["ADAPTER_INTEGRITY"],
              rV["SOURCE_PREDICTED_ORIGINAL_VERDICT"]))
    cV = rV["adapter_decode_coverage_counters"]
    check("f2_valid_counters_measured",
          cV["header_num_blocks"] == 1 and
          cV["semantically_decoded_blocks"] == 1 and
          cV["boundary_only_blocks"] == 0 and
          cV["registered_but_not_decoded_blocks"] == 0 and
          cV["unregistered_blocks"] == 0 and
          cV["unresolved_blocks"] == 0 and
          cV["not_measured_reasons"] == {},
          "counters=%s" % {k: cV[k] for k in (
              "header_num_blocks", "semantically_decoded_blocks",
              "boundary_only_blocks")})

    # COUNTEREXAMPLE A: registered-but-not-decoded must NOT be accepted
    rA = gb12core.decode(fx["REGNOTDEC"], path="<f2-REGNOTDEC>")
    cA = rA["adapter_decode_coverage_counters"]
    check("f2_registered_not_decoded_no_false_success",
          rA["load_result"]["accepted"] is False and
          rA["TOOL_VERDICT"] != "PASS" and
          rA["TOOL_VERDICT"] == "UNRESOLVED" and
          rA["ADAPTER_DECODE_COVERAGE"] == "INCOMPLETE" and
          cA["header_num_blocks"] == 3 and
          cA["semantically_decoded_blocks"] == 2 and
          cA["boundary_only_blocks"] == 1 and
          cA["registered_but_not_decoded_blocks"] == 1 and
          cA["registered_but_not_decoded_classes"] == ["NiCamera"],
          "tool=%s coverage=%s counters=%s" % (
              rA["TOOL_VERDICT"], rA["ADAPTER_DECODE_COVERAGE"],
              {k: cA[k] for k in (
                  "semantically_decoded_blocks", "boundary_only_blocks",
                  "registered_but_not_decoded_blocks")}))
    # factory_registration=YES from the independent registry census: the
    # factory KNOWS NiCamera -- the false success must NOT be re-justified
    # as ORIGINAL_GAMEBRYO_REJECTED
    check("f2_registered_not_decoded_factory_registration_yes",
          registry.is_registered("NiCamera") is True and
          "NiCamera" not in gb12core.LOADERS and
          any(o is not None and o.get("type") == "NiCamera" and
              o.get("status") == "REGISTERED_BUT_NOT_DECODED_BY_ADAPTER"
              for o in rA["objects"]) and
          rA["SOURCE_PREDICTED_ORIGINAL_VERDICT"] == "UNRESOLVED",
          "NiCamera in 198-class factory census, absent from the %d "
          "LOADERS; source=%s (registered != original rejection; the "
          "original class path is not traced in the pinned evidence)"
          % (len(gb12core.LOADERS),
             rA["SOURCE_PREDICTED_ORIGINAL_VERDICT"]))

    # COUNTEREXAMPLE B: out-of-range link -> integrity FAIL -> TOOL FAIL
    rB = gb12core.decode(fx["BADLINK"], path="<f2-BADLINK>")
    iB = rB["adapter_integrity_checks"]
    check("f2_invalid_link_no_false_success",
          rB["load_result"]["accepted"] is False and
          rB["ADAPTER_DECODE_COVERAGE"] == "COMPLETE" and
          iB["link_integrity"] == "FAIL" and
          iB["link_failure_count"] == 1 and
          rB["ADAPTER_INTEGRITY"] == "FAIL" and
          rB["TOOL_VERDICT"] == "FAIL",
          "tool=%s coverage=%s integrity=%s link_failures=%s" % (
              rB["TOOL_VERDICT"], rB["ADAPTER_DECODE_COVERAGE"],
              rB["ADAPTER_INTEGRITY"], iB["link_failure_count"]))
    check("f2_invalid_link_never_tool_unresolved",
          rB["TOOL_VERDICT"] != "UNRESOLVED" and
          rB["SOURCE_PREDICTED_ORIGINAL_VERDICT"] == "UNRESOLVED",
          "a known detected invalid link must never end TOOL_VERDICT="
          "UNRESOLVED (tool=%s); the SOURCE axis stays UNRESOLVED "
          "(debug-only assert vs release UB -- axes stay separate)"
          % rB["TOOL_VERDICT"])

    # ZERO vs NOT_MEASURED are distinct: measured zeros are ints; unknown
    # counters are None with an explicit per-counter reason
    check("f2_zero_vs_not_measured_distinct",
          cA["unregistered_blocks"] == 0 and
          isinstance(cA["unregistered_blocks"], int) and
          rB["adapter_decode_coverage_counters"]
          ["registered_but_not_decoded_blocks"] == 0,
          "measured 0 stays an int 0 (never a substitute for unknown)")

    # early RTTI halt: object-level counters null/NOT_MEASURED with
    # reasons (never derived from RTTI table names)
    fxB = _f1_fixtures()["B"]  # [NiNode, NiXyzzyx] unused-entry miss
    rH = gb12core.decode(fxB, path="<f2-early-halt>")
    cH = rH["adapter_decode_coverage_counters"]
    check("f2_early_rtti_halt_counters_not_measured",
          rH["ADAPTER_DECODE_COVERAGE"] == "NOT_MEASURED" and
          rH["ADAPTER_INTEGRITY"] == "NOT_MEASURED" and
          cH["header_num_blocks"] == 1 and
          cH["semantically_decoded_blocks"] is None and
          cH["boundary_only_blocks"] is None and
          cH["registered_but_not_decoded_blocks"] is None and
          cH["unregistered_blocks"] is None and
          cH["unresolved_blocks"] is None and
          all(cH["not_measured_reasons"].get(k)
              for k in ("semantically_decoded_blocks",
                        "boundary_only_blocks",
                        "registered_but_not_decoded_blocks",
                        "unregistered_blocks", "unresolved_blocks")) and
          rH["SOURCE_PREDICTED_ORIGINAL_VERDICT"] == "REJECTED" and
          rH["TOOL_VERDICT"] == "FAIL" and
          rH["objects"] == [],
          "early halt: header measured from the header, object-level "
          "null with reasons (a table entry is NOT an object reference); "
          "source=REJECTED -> tool=FAIL")

    # C1A/C1B (F1-C1 halt family): same NOT_MEASURED discipline
    fxc1 = _f1c1_fixtures()
    for key in ("C1A", "C1B"):
        rc = gb12core.decode(fxc1[key], path="<f2-%s-full>" % key,
                             full_decode=True)
        cc = rc["adapter_decode_coverage_counters"]
        check("f2_%s_counters_not_measured_after_table_failure" % key,
              rc["ADAPTER_DECODE_COVERAGE"] == "NOT_MEASURED" and
              cc["semantically_decoded_blocks"] is None and
              cc["boundary_only_blocks"] is None and
              cc["registered_but_not_decoded_blocks"] is None and
              cc["unresolved_blocks"] is None and
              bool(cc["not_measured_reasons"]) and
              rc["objects"] == [] and
              rc["SOURCE_PREDICTED_ORIGINAL_VERDICT"] == "REJECTED" and
              rc["TOOL_VERDICT"] == "FAIL",
              "STOP_AT_TABLE_FAILURE: no object-level census from the RTTI "
              "table; source=REJECTED preserved -> tool=FAIL")

    # integrity FAIL unconditionally implies TOOL FAIL, and accepted ==
    # (TOOL_VERDICT == PASS) across every battery result (the exact law
    # the CLI inspect exit keys on)
    allres = (("VALID", rV), ("REGNOTDEC", rA), ("BADLINK", rB),
              ("EARLYHALT", rH))
    law_ok = True
    detail = []
    for label, r in allres:
        if r["ADAPTER_INTEGRITY"] == "FAIL" and r["TOOL_VERDICT"] != "FAIL":
            law_ok = False
            detail.append("%s: integrity FAIL but tool=%s"
                          % (label, r["TOOL_VERDICT"]))
        if (r["load_result"]["accepted"] is not
                (r["TOOL_VERDICT"] == "PASS")):
            # accepted==True only ever on the PASS path; the early-halt
            # path returns before the final predicate (accepted stays the
            # initialized False == (TOOL != PASS)) -- the equivalence must
            # hold everywhere
            law_ok = False
            detail.append("%s: accepted=%s tool=%s"
                          % (label, r["load_result"]["accepted"],
                             r["TOOL_VERDICT"]))
    check("f2_integrity_fail_implies_tool_fail_and_accepted_eq_pass",
          law_ok,
          "integrity: %s; accepted==TOOL_PASS on all results: %s"
          % (", ".join("%s=%s" % (l, r["ADAPTER_INTEGRITY"])
                       for l, r in allres),
             "OK" if law_ok else "; ".join(detail)))

    # source/tool axis separation (central falsifier discipline): the
    # tool verdict must never be justified by an unproven source verdict
    check("f2_axes_never_conflated",
          rA["SOURCE_PREDICTED_ORIGINAL_VERDICT"] == "UNRESOLVED" and
          rA["TOOL_VERDICT"] == "UNRESOLVED" and
          rB["SOURCE_PREDICTED_ORIGINAL_VERDICT"] == "UNRESOLVED" and
          rB["TOOL_VERDICT"] == "FAIL" and
          rH["SOURCE_PREDICTED_ORIGINAL_VERDICT"] == "REJECTED" and
          rH["TOOL_VERDICT"] == "FAIL",
          "source != tool allowed to differ (A: UNRESOLVED/UNRESOLVED; "
          "B: UNRESOLVED/FAIL); neither ORIGINAL REJECTED nor TOOL PASS "
          "is asserted for the registered-but-not-decoded case")


def main():
    args = sys.argv[1:]
    self_tests()
    f1_rtti_table_tests()
    f1c1_extension_halt_tests()
    f2_acceptance_coverage_link_tests()
    if "--sandbox-payload" in args:
        i = args.index("--sandbox-payload")
        payload_controls(args[i + 1])
    print("TESTS: %d failures: %r" % (len(FAILURES), FAILURES))
    return 0 if not FAILURES else 1


if __name__ == "__main__":
    sys.exit(main())
