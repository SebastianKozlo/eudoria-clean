#!/usr/bin/env node
// verify_inputs.mjs — PA-2 live input identity gate (PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011)
// The EXPECTED size/SHA256 pins below are FROZEN CONSTANTS copied from the
// human-authorized INPUT_PINS.json (schema PE_FROZEN_INPUT_PINS_V1) whose own
// identity was verified in the fail-closed BOOT of this run. They are NEVER
// derived from the measured files. The measured values are computed separately
// and the verdict is a CONDITIONAL comparison — there is no literal PASS.
// A failed gate means BLOCKED_INPUT_IDENTITY: zero downstream analysis/correction/
// ref-reservation work may run (the runner enforces this with a spy).
// This module supersedes the historical PRE/gen_pre_identity.mjs literal-PASS
// generator (preserved READ_ONLY in docs/audits/PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011).
import fs from 'node:fs'; import path from 'node:path'; import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';

export const PIN_SCHEMA = 'PE_FROZEN_INPUT_PINS_V1';
export const EXPECTED_INPUT_PINS = [
  { pin: 'postaudit_REPORT_md', path: 'C:\\Users\\User\\Documents\\ChatGPT\\PE\\PE_PLACEMENT_PROBE_POSTAUDIT_938AA946_20261011\\REPORT.md', sizeBytes: 11361, sha256: '3D1A9EA1C4C358CF5730FAF61D7624F09A91F5DE5B9347303F3F186B819BD4C4' },
  { pin: 'postaudit_ADVERSARIAL_RESULTS_json', path: 'C:\\Users\\User\\Documents\\ChatGPT\\PE\\PE_PLACEMENT_PROBE_POSTAUDIT_938AA946_20261011\\ADVERSARIAL_RESULTS.json', sizeBytes: 54564, sha256: '1E4DB91477A63008B7001301B3DEEA91AA32897E07CE516F6CEC182DC32D1AA4' },
  { pin: 'postaudit_adversarial_checks_mjs', path: 'C:\\Users\\User\\Documents\\ChatGPT\\PE\\PE_PLACEMENT_PROBE_POSTAUDIT_938AA946_20261011\\adversarial_checks.mjs', sizeBytes: 7299, sha256: '1548C777988C40FA4E958D8A034BB490DAC8401C9D81A4D5679DB6C134A28196' },
  { pin: 'postaudit_INTEGRITY_RESULTS_json', path: 'C:\\Users\\User\\Documents\\ChatGPT\\PE\\PE_PLACEMENT_PROBE_POSTAUDIT_938AA946_20261011\\INTEGRITY_RESULTS.json', sizeBytes: 2638, sha256: '5D952E7C0339325E5070E80BDB23A8B762EF0E6CD601D562E434C90BC0BC69A0' },
  { pin: 'postaudit_REPLAY_RESULTS_json', path: 'C:\\Users\\User\\Documents\\ChatGPT\\PE\\PE_PLACEMENT_PROBE_POSTAUDIT_938AA946_20261011\\REPLAY_RESULTS.json', sizeBytes: 3494, sha256: '8CA27DE0315499B10856B3E53E261FC24632F1FBF25B81F3510C3ACA34A36669' },
  { pin: 'REVIEW_CHATGPT_CONTINUATION_md', path: 'C:\\Users\\User\\Documents\\ChatGPT\\PE\\PE_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_PROMPT_20261011\\REVIEW_CHATGPT_CONTINUATION.md', sizeBytes: 4799, sha256: 'D4887F4D68E529EE7D96DDAE5793C0B2B6DFC74481C33D693D3890703B6565ED' },
  { pin: 'ADDITIONAL_CLAIMS_RECHECK_json', path: 'C:\\Users\\User\\Documents\\ChatGPT\\PE\\PE_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_PROMPT_20261011\\ADDITIONAL_CLAIMS_RECHECK.json', sizeBytes: 5184, sha256: '45024942C2D9EE77CD89F6F278B99348764BAAD12E600EC856E58FCA204B1D1C' },
  { pin: 'recheck_additional_claims_mjs', path: 'C:\\Users\\User\\Documents\\ChatGPT\\PE\\PE_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_PROMPT_20261011\\recheck_additional_claims.mjs', sizeBytes: 5485, sha256: 'B575EB857128D7EE1E40578B6D0E7126F71A260D44BE51BD758B3DD9489E8736' },
  { pin: 'PE935_Placement_Probe_Kit_R1_zip', path: 'C:\\Users\\User\\Downloads\\PE935_Placement_Probe_Kit_R1.zip', sizeBytes: 21832, sha256: 'F03D6DA3E8D909014FE07F366095DBDA03FF2A54B2611BA23AFB140520A6F93B' },
  { pin: 'R2_CONTRACT_md', path: 'C:\\Users\\User\\Documents\\ChatGPT\\PE\\PE_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R2_PROMPT_20261011\\OPENCODE_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R2_COMPLETE.md', sizeBytes: 25139, sha256: '3F443D8680130BD24854F02232D29D8BD6EE6CA54B5BC9C3312087F617888EA3' },
  { pin: 'review_counterchecks_mjs', path: 'C:\\Users\\User\\Documents\\ChatGPT\\PE\\PE_PLACEMENT_PROBE_KIT_REVIEW_20261011\\review_counterchecks.mjs', sizeBytes: 9286, sha256: '3BF07497F33270791999235C78A70408105E02DF2BAD4C58EFDA38CB17823D35' },
  { pin: 'REVIEW_COUNTERCHECKS_json', path: 'C:\\Users\\User\\Documents\\ChatGPT\\PE\\PE_PLACEMENT_PROBE_KIT_REVIEW_20261011\\REVIEW_COUNTERCHECKS.json', sizeBytes: 3987, sha256: '9285636C4629F12787059948D71AE10CCEAB6C515356E5D55F6376705EC09944' },
  { pin: 'REVIEW_INPUT_IDENTITIES_json', path: 'C:\\Users\\User\\Documents\\ChatGPT\\PE\\PE_PLACEMENT_PROBE_KIT_REVIEW_20261011\\REVIEW_INPUT_IDENTITIES.json', sizeBytes: 1480, sha256: '1052F335D481A786C7F961822C97194FEA09098C4A6DFF97C591B5C3E56F8054' },
  { pin: 'review_REPORT_md', path: 'C:\\Users\\User\\Documents\\ChatGPT\\PE\\PE_PLACEMENT_PROBE_KIT_REVIEW_20261011\\REPORT.md', sizeBytes: 12241, sha256: '98BB64AF49DAFAECFC99D8C79AEAC59C512DE3E41E08D5782009E6BD8CEAA7FF' },
  { pin: 'contract_counterchecks_mjs', path: 'C:\\Users\\User\\Documents\\ChatGPT\\PE\\PE_PLACEMENT_PROBE_R2_CONTRACT_REVIEW_20261011\\contract_counterchecks.mjs', sizeBytes: 3521, sha256: '57CAF2C2450CCCEAFA6E8FE22C0574E69B18B1ED130AFABE154CC482F4C5DE4A' },
  { pin: 'CONTRACT_COUNTERCHECKS_json', path: 'C:\\Users\\User\\Documents\\ChatGPT\\PE\\PE_PLACEMENT_PROBE_R2_CONTRACT_REVIEW_20261011\\CONTRACT_COUNTERCHECKS.json', sizeBytes: 1054, sha256: '4076B5131DE4CF9507E9720B9B8CA8543FA889C26F6F2810C4633E81E60EE602' },
];

