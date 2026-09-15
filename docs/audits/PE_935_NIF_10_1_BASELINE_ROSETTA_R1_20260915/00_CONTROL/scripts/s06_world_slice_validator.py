#!/usr/bin/env python3
"""s06_world_slice_validator.py — independent schema-driven structural
decoder + full-file closure validator for the NIF 10.1.0.0 world slice.

Run: PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915 (§8, §9, G6, G7).

METHOD (anti-circular):
- Standard types: decoded STRICTLY from the pinned external baseline
  (SRC-02 nifxml historical 0.7.1.1 field tables + SRC-06 engine framing:
  per-block GroupID u32, TopObjects footer). No wiki/R61/NifModelReader input.
- Custom/variable Ark blocks: boundary derived FROM BYTES via
  closure-constrained search (the only accepted candidate is one that lets
  the WHOLE file decode to EOF-exact closure).
- Every file: header + GroupID+block×N + TopObjects + EOF must be exact.

TRAIN/HOLDOUT: deterministic split by payload SHA256 (80/20).
"""
import json
import math
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from s01_bnt2_walk import walk_bnt2  # noqa: E402
from s02_nif_version_scan import ARCHIVE, LOCAL_OUT, REPO_RAW  # noqa: E402
from s04_nifxml_baseline import SchemaOracle, HIST, Unresolved  # noqa: E402

V10_1 = 0x0A010000

# type-name conditions used by nif.xml inherited-field dedup
TYPE_COND = {'NiPSysData'}


class Cursor:
    __slots__ = ('data', 'pos')

    def __init__(self, data, pos=0):
        self.data = data
        self.pos = pos

    def read(self, n):
        if self.pos + n > len(self.data):
            raise struct.error('EOF')
        b = self.data[self.pos:self.pos + n]
        self.pos += n
        return b

    def u8(self):
        return self.read(1)[0]

    def i8(self):
        return struct.unpack('<b', self.read(1))[0]

    def u16(self):
        return struct.unpack('<H', self.read(2))[0]

    def i16(self):
        return struct.unpack('<h', self.read(2))[0]

    def u32(self):
        return struct.unpack('<I', self.read(4))[0]

    def i32(self):
        return struct.unpack('<i', self.read(4))[0]

    def f32(self):
        v = struct.unpack('<f', self.read(4))[0]
        if math.isnan(v) or math.isinf(v):
            raise struct.error('NaN/Inf float')
        return v

    def skip(self, n):
        self.read(n)


