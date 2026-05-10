# Maintainers

This file lists the maintainers of the AI RMF OSCAL Catalog project. The
maintainers are responsible for reviewing and merging pull requests,
triaging issues, and shepherding the project's evolution.

## Current maintainers

| Name        | GitHub                                              | Affiliation       | Role                  |
|-------------|-----------------------------------------------------|-------------------|-----------------------|
| Adam Lin    | [@eeee2345](https://github.com/eeee2345)            | Independent       | Founding maintainer   |

## Bus factor

The project currently has a bus factor of 1. This is a known risk and the
project is actively recruiting additional maintainers. If you are interested
in becoming a maintainer, see [becoming a maintainer](#becoming-a-maintainer).

## Decision making

Routine decisions (bug fixes, documentation, small additions) require
approval from one maintainer. The PR author and reviewer should be different
people, except for trivial fixes (typos, dependency bumps) which a maintainer
may merge on their own.

Substantive decisions (new tier profiles, structural catalog changes, new
non-canonical content) require:

- A GitHub issue describing the intent
- Open discussion period of at least 7 days
- Lazy consensus: if no maintainer objects within 7 days, the proposal is
  approved
- For breaking changes (modifying existing IDs, removing existing controls,
  bumping major version): explicit approval from at least 2 maintainers, or
  if the project still has only 1 maintainer, a 14-day public comment period

The project deliberately does not gate on consensus — explicit approval and
lazy approval both produce a clear decision record in the issue tracker.

## Becoming a maintainer

The project is actively looking for additional maintainers, particularly
people with:

- Experience with NIST OSCAL or AI RMF
- Experience with open-source standards work
- Time to triage issues and review PRs

To express interest, open an issue titled "Maintainer interest: [your
name]" with:

- Your background relevant to the project
- The kind of contributions you'd like to make
- Whether you have a conflict of interest to disclose (see below)

A new maintainer is added by consensus of existing maintainers after a
period of substantive contribution (typically 3+ merged PRs and active
participation in issue discussions over at least 8 weeks).

## Conflict of interest

Maintainers must disclose any commercial interest that could be perceived
as influencing project decisions. This includes:

- Working for a company that produces a competing or downstream OSCAL/AI
  governance product
- Holding a financial interest in such a company
- Being a NIST employee or contractor (in which case, recuse from
  decisions about NIST upstream coordination)

Disclosed conflicts are documented in this file. A maintainer with a
disclosed conflict may participate in discussion but must recuse from
final approval on PRs in the conflict area.

### Current conflict-of-interest disclosures

- **Adam Lin** is the founding maintainer of [Agent Threat Rules
  (ATR)](https://github.com/Agent-Threat-Rule/agent-threat-rules), an
  AI agent runtime detection rule corpus, and is associated with the
  PanGuard AI commercial product that uses ATR. ATR rules are
  separately mapped to AI RMF subcategories. The OSCAL catalog in this
  repository is intentionally vendor-neutral and contains no PanGuard or
  ATR-specific content. Adam recuses from decisions where ATR or PanGuard
  vendor interest could materially influence catalog content (e.g.,
  proposals to add ATR-specific implementation guidance to controls).

## Maintainer responsibilities

- Review PRs in a reasonable time (target: response within 7 days)
- Run validation locally before merging non-trivial changes
- Tag releases on GitHub using semantic version numbers (e.g., `v0.4.0`)
- Update [CHANGELOG.md](./CHANGELOG.md) for each release
- Coordinate with the NIST OSCAL Team and AI RMF team if upstream-relevant
  issues are identified
- Defer to NIST authoritative artifacts if/when published

## Removing a maintainer

A maintainer may resign at any time by editing this file. A maintainer who
has been inactive for 6+ months may be moved to "Emeritus" status by the
remaining active maintainers, with a clear PR record.

## Emeritus maintainers

(none)
