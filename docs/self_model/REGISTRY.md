# Self-Model Registry

## Purpose

`SelfModelRegistry` provides a read-only, dynamically generated view of
AI-Lab's canonical JSON self-model records.

Canonical JSON records remain the sole source of truth. The registry does not
maintain a second inventory, infer capabilities, create governance decisions,
or change record lifecycle states.

The supported existing record families are:

- capability
- gap
- verification
- plan
- warrant
- decision

Adding an instance of an existing record family requires only a valid canonical
JSON record.

Adding a new record family remains a deliberate ontology change. It requires a
validator or schema, one `RecordTypeSpec`, documentation, and focused tests.

## Canonical locations

Records are discovered dynamically from:

    docs/self_model/capabilities/CAP-*.json
    docs/self_model/gaps/GAP-*.json
    docs/self_model/verifications/VERIFY-*.json
    docs/self_model/plans/PLAN-*.json
    docs/self_model/warrants/WARR-*.json
    docs/self_model/decisions/DECISION-*.json

`docs/self_model/SELF_MODEL.json` is a generated aggregation-only projection.
It is not an additional canonical record store.

Decision records are available through `SelfModelRegistry`, but they remain
outside the current external `SELF_MODEL.json` projection.

## Read-only registry use

Example:

    from pathlib import Path

    from ai_lab.documentation.self_model import SelfModelRegistry

    registry = SelfModelRegistry(Path("."))

    all_entries = registry.entries()
    plans = registry.entries("plan")
    open_plans = registry.open_entries("plan")
    record = registry.require("PLAN-20260710-0004")
    references = registry.references()
    issues = registry.unresolved_references()
    relations = registry.relations()

Registry record mappings are recursively read-only.

Use `RegistryEntry.mutable_record()` only when an independent mutable copy is
required.

Normalized registry relations are diagnostic self-model relations. They do not
automatically enter graph-neighborhood selection, context packs, provider
prompts, runtime manifests, retrieval, or persisted graph storage.

## Creating a record

The generic CLI consumes a human-authored JSON payload containing every
substantive field required by the selected record validator.

Example:

    python scripts/create_self_model_record.py \
      gap \
      --input /tmp/gap-payload.json \
      --repo-root .

The payload file in this example must first be created by the operator. The CLI
does not automatically create substantive record content.

The type-specific ID field may be omitted. The CLI then suggests a locally
available maximum-suffix ID and writes the record to its canonical directory.

For a date-scoped record:

    python scripts/create_self_model_record.py \
      plan \
      --input /tmp/plan-payload.json \
      --repo-root . \
      --date 2026-07-14

An explicit ID may also be supplied:

    python scripts/create_self_model_record.py \
      gap \
      --input /tmp/gap-payload.json \
      --repo-root . \
      --record-id GAP-0004

The CLI performs the following operations:

1. Reads the human-authored payload.
2. Fills only the mechanical ID when it is absent.
3. Validates the complete record before writing.
4. Computes the canonical path.
5. Checks the current registry for an ID collision.
6. Creates the output using exclusive file creation.
7. Refuses to overwrite an existing path.

The CLI does not invent rationale, evidence, verification results, warrants, or
governance decisions.

It does not update `SELF_MODEL.json`, create a commit, or push changes.

The existing type-specific writer scripts remain available when their
argument-oriented interfaces are more convenient.

## ID allocation and collision handling

ID suggestions are local and non-transactional.

For `CAP` and `GAP`, the maximum suffix is calculated across the global record
family.

For `PLAN`, `VERIFY`, `WARR`, and `DECISION`, the suffix is calculated within
the selected UTC date.

A suggested ID is not reserved in another branch, clone, or worktree.
Concurrent contributors may therefore receive the same suggestion.

Before committing a new record, run:

    git status --short
    python scripts/audit_self_model_index.py --repo-root .
    python -m pytest

When a pull, merge, or rebase introduces an ID collision:

1. Retain the already merged canonical record.
2. Remove or rename the colliding local record.
3. Update or rebase the working branch.
4. Rerun `create_self_model_record.py`.
5. Update references that use the changed ID.
6. Rerun tests and audits.
7. Commit the corrected record.

A transaction-safe distributed allocator is outside the current design.

This approach should be reconsidered only if collision frequency or parallel
contribution volume makes Git-based resolution inadequate.

## Projection generation

Build the aggregation-only projection with:

    python scripts/build_self_model.py \
      --repo-root . \
      --output docs/self_model/SELF_MODEL.json

The projection may copy, sort, count, group, filter, and link canonical record
content.

It must not infer capabilities, synthesize recommendations, invent risks, or
create governance decisions.

## Projection audit

Check normalized projection freshness with:

    python scripts/audit_self_model_index.py --repo-root .

The normalized comparison excludes only the documented volatile fields:

- `generated_at`
- `repo_head`

A substantive difference between committed `SELF_MODEL.json` and a fresh
normalized projection is an audit error.

Registry reference integrity is included in the self-model audit. Missing
targets and wrong target types are errors.

## Development invariants

Production tests derive quantities and inventories from canonical JSON rather
than encoding fixed global counts or complete historical ID lists.

Exact quantities remain appropriate in independently constructed temporary
fixture repositories whose contents are deliberately controlled by the test.

The production invariants are:

- Every canonical JSON record is discovered exactly once.
- Filenames and embedded IDs agree.
- IDs are globally unique.
- Every record validates through its type specification.
- Explicit references resolve to the expected record type.
- Lifecycle openness follows static record-type metadata.
- Projection IDs match the canonical JSON records.
- Projection status counts match the canonical JSON records.
- Committed `SELF_MODEL.json` matches a normalized fresh projection.
- Adding an instance of an existing record type requires no Python change.
- Adding an instance of an existing record type requires no test-source change.

## Scope boundary

The registry is an ontology and documentation mechanism.

It does not expose CAP-0009 through provider-facing parameters, change default
context selection, perform retrieval, create embeddings, rerank records,
persist a graph database, modify runtime manifests, or automatically include
graph-local context.

Those behaviors require separate governance.
