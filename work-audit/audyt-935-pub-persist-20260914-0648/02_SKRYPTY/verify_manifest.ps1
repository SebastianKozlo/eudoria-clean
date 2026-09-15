# WORK-AUDIT (audytor: Work-Audit, audyt: audyt-935-pub-persist-20260914-0648) — plik audytora, NIE jest czescia pracy wykonawcy
$ErrorActionPreference = "Stop"
$repo = "D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
$pkg = Join-Path $repo "docs\audits\PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913"
function Get-FileSha256Upper([string]$path) {
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try { $fs = [System.IO.File]::OpenRead($path); try { $h = $sha.ComputeHash($fs) } finally { $fs.Dispose() } } finally { $sha.Dispose() }
    return ([BitConverter]::ToString($h) -replace "-", "")
}
# 1) re-hash MANIFEST_SHA256.csv
$man = Import-Csv (Join-Path $pkg "06_REPORT\MANIFEST_SHA256.csv")
$mis = 0; $ok = 0
foreach ($r in $man) {
    $p = Join-Path $pkg $r.path
    if (-not (Test-Path -LiteralPath $p)) { Write-Output ("MISSING FILE: {0}" -f $r.path); $mis++; continue }
    $h = Get-FileSha256Upper $p
    if ($h -ne $r.sha256) { Write-Output ("HASH MISMATCH: {0}" -f $r.path); $mis++ } else { $ok++ }
}
Write-Output ("MANIFEST re-hash: {0}/{1} OK, {2} mismatches" -f $ok, $man.Count, $mis)
# 2) pokrycie plikow pakietu
$pkgFiles = Get-ChildItem $pkg -Recurse -File | ForEach-Object { [IO.Path]::GetFullPath($_.FullName).Substring([IO.Path]::GetFullPath($pkg).Length + 1) -replace "\\","/" }
$manPaths = $man.path
$ai = Import-Csv (Join-Path $pkg "06_REPORT\artifact_index.csv")
$aiPaths = $ai.relpath
Write-Output ("Package files: {0}; manifest rows: {1}; artifact_index rows: {2}" -f $pkgFiles.Count, $manPaths.Count, $aiPaths.Count)
$notInMan = $pkgFiles | Where-Object { $_ -notin $manPaths }
Write-Output ("Package files NOT in manifest ({0}): {1}" -f @($notInMan).Count, ($notInMan -join " | "))
$manNotInPkg = $manPaths | Where-Object { $_ -notin $pkgFiles }
Write-Output ("Manifest rows NOT in package ({0}): {1}" -f @($manNotInPkg).Count, ($manNotInPkg -join " | "))
$diffManAi = @(($manPaths | Where-Object { $_ -notin $aiPaths }) + ($aiPaths | Where-Object { $_ -notin $manPaths }))
Write-Output ("man vs artifact_index set difference ({0}): {1}" -f $diffManAi.Count, ($diffManAi -join " | "))
# 3) artifact_index re-hash + rozmiary
$aiMis = 0; $aiOk = 0
foreach ($r in $ai) {
    $p = Join-Path $pkg $r.relpath
    if (-not (Test-Path -LiteralPath $p)) { Write-Output ("AI MISSING: {0}" -f $r.relpath); $aiMis++; continue }
    $fi = Get-Item -LiteralPath $p
    $h = Get-FileSha256Upper $p
    if ($h -ne $r.sha256 -or $fi.Length -ne [int64]$r.size_bytes) { Write-Output ("AI MISMATCH: {0}" -f $r.relpath); $aiMis++ } else { $aiOk++ }
}
Write-Output ("artifact_index re-hash: {0}/{1} OK, {2} mismatches" -f $aiOk, $ai.Count, $aiMis)
# 4) SCRIPT_SHA256 last-row (ostatni poprawny hash na skrypt)
$ss = Get-Content (Join-Path $pkg "00_CONTROL\SCRIPT_SHA256.csv") | Select-Object -Skip 1
$lastHash = @{}
foreach ($line in $ss) {
    $parts = $line -split ",", 2
    if ($parts.Count -eq 2 -and $parts[1] -match "^[0-9A-F]{64}$") { $lastHash[$parts[0]] = $parts[1] }
}
Write-Output ("Distinct scripts with operative (last) hash: {0}" -f $lastHash.Count)
$ssOk = 0; $ssBad = 0
foreach ($k in @($lastHash.Keys)) {
    $p = Join-Path $pkg ("00_CONTROL\" + $k)
    if (-not (Test-Path -LiteralPath $p)) { Write-Output ("SCRIPT MISSING: {0}" -f $k); $ssBad++; continue }
    $h = Get-FileSha256Upper $p
    if ($h -eq $lastHash[$k]) { $ssOk++ } else { Write-Output ("SCRIPT HASH MISMATCH: {0} (csv {1} vs disk {2})" -f $k, $lastHash[$k], $h); $ssBad++ }
}
Write-Output ("SCRIPT_SHA256 last-row: {0} OK, {1} bad (claim: 20/20)" -f $ssOk, $ssBad)
# 5) repo package vs lokalny 99_Audits (179 vs 190)
$loc = "D:\Eudoria_Reconstruction\99_Audits\PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913"
$locFiles = Get-ChildItem $loc -Recurse -File | ForEach-Object { [IO.Path]::GetFullPath($_.FullName).Substring([IO.Path]::GetFullPath($loc).Length + 1) -replace "\\","/" }
$repoOnly = $pkgFiles | Where-Object { $_ -notin $locFiles }
$locOnly = $locFiles | Where-Object { $_ -notin $pkgFiles }
Write-Output ("Repo-only files ({0}): {1}" -f @($repoOnly).Count, ($repoOnly -join " | "))
Write-Output ("Local-only files ({0}):" -f @($locOnly).Count)
@($locOnly) | Sort-Object | ForEach-Object { Write-Output ("  LOCAL-ONLY: $_") }
