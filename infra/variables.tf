#############################################
# Terraform Variable Schema for PR-CYBR
# Agent workspaces leverage Terraform Cloud
# variables for all secrets and configuration.
# This file defines the authoritative schema.
#############################################

variable "AGENT_ID" {
  type        = string
  description = "Unique identifier for this PR-CYBR agent workspace."
  default     = ""
}

variable "PR_CYBR_DOCKER_USER" {
  type        = string
  description = "Shared DockerHub username for PR-CYBR agents."
  default     = ""
}

variable "PR_CYBR_DOCKER_PASS" {
  type        = string
  description = "Shared DockerHub password for PR-CYBR agents."
  sensitive   = true
  default     = ""
}

variable "DOCKERHUB_USERNAME" {
  type        = string
  description = "Agent DockerHub username (mirrors shared credential)."
  default     = ""
}

variable "DOCKERHUB_TOKEN" {
  type        = string
  description = "Agent DockerHub token (mirrors shared credential)."
  sensitive   = true
  default     = ""
}

variable "GLOBAL_DOMAIN" {
  type        = string
  description = "Global PR-CYBR domain used for shared services."
  default     = ""
}

variable "AGENT_ACTIONS" {
  type        = string
  description = "GitHub Actions automation token for Codex agents."
  sensitive   = true
  default     = ""
}

variable "NOTION_TOKEN" {
  type        = string
  description = "Shared Notion integration token for automation access."
  sensitive   = true
  default     = ""
}

variable "NOTION_DISCUSSIONS_ARC_DB_ID" {
  type        = string
  description = "Notion database ID for discussions archive."
  default     = ""
}

variable "NOTION_ISSUES_BACKLOG_DB_ID" {
  type        = string
  description = "Notion database ID for the issues backlog."
  default     = ""
}

variable "NOTION_KNOWLEDGE_FILE_DB_ID" {
  type        = string
  description = "Notion database ID for the knowledge file repository."
  default     = ""
}

variable "NOTION_PROJECT_BOARD_BACKLOG_DB_ID" {
  type        = string
  description = "Notion database ID for project board backlog."
  default     = ""
}

variable "NOTION_PR_BACKLOG_DB_ID" {
  type        = string
  description = "Notion database ID for pull request backlog."
  default     = ""
}

variable "NOTION_TASK_BACKLOG_DB_ID" {
  type        = string
  description = "Notion database ID for task backlog."
  default     = ""
}

variable "NOTION_PAGE_ID" {
  type        = string
  description = "Agent-specific Notion page identifier."
  default     = ""
}

variable "TFC_TOKEN" {
  type        = string
  description = "Terraform Cloud API token used for workspace automation."
  sensitive   = true
  default     = ""
}
