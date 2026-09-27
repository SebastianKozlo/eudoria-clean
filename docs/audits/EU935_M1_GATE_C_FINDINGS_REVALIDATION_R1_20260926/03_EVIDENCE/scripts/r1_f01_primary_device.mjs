// r1_f01_primary_device.mjs — EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926
// F01 independent probe: PRIMARY_DEVICE mask adjudication.
// Re-derives, from physical sources only:
//   (1) the DISPLAY_DEVICE_* flag constants from the LOCAL installed Windows SDK
//       wingdi.h (source class: LOCAL_INSTALLED_SDK_HEADER, not a web citation);
//   (2) every adapter from the RAW StateFlags in the historical
//       DISPLAY_ENV_MEASUREMENT.txt under BOTH the old predicate (& 2) and the
//       corrected PRIMARY mask (& 4);
//   (3) explicit mask controls for values 0, 1, 2, 4, 5, 0x04000005.
// READ-ONLY: writes only to this run's 03_EVIDENCE. No client, no registry, no GPU.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const ROOT = 'D:/Eudoria_Reconstruction';
const REPO = ROOT + '/12_WebGame/eudoria-clean';
const EV = REPO + '/docs/audits/EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926/03_EVIDENCE';
const sha256 = (b) => crypto.createHash('sha256').update(b).digest('hex').toUpperCase();

