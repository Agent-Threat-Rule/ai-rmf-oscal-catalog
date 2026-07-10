"""
AI RMF OSCAL worked-example profile generators.

Emits two worked-example OSCAL profiles into profiles/, each importing the
community AI RMF v0.4 catalog. Both profiles are released under CC0 1.0 and
are illustrative — they are not normative AI RMF baselines, they are not
official NIST tiers, and they have not been endorsed by NIST.

Profiles:

    1. ai-rmf-example-1-profile.json
       18 of the 72 controls. One reasonable minimum selection for low-risk,
       internal AI use: foundational governance, basic context mapping,
       essential measurement, and minimum risk treatment.

    2. ai-rmf-example-2-profile.json
       55 of the 72 controls (example 1 plus 37 additions). A broader
       selection for AI whose outputs reach external users: fairness,
       explainability, privacy, post-deployment monitoring, third-party
       accountability, and external feedback.

A deployment that wants the entire catalog does not need a dedicated profile —
it imports the catalog directly or uses an include-all selection — so no
select-all profile is shipped.

Selection rationale for each example is documented in the profile's `remarks`
field and in profiles/EXAMPLES_RATIONALE.md.

UUIDs are deterministic uuid5 from the project namespace so that regeneration
produces byte-stable output. The uuid5 seeds are retained verbatim from the
pre-rename artifacts so that each profile keeps a stable UUID across the
rename.

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
# Example selections
# ---------------------------------------------------------------------

# Example 1: 18 controls.
# One reasonable minimum selection for low-risk, internal AI use — foundational
# governance + basic safety + essential incident response.
EXAMPLE_1_CONTROLS = [
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
assert len(EXAMPLE_1_CONTROLS) == 18, f"Example 1 expected 18 controls, got {len(EXAMPLE_1_CONTROLS)}"

# Example 2: 55 controls.
# Example 1 plus the controls that become operationally essential when AI
# outputs reach external users — fairness, explainability, privacy,
# accountability, post-deployment monitoring, third-party-related. Excludes
# specialised controls (e.g., MEASURE 2.12 environmental impact, GOVERN 6.x
# deep third-party governance) that are contextually specific.
EXAMPLE_2_CONTROLS = sorted(set(EXAMPLE_1_CONTROLS) | {
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
assert len(EXAMPLE_2_CONTROLS) == 55, f"Example 2 expected 55 controls, got {len(EXAMPLE_2_CONTROLS)}"


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

    `selection` is a dict like {"include-controls": [{"with-ids": [...]}]}.
    """
    out_path = OUT_DIR / filename
    catalog_resource_uuid = stable_uuid(resource_uuid_seed)
    party_uuid = stable_uuid(party_uuid_seed)

    profile = {
        "uuid": stable_uuid(profile_uuid_seed),
        "metadata": {
            "title": title,
            "last-modified": "PLACEHOLDER",
            "version": "0.5.0",
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
# Profile-specific remarks (no tier / foundational / customer-facing taxonomy)
# ---------------------------------------------------------------------

REMARKS_EXAMPLE_1 = (
    "Worked example profile selecting 18 of the 72 AI RMF subcategory controls. "
    "It illustrates one reasonable minimum selection for low-risk, internal AI "
    "use: foundational governance (legal compliance, executive accountability, "
    "trustworthy-AI integration, AI inventory, role definitions, safety culture, "
    "incident sharing), minimum context mapping (intended purposes, task "
    "definition, human oversight, impact identification), minimum measurement "
    "(metric selection, TEVV documentation, safety and security evaluation), and "
    "minimum risk treatment (proceed / no-go determination, risk responses, "
    "incident communication). This is one community-authored worked example, not "
    "a normative baseline and not an official tier. Released under CC0 1.0. Not "
    "produced by, endorsed by, or affiliated with NIST."
)

REMARKS_EXAMPLE_2 = (
    "Worked example profile selecting 55 of the 72 AI RMF subcategory controls "
    "(the 18 controls of example 1 plus 37 additions). It illustrates a broader "
    "selection for AI systems whose outputs reach external users: fairness and "
    "bias evaluation, explainability and interpretability, privacy risk, "
    "accountability and transparency, post-deployment monitoring, continual "
    "improvement, third-party accountability, and external feedback mechanisms. "
    "It excludes a small set of context-specific controls (for example "
    "environmental-impact MEASURE 2.12, deep third-party contingency GOVERN 6.2, "
    "unknown-risk recovery MANAGE 2.3, human-subjects-protection MEASURE 2.2). "
    "This is one community-authored worked example, not a normative baseline and "
    "not an official tier. Released under CC0 1.0. Not produced by, endorsed by, "
    "or affiliated with NIST."
)


# ---------------------------------------------------------------------
# Examples rationale doc
# ---------------------------------------------------------------------

EXAMPLES_RATIONALE_MD = """# AI RMF worked-example profiles — selection rationale

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
"""


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1) Example 1 (18 controls). UUID seed retained from the pre-rename
    #    artifact so the profile keeps a stable UUID across the rename.
    example_1 = build_profile(
        filename="ai-rmf-example-1-profile.json",
        profile_uuid_seed="profile:ai-rmf-tier-1-foundational-v0.4",
        resource_uuid_seed="profile-catalog-resource:ai-rmf-v0.4",
        party_uuid_seed="profile-party:community",
        title="AI RMF Example Profile 1 - 18-control subset (community example)",
        selection={"include-controls": [{"with-ids": EXAMPLE_1_CONTROLS}]},
        remarks=REMARKS_EXAMPLE_1,
    )
    write(OUT_DIR / "ai-rmf-example-1-profile.json", example_1)

    # 2) Example 2 (55 controls). UUID seed retained from the pre-rename
    #    artifact so the profile keeps a stable UUID across the rename.
    example_2 = build_profile(
        filename="ai-rmf-example-2-profile.json",
        profile_uuid_seed="profile:ai-rmf-tier-2-customer-facing-v0.4",
        resource_uuid_seed="profile-catalog-resource:ai-rmf-v0.4",
        party_uuid_seed="profile-party:community",
        title="AI RMF Example Profile 2 - 55-control subset (community example)",
        selection={"include-controls": [{"with-ids": EXAMPLE_2_CONTROLS}]},
        remarks=REMARKS_EXAMPLE_2,
    )
    write(OUT_DIR / "ai-rmf-example-2-profile.json", example_2)

    # 3) Examples rationale doc
    (OUT_DIR / "EXAMPLES_RATIONALE.md").write_text(EXAMPLES_RATIONALE_MD)

    print(f"wrote {OUT_DIR}/ai-rmf-example-1-profile.json ({len(EXAMPLE_1_CONTROLS)} controls)")
    print(f"wrote {OUT_DIR}/ai-rmf-example-2-profile.json ({len(EXAMPLE_2_CONTROLS)} controls)")
    print(f"wrote {OUT_DIR}/EXAMPLES_RATIONALE.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
