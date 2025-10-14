#!/usr/bin/env python3
"""RJW-IDD Evidence Harvester.

Pulls recent practitioner evidence from Hacker News, Reddit, GitHub Issues/PRs, and Stack Overflow.
Outputs normalized evidence entries that satisfy the RJW-IDD evidence schema.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from typing import Any

USER_AGENT = "RJW-IDD-EvidenceHarvester/1.0 (+https://example.invalid/rjw-idd)"
DEFAULT_RECENCY_DAYS = 28

PLATFORM_CHOICES = {"hn", "reddit", "github", "so"}
STANCE_CHOICES = {"pain", "fix", "aha", "win", "risk", "contra"}


def http_get(url: str, headers: dict[str, str] | None = None, retries: int = 2, backoff: float = 1.5) -> Any:
    request = urllib.request.Request(url, headers=headers or {"User-Agent": USER_AGENT})
    attempt = 0
    while True:
        try:
            with urllib.request.urlopen(request, timeout=30) as resp:
                data = resp.read()
                ctype = resp.headers.get("Content-Type", "")
                if "application/json" in ctype or url.endswith(".json"):
                    return json.loads(data.decode("utf-8"))
                return data.decode("utf-8")
        except Exception as exc:  # pragma: no cover - network layer
            attempt += 1
            if attempt > retries:
                raise RuntimeError(f"HTTP GET failed for {url}: {exc}") from exc
            time.sleep(backoff ** attempt)


def clamp_words(text: str, max_words: int = 50) -> str:
    words = text.strip().split()
    if len(words) <= max_words:
        return " ".join(words)
    return " ".join(words[:max_words]) + "…"


def plain_text(value: str) -> str:
    cleaned = re.sub(r"<[^>]+>", " ", html.unescape(value))
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return clamp_words(cleaned)


def iso_date(ts: float) -> str:
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc).strftime("%Y-%m-%d")


def within_recency(target_date: dt.datetime, cutoff: dt.datetime) -> bool:
    return target_date >= cutoff


def parse_date(value: str) -> dt.datetime:
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(dt.timezone.utc).replace(tzinfo=None)
    except Exception:
        return dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)


@dataclass
class EvidenceTask:
    source: str
    query: str
    tags: list[str]
    stance: str
    relevance_note: str
    limit: int = 5
    subreddit: str | None = None
    reddit_time_filter: str = "month"
    github_repo: str | None = None
    github_type: str = "issues"
    so_tagged: str | None = None
    hn_tags: str = "comment"

    @staticmethod
    def from_dict(data: dict[str, Any]) -> EvidenceTask:
        missing = {k for k in ("source", "query", "tags", "stance", "relevance_note") if k not in data}
        if missing:
            raise ValueError(f"Task missing keys: {missing}")
        stance = data["stance"].lower()
        if stance not in STANCE_CHOICES:
            raise ValueError(f"Invalid stance '{stance}' in task for query {data['query']}")
        tags = data["tags"]
        if not isinstance(tags, list) or not all(isinstance(t, str) for t in tags):
            raise ValueError("tags must be a list of strings")
        return EvidenceTask(
            source=data["source"].lower(),
            query=data["query"],
            tags=tags,
            stance=stance,
            relevance_note=data["relevance_note"],
            limit=int(data.get("limit", 5)),
            subreddit=data.get("subreddit"),
            reddit_time_filter=data.get("reddit_time_filter", "month"),
            github_repo=data.get("github_repo"),
            github_type=data.get("github_type", "issues"),
            so_tagged=data.get("so_tagged"),
            hn_tags=data.get("hn_tags", "comment"),
        )


@dataclass
class EvidenceRecord:
    evid_id: str
    uri: str
    author_or_handle: str
    platform: str
    date: str
    minimal_quote: str
    tags: list[str]
    stance: str
    relevance_note: str
    quality_flags: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def fetch_hn(task: EvidenceTask, cutoff: dt.datetime) -> Iterable[EvidenceRecord]:
    params = {
        "query": task.query,
        "tags": task.hn_tags,
        "hitsPerPage": task.limit,
        "numericFilters": f"created_at_i>{int(cutoff.timestamp())}",
    }
    url = "https://hn.algolia.com/api/v1/search_by_date?" + urllib.parse.urlencode(params)
    payload = http_get(url)
    for hit in payload.get("hits", []):
        created_at = parse_date(hit.get("created_at", ""))
        if created_at < cutoff:
            continue
        text = hit.get("comment_text") or hit.get("story_text") or hit.get("title", "")
        quote = plain_text(text)
        if not quote:
            continue
        link = hit.get("url") or hit.get("story_url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
        yield EvidenceRecord(
            evid_id="",
            uri=link,
            author_or_handle=hit.get("author", "unknown"),
            platform="hn",
            date=created_at.strftime("%Y-%m-%d"),
            minimal_quote=quote,
            tags=task.tags,
            stance=task.stance,
            relevance_note=task.relevance_note,
            quality_flags=["first-hand", "recency<=4w"],
        )


def fetch_reddit(task: EvidenceTask, cutoff: dt.datetime) -> Iterable[EvidenceRecord]:
    params = {
        "q": task.query,
        "restrict_sr": "1" if task.subreddit else "0",
        "sort": "new",
        "limit": str(task.limit * 3),
        "t": task.reddit_time_filter,
    }
    base = "https://www.reddit.com"
    path = f"/r/{task.subreddit}/search.json" if task.subreddit else "/search.json"
    url = base + path + "?" + urllib.parse.urlencode(params)
    payload = http_get(url, headers={"User-Agent": USER_AGENT})
    for child in payload.get("data", {}).get("children", []):
        data = child.get("data", {})
        created = dt.datetime.fromtimestamp(data.get("created_utc", time.time()))
        if created < cutoff:
            continue
        text = data.get("selftext") or data.get("body") or data.get("title", "")
        quote = plain_text(text)
        if not quote:
            continue
        permalink = data.get("permalink")
        uri = urllib.parse.urljoin(base, permalink) if permalink else data.get("url", base)
        flags = ["recency<=4w"]
        if bool(data.get("is_self", True)):
            flags.append("first-hand")
        yield EvidenceRecord(
            evid_id="",
            uri=uri,
            author_or_handle=data.get("author", "unknown"),
            platform="reddit",
            date=created.strftime("%Y-%m-%d"),
            minimal_quote=quote,
            tags=task.tags,
            stance=task.stance,
            relevance_note=task.relevance_note,
            quality_flags=flags,
        )


def fetch_github(task: EvidenceTask, cutoff: dt.datetime) -> Iterable[EvidenceRecord]:
    created_filter = cutoff.strftime("%Y-%m-%d")
    query = f"{task.query} created:>={created_filter}"
    if task.github_repo:
        query += f" repo:{task.github_repo}"
    params = {
        "q": query,
        "sort": "created",
        "order": "desc",
        "per_page": str(task.limit),
    }
    url = "https://api.github.com/search/issues?" + urllib.parse.urlencode(params)
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/vnd.github+json",
    }
    payload = http_get(url, headers=headers)
    for item in payload.get("items", []):
        created_at = parse_date(item.get("created_at", ""))
        if created_at < cutoff:
            continue
        body = item.get("body") or item.get("title", "")
        quote = plain_text(body)
        if not quote:
            continue
        uri = item.get("html_url")
        flags = ["first-hand", "recency<=4w"] if "experience" in body.lower() else ["recency<=4w"]
        yield EvidenceRecord(
            evid_id="",
            uri=uri,
            author_or_handle=item.get("user", {}).get("login", "unknown"),
            platform="github",
            date=created_at.strftime("%Y-%m-%d"),
            minimal_quote=quote,
            tags=task.tags,
            stance=task.stance,
            relevance_note=task.relevance_note,
            quality_flags=flags,
        )


def fetch_so(task: EvidenceTask, cutoff: dt.datetime) -> Iterable[EvidenceRecord]:
    params = {
        "order": "desc",
        "sort": "creation",
        "q": task.query,
        "site": "stackoverflow",
        "pagesize": str(task.limit),
        "filter": "withbody",
    }
    if task.so_tagged:
        params["tagged"] = task.so_tagged
    url = "https://api.stackexchange.com/2.3/search/advanced?" + urllib.parse.urlencode(params)
    payload = http_get(url)
    for item in payload.get("items", []):
        creation = dt.datetime.fromtimestamp(item.get("creation_date", time.time()))
        if creation < cutoff:
            continue
        body = item.get("body", "") or item.get("title", "")
        quote = plain_text(body)
        if not quote:
            continue
        uri = item.get("link")
        flags = ["recency<=4w"]
        if item.get("is_answered"):
            flags.append("replicable")
        yield EvidenceRecord(
            evid_id="",
            uri=uri,
            author_or_handle=item.get("owner", {}).get("display_name", "unknown"),
            platform="so",
            date=creation.strftime("%Y-%m-%d"),
            minimal_quote=quote,
            tags=task.tags,
            stance=task.stance,
            relevance_note=task.relevance_note,
            quality_flags=flags,
        )


FETCHERS = {
    "hn": fetch_hn,
    "reddit": fetch_reddit,
    "github": fetch_github,
    "so": fetch_so,
}


def load_tasks(path: str) -> list[EvidenceTask]:
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    tasks = [EvidenceTask.from_dict(item) for item in data.get("tasks", [])]
    invalid_sources = {t.source for t in tasks if t.source not in PLATFORM_CHOICES}
    if invalid_sources:
        raise ValueError(f"Unsupported sources in config: {sorted(invalid_sources)}")
    return tasks


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Harvest recency-bound evidence for RJW-IDD.")
    parser.add_argument("--config", required=True, help="Path to evidence task configuration JSON.")
    parser.add_argument("--output", required=True, help="Where to write the JSON evidence index.")
    parser.add_argument("--start-id", type=int, default=1, help="Starting numeric suffix for EVD IDs.")
    parser.add_argument("--recency-days", type=int, default=DEFAULT_RECENCY_DAYS)
    parser.add_argument("--max-records", type=int, default=500, help="Upper bound to prevent runaway collection.")
    args = parser.parse_args(argv)

    tasks = load_tasks(args.config)
    now_utc = dt.datetime.now(dt.timezone.utc)
    cutoff = (now_utc - dt.timedelta(days=args.recency_days)).replace(tzinfo=None)

    records: list[EvidenceRecord] = []
    counter = args.start_id

    for task in tasks:
        fetcher = FETCHERS[task.source]
        for record in fetcher(task, cutoff):
            if counter > 9999:
                raise ValueError("EVD counter exceeded 4 digits")
            if len(records) >= args.max_records:
                break
            record.evid_id = f"EVD-{counter:04d}"
            records.append(record)
            counter += 1
        if len(records) >= args.max_records:
            break

    # Deduplicate by URI to avoid repeats across overlapping tasks.
    deduped: dict[str, EvidenceRecord] = {}
    for record in records:
        deduped[record.uri] = record

    sorted_records = sorted(deduped.values(), key=lambda r: r.evid_id)

    output_payload = {
        "generated_at": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "recency_cutoff": cutoff.strftime("%Y-%m-%d"),
        "total_records": len(sorted_records),
        "records": [rec.to_dict() for rec in sorted_records],
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(output_payload, fh, indent=2, ensure_ascii=False)

    print(f"Wrote {len(sorted_records)} evidence records to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
