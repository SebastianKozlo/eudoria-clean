# PRE_CORRECTION_STATE — PE_935_20002_PAYLOAD30_DESKTOP_CORRECTION_R1_20261002

| Field | Value |
|---|---|
| RECORD_CLASS | FORMALIZER PRE-CORRECTION STATE (independent re-measurement; fail-closed; no repairs performed) |
| RUN_ID (correction) | PE_935_20002_PAYLOAD30_DESKTOP_CORRECTION_R1_20261002 |
| CORRECTION_OF | existing run package PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002 (this package) |
| PARENT_AUTHORIZATION | HUMAN_DECISION_ID PE_935_20002_PAYLOAD30_DESKTOP_CORRECTION_AUTH_R1_20261002 (human order 2026-10-02; one focused correction cycle after DESKTOP_POST_AUDIT_VERDICT = REQUIRE_CORRECTIONS) |
| DISPATCHED_BY | PE-MASTER direct |
| MEASURED_BY | pe-master-auditor formalizer session (PE-MASTER direct dispatch) |
| MEASURED_AT_UTC | 2026-10-02T21:05Z–2026-10-02T21:08:11.638Z (git/identity measurements and final re-verify; bijection census run 2026-10-02T21:07:15.485Z–21:07:16.406Z) |
| REPO_ROOT (git show-toplevel) | D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean |
| PACKAGE (correction output root) | D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002 |
| NEXT WRITES BY THIS FORMALIZER | CORRECTION_RUN_CONTRACT.md + CORRECTION_CONTRACT_FREEZE.json in this same directory (00_CONTROL\DESKTOP_CORRECTION_R1\) — nothing else in the package or repo |

All values below are MEASURED by this formalizer with its own commands (exact commands in
Appendix A). No value is copied from any report or memory. Expected values come from the
PE-MASTER dispatch (authorized correction order).

## 1. GIT STATE (measured)

- HEAD = `9203b6d1ad5025f4158d5165863594132aaac49f`
  - BASE_SHA (AUTHORIZED_BASE_HEAD) expected = `9203b6d1ad5025f4158d5165863594132aaac49f`
  - VERDICT: MATCH
- origin/master (LOCAL cached ref; live remote NOT contacted by this formalizer) = `9203b6d1ad5025f4158d5165863594132aaac49f`
- `git status --short` census (verbatim, at repo root):
  - `?? docs/audits/PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002/`
  - `?? docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/`
  - `?? docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/`
  - `?? docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/`
  - `?? docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/`
  - `?? experiments/`
  - UNTRACKED_GROUP_COUNT = 6 (matches expectation exactly)
  - STAGED = 0 (no staged entries in the census; no tracked-file modifications at all)
  - COMMITS_BY_THIS_WRITER = 0 (formalizer performs NO commit; persistence is a separate dispatch)
  - Tracked AUDIT_ENTRYPOINT.md (repo root) is UNMODIFIED at pre-state (absent from the status census).

## 2. ORIGINAL INPUT PHYSICAL IDENTITIES (measured)

| Input | Path | Expected | Measured size | Measured SHA256 | Verdict |
|---|---|---|---|---|---|
| Entropia.exe | D:\Eudoria_Reconstruction\pcg_install\Entropia.exe | 8,015,872 B / E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 | 8,015,872 B | E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 | MATCH |
| 20002.vfs | D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\20002.vfs | 174,864 B / C3899C3E88D72CE12CEF9B8A4F5E73B26632BB1A3207C950FF2BC40FD9C94AC4 | 174,864 B | C3899C3E88D72CE12CEF9B8A4F5E73B26632BB1A3207C950FF2BC40FD9C94AC4 | MATCH |

## 3. STARTING MANIFEST IDENTITY (measured)

| Artifact | Path | Expected | Measured | Verdict |
|---|---|---|---|---|
| Starting package manifest | 06_REPORT\MANIFEST_SHA256.csv | 50,698 B / SHA256 CD938AD7C05C41A62B5847057A92EBF12C0B1890964AEC0ADCDA0F87ECE1E4BF | 50,698 B / SHA256 CD938AD7C05C41A62B5847057A92EBF12C0B1890964AEC0ADCDA0F87ECE1E4BF | MATCH |

## 4. STARTING-MANIFEST BIJECTION CENSUS (own re-hash; full method in Appendix A)

Census window: 2026-10-02T21:07:15.485Z – 2026-10-02T21:07:16.406Z. The census was executed
BEFORE this formalizer created any file inside the package.

Schema/mechanics (measured):

