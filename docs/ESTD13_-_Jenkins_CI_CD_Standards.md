# ESTD13 — Jenkins CI/CD Standards for Unity and Web Tool Builds

**ESTD13 — Jenkins CI/CD Standards**

| Field | Value |
|:----- |:----- |
| **Document ID** | ESTD13 |
| **Version** | 5.0 |
| **Status** | Active |
| **Last Updated** | 2026-04-13 |
| **Applies To** | All engineers who author, modify, or trigger Jenkins pipelines (client builds, web tool builds, SmartFox builds) |
| **Depends On** | [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers), [ESTD5](./ESTD5_-_Cloud_Engg_Standards.md#estd5---cloud-engineering-standards-and-best-practices-for-infrastructure-management), [ESTD8](./ESTD8_-_AWS_Standards.md#estd8---aws-standards-document-for-bingo-game-infrastructure), [ESTD11](./ESTD11_-_Web_Development_and_Deployment_Standards.md#estd11--web-tools-creation-and-deployment-standards) |
| **Approval** | Director of Engineering |

---

**📋 Living Document Notice** This document is a work in progress and will evolve as our systems, practices, and understanding mature. Feedback, questions, and suggestions are welcome — please submit them via comments on the corresponding Confluence page. However, the standards defined herein **must be strictly followed** in all active work. Any exception requires **explicit written approval** from the Director of Engineering or the appropriate Architect, and must be documented in the PR description, the exception log, or the relevant Confluence page.

---

## How to Use This Document

ESTD13 defines how Jenkins is used to build, test, sign, archive, and promote artifacts for the Unity clients, internal web tools, and SmartFox extension packages. It builds on the environment strategy in [ESTD5 §3. Environment Strategy](./ESTD5_-_Cloud_Engg_Standards.md#3-environment-strategy) and the build-promotion policy in [ESTD1 §13.5 Content Reset Cadence](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#135-content-reset-cadence). Read [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers) and [ESTD5](./ESTD5_-_Cloud_Engg_Standards.md#estd5---cloud-engineering-standards-and-best-practices-for-infrastructure-management) first.

Server-side deployment pipelines for the PHP monolith and Java/SEAM microservices remain in [ESTD8 §13. AWS CodePipeline and CI/CD](./ESTD8_-_AWS_Standards.md#13-aws-codepipeline-and-cicd). SmartFox room-drain and runtime restart procedures remain in [ESTD12](./ESTD12_-_Smartfox_Server_Standards.md#estd12--smartfox-server-standards-for-bingo-game-development); ESTD13 covers the Jenkins build/package side only.

## Table of Contents

- [ESTD13 — Jenkins CI/CD Standards for Unity and Web Tool Builds](#estd13--jenkins-cicd-standards-for-unity-and-web-tool-builds)
  - [How to Use This Document](#how-to-use-this-document)
  - [Table of Contents](#table-of-contents)
  - [1. Purpose and Scope](#1-purpose-and-scope)
  - [2. Why Jenkins Is Used Here](#2-why-jenkins-is-used-here)
  - [3. Jenkins Architecture and Infrastructure](#3-jenkins-architecture-and-infrastructure)
    - [3.1 Controller and Agent Topology](#31-controller-and-agent-topology)
    - [3.2 Mandatory Architecture Rules](#32-mandatory-architecture-rules)
    - [3.3 Agent Capability Labels](#33-agent-capability-labels)
  - [4. Pipeline-as-Code Standards](#4-pipeline-as-code-standards)
    - [4.1 Declarative Pipeline Is Required](#41-declarative-pipeline-is-required)
    - [4.2 Jenkinsfile Location and Source of Truth](#42-jenkinsfile-location-and-source-of-truth)
    - [4.3 Shared Libraries Are Mandatory](#43-shared-libraries-are-mandatory)
    - [4.4 Jenkinsfiles Orchestrate; They Do Not Implement Business Logic](#44-jenkinsfiles-orchestrate-they-do-not-implement-business-logic)
    - [4.5 Required Pipeline Options](#45-required-pipeline-options)
    - [4.6 Parameter Validation Is Mandatory](#46-parameter-validation-is-mandatory)
    - [4.7 Stage Naming Convention](#47-stage-naming-convention)
    - [4.8 Post-Build Actions](#48-post-build-actions)
    - [4.9 Example Pipeline Skeleton](#49-example-pipeline-skeleton)
  - [5. Secret and Credential Management](#5-secret-and-credential-management)
    - [5.1 No Secrets in Jenkinsfiles or Repository Files](#51-no-secrets-in-jenkinsfiles-or-repository-files)
    - [5.2 Approved Storage and Access Patterns](#52-approved-storage-and-access-patterns)
    - [5.3 Credential Naming Convention](#53-credential-naming-convention)
    - [5.4 Credentials Must Not Be Echoed](#54-credentials-must-not-be-echoed)
  - [6. Build Artifact Standards](#6-build-artifact-standards)
    - [6.1 Artifact Storage](#61-artifact-storage)
    - [6.2 Versioning and Build Identity](#62-versioning-and-build-identity)
    - [6.3 Build Metadata](#63-build-metadata)
    - [6.4 Artifact Retention](#64-artifact-retention)
    - [6.5 Artifact Immutability](#65-artifact-immutability)
  - [7. Unity Client and SmartFox Build Pipelines](#7-unity-client-and-smartfox-build-pipelines)
    - [7.1 Standard Unity Pipeline Flow](#71-standard-unity-pipeline-flow)
    - [7.2 Unity Build Configurations](#72-unity-build-configurations)
    - [7.3 Agent and Tooling Requirements](#73-agent-and-tooling-requirements)
    - [7.4 Unity License Management](#74-unity-license-management)
    - [7.5 Unity Build Command Standard](#75-unity-build-command-standard)
    - [7.6 Validation, Tests, and Coverage](#76-validation-tests-and-coverage)
    - [7.7 Signing](#77-signing)
    - [7.8 BOM Generation and Vulnerability Scanning](#78-bom-generation-and-vulnerability-scanning)
    - [7.9 SmartFox Build Pipelines](#79-smartfox-build-pipelines)
  - [8. Web Tools Build Pipelines](#8-web-tools-build-pipelines)
    - [8.1 Standard Web Tool Pipeline Flow](#81-standard-web-tool-pipeline-flow)
    - [8.2 `npm ci` Is Mandatory](#82-npm-ci-is-mandatory)
    - [8.3 Minimum Validate/Test/Build Steps](#83-minimum-validatetestbuild-steps)
    - [8.4 Coverage and Bundle Size Checks](#84-coverage-and-bundle-size-checks)
    - [8.5 Test Results Must Be Published](#85-test-results-must-be-published)
    - [8.6 Environment Configuration Injection](#86-environment-configuration-injection)
    - [8.7 BOM Scan for Web Tools](#87-bom-scan-for-web-tools)
  - [9. Environment Promotion and Deployment Gates](#9-environment-promotion-and-deployment-gates)
    - [9.1 Core Rule: Promote the Same Artifact](#91-core-rule-promote-the-same-artifact)
    - [9.2 Promotion Flow](#92-promotion-flow)
    - [9.3 Approval Gates](#93-approval-gates)
    - [9.4 Promotion Job Inputs](#94-promotion-job-inputs)
    - [9.5 No Direct Production Deploys](#95-no-direct-production-deploys)
    - [9.6 Example Promotion Record](#96-example-promotion-record)
  - [10. Branch and Trigger Rules](#10-branch-and-trigger-rules)
  - [11. Notifications and Alerting](#11-notifications-and-alerting)
    - [11.1 Minimum Notification Routing](#111-minimum-notification-routing)
    - [11.2 Notification Content](#112-notification-content)
    - [11.3 Timeout and Consecutive-Failure Escalation](#113-timeout-and-consecutive-failure-escalation)
  - [12. Jenkins Agent and Node Standards](#12-jenkins-agent-and-node-standards)
    - [12.1 Workspace Isolation](#121-workspace-isolation)
    - [12.2 Disk and Resource Monitoring](#122-disk-and-resource-monitoring)
    - [12.3 No Privileged Drift](#123-no-privileged-drift)
  - [13. Plugin and Controller Configuration](#13-plugin-and-controller-configuration)
    - [13.1 Approved Plugins Only](#131-approved-plugins-only)
    - [13.2 Jenkins Configuration as Code](#132-jenkins-configuration-as-code)
    - [13.3 Plugin Update Policy](#133-plugin-update-policy)
  - [14. Pipeline Security and RBAC](#14-pipeline-security-and-rbac)
    - [14.1 Groovy Sandbox and Script Security](#141-groovy-sandbox-and-script-security)
    - [14.2 Restricting Pipeline Mutation](#142-restricting-pipeline-mutation)
    - [14.3 Approval RBAC](#143-approval-rbac)
    - [14.4 Audit Logging](#144-audit-logging)
  - [15. Maintenance and Hygiene](#15-maintenance-and-hygiene)
    - [15.1 Code Hygiene](#151-code-hygiene)
    - [15.2 Operational Maintenance Cadence](#152-operational-maintenance-cadence)
    - [15.3 Job Naming](#153-job-naming)
  - [16. Common Pitfalls to Avoid](#16-common-pitfalls-to-avoid)
  - [17. Implementation Checklist](#17-implementation-checklist)

---

## 1. Purpose and Scope

Jenkins is the CI/CD platform for Unity client builds (iOS, Android, Facebook/WebGL, and any standalone client builds where needed), for internal web tool builds (for example, Next.js/React or TypeScript-based tools), and for SmartFox extension/package builds. Jenkins is also permitted for supporting automation in the server domain such as static analysis, integration-test runners, and deployment-coordination scripts, but it is **not** the primary deployment pipeline for the PHP monolith or Java/SEAM microservices.

For the SmartFox-backed real-time Bingo product, this section governs the client and internal-tool side of delivery and the operational rules for creating and maintaining Jenkins pipelines. It covers:

- all `Jenkinsfile` definitions in any repository;  
- Jenkins shared libraries;  
- Jenkins controller and agent configuration;  
- credentials, secrets, and signing materials used by Jenkins;  
- artifact creation, storage, versioning, retention, and promotion;  
- Unity build pipelines, web tool build pipelines, SmartFox build/package pipelines, notifications, approvals, and pipeline security.

---

## 2. Why Jenkins Is Used Here

Jenkins is used for client and web tool pipelines because those workloads have platform, tooling, and licensing constraints that benefit from a managed agent fleet under direct engineering control:

- Unity builds require pinned editor versions, platform SDKs, and, in some cases, license activation/deactivation workflows.  
- iOS builds require macOS agents with pinned Xcode versions and signing material handling.  
- Android and WebGL builds benefit from dedicated Linux agents or containerized build environments.  
- Internal web tools can use the same promotion and control model as the client pipelines, which keeps release discipline consistent across the product.

The standard intent is operational consistency: the same platform runs client builds, tool builds, promotion jobs, artifact publication, and release notifications, while server-side delivery remains on its own dedicated pipeline.

---

## 3. Jenkins Architecture and Infrastructure

### 3.1 Controller and Agent Topology

A reference topology is shown below. Exact instance types may change, but the role separation must not.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ Jenkins Controller                                                           │
│  - Schedules pipelines                                                       │
│  - Stores pipeline state                                                     │
│  - Manages credentials / RBAC / audit                                        │
│  - Archives artifacts to S3                                                  │
│  - Sends notifications                                                       │
│  - Runs NO build executors                                                   │
├──────────────────────────────────────────────────────────────────────────────┤
│ macOS Agent Pool                  Linux Agent Pool          Optional Windows │
│ - Unity Editor (pinned)           - Unity headless         - Standalone      │
│ - Xcode (pinned)                  - Android SDK / NDK        client builds   │
│ - iOS signing workflow            - Node.js 20+                              │
│ - Unity licence handling          - Docker                                   │
│                                   - AWS CLI / Trivy / npm or pnpm            │
│                                   - General scripted tasks                   │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Mandatory Architecture Rules

1. The Jenkins controller must **never** run builds directly. It is reserved for scheduling, coordination, credentials, audit, and controller services only.  
2. The controller and agents must run in private network space and must not be publicly reachable from the internet. Access is via approved internal access paths such as the corporate VPN or equivalent.  
3. Agents must be created and managed through infrastructure as code. No manually created or hand-tuned “special snowflake” agent is allowed.  
4. No agent may hold long-lived production AWS credentials. Deployment credentials are injected per stage and, where possible, assumed temporarily via IAM role.  
5. Linux build environments should run inside versioned Docker images committed to the build-infrastructure repository. macOS agents must use pinned macOS and Xcode versions.  
6. macOS build agents used for iOS signing or restricted release workflows must not have unrestricted internet access during the build; signing and distribution steps must use only the approved, pre-authenticated channels required for the release path.

### 3.3 Agent Capability Labels

Each agent must advertise a capability label and every pipeline must request a specific label. `agent any` is prohibited.

| Label | Minimum Capability |
| :---- | :---- |
| `unity-build-agent` | Unity Editor, Android SDK/NDK, IL2CPP, and—where applicable—Xcode on macOS |
| `linux-unity` | Unity headless build support, Android SDK, CLI tooling |
| `web-tools-agent` | Node.js 20+, Docker, AWS CLI, test toolchain |
| `general-agent` | AWS CLI, Terraform, Python, general scripting utilities |
| `windows-unity` | Windows-only client or standalone build support when required |

---

## 4. Pipeline-as-Code Standards

### 4.1 Declarative Pipeline Is Required

All new pipelines must use **Declarative Pipeline** syntax. Scripted Pipeline syntax is prohibited for new work and must be migrated when a pipeline is materially refactored.

Use `agent none` at pipeline level when different stages require different agent types. A single, pipeline-level labeled agent is acceptable when the entire pipeline genuinely runs on one capability-specific agent. In all cases, use a concrete label, never `any`.

### 4.2 Jenkinsfile Location and Source of Truth

The primary `Jenkinsfile` must live at the repository root. Variant pipelines may exist in subdirectories such as `jenkins/Jenkinsfile.android` or `jenkins/Jenkinsfile.ios`, but the repository must still have a clearly discoverable primary pipeline entrypoint.

Pipelines configured only in the Jenkins UI, without a committed `Jenkinsfile`, are prohibited.

### 4.3 Shared Libraries Are Mandatory

Reusable pipeline logic must be centralized in the Jenkins shared library rather than duplicated across repositories. This includes, at minimum:

- S3 artifact upload and retrieval  
- Slack / chat notifications  
- build metadata generation  
- version derivation  
- BOM generation and vulnerability scan helpers  
- signing helpers  
- promotion and release-audit helpers

Depending on repository layout, the shared library may live in `bingo-jenkins-shared-lib` / `jenkins-shared-library`, but the rule is the same: no copy-pasted pipeline logic.

### 4.4 Jenkinsfiles Orchestrate; They Do Not Implement Business Logic

Jenkinsfiles are production code, but their role is orchestration. They must not contain complex business logic, data processing, or opaque Groovy-heavy implementations that cannot be tested independently. Non-trivial logic belongs in:

- shared library functions;  
- repository scripts (shell, Python, C# build scripts, etc.);  
- testable helper tools committed alongside the code they support.

### 4.5 Required Pipeline Options

Every Jenkins pipeline must define timeouts, retention, and workspace/concurrency behavior. Minimum standard:

| Option | Standard |
| :---- | :---- |
| `timeout` | Unity builds: ≤ 120 minutes; web tool builds: ≤ 30 minutes; lower limits encouraged when practical |
| `buildDiscarder` | Keep at least the last 30 builds |
| `timestamps()` | Mandatory on all pipelines |
| `disableConcurrentBuilds()` | Required for Unity pipelines; default for other pipelines unless safe concurrency is explicitly justified |
| workspace cleanup | `cleanWs()` in `post { always { ... } }` |

### 4.6 Parameter Validation Is Mandatory

Any user-supplied build parameter must be validated before it is passed to a shell command, external tool, or shared-library function that could execute side effects.

```
def allowedPlatforms = ['android', 'ios', 'webgl']
if (!allowedPlatforms.contains(params.PLATFORM)) {
    error("Invalid PLATFORM: ${params.PLATFORM}")
}
```

### 4.7 Stage Naming Convention

Stage names must be descriptive, stable, and readable in Jenkins UI views such as Blue Ocean or equivalent stage visualizations. Preferred standard vocabulary:

```
Checkout
Resolve Dependencies
Validate
Lint
Unit Tests
Build (Platform Variant)
Sign
BOM Scan
Archive Artifact
Deploy to <ENV>
Smoke Test
Notify
```

Names such as `Stage 1`, `Build Stuff`, or `My Stage` are prohibited.

### 4.8 Post-Build Actions

Every pipeline must define `post` actions for success, failure, and always. At minimum:

- notify on success and failure;  
- archive relevant logs on failure;  
- clean the workspace in `always`;  
- return any checked-out Unity license in `always` if the pipeline activated one.

### 4.9 Example Pipeline Skeleton

```
@Library('bingo-jenkins-shared-lib') _

pipeline {
    agent none

    options {
        timeout(time: 60, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '30'))
        disableConcurrentBuilds()
        timestamps()
    }

    parameters {
        choice(name: 'TARGET_ENV', choices: ['dev', 'qa', 'staging', 'production'],
               description: 'Promotion target')
    }

    stages {
        stage('Checkout') {
            agent { label 'general-agent' }
            steps { checkout scm }
        }

        stage('Build Android') {
            agent { label 'unity-build-agent' }
            steps {
                script {
                    sharedLib.buildUnityAndroid(targetEnv: params.TARGET_ENV)
                }
            }
        }
    }

    post {
        success {
            script { sharedLib.notifySlack(channel: '#builds-client', status: 'success') }
        }
        failure {
            archiveArtifacts artifacts: 'build/**/*.log', allowEmptyArchive: true
            script { sharedLib.notifySlack(channel: '#builds-client', status: 'failure') }
        }
        always {
            cleanWs()
        }
    }
}
```

---

## 5. Secret and Credential Management

### 5.1 No Secrets in Jenkinsfiles or Repository Files

Secrets must never be hard-coded in a `Jenkinsfile`, shared-library source, repository config, or checked-in environment file. This includes:

- API keys  
- signing certificates and provisioning profiles  
- Unity license files  
- passwords or tokens  
- AWS credentials  
- webhook URLs  
- App Store / Play Store credentials

### 5.2 Approved Storage and Access Patterns

| Credential Type | Approved Storage | Access Pattern |
| :---- | :---- | :---- |
| Unity licence file | Jenkins Credentials Manager (Secret File) | `withCredentials([file(...)])` |
| Slack webhook / tokens | Jenkins Credentials (Secret Text) | `withCredentials([string(...)])` |
| Android keystore / signing materials | Jenkins Credentials or AWS Secrets Manager via Jenkins binding | `withCredentials(...)` |
| iOS certificates / profiles | Jenkins Credentials + macOS Keychain workflow | injected per build |
| AWS deployment access | IAM role assumption / AWS credential binding | temporary per stage |
| Third-party distribution or store keys | Jenkins Credentials / AWS Secrets Manager | temporary runtime injection |

### 5.3 Credential Naming Convention

Credential IDs must follow a consistent pattern:

```
<domain>-<purpose>-<type>

Examples:
apple-connect-api-key
google-play-service-account
aws-deploy-role-arn
firebase-crashlytics-token
unity-license-ulf
slack-webhook-builds
```

### 5.4 Credentials Must Not Be Echoed

Pipelines must not print secrets to logs. Jenkins masking helps, but shell usage can still leak values if written carelessly. Disable shell echo where needed and avoid interpolating secret-bearing variables into verbose command lines.

```
withCredentials([string(credentialsId: 'apple-connect-api-key', variable: 'APPLE_KEY')]) {
    sh '''
        set +x
        echo "$APPLE_KEY" | some-command --password-stdin
    '''
}
```

---

## 6. Build Artifact Standards

### 6.1 Artifact Storage

All successful builds that are intended to be shared, tested, promoted, or audited must upload their artifacts to the designated S3 artifact bucket immediately after the build completes. Artifacts must never exist only in the agent workspace.

Illustrative path layout:

```
s3://bingo-build-artifacts/
  unity-android/<buildId>/
  unity-ios/<buildId>/
  unity-webgl/<buildId>/
  web-tools/<tool-name>/<buildId>/
```

Each artifact folder must include, as applicable:

- the primary deliverable (`.aab`, `.apk`, `.ipa`, `.zip`, WebGL package, etc.);  
- `build-metadata.json`;  
- vulnerability/BOM outputs;  
- build logs needed for audit or incident review.

### 6.2 Versioning and Build Identity

The versioning standard is:

```
{YYYY}.{MM}.{patch}-build.{buildNumber}
Example: 2026.03.1-build.47
```

Where:

- `YYYY.MM` aligns with the release cadence;  
- `patch` captures hotfix or intra-cycle increment;  
- `buildNumber` is the monotonically increasing Jenkins build number.

This build identity must be:

- embedded into the artifact;  
- visible in the app or tool’s About/build info surface where applicable;  
- mapped to `CFBundleShortVersionString` / equivalent iOS fields and Android `versionName` / equivalent release metadata as appropriate.

A human-readable app version and a unique build number may also be stored separately inside metadata for audit clarity.

### 6.3 Build Metadata

Every artifact must include `build-metadata.json`. Minimum recommended shape:

```json
{
  "buildId": "2026.03.1-build.47",
  "buildNumber": "47",
  "appVersion": "2026.03.1",
  "gitCommitHash": "a4f9b21c3d",
  "gitBranch": "release/2026-03",
  "platform": "android",
  "buildConfig": "release",
  "unityVersion": "2022.3.18f1",
  "buildTimestamp": "2026-03-18T03:15:00Z",
  "builtBy": "jenkins-unity-build-agent-01",
  "jenkinsBuildUrl": "https://jenkins.internal/job/unity-android/47/",
  "promotion": {
    "approvedBy": null,
    "sourceEnv": null,
    "targetEnv": null,
    "ticket": null
  }
}
```

### 6.4 Artifact Retention

Retention must be enforced with S3 lifecycle policy, not manual clean-up. Combined minimum standard:

| Artifact Class | Minimum Retention |
| :---- | :---- |
| dev branch artifacts | 7 days |
| PR validation artifacts | 14 days |
| QA artifacts | 30 days minimum; 6 weeks preferred for release-candidate traceability |
| staging artifacts | 90 days / 3 months |
| production artifacts | 12 months / 1 year minimum |
| build logs | 3 months |

Production artifacts must additionally be protected from deletion using S3 versioning, object lock, or an equivalent guardrail that prevents accidental removal during the retention window.

### 6.5 Artifact Immutability

Uploaded artifacts must not be overwritten. If a build needs to be re-run, publish a new build number and a new immutable path. Promotion always moves or references the exact artifact that passed the prior gate; it never rebuilds.

---

## 7. Unity Client and SmartFox Build Pipelines

### 7.1 Standard Unity Pipeline Flow

```
Validate -> Test -> Build -> Sign -> BOM Scan -> Archive Artifact -> Distribute / Promote
```

### 7.2 Unity Build Configurations

| Environment | Runtime / Build Mode | Logging | Development Build | Code Stripping | Notes |
| :---- | :---- | :---- | :---- | :---- | :---- |
| `debug` / `dev` | Mono or equivalent debug-capable mode where permitted | DEBUG | Yes | No | Local/dev use only; do not treat as promotable release artifact |
| `qa` | IL2CPP release-style build | INFO | No | Minimal | QA validation build |
| `staging` | IL2CPP release-style build | WARN | No | Full | Staging validation build |
| `production` | IL2CPP release-style build | ERROR | No | Full | Store / production distribution |

Production-bound builds must never originate from an unauthorized branch type.

### 7.3 Agent and Tooling Requirements

- Unity version must be pinned and must match the project’s `ProjectVersion.txt`.  
- macOS agents are required for iOS archive/sign workflows.  
- Linux agents are suitable for Android, headless test, WebGL, and web-tool workloads where applicable.  
- Windows agents may be used only for explicitly required standalone/client targets.

### 7.4 Unity License Management

Unity license activation materials must be stored as Jenkins-managed credentials and activated only for the duration of the build. The license must always be returned in `post { always { ... } }`, even if the build fails.

```
stage('Activate Unity License') {
    steps {
        withCredentials([file(credentialsId: 'unity-license-ulf', variable: 'UNITY_LICENSE_FILE')]) {
            sh '''
                "$UNITY_EXECUTABLE" -batchmode -manualLicenseFile "$UNITY_LICENSE_FILE" -quit
            '''
        }
    }
}

post {
    always {
        sh '''
            "$UNITY_EXECUTABLE" -batchmode -returnlicense -quit || true
        '''
    }
}
```

### 7.5 Unity Build Command Standard

Unity builds must be driven from the CLI and must call a static C# build entry point in the `Editor` assembly. GUI-driven build procedures and ad hoc shell logic that duplicate build configuration are prohibited.

```
stage('Build Android AAB') {
    steps {
        sh '''
            "$UNITY_EXECUTABLE" \
              -batchmode \
              -quit \
              -nographics \
              -projectPath "$WORKSPACE" \
              -buildTarget Android \
              -executeMethod BuildAutomation.BuildAndroid \
              -buildConfig "$BUILD_CONFIG" \
              -buildVersion "$BUILD_ID" \
              -logFile "$WORKSPACE/build/unity-android.log"
        '''
    }
}
```

### 7.6 Validation, Tests, and Coverage

Minimum pre-build validation should include:

- project/settings consistency checks;  
- C# linting or analyzer pass where configured;  
- Unity Test Runner EditMode tests in headless mode where available.

Where the project has coverage instrumentation enabled, the minimum target is 80% for the defined test scope, consistent with the broader engineering baseline.

### 7.7 Signing

- iOS signing materials must be managed through Jenkins credentials and the approved keychain/profile workflow. Profiles must be rotated before expiry.  
- Android release signing materials must be retrieved through an approved secret workflow and used only within the signing step.  
- No signing credential may persist on the agent beyond the build.

### 7.8 BOM Generation and Vulnerability Scanning

After a successful build, generate a software bill of materials and perform a vulnerability scan before archiving or promoting the artifact.

```
stage('BOM Scan') {
    steps {
        sh 'dotnet cyclonedx ./ProjectSettings/packages-lock.json -o build/bom.json'
        sh 'trivy sbom build/bom.json --exit-code 1 --severity HIGH,CRITICAL'
    }
}
```

### 7.9 SmartFox Build Pipelines

SmartFox extension builds and packaging workflows also run in Jenkins. This section governs the **build/package** side only; room drain, restart, and runtime validation procedures remain in ESTD12.

Requirements:

- Pin the JDK version, SmartFox Server API dependency version, and any build plugin versions in source control.
- Produce an immutable extension artifact (`.jar` or approved package zip) per build; do not rebuild separately for QA, staging, and production.
- Run unit tests for room engine/domain logic plus any available protocol-contract or integration harness tests before archiving the artifact.
- Archive the extension artifact, dependency manifest/BOM, and build metadata together.
- Inject environment-specific configuration at deploy/promote time, not by baking secrets or endpoints into the artifact.
- Do not package the full SmartFox distribution in the pipeline artifact unless the pipeline explicitly exists to produce a controlled server image.

Standard SmartFox build flow:

```
Validate -> Unit Test -> Package Extension -> BOM Scan -> Archive Artifact -> Promote Same Artifact
```

---

## 8. Web Tools Build Pipelines

### 8.1 Standard Web Tool Pipeline Flow

```
Checkout -> Install Dependencies -> Validate -> Lint -> Unit Tests -> Build -> BOM Scan -> Archive Artifact -> Deploy / Promote
```

### 8.2 `npm ci` Is Mandatory

Web tool pipelines must use `npm ci` rather than `npm install` when the repository standard is npm. This ensures lockfile-faithful, reproducible builds. Equivalent lockfile-strict commands must be used if the repository standard is another package manager.

### 8.3 Minimum Validate/Test/Build Steps

A standard web tool pipeline must, as applicable, include:

- dependency install from lockfile;  
- ESLint / formatting verification;  
- TypeScript type-check (for TS projects);  
- unit tests;  
- production build/export;  
- bundle size guardrail where defined for the tool.

### 8.4 Coverage and Bundle Size Checks

Where test coverage is configured, the minimum target is 80%. For tools with browser-delivered bundles, define and enforce a maximum bundle-size threshold (for example, fail if the principal JS bundle exceeds the agreed threshold such as 500 KB, unless an approved exception exists).

### 8.5 Test Results Must Be Published

Unit test output must be published to Jenkins using `junit` or the approved equivalent so results remain visible and trendable in the Jenkins UI.

### 8.6 Environment Configuration Injection

Environment-specific API endpoints and runtime settings must be injected at build or deployment time through the approved credential/configuration path rather than hard-coded in source. Where the pipeline is promoting the same artifact through multiple environments, prefer runtime or promotion-time configuration over recompiling the tool for each environment.

```
stage('Build Web Tool') {
    environment {
        NEXT_PUBLIC_API_URL = credentials("tools-api-url-${params.TARGET_ENV}")
        NEXT_PUBLIC_ENV     = "${params.TARGET_ENV}"
    }
    steps {
        sh 'npm ci'
        sh 'npm run lint'
        sh 'npm run test:ci'
        sh 'npm run build'
    }
}
```

### 8.7 BOM Scan for Web Tools

Web tool builds must also generate and scan a BOM before archival or promotion.

```
stage('BOM Scan') {
    steps {
        sh 'npx @cyclonedx/cyclonedx-npm --output-format json --output-file build/bom.json'
        sh 'trivy sbom build/bom.json --exit-code 1 --severity HIGH,CRITICAL'
    }
}
```

---

## 9. Environment Promotion and Deployment Gates

### 9.1 Core Rule: Promote the Same Artifact

The same artifact that passed the earlier environment must be the one promoted to the next environment. QA, staging, and production do **not** rebuild the client or tool artifact.

### 9.2 Promotion Flow

```
Build once -> Publish to S3 -> Validate in Dev/QA -> Manual approval -> Promote same artifact -> Deploy
```

More explicitly:

```
1. Build artifact and assign buildId
2. Upload artifact + build-metadata.json to S3
3. Validate in lower environment
4. Approval gate is satisfied
5. Download exact buildId from S3
6. Verify checksum / identity
7. Publish to target environment location or trigger target deployment
8. Record who approved, what moved, and when
```

### 9.3 Approval Gates

The minimum gate model is:

| Environment Transition | Gate |
| :---- | :---- |
| build -> dev | automatic where branch policy allows |
| dev -> QA | manual gate; QA lead or designated approver |
| QA -> staging | manual gate; Architect approval |
| staging -> production | manual gate; Director of Engineering or delegate, plus stakeholder/release sign-off where required |

Production promotions must also respect blackout-window rules defined by the higher-level release standard.

### 9.4 Promotion Job Inputs

Production promotions must prompt for and record:

- release ticket / JIRA / equivalent change reference;  
- approver name;  
- optional release notes;  
- source environment and target environment;  
- buildId / artifact reference.

### 9.5 No Direct Production Deploys

No engineer may bypass the promotion pipeline and trigger a direct production deployment from a branch build. Production deployment jobs must only accept approved promotion outputs.

### 9.6 Example Promotion Record

```json
{
  "buildId": "2026.03.1-build.47",
  "sourceEnv": "qa",
  "targetEnv": "staging",
  "approvedBy": "Client Architect",
  "ticket": "BINGO-1427",
  "approvedAt": "2026-03-20T10:45:00Z",
  "artifactSha256": "8ad0...f31b"
}
```

---

## 10. Branch and Trigger Rules

| Branch Pattern | Typical Trigger | Allowed Artifact Destination | Notes |
| :---- | :---- | :---- | :---- |
| `feature/*`, `fix/*` | PR open / commit push | dev-only / scratch validation | not promotable beyond dev |
| `develop` | merge / scheduled validation | dev | continuous integration branch if used by the repo |
| `release/*` | PR open + nightly / manual | QA candidate | may advance after approval |
| `main` | protected merges and release tags | validation on `main`; only approved release tags may emit staging/production-promotable artifacts | promotion required for production |
| `hotfix/*` | manual + controlled PR flow | QA then fast-track staging/production per approval | Architect approval required |

Protection rules:

1. Production-bound builds may only originate from approved branch patterns such as `main` or `release/*`.  
2. A production-bound pipeline started from any other branch must fail immediately with a clear error.  
3. `hotfix/*` fast-track behavior requires explicit written Architect approval and must still record the release ticket and approver.

---

## 11. Notifications and Alerting

### 11.1 Minimum Notification Routing

| Situation | Minimum Destination |
| :---- | :---- |
| Unity build completion | `#builds-client` |
| Web tool build completion | `#builds-tools` |
| Production promotion / release | `#releases` and `#live-ops` |
| Release-blocking build failure or timeout | `#incidents` |
| PR build failure | notify the PR author directly, in addition to normal channel rules where configured |

Mainline integration branches such as `develop` or `main` should always notify on completion. PR/scratch builds may notify on failure only, provided that the responsible engineer is directly alerted. Teams that maintain umbrella status channels such as `#build-status` or release-alert channels such as `#build-alerts` may mirror notifications there, but those mirrors do not replace the required routing above.

### 11.2 Notification Content

Every build notification must include, at minimum:

- success/failure state;  
- job name;  
- buildId or app/tool version;  
- branch;  
- commit hash (short form acceptable);  
- build duration;  
- link to the Jenkins build;  
- on failure, a direct pointer to the failing stage or relevant logs.

### 11.3 Timeout and Consecutive-Failure Escalation

If a build exceeds its timeout:

- terminate it automatically;  
- mark it failed;  
- notify the incident channel if it affects release flow or shared build capacity.

If three consecutive builds fail on a primary integration branch, page the on-call engineer or the team’s defined escalation target.

---

## 12. Jenkins Agent and Node Standards

### 12.1 Workspace Isolation

Each build must run in a clean workspace. `cleanWs()` in `post.always` is mandatory. Persistent build state between jobs is prohibited unless an explicitly managed cache mechanism is approved and isolated.

### 12.2 Disk and Resource Monitoring

Agents must be monitored for disk pressure and build-health signals. Builds must fail gracefully with a clear message if free disk falls below the defined safety threshold (10 GB minimum baseline unless a stricter platform-specific threshold is set).

### 12.3 No Privileged Drift

- `sudo` is prohibited in build scripts.  
- Agents run as non-privileged users.  
- The controller and agents must remain aligned with their IaC definitions.

---

## 13. Plugin and Controller Configuration

### 13.1 Approved Plugins Only

Only approved Jenkins plugins may be installed. The approved set must be managed in configuration repositories, such as `jenkins-config-as-code` or the infrastructure repository that defines the Jenkins controller baseline.

Typical approved set includes:

- `pipeline`  
- `workflow-aggregator`  
- `git`  
- `credentials`  
- `credentials-binding`  
- `blueocean` (or the approved UI package)  
- `slack`  
- `junit`  
- `aws-credentials`  
- `s3`  
- `timestamper`  
- `ws-cleanup`  
- `build-timeout`  
- `configuration-as-code`

Plugin additions require Architect approval and security review.

### 13.2 Jenkins Configuration as Code

Controller configuration must be managed as code, for example through JCasC YAML committed in the infrastructure repository. Manual controller configuration is prohibited except for temporary, time-bounded debugging that is subsequently codified or removed.

### 13.3 Plugin Update Policy

- review and update plugins monthly;  
- apply security-critical updates within 48 hours of disclosure;  
- validate updates in staging Jenkins before production rollout.

---

## 14. Pipeline Security and RBAC

### 14.1 Groovy Sandbox and Script Security

The Groovy sandbox must remain enabled. Any sandbox exemption or method approval must receive explicit review, and the approved list must be reviewed regularly to remove stale entries.

`script { ... }` blocks should be kept narrow and justified. Broad sandbox escapes, unreviewed approvals, or patterns equivalent to `allowAnyDelegation` are prohibited.

### 14.2 Restricting Pipeline Mutation

Only designated pipeline authors may modify Jenkinsfiles or shared-library code. Pipeline changes require PR review by at least one qualified pipeline author and, where the change affects release-critical behavior or shared infrastructure, Architect review.

### 14.3 Approval RBAC

Promotion approvals must be enforced through Jenkins RBAC. Engineers may not self-approve production deployments unless their formal role explicitly authorizes that action and the governance standard allows it.

### 14.4 Audit Logging

All build triggers, parameter changes, credential-access events where supported, promotions, and release approvals must be recorded in the Jenkins audit trail and shipped to central logging. Audit records must be retained for **12 months minimum** and restricted to administrators and other explicitly authorized roles.

---

## 15. Maintenance and Hygiene

### 15.1 Code Hygiene

Jenkinsfiles are subject to the same hygiene expectations as production application code:

- no secrets in source;  
- shared functions in shared libraries;  
- descriptive stage names;  
- root-level Jenkinsfile under source control;  
- declarative syntax for new work;  
- parameter validation before shell use;  
- `cleanWs()` in `post.always`;  
- no duplicated orchestration logic.

### 15.2 Operational Maintenance Cadence

- **Weekly:** review failed builds; no `develop`/`main` failure may remain unaddressed for more than 1 business day.  
- **Monthly:** review plugins, stale jobs, deprecated pipelines, and obsolete repositories.  
- **Quarterly:** refresh agent images and pinned tool versions (with emergency security patching faster when required).  
- **Before expiry / as scheduled:** rotate signing materials, certificates, and expiring profiles.

### 15.3 Job Naming

Jobs should follow a stable, descriptive naming convention such as:

```
{project}/{platform}/{branch-type}
Examples:
bingo-classic/ios/feature
bingo-classic/android/release
internal-tools/player-management/main
```

---

## 16. Common Pitfalls to Avoid

| # | Pitfall | Impact | Required Remedy |
| :---- | :---- | :---- | :---- |
| 1 | Running builds on the controller | controller instability and security risk | run only on labeled agents |
| 2 | Missing timeout | hung builds consume licenses and block capacity | set pipeline/stage timeout |
| 3 | Missing `cleanWs()` | stale state contaminates later builds | clean workspace in `post.always` |
| 4 | `npm install` instead of `npm ci` | non-reproducible web builds | use lockfile-faithful install |
| 5 | Hard-coded credentials | secret exposure in source and logs | use Jenkins/AWS managed credentials only |
| 6 | Not returning Unity license | next build may fail or queue indefinitely | return license in `post.always` |
| 7 | No BOM scan | vulnerable dependency can ship | scan every promotable build |
| 8 | Rebuilding for staging/production | production binary differs from QA-tested binary | promote exact artifact only |
| 9 | `agent any` or weak agent selection | wrong toolchain or hidden drift | require explicit labels |
| 10 | Unsanitized user parameters in shell | command injection risk | allowlist validate every user parameter |
| 11 | Manual controller/plugin configuration | IaC drift and weak recoverability | manage through JCasC / infra repo |
| 12 | Missing notifications | broken pipelines go unnoticed | mandatory success/failure alerting |
| 13 | Unreviewed `script` blocks or sandbox escapes | elevated pipeline risk | keep script blocks narrow and reviewed |
| 14 | Direct production deploy from branch build | bypasses release governance | production only via promotion pipeline |
| 15 | UI-only pipeline with no committed `Jenkinsfile` | pipeline cannot be reviewed, versioned, or rebuilt cleanly | keep pipeline definition in source control |
| 16 | Business logic embedded in the `Jenkinsfile` | brittle, untestable automation | move logic to scripts or shared library functions |
| 17 | Unity build command missing `-quit` / improper process cleanup | Unity editor process lingers and poisons the agent | always use proper CLI exit semantics and cleanup |
| 18 | Plugin with known CVEs left unpatched | controller or agent security exposure | perform monthly plugin review and urgent security updates |

---

## 17. Implementation Checklist

Use this checklist when authoring a new Jenkins pipeline:

- [ ] `Jenkinsfile` committed at repository root  
- [ ] Declarative pipeline syntax used  
- [ ] Explicit agent labels; no `agent any`  
- [ ] Timeout, build discarder, timestamps, and workspace cleanup defined  
- [ ] Shared library used for common actions  
- [ ] Parameters validated before shell/tool use  
- [ ] Secrets retrieved from Jenkins/AWS-managed credentials only  
- [ ] Artifact uploaded to S3 with immutable `buildId`  
- [ ] `build-metadata.json` generated  
- [ ] BOM generated and scanned  
- [ ] Notifications configured for success/failure  
- [ ] Promotion uses the same artifact, not a rebuild  
- [ ] Approval gates and RBAC applied where required  
- [ ] Logs, artifacts, and audit records conform to retention policy

