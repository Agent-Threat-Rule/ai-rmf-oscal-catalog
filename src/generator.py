"""
AI RMF OSCAL Catalog generator (all four functions, v0.2).

Builds catalogs/ai-rmf-v0.2.json conforming to OSCAL v1.2.2 catalog schema.
Control statements and category statements are taken verbatim from the AI RMF
Core (NIST AI 100-1) — see src/airmf_core_text.py. Implementation guidance
parts (about, suggested actions, documentation questions, references) come
from source/ai-rmf-playbook.json (NIST AI RMF Playbook structured export).

Why two sources: a 2026-05-10 audit found 41 of 72 subcategory descriptions
in the Playbook JSON drift from the AI RMF Core canonical text. Compliance
work cites the Core, so control statements use the Core; the Playbook
content fills in implementation guidance which is Playbook-native.

OSCAL structure: top-level groups represent the four AI RMF functions
(GOVERN, MAP, MEASURE, MANAGE); each function group contains category groups;
each category group contains controls (subcategories).

Usage:
    python3 src/generator.py
"""

import json
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from airmf_core_text import (
    ALL_CATEGORIES,
    ALL_SUBCATEGORIES,
    GOVERN_CATEGORIES, GOVERN_SUBCATEGORIES,
    MAP_CATEGORIES, MAP_SUBCATEGORIES,
    MEASURE_CATEGORIES, MEASURE_SUBCATEGORIES,
    MANAGE_CATEGORIES, MANAGE_SUBCATEGORIES,
)
from cross_references import extract_links

REPO = Path(__file__).resolve().parent.parent
SOURCE_PATH = REPO / "source" / "ai-rmf-playbook.json"
OUTPUT_PATH = REPO / "catalogs" / "ai-rmf-v0.3.json"

NS = "https://github.com/Agent-Threat-Rule/ai-rmf-oscal-catalog/ns"
NAMESPACE_OID = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")  # url namespace per RFC 4122
ATR_OSCAL_NS = uuid.uuid5(NAMESPACE_OID, "https://github.com/Agent-Threat-Rule/ai-rmf-oscal-catalog")

# Function name in source data (Playbook 'type') and in Core/AIRC titles map to
# short OSCAL-friendly prefixes used in IDs and to upper-case names used in titles.
FUNCTION_PREFIXES = {
    "GOVERN": "gv",
    "MAP": "mp",
    "MEASURE": "ms",
    "MANAGE": "mg",
}

PLAYBOOK_FUNCTION_FIELD = "type"  # values are 'Govern', 'Map', 'Measure', 'Manage' (mixed case in source)


def stable_uuid(seed: str) -> str:
    return str(uuid.uuid5(ATR_OSCAL_NS, seed))


def make_part(name: str, prose: str, ns: str | None = None) -> dict:
    part = {"name": name, "prose": prose.strip()}
    if ns is not None:
        part["ns"] = ns
    return part


def make_props(actors, topics) -> list:
    props: list = []
    for a in actors or []:
        props.append({"name": "ai-rmf-actor", "value": a, "ns": NS})
    for t in topics or []:
        props.append({"name": "ai-rmf-topic", "value": t, "ns": NS})
    return props


def split_subcat(title: str) -> tuple[str, str, str, str]:
    """Return (function_upper, cat_num, subcat_num, full_subcat_key).

    Title format in playbook source: 'GOVERN 1.1', 'MAP 2.3', etc.
    """
    function_word, num = title.split(" ", 1)
    function_upper = function_word.upper()
    cat_num, subcat_num = num.split(".")
    return function_upper, cat_num, subcat_num, num


