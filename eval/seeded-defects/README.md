# Seeded-defect catalogue

Each seeded defect is a known way that marine software failed in the field (requirements section 5.7). Each one becomes a test that First Mate must pass. A test seeds the defect condition and checks that First Mate detects it or does not have it.

The tests come after ADR-0005 (language). Until then, this file is the catalogue.

| ID | Defect | Requirements that prevent it | Test status |
|---|---|---|---|
| SD-01 | Alarm levels are saved but never checked | CORE-AB-10, AC-CORE-1 | Not written |
| SD-02 | Scheduled notices are created but never shown | CORE-AB-02 | Not written |
| SD-03 | A new display starts with all sounds off | CORE-AB-09 | Not written |
| SD-04 | A western longitude is read as south | CORE-PRN-08, AC-CORE-12 | Not written |
| SD-05 | One bad GPS fix triggers the drag alarm | AW design inputs (5.1) | Not written |
| SD-06 | Drag alarm delivery stops after an update | CORE-PL-01, CORE-AB-07 | Not written |
| SD-07 | A command is accepted but not executed, with no error | CORE-OUT-02 (future DK) | Out of scope |
| SD-08 | A command executes in the wrong direction | CORE-OUT-02 (future DK) | Out of scope |
| SD-09 | An integration fails with no values and no error | CORE-AB-10, CORE-DP-10 | Not written |
| SD-10 | A radar in standby guards nothing and raises nothing | CORE-AB-10 | Not written |

## Rules

- A seeded-defect test never changes to make code pass.
- Add a new seeded defect for every field defect that reaches the boat.
