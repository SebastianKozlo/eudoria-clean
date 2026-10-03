#!/usr/bin/env python3
# gb12core.py -- SOURCE_DERIVED_REIMPLEMENTATION of the Gamebryo 1.2.2 (GB_1_2)
# NiStream NIF load semantics for tools/gamebryo_oracle.
#
# ERA CATEGORY: GB_1_2. This module is OUR code. It re-implements the loader
# semantics proven from the ORIGINAL Gamebryo 1.2.2 source tree held locally at
# D:\gamebyroengine\extracted\Gb12_Source (read-only input). ZERO proprietary
# source bytes are embedded here; only the load semantics + class NAME lists.
#
# SOURCE CANON (per E1 02_ANALYSIS/VERSION_SUPPORT.md + NIF_LOAD_PIPELINE.md +
# direct source reads this run; all hashes are SHA256 of the cited file):
#   NiStream.cpp   E955C36EBBB442029E00BE8A154726741B8454A607F2DC043F1FD542B009DC25
#     LoadHeader L303-360: "File Format" substring test; packed-u32 gate
#       [ms_uiNifMinVersion=3.3.0.11 (L42-43), ms_uiNifMaxVersion=10.2.0.0
#       (L44-46)]; user-defined version iff file ver >= 10.0.1.8 (L335);
#       uiObjects u32 (L355).
#     LoadRTTI L412-449: u16 RTTICount; the table is validated IN SOURCE
#       ORDER (L421-433: per entry LoadRTTIString (u32 len + bytes,
#       L1145-1153) -> ms_pkLoaders factory lookup -> next entry); the FIRST
#       unregistered name aborts with RTTIError(name) (NO_CREATE_FUNCTION
#       "<name>: cannot find create function.", L396-400) -> return false
#       (ORIGINAL fail-closed verdict) BEFORE any later table name, the
#       per-object type indices (L436-444), the object groups or any body.
#       EVERY table entry is validated including entries no object
#       references (F1 fix 2026-10-03: the pre-F1 build validated by
#       iterating object type indices, silently skipping unused unregistered
#       entries and reporting the first miss in object order).
#     LoadObject L451-468 (LEGACY < 5.0.0.1): RTTI string INLINE per object
#       (the F1 table-order fix does NOT apply to this legacy layout).
#     LoadObjectGroups L470-487 (iff ver >= 5.0.0.6): u32 numGroups + u32 sizes.
#     LoadStream L506-635: bNew = ver >= 5.0.0.1; per-object LoadBinary loop;
#       link loop (LinkObject); postlink loop (PostLinkObject);
#       LoadTopLevelObjects (u32 count + u32 links); EOF at exact position.
#     ReadLinkID L219-224 (u32); ReadMultipleLinkIDs L258-268 (u32 n + n*u32);
#     LoadCString L1123-1140 (i32 len; bytes if len > 0).
#   NiObject.cpp    B137FE42126F496A37E7627061FF968256A6DA87D912784865609E2122FE470E
#     LoadBinary L134-143: per-block GroupID u32 iff 5.0.0.6 <= v < 10.1.0.114.
#   NiObjectNET.cpp 2ADB8F89CDB40F8C114FEAA6E4A32DD7A1CC73BCE30D745F669458EE6F354190
#     LoadBinary L553-571: LoadCString(name); extraData single link iff
#     v < 5.0.0.11 else ReadMultipleLinkIDs; controller link.
#   NiAVObject.cpp  72E0837149B03CCDA171BDF5E68E1E1F8C2712B2F10E7957AC3EC26344CA5EA7
#     LoadBinary L546-699: flags u16 + conversion shifts (v<4.1.0.11 / <4.1.0.12
#     / <5.0.0.1); translate 3f L602; rotate 3x3f L603; scale f L604;
#     v<5.0.0.19 legacy: velocity 3f + property ReadMultipleLinkIDs + bABV;
#     else property ReadMultipleLinkIDs + collision ReadLinkID.
#   NiNode.cpp      38C7A1DE1E166345068D296F70F34B1ADAE27C694E19EAD8FA0FBD8B62E0E016
#     LoadBinary L861-870: children + effects ReadMultipleLinkIDs.
#   NiProperty.cpp  EAE249CE21DD7A6294CF032BA75C9EF99137C36A171C51C205804714B32790F4
#     LoadBinary L444-457: NiObjectNET + flags u16 iff v < 10.0.1.2 (stashed for
#     derived classes per NiProperty::MAX_POS shift).
#   NiMaterialProperty.cpp 142876B98E8B383D7F7BAD717E9EDD398BF815BC7E0C82058FCE21F12E00B296
#     LoadBinary L94-103: amb/diff/spec/emit NiColor(3f each) + shine f + alpha f.
#   NiZBufferProperty.cpp   6C75642526A9320728272C01C550697BB572C94F6E845F50B8E68F5F1D1578A9
#     LoadBinary L52-78: own flags u16 iff v >= 10.0.1.2 (else derived from the
#     stashed NiProperty flags); enum u32 iff v >= 4.1.0.5.
#   NiAlphaProperty.cpp     3A5DBDAA65FD6DD7E874D42579C5D411EC6491B3062D19D10EB2564E46CF9DE9
#     LoadBinary L60-87: own flags u16 iff v >= 10.0.1.2; alphaTestRef u8.
#   NiVertexColorProperty.cpp FADE3838509C3B1806A5B7F6C6D2830C9BBD942177C756C335122CCE7D16AA6A
#     LoadBinary L53-77: own flags u16 iff v >= 10.0.1.2; 2 enum u32.
#   NiTexturingProperty.cpp 2BC36C08E8B9E0AB624569FF098F1CD60B8242B737C0EB7B3E4DD3A6615BA106
#     LoadBinary L238-349: apply enum u32; u32 listSize; per-map NiBool bHasMap
#     (iff v >= 4.1.0.0); bump-map slot logic (v >= 3.3.0.13); Map::LoadBinary
#     L838-867 (link + clamp enum u32 + filter enum u32 + texCoord u32 + sL s16
#     + sK s16 + 2x NiBool iff v < 4.1.0.16 + NiBool bTextureTransform iff
#     v >= 10.0.1.10 then NiTextureTransform inline); BumpMap L931-942 (+5f);
#     ShaderMap L987-991 (+u32); shader maps iff v >= 5.0.0.17 (L319-346).
#   NiTextureTransform.cpp (NiMain): LoadBinary L78-89: translate 2f + scale 2f
#     + rotate f + method enum u32 + center 2f.
#   NiSourceTexture.cpp B5D0BB026B812CA4D022E110D7CFE0B98ECA181C06F78C62A999512C0927E70E
#     LoadBinary L162-313: NiTexture (-> NiObjectNET) + v >= 10.0.1.4: bExternal
#     NiBool + LoadCString(filename) + pixelData link; legacy v < 10.0.1.4:
#     bSaveName layout; then 3 enum u32 (pixelLayout, mipMapped, alphaFmt) +
#     bStatic NiBool + bLoadDirectToRendererHint iff v >= 10.1.0.103.
#   NiGeometry.cpp FDE29A81FBD5B7F8DF34320DCF9DC91FE32D7D9F2E6E5F70B30B976953EAF335
#     LoadBinary L351-382: NiAVObject + modelData link + skinInstance link +
#     bShader NiBool iff v >= 5.0.0.21 (+NiShader inline when set).
#   NiTriBasedGeom.cpp 370C05ADBAF6BAD1DF710F3CC932FE57F9009C60CE89C02B42CE07FF05855D07 (empty shell)
#   NiTriShape.cpp     F9F3D6F769221DFA57BA9DF2B6E853853F4F2958A9BB8C3FF40FA3A860FA77A6 (empty shell)
#   NiGeometryData.cpp 7E7C09014E87027F32C07B304C58939A561C30DA076B64B4E5D4BA88712D7A8A
#     LoadBinary L519-704: GroupID iff v >= 10.1.0.114; usVertices u16;
#     keep/compress u8+u8 iff v >= 10.0.1.16; bHasVertex NiBool; vertices;
#     dataFlags u16 iff v >= 10.0.0.2 (normals x3 if NBT); bHasNormal NiBool;
#     normals; bound (NiBound: center 3f + radius f, L618); bHasColor NiBool;
#     colors; texture sets: s16 iff v < 5.0.0.10, u16 flags elif v < 10.0.0.2;
#     texcoords; dirtyFlags u16 iff v >= 5.0.0.10.
#   NiTriBasedGeomData.cpp 1AE42F53FBCFBBCAB15FFA294FB41C8F7A21804ABC04DD7E1A0EBB783D04A607
#     LoadBinary L59-64: + usTriangles u16.
#   NiTriShapeData.cpp 776D59EA2AD420028D9238B16178BC00F773B32369985AC02805122DC1DAF3A3
#     LoadBinary L220-293: + uiTriListLength u32; bHasList NiBool iff
#     v >= 10.0.1.17 (else true); tri list u16 x n; shared normals: u16 size +
#     per entry u16 count + u16 x count.
#   NiDynamicEffect.cpp 86B7E41A71B0268513483F33F680ABCC65F8503AFEC335996DAD88A01209B07A
#     LoadBinary L138-165: NiAVObject + bOn NiBool iff v >= 10.1.0.102;
#     affected-node pointer list iff v < 4.1.0.0; unaffected ReadMultipleLinkIDs
#     iff v >= 10.0.1.14.
#   NiLight.cpp     E76FD632FCC43C81B6112F7658EA2D3E10821C170167674EE8CC277FCF588E35
#     LoadBinary L75-84: dimmer f + amb/diff/spec NiColor (3f each).
#   NiDirectionalLight.cpp C4B511FC75B562CFF2960958DEB07E6C2CBC385F4C5A4902E88F24043E9C5E44 (shell)
#   NiPointLight.cpp 5F1D398E67E166D0F8ADE7BBEAC3788482EF4AEB77DC05DC4329162FC4725FDE
#     LoadBinary L64-71: + atten0/atten1/atten2 f.
#   NiTimeController.cpp B400580C0E83FAF6F794813287629622592E312F6AEEDF94CA09EFC09462FDEA
#     LoadBinary L466-516: NiObject + next link + flags u16 + frequency f +
#     phase f + loKeyTime f + hiKeyTime f + target link + v==10.0.1.1 bool /
#     v<10.0.1.1 flag shift + v<10.1.0.109 manager-bit clear.
#   NiExtraData.cpp  BD3587F1AD8B89D16144521DCF4377FFB049B282F84C12235338D693B6A7464E
#     LoadBinary L109-137: v < 5.0.0.11: next link + u32 size (+ chunk bytes iff
#     exact-kind NiExtraData); else LoadCString(name).
#   NiStringExtraData.cpp 1646ADFB51DC1D0BA40906F97B5B79A7A78860E14F3B79AEA50D1501BEDA8B1E
#     LoadBinary L81-85: NiExtraData + LoadCString(string).
#   NiColor.cpp     AA909DDF51649FE63DC6290F650617C3CB8C47687E1E67DAC26441F9E5C75503 (3f)
#   NiPoint3.cpp    9A4D8976096A3DF1E7D02F76B4CAB49020C7FE2C58985B3B84DE20AC2960F49C (3f)
#   NiBound.cpp     F34BB0B9D7BAD147EF3F0FD4E622541A53BD5AAE2F4FCD1077AF863E2FA663A1 (center+radius)
#   Win32\NiTransform.inl: operator* L15-24: scale=sa*sb; rotate=Ra*Rb;
#     translate=ta + sa*(Ra*tb). UpdateWorldData (NiAVObject_Win32.cpp L22-31):
#     m_kWorld = parent ? parent->m_kWorld * m_kLocal : m_kLocal.
#
# FACTORY REGISTRY: GB 1.2 registers loaders via NiRegisterStream(...) /
# NiStream::RegisterLoader("name", ...) in the per-lib *SDM.cpp static data
# managers. The embedded GB12_REGISTERED_CLASSES list is the de-duplicated
# census of those calls across Gb12_Source\CoreLibs (198 names; census list
# embedded in adapters/gb12/registry.py (SHA256 7CD9A5ED...; per-SDM
# provenance in its header); zero NiArk*
# classes occur anywhere in the registry). A prebuilt tool links a SUBSET of
# CoreLibs, but NiArk* is registered in NO SDM, so the fail-closed RTTI verdict
# for NiArk* blocks is invariant to the linked subset.
#
# --full-decode EXTENSION (OURS, NEVER ORIGINAL BEHAVIOR): the original GB 1.2
# Load() FAILS the whole load at the first unregistered RTTI class (in RTTI
# TABLE order, including unused entries -- F1 fix). With --full-decode the
# adapter continues the stream decode past such blocks (recording them as
# unknowns with closure-derived byte boundaries) so the known-class field
# data can be compared against our own decoder. In that mode the JSON
# reports load_result.accepted=false + error=RTTIError(<class>) +
# partial=true + decode_continued_after_rtti_gate=true, keeps
# rtti_table_validation.source_predicted_verdict=REJECTED and
# first_rtti_miss=<first miss in TABLE order>, and labels every continuation
# past the miss (extension_observation) as OUR extension. If the extension
# itself hits a parser failure (truncated later table name, corrupt/incomplete
# object indices), it halts with an EXTENDED_* warning and the
# source-predicted verdict is never masked. The ORIGINAL verdict is always
# reported and is never silently merged with the extension.

