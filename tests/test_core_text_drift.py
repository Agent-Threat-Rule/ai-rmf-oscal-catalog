"""
CI guard against silent NIST drift.

Re-fetches the AI RMF Core HTML rendering at airc.nist.gov and diffs the
GOVERN category and subcategory statements against the constants embedded
in src/airmf_core_text.py. Fails (exit 1) if any text differs.

This is a network-dependent test and is intended to run on CI on a schedule
or before each release, not on every PR. It catches the case where NIST
silently updates Core wording and our embedded constants go stale.

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
from airmf_core_text import GOVERN_CATEGORIES, GOVERN_SUBCATEGORIES  # noqa: E402

CORE_URL = "https://airc.nist.gov/airmf-resources/airmf/5-sec-core/"


def fetch_text(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "ai-rmf-oscal-catalog/0.1"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8")


def html_to_text(html: str) -> str:
    no_scripts = re.sub(r"<script.*?</script>", "", html, flags=re.DOTALL)
    no_tags = re.sub(r"<[^>]+>", " ", no_scripts)
    return re.sub(r"\s+", " ", html_lib.unescape(no_tags)).strip()


def parse_govern_table(text: str) -> tuple[dict[str, str], dict[str, str]]:
    """Extract GOVERN category and subcategory statements from Table 1.

    Source format inside the table: tokens like 'Govern N : <text>' for
    categories and 'Govern N.M : <text>' for subcategories. Categories are
    distinguished from subcategories by absence of a dot in the label.
    """
    start = text.find("Table 1: Categories and subcategories for the GOVERN function")
    end = text.find("Table 2:")
    if start < 0:
        raise RuntimeError("Could not locate AI RMF Core Table 1 in fetched HTML")
    chunk = text[start:end] if end > start else text[start:start + 6000]

    pattern = r"Govern\s+(\d+(?:\.\d+)?)\s*:\s*(.*?)(?=\s*Govern\s+\d+(?:\.\d+)?\s*:|$)"
    categories: dict[str, str] = {}
    subcats: dict[str, str] = {}
    for label, body in re.findall(pattern, chunk, re.DOTALL):
        body_clean = re.sub(r"\s+", " ", body).strip()
        body_clean = re.sub(r"\s*\d\.\d+\s+(Map|Measure|Manage)\s+The\s+\w+\s+function.*$", "", body_clean).strip()
        if "." in label:
            subcats[label] = body_clean
        else:
            categories[label] = body_clean
    return categories, subcats


def diff_dict(label: str, expected: dict[str, str], actual: dict[str, str]) -> list[str]:
    issues: list[str] = []
    for key in sorted(set(expected) | set(actual), key=lambda k: tuple(int(p) for p in k.split("."))):
        e = expected.get(key)
        a = actual.get(key)
        if e is None:
            issues.append(f"{label} {key}: present upstream but not in airmf_core_text.py")
        elif a is None:
            issues.append(f"{label} {key}: present in airmf_core_text.py but not in upstream HTML")
        elif e != a:
            issues.append(f"{label} {key}: drift")
            issues.append(f"  embedded:  {e[:120]}")
            issues.append(f"  upstream:  {a[:120]}")
    return issues


def main() -> int:
    try:
        html = fetch_text(CORE_URL)
    except Exception as exc:
        print(f"SKIP network fetch failed: {exc}")
        return 0

    text = html_to_text(html)
    upstream_categories, upstream_subcats = parse_govern_table(text)

    issues: list[str] = []
    issues += diff_dict("GOVERN", GOVERN_CATEGORIES, upstream_categories)
    issues += diff_dict("GOVERN", GOVERN_SUBCATEGORIES, upstream_subcats)

    if issues:
        print(f"FAIL drift detected: {sum(1 for i in issues if not i.startswith('  '))} issues")
        for line in issues:
            print(f"  {line}")
        return 1

    print(
        f"OK no drift: {len(GOVERN_CATEGORIES)} categories, "
        f"{len(GOVERN_SUBCATEGORIES)} subcategories match upstream AIRC Core"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
