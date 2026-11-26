# Step 3A test traceability

[ALG] This is a source/test map, not an execution report. Family identifiers
refer to the retained [48-family proposed matrix](../FALSIFICATION-MATRIX.md).
A listed test establishes only its named fixture obligation; it does not imply
that every variant of that family, or all 48 families, was implemented or run.
The scope is [A1–A4](ADMISSION-AND-CONDITIONS.md) and the
[implementation contract](IMPLEMENTATION.md).

## 1. Test sources and oracle

| Label | Source | Role |
| --- | --- | --- |
| M | [test_qualification_model.py](../../../../tests/test_qualification_model.py) | Model aggregation, time, witnesses, omissions and domain refusal |
| R | [test_qualification_records.py](../../../../tests/test_qualification_records.py) | Strict shapes, actual Git pins, immutable bytes and assessment publication |
| L | [test_qualification_legacy.py](../../../../tests/test_qualification_legacy.py) | Checked legacy projection, v1 boundary, rollback and historical persistence |
| E | [test_executor_equivalence.py](../../../../tests/test_executor_equivalence.py) | No implicit context, unconditional Boolean refusal and retired first-success behavior |
| F | [qualification_fixtures.py](../../../../tests/qualification_fixtures.py) | Real temporary Git repositories containing explicitly fictional catalog and witness evidence |

The oracle combines [r2 rules](../r2/DETERMINISTIC-RULES.md), the frozen
[schema](../r2/ASSESSMENT-SCHEMA.json) and the narrower admission. In particular,
3A expects `C3=C10=Q_C3_C10=unresolved` even where future-program r2 rules describe
synthetic negative C3 findings. Successful synthetic model controls are needed
to detect universal refusal; they never establish live qualification.

Test names below omit only the module path identified by M/R/L/E. Parameterized
tests must be reported by their collected full node IDs in execution evidence.

## 2. Model and source obligations

| Family / condition | Actual test examples | Bounded obligation |
| --- | --- | --- |
| F01, F02, F35 | M `test_f01_f43_clean_synthetic_controls`; `test_f01_same_mid_is_catalog_equivalence_not_permission`; `test_f02_f24_f43_evidence_class_pair_matrix`; `test_f35_unknown_release_blocks_identity_not_catalog_relation` | Clean same/different catalog relations; labels and unknown releases do not establish identity standing |
| F03, F19, F20 | M `test_f19_time_proven_irrelevant_contradiction_is_excluded`; `test_f20_freshness_inclusive_boundary`; `test_f38_absent_source_availability_preserves_only_diagnostic` | Stale/after-event/interval exclusion, inclusive freshness boundary, and availability gap distinguished |
| F14–F16 | M `test_f14_wrong_endpoint_cannot_resolve_same_requested_name`; `test_f14_same_requested_name_binds_distinct_endpoint_targets`; `test_f15_unknown_endpoint_has_no_nonempty_string_fallback`; `test_f16_colliding_endpoint_spelling_is_unresolved` | Exact endpoint binding; no string fallback or ambiguous spelling winner |
| F18, F21 | M `test_f14_same_requested_name_binds_distinct_endpoint_targets`; `test_f21_irrelevant_contradiction_not_global_veto` | Other-endpoint/name controls are excluded with reasons; this does not claim every F18 order variant |
| F22–F25 | M `test_f22_relevant_contradiction_survives_clean_source`; `test_f23_ambiguity_survives_clean_source`; `test_f24_cross_source_disagreement_survives_corroboration`; `test_a1_f43_witness_on_exact_alternative_chain_positive_control` | Relevant adverse evidence survives favorable sources; a real stipulated witness can bind an exact agreeing alternative chain |
| F28, F29, F36 | M `test_f28_capture_snapshot_reference_mismatch_is_typed`; `test_f29_supersession_is_not_newest_source_override`; `test_f36_null_scope_control_and_unsupported_scope` | Link mismatch is typed; unknown scope/supersession cannot silently permit |
| F31, F32 | M `test_f31_provider_self_report_cannot_claim_corroboration`; `test_f32_failed_capture_cannot_supply_positive_or_name_absence`; `test_f32_proven_irrelevant_failed_capture_is_not_global_veto`; `test_f32_string_false_is_not_boolean_capture_success` | Evidence labels and failed capture cannot manufacture positive support; Boolean types enforced |
| F33, F34 | M `test_f33_invalid_target_domain_is_typed_before_sets`; `test_f34_missing_chain_never_invents_refs`; `test_f34_existing_endpoint_is_not_a_model_target`; `test_f34_payload_hash_mismatch_is_not_corroboration`; `test_f33_raw_surrogate_query_is_typed_refusal` | Scalar, wrong-kind, missing, mismatching and malformed inputs refuse without an accepting exception path |
| F37, F38 | M `test_f37_reversed_interval_is_invalid_not_no_assertion`; `test_f37_zero_length_assertion_interval_is_inclusive`; `test_f38_capture_before_observation_is_invalid`; `test_f38_source_after_bound_is_exclusion_not_timestamp_error`; `test_f38_availability_chronology_checked_before_endpoint_exclusion` | Cross-field chronology precedes exclusion; valid late evidence differs from malformed time |

