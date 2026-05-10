# Source attribution

This catalog reproduces text from two NIST publications. Both are works of the
U.S. Government and not subject to copyright in the United States; reproduction
under CC0 1.0 in this repository is therefore permitted.

## Sources

### AI RMF Core (canonical control and category statements)

- Document: NIST AI Risk Management Framework (AI RMF 1.0), NIST AI 100-1, January 2023
- DOI: https://doi.org/10.6028/NIST.AI.100-1
- Online rendering: https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
- Sections used: Section 5, Tables 1 (GOVERN), 2 (MAP), 3 (MEASURE), 4 (MANAGE)
- Extracted on: 2026-05-10
- Extracted snapshot SHA-256: `8e331f63a1d13133049ae15753c9af45f6e3b48d112d8e51153408988c1dcbcb` (HTML rendering at extraction time)

The 19 AI RMF category statements and 72 subcategory statements reproduced
in `src/airmf_core_text.py` are taken verbatim from this source. Each
catalog control's `statement` part and each catalog category group's
`ai-rmf-category-statement` part contains the corresponding verbatim text.

### AI RMF Playbook (implementation guidance)

- Resource: NIST AI RMF Playbook
- HTML landing: https://airc.nist.gov/airmf-resources/playbook/
- Structured export: https://airc.nist.gov/docs/playbook.json
- Fetched on: 2026-05-10
- Local copy: `source/ai-rmf-playbook.json`
- Local SHA-256: `abf907645b9310d8e7b4c13ef485f79b829f453060a3af81c45db5902354fb67`

The Playbook export supplies four implementation guidance fields per
subcategory which appear in the catalog as additional parts on each control:

| Playbook field | Catalog part name (with ns) |
|---|---|
| `section_about` | `guidance` (standard OSCAL part name) |
| `section_actions` | `ai-rmf-suggested-actions` |
| `section_doc` | `ai-rmf-documentation-questions` |
| `section_ref` | `ai-rmf-references` |

The Playbook is described by NIST as "a living resource ... expected to evolve
as AI technology advances," with updates released approximately twice annually.
The fetch date and hash above pin the snapshot used for this release.

## Core vs Playbook divergence

A 2026-05-10 cross-check of the 72 subcategory descriptions in
`source/ai-rmf-playbook.json` against the AI RMF Core HTML rendering found
**41 textual deviations across all four functions** (56.9% of subcategories).
The full per-divergence inventory is in `PLAYBOOK_VS_CORE_DIVERGENCES.md`.

Headlines:

- 1 typo: GOVERN 3.1 — Playbook "Decision-makings" vs Core "Decision-making"
- 1 semantic divergence: GOVERN 5.2 — Playbook "AI actors" vs Core "the team that developed or deployed AI systems" (different stakeholder set in AI RMF terminology)
- 7 capitalisation-only: function name "MAP function" / "MEASURE function" / "MANAGE function" in Playbook is rendered as lower-case "map function" / "measure function" / "manage function" in Core
- 32 minor wording: commas, conjunctions ("and" vs "or"), pluralisation ("purpose" vs "purposes"), "and practices" included in Core but missing in Playbook, hyphenation ("Inter-disciplinary" vs "Interdisciplinary"), etc.

For control statements (the canonical text typically cited in compliance
work), the catalog uses the Core wording. The Playbook content is reproduced
unchanged in the implementation guidance parts, where it is Playbook-native
content.

## Updates

When NIST publishes a new AI RMF revision or a new Playbook export:

1. Update `source/ai-rmf-playbook.json` and refresh the hash and fetch date in
   this file.
2. If the Core has changed, update `src/airmf_core_text.py` accordingly. Run
   `python3 tests/test_core_text_drift.py` (a CI helper that re-fetches the
   AIRC Core HTML and diffs against the embedded constants) to detect drift.
3. Re-run `python3 src/generator.py` to rebuild the catalog. The generator
   preserves `last-modified` if substantive content is byte-identical to
   the prior catalog, and updates it otherwise.
4. Bump catalog `version` if the change is substantive.
5. Update `PLAYBOOK_VS_CORE_DIVERGENCES.md` if Playbook updates change which
   subcategories drift.
