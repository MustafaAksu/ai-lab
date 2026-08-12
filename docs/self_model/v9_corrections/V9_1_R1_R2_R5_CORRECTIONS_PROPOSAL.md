# ABS-0004 v9.1 — R1/R2/R5 correction proposal

## Basis

- Repository HEAD: `cee8853ba4ebdd0bd4ce8e913c9138e7acd28f0b`
- Baseline ontology SHA-256: `ce1ddb25488175ed87d7c30d904c5ee334a51527bb5bfef3c45facf063bece51`
- Candidate ontology SHA-256: `6dbd6d87f41bae1a9510c43c55d8a3f1a843f6022978bf77710f8fc77753aaaf`
- Scope: four approved edits only. No R3 or R4 ontology text is added.

## R1 — inherited-constraint referent drift

The packaging executor's initial R1 check classified C6, C7, C9, C10, and C11 as preserving semantics. That check was incomplete because it extracted referents from the constraint body and therefore missed the backward reference from Section 4.17, which identifies `VerificationRun` as "the typed record C10 requires."

Independent review established that C10's second admission branch — independent review of the verifier — has materially changed meaning. In admitted v4, a named independent review artifact converted the verifier-lineage status. In v9.1, Section 4.17 requires exact VerificationRun linkage, resolved reviewer independence, coverage of the verifier/version/rule/inputs/environment/result, and a positive review outcome; merely naming or linking an artifact changes nothing.

Final R1 disposition:

- C6: no material referent drift.
- C7: no material referent drift.
- C9: no material referent drift.
- C11: no material referent drift.
- C10: material referent drift established; text unchanged, tag changed from `[INHERITED_CONSTRAINT]` to `[PROPOSED_CONSTRAINT]`.

The earlier C3 correction remains the precedent: C3 had already been found to have semantic drift and was retagged before this R1 check. R1 therefore records both the prior successful drift detection (C3) and that the packaging executor's first C10 check missed a backward referent later found by the reviewing executor. The initial check is recorded as incomplete, not as having passed.

## R2 — limitation category leaks

### R2a — inherited-referent rule

The descriptive statement remains `[LIMITATION]`: textual continuity does not establish semantic identity when a constraint's referents differ.

The admission condition is separated as `[PROPOSED_CONSTRAINT]`:

`Such dependencies require re-examination before admission.`

This removes normative work from a category whose legend says it imposes no constraint.

### R2b — `identity_verification_status`

The descriptive statements remain `[LIMITATION]`: schema v1 syntactically accepts `verified`, no admitted capture path presently substantiates it, the current path emits `unresolved`, and validator acceptance is syntactic compatibility rather than a licensed status.

The forward-looking non-mutation rule is separated as `[PROPOSED_CONSTRAINT]`:

`Later append-only identity resolution records do not mutate or upgrade identity_verification_status.`

The other limitation statements were re-scanned for normative force. No third category leak was established; descriptive uses such as `cannot be treated` and cross-references such as `requires` do not independently impose a new obligation or status transition.

## R5 — historical challenge questions

Section 13's fourteen stale challenge questions are removed from the ontology. They are replaced by a non-normative pointer only:

`Review and challenge questions are retained as non-normative comparison artifacts under docs/comparisons/; they do not form part of this ontology.`

No new challenge set is introduced into ABS-0004.

## R4 — no ontology addition

No new R4 boundary statement is added. Section 3 already states that repository records do not by themselves establish extra-systemic entitlement and that a recorded authorization-chain terminus does not itself establish substantive authorization. R4 should therefore be recorded in the admission decision as an accepted implication of existing limitations, rather than repeated in ontology text.

## Verification

- Patch applies cleanly to an independent clean checkout at `cee8853`.
- `git diff --check`: passed.
- Resulting ontology is byte-identical to the retained candidate and hashes to `6dbd6d87f41bae1a9510c43c55d8a3f1a843f6022978bf77710f8fc77753aaaf`.
- `python3 -m pytest -q tests/test_abstraction.py`: 7 passed.
- Full suite with import-only provider SDK stubs outside the repository: patched checkout 723 passed / 3 failed. An unmodified clean checkout at the same HEAD produces the same 723 passed / 3 failed. All three failures are the pre-existing `SELF_MODEL.json` stale-state failures; the R1/R2/R5 patch adds no test regression.
- No repository file other than `docs/abstractions/ABS-0004-invocation-authorization-ontology.md` is modified by the patch.

This proposal does not adjudicate or admit v9.1.
