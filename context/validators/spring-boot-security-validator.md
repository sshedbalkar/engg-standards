# validator.spring-boot-security

- Validator ID: `validator.spring-boot-security`
- Route: `route.spring-boot-security`
- Source docs: `ESTD21`
- Overlay docs: `ESTD10`, `ESTD16`, `ESTD19`, `ESTD20`
- Applies to: Spring Boot 3.3+ banking services handling customer, account, payment, or card data — security filter chains, JWT decoding, authorization rules, encryption converters, masking, secrets access, audit writes, and retention logic.
- Pass threshold: > 75% code conformity.

## Scoring

Use the shared scoring contract in `context/validators/README.md`.

## Check Groups

| Group | Weight | ESTD Sources | Validator Focus |
|:------|------:|:-------------|:----------------|
| Authentication and token validation | 15 | `ESTD21` | resource server configuration, algorithm allowlist, issuer and audience validation, clock skew bounds, JWKS caching, principal derived only from the validated token |
| Authorization and ownership | 15 | `ESTD21`, `ESTD20` | deny-by-default matcher order, service-layer method security, scope and role separation, ownership enforced in the query, 404 over 403, four-eyes approval on high-risk operations |
| Data classification and encryption | 20 | `ESTD21` | field classification coverage, column-level encryption, envelope encryption and key custody, IV and mode selection, blind index usage, key rotation readiness, backup key separation |
| Masking, tokenization, and PCI scope | 15 | `ESTD21` | PAN and account masking at the response boundary, tokenization boundary, prohibited data never persisted, cardholder data environment scope decisions |
| Secrets management | 10 | `ESTD21` | no secrets in configuration or source, secrets manager retrieval, rotation readiness, secret handling in memory, heap dump and actuator exposure |
| Input and injection security | 10 | `ESTD21` | parameterized queries, dynamic sort and field allowlists, path traversal containment, SSRF address validation, XXE hardening, deserialization prohibition, upload controls, mass assignment |
| Audit trail and SOX evidence | 10 | `ESTD21` | audited event coverage including reads, record completeness, database-level immutability, tamper evidence chain, audit write propagation on failure, retention |
| Privacy and retention | 5 | `ESTD21` | personal data kept out of the ledger, erasure and crypto-shredding path, retention schedule enforcement, cross-border transfer constraints, consent records |

## Static Coverage

| Group | Static Check IDs | LLM Gap |
|:------|:-----------------|:--------|
| Authentication and token validation | `static.java.spotbugs`, `static.common.semgrep` | token trust boundary and issuer intent |
| Authorization and ownership | `static.java.spotbugs`, `static.common.semgrep` | object-level authorization and approval intent |
| Data classification and encryption | `static.common.secrets`, `static.common.gitleaks`, `static.java.spotbugs` | classification coverage and key custody judgment |
| Masking, tokenization, and PCI scope | `static.common.semgrep`, `static.java.spotbugs` | disclosure surface and PCI scope judgment |
| Secrets management | `static.common.secrets`, `static.common.gitleaks` | secret lifecycle and exposure judgment |
| Input and injection security | `static.common.semgrep`, `static.java.spotbugs` | injection reachability and allowlist adequacy |
| Audit trail and SOX evidence | `static.java.spotbugs`, `static.common.report-consistency` | audit completeness and immutability intent |
| Privacy and retention | `static.common.report-consistency` | erasure feasibility and retention basis |

## LLM Gap Review

Use `context/validators/llm-based-validation.md` for unresolved semantic gaps.

## Evolution Rules

- Re-resolve `route.spring-boot-security` before each validator run.
- Keep framework, persistence, and monetary findings on `validator.spring-boot-api`; do not duplicate them here.
- Update groups when the institution's compliance regime changes source obligations in `ESTD21`.
- Keep route binding aligned with `route.spring-boot-security`.
