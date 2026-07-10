# COMP-0026: Provider Comparison — Parametric self-model registry and invariant testing review

## Metadata

- comparison_id: `COMP-0026`
- title: `Parametric self-model registry and invariant testing review`
- context_policy: `latest_context`
- context_require_admission: `false`
- context_max_warning_admissions: `null`
- context_max_warning_admissions_source: `unset`
- context_manifest: `docs/comparisons/COMP-0026-parametric-self-model-registry-and-invariant-testing-review.context.json`
- created_at: `2026-07-10T19:44:17.831659+00:00`
- command: `scripts/compare_providers.py AI-Lab dynamically discovers self-model JSON records, but many production-repository tests and maintenance steps still encode exact object IDs, complete inventory lists, and exact quantities for capabilities, gaps, plans, warrants, and verifications. Adding a record therefore requires editing unrelated historical assertions, while a stale generated SELF_MODEL.json can remain inconsistent with repository records.

Evaluate whether AI-Lab should introduce a parametric self-model registry and invariant-based test infrastructure before continuing the GAP-0002 follow-up that would expose CAP-0009 through explicit opt-in parameters.

Assess all of the following:

1. Is this a distinct architectural/self-model gap, potentially GAP-0003, or only test cleanup?
2. Should existing JSON records remain the sole canonical source, with the registry generated from them and no second manually maintained inventory?
3. Should static configuration describe only record types, directories, ID fields, validators, lifecycle rules, and status semantics, while instances, IDs, relationships, and quantities remain dynamic?
4. Should adding a record instance require zero code changes, while adding an entirely new record type deliberately requires validator/schema work, one registry type specification, documentation, and focused tests in accordance with ontology-precedes-implementation?
5. How should locally suggested next IDs work in a multi-AI Git workflow? Is a documented non-transactional max-suffix allocator with merge-time collision resolution sufficient at current scale?
6. Should build_self_model_index consume the registry while preserving the current SELF_MODEL.json external schema during the first slice?
7. How should tests avoid the self-verification trap where index quantities are compared with quantities produced by the same registry implementation?
8. Should known counts and lifecycle transitions be tested only in temporary fixture repositories, while the production repository is tested through validation, uniqueness, referential integrity, lifecycle consistency, omission detection, and generated-projection drift checks?
9. Should CI or the audit fail whenever committed SELF_MODEL.json differs from the normalized current registry projection, excluding only explicitly volatile fields?
10. Should compact objects_by_id data omit redundant source paths and store only identity metadata such as kind and status, while full projections may retain source_path solely as provenance?
11. Should the first slice include a create_self_model_record.py skeleton CLI that suggests locally available IDs, refuses current-worktree collisions, creates schema-valid skeletons, validates before writing, and documents that allocation is not concurrency-safe?
12. Should normalized registry relations reuse or be losslessly compatible with the existing GraphRelation shape of source_id, predicate, target_id, and authoritative, to prevent incompatible graph representations?
13. Should this work be treated as a prerequisite that temporarily defers, but does not cancel, the GAP-0002 CAP-0009 opt-in exposure follow-up?

Recommend the safest first governed slice, explicit non-goals, acceptance criteria, and migration order. Do not implement anything. Do not assume GAP-0003 or any new PLAN has already been created or admitted. --latest-context --auto-include-l0-discovery --title Parametric self-model registry and invariant testing review`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5`
- Claude: `claude-sonnet-4-5`

## Prompt

AI-Lab dynamically discovers self-model JSON records, but many production-repository tests and maintenance steps still encode exact object IDs, complete inventory lists, and exact quantities for capabilities, gaps, plans, warrants, and verifications. Adding a record therefore requires editing unrelated historical assertions, while a stale generated SELF_MODEL.json can remain inconsistent with repository records.

Evaluate whether AI-Lab should introduce a parametric self-model registry and invariant-based test infrastructure before continuing the GAP-0002 follow-up that would expose CAP-0009 through explicit opt-in parameters.

Assess all of the following:

1. Is this a distinct architectural/self-model gap, potentially GAP-0003, or only test cleanup?
2. Should existing JSON records remain the sole canonical source, with the registry generated from them and no second manually maintained inventory?
3. Should static configuration describe only record types, directories, ID fields, validators, lifecycle rules, and status semantics, while instances, IDs, relationships, and quantities remain dynamic?
4. Should adding a record instance require zero code changes, while adding an entirely new record type deliberately requires validator/schema work, one registry type specification, documentation, and focused tests in accordance with ontology-precedes-implementation?
5. How should locally suggested next IDs work in a multi-AI Git workflow? Is a documented non-transactional max-suffix allocator with merge-time collision resolution sufficient at current scale?
6. Should build_self_model_index consume the registry while preserving the current SELF_MODEL.json external schema during the first slice?
7. How should tests avoid the self-verification trap where index quantities are compared with quantities produced by the same registry implementation?
8. Should known counts and lifecycle transitions be tested only in temporary fixture repositories, while the production repository is tested through validation, uniqueness, referential integrity, lifecycle consistency, omission detection, and generated-projection drift checks?
9. Should CI or the audit fail whenever committed SELF_MODEL.json differs from the normalized current registry projection, excluding only explicitly volatile fields?
10. Should compact objects_by_id data omit redundant source paths and store only identity metadata such as kind and status, while full projections may retain source_path solely as provenance?
11. Should the first slice include a create_self_model_record.py skeleton CLI that suggests locally available IDs, refuses current-worktree collisions, creates schema-valid skeletons, validates before writing, and documents that allocation is not concurrency-safe?
12. Should normalized registry relations reuse or be losslessly compatible with the existing GraphRelation shape of source_id, predicate, target_id, and authoritative, to prevent incompatible graph representations?
13. Should this work be treated as a prerequisite that temporarily defers, but does not cancel, the GAP-0002 CAP-0009 opt-in exposure follow-up?

Recommend the safest first governed slice, explicit non-goals, acceptance criteria, and migration order. Do not implement anything. Do not assume GAP-0003 or any new PLAN has already been created or admitted.

## OpenAI Response

- model: `gpt-5`

```
Summary recommendation
Introduce a parametric self-model registry and invariant-based test infrastructure now, as a governed prerequisite, before the GAP-0002 follow-up that would expose CAP-0009 via opt-in parameters. This is an architectural/self-model gap (GAP-0003 candidate), not just test cleanup. Keep existing JSON records as the single source of truth; generate the registry/index from them; migrate tests to invariants and drift checks; preserve the current SELF_MODEL.json external schema in the first slice. Proceed with a read-only, validation-first slice consistent with prior “ontology precedes implementation” and small, testable slices.

