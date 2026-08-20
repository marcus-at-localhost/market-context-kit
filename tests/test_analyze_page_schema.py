"""Schema extraction must surface nested entities.

schema_types lists top-level nodes only. An Article's author, an Organization's
subOrganization list and a FAQPage's questions all sit one level down, and the
schema scoring in agents/market-technical.md needs them to tell a
rich-result-eligible type that is present from one that is absent.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from analyze_page import MarketingPageParser  # noqa: E402


PAGE = """
<html><head><title>t</title>
<script type="application/ld+json">
[
  {"@type": "Article",
   "author": {"@type": "Person", "name": "A. Person"},
   "publisher": {"@type": "Organization", "name": "Pub"}},
  {"@type": "FAQPage",
   "mainEntity": [
     {"@type": "Question", "acceptedAnswer": {"@type": "Answer"}},
     {"@type": "Question", "acceptedAnswer": {"@type": "Answer"}}
   ]},
  {"@type": "Organization",
   "subOrganization": [
     {"@type": "LocalBusiness", "address": {"@type": "PostalAddress"}},
     {"@type": "LocalBusiness", "address": {"@type": "PostalAddress"}}
   ]}
]
</script>
</head><body><h1>h</h1></body></html>
"""


def parse(html):
    parser = MarketingPageParser()
    parser.feed(html)
    return parser


def test_top_level_types_stay_top_level():
    technical = parse(PAGE).get_results()["technical"]
    assert technical["schema_types"] == ["Article", "FAQPage", "Organization"]
    assert technical["schema_count"] == 3


def test_nested_entities_are_reported_with_counts():
    nested = parse(PAGE).get_results()["technical"]["schema_types_nested"]
    assert nested["Person"] == 1
    assert nested["LocalBusiness"] == 2
    assert nested["PostalAddress"] == 2
    assert nested["Question"] == 2
    assert nested["Answer"] == 2


def test_a_type_is_not_counted_as_nested_when_it_is_top_level():
    """Organization appears once at top level and once as a publisher.
    Only the publisher occurrence is nested."""
    nested = parse(PAGE).get_results()["technical"]["schema_types_nested"]
    assert nested["Organization"] == 1


def test_no_schema_yields_empty_structures():
    technical = parse("<html><body><p>none</p></body></html>").get_results()["technical"]
    assert technical["schema_types"] == []
    assert technical["schema_types_nested"] == {}


LD = '<script type="application/ld+json">%s</script>'


def wrap(head):
    return f"<html><head><title>t</title>{head}</head><body><h1>h</h1></body></html>"


def technical(head):
    return parse(wrap(head)).get_results()["technical"]


def test_a_type_list_becomes_separate_names():
    """A joined "Product, Offer" string matches neither name on an equality
    check, and contradicts how nested types are counted."""
    assert technical(LD % '{"@type":["Product","Offer"]}')["schema_types"] == ["Product", "Offer"]


def test_invalid_json_is_reported_not_swallowed():
    """A dropped block reads downstream as "no schema", which is a different
    finding with a different fix than "schema present but invalid"."""
    tech = technical(LD % '{"@type":"Organization",}')
    assert tech["schema_types"] == []
    assert len(tech["schema_parse_errors"]) == 1


def test_a_broken_block_does_not_hide_a_valid_one():
    tech = technical((LD % '{"@type":"Organization",}') + (LD % '{"@type":"WebSite"}'))
    assert tech["schema_types"] == ["WebSite"]
    assert len(tech["schema_parse_errors"]) == 1


def test_microdata_itemtype_is_collected():
    head = ('<div itemscope itemtype="https://schema.org/Product">'
            '<span itemscope itemtype="http://schema.org/Offer"></span></div>'
            '<div itemscope itemtype="https://schema.org/Product"></div>')
    assert technical(head)["schema_types_microdata"] == {"Offer": 1, "Product": 2}


def test_rdfa_typeof_is_collected_with_and_without_prefix():
    assert technical('<div typeof="Product"></div>')["schema_types_microdata"] == {"Product": 1}
    assert technical('<div typeof="schema:LocalBusiness"></div>')["schema_types_microdata"] == {"LocalBusiness": 1}


def test_a_foreign_vocabulary_stays_out_of_the_inventory():
    head = '<div itemscope itemtype="https://example.org/dc/terms/title"></div>'
    assert technical(head)["schema_types_microdata"] == {}


def test_json_ld_forms_are_equivalent():
    """One array blob, one @graph, and separate script blocks must all report
    the same types."""
    blob = LD % '[{"@type":"Organization"},{"@type":"WebSite"}]'
    graph = LD % '{"@context":"https://schema.org","@graph":[{"@type":"Organization"},{"@type":"WebSite"}]}'
    split = (LD % '{"@type":"Organization"}') + (LD % '{"@type":"WebSite"}')
    expected = ["Organization", "WebSite"]
    for head in (blob, graph, split):
        assert technical(head)["schema_types"] == expected
