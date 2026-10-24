#!/usr/bin/env python3
"""
je1_render_runner.py — JOB PE2003R3-JE1 (Wave E3)
RUN: PE2003_SCENE_BOOTSTRAP_MODEL_INSTANCE_DISCOVERY_R1_20261024

Renders the two je1 preview pages with local headless Chromium (Playwright's
chromium-1234 binary, launched directly — the MCP browser bridge was down and
no playwright package is installed; no new packages were installed).
Per (model, angle): 1 screenshot run + 1 --dump-dom run, each bounded by its own
subprocess timeout; stats JSON is parsed out of the dumped DOM (#statsjson).
"""
import subprocess, json, re, os, sys, hashlib

RUN_ID = "PE2003_SCENE_BOOTSTRAP_MODEL_INSTANCE_DISCOVERY_R1_20261024"
WORK_ROOT = r"D:\Eudoria_Reconstruction\PE2003\10_Campaigns\PE2003_SCENE_BOOTSTRAP_MODEL_INSTANCE_DISCOVERY_R1_20261024"
CHROME = r"C:\Users\User\AppData\Local\ms-playwright\chromium-1234\chrome-win64\chrome.exe"
BASE = "http://127.0.0.1:8765/preview/"
FRAMES = [("296445", 1), ("296445", 2), ("218757", 1), ("218757", 2)]
TIMEOUT = 90  # seconds per chrome invocation


def sha256_hex(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest().upper()


def run_chrome(args):
    try:
        p = subprocess.run([CHROME] + args, capture_output=True, timeout=TIMEOUT)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return -1, b'', b'TIMEOUT'


def main():
    out_dir = os.path.join(WORK_ROOT, 'preview')
    stats_dir = os.path.join(WORK_ROOT, 'data', 'je1')
    results = {}
    ok_all = True
    for mid, angle in FRAMES:
        url = "%spreview_%s.html?angle=%d" % (BASE, mid, angle)
        png = os.path.join(out_dir, "%s_frame_angle%d.png" % (mid, angle))
        rc1, _, err1 = run_chrome([
            '--headless=new', '--no-sandbox', '--disable-gpu-sandbox',
            '--enable-unsafe-swiftshader', '--hide-scrollbars',
            '--window-size=1280,720', '--screenshot=%s' % png, url])
        rc2, dom, err2 = run_chrome([
            '--headless=new', '--no-sandbox', '--disable-gpu-sandbox',
            '--enable-unsafe-swiftshader', '--hide-scrollbars',
            '--window-size=1280,720', '--virtual-time-budget=8000', '--dump-dom', url])
        m = re.search(rb'<pre id="statsjson"[^>]*>\s*(\{.*?\})\s*</pre>', dom, re.S)
        stats = None
        if m:
            try:
                stats = json.loads(m.group(1).decode('utf-8'))
            except Exception as e:
                stats = {'parse_error': str(e)}
        else:
            i = dom.find(b'statsjson')
            stats = {'statsjson_absent': True,
                     'dom_len': len(dom),
                     'dom_around': dom[max(0, i - 100):i + 400].decode('utf-8', 'replace') if i >= 0 else dom[-500:].decode('utf-8', 'replace')}
        entry = {'url': url, 'screenshot': png,
                 'screenshot_exit': rc1, 'dump_exit': rc2,
                 'screenshot_exists': os.path.exists(png),
                 'screenshot_sha256': sha256_hex(png) if os.path.exists(png) else None,
                 'stats': stats}
        good = (rc1 == 0 and rc2 == 0 and os.path.exists(png) and stats
                and stats.get('ready') and stats.get('pixel_coverage', 0) > 0.5
                and stats.get('frame_triangles') == stats.get('parse_total_triangles')
                and stats.get('geometry_triangle_sum') == stats.get('parse_total_triangles')
                and stats.get('geometry_vertex_sum') == stats.get('parse_total_vertices')
                and stats.get('draw_calls') == stats.get('meshes_rendered')
                and stats.get('pipeline_vertices_declared') == stats.get('parse_total_vertices'))
        entry['frame_ok'] = bool(good)
        ok_all = ok_all and bool(good)
        results['%s_angle%d' % (mid, angle)] = entry
        print(mid, 'angle', angle, 'ok=', entry['frame_ok'],
              'cov=', (stats or {}).get('pixel_coverage'),
              'tris=', (stats or {}).get('frame_triangles'))
        if err1 or err2:
            entry['chrome_stderr_head'] = (err1 + err2)[:300].decode('utf-8', 'replace')
    spath = os.path.join(stats_dir, 'render_stats.json')
    with open(spath, 'w', encoding='utf-8') as f:
        json.dump({'run': RUN_ID, 'chrome': CHROME, 'label': 'SYNTHETIC_PREVIEW',
                   'frames': results}, f, indent=1)
    print('RENDER', 'OK' if ok_all else 'FAILED', '->', spath)
    sys.exit(0 if ok_all else 5)


if __name__ == '__main__':
    main()
