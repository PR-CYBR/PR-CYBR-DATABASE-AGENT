**Assistant-ID**:
- `asst_RDbb47Alxh9JyU5FPSoxleDF`

**Github Repository**:
- Repo: `https://github.com/PR-CYBR/PR-CYBR-DATABASE-AGENT`
- Setup Script (local): `https://github.com/PR-CYBR/PR-CYBR-DATABASE-AGENT/blob/main/scripts/local_setup.sh`
- Setup Script (cloud): `https://github.com/PR-CYBR/PR-CYBR-DATABASE-AGENT/blob/main/.github/workflows/docker-compose.yml`
- Project Board: `https://github.com/orgs/PR-CYBR/projects/8`
- Discussion Board: `https://github.com/PR-CYBR/PR-CYBR-DATABASE-AGENT/discussions`
- Wiki: `https://github.com/PR-CYBR/PR-CYBR-DATABASE-AGENT/wiki`

**Docker Repository**:
- Repo: `https://hub.docker.com/r/prcybr/pr-cybr-database-agent`
- Pull-Command:
```shell
docker pull prcybr/pr-cybr-database-agent
```


---


```markdown
# System Instructions for PR-CYBR-DATABASE-AGENT

## Role:
You are the `PR-CYBR-DATABASE-AGENT`, an AI agent responsible for managing and maintaining the database infrastructure of the PR-CYBR initiative. Your primary role is to ensure that all data repositories are secure, optimized, and accessible to support PR-CYBR’s operations, analytics, and decision-making processes.

## Core Functions:
1. **Database Management**:
   - Design, implement, and maintain relational and non-relational database structures to support the diverse needs of PR-CYBR.
   - Regularly monitor and optimize database performance to ensure high availability and low latency.
   - Maintain and update schema definitions to adapt to evolving project requirements.

2. **Data Storage and Retrieval**:
   - Ensure efficient storage and retrieval of large datasets, including geospatial data, agent reports, logs, and analytics outputs.
   - Provide robust indexing and querying mechanisms to support fast data access for all agents and systems.
   - Enable secure multi-user access to databases with appropriate role-based permissions.

3. **Backup and Recovery**:
   - Implement automated backup processes to safeguard data integrity and prevent data loss.
   - Establish disaster recovery protocols to quickly restore data in the event of a system failure.
   - Regularly test recovery processes to ensure reliability.

4. **Data Security and Compliance**:
   - Enforce strong encryption standards for data at rest and in transit.
   - Monitor databases for unauthorized access, anomalies, and potential security threats.
   - Ensure compliance with all applicable legal and ethical standards for data storage and processing.

5. **Inter-Agent Support**:
   - Act as the central repository for structured data required by other PR-CYBR agents.
   - Provide seamless API access for data querying, updates, and reporting across agents.
   - Log and track all database transactions initiated by agents for auditing and transparency.

6. **Database Scalability**:
   - Design scalable architectures to handle the growth of PR-CYBR’s operations and data volume.
   - Optimize storage solutions to accommodate large datasets such as geospatial information, cybersecurity logs, and predictive analytics.
   - Evaluate and incorporate cloud-based database solutions when necessary to meet demands.

7. **Data Integrity and Quality**:
   - Perform routine checks to ensure data consistency and validity across all tables and records.
   - Implement constraints, triggers, and other mechanisms to maintain database integrity.
   - Work with the PR-CYBR-DATA-INTEGRATION-AGENT to validate incoming data before storage.

8. **Reporting and Diagnostics**:
   - Generate real-time diagnostics on database health, usage, and performance metrics.
   - Provide summary reports and visualizations to support PR-CYBR’s management and decision-making processes.
   - Notify system administrators of any critical issues or potential failures.

## Key Directives:
- Ensure databases are always accessible, secure, and optimized.
- Support the operational efficiency of other agents by maintaining robust database infrastructure.
- Proactively address potential issues to minimize downtime and data-related errors.
- Align database management strategies with PR-CYBR’s mission and scalability goals.

## Interaction Guidelines:
- Respond to requests for database queries, schema updates, or performance diagnostics promptly.
- Provide clear feedback on database operations, including any errors or inconsistencies.
- Collaborate with other agents to enhance data accessibility and usability.
- Use technical yet understandable language when communicating with non-technical stakeholders.

## Context Awareness:
- Maintain an understanding of PR-CYBR’s mission, data structure, and operational goals.
- Adapt to changes in database requirements as PR-CYBR expands its operations and datasets.
- Integrate with PR-CYBR-DATA-INTEGRATION-AGENT to ensure data flows smoothly into and out of the database systems.

## Tools and Integration:
You are equipped with advanced database management tools, query optimization capabilities, and access to PR-CYBR’s centralized and distributed databases. Use these tools to maintain system integrity, optimize performance, and ensure data availability for all agents and systems.
```

**Directory Structure**:

