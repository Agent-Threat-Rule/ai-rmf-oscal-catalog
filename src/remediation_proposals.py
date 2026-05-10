"""
Remediation proposals for the 41 Playbook-vs-Core text divergences.

Source: source/PLAYBOOK_VS_CORE_DIVERGENCES.md (the empirical inventory).
Each proposal classifies the divergence and recommends an editorial action
that the Playbook editorial team or NIST OSCAL team can take to bring the
Playbook description fields into alignment with the canonical AI RMF Core
text reproduced in src/airmf_core_text.py.

Severity rubric:
    3 (semantic): substitutes one defined term for another, changing scope.
    2 (typo / systemic): single typo or a systemic capitalisation pattern.
    1 (minor): wording / punctuation / whitespace that does not change meaning.

Recommendation values:
    "adopt-core": align Playbook description to match Core text.
    "preserve-playbook": keep Playbook variant for guidance reasons (rare).

Output:
    source/playbook_remediation_proposals.json  (machine-readable)
    source/PLAYBOOK_REMEDIATION_PROPOSALS.md    (human-readable per-control)

Cross-reference: each proposal carries a `divergence_type` value matching
the tag used in source/PLAYBOOK_VS_CORE_DIVERGENCES.md so the two files
remain reconcilable.
"""

import json
from collections import defaultdict
from pathlib import Path

from airmf_core_text import ALL_SUBCATEGORIES

REPO = Path(__file__).resolve().parent.parent
SOURCE_PLAYBOOK = REPO / "source" / "ai-rmf-playbook.json"
OUT_JSON = REPO / "source" / "playbook_remediation_proposals.json"
OUT_MD = REPO / "source" / "PLAYBOOK_REMEDIATION_PROPOSALS.md"

# ---------------------------------------------------------------------
# Hand-curated proposals. Keys are short subcategory references.
# Each entry: type, severity, recommendation, patch, rationale.
# ---------------------------------------------------------------------

