# Step 3 r2 baseline observations

[NUM] **189 recorded operation observations over 28 synthetic snapshot/capture pairs.** These are observations of unchanged baseline code, including returned values and exceptions. They are not 189 correctness tests, a mutation score, or evidence that the proposed r2 mechanism works.

## 1. Retained evidence and provenance

| Item | Recorded value |
| --- | --- |
| Inspected checkout | `8b8e24d133eaa3a585eefa14e76a02a519b73b03` |
| Runtime/source baseline | `5515f55894b10ad70c321340257f67a960dcc382` |
| Interpreter | Python 3.13.5 |
| Probe | [probe_resolution_contract_r2.py](probes/probe_resolution_contract_r2.py) |
| Complete fixtures and observations | [resolution_contract_r2_baseline.json](probes/resolution_contract_r2_baseline.json) |
| Probe SHA-256 | `65d6d817aa060ed2821698b46b61bd12058e967785a5c7ecbba603b948b581f6` |
| Report SHA-256 | `8ae5d767524e395f3b185f3caface07f696900c09fd24c04ce33e23bbafaca58` |
| Probe/report sizes | 17,071 / 170,794 bytes |

[ALG] The probe checks the exact checkout HEAD before import. It compares 15 inspected implementation, test and governing-document files byte-for-byte with the runtime baseline, records their SHA-256 values, and checks they remain unchanged after execution. The 15 hashes are retained under `source_hashes`; this is an explicit inspected-file set, not a hash inventory of the whole repository.

The original r1 probe and both r1 reports are checked before and after execution against their pinned hashes. They remain unchanged. Writer operations use only `writer-sandbox/` under an explicitly external output directory. No repository runtime or historical evidence is rewritten by the probe.

Actual preparation executor: ChatGPT, self-declared/unverified. This report summarizes the retained execution by the assisting ChatGPT process. The documentation pass inspected the stored observations and source; it did not rerun the probe. Same-provider assistance is not independent adjudication. The report contains no execution wall-clock timestamp; none is inferred from fixture event times.

## 2. What the observation count contains

| Operation | Observations |
| --- | ---: |
| Snapshot shape/ID validation | 27 |
| Capture shape/ID validation | 27 |
| Single-source resolve_identity | 27 |
| equivalence, both source-list orders | 54 |
| Resolution annotation construction | 23 |
| Resolution graph-seed projection | 18 |
| Direct target-record validation | 5 |
| Resolver calls demonstrating absence of a target-registry parameter | 4 |
| Direct Boolean-property construction | 1 |
| Resolution writes | 2 |
| Catalog write | 1 |
| **Total** | **189** |

[NUM] The 28 pairs include one right-side comparison control and 27 left-side cases. Not every operation is reached after an exception. The two equivalence orders permute source pairs; they are not left/right argument-swap tests. This probe does not execute the future 48-family matrix or a full permutation/mutation campaign.

## 3. Capture and target behavior

| Fixture | Observed baseline result |
| --- | --- |
| Valid MID control | Single-source resolution and annotation succeed; synthetic corroboration labels produce non_equivalent with blocks_adjudication=false against the right control |
| capture_success=false | Capture shape/ID check accepts; resolver returns resolved=true; annotation and graph seed are produced; equivalence Boolean remains false |
| capture_success="false" | Capture/resolver checks reject with CatalogRecordError: success must be Boolean |
| Dangling MID, existing EID target, arbitrary non-MID string | Resolver returns the supplied target; annotation and graph seed preserve it |
| Targets 7, true, 1.5 | Scalar targets resolve and propagate into annotations/graph seeds |
| Targets 0, false, empty string | Resolver/equivalence accept the target; annotation builder rejects through its truthiness-based required-target check |
| Targets null or list | Catalog validation rejects; these are negative controls |
| Targets true and 1 in one snapshot | Python equality/set behavior collapses them; the resolver reports the Boolean target as resolved |
| Mixed integer/string competing targets | Resolver raises TypeError while ordering the ambiguous targets; this is not a typed unresolved result |
| MID with release_identity=unknown | Resolution and comparison accept the MID reference; no release-sufficiency check is performed |

[NUM] A separate read-only inventory of the retained MID directory found **132/132** records with `release_identity=unknown`. That count is source inspection, not an extra operation in the 189-observation report. The existing records are historical input, not established release bindings.

### Target-registry boundary

[ALG] The old resolver/equivalence interfaces have **no target-registry parameter**. Four recorded calls retain differently named target-evidence contexts but explicitly mark them as not consumed by the API; the actual resolver inputs are identical. Their identical outcome does not demonstrate the resolver inspecting and accepting conflicting MID documents.

Separate direct catalog-validator controls show:

