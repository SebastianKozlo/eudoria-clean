# F5 — NifTools/PyFFI documentation: NiArk* classes

- URL: https://www.niftools.org/pyffi/pyffi/formats/nif.html
- Read date: 2026-09-13 (live fetch, HTTP 200; full page ~566 KB, persisted and grepped for the NiArk classes)
- Document: PyFFI Documentation — "pyffi.formats.nif — NetImmerse/Gamebryo (.nif and .kf)"

## VERBATIM QUOTES

### NiArkAnimationExtraData

> *class* `pyffi.formats.nif.NifFormat.NiArkAnimationExtraData`(*template=None*, *argument=None*, *parent=None*)
>
> Bases: `pyffi.formats.nif.NiExtraData`
>
> **Unknown node.**
>
> `unknown_bytes`
>
> `unknown_ints`

### NiArkImporterExtraData

> *class* `pyffi.formats.nif.NifFormat.NiArkImporterExtraData`(*template=None*, *argument=None*, *parent=None*)
>
> Bases: `pyffi.formats.nif.NiExtraData`
>
> **Unknown node.**
>
> `importer_name` — Contains a string like "Gamebryo\_1\_1" or "4.1.0.12"
>
> `unknown_bytes`
>
> `unknown_floats`
>
> `unknown_int_1`
>
> `unknown_int_2`

### Related NiArk* family (same page, all bases NiExtraData unless noted)

- `NiArkShaderExtraData` — "Unknown node." — fields: `unknown_int`, `unknown_string`
- `NiArkTextureExtraData` — Bases: `pyffi.formats.nif.NiExtraData` (page lists class; details truncated in fetch but class present in the struct list)
- `NiArkViewportInfoExtraData` — present in the xml_struct list
- `ArkTexture` struct — "A texture reference used by NiArkTextureExtraData." — fields: `texture_name`, `texturing_property`, `unknown_bytes`, `unknown_int_3`, `unknown_int_4`
- All appear in the module `xml_struct` list: `<struct 'NiArkAnimationExtraData'>, <struct 'NiArkImporterExtraData'>, <struct 'NiArkTextureExtraData'>, <struct 'NiArkViewportInfoExtraData'>, <struct 'NiArkShaderExtraData'>`

## Claim check (F5)

- NiArkAnimationExtraData = "Unknown node": **CONFIRMED VERBATIM** (class docstring "Unknown node."; fields unknown_bytes + unknown_ints).
- NiArkImporterExtraData: importerName + unknown ints/bytes/floats: **CONFIRMED VERBATIM** (importer_name "Contains a string like 'Gamebryo_1_1' or '4.1.0.12'" + unknown_bytes + unknown_floats + unknown_int_1 + unknown_int_2).
- STRUCTURAL ORACLE qualification (mandated LIMITATION): PyFFI preserves the STRUCTURE (field classes: bytes, ints, floats, and the importer-name string with example values) but explicitly labels every other field "unknown" and the whole node "Unknown node." — i.e., NifTools' public knowledge of NiArk* is STRUCTURAL, not SEMANTIC. Field names like `unknown_int_2` must never be inherited as semantic solutions. The importer_name examples ("Gamebryo_1_1", "4.1.0.12") are the ONLY semantically labeled content.
- Note: the audited ChatGPT attachment additionally cited the older NifLib C++ field counts (NiArkAnimationExtraData = 4×int + 37×byte; NiArkImporterExtraData = 2 unknown ints + importer name + 13 unknown bytes + 7 unknown floats). Those counts refer to the older NifLib implementation, which is OUTSIDE this run's claim list (F5 cites only the PyFFI page) and was NOT separately verified in this run.
