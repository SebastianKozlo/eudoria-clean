# z1_matrix_consistency.ps1 - G4 gate: machine matrix == report table
# Converts claims_matrix.csv -> claims_matrix.json and verifies row-count/ID consistency
# between the CSV, the JSON, and the markdown table in CLAIMS_MATRIX.md.
# Run: powershell -File z1_matrix_consistency.ps1
# Output: ../03_EVIDENCE/Z1_MATRIX_CONSISTENCY.json + ../02_ANALYSIS/claims_matrix.json

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$csvPath = Join-Path $root "02_ANALYSIS\claims_matrix.csv"
$mdPath  = Join-Path $root "02_ANALYSIS\CLAIMS_MATRIX.md"
$jsonOut = Join-Path $root "02_ANALYSIS\claims_matrix.json"
$reportOut = Join-Path $root "03_EVIDENCE\Z1_MATRIX_CONSISTENCY.json"

# --- parse CSV (simple RFC4180-style parser: quoted fields, doubled quotes) ---
function Import-CsvStrict([string]$path) {
    $text = [System.IO.File]::ReadAllText($path)
    $rows = New-Object System.Collections.Generic.List[object]
    $header = $null
    $field = New-Object System.Text.StringBuilder
    $row = New-Object System.Collections.Generic.List[string]
    $inQuotes = $false
    $i = 0
    while ($i -lt $text.Length) {
        $c = $text[$i]
        if ($inQuotes) {
            if ($c -eq '"') {
                if (($i + 1) -lt $text.Length -and $text[$i+1] -eq '"') { [void]$field.Append('"'); $i++ }
                else { $inQuotes = $false }
            } else { [void]$field.Append($c) }
        } else {
            if ($c -eq '"') { $inQuotes = $true }
            elseif ($c -eq ',') { $row.Add($field.ToString()); [void]$field.Clear() }
            elseif ($c -eq "`r") { }
            elseif ($c -eq "`n") {
                $row.Add($field.ToString()); [void]$field.Clear()
                if ($row.Count -gt 1 -or $row[0] -ne "") {
                    if ($null -eq $header) { $header = $row.ToArray() }
                    else { $rows.Add(@($row.ToArray())) }
                }
                $row = New-Object System.Collections.Generic.List[string]
            }
            else { [void]$field.Append($c) }
        }
        $i++
    }
    if ($field.Length -gt 0 -or $row.Count -gt 0) {
        $row.Add($field.ToString())
        if ($null -eq $header) { $header = $row.ToArray() }
        else { $rows.Add(@($row.ToArray())) }
    }
    $objects = New-Object System.Collections.Generic.List[object]
    foreach ($r in $rows) {
        $o = [ordered]@{}
        for ($j = 0; $j -lt $header.Count; $j++) {
            $o[$header[$j]] = if ($j -lt $r.Count) { $r[$j] } else { "" }
        }
        $objects.Add([pscustomobject]$o)
    }
    return $objects
}

$matrix = Import-CsvStrict $csvPath
$csvIds = @($matrix | ForEach-Object { $_.ID })
$csvCount = $matrix.Count

# --- markdown table rows: lines starting with '| ' that contain a status from the taxonomy, excluding header/separator/legend ---
$mdLines = Get-Content $mdPath
$statuses = "CONFIRMED","STRONGLY_SUPPORTED","PLAUSIBLE","UNVERIFIED","REJECTED"
$mdTableRows = @($mdLines | Where-Object {
    $_ -match '^\|\s*[A-F]' -and $_ -match '\|\s*(CONFIRMED|STRONGLY_SUPPORTED|PLAUSIBLE|UNVERIFIED|REJECTED)(\s*\||\s*\(.*\)\s*\|?)\s*$'
})
$mdIds = @($mdTableRows | ForEach-Object { ($_ -split '\|')[1].Trim() })

# tally from the MD status line
$tally = @{}
foreach ($s in $statuses) { $tally[$s] = 0 }
foreach ($r in $matrix) {
    $st = $r.STATUS
    $ok = $false
    foreach ($s in $statuses) { if ($st -eq $s -or $st.StartsWith($s + " ")) { $tally[$s]++; $ok = $true; break } }
    if (-not $ok) { throw "Row $($r.ID): unrecognized STATUS '$st'" }
}

# --- CSV field-count integrity (7 columns each) ---
$badFields = @($matrix | Where-Object { ($_.PSObject.Properties | Measure-Object).Count -ne 7 } | ForEach-Object { $_.ID })

# --- expected census ---
$expectedIds = @("A1","A2","B1","B2","B3","B4","B5","B6","C1","C2","C3","D1","D2a","D2b","D3","E1","E2","E3","F1","F2","F3","F4","F5","F6")
$missing = @($expectedIds | Where-Object { $csvIds -notcontains $_ })
$extra = @($csvIds | Where-Object { $expectedIds -notcontains $_ })

# --- write JSON ---
$jsonRows = @()
foreach ($r in $matrix) {
    $jsonRows += [ordered]@{
        id = $r.ID; claim = $r.CLAIM; source = $r.SOURCE; observation = $r.OBSERVATION
        limitation = $r.LIMITATION; relevance_to_eu935 = $r.RELEVANCE_TO_EU935; status = $r.STATUS
    }
}
$jsonObj = [ordered]@{
    run_id = "PE_935_EXTERNAL_SOURCES_MATRIX_R1_20260913"
    row_count = $csvCount
    coverage_note = "23 contract claims -> 24 rows (D2 split: D2a WarEmu code CONFIRMED, D2b RoR post UNVERIFIED)"
    rows = $jsonRows
}
[System.IO.File]::WriteAllText($jsonOut, ($jsonObj | ConvertTo-Json -Depth 5))

# --- verdicts ---
$checks = [ordered]@{
    csv_row_count = $csvCount
    md_table_row_count = $mdTableRows.Count
    csv_ids_equal_md_ids = (($csvIds -join ",") -eq ($mdIds -join ","))
    all_rows_have_7_fields = ($badFields.Count -eq 0)
    expected_census_covered = ($missing.Count -eq 0 -and $extra.Count -eq 0)
    status_tally = $tally
    missing_ids = $missing
    extra_ids = $extra
    bad_field_rows = $badFields
}
$pass = ($checks.csv_row_count -eq 24) -and ($checks.md_table_row_count -eq 24) -and $checks.csv_ids_equal_md_ids -and $checks.all_rows_have_7_fields -and $checks.expected_census_covered
$checks["G4_VERDICT"] = if ($pass) { "PASS" } else { "FAIL" }
[System.IO.File]::WriteAllText($reportOut, ($checks | ConvertTo-Json -Depth 5))
$checks | ConvertTo-Json -Depth 5
if (-not $pass) { exit 1 } else { exit 0 }
