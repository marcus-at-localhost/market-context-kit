"""Tests for scripts/competitor_scanner.py — pure logic only, no network calls."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import competitor_scanner as cs


# ---------------------------------------------------------------------------
# detect_lang
# ---------------------------------------------------------------------------

def test_detect_lang_reads_html_lang_attribute():
    html = '<html lang="de-DE"><head></head><body></body></html>'
    assert cs.detect_lang(html) == "de"


def test_detect_lang_returns_none_when_missing():
    html = "<html><head></head><body></body></html>"
    assert cs.detect_lang(html) is None


# ---------------------------------------------------------------------------
# load_pack / load_all_packs
# ---------------------------------------------------------------------------

def test_load_pack_loads_b2b_technical():
    pack = cs.load_pack("b2b-technical")
    assert pack["id"] == "b2b-technical"
    assert "en" in pack["cta_words"]


def test_load_pack_unknown_id_raises():
    try:
        cs.load_pack("does-not-exist")
        assert False, "expected FileNotFoundError"
    except FileNotFoundError:
        pass


def test_load_all_packs_returns_both_known_packs():
    packs = cs.load_all_packs()
    assert set(packs.keys()) == {"consumer-online", "b2b-technical"}


# ---------------------------------------------------------------------------
# words_for
# ---------------------------------------------------------------------------

def test_words_for_returns_language_specific_list():
    pack = cs.load_pack("b2b-technical")
    words = cs.words_for(pack, "cta_words", "de")
    assert "angebot anfordern" in words
    assert "request a quote" not in words


def test_words_for_unions_all_languages_when_lang_unknown():
    pack = cs.load_pack("b2b-technical")
    words = cs.words_for(pack, "cta_words", None)
    assert "angebot anfordern" in words
    assert "request a quote" in words


def test_words_for_unknown_language_falls_back_to_union():
    pack = cs.load_pack("b2b-technical")
    words = cs.words_for(pack, "cta_words", "ja")
    assert "request a quote" in words
    assert "angebot anfordern" in words


# ---------------------------------------------------------------------------
# detect_business_type
# ---------------------------------------------------------------------------

def test_detect_business_type_picks_b2b_technical_from_rfq_signals():
    packs = cs.load_all_packs()
    text = "download the datasheet and request a quote, iso 9001 certified distributor"
    result = cs.detect_business_type(text.lower(), packs, "en")
    assert result == "b2b-technical"


def test_detect_business_type_picks_consumer_online_from_pricing_signals():
    packs = cs.load_all_packs()
    text = "start your free trial today, $29/month, add to cart and checkout"
    result = cs.detect_business_type(text.lower(), packs, "en")
    assert result == "consumer-online"


def test_detect_business_type_returns_none_when_no_signals_match():
    packs = cs.load_all_packs()
    text = "welcome to our website, here is a paragraph about the weather"
    result = cs.detect_business_type(text.lower(), packs, "en")
    assert result is None


# ---------------------------------------------------------------------------
# merge_packs (fallback pack when type unresolved)
# ---------------------------------------------------------------------------

def test_merge_packs_unions_list_fields_per_language():
    packs = cs.load_all_packs()
    merged = cs.merge_packs(packs["consumer-online"], packs["b2b-technical"])
    en_cta = merged["cta_words"]["en"]
    assert "sign up" in en_cta
    assert "request a quote" in en_cta


# ---------------------------------------------------------------------------
# resolve_rules (flat rules dict handed to the parser)
# ---------------------------------------------------------------------------

def test_resolve_rules_returns_flat_lists_for_language():
    pack = cs.load_pack("b2b-technical")
    rules = cs.resolve_rules(pack, "de")
    assert "angebot anfordern" in rules["cta_words"]
    assert "auf anfrage" in rules["pricing_patterns"]
    assert "referenzprojekt" in rules["testimonial_words"]
    assert "zertifiziert" in rules["trust_badge_alt_keywords"]


# ---------------------------------------------------------------------------
# conversion_paths_for
# ---------------------------------------------------------------------------

def test_conversion_paths_for_b2b_german():
    pack = cs.load_pack("b2b-technical")
    paths = cs.conversion_paths_for(pack, "de")
    assert "/anfrage" in paths
    assert "/pricing" not in paths


# ---------------------------------------------------------------------------
# CompetitorPageParser driven by resolved rules
# ---------------------------------------------------------------------------

def _rules(cta_words=None, pricing_patterns=None, testimonial_words=None, trust_badge_alt_keywords=None):
    return {
        "cta_words": cta_words or [],
        "pricing_patterns": pricing_patterns or [],
        "testimonial_words": testimonial_words or [],
        "trust_badge_alt_keywords": trust_badge_alt_keywords or [],
    }


def test_parser_captures_cta_matching_rules():
    html = '<a href="/quote">Request a Quote</a>'
    parser = cs.CompetitorPageParser(_rules(cta_words=["request a quote"]))
    parser.feed(html)
    results = parser.get_results()
    assert "Request a Quote" in results["ctas"]


def test_parser_ignores_cta_not_in_rules():
    html = '<a href="/cart">Add to Cart</a>'
    parser = cs.CompetitorPageParser(_rules(cta_words=["request a quote"]))
    parser.feed(html)
    results = parser.get_results()
    assert results["ctas"] == []


def test_parser_detects_pricing_indicator_from_rules():
    html = "<p>Contact us for an RFQ today</p>"
    parser = cs.CompetitorPageParser(_rules(pricing_patterns=[r"\brfq\b"]))
    parser.feed(html)
    results = parser.get_results()
    assert results["pricing"]["has_pricing_info"] is True


def test_parser_trust_badge_alt_keyword_counts_as_logo():
    html = '<img src="/badge.png" alt="ISO 9001 Certified">'
    parser = cs.CompetitorPageParser(_rules(trust_badge_alt_keywords=["iso"]))
    parser.feed(html)
    results = parser.get_results()
    assert results["trust"]["estimated_logo_count"] == 1


def test_parser_trust_badge_alt_keyword_not_in_rules_is_not_counted():
    html = '<img src="/badge.png" alt="ISO 9001 Certified">'
    parser = cs.CompetitorPageParser(_rules(trust_badge_alt_keywords=["kunde"]))
    parser.feed(html)
    results = parser.get_results()
    assert results["trust"]["estimated_logo_count"] == 0


def test_parser_detects_testimonial_word_from_rules():
    html = "<p>Read our reference installation story</p>"
    parser = cs.CompetitorPageParser(_rules(testimonial_words=["reference installation"]))
    parser.feed(html)
    results = parser.get_results()
    assert results["trust"]["has_testimonials"] is True


# ---------------------------------------------------------------------------
# extract_main_text (trafilatura optional)
# ---------------------------------------------------------------------------

def test_extract_main_text_falls_back_without_trafilatura(monkeypatch):
    monkeypatch.setattr(cs, "HAVE_TRAFILATURA", False)
    text = cs.extract_main_text("<html><body><p>Hello world</p></body></html>", "Hello world nav footer")
    assert text == "Hello world nav footer"


def test_extract_main_text_uses_trafilatura_when_available(monkeypatch):
    monkeypatch.setattr(cs, "HAVE_TRAFILATURA", True)

    class FakeTrafilatura:
        @staticmethod
        def extract(html, **kwargs):
            return "Clean main content only"

    monkeypatch.setattr(cs, "trafilatura", FakeTrafilatura)
    text = cs.extract_main_text("<html>...</html>", "Hello world nav footer")
    assert text == "Clean main content only"


def test_extract_main_text_falls_back_when_trafilatura_returns_none(monkeypatch):
    monkeypatch.setattr(cs, "HAVE_TRAFILATURA", True)

    class FakeTrafilatura:
        @staticmethod
        def extract(html, **kwargs):
            return None

    monkeypatch.setattr(cs, "trafilatura", FakeTrafilatura)
    text = cs.extract_main_text("<html>...</html>", "fallback text")
    assert text == "fallback text"