PROPOSALS: dict[str, dict] = {
    # ===================== GOVERN (9) =====================
    "GOVERN-1.2": {
        "type": "wording",
        "severity": 1,
        "recommendation": "adopt-core",
        "patch": "Append ', and practices' after 'processes, procedures'.",
        "rationale": (
            "Core text enumerates 'policies, processes, procedures, and practices'. "
            "Playbook drops the 'and practices' clause, narrowing the enumeration."
        ),
    },
    "GOVERN-1.3": {
        "type": "wording",
        "severity": 1,
        "recommendation": "adopt-core",
        "patch": "Replace 'Processes and procedures' with 'Processes, procedures, and practices'.",
        "rationale": (
            "Core uses the three-term enumeration consistently across GOVERN 1.x; "
            "Playbook uses two terms here."
        ),
    },
    "GOVERN-1.5": {
        "type": "wording",
        "severity": 1,
        "recommendation": "adopt-core",
        "patch": (
            "Replace ', organizational roles and responsibilities are clearly defined,' "
            "with ' and organizational roles and responsibilities clearly defined,'."
        ),
        "rationale": "Core uses 'and' to coordinate two clauses; Playbook uses comma + finite verb.",
    },
    "GOVERN-1.7": {
        "type": "wording",
        "severity": 1,
        "recommendation": "adopt-core",
        "patch": "Remove the word 'of' between 'phasing out' and 'AI systems'.",
        "rationale": "Core: 'phasing out AI systems'; Playbook: 'phasing out of AI systems'.",
    },
    "GOVERN-3.1": {
        "type": "typo",
        "severity": 2,
        "recommendation": "adopt-core",
        "patch": "Replace 'Decision-makings' with 'Decision-making'.",
        "rationale": (
            "Singular 'Decision-making' is the canonical AI RMF Core form and is grammatically "
            "standard in English. Playbook 'Decision-makings' is a clear typographical error."
        ),
    },
    "GOVERN-4.1": {
        "type": "wording",
        "severity": 1,
        "recommendation": "adopt-core",
        "patch": (
            "Remove the comma between 'policies' and 'and practices'. "
            "Insert 'potential ' before 'negative impacts'."
        ),
        "rationale": (
            "Core: 'Organizational policies and practices ... minimize potential negative impacts.' "
            "Playbook adds a stray comma and drops 'potential'."
        ),
    },
    "GOVERN-4.2": {
        "type": "wording",
        "severity": 1,
        "recommendation": "adopt-core",
        "patch": (
            "Insert comma between 'evaluate' and 'and use'. "
            "Replace 'and communicate' with 'and they communicate'."
        ),
        "rationale": (
            "Core uses the Oxford comma in the verb list and supplies the explicit pronoun "
            "subject 'they' in the second coordinated clause for clarity."
        ),
    },
    "GOVERN-5.2": {
        "type": "semantic",
        "severity": 3,
        "recommendation": "adopt-core",
        "patch": (
            "Replace the FIRST occurrence of 'AI actors' with 'the team that developed "
            "or deployed AI systems'. The second occurrence ('from relevant AI actors' "
            "later in the sentence) is unchanged in Core and must be preserved — a "
            "global find-replace would corrupt it."
        ),
        "rationale": (
            "Substantive divergence. Core narrows the obligated party to the team that "
            "developed or deployed AI systems; Playbook generalises to all 'AI actors' "
            "(which in AI RMF terminology includes users, regulators, and impacted "
            "communities). The two sets are not interchangeable. Compliance work that "
            "cites Playbook would assign the obligation to the wrong actors."
        ),
    },
    "GOVERN-6.1": {
        "type": "wording",
        "severity": 1,
        "recommendation": "adopt-core-with-caveat",
        "patch": "Replace 'third party' with 'third-party' (hyphenated).",
        "rationale": (
            "Core text at GOVERN 6.1 uses hyphenated 'third-party's', while Core text at "
            "MAP 4.1 uses unhyphenated 'third party's'. The Core itself is internally "
            "inconsistent; this proposal recommends Playbook align with whichever form Core "
            "selects after Core-side standardisation. See systemic finding S-2."
        ),
    },
    # ===================== MAP (11) =====================
    "MAP-1.1": {
        "type": "wording",
        "severity": 1,
        "recommendation": "adopt-core",
        "patch": (
            "Replace 'Intended purpose' with 'Intended purposes'. "
            "Insert 'the' before 'specific set or types of users'. "
            "Replace 'about AI system purposes; uses and risks' with "
            "'about AI system purposes, uses, and risks'. "
            "Replace 'TEVV and system metrics' with 'related TEVV and system metrics'."
        ),
        "rationale": (
            "Multiple wording differences across one long sentence. Core text uses plural "
            "'purposes', restructures the second list with an Oxford comma, and prefixes "
            "'related' to the metrics phrase."
        ),
    },
    "MAP-1.2": {
        "type": "wording",
        "severity": 1,
        "recommendation": "adopt-core",
        "patch": (
            "Replace 'Inter-disciplinary' with 'Interdisciplinary' (no hyphen). "
            "Insert comma after 'skills'."
        ),
        "rationale": "Spelling and punctuation alignment.",
    },
    "MAP-1.3": {
        "type": "wording",
        "severity": 1,
        "recommendation": "adopt-core",
        "patch": "Replace 'the AI technology' with 'AI technology' (drop definite article).",
        "rationale": "Core uses bare 'AI technology'.",
    },
    "MAP-1.6": {
        "type": "whitespace",
        "severity": 1,
        "recommendation": "adopt-core",
        "patch": (
            "Replace double space between 'AI actors.' and 'Design decisions' "
            "with a single space."
        ),
        "rationale": "Pure typographical: extra space character in Playbook.",
    },
    "MAP-2.1": {
        "type": "wording",
        "severity": 1,
        "recommendation": "adopt-core",
        "patch": (
            "Replace 'specific task, and methods used to implement the task, that the AI "
            "system will support is' with 'specific tasks and methods used to implement "
            "the tasks that the AI system will support are'."
        ),
        "rationale": "Singular vs plural and removal of comma-bounded apposition.",
    },
    "MAP-2.2": {
        "type": "wording",
        "severity": 1,
        "recommendation": "adopt-core",
        "patch": "Remove the word 'informed' before 'decisions'.",
        "rationale": "Core: 'when making decisions'; Playbook: 'when making informed decisions'.",
    },
    "MAP-3.2": {
        "type": "wording",
        "severity": 1,
        "recommendation": "adopt-core",
        "patch": "Replace ASCII hyphen-minus '-' bracketing 'as connected to organizational risk tolerance' with en dashes '–'.",
        "rationale": "Typographic dash. Core uses en dashes; Playbook uses hyphen-minus.",
    },
    "MAP-3.4": {
        "type": "whitespace",
        "severity": 1,
        "recommendation": "adopt-core",
        "patch": "Insert Oxford comma between 'assessed' and 'and documented'.",
        "rationale": "Core uses the Oxford comma; Playbook drops it.",
    },
    "MAP-3.5": {
        "type": "wording",
        "severity": 1,
        "recommendation": "adopt-core",
        "patch": "Replace 'GOVERN function' with 'the govern function' (lowercase, with article).",
        "rationale": (
            "Function-name casing. Core uses lowercase 'govern function' with the definite "
            "article. See systemic finding S-1 — same pattern as the function-name casing "
            "instances in MEASURE and MANAGE controls (12 controls touched in total)."
        ),
    },
    "MAP-4.1": {
        "type": "wording",
        "severity": 1,
        "recommendation": "adopt-core-with-caveat",
        "patch": "Replace 'third-party' (hyphenated) with 'third party' (open).",
        "rationale": (
            "Internally inconsistent within Core. Core MAP 4.1 uses 'third party' open; "
            "Core GOVERN 6.1 uses 'third-party' hyphenated. Recommend Core editorial team "
            "standardise. See systemic finding S-2."
        ),
    },
    "MAP-4.2": {
        "type": "whitespace",
        "severity": 1,
        "recommendation": "adopt-core",
        "patch": "Insert commas around 'including third-party AI technologies'.",
        "rationale": "Core punctuates as a non-restrictive parenthetical with bracketing commas.",
    },
    # ===================== MEASURE (14) =====================
    "MEASURE-1.1": {
        "type": "capitalisation",
        "severity": 2,
        "recommendation": "adopt-core",
        "patch": "Replace 'the Map function' (capital M) with 'the map function' (lowercase).",
        "rationale": "Function-name casing. See systemic finding S-1.",
    },
    "MEASURE-1.2": {
        "type": "wording",
        "severity": 1,
        "recommendation": "adopt-core",
        "patch": (
            "Replace 'is regularly assessed' with 'are regularly assessed'. "
            "Insert comma after 'updated'. "
            "Insert 'potential ' before 'impacts on affected communities'."
        ),
        "rationale": "Subject-verb agreement, comma, and 'potential' prefix.",
    },
    "MEASURE-2.1": {
        "type": "wording",
        "severity": 1,
        "recommendation": "adopt-core",
        "patch": (
            "Replace 'used during test, evaluation, validation, and verification (TEVV)' "
            "with 'used during TEVV'."
        ),
        "rationale": "Core uses the abbreviation; Playbook expands it inline.",
    },
    "MEASURE-2.4": {
        "type": "capitalisation",
        "severity": 2,
        "recommendation": "adopt-core",
        "patch": "Replace 'MAP function' with 'map function'.",
        "rationale": "Function-name casing. See systemic finding S-1.",
    },
    "MEASURE-2.6": {
        "type": "wording",
        "severity": 1,
        "recommendation": "adopt-core",
        "patch": (
            "Insert 'The ' at the start of the first sentence. "
            "Replace 'MAP function' with 'map function'. "
            "Replace 'and can fail safely' with 'and it can fail safely'. "
            "Replace 'Safety metrics implicate' with 'Safety metrics reflect'."
        ),
        "rationale": (
            "Multiple changes; word choice 'reflect' vs 'implicate' is more substantive but "
            "still arguably stylistic — 'reflect' is the clearer reading."
        ),
    },
    "MEASURE-2.7": {
        "type": "capitalisation",
        "severity": 2,
        "recommendation": "adopt-core",
        "patch": "Replace 'MAP function' with 'map function'.",
        "rationale": "Function-name casing. See systemic finding S-1.",
    },
    "MEASURE-2.8": {
        "type": "capitalisation",
        "severity": 2,
        "recommendation": "adopt-core",
        "patch": "Replace 'MAP function' with 'map function'.",
        "rationale": "Function-name casing. See systemic finding S-1.",
    },
    "MEASURE-2.9": {
        "type": "wording",
        "severity": 1,
        "recommendation": "adopt-core",
        "patch": (
            "Remove double space between 'and' and 'AI system output'. "
            "Replace 'MAP function' with 'map function'. "
            "Remove the word 'and' before 'to inform' (Core reads: 'as identified in the "
            "map function – to inform responsible use')."
        ),
        "rationale": (
            "Whitespace, function-name casing, and a small clause restructure (Core drops "
            "the connective 'and', producing a tighter dash-bracketed parenthetical)."
        ),
    },
    "MEASURE-2.10": {
        "type": "capitalisation",
        "severity": 2,
        "recommendation": "adopt-core",
        "patch": "Replace 'MAP function' with 'map function'.",
        "rationale": "Function-name casing. See systemic finding S-1.",
    },
    "MEASURE-2.11": {
        "type": "capitalisation",
        "severity": 2,
        "recommendation": "adopt-core",
        "patch": "Replace 'MAP function' with 'map function'.",
        "rationale": "Function-name casing. See systemic finding S-1.",
    },
    "MEASURE-2.12": {
        "type": "capitalisation",
        "severity": 2,
        "recommendation": "adopt-core",
        "patch": "Replace 'MAP function' with 'map function'.",
        "rationale": "Function-name casing. See systemic finding S-1.",
    },
    "MEASURE-2.13": {
        "type": "capitalisation",
        "severity": 2,
        "recommendation": "adopt-core",
        "patch": "Replace 'MEASURE function' with 'measure function'.",
        "rationale": "Function-name casing. See systemic finding S-1 (note: this one is the MEASURE function, not MAP).",
    },
    "MEASURE-4.2": {
        "type": "wording",
        "severity": 1,
        "recommendation": "adopt-core",
        "patch": (
            "Replace 'across AI lifecycle' with 'across the AI lifecycle'. "
            "Replace 'and other relevant AI actors' with 'and relevant AI actors'."
        ),
        "rationale": "Article addition and removal of 'other'.",
    },
    "MEASURE-4.3": {
        "type": "whitespace",
        "severity": 1,
        "recommendation": "adopt-core",
        "patch": (
            "Insert comma after 'AI actors'. "
            "Move comma from 'characteristics, are identified' to before 'are identified' "
            "(Core: '...trustworthiness characteristics are identified')."
        ),
        "rationale": "Comma placement.",
    },
    # ===================== MANAGE (7) =====================
    "MANAGE-1.1": {
        "type": "wording",
        "severity": 1,
        "recommendation": "adopt-core",
        "patch": "Replace 'intended purpose' with 'intended purposes' (plural).",
        "rationale": "Core uses plural. Same pattern as MAP 1.1.",
    },
    "MANAGE-1.2": {
        "type": "wording",
        "severity": 1,
        "recommendation": "adopt-core",
        "patch": "Replace 'or available resources or methods' with 'and available resources or methods'.",
        "rationale": (
            "'and' vs 'or' changes the scope: Core lists impact, likelihood, AND available "
            "resources as joint inputs; Playbook reads as alternative inputs."
        ),
    },
    "MANAGE-1.3": {
        "type": "wording",
        "severity": 1,
        "recommendation": "adopt-core",
        "patch": (
            "Insert comma after 'high priority'. "
            "Replace 'Map function' with 'map function'."
        ),
        "rationale": "Punctuation and function-name casing. See systemic finding S-1.",
    },
    "MANAGE-2.1": {
        "type": "wording",
        "severity": 1,
        "recommendation": "adopt-core",
        "patch": (
            "Replace ', along with viable non-AI alternative systems, approaches, or methods,' "
            "with ' – along with viable non-AI alternative systems, approaches, or methods –'."
        ),
        "rationale": "Core uses en-dash bracketing; Playbook uses commas.",
    },
    "MANAGE-2.4": {
        "type": "wording",
        "severity": 1,
        "recommendation": "adopt-core",
        "patch": (
            "Replace 'Mechanisms are in place and applied, responsibilities are assigned and "
            "understood to' with 'Mechanisms are in place and applied, and responsibilities "
            "are assigned and understood, to'."
        ),
        "rationale": "Adds connective 'and' and bracketing comma.",
    },
    "MANAGE-3.2": {
        "type": "whitespace",
        "severity": 1,
        "recommendation": "adopt-core",
        "patch": "Replace double space between 'regular' and 'monitoring' with single space.",
        "rationale": "Pure whitespace.",
    },
    "MANAGE-4.3": {
        "type": "whitespace",
        "severity": 1,
        "recommendation": "adopt-core",
        "patch": "Insert comma after 'AI actors' (before 'including affected communities').",
        "rationale": "Core uses non-restrictive comma.",
    },
}