- Raw line count (ReadAllLines) = 391 = 1 header line + 388 file rows + 1 blank separator line (line 390) + 1 NOTE row (line 391).
- Header = `file,size_bytes,sha256,origin,note` (5 fields) — MATCHES expected schema.
- BOM = False; non-ASCII bytes = 0; CRLF line endings (391 CRLF); file ends with LF. Pure ASCII.

Row census (measured):

- DATA_ROW_COUNT = 389 — MATCHES expected 389 data rows.
- FILE_ROWS = 388; NOTE_ROWS = 1 (file column = "NOTE"; empty size/sha/origin columns; free-text note). — MATCHES expected 388 + 1.
- DUPLICATE_PATH_GROUPS = 0.
- ROW_FIELD_COUNT_HISTOGRAM = `5:388, 6:1` (all 388 file rows are strict 5-field rows; the single NOTE row line carries 6 raw fields — see observation below).

Per-file verification (own re-hash of every file row):

- VERIFIED_OK = 388/388 (every file row matches BOTH disk size AND disk SHA256) — MATCHES expected 388/388, 0 mismatch, 0 missing.
- MISSING_ON_DISK = 0 (manifest rows with no disk file: none).
- MANIFEST_NOT_ON_DISK = 0.
- SIZE_MISMATCH = 0; SHA_MISMATCH = 0; SHA_INVALID_FORMAT = 0 (all sha256 fields are 64 hex chars, valid; all recomputed and equal).

Disk census (measured):

- DISK_FILE_COUNT = 389 = 388 manifest-covered + the manifest itself (self-exclusion per the L12 precedent) — MATCHES expected.
- DISK_NOT_IN_MANIFEST = exactly 1 = `06_REPORT/MANIFEST_SHA256.csv` — MATCHES expected "manifest-only-on-disk delta".
- Coverage algebra (L11): TOTAL_DISK 389 = MANIFEST_COVERED 388 + MANIFEST_SELF 1; USED=388, INVENTORIED_ONLY=0, EXCLUDED=1 (the manifest itself), MISSING=0.

Benign formatting observation (recorded, NOT a bijection defect; no repair by this fail-closed formalizer):
the single NOTE row's free-text note column contains unquoted commas, so that raw line splits into
6 CSV fields (all 388 file rows are strict 5-field rows with no quoting anomalies). The NOTE row is
not a verifiable data row (empty size/sha columns) and does not affect the file-row bijection, which
is perfect. Carried as a note for the correction cycle's wording/count hygiene (contract §7) and the
final manifest regeneration (contract §10): do not treat the NOTE row as a file row in any census.

## 5. EXPECTED-VS-MEASURED SUMMARY

| Item | Expected | Measured | Verdict |
|---|---|---|---|
| HEAD == BASE_SHA | 9203b6d1ad5025f4158d5165863594132aaac49f | identical | MATCH |
| Untracked groups | 6 (package + 4 audit dirs + experiments/) | 6, identical paths | MATCH |
| Staged / commits by writer | 0 / 0 | 0 / 0 | MATCH |
| Entropia.exe | 8,015,872 B / E7785430…F31 | identical | MATCH |
| 20002.vfs | 174,864 B / C3899C3E…AC4 | identical | MATCH |
| MANIFEST_SHA256.csv | 50,698 B / CD938AD7…4BF | identical | MATCH |
| Manifest data rows | 389 = 388 file + 1 NOTE | 389 = 388 + 1 | MATCH |
| File-row verification | 388/388, 0 mismatch, 0 missing | 388/388, 0/0/0 | MATCH |
| Disk census | 389 = 388 + manifest itself | 389 = 388 + 1 (manifest only) | MATCH |

## 6. PRE-EXISTING UNTRACKED GROUPS — READ-ONLY

Untracked group 1 (the correction package itself, `docs/audits/PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002/`)
is the AUTHORIZED correction target: within this package only the frozen correction contract may be
extended by the separately-dispatched executor per CORRECTION_RUN_CONTRACT.md §1–§10.

The other 5 pre-existing untracked groups are READ-ONLY and must remain BYTE-IDENTICAL through the
whole correction (any change is a §12 violation and a C0/C9 persistence failure):

1. `docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/`
2. `docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/`
3. `docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/`
4. `docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/` (the historical JOIN R1 package — outside this correction package, untouchable per contract §3/§12)
5. `experiments/`

## 7. FRESH-DIRECTORY STATEMENT

