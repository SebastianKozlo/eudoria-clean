# QC_start_server.ps1 — internal QC server launcher (pe-master-auditor)
$ErrorActionPreference = 'Stop'
$qc = "D:\Eudoria_Reconstruction\12_WebGame\pe-sceneir-218757-r1\docs\audits\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\00_CONTROL_INTERNAL_QC"
$wt  = "D:\Eudoria_Reconstruction\12_WebGame\pe-sceneir-218757-r1"
$env:PORT = "8146"
$p = Start-Process -FilePath "node" -ArgumentList "compat\server-sceneir.mjs" -WorkingDirectory $wt -RedirectStandardOutput "$qc\QC_server_8146_stdout.txt" -RedirectStandardError "$qc\QC_server_8146_stderr.txt" -PassThru -NoNewWindow
$env:PORT = $null
Start-Sleep -Seconds 5
Write-Output "QC_SERVER_PID=$($p.Id) HAS_EXITED=$($p.HasExited)"
Write-Output "--- stdout ---"
Get-Content "$qc\QC_server_8146_stdout.txt"
Write-Output "--- stderr ---"
Get-Content "$qc\QC_server_8146_stderr.txt"
"$($p.Id)" | Out-File "$qc\QC_server_8146_pid.txt" -Encoding ascii
