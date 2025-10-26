########################################################
# Terraform Cloud Workspace Variable Alignment Template
# Populate these values within Terraform Cloud or via
# secure automation. Do not commit actual secrets here.
########################################################

# --- Docker / Registry ---
DOCKERHUB_TOKEN                = "<set-in-tfc>"
DOCKERHUB_USERNAME             = "prcybr-bot"
PR_CYBR_DOCKER_PASS            = "<set-in-tfc>"
PR_CYBR_DOCKER_USER            = "prcybr-bot"

# --- Global Infrastructure URIs ---
GLOBAL_DOMAIN                  = "example.prcybr.net"
GLOBAL_ELASTIC_URI             = "https://elastic.example.prcybr.net"
GLOBAL_GRAFANA_URI             = "https://grafana.example.prcybr.net"
GLOBAL_KIBANA_URI              = "https://kibana.example.prcybr.net"
GLOBAL_PROMETHEUS_URI          = "https://prometheus.example.prcybr.net"

# --- Networking / Security ---
GLOBAL_TAILSCALE_AUTHKEY       = "<set-in-tfc>"
GLOBAL_TRAEFIK_ACME_EMAIL      = "ops@example.prcybr.net"
GLOBAL_TRAEFIK_ENTRYPOINTS     = "web,websecure"
GLOBAL_ZEROTIER_NETWORK_ID     = "<set-in-tfc>"

# --- Agent Tokens ---
AGENT_ACTIONS                  = "<set-in-tfc>"
AGENT_COLLAB                   = "<set-in-tfc>"
GITHUB_TOKEN                   = "<set-in-tfc>"
TFC_TOKEN                      = "<set-in-tfc>"

# --- Notion Workspace ---
NOTION_DISCUSSIONS_ARC_DB_ID         = "<set-in-tfc>"
NOTION_ISSUES_BACKLOG_DB_ID          = "<set-in-tfc>"
NOTION_KNOWLEDGE_FILE_DB_ID          = "<set-in-tfc>"
NOTION_PAGE_ID                       = "<set-in-tfc>"
NOTION_PR_BACKLOG_DB_ID              = "<set-in-tfc>"
NOTION_PROJECT_BOARD_BACKLOG_DB_ID   = "<set-in-tfc>"
NOTION_TASK_BACKLOG_DB_ID            = "<set-in-tfc>"
NOTION_TOKEN                         = "<set-in-tfc>"
