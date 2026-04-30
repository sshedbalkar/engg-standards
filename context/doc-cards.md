# ESTD Doc Cards

## Lookup Strategy
- primary_lookup: card_kind + lookup_key
- ordering: kind_group_first, numeric_estd_id_within_group
- jump_index: present
- entry_id_format: stable ESTD ID

## Jump Index
- kind.estd-doc: `ESTD0` through `ESTD19`

## Cards

### ESTD0
- path: `docs/ESTD0_-_Markdown_format.md`
- kind: estd-doc
- purpose: template for ESTD metadata and section skeleton
- state: verified
- audience: engineers authoring or reshaping ESTD docs
- parent_docs: none
- major_overlaps: ESTD15 for non-ESTD technical docs
- common_edit_reasons: improve ESTD template, metadata table, base structure
- minimum_related_docs_to_read: `AGENTS.md`, `README.md`

### ESTD1
- path: `docs/ESTD1_-_Common_Engg_Standards_And_Best_Practices.md`
- kind: estd-doc
- purpose: root engineering standard for all engineers
- state: verified
- audience: all engineers
- parent_docs: none
- major_overlaps: every child ESTD narrows this doc
- common_edit_reasons: shared engineering rules, process, environments, documentation, trust boundaries, permission boundaries, quality bars
- minimum_related_docs_to_read: `AGENTS.md`, `README.md`

### ESTD2
- path: `docs/ESTD2_-_General_Client_Engg_Standards.md`
- kind: estd-doc
- purpose: cross-client rules for Bingo client work
- state: verified
- audience: client engineers
- parent_docs: `ESTD1`
- major_overlaps: ESTD3 for Unity/C#, ESTD10 for PR workflow
- common_edit_reasons: client architecture, UX, state flow, asset/loading concerns
- minimum_related_docs_to_read: `docs/ESTD1_-_Common_Engg_Standards_And_Best_Practices.md`

### ESTD3
- path: `docs/ESTD3_-_Unity_and_C#_Standards.md`
- kind: estd-doc
- purpose: Unity and C# coding rules
- state: verified
- audience: Unity/C# engineers
- parent_docs: `ESTD1`, `ESTD2`
- major_overlaps: ESTD14 for naming, ESTD16 for testing/paths
- common_edit_reasons: C# style, Unity-specific patterns, scene/runtime organization
- minimum_related_docs_to_read: `docs/ESTD1_-_Common_Engg_Standards_And_Best_Practices.md`, `docs/ESTD2_-_General_Client_Engg_Standards.md`

### ESTD4
- path: `docs/ESTD4_-_Server_Engg_Standards.md`
- kind: estd-doc
- purpose: server-wide baseline across PHP, Java, and SmartFox
- state: verified
- audience: server engineers
- parent_docs: `ESTD1`
- major_overlaps: ESTD6, ESTD7, ESTD9, ESTD12
- common_edit_reasons: service boundaries, APIs, trust and permission boundaries, ops, security, reliability
- minimum_related_docs_to_read: `docs/ESTD1_-_Common_Engg_Standards_And_Best_Practices.md`

### ESTD5
- path: `docs/ESTD5_-_Cloud_Engg_Standards.md`
- kind: estd-doc
- purpose: provider-agnostic cloud engineering rules
- state: verified
- audience: engineers provisioning or deploying cloud resources
- parent_docs: `ESTD1`, `ESTD4` recommended
- major_overlaps: ESTD8 for AWS specifics, ESTD13 for pipeline usage
- common_edit_reasons: environment strategy, infra principles, identity and permission boundaries, deployment guardrails
- minimum_related_docs_to_read: `docs/ESTD1_-_Common_Engg_Standards_And_Best_Practices.md`, `docs/ESTD4_-_Server_Engg_Standards.md`

### ESTD6
- path: `docs/ESTD6_-_PHP_Programming_Standards.md`
- kind: estd-doc
- purpose: PHP rules for legacy API and related PHP code
- state: verified
- audience: PHP engineers
- parent_docs: `ESTD1`, `ESTD4`, `ESTD5`
- major_overlaps: ESTD9 for DB work, ESTD14 for naming
- common_edit_reasons: PHP style, monolith patterns, safety and maintainability rules
- minimum_related_docs_to_read: `docs/ESTD1_-_Common_Engg_Standards_And_Best_Practices.md`, `docs/ESTD4_-_Server_Engg_Standards.md`

