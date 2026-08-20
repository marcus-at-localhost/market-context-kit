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