Assessments
1) Distinct gap or test cleanup
- Distinct architectural/self-model gap (GAP-0003 candidate). The lack of a parametric registry and invariant tests creates governance, consistency, and maintainability risks that affect selection, validation, and reproducibility across the repo, not only test hygiene. It directly contributes to stale or brittle self-model projections and manual edits to unrelated assertions.

2) Canonical source of truth
- Yes. Existing JSON records remain canonical. The registry/index is generated from committed records; do not maintain a second manual inventory.

3) Static configuration vs dynamic instances
- Yes. Static config should define:
  - Record kinds/types, directories, filename patterns, and ID fields.
  - Validators/schemas per kind.
  - Lifecycle rules and status semantics.
- Dynamic and discovered at runtime:
  - Instances, IDs, relationships, and quantities.

4) Zero-code for new instances; governed work for new types
- Yes. Adding a record instance should require zero code changes. Adding a new record type should require:
  - Schema/validator work.
  - One registry type specification.
  - Documentation and focused tests.
  - This aligns with “ontology precedes implementation” and prior validation-first patterns.

5) Next-ID allocation in multi-AI Git workflows
- Use a documented non-transactional max-suffix allocator that:
  - Suggests locally available next IDs.
  - Is explicitly not concurrency-safe.
  - Resolves collisions at merge time via standard Git resolution and re-run of the allocator.
- This is sufficient at current scale; revisit if collision frequency rises.