- A valid ModelIdentity and an unknown-release ModelIdentity pass their own v1 shape/ID checks.
- Adding an uninterpreted field produces different retained bytes under the same model record ID and still passes that validator.
- Changing the identity-bearing release field while retaining the old ID is rejected by the computed-ID check.
- A valid endpoint record passes generic catalog validation **as an endpoint**; that does not make it a valid model target.

These observations motivate target dereferencing, record-kind checks and complete-byte digests. They do not claim that the old resolver evaluated a conflicting target registry.

## 4. Scope, interval and availability behavior

| Fixture | Observed baseline result |
| --- | --- |
| scope=null control | Resolves |
| Unsupported scope string or object | Both pass current snapshot validation and are ignored for resolution |
| Reversed validity interval | Snapshot validation accepts; resolver returns no_applicable_assertion, without identifying an invalid interval |
| Equal validity bounds at the event | Resolves, confirming inclusive equality in this control |
| Invalid timestamp or missing nullable validity field | CatalogRecordError; retained negative controls |
| captured_at after the invocation, with earlier observed_at | Resolves |
| captured_at before observed_at | Resolves |
| Snapshot observed after the invocation | Single-source resolver correctly returns snapshot_after_invocation; outer equivalence retains different non-resolution reasons depending on source-list order |
| Uninterpreted superseded_by | Resolves without interpreting the supersession claim |

[ALG] The current API has no separate accepted event-availability proof. The capture chronology observations therefore expose missing checks; they do not establish actual historical availability or a retrospective evidence rule. Fixture timestamps are fictional. The r2 contract supplies proposed distinctions that remain unimplemented.

## 5. Annotation, graph and persistence surfaces

[NUM] The annotation builder accepts a fabricated outcome containing an arbitrary target, snapshot/capture IDs and invalid evidence/channel enum strings. The resulting record can be written by the existing resolution writer. Replacing the outcome's `resolved` Boolean with the string `"false"` still creates `resolved=true` through coercion.

Direct construction of `EquivalenceResult(status="non_equivalent")` with no identities but two synthetic `independently_corroborated` enum labels returns `blocks_adjudication=false`. These labels are test inputs, not verified witnesses. **A false helper Boolean is not an observed authorization grant.** Scoped source search under `ai_lab`, `scripts` and `.github` found no production authorization consumer of equivalence or this Boolean; the public construction/annotation surfaces nevertheless exist.

Resolution graph projections remain `authoritative=false`. They can carry the unsupported target values accepted upstream; their presence is not model identity, evidence sufficiency or ancestry proof. Dataclass type annotations do not perform that validation.

The isolated writer cases record complete before/after data and digests:

- Changing `resolved_identity` under the same RES ID writes different bytes to the same path.
- Changing `capture_success` under the same CAP ID likewise overwrites the same path.
- Different unresolved reasons can produce the same RES ID: the reversed-interval and future-observation annotations share the ID while retaining different reason/detail bytes.

These findings concern legacy mutable-path writers. They do not show an attack against a pinned Git object. The proposed consumer contract requires immutable byte-bound input and new collision-refusing assessment storage; general catalog-writer redesign is outside this slice.

## 6. Reproduction

[ALG] The script deliberately rejects a checkout whose HEAD differs from the recorded r1 commit. After r2 is committed, reproduce against a detached baseline worktree while using the retained r2 script. From the r2 repository root, with Git and Python available:

```bash
r2_probe_script="$PWD/docs/reviews/qualification_semantics/r2/probes/probe_resolution_contract_r2.py"
r2_probe_root="$(mktemp -d)"
git worktree add --detach "$r2_probe_root/baseline" 8b8e24d133eaa3a585eefa14e76a02a519b73b03
env -i PATH=/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 \
  /usr/bin/python3 -B "$r2_probe_script" \
  --repo "$r2_probe_root/baseline" \
  --output "$r2_probe_root/resolution_contract_r2_baseline.json"
```

The original interpreter was Python 3.13.5. A different interpreter must retain its own version and any behavior difference rather than claiming byte-identical reproduction. Expected report dimensions are 189 observations and 28 pairs; writer files remain outside the detached worktree. The probe performs no provider calls, pytest run, mutation campaign, admission or live qualification.

## 7. Standing

[OPEN] The baseline deficiencies remain present in production source because this revision is preparation only. The [r2 rules](DETERMINISTIC-RULES.md), [consumer matrix](CONSUMER-COMPATIBILITY.md) and [falsifier matrix](../FALSIFICATION-MATRIX.md) describe proposed future behavior. Their schema checks and existing-suite results must be reported separately from these observations.

No canonical VERIFY, corroboration witness, established tool/human binding, lineage upgrade or authority decision is created by this probe or report. PLAN remains proposed and implementation remains gated on separate admission.
