# verify_contract_completeness.ps1 - PE_OPERATING_MODEL_AMENDMENT_A1_R2_20260906
# GATE G2 PROOF (fail-closed, script-based structural verification):
#   C1: PE_MASTER_HUMAN_AUDIT_CONTRACT_v1.md exists in the repo root.
#   C2: All five section headers present exactly once: A/B/C/D/E.
#   C3: Within section A: all 14 numbered format subsections present,
#       numbered 1..10 and 11..14, each exactly once, in order.
#   C4: Within section B: all 10 percent rules present, numbered 1..10,
#       each exactly once, in order.
#   C5: The contract opens with the verbatim adoption sentence and ends with
#       the verbatim HARD STOP line (begin/end markers of the verbatim block).
#   Bonus provenance: records the '=' separator line lengths of each section
#   banner (ASCII-art fidelity record).
# Writes PASS/FAIL + evidence to 01_RAW/CONTRACT_VERIFICATION_OUTPUT.txt.
param()
$ErrorActionPreference = 'Stop'
$root = 'D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean'
$file = Join-Path $root 'PE_MASTER_HUMAN_AUDIT_CONTRACT_v1.md'
$out  = Join-Path $root 'docs\audits\PE_OPERATING_MODEL_AMENDMENT_A1_R2_20260906\01_RAW\CONTRACT_VERIFICATION_OUTPUT.txt'

