"""
Completeness check for the v0.2 full catalog (all 4 AI RMF functions).

Asserts:
- Catalog has 4 top-level function groups (GOVERN, MAP, MEASURE, MANAGE),
  in that order, with the expected category groups nested inside each.
- All 72 expected subcategory IDs are present, in the expected groups.
- Each control has the required parts (statement, guidance, suggested-actions,
  documentation-questions, references) — guidance, doc-questions, and refs
  are technically optional in the source data but every Playbook entry has
  all four populated, so we treat them as expected.
- Each function group has the right title and class.
- Each category group has an ai-rmf-category-statement part with prose
  matching the canonical AI RMF Core text in src/airmf_core_text.py.
- Each control's statement matches the canonical AI RMF Core text.
- Custom parts carry the project ns.
- No duplicate control IDs.

Usage:
    python3 src/completeness_check.py
"""

import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
from airmf_core_text import (  # noqa: E402
    ALL_CATEGORIES, ALL_SUBCATEGORIES, FUNCTION_PREFIXES_FALLBACK,
)

CATALOG_PATH = REPO / "catalogs" / "ai-rmf-v0.3.json"
PROFILE_PATH = REPO / "profiles" / "ai-rmf-baseline-profile.json"

NS = "https://github.com/Agent-Threat-Rule/ai-rmf-oscal-catalog/ns"

EXPECTED_FUNCTION_ORDER = ["GOVERN", "MAP", "MEASURE", "MANAGE"]
FUNCTION_PREFIXES = {"GOVERN": "gv", "MAP": "mp", "MEASURE": "ms", "MANAGE": "mg"}

CUSTOM_PART_NAMES = {
    "ai-rmf-category-statement", "ai-rmf-suggested-actions",
    "ai-rmf-documentation-questions", "ai-rmf-references",
}

EXPECTED_CONTROL_PART_NAMES = {
    "statement",
    "guidance",
    "ai-rmf-suggested-actions",
    "ai-rmf-documentation-questions",
    "ai-rmf-references",
}


def control_id_for(function_upper: str, subcat_key: str) -> str:
    return f"ai-rmf-{FUNCTION_PREFIXES[function_upper]}-{subcat_key}"


def category_id_for(function_upper: str, cat_num: str) -> str:
    return f"ai-rmf-{FUNCTION_PREFIXES[function_upper]}-{cat_num}"


def function_id_for(function_upper: str) -> str:
    return f"ai-rmf-{FUNCTION_PREFIXES[function_upper]}"


