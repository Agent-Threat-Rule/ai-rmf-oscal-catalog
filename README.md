# AI RMF OSCAL Catalog (community draft)

A community-contributed OSCAL catalog representation of the NIST AI Risk Management Framework (AI RMF 1.0).

## Status

v0.1 draft, community contribution. Not endorsed by NIST. The NIST OSCAL Team is the authoritative source for any official AI RMF OSCAL artifact.

This release covers the **GOVERN function only** (19 subcategories across 6 categories). MAP, MEASURE, and MANAGE will follow in v0.2 if there is demand.

## Why this exists

Teams building OSCAL profiles, compliance tooling, or AI governance pipelines today have no machine-readable AI RMF catalog to point at. The NIST OSCAL Team began conversion in early 2025 but paused due to resource constraints. This catalog aims to unblock downstream OSCAL work for AI RMF without claiming to replace any future official NIST artifact.

## What is and is not in this artifact

The catalog is faithful to AI RMF text. Each control's statement is verbatim from the NIST AI RMF Playbook (`https://airc.nist.gov/airmf-resources/playbook/`), with about-text and suggested-action text reproduced under their respective parts.

The catalog is neutral. It does not embed any specific detection rule registry, scoring approach, or vendor framing. Profiles built on top of this catalog are a separate artifact and live in separate repositories.

## Source

Generated from the NIST AI RMF Playbook JSON export at `https://airc.nist.gov/docs/playbook.json`, which is the structured representation of NIST AI 100-1 (January 2023) and the accompanying Playbook.

NIST publications are works of the U.S. Government and not subject to copyright in the United States.

## License

This catalog and its generation tooling are released under CC0 1.0 (public domain). Anyone may use, modify, redistribute, or incorporate this work without restriction.

## Validating the catalog

```
python3 src/validate.py
```

Validates `catalogs/ai-rmf-govern-v0.1.json` against the official OSCAL v1.2.2 catalog JSON schema (vendored at `schemas/oscal_catalog_schema.json`).

## Regenerating the catalog

```
python3 src/generator.py
```

Reads `source/ai-rmf-playbook.json` (NIST source) and writes `catalogs/ai-rmf-govern-v0.1.json`.

## Completeness check

```
python3 src/completeness_check.py
```

Asserts that all 19 GOVERN subcategory IDs (GOVERN 1.1 through GOVERN 6.2) are present in the generated catalog.

## Roadmap

v0.1 (this release): GOVERN function, 19 controls, schema-validated, public domain.
v0.2: extend to MAP, MEASURE, MANAGE if there is demand. Expansion approach is parallelizable across the four functions.

## Contributing

Issues and pull requests welcome. The catalog is intentionally narrow in scope; out-of-scope contributions will be redirected.

In scope: corrections to AI RMF source fidelity, OSCAL schema compliance fixes, structural improvements to the generator.

Out of scope (defer to separate artifacts): rule profiles, framework cross-walks, audit evidence formatters, Playbook full implementation guidance.

## Abandonment criteria

This catalog is maintained on a best-effort community basis. If schema validation fails on more than one control after generator changes, work pauses until the regression is understood. v0.1 commits to a shippable state of at least 18 of 19 GOVERN controls passing schema validation.

## Acknowledgments

Generated using NIST AI RMF Playbook source data. The OSCAL JSON schema is the work of the NIST OSCAL Team (`https://github.com/usnistgov/OSCAL`).
