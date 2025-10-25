"""Utilities to synchronize repository metadata with a Notion database."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

try:  # pragma: no cover - optional dependency for runtime
    from notion_client import Client as NotionClient
except ImportError:  # pragma: no cover - allow dry-run/test execution without dependency
    NotionClient = None  # type: ignore


LOGGER_NAME = "notion_sync"


class StructuredFormatter(logging.Formatter):
    """Render log records as JSON for easier ingestion."""

    def format(self, record: logging.LogRecord) -> str:  # noqa: D401 - inherited docstring
        payload: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        event = getattr(record, "event", None)
        if event:
            payload["event"] = event

        context = getattr(record, "context", None)
        if isinstance(context, dict):
            payload.update(context)

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, ensure_ascii=False)


@dataclass
class SyncResult:
    """Aggregate outcome of a Notion synchronization run."""

    created: int = 0
    updated: int = 0
    failed: int = 0

    @property
    def success(self) -> bool:
        return self.failed == 0


def setup_logger(level: str) -> logging.Logger:
    """Configure the module logger with structured output."""

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(level.upper())
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(StructuredFormatter())
        logger.addHandler(handler)

    return logger


def load_records(path: str) -> List[Dict[str, Any]]:
    """Load JSON records describing the pages to synchronize."""

    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if isinstance(payload, list):
        return payload

    if isinstance(payload, dict) and "records" in payload and isinstance(payload["records"], list):
        return payload["records"]

    raise ValueError("Records file must contain a JSON array or an object with a 'records' list")


def build_page_payload(record: Dict[str, Any]) -> Dict[str, Any]:
    """Transform a record into Notion page properties."""

    slug = record.get("slug")
    title = record.get("title")

    if not slug or not title:
        raise ValueError("Record requires both 'slug' and 'title' fields")

    properties: Dict[str, Any] = {
        "Name": {
            "title": [{"text": {"content": title}}],
        },
        "Slug": {
            "rich_text": [{"text": {"content": slug}}],
        },
    }

    status = record.get("status")
    if status:
        properties["Status"] = {"select": {"name": status}}

    url = record.get("url")
    if url:
        properties["URL"] = {"url": url}

    tags = record.get("tags")
    if isinstance(tags, Iterable) and not isinstance(tags, (str, bytes)):
        properties["Tags"] = {"multi_select": [{"name": str(tag)} for tag in tags]}

    children: List[Dict[str, Any]] = []
    description = record.get("description")
    if description:
        children.append(
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": str(description)},
                        }
                    ]
                },
            }
        )

    return {"properties": properties, "children": children}


def find_existing_page_id(
    client: Any, database_id: str, slug: str, logger: logging.Logger
) -> Optional[str]:
    """Search for an existing Notion page by slug property."""

    try:
        response = client.databases.query(
            **{
                "database_id": database_id,
                "filter": {
                    "property": "Slug",
                    "rich_text": {
                        "equals": slug,
                    },
                },
            }
        )
    except Exception:  # noqa: BLE001 - log and surface error to caller
        logger.exception(
            "Failed to query Notion database", extra={"event": "database_query_failed", "context": {"slug": slug}}
        )
        raise

    for result in response.get("results", []):
        result_id = result.get("id")
        if result_id:
            return result_id
    return None


def sync_record(
    client: Any,
    database_id: str,
    record: Dict[str, Any],
    dry_run: bool,
    logger: logging.Logger,
) -> str:
    """Create or update a Notion page for a single record."""

    slug = record.get("slug")
    payload = build_page_payload(record)

    page_id = record.get("notion_page_id")
    should_query = not page_id and not dry_run
    if not page_id and dry_run and hasattr(client, "databases"):
        should_query = True

    if should_query:
        page_id = find_existing_page_id(client, database_id, slug, logger)

    if dry_run:
        logger.info(
            "Dry-run processed record",
            extra={"event": "record_dry_run", "context": {"slug": slug, "page_id": page_id}},
        )
        return "updated" if page_id else "created"

    if page_id:
        logger.info(
            "Updating Notion page",
            extra={"event": "record_update", "context": {"slug": slug, "page_id": page_id}},
        )
        client.pages.update(page_id=page_id, properties=payload["properties"])
        return "updated"

    logger.info(
        "Creating Notion page",
        extra={"event": "record_create", "context": {"slug": slug}},
    )
    client.pages.create(parent={"database_id": database_id}, **payload)
    return "created"


def sync_records(
    client: Any,
    database_id: str,
    records: Iterable[Dict[str, Any]],
    dry_run: bool,
    logger: logging.Logger,
) -> SyncResult:
    """Synchronize all records with Notion, capturing failures per record."""

    result = SyncResult()

    for record in records:
        slug = record.get("slug", "<missing-slug>")
        try:
            outcome = sync_record(client, database_id, record, dry_run, logger)
        except Exception:  # noqa: BLE001 - per-record error handling with structured log
            result.failed += 1
            logger.exception(
                "Failed to synchronize record",
                extra={"event": "record_sync_failed", "context": {"slug": slug}},
            )
            continue

        if outcome == "created":
            result.created += 1
        elif outcome == "updated":
            result.updated += 1
        else:
            logger.warning(
                "Unknown sync outcome",
                extra={"event": "record_sync_unknown", "context": {"slug": slug, "outcome": outcome}},
            )

    return result


def ensure_client(token: Optional[str], dry_run: bool) -> Any:
    """Instantiate a Notion client when available."""

    if dry_run and not token:
        return object()  # sentinel to satisfy interface during dry-run tests

    if NotionClient is None:
        raise RuntimeError(
            "notion-client dependency is required for non-dry-run execution. Install it via 'pip install notion-client'."
        )

    if not token:
        raise RuntimeError("NOTION_TOKEN must be provided for Notion synchronization")

    return NotionClient(auth=token)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse CLI arguments for the sync script."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database-id", required=True, help="Target Notion database identifier")
    parser.add_argument("--records-file", required=True, help="Path to the JSON file describing records")
    parser.add_argument("--dry-run", action="store_true", help="Log actions without mutating Notion")
    parser.add_argument(
        "--log-level",
        default=os.environ.get("NOTION_SYNC_LOG_LEVEL", "INFO"),
        help="Python logging level to use for the run",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    """Run the Notion synchronization routine with CLI arguments."""

    args = parse_args(argv)
    logger = setup_logger(args.log_level)
    logger.info("Starting Notion synchronization", extra={"event": "sync_start"})

    try:
        records = load_records(args.records_file)
    except Exception:  # noqa: BLE001 - provide structured error logging
        logger.exception(
            "Unable to load records file",
            extra={"event": "records_load_failed", "context": {"records_file": args.records_file}},
        )
        return 1

    token = os.environ.get("NOTION_TOKEN")

    try:
        client = ensure_client(token, args.dry_run)
    except Exception:  # noqa: BLE001
        logger.exception("Unable to initialize Notion client", extra={"event": "client_init_failed"})
        return 1

    try:
        result = sync_records(client, args.database_id, records, args.dry_run, logger)
    except Exception:  # noqa: BLE001 - catch unexpected fatal error
        logger.exception("Unexpected synchronization failure", extra={"event": "sync_unhandled_exception"})
        return 1

    logger.info(
        "Synchronization summary",
        extra={
            "event": "sync_complete",
            "context": {"created": result.created, "updated": result.updated, "failed": result.failed},
        },
    )

    return 0 if result.success else 1


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    sys.exit(main())
