"""Translate GitHub webhook payloads into Notion property dictionaries."""
from __future__ import annotations

import datetime as _dt
from typing import Any, Dict

ISO_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def _rich_text(content: str) -> Dict[str, Any]:
    return {
        "rich_text": [
            {
                "type": "text",
                "text": {"content": content[:2000]},
            }
        ]
    }


def _title(content: str) -> Dict[str, Any]:
    return {
        "title": [
            {
                "type": "text",
                "text": {"content": content[:2000]},
            }
        ]
    }


def _status(name: str) -> Dict[str, Any]:
    return {"status": {"name": name}}


def _date(timestamp: str) -> Dict[str, Any]:
    try:
        _dt.datetime.strptime(timestamp, ISO_FORMAT)
        return {"date": {"start": timestamp}}
    except (ValueError, TypeError):
        return {"date": None}


def map_issue_payload_to_properties(payload: Dict[str, Any]) -> Dict[str, Any]:
    issue = payload.get("issue", {})
    repository = payload.get("repository", {})
    user = issue.get("user", {})
    assignee = issue.get("assignee") or {}

    return {
        "Title": _title(issue.get("title", "GitHub Issue")),
        "URL": {
            "url": issue.get("html_url"),
        },
        "Repository": _rich_text(repository.get("full_name", "")),
        "Number": {
            "number": issue.get("number"),
        },
        "State": _status(issue.get("state", "open").title()),
        "Author": _rich_text(user.get("login", "unknown")),
        "Assignee": _rich_text(assignee.get("login", "Unassigned")),
        "Created": _date(issue.get("created_at")),
        "Updated": _date(issue.get("updated_at")),
    }


def map_pull_request_payload_to_properties(payload: Dict[str, Any]) -> Dict[str, Any]:
    pull_request = payload.get("pull_request", {})
    repository = payload.get("repository", {})
    user = pull_request.get("user", {})
    merged_by = pull_request.get("merged_by") or {}

    status = "Open"
    if pull_request.get("merged"):
        status = "Merged"
    elif pull_request.get("state") == "closed":
        status = "Closed"

    return {
        "Title": _title(pull_request.get("title", "Pull Request")),
        "URL": {"url": pull_request.get("html_url")},
        "Repository": _rich_text(repository.get("full_name", "")),
        "Number": {"number": pull_request.get("number")},
        "State": _status(status),
        "Author": _rich_text(user.get("login", "unknown")),
        "Merged By": _rich_text(merged_by.get("login", "")),
        "Created": _date(pull_request.get("created_at")),
        "Updated": _date(pull_request.get("updated_at")),
        "Merged": _date(pull_request.get("merged_at")),
    }


def map_project_item_payload_to_properties(payload: Dict[str, Any]) -> Dict[str, Any]:
    project_item = payload.get("project_item", payload.get("project_card", {}))
    repository = payload.get("repository", {})
    content = project_item.get("content", {})
    owner = payload.get("sender", {})

    target_title = content.get("title") or content.get("name") or "Project Item"
    target_url = content.get("html_url") or content.get("url")

    return {
        "Title": _title(target_title),
        "URL": {"url": target_url},
        "Repository": _rich_text(repository.get("full_name", "")),
        "Project ID": _rich_text(str(payload.get("project_id") or project_item.get("project_id", ""))),
        "Item ID": _rich_text(str(project_item.get("id", payload.get("id", "")))),
        "Owner": _rich_text(owner.get("login", "")),
        "Updated": _date(project_item.get("updated_at") or payload.get("created_at")),
    }
