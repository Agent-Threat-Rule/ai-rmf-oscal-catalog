# Changelog

All notable changes to this catalog are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely and the
catalog version follows [Semantic Versioning](https://semver.org/) where
"MAJOR" tracks AI RMF revisions, "MINOR" tracks function coverage additions,
and "PATCH" tracks corrections that do not change the set of controls or
their statement text.

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