import hashlib
import json
import struct
import sys as _sys


TOOL_NAME = "gamebryo_oracle"
TOOL_VERSION = "1.0.0"
ORACLE_MODE = "SOURCE_DERIVED_REIMPLEMENTATION"
ERA_CATEGORY = "GB_1_2"

GB12_NIF_MIN = (3, 3, 0, 11)
GB12_NIF_MAX = (10, 2, 0, 0)
USER_VERSION_GATE = (10, 0, 1, 8)
NULL_LINKID = 0xFFFFFFFF


def ver_u32(maj, minr, patch, internal):
    return ((maj & 0xFF) << 24) | ((minr & 0xFF) << 16) | \
           ((patch & 0xFF) << 8) | (internal & 0xFF)


def u32_to_ver(v):
    return "%d.%d.%d.%d" % ((v >> 24) & 0xFF, (v >> 16) & 0xFF,
                            (v >> 8) & 0xFF, v & 0xFF)


V_MIN = ver_u32(*GB12_NIF_MIN)
V_MAX = ver_u32(*GB12_NIF_MAX)
V_USER_GATE = ver_u32(*USER_VERSION_GATE)
V_BNEW = ver_u32(5, 0, 0, 1)
V_GROUPS = ver_u32(5, 0, 0, 6)
V_GROUPID_LO = ver_u32(5, 0, 0, 6)
V_GROUPID_HI = ver_u32(10, 1, 0, 114)
V_EXTRADATA_MULTI = ver_u32(5, 0, 0, 11)
V_AVOBJ_NEW_COLLISION = ver_u32(5, 0, 0, 19)
V_AVOBJ_FLAG_4_1_11 = ver_u32(4, 1, 0, 11)
V_AVOBJ_FLAG_4_1_12 = ver_u32(4, 1, 0, 12)
V_AVOBJ_FLAG_5_0_0_1 = ver_u32(5, 0, 0, 1)
V_PROP_OWN_FLAGS = ver_u32(10, 0, 1, 2)
V_ZBUF_ENUM = ver_u32(4, 1, 0, 5)
V_TEX_BUMPSLOT = ver_u32(3, 3, 0, 13)
V_TEX_HASMAP_PTR = ver_u32(4, 1, 0, 0)
V_TEX_MANUAL = ver_u32(4, 1, 0, 16)
V_TEX_TEXTRANSFORM = ver_u32(10, 0, 1, 10)
V_TEX_SHADERMAPS = ver_u32(5, 0, 0, 17)
V_GEOM_SHADER = ver_u32(5, 0, 0, 21)
V_GEOMDATA_GROUPID = ver_u32(10, 1, 0, 114)
V_GEOMDATA_KEEPCOMPRESS = ver_u32(10, 0, 1, 16)
V_GEOMDATA_DATAFLAGS = ver_u32(10, 0, 0, 2)
V_GEOMDATA_TEXSETS_S16 = ver_u32(5, 0, 0, 10)
V_GEOMDATA_TEXPTR = ver_u32(4, 1, 0, 0)
V_TRISHAPEDATA_HASLIST = ver_u32(10, 0, 1, 17)
V_EFFECT_ON = ver_u32(10, 1, 0, 102)
V_EFFECT_AFFECTED_PTR = ver_u32(4, 1, 0, 0)
V_EFFECT_UNAFFECTED = ver_u32(10, 0, 1, 14)
V_SRCTEX_NEW = ver_u32(10, 0, 1, 4)
V_SRCTEX_DIRECTRENDER = ver_u32(10, 1, 0, 103)
V_TIMECTL_PLAYBACKWARDS_EXACT = ver_u32(10, 0, 1, 1)
V_TIMECTL_MANAGERBIT = ver_u32(10, 1, 0, 109)
V_EXTRADATA_OLD = ver_u32(5, 0, 0, 11)

# --- E3 batch version gates (particle + animation families; all cited in the
# per-class loader bodies below) ---
V_INTERP_NEW = ver_u32(10, 1, 0, 104)       # NiInterpController/NiSingleInterp-
                                           # Controller interpolator link;
                                           # NiPSysEmitterCtlr m_spData branch;
                                           # NiTextureTransformController /
                                           # NiMaterialColorController legacy
                                           # data links; emitter-active key
                                           # type enum gate
V_INTERP_MANAGER = ver_u32(10, 1, 0, 109)   # NiInterpController manager-
                                           # controlled bool window
V_MATERCOLOR_OWNFLAGS = ver_u32(10, 0, 1, 2)  # own flags u16 vs stashed flags
V_BNDUPD_SKIP_EXACT = ver_u32(10, 1, 0, 100)  # usUpdateSkip u16 (<=) vs s16
V_PARTICLESDATA_LEGTRI = ver_u32(4, 1, 0, 7)  # legacy triangles/sizes layout
V_PARTICLESDATA_RADII_ARRAY = ver_u32(10, 0, 1, 13)  # single radius vs array
V_PARTICLESDATA_ROTATIONS = ver_u32(5, 0, 0, 8)  # bHasRotation gate

# NiAnimationKey.h L38-46 (SHA256 3926E78433A2FCA3942FE261FADC07A5CAD106F1
# 5A01F99BBDB288E1C0D9AD2D): KeyType { NOINTERP, LINKEY, BEZKEY, TCBKEY,
# EULERKEY, STEPKEY, NUMKEYTYPES } -- 0..5.
KEYTYPE_NOINTERP = 0
KEYTYPE_LIN = 1
KEYTYPE_BEZ = 2
KEYTYPE_TCB = 3
KEYTYPE_EULER = 4
KEYTYPE_STEP = 5

# NiTexturingProperty::BUMP_INDEX = 3 (source: bump map slot after decal1;
# the slot is skipped as a regular map and decoded as BumpMap when present)
BUMP_INDEX = 3

# NiGeometryData.h L54-59: NBT_METHOD_NONE=0x0000, NBT_METHOD_MASK=0xF000,
# TEXTURE_SET_MASK=0x003F; GetTextureSets() = m_usDataFlags & TEXTURE_SET_MASK
# (NiGeometryData.inl L79-82); SetNumTextureSets stores into the same bits
# (inl L148-152). For v >= 10.0.0.2 the texture-set count is DERIVED from the
# data flags read at L576 (nothing more is read for it at L654-664).
NBT_METHOD_MASK = 0xF000
TEXTURE_SET_MASK = 0x003F


class DecodeError(Exception):
    """Structural decode failure (mapped to an explicit JSON error)."""


class NotSupportedByAdapter(Exception):
    """Class/feature not implemented in this adapter (fail-closed,
    recorded; NEVER silently skipped)."""


class Reader(object):
    __slots__ = ("data", "pos")

    def __init__(self, data, pos=0):
        self.data = data
        self.pos = pos

    def read(self, n):
        if self.pos + n > len(self.data):
            raise DecodeError("EOF: need %d bytes at %d" % (n, self.pos))
        b = self.data[self.pos:self.pos + n]
        self.pos += n
        return b

    def u8(self):
        return self.read(1)[0]

    def u16(self):
        return struct.unpack("<H", self.read(2))[0]

    def i16(self):
        return struct.unpack("<h", self.read(2))[0]

    def u32(self):
        return struct.unpack("<I", self.read(4))[0]

    def i32(self):
        return struct.unpack("<i", self.read(4))[0]

    def f32(self):
        return struct.unpack("<f", self.read(4))[0]

    def cstring(self):
        # NiStream::LoadCString L1123-1140: i32 length; bytes if > 0.
        n = self.i32()
        if n > 0:
            return self.read(n).decode("latin-1")
        return None

    def u32_count(self, elem=4):
        # u32 count of a following list of `elem`-byte elements (links, map
        # slots, keys). E3 plausibility bound: a count whose n*elem payload
        # cannot fit in the remaining bytes can never decode. For valid
        # streams this is OUTCOME-EQUIVALENT (the reads would fail at EOF
        # anyway); for a wrong-boundary closure candidate it fails in O(1)
        # instead of looping over the whole remaining file.
        n = self.u32()
        if n > (len(self.data) - self.pos) // elem:
            raise DecodeError("COUNT_BOUND: %d x %dB exceeds remaining %dB"
                              % (n, elem, len(self.data) - self.pos))
        return n

    def rtti_string(self):
        # NiStream::LoadRTTIString L1145-1153: u32 length + bytes.
        n = self.u32()
        return self.read(n).decode("latin-1")

    def line(self):
        # NiBinaryStream::GetLine analogue: read to newline (128 cap).
        end = self.data.find(b"\x0a", self.pos)
        if end == -1 or end - self.pos > 128:
            raise DecodeError("header line missing newline")
        line = self.data[self.pos:end]
        self.pos = end + 1
        return line.decode("latin-1")


def f(x):
    # deterministic float serialization (round-trip repr)
    return struct.unpack("<f", struct.pack("<f", x))[0]


# --------------------------------------------------------------------------
# per-class GB 1.2 LoadBinary implementations (bodies proven from source)
# --------------------------------------------------------------------------

def load_niobject(r, ver, o):
    # NiObject::LoadBinary L134-143: GroupID u32 iff 5.0.0.6 <= v < 10.1.0.114.
    if V_GROUPID_LO <= ver < V_GROUPID_HI:
        o["group_id"] = r.u32()


def load_niobjectnet(r, ver, o, links):
    # NiObjectNET::LoadBinary L553-571.
    load_niobject(r, ver, o)
    o["name"] = r.cstring()
    if ver < V_EXTRADATA_MULTI:
        links.append(("extra_data_legacy", [r.u32()]))
    else:
        n = r.u32_count(4)
        links.append(("extra_data", [r.u32() for _ in range(n)]))
    links.append(("controller", [r.u32()]))


def load_niavobject(r, ver, o, links):
    # NiAVObject::LoadBinary L546-699.
    load_niobjectnet(r, ver, o, links)
    flags = r.u16()
    # --- NIF conversion code (L554-600) ---
    if ver < V_AVOBJ_FLAG_4_1_11:
        us = flags & 0xFFFF
        flags = ((flags << 1) & 0xFFFF) & ~0x000F
        flags |= (us & 0x0007)
    if ver < V_AVOBJ_FLAG_4_1_12:
        us = flags & 0xFFFF
        flags = ((flags << 4) & 0xFFFF) & ~0x00FF
        flags |= (us & 0x000F)
        flags |= 0x0010 | 0x0020 | 0x0040
        flags &= ~0x0080
    if ver < V_AVOBJ_FLAG_5_0_0_1:
        us = flags & 0xFFFF
        flags = ((flags << 1) & 0xFFFF) & ~0x01FF
        flags |= (us & 0x00FF)
    o["flags_u16"] = flags
    # local transform L602-604
    o["local_transform"] = {
        "translate": [f(r.f32()), f(r.f32()), f(r.f32())],
        "rotate": [[f(r.f32()), f(r.f32()), f(r.f32())],
                   [f(r.f32()), f(r.f32()), f(r.f32())],
                   [f(r.f32()), f(r.f32()), f(r.f32())]],
        "scale": f(r.f32()),
    }
    o["local_transform_semantics"] = "SERIALIZED_LOCAL_TRANSFORM (NiAVObject.cpp L602-604)"
    if ver < V_AVOBJ_NEW_COLLISION:
        # legacy L606-670: velocity + property list + ABV flag
        vel = [f(r.f32()), f(r.f32()), f(r.f32())]
        n = r.u32_count(4)
        links.append(("properties", [r.u32() for _ in range(n)]))
        if ver < V_TEX_HASMAP_PTR:
            raise NotSupportedByAdapter("NiAVObject pre-4.1.0.0 ABV pointer path")
        babv = r.u8()
        o["legacy_velocity"] = vel
        o["legacy_abv_flag"] = babv
        if babv:
            raise NotSupportedByAdapter("NiAVObject legacy ABV tree (NiCollisionData)")
    else:
        n = r.u32_count(4)
        links.append(("properties", [r.u32() for _ in range(n)]))
        links.append(("collision_object", [r.u32()]))
    if ver < V_PROP_OWN_FLAGS:
        o["flags_stash_for_derived"] = flags  # SetLastNiAVObjectFlags L679-687


def load_ninode(r, ver, o, links):
    # NiNode::LoadBinary L861-870.
    load_niavobject(r, ver, o, links)
    n = r.u32_count(4)
    links.append(("children", [r.u32() for _ in range(n)]))
    n = r.u32_count(4)
    links.append(("effects", [r.u32() for _ in range(n)]))


