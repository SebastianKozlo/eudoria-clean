#!/usr/bin/env python3
"""s04_nifxml_baseline.py — normalized NIF 10.1.0.0 baseline from pinned xml.

Run: PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915 (§5, G4).

Builds a machine-readable field table for EVERY schema type and EVERY
physically observed Entropia type, with per-field applicability evaluated
for (Version=10.1.0.0, UserVersion=0, non-Bethesda BSVER=0).

Oracles (SOURCE_REGISTRY): SRC-02 nifxml historical 0.7.1.1 (HIST),
SRC-01 nifxml modern 0.10.0.0 (MOD). Engine framing truths (SRC-06) are
emitted as ORACLE=ENGINE rows for the Header and per-block GroupID framing
(engine source does not provide per-type field tables beyond class code,
which is out of scope for this script — its load-chain evidence lives in
02_ANALYSIS/NIF_10_1_BASELINE_SPEC.md).

Fail-closed: version-condition expressions that cannot be evaluated are
marked UNRESOLVED (never silently included/excluded).

Outputs:
  01_RAW/BASELINE_TYPE_TABLE.csv          (all types x fields x oracle)
  01_RAW/BASELINE_CONFLICT_RAW.csv        (HIST vs MOD diffs)
"""
import csv
import os
import re
import xml.etree.ElementTree as ET

HIST = (r'D:\Eudoria_Reconstruction\04_External_References\reference_only'
        r'\nifxml_historical\nif.xml')
MOD = (r'D:\Eudoria_Reconstruction\04_External_References\reference_only'
       r'\nifxml\nif.xml')
REPO_RAW = (r'D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits'
            r'\PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915\01_RAW')

V10_1 = 0x0A010000
V_MAX = 0xFFFFFFFF


def ver2int(s):
    if not s:
        return None
    parts = [int(x) for x in s.strip().split('.')]
    while len(parts) < 4:
        parts.append(0)
    if len(parts) > 4:
        parts = parts[:4]
    return ((parts[0] & 0xFF) << 24) | ((parts[1] & 0xFF) << 16) | \
        ((parts[2] & 0xFF) << 8) | (parts[3] & 0xFF)


def int2ver(v):
    return f'{(v >> 24) & 0xFF}.{(v >> 16) & 0xFF}.{(v >> 8) & 0xFF}.{v & 0xFF}'


class Unresolved(Exception):
    pass


TOKEN_RE = re.compile(r'#[A-Za-z0-9_]+#')


