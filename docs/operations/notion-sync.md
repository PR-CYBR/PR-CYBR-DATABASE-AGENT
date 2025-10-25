# Notion Synchronization Operations

This document explains how to run the Notion synchronization workflow, dry-run changes, and verify updates before promoting them through the CI pipeline. The implementation mirrors the patterns used across the PR-CYBR ecosystem per the [spec-bootstrap](https://github.com/PR-CYBR/spec-bootstrap/) guidelines.

## Prerequisites

- Python 3.11+
- Dependencies installed via `pip install -r requirements.txt`
- Access to the Notion integration token stored as the `NOTION_TOKEN` secret in Terraform Cloud workspace environment variables.
- Target Notion database identifier.

## Running the Script Locally

```bash
python scripts/notion_sync.py \
  --database-id "<your-notion-db-id>" \
  --records-file config/notion-records.json \
  --dry-run
```

- `--dry-run` logs intended changes without mutating Notion. Omit the flag for a full update **after** validating the dry run and only when a Notion token is available in the environment.
- Structured logs are emitted as JSON to ease ingestion in log aggregation pipelines.
- The script exits with `0` when all records succeed, or `1` if any stage fails (records loading, client initialization, or per-record sync).

## GitHub Actions Dry Runs

Use the `workflow_dispatch` trigger on the **Notion Sync** workflow to run in GitHub Actions:

1. Navigate to **Actions → Notion Sync** in GitHub.
2. Select **Run workflow** and supply:
   - `database_id` (required)
   - Optional `records_file` path if your payload differs from the default `config/notion-records.json`.
   - Leave `dry_run` as `true` for validation runs.
   - Provide a `notion_token` only when you intend to write changes. Otherwise the workflow falls back to repository or organization secrets.
3. Each run uploads the structured logs to the job summary, and the script returns a non-zero exit code if any record fails.

### Triggering via GitHub CLI

```bash
gh workflow run notion-sync.yml \
  --ref feature/notion-sync \
  -f database_id="<your-notion-db-id>" \
  -f dry_run=true \
  -f records_file="config/notion-records.json"
```

To provide an alternate records payload without committing it, create an artifact and upload it before triggering the workflow:

```bash
echo '{"records": [... your payload ...]}' > build/payload.json
# Upload artifact to the most recent run (adjust run-id as needed)
gh run upload-artifact --run-id <run-id> --name notion-records --path build/payload.json
# Reference the artifact path in the workflow dispatch input
gh workflow run notion-sync.yml \
  --ref feature/notion-sync \
  -f database_id="<your-notion-db-id>" \
  -f dry_run=true \
  -f records_file="build/payload.json"
```

## Testing

Run the integration-focused unit tests before raising a PR:

```bash
pytest tests/integrations/notion
```

## Branching and CI Requirements

All changes must originate from a feature branch (for example, `feature/notion-sync`) and pass the automated CI checks before merging. This keeps the workflow aligned with the spec-bootstrap release cadence and leverages the Terraform Cloud-managed secrets for production runs.
