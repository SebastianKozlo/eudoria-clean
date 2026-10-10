# QC DUTY 2 (part 1) — independent hash recomputation of every pinned input.
# FRESH INTERNAL QC (pe-master-auditor, fresh session). Read-only against originals.
# Output: JSON to stdout (captured to q1_hash_recompute.json by the caller).

$ErrorActionPreference = "Stop"

$targets = @(
    @{ id = "DESKTOP_POST_AUDIT_REPORT";     path = "C:\Users\User\Documents\ChatGPT\PE\PE_TEMPLATE_FINAL_CONSUMER_DESKTOP_POST_AUDIT_F99FEBE_20261009\REPORT.md" },
    @{ id = "DESKTOP_COUNTERMODELS_JSON";    path = "C:\Users\User\Documents\ChatGPT\PE\PE_TEMPLATE_FINAL_CONSUMER_DESKTOP_POST_AUDIT_F99FEBE_20261009\CLAIM_SUFFICIENCY_COUNTERMODELS.json" },
    @{ id = "DESKTOP_DEEP_CHECK_REPORT";     path = "C:\Users\User\Documents\ChatGPT\PE\PE_GAMEBRYO_SCENE_TOOLS_DEEP_CHECK_20261009\REPORT.md" },
    @{ id = "DESKTOP_DEEP_CHECK_PROBE_PY";   path = "C:\Users\User\Documents\ChatGPT\PE\PE_GAMEBRYO_SCENE_TOOLS_DEEP_CHECK_20261009\probe_tools.py" },
    @{ id = "DESKTOP_PLACEMENT_REPORT";      path = "C:\Users\User\Documents\ChatGPT\PE\PE_GAMEBRYO_PLACEMENT_MECHANISMS_LOCAL_RESEARCH_20261009\REPORT.md" },
    @{ id = "DESKTOP_NATIVE_TRANSFORM_PROBE"; path = "C:\Users\User\Documents\ChatGPT\PE\PE_GAMEBRYO_PLACEMENT_MECHANISMS_LOCAL_RESEARCH_20261009\native_transform_probe.py" },
    @{ id = "CONTRACT";                       path = "C:\Users\User\Documents\ChatGPT\PE\OPENCODE_ENGINE_ASSISTED_PE_SCENE_INSPECTION_R1_20261009\OPENCODE_GAMEBRYO_ENGINE_ASSISTED_PE_SCENE_INSPECTION_R1.md" },
    @{ id = "SCENEGRAPHPRINTER_EXE";          path = "D:\gamebyroengine\extracted\Gb12_Source\Tools\DeveloperTools\SceneGraphPrinter\Win32\VC71\SceneGraphPrinter.exe" },
    @{ id = "MSVCP71_DLL";                    path = "D:\gamebyroengine\extracted\Gb112_tools_setup\MSVCP71.DLL" },
    @{ id = "MSVCR71_DLL";                    path = "D:\gamebyroengine\extracted\Gb112_tools_setup\MSVCR71.DLL" },
    @{ id = "MODELS_BNT";                     path = "D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt" },
    @{ id = "PIN_218757_NIF";                 path = "D:\Eudoria_Reconstruction\99_Audits\PE_GAMEBRYO_ORACLE_TOOL_R1_20261003\sandbox\payloads\218757.nif" },
    @{ id = "GB12_ORACLE_EXE";                path = "D:\gamebyroengine\extracted\gb12_build\bin\gb12_oracle.exe" },
    @{ id = "ENTROPIA_EXE";                   path = "D:\Eudoria_Reconstruction\pcg_install\Entropia.exe" }
)

$results = @()
foreach ($t in $targets) {
    if (-not (Test-Path -LiteralPath $t.path)) {
        $results += [pscustomobject]@{ id = $t.id; path = $t.path; exists = $false }
        continue
    }
    $item = Get-Item -LiteralPath $t.path
    $hash = (Get-FileHash -LiteralPath $t.path -Algorithm SHA256).Hash.ToLower()
    $results += [pscustomobject]@{ id = $t.id; path = $t.path; exists = $true; size = $item.Length; sha256 = $hash }
}

$results | ConvertTo-Json -Depth 4
