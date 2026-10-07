# qc_ind_manifest_rehash.ps1 - PE-MASTER-AUDITOR independent QC, part 5.
# Independent manifest re-hash using .NET SHA256 (a different implementation
# from the executor's Python hashlib), encoding checks (BOM/CRLF/UTF-8), the
# manifest bijection vs the physical package, and BASE blob identity of the
# historical packages. ASCII-only source (PS 5.1 reads no-BOM ps1 as ANSI).

$ErrorActionPreference = "Stop"
$PKG = "D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007"
$REPO = "D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"

Write-Output "=== MANIFEST RE-HASH (independent .NET implementation) ==="
$manifest = Join-Path $PKG "MANIFEST_SHA256.csv"
$rows = @()
Get-Content -LiteralPath $manifest | ForEach-Object {
    if ($_ -and ($_ -notmatch "^#") -and ($_ -ne "path,size_bytes,sha256")) {
        $parts = $_ -split ","
        $rows += ,@($parts[0], [long]$parts[1], $parts[2])
    }
}
Write-Output ("MANIFEST data rows parsed: {0}" -f $rows.Count)

$mismatch = @()
$sha = [System.Security.Cryptography.SHA256]::Create()
foreach ($r in $rows) {
    $rel = $r[0]
    $p = Join-Path $REPO ($rel -replace "/", "\")
    if (-not (Test-Path -LiteralPath $p)) { $mismatch += "MISSING: $rel"; continue }
    $bytes = [System.IO.File]::ReadAllBytes($p)
    if ($bytes.Length -ne $r[1]) { $mismatch += "SIZE: $rel ($($bytes.Length) != $($r[1]))"; continue }
    $hash = ([System.BitConverter]::ToString($sha.ComputeHash($bytes)) -replace "-", "").ToLower()
    if ($hash -ne $r[2].ToLower()) { $mismatch += "SHA: $rel" }
}
if ($mismatch.Count) { Write-Output ("Re-hash mismatches: {0}" -f ($mismatch -join "; ")) } else { Write-Output "Re-hash mismatches: NONE (27/27 size+SHA256 match by the .NET implementation)" }

# bijection vs physical files (executor-phase scope = package minus manifest minus my QC dir)
$physical = Get-ChildItem -Recurse -File -LiteralPath $PKG | Where-Object { $_.FullName -notmatch "__pycache__" } | ForEach-Object { $_.FullName.Substring($REPO.Length + 1) -replace "\\", "/" }
$physicalRel = @($physical | Where-Object { $_ -notmatch "00_CONTROL_INTERNAL_QC" })
$listed = @($rows | ForEach-Object { $_[0] })
$extra = @($listed | Where-Object { $physicalRel -notcontains $_ })
$missing = @($physicalRel | Where-Object { $listed -notcontains $_ })
Write-Output ("Bijection: physical (excl. manifest + my QC dir) = {0}; manifest rows = {1}; missing = {2}; extra = {3}" -f $physicalRel.Count, $listed.Count, $(if ($missing.Count) { ($missing -join "; ") } else { "NONE" }), $(if ($extra.Count) { ($extra -join "; ") } else { "NONE" }))
$qcCount = @($physical | Where-Object { $_ -match "00_CONTROL_INTERNAL_QC" }).Count
Write-Output ("NOTE: 00_CONTROL_INTERNAL_QC (my QC records) = {0} files - OUT of the executor-phase manifest scope by design; the persistence phase regenerates the manifest over the final package" -f $qcCount)

Write-Output ""
Write-Output "=== ENCODING (all package files incl. manifest + my QC dir) ==="
$encFails = @()
Get-ChildItem -Recurse -File -LiteralPath $PKG | Where-Object { $_.FullName -notmatch "__pycache__" } | ForEach-Object {
    $raw = [System.IO.File]::ReadAllBytes($_.FullName)
    if ($raw.Length -ge 3 -and $raw[0] -eq 0xEF -and $raw[1] -eq 0xBB -and $raw[2] -eq 0xBF) { $encFails += "$($_.Name): BOM" }
    $txt = [System.Text.Encoding]::UTF8.GetString($raw)
    if ($txt.Contains("`r`n")) { $encFails += "$($_.Name): CRLF" }
    try { [System.Text.Encoding]::GetEncoding("utf-8", [System.Text.EncoderFallback]::ExceptionFallback, [System.Text.DecoderFallback]::ExceptionFallback).GetCharCount($raw) | Out-Null } catch { $encFails += "$($_.Name): not-strict-UTF8" }
}
if ($encFails.Count) { Write-Output ("Encoding violations: {0}" -f ($encFails -join "; ")) } else { Write-Output "Encoding violations: NONE (UTF-8 no-BOM, LF-only, strict-decodable)" }

Write-Output ""
Write-Output "=== HISTORICAL PACKAGES (BASE blob identity - my own method) ==="
foreach ($pkgRel in @("docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006", "docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007")) {
    $files = git -C $REPO ls-tree -r d65fa12e --name-only $pkgRel
    $n = 0; $mm = @()
    foreach ($f in $files) {
        $n++
        $blob = (git -C $REPO rev-parse "d65fa12e:$f").Trim()
        $diskP = Join-Path $REPO ($f -replace "/", "\")
        if (-not (Test-Path -LiteralPath $diskP)) { $mm += "MISSING $f"; continue }
        $content = [System.IO.File]::ReadAllBytes($diskP)
        $sha1 = [System.Security.Cryptography.SHA1]::Create()
        $prefix = [System.Text.Encoding]::ASCII.GetBytes("blob $($content.Length)")
        $ms = New-Object System.IO.MemoryStream
        $ms.Write($prefix, 0, $prefix.Length)
        $ms.WriteByte(0)
        $ms.Write($content, 0, $content.Length)
        $h = ([System.BitConverter]::ToString($sha1.ComputeHash($ms.ToArray())) -replace "-", "").ToLower()
        if ($h -ne $blob) { $mm += "MISMATCH $f" }
    }
    Write-Output ("{0}: {1} tracked-at-BASE files; blob-identity mismatches: {2}" -f (Split-Path $pkgRel -Leaf), $n, $(if ($mm.Count) { ($mm -join "; ") } else { "NONE ($n/$n)" }))
}