# ---------------------------------------------------------------------
# Systemic findings — patterns that span multiple controls and would be
# better fixed at the editorial layer than per-control.
# ---------------------------------------------------------------------

SYSTEMIC_FINDINGS = [
    {
        "id": "S-1",
        "title": "Function-name casing inconsistency",
        "summary": (
            "AI RMF Core uses lowercase function names with the definite article inside "
            "control statements (e.g., 'as identified in the map function'). Playbook "
            "consistently uses uppercase ('the MAP function')."
        ),
        "scope": "12 controls",
        "controls_affected": [
            "MAP-3.5 (GOVERN function reference, with article addition)",
            "MEASURE-1.1, 2.4, 2.7, 2.8, 2.10, 2.11, 2.12 (MAP function — pure capitalisation)",
            "MEASURE-2.6, 2.9 (MAP function — capitalisation bundled with other wording changes)",
            "MEASURE-2.13 (MEASURE function — self-reference)",
            "MANAGE-1.3 (MAP function reference, with comma addition)",
        ],
        "recommendation": (
            "Rather than 12 per-control patches, the Playbook editorial process should adopt "
            "a single style rule: 'When referring to the four AI RMF functions inside a "
            "control description, use lowercase ({govern, map, measure, manage}) preceded "
            "by the definite article'. This matches AI RMF Core Section 5 and brings all "
            "12 controls into alignment in one edit."
        ),
    },
    {
        "id": "S-2",
        "title": "Hyphenation of 'third-party'",
        "summary": (
            "AI RMF Core itself is internally inconsistent: GOVERN 6.1 uses hyphenated "
            "'third-party's intellectual property'; MAP 4.1 uses open 'third party's "
            "intellectual property'. Playbook mirrors the inverse choice in each location."
        ),
        "scope": "2 controls (Core + Playbook both involved)",
        "controls_affected": ["GOVERN-6.1", "MAP-4.1"],
        "recommendation": (
            "This is a Core-side finding, not a Playbook-side correction. Recommend the "
            "AI RMF Core editorial team standardise to one form — Chicago Manual of Style "
            "and APA both prefer hyphenated 'third-party' as an attributive adjective. "
            "Once Core is consistent, Playbook can be aligned."
        ),
    },
]


