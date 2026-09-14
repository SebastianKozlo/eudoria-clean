"""qc_gb6_perfile.py — per-file comparison: fresh hashes vs executor's GB6 after-census."""
import hashlib
import json
import os

PKG = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913"
PACKAGES = {
    'RUN1_TEMPLATE_CONSUMER_TRACE': r"D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912",
    'RUN2_EXTERNAL_SOURCES_MATRIX': r"D:\Eudoria_Reconstruction\99_Audits\PE_935_EXTERNAL_SOURCES_MATRIX_R1_20260913",
    'RUN3_STATIC_INSTANCE_TRACE': r"D:\Eudoria_Reconstruction\99_Audits\PE_935_STATIC_INSTANCE_TRACE_R1_20260913",
    'RUN4_PLACEMENT_SOURCE_TRACE': r"D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913",
    'ROUND_CLOSURE': r"D:\Eudoria_Reconstruction\99_Audits\PE_935_STATIC_PLACEMENT_ROUND1_20260913",
    'JOIN_ERRATA_R2': r"D:\Eudoria_Reconstruction\99_Audits\PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913",
    'DESKTOP_AUDIT': r"D:\Eudoria_Reconstruction\99_Audits\PE_935_STATIC_PLACEMENT_DESKTOP_AUDIT_R1_20260913",
    'PKG_A_RECEIVER_PROVENANCE': r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913",
}


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest().upper()


def main():
    ex = json.load(open(os.path.join(PKG, '01_RAW', 'GB6_IMMUTABLE_CENSUS_after.json'), encoding='utf-8'))
    res = {}
    all_ok = True
    for name, root in sorted(PACKAGES.items()):
        exf = {f['path'].replace('\\', '/'): (f['size'], f['sha256']) for f in ex['packages'][name]['files']}
        cur = {}
        for dp, dn, fn in os.walk(root):
            for f in fn:
                p = os.path.join(dp, f)
                rel = os.path.relpath(p, root).replace('\\', '/')
                cur[rel] = (os.path.getsize(p), sha(p))
        set_ok = set(exf) == set(cur)
        content_ok = set_ok and all(exf[k] == cur[k] for k in exf)
        res[name] = {'files': len(cur), 'set_equal': set_ok, 'content_equal': content_ok}
        print('%-30s files=%d set_equal=%s content_equal=%s' % (name, len(cur), set_ok, content_ok))
        if not content_ok:
            missing = set(exf) - set(cur)
            extra = set(cur) - set(exf)
            changed = [k for k in exf if k in cur and exf[k] != cur[k]][:20]
            print('   missing=%d extra=%d changed=%d e.g. %s' % (len(missing), len(extra), len(changed), changed[:5]))
            all_ok = False
    print('VERDICT:', 'GB6_PERFILE_IDENTICAL' if all_ok else 'GB6_PERFILE_MISMATCH')
    with open(os.path.join(PKG, '00_CONTROL', 'qc_probe', 'QC_GB6_PERFILE.json'), 'w', encoding='utf-8') as f:
        json.dump(res, f, indent=1)


if __name__ == '__main__':
    main()
