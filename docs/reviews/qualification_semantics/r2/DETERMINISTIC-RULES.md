# Deterministic qualification assessment rules — r2

[ALG] **Proposed contract, not admitted implementation.** Version:
ai_lab.qualification.r2/1. The [schema](ASSESSMENT-SCHEMA.json) fixes record
names, required fields, nullability and closed vocabularies. These rules fix
semantic checks that JSON Schema cannot establish. Production code is unchanged.

## 1. Entry points, domains and result meanings

Two future entry points are specified: evaluate_production_r2 and
evaluate_synthetic_r2. The selected entry point fixes the domain. A matching
domain string is checked, never treated as a privilege grant. Neither accepts
a caller-created trusted/established/complete/test_mode switch.

The consumer obtains its EvidenceContext by exact ID and full digest from its
configured, reviewed anchor. Query may reference that context but cannot replace
its policy, inventory commit, cutoff, selected sources or profiles. A plain
dictionary satisfying the schema does not become an accepted context. No
production context anchor is installed by this proposal.

| Output | Exact meaning in r2 |
| --- | --- |
| supplied_relation | Diagnostic relation over the structurally valid supplied catalog/fixture assertions; makes no governed-coverage claim |
| R_identity | equivalent/non_equivalent/unresolved over the complete, applicable, pinned source set; requires its integrity/applicability/coverage conditions |
| Q_identity | withheld, or conditions_satisfied **only inside a pinned synthetic fixture** with non_equivalent R_identity and all per-kind conditions |
| C3 | violated/unresolved; only an accepted synthetic negative-conflict fixture can establish violated |
| C10 | unresolved throughout r2; receiving-decision/consequence and live review acceptance are outside this input/rule scope |
| Q_C3_C10 | violated exactly when accepted synthetic C3 is violated; otherwise unresolved |

Production Q_identity is always withheld. Q_C3_C10, C3 and C10 have **no positive
value in either domain**. This deliberately bounds 3C to evidence/refusal
checks. A later positive qualification evaluator needs a separately admitted
scope, usable GAP-0008 coverage and applicable review rules.

An invalid assessment envelope returns AssessmentResult with validation_status
invalid, typed validation reasons, unresolved relations, withheld Q_identity
and unresolved constraint findings. There is no success-through-exception path.
A schema-valid but incomplete/adverse evidence set can instead return
validation_status valid with unresolved/violated semantic findings.

## 2. Strict parsing, references and input integrity

P0. Decode UTF-8 JSON; reject duplicate object keys, NaN/Infinity, unknown schema
versions, undeclared fields and nonmatching types. Boolean is not an integer
identity target. No coercion of strings to Boolean, IDs or timestamps.

P1. Timestamps require explicit offsets and real calendar values. Normalize to
UTC instants for comparison; never consult the wall clock inside the evaluator.
Malformed timestamps yield INVALID_TIMESTAMP. An interval whose upper bound is
earlier than its lower bound yields INVALID_INTERVAL. Empty intervals at one
instant are valid and inclusive. Shape parsing and these cross-field checks
precede use of a source's claims.

P2. RecordRef/ArtifactRef SHA-256 values use sha256: followed by 64 lowercase hex
digits. Hash the **complete original retained bytes**, not only the fields used
in a legacy schema ID. Verify the pinned Git commit/tree/blob relationship where
present, and recompute catalog/INV schema IDs using their named v1 identity
rules. An ID match is not a byte-integrity, record-kind or truth finding.

Missing expected bytes produce a named missing-item finding; mismatching
available bytes, conflicting bytes under one record ID, malformed linked
records or contradictory identity-bearing fields invalidate the input. Do not
deduplicate by ID alone. Exact duplicate (ID,digest) references are idempotent.

P3. Query subject fields must equal the decoded invocation's kind, executor
reference, occurred_at and model endpoint/name fields. RecordRef targets must
exist in the pinned store. Unsupported kinds or a mismatch cannot redirect a
model invocation into a synthetic human/tool profile.

All reasons are retained. Sort source findings by source_id, side and the source
digest obtained from the pinned inventory;
sort target/reference sets lexicographically. Sort reasons by numeric stage,
ReasonCode declaration order, side and sorted subject references. Diagnostic
order is not an evidence ranking. Result precedence is defined separately below.

