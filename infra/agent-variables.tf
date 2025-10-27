#############################################
# PR-CYBR Agent Variables (Terraform Cloud)
# Each variable is managed through Terraform
# Cloud and GitHub secrets to keep sensitive
# data out of the repository. All updates to
# naming must stay in sync across TFC and GH.
#############################################

# --- Core Platform Access ---
variable "AGENT_ACTIONS" {
  type        = string
  sensitive   = true
  description = "Token for CI/CD pipelines (builds, tests, deploys)"
}

variable "NOTION_TOKEN" {
  type        = string
  sensitive   = true
  description = "Integration token for Notion API access"
}

variable "NOTION_PAGE_ID" {
  type        = string
  description = "Primary Notion page identifier for the database agent"
}

variable "TFC_TOKEN" {
  type        = string
  sensitive   = true
  description = "Terraform Cloud API token for remote operations"
}

# --- Docker / Registry ---
variable "DOCKERHUB_USERNAME" {
  type        = string
  description = "Docker Hub username for publishing agent images"
}

variable "PR_CYBR_DOCKER_PASS" {
  type        = string
  sensitive   = true
  description = "Docker Hub password/token for publishing agent images"
}

# --- Global Infrastructure ---
variable "GLOBAL_DOMAIN" {
  type        = string
  description = "Root DNS domain for PR-CYBR services"
}