def load_niproperty(r, ver, o, links):
    # NiProperty::LoadBinary L444-457.
    load_niobjectnet(r, ver, o, links)
    if ver < V_PROP_OWN_FLAGS:
        o["property_flags_stash"] = r.u16()  # SetLastNiPropertyFlags L49-55
    else:
        o["property_flags_stash"] = None


def _own_flags(r, ver, o):
    if ver >= V_PROP_OWN_FLAGS:
        return r.u16()
    return o.get("property_flags_stash", 0) >> 2  # NiProperty::MAX_POS = 2


def load_nimaterialproperty(r, ver, o, links):
    # NiMaterialProperty::LoadBinary L94-103.
    load_niproperty(r, ver, o, links)
    o["ambient_color"] = [f(r.f32()), f(r.f32()), f(r.f32())]
    o["diffuse_color"] = [f(r.f32()), f(r.f32()), f(r.f32())]
    o["specular_color"] = [f(r.f32()), f(r.f32()), f(r.f32())]
    o["emissive_color"] = [f(r.f32()), f(r.f32()), f(r.f32())]
    o["shine"] = f(r.f32())
    o["alpha"] = f(r.f32())


def load_nizbufferproperty(r, ver, o, links):
    # NiZBufferProperty::LoadBinary L52-78.
    load_niproperty(r, ver, o, links)
    o["zbuffer_flags_u16"] = _own_flags(r, ver, o)
    if ver >= V_ZBUF_ENUM:
        o["zbuffer_test_mode_u32"] = r.u32()


def load_nialphaproperty(r, ver, o, links):
    # NiAlphaProperty::LoadBinary L60-87.
    load_niproperty(r, ver, o, links)
    o["alpha_flags_u16"] = _own_flags(r, ver, o)
    o["alpha_test_ref_u8"] = r.u8()


def load_nivertexcolorproperty(r, ver, o, links):
    # NiVertexColorProperty::LoadBinary L53-77.
    load_niproperty(r, ver, o, links)
    o["vertexcolor_flags_u16"] = _own_flags(r, ver, o)
    o["source_mode_u32"] = r.u32()
    o["lighting_mode_u32"] = r.u32()


def _load_texturetransform(r):
    # NiTextureTransform::LoadBinary L78-89.
    return {
        "translate": [f(r.f32()), f(r.f32())],
        "scale": [f(r.f32()), f(r.f32())],
        "rotate": f(r.f32()),
        "method_u32": r.u32(),
        "center": [f(r.f32()), f(r.f32())],
    }


def _load_map(r, ver):
    # NiTexturingProperty::Map::LoadBinary L838-867.
    m = {"texture_link": r.u32()}
    m["clamp_mode_u32"] = r.u32()
    m["filter_mode_u32"] = r.u32()
    m["tex_coord_u32"] = r.u32()
    m["s_l_i16"] = r.i16()
    m["s_k_i16"] = r.i16()
    if ver < V_TEX_MANUAL:
        m["manual_uv_0"] = r.u8()
        m["manual_uv_1"] = r.u8()
    if ver >= V_TEX_TEXTRANSFORM:
        if r.u8():
            m["texture_transform"] = _load_texturetransform(r)
    return m


def load_nitexturingproperty(r, ver, o, links):
    # NiTexturingProperty::LoadBinary L238-349.
    load_niproperty(r, ver, o, links)
    o["apply_mode_u32"] = r.u32()
    list_size = r.u32_count(1)
    maps = []
    for i in range(list_size):
        if ver < V_TEX_HASMAP_PTR:
            raise NotSupportedByAdapter("NiTexturingProperty pre-4.1.0.0 map pointer path")
        b_has = r.u8()
        if ver < V_TEX_BUMPSLOT:
            raise NotSupportedByAdapter("NiTexturingProperty pre-3.3.0.13 slot shift path")
        if i == BUMP_INDEX:
            if b_has:
                bm = _load_map(r, ver)
                bm["luma_scale"] = f(r.f32())
                bm["luma_offset"] = f(r.f32())
                bm["bump_mat00"] = f(r.f32())
                bm["bump_mat01"] = f(r.f32())
                bm["bump_mat10"] = f(r.f32())
                bm["bump_mat11"] = f(r.f32())
                maps.append({"slot": i, "kind": "bump_map", "present": True, "map": bm})
            else:
                maps.append({"slot": i, "kind": "bump_map", "present": False})
            continue
        if b_has:
            maps.append({"slot": i, "kind": "map", "present": True,
                         "map": _load_map(r, ver)})
        else:
            maps.append({"slot": i, "kind": "map", "present": False})
    o["maps"] = maps
    if ver >= V_TEX_SHADERMAPS:
        n = r.u32_count(1)
        smaps = []
        for i in range(n):
            b = r.u8()
            if b:
                sm = _load_map(r, ver)
                sm["shader_id_u32"] = r.u32()
                smaps.append({"slot": i, "present": True, "map": sm})
            else:
                smaps.append({"slot": i, "present": False})
        o["shader_maps"] = smaps


def load_nitexture(r, ver, o, links):
    # NiTexture::LoadBinary -> NiObjectNET only (NiTexture.cpp).
    load_niobjectnet(r, ver, o, links)


def load_nisourcetexture(r, ver, o, links):
    # NiSourceTexture::LoadBinary L162-313.
    load_nitexture(r, ver, o, links)
    if ver < V_SRCTEX_NEW:
        # legacy bSaveName layout L172-200
        b_save_name = r.u8()
        if b_save_name:
            o["filename"] = r.cstring()
            o["external"] = True
        else:
            o["external"] = False
            b_save_pixel = r.u8()
            if b_save_pixel:
                links.append(("pixel_data", [r.u32()]))
            else:
                links.append(("pixel_data", []))
    else:
        o["external"] = bool(r.u8())
        o["filename"] = r.cstring()
        links.append(("pixel_data", [r.u32()]))
    o["pixel_layout_u32"] = r.u32()
    o["mip_mapped_u32"] = r.u32()
    o["alpha_format_u32"] = r.u32()
    o["static_bool"] = bool(r.u8())
    if ver >= V_SRCTEX_DIRECTRENDER:
        o["load_direct_to_renderer_bool"] = bool(r.u8())


def load_nigeometry(r, ver, o, links):
    # NiGeometry::LoadBinary L351-382.
    load_niavobject(r, ver, o, links)
    links.append(("model_data", [r.u32()]))
    links.append(("skin_instance", [r.u32()]))
    if ver >= V_GEOM_SHADER:
        if r.u8():
            raise NotSupportedByAdapter("NiGeometry inline NiShader payload")


def load_nitribasedgeom(r, ver, o, links):
    # NiTriBasedGeom::LoadBinary L81-84 (shell).
    load_nigeometry(r, ver, o, links)


def load_nitrishape(r, ver, o, links):
    # NiTriShape::LoadBinary L103-106 (shell).
    load_nitribasedgeom(r, ver, o, links)


def load_nigeometrydata(r, ver, o, links):
    # NiGeometryData::LoadBinary L519-704.
    load_niobject(r, ver, o)
    if ver >= V_GEOMDATA_GROUPID:
        o["geometry_group_id"] = r.u32()
    o["num_vertices"] = r.u16()
    if ver >= V_GEOMDATA_KEEPCOMPRESS:
        o["keep_flags_u8"] = r.u8()
        o["compress_flags_u8"] = r.u8()
    n_verts = o["num_vertices"]
    if ver >= V_TEX_HASMAP_PTR:
        b_has_vertex = r.u8()
    else:
        raise NotSupportedByAdapter("NiGeometryData pre-4.1.0.0 pointer path")
    o["has_vertices"] = bool(b_has_vertex)
    if b_has_vertex and n_verts:
        o["vertices_bbox"] = _bbox(r, n_verts, 3)
        r.read(0)  # no-op keeps structure explicit
    num_normals = n_verts
    o["has_data_flags"] = ver >= V_GEOMDATA_DATAFLAGS
    if ver >= V_GEOMDATA_DATAFLAGS:
        data_flags = r.u16()
        o["data_flags_u16"] = data_flags
        if (data_flags & NBT_METHOD_MASK) != 0:
            num_normals *= 3
            o["nbt_normals"] = True
    b_has_normal = r.u8()
    o["has_normals"] = bool(b_has_normal)
    if b_has_normal and num_normals:
        o["normals_bbox"] = _bbox(r, num_normals, 3)
    # bound L618: NiBound::LoadBinary (center 3f + radius f)
    o["model_bound"] = {
        "center": [f(r.f32()), f(r.f32()), f(r.f32())],
        "radius": f(r.f32()),
        "semantics": "MODEL_SPACE serialized NiGeometryData bound "
                     "(NiGeometryData.cpp L618; BOUNDING_VOLUME_SEMANTICS.md Q1)",
    }
    b_has_color = r.u8()
    o["has_colors"] = bool(b_has_color)
    if b_has_color and n_verts:
        o["colors_bbox"] = _bbox(r, n_verts, 4)
    if ver < V_GEOMDATA_TEXSETS_S16:
        o["num_texture_sets"] = r.i16()
    elif ver < V_GEOMDATA_DATAFLAGS:
        # second m_usDataFlags read (L662) carries the texture sets for
        # 5.0.0.10 <= v < 10.0.0.2
        df2 = r.u16()
        o["data_flags_u16"] = df2
        o["num_texture_sets"] = df2 & TEXTURE_SET_MASK
    else:
        # v >= 10.0.0.2: texture sets are DERIVED from the data flags read
        # above (L576) -- nothing more is consumed here (L654-664).
        o["num_texture_sets"] = (o.get("data_flags_u16", 0) &
                                 TEXTURE_SET_MASK)
    if ver < V_GEOMDATA_TEXPTR:
        raise NotSupportedByAdapter("NiGeometryData pre-4.1.0.0 texture pointer")
    n_sets = abs(o.get("num_texture_sets", 0))
    if n_sets > 0:
        o["texcoords_bbox"] = _bbox(r, n_verts * n_sets, 2)
    if ver >= V_GEOMDATA_TEXSETS_S16:
        o["dirty_flags_u16"] = r.u16()


def _bbox(r, count, comps):
    # bounded summary of an array of float tuples (no bulk vertex data in JSON)
    if count * comps * 4 > len(r.data) - r.pos:
        raise DecodeError("COUNT_BOUND: %d x %d floats exceed remaining "
                          "bytes" % (count, comps))
    lo = [float("inf")] * comps
    hi = [float("-inf")] * comps
    for _ in range(count):
        for c in range(comps):
            v = r.f32()
            if v < lo[c]:
                lo[c] = v
            if v > hi[c]:
                hi[c] = v
    return {"count": count, "components": comps,
            "min": [f(x) for x in lo], "max": [f(x) for x in hi]}


def load_nitribasedgeomdata(r, ver, o, links):
    # NiTriBasedGeomData::LoadBinary L59-64.
    load_nigeometrydata(r, ver, o, links)
    o["num_triangles"] = r.u16()


def load_nitrishapedata(r, ver, o, links):
    # NiTriShapeData::LoadBinary L220-293.
    load_nitribasedgeomdata(r, ver, o, links)
    tri_len = r.u32()
    o["tri_list_length"] = tri_len
    b_has_list = r.u8() if ver >= V_TRISHAPEDATA_HASLIST else 1
    o["has_tri_list"] = bool(b_has_list)
    if b_has_list and tri_len > 0:
        r.read(2 * tri_len)
        o["tri_list_present"] = True
    sna_size = r.u16()
    o["shared_normals_array_size"] = sna_size
    for _ in range(sna_size):
        cnt = r.u16()
        if cnt:
            r.read(2 * cnt)


def load_nidynamiceffect(r, ver, o, links):
    # NiDynamicEffect::LoadBinary L138-165.
    load_niavobject(r, ver, o, links)
    if ver >= V_EFFECT_ON:
        o["light_on_bool"] = bool(r.u8())
    if ver < V_EFFECT_AFFECTED_PTR:
        n = r.i32()
        r.read(4 * n)
        o["legacy_affected_nodes"] = n
    if ver >= V_EFFECT_UNAFFECTED:
        n = r.u32()
        links.append(("unaffected_nodes", [r.u32() for _ in range(n)]))


def load_nilight(r, ver, o, links):
    # NiLight::LoadBinary L75-84.
    load_nidynamiceffect(r, ver, o, links)
    o["dimmer"] = f(r.f32())
    o["ambient_color"] = [f(r.f32()), f(r.f32()), f(r.f32())]
    o["diffuse_color"] = [f(r.f32()), f(r.f32()), f(r.f32())]
    o["specular_color"] = [f(r.f32()), f(r.f32()), f(r.f32())]


def load_nidirectionallight(r, ver, o, links):
    # NiDirectionalLight::LoadBinary L67-70 (shell).
    load_nilight(r, ver, o, links)


def load_nipointlight(r, ver, o, links):
    # NiPointLight::LoadBinary L64-71.
    load_nilight(r, ver, o, links)
    o["attenuation0"] = f(r.f32())
    o["attenuation1"] = f(r.f32())
    o["attenuation2"] = f(r.f32())


