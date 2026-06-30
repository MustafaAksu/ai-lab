# ADR-0002: Ontology Precedes Implementation

## Status

Accepted

## Context

AI-Lab is intended to support long-lived scientific inquiry, initially for RTG research. As the system grows, there is a risk of introducing objects because they are convenient for implementation rather than because they reflect the underlying structure of research.

## Decision

Before introducing a major knowledge-layer object, AI-Lab will ask whether the object exists in the research domain or only in the current implementation.

The knowledge-layer ontology currently centers on:

- Identity
- Relationship
- Artifact
- ResearchSession
- ResearchProgram
- Perspective

Infrastructure-layer objects include:

- Provider
- API client
- Storage adapter
- Context pack builder
- CLI
- Test utilities

## Why

AI-Lab should converge toward the underlying structure of the domain rather than inventing an artificial structure.

This follows the same spirit as RTG research: the goal is not to force the domain into a convenient framework, but to uncover a coherent structure already suggested by the work.

## Consequences

Positive:
- Cleaner long-term architecture.
- Less premature abstraction.
- Better separation between scientific concepts and infrastructure.
- Easier future extension by human or AI peers.

Negative:
- Slightly slower early development.
- Requires explicit architectural reflection before major objects are added.

## Rule

Ontology precedes implementation.
