# SHA256_DRIVER_ADDENDUM -- field_decode_check.py (F-R3 reconstruction)

field_decode_check.py sha256 EFC6CC382AEDFA9C86E182CEE86D772CACCF9F4BB24610F85E7AB14744228B18 (after last edit, before execution; self-hashed by
the driver at startup BEFORE any decoding work; the same value is embedded in
01_RAW/FIELD_DECODE_CHECK_REPRODUCTION.json -> provenance.driver_sha256)

## Provenance note

The PE-MASTER review of run PE_M1_GEOREF_P_DATUM_R1_20260905_154841 (2026-09-06) recorded
FINDING (c) F-R3 [P2]: "01_RAW/FIELD_DECODE_CHECK.json has NO persisted generator (none of
the 4 pinned drivers computes it) -- provenance gap; PE-MASTER's re-execution independently
reproduces the artifact exactly; the driver reconstruction + reproduction proof is ORDERED as
the next iteration (run-local addendum; the historical artifact stays byte-identical)."
This file is that run-local addendum. field_decode_check.py is the RECONSTRUCTED generator,
written fresh (not recovered) in run PE_FIELD_DECODE_GENERATOR_RECONSTRUCTION_R1 under the
PE-MASTER loop 0ed3ca19-99c6-4af0-974b-f64fc2842c76 iteration-2 authorization (mission item
C). It parses the BNT2 trailer index of pcg_install\Data\Textures\Textures.bnt itself,
locates entry 429259.dat from the parsed index (index 71, offset 6920273, packed 198191 B --
read from the index, not hardcoded), pins the physical payload SHA256 0BADB42EC131EE53C49E63EADEE529AA18A68A31D0CF16A57694488FF3333412 (closing
the DEFECTIVE iter029 pin 23D7742E...; CORRECTION_LEDGER entry A), asserts the TGA header
(type 2, 257x257, 24bpp, descriptor 0x00), decodes all 66,049 texels with the 16-bit model
h = ((B<<8|G)/256 - 128) * 5, and reproduces the historical values exactly: land_pct
79.60605005374798 (land_count 52579 / 66,049), hmin -639.43359375, hmax 638.90625 -- exit 0, all
asserts held. The reproduction proof is 01_RAW/FIELD_DECODE_CHECK_REPRODUCTION.json. The
historical 01_RAW/FIELD_DECODE_CHECK.json and the historical 00_CONTROL/SHA256_DRIVER.txt
are NOT modified by this run (the historical artifact stays byte-identical); this addendum
is a separate, NEW file next to the historical driver manifest.