def load_nitimecontroller(r, ver, o, links):
    # NiTimeController::LoadBinary L466-516.
    load_niobject(r, ver, o)
    links.append(("next_controller", [r.u32()]))
    flags = r.u16()
    if ver == V_TIMECTL_PLAYBACKWARDS_EXACT:
        o["play_backwards_bool"] = bool(r.u8())
    elif ver < V_TIMECTL_PLAYBACKWARDS_EXACT:
        flags = ((flags << 1) & ~0x001F) | (flags & 0x000F)
    o["time_controller_flags_u16"] = flags
    o["frequency"] = f(r.f32())
    o["phase"] = f(r.f32())
    o["lo_key_time"] = f(r.f32())
    o["hi_key_time"] = f(r.f32())
    links.append(("target", [r.u32()]))
    # v < 10.1.0.109: ManagerUpdate bit cleared (L508-514) -- post-processing,
    # byte consumption unaffected.


def load_niextraobjectdata(r, ver, o, links):
    # NiExtraData::LoadBinary L109-137.
    load_niobject(r, ver, o)
    if ver < V_EXTRADATA_OLD:
        links.append(("next_extra_data", [r.u32()]))
        size = r.u32()
        o["legacy_chunk_size"] = size
        # exact-kind chunk only when the concrete type IS NiExtraData itself;
        # all derived extra-data types do not consume it here.
    else:
        o["extra_data_name"] = r.cstring()


def load_nistringextradata(r, ver, o, links):
    # NiStringExtraData::LoadBinary L81-85.
    load_niextraobjectdata(r, ver, o, links)
    o["string_value"] = r.cstring()


# --------------------------------------------------------------------------
# E3 batch additions: particle + animation class families present in the T3
# RTTI table. All bodies proven from Gb12_Source (per-class file+line cited;
# SHA256 of each cited file recorded here once):
#   NiParticles.cpp (NiMain) CAB1A6B57DF9EDF44988A4D5E8BE617FAEE9728AC6BE05ABD81B6D864AE911A5
#   NiParticlesData.cpp (NiMain) 0AE90ADAB6BB951CD7ECD967766784559A397C5C20CD00994D3312A9927A1E3E
#   NiParticleSystem.cpp 7935E75AE1B1852B8A416AADCE42EEF1C40285DD653E297FC7F53753C5E9030C
#   NiPSysData.cpp 6D365086DA995852D27FF52B2829FE6D4B913F35C288020E551CDD6ABAC3F0E3
#   NiParticleInfo.cpp 3B7149EAA0D062AEA771058D7114DFAD50D01EBFD5D29503B89CAE3A82250031
#   NiPSysModifier.cpp 62EF9CFB45B3369F0B9075F081BEB9B907486C7938E508E8382192064875440B
#   NiPSysEmitter.cpp CD907049E7B601ADA35F89DF08E377D4365343F2A4610270B3CFF5BF31FD50C7
#   NiPSysVolumeEmitter.cpp EB9732E846E2A9FB5033245913E1A3D29BB30D8278E89EDB52B58930DAD7EC4A
#   NiPSysBoxEmitter.cpp 65B0715AA691DC98EFB4F211D2D61471DAD1DCAF8CD3C0D5C3AEAEECD0045E21
#   NiPSysAgeDeathModifier.cpp FE7A75EFF33A5E1D1E113E1F621D097504C0604AAF1166175D489ED84EC35A14
#   NiPSysSpawnModifier.cpp EEB85C4A8126928ABFFE3A1E1E92090448176F472E120F80B04DFD734C601167
#   NiPSysGrowFadeModifier.cpp 04875044A085D2B38094484C504F0D6233923AD1285616CBD395934A2BE53B99
#   NiPSysColorModifier.cpp 6069BC929FEFCB1C9FCBD02345315CA0D27B661ADAD5D776C38CDB384B1B0297
#   NiPSysPositionModifier.cpp 914F9713E14EC79F0B3F7FC176EB51CDD88F4A295EC191188F09001F427141F9
#   NiPSysBoundUpdateModifier.cpp 442BA1656003517C50F5A5C29BB82AC202ABC540D02CD75B315D0D1B8547397C
#   NiPSysModifierCtlr.cpp CB6AF650369BC2364B54D47F06AFDF08C690C9F36E7E311934CACD4D4E0330BA
#   NiPSysEmitterCtlr.cpp 3C8F5DE85005BF5BBBA5784D7EBB339BF5CD5F67AB99A95EC7C0E216036C23BE
#   NiPSysUpdateCtlr.cpp C51B8221A1C8F0B7E966E1CC22DBF91DCBFA55E91DC898721210AC994D9CE907
#   NiPSysEmitterCtlrData.cpp AF734EAD41FDF4ED134A415E1460426749EB5E77DEC2327920905D874F1394E4
#   NiInterpController.cpp A9AE2B3820C84F997DD8429476D94FB20B49040D0CFEDA552751638322719143
#   NiSingleInterpController.cpp 55F5225F1156883615E39640354B6A6A992EE216F42B78A56A6EF5C5CF9B88C6
#   NiFloatInterpController.cpp 70B60B00D7A6D9F856DB5D932379FFDE81D0879DD5E28539CCE75E71CF2B2CEC
#   NiPoint3InterpController.cpp 426B7F30F7542536399465EB382D6D3378EAE780E0AF3E8BE93D5955F3227ABA
#   NiTextureTransformController.cpp BA42798B8AECE9333E1D953D09135FB9BD3FD031206F1A98B3C07A547EECB5BE
#   NiMaterialColorController.cpp F9B086301F8961C1821C47D1D66FADE391A14D02E569613F0C61E7BF7AE1A230
#   NiFloatData.cpp AB78A37BFC9CD522567672B6F0957F77172DF0A8D2960893A29EBEB8C053AE20
#   NiColorData.cpp 52980858C605E164E825D3A942F6174BCB715FF0C2587AF3D4882DA2F293A97E
#   NiPosData.cpp B8BD1E122A370035FC1045AB4592191F1E74B6804BD3A193D5329057C2A33522
#   NiAnimationKey.cpp 9E967856B816DA75FE20FCEFA1A550B59BD4C11C0AA52820F1B77628DFA57B01
#   NiFloatKey.cpp 0ED75DDFBB970B2EF329EB178A31898E82A20D12739AAA0A55ADB3BB2A1BBBCD
#   NiColorKey.cpp FF388B5A1496C04972C4818ABC596372FD64704FFB48E7427DFAE4FB867C8E94
#   NiPosKey.cpp 7D117BC0B87E029070D59050D7A58FC123A41D9220FD4228C56C23A5B30E13FB
#   NiBoolKey.cpp F485FB1B08EFA52E7D4BE2FE838B1EA405000903DED9E8F9B8B940E4A5BCECFC
#   NiQuaternion.cpp E6C608239C0049C0C29F6C8641B9FA50CB7E8CC125BE92D96D313A968B0FF6A6
#   NiLinFloatKey.cpp D2B61A686454FCCAC0196DB66005F93949DF96781267ED56FE870646BDB0B87C
#   NiAnimationKeyMacros.h: NiImplementAnimationStream L55-70 registers the
#   per-(content, KeyType) CreateFromStream function; an UNREGISTERED combo
#   returns a NULL create function and the original code asserts
#   (assert(pfnCreateFunc)) -> load FAILS. Our reimplementation raises
#   NotSupportedByAdapter for the same combos (fail-closed, never skipped).
# --------------------------------------------------------------------------

def load_niparticles(r, ver, o, links):
    # NiParticles::LoadBinary L114-116: NiGeometry shell (empty body).
    load_nigeometry(r, ver, o, links)


def load_niparticlesystem(r, ver, o, links):
    # NiParticleSystem::LoadBinary L348-357: NiParticles + bWorldSpace NiBool
    # + m_kModifierList ReadMultipleLinkIDs.
    load_niparticles(r, ver, o, links)
    o["world_space_bool"] = bool(r.u8())
    n = r.u32_count(4)
    links.append(("modifier_list", [r.u32() for _ in range(n)]))


def load_niparticlesdata(r, ver, o, links):
    # NiParticlesData::LoadBinary L154-260: NiGeometryData + radii + usActive +
    # sizes + rotations (m_bIsOldRotatingParticlesObject is false for
    # factory-created stream objects -> the >= 5.0.0.8 branch applies).
    load_nigeometrydata(r, ver, o, links)
    if ver < V_PARTICLESDATA_LEGTRI:
        o["legacy_num_triangles_u16"] = r.u16()
    n_verts = o["num_vertices"]
    if ver < V_PARTICLESDATA_RADII_ARRAY:
        o["radii_uniform_f32"] = f(r.f32())
    else:
        b_radii = r.u8()
        o["has_radii"] = bool(b_radii)
        if b_radii and n_verts:
            o["radii_bbox"] = _bbox(r, n_verts, 1)
    o["num_active_particles_u16"] = r.u16()
    if ver < V_PARTICLESDATA_LEGTRI:
        raise NotSupportedByAdapter("NiParticlesData pre-4.1.0.7 sizes path")
    b_size = r.u8()
    o["has_sizes"] = bool(b_size)
    if b_size and n_verts:
        o["sizes_bbox"] = _bbox(r, n_verts, 1)
    if ver >= V_PARTICLESDATA_ROTATIONS:
        b_rot = r.u8()
        o["has_rotations"] = bool(b_rot)
        if b_rot and n_verts:
            # NiQuaternion::LoadBinary L240-247 (w, x, y, z) x n_verts.
            o["rotations_bbox_wxyz"] = _bbox(r, n_verts, 4)


def load_nipsysdata(r, ver, o, links):
    # NiPSysData::LoadBinary L159-171: NiParticlesData + per-vertex
    # NiParticleInfo (NiParticleInfo::LoadBinary L27-39: velocity 3f, rotation
    # axis 3f, age f, life span f, last update f, generation u16, code u16 --
    # 34 bytes each) + usNumAddedParticles u16 + usAddedParticlesBase u16.
    load_niparticlesdata(r, ver, o, links)
    n_verts = o["num_vertices"]
    if n_verts and n_verts * 40 > len(r.data) - r.pos:
        raise DecodeError("COUNT_BOUND: %d particle infos exceed remaining "
                          "bytes" % n_verts)
    if n_verts:
        lo = [float("inf")] * 9
        hi = [float("-inf")] * 9
        gen_min, gen_max = None, None
        code_min, code_max = None, None
        for _ in range(n_verts):
            for c in range(9):
                v = r.f32()
                if v < lo[c]:
                    lo[c] = v
                if v > hi[c]:
                    hi[c] = v
            gen = r.u16()
            code = r.u16()
            if gen_min is None or gen < gen_min:
                gen_min = gen
            if gen_max is None or gen > gen_max:
                gen_max = gen
            if code_min is None or code < code_min:
                code_min = code
            if code_max is None or code > code_max:
                code_max = code
        o["particle_info_summary"] = {
            "count": n_verts,
            "floats_min": [f(x) for x in lo],
            "floats_max": [f(x) for x in hi],
            "generation_min_u16": gen_min, "generation_max_u16": gen_max,
            "code_min_u16": code_min, "code_max_u16": code_max,
        }
    o["num_added_particles_u16"] = r.u16()
    o["added_particles_base_u16"] = r.u16()


def load_nipsysmodifier(r, ver, o, links):
    # NiPSysModifier::LoadBinary L86-96: NiObject + LoadCString(name) +
    # uiOrder u32 + ReadLinkID(target) + bActive NiBool.
    load_niobject(r, ver, o)
    o["modifier_name"] = r.cstring()
    o["order_u32"] = r.u32()
    links.append(("modifier_target", [r.u32()]))
    o["active_bool"] = bool(r.u8())


def load_nipsysemitter(r, ver, o, links):
    # NiPSysEmitter::LoadBinary L154-168: NiPSysModifier + 6f speed family +
    # initial color NiColor (3f) + 3f radius/life span.
    load_nipsysmodifier(r, ver, o, links)
    o["speed_f32"] = f(r.f32())
    o["speed_var_f32"] = f(r.f32())
    o["declination_f32"] = f(r.f32())
    o["declination_var_f32"] = f(r.f32())
    o["planar_angle_f32"] = f(r.f32())
    o["planar_angle_var_f32"] = f(r.f32())
    o["initial_color_rgb"] = [f(r.f32()), f(r.f32()), f(r.f32())]
    o["initial_radius_f32"] = f(r.f32())
    o["life_span_f32"] = f(r.f32())
    o["life_span_var_f32"] = f(r.f32())


def load_nipsysvolumeemitter(r, ver, o, links):
    # NiPSysVolumeEmitter::LoadBinary L102-107: NiPSysEmitter + ReadLinkID
    # (m_pkEmitterObj).
    load_nipsysemitter(r, ver, o, links)
    links.append(("emitter_object", [r.u32()]))