## 3. Governed source universe: REPO-CATALOG-ALL-1

The source universe is derived from the consumer's pinned SourceInventory and
ContextPolicy, not from Query or the order of arguments.

I1. Verify the anchor's repository commit and root tree, then recursively
enumerate **every tracked regular file** below these exact roots:

- docs/catalog/eid/
- docs/catalog/mid/
- docs/catalog/snap/
- docs/catalog/cap/
- docs/catalog/payloads/

No caller glob, source-type filter, endpoint filter, latest-file choice or
priority order is accepted. Symlinks/submodules cannot substitute unpinned
external bytes. Inventory entries must match the enumerated paths, blob IDs and
complete SHA-256 values. An extra entry or a changed commit/tree/selector fails
the pin; an omitted required file is INVENTORY_OMISSION.

I2. The anchored inventory also contains known_source_declarations and
omission_declarations. Their retained declaration bytes and their known_at
timestamps are checked against the context's knowledge_cutoff. Relevant
declarations known by that cutoff participate even when their source bytes
were not provided. A declared unavailable source may have an unknown expected
ID/digest; null means unknown and cannot become an affirmative ArtifactRef.
Missing scope details make its relevance undetermined, not irrelevant.

I3. Derive ModelSourceRef rows from every catalog capture and its snapshot,
payload, endpoint and target references. Recompute selected_source_ids; compare
the provided set to that derived set. source_id is the capture ID, with the full
capture digest retained; conflicting content under that ID is invalid. Pair all
captures, including failed and contradicted ones, before query-specific
classification. Do not let the caller supply a reduced favorable list.

A source known by the cutoff cannot disappear by deletion from provided refs,
a changed omission list, an earlier caller cutoff or a different inventory
commit. Each such change either mismatches the pinned context or leaves a
named missing/undetermined item. A new consumer anchor is a separate governed
configuration, not a function argument or retry strategy.

I4. coverage=pinned_inventory_exhausted means that this **bounded declared
universe** was enumerated and all query-relevant items accounted for. It does
not prove that no unknown source exists outside it. Include
OUTSIDE_SCOPE_UNASSESSED in scope diagnostics. A known unavailable potentially
relevant source yields missing_items/undetermined, blocking clean R_identity
and Q_identity. Proven inapplicability needs an intact, pinned declaration;
an untrusted or missing record cannot establish its own exclusion.

supplied_relation can still report the bounded observation that available
assertions agree. It cannot be substituted for R_identity or coverage by any
consumer. The currently unactivated production context and unavailable positive
evidence paths remain explicit unresolved conditions.

## 4. Model endpoint and temporal applicability

M1. Match invocation service_endpoint against endpoint_identifier in **all**
pinned EID records. Exactly one valid, byte-bound matching EID supplies a
catalog-declared endpoint mapping. No match or more than one candidate yields
ENDPOINT_MAPPING_UNRESOLVED. For no exact match also retain
ENDPOINT_ALIAS_UNRESOLVED: r2 supplies no alias rule that could resolve the
spelling. Multiple exact matches retain the mapping reason only. No spelling
is normalized by host/provider/name.

This declared mapping is distinct from affirmatively establishing which endpoint
served the invocation. The production endpoint-binding registry is empty.
No EID string, matching spelling or provider-controlled report clears that
positive binding condition.

M2. Each snapshot.service_endpoint_id must dereference to a valid EID. A source
declaring another valid, uniquely mapped catalog endpoint is
inapplicable/WRONG_ENDPOINT within that declared-catalog scope. A missing
or ambiguous EID is undetermined. capture.snapshot_id must equal the actual
snapshot schema ID and digest-bound link; inconsistency is
CAPTURE_SNAPSHOT_MISMATCH and invalid input. Endpoint spelling is never compared
directly with an EID-* string.

M3. ContextPolicy fixes a nonnegative integer freshness_window_days; the default
is 30 and the field is required. Query cannot change it. For each subject time t,
source observed time o must satisfy o <= t and t-o <= window. Equality is included.
A future observation or expired source is inapplicable with its distinct reason.

These catalog rules also apply in retrospective mode: r2 does not infer a
historical mapping from a later catalog snapshot simply because it mentions an
earlier valid_from. Later verification can assess an already event-applicable
source. Tool/human profiles use their own validity/revocation rules, not this
catalog freshness window.

