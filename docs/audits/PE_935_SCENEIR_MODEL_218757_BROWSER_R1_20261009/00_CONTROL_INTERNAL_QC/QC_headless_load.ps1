# QC_headless_load.ps1 — internal QC (pe-master-auditor): ONE independent headless Edge load
$ErrorActionPreference = 'Stop'
$qc = "D:\Eudoria_Reconstruction\12_WebGame\pe-sceneir-218757-r1\docs\audits\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\00_CONTROL_INTERNAL_QC"
$profile = "C:\Users\User\AppData\Local\Temp\opencode\qc_sceneir_headless_profile"
New-Item -ItemType Directory -Force -Path $profile | Out-Null
$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$proc = Start-Process -FilePath $edge -ArgumentList @(
  "--headless=new",
  "--user-data-dir=$profile",
  "--virtual-time-budget=30000",
  "--disable-extensions",
  "--no-first-run",
  "--dump-dom",
  "http://127.0.0.1:8146/"
) -RedirectStandardOutput "$qc\QC_HEADLESS_DOM_8146.html" -RedirectStandardError "$qc\QC_HEADLESS_STDERR_8146.txt" -PassThru -NoNewWindow
$proc.WaitForExit(60000) | Out-Null
Write-Output "EDGE_EXIT_CODE=$($proc.ExitCode)"
$dom = Get-Content "$qc\QC_HEADLESS_DOM_8146.html" -Raw
Write-Output ("DOM_CHARS=" + $dom.Length)
Write-Output ("DOM_BYTES=" + (Get-Item "$qc\QC_HEADLESS_DOM_8146.html").Length)
$status = if ($dom -match 'data-load-status="([^"]+)"') { $Matches[1] } else { "(none)" }
Write-Output "DATA_LOAD_STATUS=$status"
Write-Output ("HAS_CANVAS=" + ($dom -match 'view-canvas'))
Write-Output ("HAS_DIAG=" + ($dom -match 'diag-identity'))
if ($dom -match 'payload SHA256 ([0-9a-f]{64})') { Write-Output "PAYLOAD_SHA_IN_DOM=$($Matches[1])" }
if ($dom -match 'imported ([0-9]+) / currently visible ([0-9]+)') { Write-Output "MESH_LEDGER=imported $($Matches[1]) visible $($Matches[2])" }
