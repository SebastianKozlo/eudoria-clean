import { decodeVclPayload } from 'file:///D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean/src/pesource/VegetationClimateDecoder.js';
const enc = (s) => new Uint8Array(Buffer.from(s, 'ascii'));
const results = [];
// POSITIVE CONTROL: a valid 2-record payload (24 numeric tokens)
const good = Array.from({length: 24}, (_, i) => String(i + 1)).join('\t') + '\n';
try { const d = decodeVclPayload(enc(good)); results.push({ case: 'valid_24_tokens', outcome: 'SUCCESS recordCount=' + d.recordCount, expected: 'SUCCESS 2', pass: d.recordCount === 2 }); }
catch (e) { results.push({ case: 'valid_24_tokens', outcome: 'THROW ' + e.message, expected: 'SUCCESS 2', pass: false }); }
// NEGATIVE CONTROL 1: corrupted token (a comma token like 25.vcl)
const bad = '1\t0,2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\n13\t14\t15\t16\t17\t18\t19\t20\t21\t22\t23\t24\n';
try { decodeVclPayload(enc(bad)); results.push({ case: 'corrupt_comma_token', outcome: 'SUCCESS (UNEXPECTED)', expected: 'THROW', pass: false }); }
catch (e) { results.push({ case: 'corrupt_comma_token', outcome: 'THROW: ' + e.message.slice(0, 80), expected: 'THROW', pass: /non-numeric token/.test(e.message) }); }
// NEGATIVE CONTROL 2: trailing partial record (13 tokens)
const partial = Array.from({length: 13}, (_, i) => String(i + 1)).join('\t') + '\n';
try { decodeVclPayload(enc(partial)); results.push({ case: 'trailing_partial_13', outcome: 'SUCCESS (UNEXPECTED)', expected: 'THROW', pass: false }); }
catch (e) { results.push({ case: 'trailing_partial_13', outcome: 'THROW: ' + e.message.slice(0, 80), expected: 'THROW', pass: /not a multiple of/.test(e.message) }); }
// NEGATIVE CONTROL 3: empty payload
try { decodeVclPayload(enc('')); results.push({ case: 'empty_payload', outcome: 'SUCCESS (UNEXPECTED)', expected: 'THROW', pass: false }); }
catch (e) { results.push({ case: 'empty_payload', outcome: 'THROW: ' + e.message.slice(0, 60), expected: 'THROW', pass: /empty/.test(e.message) }); }
console.log(JSON.stringify({ probe: 'SELF_ADVERSARIAL_decoder_fail_closed_controls', node: process.version, results, all_pass: results.every(r => r.pass) }, null, 2));
