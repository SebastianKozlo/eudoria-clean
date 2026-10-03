# phaseA_inventory.ps1 - PE_GAMEBRYO_ORACLE_TOOL_R1_20261003 Batch E1 Phase A
# STATIC / LOCAL / READ-ONLY on D:\gamebyroengine. Outputs ONLY to run sandbox.
$ErrorActionPreference = 'Stop'
$root  = 'D:\gamebyroengine'
$sbx   = 'D:\Eudoria_Reconstruction\99_Audits\PE_GAMEBRYO_ORACLE_TOOL_R1_20261003\sandbox'
$seven = 'C:\Program Files\7-Zip\7z.exe'
$out   = Join-Path $sbx 'phaseA'
New-Item -ItemType Directory -Force -Path (Join-Path $sbx 'listings') | Out-Null
New-Item -ItemType Directory -Force -Path $out | Out-Null

$inv = @{
  run_id = 'PE_GAMEBRYO_ORACLE_TOOL_R1_20261003'
  phase  = 'A_forensic_inventory'
  started_utc = (Get-Date).ToUniversalTime().ToString('o')
  top_level = @(); archives = @(); dirs = @(); exes = @(); libs = @()
  small_dumps = @(); listings = @(); notes = @()
}

# ---------- 0. top-level recount ----------
$tl = Get-ChildItem -LiteralPath $root
$inv.top_level_count = $tl.Count
foreach ($i in $tl) {
  if ($i.PSIsContainer) { $inv.top_level += @{ name=$i.Name; type='directory' } }
  else { $inv.top_level += @{ name=$i.Name; type='file'; size=$i.Length } }
}

