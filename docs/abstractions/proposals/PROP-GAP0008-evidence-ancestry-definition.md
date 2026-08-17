# GAP-0008 first slice: proposed definition of artifact-level evidence ancestry

Proposed by the reviewing executor, verified by the packaging executor at
repository commit 6a1d4a0. **For operator adjudication. Not an ontology edit.**
ABS-0004 v9.1 is unchanged by this record.

## Why a definition rather than a capability

GAP-0008 records that `evidence ancestry` is the term C3 and C10 both turn on
and is defined nowhere in the admitted ontology, and that the fields which could
carry it are empty.

The packaging executor proposed that output digesting should precede the
definition, on the reasoning that a definition naming uncomputable edges repeats
the pattern v9.1 was corrected for. The reviewing executor rejected that and the
packaging executor withdrew it. The reason is that the absence of output digests
is a **capability blocker, not a definition blocker**: making
`source.output_digest == target.input_digest` the definition would make one
implementation mechanism into the ontology, and would force the implementation to
decide what counts as ancestry before the ontology has said what ancestry means.

A narrower definition covering only today's populated fields was also rejected,
because the richest available relation is the 105 same-prompt pairs, and those
are siblings rather than ancestors. Defining ancestry from them would define it
wrongly.

## The proposal

### Proposed GAP-0008 first-slice text

**`[DEF]` Artifact-level evidence ancestry.** For a governed artifact, claim-bearing artifact, or invocation output, *evidence ancestry* is the directed transitive closure of recorded provenance and effective-input relations representing **potential information dependence** from an earlier invocation or artifact to the target. An ancestor need not be the original source of a proposition; membership means only that information from, derived from, or capable of being carried from that ancestor is represented as able to influence the target.

**`[DEF]` Direct artifact-level evidence-ancestry edge.** A direct evidence-ancestry edge is a recorded directional provenance or effective-input linkage between a source invocation or artifact and a target whose information state it may influence. Representations of such a linkage include an explicit effective-input reference to an earlier invocation output or produced artifact; a content-addressed linkage between a recorded source output and content represented as an effective input of the target invocation; or an admitted directional derivation relation such as `copied_from`, `summarized_from`, `transformed_from`, or `claim_derived_from`, at the granularity supported by the retained records. `artifact produced_by invocation` identifies the producing invocation of an artifact; by itself it describes production rather than later consumption.

**`[DEF]` Spawned execution relation.** `spawned` represents execution composition between a parent invocation and subordinate execution. A separate retained effective-input, output-use, derivation, or equivalent directional-influence relation represents whether information from that subordinate execution could contribute to a later target.

**`[PROPOSED_CONSTRAINT]`** A `spawned` relation alone may not be treated as establishing an evidence-ancestry edge. A spawned invocation may enter a target's evidence ancestry only where a retained directional influence relation establishes potential information dependence on that subordinate execution.

**`[DEF]` Co-input and continuity relations.** Equality of `rendered_prompt_digest`, membership in the same comparison or protocol round, temporal proximity, common provider or executor class, and membership in the same session can represent common input, common cause, or execution continuity. None of those facts by itself represents direction of information flow from one invocation to another.

**`[PROPOSED_CONSTRAINT]`** Co-input, common-cause, and continuity relations may not be counted as evidence-ancestry edges unless an additional retained directional relation establishes potential information dependence. Where session continuity may carry relevant inherited state that is not reconstructibly represented, that lineage dimension remains `unresolved` under P5.

**`[DEF]` Artifact-level ancestry traversal result.** An ancestry traversal describes discovered potential-dependence paths together with the represented coverage of the edge classes on which the traversal depends. A negative path result describes that no path was found in the represented graph.

**`[PROPOSED_CONSTRAINT]`** A negative traversal result may not be treated as evidence of independence where an applicable input, output, derivation, subordinate-influence, or inherited-state edge is absent, incomplete, or not connectable at the retained granularity. In such a case the corresponding ancestry question remains `unresolved` under P5.

**`[LIMITATION]`** This definition does not provide claim-level lineage. An artifact can contain copied material, original observation, paraphrase, and new inference simultaneously; therefore an artifact-level path establishes potential dependence only. It neither proves that a particular claim was copied nor proves independence when no complete path is represented.

