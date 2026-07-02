from ai_lab.documentation.interaction_log import (
    EpisodeL1Summary,
    InteractionLogError,
    InteractionLogEvent,
)

import pytest


def test_interaction_log_event_from_text_hashes_raw_text():
    event = InteractionLogEvent.from_text(
        event_id="EVT-0001",
        episode_id="EP-0001",
        turn_id=0,
        created_at="2026-07-02T12:10:00+00:00",
        event_type="user_message",
        role="user",
        actor="mustafa",
        summary="Asked for the next implementation step.",
        request_text="raw prompt",
        artifact_ids=["COMP-0009"],
        topics=["memory", "warrant"],
    )

    assert event.request_text_hash is not None
    assert len(event.request_text_hash) == 64
    assert event.response_text_hash is None
    assert event.artifact_ids == ("COMP-0009",)
    assert event.topics == ("memory", "warrant")


def test_interaction_log_event_rejects_invalid_event_type():
    with pytest.raises(InteractionLogError, match="event_type"):
        InteractionLogEvent(
            event_id="EVT-0001",
            episode_id="EP-0001",
            turn_id=0,
            created_at="2026-07-02T12:10:00+00:00",
            event_type="not-a-type",
            role="user",
            actor="mustafa",
            summary="Invalid event type.",
        )


def test_episode_l1_summary_validates_citations_and_edge_seed_bridge():
    summary = EpisodeL1Summary(
        l1_id="L1-0001",
        episode_id="EP-0001",
        created_at="2026-07-02T12:15:00+00:00",
        summary_version="v1",
        summary_text="Capability-map discussion converged on warranted memory freshness.",
        source_event_ids=["EVT-0001", "EVT-0002"],
        citations=[
            "3ac9f2b1d0af@a1c2d3e|b:1024-2047",
            "4bc9f2b1d0af@a1c2d3e|t:10-40;tok=mistral-v3",
        ],
        key_decisions=["Implement L1 summary schema with future edge compatibility."],
        completed_work=["Created COMP-0009 and SYNCOMP-0005."],
        open_questions=["When should WarrantEdge become persistent?"],
        risks=["Summaries without warrants may launder stale claims."],
        next_actions=["Implement P0 schema slice."],
        topics=["memory", "warrant"],
        generation_model="gpt-5",
        generation_prompt_id="PROMPT-0001",
        coverage_score=0.8,
        freshness_state="fresh",
    )

    seeds = summary.future_edge_seed_records()

    assert summary.coverage_score == 0.8
    assert summary.stable_content_hash()
    assert {
        "source_id": "L1-0001",
        "predicate": "derived_from",
        "target_id": "EVT-0001",
    } in seeds
    assert {
        "source_id": "L1-0001",
        "predicate": "cites",
        "target_id": "3ac9f2b1d0af@a1c2d3e|b:1024-2047",
    } in seeds


def test_episode_l1_summary_rejects_bad_citation():
    with pytest.raises(InteractionLogError, match="Invalid citation"):
        EpisodeL1Summary(
            l1_id="L1-0001",
            episode_id="EP-0001",
            created_at="2026-07-02T12:15:00+00:00",
            summary_version="v1",
            summary_text="Bad citation test.",
            source_event_ids=["EVT-0001"],
            citations=["not-a-citation"],
        )


def test_episode_l1_summary_rejects_invalid_coverage_score():
    with pytest.raises(InteractionLogError, match="coverage_score"):
        EpisodeL1Summary(
            l1_id="L1-0001",
            episode_id="EP-0001",
            created_at="2026-07-02T12:15:00+00:00",
            summary_version="v1",
            summary_text="Bad coverage score test.",
            source_event_ids=["EVT-0001"],
            citations=[],
            coverage_score=1.5,
        )


def test_episode_l1_summary_rejects_duplicate_source_events():
    with pytest.raises(InteractionLogError, match="source_event_ids"):
        EpisodeL1Summary(
            l1_id="L1-0001",
            episode_id="EP-0001",
            created_at="2026-07-02T12:15:00+00:00",
            summary_version="v1",
            summary_text="Duplicate source events test.",
            source_event_ids=["EVT-0001", "EVT-0001"],
            citations=[],
        )
