# WORK-AUDIT (audytor: Work-Audit, audyt: audyt-935-pub-persist-20260914-0648) — plik audytora, NIE jest czescia pracy wykonawcy
$ErrorActionPreference = "Stop"
function Get-FileSha256Upper([string]$path) {
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try { $fs = [System.IO.File]::OpenRead($path); try { $hash = $sha.ComputeHash($fs) } finally { $fs.Dispose() } } finally { $sha.Dispose() }
    return ([BitConverter]::ToString($hash) -replace "-", "")
}
$targets = @(
    "D:\Eudoria_Reconstruction\pcg_install\Entropia.exe",
    "D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs",
    "D:\Eudoria_Reconstruction\99_Audits\PE_935_ORIGIN_SEAM_DESKTOP_AUDIT_R1_20260913",
    "D:\Eudoria_Reconstruction\99_Audits\PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913",
    "D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913",
    "D:\Eudoria_Reconstruction\99_Audits\PE_935_STATIC_PLACEMENT_ROUND1_20260913",
    "D:\Eudoria_Reconstruction\99_Audits\PE_935_STATIC_PLACEMENT_DESKTOP_AUDIT_R1_20260913",
    "D:\Eudoria_Reconstruction\99_Audits\PE_935_STATIC_INSTANCE_TRACE_R1_20260913",
    "D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913",
    "D:\Eudoria_Reconstruction\99_Audits\PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913"
)
$ms = New-Object System.IO.MemoryStream
$enc = [System.Text.Encoding]::ASCII
$totalFiles = 0
foreach ($t in $targets) {
    if (Test-Path -LiteralPath $t -PathType Leaf) {
        $s = Get-FileSha256Upper $t
        $bytes = $enc.GetBytes($s)
        $ms.Write($bytes, 0, $bytes.Length)
        $totalFiles++
        Write-Output ("FILE  {0} : {1} ({2} B)" -f $t, ($s.Substring(0,16)+"..."), (Get-Item -LiteralPath $t).Length)
    } elseif (Test-Path -LiteralPath $t -PathType Container) {
        $dirCount = 0
        $stack = New-Object System.Collections.Stack
        $stack.Push($t)
        while ($stack.Count -gt 0) {
            $dp = $stack.Pop()
            $subDirs = Get-ChildItem -LiteralPath $dp -Directory | Sort-Object Name
            foreach ($sd in $subDirs) { $stack.Push($sd.FullName) }
            $files = Get-ChildItem -LiteralPath $dp -File | Sort-Object Name
            foreach ($f in $files) {
                $rel = [System.IO.Path]::GetFullPath($f.FullName).Substring([System.IO.Path]::GetFullPath($t).Length + 1)
                $s = Get-FileSha256Upper $f.FullName
                $chunk = $rel + "|" + $s
                $bytes = $enc.GetBytes($chunk)
                $ms.Write($bytes, 0, $bytes.Length)
                $dirCount++
                $totalFiles++
            }
        }
        Write-Output ("DIR   {0} : {1} files" -f $t, $dirCount)
    } else { Write-Output ("MISSING {0}" -f $t) }
}
$ms.Position = 0
$sha2 = [System.Security.Cryptography.SHA256]::Create()
try { $hash = $sha2.ComputeHash($ms) } finally { $sha2.Dispose() }
$composite = ([BitConverter]::ToString($hash) -replace "-", "")
$ms.Dispose()
Write-Output ("TOTAL FILES: {0}" -f $totalFiles)
Write-Output ("COMPOSITE: {0}" -f $composite)
Write-Output "CLAIMED:   A606CF52CC6804702C469777013115A80328539EADC27A9053F4F199877783D0 (1022 files)"
