# insert_entrypoint_row.ps1 - PE_OPERATING_MODEL_AMENDMENT_A1_R2_20260906
# GATE G4 STEP 1 (byte-controlled insert, fail-closed):
#   1. Verify the live AUDIT_ENTRYPOINT.md is byte-identical to the .pre copy.
#   2. Locate the unique 5-column table separator of the LATEST RUNS table
#      ("|---|---|---|---|---|" + LF) - exactly one occurrence required.
#   3. Insert ONE governance row line immediately after it (newest-first
#      convention of that table). No existing byte is modified or moved;
#      the row is ASCII-only by construction.
#   4. Report pre/post sizes and SHA256.
# ASCII-only script. Aborts without writing on any verification failure.
param()
$ErrorActionPreference = 'Stop'
$root = 'D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean'
$run  = Join-Path $root 'docs\audits\PE_OPERATING_MODEL_AMENDMENT_A1_R2_20260906'
$live = Join-Path $root 'AUDIT_ENTRYPOINT.md'
$pre  = Join-Path $run '01_RAW\AUDIT_ENTRYPOINT.md.pre'
$out  = Join-Path $run '01_RAW\ENTRYPOINT_INSERT_OUTPUT.txt'

$row = '| (this governance commit; SHA discoverable via `git log -1 -- AUDIT_ENTRYPOINT.md`) | PE_OPERATING_MODEL_AMENDMENT_A1_R2_20260906 | `PE_OPERATING_MODEL_AMENDMENT_A1_R2_20260906/` | (governance) AMENDMENT A-1 appended append-only to `PROJECT_OPERATING_MODEL.md` (A1.1-A1.9 binding points; .pre full byte-prefix proven) + `PE_MASTER_HUMAN_AUDIT_CONTRACT_v1.md` created in repo root (verbatim human contract: sections A-E, 14 format points, 10 percent rules); the R1 blocker dir `PE_OPERATING_MODEL_AMENDMENT_A1_R1_20260906/` committed as arrears unchanged (worktree cleanup) | n/a (governance row; no audit-queue entry; PE-MASTER verifies from disk) |'

$log = New-Object System.Collections.Generic.List[string]
$log.Add('=== ENTRYPOINT GOVERNANCE ROW INSERT (GATE G4 step 1) - PE_OPERATING_MODEL_AMENDMENT_A1_R2_20260906 ===')
$log.Add('ran: ' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz'))

$liveB = [System.IO.File]::ReadAllBytes($live)
$preB  = [System.IO.File]::ReadAllBytes($pre)
$log.Add(('live bytes: ' + $liveB.Length + ' | pre bytes: ' + $preB.Length))
if ($liveB.Length -ne $preB.Length) { throw 'ABORT: live size != pre size' }
for ($i = 0; $i -lt $liveB.Length; $i++) { if ($liveB[$i] -ne $preB[$i]) { throw ('ABORT: live vs pre mismatch at offset ' + $i) } }
$log.Add('CHECK1 PASS: live byte-identical to .pre (no foreign edit)')

$liveTxt = [System.Text.Encoding]::UTF8.GetString($liveB)
$sep = "|---|---|---|---|---|`n"
$cnt = [regex]::Matches($liveTxt, [regex]::Escape($sep)).Count
$log.Add(('CHECK2: occurrences of the 5-column separator (with LF): ' + $cnt))
if ($cnt -ne 1) { throw 'ABORT: expected exactly one 5-column separator' }
$idx = $liveTxt.IndexOf($sep)
$log.Add('CHECK2 PASS: unique LATEST RUNS separator found at char offset ' + $idx)

$rowLine = $row + "`n"
$newTxt = $liveTxt.Insert($idx + $sep.Length, $rowLine)
[System.IO.File]::WriteAllText($live, $newTxt, (New-Object System.Text.UTF8Encoding $false))

$postB = [System.IO.File]::ReadAllBytes($live)
$log.Add(('post bytes: ' + $postB.Length + ' (expected: ' + ($liveB.Length + [System.Text.Encoding]::UTF8.GetByteCount($rowLine)) + ')'))
$log.Add(('post SHA256: ' + [System.BitConverter]::ToString([System.Security.Cryptography.SHA256]::Create().ComputeHash($postB)).Replace('-','')))
if ($postB.Length -ne ($liveB.Length + [System.Text.Encoding]::UTF8.GetByteCount($rowLine))) { throw 'ABORT: post size mismatch' }
$log.Add('INSERT DONE: one row line inserted after the separator; zero existing bytes modified')
[System.IO.File]::WriteAllLines($out, $log, (New-Object System.Text.UTF8Encoding $false))
Write-Host ($log -join [Environment]::NewLine)