# ---------------------------------------------------------------------
# Validation — sanity-check that every proposal corresponds to a real
# control in the catalog.
# ---------------------------------------------------------------------

def validate_proposals() -> list[str]:
    """Return list of validation errors. Empty list = all valid."""
    errors: list[str] = []
    for key, prop in PROPOSALS.items():
        try:
            function, subcat = key.split("-", 1)
        except ValueError:
            errors.append(f"{key}: malformed key (expected 'FUNCTION-N.M')")
            continue
        if function not in ALL_SUBCATEGORIES:
            errors.append(f"{key}: unknown function '{function}'")
            continue
        if subcat not in ALL_SUBCATEGORIES[function]:
            errors.append(f"{key}: subcategory '{subcat}' not in catalog")
            continue
        # Sanity-check required fields
        for field in ("type", "severity", "recommendation", "patch", "rationale"):
            if field not in prop:
                errors.append(f"{key}: missing field '{field}'")
        # Severity must be 1, 2, or 3
        if prop.get("severity") not in (1, 2, 3):
            errors.append(f"{key}: invalid severity {prop.get('severity')}")
        # Type must be one of the recognised tags
        valid_types = {"typo", "semantic", "capitalisation", "whitespace", "wording"}
        if prop.get("type") not in valid_types:
            errors.append(f"{key}: invalid type '{prop.get('type')}'")
    return errors


