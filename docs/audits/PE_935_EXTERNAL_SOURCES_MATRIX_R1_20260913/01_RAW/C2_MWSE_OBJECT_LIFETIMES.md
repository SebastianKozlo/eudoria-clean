# C2 — MWSE guide: Object Lifetimes

- URL: https://mwse.github.io/MWSE/guides/object-lifetimes/
- Read date: 2026-09-13 (live fetch, HTTP 200; full page persisted to tool-output file tool_09b415fdc001IQaaLVMeSLJ9Iy)
- Document: Morrowind Script Extender (MWSE) guide "Object Lifetimes"
- Source repo: https://github.com/MWSE/MWSE

## VERBATIM QUOTES (section "Definition of Objects, References and Mobiles")

> A **base object**, inheriting from the tes3baseObject class, is an object of certain type usually created in the Construction Set's Object Window. Those are: tes3armor, tes3spell, tes3static, tes3creature, etc. When an object is dragged to the Render Window, a **reference (`tes3reference`)** is created. The `tes3reference` structure holds the data for an object placed in certain cell in the game world. Those are **position, rotation, scale**, and optionally, some additional data in the attachments field. The reference data can be inspected in the CS by double-clicking on any placed reference in the Render Window. **There may be zero, one or more `tes3reference`s of a base object placed in the game world.**

Additional relevant quote (terminology caution, section header):

> Before describing the lifetimes of Morrowind objects of individual classes, it's desirable to understand the differences between objects, references (`tes3reference`s this time), and mobiles in the Morroiwind engine.

## Claim verification notes

- base object vs tes3reference distinction: CONFIRMED verbatim.
- reference = position, rotation, scale: CONFIRMED verbatim ("Those are position, rotation, scale").
- base can have 0/1/many instances: CONFIRMED verbatim ("There may be zero, one or more tes3references of a base object placed in the game world").
- Limitation: MWSE is a runtime script extender for Morrowind describing ITS engine's object model; it is evidence for Morrowind's architecture, NOT for a universal Gamebryo-era MMO standard, and NOT for Entropia's architecture.