M4. Availability is separate from declared observation/capture timestamps:

| Mode | Availability/witness knowledge bound |
| --- | --- |
| event_time | min(subject occurred_at, context knowledge_cutoff) |
| retrospective | context knowledge_cutoff, which must not precede either subject event |

An AvailabilityEvidence record must bind the exact snapshot, capture and payload
byte references, available_at, observer, observation and rule-version references.
Internal chronology must satisfy observed_at <= captured_at <= available_at.
Contradictory internal chronology is INVALID_TIMESTAMP. Timestamp equality is
allowed. Separately compare available_at with the applicable bound: a
demonstrably later source is excluded/EVIDENCE_AFTER_CUTOFF, not a timestamp
format or chronology error;
missing proof of availability is EVENT_AVAILABILITY_UNPROVEN and undetermined.

In r2 only exact availability rows in the immutable synthetic model fixture
supply the fictional proof. The production availability registry is empty:
Git commit dates, copied metadata, observed_at/captured_at strings and the
existence of bytes now do not establish their availability at a historical
event. This limitation can leave clean production R_identity unresolved while
supplied_relation remains a catalog-declared diagnostic.

A later import is not a new capture. Earlier retained capture/availability
evidence may be referenced with its original times; do not change captured_at
to import time or invent an earlier time for a late capture. Retrospective
results are new assessments linked through their exact query/context and subject
references. When the pinned context includes an earlier assessment, preserve
its ArtifactRef in provided_artifact_refs as a historical link; it is not new
identity evidence. Original capture-time identity status and earlier resolution
bytes are never replaced.

## 5. Successful capture, assertion semantics and MID targets

M5. Structurally valid capture_success=false supplies **no positive support**.
First retain any proven endpoint/time exclusion. For a potentially relevant
failed capture, do not use its alleged payload to prove requested-name absence:
return CAPTURE_UNSUCCESSFUL and unresolved applicability/coverage. An unrelated,
intact failed-source declaration can be excluded; this is not a global veto.

For a successful capture, require retained payload bytes matching content_digest
and the pinned payload ArtifactRef. A schema-valid digest string alone is
insufficient. r2 checks the asserted snapshot and its payload linkage; it does
not infer that the provider's underlying identity claim is true.

M6. Select resolves_to assertions whose subject exactly equals the requested
model name. If none exist in an intact successful snapshot, the source is
inapplicable/ASSERTION_NAME_ABSENT. Other predicates cannot supply identity.

For each matching assertion:

| Field | r2 rule |
| --- | --- |
| scope=null | No extra scope beyond this snapshot endpoint, requested name, predicate and validity interval |
| Non-null string scope | Unsupported; if otherwise relevant, ASSERTION_SCOPE_UNSUPPORTED/undetermined |
| Non-string/non-null scope | Invalid decoded shape |
| valid_from / valid_until | Real explicit-offset instants; inclusive interval; null upper bound means open-ended |
| superseded_by=null | No supersession assertion |
| Non-null superseded_by | SUPERSESSION_UNRESOLVED if material; neither latest timestamp nor a link silently removes a conflict |

A valid interval excluding t is inapplicable/ASSERTION_INTERVAL_INAPPLICABLE.
A reversed interval is malformed, not ordinary inapplicability. Unsupported
scope is not a wildcard. Query-independent input-integrity/schema failures
remain invalid even if an untrusted field claims the record is irrelevant;
semantic exclusions apply to structurally intact sources.

M7. A resolves_to target must be a nonempty MID-* string. Reject numeric/Boolean
values, empty/arbitrary strings and mixed scalars as ASSERTION_TARGET_INVALID
before equality, set or sorting operations. A string identifying an existing
record of another kind yields TARGET_WRONG_KIND. Otherwise require MID syntax,
look up the target in the pinned MID set and verify record_kind=model_identity,
v1 schema ID and full retained bytes. A well-formed missing MID yields
TARGET_MISSING. Report the precise case; no bare ID is a binding.

M8. release_identity must be a nonempty string. The literal unknown is an
explicitly unknown release. A valid unknown-release MID may support a
catalog-record-level supplied/R_identity relation when all other clean
aggregation conditions hold; set TARGET_RELEASE_UNKNOWN and withhold
Q_identity. It cannot establish stable release identity. Nonliteral release
strings likewise need the appropriate witness, not merely syntactic acceptance.
The 132 historical unknown-release records stay byte-identical.

