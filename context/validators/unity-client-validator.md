# validator.unity-client

- Validator ID: `validator.unity-client`
- Route: `route.unity-client`
- Source docs: `ESTD2`, `ESTD3`
- Overlay docs: `ESTD1`, `ESTD4`, `ESTD10`, `ESTD13`, `ESTD14`, `ESTD16`, `ESTD18`, `ESTD19`
- Applies to: Unity C# client code, UI, assets, networking, telemetry, mobile builds, WebGL client surface.
- Pass threshold: > 75% code conformity.

## Scoring

Use the shared scoring contract in `context/validators/README.md`.

## Check Groups

| Group | Weight | ESTD Sources | Validator Focus |
|:------|------:|:-------------|:----------------|
| Client architecture and state | 15 | `ESTD2`, `ESTD19` | separation of concerns, server-authoritative state, explicit state flow, dependency direction |
| Unity and C# code style | 15 | `ESTD3`, `ESTD14`, `ESTD18` | C# style, class/file organization, lifecycle use, naming, contextual collection/map names, folder placement |
| Async, networking, and resilience | 15 | `ESTD2`, `ESTD4`, `ESTD1` | centralized service layer, API contract consumption, request/response handling, cancellation, timeout, dedupe, reconnect, degraded network behavior |
| UX, accessibility, and localization | 10 | `ESTD2` | loading/error states, safe areas, responsive UI, destructive-action safeguards, accessibility, text readiness |
| Security and privacy | 10 | `ESTD1`, `ESTD2` | trust boundary, token handling, certificate pinning, anti-cheat awareness, build security |
| Performance, memory, and battery | 15 | `ESTD2`, `ESTD3` | hot paths, allocations, Addressables lifecycle, leaks, rendering, battery, profiling evidence |
| Testing and path coverage | 10 | `ESTD3`, `ESTD16` | unit-testable logic, Unity test runner, happy/sad/edge paths, coverage intent |
| Build, PR, and release evidence | 10 | `ESTD10`, `ESTD13` | build target rules, validation evidence, screenshots/videos, release-close risk notes, pipeline readiness |

## Static Coverage

| Group | Static Check IDs | LLM Gap |
|:------|:-----------------|:--------|
| Client architecture and state | `static.common.folder-structure`, `static.unity.roslyn` | architecture intent, dependency direction |
| Unity and C# code style | `static.unity.roslyn`, `static.common.folder-structure` | Unity lifecycle appropriateness |
| Async, networking, and resilience | `static.unity.roslyn`, `static.common.secrets` | API contract consumption and degraded-network behavior |
| UX, accessibility, and localization | None | UX completeness and player impact |
| Security and privacy | `static.common.secrets`, `static.common.gitleaks`, `static.common.semgrep` | trust-boundary intent |
| Performance, memory, and battery | `static.unity.roslyn` | runtime impact and profiling sufficiency |
| Testing and path coverage | `static.unity.roslyn` | path intent and coverage adequacy |
| Build, PR, and release evidence | `static.common.report-consistency` | PR evidence quality |

## LLM Gap Review

Use `context/validators/llm-based-validation.md` for unresolved semantic gaps.

## Evolution Rules

- If client route docs change, update Source or Overlay docs first.
- If a new Unity-specific ESTD is added, move related checks from overlays to Source docs.
- Keep route binding aligned with `route.unity-client`.
