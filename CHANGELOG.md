# Changelog

All notable changes to this catalog are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely and the
catalog version follows [Semantic Versioning](https://semver.org/) where
"MAJOR" tracks AI RMF revisions, "MINOR" tracks function coverage additions,
and "PATCH" tracks corrections that do not change the set of controls or
their statement text.

## [0.4.0] - 2026-05-11

### Added

- **Topic-graph cross-reference extractor** (`src/topic_cross_references.py`).
  Uses the AI RMF Playbook's own 46-topic taxonomy (already present in the
  source data) to surface topically-related controls through a deterministic,
  inverse-frequency-weighted scoring scheme. Combined with the regex
  extractor from v0.3, total cross-reference coverage rises from 24 of 72
  controls (33%) to 56 of 72 (78%). 176 total directed cross-reference links.
  Topic-derived links carry a `text` field describing the shared topics so
  consumers can distinguish them from regex-derived links.
- **Three additional worked-example profiles**:
  - `profiles/ai-rmf-tier-1-foundational-profile.json` — 18 controls, the
    minimum viable AI risk management surface for low-risk internal AI use.
  - `profiles/ai-rmf-tier-2-customer-facing-profile.json` — 55 controls,
    Tier 1 plus controls relevant for AI deployed to external users
    (fairness, explainability, privacy, post-deployment monitoring,
    third-party concerns).
  - `profiles/ai-rmf-tier-3-high-risk-profile.json` — 72 controls
    (include-all) with high-risk-specific framing.
- **Tier rationale documentation** (`profiles/TIER_RATIONALE.md`) describing
  the selection criteria, rationale for inclusions, and rationale for
  exclusions in each tier profile. Tier profiles are explicit worked
  examples; they are not normative AI RMF baselines.
- **Remediation proposals** for all 41 Playbook-vs-Core divergences:
  - `source/PLAYBOOK_REMEDIATION_PROPOSALS.md` — human-readable per-control
    proposal with type classification, severity (1=cosmetic, 2=typo or
    systemic capitalisation, 3=semantic), recommendation
    (`adopt-core` or `adopt-core-with-caveat`), literal patch text, and
    rationale.
  - `source/playbook_remediation_proposals.json` — machine-readable
    structured export of the same data.
  - 1 severity-3 (semantic GOVERN 5.2), 9 severity-2 (1 typo + 8 systemic
    capitalisation), 31 severity-1 (minor wording / whitespace).
  - 2 systemic findings: function-name casing inconsistency in MEASURE
    function references, and Core-internal hyphenation inconsistency for
    "third-party" between GOVERN 6.1 and MAP 4.1.
- **Governance documentation**:
  - `CONTRIBUTING.md` — how to contribute, validation workflow,
    contribution scope, upstream contact pointers to NIST.
  - `MAINTAINERS.md` — current maintainers, decision-making process,
    bus-factor disclosure (currently 1), conflict-of-interest declarations.
  - `SECURITY.md` — vulnerability reporting policy, threat model, scope
    of "what counts as a security issue here".
- **Catalog metadata enhancements**:
  - `published` timestamp.
  - `revisions` array with v0.1.0, v0.2.0, v0.3.0, v0.4.0 entries.
  - `roles` (canonical-source, community-maintainer).
  - `responsible-parties` mapping NIST → canonical-source and the
    community contributors → community-maintainer.
  - Community contributors party added alongside the existing NIST party.
- Multi-profile validation in `src/completeness_check.py`: verifies the
  expected control count and selection kind (`include-all` vs
  `include-controls`) for each tier profile, and verifies all
  `include-controls` IDs resolve to real controls in the catalog.
- npm scripts: per-profile validation tasks (`validate-profile-baseline`,
  `validate-profile-tier-1/2/3`) and combined `validate-profiles`.

### Changed
- Catalog filename: `catalogs/ai-rmf-v0.3.json` → `catalogs/ai-rmf-v0.4.json`.
  v0.3 history remains in git for reference.
- Profile filename `ai-rmf-baseline-profile.json` retained but rebuilt to
  reference the v0.4 catalog and the v0.4-versioned UUIDs.
- README and CHANGELOG updated to reflect v0.4 deliverables.
- Generator metadata block extended with `revisions`, `roles`,
  `responsible-parties`, and a second `parties` entry.
- `package.json` validate script targets `catalogs/ai-rmf-v0.4.json`.

### Coverage
- 72 controls (unchanged)
- 176 cross-reference links across 56 controls (up from 31 across 24)
- 4 worked-example profiles (up from 1)
- 41 remediation proposals (new)
- 5-layer validation: catalog schema + 4 profile schemas + completeness
  + cross-ref resolution + drift detection

## [0.3.0] - 2026-05-10

### Added
- Control-to-control cross-reference `links` extracted from both Core
  statement text and Playbook implementation guidance. 31 links across
  24 of 72 controls. Patterns recognised: "the {function} function",
  "{Function} N.M" subcategory references, and "{Function} N" category
  references. Self-references are dropped. Source: `src/cross_references.py`.
- Worked example profile at `profiles/ai-rmf-baseline-profile.json`.
  Imports the v0.3 catalog by back-matter resource UUID, selects all
  72 controls with `include-all`, merges as-is. Profile generator at
  `src/profile_generator.py` produces it deterministically.
