# AI RMF OSCAL Catalog (community draft)

[![validate](https://github.com/Agent-Threat-Rule/ai-rmf-oscal-catalog/actions/workflows/validate.yml/badge.svg)](https://github.com/Agent-Threat-Rule/ai-rmf-oscal-catalog/actions/workflows/validate.yml)

A community-contributed OSCAL catalog representation of the NIST AI Risk Management Framework (AI RMF 1.0), covering all four functions (GOVERN, MAP, MEASURE, MANAGE).

## What this is

- A machine-readable, OSCAL v1.2.2 catalog covering all 19 categories and 72 subcategories of NIST AI RMF 1.0.
- Statement and category text reproduced verbatim from the AI RMF Core (NIST AI 100-1, Section 5, Tables 1-4).
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

## Notable finding: AI RMF Playbook JSON drifts from AI RMF Core text

While building this catalog we cross-checked the 72 subcategory descriptions in the AI RMF Playbook structured JSON export (`https://airc.nist.gov/docs/playbook.json`) against the AI RMF Core canonical text (`https://airc.nist.gov/airmf-resources/airmf/5-sec-core/`).

**41 of 72 subcategories drift (57%)** between those two NIST sources.

Highlights:

- **GOVERN 3.1** — Playbook: `"Decision-makings ..."` vs Core: `"Decision-making ..."` (typo)
- **GOVERN 5.2** — Playbook: `"Mechanisms are established to enable AI actors ..."` vs Core: `"Mechanisms are established to enable the team that developed or deployed AI systems ..."` (semantic divergence — different stakeholder set in AI RMF terminology)
- **MAP function references** — Playbook capitalises "MAP function" / "MEASURE function" while Core uses lower-case "map function" / "measure function" (7 subcategories affected)
- 32 additional minor variations in punctuation, conjunctions, pluralisation, "and practices" wording, hyphenation

Per-function breakdown:

| Function | Subcategories with drift |
|---|---|
| GOVERN | 9 of 19 |
| MAP | 11 of 18 |
| MEASURE | 14 of 22 |
| MANAGE | 7 of 13 |

Compliance work cites the Core, so this catalog uses Core wording for control statements and Playbook content only for implementation guidance parts. The full per-divergence inventory is at `source/PLAYBOOK_VS_CORE_DIVERGENCES.md`.

## Coverage

| AI RMF function | Categories | Subcategories | Status |
|---|---|---|---|
| GOVERN | 6 | 19 | v0.2 (this release) |
| MAP | 5 | 18 | v0.2 (this release) |
| MEASURE | 4 | 22 | v0.2 (this release) |
| MANAGE | 4 | 13 | v0.2 (this release) |
| **Total** | **19** | **72** | — |

## OSCAL structure

```
catalog
└── groups (4 function groups: GOVERN / MAP / MEASURE / MANAGE)
    └── groups (19 category groups: GOVERN-1 .. MANAGE-4)
        └── controls (72 subcategory controls: GOVERN 1.1 .. MANAGE 4.3)
```

Each control carries five parts: `statement` (Core verbatim), `guidance` (Playbook section_about), `ai-rmf-suggested-actions` (Playbook section_actions), `ai-rmf-documentation-questions` (Playbook section_doc), `ai-rmf-references` (Playbook section_ref). The four custom-named parts use a project namespace so consumers can recognise them as local extensions.

## Limitations (v0.2)

- **Custom part names with explicit ns.** The Playbook structure includes content (suggested actions, documentation questions, references) that does not map cleanly onto the OSCAL standard part vocabulary. We use namespaced custom part names so consumers can recognise these as local extensions.
- **Group `class="ai-rmf-function"` and `class="ai-rmf-category"` are non-standard.** OSCAL does not prescribe class values; we chose these for clarity over fidelity to NIST 800-53 conventions like `class="family"`.
- **No control-to-control links yet.** AI RMF subcategories often reference one another implicitly (e.g., MEASURE subcategories cite "as identified in the map function"); v0.2 does not yet model these as OSCAL `links`. Planned for v0.3.
- **Single maintainer.** This is a one-person community contribution at present. PRs and issues welcome.

## Validating the catalog

```
python3 src/validate.py
```

Validates `catalogs/ai-rmf-v0.2.json` against the official OSCAL v1.2.2 catalog JSON schema. Uses ajv-cli + ajv-formats under the hood (run `npm install` first).

## Regenerating the catalog

```
python3 src/generator.py
```

Reads `source/ai-rmf-playbook.json` and the verbatim Core constants in `src/airmf_core_text.py`, writes `catalogs/ai-rmf-v0.2.json`. The generator preserves `last-modified` if substantive content is byte-identical to the prior catalog.

## Completeness check

```
python3 src/completeness_check.py
```

Asserts that all 72 subcategory IDs are present in the expected nested groups, that each control has the expected parts, that statements and category statements match the Core verbatim constants, and that custom parts carry the project namespace.

## Drift detection

```
python3 tests/test_core_text_drift.py
```

Re-fetches the AI RMF Core HTML rendering and diffs the embedded constants for all four functions. Fails (exit 1) if NIST upstream wording diverges from the local copy. Run weekly on CI on a schedule (`.github/workflows/validate.yml`).

## Roadmap

- v0.1 (2026-05-10, superseded): GOVERN function only, 19 controls, schema-validated.
- v0.2 (this release, 2026-05-10): all four functions, 72 controls, full Playbook-vs-Core divergence inventory.
- v0.3 (planned): control-to-control `links` for explicit cross-references between subcategories that AI RMF text relates ("as identified in the map function" etc.). OSCAL Team review feedback incorporated if any received.
- v1.0: stable, declared compatible with at least one OSCAL Team-published reference profile.

## Contributing

Issues and pull requests welcome. The catalog is intentionally narrow in scope; out-of-scope contributions will be redirected.

In scope: corrections to AI RMF source fidelity, OSCAL schema compliance fixes, structural improvements to the generator, control-to-control `links` modeling, additional Playbook content updates when NIST publishes new exports.

Out of scope (defer to separate artifacts): rule profiles, framework cross-walks, audit evidence formatters, Playbook full implementation guidance, scoring methodologies.

If you are part of the NIST OSCAL Team or NIST AI Lab, please open an issue describing where you would like a community catalog of AI RMF to live (this repo, a fork into `usnistgov/oscal-content`, an internal NIST repo, etc.) and we will adapt the contribution path accordingly.

## Maintainer

Adam Lin (`adam@agentthreatrule.org`). This catalog is a personal community contribution and is not produced by, endorsed by, or affiliated with NIST. The maintainer also runs the Agent Threat Rules (ATR) detection-rule project; the OSCAL catalog here is intentionally separated from that project both organisationally (different repo, different contribution path) and content-wise (catalog text is verbatim NIST, not derived from any detection rule).

## Abandonment criteria

This catalog is maintained on a best-effort community basis. If schema validation or completeness checks regress on more than one control after generator changes, work pauses until the regression is understood and reverted. v0.2 commits to a shippable state of all 72 controls passing schema validation and completeness checks.

## Acknowledgments

The AI RMF Core and AI RMF Playbook are NIST publications. NIST publications are works of the U.S. Government and not subject to copyright in the United States. The OSCAL JSON schema is the work of the NIST OSCAL Team (`https://github.com/usnistgov/OSCAL`).
