# ESTD8 - AWS Standards Document for Bingo Game Infrastructure

**ESTD8 — AWS Standards**

| Field | Value |
|:----- |:----- |
| Document ID | ESTD8 |
| Version | 4.1 |
| Status | Active |
| Last Updated | 2026-04-30 |
| Applies To | All engineers who provision, configure, or deploy AWS resources |
| Depends On | [ESTD5](./ESTD5_-_Cloud_Engg_Standards.md#estd5---cloud-engineering-standards-and-best-practices-for-infrastructure-management) |
| Approval | Director of Engineering / Server Architect |

---

> **📋 Living Document Notice** This document is a work in progress and will evolve as our systems, practices, and understanding mature. Feedback, questions, and suggestions are welcome — please submit them via comments on the corresponding Confluence page. However, the standards defined herein **must be strictly followed** in all active work. Any exception requires **explicit written approval** from the Director of Engineering or the appropriate Architect, and must be documented in the PR description, the exception log, or the relevant Confluence page.

---

## How to Use This Document

ESTD8 provides AWS-specific implementation details for the cloud principles in [ESTD5](./ESTD5_-_Cloud_Engg_Standards.md#estd5---cloud-engineering-standards-and-best-practices-for-infrastructure-management). [ESTD5](./ESTD5_-_Cloud_Engg_Standards.md#estd5---cloud-engineering-standards-and-best-practices-for-infrastructure-management) defines the "what and why"; ESTD8 defines the "how" for AWS. When a rule here conflicts with [ESTD5](./ESTD5_-_Cloud_Engg_Standards.md#estd5---cloud-engineering-standards-and-best-practices-for-infrastructure-management), the more restrictive of the two applies.

All Terraform examples in this document use Terraform HCL syntax. They are illustrative and must be adapted for the specific environment (dev/qa/staging/production) using module variables.

---

## Table of Contents

- [ESTD8 - AWS Standards Document for Bingo Game Infrastructure](#estd8---aws-standards-document-for-bingo-game-infrastructure)
  - [How to Use This Document](#how-to-use-this-document)
  - [Table of Contents](#table-of-contents)
  - [1. Purpose and Scope](#1-purpose-and-scope)
  - [2. Account Structure and AWS Organizations](#2-account-structure-and-aws-organizations)
    - [2.1 Account Layout](#21-account-layout)
    - [2.2 Terraform IaC: AWS Organizations](#22-terraform-iac-aws-organizations)
    - [2.3 Service Control Policies (SCPs)](#23-service-control-policies-scps)
  - [3. IAM and Permission Management](#3-iam-and-permission-management)
    - [3.1 EC2 Instance Profiles (Terraform)](#31-ec2-instance-profiles-terraform)
    - [3.2 IAM Role Naming Convention](#32-iam-role-naming-convention)
  - [4. EC2 and Auto Scaling Groups](#4-ec2-and-auto-scaling-groups)
    - [4.1 Instance Types](#41-instance-types)
    - [4.2 Launch Template (Terraform)](#42-launch-template-terraform)
    - [4.3 Auto Scaling Group (Terraform)](#43-auto-scaling-group-terraform)
  - [5. Elastic Load Balancing (ALB)](#5-elastic-load-balancing-alb)
    - [5.1 ALB Configuration (Terraform)](#51-alb-configuration-terraform)
    - [5.2 Target Group with Health Check](#52-target-group-with-health-check)
    - [5.3 NLB for SmartFox TCP](#53-nlb-for-smartfox-tcp)
  - [6. AWS WAF](#6-aws-waf)
    - [6.1 Mandatory WAF Rules](#61-mandatory-waf-rules)
  - [7. Amazon RDS (MySQL)](#7-amazon-rds-mysql)
    - [7.1 RDS Instance (Terraform)](#71-rds-instance-terraform)
    - [7.2 RDS Proxy (Connection Pooling)](#72-rds-proxy-connection-pooling)
  - [8. Amazon RDS Read Replicas and Database Scaling](#8-amazon-rds-read-replicas-and-database-scaling)
    - [8.1 Read Replica Topology and Allowed Use Cases](#81-read-replica-topology-and-allowed-use-cases)
    - [8.2 Traffic Routing Rules](#82-traffic-routing-rules)
    - [8.3 Terraform Pattern for a MySQL Read Replica](#83-terraform-pattern-for-a-mysql-read-replica)
    - [8.4 Monitoring, Replica Lag, and Failover](#84-monitoring-replica-lag-and-failover)
  - [9. Amazon ElastiCache (Redis) and Custom Cache](#9-amazon-elasticache-redis-and-custom-cache)
  - [10. Amazon S3](#10-amazon-s3)
    - [10.1 Game Assets Bucket](#101-game-assets-bucket)
  - [11. Amazon CloudFront](#11-amazon-cloudfront)
  - [12. AWS Secrets Manager](#12-aws-secrets-manager)
    - [12.1 Secret Naming Convention](#121-secret-naming-convention)
    - [12.2 Creating a Secret (Terraform)](#122-creating-a-secret-terraform)
    - [12.3 Accessing Secrets in PHP](#123-accessing-secrets-in-php)
  - [13. AWS CodePipeline and CI/CD](#13-aws-codepipeline-and-cicd)
    - [13.1 Pipeline Structure](#131-pipeline-structure)
    - [13.2 Blue/Green vs Rolling Deployments](#132-bluegreen-vs-rolling-deployments)
  - [14. CloudWatch and Datadog Integration](#14-cloudwatch-and-datadog-integration)
    - [14.1 CloudWatch Log Groups (Terraform)](#141-cloudwatch-log-groups-terraform)
    - [14.2 Standard CloudWatch Alarms (Terraform)](#142-standard-cloudwatch-alarms-terraform)
  - [15. Amazon SQS and SNS](#15-amazon-sqs-and-sns)
  - [16. VPC and Network Standards](#16-vpc-and-network-standards)
  - [17. Common Cost Leaks to Check Monthly](#17-common-cost-leaks-to-check-monthly)

---

## 1. Purpose and Scope

This document specifies AWS service-level configuration standards for the Bingo game infrastructure. Our primary player base is in the USA; all production resources must be deployed in a US AWS region (recommended: `us-east-1` as primary). Staging may be in the same region as production or a secondary US region. Dev and QA can use any region, but team consensus on one region simplifies cross-environment work.

---

## 2. Account Structure and AWS Organizations

### 2.1 Account Layout

```
AWS Organization: bingo-games-org
├── Management Account     ← billing, SCP policies only — NO workloads
├── bingo-production       ← live player traffic
├── bingo-staging          ← pre-release validation
├── bingo-qa               ← QA team testing
└── bingo-dev              ← developer integration testing
```

### 2.2 Terraform IaC: AWS Organizations

```hcl
# global/organizations.tf
resource "aws_organizations_organization" "main" {
  aws_service_access_principals = [
    "cloudtrail.amazonaws.com",
    "config.amazonaws.com",
    "sso.amazonaws.com",
  ]
  feature_set = "ALL"
}

resource "aws_organizations_account" "production" {
  name      = "bingo-production"
  email     = "aws-production@bingo.example.com"
  parent_id = aws_organizations_organizational_unit.workloads.id
  tags = { Environment = "production", Project = "BingoBash" }
}
```

### 2.3 Service Control Policies (SCPs)

Enforce guardrails at the organization level:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyRegionOutsideUS",
      "Effect": "Deny",
      "NotAction": ["iam:*", "sts:*", "route53:*", "support:*", "cloudfront:*"],
      "Resource": "*",
      "Condition": {
        "StringNotEquals": { "aws:RequestedRegion": ["us-east-1", "us-west-2"] }
      }
    },
    {
      "Sid": "DenyRootAccountUsage",
      "Effect": "Deny",
      "Action": "*",
      "Resource": "*",
      "Condition": { "StringEquals": { "aws:PrincipalType": "Root" } }
    }
  ]
}
```

---

## 3. IAM and Permission Management

IAM means Identity and Access Management. In AWS, IAM roles and policies are permission boundaries: they define what a workload, pipeline, or human operator can do even if the caller is authenticated. Follow [ESTD5 §4.1 Principle of Least Privilege](./ESTD5_-_Cloud_Engg_Standards.md#41-principle-of-least-privilege) and the server trust model in [ESTD4 §17.6 Server Trust and Permission Boundaries](./ESTD4_-_Server_Engg_Standards.md#176-server-trust-and-permission-boundaries). Each role must be scoped by service, environment, AWS account, secret path, resource ARN, and operation wherever AWS supports it.

Over-provisioned AWS roles are not safe defaults. A wildcard policy on a PHP API, SmartFox server, SEAM service, or deployment job can let one compromised process read secrets, alter queues, access unrelated buckets, or mutate production infrastructure. Use narrow policies by default, document every wildcard exception, and review broad permissions quarterly.

### 3.1 EC2 Instance Profiles (Terraform)

```hcl
# modules/compute/iam.tf

# Role — what the EC2 instance is allowed to do
resource "aws_iam_role" "php_api" {
  name = "bingo-${var.environment}-php-api-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })

  tags = var.common_tags
}

resource "aws_iam_role_policy" "php_api_permissions" {
  name = "bingo-${var.environment}-php-api-policy"
  role = aws_iam_role.php_api.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      # Secrets Manager — only the secrets this service needs
      {
        Effect   = "Allow"
        Action   = ["secretsmanager:GetSecretValue"]
        Resource = [
          "arn:aws:secretsmanager:${var.region}:${var.account_id}:secret:${var.environment}/php-api/*"
        ]
      },
      # Parameter Store — application configuration
      {
        Effect   = "Allow"
        Action   = ["ssm:GetParameter", "ssm:GetParametersByPath"]
        Resource = "arn:aws:ssm:${var.region}:${var.account_id}:parameter/bingo/${var.environment}/*"
      },
      # S3 — game assets bucket only
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:PutObject"]
        Resource = "${aws_s3_bucket.game_assets.arn}/*"
      },
      # SQS — send to background jobs queue only
      {
        Effect   = "Allow"
        Action   = ["sqs:SendMessage"]
        Resource = aws_sqs_queue.background_jobs.arn
      },
      # CloudWatch — emit custom metrics and write logs
      {
        Effect   = "Allow"
        Action   = ["cloudwatch:PutMetricData"]
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = ["logs:PutLogEvents", "logs:CreateLogStream"]
        Resource = "arn:aws:logs:${var.region}:${var.account_id}:log-group:/bingo/${var.environment}/php-api:*"
      },
      # SSM Session Manager — no SSH keys needed
      {
        Effect   = "Allow"
        Action   = ["ssm:StartSession", "ssm:TerminateSession", "ssm:ResumeSession"]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_instance_profile" "php_api" {
  name = "bingo-${var.environment}-php-api-profile"
  role = aws_iam_role.php_api.name
}
```

### 3.2 IAM Role Naming Convention

```hcl
bingo-{environment}-{service-name}-role
bingo-{environment}-{service-name}-policy

Examples:
  bingo-production-php-api-role
  bingo-staging-reward-service-role
  bingo-production-smartfox-role
```

---

## 4. EC2 and Auto Scaling Groups

### 4.1 Instance Types

| Server | Environment | Instance Type | Rationale |
|:-------|:------------|:--------------|:----------|
| PHP API | Production | `c6i.xlarge` (4 vCPU, 8 GB) | CPU-bound; compute-optimized |
| PHP API | Staging | `c6i.large` (2 vCPU, 4 GB) | Smaller but same family | 
| SmartFox | Production | `r6i.2xlarge` (8 vCPU, 64 GB) | JVM with large heap; memory-optimized |
| Java microservices | Production |`c6i.large` per service | Right-size per service load test |

### 4.2 Launch Template (Terraform)

```hcl
# modules/compute/launch_template.tf
resource "aws_launch_template" "php_api" {
  name_prefix   = "bingo-${var.environment}-php-api-"
  image_id      = var.ami_id      # Hardened Amazon Linux 2023 AMI, built via Packer
  instance_type = var.instance_type

  iam_instance_profile {
    name = aws_iam_instance_profile.php_api.name
  }

  network_interfaces {
    associate_public_ip_address = false  # Private subnet — no direct internet access
    security_groups             = [aws_security_group.api_ec2.id]
    delete_on_termination       = true
  }

  block_device_mappings {
    device_name = "/dev/xvda"
    ebs {
      volume_size           = 30
      volume_type           = "gp3"          # Better IOPS/cost than gp2
      encrypted             = true
      kms_key_id            = var.ebs_kms_key_arn
      delete_on_termination = true
      throughput            = 125
    }
  }

  monitoring { enabled = true }  # Detailed CloudWatch monitoring (1-minute granularity)

  metadata_options {
    http_tokens                 = "required"  # IMDSv2 — prevents SSRF attacks
    http_put_response_hop_limit = 1
    http_endpoint               = "enabled"
  }

  user_data = base64encode(templatefile("${path.module}/scripts/php_api_init.sh.tpl", {
    environment = var.environment
    region      = var.region
  }))

  tag_specifications {
    resource_type = "instance"
    tags = merge(var.common_tags, { Name = "bingo-${var.environment}-php-api" })
  }
}
```

### 4.3 Auto Scaling Group (Terraform)

```hcl
# modules/compute/asg.tf
resource "aws_autoscaling_group" "php_api" {
  name                = "bingo-${var.environment}-php-api-asg"
  min_size            = var.asg_min_size     # production: 4, staging: 2, qa: 1, dev: 1
  max_size            = var.asg_max_size     # production: 20, staging: 6
  desired_capacity    = var.asg_desired      # production: 4, set by load testing

  health_check_type         = "ELB"          # Use ALB health check, more accurate than EC2
  health_check_grace_period = 120            # Allow time for PHP-FPM to start

  vpc_zone_identifier = var.private_subnet_ids   # Multi-AZ private subnets

  launch_template {
    id      = aws_launch_template.php_api.id
    version = "$Latest"
  }

  # Scale-in protection during content reset window
  # Managed externally via scheduled actions
  protect_from_scale_in = false

  tag {
    key                 = "Environment"
    value               = var.environment
    propagate_at_launch = true
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Target tracking — scale out when average CPU > 65%
resource "aws_autoscaling_policy" "cpu_scale_out" {
  name                   = "bingo-${var.environment}-cpu-tracking"
  autoscaling_group_name = aws_autoscaling_group.php_api.name
  policy_type            = "TargetTrackingScaling"

  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }
    target_value     = 65.0
    disable_scale_in = false
  }
}

# Scheduled pre-scaling for content reset
# Content reset timing is periodic and configured separately — this example
# uses the EventBridge-triggered approach for flexibility
resource "aws_autoscaling_schedule" "presscale_for_reset" {
  scheduled_action_name  = "bingo-${var.environment}-presscale"
  autoscaling_group_name = aws_autoscaling_group.php_api.name
  min_size               = var.reset_presscale_min    # production: 12
  desired_capacity       = var.reset_presscale_desired # production: 16
  # This schedule is updated by the content reset management system
  # via Lambda or EventBridge before each reset window
  recurrence             = var.reset_presscale_cron
  time_zone              = "UTC"
}
```

---

## 5. Elastic Load Balancing (ALB)

### 5.1 ALB Configuration (Terraform)

```hcl
# modules/networking/alb.tf
resource "aws_lb" "main" {
  name               = "bingo-${var.environment}-alb"
  internal           = false                 # Internet-facing
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = var.public_subnet_ids # Public subnets only

  enable_deletion_protection = var.environment == "production"  # Prevent accidental deletion
  enable_http2               = true

  access_logs {
    bucket  = aws_s3_bucket.alb_logs.bucket
    prefix  = "alb/${var.environment}"
    enabled = true   # Always enable — essential for debugging and security auditing
  }

  tags = var.common_tags
}

# HTTPS listener
resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.main.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"  # TLS 1.2/1.3; disables TLS 1.0 and 1.1
  certificate_arn   = var.acm_certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.php_api.arn
  }
}

# Redirect HTTP to HTTPS
resource "aws_lb_listener" "http_redirect" {
  load_balancer_arn = aws_lb.main.arn
  port              = "80"
  protocol          = "HTTP"
  default_action {
    type = "redirect"
    redirect { protocol = "HTTPS"; port = "443"; status_code = "HTTP_301" }
  }
}
```

### 5.2 Target Group with Health Check

```hcl
resource "aws_lb_target_group" "php_api" {
  name        = "bingo-${var.environment}-api-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "instance"

  health_check {
    enabled             = true
    path                = "/health"         # ESTD4 §16 health endpoint
    healthy_threshold   = 2
    unhealthy_threshold = 3
    interval            = 15
    timeout             = 5
    matcher             = "200"
  }

  deregistration_delay = 30   # Allow in-flight PHP-FPM requests to complete

  tags = var.common_tags
}
```

### 5.3 NLB for SmartFox TCP

SmartFox uses persistent TCP connections — use a Network Load Balancer:

```hcl
resource "aws_lb" "smartfox" {
  name               = "bingo-${var.environment}-sfs-nlb"
  internal           = false
  load_balancer_type = "network"
  subnets            = var.public_subnet_ids
  enable_cross_zone_load_balancing = true
  tags = var.common_tags
}

resource "aws_lb_listener" "smartfox_tcp" {
  load_balancer_arn = aws_lb.smartfox.arn
  port              = "9933"  # SmartFox default TCP port
  protocol          = "TCP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.smartfox.arn
  }
}
```

---

## 6. AWS WAF

### 6.1 Mandatory WAF Rules

```hcl 
resource "aws_wafv2_web_acl" "main" {
  name  = "bingo-${var.environment}-waf"
  scope = "REGIONAL"

  default_action { allow {} }

  # 1. AWS Managed Core Rule Set — OWASP Top 10 protection
  rule {
    name     = "AWSManagedRulesCommonRuleSet"
    priority = 1
    override_action { none {} }
    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesCommonRuleSet"
        vendor_name = "AWS"
      }
    }
    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "CommonRuleSet"
      sampled_requests_enabled   = true
    }
  }

  # 2. Rate limiting — 1000 requests per 5 minutes per IP
  rule {
    name     = "RateLimitPerIP"
    priority = 2
    action { block {} }
    statement {
      rate_based_statement {
        limit              = 1000
        aggregate_key_type = "IP"
      }
    }
    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "RateLimitPerIP"
      sampled_requests_enabled   = true
    }
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "bingo-waf"
    sampled_requests_enabled   = true
  }

  tags = var.common_tags
}

resource "aws_wafv2_web_acl_association" "alb" {
  resource_arn = aws_lb.main.arn
  web_acl_arn  = aws_wafv2_web_acl.main.arn
}
```

---

## 7. Amazon RDS (MySQL)

### 7.1 RDS Instance (Terraform)

```hcl
resource "aws_db_instance" "primary" {
  identifier     = "bingo-${var.environment}-mysql"
  engine         = "mysql"
  engine_version = "8.0.36"           # Pin to specific minor version
  instance_class = var.db_instance_class  # production: db.r6g.2xlarge

  allocated_storage     = var.db_storage_gb        # production: 500
  max_allocated_storage = var.db_storage_max_gb    # production: 2000 (autoscaling)
  storage_type          = "gp3"
  storage_encrypted     = true
  kms_key_id            = var.rds_kms_key_arn

  db_name  = "bingo_${var.environment}"
  username = "bingo_app"
  password = random_password.db.result    # Generated and stored in Secrets Manager

  multi_az               = var.environment == "production" || var.environment == "staging"
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  backup_retention_period   = 14
  backup_window             = "02:00-03:00"     # 2-3 AM UTC = low traffic (US off-peak)
  maintenance_window        = "sun:04:00-sun:05:00"

  performance_insights_enabled          = true
  performance_insights_retention_period = 7
  monitoring_interval                   = 60
  monitoring_role_arn                   = aws_iam_role.rds_monitoring.arn
  enabled_cloudwatch_logs_exports       = ["error", "slowquery", "general"]

  deletion_protection       = var.environment == "production"
  skip_final_snapshot       = var.environment != "production"
  final_snapshot_identifier = var.environment == "production" ? "bingo-prod-final-${formatdate("YYYYMMDD", timestamp())}" : null

  parameter_group_name = aws_db_parameter_group.mysql8.name
  tags = var.common_tags
}

resource "aws_db_parameter_group" "mysql8" {
  family = "mysql8.0"
  name   = "bingo-${var.environment}-mysql8"

  parameter { name = "slow_query_log";                   value = "1" }
  parameter { name = "long_query_time";                  value = "0.5" }   # Log queries > 500ms
  parameter { name = "log_queries_not_using_indexes";    value = "1" }
  parameter { name = "innodb_buffer_pool_size";          value = "{DBInstanceClassMemory*3/4}" }
  parameter { name = "max_connections";                  value = "500" }
  parameter { name = "transaction_isolation";            value = "REPEATABLE-READ" }
  parameter { name = "innodb_deadlock_detect";           value = "ON" }
}
```

### 7.2 RDS Proxy (Connection Pooling)

PHP opens a new database connection per PHP-FPM worker. Without a proxy, an ASG with 10 instances and 50 workers each creates 500 connections — easily exhausting MySQL's `max_connections`.

```hcl
resource "aws_db_proxy" "main" {
  name                   = "bingo-${var.environment}-rds-proxy"
  debug_logging          = false
  engine_family          = "MYSQL"
  idle_client_timeout    = 1800
  require_tls            = true
  role_arn               = aws_iam_role.rds_proxy.arn
  vpc_security_group_ids = [aws_security_group.rds.id]
  vpc_subnet_ids         = var.data_subnet_ids

  auth {
    auth_scheme = "SECRETS"
    iam_auth    = "DISABLED"
    secret_arn  = aws_secretsmanager_secret.db_credentials.arn
  }

  tags = var.common_tags
}
```

---

## 8. Amazon RDS Read Replicas and Database Scaling

MySQL is the authoritative transactional database for both Bingo games. Read replicas are optional scaling and resilience tools around that primary, not alternative primary datastores. Use them for reporting, exports, reconciliation jobs, or carefully selected read-heavy workloads that tolerate replica lag.

### 8.1 Read Replica Topology and Allowed Use Cases

Preferred topology:

```
Writer endpoint (primary)  -> all writes, transactions, strict read-after-write flows
Reader endpoint(s)         -> reports, exports, dashboards, offline analysis, selected cache warmers
```

Rules:

- All writes go to the primary.
- Player-critical flows that require immediate read-after-write consistency stay on the primary.
- Replica-backed traffic must degrade safely if lag grows beyond tolerance.
- A read replica is not a backup and must not be treated as one.

### 8.2 Traffic Routing Rules

Application configuration must distinguish writer and reader endpoints explicitly. Never “spray and pray” SQL across endpoints.

- Legacy PHP monolith: keep economic and player-session reads on the writer unless the flow is proven replica-safe.
- Java/SEAM services: repositories that use a replica must declare that choice intentionally; do not hide it inside generic data-access helpers.
- Internal tools and exports may use replicas if stale data is acceptable and documented in the tool UX.

### 8.3 Terraform Pattern for a MySQL Read Replica

```hcl
resource "aws_db_instance" "reader" {
  identifier             = "bingo-${var.environment}-mysql-ro-1"
  replicate_source_db    = aws_db_instance.main.identifier
  instance_class         = var.read_replica_instance_class
  publicly_accessible    = false
  auto_minor_version_upgrade = true
  storage_encrypted      = true
  multi_az               = false
  performance_insights_enabled = var.environment == "production"

  monitoring_interval    = 60
  deletion_protection    = var.environment == "production"
  tags = merge(var.common_tags, {{
    Role = "read-replica"
  }})
}
```

Use the RDS **reader endpoint** when multiple replicas exist behind one cluster abstraction; otherwise, configure explicit replica endpoints in the application.

### 8.4 Monitoring, Replica Lag, and Failover

Minimum controls:

- CloudWatch alarms on replica lag, CPU, free storage, and replication stopped state;
- dashboards that separate primary and replica health;
- runbook for removing a lagging replica from traffic;
- documented criteria for replica promotion during disaster recovery.

If replica lag exceeds the workload's tolerance window, the application must stop using that replica until the lag clears or traffic is rerouted.

---

## 9. Amazon ElastiCache (Redis) and Custom Cache

```hcl
resource "aws_elasticache_replication_group" "main" {
  replication_group_id = "bingo-${var.environment}-redis"
  description          = "Bingo ${var.environment} Redis — session, cache, feature flags"

  node_type            = var.redis_node_type   # production: cache.r7g.large
  port                 = 6379
  engine_version       = "7.1"
  parameter_group_name = aws_elasticache_parameter_group.redis7.name

  automatic_failover_enabled = var.environment == "production" || var.environment == "staging"
  multi_az_enabled           = var.environment == "production" || var.environment == "staging"
  num_cache_clusters         = var.redis_num_nodes  # production: 2 (primary + 1 replica)

  subnet_group_name  = aws_elasticache_subnet_group.main.name
  security_group_ids = [aws_security_group.redis.id]

  at_rest_encryption_enabled = true
  transit_encryption_enabled = true    # TLS — required

  snapshot_retention_limit = 3
  snapshot_window          = "03:00-04:00"

  tags = var.common_tags
}

resource "aws_elasticache_parameter_group" "redis7" {
  family = "redis7"
  name   = "bingo-${var.environment}-redis7"
  parameter {
    name  = "maxmemory-policy"
    value = "allkeys-lru"    # Evict least-recently-used when memory is full
  }
}
```

---

## 10. Amazon S3

### 10.1 Game Assets Bucket

```hcl
resource "aws_s3_bucket" "game_assets" {
  bucket = "bingo-assets-${var.environment}-${var.account_id}"
  tags   = var.common_tags
}

# Block ALL public access — assets served via CloudFront, not direct S3
resource "aws_s3_bucket_public_access_block" "game_assets" {
  bucket                  = aws_s3_bucket.game_assets.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "game_assets" {
  bucket = aws_s3_bucket.game_assets.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "game_assets" {
  bucket = aws_s3_bucket.game_assets.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = var.s3_kms_key_arn
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "game_assets" {
  bucket = aws_s3_bucket.game_assets.id
  rule {
    id     = "expire-old-versions"
    status = "Enabled"
    noncurrent_version_expiration { noncurrent_days = 30 }
  }
}
```

---

## 11. Amazon CloudFront

```hcl
resource "aws_cloudfront_distribution" "assets" {
  enabled     = true
  comment     = "Bingo game asset CDN — ${var.environment}"
  price_class = "PriceClass_100"    # North America + Europe (covers US player base)

  origin {
    domain_name              = aws_s3_bucket.game_assets.bucket_regional_domain_name
    origin_id                = "S3-game-assets"
    origin_access_control_id = aws_cloudfront_origin_access_control.assets.id
  }

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "S3-game-assets"
    compress               = true
    viewer_protocol_policy = "redirect-to-https"

    cache_policy_id = aws_cloudfront_cache_policy.assets.id
  }

  viewer_certificate {
    acm_certificate_arn      = var.cloudfront_acm_certificate_arn  # Must be in us-east-1
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  restrictions {
    geo_restriction { restriction_type = "none" }
  }

  tags = var.common_tags
}

# Origin Access Control (newer, more secure than OAI)
resource "aws_cloudfront_origin_access_control" "assets" {
  name                              = "bingo-${var.environment}-assets-oac"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}
```

---

## 12. AWS Secrets Manager

### 12.1 Secret Naming Convention

```hcl
{environment}/{service-name}/{secret-name}

Examples:
  production/php-api/db-password
  production/reward-service/payment-api-key
  staging/php-api/smartfox-internal-secret
  production/shared/jwt-signing-key
```

### 12.2 Creating a Secret (Terraform)

```hcl
resource "aws_secretsmanager_secret" "db_password" {
  name                    = "${var.environment}/php-api/db-password"
  description             = "MySQL RDS password for the PHP API service — ${var.environment}"
  recovery_window_in_days = 7   # Safety net before permanent deletion
  kms_key_id              = var.secrets_kms_key_arn
  tags = var.common_tags
}

resource "aws_secretsmanager_secret_rotation" "db_password" {
  secret_id           = aws_secretsmanager_secret.db_password.id
  rotation_lambda_arn = var.db_rotation_lambda_arn
  rotation_rules {
    automatically_after_days = 90
  }
}
```

### 12.3 Accessing Secrets in PHP

```php
// In application startup — retrieve once, cache in memory
$client = new Aws\SecretsManager\SecretsManagerClient([
    'region'  => 'us-east-1',
    // No credentials needed — uses EC2 instance role automatically
]);

$secret = $client->getSecretValue([
    'SecretId' => "production/php-api/db-password"
]);

$dbPassword = $secret['SecretString'];
// Cache for 1 hour — avoid API call on every request
```

---

## 13. AWS CodePipeline and CI/CD

### 13.1 Pipeline Structure

```hcl
resource "aws_codepipeline" "php_api" {
  name     = "bingo-${var.environment}-php-api-pipeline"
  role_arn = aws_iam_role.codepipeline.arn

  artifact_store {
    location = aws_s3_bucket.pipeline_artifacts.bucket
    type     = "S3"
    encryption_key {
      id   = var.pipeline_kms_key_arn
      type = "KMS"
    }
  }

  # Stage 1: Source
  stage {
    name = "Source"
    action {
      name             = "SourceCode"
      category         = "Source"
      owner            = "AWS"
      provider         = "CodeStarSourceConnection"
      version          = "1"
      output_artifacts = ["source_output"]
      configuration = {
        ConnectionArn    = var.github_connection_arn
        FullRepositoryId = "your-org/bingo-api"
        BranchName       = var.branch_name
      }
    }
  }

  # Stage 2: Build + Test
  stage {
    name = "BuildAndTest"
    action {
      name             = "Build"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      version          = "1"
      input_artifacts  = ["source_output"]
      output_artifacts = ["build_output"]
      configuration    = { ProjectName = aws_codebuild_project.php_api.name }
    }
  }

  # Stage 3: Deploy to QA (auto)
  stage {
    name = "DeployQA"
    action {
      name            = "Deploy"
      category        = "Deploy"
      owner           = "AWS"
      provider        = "CodeDeployToEC2"  # or ECS
      version         = "1"
      input_artifacts = ["build_output"]
      configuration   = { ApplicationName = "bingo-qa-php-api" }
    }
  }

  # Stage 4: Manual approval before staging
  stage {
    name = "ApproveStaging"
    action {
      name     = "QASignOff"
      category = "Approval"
      owner    = "AWS"
      provider = "Manual"
      version  = "1"
      configuration = {
        NotificationArn = var.approval_sns_arn
        CustomData      = "QA sign-off required before promoting to Staging"
      }
    }
  }

  # Stage 5: Deploy to Staging
  # Stage 6: Architect approval
  # Stage 7: Deploy to Production
  # ... (same pattern as above)
}
```

### 13.2 Blue/Green vs Rolling Deployments

| Scenario | Strategy | Why | 
|:---------|:---------|:----|
| Routine PHP API deploy | Rolling (batch size 25%) | Zero downtime; maintains capacity |
| High-risk deploy (schema change) | Blue/Green | Instant rollback to old fleet |
| SmartFox deploy | Maintenance window | Stateful; must drain rooms first | 
| Java microservice | Rolling (ECS) | ECS handles graceful task replacement |

---

## 14. CloudWatch and Datadog Integration

### 14.1 CloudWatch Log Groups (Terraform)

```hcl
resource "aws_cloudwatch_log_group" "php_api" {
  name              = "/bingo/${var.environment}/php-api"
  retention_in_days = var.environment == "production" ? 30 : 7
  kms_key_id        = var.logs_kms_key_arn
  tags              = var.common_tags
}

# Audit logs — longer retention
resource "aws_cloudwatch_log_group" "audit" {
  name              = "/bingo/${var.environment}/audit"
  retention_in_days = 365   # 1-year retention for compliance
  kms_key_id        = var.logs_kms_key_arn
  tags              = var.common_tags
}
```

### 14.2 Standard CloudWatch Alarms (Terraform)

```hcl
# API error rate alarm
resource "aws_cloudwatch_metric_alarm" "api_error_rate" {
  alarm_name          = "bingo-${var.environment}-api-high-error-rate"
  alarm_description   = "API 5xx error rate > 1% over 5 minutes"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 3
  threshold           = 1.0
  treat_missing_data  = "notBreaching"

  metric_query {
    id          = "error_rate"
    expression  = "errors / requests * 100"
    label       = "Error Rate (%)"
    return_data = true
  }
  metric_query {
    id = "errors"
    metric {
      metric_name = "HTTPCode_Target_5XX_Count"
      namespace   = "AWS/ApplicationELB"
      period      = 60
      stat        = "Sum"
      dimensions  = { LoadBalancer = aws_lb.main.arn_suffix }
    }
  }
  metric_query {
    id = "requests"
    metric {
      metric_name = "RequestCount"
      namespace   = "AWS/ApplicationELB"
      period      = 60
      stat        = "Sum"
      dimensions  = { LoadBalancer = aws_lb.main.arn_suffix }
    }
  }

  alarm_actions = [var.critical_sns_arn]
  ok_actions    = [var.critical_sns_arn]
}

# RDS storage running low
resource "aws_cloudwatch_metric_alarm" "rds_storage_low" {
  alarm_name          = "bingo-${var.environment}-rds-low-storage"
  alarm_description   = "RDS free storage < 50 GB — provision more storage or investigate growth"
  metric_name         = "FreeStorageSpace"
  namespace           = "AWS/RDS"
  comparison_operator = "LessThanThreshold"
  threshold           = 53687091200  # 50 GB in bytes
  evaluation_periods  = 2
  period              = 300
  statistic           = "Average"
  dimensions          = { DBInstanceIdentifier = aws_db_instance.primary.id }
  alarm_actions       = [var.warning_sns_arn]
}
```

---

## 15. Amazon SQS and SNS

```hcl
# Dead letter queue
resource "aws_sqs_queue" "jobs_dlq" {
  name                      = "bingo-${var.environment}-jobs-dlq"
  message_retention_seconds = 1209600   # 14 days
  tags = var.common_tags
}

# Main job queue
resource "aws_sqs_queue" "jobs" {
  name                       = "bingo-${var.environment}-jobs"
  visibility_timeout_seconds = 300     # Must exceed max job processing time
  message_retention_seconds  = 86400   # 24 hours
  receive_wait_time_seconds  = 20      # Long polling — reduces empty receives

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.jobs_dlq.arn
    maxReceiveCount     = 3            # Move to DLQ after 3 failed attempts
  })

  tags = var.common_tags
}

# Alert when DLQ has messages — always means jobs are failing
resource "aws_cloudwatch_metric_alarm" "dlq_not_empty" {
  alarm_name          = "bingo-${var.environment}-jobs-dlq-not-empty"
  alarm_description   = "Background job DLQ has messages — investigate failing jobs"
  metric_name         = "ApproximateNumberOfMessagesVisible"
  namespace           = "AWS/SQS"
  comparison_operator = "GreaterThanThreshold"
  threshold           = 0
  evaluation_periods  = 1
  period              = 60
  statistic           = "Sum"
  dimensions          = { QueueName = aws_sqs_queue.jobs_dlq.name }
  alarm_actions       = [var.warning_sns_arn]
}
```

---

## 16. VPC and Network Standards

```hcl
# modules/networking/vpc.tf
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr    # production: 10.0.0.0/16, staging: 10.1.0.0/16
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags = merge(var.common_tags, { Name = "bingo-${var.environment}-vpc" })
}

# Public subnets — ALB, NAT Gateway (one per AZ)
resource "aws_subnet" "public" {
  count             = length(var.azs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index)
  availability_zone = var.azs[count.index]
  map_public_ip_on_launch = false   # No auto-assign — only ALB gets a public IP via EIP
  tags = merge(var.common_tags, { Name = "bingo-${var.environment}-public-${var.azs[count.index]}", Tier = "public" })
}

# Private subnets — EC2, SmartFox, ECS tasks
resource "aws_subnet" "private" {
  count             = length(var.azs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index + 10)
  availability_zone = var.azs[count.index]
  tags = merge(var.common_tags, { Name = "bingo-${var.environment}-private-${var.azs[count.index]}", Tier = "private" })
}

# Data subnets — RDS, read replicas, ElastiCache (no internet route — completely isolated)
resource "aws_subnet" "data" {
  count             = length(var.azs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index + 20)
  availability_zone = var.azs[count.index]
  tags = merge(var.common_tags, { Name = "bingo-${var.environment}-data-${var.azs[count.index]}", Tier = "data" })
}

# NAT Gateway per AZ — prevents single AZ failure from removing internet access for all private subnets
resource "aws_nat_gateway" "main" {
  count         = length(var.azs)
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id
  tags = merge(var.common_tags, { Name = "bingo-${var.environment}-nat-${var.azs[count.index]}" })
}
```

---

## 17. Common Cost Leaks to Check Monthly

| Item | How to Check | Action | 
|:-----|:-------------|:-------|
| Unattached EBS volumes | EC2 → Volumes → filter "available" | Snapshot and delete |
| Idle/underutilized EC2 | Compute Optimizer → Under-utilized | Right-size or terminate | 
| Old snapshots (> 30 days) | EC2 → Snapshots → filter by age | Delete if not required for DR |
| Unused Elastic IPs | EC2 → Elastic IPs → filter unassociated | Release |
| S3 Incomplete multipart uploads | S3 lifecycle rule or S3 Lens | Add `AbortIncompleteMultipartUpload` lifecycle rule |
| CloudWatch Log Groups with no retention | CloudWatch → Log groups → "Never expire" | Set 30-day retention on all non-audit groups |
| Unused load balancers | EC2 → Load Balancers → check RequestCount | Delete if zero traffic |
| NAT Gateway data transfer | Cost Explorer → filter "NatGateway" | Review and optimize inter-AZ traffic patterns |
| RDS/read-replica instances left running unnecessarily | Console → DB instances | Right-size, stop, or delete unused non-production DB capacity |
| Oversized RDS instances | Performance Insights → CPU, connections | Right-size with Compute Optimizer |
