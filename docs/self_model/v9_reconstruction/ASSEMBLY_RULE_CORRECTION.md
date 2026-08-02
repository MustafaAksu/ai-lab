# Assembly rule, as accepted with one correction

Accepted under DECISION-20260727-0005. The reviewing executor's proposal reads:

> Assembly rule: replace the seventeen inherited `[ADOPTED_CONSTRAINT]` tags
> with `[INHERITED_CONSTRAINT]`.

There are seventeen occurrences of the tag in the task 3 candidate, but only
**sixteen are constraints**. The seventeenth, at the top of the document, is the
sentence-discipline legend entry that defines what the tag means:

    `[ADOPTED_CONSTRAINT]` constraint adopted now with its current enforcement
    honestly stated

Applied literally, the rule would rename that definition, leaving v9 defining a
category it no longer uses and defining neither category it does use.

## Corrected rule

1. **Sixteen constraint occurrences** become `[INHERITED_CONSTRAINT]`. All
   sixteen are byte-identical to their admitted v4 text after whitespace
   normalisation, verified before acceptance, so the label is true rather than
   asserted.

2. **The legend entry is replaced, not renamed.** The `[ADOPTED_CONSTRAINT]`
   definition is removed and the two accepted categories are defined in its
   place:

   - `[LIMITATION]` — descriptive boundary on what the ontology, its records, or
     current enforcement establish. Imposes no constraint and claims no adoption.
   - `[INHERITED_CONSTRAINT]` — constraint text carried forward unchanged from
     the admitted v4 baseline. Its current governance force derives from v4's
     admission, not from the proposed v9 document. A substantive change becomes
     `[PROPOSED_CONSTRAINT]` until separately admitted.

   The task 3 candidate already adds `[LIMITATION]` to the legend; that entry is
   retained and the `[ADOPTED_CONSTRAINT]` entry it sits beside is what gets
   replaced.

3. **`[PROPOSED_CONSTRAINT]` is unaffected.** v4 already uses it seven times and
   tasks 2 and 3 added two, one of which is the ModelIdentity constraint task 2
   changed. Text that changed is proposed; text that did not is inherited. That
   distinction is the point of the category and must survive assembly.

## Why the off-by-one matters

v8 was withdrawn because a proposed document carried twenty-four constraints
tagged with a category defined as "adopted now", so the governance status of
every constraint in it was undetermined. `[INHERITED_CONSTRAINT]` resolves that
by naming which version the force comes from. A legend that still defines
`[ADOPTED_CONSTRAINT]`, or that defines neither new category, would leave the
same question open in a different place.
