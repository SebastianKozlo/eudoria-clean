[pins] R61 hashes...
[pins] R61: 10/10 OK
[pins] corpus sha256 = c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0
[pins] map sha256 = 5cb9d67e3731d924ae94584a7119188b30ce5322192a2c0ba54590683a37025e
[corpus] entries=5596 footer=b'BNT2'
[control] raw sources parse...
[control] 146709.nif: status=PASS blocks=79
[control] 424276.nif: status=PASS blocks=35
[control] 500078.nif: status=PASS blocks=121
[sandbox] MILD-1 built (byte@639 0x18->0x19)
[sandbox] MILD-2 built (byte@306 '2'->'3')
[sandbox] MILD-3 built (byte@625 0x02->0x03)
[sandbox] SCRAMBLE-2 built (version u32 -> 0xFFFFFFFF)
[sandbox] SCRAMBLE-3 built (preamble -> 0xDEADBEEF)
[sandbox] SCRAMBLE-1: copying container (395,412,868 B)...
[sandbox] SCRAMBLE-1 built (footer magic -> XXXX); SHA changed as predicted
[SCRAMBLE-1] positive control: intact original container...
[SCRAMBLE-1] positive control OK: entries=5596
[SCRAMBLE-1] result: {"status": "VALUEERROR", "message": "not a BNT2 archive: footer magic=b'XXXX'", "expected": true}
[parse] executing variants against frozen R61...
[parse] MILD-1_146709: ok=True status=PASS detail={"num_blocks": 79, "ark": {"variant": "G3E", "boundary_method": "boundary_search", "ext_size": 120}}
[parse] MILD-2_424276: ok=True status=FAIL_CLOSED detail={"num_blocks": 35, "ark": {"variant": "TEXT_CRLF", "boundary_method": null, "ext_size": null}}
[parse] MILD-3_500078: ok=True status=FAIL_CLOSED detail={"num_blocks": 121, "ark": {"variant": null, "boundary_method": null, "ext_size": null}}
[parse] SCRAMBLE-2_424276: ok=True status=FAIL_ERROR detail={"num_blocks": 0, "ark": null}
[parse] SCRAMBLE-3_500078: ok=True status=FAIL_CLOSED detail={"num_blocks": 121, "ark": null}
[MILD-1] anchor u3_offset_abs=638; ext_start computed=646
[MILD-1] N_true=24 true_boundary=766 preamble@true=0
[MILD-1 gate] {"parse_passed": true, "ark_variant_flipped_G3D_to_G3E": true, "boundary_method_boundary_search": true, "true_boundary_from_raw": 766, "preamble_u32_at_true_boundary": 0, "matrix_reported_766": 766}
[verdicts] 2/6 predictions matched