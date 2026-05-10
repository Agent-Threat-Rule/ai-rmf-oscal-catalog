"""
Topic-graph cross-reference extractor for AI RMF subcategories.

Extends the regex-based extractor (cross_references.py) with a deterministic,
authoritative-source-driven second pass that uses the AI RMF Playbook's own
`Topic` taxonomy (46 distinct topics covering all 72 subcategories) as the
basis for emitting `links` between topically-related controls.

Why this approach over LLM augmentation:
- Deterministic: same inputs always produce same outputs. No hallucination.
- Authoritative: uses NIST's own Playbook topic tags, not derived semantics.
- Reproducible: any consumer can verify by re-running against playbook.json.
- Defensible: every emitted link cites the topics that justify it.

Eligibility rule:
A topic-derived link from A to B is emitted if any of:
1. A and B share 3+ topics, OR
2. A and B share 2+ topics AND at least one shared topic appears in <=5 controls
   ("rare"; signals strong topical alignment), OR
3. A and B share 1+ topic AND at least one shared topic appears in <=3 controls
   ("ultra-rare"; signals near-unique topical specialty).

For each control, top-K (K=4) most-related targets are emitted, sorted by
count of shared topics (primary) and inverse-frequency-weighted score
(tiebreak). Self-references and same-control sibling-only signals are
dropped. Each emitted link carries a `text` field describing the basis.

Usage from generator: `topic_links_for_control(control_id)` returns a list of
OSCAL link dicts compatible with the existing extractor.
"""

import json
from collections import defaultdict
from pathlib import Path
from typing import Iterable

REPO = Path(__file__).resolve().parent.parent
PLAYBOOK_PATH = REPO / "source" / "ai-rmf-playbook.json"

FUNCTION_PREFIXES = {
    "GOVERN": "gv",
    "MAP": "mp",
    "MEASURE": "ms",
    "MANAGE": "mg",
}

# Tunable thresholds (kept conservative to limit graph noise)
RARE_TOPIC_FREQ_THRESHOLD = 5
ULTRA_RARE_TOPIC_FREQ_THRESHOLD = 3
TOP_K_PER_CONTROL = 4


def _control_id_for(item: dict) -> str:
    function_word, num = item["title"].split(" ", 1)
    function_upper = function_word.upper()
    return f"ai-rmf-{FUNCTION_PREFIXES[function_upper]}-{num}"


def _load_playbook() -> dict:
    """Returns dict: control_id -> {topics: set, function: str, ...}."""
    with PLAYBOOK_PATH.open() as f:
        items = json.load(f)
    out: dict[str, dict] = {}
    for item in items:
        cid = _control_id_for(item)
        out[cid] = {
            "topics": set(item.get("Topic") or []),
            "function": item["type"].upper(),
            "title": item["title"],
        }
    return out


def _topic_frequency(by_id: dict) -> dict[str, int]:
    freq: dict[str, int] = defaultdict(int)
    for record in by_id.values():
        for t in record["topics"]:
            freq[t] += 1
    return freq


def _eligible(shared: set[str], topic_freq: dict[str, int]) -> bool:
    if not shared:
        return False
    n = len(shared)
    if n >= 3:
        return True
    any_rare = any(topic_freq[t] <= RARE_TOPIC_FREQ_THRESHOLD for t in shared)
    if n >= 2 and any_rare:
        return True
    any_ultra = any(topic_freq[t] <= ULTRA_RARE_TOPIC_FREQ_THRESHOLD for t in shared)
    if any_ultra:
        return True
    return False


def _score(shared: set[str], topic_freq: dict[str, int]) -> float:
    """Primary signal: count of shared topics. Tiebreak: inverse-frequency sum."""
    return float(len(shared)) + sum(1.0 / topic_freq[t] for t in shared)


def compute_all_topic_links() -> dict[str, list[dict]]:
    """Compute topic-derived links for every control.

    Returns dict: control_id -> list of OSCAL link dicts.

    Each link dict:
        {
          "href": "#ai-rmf-...",
          "rel": "related",
          "text": "Topically related: shares <topic-list>"
        }
    """
    by_id = _load_playbook()
    topic_freq = _topic_frequency(by_id)

    out: dict[str, list[dict]] = {}
    for src_id, src in by_id.items():
        src_topics = src["topics"]
        if not src_topics:
            continue
        candidates = []
        for tgt_id, tgt in by_id.items():
            if tgt_id == src_id:
                continue
            tgt_topics = tgt["topics"]
            if not tgt_topics:
                continue
            shared = src_topics & tgt_topics
            if not _eligible(shared, topic_freq):
                continue
            score = _score(shared, topic_freq)
            candidates.append((score, tgt_id, frozenset(shared)))
        candidates.sort(key=lambda x: (-x[0], x[1]))
        candidates = candidates[:TOP_K_PER_CONTROL]

        if not candidates:
            continue

        links = []
        for score, tgt_id, shared in candidates:
            links.append({
                "href": f"#{tgt_id}",
                "rel": "related",
                "text": "Topically related: shares " + ", ".join(sorted(shared)),
            })
        out[src_id] = links
    return out


def merge_with_existing(existing_links: list[dict] | None, topic_links: list[dict]) -> list[dict]:
    """Merge regex-derived and topic-derived links, deduplicating by href.

    If a link is present in both lists, the regex-derived entry wins (it has
    no text field, signalling 'directly cross-referenced in source text' which
    is a stronger relationship than topical similarity).
    """
    existing = list(existing_links or [])
    seen = {link["href"] for link in existing}
    for tl in topic_links:
        if tl["href"] not in seen:
            existing.append(tl)
            seen.add(tl["href"])
    # Sort by href for stable ordering (catalog regenerations are byte-stable)
    existing.sort(key=lambda link: link["href"])
    return existing


def main() -> int:
    """CLI: print topic-graph statistics for inspection."""
    by_id = _load_playbook()
    topic_freq = _topic_frequency(by_id)
    all_links = compute_all_topic_links()
    total_edges = sum(len(v) for v in all_links.values())
    coverage = len(all_links)
    no_links_ids = sorted(set(by_id) - set(all_links))

    print("Topic-graph cross-reference extractor:")
    print(f"  controls in catalog:        {len(by_id)}")
    print(f"  controls with topic links:  {coverage}")
    print(f"  total directed edges:       {total_edges}")
    print(f"  avg edges per linked ctrl:  {total_edges / max(coverage, 1):.2f}")
    print(f"  max outdegree:              {max((len(v) for v in all_links.values()), default=0)}")
    print(f"  controls without topic links ({len(no_links_ids)}):")
    for cid in no_links_ids:
        topics = sorted(by_id[cid]["topics"])
        print(f"    {cid}  topics={topics}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
