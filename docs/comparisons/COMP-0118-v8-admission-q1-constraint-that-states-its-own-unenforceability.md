# COMP-0118: Provider Comparison — v8 admission Q1 constraint-that-states-its-own-unenforceability

## Metadata

- comparison_id: `COMP-0118`
- title: `v8 admission Q1 constraint-that-states-its-own-unenforceability`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-37de94ed5d7e30ab.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0118", "target_id": "INV-37de94ed5d7e30ab"}, {"authoritative": false, "evidence": "docs/invocations/INV-cd416cb66007f994.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0118", "target_id": "INV-cd416cb66007f994"}]`
- created_at: `2026-07-31T13:36:43.922074+00:00`
- command: `scripts/compare_providers.py --title v8 admission Q1 constraint-that-states-its-own-unenforceability You are reviewing a proposed ontology amendment and the implementation plan that depends on it. This is ONE question of eight, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

Status: ABS-0004 v8 is proposed and not admitted. PLAN-20260723-0002 is proposed and not admitted. Neither has governance force.

Three disclosures, because withholding them would be dishonest rather than isolating:

1. v8 is a response to a prior review round (COMP-0039..0046) of v7. It withdrew several claims that round found unsupported. Do not treat a sentence as sound because it is a correction; a correction can overreach or under-reach like any other text.

2. Of the 118 claims that round produced whose citations the amendment broke, 58 were adjudicated as still applying against v8. v8 made the ontology more honest about what it does not do; it did not make the mechanisms work. Do not credit v8 with having closed what it only disclosed.

3. The executor that drafted v8 also proposed the dispositions deciding which claims still applied, subject to operator approval. Treat both as one party's work.

Quote only text that appears below. Do not rely on repository access.

IMPORTANT: the evidence set below was scoped deliberately, and the scoping may be wrong. If you need a section, constraint, or record that is not present, name it explicitly and say what you would have used it for. That report is wanted output, not a failure.

Do not certify or praise. No provider product recommendations.

=== QUESTION Q1 ===
v8 requires that a wide authority_scope "must be legible as wide", and then adds a second constraint stating that this requirement is enforced by nothing: no scope grammar, no interpretation rule, no validation step, no rendering requirement, no rule governing what a summary may say.

Is a constraint that states its own unenforceability a constraint, or a note about one? Say what it obliges that the requirement alone would not, and what a reader could do with it that they could not do with the requirement plus silence. If the honest form is to delete the requirement rather than annotate it, say so and give the replacement.

=== EVIDENCE ABS-0004:v8:S3#adopted_constraint:scope-breadth-is-visible-and-bread ===
Scope breadth is visible, and breadth is not the
defect. A declared `authority_scope` may be arbitrarily wide, including
universal. A wide scope is permitted and must be legible as wide; it may not
be described, in a record or in a summary, as bounded merely because a scope
field was populated. A boundary that no one can fail to satisfy is not a
boundary, and calling it one is a defect P6 forbids.

=== EVIDENCE ABS-0004:v8:S3#adopted_constraint:the-legibility-requirement-is-unen ===
The legibility requirement is unenforced, and saying so
is part of stating it. Nothing in this ontology supplies a scope grammar, an
interpretation rule, a validation step, a rendering requirement, or a rule
governing what a summary may say about a scope field. The requirement above
therefore binds whoever writes a record or a summary, and a violation is a
defect discoverable by reading rather than one caught by a check. This
constraint is included because the earlier draft of v8 corrected exactly this
overclaim in the standing-authority constraint and reproduced it here two
paragraphs later, which is the defect class P6 names and the third occurrence
of it inside this document.

--- END OF EVIDENCE ---

Answer only the question above. If the evidence set is insufficient to answer it, say so and name what is missing.`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5.6-terra`
- Claude: `claude-sonnet-5`

## Prompt

You are reviewing a proposed ontology amendment and the implementation plan that depends on it. This is ONE question of eight, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

Status: ABS-0004 v8 is proposed and not admitted. PLAN-20260723-0002 is proposed and not admitted. Neither has governance force.

Three disclosures, because withholding them would be dishonest rather than isolating:

1. v8 is a response to a prior review round (COMP-0039..0046) of v7. It withdrew several claims that round found unsupported. Do not treat a sentence as sound because it is a correction; a correction can overreach or under-reach like any other text.

2. Of the 118 claims that round produced whose citations the amendment broke, 58 were adjudicated as still applying against v8. v8 made the ontology more honest about what it does not do; it did not make the mechanisms work. Do not credit v8 with having closed what it only disclosed.

3. The executor that drafted v8 also proposed the dispositions deciding which claims still applied, subject to operator approval. Treat both as one party's work.

Quote only text that appears below. Do not rely on repository access.

IMPORTANT: the evidence set below was scoped deliberately, and the scoping may be wrong. If you need a section, constraint, or record that is not present, name it explicitly and say what you would have used it for. That report is wanted output, not a failure.

Do not certify or praise. No provider product recommendations.

=== QUESTION Q1 ===
v8 requires that a wide authority_scope "must be legible as wide", and then adds a second constraint stating that this requirement is enforced by nothing: no scope grammar, no interpretation rule, no validation step, no rendering requirement, no rule governing what a summary may say.

Is a constraint that states its own unenforceability a constraint, or a note about one? Say what it obliges that the requirement alone would not, and what a reader could do with it that they could not do with the requirement plus silence. If the honest form is to delete the requirement rather than annotate it, say so and give the replacement.

=== EVIDENCE ABS-0004:v8:S3#adopted_constraint:scope-breadth-is-visible-and-bread ===
Scope breadth is visible, and breadth is not the
defect. A declared `authority_scope` may be arbitrarily wide, including
universal. A wide scope is permitted and must be legible as wide; it may not
be described, in a record or in a summary, as bounded merely because a scope
field was populated. A boundary that no one can fail to satisfy is not a
boundary, and calling it one is a defect P6 forbids.

=== EVIDENCE ABS-0004:v8:S3#adopted_constraint:the-legibility-requirement-is-unen ===
The legibility requirement is unenforced, and saying so
is part of stating it. Nothing in this ontology supplies a scope grammar, an
interpretation rule, a validation step, a rendering requirement, or a rule
governing what a summary may say about a scope field. The requirement above
therefore binds whoever writes a record or a summary, and a violation is a
defect discoverable by reading rather than one caught by a check. This
constraint is included because the earlier draft of v8 corrected exactly this
overclaim in the standing-authority constraint and reproduced it here two
paragraphs later, which is the defect class P6 names and the third occurrence
of it inside this document.

--- END OF EVIDENCE ---

Answer only the question above. If the evidence set is insufficient to answer it, say so and name what is missing.

## OpenAI Response

- model: `gpt-5.6-terra`

```
It remains a constraint in the normative sense, but not an enforceable one. The first passage imposes a substantive prohibition: a wide declared scope “must be legible as wide” and “may not be described, in a record or in a summary, as bounded merely because a scope field was populated.” That obligation exists even if no check detects breach.

