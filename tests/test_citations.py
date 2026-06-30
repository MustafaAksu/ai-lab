import pytest

from ai_lab.documentation.citations import (
    Citation,
    CitationError,
    CitationSpan,
    format_citation,
    parse_citation,
)


def test_parse_byte_citation():
    citation = parse_citation("3ac9f2b1d0af@a1c2d3e|b:1024-2047")

    assert citation.cid == "3ac9f2b1d0af"
    assert citation.version == "a1c2d3e"
    assert citation.span.unit == "b"
    assert citation.span.start == 1024
    assert citation.span.end == 2047
    assert citation.span.tokenizer is None


def test_parse_char_citation():
    citation = parse_citation("3ac9f2b1d0af@v1.2.3|c:10-42")

    assert citation.version == "v1.2.3"
    assert citation.span.unit == "c"
    assert citation.span.start == 10
    assert citation.span.end == 42


def test_parse_token_citation_requires_tokenizer():
    citation = parse_citation("3ac9f2b1d0af@a1c2d3e|t:10-40;tok=mistral-v3")

    assert citation.span.unit == "t"
    assert citation.span.tokenizer == "mistral-v3"


def test_parse_token_citation_without_tokenizer_raises():
    with pytest.raises(CitationError):
        parse_citation("3ac9f2b1d0af@a1c2d3e|t:10-40")


def test_parse_rejects_non_hex_cid():
    with pytest.raises(CitationError):
        parse_citation("not-a-hex-cid@a1c2d3e|b:10-20")


def test_parse_rejects_short_cid():
    with pytest.raises(CitationError):
        parse_citation("3ac9@a1c2d3e|b:10-20")


def test_span_end_must_be_greater_than_start():
    with pytest.raises(CitationError):
        CitationSpan(unit="b", start=20, end=20)


def test_tokenizer_only_allowed_for_token_spans():
    with pytest.raises(CitationError):
        CitationSpan(unit="b", start=10, end=20, tokenizer="mistral-v3")


def test_format_citation_round_trips():
    text = format_citation(
        cid="3ac9f2b1d0af",
        version="a1c2d3e",
        unit="b",
        start=1024,
        end=2047,
    )

    assert text == "3ac9f2b1d0af@a1c2d3e|b:1024-2047"
    assert str(parse_citation(text)) == text


def test_citation_stringifies():
    citation = Citation(
        cid="3ac9f2b1d0af",
        version="a1c2d3e",
        span=CitationSpan(unit="c", start=1, end=5),
    )

    assert str(citation) == "3ac9f2b1d0af@a1c2d3e|c:1-5"