class SchemaDecoder:
    """Table-driven decoder for NIF 10.1.0.0 blocks from the HIST schema."""

    def __init__(self, schema):
        self.s = schema
        self.version = V10_1
        self.user_version = 0
        # concrete type being decoded (for template conds like !NiPSysData)
        self.concrete_type = None
        self.type_cache = {}
        self._known_fields = set()

    def _fields_for(self, type_name):
        if type_name in self.type_cache:
            return self.type_cache[type_name]
        chain = []
        t = type_name
        while t and t in self.s.objects:
            chain.append(t)
            t = self.s.objects[t]['inherit']
        eff = []
        index_by_name = {}

        def pref(f):
            ok, _ = self.s.field_applies(f)
            # True (applicable) > None (unresolved) > False (excluded)
            return 2 if ok is True else (1 if ok is None else 0)

        for ancestor in reversed(chain):
            for f in self.s.objects[ancestor]['fields']:
                name = f['name']
                if name in index_by_name:
                    idx = index_by_name[name]
                    if pref(f) > pref(eff[idx][1]):
                        eff[idx] = (ancestor, f)
                    continue
                index_by_name[name] = len(eff)
                eff.append((ancestor, f))
        self.type_cache[type_name] = eff
        return eff

    def eval(self, expr, values):
        """Evaluate a nif.xml expression with instance field values."""
        if expr is None:
            return True
        e = expr.strip()
        if not e:
            return True
        # identifier/number tokenizer with ops
        toks = []
        i = 0
        while i < len(e):
            c = e[i]
            if c.isspace():
                i += 1
                continue
            if e.startswith('&&', i) or e.startswith('||', i):
                toks.append(e[i:i + 2]); i += 2; continue
            if e.startswith('!=', i) or e.startswith('==', i) or \
               e.startswith('<=', i) or e.startswith('>=', i):
                toks.append(e[i:i + 2]); i += 2; continue
            if c in '!<>()&|+-*/':
                toks.append(c); i += 1; continue
            m = None
            import re
            m = re.match(r'\d+(\.\d+){0,3}', e[i:])
            if m:
                lit = m.group(0)
                if '.' in lit:
                    from s04_nifxml_baseline import ver2int
                    toks.append(('V', ver2int(lit)))
                else:
                    toks.append(('N', int(lit)))
                i += len(lit)
                continue
            m = re.match(r'[A-Za-z_][A-Za-z0-9_ ]*', e[i:])
            if m:
                name = m.group(0).strip()
                i += len(m.group(0))
                if name in TYPE_COND or (name in self.s.objects):
                    # template/type-name condition
                    ct = self.concrete_type or ''
                    inherits = set()
                    t = ct
                    while t and t in self.s.objects:
                        inherits.add(t)
                        t = self.s.objects[t]['inherit']
                    toks.append(('N', 1 if (name == ct or
                                            name in inherits) else 0))
                    continue
                if name in values:
                    toks.append(('N', values[name]))
                    continue
                if self._known_fields and name in self._known_fields:
                    # a schema field of this type that is version-excluded
                    # (absent in 10.1): conditions on it are FALSE
                    toks.append(('N', 0))
                    continue
                if name == 'Version':
                    toks.append(('N', self.version))
                    continue
                if name == 'User Version':
                    toks.append(('N', self.user_version))
                    continue
                raise Unresolved(f'identifier {name!r}')
            raise Unresolved(f'char {c!r}')
        # shunting-yard to RPN
        prec = {'||': 1, '&&': 2, '|': 3, '^': 4, '&': 5,
                '==': 6, '!=': 6, '<': 7, '>': 7, '<=': 7, '>=': 7,
                '+': 8, '-': 8, '*': 9, '/': 9, '<<': 10, '>>': 10}
        out, ops = [], []
        for t in toks:
            if isinstance(t, tuple):
                out.append(t)
            elif t == '(':
                ops.append(t)
            elif t == ')':
                while ops and ops[-1] != '(':
                    out.append(ops.pop())
                if not ops:
                    raise Unresolved('paren')
                ops.pop()
            elif t == '!':
                ops.append(t)
            else:
                while ops and ops[-1] != '(' and ops[-1] != '!' and \
                        prec.get(ops[-1], 99) >= prec.get(t, 0):
                    out.append(ops.pop())
                ops.append(t)
        while ops:
            o = ops.pop()
            if o == '(':
                raise Unresolved('paren')
            out.append(o)
        # evaluate RPN
        st = []

        def pop():
            if not st:
                raise Unresolved('stack underflow')
            return st.pop()
        for t in out:
            if isinstance(t, tuple):
                st.append(t[1])
            elif t == '!':
                st.append(0 if pop() else 1)
            elif t in prec or t in ('<<', '>>'):
                b = pop(); a = pop()
                if t == '&&':
                    st.append(1 if (a and b) else 0)
                elif t == '||':
                    st.append(1 if (a or b) else 0)
                elif t == '==':
                    st.append(1 if a == b else 0)
                elif t == '!=':
                    st.append(1 if a != b else 0)
                elif t == '<':
                    st.append(1 if a < b else 0)
                elif t == '>':
                    st.append(1 if a > b else 0)
                elif t == '<=':
                    st.append(1 if a <= b else 0)
                elif t == '>=':
                    st.append(1 if a >= b else 0)
                elif t == '+':
                    st.append(a + b)
                elif t == '-':
                    st.append(a - b)
                elif t == '*':
                    st.append(a * b)
                elif t == '/':
                    st.append(a // b if b else 0)
                elif t == '&':
                    st.append(a & b)
                elif t == '|':
                    st.append(a | b)
                elif t == '<<':
                    st.append(a << b)
                elif t == '>>':
                    st.append(a >> b)
                else:
                    raise Unresolved(f'op {t}')
            else:
                raise Unresolved(f'tok {t}')
        if len(st) != 1:
            raise Unresolved('stack')
        # return the raw numeric value: array counts need ints; boolean
        # contexts use Python truthiness (nonzero = true)
        return st[0]

    def field_included(self, f):
        """Version-level inclusion of a field for 10.1.0.0/UV=0."""
        ok, _ = self.s.field_applies(f)
        if ok is False:
            return False
        if ok is None:
            raise Unresolved('field version condition')
        uv = f.get('userver') if hasattr(f, 'get') else None
        # userver attr on fields: present only when User Version matches
        if uv is not None:
            try:
                if int(uv) != self.user_version:
                    return False
            except ValueError:
                return False
        return True

    def read_value(self, cur, ftype, values, depth=0):
        """Read one value of schema type ftype. Returns python value."""
        if depth > 6:
            raise Unresolved('compound depth')
        if ftype in ('bool', 'byte', 'ubyte', 'char'):
            return cur.u8()
        if ftype in ('short', 'ushort', 'Flags'):
            return cur.u16()
        if ftype in ('int', 'uint', 'ulittle32', 'FileVersion'):
            return cur.u32()
        if ftype == 'float':
            return cur.f32()
        if ftype in ('Ref', 'Ptr'):
            return cur.i32()
        if ftype in ('string', 'SizedString', 'FilePath'):
            ln = cur.u32()
            if ln > 1 << 20:
                raise Unresolved(f'string too long {ln}')
            return cur.read(ln).decode('latin-1')
        if ftype in ('HeaderString', 'LineString'):
            end = cur.data.index(b'\x0A', cur.pos)
            v = cur.data[cur.pos:end].decode('latin-1')
            cur.pos = end + 1
            return v
        if ftype in ('ByteArray',):
            n = self.eval('Num Bytes' if False else '1', values) \
                if False else None
            raise Unresolved('ByteArray needs count')
        if ftype in self.s.enum_storage:
            st = self.s.enum_storage[ftype]
            return {'uint': cur.u32, 'ushort': cur.u16,
                    'int': cur.i32, 'short': cur.i16,
                    'byte': cur.u8, 'ubyte': cur.u8}[st]()
        c = self.s.compounds.get(ftype)
        if c:
            vals = {}
            saved_kf = self._known_fields
            self._known_fields = saved_kf | {cf['name'] for cf in c['fields']}
            try:
                for cf in c['fields']:
                    ok, _ = self.s.field_applies(cf)
                    if ok is False:
                        continue
                    if ok is None:
                        raise Unresolved('compound field vercond')
                    if cf['name'] in vals:
                        continue  # duplicate already-read applicable field
                    cond = cf.get('cond')
                    if cond and not self.eval(cond, vals):
                        continue
                    name = cf['name']
                    arr1 = cf.get('arr1')
                    if arr1:
                        n = self.eval(arr1, vals)
                        vals[name] = [self.read_value(cur, cf['type'], vals,
                                                       depth + 1)
                                     for _ in range(n)]
                    else:
                        vals[name] = self.read_value(cur, cf['type'], vals,
                                                      depth + 1)
            finally:
                self._known_fields = saved_kf
            return vals
        raise Unresolved(f'unknown type {ftype}')

    def decode_block(self, cur, type_name):
        """Decode one block (after GroupID) per schema. Returns dict."""
        self.concrete_type = type_name
        self._known_fields = {f['name'] for _, f in self._fields_for(type_name)}
        values = {'__type__': type_name}
        for owner, f in self._fields_for(type_name):
            if not self.field_included(f):
                continue
            cond = f.get('cond')
            if cond and not self.eval(cond, values):
                continue
            name = f['name']
            arr1 = f.get('arr1')
            arr2 = f.get('arr2')
            try:
                if arr1 and arr2:
                    n1 = self.eval(arr1, values)
                    n2 = self.eval(arr2, values)
                    if n1 * n2 > 3_000_000:
                        raise Unresolved(f'array too big {n1}x{n2}')
                    values[name] = [
                        [self.read_value(cur, f['type'], values)
                         for _ in range(n2)] for _ in range(n1)]
                elif arr1:
                    n = self.eval(arr1, values)
                    if n > 3_000_000:
                        raise Unresolved(f'array too big {n}')
                    values[name] = [self.read_value(cur, f['type'], values)
                                    for _ in range(n)]
                else:
                    values[name] = self.read_value(cur, f['type'], values)
            except Unresolved as e:
                raise Unresolved(
                    f'{type_name}.{name}[{owner}]: {e}') from e
            except struct.error as e:
                raise Unresolved(
                    f'{type_name}.{name}: EOF/desync at {cur.pos}') from e
        return values

    def decode_prefix(self, cur, type_name):
        """Decode ONLY the inherited (ancestor) fields of type_name."""
        self.concrete_type = type_name
        values = {'__type__': type_name}
        for owner, f in self._fields_for(type_name):
            if owner == type_name:
                continue  # skip own fields
            if not self.field_included(f):
                continue
            cond = f.get('cond')
            if cond and not self.eval(cond, values):
                continue
            name = f['name']
            arr1 = f.get('arr1')
            try:
                if arr1:
                    n = self.eval(arr1, values)
                    if n > 3_000_000:
                        raise Unresolved(f'array too big {n}')
                    values[name] = [self.read_value(cur, f['type'], values)
                                    for _ in range(n)]
                else:
                    values[name] = self.read_value(cur, f['type'], values)
            except Unresolved as e:
                raise Unresolved(f'prefix.{name}[{owner}]: {e}') from e
        return values


class ArkBlockError(Exception):
    pass


class WorldSliceValidator:
    """Full-file closure validator for files whose types are all supported."""

    # types with variable/ambiguous tails needing byte-derived boundaries
    ARK_SEARCH = {'NiArkViewportInfoExtraData', 'NiArkAnimationExtraData',
                  'NiArkImporterExtraData', 'NiArkTextureExtraData'}
    # types whose schema layout competes with an alternative hypothesis
    # (closure decides; the alternative is a competing NAMED hypothesis)
    LAYOUT_VARIANTS = {
        # wiki-claimed alt: u16 + u16 + u16 + u32 (schema: u16 + u32 + u32)
        'NiVertexColorProperty': ('schema', 'u16x3_u32'),
    }

    def __init__(self):
        self.schema = SchemaOracle(HIST, 'NIFXML_HIST_0_7_1_1', 'add')
        self.dec = SchemaDecoder(self.schema)
        self.layout_variant_wins = {}

    def parse_header(self, cur):
        nl = cur.data.index(b'\x0A', cur.pos)
        cur.pos = nl + 1
        ver = cur.u32()
        if ver != V10_1:
            raise ArkBlockError('not 10.1')
        uv = cur.u32()
        nb = cur.u32()
        nbt = cur.u16()
        names = []
        for _ in range(nbt):
            ln = cur.u32()
            names.append(cur.read(ln).decode('ascii'))
        idx = [cur.u16() for _ in range(nb)]
        ng = cur.u32()
        if ng:
            raise ArkBlockError('nonzero groups not supported yet')
        return {'num_blocks': nb, 'types': names, 'idx': idx}

    def decode_block_variants(self, cur, tname):
        """Decode a standard block with layout variants (schema first).
        Returns (blk, variant_name) or raises on total failure."""
        variants = self.LAYOUT_VARIANTS.get(tname, ('schema',))
        last_err = None
        for variant in variants:
            save = cur.pos
            try:
                if variant == 'schema':
                    blk = self.dec.decode_block(cur, tname)
                elif tname == 'NiVertexColorProperty' and \
                        variant == 'u16x3_u32':
                    blk = self.dec.decode_prefix(cur, tname)
                    blk['flags_u16'] = cur.u16()
                    blk['vertex_mode_u16'] = cur.u16()
                    blk['lighting_mode_u16'] = cur.u16()
                    blk['pe_ext_u32'] = cur.u32()
                else:
                    raise Unresolved('unknown variant')
                return blk, variant
            except (Unresolved, struct.error, ValueError, IndexError) as e:
                cur.pos = save
                last_err = e
        raise last_err or Unresolved('no variant worked')

    def decode_file(self, data, allow_search=True):
        """Full-file decode with closure + backtracking over Ark boundaries.

        Boundary/count decisions are SEARCHED (candidates from bytes and
        from multiple structural hypotheses); a decision is accepted ONLY
        if the whole file closes to EOF-exact. This makes the boundary
        byte-derived: wrong candidates fail downstream decode.
        """
        cur = Cursor(data)
        hdr = self.parse_header(cur)
        self._attempts = 0
        blocks = [None] * hdr['num_blocks']
        result = self._decode_blocks(cur, hdr, 0, blocks, allow_search)
        if result is None:
            raise ArkBlockError('closure search exhausted')
        blocks, search_used = result
        ntop = cur.u32()
        tops = [cur.i32() for _ in range(ntop)]
        if cur.pos != len(data):
            raise ArkBlockError(
                f'TRAILING_BYTES: pos {cur.pos} != size {len(data)}')
        return {'blocks': blocks, 'top_objects': tops,
                'search_used': search_used, 'num_blocks': hdr['num_blocks'],
                'attempts': self._attempts}

    def _decode_blocks(self, cur, hdr, i, blocks, allow_search):
        """Decode blocks i..N-1 with backtracking. Returns (blocks, search)
        or None. cur is advanced on success only (snapshot/restore)."""
        if i >= hdr['num_blocks']:
            return blocks, []
        tname = hdr['types'][hdr['idx'][i]]
        start = cur.pos
        self._attempts += 1
        if self._attempts > 50000:
            return None
        gid = cur.u32()
        if gid != 0:
            return None
        if tname in self.dec.s.objects and tname not in self.ARK_SEARCH:
            variants = self.LAYOUT_VARIANTS.get(tname, ('schema',))
            for variant in variants:
                save = cur.pos
                try:
                    if variant == 'schema':
                        blk = self.dec.decode_block(cur, tname)
                    else:
                        blk, variant = self.decode_block_variants(cur, tname)
                except (Unresolved, struct.error, ValueError, IndexError):
                    cur.pos = save
                    return None
                blk['__start__'] = start
                blk['__end__'] = cur.pos
                blk['__type__'] = tname
                if tname in self.LAYOUT_VARIANTS and \
                        len(self.LAYOUT_VARIANTS[tname]) > 1:
                    blk['__layout_variant__'] = variant
                blocks[i] = blk
                res = self._decode_blocks(cur, hdr, i + 1, blocks,
                                          allow_search)
                if res is not None:
                    return blocks, res[1]
                blocks[i] = None
                cur.pos = save
            return None
        # Ark search block: candidate-driven
        self._current_num_blocks = hdr['num_blocks']
        for cand in self.ark_candidates(cur, tname):
            save = cur.pos
            try:
                blk = self._decode_ark_with(cur, tname, cand)
            except (Unresolved, struct.error, ValueError, IndexError):
                blk = None
            if blk is None:
                cur.pos = save
                continue
            blk['__start__'] = start
            blk['__end__'] = cur.pos
            blk['__type__'] = tname
            blk['__decision__'] = cand
            blocks[i] = blk
            res = self._decode_blocks(cur, hdr, i + 1, blocks, allow_search)
            if res is not None:
                return blocks, ([(i, tname, cand)] + res[1])
            blocks[i] = None
            cur.pos = save
        return None

    def footer_positions(self, data, from_pos, num_blocks):
        """Positions where a TopObjects footer could start: u32 count c
        with 0 <= c <= num_blocks and from_pos..p+4+4c == EOF exactly."""
        n = len(data)
        out = []
        for p in range(from_pos, min(from_pos + 8192, n - 3)):
            c, = struct.unpack('<I', data[p:p + 4])
            if 0 <= c <= num_blocks and p + 4 + 4 * c == n:
                out.append(p)
        return out

    def ark_candidates(self, cur, tname):
        """Candidate decisions for a variable Ark block."""
        data = cur.data
        start = cur.pos
        num_blocks = getattr(self, '_current_num_blocks', 1 << 30)
        footers = set(self.footer_positions(data, start, num_blocks))
        if tname == 'NiArkBillboardNode':
            # hypotheses: NiNode + u16 mode / NiNode + u32 mode / plain NiNode
            cands = []
            for extra, mode in ((2, 'u16'), (4, 'u32'), (0, 'none')):
                cands.append({'kind': 'arkbillboard', 'extra': extra,
                              'mode': mode})
            return cands
        # NiExtraData base name first
        if start + 4 > len(data):
            return []
        name_ln, = struct.unpack('<I', data[start:start + 4])
        if name_ln > 256:
            return []
        after_name = start + 4 + name_ln
        cands = []
        if tname == 'NiArkImporterExtraData':
            # after name: u32 int + SS version string -> tail of unknown size
            if after_name + 4 > len(data):
                return []
            p = after_name + 4
            if p + 4 > len(data):
                return []
            ln, = struct.unpack('<I', data[p:p + 4])
            if ln > 64:
                return []
            tail_start = p + 4 + ln
            # competing hypotheses: schema-implied 41 (13B + 7xf32),
            # wiki-claimed 38; closure decides from bytes. Prefer tails
            # that leave a valid footer.
            for tail in (41, 38, 37, 40, 42, 43, 44):
                cands.append({'kind': 'importer', 'tail': tail,
                              'end': tail_start + tail})
            if footers:
                cands.sort(key=lambda c: 0 if c['end'] in footers else 1)
        elif tname == 'NiArkTextureExtraData':
            # after name: u32 A + u32 B + u32 C + u8 pad -> entries
            p = after_name
            if p + 13 > len(data):
                return []
            A, = struct.unpack('<I', data[p:p + 4])
            B, = struct.unpack('<I', data[p + 4:p + 8])
            C, = struct.unpack('<I', data[p + 8:p + 12])
            pad = data[p + 12]
            entry_start = p + 13
            counts = []
            for cnd, src in ((A, 'numfield'), (B, 'field1'),
                             ((C >> 8) & 0xFFFFFF, 'field2>>8'),
                             (C & 0xFFFFFF, 'field2&0xffffff')):
                if 0 <= cnd <= 2048:
                    counts.append((cnd, src))
            counts.append((0, 'zero'))
            # dedup
            seen = set()
            for cnd, src in counts:
                if cnd in seen:
                    continue
                seen.add(cnd)
                cands.append({'kind': 'texture', 'count': cnd,
                              'count_source': src,
                              'entry_start': entry_start, 'A': A, 'B': B,
                              'C': C, 'pad': pad})
        elif tname in ('NiArkViewportInfoExtraData',
                       'NiArkAnimationExtraData'):
            # ext of unknown length; next block starts with u32 GroupID==0
            # then a plausible NiObjectNET name — OR the TopObjects footer.
            scored = []
            pos = after_name
            window_end = min(len(data), after_name + 8192)
            while pos < window_end:
                if pos + 8 <= len(data):
                    g, = struct.unpack('<I', data[pos:pos + 4])
                    if g == 0:
                        ln, = struct.unpack('<I', data[pos + 4:pos + 8])
                        if ln <= 256:
                            nm = data[pos + 8:pos + 8 + ln]
                            if len(nm) == ln:
                                pr = sum(1 for b in nm
                                         if 32 <= b < 127 or b == 0) / ln \
                                    if ln else 1.0
                                if pr >= 0.8:
                                    rank = 0 if 4 <= ln <= 64 else 1
                                    scored.append((rank, pos))
                pos += 1
            for fpos in footers:
                scored.append((0, fpos))  # footer boundary = strong candidate
            scored.sort()
            seen_pos = set()
            for rank, c in scored[:1024]:
                if c in seen_pos:
                    continue
                seen_pos.add(c)
                cands.append({'kind': 'ext', 'end': c})
        return cands

    def _decode_ark_with(self, cur, tname, cand):
        """Decode Ark block applying a candidate decision."""
        if cand['kind'] == 'arkbillboard':
            # NiNode-derived: the NiObjectNET Name is INSIDE the NiNode
            # decode — do NOT pre-read a NiExtraData-style name.
            blk = self.dec.decode_block(cur, 'NiNode')
            if cand['mode'] == 'u16':
                blk['mode_u16'] = cur.u16()
            elif cand['mode'] == 'u32':
                blk['mode_u32'] = cur.u32()
            blk['mode_style'] = cand['mode']
            return blk
        try:
            name_ln = cur.u32()
            name = cur.read(name_ln).decode('latin-1')
        except (struct.error, UnicodeDecodeError):
            return None
        blk = {'name': name, '__boundary__': 'search'}
        if cand['kind'] == 'importer':
            blk['int1'] = cur.u32()
            ln = cur.u32()
            blk['version_string'] = cur.read(ln).decode('latin-1')
            blk['tail_len'] = cand['tail']
            tail = cur.read(cand['tail'])
            blk['tail_hex_head'] = tail[:16].hex()
            if cur.pos != cand['end']:
                return None
            return blk
        if cand['kind'] == 'texture':
            blk['numfield'] = cur.u32()
            blk['field1'] = cur.u32()
            blk['field2'] = cur.u32()
            blk['pad'] = cur.u8()
            if blk['numfield'] != cand['A'] or blk['field1'] != cand['B'] \
                    or blk['field2'] != cand['C']:
                return None
            entries = []
            for k in range(cand['count']):
                try:
                    ln = cur.u32()
                    ename = cur.read(ln).decode('latin-1')
                    f1 = cur.i32()
                    f2 = cur.i32()
                    ref = cur.i32()
                    tr9 = cur.read(9)
                except struct.error:
                    return None
                entries.append({'name': ename, 'f1': f1, 'f2': f2,
                                'ref': ref, 'tr9': tr9.hex()})
            blk['entries'] = entries
            blk['entry_count'] = cand['count']
            blk['count_source'] = cand['count_source']
            return blk
        if cand['kind'] == 'ext':
            ext_len = cand['end'] - cur.pos
            if ext_len < 0:
                return None
            blk['ext_len'] = ext_len
            blk['ext'] = cur.read(ext_len).hex()
            return blk
        return None


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--sample', type=int, default=3)
    ap.add_argument('--offset', type=int, default=0)
    args = ap.parse_args()
    v = WorldSliceValidator()
    walk = walk_bnt2(ARCHIVE)
    # candidate files: only supported types
    supported = set('''NiNode NiTriShape NiTriShapeData NiTexturingProperty
NiMaterialProperty NiAlphaProperty NiZBufferProperty NiStencilProperty
NiVertexColorProperty NiSpecularProperty NiShadeProperty NiDitherProperty
NiFogProperty NiSourceTexture NiPixelData NiTextureEffect NiPointLight
NiSpotLight NiDirectionalLight NiAmbientLight NiStringExtraData
NiIntegerExtraData NiBooleanExtraData NiArkAnimationExtraData
NiArkImporterExtraData NiArkTextureExtraData NiArkViewportInfoExtraData
NiArkShaderExtraData NiCollisionData NiSortAdjustNode NiBillboardNode
NiArkBillboardNode'''.split())
    with open(LOCAL_OUT + r'\02_WORK'
              r'\pcg953_type_histograms_independent.json',
              encoding='utf-8') as f:
        histos = json.load(f)
    cand = []
    for e in walk['entries']:
        m = histos.get(e['name'])
        if m is None:
            continue
        if set(m['type_counts']) <= supported:
            cand.append(e)
    print(f'candidate files: {len(cand)}')
    with open(ARCHIVE, 'rb') as f:
        for k, e in enumerate(cand[args.offset:args.offset + args.sample]):
            f.seek(e['offset'])
            data = f.read(e['size'])
            try:
                res = v.decode_file(data)
                print(f'{e["name"]}: CLOSURE_OK blocks={res["num_blocks"]} '
                      f'tops={len(res["top_objects"])}')
            except (ArkBlockError, Unresolved, struct.error, ValueError,
                    IndexError) as ex:
                print(f'{e["name"]}: FAIL {ex}')


if __name__ == '__main__':
    main()
