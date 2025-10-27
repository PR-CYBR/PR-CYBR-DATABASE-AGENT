############################################################
# PR-CYBR Agent Bootstrap Configuration
# This Terraform configuration provides a minimal baseline
# that validates workspace variables and makes them available
# as structured outputs for downstream automation (e.g. the
# tfc-sync GitHub Action). Actual provisioning of resources
# occurs in centralized modules managed by the platform team.
############################################################

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }
}

# A simple null resource allows plan/apply to exercise the
# configuration without modifying infrastructure. The triggers
# reference key locals to ensure Terraform detects changes
# whenever workspace variables drift.
resource "null_resource" "agent_configuration_checksum" {
  triggers = {
    agent_identity_hash  = sha1(jsonencode(local.agent_identity))
    docker_registry_hash = sha1(jsonencode(local.docker_registry))
    notion_hash          = sha1(jsonencode(local.notion))
    github_actions_hash  = sha1(jsonencode(local.github_actions))
  }
}
