"""
Cross-reference extractor for AI RMF subcategories.

Scans both AI RMF Core statement text and AI RMF Playbook implementation
guidance fields for references to other functions/categories/subcategories
and emits OSCAL `links` entries connecting controls.

Reference patterns recognised:
- "the {govern|map|measure|manage} function" (any case) → link to the
  corresponding function group (href="#ai-rmf-{prefix}", rel="related").
- "{Govern|Map|Measure|Manage} N.M" → link to a specific subcategory
  control (href="#ai-rmf-{prefix}-N.M", rel="related").
- "{Govern|Map|Measure|Manage} N" (category-only, no decimal) → link to
  the category group (href="#ai-rmf-{prefix}-N", rel="related").

Self-references (control referring to its own ID or category or function)
are dropped.

Usage from generator: `extract_links(item, function_upper, control_id)`
returns a list of OSCAL link dicts.
"""

import re
from typing import Iterable

from airmf_core_text import ALL_CATEGORIES, ALL_SUBCATEGORIES

FUNCTION_PREFIXES = {
    "GOVERN": "gv",
    "MAP": "mp",
    "MEASURE": "ms",
    "MANAGE": "mg",
}

# "the map function" / "the Govern function" — any case, any of the 4 functions.
FUNCTION_PATTERN = re.compile(r"\bthe\s+(govern|map|measure|manage)\s+function\b", re.IGNORECASE)

# "Govern 1.5", "Map 2.1", "MEASURE 2.4" — case-insensitive on the function word.
SUBCATEGORY_PATTERN = re.compile(r"\b(Govern|Map|Measure|Manage)\s+(\d+\.\d+)\b", re.IGNORECASE)

# "Govern 1" without a decimal — must NOT match the subcategory pattern (avoid
# duplicate hits where "Govern 1" leads "Govern 1.5"). Use a negative lookahead.
CATEGORY_PATTERN = re.compile(r"\b(Govern|Map|Measure|Manage)\s+(\d+)(?!\.\d)\b", re.IGNORECASE)


def function_to_id(function_upper: str) -> str:
    return f"ai-rmf-{FUNCTION_PREFIXES[function_upper]}"


def category_to_id(function_upper: str, cat_num: str) -> str:
    return f"ai-rmf-{FUNCTION_PREFIXES[function_upper]}-{cat_num}"


def control_to_id(function_upper: str, subcat_key: str) -> str:
    return f"ai-rmf-{FUNCTION_PREFIXES[function_upper]}-{subcat_key}"


def find_references(text: str) -> set[str]:
    """Return the set of OSCAL fragment refs ('#ai-rmf-...') found in text.

    The set deduplicates within a single text block. Caller is responsible
    for further deduplication across multiple text fields per control.
    """
    refs: set[str] = set()
    if not text:
        return refs

    for m in FUNCTION_PATTERN.finditer(text):
        function_word = m.group(1).upper()
        refs.add(f"#{function_to_id(function_word)}")

    for m in SUBCATEGORY_PATTERN.finditer(text):
        function_word = m.group(1).upper()
        subcat_key = m.group(2)
        prefix = FUNCTION_PREFIXES[function_word]
        # Sanity check — only emit a link if the target subcategory exists.
        if subcat_key in ALL_SUBCATEGORIES.get(function_word, {}):
            refs.add(f"#ai-rmf-{prefix}-{subcat_key}")

    for m in CATEGORY_PATTERN.finditer(text):
        function_word = m.group(1).upper()
        cat_num = m.group(2)
        if cat_num in ALL_CATEGORIES.get(function_word, {}):
            refs.add(f"#{category_to_id(function_word, cat_num)}")

    return refs


def extract_links(playbook_item: dict, function_upper: str, control_id: str) -> list[dict]:
    """Extract OSCAL `links` for one control by scanning its Core statement
    and Playbook implementation-guidance fields.

    Self-references (to the control's own id, its own category, or its own
    function) are dropped.
    """
    self_function_id = function_to_id(function_upper)
    own_cat_num = control_id.split("-")[-1].split(".")[0]
    self_category_id = category_to_id(function_upper, own_cat_num)
    self_control_href = f"#{control_id}"

    self_hrefs = {self_control_href, f"#{self_function_id}", f"#{self_category_id}"}

    candidate_fields: list[str] = []
    # Statement comes from Core (we look it up via the title key)
    title_parts = playbook_item.get("title", "").split(" ", 1)
    if len(title_parts) == 2:
        subcat_key = title_parts[1]
        statement = ALL_SUBCATEGORIES.get(function_upper, {}).get(subcat_key)
        if statement:
            candidate_fields.append(statement)
    # Playbook fields
    for field in ("section_about", "section_actions", "section_doc", "section_ref"):
        v = playbook_item.get(field)
        if v:
            candidate_fields.append(v)

    refs: set[str] = set()
    for text in candidate_fields:
        refs |= find_references(text)

    refs -= self_hrefs

    return [{"href": href, "rel": "related"} for href in sorted(refs)]


__all__ = ["extract_links", "find_references", "function_to_id", "category_to_id", "control_to_id"]
