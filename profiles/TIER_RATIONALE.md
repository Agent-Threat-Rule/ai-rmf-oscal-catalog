# AI RMF profile tiers — selection rationale

This document accompanies the four worked-example OSCAL profiles in
`profiles/`. It describes how each tier was constructed and why specific
controls were selected or excluded.

These profiles are illustrative worked examples. They are not normative AI
RMF baselines, and they have not been endorsed by NIST. Downstream consumers
should derive their own profiles based on the specific risk posture and
deployment context of their AI system.

## Tiering principles

The AI RMF Core does not prescribe tiering — every subcategory is presented
as universally applicable, and the framework is explicitly designed to be
applied with the rigour that matches the context. These worked examples take
that principle and make three illustrative tiering choices a deploying
organisation might reasonably make:

- **Tier 1 (Foundational):** the minimum viable surface for low-risk
  internal AI use. Below this, the controls left out are unlikely to be
  meaningful in the deployed context.
- **Tier 2 (Customer-Facing):** the operationally essential surface when AI
  outputs reach external users — adds fairness, explainability, privacy,
  accountability, post-deployment monitoring, and third-party concerns.
- **Tier 3 (High-Risk):** the full catalog, framed for regulated or
  safety-critical contexts where exclusions are not appropriate.

## Tier 1 (18 controls)

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
- MANAGE minimum: proceed/no-go determination (1.1), risk responses (1.3),
  incident communication (4.3) — minimum operational risk handling.

## Tier 2 (55 controls = Tier 1 + 37 additions)

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

Excluded from Tier 2 (17 controls):

- GOVERN 6.2 (third-party contingency processes) — relevant only when
  high-risk third-party systems are in scope.
- MAP 1.4 (business value), MAP 1.5 (risk tolerance specific), MAP 3.1
  (benefits) [moved to T2], MAP 3.2 (cost analysis), MAP 3.3 (application
  scope), MAP 3.4 (operator proficiency) — depth-specialised aspects of
  context establishment.
- MEASURE 1.2 (metric appropriateness), 1.3 (internal experts), 2.2 (human
  subjects), 2.12 (environmental impact), 2.13 (TEVV effectiveness), 3.2
  (settings without measurement), 4.1-4.3 (measurement-of-measurement
  feedback) — measurement-of-measurement and contextually specific.
- MANAGE 2.3 (recover from previously unknown risk), MANAGE 3.2 (pre-trained
  model monitoring) — specialised operational controls.

## Tier 3 (72 controls)

Identical control selection to the baseline profile (include-all). The
distinction is narrative: Tier 3 is framed for regulated or safety-critical
deployment contexts where exclusions from the catalog are not appropriate.

## Reproducibility

All four profiles are generated from `src/profile_generator.py`. Re-running
that script produces byte-identical output (UUIDs are deterministic uuid5
from the project namespace; `last-modified` is preserved when content is
unchanged).

Validate any profile against the OSCAL profile schema:

    python3 src/validate_profiles.py
    python3 src/completeness_check.py