6) build_self_model_index and first-slice compatibility
- Yes. Have build_self_model_index consume the new registry and preserve the current SELF_MODEL.json external schema in the first slice to avoid downstream breakage.

7) Avoiding the self-verification trap in tests
- Do not assert repository-wide counts derived by the same registry implementation that produced the index.
- Use:
  - Independent, minimal fixtures with known contents to assert counts and lifecycle transitions.
  - In production, assert invariants (validation, uniqueness, referential integrity, lifecycle consistency) and drift between committed SELF_MODEL.json and a normalized fresh projection, not raw counts produced by the same code path.

8) Where to test counts vs production invariants
- Yes. Known counts and lifecycle transitions only in temporary fixture repositories.
- Production repository tests should focus on:
  - Schema validation and required fields.
  - ID uniqueness and referential integrity (including relations).
  - Lifecycle/status consistency rules.
  - Omission detection (e.g., known directories contain only valid or explicitly ignored files).
  - Generated-projection drift checks.

9) CI/audit behavior on drift
- Yes. CI (or audit) should fail whenever committed SELF_MODEL.json differs from the normalized current registry projection, excluding explicitly volatile fields (for example, timestamps, content hashes if designed to change, or tool-version stamps). Provide a documented suppression path only for exceptional, approved windows.

10) Compact objects_by_id vs provenance
- Yes. Compact objects_by_id should store only identity and minimal status (e.g., kind, status, id). Omit redundant source paths there.
- Full projections may retain source_path solely as provenance.

11) create_self_model_record.py skeleton CLI in first slice
- Yes. Include a CLI that:
  - Suggests locally available IDs.
  - Refuses collisions in the current worktree.
  - Creates schema-valid skeletons for the selected record type.
  - Validates before writing.
  - Clearly documents that allocation is not concurrency-safe.

12) Registry relations shape
- Yes. Normalize relations to reuse or be losslessly compatible with the existing GraphRelation shape:
  - source_id, predicate, target_id, authoritative.
- Avoid introducing an incompatible graph representation.

13) Prerequisite to GAP-0002 CAP-0009 follow-up
- Yes. Treat this as a prerequisite that temporarily defers (but does not cancel) the GAP-0002 CAP-0009 opt-in exposure work. Finishing the registry and invariant tests reduces brittle surfaces before exposing new opt-in capabilities.

Safest first governed slice (read-only, validation-first)
- Scope
  - Introduce a parametric registry configuration describing record kinds, directories, ID fields, schemas/validators, lifecycle rules, and status semantics.
  - Implement a registry loader that discovers instances dynamically from the repo and validates them.
  - Implement build_self_model_index to consume the registry and emit a normalized projection that preserves the current SELF_MODEL.json external schema.
  - Add a drift checker that compares committed SELF_MODEL.json to the freshly generated normalized projection, ignoring explicitly volatile fields.
  - Provide create_self_model_record.py skeleton CLI (suggest-next-ID, validate-before-write, refuse local collisions).
  - Add production-invariant CI checks (validation, uniqueness, referential integrity, lifecycle consistency, omission detection via safe patterns).
  - Add fixture repositories and tests that assert known counts and lifecycle transitions.
- Non-goals (first slice)
  - No change to the SELF_MODEL.json external schema.
  - No new lifecycle states or ontology expansion beyond encoding what already exists.
  - No concurrency-safe or centralized ID allocator.
  - No automatic commits or write-back beyond the explicit CLI.
  - No integration with external stores or live retrieval.
  - No graph-engine upgrades; only ensure relation shape compatibility.
- Acceptance criteria
  - From a clean checkout, running the registry builder validates all records and produces a projection byte-for-byte equal to committed SELF_MODEL.json, excluding documented volatile fields.
  - CI fails on drift between committed SELF_MODEL.json and the normalized projection.
  - Adding a new record instance (of an existing type) requires no code changes and passes validation/CI after running the CLI to generate a skeleton and filling required fields.
  - Fixture tests pass with known counts and lifecycle transitions; production tests contain no repository-wide count assertions.
  - Relations in the projection are GraphRelation-compatible (source_id, predicate, target_id, authoritative).
  - Documentation exists for registry config, CLI usage, volatile fields policy, ID allocation caveats, and developer workflow.
