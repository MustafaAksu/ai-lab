# Slice C admission round: consolidated findings

Round COMP-0039..0046, eight questions, sixteen complete responses. For the
operator's adjudication of ABS-0004 v7 and PLAN-20260723-0002, both of which
remain **proposed, not admitted**.

Findings are organised by the block of source text they concern, not by the
question that produced them, because several findings span questions that could
not see each other. Block ids and hashes are given so that an amendment which
changes a block breaks the citation and forces this record to be revisited.

## How to read attributions

Three kinds of statement appear here and must not be conflated.

- **Reviewer findings**, attributed to question and provider. These are claims
  the reviewers made. Their being recorded here is not endorsement.
- **Resolutions**, marked `[RESOLVED]`. Where the reviewers disagreed, and the
  disagreement was settled against records neither reviewer was given.
- **Drafting-executor analysis**, marked `[ANALYSIS]`. Assessment by the
  drafting executor from records outside every reviewer's evidence set. This is
  not a third witness. It is one party's reading, offered for adjudication.

## Witness independence

The two providers are `gpt-5.6-terra` and `claude-sonnet-5`, asked separately
with no sight of each other. Under ABS-0004 v7 constraint C3 this is
`independence_unresolved`, never an independent path: every InvocationRecord in
this repository carries unresolved executor equivalence. Convergence between the
two witnesses is evidence, and it is not two-witness corroboration in the sense
C3 reserves for established identity independence.

Sixteen of sixteen tier-1 invocations returned complete responses. The absence of
truncation is observed from response content only: InvocationRecord carries no
`stop_reason` or output-token field, which is itself an open defect (see
"Unaddressed" below).

---

## 1. The pattern the round found

Across Q1, Q2, Q3 and Q5 the witnesses converged on one structural observation,
each reaching it from a different question:

**v7 is right that verification is impossible, and its constraints nonetheless do
less than their text implies, because their operative consequences defer to
machinery that does not exist.**

| constraint | stated force | force today |
| --- | --- | --- |
| standing authority recorded, never verified | "every authorization resting on it" legible | recording; completeness unenforced |
| scope breadth legible as wide | breadth cannot be misdescribed | a label; no consequence attaches |
| self-issued disqualified from independence | changes what the record can be used for | inert until AuthorizationPolicy exists |
| plan `check_depth` | consumer "cannot" misread | constant value; discloses shape, not instance |

This is the defect ABS-0004's own P6 names: a record whose label implies
confirmation where none exists is a defect regardless of the correctness of its
contents, because consumers read the label, not the caveat. P6 was itself derived
from COMP-0035, where two witnesses independently found a name implying
self-verification. The round is the third occurrence of the pattern, and the
second inside ABS-0004 itself.

---

## 2. ABS-0004 v7

### 2.1 Standing-authority constraint

`ABS-0004:v7:S3#adopted_constraint:a-standing-authority-claim-is-reco`
sha256 `22d6ac40afc0ecb0` · 66 edges from Q1, Q2, Q3, both providers

**Finding (Q2, both).** The sentence "the claim, its declared scope, and every
authorization resting on it are legible and attributable" asserts completeness the
mechanism does not deliver. Claude's form is stronger: Section 3 contradicts
itself two paragraphs apart, since the subordinate-inheritance rule concedes that
undeclared subordinate execution occurs and is "a disclosure violation under 4.7",
so authorizations can exist that this constraint does not make legible.

**Finding (Q2, gpt).** "It has no means to do so" over-reaches. P7 supports only
that *repository arrangements* cannot verify entitlement, not that AI-Lab has no
means at all, including external processes outside the repository.

**Recommendation.** State visibility as the intended and bounded function, scoped
to authorizations that are declared and correctly chained, and say plainly that
undeclared ones are not made visible by this constraint.

### 2.2 Scope-breadth constraint

`ABS-0004:v7:S3#adopted_constraint:scope-breadth-is-visible-not-bound`
sha256 `5f71607ef126889e` · 37 edges from Q1, Q2, Q3, both providers