## 6. Complete model aggregation and relation

A1. Evaluate every selected source; do not return on the first success.
Keep applicable, inapplicable and undetermined findings separately.

A2. A capture-wide contradicted status blocks every otherwise applicable mapping
from that capture. A valid snapshot with multiple applicable targets yields
TARGETS_AMBIGUOUS. Different valid targets across applicable sources yield
TARGETS_CONFLICT. A corroboration label cannot overrule a conflicting provider
mapping. No rank, vote, last/newest winner or unreviewed supersession rule exists.

A3. For each side, a clean resolved catalog target exists iff:

    validation is valid
    AND pinned inventory coverage is exhausted for the query
    AND no potentially relevant item is undetermined/missing
    AND no applicable contradiction, ambiguity or target conflict exists
    AND the union of applicable valid MID targets contains exactly one target

Unknown release affects positive identity sufficiency, not the existence of the
attributed catalog record. Preserve all source classes and witnesses as sets;
do not replace a self-report's class with that of another source.

A4. If both sides cleanly resolve, equal canonical MID records yield equivalent;
distinct canonical records yield non_equivalent within the stated catalog-record
scope. Otherwise R_identity is unresolved. Cross-kind pairs always yield
unresolved/CROSS_KIND_UNDEFINED. Diagnostic supplied_relation may be computed
over valid supplied assertions alone, with missing-context/coverage limits
attached; even that diagnostic cannot use failed captures, unsupported targets
or ambiguous/conflicting supplied evidence.

## 7. Corroboration-witness acceptance and full pair matrix

W1. A CorroborationWitness is a proposed record, not an accepted claim of success.
Its subject binds the exact endpoint ArtifactRef, requested name, target MID
ArtifactRef, event time and property_id=model_reference_resolves_to_identity.
It also binds every evidence digest, verifier executor/version, rule version,
verification artifact, assessed_at, applicable interval and assessment scope.

W2. SYN-MODEL-WITNESS-1 accepts a necessary-condition witness only when **every**
field and referenced byte matches one unique row of the harness-pinned fixture
bundle. All referenced bytes must exist; the fixture verification artifact and
scope must be the ones named by that row. assessed_at and availability respect
the mode's bound, and the interval covers the event without revocation.
A witness ID, positive string or catalog evidence label is insufficient.

W3. Live corroboration rules are **not** enabled. Production witnesses have no
admitted verifier/issuer/acceptance path in this slice. Even a structurally
perfect witness returns Q_identity=withheld/PROFILE_UNAVAILABLE. This does not
amend DECISION-20260814-0001: the future compatibility/threshold change requires
its explicitly governed successor at implementation admission.

W4. The model synthetic identity condition additionally requires non_equivalent
R_identity, known release bindings, the complete context/coverage checks, and a
matching corroboration witness on each side. The independently_corroborated
capture classification remains a necessary declared model condition for its
witness source; source_type or classification alone cannot make a witness valid.
Agreeing weak sources remain visible and cannot fabricate or erase a witness.

For a clean non_equivalent synthetic pair, let V mean an exact valid fixture
witness, M missing and X invalid/misbound. The complete witness matrix is:

| Left \ Right | V | M | X |
| --- | --- | --- | --- |
| V | conditions_satisfied | withheld | withheld |
| M | withheld | withheld | withheld |
| X | withheld | withheld | withheld |

Equivalent or unresolved R_identity, unknown release, unresolved coverage or a
blocking source finding changes **every cell** to withheld. Production changes
every cell to withheld regardless of labels. The four legacy content-evidence
classes are not ranked; their 4×4 pair combinations cannot substitute for this
witness test. Synthetic necessary-condition success is not C3/C10 clearance.

## 8. Frozen synthetic tool and human profiles

The trusted test harness fixes the complete fixture bundle ID/digest **before**
receiving Query. A test may construct another explicitly pinned fixture to test
a counterexample; the query cannot replace its issuer/principal/actor tables.
Schema-example dummy digests are shape examples, not digest-verified fixtures.