- Migration order
  1) Define the registry configuration schema (kinds, directories, ID fields, validators, lifecycle/status semantics).
  2) Implement validators and normalize status/lifecycle rules per kind.
  3) Implement the registry loader and normalization logic.
  4) Implement build_self_model_index to consume the registry and emit the existing SELF_MODEL.json schema.
  5) Implement the drift checker and wire it into CI, with an allowlist only for explicitly volatile fields.
  6) Create fixture repositories and add invariant and count-based tests against those fixtures.
  7) Replace production count-based tests with invariant checks and drift checks; remove brittle full-inventory assertions.
  8) Add create_self_model_record.py and documentation; require it for new records.
  9) Run one-time regeneration of SELF_MODEL.json to establish a normalized baseline; commit with a change note referencing the new validation path.
  10) Unblock and continue the GAP-0002 CAP-0009 opt-in exposure follow-up, now on top of the stabilized registry and tests.

Rationale anchors
- Aligns with prior patterns: small, read-only, validation-first governed slices; strong schema/validation/idempotency emphasis; reproducible manifests; ontology precedes implementation. This reduces drift and manual maintenance friction while keeping the first slice low risk.
```

## Claude Response

- model: `claude-sonnet-4-5`

````
# Evaluation: Parametric Self-Model Registry and Invariant-Based Testing Infrastructure

## Executive Summary

**This is a distinct architectural gap (GAP-0003 candidate) that should be addressed before GAP-0002 follow-up work.** It represents foundational self-model infrastructure that prevents brittle test maintenance and enables safe record addition without code changes. The current state—hard-coded counts and IDs scattered across tests—violates the dynamic discovery principle that already governs runtime behavior but not verification.

---

## Question-by-Question Assessment

### 1. Is this a distinct architectural/self-model gap, potentially GAP-0003, or only test cleanup?

**Distinct gap.** Evidence:

- **Current asymmetry**: Runtime components (e.g., `build_self_model_index`, `artifact_history`) dynamically discover records via filesystem scanning, but tests encode exact inventories (e.g., "assert len(capabilities) == 4", "assert 'CAP-0001' in ids").
- **Maintenance burden observed**: The task description cites adding a record requiring edits to "unrelated historical assertions" and stale `SELF_MODEL.json` inconsistency—these are symptoms of missing abstraction, not isolated tech debt.
- **Self-model scope**: This affects how AI-Lab **knows and verifies its own structure**. Tests that break when CAP-0005 is added cannot reliably verify self-model correctness; they verify a snapshot.
- **Prerequisite nature**: GAP-0002 follow-up (exposing CAP-0009 via opt-in) would add more records and exacerbate the problem without fixing the root cause.

**Why not "just test cleanup":**
- Cleanup implies local fixes; this requires systematic infrastructure (registry, validators, projection logic).
- The gap blocks safe addition of new record instances, which is a capability limitation.
- It touches ontology (what is a "record type," what are lifecycle rules) and must precede implementation (ADR-0002).

**Recommendation**: Open as **GAP-0003: Parametric self-model registry and invariant-based verification infrastructure**.

---

### 2. Should existing JSON records remain the sole canonical source, with the registry generated from them and no second manually maintained inventory?

**Yes.** Rationale:

- **Single source of truth**: JSON records in `docs/capabilities/`, `docs/gaps/`, `docs/plans/`, etc., are already authoritative for both runtime and audit.
- **No duplication**: A manually maintained registry (e.g., Python constants or separate YAML) would inevitably drift from committed records.
- **Discovery already works**: `build_self_model_index` and `artifact_history` scan directories and parse front matter; the registry should formalize and reuse this pattern.
- **Write path**: When creating a record, authors edit JSON/YAML in `docs/`; the registry materializes on demand from those files.

**Registry role**: Parser + validator + typed accessor + projection generator, **not** a separate data store.

---

### 3. Should static configuration describe only record types, directories, ID fields, validators, lifecycle rules, and status semantics, while instances, IDs, relationships, and quantities remain dynamic?

**Yes.** This is the correct separation. Static configuration defines:

```python
# Example (not implementation)
RECORD_TYPES = {
    "capability": {
        "directory": "docs/capabilities",
        "id_pattern": r"^CAP-\d{4}$",
        "required_fields": ["capability_id", "title", "status"],
        "valid_statuses": ["proposed", "approved", "deployed"],
        "lifecycle_edges": [("proposed", "approved"), ("approved", "deployed")],
    },
    "gap": { ... },
    # ...
}
```

Dynamic discovery yields:

```python
# Generated at runtime from filesystem
registry = {
    "capabilities": [
        {"capability_id": "CAP-0001", "status": "deployed", "source_path": "..."},
        {"capability_id": "CAP-0002", "status": "deployed", ...},
        # Count, IDs, relations populated by scanning docs/
    ]
}
```

**Why this matters**:
- Tests assert **invariants** ("all capabilities have unique IDs," "no gaps reference nonexistent plans"), not counts.
- Adding CAP-0005 requires zero config changes; adding a new record **type** (e.g., "observation") requires deliberate schema/validator work.
- Aligns with ontology-precedes-implementation (ADR-0002): type definitions are ontological; instances are data.

---

### 4. Should adding a record instance require zero code changes, while adding an entirely new record type deliberately requires validator/schema work, one registry type specification, documentation, and focused tests?

**Yes.** This is the design goal.

**Adding CAP-0005** (instance):
1. Author creates `docs/capabilities/CAP-0005-new-feature.json` with valid schema.
2. CI runs `validate_self_model_records` → scans directory → validates schema/ID uniqueness.
3. `build_self_model_index` regenerates `SELF_MODEL.json` → includes CAP-0005.
4. No test changes required (tests assert "all IDs unique," not "exactly 4 capabilities").

**Adding "observation" record type**:
1. Define schema in `schemas/observation.schema.json`.
2. Add `RECORD_TYPES["observation"]` entry with directory, ID pattern, lifecycle rules.
3. Write `ObservationValidator` (or extend generic validator).
4. Update registry projection logic to include observations.
5. Document purpose, lifecycle, and integration in `docs/self-model/`.
6. Add focused tests for observation-specific invariants.
7. **This work is deliberate friction**—new types expand the ontology.

**Consistency with development_directions**:
> "The safer sequence is: 1. Document the graph ontology. 2. Add lightweight schemas. 3. Generate metadata from existing artifacts."

Record type addition = ontology expansion; instance addition = metadata generation.

---

### 5. How should locally suggested next IDs work in a multi-AI Git workflow? Is a documented non-transactional max-suffix allocator with merge-time collision resolution sufficient at current scale?

**Sufficient for now, with explicit documentation of limitations.**

**Proposed mechanism**:
```python
# scripts/create_self_model_record.py
def suggest_next_id(record_type: str, worktree_path: str) -> str:
    """
    Scans committed + staged + worktree records of `record_type`.
    Returns next available ID by incrementing max numeric suffix.
    
    NOT CONCURRENCY-SAFE. Concurrent branches may allocate the same ID.
    Collision resolution: manual at merge time or via CI rejection.
    """
    existing = scan_records(record_type, include_worktree=True)
    max_suffix = max(parse_suffix(r.id) for r in existing)
    return f"{record_type.upper()}-{max_suffix + 1:04d}"
