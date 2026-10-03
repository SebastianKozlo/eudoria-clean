#!/usr/bin/env python3
# build_fixtures_c1.py -- hand-built synthetic NIF fixtures for the F1-C1
# correction run PE_GAMEBRYO_ORACLE_F1_C1_EXTENSION_HALT_R1_20261003
# (Desktop post-audit
#  C:\Users\User\Documents\ChatGPT\PE\
#  PE_GAMEBRYO_ORACLE_F1_DESKTOP_POST_AUDIT_20261003\REPORT.md,
#  finding F1-C1/P2: a DecodeError on a LATER RTTI name under --full-decode
#  must STOP the extension AT the table failure -- never continue into
#  object indices/groups/bodies from the undetermined table boundary).
#
# QC DISCIPLINE: the byte layouts below are derived INDEPENDENTLY from the
# pinned source canon (NiStream.cpp E955C36E...: LoadHeader L303-360,
# LoadRTTI L412-449 [u16 usRTTICount; per entry LoadRTTIString u32 len +
# bytes, L1145-1153], LoadObjectGroups L470-487, LoadTopLevelObjects
# L367-385; NiStream.cpp L70: MAX_RTTI_LEN = 256 -- a valid RTTI string
# length satisfies 0 < uiLength < 256; NiObject.cpp B137FE42...: GroupID
# u32 iff 5.0.0.6 <= v < 10.1.0.114; NiObjectNET.cpp 2ADB8F89...: name
# LoadCString, extraData multi-link list iff v >= 5.0.0.11, controller
# link; NiAVObject.cpp 72E08371...: flags u16 + local transform 3f/9f/f +
# properties list + collision link for v >= 5.0.0.19; NiNode.cpp
# 38C7A1DE...: children + effects lists) -- NOT from the adapter code
# under correction.
#
# All bytes are OUR OWN synthetic data. Zero proprietary content.
#
# REPO POLICY: the repo-wide .gitignore excludes *.nif (zero NIF files are
# tracked anywhere in this repo by design). The generated fixtures are NOT
# committed; this script is the committed DETERMINISTIC regeneration source
# (byte-identical output; SIZE + SHA256 pins in ../INPUT_IDENTITIES.md).
# Physical copies are preserved in this run's external sandbox:
# D:\Eudoria_Reconstruction\99_Audits\
# PE_GAMEBRYO_ORACLE_F1_C1_EXTENSION_HALT_R1_20261003\sandbox\01_FIXTURES\
# The raw-test records reference the package-dir execution paths used
# during the run; regenerate with `python build_fixtures_c1.py` in any
# directory to verify the SIZE + SHA256 pins.
#
# Fixtures (all declare NIF 10.1.0.0, 1 header block):
#   fx_C1A_truncated_name_indexlike.nif -- counterexample class A
#     (TRUNCATED RTTI NAME + INDEX-LIKE REMAINING BYTES). Table declares
#     n_types=3: name[0]="NiNode" (registered), name[1]=
#     "NiDesktopFirstMissing" (UNREGISTERED -- the first table miss at
#     table index 1), name[2] declares a correct source-range length 127
#     (0 < 127 < MAX_RTTI_LEN=256) but only 2 payload bytes exist before
#     EOF (the truncated-name payload bytes are "\x02\x00": a value a
#     buggy continuation would read as the VALID type index 2 < n_types).
#     PRE-FIX --full-decode: the leftover name bytes are consumed as the
#     object type index; the histogram loop then raises IndexError
#     (type_names[2] with only 2 names read) -> traceback, empty stdout,
#     exit 1 (the Desktop counterexample 1 behavior family).
#   fx_C1B_truncated_name_fake_body.nif -- counterexample class B
#     (TRUNCATED RTTI NAME + FAKE-BODY-LIKE REMAINING BYTES). Same table
#     shape; the declared length is again 127, but the 104 remaining
#     bytes are crafted so a buggy continuation reads them as a COMPLETE
#     stream: u16 type index 0 (NiNode) + u32 object groups 0 + a 90-byte
#     NiNode body (pinned per-class field sequence for 10.1.0.0) + a valid
#     8-byte TopObjects footer (count 1, root 0). PRE-FIX --full-decode:
#     a SPURIOUS NiNode object, object_reference_histogram/census, groups
#     and roots=[0] are reconstructed out of the unfinished name's bytes
#     (the Desktop counterexample 2 behavior family).
#   fx_F_truncated_later_name.nif -- byte-identical regeneration of the
#     published F1-run fixture F (SIZE 79 / SHA256 B171020E... pins in
#     INPUT_IDENTITIES.md), re-generated here only so this run can record
#     the F-fixture --full-decode delta (the halt now happens AT the
#     table failure instead of at the object-index stage) without
#     touching the historical package.
#
# Registry assumptions (verified by the run's QC):
#   "NiNode" IS in the GB12 factory registry; "NiDesktopFirstMissing" is
#   NOT (synthetic name, absent from the 198-class census).