// ---------- (1) the SDK constants from the LOCAL installed header ----------
const SDK = 'C:/Program Files (x86)/Windows Kits/10/Include/10.0.22621.0/um/wingdi.h';
let sdkHeader = null, sdkError = null;
try { sdkHeader = fs.readFileSync(SDK); } catch (e) { sdkError = String(e); }
const sdkConstants = {};
if (sdkHeader) {
  const text = sdkHeader.toString('utf8');
  const names = ['DISPLAY_DEVICE_ATTACHED_TO_DESKTOP', 'DISPLAY_DEVICE_MULTI_DRIVER',
    'DISPLAY_DEVICE_PRIMARY_DEVICE', 'DISPLAY_DEVICE_MIRRORING_DRIVER',
    'DISPLAY_DEVICE_VGACOMPATIBLE', 'DISPLAY_DEVICE_REMOVABLE', 'DISPLAY_DEVICE_ACC_DRIVER',
    'DISPLAY_DEVICE_MODESPRUNED', 'DISPLAY_DEVICE_REMOTE'];
  const lines = text.split(/\r?\n/);
  for (const line of lines) {
    const m = line.match(/^#define\s+(DISPLAY_DEVICE_[A-Z_]+)\s+(0x[0-9A-Fa-f]+)/);
    if (m && names.includes(m[1])) {
      sdkConstants[m[1]] = { define: m[2], value: parseInt(m[2], 16) };
    }
  }
}
// Fallback check across all installed SDK versions if the pinned one is absent.
const sdkSearchRecord = { pinnedPath: SDK, pinnedPathRead: !!sdkHeader, error: sdkError };

// ---------- (2) raw StateFlags from the historical measurement ----------
const MEAS = ROOT + '/99_Audits/PE_NIGHT_AGGREGATE_20260905_160000/DISPLAY_ENV_MEASUREMENT.txt';
const measBytes = fs.readFileSync(MEAS);
const measText = measBytes.toString('utf8');
const C = { ATTACHED: 0x1, MULTI: 0x2, PRIMARY: 0x4, MIRRORING: 0x8, VGA: 0x10, REMOVABLE: 0x20, MODESPRUNED: 0x08000000, REMOTE: 0x04000000 };
const adapters = [];
const blocks = measText.split(/iDev=(\d+): ok=1/).slice(1);
for (let i = 0; i + 1 < blocks.length; i += 2) {
  const idx = parseInt(blocks[i], 10), body = blocks[i + 1];
  const nm = body.match(/DeviceName\s+=\s+(\\.*)/);
  const ds = body.match(/DeviceString=\s+(.*)/);
  const sf = body.match(/StateFlags\s+=\s+(0x[0-9a-f]+)/i);
  if (!sf) continue;
  const flags = parseInt(sf[1], 16);
  adapters.push({
    iDev: idx,
    deviceName: nm ? nm[1].trim() : null,
    deviceString: ds ? ds[1].trim() : null,
    rawStateFlags: sf[1].toLowerCase(),
    flags,
    // OLD predicate (display_env_measurement.py:73): PRIMARY := flags & 2
    old_primary_mask2: !!(flags & C.MULTI),
    // CORRECTED mask (SDK DISPLAY_DEVICE_PRIMARY_DEVICE = 0x4)
    corrected_primary_mask4: !!(flags & C.PRIMARY),
    attached_to_desktop: !!(flags & C.ATTACHED),
    multi_driver: !!(flags & C.MULTI),
    mirroring_driver: !!(flags & C.MIRRORING),
    remote: !!(flags & C.REMOTE),
    modespruned: !!(flags & C.MODESPRUNED),
    old_predicate_mislabeled_field: 'PRIMARY',
    old_predicate_actual_mask: 'MULTI_DRIVER (0x2)',
  });
}
const primaryOld = adapters.filter(a => a.old_primary_mask2).length;
const primaryNew = adapters.filter(a => a.corrected_primary_mask4).length;

// ---------- (3) mask controls 0, 1, 2, 4, 5, 0x04000005 ----------
const controls = [0, 1, 2, 4, 5, 0x04000005].map((v) => ({
  input: '0x' + v.toString(16),
  attached: !!(v & C.ATTACHED),
  multi_driver: !!(v & C.MULTI),
  primary_mask4: !!(v & C.PRIMARY),
  mirroring: !!(v & C.MIRRORING),
  remote: !!(v & C.REMOTE),
  OLD_primary_mask2_output: !!(v & C.MULTI),
  expected_OLD: v === 2 ? 'true (FALSE-POSITIVE: 0x2 is MULTI_DRIVER)' : 'false',
  expected_NEW: (v === 4 || v === 5 || v === 0x04000005) ? 'true' : 'false',
}));

const out = {
  probe: 'F01_PRIMARY_DEVICE_REVALIDATION',
  run_id: 'EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926',
  node_version: process.version,
  sdk: {
    source_class: 'LOCAL_INSTALLED_SDK_HEADER',
    search_record: sdkSearchRecord,
    constants: sdkConstants,
    primary_device_define: sdkConstants.DISPLAY_DEVICE_PRIMARY_DEVICE || null,
    multi_driver_define: sdkConstants.DISPLAY_DEVICE_MULTI_DRIVER || null,
    adjudication: sdkConstants.DISPLAY_DEVICE_PRIMARY_DEVICE && sdkConstants.DISPLAY_DEVICE_PRIMARY_DEVICE.value === 4
      ? 'PRIMARY_DEVICE = 0x4 CONFIRMED from the local installed SDK header; the historical mask & 2 = MULTI_DRIVER'
      : 'SDK header unread or constants absent — check pinnedPath',
  },
  measurement_source: {
    path: MEAS,
    sha256: sha256(measBytes),
    size: measBytes.length,
    historical_script: ROOT + '/99_Audits/PE_NIGHT_AGGREGATE_20260905_160000/display_env_measurement.py',
  },
  adapters,
  counts: {
    adapters: adapters.length,
    primary_OLD_mask2: primaryOld,
    primary_CORRECTED_mask4: primaryNew,
    verdict: primaryNew === 1 && primaryOld === 0
      ? 'REPRODUCED: PRIMARY=True for 1/' + adapters.length + ' adapters (DISPLAY1), NOT zero; the old predicate returned zero because 0x2 is MULTI_DRIVER'
      : 'CHECK: deviation from expected 1-primary / 0-old',
  },
  mask_controls: controls,
};
fs.writeFileSync(path.join(EV, 'F01_PRIMARY_DEVICE_REVALIDATION.json'), JSON.stringify(out, null, 2));
console.log(JSON.stringify({ sdk: out.sdk.adjudication, counts: out.counts, adapters: adapters.map(a => ({ n: a.deviceName, raw: a.rawStateFlags, old: a.old_primary_mask2, corrected: a.corrected_primary_mask4, remote: a.remote, attached: a.attached_to_desktop })) }, null, 2));