Shared interval rule: valid_from <= event <= valid_until where present, and
revoked_at is null or event < revoked_at. Revocation at the event is effective.
No automatic latest-row choice, reassignment or expiry extension is allowed.
All alias matches are exact strings and all referenced artifact bytes are
checked. Conflicting applicable rows are BINDING_CONFLICT; missing rows are
BINDING_MISSING; effective revocation is BINDING_REVOKED.

### SYN-TOOL-1

Namespace is fixture:tools. ToolIssuerRow establishes only the fictional issuer's
namespace membership. ToolReleaseRow binds that issuer, tool_identity,
version_identity, interval and artifact_refs. A matching ToolAliasRow resolves
the query reference to that exact pair. ToolExecutionRow must bind the exact
invocation digest and event time to an executed artifact in that release and
its pinned observation bytes.

Require all four links and unique applicable rows. Compare (tool_identity,
version_identity) only after binding validation. Same pair is equivalent;
distinct established pairs in the fixture namespace are non_equivalent.
Artifact/configuration equality is not the identity test. Missing full execution
disclosure blocks the applicable standing claim separately; it erases the
identity relation only when it prevents knowing what tool/version ran.
Production tool bindings always remain unresolved/PROFILE_UNAVAILABLE.

### SYN-HUMAN-1

Namespace is fixture:human-persons. A HumanPrincipalRow maps one immutable
fictional_person_id to one principal_id, bijectively within the pinned fixture.
A person cannot be duplicated by assigning another role/account/key/principal
label. Inconsistent person/principal rows are BINDING_CONFLICT.

HumanAliasRow binds the exact account/key/display alias to that principal for
the event interval. A separate HumanActorRow must match the exact invocation,
event and principal and its actor_observation_ref bytes. Shared credentials
without a unique actor row are ACTOR_UNRESOLVED; delegation/role changes never
rename the actor. Both reference and actor links are required.

Same fictional person/principal yields equivalent. Distinct rows under the
fixture's bijective person semantics yield non_equivalent. These are fictional
premises, not human identity documents or a live enrollment registry. Production
human comparisons remain unresolved/PROFILE_UNAVAILABLE. No model catalog
evidence-class vocabulary is applied to either profile.

For tool/human fixtures Q_identity can be conditions_satisfied only for a clean
non_equivalent relation and all the profile checks above. The result remains
synthetic and cannot enter a production binding or qualification store.

## 9. C3/C10 refusal rules and precedence

C1. Read only digest-bound context evidence, not caller booleans asserting full
ancestry or independence. Required edge classes/obligations come from the pinned
context and must include input, output, derivation, subordinate-influence and
inherited-state obligations wherever applicable. An omitted class cannot be
made inapplicable by deleting it from Query. r2 supplies no positive ancestry
profile; no path-found result or complete flag can yield positive qualification.

C2. A C3Context names the adjudicator, exact claim, directional paths, retained
edge evidence and ancestor identity assessments. Production has no accepted
directional-evidence rule, so production C3 is unresolved. Opaque edge byte
digests, spawned alone, shared prompt, provider, session or kind tags do not
establish direction in any domain.

The negative-only **SYN-C3-CONFLICT-1** fixture sub-rule is fixed inside the
same harness-pinned SyntheticFixtureBindings, not selected by Query. It has
context_rows with the complete C3Context, explicit edge rows and ancestor
assessment rows. These are stipulated fictional directional premises, not
observations of live ancestry or evidence of complete coverage.

For synthetic evaluation:

1. Require one unique exact context row. No matching row gives
   ANCESTRY_UNRESOLVED; conflicting matching rows give BINDING_CONFLICT and
   unresolved. Identical repeated bytes add no evidence. Check every reference
   against the fixture's retained bytes before evaluating a path.
2. Each edge row pairs edge_ref with its complete decoded
   synthetic_directed_edge object: fixed rule/domain/version, source_ref,
   target_ref, edge_class and observation_ref. All must match exactly. An
   unbound, mismatched or unsupported edge cannot establish a directional step.
3. Require edge count = node count - 1, exact ordered source/target linkage,
   checked node/observation digests, and a final node equal to claim_ref.
   Every path step must be one of those accepted fictional edge rows. No
   transitive step is inferred from a shared input or adjacency of file names.
4. An accepted path beginning at adjudicator_ref yields
   DIRECT_LINEAGE_CONFLICT and C3=violated.
