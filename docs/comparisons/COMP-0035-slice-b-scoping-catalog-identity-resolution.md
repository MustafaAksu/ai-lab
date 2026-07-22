# COMP-0035: Provider Comparison — Slice B scoping: catalog identity resolution

## Metadata

- comparison_id: `COMP-0035`
- title: `Slice B scoping: catalog identity resolution`
- invocation_produced_by: `[{'source_id': 'COMP-0035', 'predicate': 'produced_by', 'target_id': 'INV-9fd60000b4da1499', 'relation_source': 'future_edge_seed', 'authoritative': False, 'scope': 'invocation_provenance_slice_a', 'evidence': 'docs/invocations/INV-9fd60000b4da1499.json'}, {'source_id': 'COMP-0035', 'predicate': 'produced_by', 'target_id': 'INV-23b4d4298e0aa443', 'relation_source': 'future_edge_seed', 'authoritative': False, 'scope': 'invocation_provenance_slice_a', 'evidence': 'docs/invocations/INV-23b4d4298e0aa443.json'}]`
- created_at: `2026-07-22T20:49:02.948261+00:00`
- command: `scripts/compare_providers.py --title Slice B scoping: catalog identity resolution AI-Lab has just implemented ABS-0004 Slice A: invocation provenance capture on this very comparison path. Every provider call now emits an InvocationRecord with executor reference, requested API model name, service endpoint, session identity, an EffectiveInputManifest (rendered prompt digest, completeness attestation), and an ExecutionProfile including the output-token limit. Model identity is recorded as requested and marked identity_verification_status: unresolved, because no resolution mechanism exists.

Slice B is next: catalog identity resolution. Its admitted boundary is ModelIdentity, ServiceEndpointIdentity, atomic CatalogAssertions grouped into CatalogSnapshots with separate CatalogVerification records, requested-name to resolved-identity linkage, and a freshness and verification validator.

Assess, in order: (1) What is the smallest Slice B that would let an already-captured invocation record move from identity_verification_status unresolved to verified, and what exactly must be true for that transition to be honest rather than cosmetic? (2) How should a catalog assertion be verified in practice, given that the only available evidence is what a provider API returns about itself, and a provider asserting its own catalog is not independent verification of that catalog? Name the failure mode where self-assertion masquerades as verification. (3) What should happen to previously captured records when a catalog assertion they relied on is later found stale or wrong: are they re-verified, annotated, or left alone, and what does each choice cost? (4) Which parts of Slice B, if any, cannot be tested without live network access, and how should those be governed?

Ground your answers in the described design. Distinguish defects from preferences. Do not certify or praise. Do not recommend specific provider products, model names, or pricing.`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5`
- Claude: `claude-sonnet-4-5`

## Prompt

AI-Lab has just implemented ABS-0004 Slice A: invocation provenance capture on this very comparison path. Every provider call now emits an InvocationRecord with executor reference, requested API model name, service endpoint, session identity, an EffectiveInputManifest (rendered prompt digest, completeness attestation), and an ExecutionProfile including the output-token limit. Model identity is recorded as requested and marked identity_verification_status: unresolved, because no resolution mechanism exists.

Slice B is next: catalog identity resolution. Its admitted boundary is ModelIdentity, ServiceEndpointIdentity, atomic CatalogAssertions grouped into CatalogSnapshots with separate CatalogVerification records, requested-name to resolved-identity linkage, and a freshness and verification validator.

Assess, in order: (1) What is the smallest Slice B that would let an already-captured invocation record move from identity_verification_status unresolved to verified, and what exactly must be true for that transition to be honest rather than cosmetic? (2) How should a catalog assertion be verified in practice, given that the only available evidence is what a provider API returns about itself, and a provider asserting its own catalog is not independent verification of that catalog? Name the failure mode where self-assertion masquerades as verification. (3) What should happen to previously captured records when a catalog assertion they relied on is later found stale or wrong: are they re-verified, annotated, or left alone, and what does each choice cost? (4) Which parts of Slice B, if any, cannot be tested without live network access, and how should those be governed?

Ground your answers in the described design. Distinguish defects from preferences. Do not certify or praise. Do not recommend specific provider products, model names, or pricing.

## OpenAI Response

- model: `gpt-5`

```
Below is an assessment keyed to the Slice A/B design and its data types. It distinguishes what is required for correctness (defects if absent) from optional design choices (preferences).

1) Smallest Slice B that can turn an invocation from unresolved to verified — and what must be true for that to be honest

