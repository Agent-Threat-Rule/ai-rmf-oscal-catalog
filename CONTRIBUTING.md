# Contributing to the AI RMF OSCAL Catalog

This is a community-contributed OSCAL representation of the NIST AI Risk
Management Framework (AI RMF 1.0). It is **not** produced by, endorsed by, or
affiliated with NIST.

Released under CC0 1.0 Universal — see [LICENSE](./LICENSE).

## Scope of contributions

The project welcomes:

- **Catalog generator improvements** — bug fixes in `src/generator.py`,
  `src/cross_references.py`, `src/topic_cross_references.py`, etc.
- **Profile additions** — new worked-example profiles representing other
  reasonable tier choices (e.g., research-only AI use, AI-assisted code
  review, agentic AI, foundation-model deployment).
- **Validation expansion** — additional sanity checks in
  `src/completeness_check.py` or new test files in `tests/`.
- **Drift detection** — improvements to `tests/test_core_text_drift.py` so
  upstream changes to AI RMF Core (NIST AI 100-1) are detected promptly.
- **Remediation proposals** — clarifications, corrections, or new patterns
  identified in `source/PLAYBOOK_VS_CORE_DIVERGENCES.md` and related files.
- **Documentation improvements** — README, governance, methodology.

The project does **not** rewrite NIST source text. Statement and category
text in the catalog is reproduced verbatim from AI RMF Core (NIST AI 100-1
Section 5, Tables 1–4). Implementation guidance is reproduced unchanged from
the AI RMF Playbook structured export. If you believe NIST source text
should change, raise the issue with NIST directly — see
[upstream contact](#upstream-contact-nist).

## How to contribute

### 1. Open an issue first

For non-trivial changes, open a GitHub issue describing the intent. This
prevents wasted effort on changes the maintainers would not accept.

### 2. Fork and branch

Standard GitHub flow. Branch names should be short and descriptive:
`feat/tier-4-profile`, `fix/regex-extractor-edge-case`, etc.

### 3. Run validation locally

```bash
# Catalog and profile schema validation (requires Node + npm)
npm install
npm run validate

# Generator + completeness + drift tests (requires Python 3.10+)
python3 src/generator.py
python3 src/profile_generator.py
python3 src/completeness_check.py
python3 src/remediation_proposals.py

# Optional: re-fetch Core HTML and verify embedded text matches
python3 -m pytest tests/test_core_text_drift.py
```

All five must pass before submitting a PR.

### 4. Submit a pull request

In the PR description:

- Summarise the change.
- Note whether the change affects generated artifacts (catalog, profiles)
  or only source generators.
- If you regenerated artifacts, include the regeneration command and the
  output of `python3 src/completeness_check.py`.

### 5. Review and merge

PRs require approval from at least one maintainer (see
[MAINTAINERS.md](./MAINTAINERS.md)). PRs that pass CI and have no
substantive review feedback within 7 days may be lazy-approved by any
maintainer.

## Coding style

- **Python**: 3.10+. PEP 8 with line length 100. Type hints on function
  signatures where helpful. No external linting tools are required, but
  consistency with the existing modules is expected.
- **JSON output**: 2-space indent, `ensure_ascii=False`, sorted keys where
  it does not affect OSCAL semantics.
- **Determinism**: any change to a generator must preserve byte-stable
  output for unchanged content. UUIDs are deterministic uuid5 from the
  project namespace; `last-modified` is preserved across regenerations
  when content is unchanged.

## Upstream contact (NIST)

If a contribution would be more appropriately addressed by NIST directly:

- For AI RMF Core text issues: contact the AI RMF team via the
  [AI Resource Center](https://airc.nist.gov/) or
  [aiframework@nist.gov](mailto:aiframework@nist.gov).
- For NIST OSCAL Team issues: file an issue in
  [usnistgov/OSCAL](https://github.com/usnistgov/OSCAL).
- For NIST CAISI: see the [CAISI website](https://www.nist.gov/caisi).

This project is a community work intended to be useful to the AI RMF
ecosystem until NIST publishes its own OSCAL representation. If NIST
publishes an authoritative OSCAL AI RMF artifact, this project will
explicitly defer to it.

## License of contributions

By submitting a contribution to this project, you agree that the
contribution is released under
[CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).

## Code of conduct

Project participants are expected to be respectful, constructive, and
focused on the technical work. Disagreements are normal and welcome;
personal attacks are not. Maintainers may close issues or PRs that do not
meet this standard.