5. Otherwise, a path beginning at an ancestor invocation needs a unique exact
   ancestor_assessment_row linking that invocation, adjudicator, retained
   assessment and identity query. The old query/result/context/fixture must
   form an earlier, separately byte-bound **acyclic provenance dependency
   graph**; none can depend back on the current fixture or current context.
   Check those bytes and their internal links, but treat the old context,
   policy and R label as history only. Validate both old Query Subject objects
   against current-pinned invocation bytes; their pair must be exactly the
   ancestor and adjudicator, in either order. An internal identity-only
   evaluation takes that validated subject pair plus the **current** consumer
   inventory, profiles and cutoff. It neither calls the old public Query
   adapter nor adopts its context or recurses into C3/C10. Require the newly
   computed valid R_identity=equivalent. This yields EQUIVALENT_ANCESTOR and
   C3=violated; the stored equivalent label/hash is insufficient.
6. Any established conflict in steps 4–5 dominates missing unrelated coverage.
   With no such conflict, C3 is unresolved, including seemingly complete
   fictional no-conflict evidence. Invalid input envelopes still follow §1.

Missing relations/coverage or a tool adjudicator compared with model/human
ancestors cannot supply step 5 equivalence. Cross-kind remains unresolved.
SYN-C3-CONFLICT-1 creates no positive ancestry profile or production binding.
Step 3 therefore cannot establish Step 5 readiness.

The step5 provenance graph is a reference dependency graph, not the directional
influence graph. Check it before recursive dereference. A cycle or current
fixture/context back-dependency gives invalid input with
CONTEXT_ANCHOR_MISMATCH at stage7. An earlier identity-only fixture with empty
C3 rows supplies an acyclic construction; its prior result still grants no
current standing. The current context must include the exact ancestor/adjudicator
invocation bytes needed for the fresh identity-only assessment.

C3. C10Context.run freezes the exact VerificationRun, property, verifier
executor/version, rule/test version, input manifest, environment, result,
subject output and producer ModelIdentity references. Refuse a mismatched
reference/digest, a review of another run/property, or missing required evidence.
ReviewBinding must match all those run fields and identify the reviewer
invocation/executor, every C5 dimension's evidence and its outcome artifact.
A matching reference or asserted positive outcome is not an accepted
independence review. A run/property mismatch retains REVIEW_LINKAGE_MISMATCH;
missing or unsupported review evidence retains REVIEW_INDEPENDENCE_UNRESOLVED.

Known shared verifier code/schema/test/configuration ancestry is affirmative
shared ancestry only under an applicable accepted directional-evidence rule.
r2 has no such live rule; unaccepted claims remain attributed diagnostics.
Unknown ancestry remains unknown; do not label it independent **or self-authored**
by default. Shared ancestry alone is not a C10 violation. This input schema
does not bind a receiving decision, its consequence or an attempted reliance,
and no live review-admissibility rule is enabled. Therefore **C10 is always
unresolved in r2**, including complete synthetic necessary-condition evidence.
Missing/mismatched references and alleged shared ancestry remain named refusal
findings; they do not manufacture a high-consequence violation. A later scope
must bind those additional premises before deriving C10=violated. No canonical
verifier_lineage_status is written or upgraded.

C4. On valid inputs, violated dominates unresolved **within** the named
constraint; missing coverage cannot hide a proven conflict. Q_C3_C10 combines
the two findings by that same rule. Invalid envelopes follow §1's invalid
result instead; they never create clearance. Any typed refusal, disabled path,
unsupported version or adapter failure must remain non-permitting.

## 10. Determinism and implementation admission boundary

Input order, exact duplicate insertion and left/right swapping cannot change a
semantic result except for exchanging side-specific evidence. Preserve every
reason, support set, exclusion and unresolved obligation; no last-reason default.

The [consumer contract](CONSUMER-COMPATIBILITY.md) governs all old public paths
and safe rollback. The [schema checker](check_schema_examples.py) checks shapes
and parsing examples only. It does not execute these rules or fix the baseline.

No implementation admission is created here. The exact schemas, these rules,
the result/consumer contract and the expanded falsifier matrix must be reviewed
together before 3A begins. The remaining lack of live evidence is represented by
closed outcomes, not an unspecified developer-selected trust policy.