def main() -> int:
    with CATALOG_PATH.open() as f:
        doc = json.load(f)

    catalog = doc.get("catalog", {})
    function_groups = catalog.get("groups", [])
    failures: list[str] = []

    actual_function_ids = [g.get("id") for g in function_groups]
    expected_function_ids = [function_id_for(fn) for fn in EXPECTED_FUNCTION_ORDER]
    if actual_function_ids != expected_function_ids:
        failures.append(
            f"function group ordering: expected {expected_function_ids}, got {actual_function_ids}"
        )

    all_control_ids: list[str] = []

    for function_upper in EXPECTED_FUNCTION_ORDER:
        function_id = function_id_for(function_upper)
        fg = next((g for g in function_groups if g.get("id") == function_id), None)
        if fg is None:
            failures.append(f"missing function group {function_id}")
            continue
        if fg.get("title") != function_upper:
            failures.append(f"{function_id}: expected title {function_upper!r}, got {fg.get('title')!r}")
        if fg.get("class") != "ai-rmf-function":
            failures.append(f"{function_id}: expected class 'ai-rmf-function', got {fg.get('class')!r}")

        expected_categories = ALL_CATEGORIES[function_upper]
        category_groups = fg.get("groups", [])
        actual_cat_ids = [cg.get("id") for cg in category_groups]
        expected_cat_ids = [category_id_for(function_upper, c) for c in sorted(expected_categories.keys(), key=int)]
        if actual_cat_ids != expected_cat_ids:
            failures.append(
                f"{function_id}: category ordering expected {expected_cat_ids}, got {actual_cat_ids}"
            )

        # Verify each category group: title, class, statement part, controls
        expected_subs = ALL_SUBCATEGORIES[function_upper]
        for cat_num, expected_cat_text in expected_categories.items():
            cat_id = category_id_for(function_upper, cat_num)
            cg = next((c for c in category_groups if c.get("id") == cat_id), None)
            if cg is None:
                failures.append(f"missing category group {cat_id}")
                continue
            if cg.get("title") != f"{function_upper} {cat_num}":
                failures.append(f"{cat_id}: expected title '{function_upper} {cat_num}', got {cg.get('title')!r}")
            if cg.get("class") != "ai-rmf-category":
                failures.append(f"{cat_id}: expected class 'ai-rmf-category', got {cg.get('class')!r}")

            # Category statement part
            cat_statement_parts = [p for p in cg.get("parts", []) if p.get("name") == "ai-rmf-category-statement"]
            if not cat_statement_parts:
                failures.append(f"{cat_id}: no ai-rmf-category-statement part")
            else:
                actual_text = (cat_statement_parts[0].get("prose") or "").strip()
                if actual_text != expected_cat_text:
                    failures.append(
                        f"{cat_id}: ai-rmf-category-statement drift from Core "
                        f"(actual {actual_text[:80]!r} vs expected {expected_cat_text[:80]!r})"
                    )
                if cat_statement_parts[0].get("ns") != NS:
                    failures.append(
                        f"{cat_id}: ai-rmf-category-statement missing or wrong ns "
                        f"(got {cat_statement_parts[0].get('ns')!r})"
                    )

            # Controls under this category
            controls = cg.get("controls", [])
            expected_in_cat = sorted(
                [k for k in expected_subs if k.startswith(f"{cat_num}.")],
                key=lambda s: int(s.split(".")[1]),
            )
            expected_ctrl_ids = [control_id_for(function_upper, k) for k in expected_in_cat]
            actual_ctrl_ids = [c.get("id") for c in controls]
            if actual_ctrl_ids != expected_ctrl_ids:
                failures.append(
                    f"{cat_id}: control ordering expected {expected_ctrl_ids}, got {actual_ctrl_ids}"
                )

            for c in controls:
                cid = c.get("id")
                all_control_ids.append(cid)
                parts_by_name = {p.get("name"): p for p in c.get("parts", [])}

                # Statement must match Core verbatim
                key = cid.removeprefix(f"ai-rmf-{FUNCTION_PREFIXES[function_upper]}-")
                expected_statement = expected_subs.get(key)
                stmt = parts_by_name.get("statement")
                if stmt is None:
                    failures.append(f"{cid}: missing required 'statement' part")
                elif expected_statement:
                    actual = (stmt.get("prose") or "").strip()
                    if not actual:
                        failures.append(f"{cid}: empty statement prose")
                    elif actual != expected_statement:
                        failures.append(
                            f"{cid}: statement drift from Core "
                            f"(actual {actual[:80]!r} vs expected {expected_statement[:80]!r})"
                        )

                # Expected supplementary parts
                for expected_part in EXPECTED_CONTROL_PART_NAMES - {"statement"}:
                    if expected_part not in parts_by_name:
                        failures.append(f"{cid}: missing expected part {expected_part!r}")

                # Custom parts must have ns
                for p in c.get("parts", []):
                    if p.get("name") in CUSTOM_PART_NAMES and p.get("ns") != NS:
                        failures.append(
                            f"{cid}: custom part {p.get('name')!r} has wrong or missing ns (got {p.get('ns')!r})"
                        )

    # Cross-cutting: no duplicate control IDs
    if duplicates := [cid for cid, c in Counter(all_control_ids).items() if c > 1]:
        failures.append(f"duplicate control IDs: {sorted(duplicates)}")

    expected_total = sum(len(subs) for subs in ALL_SUBCATEGORIES.values())
    if len(all_control_ids) != expected_total:
        failures.append(f"expected {expected_total} controls total, found {len(all_control_ids)}")

    # Cross-reference links: every href in a control's links[] must resolve
    # to a real ID in the catalog (function group, category group, or
    # control). Self-references must be absent.
    valid_ids: set[str] = set()
    for fg in function_groups:
        valid_ids.add(fg.get("id", ""))
        for cg in fg.get("groups", []):
            valid_ids.add(cg.get("id", ""))
            for c in cg.get("controls", []):
                valid_ids.add(c.get("id", ""))
    valid_ids.discard("")

    total_links = 0
    controls_with_links = 0
    for fg in function_groups:
        for cg in fg.get("groups", []):
            own_function_id = fg.get("id")
            own_category_id = cg.get("id")
            for c in cg.get("controls", []):
                cid = c.get("id")
                links = c.get("links") or []
                if links:
                    controls_with_links += 1
                for link in links:
                    href = link.get("href", "")
                    if not href.startswith("#"):
                        failures.append(
                            f"{cid}: link href {href!r} must start with '#' (internal fragment)"
                        )
                        continue
                    target_id = href[1:]
                    if target_id not in valid_ids:
                        failures.append(f"{cid}: link href {href!r} does not resolve to any ID in catalog")
                    if target_id in {cid, own_function_id, own_category_id}:
                        failures.append(f"{cid}: link href {href!r} is self-reference, should be removed")
                    if not link.get("rel"):
                        failures.append(f"{cid}: link missing 'rel' attribute")
                    total_links += 1

    # Profile completeness: must exist, must import the catalog by UUID,
    # the import UUID must match a back-matter resource UUID, and the
    # resource rlinks must include the expected catalog href.
    if not PROFILE_PATH.exists():
        failures.append(f"profile missing: {PROFILE_PATH}")
    else:
        with PROFILE_PATH.open() as f:
            profile_doc = json.load(f)
        profile = profile_doc.get("profile", {})

        imports = profile.get("imports", [])
        if len(imports) != 1:
            failures.append(f"profile expected 1 import, found {len(imports)}")

        import_href = imports[0].get("href", "") if imports else ""
        if not import_href.startswith("#"):
            failures.append(
                f"profile import href {import_href!r} should be a fragment ref to a back-matter resource"
            )

        if imports and "include-all" not in imports[0] and "include-controls" not in imports[0]:
            failures.append("profile import must declare include-all or include-controls")

        bm_resources = profile.get("back-matter", {}).get("resources", []) or []
        catalog_resource_uuid = import_href[1:] if import_href.startswith("#") else None
        catalog_resource = next((r for r in bm_resources if r.get("uuid") == catalog_resource_uuid), None)
        if catalog_resource is None:
            failures.append(
                f"profile back-matter resource {catalog_resource_uuid!r} not found "
                f"(import href does not resolve)"
            )
        else:
            rlinks = catalog_resource.get("rlinks") or []
            hrefs = [r.get("href", "") for r in rlinks]
            if not any(h.endswith("ai-rmf-v0.3.json") for h in hrefs):
                failures.append(
                    f"profile back-matter resource rlinks should include ai-rmf-v0.3.json target; "
                    f"got {hrefs!r}"
                )

    if failures:
        print(f"FAIL completeness: {len(failures)} issue(s)")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(
        f"OK completeness: {expected_total} controls across "
        f"{sum(len(c) for c in ALL_CATEGORIES.values())} categories in 4 functions; "
        f"{total_links} cross-ref links across {controls_with_links} controls all resolve; "
        f"baseline profile imports catalog cleanly; all statements match Core verbatim; "
        f"all custom parts have ns"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
