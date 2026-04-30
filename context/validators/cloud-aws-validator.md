# validator.cloud-aws

- Validator ID: `validator.cloud-aws`
- Route: `route.cloud-aws`
- Source docs: `ESTD5`, `ESTD8`
- Overlay docs: `ESTD1`, `ESTD4`, `ESTD9`, `ESTD10`, `ESTD13`, `ESTD18`, `ESTD19`
- Applies to: AWS resources, Terraform, networking, IAM, EC2, load balancers, RDS, S3, CloudFront, WAF, Secrets Manager, messaging, observability, and cloud cost controls.
- Pass threshold: > 75% code conformity.

## Scoring

Use the shared scoring contract in `context/validators/README.md`.

## Check Groups

| Group | Weight | ESTD Sources | Validator Focus |
|:------|------:|:-------------|:----------------|
| Environment and IaC shape | 15 | `ESTD5`, `ESTD8`, `ESTD18` | environment parity, Terraform/source control, module placement, config separation |
| IAM, secrets, and identity | 20 | `ESTD1`, `ESTD5`, `ESTD8` | least privilege, permission boundaries, over-provisioning risk, secret storage, credential rotation, Okta/IAM boundaries |
| Network and edge security | 15 | `ESTD5`, `ESTD8` | VPC, security groups, HTTPS, WAF, load balancers, CDN boundaries |
| Data, backup, and retention | 10 | `ESTD8`, `ESTD9` | RDS/S3 safety, backups, encryption, restore evidence, data retention |
| Deployment and promotion safety | 15 | `ESTD5`, `ESTD8`, `ESTD13` | Dev/QA/Staging/Production gates, rollback, immutable artifacts, approvals |
| Observability, resilience, and cost | 15 | `ESTD1`, `ESTD5`, `ESTD8` | metrics, alarms, graceful degradation, scaling, cost controls |
| PR and exception evidence | 10 | `ESTD10`, `ESTD19` | terraform plan evidence, destructive-change callouts, release-close risk notes, coupling and approval notes |

## Static Coverage

| Group | Static Check IDs | LLM Gap |
|:------|:-----------------|:--------|
| Environment and IaC shape | `static.cloud.terraform-validate`, `static.common.folder-structure` | environment strategy intent |
| IAM, secrets, and identity | `static.cloud.checkov`, `static.common.secrets`, `static.common.gitleaks` | least-privilege and permission-boundary judgment |
| Network and edge security | `static.cloud.checkov`, `static.cloud.terraform-validate` | network exposure intent |
| Data, backup, and retention | `static.cloud.checkov`, `static.cloud.terraform-validate` | restore and retention adequacy |
| Deployment and promotion safety | `static.common.report-consistency` | promotion strategy and approval context |
| Observability, resilience, and cost | `static.cloud.checkov` | resilience and cost trade-offs |
| PR and exception evidence | `static.common.report-consistency` | destructive-change evidence quality |

## LLM Gap Review

Use `context/validators/llm-based-validation.md` for unresolved semantic gaps.

## Evolution Rules

- Re-resolve `route.cloud-aws` before each validator run.
- If provider-agnostic and AWS-specific rules diverge further, keep AWS checks in Source docs.
- Keep route binding aligned with `route.cloud-aws`.
