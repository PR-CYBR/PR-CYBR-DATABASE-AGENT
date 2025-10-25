import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict

import pytest

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.notion_sync import (
    SyncResult,
    build_page_payload,
    load_records,
    sync_record,
    sync_records,
)


@pytest.fixture
def sample_record() -> Dict[str, Any]:
    return {
        "slug": "database-agent",
        "title": "Database Agent",
        "status": "Active",
        "url": "https://example.com/agents/database",
        "tags": ["python", "automation"],
        "description": "Synchronizes metadata with Notion.",
    }


class MockDatabases:
    def __init__(self, response: Dict[str, Any]):
        self.response = response
        self.calls = []

    def query(self, **kwargs: Any) -> Dict[str, Any]:
        self.calls.append(kwargs)
        return self.response


class MockPages:
    def __init__(self):
        self.created = []
        self.updated = []

    def create(self, **kwargs: Any) -> None:
        self.created.append(kwargs)

    def update(self, **kwargs: Any) -> None:
        self.updated.append(kwargs)


class MockClient:
    def __init__(self, database_response: Dict[str, Any]):
        self.databases = MockDatabases(database_response)
        self.pages = MockPages()


def test_build_page_payload_maps_core_fields(sample_record: Dict[str, Any]) -> None:
    payload = build_page_payload(sample_record)
    properties = payload["properties"]

    assert properties["Name"]["title"][0]["text"]["content"] == sample_record["title"]
    assert properties["Slug"]["rich_text"][0]["text"]["content"] == sample_record["slug"]
    assert properties["Status"]["select"]["name"] == sample_record["status"]
    assert properties["URL"]["url"] == sample_record["url"]
    assert {tag["name"] for tag in properties["Tags"]["multi_select"]} == {"python", "automation"}

    children = payload["children"]
    assert len(children) == 1
    assert children[0]["paragraph"]["rich_text"][0]["text"]["content"] == sample_record["description"]


def test_sync_record_creates_page_when_absent(sample_record: Dict[str, Any]) -> None:
    client = MockClient({"results": []})
    result = sync_record(client, "db", sample_record, dry_run=False, logger=logging.getLogger("test"))

    assert result == "created"
    assert len(client.pages.created) == 1
    created_payload = client.pages.created[0]
    assert created_payload["parent"]["database_id"] == "db"
    assert created_payload["properties"]["Name"]["title"][0]["text"]["content"] == sample_record["title"]


def test_sync_record_updates_page_when_existing(sample_record: Dict[str, Any]) -> None:
    client = MockClient({"results": [{"id": "page-123"}]})
    result = sync_record(client, "db", sample_record, dry_run=False, logger=logging.getLogger("test"))

    assert result == "updated"
    assert len(client.pages.updated) == 1
    update_payload = client.pages.updated[0]
    assert update_payload["page_id"] == "page-123"
    assert update_payload["properties"]["Slug"]["rich_text"][0]["text"]["content"] == sample_record["slug"]


def test_sync_records_handles_errors_and_returns_failures(sample_record: Dict[str, Any]) -> None:
    failing_client = MockClient({"results": []})

    def boom(**_: Any) -> None:
        raise RuntimeError("API failure")

    failing_client.pages.create = boom  # type: ignore[assignment]

    logger = logging.getLogger("test")
    result = sync_records(failing_client, "db", [sample_record], dry_run=False, logger=logger)

    assert isinstance(result, SyncResult)
    assert result.failed == 1
    assert result.created == 0
    assert result.updated == 0


def test_load_records_supports_wrapped_payload(tmp_path: Path) -> None:
    data = {"records": [{"slug": "abc", "title": "Example"}]}
    records_path = tmp_path / "records.json"
    records_path.write_text(json.dumps(data), encoding="utf-8")

    records = load_records(str(records_path))
    assert records == data["records"]


def test_load_records_rejects_invalid_structure(tmp_path: Path) -> None:
    records_path = tmp_path / "records.json"
    records_path.write_text(json.dumps({"slug": "missing-list"}), encoding="utf-8")

    with pytest.raises(ValueError):
        load_records(str(records_path))