```

**Why this is acceptable**:
- **Current scale**: Small team, infrequent parallel record creation.
- **Git workflow already requires merge conflict resolution**; ID collisions are similar.
- **CI enforcement**: Pre-commit or CI hook runs `validate_self_model_records` → fails on duplicate IDs → author re-allocates before merge.
- **No database dependency**: Keeps workflow lightweight and Git-native.

**Documentation requirements** (in `docs/self-model/record_creation.md` or similar):
- "ID allocation is not transactional. If two branches concurrently create GAP-0004, CI will reject the second merge."
- "Resolution: `git pull`, re-run `create_self_model_record.py --suggest`, update ID, re-commit."
- "For high-concurrency workflows, consider centralized ID service (future enhancement)."

**When to revisit**: If >5 collisions/month occur, or if team size >10 with frequent parallel work.

---

### 6. Should `build_self_model_index` consume the registry while preserving the current SELF_MODEL.json external schema during the first slice?

**Yes. This is critical for safe migration.**

**First slice behavior**:
```python
# OLD (current):
def build_self_model_index():
    capabilities = scan_directory("docs/capabilities")
    gaps = scan_directory("docs/gaps")
    # ... hand-coded logic for each type
    return {"capabilities": [...], "gaps": [...], "metadata": {...}}