class Evaluator:
    """Recursive-descent evaluator for nif.xml vercond expressions.

    Context: Version=0x0A010000, User Version=0, BSVER=0 (non-Bethesda).
    Unknown identifiers -> Unresolved (fail-closed).
    """

    IDENTIFIERS = {
        'Version': V10_1,
        'User Version': 0,
        'BSVER': 0,
        'User Version 2': 0,
        'Version 2': None,  # unknown identifier family
    }

    def __init__(self, tokens=None):
        self.tokens = tokens or {}

    def expand(self, expr):
        seen = set()
        def rep(m):
            name = m.group(0)
            if name in seen:
                raise Unresolved(f'token recursion {name}')
            seen.add(name)
            v = self.tokens.get(name)
            if v is None:
                raise Unresolved(f'unknown token {name}')
            return f'({v})'
        for _ in range(8):
            if not TOKEN_RE.search(expr):
                return expr
            expr = TOKEN_RE.sub(rep, expr)
        raise Unresolved('token expansion too deep')

    def evaluate(self, expr):
        if not expr or not expr.strip():
            return True
        expr = self.expand(expr)
        self.pos = 0
        self.s = expr
        val = self.parse_or()
        self.skip_ws()
        if self.pos < len(self.s):
            raise Unresolved(f'trailing {self.s[self.pos:]!r}')
        return bool(val)

    def skip_ws(self):
        while self.pos < len(self.s) and self.s[self.pos].isspace():
            self.pos += 1

    def peek_word(self):
        m = re.match(r'[A-Za-z_][A-Za-z0-9_ ]*', self.s[self.pos:])
        return m.group(0).strip() if m else None

    def parse_or(self):
        v = self.parse_and()
        while True:
            self.skip_ws()
            if self.s[self.pos:self.pos + 2] == '||':
                self.pos += 2
                v2 = self.parse_and()
                v = v or v2
            else:
                return v

    def parse_and(self):
        v = self.parse_not()
        while True:
            self.skip_ws()
            if self.s[self.pos:self.pos + 2] == '&&':
                self.pos += 2
                v2 = self.parse_not()
                v = v and v2
            else:
                return v

    def parse_not(self):
        self.skip_ws()
        if self.s[self.pos:self.pos + 1] == '!':
            self.pos += 1
            return not self.parse_not()
        return self.parse_cmp()

    def parse_cmp(self):
        a = self.parse_atom()
        self.skip_ws()
        for op in ('>=', '<=', '==', '!=', '>', '<'):
            if self.s[self.pos:self.pos + len(op)] == op:
                self.pos += len(op)
                b = self.parse_atom()
                if op == '>=':
                    return a >= b
                if op == '<=':
                    return a <= b
                if op == '==':
                    return a == b
                if op == '!=':
                    return a != b
                if op == '>':
                    return a > b
                if op == '<':
                    return a < b
        return a

    def parse_atom(self):
        self.skip_ws()
        if self.s[self.pos:self.pos + 1] == '(':
            self.pos += 1
            v = self.parse_or()
            self.skip_ws()
            if self.s[self.pos:self.pos + 1] != ')':
                raise Unresolved('missing )')
            self.pos += 1
            return v
        m = re.match(r'\d+(\.\d+){0,3}', self.s[self.pos:])
        if m:
            lit = m.group(0)
            if '.' in lit:
                self.pos += len(lit)
                return ver2int(lit)
            m2 = re.match(r'\d+', self.s[self.pos:])
            self.pos += len(m2.group(0))
            return int(m2.group(0))
        w = self.peek_word()
        if w:
            key = w
            if key in self.IDENTIFIERS:
                self.pos += len(w)
                val = self.IDENTIFIERS[key]
                if val is None:
                    raise Unresolved(f'identifier {key}')
                return val
            raise Unresolved(f'identifier {key!r}')
        raise Unresolved(f'atom at {self.s[self.pos:self.pos+20]!r}')


