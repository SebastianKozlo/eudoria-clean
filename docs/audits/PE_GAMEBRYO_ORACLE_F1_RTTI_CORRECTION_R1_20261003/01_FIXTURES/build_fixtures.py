#!/usr/bin/env python3
# build_fixtures.py -- hand-built synthetic NIF fixtures for the F1 correction
# run PE_GAMEBRYO_ORACLE_F1_RTTI_CORRECTION_R1_20261003.
#
# QC DISCIPLINE: the fixture byte layouts below are derived INDEPENDENTLY from
# the pinned source canon (NiStream.cpp E955C36E...: LoadHeader L303-360,
# LoadRTTI L412-449, LoadRTTIString L1145-1153, LoadObjectGroups L470-487,
# LoadTopLevelObjects L367-385; NiObject.cpp B137FE42...: GroupID u32 iff
# 5.0.0.6 <= v < 10.1.0.114; NiObjectNET.cpp 2ADB8F89...: name LoadCString,
# extraData multi-link list iff v >= 5.0.0.11, controller link; NiAVObject.cpp
# 72E08371...: flags u16 + local transform 3f/9f/f + (v >= 5.0.0.19)
# properties list + collision link; NiNode.cpp 38C7A1DE...: children + effects
# lists) -- NOT from the adapter code under correction.
#
# All bytes are OUR OWN synthetic data. Zero proprietary content.
#
# REPO POLICY: the repo-wide .gitignore excludes *.nif (zero NIF files are
# tracked anywhere in this repo by design). The generated fixtures are NOT
# committed; this script is the committed DETERMINISTIC regeneration source
# (byte-identical output; SHA256 pins in ../INPUT_IDENTITIES.md). Physical
# copies are preserved in this run's external sandbox:
# D:\Eudoria_Reconstruction\99_Audits\
# PE_GAMEBRYO_ORACLE_F1_RTTI_CORRECTION_R1_20261003\sandbox\01_FIXTURES\
# The raw-test records reference the package-dir execution paths used
# during the run; regenerate with `python build_fixtures.py` in any
# directory to verify the SHA pins.
#
# Fixtures:
#   fx_A_registered_only.nif      -- table [NiNode], 1 object NiNode -> baseline
#                                    accepted (matches the Desktop
#                                    synthetic_valid_node.nif layout family)
#   fx_B_unused_unregistered.nif -- table [NiNode, NiXyzzyx], 1 object NiNode
#                                    (type_idx 0); the NiXyzzyx entry is
#                                    UNUSED by any object -- the F1
#                                    counterexample shape (Desktop
#                                    unused_unregistered_rtti.nif)
#   fx_C_table_vs_object_order.nif -- table [NiNode, NiXyzzyx, NiQuuxzyx];
#                                    objects: obj0 -> idx 0 (NiNode),
#                                    obj1 -> idx 2 (NiQuuxzyx). Object
#                                    reference order meets NiQuuxzyx FIRST;
#                                    source table order meets NiXyzzyx
#                                    FIRST. >= 2 unregistered entries.
#   fx_E_incomplete_indices.nif  -- table [NiNode, NiXyzzyx], header claims 3
#                                    blocks, only ONE u16 type index present
#                                    then the stream continues with body
#                                    bytes: the ordinary-mode source scan
#                                    must reject at the factory miss BEFORE
#                                    the incomplete index list is ever read.
#   fx_F_truncated_later_name.nif -- table [NiNode, NiXyzzyx, <truncated 3rd
#                                    name: u32 length beyond EOF>]; the FIRST
#                                    table miss (NiXyzzyx) precedes the
#                                    truncated later name, so the factory miss
#                                    must be preserved (no parser error may
#                                    mask it).

import hashlib
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))

VER_10_1_0_0 = 0x0A010000
NULL_LINK = 0xFFFFFFFF


def rtti_string(s):
    # NiStream::LoadRTTIString L1145-1153: u32 length + bytes.
    b = s.encode("latin-1")
    return struct.pack("<I", len(b)) + b


def cstring(s):
    # NiStream::LoadCString L1123-1140: i32 length; bytes if > 0.
    b = s.encode("latin-1")
    return struct.pack("<i", len(b)) + b


def header(n_blocks, user_ver=0):
    # LoadHeader L303-360: line; u32 version; u32 user version iff
    # file >= 10.0.1.8 (10.1.0.0 qualifies); u32 uiObjects.
    return (b"Gamebryo File Format, Version 10.1.0.0\n"
            + struct.pack("<I", VER_10_1_0_0)
            + struct.pack("<I", user_ver)
            + struct.pack("<I", n_blocks))


def rtti_table(names):
    # LoadRTTI L414-434: u16 usRTTICount + per entry LoadRTTIString.
    out = struct.pack("<H", len(names))
    for n in names:
        out += rtti_string(n)
    return out


def type_indices(idxs):
    # LoadRTTI L436-444: one u16 per object (order = object order).
    return b"".join(struct.pack("<H", i) for i in idxs)


def groups():
    # LoadObjectGroups L470-487 (iff ver >= 5.0.0.6): u32 numGroups (the
    # source reads numGroups then ++ for the null group; zero here).
    return struct.pack("<I", 0)