def make_control(item: dict) -> dict:
    function_upper, cat_num, subcat_num, key = split_subcat(item["title"])
    prefix = FUNCTION_PREFIXES[function_upper]
    control_id = f"ai-rmf-{prefix}-{cat_num}.{subcat_num}"

    statement_text = ALL_SUBCATEGORIES[function_upper].get(key)
    if not statement_text:
        raise ValueError(
            f"missing AI RMF Core text for {function_upper} {key}; update src/airmf_core_text.py"
        )

    parts: list[dict] = [make_part("statement", statement_text)]

    # Implementation guidance from Playbook. Custom (non-standard) part names
    # carry the project ns so consumers know they are local extensions.
    if item.get("section_about"):
        parts.append(make_part("guidance", item["section_about"]))
    if item.get("section_actions"):
        parts.append(make_part("ai-rmf-suggested-actions", item["section_actions"], ns=NS))
    if item.get("section_doc"):
        parts.append(make_part("ai-rmf-documentation-questions", item["section_doc"], ns=NS))
    if item.get("section_ref"):
        parts.append(make_part("ai-rmf-references", item["section_ref"], ns=NS))

    control = {
        "id": control_id,
        "class": "ai-rmf-subcategory",
        "title": item["title"],
        "parts": parts,
    }
    props = make_props(item.get("AI Actors"), item.get("Topic"))
    if props:
        control["props"] = props
    links = extract_links(item, function_upper, control_id)
    if links:
        control["links"] = links
    return control


def make_category_group(function_upper: str, category_num: str, items: list) -> dict:
    prefix = FUNCTION_PREFIXES[function_upper]
    category_id = f"ai-rmf-{prefix}-{category_num}"
    category_text = ALL_CATEGORIES[function_upper].get(category_num)
    if not category_text:
        raise ValueError(
            f"missing AI RMF Core text for {function_upper}-{category_num}; update src/airmf_core_text.py"
        )

    items_sorted = sorted(items, key=lambda i: int(i["title"].split(".")[1]))

    return {
        "id": category_id,
        "class": "ai-rmf-category",
        "title": f"{function_upper} {category_num}",
        "parts": [make_part("ai-rmf-category-statement", category_text, ns=NS)],
        "controls": [make_control(i) for i in items_sorted],
    }


def make_function_group(function_upper: str, items: list) -> dict:
    """Outer group representing one AI RMF function (GOVERN, MAP, MEASURE, MANAGE).

    Contains nested category groups, each containing the subcategory controls.
    """
    prefix = FUNCTION_PREFIXES[function_upper]
    function_id = f"ai-rmf-{prefix}"

    by_cat: dict[str, list] = defaultdict(list)
    for it in items:
        _, cat_num, _, _ = split_subcat(it["title"])
        by_cat[cat_num].append(it)

    cat_groups = [
        make_category_group(function_upper, c, by_cat[c])
        for c in sorted(by_cat.keys(), key=int)
    ]

    return {
        "id": function_id,
        "class": "ai-rmf-function",
        "title": function_upper,
        "groups": cat_groups,
    }


def preserved_last_modified(new_doc: dict) -> str:
    """Return the existing catalog's last-modified if substantive content
    (excluding the timestamp field itself) is byte-identical to the new
    document; otherwise return a fresh ISO-8601 UTC timestamp.
    """
    fresh = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    if not OUTPUT_PATH.exists():
        return fresh
    try:
        with OUTPUT_PATH.open() as f:
            existing = json.load(f)
    except (OSError, json.JSONDecodeError):
        return fresh

    def stripped(doc: dict) -> dict:
        cat = dict(doc.get("catalog", {}))
        meta = dict(cat.get("metadata", {}))
        meta.pop("last-modified", None)
        cat["metadata"] = meta
        return {"catalog": cat}

    if stripped(existing) == stripped(new_doc):
        return existing.get("catalog", {}).get("metadata", {}).get("last-modified", fresh)
    return fresh


