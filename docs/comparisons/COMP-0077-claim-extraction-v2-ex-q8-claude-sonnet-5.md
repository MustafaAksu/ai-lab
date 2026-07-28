# COMP-0077: Provider Comparison — Claim extraction v2 EX-Q8-claude-sonnet-5

## Metadata

- comparison_id: `COMP-0077`
- title: `Claim extraction v2 EX-Q8-claude-sonnet-5`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-bf1c560be6590278.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0077", "target_id": "INV-bf1c560be6590278"}, {"authoritative": false, "evidence": "docs/invocations/INV-4fd76fc6fc496882.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0077", "target_id": "INV-4fd76fc6fc496882"}]`
- created_at: `2026-07-28T20:17:33.319923+00:00`
- command: `scripts/compare_providers.py --title Claim extraction v2 EX-Q8-claude-sonnet-5 You are extracting claims from a review answer so they can be recorded as separate, addressable records. You are not evaluating the answer and not deciding whether any claim is correct.

WHAT COUNTS AS A CLAIM. A claim is an assertion a reader could accept, reject, or act on. It is defined by function, not by sentence boundaries. Do NOT extract:
  - restatements of the material the answer was given;
  - intermediate steps of an argument whose conclusion you are already extracting;
  - transitions, framing, or summaries of what the answer is about.
Extract the conclusions the answer asserts, not the reasoning that reaches them.

HOW MANY. Most answers contain between 5 and 15 such claims. Extract at most 20. If more than 20 meet the definition, extract the 20 the answer's conclusions depend on most and report the number you left out in "claims_omitted". Do not pad toward 20 and do not split a claim to reach it.

Rules:

1. One assertion per claim.
2. Extract only what the answer says. Do not add, infer, complete, or improve.
3. PRESERVE HEDGES EXACTLY. If the answer says "may", "appears to", "I cannot determine", "only in the narrow sense that", or "less certain", the claim text must carry that same force. Never state a hedged claim flatly. A claim recorded more confidently than it was made is the most damaging error you can make here.
4. Give each claim a type, one of:
   - "finding": an assertion about the reviewed material
   - "recommendation": something the answer says should be done or changed
   - "evidence_gap": material the answer says it needed and did not have
   - "limitation": a stated bound on the answer's own reliability or reach
5. For each claim give "about": the specific thing it concerns, as precisely as the answer allows - for example "ABS-0004 v7 Section 3 visibility constraint", "PLAN-20260723-0002 scope[12]", "refusal reason 9". Use "unspecified" if the answer does not say.
6. QUOTE RULES, applied strictly. "quote" must be ONE contiguous span copied character-for-character from the answer, under 30 words.
   - No ellipsis. Never use "..." to bridge omitted material.
   - Never join text across bullets, list items, paragraphs, or headings.
   - Never add or remove quotation marks, brackets, or punctuation at either end.
   If no single contiguous span states the claim, choose a shorter span that supports it, or extract a different claim. A quote that reads as verbatim while having been shortened or rejoined is worse than no quote, because it cannot be checked by eye.

Output STRICT JSON and nothing else. No preamble, no commentary, no markdown fences. Exactly this shape:

{"claims":[{"text":"...","type":"finding","about":"...","quote":"..."}],
 "claims_omitted":0}

If the answer makes no extractable claim, output {"claims":[],"claims_omitted":0}.

=== QUESTION THAT WAS ASKED (Q8) ===
Which decisions in this slice constrain later evidence admission and lineage work, and which of them would be expensive to reverse once records exist?

Distinguish decisions that only require changing validation code from decisions that would require migrating existing records, and say which category each falls in.

=== ANSWER TO EXTRACT FROM ===
## Decisions in this slice that constrain later evidence-admission / lineage work

**1. The DecisionRecord record-family shape (ABS-0004 v7 §4.13), instantiated now by InvocationAuthorization.**

Section 4.13 marks the family design as unresolved:

> `[OPEN]` Whether existing warrant/admission records are extended to fulfill this or a new record family is created, and whether kinds are subtypes or one record family.

The plan nonetheless persists `InvocationAuthorization` as a concrete `DecisionRecord` kind now (scope item: *"InvocationAuthorization as a DecisionRecord kind... alongside its kind-specific fields"*), and the plan itself notes the reconciliation gap was still open at review time:

> "COMP-0037 found the plan's field list and the ontology's inherited list unreconciled."

**Category: migration-required.** Once InvocationAuthorization records exist under one field layout, and `EvidenceAdmissionDecision` (Slice D) is later built under whichever family design the `[OPEN]` item resolves to, existing authorization records may need structural migration to conform — this is not a validator change, it is a change to persisted record shape.

**2. RoleDefinition's three axes and `required_verified_properties` (§4.9).**

> "`required_verified_properties` (the properties that must be established by admissible verification before this role's outputs enter governed evidence...)"

This field is the direct hook `EvidenceAdmissionDecision` (§4.13) uses: *"an enumeration of verified properties against the receiving role's `required_verified_properties`."* The plan seeds real role records now (drafting actuator, comparison advisor, adjudicating principal, deterministic verifier) with this field populated, and the plan's own risk section says as much:

> "Role and consequence vocabularies decided here are load-bearing for Slice D's admission rules, and a coarse role taxonomy would propagate."

**Category: migration-required.** Seed role records are persisted artifacts (`docs/roles/`). If the vocabulary or `required_verified_properties` semantics needs revision once Slice D's admission logic is built against it, those stored role records — and anything that already cites them as authority for a governed classification — need migration, not just a validator update.

**3. AccountablePrincipal shape (§4.13), seeded now.**

The plan creates a real seed record ("the operator's AccountablePrincipal record"). `EvidenceAdmissionDecision` and future admission work will reference `AccountablePrincipal` as accountable approver. 

**Category: migration-required.** Changing `principal_id`/`principal_kind`/`authority_scope`/`delegation_reference` semantics later means migrating the persisted seed record and anything chaining to it.

**4. `self_issued` computed by exact-identifier party sameness only.**

> "Party sameness is decided on exact identifier equality only, and the documentation states that broader sameness is not detected."

This flag is stored per authorization record at issue time, not recomputed on demand. Independence findings for evidence admission (§4.13: *"lineage and independence findings relied on"*) will eventually need a broader sameness notion for lineage work.

**Category: migration-required.** If broader-sameness detection is adopted later, previously persisted `self_issued=false` records that are actually same-party under the broader rule are now wrong and must be recomputed/migrated — this is a record-content problem, not a code-only fix, because the flag was written once and consumed downstream (independence checks) as a fact.

**5. The one-hop `check_depth` bound on the self-adjudication check.**

> "the self-adjudication outcome carries an explicit `check_depth` field naming it a direct check, so a consumer cannot read a permitted result as a general independence finding."

**Category: validation-code-only (with a caveat).** As long as Slice D's multi-hop check is additive — new records/new `check_depth` values sitting alongside existing one-hop results — existing records remain valid instances and need no migration. This only becomes migration-required if the eventual multi-hop design requires reinterpreting or restructuring the existing `check_depth` enum rather than extending it; the evidence set doesn't show that design, so I can't rule it out.

**6. Refusal-reason enumeration and predicate registry entries.**

Both are described as enumerable/extensible ("Ten reasons, each with a fixture," "no predicate outside the registered Slice A, B, and C lists" — extended by later slices). Adding refusal reasons or Slice D predicates is additive to an enum/registry.

**Category: validation-code-only.** Nothing about existing records is invalidated by adding new reasons or predicates; only validators/consumers need updating.

**7. Consequence classification (default by target type, modifiers only raise).**

Effective consequence is computed and stored per authorization at issue time (a decision fact), not derived live.

**Category: migration-required if the default/modifier table changes**, since past records embed the old computation as a governance fact; **validation-code-only if only new modifiers are added going forward** without touching already-issued records' stored effective class.

---

## What would be needed but is not in this evidence set

- **ABS-0004 v7 Section 8** (consequence classification detail) — needed to judge how tightly the stored effective-consequence value is coupled to the classification table, i.e., whether a table change is migration-required or re-derivable.
- **ABS-0004 v7 Section 11** (OutboundInteractionLog) — referenced as the enforcement object for external-interaction disclosure; needed to judge whether Slice D lineage work depends on that log's shape and whether it's already schema-frozen.
- **The full text of the `[OPEN]` DecisionRecord resolution**, and **COMP-0037's record itself** — the plan quotes findings from COMP-0037 but the review artifact isn't in evidence; I'd want it to confirm exactly what field reconciliation was left unresolved before implementation, since that bears directly on migration cost for InvocationAuthorization records.
- **Any schema-versioning/migration policy document for AI-Lab's self_model records** — none is in evidence. Without it I can't confirm whether "migration" here means a one-time backfill script or a harder irreversible-record problem; I've assumed the latter is the relevant risk given the plan's own framing of role/consequence vocabulary as "load-bearing."

---

## On the disclosure

The plan frames the v6→v7 break narrowly, as a self-authorization/chain-termination problem solved by declaring root authority extra-systemic. I'm not treating that as the only break relevant to this slice's lineage exposure: Section 4.7 records a second, separate open construction — the `ExecutorIdentity` superclass question reopened by COMP-0032 ("a superclass with identity-equivalence semantics defined per subtype would make constraints such as C3 properly polymorphic across executor kinds") — which is unresolved and bears directly on lineage/independence comparison across `ModelIdentity`/`ToolIdentity`/`HumanIdentity`. Whether resolving it later is validation-code-only or migration-required depends on whether identity-equivalence semantics can be added as a code-level interface over existing subtype records or requires new persisted fields on them; that determination isn't answerable from the evidence here and is a second, independent risk from the one the plan foregrounds.

--- END OF ANSWER ---

Output the JSON now.`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5.6-terra`
- Claude: `claude-sonnet-5`

## Prompt

You are extracting claims from a review answer so they can be recorded as separate, addressable records. You are not evaluating the answer and not deciding whether any claim is correct.

WHAT COUNTS AS A CLAIM. A claim is an assertion a reader could accept, reject, or act on. It is defined by function, not by sentence boundaries. Do NOT extract:
  - restatements of the material the answer was given;
  - intermediate steps of an argument whose conclusion you are already extracting;
  - transitions, framing, or summaries of what the answer is about.
Extract the conclusions the answer asserts, not the reasoning that reaches them.

HOW MANY. Most answers contain between 5 and 15 such claims. Extract at most 20. If more than 20 meet the definition, extract the 20 the answer's conclusions depend on most and report the number you left out in "claims_omitted". Do not pad toward 20 and do not split a claim to reach it.

Rules:

1. One assertion per claim.
2. Extract only what the answer says. Do not add, infer, complete, or improve.
3. PRESERVE HEDGES EXACTLY. If the answer says "may", "appears to", "I cannot determine", "only in the narrow sense that", or "less certain", the claim text must carry that same force. Never state a hedged claim flatly. A claim recorded more confidently than it was made is the most damaging error you can make here.
4. Give each claim a type, one of:
   - "finding": an assertion about the reviewed material
   - "recommendation": something the answer says should be done or changed
   - "evidence_gap": material the answer says it needed and did not have
   - "limitation": a stated bound on the answer's own reliability or reach
5. For each claim give "about": the specific thing it concerns, as precisely as the answer allows - for example "ABS-0004 v7 Section 3 visibility constraint", "PLAN-20260723-0002 scope[12]", "refusal reason 9". Use "unspecified" if the answer does not say.
6. QUOTE RULES, applied strictly. "quote" must be ONE contiguous span copied character-for-character from the answer, under 30 words.
   - No ellipsis. Never use "..." to bridge omitted material.
   - Never join text across bullets, list items, paragraphs, or headings.
   - Never add or remove quotation marks, brackets, or punctuation at either end.
   If no single contiguous span states the claim, choose a shorter span that supports it, or extract a different claim. A quote that reads as verbatim while having been shortened or rejoined is worse than no quote, because it cannot be checked by eye.

Output STRICT JSON and nothing else. No preamble, no commentary, no markdown fences. Exactly this shape:

{"claims":[{"text":"...","type":"finding","about":"...","quote":"..."}],
 "claims_omitted":0}

If the answer makes no extractable claim, output {"claims":[],"claims_omitted":0}.

=== QUESTION THAT WAS ASKED (Q8) ===
Which decisions in this slice constrain later evidence admission and lineage work, and which of them would be expensive to reverse once records exist?

Distinguish decisions that only require changing validation code from decisions that would require migrating existing records, and say which category each falls in.

=== ANSWER TO EXTRACT FROM ===
## Decisions in this slice that constrain later evidence-admission / lineage work

**1. The DecisionRecord record-family shape (ABS-0004 v7 §4.13), instantiated now by InvocationAuthorization.**

Section 4.13 marks the family design as unresolved:

> `[OPEN]` Whether existing warrant/admission records are extended to fulfill this or a new record family is created, and whether kinds are subtypes or one record family.

The plan nonetheless persists `InvocationAuthorization` as a concrete `DecisionRecord` kind now (scope item: *"InvocationAuthorization as a DecisionRecord kind... alongside its kind-specific fields"*), and the plan itself notes the reconciliation gap was still open at review time:

> "COMP-0037 found the plan's field list and the ontology's inherited list unreconciled."

**Category: migration-required.** Once InvocationAuthorization records exist under one field layout, and `EvidenceAdmissionDecision` (Slice D) is later built under whichever family design the `[OPEN]` item resolves to, existing authorization records may need structural migration to conform — this is not a validator change, it is a change to persisted record shape.

**2. RoleDefinition's three axes and `required_verified_properties` (§4.9).**

> "`required_verified_properties` (the properties that must be established by admissible verification before this role's outputs enter governed evidence...)"

This field is the direct hook `EvidenceAdmissionDecision` (§4.13) uses: *"an enumeration of verified properties against the receiving role's `required_verified_properties`."* The plan seeds real role records now (drafting actuator, comparison advisor, adjudicating principal, deterministic verifier) with this field populated, and the plan's own risk section says as much:

> "Role and consequence vocabularies decided here are load-bearing for Slice D's admission rules, and a coarse role taxonomy would propagate."

**Category: migration-required.** Seed role records are persisted artifacts (`docs/roles/`). If the vocabulary or `required_verified_properties` semantics needs revision once Slice D's admission logic is built against it, those stored role records — and anything that already cites them as authority for a governed classification — need migration, not just a validator update.

**3. AccountablePrincipal shape (§4.13), seeded now.**

The plan creates a real seed record ("the operator's AccountablePrincipal record"). `EvidenceAdmissionDecision` and future admission work will reference `AccountablePrincipal` as accountable approver. 

**Category: migration-required.** Changing `principal_id`/`principal_kind`/`authority_scope`/`delegation_reference` semantics later means migrating the persisted seed record and anything chaining to it.

**4. `self_issued` computed by exact-identifier party sameness only.**

> "Party sameness is decided on exact identifier equality only, and the documentation states that broader sameness is not detected."

This flag is stored per authorization record at issue time, not recomputed on demand. Independence findings for evidence admission (§4.13: *"lineage and independence findings relied on"*) will eventually need a broader sameness notion for lineage work.

**Category: migration-required.** If broader-sameness detection is adopted later, previously persisted `self_issued=false` records that are actually same-party under the broader rule are now wrong and must be recomputed/migrated — this is a record-content problem, not a code-only fix, because the flag was written once and consumed downstream (independence checks) as a fact.

**5. The one-hop `check_depth` bound on the self-adjudication check.**

> "the self-adjudication outcome carries an explicit `check_depth` field naming it a direct check, so a consumer cannot read a permitted result as a general independence finding."

**Category: validation-code-only (with a caveat).** As long as Slice D's multi-hop check is additive — new records/new `check_depth` values sitting alongside existing one-hop results — existing records remain valid instances and need no migration. This only becomes migration-required if the eventual multi-hop design requires reinterpreting or restructuring the existing `check_depth` enum rather than extending it; the evidence set doesn't show that design, so I can't rule it out.

**6. Refusal-reason enumeration and predicate registry entries.**

Both are described as enumerable/extensible ("Ten reasons, each with a fixture," "no predicate outside the registered Slice A, B, and C lists" — extended by later slices). Adding refusal reasons or Slice D predicates is additive to an enum/registry.

**Category: validation-code-only.** Nothing about existing records is invalidated by adding new reasons or predicates; only validators/consumers need updating.

**7. Consequence classification (default by target type, modifiers only raise).**

Effective consequence is computed and stored per authorization at issue time (a decision fact), not derived live.

**Category: migration-required if the default/modifier table changes**, since past records embed the old computation as a governance fact; **validation-code-only if only new modifiers are added going forward** without touching already-issued records' stored effective class.

---

## What would be needed but is not in this evidence set

- **ABS-0004 v7 Section 8** (consequence classification detail) — needed to judge how tightly the stored effective-consequence value is coupled to the classification table, i.e., whether a table change is migration-required or re-derivable.
- **ABS-0004 v7 Section 11** (OutboundInteractionLog) — referenced as the enforcement object for external-interaction disclosure; needed to judge whether Slice D lineage work depends on that log's shape and whether it's already schema-frozen.
- **The full text of the `[OPEN]` DecisionRecord resolution**, and **COMP-0037's record itself** — the plan quotes findings from COMP-0037 but the review artifact isn't in evidence; I'd want it to confirm exactly what field reconciliation was left unresolved before implementation, since that bears directly on migration cost for InvocationAuthorization records.
- **Any schema-versioning/migration policy document for AI-Lab's self_model records** — none is in evidence. Without it I can't confirm whether "migration" here means a one-time backfill script or a harder irreversible-record problem; I've assumed the latter is the relevant risk given the plan's own framing of role/consequence vocabulary as "load-bearing."

---

## On the disclosure

The plan frames the v6→v7 break narrowly, as a self-authorization/chain-termination problem solved by declaring root authority extra-systemic. I'm not treating that as the only break relevant to this slice's lineage exposure: Section 4.7 records a second, separate open construction — the `ExecutorIdentity` superclass question reopened by COMP-0032 ("a superclass with identity-equivalence semantics defined per subtype would make constraints such as C3 properly polymorphic across executor kinds") — which is unresolved and bears directly on lineage/independence comparison across `ModelIdentity`/`ToolIdentity`/`HumanIdentity`. Whether resolving it later is validation-code-only or migration-required depends on whether identity-equivalence semantics can be added as a code-level interface over existing subtype records or requires new persisted fields on them; that determination isn't answerable from the evidence here and is a second, independent risk from the one the plan foregrounds.

--- END OF ANSWER ---

Output the JSON now.

## OpenAI Response

- model: `gpt-5.6-terra`

```
{"claims":[{"text":"Persisting InvocationAuthorization under the current DecisionRecord field layout is migration-required if the later DecisionRecord family resolution uses a different structure.","type":"finding","about":"InvocationAuthorization DecisionRecord family shape (ABS-0004 v7 §4.13)","quote":"existing authorization records may need structural migration to conform — this is not a validator change"},{"text":"Revising RoleDefinition vocabulary or required_verified_properties semantics after Slice D admission logic is built would require migration of stored role records and governed classifications citing them.","type":"finding","about":"RoleDefinition three axes and required_verified_properties (ABS-0004 v7 §4.9)","quote":"those stored role records — and anything that already cites them as authority for a governed classification — need migration"},{"text":"Changing AccountablePrincipal field semantics later would require migrating the persisted seed record and records chained to it.","type":"finding","about":"AccountablePrincipal shape (ABS-0004 v7 §4.13)","quote":"Changing `principal_id`/`principal_kind`/`authority_scope`/`delegation_reference` semantics later means migrating the persisted seed record and anything chaining to it."},{"text":"Party sameness for self_issued is decided solely by exact identifier equality, and broader sameness is not detected.","type":"finding","about":"InvocationAuthorization self_issued party-sameness rule","quote":"Party sameness is decided on exact identifier equality only, and the documentation states that broader sameness is not detected."},{"text":"Adopting broader-sameness detection later would require recomputing or migrating previously persisted self_issued=false records that are same-party under the broader rule.","type":"finding","about":"InvocationAuthorization self_issued stored flag","quote":"previously persisted `self_issued=false` records that are actually same-party under the broader rule are now wrong and must be recomputed/migrated"},{"text":"The one-hop check_depth bound is validation-code-only so long as Slice D multi-hop checking is additive.","type":"finding","about":"self-adjudication check_depth bound","quote":"As long as Slice D's multi-hop check is additive — new records/new `check_depth` values sitting alongside existing one-hop results — existing records remain valid instances and need no migration."},{"text":"The one-hop check_depth bound becomes migration-required if the eventual multi-hop design reinterprets or restructures the existing check_depth enum rather than extending it.","type":"finding","about":"self-adjudication check_depth enum","quote":"This only becomes migration-required if the eventual multi-hop design requires reinterpreting or restructuring the existing `check_depth` enum rather than extending it;"},{"text":"The evidence set does not establish whether the eventual multi-hop design will require reinterpretation or restructuring of the existing check_depth enum.","type":"limitation","about":"future multi-hop self-adjudication check_depth design","quote":"the evidence set doesn't show that design, so I can't rule it out."},{"text":"Adding refusal reasons or Slice D predicates is validation-code-only because existing records are not invalidated.","type":"finding","about":"refusal-reason enumeration and predicate registry entries","quote":"Nothing about existing records is invalidated by adding new reasons or predicates; only validators/consumers need updating."},{"text":"Changing the consequence default/modifier table is migration-required because past records store the prior effective-consequence computation as a governance fact.","type":"finding","about":"InvocationAuthorization consequence classification","quote":"migration-required if the default/modifier table changes"},{"text":"Adding new consequence modifiers only for future records is validation-code-only if already-issued records' stored effective class is unchanged.","type":"finding","about":"InvocationAuthorization consequence classification modifiers","quote":"validation-code-only if only new modifiers are added going forward"},{"text":"ABS-0004 v7 Section 8 is needed to determine whether stored effective-consequence values are tightly coupled to the classification table.","type":"evidence_gap","about":"ABS-0004 v7 Section 8 consequence classification detail","quote":"needed to judge how tightly the stored effective-consequence value is coupled to the classification table"},{"text":"ABS-0004 v7 Section 11 is needed to determine whether Slice D lineage work depends on OutboundInteractionLog's shape and whether it is schema-frozen.","type":"evidence_gap","about":"ABS-0004 v7 Section 11 OutboundInteractionLog","quote":"needed to judge whether Slice D lineage work depends on that log's shape and whether it's already schema-frozen."},{"text":"The full DecisionRecord resolution and COMP-0037 record are needed to confirm what field reconciliation remained unresolved before implementation.","type":"evidence_gap","about":"[OPEN] DecisionRecord resolution and COMP-0037","quote":"I'd want it to confirm exactly what field reconciliation was left unresolved before implementation"},{"text":"No schema-versioning or migration policy document for AI-Lab self_model records is in evidence.","type":"evidence_gap","about":"AI-Lab self_model schema-versioning and migration policy","quote":"none is in evidence."},{"text":"Without a schema-versioning or migration policy, the answer cannot confirm whether migration means a one-time backfill script or a harder irreversible-record problem.","type":"limitation","about":"meaning and reversibility of self_model record migration","quote":"Without it I can't confirm whether \"migration\" here means a one-time backfill script or a harder irreversible-record problem;"},{"text":"The ExecutorIdentity superclass question is unresolved and directly affects lineage and independence comparison across ModelIdentity, ToolIdentity, and HumanIdentity.","type":"finding","about":"ExecutorIdentity superclass question (ABS-0004 v7 §4.7; COMP-0032)","quote":"which is unresolved and bears directly on lineage/independence comparison across `ModelIdentity`/`ToolIdentity`/`HumanIdentity`."},{"text":"The evidence does not determine whether resolving ExecutorIdentity identity-equivalence semantics would be validation-code-only or migration-required.","type":"limitation","about":"ExecutorIdentity identity-equivalence semantics resolution","quote":"that determination isn't answerable from the evidence here"}],"claims_omitted":0}
```

## Claude Response

- model: `claude-sonnet-5`

```
{"claims":[
{"text":"The DecisionRecord record-family shape (ABS-0004 v7 §4.13) is a decision that constrains later evidence-admission/lineage work, and it is currently instantiated by InvocationAuthorization even though the family design is marked open.","type":"finding","about":"ABS-0004 v7 §4.13 DecisionRecord family shape","quote":"Whether existing warrant/admission records are extended to fulfill this or a new record family is created, and whether kinds are subtypes or one record family."},
{"text":"Once InvocationAuthorization records exist under one field layout and EvidenceAdmissionDecision is later built under whichever family design resolves the open item, existing authorization records may need structural migration rather than just a validator change.","type":"finding","about":"InvocationAuthorization / DecisionRecord family reconciliation","quote":"existing authorization records may need structural migration to conform — this is not a validator change, it is a change to persisted record shape"},
{"text":"RoleDefinition's required_verified_properties field (§4.9) is the direct hook used by EvidenceAdmissionDecision, and seed role records populate this field now, making the role vocabulary load-bearing for later admission logic.","type":"finding","about":"ABS-0004 v7 §4.9 RoleDefinition required_verified_properties","quote":"Role and consequence vocabularies decided here are load-bearing for Slice D's admission rules, and a coarse role taxonomy would propagate."},
{"text":"Seed role records are persisted artifacts, so if the role vocabulary or required_verified_properties semantics needs revision once Slice D's admission logic is built, those stored records and anything citing them need migration, not just a validator update.","type":"finding","about":"seed RoleDefinition records in docs/roles/","quote":"those stored role records — and anything that already cites them as authority for a governed classification — need migration, not just a validator update"},
{"text":"AccountablePrincipal shape (§4.13) is seeded now with a real operator record, and changing principal_id/principal_kind/authority_scope/delegation_reference semantics later would require migrating the persisted seed record and anything chaining to it.","type":"finding","about":"ABS-0004 v7 §4.13 AccountablePrincipal shape","quote":"Changing `principal_id`/`principal_kind`/`authority_scope`/`delegation_reference` semantics later means migrating the persisted seed record and anything chaining to it."},
{"text":"self_issued is computed by exact-identifier party sameness only, with broader sameness not detected, and this flag is stored per authorization record at issue time rather than recomputed on demand.","type":"finding","about":"self_issued exact-identifier party sameness computation","quote":"Party sameness is decided on exact identifier equality only, and the documentation states that broader sameness is not detected."},
{"text":"If broader-sameness detection is adopted later, previously persisted self_issued=false records that are actually same-party under the broader rule would be wrong and would need to be recomputed or migrated, since the flag was written once and consumed downstream as fact.","type":"finding","about":"self_issued flag migration risk","quote":"previously persisted `self_issued=false` records that are actually same-party under the broader rule are now wrong and must be recomputed/migrated"},
{"text":"The self-adjudication outcome carries an explicit check_depth field naming it a direct check, so a consumer cannot read a permitted result as a general independence finding.","type":"finding","about":"self-adjudication check_depth field","quote":"the self-adjudication outcome carries an explicit `check_depth` field naming it a direct check, so a consumer cannot read a permitted result as a general independence finding"},
{"text":"As long as Slice D's multi-hop check is additive, existing one-hop check_depth records remain valid instances and need no migration; this only becomes migration-required if the eventual multi-hop design requires reinterpreting or restructuring the existing check_depth enum, and the evidence set doesn't show that design so it can't be ruled out.","type":"finding","about":"check_depth one-hop bound future extension","quote":"this only becomes migration-required if the eventual multi-hop design requires reinterpreting or restructuring the existing `check_depth` enum rather than extending it; the evidence set doesn't show that design, so I can't rule it out"},
{"text":"The refusal-reason enumeration and predicate registry entries are described as enumerable/extensible, so adding refusal reasons or Slice D predicates is additive to an enum/registry and does not invalidate existing records, only requiring validator/consumer updates.","type":"finding","about":"refusal-reason enumeration and predicate registry","quote":"Nothing about existing records is invalidated by adding new reasons or predicates; only validators/consumers need updating."},
{"text":"Effective consequence classification is computed and stored per authorization at issue time as a decision fact, not derived live.","type":"finding","about":"consequence classification storage","quote":"Effective consequence is computed and stored per authorization at issue time (a decision fact), not derived live."},
{"text":"Changing the default/modifier consequence classification table would be migration-required because past records embed the old computation as a governance fact, whereas adding only new modifiers going forward without touching already-issued records' stored class would be validation-code-only.","type":"finding","about":"consequence default/modifier table changes","quote":"migration-required if the default/modifier table changes**, since past records embed the old computation as a governance fact; **validation-code-only if only new modifiers are added going forward** without touching already-issued records' stored effective class"},
{"text":"ABS-0004 v7 Section 8 (consequence classification detail) is needed to judge how tightly the stored effective-consequence value is coupled to the classification table, i.e., whether a table change is migration-required or re-derivable.","type":"evidence_gap","about":"ABS-0004 v7 Section 8 consequence classification detail","quote":"needed to judge how tightly the stored effective-consequence value is coupled to the classification table, i.e., whether a table change is migration-required or re-derivable"},
{"text":"ABS-0004 v7 Section 11 (OutboundInteractionLog) is needed to judge whether Slice D lineage work depends on that log's shape and whether it is already schema-frozen.","type":"evidence_gap","about":"ABS-0004 v7 Section 11 OutboundInteractionLog","quote":"needed to judge whether Slice D lineage work depends on that log's shape and whether it's already schema-frozen"},
{"text":"The full text of the [OPEN] DecisionRecord resolution and COMP-0037's record itself are needed to confirm exactly what field reconciliation was left unresolved before implementation, since that bears directly on migration cost for InvocationAuthorization records.","type":"evidence_gap","about":"COMP-0037 record and [OPEN] DecisionRecord resolution text","quote":"I'd want it to confirm exactly what field reconciliation was left unresolved before implementation, since that bears directly on migration cost for InvocationAuthorization records"},
{"text":"No schema-versioning/migration policy document for AI-Lab's self_model records is in evidence, so it cannot be confirmed whether \"migration\" here means a one-time backfill script or a harder irreversible-record problem.","type":"evidence_gap","about":"schema-versioning/migration policy document","quote":"Without it I can't confirm whether \"migration\" here means a one-time backfill script or a harder irreversible-record problem"},
{"text":"The answer does not treat the v6→v7 self-authorization/chain-termination framing as the only break relevant to this slice's lineage exposure; Section 4.7's ExecutorIdentity superclass question, reopened by COMP-0032, is a second unresolved construction bearing directly on lineage/independence comparison across ModelIdentity/ToolIdentity/HumanIdentity.","type":"finding","about":"ABS-0004 v7 §4.7 ExecutorIdentity superclass question (COMP-0032)","quote":"a superclass with identity-equivalence semantics defined per subtype would make constraints such as C3 properly polymorphic across executor kinds"},
{"text":"Whether resolving the ExecutorIdentity superclass question later is validation-code-only or migration-required depends on whether identity-equivalence semantics can be added as a code-level interface over existing subtype records or requires new persisted fields, and this cannot be determined from the evidence here.","type":"limitation","about":"ExecutorIdentity superclass resolution migration category","quote":"that determination isn't answerable from the evidence here and is a second, independent risk from the one the plan foregrounds"}
],
"claims_omitted":0}
```