Smallest functional scope:
- Data types and links
  - ModelIdentity and ServiceEndpointIdentity (stable, content-addressable identifiers).
  - Atomic CatalogAssertions that bind: (service_endpoint_identity, requested_model_name) -> resolved ModelIdentity, with evidence_digest and assertion_time.
  - CatalogSnapshots as immutable sets of CatalogAssertions with a validity interval [valid_from, valid_to] and a unique snapshot_id.
  - CatalogVerification records that describe how the snapshot was verified and to what scope.
  - Linkage from InvocationRecord → (snapshot_id, assertion_id) that was in force at the invocation time.
  - A freshness-and-verification validator that evaluates an invocation + snapshot pair and emits a decision with reasons.

Minimal transition rule from unresolved → verified:
- Endpoint match: The InvocationRecord.service_endpoint resolves to a ServiceEndpointIdentity that is present in the CatalogSnapshot.
- Name match: The InvocationRecord.requested API model name exactly matches a CatalogAssertion key in that snapshot.
- Time-bounded: InvocationRecord.timestamp ∈ snapshot.validity interval (or within a configured staleness tolerance if you permit grace periods).
- Unambiguous: There is exactly one applicable assertion for the (endpoint, requested_name) at that time. If multiple conflicting assertions exist, do not mark verified (defect if you do).
- Verified scope recorded: The snapshot has a CatalogVerification entry whose method and scope explicitly state what was verified (e.g., “endpoint TLS identity and authenticated provider self-assertion of catalog”) and the result = pass.
- Evidence retained: The raw catalog response (or its content-addressed digest) and the endpoint TLS peer identity (e.g., cert chain/SPKI digest) are retained and referenced by the assertion. Not retaining this is a defect.

What makes the transition honest rather than cosmetic:
- Verified must mean “we proved who said what, via which endpoint, and when,” not “we proved the ground truth of the model’s nature.” The status (or an attached qualifier) must reflect the scope, e.g., verified(scope=endpoint+authenticated-self-assertion). Omitting scope is a defect because it over-claims certainty.
- The linkage must be reproducible: given the invocation timestamp, endpoint, and evidence digests, an auditor can reconstruct the same mapping and decision. Not being able to reproduce is a defect.
- Conflicts are handled deterministically: if any snapshot or later evidence shows contradictory assertions for the same time window, you cannot keep “verified” without annotation or downgrade. Silently ignoring conflicts is a defect.

2) How to verify a catalog assertion when the only evidence is what a provider API returns about itself; name the failure mode

In practice, verification decomposes into two separable parts with different trust properties:

- Endpoint/transport authentication (independent of provider claims)
  - Verify the ServiceEndpointIdentity via TLS (hostname to cert CN/SAN), a valid CA chain, optional SPKI pin, and record the peer identity (cert chain hash). This authenticates “who you connected to.”
  - Store handshake metadata sufficient for later audit (at least cert chain digests and servername).

- Authenticated self-assertion of catalog content (not independent)
  - Fetch the catalog (or the specific model mapping) over the authenticated channel above.
  - Store the exact bytes and a content digest (e.g., SHA-256), with headers (Date/ETag) and time-of-retrieval.
  - Record a CatalogVerification method like: method=“TLS-bound self-assertion”, scope=“catalog content as stated by endpoint X at time T”, result=pass, evidence_digest=… This verifies provenance and freshness of the statement, not its truth.

Given only provider-returned evidence, you cannot independently validate the model mapping itself. You can only:
- Verify endpoint identity and integrity of the returned statement at a time.
- Check consistency across time and across the provider’s own endpoints (consistency is helpful but still not independence).

Name of the failure mode where self-assertion masquerades as verification:
- Circular self-attestation (a.k.a. self-verification). Treat it as attestation, not independent verification, and label it as such in CatalogVerification.scope.

3) What to do with previously captured records if a relied-on catalog assertion is later stale or wrong

Three distinct actions and their costs:

- Annotate (append-only revocation/contradiction notes)
  - Action: Do not mutate historical verification. Append a VerificationUpdate that links the InvocationRecord to the affected assertion/snapshot and marks the reason: expired freshness window, contradicted by newer snapshot, or explicit error. Optionally downgrade the current effective status to disputed or revoked_ascertion while retaining the original decision and evidence.
  - Costs: Slight storage overhead; validator and query paths must handle multi-state (verified, disputed, revoked). Preserves auditability and reproducibility.

- Re-verify (re-run resolution under new knowledge) in addition to annotate
  - Action: Re-run the linkage using the best-known snapshot for the original invocation time. Record both the original decision and the retrospective decision, clearly labeled as post-facto. Do not replace the original; present both in queries that ask for “current best belief.”
  - Costs: More compute and state complexity; clear semantics needed to prevent historical rewriting. Increases clarity for analytics that need corrected attributions.