**Finding (Q1, claude).** v7 bundles three adopted constraints with different
justificatory status. P7 entails the standing-authority clause; it does not entail
the scope-breadth clause, because "may be arbitrarily wide" is a statement about
what the system *accepts and acts on*, not about what it can *verify*.

**[ANALYSIS] Q1's supporting premise is false, and the conclusion needs a
different footing.** Q1 charged that v7 transferred a justification earned against
self-issuance onto scope breadth. COMP-0037 refutes this. Claude's own review
there found that nothing constrained "the *content* or *breadth* of what may be
declared as `authority_scope`", and gpt-5.6-terra recommended rejecting scopes
"that are universal, unparseable, or circular". Scope was squarely implicated, so
the transfer was not unearned.

The record shows something more useful. The two COMP-0037 attacks ran in
**opposite directions**: Claude's used a scope too *wide*, gpt's used one
*narrowly tailored to authorize itself*. A breadth bound stops neither pair. The
defect is not width, it is that the declarant defines its own scope — which means
v7's refusal to bound width is defensible for a reason v7 never gives, and Q1's
proposed remedy (disqualify wide scopes from independence) fails against gpt's
narrow-tailoring path.

**[ANALYSIS] What v7 does not disclose.** gpt-5.6-terra explicitly recommended
rejecting universal scopes in COMP-0037. v7 adopts the opposite. The `[OPEN]`
paragraph describes COMP-0037 only as "the same self-authorization path", omitting
that both reviewers recommended mechanical scope bounding. v7 under-reports what
it is overriding.

**Recommendation for v8.** Reframe from "how wide may a scope be" to "what makes
a scope declaration something other than self-assertion" — the question v7's own
`[OPEN]` paragraph poses and leaves open. Disclose the overridden recommendation.

### 2.3 Self-issued constraint

`ABS-0004:v7:S3#adopted_constraint:self-issued-authorization-is-marke`
sha256 `f74d8bb1fcbad44e` · 65 edges from Q1, Q2, Q3, both providers

**Finding (Q3, claude).** The disqualification is conditional and nothing
establishes when independence is required. Since the issuing principal populates
its own `independence requirements` field, it can truthfully record that no
independence requirement applies. The clause "disqualifies self-issuance from
independence, but does not itself impose independence."

**Finding (Q2, gpt).** A `self_issued: true` mark does not itself require any
consumer to reject the authorization where independence is required.

**Finding (Q2, gpt).** "At the root of any chain, the accountable party
necessarily authorizes work it is also responsible for" is false as stated. The
definitions allow but do not require one party to hold both roles; a principal can
authorize an invocation performed by another executor. Responsibility is not
performance.

**[RESOLVED] The clause is inert today.** ABS-0004 §4.16 defines
AuthorizationPolicy — where independence requirements would be specified — and
defers it. No reviewer held §4.16. Until it exists, nothing imposes independence,
so nothing is disqualified.

**[ANALYSIS] A cross-question self-correction.** Q1 argued for reading (b) on
scope breadth *by contrast* with this clause, crediting it with "a real downstream
consequence, not a label". Q1 also flagged its own weak point: that without
knowing when independence is required it could not assess how much work the clause
does. Q3, a separate invocation with no sight of Q1, answered exactly that, and
the answer destroys the contrast. v7 does not have one label and one control. It
has two labels.

### 2.4 The `[OPEN]` paragraph

`ABS-0004:v7:S3#open:whether-standing-authority-require`
sha256 `ede8eee7a4da97b3` · 45 edges from Q1, Q2, both providers, 11 recommendations

**Finding (Q2, both).** "It records that no internal control can close it"
converts the demonstrated failure of one rule into a universal impossibility claim.
COMP-0037 showed v6's control was defeated; it did not show that no internal
control could be. Claude notes that this is the same move the round's own
instructions told reviewers not to accept from the plan.

**Recommendation (Q2, claude).** State that the one control tried was defeated,
that v7 knows of no internal control surviving that path, and that whether some
other could remains unresolved — a stated position consistent with P7, not a
result demonstrated by COMP-0037.

