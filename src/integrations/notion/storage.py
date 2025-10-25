"""Persistence helpers for GitHub ↔ Notion ID mappings."""
from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional


LOGGER = logging.getLogger(__name__)


@dataclass
class MappingRecord:
    """Represents a stored mapping between GitHub artifacts and Notion pages."""

    github_id: str
    notion_page_id: str
    metadata: Optional[Dict[str, str]] = None


class NotionMappingStorage:
    """File-based storage for GitHub ↔ Notion mappings."""

    def __init__(self, storage_path: str = "build/notion_mappings.json") -> None:
        self._path = Path(storage_path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._cache: Dict[str, Dict[str, str]] = {}
        self._loaded = False

    def _load(self) -> None:
        if self._loaded:
            return
        if self._path.exists():
            try:
                with self._path.open("r", encoding="utf-8") as handle:
                    self._cache = json.load(handle)
            except json.JSONDecodeError as err:
                LOGGER.warning("Failed to decode Notion mapping file %s: %s", self._path, err)
                backup_path = self._path.with_suffix(".bak")
                os.replace(self._path, backup_path)
                LOGGER.warning("Corrupt mapping file moved to %s", backup_path)
                self._cache = {}
        self._loaded = True

    def _save(self) -> None:
        with self._path.open("w", encoding="utf-8") as handle:
            json.dump(self._cache, handle, indent=2, sort_keys=True)

    def get(self, key: str) -> Optional[str]:
        self._load()
        mapping = self._cache.get(key)
        if mapping:
            return mapping.get("notion_page_id")
        return None

    def set(self, key: str, notion_page_id: str, *, metadata: Optional[Dict[str, str]] = None) -> MappingRecord:
        self._load()
        record = {
            "notion_page_id": notion_page_id,
            "metadata": metadata or {},
        }
        self._cache[key] = record
        self._save()
        return MappingRecord(github_id=key, notion_page_id=notion_page_id, metadata=record["metadata"])

    def delete(self, key: str) -> None:
        self._load()
        if key in self._cache:
            del self._cache[key]
            self._save()

    def as_dict(self) -> Dict[str, Dict[str, str]]:
        self._load()
        return dict(self._cache)
