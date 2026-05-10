# AI RMF OSCAL Catalog (community draft)

[![validate](https://github.com/Agent-Threat-Rule/ai-rmf-oscal-catalog/actions/workflows/validate.yml/badge.svg)](https://github.com/Agent-Threat-Rule/ai-rmf-oscal-catalog/actions/workflows/validate.yml)

A community-contributed OSCAL catalog representation of the NIST AI Risk Management Framework (AI RMF 1.0).

## What this is

- A machine-readable, OSCAL v1.2.2 catalog covering the GOVERN function of NIST AI RMF 1.0 (19 controls across 6 categories).
- Statement and category text reproduced verbatim from the AI RMF Core (NIST AI 100-1, Section 5, Table 1).
- Implementation guidance reproduced from the NIST AI RMF Playbook structured export.
- Released under CC0 1.0 (public domain).
- Schema-validated against the official OSCAL v1.2.2 catalog schema vendored at `schemas/oscal_catalog_schema.json`.

## What this is not

- Not endorsed by NIST. The NIST OSCAL Team is the authoritative source for any official AI RMF OSCAL artifact, and we expect this catalog will be superseded if and when an official NIST artifact is published.
- Not a profile. Profiles tailor a catalog to a specific deployment context. The catalog itself is neutral — no specific rule registry, scoring model, or vendor framing is embedded.
- Not a Playbook implementation guide. The Playbook is reproduced inside parts on each control as guidance, not interpreted or extended.
- Not a substitute for reading AI RMF 1.0. The catalog is a structural artifact for tooling; the framework document remains the authoritative source.

## Why this exists

Teams building OSCAL profiles, compliance tooling, or AI governance pipelines today have no machine-readable AI RMF catalog to point at. The NIST OSCAL Team began converting AI RMF in early 2025 but paused due to resource constraints (see [usnistgov/OSCAL#2234](https://github.com/usnistgov/OSCAL/issues/2234)). This catalog aims to unblock downstream OSCAL work for AI RMF without claiming to replace any future official NIST artifact.

## Notable finding: Playbook JSON drifts from AI RMF Core text

While building this catalog we cross-checked the 19 GOVERN subcategory descriptions in the AI RMF Playbook structured JSON export (`https://airc.nist.gov/docs/playbook.json`) against the AI RMF Core canonical text (`https://airc.nist.gov/airmf-resources/airmf/5-sec-core/`).

10 of 19 GOVERN subcategories show textual divergence. Examples:

- **GOVERN 3.1** — Playbook: `"Decision-makings ..."` vs Core: `"Decision-making ..."` (typo)
- **GOVERN 5.2** — Playbook: `"Mechanisms are established to enable AI actors to regularly incorporate adjudicated feedback ..."` vs Core: `"Mechanisms are established to enable the team that developed or deployed AI systems to regularly incorporate adjudicated feedback ..."` (semantic divergence)
- 8 additional minor variations in punctuation, conjunctions, and "and practices" wording

Compliance work cites the Core, so this catalog uses Core wording for control statements and Playbook content only for implementation guidance parts. See `source/ATTRIBUTION.md` for the full divergence inventory.

## Coverage

| AI RMF function | Status | Subcategories |
|---|---|---|
| GOVERN | v0.1 (this release) | 19 |
| MAP | not yet | 17 |
| MEASURE | not yet | 14 |
| MANAGE | not yet | 13 |

v0.2+ will expand to additional functions if there is demand and reviewer feedback supports the structure of v0.1.

## Limitations (v0.1)

- **GOVERN function only.** MAP, MEASURE, and MANAGE are not in this release.
- **No cross-control links.** AI RMF subcategories often reference one another implicitly; this version does not yet model `links` with `rel="related"` between controls. Planned for v0.2.
- **Custom part names (with explicit ns).** The Playbook structure includes content (suggested actions, documentation questions, references) that does not map cleanly onto the OSCAL standard part vocabulary. We use namespaced custom part names (`ai-rmf-suggested-actions`, `ai-rmf-documentation-questions`, `ai-rmf-references`, `ai-rmf-category-statement`) so consumers can recognise these as local extensions.
- **Group `class="ai-rmf-category"` is non-standard.** OSCAL does not prescribe class values; we chose this for clarity over fidelity to NIST 800-53 conventions like `class="family"`.
- **Single maintainer.** This is a one-person community contribution at present. PRs and issues welcome.

## Validating the catalog

```
python3 src/validate.py
```

Validates `catalogs/ai-rmf-govern-v0.1.json` against the official OSCAL v1.2.2 catalog JSON schema. Uses ajv-cli + ajv-formats under the hood (run `npm install` first).

## Regenerating the catalog

```
python3 src/generator.py
```

Reads `source/ai-rmf-playbook.json` and the verbatim Core constants in `src/airmf_core_text.py`, writes `catalogs/ai-rmf-govern-v0.1.json`. The generator preserves `last-modified` if substantive content is byte-identical to the prior catalog.

## Completeness check

```
python3 src/completeness_check.py
```

Asserts that all 19 GOVERN subcategory IDs are present in the expected groups, that each control has the expected parts, that statements and category statements match the Core verbatim constants, and that custom parts carry the project namespace.

## Drift detection

```
python3 tests/test_core_text_drift.py
```

Re-fetches the AI RMF Core HTML rendering and diffs the GOVERN statements against the embedded constants. Fails (exit 1) if NIST upstream wording diverges from the local copy. Run weekly on CI on a schedule (`.github/workflows/validate.yml`).

## Roadmap

- v0.1 (this release): GOVERN function, 19 controls, schema-validated, public domain.
- v0.2 (next): MAP, MEASURE, MANAGE functions; control-to-control `links` for explicit cross-references; OSCAL Team review feedback incorporated if any received.
- v1.0: stable, declared compatible with at least one OSCAL Team-published reference profile.

## Contributing

Issues and pull requests welcome. The catalog is intentionally narrow in scope; out-of-scope contributions will be redirected.

In scope: corrections to AI RMF source fidelity, OSCAL schema compliance fixes, structural improvements to the generator, additional functions (MAP / MEASURE / MANAGE), control-to-control `links` modeling.

Out of scope (defer to separate artifacts): rule profiles, framework cross-walks, audit evidence formatters, Playbook full implementation guidance, scoring methodologies.

If you are part of the NIST OSCAL Team or NIST AI Lab, please open an issue describing where you would like a community catalog of AI RMF to live (this repo, a fork into `usnistgov/oscal-content`, an internal NIST repo, etc.) and we will adapt the contribution path accordingly.

## Maintainer

Adam Lin (`adam@agentthreatrule.org`). This catalog is a personal community contribution and is not produced by, endorsed by, or affiliated with NIST. The maintainer also runs the Agent Threat Rules (ATR) detection-rule project; the OSCAL catalog here is intentionally separated from that project both organisationally (different repo, different contribution path) and content-wise (catalog text is verbatim NIST, not derived from any detection rule).

## Abandonment criteria

This catalog is maintained on a best-effort community basis. If schema validation or completeness checks regress on more than one control after generator changes, work pauses until the regression is understood and reverted. v0.1 commits to a shippable state of all 19 GOVERN controls passing schema validation and completeness checks.

## Acknowledgments

The AI RMF Core and AI RMF Playbook are NIST publications. NIST publications are works of the U.S. Government and not subject to copyright in the United States. The OSCAL JSON schema is the work of the NIST OSCAL Team (`https://github.com/usnistgov/OSCAL`).
