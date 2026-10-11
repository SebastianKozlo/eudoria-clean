// validate_receipt.mjs — PA2-RC1/P2 shared receipt qualification validator
// (RUN_ID PE_935_PLACEMENT_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_20261011, contract §4).
//
// WHY THIS EXISTS: the predecessor full POST (BASE 28e91eb,
// docs/audits/PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011/POST/run_post.mjs
// line ~410) accepted the PA2 live receipt on only
//   gate.verdict === 'PASS' && gate.matched === 16 && mode === 'REAL_SEQUENCE'
// and never compared the receipt's perPin MEASURED bytes against the frozen
// trusted pins nor the receipt's moduleIdentity SHAs against the trusted source
// files — an externally measured false-PASS (Desktop post-audit M1/M2, both
// QUALIFICATION_PASS/exit0). This module implements the corrected acceptance
// condition: every receipt claim is re-derived from trusted sources and the
// live evidence, and any contradiction is a controlled PA2 failure.
//
// HISTORICAL RECEIPT COMPATIBILITY (contract §4.1): the archived CLEAN receipt
// (PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011 / PA2_LIVE_IDENTITY_GATE /
// REAL_SEQUENCE, contextBase 28e91eb) has NO top-level schema field and NO perPin
// inputMatch field; its per-pin shape is {pin, compareResult, EXPECTED{sizeBytes,
// sha256}, MEASURED{exists, sizeBytes, sha256}}. This exact legacy shape is
// validated through the explicit trusted profile below: absent fields are never
// required; present fields must be strictly typed (no string->integer, no
// truthy->boolean coercion). SHA comparisons normalize hex case only — never
// bytes. The CLEAN whole-file hash is NOT a validator rule: mutants must be
// refused by the corrected semantics, not by hash-listing.
//
// DIAGNOSTIC DESIGN: the validator computes every quantity that is computable
// (live remeasurement, profile, module identity, per-pin/summary consistency)
// and collects ALL refusal reasons before failing once — a refusal preserves the
// full diagnostics of WHICH checks failed and which still held (predicate 7,
// fail-closed with preserved diagnostics). Any exception is a controlled failure.
//
// This is a context-specific requalification of archived evidence — NOT proof of
// historical execution, authorship, or a signature. No signing service and no
// universal receipt framework is implemented or claimed.
import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { pathToFileURL } from 'node:url';

export const QUALIFICATION_SCHEMA = 'PE_PA2_RECEIPT_QUALIFICATION_V1';

// ---- trusted sources (contract §1, frozen constants; NEVER derived from a receipt) ----
export const TRUSTED_GATE_MODULE = {
  path: 'tools/placement_probe/verify_inputs.mjs',
  sha256: '568CE3F29F68EBDDF5AA40E7550278717CD6E9F868A239FB132AE2C623A2B43D',
};
export const TRUSTED_RUNNER = {
  path: 'docs/audits/PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011/PRE/verify_inputs_runner.mjs',
  sha256: 'A4733B0DCF17C669E564232FE3E6663DE08B0093E66F30A9D5F3B502BF6C2FDC',
};
// exact historical context the archived receipt must carry (contract §4.1)
export const RECEIPT_PROFILE = {
  runId: 'PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011',
  stage: 'PA2_LIVE_IDENTITY_GATE',
  mode: 'REAL_SEQUENCE',
  contextBase: '28e91eb67511a3022a911ab6d4e02e68119b1f68',
};
export const EXPECTED_PIN_COUNT = 16;
const HEX64 = /^[0-9a-fA-F]{64}$/;
const COMPARE_RESULTS = new Set(['MATCH', 'SIZE_MISMATCH', 'SHA_MISMATCH', 'MISSING']);

const sha = b => createHash('sha256').update(b).digest('hex');
const shaF = p => sha(fs.readFileSync(p));
const normHex = s => (typeof s === 'string' ? s.toUpperCase() : s);
const normPath = s => (typeof s === 'string' ? s.replaceAll('\\', '/') : s);