$log = New-Object System.Collections.Generic.List[string]
$log.Add('=== CONTRACT COMPLETENESS VERIFICATION (GATE G2) - PE_OPERATING_MODEL_AMENDMENT_A1_R2_20260906 ===')
$log.Add('ran: ' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz'))

$fail = $null
if (-not (Test-Path -LiteralPath $file)) {
  $log.Add('C1 FAIL: contract file missing'); $fail = 'C1'
  [System.IO.File]::WriteAllLines($out, $log, (New-Object System.Text.UTF8Encoding $false)); exit 1
}
$bytes = [System.IO.File]::ReadAllBytes($file)
$text = [System.Text.Encoding]::UTF8.GetString($bytes)
$log.Add(('C1 PASS: file exists | ' + $bytes.Length + ' B | SHA256 ' + [System.BitConverter]::ToString([System.Security.Cryptography.SHA256]::Create().ComputeHash($bytes)).Replace('-','')))

$secA = 'A. KANONICZNY FORMAT KAŻDEGO MASTER AUDITU'
$secB = 'B. ZASADY PROCENTÓW'
$secC = 'C. STYL RAPORTU'
$secD = 'D. RELACJA Z DAILY DESKTOP I MILESTONE DESKTOP'
$secE = 'E. IMPLEMENTACJA KONTRAKTU'
$headers = @{ A = $secA; B = $secB; C = $secC; D = $secD; E = $secE }
$hdrFail = @()
foreach ($k in @('A','B','C','D','E')) {
  $n = [regex]::Matches($text, [regex]::Escape($headers[$k])).Count
  $log.Add(('C2 section ' + $k + ': occurrences = ' + $n))
  if ($n -ne 1) { $hdrFail += $k }
}
if ($hdrFail.Count -gt 0) { $log.Add('C2 FAIL: sections with count != 1: ' + ($hdrFail -join ',')); $fail = 'C2' } else { $log.Add('C2 PASS: all five section headers A/B/C/D/E present exactly once') }

# spans
$iA = $text.IndexOf($secA); $iB = $text.IndexOf($secB); $iC = $text.IndexOf($secC); $iD = $text.IndexOf($secD); $iE = $text.IndexOf($secE)
$spanA = $text.Substring($iA, $iB - $iA)
$spanB = $text.Substring($iB, $iC - $iB)
$linesA = $spanA -split "`n"
$linesB = $spanB -split "`n"

# C3: 14 numbered subsections in section A (each numbered title line exactly once, in order)
$subTitles = @{
  1 = '1. AUDIT TARGET'; 2 = '2. EXECUTIVE VERDICT'; 3 = '3. CO RUN MIAŁ ZROBIĆ';
  4 = '4. CO TA PRACA FAKTYCZNIE POKAZAŁA'; 5 = '5. CLAIM → EVIDENCE → INDEPENDENT VALIDATION → VERDICT';
  6 = '6. CO JEST BŁĘDNE / OVERCLAIMED'; 7 = '7. CZEGO NADAL NIE WIEMY';
  8 = '8. RETRACTIONS / SUPERSESSIONS'; 9 = '9. BLAST RADIUS';
  10 = '10. CO ZMIENIŁO SIĘ W STANIE PROJEKTU';
  11 = '11. PROJECT PROGRESS DASHBOARD — OBOWIĄZKOWY W KAŻDYM AUDYCIE';
  12 = '12. PROGRESS THIS RUN'; 13 = '13. NEXT ACTION'; 14 = '14. READY-TO-PASTE NEXT PROMPT'
}
$missingA = @(); $dupA = @()
foreach ($n in 1..14) {
  $cnt = 0; foreach ($ln in $linesA) { if ($ln.TrimEnd() -eq $subTitles[$n]) { $cnt++ } }
  if ($cnt -eq 0) { $missingA += $n } elseif ($cnt -gt 1) { $dupA += ($n.ToString() + 'x' + $cnt) }
}
# in-order check
$positions = @(); foreach ($n in 1..14) { $p = $spanA.IndexOf($subTitles[$n]); if ($p -lt 0) { $positions += -1 } else { $positions += $p } }
$inOrder = $true; for ($x = 1; $x -lt 14; $x++) { if ($positions[$x] -lt $positions[$x - 1]) { $inOrder = $false } }
$log.Add(('C3 subsections found in section A: ' + (14 - $missingA.Count) + '/14 | missing: ' + ($(if ($missingA.Count) { $missingA -join ',' } else { 'NONE' })) + ' | duplicated: ' + ($(if ($dupA.Count) { $dupA -join ',' } else { 'NONE' })) + ' | in-order: ' + $inOrder))
if ($missingA.Count -gt 0 -or $dupA.Count -gt 0 -or -not $inOrder) { $log.Add('C3 FAIL'); $fail = 'C3' } else { $log.Add('C3 PASS: all 14 numbered format subsections present, exactly once each, in order 1..14') }

# C4: 10 percent rules in section B
$ruleLines = @($linesB | Where-Object { $_ -match '^\s*(\d{1,2})\. ' })
$nums = @($ruleLines | ForEach-Object { [int]([regex]::Match($_, '^\s*(\d{1,2})\. ').Groups[1].Value) })
$expected = @(1..10)
$missingB = @($expected | Where-Object { $nums -notcontains $_ })
$extraB = @($nums | Where-Object { $_ -notin $expected })
$inOrderB = $true; for ($x = 1; $x -lt $nums.Count; $x++) { if ($nums[$x] -lt $nums[$x - 1]) { $inOrderB = $false } }
$log.Add(('C4 percent rules found in section B: ' + $nums.Count + ' | numbers: [' + ($nums -join ',') + '] | missing: ' + ($(if ($missingB.Count) { $missingB -join ',' } else { 'NONE' })) + ' | extra: ' + ($(if ($extraB.Count) { $extraB -join ',' } else { 'NONE' })) + ' | in-order: ' + $inOrderB))
if ($nums.Count -ne 10 -or $missingB.Count -gt 0 -or $extraB.Count -gt 0 -or -not $inOrderB) { $log.Add('C4 FAIL'); $fail = 'C4' } else { $log.Add('C4 PASS: all 10 percent rules present, numbered 1..10, exactly once each, in order') }

# C5: verbatim block begin/end markers
$opening = 'Od tej chwili wprowadź jako stały kanoniczny kontrakt'
$closing = 'HARD STOP po przedstawieniu tego wyniku.'
$o = $text.Contains($opening); $c = $text.Contains($closing) -and $text.TrimEnd().EndsWith($closing)
$log.Add(('C5 opening sentence present: ' + $o + ' | closing HARD STOP line present & final: ' + $c))
if (-not ($o -and $c)) { $log.Add('C5 FAIL'); $fail = 'C5' } else { $log.Add('C5 PASS: verbatim block begin and end markers intact') }

# bonus: '=' banner lengths per section
$bannerLens = @($text -split "`n" | Where-Object { $_ -match '^=+$' } | ForEach-Object { $_.Length })
$log.Add(('BONUS: equals-banner line lengths in order: ' + ($bannerLens -join ',')))

if ($fail) { $log.Add('OVERALL: FAIL (' + $fail + ')') } else { $log.Add('OVERALL: PASS - GATE G2 (contract completeness) PROVEN') }
[System.IO.File]::WriteAllLines($out, $log, (New-Object System.Text.UTF8Encoding $false))
Write-Host ($log -join [Environment]::NewLine)
if ($fail) { exit 1 } else { exit 0 }
