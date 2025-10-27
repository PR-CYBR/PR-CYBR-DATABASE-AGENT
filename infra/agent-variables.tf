############################################################
# PR-CYBR Agent Variable Aggregation
# This file groups Terraform Cloud provided variables into
# logical structures that downstream modules or automation
# scripts can consume. All values are sourced from the
# variables defined in variables.tf and populated via TFC.
############################################################

locals {
  agent_identity = {
    id             = var.AGENT_ID
    notion_page_id = var.NOTION_PAGE_ID
  }

  docker_registry = {
    username    = var.PR_CYBR_DOCKER_USER
    password    = var.PR_CYBR_DOCKER_PASS
    user_alias  = var.DOCKERHUB_USERNAME
    token       = var.DOCKERHUB_TOKEN
    global_host = var.GLOBAL_DOMAIN
  }

  github_actions = {
    automation_token = var.AGENT_ACTIONS
    tfc_token        = var.TFC_TOKEN
  }

  notion = {
    token                      = var.NOTION_TOKEN
    discussions_database_id    = var.NOTION_DISCUSSIONS_ARC_DB_ID
    issues_database_id         = var.NOTION_ISSUES_BACKLOG_DB_ID
    knowledge_file_database_id = var.NOTION_KNOWLEDGE_FILE_DB_ID
    project_board_backlog_id   = var.NOTION_PROJECT_BOARD_BACKLOG_DB_ID
    pull_request_backlog_id    = var.NOTION_PR_BACKLOG_DB_ID
    task_backlog_id            = var.NOTION_TASK_BACKLOG_DB_ID
    primary_page_id            = var.NOTION_PAGE_ID
  }
}

output "agent_identity" {
  description = "Core identity fields for the active PR-CYBR agent."
  value       = local.agent_identity
}

output "docker_registry" {
  description = "Shared Docker registry credentials used by all agents."
  value       = local.docker_registry
  sensitive   = true
}

output "github_actions" {
  description = "Tokens leveraged by GitHub Actions automation workflows."
  value       = local.github_actions
  sensitive   = true
}

output "notion" {
  description = "Notion automation identifiers consumed by shared tooling."
  value       = local.notion
  sensitive   = true
}
