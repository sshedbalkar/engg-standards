# ESTD21 - Data Protection, Security and Audit Standards for Spring Boot Banking Services

**ESTD21 — Data Protection, Security and Audit Standards**

| Field | Value |
|:----- |:----- |
| Document ID | ESTD21 |
| Version | 1.0 |
| Status | Draft |
| Last Updated | 2026-09-02 |
| Applies To | Spring Boot 3.3+ / Java 21 services handling customer, account, payment, or card data |
| Depends On | [ESTD20](./ESTD20_-_Spring_Boot_Framework_Standards.md#estd20---spring-boot-framework-standards-for-banking-services) |
| Approval | Director of Engineering / Security Architect |

---

> **📋 Living Document Notice** This document is a work in progress and will evolve as our systems, practices, and understanding mature. Feedback, questions, and suggestions are welcome — please submit them via comments on the corresponding Confluence page. However, the standards defined herein **must be strictly followed** in all active work. Any exception requires **explicit written approval** from the Director of Engineering or the appropriate Architect, and must be documented in the PR description, the exception log, or the relevant Confluence page.

---

## How to Use This Document

ESTD21 covers everything about protecting data and proving what happened to it: trust boundaries, authentication, authorization, encryption, masking, tokenization, secrets, injection defence, rate limiting, audit trail, privacy compliance, and incident response.

Read [ESTD20](./ESTD20_-_Spring_Boot_Framework_Standards.md#estd20---spring-boot-framework-standards-for-banking-services) first. ESTD20 defines the framework structure this document assumes: layering, configuration, transactions, and the ledger model. ESTD21 does not restate those rules; it adds the protection layer over them.

**These rules are not advisory.** Several map directly to obligations under the Payment Card Industry Data Security Standard (PCI DSS) 4.0, the General Data Protection Regulation (GDPR) and Digital Personal Data Protection (DPDP) regimes, and the Sarbanes-Oxley Act (SOX). A deviation is not a code-review preference — it is a finding, and in some cases a reportable one. Exceptions require written approval from the Security Architect and must be recorded in the exception log with a compensating control and a review date.

**Regulatory note**: this document encodes the engineering controls. It does not replace the institution's own compliance policy, its Data Protection Officer's determinations, or its PCI assessor's scoping decisions. Where they differ, they win, and this document is updated.

---

## Table of Contents

- [ESTD21 - Data Protection, Security and Audit Standards for Spring Boot Banking Services](#estd21---data-protection-security-and-audit-standards-for-spring-boot-banking-services)
  - [How to Use This Document](#how-to-use-this-document)
  - [Table of Contents](#table-of-contents)
  - [1. Purpose and Scope](#1-purpose-and-scope)
  - [2. Trust Boundaries and Threat Model](#2-trust-boundaries-and-threat-model)
    - [2.1 The Boundaries](#21-the-boundaries)
    - [2.2 Rules That Follow From the Boundaries](#22-rules-that-follow-from-the-boundaries)
    - [2.3 Assume Breach](#23-assume-breach)
  - [3. Authentication — OAuth2 Resource Server](#3-authentication--oauth2-resource-server)
    - [3.1 The Service Validates the Token Itself](#31-the-service-validates-the-token-itself)
    - [3.2 Decoder Configuration](#32-decoder-configuration)
    - [3.3 Token Handling Rules](#33-token-handling-rules)
    - [3.4 Extracting the Principal](#34-extracting-the-principal)
  - [4. Authorization](#4-authorization)
    - [4.1 Deny by Default](#41-deny-by-default)
    - [4.2 Authorize at the Service Layer](#42-authorize-at-the-service-layer)
    - [4.3 Scopes and Roles](#43-scopes-and-roles)
    - [4.4 Ownership Checks Are Mandatory](#44-ownership-checks-are-mandatory)
    - [4.5 Four-Eyes Approval for High-Risk Operations](#45-four-eyes-approval-for-high-risk-operations)
  - [5. Transport and Endpoint Security](#5-transport-and-endpoint-security)
    - [5.1 TLS](#51-tls)
    - [5.2 Security Headers](#52-security-headers)
    - [5.3 CORS](#53-cors)
    - [5.4 CSRF](#54-csrf)
    - [5.5 Actuator Exposure](#55-actuator-exposure)
  - [6. Data Classification](#6-data-classification)
    - [6.1 Enforcing Classification in Code](#61-enforcing-classification-in-code)
  - [7. Data at Rest](#7-data-at-rest)
    - [7.1 Layered Encryption](#71-layered-encryption)
    - [7.2 Envelope Encryption](#72-envelope-encryption)
    - [7.3 Searchability](#73-searchability)
    - [7.4 Key Rotation](#74-key-rotation)
    - [7.5 Backups](#75-backups)
  - [8. Data in Transit and In Use](#8-data-in-transit-and-in-use)
    - [8.1 The Logging Prohibition](#81-the-logging-prohibition)
    - [8.2 Defence at the Serialization Layer](#82-defence-at-the-serialization-layer)
    - [8.3 Never in a URL](#83-never-in-a-url)
    - [8.4 Traces and Metrics Follow the Same Rules](#84-traces-and-metrics-follow-the-same-rules)
    - [8.5 Error Responses](#85-error-responses)
  - [9. Masking and Tokenization](#9-masking-and-tokenization)
    - [9.1 PAN Masking](#91-pan-masking)
    - [9.2 Account Number and IBAN Masking](#92-account-number-and-iban-masking)
    - [9.3 Tokenization](#93-tokenization)
    - [9.4 Never Stored, Under Any Circumstances](#94-never-stored-under-any-circumstances)
  - [10. Secrets Management](#10-secrets-management)
    - [10.1 Where Secrets Come From](#101-where-secrets-come-from)
    - [10.2 Rotation](#102-rotation)
    - [10.3 Detection](#103-detection)
    - [10.4 Secrets in Memory and Heap Dumps](#104-secrets-in-memory-and-heap-dumps)
  - [11. Input Security](#11-input-security)
    - [11.1 Parameterized Queries Only](#111-parameterized-queries-only)
    - [11.2 Dynamic Sorting and Field Selection](#112-dynamic-sorting-and-field-selection)
    - [11.3 Path Traversal](#113-path-traversal)
    - [11.4 Server-Side Request Forgery](#114-server-side-request-forgery)
    - [11.5 XML External Entities](#115-xml-external-entities)
    - [11.6 Java Deserialization Is Prohibited](#116-java-deserialization-is-prohibited)
    - [11.7 File Uploads](#117-file-uploads)
    - [11.8 Mass Assignment](#118-mass-assignment)
  - [12. Rate Limiting and Abuse Prevention](#12-rate-limiting-and-abuse-prevention)
    - [12.1 Limits](#121-limits)
    - [12.2 Behaviour](#122-behaviour)
    - [12.3 Enumeration Resistance](#123-enumeration-resistance)
  - [13. Audit Trail](#13-audit-trail)
    - [13.1 What Must Be Audited](#131-what-must-be-audited)
    - [13.2 Record Structure](#132-record-structure)
    - [13.3 The Audit Trail Is Append-Only at the Database](#133-the-audit-trail-is-append-only-at-the-database)
    - [13.4 Tamper Evidence](#134-tamper-evidence)
    - [13.5 Audit Writes Must Survive a Business Rollback](#135-audit-writes-must-survive-a-business-rollback)
    - [13.6 Retention](#136-retention)
  - [14. Privacy Compliance (GDPR / DPDP)](#14-privacy-compliance-gdpr--dpdp)
    - [14.1 Principles as Engineering Rules](#141-principles-as-engineering-rules)
    - [14.2 Data Subject Rights](#142-data-subject-rights)
    - [14.3 Erasure Versus the Immutable Ledger](#143-erasure-versus-the-immutable-ledger)
    - [14.4 Retention Schedule](#144-retention-schedule)
    - [14.5 Cross-Border Transfer](#145-cross-border-transfer)
    - [14.6 Consent](#146-consent)
  - [15. PCI DSS 4.0 Scope Management](#15-pci-dss-40-scope-management)
    - [15.1 What Puts a Service in Scope](#151-what-puts-a-service-in-scope)
    - [15.2 Stay Out of Scope](#152-stay-out-of-scope)
    - [15.3 If a Service Must Be In Scope](#153-if-a-service-must-be-in-scope)
  - [16. Session, Token and Credential Handling](#16-session-token-and-credential-handling)
    - [16.1 Token Lifetimes](#161-token-lifetimes)
    - [16.2 Revocation](#162-revocation)
    - [16.3 Credential Storage](#163-credential-storage)
    - [16.4 Step-Up Authentication](#164-step-up-authentication)
  - [17. Security Testing and Verification](#17-security-testing-and-verification)
    - [17.1 Automated Gates](#171-automated-gates)
    - [17.2 Security Tests Are Written, Not Assumed](#172-security-tests-are-written-not-assumed)
    - [17.3 Manual Review Checkpoints](#173-manual-review-checkpoints)
    - [17.4 Penetration Testing](#174-penetration-testing)
  - [18. Incident Response Hooks](#18-incident-response-hooks)
    - [18.1 What the Application Must Provide](#181-what-the-application-must-provide)
    - [18.2 Alertable Security Events](#182-alertable-security-events)
    - [18.3 Breach Notification Clocks](#183-breach-notification-clocks)
    - [18.4 Evidence Preservation](#184-evidence-preservation)
  - [19. Common Pitfalls to Avoid](#19-common-pitfalls-to-avoid)

---

## 1. Purpose and Scope

**Why this document exists**: the framework rules in ESTD20 produce a correct service. They do not produce a safe one. A service can be perfectly transactional, perfectly reconciled, and still expose every customer's account number in a log file, accept an unsigned token, or let one customer read another's statement because an ownership check was written as a comment.

The failures this document prevents are specific:

- A JSON Web Token (JWT) accepted without validating its audience, so a token minted for a different application authenticates against this one.
- An endpoint that loads a resource by id and checks ownership afterwards — or not at all — so changing one digit in a URL returns another customer's data.
- `log.info("payload={}", request)` on a payment endpoint, writing full card numbers into a log aggregator that half the company can query.
- A `Sort` built from a request parameter, turning a query into an injection point.
- An audit table with an `UPDATE` grant, so the record of who did what is editable by the thing being audited.
- A right-to-erasure request that cannot be honoured because personal data was written into an immutable ledger.

**In scope**: trust boundaries, OAuth2 resource server authentication, authorization and ownership, transport and endpoint security, data classification, encryption at rest, data in transit and in use, masking and tokenization, secrets management, input and injection security, rate limiting, audit trail, GDPR/DPDP compliance, PCI DSS 4.0 scope management, token and credential handling, security testing, and incident response hooks.

**Out of scope**: network segmentation, host hardening, web application firewall (WAF) configuration, identity provider (IdP) administration, and key management infrastructure. These are platform responsibilities. This document specifies what the application must assume about them and what it must do with what they provide.

---

## 2. Trust Boundaries and Threat Model

### 2.1 The Boundaries

```
   ┌─────────────────────────────────────────────────────────────────┐
   │  UNTRUSTED                                                      │
   │  Mobile app · web app · third-party TPP · partner integration   │
   └───────────────────────────┬─────────────────────────────────────┘
                               │  TLS 1.2+, bearer token
   ════════════════════════════╪══════════ TRUST BOUNDARY 1 ═════════
                               │  Edge: WAF, rate limit, TLS termination
   ┌───────────────────────────▼─────────────────────────────────────┐
   │  SEMI-TRUSTED — the API gateway has authenticated, not authorized│
   └───────────────────────────┬─────────────────────────────────────┘
                               │
   ════════════════════════════╪══════════ TRUST BOUNDARY 2 ═════════
                               │  The service validates the token ITSELF
   ┌───────────────────────────▼─────────────────────────────────────┐
   │  APPLICATION                                                     │
   │   ├─ Authentication  — is the token valid, for THIS audience?    │
   │   ├─ Authorization   — may this subject perform this action?     │
   │   ├─ Ownership       — does this subject own THIS resource?      │
   │   └─ Validation      — is the input well-formed and in bounds?   │
   └───────────────────────────┬─────────────────────────────────────┘
                               │
   ════════════════════════════╪══════════ TRUST BOUNDARY 3 ═════════
                               │  Least-privilege database role
   ┌───────────────────────────▼─────────────────────────────────────┐
   │  DATA — encrypted at rest, append-only ledger, audit trail       │
   └──────────────────────────────────────────────────────────────────┘
```

### 2.2 Rules That Follow From the Boundaries

- **The service authenticates independently.** It never trusts a header the gateway claims to have validated. A header such as `X-Authenticated-User` is client input unless it arrives over a channel the service itself authenticated. If the gateway is compromised or bypassed, header-based trust is a total authentication failure.
- **Authentication is not authorization, and authorization is not ownership.** All three checks are separate, and all three are mandatory on every resource-accessing endpoint.
- **Client-side checks are user-interface behaviour, never enforcement.** Every rule enforced in the mobile app is enforced again in the service, because the app is under the attacker's control.
- **Every trust boundary crossing revalidates.** Data that was validated on the way in is validated again if it leaves and returns — a value round-tripped through the client is not the value that was sent.
- **Least privilege at every layer.** The service's database role can do exactly what the service needs and nothing more; see [§13.3](#133-the-audit-trail-is-append-only-at-the-database).

### 2.3 Assume Breach

Design so that a single failure is not a total failure:

| If this is compromised | It must not yield |
|:-----------------------|:------------------|
| One access token | Anything beyond that customer's own data, for the token's short lifetime |
| The application log store | Any account number, card number (Primary Account Number, PAN), credential, or identifiable customer record |
| A database backup | Readable card data or unencrypted personally identifiable information (PII) — encryption keys live elsewhere |
| One service's database role | Write access to another service's schema, or any grant on the audit and ledger tables |
| A heap dump | A long-lived secret — secrets are held as `char[]` and cleared, never as interned `String` constants |

---

## 3. Authentication — OAuth2 Resource Server

### 3.1 The Service Validates the Token Itself

Every service is an OAuth2 Resource Server. It validates the JWT presented on each request against the institution's identity provider — signature, issuer, audience, expiry, and algorithm — on every request, with no exception for internal callers.

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http,
                                           JwtAuthenticationConverter converter) throws Exception {
        return http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/actuator/health/**").permitAll()
                .anyRequest().authenticated())               // DENY BY DEFAULT
            .oauth2ResourceServer(oauth -> oauth
                .jwt(jwt -> jwt.jwtAuthenticationConverter(converter)))
            .sessionManagement(session -> session
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .csrf(AbstractHttpConfigurer::disable)           // Justified in section 5.4
            .headers(headers -> headers
                .httpStrictTransportSecurity(hsts -> hsts
                    .includeSubDomains(true)
                    .maxAgeInSeconds(31_536_000))
                .contentSecurityPolicy(csp -> csp
                    .policyDirectives("default-src 'none'; frame-ancestors 'none'"))
                .frameOptions(FrameOptionsConfig::deny)
                .referrerPolicy(referrer -> referrer
                    .policy(ReferrerPolicy.NO_REFERRER)))
            .build();
    }
}
```

`.anyRequest().authenticated()` is the last matcher, always. An endpoint added later is protected by default rather than exposed by default. A `permitAll()` after it would make everything public — matcher order is evaluated top to bottom and the first match wins.

### 3.2 Decoder Configuration

The defaults are not sufficient. Configure the decoder explicitly:

```java
@Bean
public JwtDecoder jwtDecoder(OAuth2ResourceServerProperties properties,
                             SecurityProperties securityProperties) {

    NimbusJwtDecoder decoder = NimbusJwtDecoder
        .withJwkSetUri(properties.getJwt().getJwkSetUri())
        .jwsAlgorithms(algorithms -> {
            algorithms.clear();                     // Drop every default
            algorithms.add(SignatureAlgorithm.RS256);
            algorithms.add(SignatureAlgorithm.ES256);
        })
        .build();

    decoder.setJwtValidator(new DelegatingOAuth2TokenValidator<>(
        new JwtTimestampValidator(Duration.ofSeconds(30)),          // Bounded clock skew
        new JwtIssuerValidator(securityProperties.issuerUri()),
        new JwtClaimValidator<List<String>>("aud",
            audiences -> audiences != null && audiences.contains(securityProperties.audience())),
        new JwtClaimValidator<String>("sub", Objects::nonNull),
        new JwtClaimValidator<Instant>("iat", Objects::nonNull)));

    return decoder;
}
```

Each line prevents a specific attack:

| Control | Attack Prevented |
|:--------|:-----------------|
| Explicit algorithm allowlist | `alg: none` acceptance; RS256-to-HS256 confusion — an asymmetric signature swapped for a symmetric one — where the public key is used as a hash-based message authentication code (HMAC) secret |
| Issuer validation | A token from a different, attacker-controlled issuer |
| **Audience validation** | A valid token minted for a different application in the same estate being replayed here |
| Bounded clock skew (30 s) | An expired token accepted because of a generous skew allowance |
| Signature via the JSON Web Key Set (JWKS) | A forged or unsigned token |

**Audience validation is the one most often omitted and the one that matters most in a multi-application estate.** Without it, any service that trusts the same issuer accepts any token the issuer ever minted, including one obtained from a low-value application.

### 3.3 Token Handling Rules

- **Never in a URL path or query string.** URLs are logged by every proxy, load balancer, and browser history along the way. The token goes in the `Authorization: Bearer` header, always.
- **Never logged.** Not at `DEBUG`, not in a request dump, not in an exception message.
- **Never persisted** by the service. A resource server validates and discards.
- **Access token lifetime: 15 minutes or less.** Refresh handling is the identity provider's concern; see [§16](#16-session-token-and-credential-handling).
- **Never in `localStorage`** in a browser client — that is readable by cross-site scripting (XSS). This is a client-side rule the service cannot enforce, so it is stated in the API contract and verified at integration review.
- **JWKS is cached with a bounded time-to-live (TTL) and a refresh on unknown `kid`.** Fetching JWKS per request is a denial-of-service vector against your own identity provider; caching forever breaks key rotation.

### 3.4 Extracting the Principal

```java
public record CustomerPrincipal(UUID customerId, Set<String> scopes, String tokenId) { }

@Component
public class CustomerPrincipalResolver implements HandlerMethodArgumentResolver {

    @Override
    public Object resolveArgument(MethodParameter parameter, ...) {
        Jwt jwt = (Jwt) SecurityContextHolder.getContext().getAuthentication().getPrincipal();

        // The customer id comes from the validated token, NEVER from a request parameter
        String subject = jwt.getSubject();
        if (subject == null || subject.isBlank()) {
            throw new InvalidTokenException("Token has no subject claim");
        }
        return new CustomerPrincipal(
            UUID.fromString(subject),
            Set.copyOf(jwt.getClaimAsStringList("scope")),
            jwt.getId());
    }
}
```

**The acting customer's identity always comes from the validated token, never from the request.**

```java
// CATASTROPHIC — the caller states who they are
@GetMapping("/accounts")
public List<AccountResponse> list(@RequestParam UUID customerId) { ... }

// GOOD — identity comes from the token
@GetMapping("/accounts")
public List<AccountResponse> list(@AuthenticationPrincipal CustomerPrincipal principal) { ... }
```

An operation performed *on behalf of* another party — a staff user acting for a customer — is a distinct, separately authorized operation with its own scope, its own audit record naming both parties, and its own approval requirement. It is never a customer-id parameter.

---

## 4. Authorization

### 4.1 Deny by Default

Access is denied unless a rule grants it. Every new endpoint is protected the moment it exists, before anyone remembers to secure it.

```java
@Configuration
@EnableMethodSecurity                    // Enables @PreAuthorize / @PostAuthorize
public class MethodSecurityConfig { }
```

### 4.2 Authorize at the Service Layer

Controller-level rules protect a URL. Service-level rules protect an operation, and the operation is what actually matters — the same service method may be reachable from a controller, a scheduled job, a message consumer, and a batch step.

```java
@Service
public class TransferService {

    @PreAuthorize("hasAuthority('SCOPE_payments:write')")
    @Transactional(timeout = 5)
    public TransferResult execute(CustomerId customerId, TransferCommand command, IdempotencyKey key) {
        ...
    }
}
```

`@PreAuthorize` is proxy-based, so [ESTD20 §10.2](./ESTD20_-_Spring_Boot_Framework_Standards.md#102-the-self-invocation-trap) applies: a self-invocation bypasses it entirely. Method security on a method called from within the same bean is not enforced.

### 4.3 Scopes and Roles

| Kind | Answers | Example |
|:-----|:--------|:--------|
| Scope | What is the *client application* permitted to request | `SCOPE_payments:write`, `SCOPE_accounts:read` |
| Role | What is the *user* permitted to do | `ROLE_CUSTOMER`, `ROLE_BRANCH_OFFICER`, `ROLE_OPS_SUPERVISOR` |

Both are checked where both apply. A branch officer using an application without the payments scope cannot initiate a payment, and an application with the scope cannot act for a user who lacks the role.

Scope naming is `resource:action` and is granular. A single `SCOPE_banking` grants everything and makes least privilege impossible.

### 4.4 Ownership Checks Are Mandatory

Authorization says the caller may perform the action. It does not say they may perform it on *this* resource. Broken object-level authorization is consistently the most exploited API vulnerability, and it is trivially avoidable.

```java
// CATASTROPHIC — any authenticated customer can read any account by changing the id
@GetMapping("/{accountId}")
@PreAuthorize("hasAuthority('SCOPE_accounts:read')")
public AccountResponse get(@PathVariable UUID accountId) {
    return AccountResponse.from(accountRepository.findById(accountId).orElseThrow());
}
```

**Ownership belongs in the query, not in an `if` after the query.** A check written as a separate statement can be forgotten, reordered, or bypassed by a new code path. A query that cannot return another customer's row cannot leak one.

```java
// GOOD — the constraint is structural
@GetMapping("/{accountId}")
@PreAuthorize("hasAuthority('SCOPE_accounts:read')")
public AccountResponse get(@PathVariable UUID accountId,
                           @AuthenticationPrincipal CustomerPrincipal principal) {

    Account account = accountRepository
        .findByIdAndCustomerId(accountId, principal.customerId())
        .orElseThrow(() -> new AccountNotFoundException(ApiErrorCode.ACCOUNT_NOT_FOUND, "…"));

    return AccountResponse.from(account);
}
```

**Return 404, never 403, for a resource the caller does not own.** A 403 confirms that the account exists, which lets an attacker enumerate valid account identifiers. A 404 is indistinguishable from a resource that never existed.

Identifiers exposed to clients are **opaque UUIDs**, never sequential integers and never the account number itself. A sequential id invites enumeration; an account number in a URL is regulated data in a log.

### 4.5 Four-Eyes Approval for High-Risk Operations

Some operations must not be completable by one person. SOX segregation-of-duties expects this, and it is the control that stops a single compromised staff account from doing unbounded damage.

Operations requiring a second, different approver:

- A transfer above the institution's defined threshold
- Any manual ledger adjustment or correction
- Changing a customer's registered contact details followed by a payment (the classic takeover sequence)
- Adding a payee outside the standard cooling-off window
- Any change to limits, fees, or interest rates
- Any bulk or batch operation affecting more than a configured number of accounts

```java
@Service
public class MakerCheckerService {

    @Transactional
    public void approve(UUID requestId, StaffPrincipal approver) {

        ApprovalRequest request = approvalRepository.findByIdForUpdate(requestId)
            .orElseThrow(() -> new ApprovalRequestNotFoundException(...));

        // The maker can never be the checker. Enforced here AND by a database constraint.
        if (request.makerId().equals(approver.staffId())) {
            auditService.record(AuditEvent.selfApprovalAttempt(request, approver));
            throw new SelfApprovalProhibitedException(
                ApiErrorCode.SELF_APPROVAL_PROHIBITED, "The maker cannot approve their own request");
        }
        if (request.isExpired(clock)) {
            throw new ApprovalExpiredException(...);
        }

        request.approve(approver.staffId(), Instant.now(clock));
        auditService.record(AuditEvent.approved(request, approver));
    }
}
```

```sql
ALTER TABLE approval_request
    ADD CONSTRAINT ck_approval_maker_not_checker
    CHECK (checker_id IS NULL OR checker_id <> maker_id);
```

A rejected self-approval attempt is itself an audited security event. It is one of the strongest early signals of a compromised staff account.

---

## 5. Transport and Endpoint Security

### 5.1 TLS

- **Transport Layer Security (TLS) 1.2 minimum; TLS 1.3 preferred.** TLS 1.0 and 1.1 are disabled — PCI DSS 4.0 requires it and they are broken independently of that.
- **HTTP is never served.** Not for a redirect, not for a health check, not in any environment.
- Certificate validation is never disabled. A "temporary" trust-all `TrustManager` in a client is prohibited outright; it has an unbroken record of surviving into production.

### 5.2 Security Headers

Set in the filter chain shown in [§3.1](#31-the-service-validates-the-token-itself):

| Header | Value | Prevents |
|:-------|:------|:---------|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | Protocol downgrade, Secure Sockets Layer (SSL) stripping |
| `X-Content-Type-Options` | `nosniff` | Multipurpose Internet Mail Extensions (MIME) confusion leading to script execution |
| `X-Frame-Options` | `DENY` | Clickjacking |
| `Content-Security-Policy` | `default-src 'none'; frame-ancestors 'none'` | Injection surface on an API that serves no markup |
| `Cache-Control` | `no-store` on every response carrying customer data | Sensitive responses cached by a proxy or the browser |
| `Referrer-Policy` | `no-referrer` | Identifiers leaking through the referrer header |

`Cache-Control: no-store` on customer data endpoints is not optional. A cached statement response served to the next user of a shared device is a disclosure.

### 5.3 CORS

Cross-Origin Resource Sharing (CORS) is the browser-enforced rule set deciding which other origins may call this API from a page. It constrains browsers only — a non-browser client ignores it — so it is a defence for the customer's browser session, never an authorization control.

```java
@Bean
public CorsConfigurationSource corsConfigurationSource(WebProperties properties) {
    CorsConfiguration config = new CorsConfiguration();
    config.setAllowedOrigins(properties.allowedOrigins());     // Explicit list from config
    config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE"));
    config.setAllowedHeaders(List.of("Authorization", "Content-Type", "Idempotency-Key",
                                     "X-Correlation-Id"));
    config.setAllowCredentials(true);
    config.setMaxAge(3600L);

    UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    source.registerCorsConfiguration("/api/**", config);
    return source;
}
```

**`allowedOrigins("*")` is prohibited**, and combining a wildcard with `allowCredentials(true)` is prohibited absolutely — it is rejected by browsers and by any review. `allowedOriginPatterns` with a wildcard is the same mistake wearing a different method name. Origins are an explicit, environment-specific list.

### 5.4 CSRF

Cross-site request forgery (CSRF) protection is disabled **only** because the API is stateless and authenticates exclusively via the `Authorization` header, which a browser does not attach automatically to a cross-site request. That justification is recorded here so a future reader does not assume it was an oversight.

If any endpoint ever authenticates via a cookie, CSRF protection becomes mandatory for it immediately. The two decisions are linked; changing one without the other is a vulnerability.

### 5.5 Actuator Exposure

```yaml
management:
  server:
    port: 9090                      # Separate port, never routed publicly
  endpoints:
    web:
      exposure:
        include: health,info,prometheus,metrics      # Explicit allowlist
  endpoint:
    health:
      show-details: when-authorized
      probes:
        enabled: true
  info:
    env:
      enabled: false                # Would expose configuration
    git:
      mode: simple                  # Commit id only, never the full build environment
```

- **`include: "*"` is prohibited.** It exposes `/actuator/env` (every configuration value, including anything the masking heuristic misses), `/actuator/heapdump` (the full heap, containing customer data in memory), `/actuator/threaddump`, `/actuator/loggers` (log level mutation), and `/actuator/mappings`.
- **`/actuator/heapdump` and `/actuator/env` are never exposed over HTTP in any environment.** A heap dump from a banking service is a complete disclosure of everything in memory.
- The management port is bound to the internal network only and is never reachable from the ingress.

---

## 6. Data Classification

Every field this service handles falls into one of these classes. The class determines what may be done with it. When in doubt, classify upward.

| Class | Examples | Storage | Logging | Response | Retention |
|:------|:---------|:--------|:--------|:---------|:----------|
| **Prohibited** | Card Verification Value or Code (CVV/CVC), Personal Identification Number (PIN), full magnetic-stripe or chip track data, private keys | **Never stored, in any form, encrypted or not** | Never | Never | N/A |
| **Restricted** | PAN (card number), credentials, authentication tokens, national identifier | Encrypted or tokenized; PAN only if unavoidable and in a PCI-scoped store | Never | Masked only | Minimum required by regulation |
| **Confidential** | Account number, International Bank Account Number (IBAN), balance, transaction detail, date of birth, address | Encrypted at rest; access controlled | Never in full; internal ids only | Masked unless the endpoint's purpose requires full | Per retention schedule |
| **Internal** | Internal UUIDs, correlation ids, error codes, product codes, feature flags | Standard | Yes | Yes | Standard |
| **Public** | Currency codes, branch directory, product catalogue, fee schedules | Standard | Yes | Yes | Standard |

### 6.1 Enforcing Classification in Code

Classification that lives only in a table is classification that gets forgotten. Mark it in the type system:

```java
@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.FIELD, ElementType.RECORD_COMPONENT})
public @interface Sensitive {
    DataClass value();
    boolean maskInResponses() default true;
}

public record CardDetails(
    @Sensitive(DataClass.RESTRICTED)
    String pan,

    @Sensitive(DataClass.CONFIDENTIAL)
    String cardholderName,

    // CVV has no field. It is never held in a domain object, DTO, entity, or log.
    YearMonth expiry
) {
    @Override
    public String toString() {
        // MANDATORY on every type carrying restricted or confidential data
        return "CardDetails[pan=" + PanMasker.mask(pan) + ", expiry=" + expiry + "]";
    }
}
```

An architecture test asserts that every field annotated `@Sensitive` is either excluded from serialization or routed through a masking serializer, so a new field cannot silently reach a response body.

---

## 7. Data at Rest

### 7.1 Layered Encryption

```
┌──────────────────────────────────────────────────────────┐
│ Layer 3 — Application-level column encryption            │
│           PAN, national identifier, credentials.         │
│           Protects against a DBA, a leaked backup, and   │
│           a SQL-injection read.                          │
├──────────────────────────────────────────────────────────┤
│ Layer 2 — Database transparent encryption (TDE)          │
│           Protects the files on disk. Does NOT protect   │
│           against anything with a valid connection.      │
├──────────────────────────────────────────────────────────┤
│ Layer 1 — Volume / storage encryption                    │
│           Protects a stolen or decommissioned disk.      │
└──────────────────────────────────────────────────────────┘
```

Layers 1 and 2 are platform responsibilities and are mandatory. **Layer 3 is the application's responsibility**, and it is the only layer that protects data from someone who has legitimate database access or has obtained a connection.

### 7.2 Envelope Encryption

Data keys encrypt data. A master key in the institution's key management service (KMS) or hardware security module (HSM) encrypts the data keys. The master key never leaves the KMS.

```
   plaintext ──[ AES-256-GCM with data key ]──▶ ciphertext ─┐
                                                            ├─▶ stored together
   data key ──[ encrypted by KMS master key ]──▶ wrapped key┘
```

This makes key rotation tractable: rotating the master key re-wraps the data keys, which is cheap, rather than re-encrypting every row, which is not.

```java
@Converter
public class EncryptedStringConverter implements AttributeConverter<String, String> {

    private final CryptoService cryptoService;   // Wraps the KMS client

    @Override
    public String convertToDatabaseColumn(String plaintext) {
        if (plaintext == null) {
            return null;
        }
        // AES-256-GCM: authenticated encryption. A random IV per value, never reused.
        return cryptoService.encrypt(plaintext, KeyPurpose.PII);
    }

    @Override
    public String convertToEntityAttribute(String ciphertext) {
        return ciphertext == null ? null : cryptoService.decrypt(ciphertext);
    }
}
```

```java
@Entity
public class Customer {

    @Convert(converter = EncryptedStringConverter.class)
    @Column(name = "national_id_encrypted", length = 512)
    private String nationalId;

    // Blind index: deterministic HMAC of the normalized value, for equality lookup only
    @Column(name = "national_id_index", length = 64)
    private String nationalIdIndex;
}
```

Requirements, each of which is a real failure mode when omitted:

- **AES-256-GCM** — the Advanced Encryption Standard (AES) in Galois/Counter Mode (GCM) — not Cipher Block Chaining (CBC). GCM is authenticated; CBC without a separate message authentication code (MAC) is malleable and has a long history of padding-oracle attacks.
- **A fresh random initialization vector (IV) for every encryption.** IV reuse under GCM is catastrophic — it leaks the authentication key, not just the plaintext.
- **The key identifier is stored with the ciphertext** so a rotated key can still decrypt historical rows.
- **Keys are never in application configuration, environment variables, or source.** They come from the KMS at runtime.

### 7.3 Searchability

Randomized encryption produces different ciphertext for the same plaintext, which is what you want and which makes `WHERE national_id = ?` impossible. Do not solve this by switching to deterministic encryption for the whole column — that leaks equality across the entire dataset and enables frequency analysis.

Solve it with a **blind index**: a keyed HMAC of the normalized value, stored in a separate indexed column.

```java
public String blindIndex(String value) {
    String normalized = value.trim().toUpperCase(Locale.ROOT);
    return HexFormat.of().formatHex(
        hmacSha256(normalized, blindIndexKey));     // A separate key from the encryption key
}
```

This supports exact-match lookup and nothing else — no range queries, no prefix search, no ordering. That limitation is the point. If a use case needs range queries over restricted data, it needs a design review, not a weaker cipher.

### 7.4 Key Rotation

| Key | Rotation | On Compromise |
|:----|:---------|:--------------|
| KMS master key | Annually, or per the institution's policy | Immediately; re-wrap all data keys |
| Data encryption keys | Per the KMS policy, typically annually | Immediately; re-encrypt affected data |
| Blind index key | Rarely — rotation requires rebuilding the index column | Rebuild the index column offline |
| JWT signing keys | Identity provider's schedule | Identity provider revokes; services refresh JWKS |

Rotation is tested in a non-production environment before it is scheduled in production. An untested rotation procedure is not a procedure.

### 7.5 Backups

Backups carry the same classification as the data. They are encrypted, access-controlled, and their restore procedure is tested on a schedule. **A backup encrypted with a key stored alongside it is not encrypted.** Restore testing must include verifying that decryption works with the current key hierarchy — a restore that cannot be decrypted is not a backup.

---

## 8. Data in Transit and In Use

### 8.1 The Logging Prohibition

This is the single most frequently violated rule in this document, and the violation is usually one line long.

**Never log:**

- Full account numbers, IBANs, card numbers, sort codes with account numbers
- CVV, PIN, passwords, tokens, API keys, `Authorization` header contents
- Customer names, addresses, dates of birth, national identifiers, email addresses, phone numbers
- Balances or amounts alongside anything that identifies a customer
- Full request or response bodies on any endpoint carrying customer data
- Query parameters on any endpoint carrying customer data
- Exception messages or stack traces that embed any of the above

```java
// CATASTROPHIC — this one line puts regulated data in the log store permanently
log.info("Processing transfer request: {}", request);

// CATASTROPHIC — the exception message contains the account number
log.error("Transfer failed for account " + accountNumber, e);

// GOOD — internal identifiers only
log.info("Transfer accepted. transferId={}, debitAccountId={}, rail={}",
         transferId, debitAccountId, rail);
```

**Logs are hard to unwrite.** A log line reaches the aggregator, the index, the backups, and the retention archive within seconds. Removing it means a coordinated purge across all of them, and it is a reportable incident in the meantime.

### 8.2 Defence at the Serialization Layer

Relying on every developer to remember [§8.1](#81-the-logging-prohibition) will fail. Make the safe behaviour automatic.

```java
// Every type carrying restricted or confidential data overrides toString()
public record BankAccount(String accountNumber, String iban, BigDecimal balance) {
    @Override
    public String toString() {
        return "BankAccount[accountNumber=" + AccountNumberMasker.mask(accountNumber) + "]";
    }
}
```

```java
// A Jackson module that masks annotated fields wherever they are serialized
public class SensitiveDataModule extends SimpleModule {
    @Override
    public void setupModule(SetupContext context) {
        context.insertAnnotationIntrospector(new MaskingAnnotationIntrospector());
    }
}
```

**Lombok's `@Data` and `@ToString` are prohibited on any type carrying confidential or restricted data.** They generate a `toString()` over every field, which is how account numbers end up in logs without anyone writing a log statement containing one.

### 8.3 Never in a URL

```
PROHIBITED:  GET /api/v1/accounts?accountNumber=GB29NWBK60161331926819
PROHIBITED:  GET /api/v1/customers/198001011234567/accounts
PROHIBITED:  GET /api/v1/statements?email=customer@example.com

GOOD:        GET /api/v1/accounts/3f2a9c11-8f4e-4c2b-9a10-6d4c2e7b1a55
GOOD:        POST /api/v1/accounts/search   { "iban": "GB29NWBK60161331926819" }
```

URLs are logged by the load balancer, the reverse proxy, the content delivery network (CDN), the browser, and the access log — none of which apply the masking rules the application does.

### 8.4 Traces and Metrics Follow the Same Rules

A distributed-tracing span attribute and a metric tag are as durable and as widely readable as a log line. Span attributes carry internal identifiers only. Metric tags never carry a customer id, account id, or any unbounded value — that is both a privacy problem and a cardinality problem.

### 8.5 Error Responses

Covered by [ESTD20 §8.3](./ESTD20_-_Spring_Boot_Framework_Standards.md#83-the-global-exception-handler): `e.getMessage()` never reaches the client. Restated here because it is a disclosure control, not only an error-handling convention. Exception messages routinely contain account identifiers, SQL fragments, table names, internal hostnames, and library versions.

---

## 9. Masking and Tokenization

### 9.1 PAN Masking

PCI DSS 4.0 permits displaying at most the first six and last four digits of a card number, and only to personnel with a documented business need. Everyone else sees the last four at most.

```java
public final class PanMasker {

    private PanMasker() { }

    /** Default display: last four only. */
    public static String mask(String pan) {
        if (pan == null || pan.length() < 4) {
            return "****";
        }
        return "*".repeat(pan.length() - 4) + pan.substring(pan.length() - 4);
    }

    /** First six and last four. Requires a documented business need and an audit record. */
    public static String maskForAuthorizedPersonnel(String pan) {
        if (pan == null || pan.length() < 10) {
            return mask(pan);
        }
        return pan.substring(0, 6)
             + "*".repeat(pan.length() - 10)
             + pan.substring(pan.length() - 4);
    }
}
```

### 9.2 Account Number and IBAN Masking

```java
// GB29NWBK60161331926819  ->  GB29****************6819
public static String maskIban(String iban) {
    if (iban == null || iban.length() < 8) {
        return "****";
    }
    return iban.substring(0, 4)
         + "*".repeat(iban.length() - 8)
         + iban.substring(iban.length() - 4);
}
```

Masking is applied at the **response mapper**, not at the point of storage. The stored value stays complete because the ledger and the payment rails need it; the boundary decides what leaves.

### 9.3 Tokenization

Tokenization replaces a sensitive value with a surrogate that has no mathematical relationship to it. Unlike encryption, no key held by this service can reverse it.

```
   PAN 4111111111111111
        │
        ▼
   ┌──────────────────────┐
   │ Tokenization service │  (PCI-scoped, separately controlled)
   │  token ⇄ PAN vault   │
   └──────────┬───────────┘
              ▼
   token  tok_9f2b4c8e1a5d7f30
        │
        ▼
   This service stores ONLY the token.
   It is therefore out of PCI DSS scope for card data.
```

**Tokenization is the preferred design for any card data.** A service that never holds a PAN cannot leak one, and it stays outside the cardholder data environment, which removes an entire category of assessment obligation.

### 9.4 Never Stored, Under Any Circumstances

| Data | Rule |
|:-----|:-----|
| CVV / CVC / CVV2 | Never stored after authorization. Not encrypted, not hashed, not "temporarily", not in a log, not in a cache, not in a message payload. |
| PIN or PIN block | Never stored outside a certified HSM. |
| Full magnetic-stripe or chip track data | Never stored after authorization. |
| The private half of any key pair | Never in the application, its config, or its database. HSM or KMS only. |

These are absolute. There is no approval path for an exception, because the prohibition is not ours to waive.

---

## 10. Secrets Management

### 10.1 Where Secrets Come From

Secrets are fetched at startup from the institution's secrets manager, using a workload identity the platform provides. They are held in memory and never written to disk.

**Prohibited, without exception:**

- Secrets in `application.yml`, `application-prod.yml`, or any file in the repository
- Secrets in environment variables set from a committed file, or visible in a container image layer
- Secrets in a Docker image, a build argument, or continuous integration (CI) logs
- Secrets in code, including "temporary" test credentials for a shared environment
- Secrets in a comment, a commit message, or a ticket

```yaml
# PROHIBITED
spring:
  datasource:
    password: Pr0d-P@ssw0rd

# GOOD — resolved at startup from the secrets manager
spring:
  datasource:
    password: ${DB_PASSWORD}          # Injected by the platform from the secrets manager
```

### 10.2 Rotation

Every secret has a rotation schedule, and the application must survive rotation without a restart where the platform supports it.

| Secret | Rotation |
|:-------|:---------|
| Database credentials | 90 days, or per policy |
| Downstream API keys | 90 days |
| Encryption keys | See [§7.4](#74-key-rotation) |
| Any secret after a suspected exposure | Immediately, before investigation completes |

A secret that has ever been committed to version control is compromised permanently and must be rotated, even after the commit is removed. Git history, forks, clones, and CI caches all retain it.

### 10.3 Detection

Secret scanning runs on every commit and on the full history in CI, and it blocks the merge on a finding. A pre-commit hook catches most cases before they reach the remote, which is materially cheaper than rotating afterwards.

### 10.4 Secrets in Memory and Heap Dumps

```java
// Better — a char[] can be cleared; a String cannot
char[] password = secretsManager.fetchPassword();
try {
    dataSource.setPassword(password);
} finally {
    Arrays.fill(password, '\0');
}
```

Java `String` objects are immutable and remain in the heap until collected, so they appear in heap dumps. Where the API permits it, hold secrets as `char[]` and clear them after use.

Heap dumps are regulated data. They are written to encrypted storage with restricted access, retained for the minimum period needed for diagnosis, and deleted afterwards. `/actuator/heapdump` is never exposed ([§5.5](#55-actuator-exposure)).

---

## 11. Input Security

### 11.1 Parameterized Queries Only

```java
// CATASTROPHIC — SQL injection
@Query(value = "SELECT * FROM account WHERE customer_id = '" + customerId + "'",
       nativeQuery = true)

// CATASTROPHIC — string concatenation into a JPQL query
String jpql = "SELECT a FROM Account a WHERE a.status = '" + status + "'";
entityManager.createQuery(jpql, Account.class);

// GOOD — named parameters, bound by the driver
@Query("SELECT a FROM Account a WHERE a.customerId = :customerId AND a.status = :status")
List<Account> findByCustomerAndStatus(@Param("customerId") UUID customerId,
                                      @Param("status") AccountStatus status);
```

There is no acceptable reason to concatenate user input into a query. Dynamic queries use the Criteria API or a query builder, never string assembly.

### 11.2 Dynamic Sorting and Field Selection

Spring Data's `Sort` accepts a property name, and that name reaches the query. A `Sort` built from an unvalidated request parameter is an injection point.

```java
// PROHIBITED — the sort field comes straight from the request
Sort sort = Sort.by(request.getParameter("sortBy"));

// GOOD — an allowlist maps a client-facing token to a known property
private static final Map<String, String> SORTABLE = Map.of(
    "date",   "bookedAt",
    "amount", "amount",
    "status", "status");

Sort sort = Optional.ofNullable(SORTABLE.get(sortBy))
    .map(Sort::by)
    .orElseThrow(() -> new ValidationException("Unsupported sort field"));
```

The same applies to any client-supplied value that becomes a field name, a table name, a projection, or a filter path.

### 11.3 Path Traversal

```java
// PROHIBITED — "../../etc/passwd" reads whatever the process can read
Path file = Path.of(baseDirectory, request.getFilename());

// GOOD — normalize, then verify containment
Path base = Path.of(baseDirectory).toAbsolutePath().normalize();
Path target = base.resolve(request.getFilename()).normalize();
if (!target.startsWith(base)) {
    throw new ValidationException("Invalid file path");
}
```

Generated filenames — a statement PDF, an export — are constructed from internal identifiers, never from client input.

### 11.4 Server-Side Request Forgery

Any outbound URL derived from user input is a server-side request forgery (SSRF) vector: it lets a caller use the service to reach the cloud metadata endpoint, internal admin interfaces, or another service's private port.

```java
public void validateOutboundUrl(URI uri) {
    if (!Set.of("https").contains(uri.getScheme())) {
        throw new ValidationException("Only https is permitted");
    }
    if (!ALLOWED_HOSTS.contains(uri.getHost())) {           // Allowlist, not a blocklist
        throw new ValidationException("Host is not permitted");
    }
    InetAddress address = InetAddress.getByName(uri.getHost());
    if (address.isLoopbackAddress() || address.isSiteLocalAddress()
            || address.isLinkLocalAddress() || address.isAnyLocalAddress()) {
        throw new ValidationException("Internal addresses are not permitted");
    }
}
```

Validate the **resolved address**, not only the hostname — a DNS name under the attacker's control can resolve to a private address. Redirects are not followed automatically on any client that accepts a user-influenced URL.

### 11.5 XML External Entities

XML parsing is avoided where possible. Where a payment or regulatory format requires it, external entity resolution is disabled explicitly:

```java
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
factory.setXIncludeAware(false);
factory.setExpandEntityReferences(false);
```

### 11.6 Java Deserialization Is Prohibited

Deserializing untrusted data with `ObjectInputStream` is a remote code execution vulnerability with a long history of gadget chains in common libraries. It is prohibited outright — in HTTP endpoints, in message consumers, and in cache serialization ([ESTD20 §14.2](./ESTD20_-_Spring_Boot_Framework_Standards.md#142-cache-configuration)).

Use JSON with explicit types. Jackson's polymorphic type handling (`enableDefaultTyping`, `@JsonTypeInfo` over an open hierarchy) reintroduces the same class of vulnerability and is equally prohibited.

### 11.7 File Uploads

| Control | Rule |
|:--------|:-----|
| Size | Hard maximum, enforced by the container before the body is read |
| Type | Verified by content inspection (magic bytes), never by the declared `Content-Type` or the extension |
| Filename | Never used as a path component; the stored name is generated |
| Storage | Outside the web root, on storage with no execute permission |
| Scanning | Malware scanned before any downstream system reads it |
| Serving back | `Content-Disposition: attachment` with a generated filename, never inline |

### 11.8 Mass Assignment

The data transfer object (DTO) defines exactly what a client may set. Binding a request directly onto an entity lets a caller set `status`, `balance`, `customerId`, or `role` by adding a field to the JSON body.

```java
// PROHIBITED — the client controls every settable property of the entity
@PostMapping
public Account create(@RequestBody Account account) { ... }
```

`fail-on-unknown-properties: true` ([ESTD20 §7.4](./ESTD20_-_Spring_Boot_Framework_Standards.md#74-reject-unknown-properties)) rejects the extra field outright, which is the second line of defence behind using a purpose-built request record.

---

## 12. Rate Limiting and Abuse Prevention

### 12.1 Limits

Edge rate limiting is a platform control. The application adds limits the edge cannot express, because it is the only layer that knows the customer identity and the business meaning of an operation.

| Operation | Limit | Why |
|:----------|:------|:----|
| Authentication attempts | 5 per account per 15 minutes, then lockout | Credential stuffing |
| Payment initiation | Per-customer velocity limit, per hour and per day | Automated fraud, account takeover |
| Payee creation | Small daily cap | Bulk mule-account setup |
| Statement or export generation | Low cap; these are expensive | Resource exhaustion |
| Any read endpoint | Generous per-token cap | Scraping, enumeration |
| Password or contact-detail change | Tight cap, plus step-up authentication | Takeover sequence |

### 12.2 Behaviour

```java
if (!rateLimiter.tryAcquire(key)) {
    // 429, with Retry-After. Never a 500, never a silent drop.
    throw new RateLimitExceededException(ApiErrorCode.RATE_LIMITED, retryAfter);
}
```

- Rate limit state is **shared across instances** (Redis or the database). A per-instance limiter multiplies the effective limit by the instance count.
- Limits key on the authenticated subject where one exists, and on the source address only where one does not. Keying solely on address penalizes shared network address translation (NAT) egress and is trivially evaded.
- **Every limit breach is an audited security event** ([§13](#13-audit-trail)). A burst of them is a strong attack signal.
- Responses to a rate-limited caller reveal nothing about the limit's internals beyond `Retry-After`.

### 12.3 Enumeration Resistance

Responses must not let an attacker distinguish "this account exists" from "it does not":

- 404, not 403, for a resource the caller does not own ([§4.4](#44-ownership-checks-are-mandatory))
- Identical response text and, as far as practical, identical timing for "unknown customer" and "wrong credentials"
- No message that confirms an email address, phone number, or account number is registered

---

## 13. Audit Trail

### 13.1 What Must Be Audited

The audit trail answers, under regulatory examination, "who did what, to which record, when, from where, and what changed". If an event cannot be reconstructed from the audit trail, it is not auditable, whatever the logs contain.

| Category | Events |
|:---------|:-------|
| Authentication | Success, failure, lockout, token issuance, step-up challenge and outcome |
| Authorization | Every denied access attempt; every privileged action |
| Money movement | Every transfer, payment, reversal, adjustment, fee, and interest posting |
| Account lifecycle | Open, close, freeze, unfreeze, limit change, product change |
| Customer data | Every read of restricted data, and every change to customer details |
| Staff actions | Every staff action on a customer record, always naming the staff member |
| Four-eyes | Request, approval, rejection, and every self-approval attempt |
| Configuration | Every change to limits, fees, rates, and feature flags affecting money |
| Data subject rights | Every access, rectification, erasure, and portability request and its outcome |

**Reads of restricted data are audited, not only writes.** "Who looked at this customer's records" is a question regulators and internal investigations ask routinely.

### 13.2 Record Structure

```java
@Entity
@Table(name = "audit_event")
public class AuditEvent {

    @Id
    private UUID id;

    @Column(nullable = false, updatable = false)
    private Instant occurredAt;              // WHEN — server clock, UTC

    @Column(nullable = false, updatable = false, length = 64)
    private String actorId;                  // WHO — customer or staff id from the token

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, updatable = false, length = 16)
    private ActorType actorType;             // CUSTOMER, STAFF, SYSTEM, BATCH

    @Column(nullable = false, updatable = false, length = 120)
    private String action;                   // WHAT — TRANSFER_EXECUTED, ACCOUNT_FROZEN

    @Column(nullable = false, updatable = false, length = 64)
    private String resourceType;             // WHICH
    @Column(nullable = false, updatable = false)
    private UUID resourceId;

    @Column(nullable = false, updatable = false, length = 45)
    private String sourceIp;                 // WHERE
    @Column(updatable = false, length = 256)
    private String userAgent;

    @Column(nullable = false, updatable = false, length = 64)
    private String correlationId;            // Ties the audit record to the request

    @Column(updatable = false, columnDefinition = "jsonb")
    private String beforeState;              // Masked. Restricted values NEVER in full.
    @Column(updatable = false, columnDefinition = "jsonb")
    private String afterState;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, updatable = false, length = 16)
    private AuditOutcome outcome;            // SUCCESS, FAILURE, DENIED

    @Column(nullable = false, updatable = false, length = 64)
    private String previousHash;             // Tamper evidence — see 13.4
    @Column(nullable = false, updatable = false, length = 64)
    private String recordHash;
}
```

The audit record obeys the same classification rules as everything else. `beforeState` and `afterState` are masked. An audit trail that records a full PAN has moved the problem, not solved it.

### 13.3 The Audit Trail Is Append-Only at the Database

Application-level immutability is a convention. Database-level immutability is a control.

```sql
-- The application can insert audit records. It cannot alter or remove them.
REVOKE UPDATE, DELETE, TRUNCATE ON audit_event FROM app_write_role;
GRANT  INSERT, SELECT ON audit_event TO app_write_role;

-- Defence in depth: refuse the operation even if a grant is restored by mistake
CREATE OR REPLACE FUNCTION audit_event_is_immutable() RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'audit_event rows are immutable';
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_audit_event_immutable
    BEFORE UPDATE OR DELETE ON audit_event
    FOR EACH ROW EXECUTE FUNCTION audit_event_is_immutable();
```

Retention-period deletion, where the retention schedule requires it, is performed by a separate, privileged, four-eyes-approved process — never by the application role.

### 13.4 Tamper Evidence

Each record's hash covers its own content plus the previous record's hash, forming a chain. Altering or removing any record breaks every hash after it, which a periodic verification job detects.

```java
public String computeHash(AuditEvent event, String previousHash) {
    String canonical = String.join("|",
        event.getId().toString(),
        event.getOccurredAt().toString(),
        event.getActorId(),
        event.getAction(),
        event.getResourceType(),
        event.getResourceId().toString(),
        event.getOutcome().name(),
        previousHash);
    return HexFormat.of().formatHex(sha256(canonical.getBytes(UTF_8)));
}
```

The verification job runs daily, walks the chain, and raises a critical alert on any break. Anchoring the chain head to a separate, append-only store makes the chain resistant to wholesale replacement as well as to individual edits.

### 13.5 Audit Writes Must Survive a Business Rollback

A **denied** or **failed** action must still be audited. If the audit write shares the transaction that rolled back, the record of the attempt disappears — and the attempt is exactly what a security investigation needs.

```java
@Service
public class AuditService {

    // A new transaction: the audit record commits even when the business transaction rolls back
    @Transactional(propagation = Propagation.REQUIRES_NEW, timeout = 5)
    public void record(AuditEvent event) {
        auditRepository.save(event);
    }
}
```

For **successful** money movement, the opposite applies: the audit record must commit with the business change. Use the caller's transaction there, so a committed transfer can never lack its audit record.

**An audit write failure fails the operation.** An action that cannot be audited must not be permitted to complete — that is what "auditable" means.

### 13.6 Retention

| Category | Minimum Retention |
|:---------|:------------------|
| Money movement and ledger | Per the institution's regulatory obligation, typically 7–10 years |
| Authentication and authorization | 2 years minimum |
| Staff actions on customer records | Per SOX and internal policy, typically 7 years |
| Data subject rights requests | Life of the relationship plus the statutory period |

Audit data older than the retention period is archived to immutable storage before it leaves the primary database, never simply deleted.

---

## 14. Privacy Compliance (GDPR / DPDP)

### 14.1 Principles as Engineering Rules

| Principle | What It Means in the Code |
|:----------|:--------------------------|
| Lawful basis | Every personal-data field exists for a recorded, specific reason. A field with no stated purpose is deleted. |
| Data minimisation | Collect only what the purpose requires. "Might be useful later" is not a basis. |
| Purpose limitation | Data collected for payments is not repurposed for marketing without a fresh basis. |
| Accuracy | Correction is a supported operation, not a database ticket. |
| Storage limitation | Every personal-data field has a retention period and an automated expiry. |
| Integrity and confidentiality | [§7](#7-data-at-rest) and [§8](#8-data-in-transit-and-in-use). |
| Accountability | The audit trail is the evidence. |

### 14.2 Data Subject Rights

| Right | Engineering Requirement | Deadline |
|:------|:------------------------|:---------|
| Access | Export everything held about the subject, in a readable format | 30 days |
| Rectification | Correct inaccurate data; the correction is audited | 30 days |
| Erasure | Delete or irreversibly anonymize — subject to legal-retention overrides | 30 days |
| Portability | Structured, machine-readable export | 30 days |
| Restriction | Suspend processing while retaining the data | 30 days |
| Objection | Stop processing on the objected basis | 30 days |

Each of these is an implemented, tested operation with an audit record. A right that is honoured by a manual database script is not honoured reliably and cannot be evidenced.

### 14.3 Erasure Versus the Immutable Ledger

These two obligations appear to conflict:

- GDPR Article 17 gives a data subject the right to erasure.
- Financial regulation requires transaction records to be retained, unaltered, for years.

They are reconciled by **separating personal data from transaction data**, then erasing only the personal data.

```
   ┌─────────────────────────────┐        ┌──────────────────────────────┐
   │ customer (personal data)    │        │ ledger_entry (financial)     │
   │  name, address, DOB,        │        │  account_id, amount,         │
   │  national id, contact       │        │  direction, booked_at        │
   │                             │        │                              │
   │  ERASABLE                   │◀──id───│  RETAINED — no personal data │
   └─────────────────────────────┘        └──────────────────────────────┘

   Erasure removes the personal data. The financial record survives,
   referencing an account id that no longer resolves to an identifiable person.
```

**The ledger must never contain personal data.** No names in a reference field, no addresses in a narrative, no free-text field that a user can put a name into without it being classified and handled accordingly.

**Crypto-shredding** is the mechanism where a record genuinely cannot be deleted: the personal data is encrypted with a per-subject key, and erasure destroys that key. The ciphertext remains — satisfying retention — and is permanently unreadable, satisfying erasure.

```java
@Transactional
public void eraseCustomerData(UUID customerId, ErasureRequest request) {

    // 1. Legal holds and regulatory retention override the erasure request
    if (legalHoldService.isUnderHold(customerId)) {
        throw new ErasureBlockedException("Customer is under a legal hold");
    }
    if (retentionPolicy.isWithinMandatoryPeriod(customerId)) {
        // Restrict processing instead of erasing, and tell the subject why
        customerService.restrictProcessing(customerId);
        auditService.record(AuditEvent.erasureDeferred(customerId, request));
        return;
    }

    // 2. Destroy the per-subject key — all encrypted personal data becomes unreadable
    cryptoService.destroySubjectKey(customerId);

    // 3. Anonymize the fields that are not encrypted
    customerRepository.anonymize(customerId);

    // 4. The ledger is untouched. It contains no personal data by construction.

    // 5. The erasure itself is audited — the audit record names the request, not the data
    auditService.record(AuditEvent.erasureCompleted(customerId, request));
}
```

### 14.4 Retention Schedule

Every table holding personal data has an entry here, and an automated expiry job that enforces it.

| Data | Retention | Basis |
|:-----|:----------|:------|
| Transaction and ledger records | 7–10 years per jurisdiction | Financial regulation |
| Know Your Customer (KYC) and identity documents | 5 years after the relationship ends | Anti-money-laundering (AML) regulation |
| Customer contact details | Life of the relationship + statutory period | Contract |
| Marketing consent records | Until withdrawn + 2 years | Proof of consent |
| Application logs | 90 days | Operational |
| Audit trail | Per [§13.6](#136-retention) | Regulatory |
| Session and token records | 30 days | Security investigation |

### 14.5 Cross-Border Transfer

Personal data does not leave its permitted jurisdiction without a documented legal basis. This constrains architecture directly: replica regions, backup regions, log aggregation endpoints, monitoring vendors, and support tooling are all data transfers. Every one requires the same check.

### 14.6 Consent

Where processing relies on consent, consent is recorded with its timestamp, its version of the notice, and its scope. Withdrawal is as easy as granting, and takes effect immediately rather than at the next batch cycle.

---

## 15. PCI DSS 4.0 Scope Management

### 15.1 What Puts a Service in Scope

A service is inside the cardholder data environment if it stores, processes, or transmits cardholder data, or if it can affect the security of a system that does. Being in scope brings segmentation, logging, scanning, access control, and annual assessment obligations across the whole service.

| Handling | In Scope | Note |
|:---------|:---------|:-----|
| Stores the PAN, encrypted or not | Yes | Full obligations |
| Transmits the PAN, even in passing | Yes | Including a proxy that never persists it |
| Holds only a token from a PCI-scoped tokenization service | **No** | The preferred design |
| Displays only a masked PAN it never held in full | No | |
| Shares a network segment with a cardholder data environment (CDE) system without segmentation | Yes | Segmentation must be demonstrable |

### 15.2 Stay Out of Scope

The cheapest way to satisfy PCI DSS for a service is for the service not to handle card data at all.

```
   Client ──── PAN ────▶ ┌────────────────────────┐
                         │ Tokenization service   │  ◀── the only PCI-scoped component
                         │  (or the PSP directly) │
                         └───────────┬────────────┘
                                     │  token
                                     ▼
                         ┌────────────────────────┐
                         │  This service          │  ◀── out of scope
                         │  stores only the token │
                         └────────────────────────┘
```

Where the client must submit card details, they go directly to the payment service provider (PSP) or the tokenization endpoint — never through this service, and never through a form this service renders and posts.

### 15.3 If a Service Must Be In Scope

Requires written approval from the Security Architect, and then:

- Documented network segmentation, with the boundary tested
- Application-level encryption of the PAN, with keys in an HSM or KMS ([§7](#7-data-at-rest))
- Masked display everywhere ([§9.1](#91-pan-masking))
- No CVV, PIN, or track data stored, ever ([§9.4](#94-never-stored-under-any-circumstances))
- All access logged and retained per [§13](#13-audit-trail)
- Quarterly vulnerability scanning and annual penetration testing
- Change control and access review evidence maintained continuously, not assembled before an assessment

---

## 16. Session, Token and Credential Handling

### 16.1 Token Lifetimes

| Token | Lifetime | Rotation |
|:------|:---------|:---------|
| Access token | ≤ 15 minutes | Not rotated; re-issued from a refresh token |
| Refresh token | ≤ 30 days | **Rotated on every use** |
| Step-up token for a high-risk operation | ≤ 5 minutes | Single use |

**Refresh token rotation with reuse detection** is the key control: each use issues a new refresh token and invalidates the old one. Presenting an already-used refresh token means the token was stolen, and the entire token family for that session is revoked immediately.

### 16.2 Revocation

A short access-token lifetime bounds the damage from a stolen token, but it does not stop an in-progress session. For events that must take effect immediately — a reported compromise, a staff termination, a fraud lock — the service checks a revocation list.

The list is keyed by the token's `jti` claim and by subject, cached with a short TTL, and consulted on every request for privileged and money-moving operations.

### 16.3 Credential Storage

Where this service stores a credential at all — usually it does not, because the identity provider owns them:

- **Argon2id** with parameters tuned so a single verification takes roughly 250–500 ms on production hardware. bcrypt with a cost factor of 12 or more is the fallback where Argon2 is unavailable.
- **Never the Secure Hash Algorithm (SHA-256), Message Digest 5 (MD5), or any fast hash**, with or without a salt. Fast hashes are the point of the attack, not a defence against it.
- **Constant-time comparison** for every secret comparison, including tokens, HMACs, and API keys. A short-circuiting `equals` leaks the value one byte at a time under timing analysis.

```java
// PROHIBITED — early return leaks the comparison position
if (providedToken.equals(storedToken)) { ... }

// GOOD
if (MessageDigest.isEqual(providedToken.getBytes(UTF_8), storedToken.getBytes(UTF_8))) { ... }
```

### 16.4 Step-Up Authentication

Re-authentication is required, regardless of an otherwise valid session, for:

- A transfer above the step-up threshold
- Adding or modifying a payee
- Changing contact details, credentials, or authentication factors
- Any staff action on a customer's financial data
- Viewing full card details

The step-up outcome is bound to the specific operation — the transfer id, the payee id — not to the session. A step-up that authorizes "the session" lets a later, different operation ride on it.

---

## 17. Security Testing and Verification

### 17.1 Automated Gates

| Gate | Tool Class | Fails The Build On |
|:-----|:-----------|:-------------------|
| Dependency vulnerabilities | Open Worldwide Application Security Project (OWASP) Dependency-Check, or equivalent | HIGH or CRITICAL ([ESTD20 §19.2](./ESTD20_-_Spring_Boot_Framework_Standards.md#192-vulnerability-gating)) |
| Static analysis | SpotBugs with FindSecBugs, plus Semgrep | Any security-category finding |
| Secret scanning | Gitleaks, or equivalent | Any finding, including in history |
| Container scanning | Trivy, or equivalent | HIGH or CRITICAL in the base image |
| Dynamic scanning | Dynamic application security testing (DAST) against a deployed non-production instance | HIGH or CRITICAL |

### 17.2 Security Tests Are Written, Not Assumed

Every control in this document has a test that proves it, and a test that proves the negative case.

```java
@Test
void getAccount_whenAccountBelongsToAnotherCustomer_returns404NotForbidden() throws Exception {
    UUID otherCustomersAccount = seedAccountFor(otherCustomerId);

    mockMvc.perform(get("/api/v1/accounts/{id}", otherCustomersAccount)
            .with(jwt().jwt(j -> j.subject(customerId.toString()))))
        .andExpect(status().isNotFound());         // 404, not 403 — no existence disclosure
}

@Test
void anyEndpoint_withoutToken_returns401() throws Exception {
    mockMvc.perform(get("/api/v1/accounts"))
        .andExpect(status().isUnauthorized());
}

@Test
void anyEndpoint_withTokenForAnotherAudience_returns401() throws Exception {
    mockMvc.perform(get("/api/v1/accounts")
            .header("Authorization", "Bearer " + tokenWithAudience("other-application")))
        .andExpect(status().isUnauthorized());
}

@Test
void errorResponse_neverContainsAccountNumberOrSql() throws Exception {
    MvcResult result = mockMvc.perform(post("/api/v1/transfers")
            .header("Idempotency-Key", UUID.randomUUID().toString())
            .contentType(APPLICATION_JSON)
            .content(transferJsonForNonexistentAccount()))
        .andReturn();

    String body = result.getResponse().getContentAsString();
    assertThat(body).doesNotContain("GB29NWBK", "SELECT", "jakarta.persistence", "Exception");
}

@Test
void auditEvent_cannotBeUpdated() {
    AuditEvent event = auditRepository.save(sampleEvent());

    assertThatThrownBy(() -> jdbcTemplate.update(
            "UPDATE audit_event SET action = 'TAMPERED' WHERE id = ?", event.getId()))
        .isInstanceOf(DataAccessException.class);
}

@Test
void approve_whenApproverIsTheMaker_isRejectedAndAudited() {
    assertThatThrownBy(() -> makerCheckerService.approve(requestId, sameStaffPrincipal))
        .isInstanceOf(SelfApprovalProhibitedException.class);

    assertThat(auditRepository.findByAction("SELF_APPROVAL_ATTEMPT")).isNotEmpty();
}
```

### 17.3 Manual Review Checkpoints

| Trigger | Review |
|:--------|:-------|
| A new endpoint | Authentication, authorization, ownership, validation, response classification |
| A new field on any entity or DTO | Data classification, masking, retention, whether it belongs in the ledger |
| A new outbound integration | SSRF validation, timeout, circuit breaker, credential handling, data transferred |
| A change to the security filter chain | Full security review; never merged on a single approval |
| A change touching money movement or the ledger | Security review plus four-eyes approval on the pull request (PR) |
| A new dependency | Licence, maintenance status, Common Vulnerabilities and Exposures (CVE) history, whether the platform already provides it |

### 17.4 Penetration Testing

An external penetration test is performed at least annually and after any significant architectural change. Findings are tracked to closure with an agreed remediation window by severity. A CRITICAL finding blocks the next release.

---

## 18. Incident Response Hooks

### 18.1 What the Application Must Provide

Incident response is an organizational process. The application's obligation is to make it possible:

- **Detection signals** as metrics and alerts, not only as log lines somebody might read
- **A correlation id on every request**, so one customer complaint becomes one complete trace
- **An audit trail** sufficient to reconstruct what happened without guessing
- **A kill switch** — a feature flag per money-moving operation, so a compromised flow can be disabled in seconds without a deployment
- **Immediate revocation** for tokens and sessions ([§16.2](#162-revocation))

### 18.2 Alertable Security Events

| Signal | Threshold |
|:-------|:----------|
| Authentication failures for one account | 5 in 15 minutes |
| Authentication failures across accounts from one source | 50 in 15 minutes |
| Authorization denials for one subject | 10 in 5 minutes |
| Self-approval attempts | **Any** |
| Audit hash-chain verification failure | **Any** |
| Balance reconciliation divergence | **Any** |
| A restricted-data read outside business hours by a staff account | Any |
| Rate-limit breaches from one subject | Sustained |
| Circuit breaker open on a compliance dependency | Any |

The "any" thresholds are deliberate. Those events have no benign explanation.

### 18.3 Breach Notification Clocks

| Regime | Clock | Starts |
|:-------|:------|:-------|
| GDPR | 72 hours to the supervisory authority | On becoming aware |
| GDPR | Without undue delay to data subjects | Where the risk is high |
| DPDP | Per the Data Protection Board's prescribed timeline | On becoming aware |
| PCI DSS | Immediately to the acquirer and card brands | On suspicion, not confirmation |
| Institutional regulator | Per the institution's licence conditions | Per those conditions |

**The clock starts on awareness, not on confirmation.** An engineer who suspects a data exposure escalates immediately; determining the scope happens in parallel with notification, never before it.

### 18.4 Evidence Preservation

On suspicion of a security incident:

- **Do not delete, redeploy over, or "clean up" anything.** Restarting the affected instance destroys the evidence.
- Preserve logs, audit records, heap state, and database point-in-time recovery targets before any remediation.
- Record every action taken, with its timestamp and the person who took it.
- Rotate potentially exposed credentials immediately — this is the one remediation that precedes investigation.

---

## 19. Common Pitfalls to Avoid

| # | Pitfall | Consequence | Prevention |
|:--|:--------|:------------|:-----------|
| 1 | JWT accepted without audience validation | A token minted for another application authenticates here | Explicit `aud` validator ([§3.2](#32-decoder-configuration)) |
| 2 | Trusting a gateway-supplied identity header | Total authentication bypass if the gateway is bypassed | The service validates the token itself, always |
| 3 | Customer id taken from a request parameter | Any customer reads any other customer's data | Identity comes only from the validated token ([§3.4](#34-extracting-the-principal)) |
| 4 | Ownership checked after loading, or not at all | Broken object-level authorization; mass data exposure | Ownership in the query: `findByIdAndCustomerId` ([§4.4](#44-ownership-checks-are-mandatory)) |
| 5 | 403 returned for another customer's resource | Confirms existence; enables account enumeration | Return 404 |
| 6 | Sequential integer ids exposed to clients | Trivial enumeration of every record | Opaque UUIDs |
| 7 | `permitAll()` placed after `anyRequest().authenticated()` | Endpoints silently unprotected | `anyRequest().authenticated()` last, always |
| 8 | `@PreAuthorize` on a self-invoked method | Authorization silently not enforced | Method security is proxy-based; cross the bean boundary |
| 9 | Logging a request or response object | Regulated data permanently in the log store | Log internal identifiers only ([§8.1](#81-the-logging-prohibition)) |
| 10 | Lombok `@Data` or `@ToString` on a sensitive type | Account numbers reach logs with no log statement naming them | Hand-written `toString()` with masking |
| 11 | Account number or IBAN in a URL | Regulated data in proxy, CDN, and browser logs | Opaque ids in paths; sensitive lookups in a POST body |
| 12 | `e.getMessage()` returned to the client | SQL, hostnames, and identifiers disclosed | Curated messages keyed by error code |
| 13 | CVV stored "temporarily" | Absolute PCI DSS violation; no exception path exists | Never persisted, cached, logged, or messaged |
| 14 | Deterministic encryption used to make a column searchable | Equality leaked across the whole dataset | Randomized encryption plus a blind index ([§7.3](#73-searchability)) |
| 15 | AES-CBC without authentication, or a reused IV | Malleable ciphertext; GCM key recovery on IV reuse | AES-256-GCM with a fresh random IV per value |
| 16 | Encryption key stored with the encrypted data or in config | Encryption provides no protection at all | KMS or HSM; envelope encryption |
| 17 | Secret committed to version control | Permanently compromised; history, forks, and CI caches retain it | Secret scanning that blocks the merge; rotate on any exposure |
| 18 | `actuator` exposure set to `*` | `/env` and `/heapdump` expose configuration and memory | Explicit allowlist on a separate, internal port ([§5.5](#55-actuator-exposure)) |
| 19 | String concatenation into a query | SQL injection | Named parameters only ([§11.1](#111-parameterized-queries-only)) |
| 20 | `Sort` built from an unvalidated request parameter | Injection through a path most reviewers do not check | Allowlist mapping client tokens to properties |
| 21 | Java native deserialization of untrusted input | Remote code execution | JSON with explicit types; no polymorphic default typing |
| 22 | Outbound URL from user input, unvalidated | SSRF to cloud metadata and internal services | Scheme and host allowlist, plus resolved-address checks |
| 23 | Request bound directly onto an entity | Mass assignment sets `status`, `balance`, or `role` | Purpose-built request records; reject unknown properties |
| 24 | CORS `allowedOrigins("*")` with credentials | Any origin reads authenticated responses | Explicit per-environment origin list |
| 25 | Audit record in the rolled-back business transaction | Denied and failed attempts leave no trace | `REQUIRES_NEW` for failures and denials ([§13.5](#135-audit-writes-must-survive-a-business-rollback)) |
| 26 | `UPDATE` or `DELETE` granted on the audit table | The audit trail is editable by the thing it audits | Revoke at the database, plus an immutability trigger |
| 27 | Personal data written into the ledger | Right to erasure becomes impossible to honour | Ledger holds financial data only; erase the customer record |
| 28 | Fast hash (SHA-256, MD5) for credential storage | Offline cracking at billions of guesses per second | Argon2id, or bcrypt cost ≥ 12 |
| 29 | `equals()` used to compare a token or HMAC | Value recoverable byte by byte under timing analysis | `MessageDigest.isEqual` |
| 30 | Maker able to approve their own request | Segregation of duties defeated; one account is unbounded | Enforced in code and by a database constraint ([§4.5](#45-four-eyes-approval-for-high-risk-operations)) |
| 31 | Rate limiter with per-instance state | The effective limit is multiplied by the instance count | Shared state in Redis or the database |
| 32 | Restarting an affected instance during an incident | Evidence destroyed before it is captured | Preserve first; rotate credentials; then remediate |