import hashlib
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))

VER_10_1_0_0 = 0x0A010000
NULL_LINK = 0xFFFFFFFF
MAX_RTTI_LEN = 256          # NiStream.cpp L70
DECLARED_NAME2_LEN = 127    # 0 < 127 < MAX_RTTI_LEN (source-valid range)
MISS_NAME = "NiDesktopFirstMissing"   # 21 chars, unregistered synthetic


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


def truncated_name_table(prefix_bytes):
    # LoadRTTI L414-434 layout with a THIRD entry whose declared length is
    # source-valid (127) but whose payload is `prefix_bytes` (< 127) and
    # then EOF: the ORIGINAL LoadRTTIString read of entry[2] cannot
    # complete -- the table boundary past entry[1] is UNDETERMINED.
    out = header(1)
    out += struct.pack("<H", 3)
    out += rtti_string("NiNode")
    out += rtti_string(MISS_NAME)
    out += struct.pack("<I", DECLARED_NAME2_LEN)
    out += prefix_bytes
    return out


def write(name, data):
    path = os.path.join(HERE, name)
    with open(path, "wb") as fh:
        fh.write(data)
    print("%s size=%d sha256=%s" %
           (name, len(data),
            hashlib.sha256(data).hexdigest().upper()))
    return path


def main():
    # Counterexample class A: the 2 leftover bytes of the unfinished
    # third name are "\x02\x00" -- a buggy continuation reads them as the
    # VALID object type index 2 (< n_types=3).
    write("fx_C1A_truncated_name_indexlike.nif",
          truncated_name_table(b"\x02\x00"))

    # Counterexample class B: the 104 leftover bytes of the unfinished
    # third name are crafted as a COMPLETE post-table stream (index +
    # groups + NiNode body + valid footer) for a buggy continuation to
    # "reconstruct".
    fake = (struct.pack("<H", 0)          # object type index -> NiNode
            + struct.pack("<I", 0)         # LoadObjectGroups: numGroups 0
            + ninode_body("root")          # 90-byte NiNode body
            + footer([0]))                # TopObjects footer
    assert len(fake) == 2 + 4 + 90 + 8 == 104
    assert len(fake) < DECLARED_NAME2_LEN   # the name read still fails
    write("fx_C1B_truncated_name_fake_body.nif",
          truncated_name_table(fake))

    # Byte-identical regeneration of the published F1-run fixture F
    # (verified against the pin SHA256 B171020E... at run time; kept for
    # the F-fixture --full-decode delta record of THIS run only).
    write("fx_F_truncated_later_name.nif",
          header(1)
          + struct.pack("<H", 3)
          + rtti_string("NiNode") + rtti_string("NiXyzzyx")
          + struct.pack("<I", 0x00000400))


if __name__ == "__main__":
    main()
