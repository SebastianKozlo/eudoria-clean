# prove_byte_prefix.ps1 - PE_OPERATING_MODEL_AMENDMENT_A1_R2_20260906
# GATE G1 PROOF (fail-closed, byte-by-byte):
#   P1: 01_RAW/PROJECT_OPERATING_MODEL.md.pre is a FULL byte-prefix of the live
#       PROJECT_OPERATING_MODEL.md (every pre-byte identical at the same offset,
#       pre-length <= post-length, post strictly longer).
#   P2 (bonus provenance): the appended suffix (post bytes after the pre-length)
#       is byte-identical to 00_CONTROL/amendment_source.md (the committed source
#       == the exact appended bytes).
#   P3 (bonus): the appended suffix physically contains the required section
#       heading and the binding point markers A1.1..A1.9.
# ASCII-only script; writes PASS/FAIL + evidence to 01_RAW/PREFIX_PROOF_OUTPUT.txt.
param()
$ErrorActionPreference = 'Stop'
$root   = 'D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean'
$run    = Join-Path $root 'docs\audits\PE_OPERATING_MODEL_AMENDMENT_A1_R2_20260906'
$postF  = Join-Path $root 'PROJECT_OPERATING_MODEL.md'
$preF   = Join-Path $run '01_RAW\PROJECT_OPERATING_MODEL.md.pre'
$srcF   = Join-Path $run '00_CONTROL\amendment_source.md'
$out    = Join-Path $run '01_RAW\PREFIX_PROOF_OUTPUT.txt'

$log = New-Object System.Collections.Generic.List[string]
$log.Add('=== PREFIX PROOF (GATE G1) - PE_OPERATING_MODEL_AMENDMENT_A1_R2_20260906 ===')
$log.Add('ran: ' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz'))
$preB  = [System.IO.File]::ReadAllBytes($preF)
$postB = [System.IO.File]::ReadAllBytes($postF)
$srcB  = [System.IO.File]::ReadAllBytes($srcF)
$log.Add(('pre  file: ' + $preF + ' | ' + $preB.Length + ' B'))
$log.Add(('post file: ' + $postF + ' | ' + $postB.Length + ' B'))
$log.Add(('src  file: ' + $srcF + ' | ' + $srcB.Length + ' B'))

$fail = $null
# P1: full byte-prefix
if ($postB.Length -lt $preB.Length) { $fail = 'post shorter than pre' }
if (-not $fail) {
  $mismatch = -1
  for ($i = 0; $i -lt $preB.Length; $i++) {
    if ($postB[$i] -ne $preB[$i]) { $mismatch = $i; break }
  }
  if ($mismatch -ge 0) { $fail = 'byte mismatch at offset ' + $mismatch }
}
if ($fail) {
  $log.Add('P1 FAIL: ' + $fail)
} else {
  $log.Add('P1 PASS: every pre-byte identical at the same offset (0..' + ($preB.Length - 1) + '); post is longer by ' + ($postB.Length - $preB.Length) + ' B -> .pre IS A FULL BYTE-PREFIX of the post file (append-only PROVEN)')
  # P2: suffix == source bytes
  $suffixOk = $true
  if (($postB.Length - $preB.Length) -ne $srcB.Length) { $suffixOk = $false }
  if ($suffixOk) {
    for ($j = 0; $j -lt $srcB.Length; $j++) {
      if ($postB[$preB.Length + $j] -ne $srcB[$j]) { $suffixOk = $false; break }
    }
  }
  if ($suffixOk) {
    $log.Add('P2 PASS: appended suffix byte-identical to amendment_source.md (' + $srcB.Length + ' B) - committed source == exact appended bytes')
  } else {
    $log.Add('P2 FAIL: suffix != amendment_source.md bytes')
    $fail = 'P2'
  }
}
if (-not $fail) {
  # P3: structural markers present in the suffix (decoded UTF-8)
  $suffixTxt = [System.Text.Encoding]::UTF8.GetString($postB, $preB.Length, $srcB.Length)
  $markers = @(
    '## AMENDMENT A-1',
    'GOVERNANCE MODEL v2',
    'PE-MASTER HUMAN AUDIT CONTRACT',
    'ADOPTED 2026-09-06',
    'A1.1', 'A1.2', 'A1.3', 'A1.4', 'A1.5', 'A1.6', 'A1.7', 'A1.8', 'A1.9',
    'PE_MASTER_HUMAN_AUDIT_CONTRACT_v1.md'
  )
  $missing = @($markers | Where-Object { -not $suffixTxt.Contains($_) })
  if ($missing.Count -gt 0) {
    $log.Add('P3 FAIL: missing markers: ' + ($missing -join ', '))
    $fail = 'P3'
  } else {
    $log.Add('P3 PASS: heading + A1.1..A1.9 markers + contract file reference all present in the appended suffix')
  }
}
$sha = { param($b) [System.BitConverter]::ToString([System.Security.Cryptography.SHA256]::Create().ComputeHash($b)).Replace('-','') }
$log.Add(('pre  SHA256: ' + (& $sha $preB)))
$log.Add(('post SHA256: ' + (& $sha $postB)))
$log.Add(('src  SHA256: ' + (& $sha $srcB)))
if ($fail) {
  $log.Add('OVERALL: FAIL (' + $fail + ')')
} else {
  $log.Add('OVERALL: PASS - GATE G1 (append-only, byte-prefix) PROVEN')
}
[System.IO.File]::WriteAllLines($out, $log, (New-Object System.Text.UTF8Encoding $false))
Write-Host ($log -join [Environment]::NewLine)
if ($fail) { exit 1 } else { exit 0 }