// ---- predicate 1: verify the trusted BASE gate-module + predecessor-runner SHA
// BEFORE loading the expected pins; freeze the 16 pins from that trusted source. ----
export function loadTrusted(worktreeRoot) {
  const reasons = [];
  const gatePath = path.join(worktreeRoot, ...TRUSTED_GATE_MODULE.path.split('/'));
  const runnerPath = path.join(worktreeRoot, ...TRUSTED_RUNNER.path.split('/'));
  const result = { ok: false, worktreeRoot, moduleShas: {}, schema: null, pins: [], pinNames: [] };
  for (const [label, p, trusted] of [['gateModule', gatePath, TRUSTED_GATE_MODULE], ['runner', runnerPath, TRUSTED_RUNNER]]) {
    if (!fs.existsSync(p)) { reasons.push('trusted ' + label + ' file missing: ' + trusted.path); continue; }
    const measured = shaF(p);
    result.moduleShas[label] = measured;
    if (normHex(measured) !== normHex(trusted.sha256)) reasons.push('trusted ' + label + ' SHA mismatch: measured ' + measured + ' != frozen ' + trusted.sha256);
  }
  if (reasons.length) { result.reasons = reasons; return result; }
  // gate module bytes verified -> import it and freeze the expected pins from it
  const mod = import(pathToFileURL(gatePath).href); // promise; resolved below
  return mod.then(m => {
    const pins = m.EXPECTED_INPUT_PINS;
    if (!Array.isArray(pins) || pins.length !== EXPECTED_PIN_COUNT) { result.reasons = ['trusted gate module does not carry exactly ' + EXPECTED_PIN_COUNT + ' pins (got ' + (Array.isArray(pins) ? pins.length : typeof pins) + ')']; return result; }
    const names = pins.map(p => p?.pin);
    if (new Set(names).size !== EXPECTED_PIN_COUNT) { result.reasons = ['trusted gate module pin names are not distinct']; return result; }
    result.ok = true; result.schema = m.PIN_SCHEMA; result.pins = pins; result.pinNames = names;
    result.module = m; // verified gate module (verifyAllInputs for live remeasurement)
    return result;
  }).catch(e => { result.reasons = ['trusted gate module import failed (fail-closed): ' + String(e?.message || e)]; return result; });
}