# ---------- 1. archive SHA256 + 7z listings ----------
foreach ($f in ($tl | Where-Object { -not $_.PSIsContainer })) {
  $t0 = Get-Date
  $h = (Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256).Hash
  $inv.archives += @{ name=$f.Name; size=$f.Length; sha256=$h
                     hash_seconds=[math]::Round(((Get-Date)-$t0).TotalSeconds,1) }
  $listName = ($f.Name -replace '[^A-Za-z0-9_.-]', '_') + '.txt'
  $listPath = Join-Path $sbx "listings\$listName"
  $errPath  = Join-Path $sbx "listings\err_$listName"
  $t1 = Get-Date
  & $seven l -ba $f.FullName > $listPath 2> $errPath
  $exit = $LASTEXITCODE
  $tailLines = @(Get-Content -LiteralPath $listPath -Tail 3)
  $inv.listings += @{ archive=$f.Name; listing_rel=("sandbox\listings\"+$listName)
                     sevenzip_exit=$exit; listing_seconds=[math]::Round(((Get-Date)-$t1).TotalSeconds,1)
                     listing_bytes=(Get-Item -LiteralPath $listPath).Length
                     footer=($tailLines -join ' | ') }
}

# ---------- 2. directory censuses (recursive file_count + total bytes + structure summary) ----------
foreach ($d in ($tl | Where-Object { $_.PSIsContainer })) {
  $files = Get-ChildItem -LiteralPath $d.FullName -Recurse -File
  $cnt = @($files).Count
  $sum = ($files | Measure-Object -Property Length -Sum).Sum
  if ($null -eq $sum) { $sum = 0 }
  $subs = @()
  foreach ($s in (Get-ChildItem -LiteralPath $d.FullName -Directory)) {
    $sf = Get-ChildItem -LiteralPath $s.FullName -Recurse -File
    $ssum = ($sf | Measure-Object -Property Length -Sum).Sum
    if ($null -eq $ssum) { $ssum = 0 }
    $subs += ('{0}={1}f/{2}B' -f $s.Name, @($sf).Count, $ssum)
  }
  # top-level loose files (bounded 40)
  $loose = @()
  foreach ($lf in (@(Get-ChildItem -LiteralPath $d.FullName -File) | Select-Object -First 40)) {
    $loose += ('{0}={1}B' -f $lf.Name, $lf.Length)
  }
  $inv.dirs += @{ name=$d.Name; file_count=$cnt; total_bytes=$sum
                  structure_subdirs=($subs -join '; '); loose_files=($loose -join '; ') }
}

# ---------- 3. exe census (path, size, sha256, PE version evidence) ----------
$allFiles = Get-ChildItem -LiteralPath $root -Recurse -File
$exes = @($allFiles | Where-Object { $_.Extension -ieq '.exe' })
foreach ($e in $exes) {
  $vi = $e.VersionInfo
  $inv.exes += @{
    rel_path = $e.FullName.Substring($root.Length + 1)
    size = $e.Length
    sha256 = (Get-FileHash -LiteralPath $e.FullName -Algorithm SHA256).Hash
    pe_company = $vi.CompanyName; pe_file_version = $vi.FileVersion
    pe_product = $vi.ProductName; pe_product_version = $vi.ProductVersion
    pe_description = $vi.FileDescription
  }
}

# ---------- 4. NiMain.lib census (all copies hashed) ----------
$libs = @($allFiles | Where-Object { $_.Name -like 'NiMain.lib*' })
foreach ($l in $libs) {
  $inv.libs += @{ rel_path = $l.FullName.Substring($root.Length + 1); size = $l.Length
                  sha256 = (Get-FileHash -LiteralPath $l.FullName -Algorithm SHA256).Hash }
}

# ---------- 5. small evidence dumps (version identity sources) ----------
function Dump-Text($label, $path) {
  if (Test-Path -LiteralPath $path) {
    $bytes = [System.IO.File]::ReadAllBytes($path)
    $txt = [System.Text.Encoding]::GetEncoding('Windows-1252').GetString($bytes)
    $lines = $txt -split "`r?`n"
    $numbered = New-Object System.Collections.Generic.List[string]
    for ($i = 0; $i -lt $lines.Count; $i++) { $numbered.Add(('{0:D4}: {1}' -f ($i+1), $lines[$i])) }
    $script:inv.small_dumps += @{ label=$label; path=$path; size=$bytes.Length
      sha256=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash
      content=($numbered -join "`n") }
  } else { $script:inv.notes += "MISSING dump target: $label at $path" }
}
Dump-Text 'GB12_NiVersion_h_SDK_Win32'       "$root\extracted\Gb12_Source\SDK\Win32\Include\NiVersion.h"
Dump-Text 'GB12_NiVersion_h_CoreLibs'        "$root\extracted\Gb12_Source\CoreLibs\NiSystem\NiVersion.h"
Dump-Text 'GB12_NiViewerStrings_cpp'         "$root\extracted\Gb12_Source\CoreLibs\NiMain\NiViewerStrings.cpp"
Dump-Text 'GB12_NiVersion_h_gb12build'       "$root\extracted\gb12_build\src\CoreLibs\NiSystem\NiVersion.h"
Dump-Text 'GB26_NiVersion_h'                 "$root\extracted\Gb26_src\NiVersion.h"
Dump-Text 'GB26_NiViewerStrings_cpp'         "$root\extracted\Gb26_src\NiViewerStrings.cpp"
Dump-Text 'GB112_NiVersion_h_installed'      "$root\Gamebryo 1.1.2 Evaluation\SDK\Win32\Include\NiVersion.h"
Dump-Text 'GB112_license_txt'                "$root\Gamebryo 1.1.2 Evaluation\license.txt"
Dump-Text 'GB112_GbEvaluationSetup_dat'       "$root\Gamebryo 1.1.2 Evaluation\GbEvaluationSetup.dat"

# ---------- 6. finalize ----------
$inv.completed_utc = (Get-Date).ToUniversalTime().ToString('o')
$invJson = $inv | ConvertTo-Json -Depth 6
[System.IO.File]::WriteAllText((Join-Path $out 'inventory_data.json'), $invJson, (New-Object System.Text.UTF8Encoding($false)))
Write-Output ('PHASEA_DONE top_level=' + $inv.top_level_count + ' archives=' + $inv.archives.Count + ' dirs=' + $inv.dirs.Count + ' exes=' + $inv.exes.Count + ' libs=' + $inv.libs.Count + ' dumps=' + $inv.small_dumps.Count)
foreach ($a in $inv.archives) { Write-Output ('ARCHIVE ' + $a.name + ' ' + $a.size + ' ' + $a.sha256 + ' hash_s=' + $a.hash_seconds) }
foreach ($l in $inv.listings) { Write-Output ('LISTING ' + $l.archive + ' exit=' + $l.sevenzip_exit + ' s=' + $l.listing_seconds + ' bytes=' + $l.listing_bytes + ' FOOTER: ' + $l.footer) }
foreach ($d in $inv.dirs) { Write-Output ('DIR ' + $d.name + ' files=' + $d.file_count + ' bytes=' + $d.total_bytes) }
Write-Output ('P4_GB112_VC71_ReleaseLib: ' + (($inv.libs | Where-Object { $_.rel_path -like 'Gamebryo 1.1.2 Evaluation\SDK\Win32\Lib\VC71\ReleaseLib\NiMain.lib' } | ForEach-Object { $_.sha256 }) -join ','))