# NEW (first slice):
def build_self_model_index():
    registry = SelfModelRegistry.from_filesystem()
    projection = registry.to_legacy_json_projection()  # <-- compatibility shim
    # projection matches old schema exactly
    return projection
```

**Why preserve schema initially**:
- **External consumers**: If any scripts, dashboards, or documentation tooling reads `SELF_MODEL.json`, breaking the schema mid-refactor risks silent failures.
- **Incremental verification**: Diff old vs. new output during slice acceptance; identical output proves refactor correctness.
- **Schema evolution later**: Once registry is stable, a second slice can propose an improved schema (e.g., richer metadata, explicit relations).

**Acceptance criterion**: Generated `SELF_MODEL.json` in first slice is byte-for-byte identical to current output (modulo timestamps or other explicitly volatile fields).

---

### 7. How should tests avoid the self-verification trap where index quantities are compared with quantities produced by the same registry implementation?

**Test invariants and external ground truth, not derived counts.**

**Anti-pattern (self-verification trap)**:
```python
# BAD: Registry counts itself
def test_capability_count():
    registry = SelfModelRegistry.from_filesystem()
    index = build_self_model_index(registry)  # uses registry
    assert len(index["capabilities"]) == len(registry.capabilities)
    # ❌ If registry misses a file, test still passes
```

**Safe patterns**:

**A. Invariant-based (no hardcoded counts)**:
```python
def test_capability_ids_unique():
    registry = SelfModelRegistry.from_filesystem()
    ids = [c.capability_id for c in registry.capabilities]
    assert len(ids) == len(set(ids)), "Duplicate capability IDs"

def test_all_plans_reference_valid_gaps():
    registry = SelfModelRegistry.from_filesystem()
    gap_ids = {g.gap_id for g in registry.gaps}
    for plan in registry.plans:
        assert plan.addresses_gap in gap_ids, f"{plan.plan_id} references nonexistent {plan.addresses_gap}"
```

**B. Fixture-based (known ground truth)**:
```python
def test_registry_completeness_fixture(tmp_path):
    # Create temporary repo with known contents
    write_fixture(tmp_path / "docs/capabilities/CAP-9001.json", {...})
    write_fixture(tmp_path / "docs/gaps/GAP-9001.json", {...})
    
    registry = SelfModelRegistry.from_filesystem(root=tmp_path)
    assert len(registry.capabilities) == 1
    assert registry.capabilities[0].capability_id == "CAP-9001"
    # ✅ Test knows fixture contents independently
```

**C. Projection consistency (not self-verification)**:
```python
def test_index_matches_registry_projection():
    registry = SelfModelRegistry.from_filesystem()
    index_json = build_self_model_index(registry)
    
    # Compare registry's internal model with its JSON projection
    # (tests projection logic, not scanning logic)
    assert set(index_json["capabilities"].keys()) == {c.capability_id for c in registry.capabilities}
```

**D. External validation (filesystem ground truth)**:
```python
def test_registry_finds_all_committed_capabilities():
    # Independent scan (e.g., via subprocess git ls-files or os.walk)
    committed_cap_files = subprocess.check_output(
        ["git", "ls-files", "docs/capabilities/*.json"],
        text=True
    ).splitlines()
    
    registry = SelfModelRegistry.from_filesystem()
    assert len(registry.capabilities) == len(committed_cap_files)
    # ✅ Git is external ground truth