```shell
PR-CYBR-DATABASE-AGENT/
	.github/
		workflows/
			ci-cd.yml
			docker-compose.yml
			openai-function.yml
	config/
		docker-compose.yml
		secrets.example.yml
		settings.yml
	docs/
		OPORD/
		README.md
	scripts/
		deploy_agent.sh
		local_setup.sh
		provision_agent.sh
	src/
		agent_logic/
			__init__.py
			core_functions.py
		shared/
			__init__.py
			utils.py
	tests/
		test_core_functions.py
	web/
		README.md
		index.html
	.gitignore
	LICENSE
	README.md
	requirements.txt
	setup.py
```

## Agent Core Functionality Overview

```markdown
# PR-CYBR-DATABASE-AGENT Core Functionality Technical Outline

## Introduction

The **PR-CYBR-DATABASE-AGENT** is responsible for managing and maintaining the database infrastructure of the PR-CYBR initiative. Its primary role is to ensure that all data repositories are secure, optimized, and accessible to support PR-CYBR’s operations, analytics, and decision-making processes.
```

```markdown
### Directory Structure

PR-CYBR-DATABASE-AGENT/
├── config/
│   ├── docker-compose.yml
│   ├── secrets.example.yml
│   └── settings.yml
├── scripts/
│   ├── deploy_agent.sh
│   ├── local_setup.sh
│   └── provision_agent.sh
├── src/
│   ├── agent_logic/
│   │   ├── __init__.py
│   │   └── core_functions.py
│   ├── db_management/
│   │   ├── __init__.py
│   │   ├── schema_definition.py
│   │   ├── backup_and_recovery.py
│   │   └── performance_optimization.py
│   ├── shared/
│   │   ├── __init__.py
│   │   └── utils.py
│   └── interfaces/
│       ├── __init__.py
│       └── inter_agent_comm.py
├── tests/
│   ├── test_core_functions.py
│   ├── test_backup_and_recovery.py
│   └── test_performance.py
└── web/
    ├── static/
    ├── templates/
    └── app.py
```

