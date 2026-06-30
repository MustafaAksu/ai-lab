from ai_lab.research.session import ResearchSession


def test_research_session_has_identity():
    session = ResearchSession(title="RTG Test Session")

    assert session.title == "RTG Test Session"
    assert session.session_id
    assert session.created_at


def test_research_session_tracks_participants_artifacts_and_events():
    session = ResearchSession(title="RTG Test Session")

    session.add_participant("human:mustafa")
    session.add_participant("ai_peer:openai")
    session.add_participant("ai_peer:openai")

    session.add_artifact("dsn:rtg-open-m-v0.6")
    session.add_artifact("dsn:rtg-open-m-v0.6")

    session.add_event("note", "Initial session created.")

    assert session.participants == ["human:mustafa", "ai_peer:openai"]
    assert session.artifacts == ["dsn:rtg-open-m-v0.6"]
    assert len(session.events) == 1
    assert session.events[0]["type"] == "note"


def test_research_session_save_and_load(tmp_path):
    session = ResearchSession(title="Persistence Test")
    session.add_participant("human:mustafa")
    session.add_event("note", "Testing persistence.")

    path = tmp_path / "session.json"
    session.save(path)

    loaded = ResearchSession.load(path)

    assert loaded.session_id == session.session_id
    assert loaded.title == session.title
    assert loaded.participants == session.participants
    assert loaded.events == session.events