## 3. A1–A3 controls

| Condition / family | Actual test examples | Bounded obligation |
| --- | --- | --- |
| A1 / F43 | M `test_f43_complete_witness_pair_matrix`; `test_f02_f24_f43_evidence_class_pair_matrix` | Valid/missing/mismatched witness pairs and legacy evidence-class pairs; only exact bilateral premises can satisfy synthetic Q_identity |
| A1 / F43 | M `test_a1_f43_borrowed_corroboration_label_cannot_qualify_other_chain`; `test_a1_f43_verification_premise_is_bound_to_exact_chain`; `test_a1_f43_witness_payload_from_other_side_is_rejected` | No borrowed CAP label, swapped payload or verification-body mismatch |
| A1 / F43 | M `test_f43_exact_witness_property_binding`; `test_f43_exact_row_not_merely_witness_label`; `test_f43_unknown_property_is_not_model_identity_evidence`; `test_f43_proof_row_pins_checker_rule_version_and_scope`; `test_f43_witness_revocation_boundary`; `test_f43_duplicate_conflicting_fixture_row_identity_is_invalid` | Exact endpoint/name/target/event/property, row, verifier/rule/scope and revocation conditions |
| A1 / F38 | M `test_a1_f38_late_witness_not_cleared_by_early_assessed_at`; `test_a1_f38_missing_witness_availability_is_not_assessed_at` | Assessment timestamp cannot substitute for timely witness-and-verification availability |
| A2 / F34, F42 | M `test_a2_f34_explicit_missing_chain_declaration_is_representable`; `test_a2_f42_unknown_digest_omission_blocks_clean_but_not_supplied_relation`; `test_a2_f42_orphan_snapshot_cannot_be_silently_dropped` | Explicit payload/MID omission, null unknown digest/ID, and unrepresentable linkage refusal |
| A2 / F42 | M `test_a2_f42_proven_irrelevant_omission_control`; `test_a2_f42_declaration_after_cutoff_is_not_known_at_event`; `test_a2_f42_declaration_body_must_match_retained_bytes`; `test_f42_known_external_source_cannot_be_counted_as_exhausted` | Declaration body, relevance and fixed-cutoff checks; known external uncertainty retained |
| A1–A2 / F42 | M `test_f42_inventory_source_removal_is_detected`; `test_f42_inventory_file_removal_is_detected`; `test_f42_selected_sources_cannot_prune_pinned_inventory`; `test_a1_f42_source_target_manifest_cannot_drop_decoded_target`; `test_f42_query_cannot_replace_pinned_context`; `test_f42_query_has_no_caller_authority_fields` | No source/target pruning, context replacement or caller authority switch |
| A3 / F10, F26, F27 | M `test_f10_f26_permutation_and_exact_duplicate_invariance`; `test_a3_total_diagnostic_order_has_canonical_tie_break`; R `test_conflicting_same_id_bytes_have_order_invariant_diagnostic`; `test_identical_duplicate_record_bytes_are_idempotent` | Stable semantic axes and complete-diagnostic tie-break; duplicates add no source weight |
| A3 / F39 | L `test_checked_full_context_still_never_projects_positive_legacy_resolution`; `test_checked_equivalence_can_project_relation_but_never_permission`; `test_legacy_arguments_must_equal_the_complete_retained_invocation`; `test_wrong_subject_order_cannot_borrow_another_query`; E `test_legacy_boolean_always_blocks_even_direct_construction` | Exact-subject diagnostic projection cannot clear the legacy Boolean or resolver |
| A3 / F39, F41 | L `test_disabled_or_failing_engine_never_recovers_old_permitting_path`; `test_assessment_for_another_query_is_not_a_projection_source`; `test_malformed_assessment_cannot_be_projected`; E `test_no_context_never_iterates_a_caller_selected_source_universe`; `test_known_first_success_counterexample_is_now_order_invariant` | Missing/disabled/failing engine and forged output cannot recover R13/R14 permitting |
| A3 / F39, F40 | L `test_r2_refusal_and_assessment_cannot_be_written_as_historical_records`; `test_new_v1_builder_never_coerces_resolved_to_boolean`; `test_new_v1_builder_rejects_fabricated_positive_projection_shapes`; `test_historical_graph_and_idempotent_storage_do_not_upgrade_standing`; `test_same_legacy_id_with_changed_bytes_cannot_overwrite_history`; `test_failed_atomic_publication_leaves_no_valid_record` | Separate r2/v1 kinds; history remains diagnostic; collision and interrupted-publication refusal |