def load_nipsysboxemitter(r, ver, o, links):
    # NiPSysBoxEmitter::LoadBinary L95-102: NiPSysVolumeEmitter + 3f.
    load_nipsysvolumeemitter(r, ver, o, links)
    o["emitter_width_f32"] = f(r.f32())
    o["emitter_height_f32"] = f(r.f32())
    o["emitter_depth_f32"] = f(r.f32())


def load_nipsysagedeathmodifier(r, ver, o, links):
    # NiPSysAgeDeathModifier::LoadBinary L131-139: NiPSysModifier +
    # bSpawnOnDeath NiBool + ReadLinkID(m_pkSpawnModifier).
    load_nipsysmodifier(r, ver, o, links)
    o["spawn_on_death_bool"] = bool(r.u8())
    links.append(("spawn_modifier", [r.u32()]))


def load_nipspysspawnmodifier(r, ver, o, links):
    # NiPSysSpawnModifier::LoadBinary L245-257: NiPSysModifier + 2 u16 +
    # percentage f + 2 u16 + 4 f.
    load_nipsysmodifier(r, ver, o, links)
    o["num_spawn_generations_u16"] = r.u16()
    o["percentage_spawned_f32"] = f(r.f32())
    o["min_num_to_spawn_u16"] = r.u16()
    o["max_num_to_spawn_u16"] = r.u16()
    o["spawn_speed_chaos_f32"] = f(r.f32())
    o["spawn_dir_chaos_f32"] = f(r.f32())
    o["spawn_life_span_f32"] = f(r.f32())
    o["spawn_life_span_var_f32"] = f(r.f32())


def load_nipsysgrowfademodifier(r, ver, o, links):
    # NiPSysGrowFadeModifier::LoadBinary L100-109: NiPSysModifier +
    # fGrowTime f + usGrowGeneration u16 + fFadeTime f + usFadeGeneration u16.
    load_nipsysmodifier(r, ver, o, links)
    o["grow_time_f32"] = f(r.f32())
    o["grow_generation_u16"] = r.u16()
    o["fade_time_f32"] = f(r.f32())
    o["fade_generation_u16"] = r.u16()


def load_nipsyscolormodifier(r, ver, o, links):
    # NiPSysColorModifier::LoadBinary L119-124: NiPSysModifier + ReadLinkID
    # (m_spColorData).
    load_nipsysmodifier(r, ver, o, links)
    links.append(("color_data", [r.u32()]))


def load_nipsyspositionmodifier(r, ver, o, links):
    # NiPSysPositionModifier::LoadBinary L80-83: NiPSysModifier (empty body).
    load_nipsysmodifier(r, ver, o, links)


def load_nipsysboundupdatemodifier(r, ver, o, links):
    # NiPSysBoundUpdateModifier::LoadBinary L238-255: NiPSysModifier +
    # usUpdateSkip u16 iff v <= 10.1.0.100 else sUpdateSkip s16.
    load_nipsysmodifier(r, ver, o, links)
    if ver <= V_BNDUPD_SKIP_EXACT:
        o["update_skip_u16"] = r.u16()
    else:
        o["update_skip_i16"] = r.i16()


def load_niintercontroller(r, ver, o, links):
    # NiInterpController::LoadBinary L115-130: NiTimeController; nothing for
    # v < 10.1.0.104; bManagerControlled NiBool iff 10.1.0.104 <= v <
    # 10.1.0.109.
    load_nitimecontroller(r, ver, o, links)
    if ver < V_INTERP_NEW:
        return
    if ver < V_INTERP_MANAGER:
        o["manager_controlled_bool"] = bool(r.u8())


def load_nisingleinterpcontroller(r, ver, o, links):
    # NiSingleInterpController::LoadBinary L113-123: NiInterpController +
    # interpolator ReadLinkID iff v >= 10.1.0.104.
    load_niintercontroller(r, ver, o, links)
    if ver < V_INTERP_NEW:
        return
    links.append(("interpolator", [r.u32()]))


def load_nifloatinterpcontroller(r, ver, o, links):
    # NiFloatInterpController::LoadBinary L81-84: NiSingleInterpController shell.
    load_nisingleinterpcontroller(r, ver, o, links)


def load_nipoint3interpcontroller(r, ver, o, links):
    # NiPoint3InterpController::LoadBinary L81-88: NiSingleInterpController;
    # early return for v < 10.1.0.104 (nothing further).
    load_nisingleinterpcontroller(r, ver, o, links)


def load_nipsysmodifierctlr(r, ver, o, links):
    # NiPSysModifierCtlr::LoadBinary L121-126: NiSingleInterpController +
    # LoadCString(m_pcModifierName).
    load_nisingleinterpcontroller(r, ver, o, links)
    o["ctlr_modifier_name"] = r.cstring()


def load_nipsysemitterctlr(r, ver, o, links):
    # NiPSysEmitterCtlr::LoadBinary L830-841: NiPSysModifierCtlr; v <
    # 10.1.0.104 -> ReadLinkID (m_spData) + return; v >= 10.1.0.104 ->
    # ReadLinkID (m_spEmitterActiveInterpolator).
    load_nipsysmodifierctlr(r, ver, o, links)
    if ver < V_INTERP_NEW:
        links.append(("emitter_ctlr_data", [r.u32()]))
        return
    links.append(("emitter_active_interpolator", [r.u32()]))


def load_nipsysupdatectlr(r, ver, o, links):
    # NiPSysUpdateCtlr::LoadBinary L99-102: NiTimeController shell.
    load_nitimecontroller(r, ver, o, links)


def load_nitexturetransformcontroller(r, ver, o, links):
    # NiTextureTransformController::LoadBinary L300-316:
    # NiFloatInterpController + bShaderMap NiBool + uiMapIndex u32 + eMember
    # enum u32 + ReadLinkID (m_spFloatData) iff v < 10.1.0.104.
    load_nifloatinterpcontroller(r, ver, o, links)
    o["shader_map_bool"] = bool(r.u8())
    o["map_index_u32"] = r.u32()
    o["transform_member_u32"] = r.u32()
    if ver < V_INTERP_NEW:
        links.append(("float_data", [r.u32()]))


def load_nimaterialcolorcontroller(r, ver, o, links):
    # NiMaterialColorController::LoadBinary L166-192: NiPoint3InterpController
    # + m_uFlags u16 iff v >= 10.0.1.2 (else derived from the stashed
    # NiTimeController flags -- zero byte consumption) + ReadLinkID
    # (m_spPosData) iff v < 10.1.0.104.
    load_nipoint3interpcontroller(r, ver, o, links)
    if ver < V_MATERCOLOR_OWNFLAGS:
        o["material_color_flags_u16"] = \
            o.get("time_controller_flags_u16", 0) >> 2  # MAX_POS shift, L174-181
    else:
        o["material_color_flags_u16"] = r.u16()
    if ver < V_INTERP_NEW:
        links.append(("pos_data", [r.u32()]))


_FLOAT_KEY_COMBOS = {KEYTYPE_LIN: "lin", KEYTYPE_BEZ: "bez",
                     KEYTYPE_TCB: "tcb", KEYTYPE_STEP: "step"}
_COLOR_KEY_COMBOS = {KEYTYPE_LIN: "lin", KEYTYPE_STEP: "step"}
_POS_KEY_COMBOS = {KEYTYPE_LIN: "lin", KEYTYPE_BEZ: "bez",
                   KEYTYPE_TCB: "tcb", KEYTYPE_STEP: "step"}


def _load_float_keys(r, count, ttype):
    # NiFloatKey family: time + value f32 (NiFloatKey::LoadBinary L140-145);
    # bez adds in/out tan 2f (NiBezFloatKey.cpp L180-184); tcb adds
    # tension/continuity/bias 3f (NiTCBFloatKey.cpp L209-216); lin/step are
    # bare (NiLinFloatKey.cpp L132-135 / NiStepFloatKey.cpp L132-135).
    name = _FLOAT_KEY_COMBOS.get(ttype)
    if name is None:
        raise NotSupportedByAdapter(
            "float_key_type_%d_not_registered" % ttype)
    if count * 8 > len(r.data) - r.pos:
        raise DecodeError("COUNT_BOUND: %d float keys exceed remaining "
                          "bytes" % count)
    tmin, tmax = float("inf"), float("-inf")
    vmin, vmax = float("inf"), float("-inf")
    n_extra = 2 if name == "bez" else (3 if name == "tcb" else 0)
    xmin = [float("inf")] * n_extra
    xmax = [float("-inf")] * n_extra
    for _ in range(count):
        t = r.f32()
        v = r.f32()
        if t < tmin:
            tmin = t
        if t > tmax:
            tmax = t
        if v < vmin:
            vmin = v
        if v > vmax:
            vmax = v
        for c in range(n_extra):
            x = r.f32()
            if x < xmin[c]:
                xmin[c] = x
            if x > xmax[c]:
                xmax[c] = x
    out = {"count": count, "type_name": "float_" + name,
           "time_min_f32": f(tmin), "time_max_f32": f(tmax),
           "value_min_f32": f(vmin), "value_max_f32": f(vmax)}
    if n_extra:
        out["extras_min_f32"] = [f(x) for x in xmin]
        out["extras_max_f32"] = [f(x) for x in xmax]
    return out


def _load_vec3_keys(r, count, ttype, combos, kind):
    # NiColorKey family (NiColorKey::LoadBinary L129-134: time + NiColor 3f;
    # NiLinColorKey.cpp L115-118 / NiStepColorKey.cpp L116-119 bare) and
    # NiPosKey family (NiPosKey::LoadBinary L188-193: time + NiPoint3 3f;
    # NiBezPosKey.cpp L248-254 adds in/out tan 2x3f; NiTCBPosKey.cpp
    # L273-280 adds tension/continuity/bias 3f; NiLinPosKey.cpp L140-143 /
    # NiStepPosKey.cpp L140-143 bare).
    name = combos.get(ttype)
    if name is None:
        raise NotSupportedByAdapter(
            "%s_key_type_%d_not_registered" % (kind, ttype))
    if count * 16 > len(r.data) - r.pos:
        raise DecodeError("COUNT_BOUND: %d vec3 keys exceed remaining "
                          "bytes" % count)
    n_extra = (2 if name == "bez" else (3 if name == "tcb" else 0))
    tmin, tmax = float("inf"), float("-inf")
    vmin = [float("inf")] * 3
    vmax = [float("-inf")] * 3
    xmin = [float("inf")] * (n_extra * 3)
    xmax = [float("-inf")] * (n_extra * 3)
    for _ in range(count):
        t = r.f32()
        if t < tmin:
            tmin = t
        if t > tmax:
            tmax = t
        for c in range(3):
            v = r.f32()
            if v < vmin[c]:
                vmin[c] = v
            if v > vmax[c]:
                vmax[c] = v
        for c in range(n_extra * 3):
            x = r.f32()
            if x < xmin[c]:
                xmin[c] = x
            if x > xmax[c]:
                xmax[c] = x
    out = {"count": count, "type_name": "%s_%s" % (kind, name),
           "time_min_f32": f(tmin), "time_max_f32": f(tmax),
           "value_min": [f(x) for x in vmin],
           "value_max": [f(x) for x in vmax]}
    if n_extra:
        out["extras_min_f32"] = [f(x) for x in xmin]
        out["extras_max_f32"] = [f(x) for x in xmax]
    return out


def _load_bool_keys(r, count):
    # NiBoolKey::LoadBinary L143-151: time f32 + NiBool u8; only the STEPKEY
    # create function is registered for BOOL content (NiStepBoolKey via
    # NiImplementAnimationStream).
    if count * 5 > len(r.data) - r.pos:
        raise DecodeError("COUNT_BOUND: %d bool keys exceed remaining "
                          "bytes" % count)
    tmin, tmax = float("inf"), float("-inf")
    n_true = 0
    for _ in range(count):
        t = r.f32()
        if t < tmin:
            tmin = t
        if t > tmax:
            tmax = t
        if r.u8():
            n_true += 1
    return {"count": count, "type_name": "bool_step",
            "time_min_f32": f(tmin), "time_max_f32": f(tmax),
            "num_true": n_true}


def load_nifloatdata(r, ver, o, links):
    # NiFloatData::LoadBinary L106-132: NiObject + uiNumKeys u32 + (iff > 0)
    # KeyType enum u32 + keys via the per-type create function.
    load_niobject(r, ver, o)
    n = r.u32_count(4)
    o["num_keys"] = n
    if n > 0:
        ttype = r.u32()
        o["key_type_u32"] = ttype
        o["keys"] = _load_float_keys(r, n, ttype)


def load_nicolordata(r, ver, o, links):
    # NiColorData::LoadBinary L106-128: NiObject + uiNumKeys u32 + (iff > 0)
    # KeyType enum u32 + color keys.
    load_niobject(r, ver, o)
    n = r.u32_count(4)
    o["num_keys"] = n
    if n > 0:
        ttype = r.u32()
        o["key_type_u32"] = ttype
        o["keys"] = _load_vec3_keys(r, n, ttype, _COLOR_KEY_COMBOS, "color")