// ---- separate measurement (independent of any expected value) ----
export function measureInput(p) {
  const measured = { path: p, exists: false, sizeBytes: null, sha256: null, error: null };
  try {
    measured.exists = fs.existsSync(p);
    if (measured.exists) {
      const b = fs.readFileSync(p);
      measured.sizeBytes = b.length;
      measured.sha256 = createHash('sha256').update(b).digest('hex');
    }
  } catch (e) { measured.error = String(e?.message || e); }
  return measured;
}

// ---- conditional comparison of ONE pin (optionally against a private mutant copy) ----
export function verifyPin(pin, overridePath) {
  const target = overridePath ?? pin.path;
  const expected = { sizeBytes: pin.sizeBytes, sha256: pin.sha256 };
  const measured = measureInput(target);
  let compareResult, reason;
  if (!measured.exists) { compareResult = 'MISSING'; reason = 'input file not found'; }
  else if (measured.sizeBytes !== expected.sizeBytes) { compareResult = 'SIZE_MISMATCH'; reason = 'expected ' + expected.sizeBytes + ' B, measured ' + measured.sizeBytes + ' B'; }
  else if (measured.sha256.toUpperCase() !== expected.sha256.toUpperCase()) { compareResult = 'SHA_MISMATCH'; reason = 'size matches (' + expected.sizeBytes + ' B) but SHA256 differs'; }
  else { compareResult = 'MATCH'; reason = 'size and SHA256 both match the frozen pin'; }
  return {
    pin: pin.pin, path: target, expected, measured: { exists: measured.exists, sizeBytes: measured.sizeBytes, sha256: measured.sha256 },
    compareResult, reason, inputMatch: compareResult === 'MATCH', error: measured.error,
  };
}