// ---- strict legacy-shape profile (contract §4.1/§4.2 predicate 2: no coercion) ----
function profileViolations(receipt) {
  const v = [];
  if (typeof receipt !== 'object' || receipt === null || Array.isArray(receipt)) { v.push('receipt root is not a JSON object'); return v; }
  if (typeof receipt.runId !== 'string') v.push('runId is not a string');
  if (typeof receipt.stage !== 'string') v.push('stage is not a string');
  if (typeof receipt.mode !== 'string') v.push('mode is not a string');
  if (!Array.isArray(receipt.perPin)) v.push('perPin is not an array');
  const g = receipt.gate;
  if (typeof g !== 'object' || g === null || Array.isArray(g)) v.push('gate is not an object');
  else {
    if (typeof g.verdict !== 'string') v.push('gate.verdict is not a string');
    if (typeof g.EFFECTIVE_GATE_RESULT !== 'string') v.push('gate.EFFECTIVE_GATE_RESULT is not a string');
    for (const k of ['total', 'matched', 'blockedCount']) if (!Number.isSafeInteger(g[k])) v.push('gate.' + k + ' is not a safe integer (no coercion)');
    if (!Array.isArray(g.blockedPins)) v.push('gate.blockedPins is not an array');
  }
  const mi = receipt.moduleIdentity;
  if (typeof mi !== 'object' || mi === null || Array.isArray(mi)) v.push('moduleIdentity is not an object');
  else for (const k of ['gateModule', 'runner']) {
    const m = mi[k];
    if (typeof m !== 'object' || m === null || Array.isArray(m)) v.push('moduleIdentity.' + k + ' is not an object');
    else {
      if (typeof m.path !== 'string') v.push('moduleIdentity.' + k + '.path is not a string');
      if (typeof m.sha256 !== 'string' || !HEX64.test(m.sha256)) v.push('moduleIdentity.' + k + '.sha256 is not a 64-hex string');
    }
  }
  if (Array.isArray(receipt.perPin)) {
    receipt.perPin.forEach((e, i) => {
      const tag = 'perPin[' + i + ']';
      if (typeof e !== 'object' || e === null || Array.isArray(e)) { v.push(tag + ' is not an object'); return; }
      if (typeof e.pin !== 'string') v.push(tag + '.pin is not a string');
      if (typeof e.compareResult !== 'string' || !COMPARE_RESULTS.has(e.compareResult)) v.push(tag + '.compareResult is not one of ' + [...COMPARE_RESULTS].join('|'));
      for (const [fld] of [['EXPECTED'], ['MEASURED']]) {
        const o = e[fld];
        if (typeof o !== 'object' || o === null || Array.isArray(o)) { v.push(tag + '.' + fld + ' is not an object'); continue; }
        if (fld === 'EXPECTED') {
          if (!Number.isSafeInteger(o.sizeBytes)) v.push(tag + '.EXPECTED.sizeBytes is not a safe integer');
          if (typeof o.sha256 !== 'string' || !HEX64.test(o.sha256)) v.push(tag + '.EXPECTED.sha256 is not a 64-hex string');
        } else {
          if (typeof o.exists !== 'boolean') v.push(tag + '.MEASURED.exists is not a strict boolean');
          if (o.exists === true) {
            if (!Number.isSafeInteger(o.sizeBytes)) v.push(tag + '.MEASURED.sizeBytes is not a safe integer while exists=true');
            if (typeof o.sha256 !== 'string' || !HEX64.test(o.sha256)) v.push(tag + '.MEASURED.sha256 is not a 64-hex string while exists=true');
          } else {
            if (o.sizeBytes !== null) v.push(tag + '.MEASURED.sizeBytes is not null while exists=false');
            if (o.sha256 !== null) v.push(tag + '.MEASURED.sha256 is not null while exists=false');
          }
        }
      }
      // NO legacy inputMatch field is required (absent in the historical shape);
      // if a receipt carries one anyway, it must be a boolean consistent with the
      // independently derived match (validated in consistency, not trusted here).
      if ('inputMatch' in e && typeof e.inputMatch !== 'boolean') v.push(tag + '.inputMatch is present but not a boolean');
    });
  }
  return v;
}

