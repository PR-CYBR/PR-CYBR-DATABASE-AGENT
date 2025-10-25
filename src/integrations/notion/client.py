"""Notion API client wrapper with retry logic and logging."""
from __future__ import annotations

import logging
import time
from typing import Any, Callable, Dict, Optional

from notion_client import Client
from notion_client.errors import APIResponseError, RequestTimeoutError


class NotionClient:
    """Simple wrapper around the official Notion client with retries."""

    def __init__(
        self,
        token: str,
        *,
        max_retries: int = 3,
        backoff_factor: float = 1.0,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self._client = Client(auth=token)
        self._max_retries = max(1, max_retries)
        self._backoff_factor = max(0.1, backoff_factor)
        self._logger = logger or logging.getLogger(__name__)

    @property
    def api(self) -> Client:
        """Expose the underlying Notion client for advanced interactions."""

        return self._client

    def _execute(self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        delay = self._backoff_factor
        attempt = 0
        last_error: Optional[Exception] = None

        while attempt < self._max_retries:
            attempt += 1
            try:
                self._logger.debug("Calling Notion API %s (attempt %d)", fn.__name__, attempt)
                return fn(*args, **kwargs)
            except (APIResponseError, RequestTimeoutError) as err:
                last_error = err
                status = getattr(err, "status", "unknown")
                self._logger.warning(
                    "Notion API call %s failed with status %s on attempt %d/%d: %s",
                    fn.__name__,
                    status,
                    attempt,
                    self._max_retries,
                    err,
                )
                if attempt >= self._max_retries:
                    break
                time.sleep(delay)
                delay *= 2
            except Exception as err:  # pylint: disable=broad-except
                last_error = err
                self._logger.error("Unexpected error while calling Notion API: %s", err, exc_info=True)
                break

        if last_error:
            raise last_error
        raise RuntimeError("Notion API request failed without an explicit error")

    def upsert_page(
        self,
        database_id: str,
        properties: Dict[str, Any],
        *,
        page_id: Optional[str] = None,
        icon: Optional[Dict[str, Any]] = None,
        cover: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Create or update a Notion page and return the resulting page ID."""

        if page_id:
            self._logger.info("Updating Notion page %s in database %s", page_id, database_id)
            response = self._execute(
                self._client.pages.update,
                page_id,
                properties=properties,
                icon=icon,
                cover=cover,
            )
        else:
            self._logger.info("Creating Notion page in database %s", database_id)
            response = self._execute(
                self._client.pages.create,
                parent={"database_id": database_id},
                properties=properties,
                icon=icon,
                cover=cover,
            )

        page_id = response.get("id")
        if not page_id:
            raise ValueError("Notion API response did not include a page ID")
        return page_id

    def retrieve_page(self, page_id: str) -> Dict[str, Any]:
        """Retrieve a single Notion page."""

        self._logger.debug("Retrieving Notion page %s", page_id)
        return self._execute(self._client.pages.retrieve, page_id)

    def query_database(self, database_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Proxy to query a Notion database with retry logic."""

        self._logger.debug("Querying Notion database %s", database_id)
        return self._execute(self._client.databases.query, database_id, **kwargs)
