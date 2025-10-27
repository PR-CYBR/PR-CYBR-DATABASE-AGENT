terraform {
  required_version = ">= 1.5.0"

  cloud {
    organization = "pr-cybr"

    workspaces {
      name = "PR-CYBR-DATABASE-AGENT"
    }
  }
}