## 4. Record boundary and domain controls

| Family / boundary | Actual test examples | Bounded obligation |
| --- | --- | --- |
| F33, F37 / strict input | R `test_strict_json_rejects_duplicate_nonfinite_and_invalid_utf8`; `test_canonical_bytes_is_total_and_does_not_coerce_non_json`; `test_shape_validation_checks_actual_calendar_and_offsets`; `test_valid_explicit_offset_boundaries_are_preserved`; `test_shape_validator_rejects_wrong_types_and_unknown_fields`; `test_shape_error_detail_does_not_depend_on_dictionary_order` | Strict JSON, calendar/offset bounds, closed shapes and canonical schema diagnostics |
| F34, F42 / real bytes | R `test_artifact_reference_never_invents_bytes_or_identity`; `test_anchor_uses_pinned_git_bytes_and_freezes_all_inputs`; `test_query_cannot_construct_an_anchor`; `test_anchor_rejects_source_inventory_pruning`; `test_anchor_rejects_wrong_tree_without_inventing_pin`; `test_auxiliary_bytes_cannot_override_a_pinned_path`; `test_nonnull_git_blob_requires_path_membership_not_just_equal_hash`; `test_catalog_symlink_cannot_replace_retained_regular_bytes` | Real tree/blob/path binding and immutable externally pinned source universe |
| F40 / assessment persistence | R `test_invalid_result_envelope_cannot_be_published_as_an_assessment`; `test_assessment_store_recomputes_and_identical_replay_is_idempotent`; `test_shape_valid_forged_assessment_cannot_be_published`; `test_accepted_assessment_cannot_overwrite_conflicting_store_bytes`; `test_interrupted_publication_does_not_publish_partial_bytes` | Shape validity alone cannot publish; exact recomputation, idempotence and no partial/overwriting write |
| F44 / production boundary | M `test_f44_no_anchor_production_cannot_invent_context`; `test_f44_synthetic_anchor_cannot_enter_production`; R `test_synthetic_result_cannot_be_published_in_production_domain`; `test_synthetic_assessment_store_cannot_enter_production_checkout` | No production context/acceptance or synthetic replay into production storage |
| F09, F48 / refusal portion | M `test_f48_unadmitted_kinds_and_cross_kind_remain_unresolved`; `test_f01_f43_clean_synthetic_controls` | Selected tool/human/cross-kind refusal fixtures and unresolved C3/C10 even in the successful model control; no full wrapper/ancestry coverage claim |

## 5. Planned work not established by this matrix

[OPEN] F04–F08 and F45 tool/human binding semantics belong to 3B. F11–F13,
F46 and F47 ancestry/conflict/lineage evaluation belong to separately admitted
3C work; constant refusal is not implementation of those evaluators. F17's
admitted alias path is absent. F30's full retrospective append/history scenario
is not claimed by the event-time witness controls. F09/F48 here cover only
the stated refusal fixtures, not all swapped/wrapped ancestry scenarios or
Step 5 activation. Other broad families retain untested variants beyond the
specific rows above.

Schema corpus checks show shape acceptance/rejection only. The retained r1/r2
baseline probes describe the historical implementation. Neither substitutes
for these runtime assertions, a targeted mutation result or exact-subject
observed-execution evidence.

## 6. Targeted falsification and reporting

[ALG] [falsify_qualification_3a.py](../../../../scripts/falsify_qualification_3a.py)
defines selected admitted guard mutations and reuses the strict classifier in
[falsify_verify_v2.py](../../../../scripts/falsify_verify_v2.py). It copies the
observed source files into temporary workspaces and does not mutate the source
repository. The report destination must be outside that repository.

```sh
python -I scripts/falsify_qualification_3a.py . --report /tmp/qualification-3a.json
```

Each selected unmodified baseline must pass. The identical collected node IDs
must then execute under mutation, with an ordinary call-phase assertion/test
failure. Collection/selection drift, setup/teardown failure, runtime exception,
usage/internal error, process-launch failure and timeout are not catches. The
report retains the baseline, mutation, exact failed node IDs, phase reports and
complete stdout/stderr.

No mutation score or pytest total is asserted here. The final retained evidence
must identify the actual subject, interpreter, commands, results and limits.
Synthetic fixture success, targeted mutation detection and same-provider review
do not independently establish origin, verifier lineage, adjudication standing
or authorization.
