"""
Completeness check for the GOVERN function v0.1 catalog.

Asserts that:
- All 19 expected GOVERN subcategory IDs are present, in the expected groups
- Each control has the required parts (statement, guidance, suggested-actions, documentation-questions, references)
- Each group has an ai-rmf-category-statement part with prose
- Each control's statement matches the canonical AI RMF Core text from src/airmf_core_text.py
- No duplicate IDs

Usage:
    python3 src/completeness_check.py
"""

import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
from airmf_core_text import GOVERN_CATEGORIES, GOVERN_SUBCATEGORIES  # noqa: E402

CATALOG_PATH = REPO / "catalogs" / "ai-rmf-govern-v0.1.json"

EXPECTED_BY_GROUP = {
    "ai-rmf-gv-1": ["ai-rmf-gv-1.1", "ai-rmf-gv-1.2", "ai-rmf-gv-1.3", "ai-rmf-gv-1.4",
                    "ai-rmf-gv-1.5", "ai-rmf-gv-1.6", "ai-rmf-gv-1.7"],
    "ai-rmf-gv-2": ["ai-rmf-gv-2.1", "ai-rmf-gv-2.2", "ai-rmf-gv-2.3"],
    "ai-rmf-gv-3": ["ai-rmf-gv-3.1", "ai-rmf-gv-3.2"],
    "ai-rmf-gv-4": ["ai-rmf-gv-4.1", "ai-rmf-gv-4.2", "ai-rmf-gv-4.3"],
    "ai-rmf-gv-5": ["ai-rmf-gv-5.1", "ai-rmf-gv-5.2"],
    "ai-rmf-gv-6": ["ai-rmf-gv-6.1", "ai-rmf-gv-6.2"],
}

EXPECTED_TOTAL = sum(len(v) for v in EXPECTED_BY_GROUP.values())

REQUIRED_CONTROL_PART_NAMES = {"statement"}  # Always required.
EXPECTED_CONTROL_PART_NAMES = {
    "statement", "guidance", "ai-rmf-suggested-actions",
    "ai-rmf-documentation-questions", "ai-rmf-references",
}


def control_id_to_subcat_key(cid: str) -> str:
    return cid.removeprefix("ai-rmf-gv-")


def group_id_to_cat_key(gid: str) -> str:
    return gid.removeprefix("ai-rmf-gv-")


def main() -> int:
    with CATALOG_PATH.open() as f:
        doc = json.load(f)

    catalog = doc.get("catalog", {})
    groups = catalog.get("groups", [])
    failures: list[str] = []

    actual_by_group = {g.get("id"): [c.get("id") for c in g.get("controls", [])] for g in groups}
    all_ids = [cid for ids in actual_by_group.values() for cid in ids]

    # 1. Group + control ID coverage.
    if missing := set(EXPECTED_BY_GROUP) - set(actual_by_group):
        failures.append(f"missing groups: {sorted(missing)}")
    if extra := set(actual_by_group) - set(EXPECTED_BY_GROUP):
        failures.append(f"unexpected groups: {sorted(extra)}")

    for gid, expected_ids in EXPECTED_BY_GROUP.items():
        actual_ids = actual_by_group.get(gid, [])
        if missing_in_group := set(expected_ids) - set(actual_ids):
            failures.append(f"group {gid} missing: {sorted(missing_in_group)}")
        if extra_in_group := set(actual_ids) - set(expected_ids):
            failures.append(f"group {gid} unexpected: {sorted(extra_in_group)}")

    if duplicates := [cid for cid, c in Counter(all_ids).items() if c > 1]:
        failures.append(f"duplicate control IDs: {sorted(duplicates)}")

    # 2. Per-group: ai-rmf-category-statement part with verbatim Core text.
    for g in groups:
        gid = g.get("id")
        cat_key = group_id_to_cat_key(gid)
        expected_text = GOVERN_CATEGORIES.get(cat_key)
        cat_parts = [p for p in g.get("parts", []) if p.get("name") == "ai-rmf-category-statement"]
        if not cat_parts:
            failures.append(f"group {gid}: no ai-rmf-category-statement part")
            continue
        actual_text = (cat_parts[0].get("prose") or "").strip()
        if expected_text and actual_text != expected_text:
            failures.append(
                f"group {gid}: ai-rmf-category-statement drift from Core "
                f"(first 80 chars: actual {actual_text[:80]!r} vs expected {expected_text[:80]!r})"
            )

    # 3. Per-control: required and expected parts; statement matches Core verbatim.
    for g in groups:
        for c in g.get("controls", []):
            cid = c.get("id")
            parts_by_name = {p.get("name"): p for p in c.get("parts", [])}

            for required in REQUIRED_CONTROL_PART_NAMES:
                if required not in parts_by_name:
                    failures.append(f"{cid}: missing required part {required!r}")

            for expected in EXPECTED_CONTROL_PART_NAMES - REQUIRED_CONTROL_PART_NAMES:
                if expected not in parts_by_name:
                    failures.append(f"{cid}: missing expected part {expected!r}")

            statement = parts_by_name.get("statement")
            if statement is not None:
                actual = (statement.get("prose") or "").strip()
                key = control_id_to_subcat_key(cid)
                expected = GOVERN_SUBCATEGORIES.get(key)
                if not actual:
                    failures.append(f"{cid}: empty statement prose")
                elif expected and actual != expected:
                    failures.append(
                        f"{cid}: statement drift from Core "
                        f"(first 80 chars: actual {actual[:80]!r} vs expected {expected[:80]!r})"
                    )

    # 4. Custom parts that should carry the project ns.
    expected_ns = "https://github.com/Agent-Threat-Rule/ai-rmf-oscal-catalog/ns"
    custom_part_names = {"ai-rmf-category-statement", "ai-rmf-suggested-actions",
                         "ai-rmf-documentation-questions", "ai-rmf-references"}
    for g in groups:
        for source in [g] + g.get("controls", []):
            for p in source.get("parts", []):
                if p.get("name") in custom_part_names and p.get("ns") != expected_ns:
                    failures.append(
                        f"{source.get('id')}: custom part {p.get('name')!r} missing or wrong ns "
                        f"(got {p.get('ns')!r})"
                    )

    if failures:
        print(f"FAIL completeness: {len(failures)} issue(s)")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"OK completeness: {EXPECTED_TOTAL} GOVERN controls, all parts present, all statements match Core verbatim")
    return 0


if __name__ == "__main__":
    sys.exit(main())
