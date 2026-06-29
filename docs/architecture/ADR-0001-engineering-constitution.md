# ADR-0001: Engineering Constitution

## Status

Accepted

## Context

AI-Lab is intended to become a long-lived research environment, initially focused on RTG. The project must remain understandable and extensible even if future contributors replace the original authors.

## Decision

AI-Lab will preserve not only code, but also the reasoning behind major design decisions.

The project follows these principles:

1. No throwaway code.
2. Small vertical slices.
3. Every step must be testable.
4. Main branch should remain releasable.
5. Secrets must not be committed.
6. Important architectural choices must be documented.
7. RTG documents and DSNs must remain canonical and version-aware.
8. Provider integrations must be modular.

## Why

Code alone explains what the system does, but not why it was built that way. For long-term research continuity, the project needs design memory.

This allows future contributors, researchers, or AI assistants to continue the work without reconstructing intent from scattered conversations.

## Consequences

Positive:
- Easier onboarding.
- Lower rollback risk.
- Better auditability.
- Better continuity for RTG research.

Negative:
- Slightly more documentation overhead.
- Slower initial development pace.

## Notes

The project treats "why" as a first-class artifact.
