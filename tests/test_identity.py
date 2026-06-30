from ai_lab.research.identity import Identity, IdentityKind


def test_identity_represents_persistent_research_peer():
    identity = Identity(
        identity_id="human:mustafa",
        name="Mustafa Aksu",
        kind=IdentityKind.HUMAN,
        description="Human research peer and project originator.",
    )

    assert identity.identity_id == "human:mustafa"
    assert identity.kind == IdentityKind.HUMAN


def test_identity_serialization_round_trip():
    identity = Identity(
        identity_id="ai_peer:openai",
        name="OpenAI Peer",
        kind=IdentityKind.AI_PEER,
        description="AI peer accessed through an OpenAI provider.",
    )

    loaded = Identity.from_dict(identity.to_dict())

    assert loaded == identity
    assert loaded.kind == IdentityKind.AI_PEER
