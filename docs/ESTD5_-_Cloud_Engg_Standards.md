# ESTD5 - Cloud Engineering Standards and Best Practices for Infrastructure Management

**ESTD5 — Cloud Engineering Standards**

| Field | Value |
|:----- |:----- |
| Document ID | ESTD5 |
| Version | 5.1 |
| Status | Active |
| Last Updated | 2026-04-30 |
| Applies To | All engineers who provision, configure, or deploy cloud resources |
| Depends On | [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers), [ESTD4](./ESTD4_-_Server_Engg_Standards.md#estd4---server-engineering-standards-and-best-practices) (recommended) |
| Approval | Director of Engineering / Server Architect |

---

> **📋 Living Document Notice** This document is a work in progress and will evolve as our systems, practices, and understanding mature. Feedback, questions, and suggestions are welcome — please submit them via comments on the corresponding Confluence page. However, the standards defined herein **must be strictly followed** in all active work. Any exception requires **explicit written approval** from the Director of Engineering or the appropriate Architect, and must be documented in the PR description, the exception log, or the relevant Confluence page.

---

## How to Use This Document

ESTD5 defines cloud-provider-agnostic principles and standards. It covers the "what and why" of cloud engineering — principles that apply regardless of whether the underlying cloud provider is AWS, GCP, or Azure. [ESTD8](./ESTD8_-_AWS_Standards.md#estd8---aws-standards-document-for-bingo-game-infrastructure) (AWS Standards) translates these principles into specific AWS service configurations and Terraform examples. When a rule in ESTD5 conflicts with [ESTD8](./ESTD8_-_AWS_Standards.md#estd8---aws-standards-document-for-bingo-game-infrastructure), the more restrictive of the two applies.

---

## Table of Contents

- [ESTD5 - Cloud Engineering Standards and Best Practices for Infrastructure Management](#estd5---cloud-engineering-standards-and-best-practices-for-infrastructure-management)
  - [How to Use This Document](#how-to-use-this-document)
  - [Table of Contents](#table-of-contents)
  - [1. Purpose and Scope](#1-purpose-and-scope)
  - [2. Infrastructure as Code (IaC)](#2-infrastructure-as-code-iac)
    - [2.1 All Infrastructure Must Be Code](#21-all-infrastructure-must-be-code)
    - [2.2 IaC Tool Choice](#22-iac-tool-choice)
    - [2.3 IaC Code Quality Standards](#23-iac-code-quality-standards)
    - [2.4 IaC Module Structure](#24-iac-module-structure)
    - [2.5 State Management](#25-state-management)
    - [2.6 Drift Detection](#26-drift-detection)
    - [2.7 IaC Security Vulnerabilities](#27-iac-security-vulnerabilities)
  - [3. Environment Strategy](#3-environment-strategy)
    - [3.1 Mandatory Environments](#31-mandatory-environments)
    - [3.2 Environment Parity](#32-environment-parity)
    - [3.3 Build Promotion Policy](#33-build-promotion-policy)
    - [3.4 Periodic Content Reset Environments](#34-periodic-content-reset-environments)
  - [4. Security and Identity Principles](#4-security-and-identity-principles)
    - [4.1 Principle of Least Privilege](#41-principle-of-least-privilege)
    - [4.2 Account/Project Separation](#42-accountproject-separation)
    - [4.3 No Long-Lived Credentials for Workloads](#43-no-long-lived-credentials-for-workloads)
    - [4.4 MFA for All Human Access](#44-mfa-for-all-human-access)
    - [4.5 Cloud Security Vulnerabilities](#45-cloud-security-vulnerabilities)
  - [5. Network Security Architecture](#5-network-security-architecture)
    - [5.1 Layered Network Design](#51-layered-network-design)
    - [5.2 Security Groups / Firewall Rules](#52-security-groups--firewall-rules)
    - [5.3 Encryption in Transit](#53-encryption-in-transit)
    - [5.4 Web Application Firewall (WAF)](#54-web-application-firewall-waf)
    - [5.5 Network and Transport Vulnerabilities](#55-network-and-transport-vulnerabilities)
  - [6. Secrets Management in Cloud](#6-secrets-management-in-cloud)
    - [6.1 Cloud-Native Secrets Manager](#61-cloud-native-secrets-manager)
    - [6.2 Secret Access Pattern](#62-secret-access-pattern)
    - [6.3 Migration from Environment Variables](#63-migration-from-environment-variables)
  - [7. Compute: Sizing, Scaling, and Cost](#7-compute-sizing-scaling-and-cost)
    - [7.1 Right-Sizing Principle](#71-right-sizing-principle)
    - [7.2 Horizontal vs. Vertical Scaling](#72-horizontal-vs-vertical-scaling)
    - [7.3 Auto Scaling for Stateless Services](#73-auto-scaling-for-stateless-services)
    - [7.4 Scheduled Scaling for Known Traffic Patterns](#74-scheduled-scaling-for-known-traffic-patterns)
  - [8. Deployment Pipelines](#8-deployment-pipelines)
    - [8.1 CI/CD Is Mandatory](#81-cicd-is-mandatory)
    - [8.2 Pipeline Structure](#82-pipeline-structure)
    - [8.3 Deployment Strategies](#83-deployment-strategies)
    - [8.4 Deployment Safety Rules](#84-deployment-safety-rules)
    - [8.5 Jenkins for Client and Web Tool Builds](#85-jenkins-for-client-and-web-tool-builds)
    - [8.6 CI/CD and Supply Chain Vulnerabilities](#86-cicd-and-supply-chain-vulnerabilities)
  - [9. Observability in the Cloud](#9-observability-in-the-cloud)
    - [9.1 Observability Stack](#91-observability-stack)
    - [9.2 Universal Tagging](#92-universal-tagging)
    - [9.3 Standard Operational Dashboards](#93-standard-operational-dashboards)
  - [10. Data Storage Standards](#10-data-storage-standards)
    - [10.1 Encryption at Rest](#101-encryption-at-rest)
    - [10.2 Database High Availability](#102-database-high-availability)
    - [10.3 Backup Requirements](#103-backup-requirements)
    - [10.4 S3 / Object Storage](#104-s3--object-storage)
  - [11. Backup, Recovery, and Resilience](#11-backup-recovery-and-resilience)
    - [11.1 Multi-Availability Zone Deployment](#111-multi-availability-zone-deployment)
    - [11.2 Restore Testing](#112-restore-testing)
    - [11.3 Runbooks for Recovery](#113-runbooks-for-recovery)
  - [12. Cost Management](#12-cost-management)
    - [12.1 Cost Awareness Is Everyone's Responsibility](#121-cost-awareness-is-everyones-responsibility)
    - [12.2 Monthly Cost Review](#122-monthly-cost-review)
    - [12.3 Reserved Capacity for Predictable Workloads](#123-reserved-capacity-for-predictable-workloads)
    - [12.4 Cost Anomaly Detection](#124-cost-anomaly-detection)
  - [13. Compliance and Data Residency](#13-compliance-and-data-residency)
  - [14. Common Pitfalls to Avoid](#14-common-pitfalls-to-avoid)

---

## 1. Purpose and Scope

This document applies to all cloud infrastructure used by both Bingo games. The primary cloud provider is AWS (see [ESTD8](./ESTD8_-_AWS_Standards.md#estd8---aws-standards-document-for-bingo-game-infrastructure) for AWS-specific implementation). All infrastructure — compute, storage, networking, databases, messaging, CDN — must be provisioned and managed according to these standards.

**Our geography context:** Primary player base is in the USA (US-East and US-West time zones). Engineering and operations teams are in India (IST, UTC+5:30). Cloud infrastructure should be optimized for US player latency while supporting 
operational workflows during Indian business hours.

---

## 2. Infrastructure as Code (IaC)

Manual infrastructure changes are invisible, un-reviewable, and unrepeatable. In a live-service environment, an undocumented manual change made at 2 a.m. during an incident becomes an unknown variable in every subsequent incident. IaC makes infrastructure as auditable, reviewable, and version-controlled as application code.

### 2.1 All Infrastructure Must Be Code

No cloud resource may be created or modified through the cloud provider's console except for:

- Initial bootstrapping of the IaC state backend itself.  
- Emergency break-glass actions during an active P1 incident (must be followed by an IaC update within 48 hours, including a comment explaining the emergency change).

### 2.2 IaC Tool Choice

Choose a single IaC tool and standardize on it across all teams. The choice must be approved by the Server Architect and the Director of Engineering. Once chosen, changing tools requires a full migration plan. Currently: **Terraform** (see [ESTD8](./ESTD8_-_AWS_Standards.md#estd8---aws-standards-document-for-bingo-game-infrastructure) for detailed Terraform examples).

### 2.3 IaC Code Quality Standards

IaC code is subject to the same quality standards as application code:

- Version-controlled in Git, following the same Gitflow branching strategy as application code.  
- Reviewed via PR before any infrastructure change is applied — infrastructure changes can have as much impact as application changes.  
- **Modular:** Separate modules/stacks for networking, compute, database, and monitoring. No single monolithic IaC file.  
- **Commented:** Every resource must have a comment explaining its purpose.  
- **Parameterized:** All environment-specific values must be variables. Never hardcode production resource names or IDs in a module.

### 2.4 IaC Module Structure

```
infrastructure/
├── modules/              ← Reusable, environment-agnostic modules
│   ├── compute/          ← EC2/ASG module
│   ├── database/         ← RDS module
│   ├── cache/            ← ElastiCache module
│   ├── storage/          ← S3 module
│   ├── networking/       ← VPC/subnets/SGs module
│   └── monitoring/       ← CloudWatch/alerting module
├── environments/
│   ├── dev/              ← dev environment composition
│   ├── qa/               ← QA environment composition
│   ├── staging/          ← staging environment composition
│   └── production/       ← production environment composition
└── global/               ← Account-level resources (IAM roles, DNS, CDN)
```

### 2.5 State Management

IaC state files must be stored in a remote, encrypted, access-controlled backend (e.g., S3 with DynamoDB state locking for Terraform). State files must never be committed to Git. All engineers working on infrastructure must use the same remote state backend.

### 2.6 Drift Detection

Run IaC plan checks (`terraform plan`) in CI on a schedule to detect out-of-band manual changes. Any detected drift from IaC-defined state must be resolved within 48 hours — either by reverting the manual change or by updating the IaC to reflect the intentional change.

### 2.7 IaC Security Vulnerabilities

| Vulnerability | What It Looks Like in Our Environment | Required Controls |
|:--------------|:--------------------------------------|:------------------|
| **Secrets in Terraform state or IaC files** | Passwords, tokens, or private keys appear in `tfstate`, `tfvars`, CDK context, or committed config | Store secrets in managed secret stores; keep state encrypted and access-controlled; never commit live secrets |
| **Wildcard resource Amazon Resource Names (ARNs) / overly broad policy code** | Infrastructure as Code (IaC) creates identity and access management (IAM) policies with `Resource: "*"` or equivalent broad access | Scope resources explicitly; review permission diff carefully in PR; reject permissive defaults |
| **Drift between IaC and live infrastructure** | Manual console changes create untracked exposure that code review never sees | Detect drift regularly and drive all durable changes back into IaC as the source of truth |
| **No peer review on infrastructure changes** | Teams treat infra changes as "just config" and merge or apply them without the same scrutiny as code | Apply the normal PR process to IaC; require review by appropriately skilled engineers |
| **Public-by-default resources** | New load balancers, buckets, or security groups are created with exposure broader than intended | Make secure defaults part of modules; require explicit opt-in for public exposure; add policy checks in CI |
| **Manual hotfixes not backported to code** | Emergency console changes fix an incident temporarily but remain invisible to future reviews and redeploys | After any manual emergency action, reconcile the change into IaC immediately and document it in the incident record |

---

## 3. Environment Strategy

Without isolated environments, a development experiment can corrupt staging data, and a staging change can accidentally propagate to production. Environment isolation also ensures that the build artifact being validated in staging is truly the same artifact that goes to production.

### 3.1 Mandatory Environments

Four environments are required for this project:

| Environment | Purpose | Scale | Data Policy |
|:------------|:--------|:------|:------------|
| **dev** | Individual developer integration testing | Minimal; single-AZ, smallest instance sizes | Synthetic test data only. No real player data. |
| **qa** | Functional QA, regression testing, feature validation | Single-AZ; production-like topology, small instances | Anonymized synthetic data |
| **staging** | Pre-release validation, load testing, stakeholder sign-off | Multi-AZ; production-like topology, 30-50% of production capacity | Anonymized production-like data (PII removed) |
| **production** | Live player traffic | Full production scale, multi-AZ | Real player data |

`dev` and `qa` environments must never have access to production data, production secrets, or production infrastructure. Enforced through separate cloud accounts and strict IAM policies.

### 3.2 Environment Parity

Staging must replicate production's topology: same number of availability zones, same load balancer configuration, same service-to-service communication paths. Scale down instance sizes and reduce capacity to control cost, but **do not simplify the topology.** A staging environment that is architecturally simpler than production will not catch production-specific issues.

Use the same IaC modules for all environments. The only differences are the values of the variables (instance types, counts, capacity).

```hcl
# production/main.tf
module "api_compute" {
  source          = "../../modules/compute"
  instance_type   = "c6i.xlarge"
  min_capacity    = 4
  max_capacity    = 20
  environment     = "production"
}

# staging/main.tf
module "api_compute" {
  source          = "../../modules/compute"
  instance_type   = "c6i.large"   # smaller, but same module
  min_capacity    = 2
  max_capacity    = 6
  environment     = "staging"
}
```

### 3.3 Build Promotion Policy

The exact same build artifact must be promoted through all environments. The artifact that passes QA is the one that goes to staging, and then to production.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Build Promotion Flow                         │
│                                                                 │
│  Code commit                                                    │
│       │                                                         │
│       ▼                                                         │
│  CI Build (lint + unit tests + build artifact)                  │
│       │                                                         │
│       ▼                                                         │
│  Deploy to Dev  → developer smoke test                          │
│       │                                                         │
│       ▼  [passes CI gates]                                      │
│  Deploy to QA   → QA team functional testing + regression       │
│       │                                                         │
│       ▼  [QA sign-off]                                          │
│  Deploy to Staging → load test + stakeholder review             │
│       │                                                         │
│       ▼  [architect approval + staging validation]              │
│  Deploy to Production                                           │
│                                                                 │
│  RULE: The same binary/container image that passed QA is what   │
│  goes to Staging and Production. No rebuilds.                   │
└─────────────────────────────────────────────────────────────────┘
```

Environment-specific configuration (DB endpoints, API keys, feature flags) is injected at deploy time via environment variables or a secrets manager, never baked into the artifact.

### 3.4 Periodic Content Reset Environments

For validating content resets in staging, the staging environment must be configurable to simulate the state of a content reset without affecting production. Use feature flags and CMS configuration, not code changes. Never trigger a "test content reset" in production.

---

## 4. Security and Identity Principles

### 4.1 Principle of Least Privilege

Every identity (human user, service account, application role) must have the minimum permissions required for its specific function. Wildcard permissions are prohibited except in explicitly approved, time-limited administrative roles. Review permissions quarterly and remove anything that is no longer needed.

Cloud permissions are permission boundaries as defined in [ESTD1 §10. Boundary Functions](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#10-boundary-functions) and applied to servers in [ESTD4 §17.6 Server Trust and Permission Boundaries](./ESTD4_-_Server_Engg_Standards.md#176-server-trust-and-permission-boundaries). Identity and access management (IAM) systems must scope each role to the exact service, environment, secret path, queue, database, bucket, and network action required. Over-provisioning "for convenience" increases blast radius: a compromised service can read unrelated secrets, reach production data, mutate infrastructure, or impersonate a deployment job.

### 4.2 Account/Project Separation

Use separate cloud accounts (or equivalent isolation primitives in non-AWS clouds) per environment:

- `bingo-dev` account  
- `bingo-qa` account  
- `bingo-staging` account  
- `bingo-production` account

This provides blast radius isolation: a misconfiguration or security incident in the dev account cannot affect production.

### 4.3 No Long-Lived Credentials for Workloads

Application workloads must use short-lived credentials obtained from the cloud provider's identity system (e.g., AWS IAM instance roles) rather than long-lived access keys. Long-lived credentials are acceptable only for external integrations where short-lived credentials are technically impossible — and even then, they must be stored in the secrets manager, rotated every 90 days, and their access must be logged.

### 4.4 MFA for All Human Access

All cloud console logins must require multi-factor authentication. Root or superadmin accounts must have MFA enabled and credentials stored offline. Root accounts must never be used for day-to-day operations.

### 4.5 Cloud Security Vulnerabilities

| Vulnerability | What It Looks Like in Our Environment | Required Controls |
|:--------------|:--------------------------------------|:------------------|
| **Overly permissive IAM** | An EC2 instance, Lambda, or CI role has broad access such as * actions or unrestricted resource scope | Apply least privilege, review permissions regularly, and prefer scoped roles over static keys |
| **Public object storage** | S3 buckets containing player data, config, logs, or build artifacts are accidentally exposed publicly | Block public access by default; review bucket policy in IaC; separate public content from private content |
| **Security group / firewall misconfiguration** | SSH, MySQL, Redis, or internal admin ports are reachable from the public internet | Keep databases and internal services private; use layered security groups; avoid direct SSH where approved alternatives exist |
| **Secrets in environment variables, user data, or AMI bake scripts** | Secrets leak through instance metadata, launch scripts, process listings, or diagnostic dumps | Retrieve secrets at runtime from a managed store with least-privilege access; keep secrets out of bootstrap artifacts |
| **Unencrypted data at rest** | EBS, RDS, S3, or backup volumes are readable if storage is accessed outside the application path | Enforce encryption at rest for all production and staging data stores |
| **Exposed metadata endpoint abuse** | SSRF or local compromise is used to query EC2 metadata and steal temporary credentials | Use IMDSv2 and harden workloads so they cannot fetch arbitrary internal targets |
| **Unrotated credentials** | Access keys, database passwords, or integration secrets remain valid far longer than intended | Rotate regularly, alert on age, and prefer short-lived credentials issued through IAM where possible |
| **Log data exfiltration** | Logs shipped to third-party systems contain PII, auth tokens, or secret material | Sanitize logs before shipping; mask sensitive fields; review logging on high-risk endpoints |
| **Unpatched runtime or dependency layers** | Base images, AMIs, libraries, or agents contain known CVEs and remain deployed | Run vulnerability scans in CI/CD and patch critical issues on an expedited timeline |

---

## 5. Network Security Architecture

### 5.1 Layered Network Design

Compute and data resources must not be directly accessible from the internet. Use a layered network topology:

```
Internet
    │
    ▼
[ Public Layer ]  ← Load balancer, CDN origin, NAT Gateway
    │               (internet-facing only; no compute here)
    ▼
[ Application Layer ]  ← EC2 servers, containers, SmartFox
    │                    (private; accessible from public layer only)
    ▼
[ Data Layer ]  ← Databases (MySQL), Cache (Redis)
                  (isolated; accessible from application layer only)
                  (no route to internet, incoming or outgoing)
```

Database subnets must have no route to the internet, incoming or outgoing.

### 5.2 Security Groups / Firewall Rules

Apply the principle of least privilege to network rules:

- Only open ports that are explicitly required.  
- Document the purpose of every firewall rule.  
- Database rules must only allow connections from application-tier IPs/groups — never from `0.0.0.0/0`. 
- Regularly audit rules for stale, overly permissive entries.

### 5.3 Encryption in Transit

All external traffic must use TLS 1.2 or higher. TLS 1.0 and 1.1 must be disabled everywhere. Internal service-to-service HTTP traffic must also use TLS where feasible. SmartFox connections from clients must use WSS (WebSocket Secure / TLS).

### 5.4 Web Application Firewall (WAF)

A WAF must be attached to all public-facing load balancers. At minimum, enable: managed core rule sets (protection against OWASP Top 10), rate limiting rules (per-IP and per-player-ID), and bot control rules. WAF logs must be shipped to the observability platform.

### 5.5 Network and Transport Vulnerabilities

| Vulnerability | What It Looks Like in Our Environment | Required Controls |
|:--------------|:--------------------------------------|:------------------|
| **DDoS (volumetric)** | Large traffic floods saturate ALB, NLB, or upstream bandwidth and make the service unavailable | Use AWS Shield protections, autoscaling where applicable, and traffic-aware alerting |
| **DDoS (application layer / L7)** | Attackers target expensive HTTP endpoints such as login, room join, or reward claim flows | Use WAF rate-based rules, caching where safe, and endpoint-specific throttling |
| **DNS hijacking** | DNS records are altered so players or operators are redirected to attacker-controlled endpoints | Use Route 53 protections, strong change control, and alerting on unexpected DNS modifications |
| **TLS downgrade / weak transport policy** | A client or proxy is allowed to negotiate insecure transport settings | Enforce modern TLS minimums on all public and internal entry points; do not allow insecure fallback |
| **Cleartext internal or real-time traffic** | Service-to-service traffic or SmartFox transport can be observed or modified on an untrusted path | Encrypt traffic in transit, including internal service calls and SmartFox connectivity where applicable |
| **Exposed admin endpoints** | Internal operator endpoints, dashboards, or maintenance APIs are reachable from the public internet | Keep admin surfaces private; require RBAC and controlled network access such as VPN, SSM, or equivalent approved access paths |

---

## 6. Secrets Management in Cloud

This section implements [ESTD1 §19. Secrets Management](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#19-secrets-management) at the cloud level.

### 6.1 Cloud-Native Secrets Manager

All application secrets must be stored in the cloud provider's secrets management service (AWS Secrets Manager for this project). Secrets must be:

- Organized by environment and service: `{env}/{service-name}/{secret-name}`  
- Example: `production/php-api/db-password`, `staging/reward-service/payment-api-key`
- Accessible only to the specific service that needs them, via the service's IAM role.  
- Configured for automatic rotation where the secrets manager supports it.

### 6.2 Secret Access Pattern

Applications must retrieve secrets at startup using the cloud SDK (using the instance's IAM role — no hardcoded access keys). Cache secrets in application memory for a reasonable period (1 hour) to avoid API call costs. Refresh the cache before the cached value might become stale.

### 6.3 Migration from Environment Variables

Procedure for migrating existing env-var-based secrets:

1. Create the secret in the secrets manager.  
2. Update the application to read from the secrets manager first, falling back to the env var.  
3. Validate in dev, qa, then staging.  
4. Deploy to production.  
5. Remove the environment variable from all deployment configs and documentation.

---

## 7. Compute: Sizing, Scaling, and Cost

### 7.1 Right-Sizing Principle

Do not over-provision "just to be safe." Over-provisioning wastes money and builds false confidence. Instead:

- Start with a smaller instance type than you think you need.  
- Measure actual CPU, memory, and network utilization under realistic load (load test).  
- Scale up to the minimum size that keeps utilization between 40–70% under normal load.  
- Review sizing quarterly and adjust based on actual metrics.

### 7.2 Horizontal vs. Vertical Scaling

```
Horizontal Scaling (adding more instances)   Vertical Scaling (larger instance)
──────────────────────────────────────────   ───────────────────────────────────
PHP API / Java microservices                 SmartFox (stateful; hard to scale out)
Preferred for stateless services             Acceptable for stateful services
Zero downtime — add instances while live     Requires restart to resize
No single instance is a SPOF                 Single instance remains a SPOF
Naturally resilient to instance failure      Requires separate HA strategy
```

Use **horizontal scaling** for the stateless PHP API and Java microservices with Auto Scaling Groups. Use vertical scaling with redundancy (multiple instances with room affinity routing) for SmartFox.

### 7.3 Auto Scaling for Stateless Services

Auto Scaling must be configured for all stateless API servers. Configuration principles (see [ESTD8](./ESTD8_-_AWS_Standards.md#estd8---aws-standards-document-for-bingo-game-infrastructure) for specific values):

- **Minimum:** Enough instances to handle 50% of expected peak load, distributed across at least 2 availability zones.  
- **Maximum:** Enough instances to handle 3× peak load (including content reset spikes).  
- **Scale-out trigger:** CPU utilization or request queue depth crossing a threshold. 
- **Scale-in protection:** During and immediately after a content reset, disable scale-in for 30 minutes to prevent the ASG from removing instances during a traffic spike.

### 7.4 Scheduled Scaling for Known Traffic Patterns

Content resets generate predictable traffic spikes. Pre-scale compute resources before the reset starts, not after the spike is detected. Schedule a scaling action to increase minimum capacity 15-30 minutes before any scheduled content reset window.

---

## 8. Deployment Pipelines

### 8.1 CI/CD Is Mandatory

All code deployments to any environment above dev must go through an automated CI/CD pipeline. No manual deployments except in documented emergency procedures (and even then, every manual action must be logged).

### 8.2 Pipeline Structure

```
Commit push
    │
    ▼
Static analysis (lint, Static Application Security Testing (SAST), dependency scan)
    │
    ▼
Unit tests + integration tests
    │
    ▼
Build artifact (Docker image / deployment package)
    │
    ▼
Deploy to dev (automatic on commit to feature branch)
    │
    ▼
Deploy to QA (automatic on merge to main / release branch)
    │
    ▼
Integration + regression tests on QA
    │
    ▼
Manual gate: QA sign-off
    │
    ▼
Deploy to staging (automatic after QA sign-off)
    │
    ▼
Load test + smoke test on staging
    │
    ▼
Manual gate: Architect approval
    │
    ▼
Deploy to production (scheduled, with monitoring)
    │
    ▼
Automated smoke tests + 15-minute monitoring watch period
```

### 8.3 Deployment Strategies

| Strategy | Use For | Description | 
|:---------|:--------|:------------|
| **Rolling** | Routine PHP API / Java microservice releases | Replace a batch of instances at a time; maintains capacity throughout |
| **Blue/Green** | High-risk releases (schema changes, major features) | Spin up entirely new fleet, shift traffic, keep old fleet for rapid rollback |
| **Canary** | Performance-sensitive changes | Route 5% of traffic to new version, monitor, then expand |
| **Maintenance window** | SmartFox deploys | Drain active rooms, take server offline, deploy, restart, monitor reconnects |

### 8.4 Deployment Safety Rules

- **Never deploy on Fridays after 3 PM IST** (approaches US peak hours — players waking up).  
- **Never deploy within 30 minutes of a scheduled content reset or launch.**
- Every production deployment must have a documented rollback plan before it begins. 
- Define rollback triggers before deploying: "If error rate > 2% or p95 > 1 second within 15 minutes, rollback immediately."

### 8.5 Jenkins for Client and Web Tool Builds

Unity client builds (iOS, Android, WebGL) and internal web tool builds are automated using Jenkins. Jenkins is not used for SEAM microservice or PHP API pipelines (which use AWS CodePipeline — [ESTD8 §13. AWS CodePipeline and CI/CD](./ESTD8_-_AWS_Standards.md#13-aws-codepipeline-and-cicd)). See [ESTD13](./ESTD13_-_Jenkins_CI_CD_Standards.md#estd13--jenkins-cicd-standards-for-unity-and-web-tool-builds) for the full Jenkins standards covering agent topology, Jenkinsfile authoring, build promotion, credential management, and artifact storage.

The Jenkins build promotion flow aligns with the environment promotion policy in [§3.3 Build Promotion Policy](#33-build-promotion-policy):

```
Git push → Jenkins PR Build (lint + test)
         → Auto-deploy to Dev
         → Manual gate → QA
         → Manual gate + Architect approval → Staging
         → Manual gate + Director approval → Production
```

### 8.6 CI/CD and Supply Chain Vulnerabilities

| Vulnerability | What It Looks Like in Our Environment | Required Controls |
|:--------------|:--------------------------------------|:------------------|
| **Hardcoded pipeline secrets / secret leakage in logs** | Jenkinsfiles, shell steps, build scripts, or pipeline logs reveal credentials or signing material | Use approved credential stores and masking; never echo secrets; keep pipeline code free of literal secrets |
| **Overprivileged CI agents or deploy roles** | Build nodes or deployment jobs can access systems far beyond the scope of the build they run | Scope agent credentials tightly; separate build, signing, and deploy privileges; review CI RBAC regularly |
| **Dependency CVEs / compromised packages / unsafe plugins** | Unity packages, Composer packages, Maven dependencies, npm packages, or Jenkins plugins introduce exploitable code | Pin dependencies intentionally, generate BOMs, scan dependencies and plugins, and patch high-severity issues promptly |
| **Artifact tampering or non-promoted deploys** | A different artifact is deployed to production than the one validated in earlier environments | Promote the exact same immutable artifact through environments; do not rebuild between promotion stages |
| **Build-script injection / unsafe shell execution** | Pipeline parameters or scripts are executed without validation and allow unintended command execution | Validate pipeline parameters, prefer checked-in scripts over ad-hoc shell, and keep Jenkinsfiles orchestration-only |
| **Unsigned or weakly tracked release outputs** | Teams cannot prove what code and dependencies produced a given build | Require build identity, artifact metadata, retention discipline, and BOM generation for release artifacts |

---

## 9. Observability in the Cloud

### 9.1 Observability Stack

All cloud infrastructure must support three pillars of observability:

| Pillar | Implementation |
|:-------|:---------------|
| **Logs** | Centralized log aggregation (CloudWatch Logs → Datadog) |
| **Metrics** | Cloud metrics + custom application metrics (Datadog) |
| **Traces** | Distributed tracing across services (Datadog APM) |

### 9.2 Universal Tagging

Every cloud resource must be tagged with a consistent set of tags. Tags enable cost allocation, automated compliance checks, and filtered monitoring dashboards.

| Tag Key | Example Values | Purpose |
|:--------|:---------------|:--------|
| `Project` | `BingoBash`, `BashForward` | Which game |
| `Environment` | `production`, `staging`, `qa`, `dev` | Cost isolation |
| `Service` | `php-api`, `reward-service`, `live-server` | Which component |
| `Owner` | `server-team`, `client-team` | Responsibility |
| `ManagedBy` | `terraform`, `manual` | IaC provenance |
| `CostCenter` | `engineering`, `ai` | Finance allocation |

Untagged resources must be automatically flagged and remediated within 48 hours.

### 9.3 Standard Operational Dashboards

Maintain and keep current:

- **Operations Overview:** Real-time active players, room count, API error rate, latency p95  
- **Infrastructure Health:** Compute CPU/memory, DB metrics, cache hit rate, load balancer metrics  
- **Content Reset Dashboard:** Used during reset windows to monitor reset job progress and traffic patterns  
- **Cost Dashboard:** Daily spend by environment and component

---

## 10. Data Storage Standards

### 10.1 Encryption at Rest

All data at rest must be encrypted: relational databases (MySQL on RDS), object storage (S3), block storage (EBS), and cache (Redis/ElastiCache). Use cloud-provider managed keys as a minimum; use customer-managed keys for sensitive player data.

### 10.2 Database High Availability

Production databases must use the cloud provider's high-availability features (Multi-AZ deployment for RDS primary instances; read replicas where read scale or reporting isolation is required). A single-node production database is not acceptable.

### 10.3 Backup Requirements

| Resource | Minimum Backup Frequency | Minimum Retention | Restore Test Frequency |
|:---------|:-------------------------|:------------------|:-----------------------|
| MySQL (RDS) | Daily automated backup | 14 days | Monthly |
| Redis / ElastiCache | Daily snapshot | 3 days | Quarterly |
| S3 assets | Versioning enabled | 90 days (versions) | Quarterly |
| Configuration | Git (IaC) | Indefinite | At every deployment |

### 10.4 S3 / Object Storage

- Enable versioning on all buckets that store game assets and player data exports.  
- Enable server-side encryption on all buckets.  
- Block all public access unless the bucket explicitly serves as a public CDN source. 
- Apply lifecycle policies to transition infrequently accessed objects to lower-cost storage tiers and expire old versions.

---

## 11. Backup, Recovery, and Resilience

### 11.1 Multi-Availability Zone Deployment

All production services must be deployed across a minimum of two availability zones. Single-AZ production deployments are prohibited. This provides resilience against the full loss of a single data center.

### 11.2 Restore Testing

A backup that has never been tested is not a backup — it is a hope. Restore tests must be conducted on a schedule. A successful restore test means: the restore procedure was executed end-to-end, the restored data was verified for integrity, and the procedure was documented with the time it took.

### 11.3 Runbooks for Recovery

Every CRITICAL cloud alarm must have a linked runbook. The runbook must document: what the alarm indicates, what to check immediately, step-by-step recovery procedure, expected recovery time, and escalation path if the runbook fails.

---

## 12. Cost Management

### 12.1 Cost Awareness Is Everyone's Responsibility

Every engineer who provisions or configures cloud resources is responsible for understanding the cost impact of their choices. Over-provisioned instances, unattached storage volumes, forgotten test resources, and unbounded data transfer all add up.

### 12.2 Monthly Cost Review

A monthly cloud cost review must be conducted by the team. The review covers: actual spend vs. budget by environment and component, identification of cost anomalies, right-sizing opportunities, and savings plan coverage gaps.

### 12.3 Reserved Capacity for Predictable Workloads

Baseline compute capacity that runs 24/7 (the PHP API minimum instances, the SmartFox server) should be covered by reserved capacity (Reserved Instances or Savings Plans). Variable/burst capacity uses on-demand pricing. This typically saves 30–50% on baseline compute costs.

### 12.4 Cost Anomaly Detection

Configure automated cost anomaly detection on the cloud provider's billing system. Set a budget alert to trigger when daily spend deviates significantly from the baseline. Do not wait until the end of the month to discover a runaway cost.

---

## 13. Compliance and Data Residency

- Player data must remain in the cloud region(s) configured for the specific game. For the US player base, all primary data must reside in a US region.  
- Cross-region data replication for disaster recovery must comply with data residency requirements.  
- GDPR/CCPA data deletion and export requests must be operable across all cloud storage types.  
- Log data that contains PII must be configured with the appropriate retention policy and masking.

---

## 14. Common Pitfalls to Avoid

| # | Pitfall | Impact | Prevention | 
|:--|:--------|:-------|:-----------|
| 1 | Manual resource creation (ClickOps) | Undocumented, unrepeatable, audit-invisible | Enforce IaC; detect drift in CI |
| 2 | All environments in one cloud account | Dev mistake can affect production | Separate accounts per environment |
| 3 | Over-provisioned "to be safe" | Unnecessary cloud spend | Right-size; use auto-scaling |
| 4 | No deployment rollback plan | Stuck with broken code in production | Define rollback trigger before deploying |
| 5 | Single-AZ production deployment | One AZ failure = full outage | Mandatory multi-AZ in production |
| 6 | Backup never tested | Backup exists but cannot be restored during an incident | Monthly restore drill |
| 7 | Deploying during content reset window | Deploying into a traffic spike | Deployment blackout window enforced in pipeline |
| 8 | No cost anomaly alerts | Bill shock at month end | Automated daily cost alerts |
| 9 | Wildcard IAM permissions | Over-privileged service can access resources it shouldn't | Least privilege; quarterly permission review |
| 10 | Skipping environments in promotion | "Works on my machine" production failure | Build promotion policy enforced in CI/CD |