// ---- the gate over ALL pins; the verdict is COMPUTED, never asserted ----
export function verifyAllInputs(pins = EXPECTED_INPUT_PINS, overrides = {}) {
  const results = pins.map(pin => verifyPin(pin, overrides[pin.pin]));
  const blocked = results.filter(r => !r.inputMatch);
  const verdict = blocked.length === 0 ? 'PASS' : 'BLOCKED_INPUT_IDENTITY';
  return {
    schema: PIN_SCHEMA, verdict,
    EFFECTIVE_GATE_RESULT: verdict === 'PASS' ? 'GATE_PASS__DOWNSTREAM_AUTHORIZED' : 'GATE_BLOCKED__DOWNSTREAM_REFUSED_ZERO_CALLS',
    total: results.length, matched: results.length - blocked.length, blockedCount: blocked.length,
    blockedPins: blocked.map(r => ({ pin: r.pin, compareResult: r.compareResult, reason: r.reason })),
    results,
  };
}

export function formatGateReport(gate) {
  const lines = ['=== PA-2 LIVE IDENTITY GATE ==='];
  for (const r of gate.results) {
    lines.push(`PIN ${r.pin}`);
    lines.push(`  EXPECTED size=${r.expected.sizeBytes} sha256=${r.expected.sha256}`);
    lines.push(`  MEASURED exists=${r.measured.exists} size=${r.measured.sizeBytes} sha256=${r.measured.sha256 ?? 'N/A'}`);
    lines.push(`  COMPARE_RESULT=${r.compareResult} (${r.reason})`);
  }
  lines.push(`EFFECTIVE_GATE_RESULT=${gate.EFFECTIVE_GATE_RESULT}`);
  lines.push(`VERDICT=${gate.verdict} matched=${gate.matched}/${gate.total} blocked=${gate.blockedCount}`);
  return lines.join('\n');
}

// ---- CLI: node verify_inputs.mjs [--overrides-json <file>] (exit 0 only on a real PASS) ----
export function main(argv) {
  const oi = argv.indexOf('--overrides-json');
  let overrides = {};
  if (oi >= 0) { overrides = JSON.parse(fs.readFileSync(path.resolve(argv[oi + 1]), 'utf8')); } // mutant testing only (private copies); expected pins stay frozen
  const gate = verifyAllInputs(EXPECTED_INPUT_PINS, overrides);
  process.stdout.write(formatGateReport(gate) + '\n');
  if (gate.verdict !== 'PASS') { process.stderr.write('BLOCKED_INPUT_IDENTITY: ' + gate.blockedPins.map(b => b.pin + ':' + b.compareResult).join(', ') + '\n'); process.exitCode = 3; }
  return gate;
}
if (process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) { main(process.argv.slice(2)); }