// ---- the corrected qualification (contract §4.2 predicates 1-7; fail-closed with
// preserved diagnostics: every computable quantity is computed, ALL refusal
// reasons are collected, the verdict fails once on any contradiction) ----
// Returns four separate quantities:
//   INPUT_BYTES_REMEASURED, RECEIPT_INTERNAL_CONSISTENCY, MODULE_CODE_IDENTITY, RECEIPT_QUALIFICATION
export async function qualifyReceipt({ receiptPath, trusted }) {
  const quantities = {};
  const allReasons = [];
  try {
    // predicate 1: trusted sources must verify BEFORE any pin use
    if (!trusted || trusted.ok !== true) {
      return {
        RECEIPT_PROFILE: { ok: false, reasons: ['no verified trusted source supplied'] },
        RECEIPT_QUALIFICATION: { verdict: 'FAIL', refusalReason: 'trusted source verification failed before qualification: ' + ((trusted?.reasons ?? ['no trusted source supplied']).join('; ')), reasons: ['trusted source verification failed before qualification: ' + ((trusted?.reasons ?? ['no trusted source supplied']).join('; '))], receiptIdentity: null, contextBase: RECEIPT_PROFILE.contextBase },
      };
    }
    const pins = trusted.pins;
    const byName = new Map(pins.map(p => [p.pin, p]));
    // predicate 6 FIRST: the live remeasurement is independent of the receipt — always computable
    const live = trusted.module.verifyAllInputs(pins, {});
    quantities.INPUT_BYTES_REMEASURED = {
      performed: true,
      method: 'verifyAllInputs(EXPECTED_INPUT_PINS, {}) — the SHA-verified unchanged gate module, live remeasurement of the 16 pinned evidence files',
      verdict: live.verdict, total: live.total, matched: live.matched, blockedCount: live.blockedCount,
      blockedPins: live.blockedPins,
      perPin: live.results.map(r => ({ pin: r.pin, exists: r.measured.exists, sizeBytes: r.measured.sizeBytes, sha256: r.measured.sha256, compareResult: r.compareResult })),
      required: 'PASS', pass: live.verdict === 'PASS' && live.matched === EXPECTED_PIN_COUNT && live.blockedCount === 0,
      timeUtc: new Date().toISOString(), moduleShas: trusted.moduleShas,
      whyNonCircular: 'the current physical input bytes are re-measured now, independent of the archived receipt; hash consistency is NOT proof of historical execution or authorship',
      note: 'M1/M2-style receipt failures remain failures even when the current files are clean — this quantity cannot repair a contradictory receipt',
    };
    const liveReasons = quantities.INPUT_BYTES_REMEASURED.pass ? [] : ['live input identity remeasurement refused: ' + live.blockedPins.map(b => b.pin + ':' + b.compareResult).join(', ')];
    allReasons.push(...liveReasons);
    // receipt identity + controlled parse (predicate 7: no exception-to-PASS)
    if (typeof receiptPath !== 'string' || !fs.existsSync(receiptPath)) {
      quantities.RECEIPT_PROFILE = { ok: false, reasons: ['receipt file missing: ' + String(receiptPath)] };
      quantities.RECEIPT_INTERNAL_CONSISTENCY = { ok: false, performed: false, reasons: ['receipt not parseable — consistency not computable'] };
      quantities.MODULE_CODE_IDENTITY = { ok: false, performed: false, reasons: ['receipt not parseable — module identity not verifiable'] };
      quantities.RECEIPT_QUALIFICATION = { verdict: 'FAIL', refusalReason: 'receipt file missing: ' + String(receiptPath), reasons: ['receipt file missing: ' + String(receiptPath)], receiptIdentity: null, contextBase: RECEIPT_PROFILE.contextBase };
      return quantities;
    }
    const receiptBytes = fs.readFileSync(receiptPath);
    const receiptIdentity = { sizeBytes: receiptBytes.length, sha256: sha(receiptBytes) };
    let receipt; let parseError = null;
    try { receipt = JSON.parse(receiptBytes.toString('utf8')); } catch (e) { parseError = String(e?.message || e); }
    if (parseError !== null) {
      quantities.RECEIPT_PROFILE = { ok: false, reasons: ['receipt is not valid JSON (unreadable/truncated): ' + parseError] };
      quantities.RECEIPT_INTERNAL_CONSISTENCY = { ok: false, performed: false, reasons: ['receipt not parseable — consistency not computable'] };
      quantities.MODULE_CODE_IDENTITY = { ok: false, performed: false, reasons: ['receipt not parseable — module identity not verifiable'] };
      quantities.RECEIPT_QUALIFICATION = { verdict: 'FAIL', refusalReason: 'receipt is not valid JSON (unreadable/truncated): ' + parseError, reasons: [...allReasons, 'receipt is not valid JSON (unreadable/truncated): ' + parseError], receiptIdentity, contextBase: RECEIPT_PROFILE.contextBase };
      return quantities;
    }
    // predicate 2: exact historical profile, strict types, 16 distinct pin names
    const profileViolationsFound = profileViolations(receipt);
    const claimedNames = Array.isArray(receipt.perPin) ? receipt.perPin.map(e => e?.pin) : [];
    const nameIssues = [];
    if (!Array.isArray(receipt.perPin) || receipt.perPin.length !== EXPECTED_PIN_COUNT) nameIssues.push('perPin count is ' + (Array.isArray(receipt.perPin) ? receipt.perPin.length : 'not-an-array') + ' != expected ' + EXPECTED_PIN_COUNT);
    const dup = claimedNames.filter((n, i) => claimedNames.indexOf(n) !== i);
    if (dup.length) nameIssues.push('duplicate perPin entries for pin(s): ' + [...new Set(dup)].join(','));
    const missingPins = trusted.pinNames.filter(n => !claimedNames.includes(n));
    const extraPins = claimedNames.filter(n => !byName.has(n));
    if (missingPins.length) nameIssues.push('missing expected pin(s): ' + missingPins.join(','));
    if (extraPins.length) nameIssues.push('unexpected pin(s): ' + [...new Set(extraPins)].join(','));
    const exactContext = receipt.runId === RECEIPT_PROFILE.runId && receipt.stage === RECEIPT_PROFILE.stage && receipt.mode === RECEIPT_PROFILE.mode;
    const contextIssues = exactContext ? [] : ['runId/stage/mode do not match the frozen historical context (expected ' + RECEIPT_PROFILE.runId + ' / ' + RECEIPT_PROFILE.stage + ' / ' + RECEIPT_PROFILE.mode + ')'];
    quantities.RECEIPT_PROFILE = {
      schema: QUALIFICATION_SCHEMA, legacyFormatProfile: 'historical PE_PA2 receipt (no schema field, no perPin inputMatch — both optional-absent)',
      ok: profileViolationsFound.length === 0 && nameIssues.length === 0 && exactContext,
      context: { runId: receipt.runId, stage: receipt.stage, mode: receipt.mode, expected: { ...RECEIPT_PROFILE } },
      contextOk: exactContext, strictTypeViolations: profileViolationsFound, pinNameIssues: nameIssues,
      note: 'exact historical runId/stage/mode validated against the frozen predecessor context; no age limit imposed; timeUtc not treated as proof of anything',
    };
    const profileReasons = [...profileViolationsFound, ...nameIssues, ...contextIssues];
    allReasons.push(...profileReasons);
    // predicate 5: module identity paths (slash normalization only) + SHAs vs trusted source files
    const miOkShape = typeof receipt.moduleIdentity?.gateModule === 'object' && receipt.moduleIdentity?.gateModule !== null && typeof receipt.moduleIdentity?.runner === 'object' && receipt.moduleIdentity?.runner !== null;
    const gM = miOkShape ? receipt.moduleIdentity.gateModule : null;
    const rn = miOkShape ? receipt.moduleIdentity.runner : null;
    const gatePathOk = typeof gM?.path === 'string' && normPath(gM.path) === normPath(TRUSTED_GATE_MODULE.path);
    const runnerPathOk = typeof rn?.path === 'string' && normPath(rn.path) === normPath(TRUSTED_RUNNER.path);
    const gateShaOk = typeof gM?.sha256 === 'string' && normHex(gM.sha256) === normHex(TRUSTED_GATE_MODULE.sha256);
    const runnerShaOk = typeof rn?.sha256 === 'string' && normHex(rn.sha256) === normHex(TRUSTED_RUNNER.sha256);
    quantities.MODULE_CODE_IDENTITY = {
      ok: gatePathOk && runnerPathOk && gateShaOk && runnerShaOk,
      performed: true,
      gateModule: { claimedPath: gM?.path ?? null, normalizedPath: typeof gM?.path === 'string' ? normPath(gM.path) : null, trustedPath: TRUSTED_GATE_MODULE.path, pathOk: gatePathOk, claimedSha256: gM?.sha256 ?? null, trustedSha256: TRUSTED_GATE_MODULE.sha256, shaOk: gateShaOk },
      runner: { claimedPath: rn?.path ?? null, normalizedPath: typeof rn?.path === 'string' ? normPath(rn.path) : null, trustedPath: TRUSTED_RUNNER.path, pathOk: runnerPathOk, claimedSha256: rn?.sha256 ?? null, trustedSha256: TRUSTED_RUNNER.sha256, shaOk: runnerShaOk },
      trustedModuleShasMeasured: trusted.moduleShas,
      whyNonCircular: 'claimed SHAs are compared against independently frozen constants and the physically re-measured source files — a receipt-declared hash confers no authority',
    };
    const moduleReasons = [];
    if (!gatePathOk) moduleReasons.push('moduleIdentity.gateModule.path does not match the trusted gate module path');
    if (!gateShaOk) moduleReasons.push('moduleIdentity.gateModule.sha256 does not match the trusted gate module file');
    if (!runnerPathOk) moduleReasons.push('moduleIdentity.runner.path does not match the trusted predecessor runner path');
    if (!runnerShaOk) moduleReasons.push('moduleIdentity.runner.sha256 does not match the trusted predecessor runner file');
    allReasons.push(...moduleReasons);
    // predicate 3+4: re-derive every per-pin comparison and the summary from the trusted pins
    const perPinReasons = [];
    const perPinChecks = [];
    let derivedMatched = 0;
    const derivedBlocked = [];
    if (Array.isArray(receipt.perPin)) {
      for (const e of receipt.perPin) {
        const t = byName.get(e?.pin);
        if (!t) { perPinReasons.push('pin entry ' + JSON.stringify(e?.pin) + ' is not a trusted expected pin'); continue; }
        const expectedSizeOk = e.EXPECTED?.sizeBytes === t.sizeBytes;
        const expectedShaOk = typeof e.EXPECTED?.sha256 === 'string' && normHex(e.EXPECTED.sha256) === normHex(t.sha256);
        const existsTrue = e.MEASURED?.exists === true;
        const sizeVsTrustedOk = existsTrue && e.MEASURED?.sizeBytes === t.sizeBytes;
        const shaVsTrustedOk = existsTrue && typeof e.MEASURED?.sha256 === 'string' && normHex(e.MEASURED.sha256) === normHex(t.sha256);
        let derivedCompareResult;
        if (!existsTrue) derivedCompareResult = 'MISSING';
        else if (e.MEASURED.sizeBytes !== t.sizeBytes) derivedCompareResult = 'SIZE_MISMATCH';
        else if (!shaVsTrustedOk) derivedCompareResult = 'SHA_MISMATCH';
        else derivedCompareResult = 'MATCH';
        const derivedMatch = derivedCompareResult === 'MATCH';
        if (derivedMatch) derivedMatched++;
        else derivedBlocked.push({ pin: e.pin, compareResult: derivedCompareResult });
        const claimedValid = e.compareResult === derivedCompareResult;
        const check = {
          pin: e.pin,
          expectedVsTrusted: { sizeOk: expectedSizeOk, shaOk: expectedShaOk },
          measuredExistsTrue: existsTrue,
          measuredSizeVsTrusted: sizeVsTrustedOk, measuredShaVsTrusted: shaVsTrustedOk,
          derivedCompareResult, derivedMatch,
          claimedCompareResult: e.compareResult, compareResultValid: claimedValid,
          inputMatchField: 'inputMatch' in e ? { present: true, value: e.inputMatch, consistent: e.inputMatch === derivedMatch } : { present: false },
        };
        if (!expectedSizeOk) perPinReasons.push('pin ' + e.pin + ': receipt EXPECTED.sizeBytes ' + e.EXPECTED.sizeBytes + ' != trusted pin ' + t.sizeBytes);
        if (!expectedShaOk) perPinReasons.push('pin ' + e.pin + ': receipt EXPECTED.sha256 differs from the trusted pin');
        if (!existsTrue) perPinReasons.push('pin ' + e.pin + ': MEASURED.exists is not true (live evidence currently exists — a PASS receipt may not claim a missing input)');
        else {
          if (e.MEASURED.sizeBytes !== t.sizeBytes) perPinReasons.push('pin ' + e.pin + ': MEASURED.sizeBytes ' + e.MEASURED.sizeBytes + ' != trusted pin ' + t.sizeBytes);
          if (!shaVsTrustedOk) perPinReasons.push('pin ' + e.pin + ': MEASURED.sha256 differs from the trusted pin (claimed ' + e.compareResult + ')');
        }
        if (!claimedValid) perPinReasons.push('pin ' + e.pin + ': claimed compareResult ' + e.compareResult + ' contradicts the independently derived ' + derivedCompareResult);
        if (check.inputMatchField.present && !check.inputMatchField.consistent) perPinReasons.push('pin ' + e.pin + ': legacy inputMatch field contradicts the independently derived match');
        perPinChecks.push(check);
      }
    }
    const recomputed = {
      total: Array.isArray(receipt.perPin) ? receipt.perPin.length : null, matched: derivedMatched, blockedCount: derivedBlocked.length,
      blockedPins: derivedBlocked,
      verdict: derivedBlocked.length === 0 ? 'PASS' : 'BLOCKED_INPUT_IDENTITY',
      EFFECTIVE_GATE_RESULT: derivedBlocked.length === 0 ? 'GATE_PASS__DOWNSTREAM_AUTHORIZED' : 'GATE_BLOCKED__DOWNSTREAM_REFUSED_ZERO_CALLS',
    };
    const claimed = {
      total: receipt.gate?.total ?? null, matched: receipt.gate?.matched ?? null, blockedCount: receipt.gate?.blockedCount ?? null,
      blockedPins: receipt.gate?.blockedPins ?? null, verdict: receipt.gate?.verdict ?? null, EFFECTIVE_GATE_RESULT: receipt.gate?.EFFECTIVE_GATE_RESULT ?? null,
    };
    const summaryMismatches = [];
    if (claimed.total !== recomputed.total) summaryMismatches.push('gate.total ' + claimed.total + ' != recomputed ' + recomputed.total);
    if (claimed.matched !== recomputed.matched) summaryMismatches.push('gate.matched ' + claimed.matched + ' != recomputed ' + recomputed.matched);
    if (claimed.blockedCount !== recomputed.blockedCount) summaryMismatches.push('gate.blockedCount ' + claimed.blockedCount + ' != recomputed ' + recomputed.blockedCount);
    if (Array.isArray(claimed.blockedPins) && Array.isArray(recomputed.blockedPins)) {
      if (claimed.blockedPins.length !== recomputed.blockedPins.length) summaryMismatches.push('gate.blockedPins length ' + claimed.blockedPins.length + ' != recomputed ' + recomputed.blockedPins.length);
      else for (let i = 0; i < recomputed.blockedPins.length; i++) {
        if (claimed.blockedPins[i]?.pin !== recomputed.blockedPins[i].pin || claimed.blockedPins[i]?.compareResult !== recomputed.blockedPins[i].compareResult) {
          summaryMismatches.push('gate.blockedPins[' + i + '] (' + claimed.blockedPins[i]?.pin + '/' + claimed.blockedPins[i]?.compareResult + ') contradicts recomputed (' + recomputed.blockedPins[i].pin + '/' + recomputed.blockedPins[i].compareResult + ')');
        }
      }
    } else if (!Array.isArray(claimed.blockedPins)) summaryMismatches.push('gate.blockedPins is not an array');
    if (claimed.verdict !== recomputed.verdict) summaryMismatches.push('gate.verdict ' + claimed.verdict + ' != recomputed ' + recomputed.verdict + ' (a contradictory summary refuses qualification)');
    if (claimed.EFFECTIVE_GATE_RESULT !== recomputed.EFFECTIVE_GATE_RESULT) summaryMismatches.push('gate.EFFECTIVE_GATE_RESULT ' + claimed.EFFECTIVE_GATE_RESULT + ' != recomputed ' + recomputed.EFFECTIVE_GATE_RESULT);
    if (recomputed.verdict === 'PASS' && (recomputed.total !== EXPECTED_PIN_COUNT || recomputed.matched !== EXPECTED_PIN_COUNT || recomputed.blockedCount !== 0 || recomputed.blockedPins.length !== 0)) summaryMismatches.push('PASS requires all ' + EXPECTED_PIN_COUNT + ' pins matching, zero blocked and an empty blockedPins array');
    quantities.RECEIPT_INTERNAL_CONSISTENCY = {
      ok: perPinReasons.length === 0 && summaryMismatches.length === 0,
      performed: true, perPinChecks, recomputed, claimed, perPinReasons, summaryMismatches,
      whyNonCircular: 'compareResult/match/total/matched/blockedCount/blockedPins/verdict/EFFECTIVE_GATE_RESULT are all independently recomputed from the trusted pins — the receipt\u2019s own claims are only ever COMPARED, never trusted',
    };
    allReasons.push(...perPinReasons, ...summaryMismatches);
    // conjunction: all four quantities OK (any collected reason refuses)
    quantities.RECEIPT_QUALIFICATION = {
      verdict: allReasons.length === 0 ? 'PASS' : 'FAIL',
      profileOk: quantities.RECEIPT_PROFILE.ok,
      refusalReason: allReasons[0] ?? null, reasons: allReasons,
      receiptIdentity, contextBase: RECEIPT_PROFILE.contextBase,
      independence: 'trusted pins come from the SHA-verified gate module (never from the receipt); receipt claims are re-derived, not trusted; live remeasurement is independent of the receipt',
    };
    return quantities;
  } catch (e) {
    // predicate 7: any error is a controlled PA2 failure — never an omitted case, default PASS or empty success
    quantities.RECEIPT_QUALIFICATION = {
      verdict: 'FAIL', refusalReason: 'qualification error (fail-closed): ' + String(e?.message || e),
      reasons: [...(allReasons.length ? allReasons : []), 'qualification error (fail-closed): ' + String(e?.message || e)],
      receiptIdentity: quantities.RECEIPT_QUALIFICATION?.receiptIdentity ?? null, contextBase: RECEIPT_PROFILE.contextBase,
    };
    return quantities;
  }
}