- Leave alone (no change)
  - Action: Keep the original verified status even after contradiction.
  - Costs: Lowest engineering cost, highest risk of misattribution and misleading consumers. This is a defect if your system claims ongoing verification or freshness guarantees.

Practically: use annotate as the baseline behavior; optionally add re-verify for consumers who want corrected lineage, while preserving the original record. Never silently overwrite; use append-only updates for integrity.

Triggers that should cause annotation/downgrade:
- Freshness window exceeded for the assertion used.
- A later CatalogSnapshot asserts a different ModelIdentity for the same (endpoint, name) and overlapping time.
- Verification failure on re-fetch (e.g., endpoint identity mismatch, TLS failure) when refreshing assertions.
- Explicit error report or withdrawal of prior assertion by the provider (store evidence).

4) What parts of Slice B cannot be tested without live network access, and how to govern them

Not fully testable offline:
- Real TLS endpoint identity verification: certificate chains, OCSP/CRL revocation checks, hostname binding, live cert rotations.
- Live catalog retrieval behaviors: headers like Date/ETag/Cache-Control, pagination quirks, eventual consistency, and rate limits.
- Change detection in the wild: how often catalogs change, contradictory updates, and timing edge cases.
- DNS behaviors and failures (including split-horizon, outages, or hijacks).

Governance for these:
- Separate deterministic unit tests (offline) from networked integration tests.
  - Unit tests treat the validator as a pure function over inputs: InvocationRecord, CatalogSnapshot, CatalogVerification, and evidence digests. Use golden fixtures simulating normal, stale, and contradictory sequences.
  - Provide recorded “cassettes” for TLS metadata and catalog payloads to keep integration tests reproducible where possible. Clearly mark when recordings expire.
- Run live integration tests in controlled environments with:
  - Explicit allowlists for endpoints.
  - Rate limiting and backoff.
  - Secrets management for any required credentials.
  - Change management: failures do not auto-downgrade production statuses without human review unless the policy explicitly allows it.
- Record-and-replay harness
  - Capture full evidence (payload digests and TLS peer-identity digests) during live runs; replay those in offline CI to exercise validator logic without the network.
- Policy gates
  - A policy that forbids upgrading identity_verification_status to a broader scope (e.g., from “endpoint+attested” to “independently verified”) unless independent evidence sources are configured and active.
  - SLA for refresh cadence and maximum freshness window; exceeding it triggers automatic annotation rather than silent pass-through.

Defects vs preferences

Defects (must-fix to meet the design’s truthfulness goals):
- Marking an invocation “verified” without binding to a ServiceEndpointIdentity and time-bounded CatalogSnapshot.
- Failing to store evidence (catalog bytes digest and TLS peer identity) used to make the verification decision.
- Collapsing different verification scopes into a single undifferentiated “verified” flag.
- Allowing contradictory assertions for the same key/time to remain “verified” without annotation/downgrade.
- Mutating historical verification in place (erasing what was believed when) rather than append-only updates.

