# qc_negative_controls.ps1 - PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO independent QC negative controls.
# RUN_ID: PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_QC_INTERNAL_R1_20261006
# Worker: pe-master-auditor (fresh-context independent internal QC; STATIC-ONLY; reads the pinned EXE only).
# Purpose (L9): exercise the actual predicates of (1) the CTRL_C resource-family detector,
# (2) my own E8 census, with executed falsifiers - not code-review-only verification.
# The EXE on disk is NEVER modified: all mutations are in-memory copies.

param(
    [string]$ExePath = "D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
)

$ErrorActionPreference = "Stop"
$b = [IO.File]::ReadAllBytes($ExePath)

# --- identity re-check before the controls ---
$sha = (Get-FileHash -Algorithm SHA256 -LiteralPath $ExePath).Hash
$sizeOk = ($b.Length -eq 8015872)
$shaOk = ($sha -eq "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31")
Write-Output ("EXE_IDENTITY: size={0} sha_match={1}" -f $sizeOk, $shaOk)
if (-not ($sizeOk -and $shaOk)) { Write-Output "EXE_IDENTITY=FAIL - aborting"; exit 1 }

# ============ CONTROL NC1: CTRL_C falsifier re-run (my own detector) ============
# The real examined key-to-map operation: FUN_00856190 body 0x00856190..0x00856210.
# Clean expectation: ZERO E8 calls into the BASE-canon resource family.
# Falsifier: inject a fake E8 -> FUN_0072F580 at body offset 0x7B (VA 0x0085620B,
# the same injection point as the executor's qc_controls.py CTRL_C) in an in-memory
# copy; my independent detector MUST find exactly 1.
$BODY_LO = 0x00856190
$BODY_LEN = 0x80
$boff = ($BODY_LO - 0x00400000)  # .text: file offset == RVA (raw_ptr == vaddr == 0x1000)
$FAMILY = @(0x0072F580, 0x006C9700, 0x006CB6F0, 0x006CB020, 0x0043A550)

function Find-FamilyE8([byte[]]$buf, [int]$lo, [int]$len) {
    $found = @()
    for ($i = 0; $i -lt $len - 4; $i++) {
        if ($buf[$lo + $i] -eq 0xE8) {
            $rbytes = @($buf[($lo + $i + 1)], $buf[($lo + $i + 2)], $buf[($lo + $i + 3)], $buf[($lo + $i + 4)])
            $rel = [BitConverter]::ToInt32([byte[]]$rbytes, 0)
            $va = $BODY_LO + $i
            $t = ($va + 5 + $rel) -band 0xFFFFFFFF
            if ($FAMILY -contains $t) { $found += ("0x{0:X8}->0x{1:X8}" -f $va, $t) }
        }
    }
    return , $found
}

$cleanFound = Find-FamilyE8 $b $boff $BODY_LEN
Write-Output ("NC1_CLEAN: resource-family E8 in insert body = {0} (expect 0)" -f $cleanFound.Count)

$mut = $b.Clone()
$fakeOff = $boff + 0x7B
$mut[$fakeOff] = 0xE8
$fakeVa = $BODY_LO + 0x7B
$rel = [Int32](0x0072F580 - ($fakeVa + 5))
$rb = [BitConverter]::GetBytes($rel)
$mut[$fakeOff + 1] = $rb[0]; $mut[$fakeOff + 2] = $rb[1]; $mut[$fakeOff + 3] = $rb[2]; $mut[$fakeOff + 4] = $rb[3]
$mutFound = Find-FamilyE8 $mut $boff $BODY_LEN
Write-Output ("NC1_MUTATED: detector found {0} (expect 1) -> {1}" -f $mutFound.Count, ($mutFound -join ','))
$nc1 = ($cleanFound.Count -eq 0) -and ($mutFound.Count -eq 1) -and ($mutFound[0] -like "*0x0072F580")
Write-Output ("NC1_VERDICT: {0}" -f ($(if ($nc1) { "PASS" } else { "FAIL" })))

# ============ CONTROL NC2: my census detector positive control ============
# Inject a synthetic E8 -> 0x00414130 at file offset 0x569C0 (VA 0x004569C0, a neutral
# offset that does NOT overlap any real hit's E8 opcode byte) in a COPY - my census
# must count 7 (6 real + 1 synthetic). QC self-note: the first version of this control
# injected at 0x569D0, which clobbered the real hit's E8 opcode @0x569D3 (my tooling
# error, detector behavior was correct: 5 real + 1 synthetic = 6); fixed to 0x569C0.
$TGT = 0x00414130
$mut2 = $b.Clone()
$o2 = 0x569C0
$mut2[$o2] = 0xE8
$va2 = 0x00401000 + ($o2 - 0x1000)
$rel2 = [Int32]($TGT - ($va2 + 5))
$rb2 = [BitConverter]::GetBytes($rel2)
$mut2[$o2 + 1] = $rb2[0]; $mut2[$o2 + 2] = $rb2[1]; $mut2[$o2 + 3] = $rb2[2]; $mut2[$o2 + 4] = $rb2[3]
$hits = @()
$pos = 0x1000
while ($true) {
    $i = [Array]::IndexOf($mut2, [byte]0xE8, $pos, (0x1000 + 0x674000 - $pos))
    if ($i -lt 0) { break }
    $relx = [BitConverter]::ToInt32($mut2, $i + 1)
    $va = 0x00401000 + ($i - 0x1000)
    if ((($va + 5 + $relx) -band 0xFFFFFFFF) -eq $TGT) { $hits += ("0x{0:X8}" -f $va) }
    $pos = $i + 1
}
Write-Output ("NC2_MUTATED: my census on copy = {0} hits (expect 7)" -f $hits.Count)
Write-Output ("NC2_HITS: {0}" -f ($hits -join ', '))
$nc2 = ($hits.Count -eq 7) -and ($hits -contains "0x004569C0")
Write-Output ("NC2_VERDICT: {0}" -f ($(if ($nc2) { "PASS" } else { "FAIL" })))

# ============ CONTROL NC3: mutated-expectation negative (wrong target) ============
# Same census on the UNMUTATED EXE but expecting the WRONG target 0x00414134:
# must find 0 (no false positives; the 6 real hits are target-discriminated).
$hits3 = @()
$pos = 0x1000
while ($true) {
    $i = [Array]::IndexOf($b, [byte]0xE8, $pos, (0x1000 + 0x674000 - $pos))
    if ($i -lt 0) { break }
    $relx = [BitConverter]::ToInt32($b, $i + 1)
    $va = 0x00401000 + ($i - 0x1000)
    if ((($va + 5 + $relx) -band 0xFFFFFFFF) -eq 0x00414134) { $hits3 += ("0x{0:X8}" -f $va) }
    $pos = $i + 1
}
Write-Output ("NC3_WRONG_TARGET(0x00414134): {0} hits (expect 0)" -f $hits3.Count)
$nc3 = ($hits3.Count -eq 0)
Write-Output ("NC3_VERDICT: {0}" -f ($(if ($nc3) { "PASS" } else { "FAIL" })))

Write-Output ("OVERALL_NEGATIVE_CONTROLS: {0}" -f ($(if ($nc1 -and $nc2 -and $nc3) { "ALL_PASS" } else { "FAIL" })))