def load_niposdata(r, ver, o, links):
    # NiPosData::LoadBinary L105-131: NiObject + uiNumKeys u32 + (iff > 0)
    # KeyType enum u32 + position keys.
    load_niobject(r, ver, o)
    n = r.u32_count(4)
    o["num_keys"] = n
    if n > 0:
        ttype = r.u32()
        o["key_type_u32"] = ttype
        o["keys"] = _load_vec3_keys(r, n, ttype, _POS_KEY_COMBOS, "pos")


def load_nipsysemitterctlrdata(r, ver, o, links):
    # NiPSysEmitterCtlrData::LoadBinary L79-129: NiObject + birth-rate keys
    # (u32 count; iff > 0: KeyType enum u32 + NiFloatKey family) + emitter-
    # active keys (u32 count; iff > 0: KeyType enum u32 iff v >= 10.1.0.104 --
    # else hardcoded STEPKEY -- + NiBoolKey family).
    load_niobject(r, ver, o)
    n = r.u32_count(4)
    o["num_birth_rate_keys"] = n
    if n > 0:
        ttype = r.u32()
        o["birth_rate_key_type_u32"] = ttype
        o["birth_rate_keys"] = _load_float_keys(r, n, ttype)
    n2 = r.u32_count(4)
    o["num_emitter_active_keys"] = n2
    if n2 > 0:
        if ver >= V_INTERP_NEW:
            ttype2 = r.u32()
            o["emitter_active_key_type_u32"] = ttype2
            if ttype2 != KEYTYPE_STEP:
                raise NotSupportedByAdapter(
                    "bool_key_type_%d_not_registered" % ttype2)
        o["emitter_active_keys"] = _load_bool_keys(r, n2)


LOADERS = {
    "NiNode": load_ninode,
    "NiMaterialProperty": load_nimaterialproperty,
    "NiZBufferProperty": load_nizbufferproperty,
    "NiAlphaProperty": load_nialphaproperty,
    "NiVertexColorProperty": load_nivertexcolorproperty,
    "NiTexturingProperty": load_nitexturingproperty,
    "NiSourceTexture": load_nisourcetexture,
    "NiTexture": load_nitexture,
    "NiTriShape": load_nitrishape,
    "NiTriBasedGeom": load_nitribasedgeom,
    "NiGeometry": load_nigeometry,
    "NiTriShapeData": load_nitrishapedata,
    "NiTriBasedGeomData": load_nitribasedgeomdata,
    "NiGeometryData": load_nigeometrydata,
    "NiLight": load_nilight,
    "NiDirectionalLight": load_nidirectionallight,
    "NiPointLight": load_nipointlight,
    "NiTimeController": load_nitimecontroller,
    "NiExtraData": load_niextraobjectdata,
    "NiStringExtraData": load_nistringextradata,
    # E3 additions (particle + animation families; abstract bases are NOT
    # registered as factory types -- only concrete block types are listed)
    "NiParticles": load_niparticles,
    "NiParticlesData": load_niparticlesdata,
    "NiParticleSystem": load_niparticlesystem,
    "NiPSysData": load_nipsysdata,
    "NiPSysAgeDeathModifier": load_nipsysagedeathmodifier,
    "NiPSysBoxEmitter": load_nipsysboxemitter,
    "NiPSysSpawnModifier": load_nipspysspawnmodifier,
    "NiPSysGrowFadeModifier": load_nipsysgrowfademodifier,
    "NiPSysColorModifier": load_nipsyscolormodifier,
    "NiPSysPositionModifier": load_nipsyspositionmodifier,
    "NiPSysBoundUpdateModifier": load_nipsysboundupdatemodifier,
    "NiPSysEmitterCtlr": load_nipsysemitterctlr,
    "NiPSysUpdateCtlr": load_nipsysupdatectlr,
    "NiPSysEmitterCtlrData": load_nipsysemitterctlrdata,
    "NiTextureTransformController": load_nitexturetransformcontroller,
    "NiMaterialColorController": load_nimaterialcolorcontroller,
    "NiFloatData": load_nifloatdata,
    "NiColorData": load_nicolordata,
    "NiPosData": load_niposdata,
}

# Every type in the registry but NOT in LOADERS is REGISTERED_BUT_NOT_
# DECODED (fail-closed, recorded per block; never silently skipped).
# Types absent from the registry entirely are UNREGISTERED (RTTIError in the
# original GB 1.2 semantics).

