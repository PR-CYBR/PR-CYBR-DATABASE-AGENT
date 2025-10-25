"""Synchronise GitHub webhook payloads with Notion databases."""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from dataclasses import dataclass
from typing import Any, Callable, Dict

from integrations.notion import (
    NotionClient,
    NotionMappingStorage,
    map_issue_payload_to_properties,
    map_project_item_payload_to_properties,
    map_pull_request_payload_to_properties,
)


LOGGER = logging.getLogger(__name__)


@dataclass
class HandlerResult:
    success: bool
    critical: bool
    message: str


def _load_payload(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _build_client() -> NotionClient:
    token = os.getenv("NOTION_TOKEN")
    if not token:
        raise RuntimeError("NOTION_TOKEN environment variable must be set")
    return NotionClient(token=token, max_retries=4, backoff_factor=1.5, logger=LOGGER)


def handle_issue_event(notion_client: NotionClient, payload: Dict[str, Any], storage: NotionMappingStorage) -> HandlerResult:
    database_id = os.getenv("NOTION_ISSUE_DATABASE_ID")
    if not database_id:
        return HandlerResult(False, True, "NOTION_ISSUE_DATABASE_ID environment variable is missing")

    issue = payload.get("issue")
    if not issue:
        return HandlerResult(False, True, "Payload does not contain issue information")

    properties = map_issue_payload_to_properties(payload)
    mapping_key = f"issue:{issue.get('id')}"
    existing_page_id = storage.get(mapping_key)

    try:
        page_id = notion_client.upsert_page(database_id, properties, page_id=existing_page_id)
    except Exception as err:  # pylint: disable=broad-except
        LOGGER.error("Failed to sync issue %s with Notion: %s", issue.get("id"), err, exc_info=True)
        return HandlerResult(False, True, f"Failed to sync issue: {err}")

    storage.set(
        mapping_key,
        page_id,
        metadata={
            "repository": payload.get("repository", {}).get("full_name", ""),
            "number": str(issue.get("number")),
        },
    )
    LOGGER.info("Issue #%s synced to Notion page %s", issue.get("number"), page_id)
    return HandlerResult(True, False, "Issue synchronised successfully")


def handle_pr_event(notion_client: NotionClient, payload: Dict[str, Any], storage: NotionMappingStorage) -> HandlerResult:
    database_id = os.getenv("NOTION_PR_DATABASE_ID")
    if not database_id:
        return HandlerResult(False, True, "NOTION_PR_DATABASE_ID environment variable is missing")

    pull_request = payload.get("pull_request")
    if not pull_request:
        return HandlerResult(False, True, "Payload does not contain pull_request information")

    properties = map_pull_request_payload_to_properties(payload)
    mapping_key = f"pull_request:{pull_request.get('id')}"
    existing_page_id = storage.get(mapping_key)

    try:
        page_id = notion_client.upsert_page(database_id, properties, page_id=existing_page_id)
    except Exception as err:  # pylint: disable=broad-except
        LOGGER.error("Failed to sync pull request %s with Notion: %s", pull_request.get("id"), err, exc_info=True)
        return HandlerResult(False, True, f"Failed to sync pull request: {err}")

    storage.set(
        mapping_key,
        page_id,
        metadata={
            "repository": payload.get("repository", {}).get("full_name", ""),
            "number": str(pull_request.get("number")),
        },
    )
    LOGGER.info("Pull request #%s synced to Notion page %s", pull_request.get("number"), page_id)
    return HandlerResult(True, False, "Pull request synchronised successfully")


def handle_project_event(notion_client: NotionClient, payload: Dict[str, Any], storage: NotionMappingStorage) -> HandlerResult:
    database_id = os.getenv("NOTION_PROJECT_DATABASE_ID")
    if not database_id:
        return HandlerResult(False, False, "NOTION_PROJECT_DATABASE_ID is not configured; skipping project sync")

    project_item = payload.get("project_item") or payload.get("project_card")
    if not project_item:
        return HandlerResult(False, True, "Payload does not contain project item information")

    properties = map_project_item_payload_to_properties(payload)
    project_item_id = project_item.get("id") or payload.get("id")
    mapping_key = f"project_item:{project_item_id}"
    existing_page_id = storage.get(mapping_key)

    try:
        page_id = notion_client.upsert_page(database_id, properties, page_id=existing_page_id)
    except Exception as err:  # pylint: disable=broad-except
        LOGGER.error("Failed to sync project item %s with Notion: %s", project_item_id, err, exc_info=True)
        return HandlerResult(False, True, f"Failed to sync project item: {err}")

    storage.set(
        mapping_key,
        page_id,
        metadata={
            "project_id": str(payload.get("project_id") or project_item.get("project_id")),
            "content_type": project_item.get("type", ""),
        },
    )
    LOGGER.info("Project item %s synced to Notion page %s", project_item_id, page_id)
    return HandlerResult(True, False, "Project item synchronised successfully")


def main(argv: Any = None) -> int:
    parser = argparse.ArgumentParser(description="Sync GitHub events to Notion")
    parser.add_argument("--event-type", required=True, choices=["issues", "pull_request", "project"], help="GitHub event type")
    parser.add_argument("--payload-path", required=True, help="Path to the event payload JSON file")
    parser.add_argument("--log-level", default=os.getenv("LOG_LEVEL", "INFO"), help="Logging level")
    args = parser.parse_args(argv)

    logging.basicConfig(level=args.log_level.upper(), format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    try:
        payload = _load_payload(args.payload_path)
    except (OSError, json.JSONDecodeError) as err:
        LOGGER.error("Failed to load payload from %s: %s", args.payload_path, err)
        return 1

    try:
        notion_client = _build_client()
    except RuntimeError as err:
        LOGGER.error(str(err))
        return 1

    storage = NotionMappingStorage()

    handlers: Dict[str, Callable[[NotionClient, Dict[str, Any], NotionMappingStorage], HandlerResult]] = {
        "issues": handle_issue_event,
        "pull_request": handle_pr_event,
        "project": handle_project_event,
    }

    handler = handlers.get(args.event_type)
    if not handler:
        LOGGER.error("Unsupported event type: %s", args.event_type)
        return 1

    result = handler(notion_client, payload, storage)

    log_method = LOGGER.info if result.success else LOGGER.error if result.critical else LOGGER.warning
    log_method(result.message)

    if not result.success and result.critical:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