The second passage does not supply a scope meaning, test, or enforcement mechanism. Its added obligation is chiefly one of candour about the first passage’s limits: “The legibility requirement is unenforced, and saying so is part of stating it.” It also fixes the intended accountability model: the requirement “binds whoever writes a record or a summary,” and breach is “discoverable by reading rather than one caught by a check.”

Thus it is more than a merely private explanatory note, because it prevents the requirement from being presented as though the ontology operationalizes or validates legibility. But it is not a second mechanism-level constraint. It neither determines when a scope is wide nor gives a reproducible criterion for deciding whether language makes that width legible.

Compared with the requirement plus silence, the disclosure lets a reader:

- distinguish a manual reading-based allegation of misleading description from a validation failure;
- refuse an implication that field population, schema conformance, or a check establishes boundedness or legibility;
- identify that no supplied ontology feature decides disputed cases consistently; and
- hold the record or summary writer responsible for the description without claiming that the ontology prevented or detected their breach.

The honest form is not necessarily deletion. An unenforced normative prohibition can still be a constraint; deletion would remove even the stated duty not to describe an arbitrarily wide scope as bounded. The honest replacement is to retain the prohibition but state its limited character more directly, for example:

> A declared `authority_scope` may be arbitrarily wide, including universal. Records and summaries must not describe such a scope as bounded merely because a scope field was populated. This ontology provides no grammar, interpretation rule, validation, rendering requirement, or summary rule to determine or enforce that judgment; compliance is assessed by reading the record or summary.

