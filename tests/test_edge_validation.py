from ai_lab.documentation.edge_validation import validate_edge_record


def valid_edge():
    return {
        "id": "EDGE-0001",
        "origin_type": "relation_record",
        "current_type": "relation_record",
        "title": "P-0001 based on SYN-0004",
        "created_at": "2026-06-30T00:00:00Z",
        "subject": {
            "id": "P-0001",
            "scope": "version",
            "version": "0.3-draft",
        },
        "predicate": {
            "id": "based_on",
            "vocabulary": "bootstrap_predicates",
            "version": "0.1",
        },
        "object": {
            "id": "SYN-0004",
            "scope": "version",
            "version": "0.1-draft",
        },
        "warrant": {
            "summary": "P-0001 v0.3 incorporates SYN-0004.",
        },
        "contributors": [
            {
                "peer_id": "PEER-0002",
                "role": "relation_author",
                "substrate": "GPT-5.5 Thinking",
            }
        ],
    }


def test_valid_edge_record_has_no_errors():
    assert validate_edge_record(valid_edge()) == []


def test_created_at_is_required():
    edge = valid_edge()
    del edge["created_at"]

    errors = validate_edge_record(edge)

    assert any("created_at" in error for error in errors)


def test_status_is_not_allowed_on_edge_records():
    edge = valid_edge()
    edge["status"] = "active"

    errors = validate_edge_record(edge)

    assert any("status" in error for error in errors)


def test_predicate_must_use_bootstrap_vocabulary():
    edge = valid_edge()
    edge["predicate"]["id"] = "qualifies"

    errors = validate_edge_record(edge)

    assert any("predicate.id" in error for error in errors)


def test_scope_is_required():
    edge = valid_edge()
    del edge["object"]["scope"]

    errors = validate_edge_record(edge)

    assert any("object.scope" in error for error in errors)


def test_version_scope_requires_version():
    edge = valid_edge()
    del edge["object"]["version"]

    errors = validate_edge_record(edge)

    assert any("object.version" in error for error in errors)


def test_lineage_scope_must_not_include_version():
    edge = valid_edge()
    edge["object"]["scope"] = "lineage"

    errors = validate_edge_record(edge)

    assert any("object.version" in error for error in errors)
