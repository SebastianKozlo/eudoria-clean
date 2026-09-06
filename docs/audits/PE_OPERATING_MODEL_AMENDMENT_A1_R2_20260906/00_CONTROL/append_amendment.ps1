# append_amendment.ps1 - PE_OPERATING_MODEL_AMENDMENT_A1_R2_20260906
# Purpose: byte-exact APPEND-ONLY edit of PROJECT_OPERATING_MODEL.md.
# Method (pure byte operations, fail-closed):
#   1. Verify the live PROJECT_OPERATING_MODEL.md is byte-identical to the .pre copy
#      (proves no foreign edit happened between .pre capture and this append).
#   2. Verify the live file currently ends with LF (append boundary sanity).
#   3. Append the bytes of 00_CONTROL/amendment_source.md (already normalized to
#      LF + UTF-8-no-BOM) VERBATIM, as raw bytes, to the end of the live file.
#   4. Report pre/post sizes and SHA256.
# Abort without writing if any verification fails.
# NOTE: this script contains ASCII only; all non-ASCII content lives in the
# amendment_source.md data file (write-tool authored, UTF-8).
param()
$ErrorActionPreference = 'Stop'
$root   = 'D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean'
$run    = Join-Path $root 'docs\audits\PE_OPERATING_MODEL_AMENDMENT_A1_R2_20260906'
$target = Join-Path $root 'PROJECT_OPERATING_MODEL.md'
$pre    = Join-Path $run '01_RAW\PROJECT_OPERATING_MODEL.md.pre'
$src    = Join-Path $run '00_CONTROL\amendment_source.md'
$out    = Join-Path $run '01_RAW\OM_APPEND_OUTPUT.txt'

$log = New-Object System.Collections.Generic.List[string]
$log.Add('=== OM APPEND (AMENDMENT A-1) - byte-exact append-only ===')
$log.Add('started: ' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz'))

$live = [System.IO.File]::ReadAllBytes($target)
$preB = [System.IO.File]::ReadAllBytes($pre)
$srcB = [System.IO.File]::ReadAllBytes($src)

$log.Add(('live bytes: ' + $live.Length))
$log.Add(('pre  bytes: ' + $preB.Length))
$log.Add(('src  bytes: ' + $srcB.Length))
$log.Add(('live SHA256: ' + [System.BitConverter]::ToString([System.Security.Cryptography.SHA256]::Create().ComputeHash($live)).Replace('-','')))
$log.Add(('pre  SHA256: ' + [System.BitConverter]::ToString([System.Security.Cryptography.SHA256]::Create().ComputeHash($preB)).Replace('-','')))
$log.Add(('src  SHA256: ' + [System.BitConverter]::ToString([System.Security.Cryptography.SHA256]::Create().ComputeHash($srcB)).Replace('-','')))

if ($live.Length -ne $preB.Length) { throw 'ABORT: live size != pre size - foreign edit detected' }
for ($i = 0; $i -lt $live.Length; $i++) {
  if ($live[$i] -ne $preB[$i]) { throw ('ABORT: live vs pre byte mismatch at offset ' + $i) }
}
$log.Add('CHECK1 PASS: live file byte-identical to .pre (no foreign edit before append)')
if ($live[$live.Length - 1] -ne 0x0A) { throw 'ABORT: live file does not end with LF' }
$log.Add('CHECK2 PASS: live file ends with LF (clean append boundary)')

$newBytes = New-Object byte[] ($live.Length + $srcB.Length)
[Array]::Copy($live, 0, $newBytes, 0, $live.Length)
[Array]::Copy($srcB, 0, $newBytes, $live.Length, $srcB.Length)
[System.IO.File]::WriteAllBytes($target, $newBytes)

$post = [System.IO.File]::ReadAllBytes($target)
$log.Add(('post bytes: ' + $post.Length + ' (expected: ' + ($live.Length + $srcB.Length) + ')'))
$log.Add(('post SHA256: ' + [System.BitConverter]::ToString([System.Security.Cryptography.SHA256]::Create().ComputeHash($post)).Replace('-','')))
if ($post.Length -ne ($live.Length + $srcB.Length)) { throw 'ABORT: post-append size mismatch' }
$log.Add('APPEND DONE: pre [' + $live.Length + ' B] + source [' + $srcB.Length + ' B] = post [' + $post.Length + ' B]')
[System.IO.File]::WriteAllLines($out, $log, (New-Object System.Text.UTF8Encoding $false))
Write-Host ($log -join [Environment]::NewLine)