The supplied evidence is insufficient to assess whether the terms “wide,” “legible,” “bounded,” or the referenced defect class “P6” have definitions elsewhere that would make manual assessment more determinate. I would need those definitions, and any stated adjudication procedure, to assess whether this is a usable constraint rather than only an aspiration with a disclosure.
```

## Claude Response

- model: `claude-sonnet-5`

```
## Constraint or note?

Read functionally, the second block does not constrain any party's action beyond what the first block already constrains. A constraint forbids, requires, or permits some act by some party. The first block does that: it requires that a wide scope "must be legible as wide" and forbids describing it "as bounded merely because a scope field was populated." The second block adds no new prohibition, permission, or procedure. It:

- asserts an absence ("Nothing in this ontology supplies a scope grammar, an interpretation rule, a validation step, a rendering requirement, or a rule governing what a summary may say about a scope field"),
- restates that the prior requirement "binds whoever writes a record or a summary" — a restatement, not a new obligation,
- reclassifies how a violation would be found ("a violation is a defect discoverable by reading rather than one caught by a check"),
- and gives a document-internal reason for its own inclusion (naming this as "the third occurrence" of a pattern P6 names, following a correction made earlier "in the standing-authority constraint").

None of these are obligations on a record-writer, a summarizer, a validator, or a tool. They are findings about the state of the ontology's own machinery. That makes this block a **note about a constraint**, not a constraint in its own right — it documents that the constraint above it is unbacked, rather than doing anything to back it.

## What it obliges that the requirement alone would not

Nothing operative. It does not create a grammar, an interpretation rule, a validation step, a rendering rule, or a review obligation — it explicitly disclaims all five. The only thing it obliges is a representational one: it forecloses a specific kind of claim, namely that a check exists. After this text, no one implementing or auditing against v8 can truthfully assert that a scope-legibility violation would be *caught* by anything the ontology supplies. That is a constraint on future *claims about* the ontology, not a constraint on scope declarations, records, or summaries themselves.

## What a reader can do with it that requirement-plus-silence would not allow

With the requirement alone and silence on enforcement, a reader has to investigate (or guess) whether a grammar, validator, or rendering rule exists elsewhere before relying on the requirement, and could reasonably assume — wrongly — that some such mechanism is implied by the requirement's phrasing ("must be legible as wide" reads like a testable rule). With the disclosure, a reader can immediately conclude:

- no tooling or automated check will ever surface a violation ("discoverable by reading rather than one caught by a check"),
- any implementation (e.g., PLAN-20260723-0002) that assumes the ontology enforces scope legibility is relying on something the amendment itself says does not exist, and
- this is not a one-off gap but, per the note's own account, a *recurring* defect pattern inside v8 ("the third occurrence of it inside this document") — which bears on how much weight to give any other "must" in this amendment that isn't separately checked.

That last point is real information: it tells a reader where the burden of verification actually sits (entirely on manual reading, by an unspecified party, at an unspecified time) rather than leaving that question open.

## Should the requirement be deleted rather than annotated?

The note discloses not just an absent *checker* but an absent *definition*: "no scope grammar, an interpretation rule ... " Without an interpretation rule, "legible as wide" has no stated criterion even for a human reader to apply consistently — this is not merely unenforced, it is uninterpreted. A "must" with no stated interpretation rule and no grammar is not a requirement a reader can comply with or fail to comply with in any checkable sense, manually or otherwise; it is an aspiration dressed as an obligation. On that basis, the honest form is not to keep the "must" and annotate its unenforcement, but to withdraw the imperative and state the gap plainly, e.g.:

> "Wide authority_scope declarations are permitted. This ontology defines no grammar, interpretation rule, validation step, or rendering rule for what makes a scope 'legible as wide.' Whether a given record or summary satisfies legibility is therefore not decidable under this ontology as written."

That formulation keeps everything the note actually establishes (the gap) and drops the part it cannot support (a binding "must" with no criterion of satisfaction).

## Missing evidence

Two things referenced by the note are not in this evidence set and would matter to a full answer:

- **The text of "defect P6"** — the note relies on P6 to characterize the violation as a named, recognized defect class, but P6's own definition isn't provided, so I can't confirm the note's characterization of what P6 forbids beyond the paraphrase given here.
- **The "standing-authority constraint" text** — the note claims this same overclaim was "corrected" there and "reproduced ... here two paragraphs later." Without that constraint's text, I can't verify the claimed correction-then-recurrence, only report that the note asserts it.
```
