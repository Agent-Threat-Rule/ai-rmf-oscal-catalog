# AI RMF worked-example profiles — selection rationale

This document accompanies the two worked-example OSCAL profiles in `profiles/`.
It describes how each example selects controls from the community AI RMF v0.4
catalog and why specific subcategories were included or excluded.

These profiles are illustrative worked examples. They are not normative AI RMF
baselines, they are not official NIST tiers, and they have not been endorsed by
NIST. Downstream consumers should derive their own profiles based on the
specific risk posture and deployment context of their AI system.

## Why two examples

The AI RMF Core does not prescribe any grading or tiering — every subcategory is
presented as universally applicable, and the framework is explicitly designed to
be applied with the rigour that matches the context. These two examples simply
show two points on the spectrum of how much of the catalog a given deployment
might reasonably select, expressed purely as control counts:

- Example 1 (18 of 72 controls): one reasonable minimum selection for a low-risk,
  internal AI use.
- Example 2 (55 of 72 controls): a broader selection for AI whose outputs reach
  external users.

A deployment that wants the entire catalog does not need a dedicated profile: it
can import the catalog directly or use an `include-all` selection. A regulated or
safety-critical context is the natural case for exactly that — apply the full
catalog with no exclusions — so no separate select-all profile is shipped.

## Example 1 (18 controls)

GOVERN (7): 1.1, 1.2, 1.6, 2.1, 2.3, 4.1, 4.3
MAP (4): 1.1, 2.1, 3.5, 5.1
MEASURE (4): 1.1, 2.1, 2.6, 2.7
MANAGE (3): 1.1, 1.3, 4.3

Selection rationale:

- GOVERN minimum: legal compliance (1.1), trustworthy-AI principles (1.2),
  AI inventory (1.6), roles and responsibilities (2.1), executive
  accountability (2.3), safety-first culture (4.1), and incident testing
  with information sharing (4.3) — without these, an organisation does not
  have functioning AI governance at any scale.
- MAP minimum: intended purpose (1.1), task definition (2.1), human
  oversight (3.5), and impact identification (5.1) — establishes context
  before measurement.
- MEASURE minimum: metric selection (1.1), TEVV documentation (2.1), safety
  evaluation (2.6), security and resilience (2.7) — without these, the
  organisation cannot verify the system is performing as intended.
- MANAGE minimum: proceed / no-go determination (1.1), risk responses (1.3),
  incident communication (4.3) — minimum operational risk handling.

## Example 2 (55 controls = Example 1 + 37 additions)

Adds 37 controls covering:

- GOVERN additions (11): risk tolerance (1.3), transparent policies (1.4),
  ongoing monitoring (1.5), decommissioning (1.7), AI risk training (2.2),
  diverse decision-making (3.1), human-AI configuration (3.2), risk
  documentation and communication (4.2), external feedback (5.1, 5.2), and
  third-party AI risk policies (6.1).
- MAP additions (9): interdisciplinary actors (1.2), mission and goals (1.3),
  system requirements (1.6), knowledge limits (2.2), scientific integrity
  (2.3), benefits examination (3.1), third-party legal and risk mapping
  (4.1, 4.2), and broader engagement (5.2).
- MEASURE additions (9): performance criteria (2.3), functionality
  monitoring (2.4), validity and reliability (2.5), transparency and
  accountability (2.8), explainability (2.9), privacy (2.10), fairness and
  bias (2.11), risk tracking (3.1), and end-user feedback (3.3).
- MANAGE additions (8): risk treatment prioritisation (1.2), residual risks
  (1.4), resources (2.1), value sustainment (2.2), disengagement mechanisms
  (2.4), third-party monitoring (3.1), post-deployment monitoring (4.1), and
  continual improvement (4.2).

Excluded from Example 2 (17 controls):

The 17 controls left out are contextually specific — meaningful only in
particular deployment settings rather than for external-facing AI in general.
Representative exclusions: environmental-impact MEASURE 2.12, deep third-party
contingency GOVERN 6.2, unknown-risk recovery MANAGE 2.3, and human-subjects
protection MEASURE 2.2. The remainder are measurement-of-measurement
subcategories and depth-specialised aspects of context establishment. A
deployment for which any of these is in scope should add it back explicitly.

## Reproducibility

Both profiles are generated from `src/profile_generator.py`. Re-running that
script produces byte-identical output (UUIDs are deterministic uuid5 from the
project namespace; `last-modified` is preserved when content is unchanged).

Validate the profiles against the OSCAL profile schema:

    npm run validate-profiles
    python3 src/completeness_check.py