Preferences (policy/implementation choices):
- Exact freshness window durations and grace periods.
- Naming of verification scopes and statuses.
- Whether to use external timestamping services for snapshots.
- Whether to implement automatic re-verify in addition to annotation, and how often to re-run it.
- How aggressively to use recorded cassettes vs. fully live integration tests in CI.
```

## Claude Response

- model: `claude-sonnet-4-5`

````
# Assessment of Slice B: Catalog Identity Resolution

## (1) Smallest Slice B for Status Transition

### Minimum Implementation

The smallest slice requires:

- **ModelIdentity record**: `{requested_name, resolved_canonical_id, resolution_timestamp, catalog_snapshot_ref}`
- **CatalogSnapshot**: `{snapshot_id, capture_timestamp, assertions[]}`
- **CatalogAssertion**: `{provider_id, model_canonical_id, endpoint, assertion_timestamp}`
- **Resolution function**: `resolve(requested_name, catalog_snapshot) → ModelIdentity | null`
- **Status transition logic**: Update `identity_verification_status: unresolved` to `verified` when `InvocationRecord.requested_model_name` has corresponding `ModelIdentity` entry with non-null `resolved_canonical_id`

### Honesty Requirements

For the transition to be honest rather than cosmetic:

1. **Temporal consistency**: The `CatalogSnapshot` referenced must have `capture_timestamp ≤ InvocationRecord.execution_timestamp`
2. **Name-matching determinism**: The resolution function must apply documented matching rules (exact match, alias expansion, version resolution) with no silent fallbacks
3. **Provenance chain**: Every `ModelIdentity.catalog_snapshot_ref` must resolve to an actual `CatalogSnapshot` with retrievable `CatalogAssertion` records
4. **Negative capability**: The system must record when resolution *fails* (requested name has no catalog entry) distinctly from when it *succeeds*, not default unresolvable names to "verified unknown"
5. **Immutability of past resolutions**: Once an `InvocationRecord` transitions to `verified` with a specific `ModelIdentity` reference, that reference remains stable even if later catalog updates would resolve differently

**Defect if missing**: Without temporal consistency (1), a snapshot captured *after* the invocation could claim to verify what the provider offered *before*. Without immutability (5), verification status becomes a mutable opinion rather than a historical fact.

## (2) Catalog Assertion Verification

### The Circular Evidence Problem

Available evidence sources:
- Provider API self-description endpoints (`/models`, `/v1/models`, capability metadata)
- Provider API response headers (model name in usage metadata, rate limit scopes)
- Provider API error messages (unrecognized model name responses)

**Critical defect**: All sources are provider-controlled. The provider asserting "model X exists with capabilities Y" is definitionally not *verification* of that assertion—it is the *primary assertion itself*.

### The Self-Assertion Masquerade

**Failure mode name**: **Verification Collapse** or **Circular Attestation**

Occurs when:
1. System queries `provider.com/api/models` 
2. Receives `{"models": [{"id": "model-foo", "capabilities": [...]}]}`
3. Stores this as `CatalogAssertion`
4. Marks `CatalogVerification.status: verified`
5. Uses "verified" status as evidence of catalog correctness

The circle: Provider API → CatalogAssertion → "verified" → trusted as verification of Provider API

This is **cosmetic verification**—renaming "assertion" to "verified assertion" without introducing independent evidence.

### Honest Alternatives

Given constraint (only provider APIs available), the honest implementation:

1. **Terminology correction**: Rename `CatalogVerification` to `CatalogCapture` with fields:
   - `capture_method`: "provider_self_report"
   - `capture_timestamp`
   - `capture_success`: boolean (did the query succeed?)
   - Remove any `verified` status

2. **Differential verification** (partial honesty): 
   - Cross-check multiple provider endpoints for consistency
   - Record *inconsistencies* between what `/models` lists and what inference endpoint accepts
   - Mark status as `consistent_self_report` vs. `inconsistent_self_report`
   - Flag when provider model list changes unexpectedly (model disappeared, capabilities changed)

3. **External evidence** (requires expansion beyond stated sources):
   - Provider-signed catalog manifests with cryptographic signatures
   - Third-party model registries (industry consortia, academic benchmarks)
   - Historical invocation success/failure rates as probabilistic evidence

**Defect in Slice B as described**: If `CatalogVerification` records exist with a `verified` status derived solely from provider self-assertion, the schema encodes a false claim. The naming implies independent confirmation that does not exist.

**Minimum honest implementation**: `CatalogAssertion` should reference a `CatalogCapture` record documenting *how* and *when* the assertion was obtained, with `source_type: "provider_self_report"` explicit. No separate "verification" layer unless independent evidence exists.

## (3) Handling Stale or Wrong Assertions

### Three Options

**Option A: Re-verify existing records**
- Process: When catalog assertion invalidated, re-run resolution for all `InvocationRecord` entries referencing affected `ModelIdentity`
- Cost: Computational (potentially millions of records), and logical impossibility—cannot re-resolve past requests against past provider state if that state is no longer accessible
- **Defect**: Changes historical facts. If an invocation at T₀ was matched against catalog C₀, later discovering C₀ was wrong doesn't change what *was requested and executed* at T₀

**Option B: Annotate existing records**
- Process: Add `ModelIdentity.resolution_quality` or `InvocationRecord.verification_caveat` field
- Mark affected records: `"catalog_snapshot_later_invalidated"`
- Preserve original resolution but add warning metadata
- Cost: Storage (small), query complexity (must filter/group by quality markers)
- Maintains: Historical accuracy (records still show what was believed at execution time)

**Option C: Leave alone**
- Process: No changes to existing `InvocationRecord` or `ModelIdentity` entries
- New invocations use updated catalog
- Cost: Silent degradation—no indication that historical "verified" status is now suspect
- **Defect**: Implies past verifications remain trustworthy when they don't

### Correct Choice

**Option B (annotation) is the only honest approach** for records that have already transitioned to `verified`.

**Reasoning**: 
- An `InvocationRecord` documents what happened at a point in time
- The `identity_verification_status: verified` meant "resolved against best-available catalog at execution time"
- Learning the catalog was wrong doesn't retroactively change what was *attempted*—it changes our *confidence in the interpretation*
- Annotation preserves both facts: (a) historical resolution, (b) current doubt

**Implementation**:
```
ModelIdentity {
  ...
  resolution_quality: enum {
    "current",           // based on fresh catalog
    "catalog_superseded", // catalog later updated (not wrong, just old)
    "catalog_invalidated" // catalog found incorrect
  },
  invalidation_timestamp: optional<timestamp>,
  invalidation_reason: optional<string>
}
```

**Cost tradeoffs**:
- Re-verification: High compute cost, logical impossibility, corrupts history
- Annotation: Low cost, preserves history, requires query awareness
- Ignore: Zero cost, silent incorrectness, violates provenance purpose

**Defect if choosing A or C**: Option A contradicts immutability principle from (1). Option C makes verification status meaningless over time—"verified" becomes "verified until we discover otherwise, but we won't tell you."

## (4) Parts Requiring Live Network Access

### Components Requiring Network

1. **CatalogAssertion capture**: Must query provider API endpoints
2. **ModelIdentity resolution for new invocations**: Requires current catalog
3. **Catalog freshness validation**: Must check if provider catalog has updated
4. **Endpoint reachability verification**: Confirming `ServiceEndpointIdentity` URLs respond

### Components NOT Requiring Network

1. **Resolution function logic**: Mapping requested names to catalog entries (pure function over captured data)
2. **Status transition logic**: Updating `identity_verification_status` based on existing `ModelIdentity` records
3. **Staleness detection**: Comparing `CatalogSnapshot.capture_timestamp` against policy thresholds
4. **Verification record linking**: Associating `InvocationRecord` → `ModelIdentity` → `CatalogSnapshot`

### Governance Requirements

**Defects introduced by ungoverned network access**:

1. **Test nondeterminism**: Tests depending on live provider APIs fail when APIs are down, rate-limited, or return different data
2. **Captured credentials leakage**: Test suites making real API calls may log or transmit API keys
3. **Cost accumulation**: Repeated test runs against metered APIs
4. **Provider notification**: High-frequency testing may trigger abuse detection

**Governance mechanisms**:

1. **Network access boundary**: 
   - Mark catalog capture functions with `@RequiresNetwork` annotation
   - Dependency injection: `CatalogCaptureService` interface with `LiveCaptureService` and `MockCaptureService` implementations
   - Default test configuration uses mocks

2. **Fixture-based testing**:
   - Commit known-good `CatalogSnapshot` samples to test fixtures
   - Unit tests exercise resolution logic against fixture snapshots
   - No network calls in unit test suite

3. **Integration test isolation**:
   - Separate test suite: `tests/integration/catalog_capture_live_test.py`
   - Explicit opt-in: Requires environment variable `ALLOW_LIVE_CATALOG_TESTS=true`
   - Rate limiting: Runs only on manual trigger or nightly schedule, not per-commit
   - Credential management: Uses dedicated test-only API keys with spend limits

4. **Replay testing**:
   - Record actual provider responses with timestamps
   - Replay tests use recordings to verify parsing/resolution without network
   - Distinguish "recorded on DATE" from "currently valid"

**Defect if ungoverned**: Slice B becomes untestable in CI/CD without either (a) skipping catalog capture tests entirely, or (b) making real API calls on every commit. The first gives false confidence; the second is operationally unsustainable.

**Minimum governance**: 
- `CatalogCaptureService` interface with injectable implementation
- Fixture snapshots for 3+ major providers covering common model names
- Live capture tests in separate suite with explicit opt-in
- Documentation: "Network-dependent tests disabled by default; see docs/testing-catalog-capture.md for local execution"

---

## Summary of Defects vs. Preferences

**Defects** (correctness issues):
- Allowing verification status transition without temporal consistency (1)
- Naming provider self-assertion as "verified" without independent evidence (2)
- Re-verifying past records or ignoring invalidation (corrupts history or hides problems) (3)
- Unmarked network dependencies causing test suite brittleness (4)

**Preferences** (design choices with tradeoffs):
- Exact schema field names (`resolution_quality` vs. `verification_confidence`)
- Annotation verbosity (minimal flag vs. detailed audit trail)
- Integration test trigger frequency (nightly vs. weekly)

The core defect risk in Slice B: **building verification theater**—a system that uses the word "verified" for self-asserted, non-independent, potentially stale data, giving users false confidence in identity resolution accuracy.
````