- Measured immediately before creation: `00_CONTROL\DESKTOP_CORRECTION_R1\` did NOT pre-exist (R1_DIR_EXISTS = False). Created by this formalizer at 2026-10-02T21:08:11.638Z.
- Its three initial files (PRE_CORRECTION_STATE.md, CORRECTION_RUN_CONTRACT.md, CORRECTION_CONTRACT_FREEZE.json) are NOT covered by the starting manifest (50,698 B / CD938AD7…4BF covers exactly the pre-correction 389-file state measured above).
- The executor's BEFORE-copy discipline (contract §3) and the final manifest regeneration (contract §10 step 10) cover the final state; the final package physical file count must be freshly measured per contract §7 item 2 (do NOT hard-code 389).

## 8. STATUS

- STATUS = PASS (every measured identity and the full bijection match the authorized expectations; no input discrepancy).
- HARD_STOP_INPUT_CHECK = NO_BLOCKER.
- This formalizer's part ends after writing the three contract files in 00_CONTROL\DESKTOP_CORRECTION_R1\. Execution/QC/persistence are separate PE-MASTER dispatches (NO_NESTED_TASKS). The executor must RE-VERIFY every value in this record at execution start (gate C0 of CORRECTION_RUN_CONTRACT.md §11).

## Appendix A — exact measurement commands (evidence lineage)

A.1 Git (at repo root D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean):

```
git rev-parse --show-toplevel
git rev-parse HEAD
git rev-parse origin/master
git status --short
```

A.2 Input identities (each file: exact size + SHA256):

```
(Get-Item -LiteralPath <path>).Length
(Get-FileHash -LiteralPath <path> -Algorithm SHA256).Hash
```

A.3 Starting-manifest bijection census — the full script below was executed
(workdir-independent; absolute package path pinned inside the script). The census uses a
self-written CSV state-machine parser (no Import-Csv), re-hashes every file row with
Get-FileHash SHA256, and enumerates the package disk census with Get-ChildItem -Recurse -File.
The script file was kept OUTSIDE the package (formalizer scratch), so its text is reproduced
here verbatim for independent re-execution:

```powershell
$ErrorActionPreference = 'Stop'
$pkg = 'D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002'
$manifestPath = Join-Path $pkg '06_REPORT\MANIFEST_SHA256.csv'
"CENSUS_UTC_START=" + [DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ss.fffZ')

# --- raw bytes / BOM / non-ascii / line endings ---
$bytes = [System.IO.File]::ReadAllBytes($manifestPath)
$bom = ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF)
$nonAscii = 0; foreach ($b in $bytes) { if ($b -gt 0x7F) { $nonAscii++ } }
"MANIFEST_SIZE_BYTES=$($bytes.Length)"
"MANIFEST_BOM=$bom"
"MANIFEST_NON_ASCII_BYTES=$nonAscii"
$crlf = 0; $lf = 0
for ($i = 0; $i -lt $bytes.Length - 1; $i++) { if ($bytes[$i] -eq 13 -and $bytes[$i+1] -eq 10) { $crlf++ } }
for ($i = 0; $i -lt $bytes.Length; $i++) { if ($bytes[$i] -eq 10) { $lf++ } }
"MANIFEST_CRLF_COUNT=$crlf"
"MANIFEST_LF_COUNT=$lf"
"MANIFEST_ENDS_WITH_LF=" + ($bytes[$bytes.Length-1] -eq 10)

$rawLines = [System.IO.File]::ReadAllLines($manifestPath)
"RAW_LINE_COUNT_READALLLINES=$($rawLines.Count)"

# --- CSV state-machine parser (quoting-safe, own implementation) ---
function Parse-CsvLine([string]$line) {
  $fields = New-Object System.Collections.Generic.List[string]
  $sb = New-Object System.Text.StringBuilder
  $inQuotes = $false; $i = 0
  while ($i -lt $line.Length) {
    $c = $line[$i]
    if ($inQuotes) {
      if ($c -eq '"') {
        if (($i + 1) -lt $line.Length -and $line[$i+1] -eq '"') { [void]$sb.Append('"'); $i++ }
        else { $inQuotes = $false }
      } else { [void]$sb.Append($c) }
    } else {
      if ($c -eq '"') { $inQuotes = $true }
      elseif ($c -eq ',') { $fields.Add($sb.ToString()); [void]$sb.Clear() }
      else { [void]$sb.Append($c) }
    }
    $i++
  }
  $fields.Add($sb.ToString())
  return ,$fields
}

$header = Parse-CsvLine $rawLines[0]
"HEADER=" + ($header -join '|')
"HEADER_FIELD_COUNT=$($header.Count)"

$dataRows = New-Object System.Collections.Generic.List[object]
$hist = @{}
$emptyLines = 0
for ($j = 1; $j -lt $rawLines.Count; $j++) {
  if ($rawLines[$j] -match '^\s*$') { $emptyLines++; continue }
  $fields = Parse-CsvLine $rawLines[$j]
  $n = [string]$fields.Count
  if ($hist.ContainsKey($n)) { $hist[$n]++ } else { $hist[$n] = 1 }
  $dataRows.Add([pscustomobject]@{ line = ($j + 1); f = $fields })
}
"EMPTY_LINES=$emptyLines"
"DATA_ROW_COUNT=$($dataRows.Count)"
"ROW_FIELD_COUNT_HISTOGRAM=" + (($hist.GetEnumerator() | Sort-Object Key | ForEach-Object { "$($_.Key):$($_.Value)" }) -join ',')

