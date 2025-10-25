# Notion Sync Operations

## Bi-Directional Sync Architecture

The bi-directional integration relies on a scheduled GitHub Actions workflow that runs at regular intervals (for example, every 10 minutes) and calls the Notion REST API to poll for changes. When GitHub is the source of truth (issue or pull request updates), the same workflow pushes updates back to Notion by invoking the Notion API with the relevant page identifiers. Optionally, a lightweight webhook receiver (hosted behind the repository’s automation infrastructure) can accept outbound notifications from Notion and enqueue follow-up GitHub API calls, allowing near real-time synchronization while keeping the polling workflow as a fallback.

## Identifier Storage Strategy

To maintain referential integrity between systems, each record keeps the other system’s identifier in a dedicated field:

- **Notion**: a database property named `GitHub ID` stores the corresponding GitHub issue or pull request number.
- **GitHub**: the matching issue (or pull request) keeps a persistent comment that records the Notion page ID. Alternatively, the Notion identifier can be stored in issue metadata using labels or the issue body, but a dedicated automation comment is preferred so that humans can easily locate and audit the linkage.

## Actions Triggered by Notion Updates

- **New Notion task**: when a new page is created in the tracked Notion database and lacks a `GitHub ID`, the automation creates a GitHub issue that mirrors the task details, then writes the GitHub issue number back into the Notion `GitHub ID` property.
- **Status changes**: when a tracked page’s status is set to `Done`, the workflow closes the linked GitHub issue (or merges the linked pull request, if applicable) and leaves a comment summarizing the change to preserve auditability.

## Required Permissions

- **GitHub**: the GitHub Actions workflow requires a token with `repo` scope (read/write on issues, pull requests, and comments) to create, update, and close issues as well as post synchronization logs.
- **Notion**: the integration must be granted read and update permissions on the relevant Notion database so it can query pages, create new pages, and modify properties such as `GitHub ID` or status fields.

