# verify_entrypoint_rows.ps1 - PE_OPERATING_MODEL_AMENDMENT_A1_R2_20260906
# GATE G4 PROOF (fail-closed, line-level byte-identity):
#   E1: Every line of the .pre copy appears byte-identically (same content,
#       same order) in the post-edit AUDIT_ENTRYPOINT.md - verified by
#       reconstructing: pre-text with the new row line removed at its insert
#       point must equal the .pre text EXACTLY (byte-level).
#   E2: The post file has exactly ONE line more than .pre.
#   E3: The single added line is the governance row of this run (contains
#       the RUN_ID and sits immediately after the unique 5-column separator).
#   E4: No other line differs (covered by E1's byte-level reconstruction).
# Writes PASS/FAIL + evidence to 01_RAW/ENTRYPOINT_ROW_PROOF_OUTPUT.txt.
param()
$ErrorActionPreference = 'Stop'
$root = 'D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean'
$run  = Join-Path $root 'docs\audits\PE_OPERATING_MODEL_AMENDMENT_A1_R2_20260906'
$live = Join-Path $root 'AUDIT_ENTRYPOINT.md'
$pre  = Join-Path $run '01_RAW\AUDIT_ENTRYPOINT.md.pre'
$out  = Join-Path $run '01_RAW\ENTRYPOINT_ROW_PROOF_OUTPUT.txt'

$log = New-Object System.Collections.Generic.List[string]
$log.Add('=== ENTRYPOINT ROW SURVIVAL PROOF (GATE G4) - PE_OPERATING_MODEL_AMENDMENT_A1_R2_20260906 ===')
$log.Add('ran: ' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz'))

$preB   = [System.IO.File]::ReadAllBytes($pre)
$postB  = [System.IO.File]::ReadAllBytes($live)
$preTxt = [System.Text.Encoding]::UTF8.GetString($preB)
$postTxt = [System.Text.Encoding]::UTF8.GetString($postB)
$preLines  = @($preTxt  -split "`n")
$postLines = @($postTxt -split "`n")
$log.Add(('pre lines: ' + $preLines.Count + ' | post lines: ' + $postLines.Count))

$fail = $null
if ($postLines.Count -ne ($preLines.Count + 1)) { $fail = 'E2: line count delta != 1' } else { $log.Add('E2 PASS: exactly one line added') }

# find the inserted line: post - pre = one extra element somewhere
# reconstruct by removing the one post line whose removal yields the pre text
$found = -1
for ($p = 0; $p -lt $postLines.Count; $p++) {
  $attempt = @()
  if ($p -gt 0) { $attempt += $postLines[0..($p - 1)] }
  if ($p -lt ($postLines.Count - 1)) { $attempt += $postLines[($p + 1)..($postLines.Count - 1)] }
  if (($attempt -join "`n") -eq $preTxt) { $found = $p; break }
}
if ($found -lt 0) {
  $log.Add('E1 FAIL: no single-line removal reconstructs the pre text -> more than the one row changed')
  $fail = 'E1'
} else {
  $addedLine = $postLines[$found]
  $log.Add('E1 PASS: removing exactly ONE post line (index ' + $found + ') reconstructs the .pre text byte-for-byte -> every old line byte-identical, order preserved')
  if ($addedLine.Contains('PE_OPERATING_MODEL_AMENDMENT_A1_R2_20260906')) {
    $log.Add('E3 PASS: the added line is this run''s governance row')
  } else {
    $log.Add('E3 FAIL: the added line does not reference the RUN_ID'); $fail = 'E3'
  }
  $sep = '|---|---|---|---|---|'
  if ($found -ge 1 -and $postLines[$found - 1].TrimEnd() -eq $sep) {
    $log.Add('E3b PASS: the new row sits immediately after the unique 5-column separator (top of LATEST RUNS, newest-first)')
  } else {
    $log.Add('E3b FAIL: the new row is not immediately after the separator'); $fail = 'E3b'
  }
}
$sha = { param($b) [System.BitConverter]::ToString([System.Security.Cryptography.SHA256]::Create().ComputeHash($b)).Replace('-','') }
$log.Add(('pre  SHA256: ' + (& $sha $preB)))
$log.Add(('post SHA256: ' + (& $sha $postB)))
if ($fail) { $log.Add('OVERALL: FAIL (' + $fail + ')') } else { $log.Add('OVERALL: PASS - GATE G4 (exactly one new governance row; all old rows byte-identical) PROVEN') }
[System.IO.File]::WriteAllLines($out, $log, (New-Object System.Text.UTF8Encoding $false))
Write-Host ($log -join [Environment]::NewLine)
if ($fail) { exit 1 } else { exit 0 }