```

**Answer to question 7**: Use invariants + fixtures + external validation. Never compare registry counts with index counts derived from the same registry.

---

### 8. Should known counts and lifecycle transitions be tested only in temporary fixture repositories, while the production repository is tested through validation, uniqueness, referential integrity, lifecycle consistency, omission detection, and generated-projection drift checks?

**Yes. This is the correct testing strategy.**

**Fixture tests** (controlled, synthetic data):
```python
def test_lifecycle_invalid_transition_rejected(tmp_path):
    write_fixture(tmp_path / "docs/gaps/GAP-9001.json", {
        "gap_id": "GAP-9001",
        "status": "closed",  # No plan references this gap
    })
    registry = SelfModelRegistry.from_filesystem(root=tmp_path)
    
    errors = registry.validate_lifecycle_consistency()
    assert any("GAP-9001 closed without plan" in e for e in errors)
```

**Production repository tests** (real data, invariant-based):
```python
def test_production_all_ids_unique():
    registry = SelfModelRegistry.from_filesystem()  # real docs/
    all_ids = [r.id for r in registry.all_records()]
    assert len(all_ids) == len(set(all_ids))

def test_production_no_dangling_references():
    registry = SelfModelRegistry.from_filesystem()
    errors = registry.validate_referential_integrity()
    assert not errors, f"Dangling references: {errors}"

def test_production_index_up_to_date():
    """Fail if committed SELF_MODEL.json differs from current projection."""
    committed_index = json.loads(Path("SELF_MODEL.json").read_text())
    registry = SelfModelRegistry.from_filesystem()
    current_projection = registry.to_legacy_json_projection()
    
    # Exclude volatile fields
    for idx in [committed_index, current_projection]:
        idx["metadata"].pop("generated_at", None)
    
    assert committed_index == current_projection, "SELF_MODEL.json is stale"
```

**Why this separation**:
- **Fixture tests**: Prove correctness of validation logic against known bad data.
- **Production tests**: Prove the actual repository satisfies invariants.
- **No hardcoded production counts**: If GAP-0005 is added, production tests still pass (they check "no duplicates," not "exactly 3 gaps").

---

### 9. Should CI or the audit fail whenever committed SELF_MODEL.json differs from the normalized current registry projection, excluding only explicitly volatile fields?

**Yes. This is essential for preventing drift.**

**Proposed CI check**:
```bash
# .github/workflows/self_model_audit.yml
- name: Verify SELF_MODEL.json is current
  run: |
    python scripts/build_self_model_index.py --output /tmp/current_index.json
    python scripts/compare_self_model_projections.py \
      SELF_MODEL.json /tmp/current_index.json \
      --exclude-fields metadata.generated_at,metadata.builder_version
    # Fails if non-volatile fields differ
```

**Volatile fields** (excluded from comparison):
- `metadata.generated_at` (timestamp)
- `metadata.builder_version` (may change with script updates)
- `metadata.generation_model` (if using LLM for summaries)

**Non-volatile fields** (must match):
- All `capabilities`, `gaps`, `plans`, `warrants`, `verifications` records
- `objects_by_id` mappings
- Lifecycle states, relations, counts

**Failure message**:
```
SELF_MODEL.json is stale. Regenerate with:
  python scripts/build_self_model_index.py
  git add SELF_MODEL.json
  git commit --amend --no-edit
```

**Why this matters**:
- **Prevents inconsistency**: Stale `SELF_MODEL.json` could mislead downstream consumers or audits.
- **Forces regeneration discipline**: Authors must rebuild index when adding/modifying records.
- **Self-model correctness**: The index is a self-model artifact; drift invalidates self-knowledge.

---

### 10. Should compact `objects_by_id` data omit redundant source paths and store only identity metadata such as kind and status, while full projections may retain `source_path` solely as provenance?

**Yes. Optimize for common access patterns.**

**Compact form** (for `objects_by_id` lookup):
```json
````