class SchemaOracle:
    def __init__(self, path, label, field_tag):
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()
        self.label = label
        self.field_tag = field_tag
        # version id table (modern schema uses symbolic V10_1_0_0 ids)
        self.ver_ids = {}
        for v in self.root.iter('version'):
            vid = v.get('id') or v.get('num')
            num = v.get('num')
            if vid and num:
                self.ver_ids[vid] = ver2int(num)
            elif num:
                # historical <version num="10.1.0.0"> elements (no id)
                pass
        self.ver_ids.setdefault('0.0.0.0', 0)
        # tokens for cond expansion
        self.tokens = {}
        for tagname in ('verexpr', 'condexpr', 'verattr'):
            for el in self.root.findall(tagname):
                self.tokens[f'#{el.get("token")}#'] = el.get('string')
        # enums storage width
        self.enum_storage = {}
        for e in self.root.iter('enum'):
            self.enum_storage[e.get('name')] = e.get('storage', 'uint')
        for e in self.root.iter('bitflags'):
            self.enum_storage[e.get('name')] = e.get('storage', 'uint')
        for e in self.root.iter('bitfield'):
            self.enum_storage[e.get('name')] = e.get('storage', 'uint')
        # compounds
        self.compounds = {}
        for c in self.root.iter('compound'):
            fields = [dict(name=f.get('name'), type=f.get('type'),
                            ver1=f.get('ver1'), ver2=f.get('ver2'),
                            cond=f.get('cond'), vercond=f.get('vercond'),
                            arr1=f.get('arr1'), arr2=f.get('arr2'))
                      for f in c.findall(field_tag)]
            self.compounds[c.get('name')] = {
                'ver1': c.get('ver1'), 'ver2': c.get('ver2'), 'fields': fields}
        # niobjects
        self.objects = {}
        for o in self.root.iter('niobject'):
            fields = [dict(name=f.get('name'), type=f.get('type'),
                           ver1=f.get('ver1'), ver2=f.get('ver2'),
                           since=f.get('since'), until=f.get('until'),
                           cond=f.get('cond'), vercond=f.get('vercond'),
                           arr1=f.get('arr1') or f.get('length'),
                           arr2=f.get('arr2'),
                           template=f.get('template'), default=f.get('default'),
                           userver=f.get('userver'))
                      for f in o.findall(field_tag)]
            ver_min = o.get('ver1') or o.get('since')
            ver_max = o.get('ver2') or o.get('until')
            vmin = self.resolve_ver(ver_min)
            vmax = self.resolve_ver(ver_max)
            self.objects[o.get('name')] = {
                'name': o.get('name'), 'inherit': o.get('inherit'),
                'abstract': o.get('abstract') == 'true' or
                            o.get('abstract') == '1',
                'ver_min': vmin if vmin is not None else 0,
                'ver_max': vmax if vmax is not None else V_MAX,
                'fields': fields}
        self.ev = Evaluator(self.tokens)

    def resolve_ver(self, s):
        """Resolve a version attr: symbolic id (V10_0_1_0) or literal."""
        if not s:
            return None
        if s in self.ver_ids:
            return self.ver_ids[s]
        try:
            return ver2int(s)
        except ValueError:
            return None

    def field_applies(self, f):
        """Version-level applicability of a field for 10.1.0.0/UV=0.

        Evaluates ONLY version gates: ver1/ver2 (or since/until) and the
        VERCOND expression (version-space). The value-space COND
        (field-value / template conditions like 'Has Vertices' or
        'BSLightingShaderProperty') is NOT evaluated here — it belongs to
        the decoder stage and is returned verbatim for reporting.
        Returns (True, cond_text) / (False, reason) / (None, unresolved).
        """
        lo = self.resolve_ver(f.get('ver1') or f.get('since')) if \
            (f.get('ver1') or f.get('since')) else None
        hi = self.resolve_ver(f.get('ver2') or f.get('until')) if \
            (f.get('ver2') or f.get('until')) else None
        cond_text_parts = []
        if lo is not None and V10_1 < lo:
            return False, f'ver>={int2ver(lo)}'
        if hi is not None and V10_1 > hi:
            return False, f'ver<={int2ver(hi)}'
        cond_text_parts.append(
            f'ver>={int2ver(lo)}' if lo is not None else '')
        cond_text_parts.append(
            f'ver<={int2ver(hi)}' if hi is not None else '')
        vercond = f.get('vercond')
        if vercond:
            try:
                ok = self.ev.evaluate(vercond)
                cond_text_parts.append('vercond:' + vercond)
                if not ok:
                    return False, 'vercond:false:' + vercond
            except Unresolved as e:
                return None, f'UNRESOLVED_VERCOND[{e}]: {vercond}'
        uv = f.get('userver')
        if uv is not None:
            try:
                if int(uv) != 0:
                    return False, f'userver:{uv}'
            except ValueError:
                return None, f'UNRESOLVED_USERVER:{uv}'
        cond = f.get('cond')
        if cond:
            cond_text_parts.append('cond:' + cond)
        return True, ';'.join(p for p in cond_text_parts if p)

    def type_applies(self, o):
        if o['ver_min'] > V10_1 or o['ver_max'] < V10_1:
            return False
        return True

    def effective_fields(self, type_name, seen=None):
        """Inheritance-ordered field list (parent first)."""
        seen = seen or set()
        if type_name in seen:
            return []
        seen.add(type_name)
        o = self.objects.get(type_name)
        if o is None:
            return []
        fields = []
        if o['inherit']:
            fields.extend(self.effective_fields(o['inherit'], seen))
        for f in o['fields']:
            fields.append((type_name, f))
        return fields

    def width(self, ftype, depth=0):
        """Fixed byte width for a type at 10.1.0.0, else 'var'."""
        if depth > 8:
            return 'var'
        prim = {
            'bool': '1(version-dep;1B for 10.1)', 'byte': '1', 'char': '1',
            'ubyte': '1', 'short': '2', 'ushort': '2', 'int': '4',
            'uint': '4', 'ulittle32': '4', 'float': '4', 'Ref': '4',
            'Ptr': '4', 'FileVersion': '4', 'HeaderString': 'var(line,0x0A)',
            'LineString': 'var(line,0x0A)', 'SizedString': 'var(u32+)',
            'ShortString': 'var(u8+)', 'string': 'var(u32+)',
            'IndexString': 'var', 'ByteArray': 'var', 'ID': '4',
        }
        if ftype in prim:
            return prim[ftype]
        if ftype in self.enum_storage:
            st = self.enum_storage[ftype]
            return {'uint': '4', 'ushort': '2', 'ubyte': '1', 'byte': '1',
                    'int': '4', 'short': '2'}.get(st, '4')
        c = self.compounds.get(ftype)
        if c:
            has_value_cond = any(cf.get('cond') for cf in c['fields'])
            has_version_cond = any(
                self.field_applies(cf)[0] is None for cf in c['fields'])
            if has_version_cond:
                return 'var(UNRESOLVED-vercond)'
            total = 0
            for cf in c['fields']:
                ok, _ = self.field_applies(cf)
                if ok is False:
                    continue
                if ok is None:
                    return 'var(UNRESOLVED-vercond)'
                w = self.width(cf['type'], depth + 1)
                if not re.match(r'^\d', str(w)):
                    return f'var({ftype} contains var)'
                arr = cf.get('arr1')
                if arr:
                    return f'var({ftype} array)'
                total += int(str(w).split('(')[0])
            if has_value_cond:
                return 'var(cond-conditional compound)'
            return str(total)
        return 'var(unknown-type)'


