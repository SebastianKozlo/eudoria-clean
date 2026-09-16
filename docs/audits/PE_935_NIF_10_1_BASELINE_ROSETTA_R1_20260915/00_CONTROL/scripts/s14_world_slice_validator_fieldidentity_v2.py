#!/usr/bin/env python3
# s14_world_slice_validator_fieldidentity_v2.py -- FIELD-IDENTITY-V2
# successor of s06_world_slice_validator.py for
# PE_935_NIF_10_1_WORKAUDIT_CORRECTION_R1_20260916 (contracts C3-C6).
#
# SUPERSEDES TOOLING BEHAVIOR: SchemaDecoder._fields_for is replaced by
# an OCCURRENCE-PRESERVING field list (FIELD_IDENTITY_V2: identity =
# owner_type + field_name + occurrence_index + field_type + ver1 + ver2
# + vercond + cond + template + schema_order; DISPLAY LABEL != SCHEMA
# FIELD IDENTITY; conditional alternatives stay distinct until
# value-condition evaluation).
# DOES NOT REWRITE HISTORICAL HOLDOUT: s06/s04 bytes are unchanged;
# s14 subclasses them. The ONLY behavioral delta vs the frozen decoder
# is _fields_for -- every other code path (header parse, Ark search,
# candidates, closure discipline, gid==0 invariant) is inherited
# byte-for-byte from s06, so old-vs-v2 comparisons isolate exactly the
# field-identity model.
#
# Used by:
#   C5  NiSourceTexture bounded structural regression (corpus-wide)
#   C6  2363-file world-slice regression (old vs v2)
#   C12 revalidation evidence
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from s06_world_slice_validator import (  # noqa: E402
    WorldSliceValidator, SchemaDecoder)
from s04_nifxml_baseline import SchemaOracle, HIST  # noqa: E402


class SchemaDecoderV2(SchemaDecoder):
    """s06 SchemaDecoder with the field-identity defect repaired.

    The frozen s06 _fields_for deduplicated effective fields by bare
    FIELD NAME across the inheritance chain (first occurrence wins
    unless a later one has strictly higher version-preference). That
    LOSES same-name occurrences whose conditions differ, e.g.
    NiSourceTexture "File Name"[Use External == 1] vs
    "File Name"[Use External == 0, ver1=10.1.0.0] -- for
    Use External == 0 blocks the filename was then never consumed,
    shifting the block boundary (BABYLENGUIN counterexample).
    """

    def _fields_for(self, type_name):
        # FIELD_IDENTITY_V2: NO name dedup. Every schema field
        # occurrence in the chain is preserved, in schema order
        # (parent first). The decoder's existing per-field logic
        # (field_included version gate -> cond evaluation) then decides
        # which occurrence applies; alternatives remain distinct until
        # value-condition evaluation.
        if type_name in self.type_cache:
            return self.type_cache[type_name]
        chain = []
        t = type_name
        while t and t in self.s.objects:
            chain.append(t)
            t = self.s.objects[t]['inherit']
        eff = []
        for ancestor in reversed(chain):
            for f in self.s.objects[ancestor]['fields']:
                eff.append((ancestor, f))
        self.type_cache[type_name] = eff
        return eff


class WorldSliceValidatorV2(WorldSliceValidator):
    """s06 WorldSliceValidator using SchemaDecoderV2.

    Everything except the decoder construction is inherited unchanged
    from the frozen s06 class (including the Ark block byte-search and
    the closure discipline). The gid==0 invariant is PE-scoped and
    stays as designed.
    """

    def __init__(self):
        self.schema = SchemaOracle(HIST, 'NIFXML_HIST_0_7_1_1', 'add')
        self.dec = SchemaDecoderV2(self.schema)
        self.layout_variant_wins = {}


def build_validator():
    return WorldSliceValidatorV2()
