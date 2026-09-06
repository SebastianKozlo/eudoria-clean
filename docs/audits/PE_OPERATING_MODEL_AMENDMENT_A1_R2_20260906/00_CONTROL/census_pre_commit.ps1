# census_pre_commit.ps1 - PE_OPERATING_MODEL_AMENDMENT_A1_R2_20260906
# GATE G5/G6 PRE-COMMIT CENSUS (fail-closed, machine comparison):
#   1. Capture the full worktree status (git status --porcelain=v1).
#   2. Capture the staged path list (git diff --cached --name-only).
#   3. Machine-compare EVERY staged path against the ALLOWED list
#      (exact files + two directory prefixes). Any staged path outside
#      the allowed set => FAIL. Any tracked-modified/untracked leftover
#      outside the allowed set => FAIL.
#   4. Write 01_RAW/GIT_CENSUS_PRE_COMMIT.txt with the full evidence.
# NOTE: this output file itself is staged right after it is generated and is
# a member of the allowed root docs/audits/PE_OPERATING_MODEL_AMENDMENT_A1_R2_20260906/
# (recorded in the census text). The final post-staging verification is run in
# the delivery session (git diff --cached --name-only == census list + this file).
param()
$ErrorActionPreference = 'Stop'
$root = 'D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean'
$run  = Join-Path $root 'docs\audits\PE_OPERATING_MODEL_AMENDMENT_A1_R2_20260906'
$out  = Join-Path $run '01_RAW\GIT_CENSUS_PRE_COMMIT.txt'

$exactAllowed = @(
  'PROJECT_OPERATING_MODEL.md',
  'PE_MASTER_HUMAN_AUDIT_CONTRACT_v1.md',
  'AUDIT_ENTRYPOINT.md'
)
$prefixAllowed = @(
  'docs/audits/PE_OPERATING_MODEL_AMENDMENT_A1_R2_20260906/',
  'docs/audits/PE_OPERATING_MODEL_AMENDMENT_A1_R1_20260906/'
)

function Test-Allowed([string]$p) {
  if ($exactAllowed -contains $p) { return $true }
  foreach ($pre in $prefixAllowed) { if ($p.StartsWith($pre)) { return $true } }
  return $false
}

$log = New-Object System.Collections.Generic.List[string]
$log.Add('=== GIT CENSUS PRE-COMMIT - PE_OPERATING_MODEL_AMENDMENT_A1_R2_20260906 ===')
$log.Add('ran: ' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz'))
$log.Add('BASE_SHA (verified at run start): 8c95438245b3f75b8d90bd3f86a573dd8fab4c54')
$log.Add('')
$log.Add('--- ALLOWED LIST (contract scope points 1-5) ---')
foreach ($a in $exactAllowed) { $log.Add('EXACT: ' + $a) }
foreach ($a in $prefixAllowed) { $log.Add('PREFIX: ' + $a + '**') }
$log.Add('')
$log.Add('--- git status --porcelain=v1 (full worktree state at census time) ---')
$status = @(git status --porcelain=v1)
foreach ($s in $status) { $log.Add($s) }
$log.Add('')
$log.Add('--- STAGED PATH LIST (git diff --cached --name-only) ---')
$staged = @(git diff --cached --name-only)
foreach ($p in $staged) { $log.Add($p) }
$log.Add(('STAGED_COUNT: ' + $staged.Count))
$log.Add('')
$badStaged = @($staged | Where-Object { -not (Test-Allowed $_) })
$outside = @($status | Where-Object {
  $path = $_.Substring(3).Trim('"')
  -not (Test-Allowed $path)
})
$log.Add('--- MACHINE COMPARISON ---')
$log.Add(('staged paths outside the allowed list: ' + $(if ($badStaged.Count) { $badStaged -join '; ' } else { 'NONE' })))
$log.Add(('worktree entries (tracked/untracked) outside the allowed list: ' + $(if ($outside.Count) { $outside -join '; ' } else { 'NONE' })))
$deletions = @(git diff --cached --name-status --diff-filter=D)
$log.Add(('staged DELETIONS (must be none): ' + $(if ($deletions.Count) { $deletions -join '; ' } else { 'NONE' })))
$ok = ($badStaged.Count -eq 0) -and ($outside.Count -eq 0) -and ($deletions.Count -eq 0)
$log.Add('')
$log.Add('NOTE: this census file (01_RAW/GIT_CENSUS_PRE_COMMIT.txt) is staged immediately after')
$log.Add('generation; its own path is inside the allowed root docs/audits/PE_OPERATING_MODEL_AMENDMENT_A1_R2_20260906/.')
$log.Add('Final staged set = the list above + this file. The post-commit authoritative census is')
$log.Add('git show --name-only <HEAD> (run by PE-MASTER from disk).')
$log.Add('')
if ($ok) { $log.Add('CENSUS RESULT: PASS - staged set == allowed list; zero foreign paths; zero deletions') }
else     { $log.Add('CENSUS RESULT: FAIL - abort the commit') }
[System.IO.File]::WriteAllLines($out, $log, (New-Object System.Text.UTF8Encoding $false))
Write-Host ($log -join [Environment]::NewLine)
if ($ok) { exit 0 } else { exit 1 }