**Recommendation (Q1, gpt).** Specify the external-evidence test the paragraph
gestures at: the external source or accountable process, who may assess it, what
counts as sufficient, and what follows when it is absent, contested, or narrower
than the declaration.

### 2.5 Subordinate-authorization inheritance

`ABS-0004:v7:S3#def:subordinate-authorization-inherita`
sha256 `0796e537fbb1cabc` · 19 edges from Q1, Q2, Q3, Q4 — the widest question
span in the round

Load-bearing for 2.1 (it concedes undeclared execution occurs) and for the refusal
enumeration in 3.1 (reason 9 reaches only *declared* subordinates).

### 2.6 Attack surviving Section 3 as written

**Finding (Q3, both).** A party declares itself an AccountablePrincipal with
universal `authority_scope`, self-issues an authorization to itself as executor,
marks it `self_issued: true`, and faces no independence check because none was
declared applicable. Every sentence of Section 3 is satisfied. Neither reviewer
was forcing the attack; both were invited to report if the marking blocked it.

**Finding (Q3, claude), hedged as less certain.** Subordinate execution classes
have no breadth-legibility requirement analogous to `authority_scope`, so a parent
authorization may declare very broad subordinate classes without triggering any
visibility obligation.

**[ANALYSIS] Confirmed across the whole document.** "Legible as wide" occurs
exactly once in ABS-0004, for `authority_scope`. Nothing analogous constrains
subordinate execution classes. The reviewer could not confirm this from its
excerpt; it holds for the full text.

---

## 3. PLAN-20260723-0002

### 3.1 The refusal enumeration

`PLAN-20260723-0002#scope[4]` sha256 `56863a9be4cf807f`
85 edges from Q4, Q6, Q8, both providers, 13 recommendations — the largest cluster

**Finding (Q4, both).** The ten reasons are incomplete, and both witnesses found
the same gap precisely: reason 9 reaches a subordinate that *is* represented and
falls outside its parent's declared classes. It does not reach one never disclosed
as an Invocation at all, which §3 says is "not an implicitly authorized act" — a
categorically different failure.

**Finding (Q4, gpt).** There is no refusal reason for "no authorization covers
this invocation". "Authorized executor does not match" presupposes one exists.

**Finding (Q4, both).** The plan never states whether §4.7's disclosure
constraints are inside or outside what `authorize()` checks.

**[RESOLVED] The disposition is exclusion, and gpt's alternative is not
implementable.** gpt recommended `authorize()` check all three §4.7 constraints
from stored records. Each fails for a specific reason:

- `OutboundInteractionLog` is listed in ABS-0004 §11, "Defined but Deferred". No
  such records exist, so the check has no data source.
- Tool-configuration disclosure would rest on `EffectiveInputManifest`, which
  exists but whose every record carries
  `completeness_attestation: "partial_declared_channels_only"`. A manifest that
  attests its own partiality cannot ground a refusal for *undeclared*
  configuration.
- Undisclosed subordinate execution requires detecting an absence. No stored
  record can supply it.

Claude's recommendation — exclude them and say so — is correct, and it named §11
as the evidence that would settle the question before seeing it.

**Recommendation.** At least thirteen reasons; §4.7 explicitly excluded and stated
as excluded; "governed" narrowed in the documentation to "covered by an
authorization record".

### 3.2 The `check_depth` claim

`PLAN-20260723-0002#scope[12]` sha256 `dcfcbd2c0d836a1a`
72 edges from Q5, Q6, Q8, both providers

**Finding (Q5, both).** A field is data, not a control. Both witnesses
independently constructed the same two-hop case: A produces X; B produces Y from
X; A adjudicates Y; the one-hop check sees only B and permits.

**Finding (Q5, claude).** `check_depth` is a constant attached to every outcome.
It cannot distinguish a two-hop-clean artifact from a two-hop-colliding one; both
return permitted with the identical value. The field discloses the shape of the
gap, not the presence of a gap instance — so "machine-visible, not only
documented" is a second overclaim inside the same scope item.

