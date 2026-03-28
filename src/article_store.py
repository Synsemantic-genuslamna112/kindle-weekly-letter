"""Daily article accumulator — stores articles per topic across the week."""

import json
from datetime import datetime
from pathlib import Path

from .config import OUTPUT_DIR, TOPICS

WEEKLY_DIR = OUTPUT_DIR / "weekly"
SENT_HISTORY_PATH = OUTPUT_DIR / "sent_history.json"


def ensure_weekly_dir():
    WEEKLY_DIR.mkdir(parents=True, exist_ok=True)


def get_store_path(topic_id: str) -> Path:
    return WEEKLY_DIR / f"{topic_id}.json"


def load_articles(topic_id: str) -> list[dict]:
    """Load accumulated articles for a topic."""
    path = get_store_path(topic_id)
    if path.exists():
        return json.loads(path.read_text())
    return []


def save_articles(topic_id: str, articles: list[dict]):
    """Save articles for a topic."""
    ensure_weekly_dir()
    path = get_store_path(topic_id)
    path.write_text(json.dumps(articles, indent=2, ensure_ascii=False))


def load_sent_history() -> set[str]:
    """Load URLs of all previously sent articles."""
    if SENT_HISTORY_PATH.exists():
        data = json.loads(SENT_HISTORY_PATH.read_text())
        return set(data.get("sent_urls", []))
    return set()


def save_to_sent_history(articles: list[dict]):
    """Append article URLs to sent history after EPUB delivery."""
    sent = load_sent_history()
    for article in articles:
        sent.add(article["url"])
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SENT_HISTORY_PATH.write_text(json.dumps(
        {"sent_urls": sorted(sent)},
        indent=2,
        ensure_ascii=False,
    ))


def add_articles(topic_id: str, new_articles: list[dict]) -> int:
    """Add new articles, deduplicate by URL and sent history. Returns total count."""
    existing = load_articles(topic_id)
    existing_urls = {a["url"] for a in existing}
    sent_urls = load_sent_history()
    skipped = 0
    for article in new_articles:
        if article["url"] in existing_urls:
            continue
        if article["url"] in sent_urls:
            skipped += 1
            continue
        article["collected_date"] = datetime.now().strftime("%Y-%m-%d")
        existing.append(article)
        existing_urls.add(article["url"])
    if skipped:
        print(f"  Skipped {skipped} already-sent article(s)")
    save_articles(topic_id, existing)
    return len(existing)


def get_article_count(topic_id: str) -> int:
    return len(load_articles(topic_id))


def get_all_counts() -> dict[str, int]:
    """Return {topic_id: article_count} for all topics."""
    return {t["id"]: get_article_count(t["id"]) for t in TOPICS}


def clear_weekly():
    """Clear all accumulated articles (call after Sunday EPUB generation)."""
    if WEEKLY_DIR.exists():
        for f in WEEKLY_DIR.glob("*.json"):
            f.unlink()


def get_status_summary() -> str:
    """Human-readable status of article collection."""
    counts = get_all_counts()
    lines = []
    for t in TOPICS:
        count = counts[t["id"]]
        status = "READY" if count >= 10 else f"{count}/10"
        lines.append(f"  {t['name']}: {status}")
    return "\n".join(lines)
