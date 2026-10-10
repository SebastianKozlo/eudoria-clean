# QC DUTY 3 — independent re-execution of native SDK graph controls.
# FRESH INTERNAL QC (pe-master-auditor). My OWN invocation of the pinned stock
# printer with child-process PATH DLL exposure (same class as the executor).
# Read-only against all originals; raw outputs captured under 00_CONTROL_INTERNAL_QC.

$ErrorActionPreference = "Stop"
$exe = "D:\gamebyroengine\extracted\Gb12_Source\Tools\DeveloperTools\SceneGraphPrinter\Win32\VC71\SceneGraphPrinter.exe"
$dllDir = "D:\gamebyroengine\extracted\Gb112_tools_setup"
$qc = "D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009\00_CONTROL_INTERNAL_QC"

# Pre-execution identity checks (fail-closed)
$exeHash = (Get-FileHash -LiteralPath $exe -Algorithm SHA256).Hash.ToLower()
if ($exeHash -ne "fd693af2d713c021b959fc7506200173435307c8fccc24ccd5851dfceb241c7c") { throw "PRINTER IDENTITY MISMATCH" }
"printer sha256: $exeHash (MATCH pin)"

$cases = @(
    @{ id = "QC_POS_WORLD";   input = "D:\gamebyroengine\extracted\Gb12_Source\Samples\Tutorials\Data\Win32\WORLD.nif" },
    @{ id = "QC_POS_OBJECT";  input = "D:\gamebyroengine\extracted\Gb12_Source\Samples\Tutorials\Data\Win32\OBJECT.NIF" },
    @{ id = "QC_SYNTH_TRANSLATED_PARENT"; input = "D:\Eudoria_Reconstruction\99_Audits\PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009\01_SDK_fixtures\synthetic\TRANSLATED_PARENT.nif" }
)

$results = @()
foreach ($c in $cases) {
    $inHash = (Get-FileHash -LiteralPath $c.input -Algorithm SHA256).Hash.ToLower()
    $inSize = (Get-Item -LiteralPath $c.input).Length
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $exe
    $psi.Arguments = "-in `"$($c.input)`" -trans -extra -prop -geom -bs -mem"
    $psi.UseShellExecute = $false
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.WorkingDirectory = $qc
    # CHILD_PROCESS_PATH_DLL_EXPOSURE: prepend legacy runtime dir to child PATH only
    $psi.EnvironmentVariables["PATH"] = "$dllDir;" + $env:PATH
    $p = New-Object System.Diagnostics.Process
    $p.StartInfo = $psi
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    [void]$p.Start()
    $stdout = $p.StandardOutput.ReadToEnd()
    $stderr = $p.StandardError.ReadToEnd()
    if (-not $p.WaitForExit(30000)) {
        $p.Kill(); $results += [pscustomobject]@{ id=$c.id; exit="TIMEOUT" }; continue
    }
    $sw.Stop()
    $exit = $p.ExitCode
    $stdoutPath = Join-Path $qc ("qc3_" + $c.id + ".stdout.txt")
    $stderrPath = Join-Path $qc ("qc3_" + $c.id + ".stderr.txt")
    [System.IO.File]::WriteAllText($stdoutPath, $stdout)
    [System.IO.File]::WriteAllText($stderrPath, $stderr)
    # quick visit count (numbered lines starting with digits+dot)
    $visitLines = ($stdout -split "`r?`n" | Where-Object { $_ -match '^\s*\d+[\.\)]' }).Count
    $results += [pscustomobject]@{
        id = $c.id; input = $c.input; input_size = $inSize; input_sha256 = $inHash
        exit_code = $exit; elapsed_ms = $sw.ElapsedMilliseconds
        stdout_size = $stdout.Length; stderr_size = $stderr.Length
        stderr_text = $stderr.Trim(); numbered_visit_lines = $visitLines
        stdout_path = $stdoutPath; stderr_path = $stderrPath
    }
}
"---"
$results | ConvertTo-Json -Depth 3
# post-run printer identity re-check
$postHash = (Get-FileHash -LiteralPath $exe -Algorithm SHA256).Hash.ToLower()
"post_run_printer_sha256: $postHash"
