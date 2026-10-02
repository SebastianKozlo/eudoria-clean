# s6_before_copies.ps1 — BEFORE-copy discipline for DESKTOP_CORRECTION_R1
# Byte-for-byte copies of every artifact this correction will modify, into
# 00_CONTROL\DESKTOP_CORRECTION_R1\BEFORE\<relative path>, plus size+SHA256
# recorded in BEFORE_COPIES_INDEX.json (written once, append-only afterwards).
$ErrorActionPreference = 'Stop'
$pkg = 'D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002'
$beforeRoot = Join-Path $pkg '00_CONTROL\DESKTOP_CORRECTION_R1\BEFORE'

$targets = @(
  '02_ANALYSIS\FIELD_TO_DESTINATION_TRACE.md',
  '02_ANALYSIS\CONSUMER_TRACE.md',
  '02_ANALYSIS\SEMANTIC_ASSESSMENT.md',
  '02_ANALYSIS\NEGATIVE_CONTROLS.md',
  '02_ANALYSIS\DESTINATION_CONSUMER_CENSUS.json',
  '02_ANALYSIS\BLAST_RADIUS.md',
  '06_REPORT\REPORT.md',
  '06_REPORT\EVIDENCE_INDEX.md',
  '06_REPORT\HANDOFF.md'
)

$index = New-Object System.Collections.Generic.List[string]
$index.Add('{')
$index.Add(' "run_id": "PE_935_20002_PAYLOAD30_DESKTOP_CORRECTION_R1_20261002",')
$index.Add(' "record_class": "BEFORE_COPIES_INDEX (executor BEFORE-copy discipline; byte-for-byte copies + size + SHA256 at copy time)",')
$index.Add(' "copied_at_utc": "' + [DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ss.fffZ') + '",')
$index.Add(' "copies": [')
$i = 0
foreach ($t in $targets) {
  $src = Join-Path $pkg $t
  $dst = Join-Path $beforeRoot $t
  $dstDir = Split-Path $dst -Parent
  if (-not (Test-Path -LiteralPath $dstDir)) { New-Item -ItemType Directory -Path $dstDir -Force | Out-Null }
  Copy-Item -LiteralPath $src -Destination $dst -Force
  $fi = Get-Item -LiteralPath $dst
  $sha = (Get-FileHash -LiteralPath $dst -Algorithm SHA256).Hash
  # byte-for-byte verification
  $srcSha = (Get-FileHash -LiteralPath $src -Algorithm SHA256).Hash
  if ($srcSha -ne $sha) { throw "BEFORE copy mismatch for $t" }
  $comma = if ($i -lt $targets.Count - 1) { ',' } else { '' }
  $index.Add('  {"relative_path": "' + ($t -replace '\\','/') + '", "size_bytes": ' + $fi.Length + ', "sha256": "' + $sha + '"}' + $comma)
  $i++
}
$index.Add(' ]')
$index.Add('}')
$indexPath = Join-Path $beforeRoot 'BEFORE_COPIES_INDEX.json'
$index | Set-Content -LiteralPath $indexPath -Encoding UTF8
Write-Output "BEFORE copies complete: $($targets.Count) files"
Write-Output "index: $indexPath"
Get-ChildItem -LiteralPath $beforeRoot -Recurse -File | ForEach-Object { Write-Output ("  " + $_.FullName.Substring($beforeRoot.Length+1) + " (" + $_.Length + " B)") }
