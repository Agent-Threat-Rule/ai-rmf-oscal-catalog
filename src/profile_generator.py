"""
AI RMF OSCAL profile generators (v0.4).

Emits four worked-example OSCAL profiles into profiles/, each importing the
community AI RMF v0.4 catalog. All profiles are released under CC0 1.0 and
are illustrative — they are not normative AI RMF baselines and have not been
endorsed by NIST.

Profiles:

    1. ai-rmf-baseline-profile.json
       The reference profile: 72 controls (include-all), no tier opinion.
       Useful when a downstream consumer needs the full catalog and wants to
       derive their own narrower profile from it.

    2. ai-rmf-tier-1-foundational-profile.json (NEW in v0.4)
       18 controls. Designed as the minimum viable AI risk management
       baseline: foundational governance, basic safety mapping, essential
       incident response. Suitable for internal, low-risk AI use (e.g.,
       internal-only content tools, low-stakes prediction models with human
       oversight).

    3. ai-rmf-tier-2-customer-facing-profile.json (NEW in v0.4)
       55 controls. Tier 1 plus the controls relevant when AI is deployed
       to external customers or end-users: fairness, explainability,
       privacy, post-deployment monitoring, third-party accountability.

    4. ai-rmf-tier-3-high-risk-profile.json (NEW in v0.4)
       72 controls (include-all), with high-risk-specific remarks. Designed
       for AI in regulated or safety-critical contexts (healthcare, finance,
       government, infrastructure). Same control selection as the baseline
       profile but with explicit narrative on why the full catalog applies.

Selection rationale for Tier 1 and Tier 2 is documented in each profile's
`remarks` field and in profiles/TIER_RATIONALE.md.

UUIDs are deterministic uuid5 from the project namespace so that regeneration
produces byte-stable output.

Usage:
    python3 src/profile_generator.py
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT_DIR = REPO / "profiles"

NAMESPACE_OID = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")  # url namespace per RFC 4122
ATR_OSCAL_NS = uuid.uuid5(NAMESPACE_OID, "https://github.com/Agent-Threat-Rule/ai-rmf-oscal-catalog")

CATALOG_HTTPS = (
    "https://raw.githubusercontent.com/Agent-Threat-Rule/ai-rmf-oscal-catalog/"
    "main/catalogs/ai-rmf-v0.4.json"
)
CATALOG_LOCAL = "../catalogs/ai-rmf-v0.4.json"


def stable_uuid(seed: str) -> str:
    return str(uuid.uuid5(ATR_OSCAL_NS, seed))


def control_id(function: str, subcat: str) -> str:
    prefix = {"GOVERN": "gv", "MAP": "mp", "MEASURE": "ms", "MANAGE": "mg"}[function]
    return f"ai-rmf-{prefix}-{subcat}"


# ---------------------------------------------------------------------
# Tier selections
# ---------------------------------------------------------------------

# Tier 1 (foundational baseline): 18 controls.
# Selection criteria: foundational governance + basic safety + essential
# incident response. Every AI system, regardless of deployment context,
# benefits from these controls.
TIER_1_CONTROLS = [
    # GOVERN — minimum governance scaffolding
    control_id("GOVERN", "1.1"),  # Legal and regulatory requirements
    control_id("GOVERN", "1.2"),  # Trustworthy AI characteristics integrated
    control_id("GOVERN", "1.6"),  # Inventory of AI systems
    control_id("GOVERN", "2.1"),  # Roles, responsibilities, communication
    control_id("GOVERN", "2.3"),  # Executive accountability
    control_id("GOVERN", "4.1"),  # Safety-first culture
    control_id("GOVERN", "4.3"),  # Incident testing and information sharing
    # MAP — minimum context establishment
    control_id("MAP", "1.1"),  # Intended purposes and prospective settings
    control_id("MAP", "2.1"),  # Specific tasks and methods defined
    control_id("MAP", "3.5"),  # Human oversight processes
    control_id("MAP", "5.1"),  # Likelihood and magnitude of impacts
    # MEASURE — minimum performance and safety evaluation
    control_id("MEASURE", "1.1"),  # Approaches and metrics for measurement
    control_id("MEASURE", "2.1"),  # Test sets and TEVV documentation
    control_id("MEASURE", "2.6"),  # Safety risks evaluated
    control_id("MEASURE", "2.7"),  # Security and resilience evaluated
    # MANAGE — minimum risk treatment and incident handling
    control_id("MANAGE", "1.1"),  # Determination to proceed
    control_id("MANAGE", "1.3"),  # Risk responses developed and documented
    control_id("MANAGE", "4.3"),  # Incidents communicated to AI actors
]
assert len(TIER_1_CONTROLS) == 18, f"Tier 1 expected 18 controls, got {len(TIER_1_CONTROLS)}"

# Tier 2 (customer-facing): 45 controls.
# Selection criteria: Tier 1 plus the controls that become operationally
# essential when AI outputs reach external users — fairness, explainability,
# privacy, accountability, post-deployment monitoring, third-party-related.
# Excludes specialised controls (e.g., MEASURE 2.12 environmental impact,
# GOVERN 6.x deep third-party governance) that are contextually specific.
TIER_2_CONTROLS = sorted(set(TIER_1_CONTROLS) | {
    # GOVERN additions: training, ethics, third-party basics
    control_id("GOVERN", "1.3"),  # Risk tolerance levels
    control_id("GOVERN", "1.4"),  # Risk priorities through transparent policies
    control_id("GOVERN", "1.5"),  # Ongoing monitoring of risk management
    control_id("GOVERN", "1.7"),  # Decommissioning processes
    control_id("GOVERN", "2.2"),  # AI risk management training
    control_id("GOVERN", "3.1"),  # Diverse decision-making team
    control_id("GOVERN", "3.2"),  # Human-AI configuration roles
    control_id("GOVERN", "4.2"),  # Risk impact documentation and communication
    control_id("GOVERN", "5.1"),  # External feedback collection
    control_id("GOVERN", "5.2"),  # Mechanisms for adjudicated feedback
    control_id("GOVERN", "6.1"),  # Third-party AI risk policies
    # MAP additions
    control_id("MAP", "1.2"),  # Interdisciplinary AI actors
    control_id("MAP", "1.3"),  # Mission and goals understood
    control_id("MAP", "1.6"),  # System requirements elicited
    control_id("MAP", "2.2"),  # Knowledge limits documented
    control_id("MAP", "2.3"),  # Scientific integrity and TEVV
    control_id("MAP", "3.1"),  # Benefits examined and documented
    control_id("MAP", "4.1"),  # Third-party legal risks mapped
    control_id("MAP", "4.2"),  # Third-party AI tech risk controls
    control_id("MAP", "5.2"),  # Engagement with relevant AI actors
    # MEASURE additions
    control_id("MEASURE", "2.3"),  # Performance criteria measured
    control_id("MEASURE", "2.4"),  # Functionality and behavior monitored
    control_id("MEASURE", "2.5"),  # Validity and reliability demonstrated
    control_id("MEASURE", "2.8"),  # Transparency and accountability risks
    control_id("MEASURE", "2.9"),  # Model explained and validated
    control_id("MEASURE", "2.10"),  # Privacy risk examined
    control_id("MEASURE", "2.11"),  # Fairness and bias evaluated
    control_id("MEASURE", "3.1"),  # Risk tracking approaches
    control_id("MEASURE", "3.3"),  # Feedback processes for end users
    # MANAGE additions
    control_id("MANAGE", "1.2"),  # Risk treatment prioritisation
    control_id("MANAGE", "1.4"),  # Negative residual risks documented
    control_id("MANAGE", "2.1"),  # Resources for managing AI risks
    control_id("MANAGE", "2.2"),  # Mechanisms to sustain AI system value
    control_id("MANAGE", "2.4"),  # Mechanisms to disengage AI systems
    control_id("MANAGE", "3.1"),  # Third-party AI risk monitoring
    control_id("MANAGE", "4.1"),  # Post-deployment monitoring plans
    control_id("MANAGE", "4.2"),  # Continual improvements integrated
})
assert len(TIER_2_CONTROLS) == 55, f"Tier 2 expected 55 controls, got {len(TIER_2_CONTROLS)}"


# ---------------------------------------------------------------------
# Profile builder
# ---------------------------------------------------------------------

def _preserved_last_modified(out_path: Path, new_doc: dict) -> str:
    fresh = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    if not out_path.exists():
        return fresh
    try:
        with out_path.open() as f:
            existing = json.load(f)
    except (OSError, json.JSONDecodeError):
        return fresh

    def stripped(doc: dict) -> dict:
        prof = dict(doc.get("profile", {}))
        meta = dict(prof.get("metadata", {}))
        meta.pop("last-modified", None)
        prof["metadata"] = meta
        return {"profile": prof}

    if stripped(existing) == stripped(new_doc):
        return existing.get("profile", {}).get("metadata", {}).get("last-modified", fresh)
    return fresh


def build_profile(*,
                  filename: str,
                  profile_uuid_seed: str,
                  resource_uuid_seed: str,
                  party_uuid_seed: str,
                  title: str,
                  selection: dict,
                  remarks: str) -> dict:
    """Builds one OSCAL profile document.

    `selection` is a dict like {"include-all": {}} or
    {"include-controls": [{"with-ids": [...]}]}.
    """
    out_path = OUT_DIR / filename
    catalog_resource_uuid = stable_uuid(resource_uuid_seed)
    party_uuid = stable_uuid(party_uuid_seed)

    profile = {
        "uuid": stable_uuid(profile_uuid_seed),
        "metadata": {
            "title": title,
            "last-modified": "PLACEHOLDER",
            "version": "0.4.0",
            "oscal-version": "1.2.2",
            "parties": [
                {
                    "uuid": party_uuid,
                    "type": "organization",
                    "name": "ai-rmf-oscal-catalog community contributors",
                    "remarks": (
                        "Community contributors to the ai-rmf-oscal-catalog project. "
                        "Not produced by, endorsed by, or affiliated with NIST."
                    ),
                },
            ],
            "remarks": remarks,
        },
        "imports": [
            {
                "href": f"#{catalog_resource_uuid}",
                **selection,
            },
        ],
        "merge": {
            "as-is": True,
        },
        "back-matter": {
            "resources": [
                {
                    "uuid": catalog_resource_uuid,
                    "title": "AI RMF community OSCAL catalog (v0.4)",
                    "description": (
                        "Resolves to the v0.4 catalog generated by src/generator.py "
                        "from this repository. Two rlinks are provided: the canonical "
                        "HTTPS URL on GitHub for production use, and a relative "
                        "filesystem path for local validation runs."
                    ),
                    "rlinks": [
                        {"href": CATALOG_HTTPS},
                        {"href": CATALOG_LOCAL},
                    ],
                    "remarks": (
                        "First rlink is preferred when validating from outside this "
                        "repository. Second rlink works when validating from inside "
                        "the repo (relative to profiles/)."
                    ),
                },
            ],
        },
    }

    document = {"profile": profile}
    profile["metadata"]["last-modified"] = _preserved_last_modified(out_path, document)
    return document


def write(out_path: Path, document: dict) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w") as f:
        json.dump(document, f, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------
# Profile-specific remarks
# ---------------------------------------------------------------------

REMARKS_BASELINE = (
    "Reference profile that imports the community AI RMF v0.4 catalog and "
    "selects all 72 subcategory controls (include-all). This profile is the "
    "simplest valid pattern, useful when a downstream consumer needs the "
    "complete catalog as a single profile and intends to derive a narrower "
    "selection by adding `exclude-controls` entries. It does not impose any "
    "tier opinion on the controls. Released under CC0 1.0. Not endorsed by NIST."
)

REMARKS_TIER_1 = (
    "Tier 1 — Foundational worked example. Selects 18 controls covering the "
    "minimum viable AI risk management surface for low-risk, internal AI use. "
    "Includes foundational governance (legal compliance, executive accountability, "
    "trustworthy AI integration, AI inventory, role definitions, safety culture, "
    "incident sharing); minimum context mapping (intended purposes, task "
    "definition, human oversight, impact identification); minimum measurement "
    "(metric selection, TEVV documentation, safety and security evaluation); "
    "and minimum risk treatment (proceed/no-go determination, risk responses, "
    "incident communication). This is a worked example, not a normative "
    "baseline. Released under CC0 1.0. Not endorsed by NIST."
)

REMARKS_TIER_2 = (
    "Tier 2 — Customer-facing worked example. Selects 55 controls (Tier 1 "
    "plus 37 additions). Designed for AI systems whose outputs reach external "
    "customers or end-users. Adds controls for fairness and bias evaluation, "
    "explainability and interpretability, privacy risk, accountability and "
    "transparency, post-deployment monitoring, continual improvement, "
    "third-party accountability, and external feedback mechanisms. Excludes "
    "specialised controls that are contextually specific (e.g., environmental "
    "impact MEASURE 2.12, deep third-party contingency GOVERN 6.2, unknown-risk "
    "recovery MANAGE 2.3, human-subjects-protection MEASURE 2.2). This is a "
    "worked example, not a normative baseline. Released under CC0 1.0. Not "
    "endorsed by NIST."
)

REMARKS_TIER_3 = (
    "Tier 3 — High-risk worked example. Selects all 72 controls (include-all) "
    "with the explicit framing that AI in regulated or safety-critical "
    "contexts (healthcare, finance, government, infrastructure, autonomous "
    "transport) requires the full AI RMF surface area. Differs from the "
    "baseline profile only in narrative framing. The same selection (all "
    "72 controls) but with the explicit position that exclusions are not "
    "appropriate for high-risk deployment contexts. This is a worked example, "
    "not a normative baseline. Released under CC0 1.0. Not endorsed by NIST."
)


# ---------------------------------------------------------------------
# Tier rationale doc
# ---------------------------------------------------------------------

TIER_RATIONALE_MD = """# AI RMF profile tiers — selection rationale

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
"""


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1) Baseline (existing, refreshed)
    baseline = build_profile(
        filename="ai-rmf-baseline-profile.json",
        profile_uuid_seed="profile:ai-rmf-baseline-v0.4",
        resource_uuid_seed="profile-catalog-resource:ai-rmf-v0.4",
        party_uuid_seed="profile-party:community",
        title="AI RMF Baseline Profile (community example)",
        selection={"include-all": {}},
        remarks=REMARKS_BASELINE,
    )
    write(OUT_DIR / "ai-rmf-baseline-profile.json", baseline)

    # 2) Tier 1 — foundational (18 controls)
    tier_1 = build_profile(
        filename="ai-rmf-tier-1-foundational-profile.json",
        profile_uuid_seed="profile:ai-rmf-tier-1-foundational-v0.4",
        resource_uuid_seed="profile-catalog-resource:ai-rmf-v0.4",
        party_uuid_seed="profile-party:community",
        title="AI RMF Tier 1 Foundational Profile (community example)",
        selection={"include-controls": [{"with-ids": TIER_1_CONTROLS}]},
        remarks=REMARKS_TIER_1,
    )
    write(OUT_DIR / "ai-rmf-tier-1-foundational-profile.json", tier_1)

    # 3) Tier 2 — customer-facing (45 controls)
    tier_2 = build_profile(
        filename="ai-rmf-tier-2-customer-facing-profile.json",
        profile_uuid_seed="profile:ai-rmf-tier-2-customer-facing-v0.4",
        resource_uuid_seed="profile-catalog-resource:ai-rmf-v0.4",
        party_uuid_seed="profile-party:community",
        title="AI RMF Tier 2 Customer-Facing Profile (community example)",
        selection={"include-controls": [{"with-ids": TIER_2_CONTROLS}]},
        remarks=REMARKS_TIER_2,
    )
    write(OUT_DIR / "ai-rmf-tier-2-customer-facing-profile.json", tier_2)

    # 4) Tier 3 — high-risk (72 controls, include-all with high-risk framing)
    tier_3 = build_profile(
        filename="ai-rmf-tier-3-high-risk-profile.json",
        profile_uuid_seed="profile:ai-rmf-tier-3-high-risk-v0.4",
        resource_uuid_seed="profile-catalog-resource:ai-rmf-v0.4",
        party_uuid_seed="profile-party:community",
        title="AI RMF Tier 3 High-Risk Profile (community example)",
        selection={"include-all": {}},
        remarks=REMARKS_TIER_3,
    )
    write(OUT_DIR / "ai-rmf-tier-3-high-risk-profile.json", tier_3)

    # 5) Tier rationale doc
    (OUT_DIR / "TIER_RATIONALE.md").write_text(TIER_RATIONALE_MD)

    print(f"wrote {OUT_DIR}/ai-rmf-baseline-profile.json (72 controls, include-all)")
    print(f"wrote {OUT_DIR}/ai-rmf-tier-1-foundational-profile.json ({len(TIER_1_CONTROLS)} controls)")
    print(f"wrote {OUT_DIR}/ai-rmf-tier-2-customer-facing-profile.json ({len(TIER_2_CONTROLS)} controls)")
    print(f"wrote {OUT_DIR}/ai-rmf-tier-3-high-risk-profile.json (72 controls, include-all)")
    print(f"wrote {OUT_DIR}/TIER_RATIONALE.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