```markdown
## Key Files and Modules

- **`src/agent_logic/core_functions.py`**: Contains the main logic for database operations.
- **`src/db_management/schema_definition.py`**: Manages database schemas and migrations.
- **`src/db_management/backup_and_recovery.py`**: Implements backup and disaster recovery processes.
- **`src/db_management/performance_optimization.py`**: Handles performance tuning and monitoring.
- **`src/shared/utils.py`**: Provides utility functions for database connectivity and logging.
- **`src/interfaces/inter_agent_comm.py`**: Facilitates data exchange with other agents.

## Core Functionalities

### 1. Database Management (`core_functions.py`)

#### Modules and Functions:

- **`initialize_database()`**
  - Inputs: Schema definitions from `schema_definition.py`.
  - Processes: Sets up initial database structures.
  - Outputs: Operational database ready for data insertion.

- **`manage_connections()`**
  - Inputs: Connection requests from agents.
  - Processes: Manages connection pooling and authentication.
  - Outputs: Secure database connections.

#### Interaction with Other Agents:

- **Data Access**: Provides secure connections to agents like `PR-CYBR-DATA-INTEGRATION-AGENT`.
- **Schema Updates**: Coordinates with `PR-CYBR-BACKEND-AGENT` for schema changes.

### 2. Schema Definition and Management (`schema_definition.py`)

#### Modules and Functions:

- **`define_schema()`**
  - Inputs: Data models and requirements from other agents.
  - Processes: Creates or updates database schemas.
  - Outputs: Updated schemas applied to the database.

- **`run_migrations()`**
  - Inputs: Migration scripts.
  - Processes: Applies changes to the database structure safely.
  - Outputs: Database structure updated without data loss.

#### Interaction with Other Agents:

- **Data Consistency**: Ensures that schema changes are backward compatible.
- **Change Notifications**: Informs `PR-CYBR-DATA-INTEGRATION-AGENT` of schema updates.

### 3. Backup and Recovery (`backup_and_recovery.py`)

#### Modules and Functions:

- **`perform_backup()`**
  - Inputs: Backup schedules from `settings.yml`.
  - Processes: Creates backups of the database at specified intervals.
  - Outputs: Backup files stored securely.

- **`restore_from_backup()`**
  - Inputs: Backup files, restore point information.
  - Processes: Restores database to a previous state.
  - Outputs: Database state reverted as needed.

#### Interaction with Other Agents:

- **Disaster Recovery**: Coordinates with `PR-CYBR-INFRASTRUCTURE-AGENT` for infrastructure-level recovery.
- **Data Integrity**: Ensures that `PR-CYBR-SECURITY-AGENT` protocols are followed during backup and restore.

### 4. Performance Optimization (`performance_optimization.py`)

#### Modules and Functions:

- **`monitor_performance()`**
  - Inputs: Real-time performance metrics.
  - Processes: Analyzes database performance, identifies slow queries.
  - Outputs: Performance reports and alerts.

- **`optimize_queries()`**
  - Inputs: Query logs, index usage statistics.
  - Processes: Rewrites queries, adds indexes, and adjusts configurations.
  - Outputs: Improved database performance.

#### Interaction with Other Agents:

- **Feedback Loop**: Works with `PR-CYBR-PERFORMANCE-AGENT` to align optimization efforts.
- **Resource Allocation**: Informs `PR-CYBR-MGMT-AGENT` of resource needs.

### 5. Data Storage and Retrieval (`core_functions.py`)

#### Modules and Functions:

- **`execute_query()`**
  - Inputs: SQL queries from other agents.
  - Processes: Executes queries securely.
  - Outputs: Query results returned to requesting agents.

- **`manage_transactions()`**
  - Inputs: Transactional operations.
  - Processes: Ensures ACID properties are maintained.
  - Outputs: Consistent and reliable data transactions.

#### Interaction with Other Agents:

- **Data Provisioning**: Supplies data to `PR-CYBR-FRONTEND-AGENT` and `PR-CYBR-BACKEND-AGENT`.
- **Data Integrity**: Collaborates with `PR-CYBR-DATA-INTEGRATION-AGENT` to ensure data consistency.

## Inter-Agent Communication Mechanisms

### Communication Protocols

- **Database Drivers**: Agents connect using standardized database drivers (e.g., psycopg2 for PostgreSQL).
- **API Endpoints**: Exposes APIs for database operations when direct connections are not ideal.

### Data Formats

- **SQL Queries and Results**: Standard SQL used for data manipulation.
- **JSON**: For API-based data exchange.

### Authentication and Authorization

- **Database Credentials**: Managed securely, with role-based permissions.
- **SSL/TLS**: Encrypted connections to the database.

## Interaction with Specific Agents

### PR-CYBR-BACKEND-AGENT

- **Data Access**: Provides database connectivity for backend services.
- **Schema Synchronization**: Coordinates on data models and ORM mappings.

### PR-CYBR-SECURITY-AGENT

- **Security Audits**: Receives security guidelines and implements them.
- **Encryption**: Works together to encrypt sensitive data fields.

### PR-CYBR-DATA-INTEGRATION-AGENT

- **Data Insertion**: Receives validated data for storage.
- **Data Retrieval**: Provides data upon request for integration purposes.

## Technical Workflows

### Backup and Recovery Workflow

1. **Scheduled Backup**: `perform_backup()` runs based on schedule.
2. **Backup Storage**: Backups are stored in secure, redundant locations.
3. **Recovery Process**: In the event of failure, `restore_from_backup()` is executed.
4. **Validation**: Post-recovery validation to ensure data integrity.

### Performance Monitoring Workflow

1. **Data Collection**: `monitor_performance()` collects metrics.
2. **Analysis**: Identifies performance issues like slow queries.
3. **Optimization**: `optimize_queries()` implements improvements.
4. **Reporting**: Shares performance reports with relevant agents.

## Database Technologies Used

- **Primary Database**: PostgreSQL (or another robust RDBMS).
- **Replication**: Implements master-slave replication for redundancy.
- **Clustering**: Uses database clustering for load balancing.

## Error Handling and Logging

- **Error Logging**: Captures database errors and exceptions.
- **Alerting**: Sends alerts to `PR-CYBR-MGMT-AGENT` and `PR-CYBR-SECURITY-AGENT` when critical issues occur.
- **Transaction Rollback**: Ensures failed transactions do not corrupt data.

## Security Considerations

- **Access Controls**: Strict user roles and permissions.
- **Data Encryption**: Encrypts data at rest and in transit.
- **Audit Trails**: Maintains logs for all database activities.

## Deployment and Scaling

- **Containerization**: Runs the database in Docker containers where appropriate.
- **Horizontal Scaling**: Adds read replicas to distribute load.
- **Vertical Scaling**: Increases resources for the primary database server when necessary.

## Conclusion

The **PR-CYBR-DATABASE-AGENT** is crucial for the reliable storage and retrieval of data within the PR-CYBR initiative. By providing secure, efficient, and scalable database services, it supports the data needs of all other agents and ensures that the initiative's operations are underpinned by robust data infrastructure.
```


---

## OpenAI Functions

## Function List for PR-CYBR-DATABASE-AGENT

```markdown
## Function List for PR-CYBR-DATABASE-AGENT

1. **load_data**: Loads datasets into the database from specified file sources, enabling efficient data storage and processing.
2. **query_data**: Executes queries on the database to retrieve specific information based on user-defined parameters, ensuring quick data access.
3. **backup_database**: Automates the process of backing up database contents to prevent data loss and ensure data integrity.
4. **restore_database**: Restores the database from backups in the event of data loss or system failure, allowing for quick recovery.
5. **monitor_performance**: Continuously monitors database performance metrics and provides diagnostics for optimizing database speed and efficiency.
6. **encrypt_data**: Applies encryption protocols to secure sensitive data at rest and in transit, ensuring compliance with security standards.
7. **track_transactions**: Logs and tracks all database transactions initiated by agents for auditing purposes and to enhance transparency.
8. **generate_reports**: Creates custom reports based on database queries that visualize data insights for management and decision-making processes.
9. **manage_permissions**: Configures role-based access controls to manage user permissions and ensure secure database interactions.
10. **validate_data_integrity**: Performs checks to validate the consistency and integrity of the data stored in the database.
```