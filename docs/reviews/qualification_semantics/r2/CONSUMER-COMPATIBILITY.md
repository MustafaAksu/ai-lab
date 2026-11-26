# Consumer, compatibility and rollback contract — r2

[ALG] Proposed interface changes for later 3A–3C admission. No current function
is changed by this PR. The exact shapes are in [ASSESSMENT-SCHEMA.json](ASSESSMENT-SCHEMA.json);
evaluation is specified in [DETERMINISTIC-RULES.md](DETERMINISTIC-RULES.md).

## 1. Existing surfaces and required treatment

Source inspection and isolated probes are retained in
[R2-BASELINE-OBSERVATIONS.md](R2-BASELINE-OBSERVATIONS.md). No production
authorization consumer of equivalence/blocks_adjudication was found under
ai_lab, scripts or .github at baseline 5515f558. That does not make the public
functions safe for new consumers.

| Surface | Future r2 contract |
| --- | --- |
| catalog.validate_assertion / validate_catalog_record | Historical v1 shape/ID checks remain identifiable. A pass never substitutes for target dereference, byte integrity, interval validity, availability or evidence sufficiency. |
| catalog_resolution.resolve_identity | Old argument set without the pinned context returns resolved=false and LEGACY_CONTEXT_REQUIRED. With an explicit accepted context, delegate to the shared r2 source/assessment pipeline; no single-source shortcut. |
| executor_equivalence._resolve_one | Remove first-success/last-reason semantics from the active r2 path. It is not an alternate public proof route. Any retained historical decoder is separately named and produces diagnostics only. |
| executor_equivalence.equivalence | Without context: unresolved with LEGACY_CONTEXT_REQUIRED. With context: project the r2 relation and preserve an assessment reference; never select arbitrary captures or synthesize a context from names. |
| EquivalenceResult constructor and blocks_adjudication | The legacy Boolean returns true unconditionally in r2, including manually constructed and synthetic results. Model evidence labels cannot make it false. New callers consume the structured three-axis result. |
| build_resolution_record / validate_resolution_record | v1 RES parsing remains historical compatibility. A supplied resolved dictionary is not accepted as an r2 assessment or binding. No bool(string) conversion, evidence-enum upgrade or unchecked target projection. |
| write_resolution_record | Existing overwrite behavior cannot be reused for new r2 assessment persistence. New writes require the r2 checked envelope, immutable content identity and collision-safe storage. |
| resolution_relations / GraphRelation | Historical seeds remain authoritative=false. Their existence or dataclass annotation does not validate a MID or establish binding/coverage. No graph join upgrades a v1 RES seed into Q evidence. |
| write_catalog_records / capture_catalog.py | General legacy catalog-writer hardening is outside this slice. r2 readers consume pinned commit/blob/digest bytes, never mutable latest paths; overwrites cannot silently change an accepted context. |
| Tests / historical artifacts | Keep all retained old records. Replace assertions pinning unsafe behavior only in separately admitted implementation, preserving the baseline probe. Do not modify old evidence to satisfy new rules. |

No fallback after missing context, invalid input, unsupported schema/rule,
failed witness, disabled feature or storage failure can call the old permissive
resolver. The new structured result is the only r2 input to an evidence-condition
consumer, and its serialized presence is still not proof that its premises hold.

## 2. Legacy return projection

The old resolver dictionary cannot represent the new three axes. Its safe
projection in this bounded slice is:

    resolved = false
    resolved_identity = null
    reason = LEGACY_CONTEXT_REQUIRED if context is absent
             else LEGACY_POSITIVE_DISABLED
    assessment_ref = checked r2 assessment reference, when one exists

The catalog-declared result remains available through the new supplied_relation
and R_identity fields, not through a historical resolved=true shortcut.

The equivalence projection may expose the structured assessment's R_identity
for diagnostic compatibility when context is accepted, but
blocks_adjudication=true in every case. Without context its relation is
unresolved. A constructed EquivalenceResult with labels alone cannot provide an
assessment reference or a false Boolean.

This deliberately changes the old positive ABI. Before implementation, the
admission must explicitly reference this compatibility change and the governed
successor to DECISION-20260814-0001's Boolean selection behavior. This PR issues
neither that successor nor an admission. The historical decision remains intact;
its distinction between asserted relation and permission remains preserved.

## 3. Historical annotation and strict assessment storage

IdentityResolution v1 names one snapshot/capture. It is not silently reinterpreted
as a complete multi-source assessment, a corroboration witness or a C3/C10 check.
The existing builder's acceptance of caller outcomes and deterministic-path
overwriting are retained baseline findings, not endorsed r2 write semantics.

Future r2 assessment persistence must:

1. Validate the output schema, context/domain reference and rule version, and
   recheck reference/digest linkage against the exact input manifest.
2. Preserve complete serialized bytes and derive storage identity from their
   complete digest. A display assessment_id is not overwrite authority.
3. Write atomically without replacing an existing different byte sequence.
   Identical-byte replay is idempotent; same display ID with differing bytes is
   an explicit conflict and is not published. A legitimate later assessment
   receives a new display ID; any earlier assessment included by the pinned
   context remains a historical ArtifactRef in provided_artifact_refs.
4. Refuse cross-domain writes. Synthetic results stay in the isolated fixture
   output store; they are not canonical live bindings, VERIFY records or
   lineage findings.
5. Publish only after validation and successful atomic storage. Failure produces
   a bounded diagnostic and no accepted assessment.
6. Keep the old InvocationRecord, catalog capture, RES and VERIFY bytes unchanged.
   Readers must select the rule/version named by the stored record and never
   reinterpret old evidence under a newer schema by default.

No general claim of current append-only enforcement is made: the baseline probe
demonstrates same-ID overwrites in both existing writers.

## 4. C3/C10 consumer boundary

R_identity, Q_identity and Q_C3_C10 are distinct fields. Production Q_identity
is withheld; C3 is violated/unresolved and C10 is always unresolved in either
domain. Only the pinned synthetic negative-conflict rule can establish a C3
violation in r2; opaque/live edge evidence remains unresolved.
Neither a successful shape check nor a synthetic necessary-condition result
can become an independent/authorized result at a consumer boundary.

A consumer must check domain, exact query/context references and rule version
before reading any field. It cannot infer missing fields from blocks_adjudication,
a PASS string, a v1 resolution, an evidence-class label or an empty ancestry
array. Direct/equivalent conflicts remain blocking when coverage is incomplete.

A tool adjudicator facing model/human ancestry retains unresolved cross-kind
comparisons. Completion of Step 3 therefore supplies neither Step 4 authority
machinery nor Step 5 bootstrap readiness.

## 5. Safe deployment and rollback sequence after future admission

Before any new evidence-condition consumer is connected, install and test the
non-permitting compatibility boundary. It remains outside any optional enabling
switch for the new evaluator.

If the evaluator fails, is disabled, or must be reverted:

- Disable its consumption and return typed withheld/unresolved findings.
- Retain the refusal shim or remove the affected public route entirely.
- Preserve diagnostic and evidence records for the failed version.
- Do not restore an old resolved=true projection, label-based false Boolean,
  first-success fallback or mutable-path read.
- A whole-commit rollback that would remove the refusal boundary requires the
  affected consumers/routes to be disabled first and to remain disabled.

Rollback is operationally a withdrawal of reliance, never reactivation of the
known R13/R14 permitting path. These obligations belong in the future admitted
implementation's integration and rollback tests; they are not executed changes
in this proposal.