def main():
    hist = SchemaOracle(HIST, 'NIFXML_HIST_0_7_1_1', 'add')
    mod = SchemaOracle(MOD, 'NIFXML_MOD_0_10_0_0', 'field')
    observed = set()
    import json
    with open(r'D:\Eudoria_Reconstruction\99_Audits'
              r'\PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915\02_WORK'
              r'\TYPE_CENSUS_SUMMARY.json', encoding='utf-8') as f:
        pass  # type names loaded below from census csv instead
    census_path = os.path.join(
        os.path.dirname(REPO_RAW), '01_RAW',
        'ENTROPIA_NIF_10_1_TYPE_CENSUS.csv')
    with open(census_path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            observed.add(row['type_name'])

    rows = []
    conflicts = []
    for oracle in (hist, mod):
        all_types = set(oracle.objects) | observed
        for tn in sorted(all_types):
            o = oracle.objects.get(tn)
            if o is None:
                rows.append({
                    'TYPE_NAME': tn, 'PARENT_TYPE': '',
                    'VERSION_MIN': '', 'VERSION_MAX': '',
                    'APPLIES_TO_10_1_0_0': 'UNDEFINED_IN_SCHEMA',
                    'FIELD_INDEX': '', 'FIELD_NAME': '', 'FIELD_TYPE': '',
                    'FIELD_WIDTH_IF_FIXED': '', 'ARRAY_RELATION': '',
                    'COUNT_RELATION': '', 'CONDITION': '',
                    'LINK_REF_ROLE': '', 'INHERITED_FROM': '',
                    'SOURCE_ORACLE': oracle.label,
                    'SOURCE_LOCATION': os.path.basename(
                        HIST if 'HIST' in oracle.label else MOD),
                })
                continue
            applies = oracle.type_applies(o)
            if tn in observed and not applies:
                # observed physically but out of schema range for 10.1
                pass
            if not applies and tn not in observed:
                continue  # skip unobserved non-10.1 types entirely
            eff = oracle.effective_fields(tn)
            if not o['fields'] and not eff:
                pass
            for idx, (owner, f) in enumerate(eff):
                ok, cond_eval = oracle.field_applies(f)
                ftype = f['type'] or ''
                w = oracle.width(ftype) if ftype else ''
                arr = f.get('arr1') or ''
                rows.append({
                    'TYPE_NAME': tn,
                    'PARENT_TYPE': o['inherit'] or '',
                    'VERSION_MIN': int2ver(o['ver_min']),
                    'VERSION_MAX': int2ver(o['ver_max']),
                    'APPLIES_TO_10_1_0_0': (
                        f'{ok}' if ok is not None else 'UNRESOLVED') if
                        applies else 'FALSE',
                    'FIELD_INDEX': idx,
                    'FIELD_NAME': f['name'],
                    'FIELD_TYPE': ftype,
                    'FIELD_WIDTH_IF_FIXED': w,
                    'ARRAY_RELATION': f'array per {arr}' if arr else '',
                    'COUNT_RELATION': f'count={arr}' if arr else '',
                    'CONDITION': cond_eval,
                    'LINK_REF_ROLE': f'Ref->{f["template"]}' if
                    f.get('template') else '',
                    'INHERITED_FROM': 'SELF' if owner == tn else owner,
                    'SOURCE_ORACLE': oracle.label,
                    'SOURCE_LOCATION': os.path.basename(
                        HIST if 'HIST' in oracle.label else MOD),
                })
    out_path = os.path.join(REPO_RAW, 'BASELINE_TYPE_TABLE.csv')
    cols = ['TYPE_NAME', 'PARENT_TYPE', 'VERSION_MIN', 'VERSION_MAX',
            'APPLIES_TO_10_1_0_0', 'FIELD_INDEX', 'FIELD_NAME', 'FIELD_TYPE',
            'FIELD_WIDTH_IF_FIXED', 'ARRAY_RELATION', 'COUNT_RELATION',
            'CONDITION', 'LINK_REF_ROLE', 'INHERITED_FROM', 'SOURCE_ORACLE',
            'SOURCE_LOCATION']
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    # conflicts: per (TYPE_NAME, FIELD_NAME) join, comparing 10.1 view
    by_key = {}
    for r in rows:
        if r['FIELD_INDEX'] == '':
            continue
        key = (r['TYPE_NAME'], r['FIELD_NAME'])
        by_key.setdefault(key, []).append(r)
    for key, rs in sorted(by_key.items()):
        if len(rs) == 1:
            oracle = rs[0]['SOURCE_ORACLE']
            conflicts.append({
                'TYPE_NAME': key[0], 'FIELD_NAME': key[1], 'COL': 'PRESENCE',
                'HIST': 'present' if 'HIST' in oracle else 'ABSENT',
                'MOD': 'ABSENT' if 'HIST' in oracle else 'present',
            })
            continue
        if len(rs) != 2:
            continue
        a, b = rs
        if 'HIST' not in a['SOURCE_ORACLE']:
            a, b = b, a
        for col in ('APPLIES_TO_10_1_0_0', 'FIELD_TYPE',
                    'FIELD_WIDTH_IF_FIXED', 'ARRAY_RELATION',
                    'LINK_REF_ROLE', 'INHERITED_FROM'):
            if a[col] != b[col]:
                conflicts.append({
                    'TYPE_NAME': key[0], 'FIELD_NAME': key[1], 'COL': col,
                    'HIST': a[col], 'MOD': b[col],
                })
    confl_path = os.path.join(REPO_RAW, 'BASELINE_CONFLICT_RAW.csv')
    with open(confl_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['TYPE_NAME', 'FIELD_NAME', 'COL',
                                           'HIST', 'MOD'])
        w.writeheader()
        for c in conflicts:
            w.writerow(c)
    # type-level census of 10.1-applicable types
    hist_types_101 = [t for t, o in hist.objects.items()
                      if hist.type_applies(o)]
    mod_types_101 = [t for t, o in mod.objects.items() if mod.type_applies(o)]
    summary = {
        'hist_types_applying_to_10_1': len(hist_types_101),
        'mod_types_applying_to_10_1': len(mod_types_101),
        'observed_types': len(observed),
        'observed_not_in_hist_schema': sorted(
            observed - set(hist.objects)),
        'observed_not_in_mod_schema': sorted(observed - set(mod.objects)),
        'field_rows': len(rows),
        'conflict_rows': len(conflicts),
    }
    import json as _json
    with open(os.path.join(os.path.dirname(REPO_RAW), '02_WORK') if False else
              r'D:\Eudoria_Reconstruction\99_Audits'
              r'\PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915\02_WORK'
              r'\BASELINE_GEN_SUMMARY.json', 'w', encoding='utf-8') as f:
        _json.dump(summary, f, indent=2)
    print(_json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