### ESTD7
- path: `docs/ESTD7_-_Java_Programming_Standards.md`
- kind: estd-doc
- purpose: Java rules for SEAM services and SmartFox Java code
- state: verified
- audience: Java engineers
- parent_docs: `ESTD1`, `ESTD4`, `ESTD5`
- major_overlaps: ESTD12 for SmartFox specialization, ESTD9 for persistence rules
- common_edit_reasons: Java structure, service design, code style, operational patterns
- minimum_related_docs_to_read: `docs/ESTD1_-_Common_Engg_Standards_And_Best_Practices.md`, `docs/ESTD4_-_Server_Engg_Standards.md`

### ESTD8
- path: `docs/ESTD8_-_AWS_Standards.md`
- kind: estd-doc
- purpose: AWS-specific implementation rules under cloud standards
- state: verified
- audience: engineers working on AWS resources
- parent_docs: `ESTD5`
- major_overlaps: ESTD13 for CI/CD infra, ESTD9 for database hosting constraints
- common_edit_reasons: service configuration, IAM permission boundaries, AWS deployment rules, examples
- minimum_related_docs_to_read: `docs/ESTD5_-_Cloud_Engg_Standards.md`

### ESTD9
- path: `docs/ESTD9_-_Database_Standards.md`
- kind: estd-doc
- purpose: authoritative DB standard for schema, query, migration, backup, and ops work
- state: verified
- audience: engineers touching database design or operations
- parent_docs: `ESTD1`, `ESTD4`, `ESTD8`
- major_overlaps: ESTD6 and ESTD7 for application access patterns, ESTD5 for infra principles
- common_edit_reasons: schema rules, query guidance, database permission boundaries, migration process, backup/restore policy
- minimum_related_docs_to_read: `docs/ESTD1_-_Common_Engg_Standards_And_Best_Practices.md`, `docs/ESTD4_-_Server_Engg_Standards.md`, `docs/ESTD8_-_AWS_Standards.md`

### ESTD10
- path: `docs/ESTD10_-_PR_Authoring_And_Reviewing_Standards.md`
- kind: estd-doc
- purpose: PR authoring and reviewing rules that enforce the standards in practice
- state: verified
- audience: all engineers
- parent_docs: `ESTD1` through `ESTD13`
- major_overlaps: every implementation standard, especially review-ready evidence and exceptions
- common_edit_reasons: PR template, reviewer expectations, approval flow, evidence requirements
- minimum_related_docs_to_read: `docs/ESTD1_-_Common_Engg_Standards_And_Best_Practices.md`, `README.md`

### ESTD11
- path: `docs/ESTD11_-_Web_Development_and_Deployment_Standards.md`
- kind: estd-doc
- purpose: standards for internal web tools and dashboards
- state: verified
- audience: engineers building or deploying internal web tools
- parent_docs: `ESTD1`, `ESTD4`, `ESTD5`, `ESTD8`, `ESTD13`
- major_overlaps: ESTD13 for pipelines, ESTD9 for persistence, ESTD14 for naming
- common_edit_reasons: web architecture, deployment, security, operational UX for internal tools
- minimum_related_docs_to_read: `docs/ESTD1_-_Common_Engg_Standards_And_Best_Practices.md`, `docs/ESTD4_-_Server_Engg_Standards.md`, `docs/ESTD5_-_Cloud_Engg_Standards.md`

### ESTD12
- path: `docs/ESTD12_-_Smartfox_Server_Standards.md`
- kind: estd-doc
- purpose: SmartFox-specific Java and live-server rules
- state: verified
- audience: engineers contributing to SmartFox live server
- parent_docs: `ESTD1`, `ESTD4`, `ESTD7`
- major_overlaps: ESTD7 for Java baseline, ESTD9 for persistence checkpoints
- common_edit_reasons: SmartFox runtime patterns, room logic, live-server operational safeguards
- minimum_related_docs_to_read: `docs/ESTD4_-_Server_Engg_Standards.md`, `docs/ESTD7_-_Java_Programming_Standards.md`

