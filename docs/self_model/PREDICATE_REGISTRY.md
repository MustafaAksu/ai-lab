# Predicate Registry

Registry of relation predicates used by AI-Lab, in the `GraphRelation` shape
of `ai_lab/documentation/graph_neighborhood.py` (`source_id`, `predicate`,
`target_id`, `relation_source`, `authoritative`, `scope`, `evidence`). No
parallel edge vocabulary exists; ABS-0004 Section 5 adopts this shape as a
constraint.

Each entry records source type, target type, meaning, cardinality, inverse,
temporal semantics, transitivity, evidence requirement, and authoritative
default. A predicate absent from this registry may not be emitted.

## Slice A predicates (ABS-0004 Section 5, PLAN-20260722-0001)

These seven are the complete Slice A set. No predicate outside this list may
be introduced by that slice (WARR-20260722-0001 condition 8).

### produced_by

- source type: artifact identifier (for example a comparison artifact id)
- target type: invocation id
- meaning: the artifact was produced by that invocation. Production, not
  approval: producing an artifact grants no authority to accept it
  (ABS-0004 4.9).
- cardinality: an artifact may be produced by many invocations; an
  invocation may produce many artifacts
- inverse: produces (not emitted in Slice A)
- temporal semantics: fixed at production time; never revised
- transitive: no
- evidence requirement: the invocation record path
- authoritative default: false (diagnostic seed until an admission consumer
  exists)

### executed_by

- source type: invocation id
- target type: executor identity reference (model, tool, or human)
- meaning: the invocation was performed by that executor. In Slice A the
  reference is the requested model name; resolution to a ModelIdentity is
  Slice B work, and the record carries
  `identity_verification_status: unresolved` until then.
- cardinality: exactly one per invocation
- inverse: executed (not emitted in Slice A)
- temporal semantics: fixed at execution time
- transitive: no
- evidence requirement: the invocation record path
- authoritative default: false

### requested_via

- source type: invocation id
- target type: service endpoint identifier
- meaning: the invocation was requested through that API surface. Endpoint
  diversity never implies model independence (ABS-0004 4.2).
- cardinality: exactly one per invocation
- inverse: served (not emitted in Slice A)
- temporal semantics: fixed at execution time
- transitive: no
- evidence requirement: the invocation record path
- authoritative default: false

### used_execution_profile

- source type: invocation id
- target type: `<invocation_id>::execution_profile`
- meaning: the configuration in effect for the invocation, including the
  output-token limit. Configuration changes the profile, never the executor
  identity (ABS-0004 4.8).
- cardinality: exactly one per invocation
- inverse: configured (not emitted in Slice A)
- temporal semantics: fixed at execution time
- transitive: no
- evidence requirement: the invocation record path
- authoritative default: false

### used_inputs

- source type: invocation id
- target type: `<invocation_id>::effective_input_manifest`
- meaning: the information that could influence the result. The target is
  exactly one manifest, never an individual input artifact; the manifest
  carries `completeness_attestation` stating whether it is exhaustive for
  all effective-input channels (ABS-0004 4.12 and Section 5 notes).
- cardinality: exactly one per invocation
- inverse: informed (not emitted in Slice A)
- temporal semantics: fixed at execution time
- transitive: no
- evidence requirement: the invocation record path
- authoritative default: false

### member_of

- source type: invocation id
- target type: session identifier
- meaning: the invocation belongs to that continuity boundary. Session
  identity is a field, not a Run or ProtocolRound object; those remain
  deferred (ABS-0004 Section 11, WARR-20260722-0001 condition 5).
- cardinality: at most one session per invocation; a session may have many
  invocations
- inverse: contains (not emitted in Slice A)
- temporal semantics: fixed at execution time
- transitive: no
- evidence requirement: the invocation record path
- authoritative default: false

### spawned

- source type: parent invocation id
- target type: subordinate invocation id
- meaning: the parent invocation caused the subordinate execution. Required
  by composite-executor disclosure: authority cannot be acquired through an
  opaque wrapper (ABS-0004 P4 and 4.7). `called` was dropped in ABS-0004 v4
  as an undefined duplicate; `spawned` is the sole subordinate-execution
  predicate for all executor kinds.
- cardinality: a parent may spawn many; a subordinate has one parent
- inverse: spawned_by (not emitted in Slice A)
- temporal semantics: fixed at execution time
- transitive: no. Ancestry traversal is Slice D work and must walk the graph
  explicitly rather than assume transitivity.
- evidence requirement: the invocation record path
- authoritative default: false

## Deferred predicates

`resolved_to`, `asserted_by`, `concerns`, and `verifies` belong to Slice B;
`assigned_role`, `authorized_by`, `authorizes` to Slice C; `admitted_by`,
`claim_derived_from`, `transformed_from`, `copied_from`, `summarized_from`,
`used_prompt`, `continued_from`, and the decision predicates to Slice D or
later. They are defined in ABS-0004 Section 5 and are not registered here
because no slice has been admitted to emit them.