# ---------------------------------------------------------------------
# Output generators
# ---------------------------------------------------------------------

def _short_subcat_id(key: str) -> str:
    """'GOVERN-3.1' -> 'ai-rmf-gv-3.1'."""
    function, subcat = key.split("-", 1)
    prefix = {"GOVERN": "gv", "MAP": "mp", "MEASURE": "ms", "MANAGE": "mg"}[function]
    return f"ai-rmf-{prefix}-{subcat}"


def build_json() -> dict:
    proposals_out = []
    for key, prop in sorted(PROPOSALS.items()):
        function, subcat = key.split("-", 1)
        proposals_out.append({
            "control_id": _short_subcat_id(key),
            "function": function,
            "subcategory": subcat,
            "type": prop["type"],
            "severity": prop["severity"],
            "recommendation": prop["recommendation"],
            "patch": prop["patch"],
            "rationale": prop["rationale"],
            "core_text": ALL_SUBCATEGORIES[function][subcat],
        })

    by_severity = defaultdict(int)
    by_type = defaultdict(int)
    for p in proposals_out:
        by_severity[p["severity"]] += 1
        by_type[p["type"]] += 1

    return {
        "version": "0.4.0",
        "total_divergences": len(proposals_out),
        "by_severity": dict(by_severity),
        "by_type": dict(by_type),
        "systemic_findings": SYSTEMIC_FINDINGS,
        "proposals": proposals_out,
    }