- OSCAL profile JSON schema (v1.2.2) vendored at
  `schemas/oscal_profile_schema.json`.
- npm scripts split: `validate-catalog`, `validate-profile`, and a
  combined `validate` running both. CI workflow updated to validate
  both artifacts and to verify generator output (catalog + profile)
  is committed and reproducible.
- Completeness check extended: cross-reference links must resolve to
  real IDs in the catalog (function group, category group, or control)
  and must not be self-references; profile imports must declare
  `include-all` or `include-controls`; profile back-matter resource
  must include an rlink to the v0.3 catalog file.

### Changed
- Catalog filename: `catalogs/ai-rmf-v0.2.json` → `catalogs/ai-rmf-v0.3.json`.
  v0.2 history remains in git for reference.
- README: added "Using this catalog in OSCAL profiles" section,
  updated coverage table, OSCAL structure diagram, and limitations
  list to reflect what v0.3 actually delivers (links present,
  parameters intentionally absent).

## [0.2.0] - 2026-05-10

### Added
- Expanded coverage to all four AI RMF functions (GOVERN, MAP, MEASURE, MANAGE).
  v0.2 catalog contains 19 categories and 72 subcategories — full coverage of
  AI RMF 1.0 Tables 1-4.
- Hierarchical OSCAL group structure: 4 top-level function groups, each with
  nested category groups, each containing subcategory controls. This matches
  the AI RMF document organisation.
- Verbatim AI RMF Core text for all 19 categories and 72 subcategories in
  `src/airmf_core_text.py`, programmatically extracted from the AIRC Core
  HTML rendering and sanity-cleaned against trailing site-footer artifacts.
- Full Playbook-vs-Core divergence inventory at
  `source/PLAYBOOK_VS_CORE_DIVERGENCES.md`. The audit found 41 of 72
  subcategories drift between the Playbook JSON export and the Core
  canonical text — 1 typo, 1 semantic divergence at GOVERN 5.2,
  7 capitalisation-only divergences (function names rendered as lower-case
  in Core but upper-case in Playbook), and 32 minor wording variations.
- Drift test (`tests/test_core_text_drift.py`) extended to verify all four
  functions against upstream AIRC Core.
- Completeness checker extended to verify nested group structure, function
  ordering, category ordering, and 72 expected control IDs.

### Changed
- Catalog filename: `catalogs/ai-rmf-govern-v0.1.json` removed; replaced by
  `catalogs/ai-rmf-v0.2.json` (no longer GOVERN-only).
- README: rewrote scope and coverage sections to reflect the full four-function
  catalog. Notable-finding section expanded with per-function drift breakdown.
- Generator: refactored to loop across all four functions, with helper
  functions for function-level groups, category-level groups, and controls.
- `package.json` validate script now targets `catalogs/ai-rmf-v0.2.json`.

### Removed
- `catalogs/ai-rmf-govern-v0.1.json` — superseded by v0.2 full catalog.
  v0.1 history remains in git for reference.

## [0.1.0] - 2026-05-10

### Added
- Initial OSCAL v1.2.2 catalog covering the GOVERN function of NIST AI RMF 1.0.
- 19 controls across 6 GOVERN categories, all statement and category text
  reproduced verbatim from the AI RMF Core (NIST AI 100-1, Section 5, Table 1).
- Implementation guidance parts on each control reproduced from the AI RMF
  Playbook structured export: `guidance` (about), `ai-rmf-suggested-actions`,
  `ai-rmf-documentation-questions`, `ai-rmf-references`.
- Each control carries `ai-rmf-actor` and `ai-rmf-topic` properties from the
  Playbook AI Actors and Topic fields.
- Each group carries an `ai-rmf-category-statement` part with verbatim
  category text from AI RMF Core Table 1.
- Generator (`src/generator.py`) reads Playbook JSON + Core constants and
  emits the catalog. Preserves `last-modified` when substantive content is
  byte-identical to the prior catalog.
- Schema validation tooling (`src/validate.py`, ajv-cli + ajv-formats).
- Completeness checker (`src/completeness_check.py`) verifying expected
  subcategory IDs, expected parts, verbatim Core text, and custom-part ns.
- Drift detection test (`tests/test_core_text_drift.py`) that re-fetches
  AI RMF Core HTML and diffs against embedded constants.
- CI workflow (`.github/workflows/validate.yml`) running schema +
  completeness on every push and PR, plus weekly drift detection.
- Source attribution document (`source/ATTRIBUTION.md`) recording fetch
  date, source URLs, SHA-256 hashes, and a Core-vs-Playbook divergence
  inventory.

### Notable findings
- Cross-checking the AI RMF Playbook structured JSON export against the
  AI RMF Core HTML rendering surfaced 10 textual deviations across the 19
  GOVERN subcategories, including a typo at GOVERN 3.1 ("Decision-makings"
  vs Core "Decision-making") and a semantic divergence at GOVERN 5.2
  ("AI actors" vs Core "the team that developed or deployed AI systems").
  See `source/ATTRIBUTION.md` for the full inventory. The catalog uses
  Core wording for control statements; Playbook content is reproduced
  unchanged in implementation guidance parts.