MAX_SEARCH_ATTEMPTS = 250000
MAX_RUN_SKIP = 65536
# E3 pre-solver budget (footer-anchored suffix scans are byte-position walks
# over the file; each attempt is an O(few reads) decode attempt)
PRESOLVE_MAX_ATTEMPTS = 12000000


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def decode(data, path="<memory>", full_decode=False,
           registered_classes=None):
    """Run the GB 1.2 load semantics over `data`.

    Returns the oracle result dict (s8 minimum + extensions). Deterministic:
    no wall-clock data enters the output.
    """
    from adapters.gb12.registry import GB12_REGISTERED_CLASSES
    if registered_classes is None:
        registered_classes = GB12_REGISTERED_CLASSES

    res = {
        "schema": "gamebryo_oracle/oracle_result@1.0",
        "adapter": "gb12",
        "ORACLE_MODE": ORACLE_MODE,
        "era_category": ERA_CATEGORY,
        "decode_continued_after_rtti_gate": False,
        "input_identity": {},
        "oracle": {
            "gamebryo_version": "GB_1_2 (Gamebryo 1.2.2, NIF write version 10.2.0.0)",
            "loader_identity": "NiStream::Load -> LoadHeader -> LoadRTTI -> LoadBinary loop -> link -> postlink (GB 1.2.2 CoreLibs NiMain)",
            "loader_source_identity": {
                "file": "D:\\gamebyroengine\\extracted\\Gb12_Source\\CoreLibs\\NiMain\\NiStream.cpp",
                "sha256": "E955C36EBBB442029E00BE8A154726741B8454A607F2DC043F1FD542B009DC25",
                "semantics_provenance": "see gb12core.py header citation block",
            },
            "tool_version": "%s/%s gb12 source-derived reimplementation" % (TOOL_NAME, TOOL_VERSION),
        },
        "version_gate": {"min": u32_to_ver(V_MIN), "max": u32_to_ver(V_MAX)},
        "load_result": {"accepted": False, "partial": False, "error": None,
                        "error_code": None},
        "objects": [],
        "scene_graph": {"roots": [], "edges": []},
        "type_histogram": {},
        "controllers": [],
        "properties": [],
        "textures": [],
        "bounds": [],
        "warnings": [],
        "unknowns": [],
    }
    res["input_identity"] = {
        "path": path,
        "size": len(data),
        "sha256": hashlib.sha256(data).hexdigest().upper(),
    }

    r = Reader(data)
    try:
        header_line = r.line()
    except DecodeError as e:
        res["load_result"].update(accepted=False, error="NOT_NIF_FILE",
                                  error_code="NOT_NIF_FILE")
        res["warnings"].append("header line unreadable: %s" % e)
        return res
    res["input_identity"]["header"] = header_line
    if "File Format" not in header_line:
        # NiStream.cpp L311-316
        res["load_result"].update(
            accepted=False, error="NOT_NIF_FILE: 'File Format' absent",
            error_code="NOT_NIF_FILE")
        return res
    ver = r.u32()
    res["input_identity"]["nif_version"] = u32_to_ver(ver)
    res["input_identity"]["nif_version_u32"] = ver
    # LoadHeader gate L320-332
    if ver < V_MIN:
        res["load_result"].update(
            accepted=False,
            error="OLDER_VERSION: NIF version is too old.",
            error_code="OLDER_VERSION")
        return res
    if ver > V_MAX:
        res["load_result"].update(
            accepted=False,
            error="LATER_VERSION: Unknown NIF version.",
            error_code="LATER_VERSION")
        return res
    res["version_gate"]["verdict"] = "ACCEPTED"
    if ver >= V_USER_GATE:
        res["input_identity"]["user_defined_version"] = u32_to_ver(r.u32())
    n_obj = r.u32()
    res["input_identity"]["num_blocks_from_header"] = n_obj
    # decode_rest() recurses once per block; T3-scale files (1288 blocks)
    # exceed CPython's default recursion limit. Raise the limit to the
    # block count + headroom (deterministic; no output impact).
    _sys.setrecursionlimit(max(_sys.getrecursionlimit(), n_obj + 256))

    b_new = ver >= V_BNEW
    type_names = None
    type_idx = None
    if b_new:
        # LoadRTTI L412-449 -- SOURCE TABLE ORDER (F1 fix 2026-10-03).
        # The ORIGINAL algorithm (NiStream.cpp L421-433) reads the RTTI table
        # ONE ENTRY AT A TIME: LoadRTTIString -> ms_pkLoaders->GetAt factory
        # check -> NEXT entry. The FIRST unregistered name aborts LoadRTTI
        # with RTTIError -> Load() returns false BEFORE any later table name,
        # ANY object type index (L436-444), the object groups (L470-487) or
        # any body byte is read. EVERY table entry is validated, INCLUDING
        # entries that no object references; the scan order is TABLE order,
        # never object-reference order. The pre-F1 build validated by
        # iterating object type indices instead (Desktop post-audit finding
        # F1): unused unregistered entries were silently skipped and the
        # first miss was reported in object order.
        n_types = r.u16()
        type_names = []
        first_miss_table_index = None
        first_miss_name = None
        for i in range(n_types):
            try:
                name = r.rtti_string()
            except DecodeError as e:
                if first_miss_table_index is not None:
                    # full-decode extension only: the ORIGINAL loader never
                    # reaches this read (it failed at the first miss).
                    res["warnings"].append(
                        "EXTENDED_TABLE_READ_FAILED (OUR extension; the "
                        "ORIGINAL GB 1.2 load already failed at the RTTI "
                        "factory miss): %s" % e)
                    break
                raise  # no table miss yet: unchanged pre-F1 behavior
            type_names.append(name)
            if name not in registered_classes and first_miss_name is None:
                # FIRST miss in TABLE order (NiStream.cpp L427-433); in
                # --full-decode the scan continues for inspection but the
                # first miss is never overwritten by a later entry.
                first_miss_table_index = i
                first_miss_name = name
                if not full_decode:
                    # ORIGINAL: stop reading further names at the miss.
                    break
                # --full-decode (OUR extension): keep reading the table
                # for inspection; the source-predicted verdict is fixed.
        full_table_read = len(type_names) == n_types
        unregistered_table = [nm for nm in type_names
                              if nm not in registered_classes]
        res["rtti_table_validation"] = {
            "scan_order": "SOURCE_TABLE_ORDER (NiStream.cpp LoadRTTI "
                          "L421-433: name -> factory lookup -> next name)",
            "file_type_count": n_types,
            "registered_class_count": len(registered_classes),
            "names_read": len(type_names),
            "full_table_read": full_table_read,
            "first_miss_table_index": first_miss_table_index,
            "first_rtti_miss": first_miss_name,
            "unregistered_table_entries": unregistered_table,
            "source_predicted_verdict": ("REJECTED" if first_miss_name
                                         is not None else "ACCEPTED"),
            "unused_entry_note": "table entries not referenced by any "
                                 "object are still validated in table "
                                 "order (F1 fix; NiStream.cpp L421-433 "
                                 "precedes the L436-444 index loop)",
            "registry_provenance": "Gb12_Source CoreLibs *SDM.cpp "
                                   "NiRegisterStream/RegisterLoader census "
                                   "(see adapters/gb12/registry.py)",
        }
        if first_miss_name is not None and full_decode:
            res["rtti_table_validation"]["extension_observation"] = (
                "table scan continued past the first miss ONLY under "
                "--full-decode (OUR extension; the ORIGINAL GB 1.2 loader "
                "stops at the first miss); SOURCE_PREDICTED_VERDICT="
                "REJECTED, FIRST_RTTI_MISS=%s (table index %d)"
                % (first_miss_name, first_miss_table_index))
        # back-compat compact view of the same TABLE scan (the pre-F1 key
        # name is kept for downstream/compare stability; content is the
        # table-order validation, NOT object references)
        res["rtti_gate"] = {
            "registered_class_count": len(registered_classes),
            "file_type_count": n_types,
            "unregistered_types": unregistered_table,
            "first_unregistered_scan_order": first_miss_name,
            "scan_basis": "RTTI TABLE order (LoadRTTI L421-433); the "
                          "pre-F1 build scanned object reference order",
            "registry_provenance": "Gb12_Source CoreLibs *SDM.cpp "
                                   "NiRegisterStream/RegisterLoader census "
                                   "(see adapters/gb12/registry.py)",
            "deprecated_alias_of": "rtti_table_validation",
        }
        if first_miss_name is not None:
            # ORIGINAL fail-closed verdict: LoadRTTI -> RTTIError -> false.
            # In ordinary mode NOTHING past the miss was read: later table
            # names, object indices, groups and bodies are NOT reported.
            res["load_result"].update(
                accepted=False, partial=False,
                error="RTTIError(%s): cannot find create function."
                      % first_miss_name,
                error_code="RTTIError")
            res["unknowns"] = [
                {"class": first_miss_name,
                 "status": "UNREGISTERED_IN_GB12_FACTORY"}]
            if not full_decode:
                return res
            # OUR extension: continue the decode (never original behavior)
            res["decode_continued_after_rtti_gate"] = True
            res["load_result"]["partial"] = True
            res["warnings"].append(
                "decode_continued_after_rtti_gate=true is OUR extension; the "
                "ORIGINAL GB 1.2 Load() returns false at LoadRTTI (verdict "
                "reported in load_result); SOURCE_PREDICTED_VERDICT=REJECTED "
                "FIRST_RTTI_MISS=%s (table index %d)"
                % (first_miss_name, first_miss_table_index))
        # per-object type indices (LoadRTTI L436-444) -- read ONLY after the
        # whole table validated (ordinary) or under the labeled extension
        # (full-decode); these are OBJECT references, a separate artifact
        # from the RTTI_TABLE_VALIDATION scan above.
        type_idx = []
        index_stage_failed = None
        try:
            for _ in range(n_obj):
                # NiStream.cpp L441: assert(usRTTI < usRTTICount) -- a
                # corrupted index must be DETECTED, never trusted.
                ix = r.u16()
                if ix >= n_types:
                    index_stage_failed = (
                        "INVALID_TYPE_INDEX: block type index %d out "
                        "of range (num types %d)" % (ix, n_types))
                    break
                type_idx.append(ix)
        except DecodeError:
            index_stage_failed = "NOT_NIF_FILE: truncated RTTI table"
        if index_stage_failed is not None:
            if full_decode and first_miss_name is not None:
                # extension-only failure: the ORIGINAL verdict is the
                # factory miss (the original never reads these indices);
                # the extension halts honestly without masking it.
                res["warnings"].append(
                    "EXTENDED_INSPECTION_HALTED at the object-index stage "
                    "(OUR extension): %s -- the ORIGINAL GB 1.2 load "
                    "already failed at the RTTI factory miss; no body "
                    "inspection is possible without a complete type-index "
                    "list" % index_stage_failed)
                res["rtti_table_validation"]["extension_observation"] = (
                    "extended inspection halted at the object-index stage: "
                    "%s (the ORIGINAL loader never reads these indices)"
                    % index_stage_failed)
                res["objects"] = []
                return res
            res["load_result"].update(
                accepted=False, partial=False,
                error=index_stage_failed,
                error_code=("INVALID_TYPE_INDEX"
                            if index_stage_failed.startswith("INVALID_TYPE_")
                            else "NOT_NIF_FILE"))
            return res
        # OBJECT_REFERENCE_HISTOGRAM / OBJECT_REFERENCE_CENSUS (LoadRTTI
        # L436-444 artifacts; separate from RTTI_TABLE_VALIDATION).
        res["type_histogram"] = {}
        for ix in type_idx:
            tn = type_names[ix]
            res["type_histogram"][tn] = res["type_histogram"].get(tn, 0) + 1
        res["object_reference_histogram"] = dict(res["type_histogram"])
        referenced = set(type_idx)
        res["object_reference_census"] = {
            "header_num_blocks": n_obj,
            "type_indices_read": len(type_idx),
            "referenced_table_indices": sorted(referenced),
            "unreferenced_table_indices": [i for i in range(n_types)
                                           if i not in referenced],
            "semantics": "OBJECT references into the RTTI table (LoadRTTI "
                         "L436-444); NOT the table-order factory validation "
                         "(L421-433) -- unused entries are validated by the "
                         "table scan, not by this census",
        }
        # LoadObjectGroups L470-487 (iff ver >= 5.0.0.6)
        if ver >= V_GROUPS:
            n_groups = r.u32()
            res["object_groups"] = {"num_groups": n_groups}
            for _ in range(n_groups):
                r.u32()
    else:
        # LEGACY (< 5.0.0.1): RTTI string inline per object (LoadObject L451-468)
        res["rtti_gate"] = {
            "registered_class_count": len(registered_classes),
            "file_type_count": None,
            "unregistered_types": [],
            "registry_provenance": "Gb12_Source CoreLibs *SDM.cpp census (legacy inline-RTTI layout)",
        }

    # ---------------- LoadBinary loop (+ our closure extension) -----------
    objects = [None] * n_obj
    search_attempts = [0]
    footer_holder = [None]

    def footer_at(pos):
        """Valid TopObjects footer starting exactly at pos? Returns count."""
        if pos + 4 > len(data):
            return None
        (c,) = struct.unpack("<I", data[pos:pos + 4])
        if 0 <= c <= n_obj and pos + 4 + 4 * c == len(data):
            return c
        return None

    def decode_block_at(pos, i):
        """Decode block i at pos; returns (new_pos, obj, links) or raises."""
        rr = Reader(data, pos)
        o = {"index": i}
        links = []
        if b_new:
            tname = type_names[type_idx[i]]
        else:
            tname = rr.rtti_string()
        o["type"] = tname
        if tname not in registered_classes:
            raise NotSupportedByAdapter("unregistered:%s" % tname)
        loader = LOADERS.get(tname)
        if loader is None:
            raise NotSupportedByAdapter("registered_but_not_decoded:%s" % tname)
        loader(rr, ver, o, links)
        o["byte_start"] = pos
        o["byte_end"] = rr.pos
        o["byte_size"] = rr.pos - pos
        return rr.pos, o, links

    def block_kind(i):
        """'known' | 'unknown' (legacy inline types resolved at decode)."""
        if not b_new:
            return "legacy"
        tname = type_names[type_idx[i]]
        if tname not in registered_classes:
            return "unknown"
        if tname not in LOADERS:
            return "unknown"
        return "known"

    def record_run(i, j, p0, p1):
        """Record the [i..j) unknown-block run (b_new only: membership from
        the RTTI table; individual splits inside the run stay
        UNDETERMINED_INDIVIDUAL)."""
        for k in range(i, j):
            tname = type_names[type_idx[k]]
            status = ("UNREGISTERED_IN_GB12_FACTORY"
                      if tname not in registered_classes
                      else "REGISTERED_BUT_NOT_DECODED_BY_ADAPTER")
            objects[k] = {
                "index": k, "type": tname, "status": status,
                "byte_start": p0, "byte_end": p1,
                "boundary_method": "closure_search_extension (OUR extension; "
                                   "individual split inside the unknown run "
                                   "is UNDETERMINED_INDIVIDUAL)",
            }

    def record_unknown_block(i, tname, p0, p1):
        """Record ONE boundary-only block (legacy: name + boundary both
        derived from the bytes; b_new never uses this)."""
        status = ("UNREGISTERED_IN_GB12_FACTORY"
                  if tname not in registered_classes
                  else "REGISTERED_BUT_NOT_DECODED_BY_ADAPTER")
        objects[i] = {
            "index": i, "type": tname, "status": status,
            "byte_start": p0, "byte_end": p1,
            "boundary_method": "closure_search_extension (OUR extension)",
        }

    def legacy_walk(pos, i):
        """LEGACY (< 5.0.0.1) sequential LoadObject walk: every block starts
        with an INLINE RTTI string that NAMES the block's class unambiguously
        (NiStream::LoadObject L451-468). A registered+implemented class must
        decode exactly here (no alternative interpretation); an unregistered
        or adapter-unimplemented class is a boundary-only block whose body
        ends where the next block's inline RTTI string starts (scanned in
        ascending order; validated by full-file closure)."""
        if i >= n_obj:
            c = footer_at(pos)
            if c is not None:
                footer_holder[0] = (pos, c)
                return pos
            return None
        search_attempts[0] += 1
        if search_attempts[0] > MAX_SEARCH_ATTEMPTS:
            raise DecodeError("closure search budget exhausted")
        try:
            rr = Reader(data, pos)
            tname = rr.rtti_string()
        except DecodeError:
            return None
        if not (4 <= len(tname) <= 64 and tname.startswith("Ni")):
            return None  # not a block start -> invalid interpretation
        if tname in registered_classes and tname in LOADERS:
            # unambiguous: the block at pos IS this class; decode or fail
            try:
                rr2 = Reader(data, pos)
                o = {"index": i, "type": tname}
                links = []
                rr2.rtti_string()
                LOADERS[tname](rr2, ver, o, links)
            except (DecodeError, NotSupportedByAdapter):
                return None
            o["byte_start"] = pos
            o["byte_end"] = rr2.pos
            o["byte_size"] = rr2.pos - pos
            objects[i] = o
            links_all[i] = links
            rpos = legacy_walk(rr2.pos, i + 1)
            if rpos is not None:
                return rpos
            objects[i] = None
            links_all[i] = None
            return None
        # unknown block (unregistered or not implemented): its body boundary
        # is the start of block i+1 -- found by scanning for the next inline
        # RTTI string (any class name; decodable classes end the run,
        # unknown names chain the run deterministically).
        limit = min(len(data) - 4, pos + MAX_RUN_SKIP)
        for q in range(pos + 4 + len(tname), limit):
            search_attempts[0] += 1
            if search_attempts[0] > MAX_SEARCH_ATTEMPTS:
                raise DecodeError("closure search budget exhausted")
            try:
                rrq = Reader(data, q)
                tn2 = rrq.rtti_string()
            except DecodeError:
                continue
            if not (4 <= len(tn2) <= 64 and tn2.startswith("Ni")):
                continue
            record_unknown_block(i, tname, pos, q)
            rpos = legacy_walk(q, i + 1)
            if rpos is not None:
                return rpos
            objects[i] = None
        return None

    def decode_rest(pos, i):
        """Decode blocks i..n-1 from pos; backtracking over unknown runs.
        Returns footer position on success, None on failure."""
        if not b_new:
            return legacy_walk(pos, i)
        if i >= n_obj:
            c = footer_at(pos)
            if c is not None:
                footer_holder[0] = (pos, c)
                return pos
            return None
        search_attempts[0] += 1
        if search_attempts[0] > MAX_SEARCH_ATTEMPTS:
            raise DecodeError("closure search budget exhausted")
        if block_kind(i) == "known":
            try:
                pos2, o, links = decode_block_at(pos, i)
            except (DecodeError, NotSupportedByAdapter):
                return None
            objects[i] = o
            links_all[i] = links
            rpos = decode_rest(pos2, i + 1)
            if rpos is not None:
                return rpos
            objects[i] = None
            links_all[i] = None
            return None
        # unknown block (b_new): the type table pins the run exactly
        run_end = i
        while run_end < n_obj and block_kind(run_end) != "known":
            run_end += 1
        # candidate boundaries: (a) footer start, (b) next-known decodes
        # Link-validity prefilter (E3): a REAL block's link IDs are always
        # NULL_LINKID or valid block indices; a garbage-position decode
        # almost always carries out-of-range IDs -> reject it O(1) instead
        # of recursing a full subtree. Applied ONLY in this boundary scan
        # (OUR extension); the sequential known-block walk never filters
        # (out-of-range links there are honest LINK_FAILURE warnings).
        candidates = []
        limit = min(len(data), pos + MAX_RUN_SKIP)
        for p in range(pos, limit):
            search_attempts[0] += 1
            if search_attempts[0] > MAX_SEARCH_ATTEMPTS:
                raise DecodeError("closure search budget exhausted")
            if run_end >= n_obj:
                if footer_at(p) is not None:
                    candidates.append(p)
            else:
                try:
                    _, _, lc = decode_block_at(p, run_end)
                except (DecodeError, NotSupportedByAdapter):
                    continue
                bad = False
                for _, lids in lc:
                    for lid in lids:
                        if lid != NULL_LINKID and lid >= n_obj:
                            bad = True
                            break
                    if bad:
                        break
                if bad:
                    continue
                candidates.append(p)
        for p in candidates:
            if p == pos:
                # a run of >= 1 block cannot occupy ZERO bytes (each block
                # consumes at least its GroupID u32); invalid -> skip
                continue
            min_span = 4 * (run_end - i)
            if p - pos < min_span:
                continue
            if run_end >= n_obj:
                record_run(i, run_end, pos, p)
                footer_holder[0] = (p, footer_at(p))
                return p
            try:
                pos3, o, links = decode_block_at(p, run_end)
            except (DecodeError, NotSupportedByAdapter):
                continue
            objects[run_end] = o
            links_all[run_end] = links
            rpos = decode_rest(pos3, run_end + 1)
            if rpos is not None:
                record_run(i, run_end, pos, p)
                return rpos
            objects[run_end] = None
            links_all[run_end] = None
        return None

    def presolve_runs():
        """E3 right-to-left footer-anchored solver for b_new files with
        unknown runs. ACCEPTANCE SEMANTICS IDENTICAL to decode_rest (the
        first closing assignment in the same lexicographic order; the same
        decode_block_at + link-plausibility + min_span rules; full closure
        to the footer required) -- only the SEARCH ORDER differs: the LAST
        run's candidates are footer-anchored (suffix walk closes to EOF),
        which kills the garbage-candidate explosion of the pure DFS (a
        permissive next-known class, e.g. a zero-count NiNode, admits
        thousands of vacuous candidates whose subtrees exhaust
        MAX_SEARCH_ATTEMPTS before the true boundary is reached).
        Returns the footer position and fills objects/links_all, or None
        (caller clears state and falls back to decode_rest)."""
        runs = []
        k = 0
        while k < n_obj:
            if block_kind(k) == "known":
                k += 1
                continue
            e = k
            while e < n_obj and block_kind(e) != "known":
                e += 1
            runs.append((k, e))
            k = e
        if not runs or len(runs) > 16:
            return None  # no runs (cheap DFS walk) / too many for pre-solve

        def plausible_links(links):
            for _, lids in links:
                for lid in lids:
                    if lid != NULL_LINKID and lid >= n_obj:
                        return False
            return True

        attempts = [0]

        # ---- suffix sets, right-to-left ----
        # S[last] = boundaries whose decode + known-suffix walk close to the
        # footer exactly; S[k] = boundaries whose decode + known-walk to the
        # next run's start admit a next-run boundary >= the walk arrival.
        S = {}
        last_a, last_e = runs[-1]
        S_last = []
        for p in range(pos_start, len(data)):
            attempts[0] += 1
            if attempts[0] > PRESOLVE_MAX_ATTEMPTS:
                return None
            if last_e >= n_obj:
                # run extends to EOF: candidates are footer starts (span is
                # checked against the arrival position at assembly time)
                if footer_at(p) is not None:
                    S_last.append(p)
                continue
            try:
                pe, _, lc = decode_block_at(p, last_e)
            except (DecodeError, NotSupportedByAdapter):
                continue
            if not plausible_links(lc):
                continue
            # screening walk (link-plausibility REJECTS garbage fast; the
            # final assembly walk is UNFILTERED and re-verifies closure)
            q, ok = pe, True
            bi = last_e + 1
            while ok and bi < n_obj:
                attempts[0] += 1
                if attempts[0] > PRESOLVE_MAX_ATTEMPTS:
                    return None
                try:
                    q, _, lc2 = decode_block_at(q, bi)
                except (DecodeError, NotSupportedByAdapter):
                    ok = False
                    break
                if not plausible_links(lc2):
                    ok = False
                    break
                bi += 1
            if ok and footer_at(q) is not None:
                S_last.append(p)
                # lexicographic-first: the DFS accepts the SMALLEST closing
                # suffix boundary; the scan stops at the first closer. (A
                # later closer would only matter if no chain closes through
                # this one -- in that case the DFS fallback runs.)
                break
        if not S_last:
            return None
        S[len(runs) - 1] = S_last
        for ki in range(len(runs) - 2, -1, -1):
            a, e = runs[ki]
            hi = min(S[ki + 1])
            cand = []
            for p in range(pos_start, hi):
                attempts[0] += 1
                if attempts[0] > PRESOLVE_MAX_ATTEMPTS:
                    return None
                try:
                    pe, _, lc = decode_block_at(p, e)
                except (DecodeError, NotSupportedByAdapter):
                    continue
                if not plausible_links(lc):
                    continue
                q, ok = pe, True
                bi = e + 1
                nxt_a = runs[ki + 1][0]
                while ok and bi < nxt_a:
                    attempts[0] += 1
                    if attempts[0] > PRESOLVE_MAX_ATTEMPTS:
                        return None
                    try:
                        q, _, lc2 = decode_block_at(q, bi)
                    except (DecodeError, NotSupportedByAdapter):
                        ok = False
                        break
                    if not plausible_links(lc2):
                        ok = False
                        break
                    bi += 1
                if ok and any(b >= q + 4 * (runs[ki + 1][1] - nxt_a)
                              for b in S[ki + 1]):
                    cand.append(p)
            if not cand:
                return None
            S[ki] = cand

        # ---- lexicographic-first assembly (same order as decode_rest) ----
        def assemble(ki, pos, bi):
            a, e = runs[ki]
            q, ok = pos, True
            while ok and bi < a:
                try:
                    q, o, lc = decode_block_at(q, bi)
                except (DecodeError, NotSupportedByAdapter):
                    return False
                objects[bi] = o
                links_all[bi] = lc
                bi += 1
            if not ok:
                return None
            for b in S[ki]:
                if b < q + 4 * (e - a):
                    continue  # run of (e-a) blocks needs >= 4 bytes each
                try:
                    be, o, lc = decode_block_at(b, e)
                except (DecodeError, NotSupportedByAdapter):
                    continue
                if ki == len(runs) - 1:
                    record_run(a, e, q, b)
                    objects[e] = o
                    links_all[e] = lc
                    qq, ok2 = be, True
                    bidx = e + 1
                    while ok2 and bidx < n_obj:
                        try:
                            qq, o2, lc2 = decode_block_at(qq, bidx)
                        except (DecodeError, NotSupportedByAdapter):
                            ok2 = False
                            break
                        objects[bidx] = o2
                        links_all[bidx] = lc2
                        bidx += 1
                    if ok2 and footer_at(qq) is not None:
                        footer_holder[0] = (qq, footer_at(qq))
                        return qq
                    for bidx2 in range(e, n_obj):
                        objects[bidx2] = None
                        links_all[bidx2] = None
                    continue
                sub = assemble(ki + 1, be, e + 1)
                if sub is not None:
                    record_run(a, e, q, b)
                    objects[e] = o
                    links_all[e] = lc
                    return sub
            return None

        return assemble(0, pos_start, 0)

    links_all = [None] * n_obj
    if not b_new:
        # LEGACY ORIGINAL-VERDICT WALK: for < 5.0.0.1 files there is no RTTI
        # table, so the ORIGINAL verdict (LoadObject -> RTTIError) is derived
        # by walking blocks sequentially with GB 1.2 semantics until an
        # UNREGISTERED inline class is met (LoadObject L451-468) or an
        # adapter-unimplemented class blocks the walk (verdict stays
        # UNDETERMINED, honestly).
        walk_pos = r.pos
        walk_err = None
        walk_blocked = None
        for wi in range(n_obj):
            try:
                rr2 = Reader(data, walk_pos)
                tname = rr2.rtti_string()
            except DecodeError:
                break
            if tname not in registered_classes:
                walk_err = tname
                break
            if tname not in LOADERS:
                walk_blocked = tname
                break
            try:
                o2 = {"index": wi}
                l2 = []
                LOADERS[tname](rr2, ver, o2, l2)
                walk_pos = rr2.pos
            except (DecodeError, NotSupportedByAdapter):
                walk_blocked = tname
                break
        if walk_err is not None:
            # ORIGINAL fail-closed verdict: LoadObject -> RTTIError -> false
            res["load_result"].update(
                accepted=False, partial=False,
                error="RTTIError(%s): cannot find create function." % walk_err,
                error_code="RTTIError")
            res["rtti_gate"] = {
                "registered_class_count": len(registered_classes),
                "file_type_count": None,
                "unregistered_types": [walk_err],
                "first_unregistered_scan_order": walk_err,
                "layout": "legacy inline-RTTI (< 5.0.0.1)",
                "registry_provenance": "Gb12_Source CoreLibs *SDM.cpp census",
            }
            res["unknowns"] = [
                {"class": walk_err, "status": "UNREGISTERED_IN_GB12_FACTORY"}]
            if not full_decode:
                return res
            # OUR extension continues below (never original behavior)
            res["decode_continued_after_rtti_gate"] = True
            res["load_result"]["partial"] = True
            res["warnings"].append(
                "decode_continued_after_rtti_gate=true is OUR extension; the "
                "ORIGINAL GB 1.2 Load() returns false at LoadObject")
        elif walk_blocked is not None:
            res["warnings"].append(
                "legacy original-verdict walk blocked at class %r (adapter "
                "not implemented); original verdict UNDETERMINED beyond it"
                % walk_blocked)
    closure_error = None
    pos_start = r.pos
    fpos = None
    if b_new:
        # E3: try the right-to-left footer-anchored pre-solver first (same
        # acceptance semantics as decode_rest; see presolve_runs docstring)
        fpos = presolve_runs()
    if fpos is None:
        if b_new:
            # clear any partial pre-solver state before the DFS fallback
            for bidx in range(n_obj):
                objects[bidx] = None
                links_all[bidx] = None
        try:
            fpos = decode_rest(r.pos, 0)
        except DecodeError as e:
            closure_error = str(e)
            fpos = None
    if fpos is None:
        if closure_error is None:
            closure_error = ("CLOSURE_SEARCH_FAILED: no boundary assignment "
                             "closes the file to EOF")
        if res["load_result"]["error"] is None:
            res["load_result"].update(
                accepted=False, partial=True,
                error="DECODE_ERROR: %s" % closure_error,
                error_code="DECODE_ERROR")
        res["warnings"].append(closure_error)
        res["objects"] = [o for o in objects if o is not None]
    res["objects"] = objects
    if not b_new:
        # legacy files have no RTTI table; derive the histogram from the
        # walked blocks (their inline RTTI names the classes)
        hist = {}
        for o in objects:
            if o and o.get("type"):
                hist[o["type"]] = hist.get(o["type"], 0) + 1
        res["type_histogram"] = hist
        return res

    if fpos is None:
        # E3 fix (E2 defect): b_new closure failure must return the honest
        # partial result -- the E2 code fell through to the footer read with
        # fpos=None and crashed (TypeError) instead of reporting DECODE_ERROR.
        return res

    # ---------------- footer: LoadTopLevelObjects L367-385 ---------------
    rr = Reader(data, fpos)
    n_top = rr.u32()
    tops = [rr.i32() for _ in range(n_top)]
    if rr.pos != len(data):
        res["warnings"].append("TRAILING_BYTES after footer")
    res["scene_graph"]["roots"] = tops

    # ---------------- link phase (GB12 semantics, per-object order) ------
    for i, o in enumerate(objects):
        if o is None or links_all[i] is None:
            continue
        tname = o.get("type")
        for field, lids in links_all[i]:
            resolved = []
            for lid in lids:
                if lid == NULL_LINKID:
                    resolved.append(None)
                elif lid >= n_obj:
                    res["warnings"].append(
                        "LINK_FAILURE: block %d (%s) field %s link %d out of "
                        "range (num_blocks=%d)" % (i, tname, field, lid, n_obj))
                    resolved.append("LINK_ERROR_OUT_OF_RANGE")
                else:
                    resolved.append(lid)
            o.setdefault("links", {})[field] = resolved
            if field == "children" and tname == "NiNode":
                for c in resolved:
                    if isinstance(c, int):
                        res["scene_graph"]["edges"].append(
                            {"parent": i, "child": c, "field": "children"})

    # object-count mismatch detector (fail-closed, s17)
    decoded_count = sum(1 for o in objects if o is not None)
    res["object_count_check"] = {
        "header_num_blocks": n_obj,
        "decoded_blocks": decoded_count,
        "match": decoded_count == n_obj,
    }
    if decoded_count != n_obj:
        res["warnings"].append(
            "OBJECT_COUNT_MISMATCH: header %d vs decoded %d"
            % (n_obj, decoded_count))

    res["objects"] = objects
    had_unregistered = bool(res.get("rtti_gate", {}).get("unregistered_types"))
    if not had_unregistered and all(o is not None for o in objects):
        res["load_result"].update(accepted=True, partial=False, error=None,
                                  error_code=None)
    else:
        res["load_result"]["partial"] = True
        res["load_result"]["accepted"] = False
    # controllers / properties / textures / bounds summaries
    for o in objects:
        if o is None:
            continue
        t = o.get("type", "")
        if t == "NiTimeController" or t.endswith("Controller"):
            res["controllers"].append(
                {"index": o["index"], "type": t,
                 "target": (o.get("links", {}).get("target") or [None])[0],
                 "next": (o.get("links", {}).get("next_controller") or [None])[0]})
        if t.endswith("Property"):
            res["properties"].append({"index": o["index"], "type": t,
                                      "name": o.get("name")})
        if t in ("NiSourceTexture", "NiTexture"):
            res["textures"].append(
                {"index": o["index"], "type": t,
                 "filename": o.get("filename"),
                 "external": o.get("external")})
        if "model_bound" in o:
            res["bounds"].append({"geometry_data_block": o["index"],
                                  "type": t, "model_bound": o["model_bound"]})
        if o.get("status") in ("UNREGISTERED_IN_GB12_FACTORY",
                               "REGISTERED_BUT_NOT_DECODED_BY_ADAPTER",
                               "UNKNOWN_BLOCK_BOUNDARY_ONLY"):
            res["unknowns"].append({
                "index": o["index"], "class": o.get("type"),
                "status": o.get("status"),
                "byte_start": o.get("byte_start"),
                "byte_end": o.get("byte_end"),
            })
    return res