def ninode_body(name="root", gid=0):
    # Hand-derived from the pinned per-class loaders for 10.1.0.0.
    out = struct.pack("<I", gid)            # NiObject GroupID (gate range)
    out += cstring(name)                     # NiObjectNET name
    out += struct.pack("<I", 0)              # extraData multi-link count
    out += struct.pack("<I", NULL_LINK)      # controller link
    out += struct.pack("<H", 0)              # NiAVObject flags u16
    out += struct.pack("<3f", 0.0, 0.0, 0.0)             # translate
    out += struct.pack("<9f", 1.0, 0.0, 0.0,             # rotate identity
                       0.0, 1.0, 0.0,
                       0.0, 0.0, 1.0)
    out += struct.pack("<f", 1.0)                       # scale
    out += struct.pack("<I", 0)              # properties list (v >= 5.0.0.19)
    out += struct.pack("<I", NULL_LINK)      # collision link
    out += struct.pack("<I", 0)              # NiNode children list
    out += struct.pack("<I", 0)              # NiNode effects list
    return out


def footer(roots):
    # LoadTopLevelObjects L367-385: u32 count + i32 per root.
    return struct.pack("<I", len(roots)) + \
        b"".join(struct.pack("<i", r) for r in roots)


def write(name, data):
    path = os.path.join(HERE, name)
    with open(path, "wb") as fh:
        fh.write(data)
    print("%s size=%d sha256=%s" %
           (name, len(data),
            hashlib.sha256(data).hexdigest().upper()))
    return path


def main():
    # A. registered-only baseline: table [NiNode], 1 object -> NiNode.
    write("fx_A_registered_only.nif",
          header(1) + rtti_table(["NiNode"]) + type_indices([0]) +
          groups() + ninode_body() + footer([0]))

    # B. the F1 counterexample shape: table [NiNode, NiXyzzyx], 1 object ->
    # idx 0 (NiNode). NiXyzzyx is UNUSED by any object.
    write("fx_B_unused_unregistered.nif",
          header(1) + rtti_table(["NiNode", "NiXyzzyx"]) +
          type_indices([0]) + groups() + ninode_body() + footer([0]))

    # C1. table-order first miss + TRAILING unknown run (2 objects, the
    # unknown block is LAST): table [NiNode, NiXyzzyx, NiQuuxzyx]; obj0 ->
    # idx 0 (NiNode), obj1 -> idx 2 (NiQuuxzyx). Kept as a permanent input
    # documenting the PRE-EXISTING presolver boundary crash (the E3
    # pre-solver's assemble() calls decode_block_at(b, run_end) with
    # run_end == n_obj when the last unknown run extends to EOF; Desktop
    # post-audit F4 territory, OUT OF SCOPE of the F1 run -- --full-decode
    # on this fixture exits 1 both pre- and post-F1-fix).
    body1_pad = struct.pack("<I", 0xDEADBEEF)
    write("fx_C1_trailing_unknown_run.nif",
          header(2) + rtti_table(["NiNode", "NiXyzzyx", "NiQuuxzyx"]) +
          type_indices([0, 2]) + groups() + ninode_body("n0") +
          body1_pad + footer([0]))

    # C2. THE C test: >= 2 unregistered table entries + object order
    # different from table order, with the unknown run in the MIDDLE
    # (standard T-corpus shape; the closure machinery is expected to work):
    # table [NiNode, NiXyzzyx, NiQuuxzyx]; obj0 -> idx 0 (NiNode),
    # obj1 -> idx 2 (NiQuuxzyx), obj2 -> idx 0 (NiNode). Object-reference
    # order meets NiQuuxzyx FIRST; source table order meets NiXyzzyx FIRST
    # (table index 1). Ordinary mode must reject at NiXyzzyx; --full-decode
    # must keep SOURCE_PREDICTED_VERDICT=REJECTED with FIRST_RTTI_MISS=
    # NiXyzzyx (table order), never the object-order miss.
    write("fx_C2_table_vs_object_order.nif",
          header(3) + rtti_table(["NiNode", "NiXyzzyx", "NiQuuxzyx"]) +
          type_indices([0, 2, 0]) + groups() + ninode_body("n0") +
          body1_pad + ninode_body("n2") + footer([0]))

    # E. unused first table miss + incomplete later object indices:
    # header claims 3 blocks; only ONE u16 type index exists before the body
    # region. The ordinary-mode source scan must reject at NiXyzzyx BEFORE
    # the incomplete index list is ever read.
    write("fx_E_incomplete_indices.nif",
          header(3) + rtti_table(["NiNode", "NiXyzzyx"]) +
          type_indices([0]) + groups() + ninode_body() + footer([0]))

    # F. first table miss + truncated later RTTI name: table count = 3;
    # name[0] = NiNode, name[1] = NiXyzzyx (the FIRST miss, table index 1),
    # name[2] declares a u32 length (0x00000400) with NO bytes behind it
    # (EOF). The FIRST miss precedes the truncated later name and must be
    # preserved (no parser error may mask it).
    write("fx_F_truncated_later_name.nif",
          header(1)
          + struct.pack("<H", 3)
          + rtti_string("NiNode") + rtti_string("NiXyzzyx")
          + struct.pack("<I", 0x00000400))


if __name__ == "__main__":
    main()