def build_catalog(playbook: list) -> dict:
    by_function: dict[str, list] = defaultdict(list)
    for item in playbook:
        function_upper = item[PLAYBOOK_FUNCTION_FIELD].upper()
        if function_upper not in FUNCTION_PREFIXES:
            continue
        by_function[function_upper].append(item)

    function_order = ["GOVERN", "MAP", "MEASURE", "MANAGE"]
    groups = [make_function_group(fn, by_function[fn]) for fn in function_order if fn in by_function]

    nist_party_uuid = stable_uuid("party:nist")

    catalog = {
        "uuid": stable_uuid("catalog:ai-rmf-v0.3"),
        "metadata": {
            "title": "NIST AI Risk Management Framework: full catalog (community OSCAL)",
            "last-modified": "PLACEHOLDER",
            "version": "0.3.0",
            "oscal-version": "1.2.2",
            "parties": [
                {
                    "uuid": nist_party_uuid,
                    "type": "organization",
                    "name": "National Institute of Standards and Technology",
                    "short-name": "NIST",
                    "remarks": (
                        "NIST is the authoritative source of AI Risk Management Framework "
                        "text reproduced in this catalog. NIST does not publish or endorse "
                        "this community OSCAL representation."
                    ),
                },
            ],
            "remarks": (
                "Community-contributed OSCAL catalog covering all four functions of "
                "NIST AI RMF 1.0 (GOVERN, MAP, MEASURE, MANAGE). Statement and category "
                "text reproduced verbatim from the AI RMF Core (Section 5, Tables 1-4). "
                "Implementation guidance parts (about, suggested actions, documentation "
                "questions, references) are reproduced from the AI RMF Playbook structured "
                "export. Released under CC0 1.0. Not endorsed by NIST. The NIST OSCAL "
                "Team is the authoritative source for any official AI RMF OSCAL artifact."
            ),
        },
        "groups": groups,
        "back-matter": {
            "resources": [
                {
                    "uuid": stable_uuid("resource:ai-rmf-1.0"),
                    "title": "NIST AI Risk Management Framework (AI RMF 1.0)",
                    "rlinks": [
                        {"href": "https://doi.org/10.6028/NIST.AI.100-1"},
                    ],
                    "remarks": (
                        "NIST AI 100-1, January 2023. Source of AI RMF Core text "
                        "reproduced in this catalog (control and category statements)."
                    ),
                },
                {
                    "uuid": stable_uuid("resource:ai-rmf-core-page"),
                    "title": "AI RMF Core (online)",
                    "rlinks": [
                        {"href": "https://airc.nist.gov/airmf-resources/airmf/5-sec-core/"},
                    ],
                    "remarks": (
                        "Online AIRC rendering of AI RMF Core Section 5, used as the "
                        "extraction source for verbatim Core text in src/airmf_core_text.py."
                    ),
                },
                {
                    "uuid": stable_uuid("resource:ai-rmf-playbook"),
                    "title": "NIST AI RMF Playbook",
                    "rlinks": [
                        {"href": "https://airc.nist.gov/airmf-resources/playbook/"},
                        {"href": "https://airc.nist.gov/docs/playbook.json"},
                    ],
                    "remarks": (
                        "Structured Playbook export. Source of implementation guidance "
                        "parts (about, suggested actions, documentation questions, "
                        "references). The Playbook contains 41 textual deviations from "
                        "the Core across 72 subcategories (typos, conjunctions, "
                        "pluralisation, capitalisation, and at least one semantic "
                        "divergence at GOVERN 5.2); the Playbook is therefore not used "
                        "as the source for Core control statements. See "
                        "source/ATTRIBUTION.md for the full inventory."
                    ),
                },
            ],
        },
    }

    document = {"catalog": catalog}
    catalog["metadata"]["last-modified"] = preserved_last_modified(document)
    return document


def main() -> int:
    with SOURCE_PATH.open() as f:
        playbook = json.load(f)

    catalog = build_catalog(playbook)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    function_groups = catalog["catalog"]["groups"]
    total_categories = sum(len(fg.get("groups", [])) for fg in function_groups)
    all_controls = [
        c
        for fg in function_groups
        for cg in fg.get("groups", [])
        for c in cg.get("controls", [])
    ]
    total_controls = len(all_controls)
    total_links = sum(len(c.get("links") or []) for c in all_controls)
    controls_with_links = sum(1 for c in all_controls if c.get("links"))
    print(f"wrote {OUTPUT_PATH}")
    print(f"  function groups: {len(function_groups)}")
    print(f"  category groups: {total_categories}")
    print(f"  controls:        {total_controls}")
    print(f"  cross-ref links: {total_links} across {controls_with_links} controls")
    print(f"  last-modified:   {catalog['catalog']['metadata']['last-modified']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
