// witness_457485_regression.test.mjs — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
// T6 (plan T8): the 457485 witness guard. src/pesource/NifModelReader.js is
// the SINGLE-WITNESS reader; this run's adapter extends via NEW code under
// src/pecompat/ and MUST NOT touch it. The planned outcome is
// NOT_APPLICABLE_UNTOUCHED (WITNESS_UNTOUCHED). If the file HAS changed, this
// test FAILS loudly and the mandated witness regression battery becomes
// REQUIRED before any such change could be accepted (contract §7) — the
// executor would STOP and report why.
//
// MEASURED_QUANTITY: working-tree SHA256 of src/pesource/NifModelReader.js vs
//   the same file at the pinned BASE commit (git object), plus the git status
//   of src/pesource/.
// INDEPENDENT_SOURCE_OF_TRUTH: the BASE commit's blob content (git).
// WHY_NON_CIRCULAR: git object comparison — not any run-produced value.
// FAILURE_CASE_DETECTED: any byte difference (or any dirty path under
//   src/pesource/) fails this test.
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { record } from './_helpers.mjs';

const WITNESS_PATH = 'src/pesource/NifModelReader.js';

function gitBytes(args, cwd) {
  return execFileSync('git', args, { cwd, maxBuffer: 16 * 1024 * 1024 });
}

export async function run(ctx) {
  const out = [];
  const cwd = ctx.repoRoot;
  try {
    // working tree blob id + SHA256:
    const wtHash = execFileSync('git', ['hash-object', '-w', '--', WITNESS_PATH], { cwd }).toString().trim();
    // BASE copy (HEAD == BASE by construction of this run):
    const baseBlob = gitBytes(['show', `HEAD:${WITNESS_PATH}`], cwd);
    const baseSha256 = createHash('sha256').update(baseBlob).digest('hex');
    // working tree SHA256 (read the file directly — independent of git filters):
    const { readFile } = await import('node:fs/promises');
    const wtBytes = await readFile(`${cwd}/${WITNESS_PATH}`);
    const wtSha256 = createHash('sha256').update(wtBytes).digest('hex');
    // git status of src/pesource/ — the DISCIPLINE (R2 refinement, labeled):
    // no EXISTING pesource file may be MODIFIED or DELETED (the readers stay
    // byte-locked); NEW untracked files are permitted ONLY when listed in the
    // run allowlist (R2 adds exactly one: src/pesource/DdsDecoder.js — the
    // QUALIFIED DDS DXT1/DXT5 strict subset decoder for the two REAL same-era
    // texture formats, contract §6.6; it modifies NO existing reader).
    const status = execFileSync('git', ['status', '--porcelain', '--', 'src/pesource/'], { cwd }).toString().trim();
    const lines = status ? status.split(/\r?\n/).filter(Boolean) : [];
    const modifiedOrDeleted = lines.filter((l) => !l.startsWith('?? '));
    const newFiles = lines.filter((l) => l.startsWith('?? ')).map((l) => l.slice(3).trim());
    const allowedNewFiles = ['src/pesource/DdsDecoder.js'];
    const newFilesAllowed = newFiles.every((f) => allowedNewFiles.includes(f));
    const clean = modifiedOrDeleted.length === 0 && newFilesAllowed;
    const untouched = wtSha256 === baseSha256 && clean;
    out.push(record('T6_witness_457485_untouched', '457485 witness reader untouched (WITNESS_UNTOUCHED)', untouched ? 'PASS' : 'FAIL', {
      measuredQuantity: 'working-tree vs BASE SHA256 of src/pesource/NifModelReader.js + src/pesource/ discipline (no modified/deleted readers; new files allowlisted + listed)',
      independentSourceOfTruth: 'the pinned BASE commit blob (git HEAD:src/pesource/NifModelReader.js)',
      whyNonCircular: 'git object comparison against the pinned base; no run-produced values involved',
      measured: {
        witnessStatus: untouched ? 'WITNESS_UNTOUCHED' : 'WITNESS_MODIFIED',
        plannedOutcome: 'NOT_APPLICABLE_UNTOUCHED (the adapter uses new code; R2 adds the allowlisted DdsDecoder.js — no existing reader touched)',
        workingTreeSha256: wtSha256,
        baseSha256,
        gitHashObject: wtHash,
        pesourceModifiedOrDeleted: modifiedOrDeleted,
        pesourceNewFiles: newFiles,
        newFilesAllowlist: allowedNewFiles,
      },
      expected: {
        witnessStatus: 'WITNESS_UNTOUCHED',
        pesourceModifiedOrDeleted: [],
        pesourceNewFilesWithinAllowlist: true,
      },
      failureCaseDetected: untouched
        ? modifiedOrDeleted.length === 0
          ? 'none — the reader is byte-identical to BASE and the only pesource addition is the allowlisted new-file decoder'
          : 'none — no witness regression battery required (its code path was never touched)'
        : 'WITNESS MODIFIED — the mandated 457485 regression battery is REQUIRED before acceptance; executor must STOP and report why the change was needed',
    }));
  } catch (e) {
    out.push(record('T6_witness_457485_untouched', '457485 witness reader untouched (WITNESS_UNTOUCHED)', 'FAIL', {
      measuredQuantity: 'witness comparison',
      measured: String(e?.message ?? e),
      failureCaseDetected: 'witness check could not be executed (git unavailable?)',
    }));
  }
  return out;
}