**`[LIMITATION]` Current capture cannot evaluate this definition for historical InvocationRecords.** At the measured repository state, `spawned`, `prior_tool_result_references`, and `context_manifest_reference` carry no ancestry links, while invocation outputs have no retained content digest that can be matched to later effective inputs. `rendered_prompt_digest` is populated, but equality of that digest establishes common rendered input rather than directional ancestry. The currently observed paired comparison records therefore identify sibling/co-input structure, not an evidence-ancestry graph.

**`[PROPOSAL]`** The first capability slice after this definition should capture **one honest directional edge class end to end** rather than implement general traversal over empty provenance. Candidate capture mechanisms include explicit prior-output references and content-addressed output-to-effective-input linkage. Selection of the first mechanism, its completeness boundary, and any output-digest schema change require a separately admitted implementation plan.

---

## Verification by the packaging executor

The reviewing executor noted it could not re-measure against `6a1d4a0`. Every
measurable claim above was re-derived at that commit:

| claim | measured |
| --- | --- |
| 210 InvocationRecords forming 105 same-prompt pairs | 210 records, 105 distinct digests, every group of size exactly 2 |
| `spawned` carries no ancestry links | populated on 0 of 210 |
| `prior_tool_result_references` empty | populated on 0 of 210 |
| `context_manifest_reference` empty | populated on 0 of 210 |
| `rendered_prompt_digest` populated | 210 of 210 |
| invocation outputs have no retained content digest | 28 outcome blocks, none carrying any digest or hash field |
| the derivation vocabulary exists | `copied_from`, `summarized_from`, `transformed_from`, `claim_derived_from`, `produced_by` all present |
| `evidence ancestry` is undefined | 4 occurrences, no `[DEF]` introduces it |

C5 was also checked, because the proposal relies on it to justify separating
co-input from lineage. C5 states that isolation from other witness outputs is
necessary but not sufficient, and that **common leading prompts** among other
factors defeat witness-path independence. The ontology therefore already treats
prompt common cause as distinct from lineage, which is the argument for putting
the sibling distinction in the definition rather than only in GAP-0008's
evidence.

## Sentence discipline

An earlier draft placed three prohibitions and one status-changing consequence
under `[DEF]`, which the A6 correction to v9.1 forbids: a `[DEF]` introduces a
term, record shape, relation or descriptive derivation and does not by itself
impose an obligation, prohibition, permission, admission condition or
status-changing consequence. The packaging executor found this; the reviewing
executor split each block so the description remains `[DEF]` and the rule becomes
`[PROPOSED_CONSTRAINT]`, and additionally changed "is evidenced only by" to "is a
recorded directional linkage" in the second definition, removing an admission
condition the packaging executor had not flagged.

The retagged text was checked mechanically: 5 `[DEF]` blocks with no normative
language, 3 `[PROPOSED_CONSTRAINT]` blocks each carrying it, 2 `[LIMITATION]`
blocks and 1 `[PROPOSAL]`, all descriptive.

## What this record does not do

- It does not amend ABS-0004. If admitted, the text becomes an amendment
  requiring its own admission event, and the constraints would enter as
  `proposed-v9` in the enforcement matrix with enforcement evidence `none`.
- It does not decide the output-digest schema, whether output hashing suffices or
  an explicit output object is needed, how a ContextManifest item identifies its
  producing invocation, traversal strategy, claim-level lineage, whether every
  `spawned` child contributes epistemically, a completeness threshold, or C3 and
  C10 enforcement. Each is capability or policy work after the definition.
- It does not make C3 evaluable. C3 remains unevaluable for any real claim: the
  equivalence half resolves under DECISION-20260814-0001 and blocks, and the
  ancestry half has a proposed definition with no populated edges.
- It has not been mechanically rebased against `6a1d4a0` by its author. The
  measurements are the packaging executor's; the text is the reviewing
  executor's.

## Recommended sequence, if admitted

Definition, then operator adjudication, then one directional capture slice with
its own plan and warrant, then falsification of that capture's completeness,
then traversal, then C3 and C10 use. Not output hash, then traversal, then
deciding afterwards what the graph meant.