// ---- predicate 8 + §5: the ACTUAL aggregator (identical semantics to the predecessor
// computeQualification; only explicitly documented success statuses count) ----
export function computeQualification(outcomes, expectations) {
  const missing = Object.keys(expectations).filter(id => !(id in outcomes));
  const failing = Object.keys(expectations).filter(id => id in outcomes && outcomes[id] !== expectations[id]);
  const ok = missing.length === 0 && failing.length === 0;
  const verdict = ok ? 'QUALIFICATION_PASS' : 'QUALIFICATION_REFUSED';
  const exitCode = ok ? 0 : 4;
  return { verdict, ok, missing, failing, exitCode };
}

// canonical required outcomes of the corrected POST battery (contract §5: the PA2
// result is a required conjunct; missing/FAIL/ERROR/NOT_PERFORMED => overall REFUSED)
export const EXPECTED_OUTCOMES = Object.freeze({
  ORIGINAL_SEVEN: 'PASS', BASE_53_REPLAY: 'PASS', FULL_SUITE: 'PASS',
  DA1_CENSUS: 'PASS', DA1_NOT_OPENED: 'PASS',
  DA2_CAP4: 'PASS', DA2_CAP256: 'PASS', DA2_MUTANT_COPY: 'CONTROL_PASS', DA2_SMALL_FIXTURE: 'PASS', DA2_TWO_SOURCE: 'PASS',
  DA3_REFUSALS: 'PASS', DA3_POSITIVES: 'PASS',
  PA1_REGRESSION: 'PASS', PA2_RECEIPT_QUALIFICATION: 'PASS',
});