def build_markdown() -> str:
    lines: list[str] = []
    lines.append("# Playbook-vs-Core remediation proposals\n")
    lines.append(
        "This document accompanies `source/PLAYBOOK_VS_CORE_DIVERGENCES.md`. "
        "Where the divergences file describes _what_ differs, this file proposes "
        "_what to do about it_. Each of the 41 divergences has a classification, "
        "severity, recommended action, and a literal patch suggestion that the "
        "AI RMF Playbook editorial team or the NIST OSCAL team can action.\n"
    )
    lines.append("Released under CC0 1.0 alongside the catalog.\n")
    lines.append("## Methodology\n")
    lines.append(
        "- Source A (canonical): AI RMF Core text reproduced verbatim in "
        "`src/airmf_core_text.py` from "
        "https://airc.nist.gov/airmf-resources/airmf/5-sec-core/.\n"
        "- Source B: AI RMF Playbook structured export at "
        "https://airc.nist.gov/docs/playbook.json.\n"
        "- For each of the 41 divergences identified in `PLAYBOOK_VS_CORE_DIVERGENCES.md`, "
        "the proposal classifies the divergence type, assigns a severity (1=cosmetic, "
        "2=typo or systemic capitalisation, 3=semantic), and recommends an action.\n"
        "- Recommendations are `adopt-core` (align Playbook to Core) by default, with "
        "two `adopt-core-with-caveat` cases where Core itself is internally inconsistent.\n"
    )

    by_severity = defaultdict(list)
    for key, prop in sorted(PROPOSALS.items()):
        by_severity[prop["severity"]].append((key, prop))

    by_type = defaultdict(int)
    for prop in PROPOSALS.values():
        by_type[prop["type"]] += 1

    lines.append("## Summary\n")
    lines.append(f"Total divergences proposed for remediation: **{len(PROPOSALS)}**\n")
    lines.append("By severity:")
    lines.append(f"- Severity 3 (semantic, scope-changing): **{len(by_severity[3])}**")
    lines.append(f"- Severity 2 (typo or systemic capitalisation): **{len(by_severity[2])}**")
    lines.append(f"- Severity 1 (minor wording / whitespace): **{len(by_severity[1])}**\n")
    lines.append("By type:")
    for type_name in ("semantic", "typo", "capitalisation", "wording", "whitespace"):
        if by_type[type_name]:
            lines.append(f"- {type_name}: **{by_type[type_name]}**")
    lines.append("")

    # Systemic findings first
    lines.append("## Systemic findings\n")
    lines.append(
        "These are patterns that span multiple controls and would be better addressed "
        "by an editorial style rule than by per-control edits.\n"
    )
    for sf in SYSTEMIC_FINDINGS:
        lines.append(f"### {sf['id']}: {sf['title']}\n")
        lines.append(f"**Summary:** {sf['summary']}\n")
        lines.append(f"**Scope:** {sf['scope']}\n")
        lines.append("**Controls affected:**")
        for c in sf["controls_affected"]:
            lines.append(f"- {c}")
        lines.append("")
        lines.append(f"**Recommendation:** {sf['recommendation']}\n")

    # Per-severity breakdown
    severity_titles = {
        3: "Severity 3 — Semantic (scope-changing)",
        2: "Severity 2 — Typo and systemic capitalisation",
        1: "Severity 1 — Minor wording and whitespace",
    }

    for sev in (3, 2, 1):
        items = by_severity[sev]
        if not items:
            continue
        lines.append(f"## {severity_titles[sev]}\n")
        for key, prop in items:
            function, subcat = key.split("-", 1)
            lines.append(f"### {key}\n")
            lines.append(f"- **Type:** {prop['type']}")
            lines.append(f"- **Severity:** {prop['severity']}")
            lines.append(f"- **Recommendation:** `{prop['recommendation']}`")
            lines.append(f"- **Control statement (Core):** {ALL_SUBCATEGORIES[function][subcat]}")
            lines.append(f"- **Patch:** {prop['patch']}")
            lines.append(f"- **Rationale:** {prop['rationale']}\n")

    lines.append("## Provenance\n")
    lines.append(
        "Proposals authored against AI RMF Core HTML rendering and Playbook JSON export "
        "fetched 2026-05-10. Curated by hand, sanity-checked against the catalog by "
        "`src/remediation_proposals.py:validate_proposals()`. All recommendations are "
        "non-binding suggestions for the AI RMF editorial team and the NIST OSCAL Team.\n"
    )

    return "\n".join(lines) + "\n"


def main() -> int:
    errors = validate_proposals()
    if errors:
        print("Validation errors:")
        for e in errors:
            print(f"  - {e}")
        return 1

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(build_json(), indent=2, ensure_ascii=False) + "\n")
    OUT_MD.write_text(build_markdown())

    by_severity = defaultdict(int)
    for prop in PROPOSALS.values():
        by_severity[prop["severity"]] += 1

    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    print(f"  total proposals:    {len(PROPOSALS)}")
    print(f"  severity 3 (semantic): {by_severity[3]}")
    print(f"  severity 2:            {by_severity[2]}")
    print(f"  severity 1:            {by_severity[1]}")
    print(f"  systemic findings:  {len(SYSTEMIC_FINDINGS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