### ESTD13
- path: `docs/ESTD13_-_Jenkins_CI_CD_Standards.md`
- kind: estd-doc
- purpose: Jenkins rules for build, sign, archive, promote, and pipeline behavior
- state: verified
- audience: engineers authoring, modifying, or running Jenkins pipelines
- parent_docs: `ESTD1`, `ESTD5`, `ESTD8`, `ESTD11`
- major_overlaps: ESTD11 for web tool builds, ESTD5/ESTD8 for environment and AWS rules
- common_edit_reasons: pipeline design, promotion rules, artifact handling, build agent usage
- minimum_related_docs_to_read: `docs/ESTD1_-_Common_Engg_Standards_And_Best_Practices.md`, `docs/ESTD5_-_Cloud_Engg_Standards.md`, `docs/ESTD8_-_AWS_Standards.md`

### ESTD14
- path: `docs/ESTD14_-_Hierarchical_Naming_Strategy_for_Programming_Entities.md`
- kind: estd-doc
- purpose: language-agnostic naming strategy for programming entities
- state: verified
- audience: all engineers
- parent_docs: none
- major_overlaps: ESTD3, ESTD6, ESTD7, ESTD11, ESTD17
- common_edit_reasons: identifier naming rules, examples, terminology alignment
- minimum_related_docs_to_read: `AGENTS.md`

### ESTD15
- path: `docs/ESTD15_-_Technical_Document_Guide_and_Template.md`
- kind: estd-doc
- purpose: guide and templates for TADs, ADRs, runbooks, RCAs, and migration plans
- state: verified
- audience: engineers writing technical documents
- parent_docs: `ESTD1`
- major_overlaps: ESTD0 for ESTD docs, ESTD10 for review expectations
- common_edit_reasons: document templates, review rules, document lifecycle, writing standards
- minimum_related_docs_to_read: `docs/ESTD1_-_Common_Engg_Standards_And_Best_Practices.md`, `docs/ESTD0_-_Markdown_format.md`

### ESTD16
- path: `docs/ESTD16_-_Paths_And_Unit_Testing_Strategy.md`
- kind: estd-doc
- purpose: path planning, branch discipline, and unit-testing strategy
- state: verified
- audience: all engineers
- parent_docs: none
- major_overlaps: ESTD3, ESTD6, ESTD7, ESTD11
- common_edit_reasons: test strategy, path design, branch usage, edge-case planning
- minimum_related_docs_to_read: `AGENTS.md`

### ESTD17
- path: `docs/ESTD17_-_Waterfall_Data_Processing_Pattern.md`
- kind: estd-doc
- purpose: shared pattern for staged data transformation pipelines
- state: verified
- audience: all engineers, especially server/tooling/automation work
- parent_docs: `ESTD1`, `ESTD4`, `ESTD14`
- major_overlaps: ESTD4 for server architecture, ESTD14 for pipeline naming
- common_edit_reasons: processor flow, fallback behavior, pipeline naming, failure handling
- minimum_related_docs_to_read: `docs/ESTD1_-_Common_Engg_Standards_And_Best_Practices.md`, `docs/ESTD4_-_Server_Engg_Standards.md`, `docs/ESTD14_-_Hierarchical_Naming_Strategy_for_Programming_Entities.md`

### ESTD18
- path: `docs/ESTD18_-_Codebase_Folder_Structure_Standards.md`
- kind: estd-doc
- purpose: canonical root-level folder structure for project types
- state: verified
- audience: all engineers
- parent_docs: `ESTD1`
- major_overlaps: ESTD3, ESTD5, ESTD6, ESTD7, ESTD8, ESTD11, ESTD12, ESTD13
- common_edit_reasons: repo layout rules, top-level folder expectations, cross-project structure
- minimum_related_docs_to_read: `docs/ESTD1_-_Common_Engg_Standards_And_Best_Practices.md`, `AGENTS.md`

### ESTD19
- path: `docs/ESTD19_-_Dependency_Management_and_Coupling_Standards.md`
- kind: estd-doc
- purpose: standards for coupling and dependency management
- state: verified
- audience: all engineers
- parent_docs: `ESTD1`
- major_overlaps: ESTD4 for service boundaries, ESTD17 for pipeline composition
- common_edit_reasons: layering rules, coupling guidance, dependency direction, examples
- minimum_related_docs_to_read: `docs/ESTD1_-_Common_Engg_Standards_And_Best_Practices.md`
