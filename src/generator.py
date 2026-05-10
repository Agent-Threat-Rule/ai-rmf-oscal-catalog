"""
AI RMF OSCAL Catalog generator (GOVERN function, v0.1).

Builds catalogs/ai-rmf-govern-v0.1.json conforming to OSCAL v1.2.2 catalog
schema. Control and category statements are taken verbatim from the AI RMF
Core (NIST AI 100-1) — see src/airmf_core_text.py. Implementation guidance
parts (about, suggested actions, documentation questions, references) come
from source/ai-rmf-playbook.json (NIST AI RMF Playbook structured export).

Why two sources: the Playbook JSON export contains minor textual deviations
from the Core canonical text (typos, dropped "and practices", and at least
one semantic divergence at GOVERN 5.2). The catalog statement must cite the
Core; the Playbook content fills in implementation guidance which is
Playbook-native.

Usage:
    python3 src/generator.py
"""

import json
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from airmf_core_text import GOVERN_CATEGORIES, GOVERN_SUBCATEGORIES

REPO = Path(__file__).resolve().parent.parent
SOURCE_PATH = REPO / "source" / "ai-rmf-playbook.json"
OUTPUT_PATH = REPO / "catalogs" / "ai-rmf-govern-v0.1.json"

NS = "https://github.com/Agent-Threat-Rule/ai-rmf-oscal-catalog/ns"
NAMESPACE_OID = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")  # url namespace per RFC 4122
ATR_OSCAL_NS = uuid.uuid5(NAMESPACE_OID, "https://github.com/Agent-Threat-Rule/ai-rmf-oscal-catalog")


def stable_uuid(seed: str) -> str:
    return str(uuid.uuid5(ATR_OSCAL_NS, seed))


def make_part(name: str, prose: str, ns: str | None = None) -> dict:
    part = {"name": name, "prose": prose.strip()}
    if ns is not None:
        part["ns"] = ns
    return part


def make_props(actors, topics) -> list:
    props = []
    for a in actors or []:
        props.append({"name": "ai-rmf-actor", "value": a, "ns": NS})
    for t in topics or []:
        props.append({"name": "ai-rmf-topic", "value": t, "ns": NS})
    return props


def split_subcat(title: str) -> tuple[str, str, str]:
    """Return (category_num, subcat_num, full_key). Title format: 'GOVERN 1.1'."""
    _, num = title.split(" ")
    cat_num, subcat_num = num.split(".")
    return cat_num, subcat_num, num


def make_control(item: dict) -> dict:
    cat_num, subcat_num, key = split_subcat(item["title"])
    control_id = f"ai-rmf-gv-{cat_num}.{subcat_num}"

    statement_text = GOVERN_SUBCATEGORIES.get(key)
    if not statement_text:
        raise ValueError(
            f"missing AI RMF Core text for GOVERN {key}; update src/airmf_core_text.py"
        )

    parts: list[dict] = [make_part("statement", statement_text)]

    # Implementation guidance parts come from Playbook. Custom (non-OSCAL-standard)
    # part names get our ns so consumers know they are local extensions.
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
    return control


def make_group(category_id: str, items: list) -> dict:
    cat_num = category_id.split("-")[1]
    group_id = f"ai-rmf-gv-{cat_num}"
    category_text = GOVERN_CATEGORIES.get(cat_num)
    if not category_text:
        raise ValueError(
            f"missing AI RMF Core text for GOVERN-{cat_num}; update src/airmf_core_text.py"
        )

    items_sorted = sorted(items, key=lambda i: int(i["title"].split(".")[1]))

    return {
        "id": group_id,
        "class": "ai-rmf-category",
        "title": f"GOVERN {cat_num}",
        "parts": [make_part("ai-rmf-category-statement", category_text, ns=NS)],
        "controls": [make_control(i) for i in items_sorted],
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
    govern = [x for x in playbook if x["type"].lower() == "govern"]

    by_cat: dict[str, list] = defaultdict(list)
    for item in govern:
        by_cat[item["category"]].append(item)

    groups = [
        make_group(cat, by_cat[cat])
        for cat in sorted(by_cat.keys(), key=lambda k: int(k.split("-")[1]))
    ]

    nist_party_uuid = stable_uuid("party:nist")

    catalog = {
        "uuid": stable_uuid("catalog:ai-rmf-govern-v0.1"),
        "metadata": {
            "title": "NIST AI Risk Management Framework: GOVERN function (community OSCAL catalog)",
            "last-modified": "PLACEHOLDER",
            "version": "0.1.0",
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
                "Community-contributed OSCAL catalog for the GOVERN function of "
                "NIST AI RMF 1.0. Statement and category text reproduced verbatim "
                "from the AI RMF Core (Section 5, Table 1). Implementation guidance "
                "parts (about, suggested actions, documentation questions, references) "
                "are reproduced from the AI RMF Playbook structured export. Released "
                "under CC0 1.0. Not endorsed by NIST. The NIST OSCAL Team is the "
                "authoritative source for any official AI RMF OSCAL artifact."
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
                        "references). The Playbook contains minor textual deviations "
                        "from the Core (typos, comma differences, and at least one "
                        "semantic divergence at GOVERN 5.2); the Playbook is therefore "
                        "not used as the source for Core control statements."
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

    groups = catalog["catalog"]["groups"]
    controls = sum(len(g["controls"]) for g in groups)
    print(f"wrote {OUTPUT_PATH}")
    print(f"  groups:         {len(groups)}")
    print(f"  controls:       {controls}")
    print(f"  last-modified:  {catalog['catalog']['metadata']['last-modified']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
