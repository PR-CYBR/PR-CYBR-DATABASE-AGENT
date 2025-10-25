# Notion Sync Operations Guide

This document explains how the Notion sync automation is configured for the PR-CYBR database agent project. It covers the GitHub secrets required by the workflow, the Terraform Cloud (TFC) workspace variables that must mirror those secrets, and the steps needed to grant the Notion integration access to the relevant database.

## Required GitHub Secrets

Create the following repository or organization secrets so the workflow can authenticate with Notion and locate the database resources it needs to synchronize:

| Secret name | Purpose |
|-------------|---------|
| `NOTION_TOKEN` | Internal integration token generated from Notion. Used to authenticate API calls. |
| `NOTION_DATABASE_ID` | Identifier of the database (32-character UUID without dashes) that the sync process updates. |
| `NOTION_PARENT_PAGE_ID` | Identifier of the parent page that stores the database or other related content used during the sync. |

> **Note:** Store these values as encrypted GitHub secrets. Never commit them to the repository.

## Terraform Cloud Workspace Variables

Our automation mirrors the GitHub secrets inside Terraform Cloud workspace environment variables. Configure the workspace associated with this repository with the following sensitive environment variables:

| Variable name | Value |
|---------------|-------|
| `NOTION_TOKEN` | Same value as the GitHub secret `NOTION_TOKEN`. Mark as *sensitive*. |
| `NOTION_DATABASE_ID` | Same value as the GitHub secret `NOTION_DATABASE_ID`. Mark as *sensitive*. |
| `NOTION_PARENT_PAGE_ID` | Same value as the GitHub secret `NOTION_PARENT_PAGE_ID`. Mark as *sensitive*. |

Adding these variables to the workspace ensures both Terraform and downstream GitHub Actions can access them when triggered via the Terraform Cloud run tasks.

## Granting the Notion Integration Access

1. Navigate to [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations) and create a new internal integration (or open the existing integration used by this project).
2. Copy the *Internal Integration Token* and store it in the `NOTION_TOKEN` secret/variable locations listed above.
3. Open the target workspace and locate the database page that should be synchronized.
4. Share the database with the integration:
   - Click the **Share** button in the top-right corner of the page.
   - Select **Invite** and search for the integration name you created.
   - Grant the integration at least **Can edit** permissions so it can update database entries.
5. Record the database URL and extract the 32-character identifier (the part after the last `/` in the URL) for use as `NOTION_DATABASE_ID`.
6. If the workflow requires a parent page ID, open the parent page, copy its URL, and extract the final 32-character identifier to populate `NOTION_PARENT_PAGE_ID`.

Once the integration is shared and the variables are configured, the GitHub Action defined in `.github/workflows/notion-sync.yml` can authenticate with Notion and perform the synchronization safely.
