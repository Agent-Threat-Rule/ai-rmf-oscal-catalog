"""
CI guard against silent NIST drift.

Re-fetches the AI RMF Core HTML rendering at airc.nist.gov and diffs the
GOVERN, MAP, MEASURE, MANAGE category and subcategory statements against
the constants embedded in src/airmf_core_text.py. Fails (exit 1) if any
text differs.

This is a network-dependent test and is intended to run on a CI schedule
(weekly is fine) or before each release, not on every PR. It catches the
case where NIST silently updates Core wording and our embedded constants
go stale.

Usage:
    python3 tests/test_core_text_drift.py

Network access is required.
"""

import html as html_lib
import re
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
from airmf_core_text import ALL_CATEGORIES, ALL_SUBCATEGORIES  # noqa: E402

CORE_URL = "https://airc.nist.gov/airmf-resources/airmf/5-sec-core/"

TABLES = [
    (1, "GOVERN", "Table 2:"),
    (2, "MAP", "Table 3:"),
    (3, "MEASURE", "Table 4:"),
    (4, "MANAGE", None),  # last table — bound by site footer
]


def fetch_text(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "ai-rmf-oscal-catalog/0.2"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8")


def html_to_text(html: str) -> str:
    no_scripts = re.sub(r"<script.*?</script>", "", html, flags=re.DOTALL)
    no_tags = re.sub(r"<[^>]+>", " ", no_scripts)
    return re.sub(r"\s+", " ", html_lib.unescape(no_tags)).strip()


def trim_footer(text: str) -> str:
    footer_markers = [
        r"\s+HEADQUARTERS\s+\d+\s+Bureau\s+Drive",
        r"\s+(?:HHS|Vulnerability\s+Disclosure|No\s+Fear\s+Act\s+Policy)",
    ]
    cut = len(text)
    for pat in footer_markers:
        m = re.search(pat, text)
        if m and m.start() < cut:
            cut = m.start()
    return text[:cut]


def parse_function_table(text: str, table_num: int, function_name: str, end_marker: str | None) -> tuple[dict, dict]:
    """Extract one function's category and subcategory statements from its table."""
    start = text.find(f"Table {table_num}: Categories and subcategories for the {function_name} function")
    if start < 0:
        raise RuntimeError(f"Could not locate AI RMF Core Table {table_num} ({function_name}) in fetched HTML")
    if end_marker:
        end = text.find(end_marker, start)
        chunk = text[start:end] if end > start else text[start:]
    else:
        chunk = text[start:]

    function_word = function_name.capitalize()
    pattern = rf"{function_word}\s+(\d+(?:\.\d+)?)\s*:\s*(.*?)(?=\s*{function_word}\s+\d+(?:\.\d+)?\s*:|$)"

    cats: dict[str, str] = {}
    subs: dict[str, str] = {}
    for label, body in re.findall(pattern, chunk, re.DOTALL):
        body_clean = re.sub(r"\s+", " ", body).strip()
        body_clean = re.sub(r"\s*Table\s+\d+:.*$", "", body_clean).strip()
        body_clean = re.sub(r"\s+\d+\.\d+\s+(Govern|Map|Measure|Manage)\s+The\s+\w+\s+function.*$", "", body_clean).strip()
        body_clean = re.sub(r"\s+\d+\.\d+\s+(Govern|Map|Measure|Manage)\s*$", "", body_clean).strip()
        if "." in label:
            subs[label] = body_clean
        else:
            cats[label] = body_clean.rstrip()
            # Add trailing period if missing (Core sometimes drops it before next subcat marker)
            if cats[label] and not cats[label].rstrip().endswith((".", "?", "!")):
                cats[label] = cats[label].rstrip() + "."
    return cats, subs


def diff_dict(label: str, expected: dict[str, str], actual: dict[str, str]) -> list[str]:
    issues: list[str] = []
    keys = sorted(set(expected) | set(actual), key=lambda k: tuple(int(p) for p in k.split(".")) if "." in k else (int(k),))
    for key in keys:
        e = expected.get(key)
        a = actual.get(key)
        if e is None:
            issues.append(f"{label} {key}: present upstream but not in airmf_core_text.py")
        elif a is None:
            issues.append(f"{label} {key}: present in airmf_core_text.py but not in upstream HTML")
        elif e != a:
            issues.append(f"{label} {key}: drift")
            issues.append(f"  embedded:  {e[:140]}")
            issues.append(f"  upstream:  {a[:140]}")
    return issues


def main() -> int:
    try:
        html = fetch_text(CORE_URL)
    except Exception as exc:
        print(f"SKIP network fetch failed: {exc}")
        return 0

    text = trim_footer(html_to_text(html))

    issues: list[str] = []
    for table_num, function_name, end_marker in TABLES:
        try:
            upstream_categories, upstream_subcats = parse_function_table(text, table_num, function_name, end_marker)
        except RuntimeError as exc:
            issues.append(f"{function_name}: extraction error: {exc}")
            continue
        issues += diff_dict(function_name, ALL_CATEGORIES[function_name], upstream_categories)
        issues += diff_dict(function_name, ALL_SUBCATEGORIES[function_name], upstream_subcats)

    if issues:
        # Don't double-count the indented detail lines when summarising
        primary = sum(1 for line in issues if not line.startswith("  "))
        print(f"FAIL drift detected: {primary} issues")
        for line in issues:
            print(f"  {line}")
        return 1

    total_cat = sum(len(c) for c in ALL_CATEGORIES.values())
    total_sub = sum(len(s) for s in ALL_SUBCATEGORIES.values())
    print(
        f"OK no drift: {total_cat} categories, {total_sub} subcategories "
        f"across 4 functions match upstream AIRC Core"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