**[ANALYSIS] This is admission-blocking on the plan's own terms.**
`constraints[1]` states that field names and semantics follow ABS-0004 v7 exactly.
P6 holds that a record whose label implies confirmation where none exists is a
defect regardless of its contents, because consumers read the label, not the
caveat. `scope[12]` asserts a consumer *cannot* misread a permitted result. The
plan contradicts an adopted principle of the ontology it claims to follow.

**Recommendation (all six, both providers, converged).** Replace with wording
that the outcome records only that a direct check was performed, that a permitted
result establishes no general independence finding, and that no mechanism in this
slice prevents misuse.

### 3.3 Success criteria

**Finding (Q7, both).** Criteria 4, 9 and 10 are not mechanically checkable as
written.

**Finding (Q7, claude).** Criterion 5 is checkable only as a formula-consistency
test, not a classification-correctness test: ABS-0004 §8 leaves the detailed
classification function `[OPEN]`, so no rule derives which modifier levels apply
to a given invocation. Fixtures can assert that the effective class equals the
maximum of hand-assigned inputs; they cannot assert the inputs were right.

### 3.4 C6 evidence

**Finding (Q6, both).** `rationale[0]` — "Slice C is what lets that row cite
something" — holds only in the narrow sense that Slice C supplies the role records
the enforcement matrix names as C6's activation dependency. It does not supply an
enforcement artifact. The one-hop check is identity-based, not axis-based, and
does not touch C6's exercise restriction.

**Recommendation.** Weaken to the dependency sense both witnesses endorsed.

### 3.5 Slice D constraint

**Finding (Q8, claude).** Several decisions are migration-required rather than
validation-code-only: the DecisionRecord family design, RoleDefinition axes,
AccountablePrincipal shape, consequence classification if the table changes, and
`self_issued` computed on exact-identifier equality — persisted `self_issued:
false` records become wrong if broader sameness detection is ever adopted.

**Finding (Q8, claude).** No schema-versioning or migration policy exists for
self-model records, so "migration-required" has no defined cost.

---

## 4. What the round did not settle

- **Whether v7's visibility-only approach is preferable to an operational
  scope-bound regime.** Both witnesses said their evidence was insufficient. The
  reframing in 2.2 changes the question rather than answering it.
- **Whether any internal control could close the regress.** Both witnesses
  rejected v7's universal claim; neither asserted the contrary.
- **Anything requiring §4.7, §11, P1, P6, COMP-0037 or v6 text.** These were
  cited by the evidence units attached and not themselves attached — a scoping
  defect of the round, recorded in `comp0039/MANIFEST.json`. Both witnesses named
  the gaps rather than guessing, which is the scope-validation instruction
  working.

## 5. Unaddressed defects noted during the round

- **InvocationRecord cannot represent zero-content-as-success.**
  `INVOCATION_STATUSES` admits only `success` and `failure`; there is no
  `stop_reason` or output-token field; `execution_profile` records supplied rather
  than effective configuration. Diagnosed against COMP-0038, addendum committed
  at `9a097b1`; no gap record or CAP-0015 limits amendment has been written.
- **Witness output-budget asymmetry.** `output_token_limit` is 16000 for
  `claude-sonnet-5` and `null` for `gpt-5.6-terra`. AI-Lab caps one witness and
  not the other, and the records cannot establish that the two had comparable room
  to answer. Present in COMP-0037 and every round since; disclosed in none.
- **Claim-graph limitations**, recorded in `comp0039/CLAIM_GRAPH.md`. Most
  relevant here: a claim node cannot carry that it was later refuted, so
  `CLAIM-7f96b4ee3de269fc` still asserts the premise corrected in 2.2.

## 6. Standing

Neither ABS-0004 v7 nor PLAN-20260723-0002 is admitted. The round produced
specific, converged, evidence-backed grounds for revising both before admission,
and the revisions are enumerated above. This record does not adjudicate; it
assembles what the round found for the accountable principal to adjudicate.