$fileRows = New-Object System.Collections.Generic.List[object]
$noteRows = New-Object System.Collections.Generic.List[object]
foreach ($r in $dataRows) {
  if ($r.f[0] -eq 'NOTE') { $noteRows.Add($r) } else { $fileRows.Add($r) }
}
"FILE_ROWS=$($fileRows.Count)"
"NOTE_ROWS=$($noteRows.Count)"
foreach ($n in $noteRows) { "NOTE_ROW@line$($n.line): [" + ($n.f -join '|') + "]" }

# --- duplicates among file rows ---
$dup = @($fileRows | Group-Object { $_.f[0] } | Where-Object { $_.Count -gt 1 })
"DUPLICATE_PATH_GROUPS=$($dup.Count)"
foreach ($d in $dup) { "DUP=" + $d.Name + " x" + $d.Count }

# --- per-file verification (own re-hash) ---
$okCount = 0
$missing = New-Object System.Collections.Generic.List[string]
$sizeMismatch = New-Object System.Collections.Generic.List[string]
$shaInvalid = New-Object System.Collections.Generic.List[string]
$shaMismatch = New-Object System.Collections.Generic.List[string]
foreach ($r in $fileRows) {
  $rel = $r.f[0]; $szMan = $r.f[1]; $shaMan = $r.f[2]
  $full = Join-Path $pkg ($rel -replace '/', '\')
  if (-not (Test-Path -LiteralPath $full -PathType Leaf)) { $missing.Add($rel); continue }
  $fi = Get-Item -LiteralPath $full
  $szOk = ($szMan -match '^[0-9]+$') -and ([int64]$szMan -eq $fi.Length)
  if (-not $szOk) { $sizeMismatch.Add("$rel|manifest=$szMan|disk=$($fi.Length)") }
  $shaOk = ($shaMan -match '^[0-9A-Fa-f]{64}$')
  if (-not $shaOk) { $shaInvalid.Add("$rel|sha_field=$shaMan") }
  else {
    $shaDisk = (Get-FileHash -LiteralPath $full -Algorithm SHA256).Hash
    if ($shaDisk -ne $shaMan.ToUpper()) { $shaMismatch.Add("$rel|manifest=$shaMan|disk=$shaDisk") }
    elseif ($szOk) { $okCount++ }
  }
}
"VERIFIED_OK=$okCount"
"MISSING_ON_DISK=$($missing.Count)"; foreach ($m in $missing) { "MISSING=$m" }
"SIZE_MISMATCH=$($sizeMismatch.Count)"; foreach ($m in $sizeMismatch) { "SIZEMISMATCH=$m" }
"SHA_INVALID_FORMAT=$($shaInvalid.Count)"; foreach ($m in $shaInvalid) { "SHAINVALID=$m" }
"SHA_MISMATCH=$($shaMismatch.Count)"; foreach ($m in $shaMismatch) { "SHAMISMATCH=$m" }

# --- disk census ---
$diskFiles = @(Get-ChildItem -LiteralPath $pkg -Recurse -File)
"DISK_FILE_COUNT=$($diskFiles.Count)"
$manifestSet = New-Object 'System.Collections.Generic.HashSet[string]'
foreach ($r in $fileRows) { [void]$manifestSet.Add($r.f[0].ToLower()) }
$diskSet = New-Object 'System.Collections.Generic.HashSet[string]'
$diskNotInManifest = New-Object System.Collections.Generic.List[string]
foreach ($f in $diskFiles) {
  $rel = ($f.FullName.Substring($pkg.Length + 1)) -replace '\\','/'
  [void]$diskSet.Add($rel.ToLower())
  if (-not $manifestSet.Contains($rel.ToLower())) { $diskNotInManifest.Add($rel) }
}
"DISK_NOT_IN_MANIFEST=$($diskNotInManifest.Count)"; foreach ($m in $diskNotInManifest) { "EXTRA_DISK=$m" }
$ghosts = New-Object System.Collections.Generic.List[string]
foreach ($r in $fileRows) { if (-not $diskSet.Contains($r.f[0].ToLower())) { $ghosts.Add($r.f[0]) } }
"MANIFEST_NOT_ON_DISK=$($ghosts.Count)"; foreach ($m in $ghosts) { "GHOST=$m" }

"CENSUS_UTC_END=" + [DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ss.fffZ')
```

(End of record)
