#!/usr/bin/env python3
"""
Competitor Scanner — Utility script for Market Context Kit
Scans competitor websites to extract positioning, pricing, features, and trust signals
for competitive analysis.

Behavior is driven by business-type fingerprint packs in references/fingerprints/
(consumer-online, b2b-technical — same ids as references/business-context.md) so a SaaS
pricing page and an industrial RFQ page are scored on their own terms, not one blob of
sign-up/checkout vocabulary. The page's --type is used if given; otherwise the business
type is auto-detected from on-page signals, same as references/business-context.md's
own classification table. Vocabulary is per-language (en/de/es/fr/it/nl), selected by
<html lang>, mirroring analyze_page.py's cta_words_for(lang) union-fallback pattern.
"""

import sys
import json
import re
import urllib.request
import urllib.error
import ssl
import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

try:
    import trafilatura
    HAVE_TRAFILATURA = True
except ImportError:
    trafilatura = None
    HAVE_TRAFILATURA = False


FINGERPRINTS_DIR = Path(__file__).resolve().parent.parent / "references" / "fingerprints"
KNOWN_PACKS = ("consumer-online", "b2b-technical")
LIST_FIELDS = (
    "detection_signals", "cta_words", "pricing_indicator_patterns",
    "testimonial_words", "trust_badge_alt_keywords", "conversion_paths",
)

_LANG_RE = re.compile(r'<html[^>]*\blang=["\']([a-zA-Z-]+)["\']', re.IGNORECASE)


def detect_lang(html):
    """Return the primary language subtag from <html lang="...">, or None."""
    match = _LANG_RE.search(html)
    if not match:
        return None
    return match.group(1).split("-", 1)[0].strip().lower() or None


def load_pack(pack_id):
    """Load one fingerprint pack by id. Raises FileNotFoundError if unknown."""
    path = FINGERPRINTS_DIR / f"{pack_id}.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_all_packs():
    """Load every known fingerprint pack, keyed by id."""
    return {pack_id: load_pack(pack_id) for pack_id in KNOWN_PACKS}


def words_for(pack, field, lang):
    """Return pack[field] for `lang`, or the union of every language when
    `lang` is missing/unknown — missing a signal is worse than a false positive,
    same reasoning as analyze_page.py's cta_words_for()."""
    by_lang = pack[field]
    if lang and lang in by_lang:
        return by_lang[lang]
    merged = []
    for words in by_lang.values():
        merged.extend(words)
    return merged


def detect_business_type(text_lower, packs, lang):
    """Score each pack's detection_signals against `text_lower`, return the
    highest-scoring pack id, or None if there's no signal or a tie."""
    scores = {}
    for pack_id, pack in packs.items():
        signals = words_for(pack, "detection_signals", lang)
        scores[pack_id] = sum(text_lower.count(s) for s in signals)

    best_id = max(scores, key=scores.get)
    best_score = scores[best_id]
    if best_score == 0:
        return None
    if list(scores.values()).count(best_score) > 1:
        return None
    return best_id


def merge_packs(pack_a, pack_b):
    """Union two packs' list fields per language. Used as the fallback ruleset
    when the business type can't be resolved — broader, not narrower, recall."""
    merged = {"id": "unresolved"}
    for field in LIST_FIELDS:
        merged[field] = {}
        langs = set(pack_a.get(field, {})) | set(pack_b.get(field, {}))
        for lang in langs:
            a_words = pack_a.get(field, {}).get(lang, [])
            b_words = pack_b.get(field, {}).get(lang, [])
            seen = []
            for w in a_words + b_words:
                if w not in seen:
                    seen.append(w)
            merged[field][lang] = seen
    return merged


def resolve_rules(pack, lang):
    """Flatten a pack into the language-resolved rules dict CompetitorPageParser
    consumes. Keeps the parser ignorant of packs/languages entirely."""
    return {
        "cta_words": words_for(pack, "cta_words", lang),
        "pricing_patterns": words_for(pack, "pricing_indicator_patterns", lang),
        "testimonial_words": words_for(pack, "testimonial_words", lang),
        "trust_badge_alt_keywords": words_for(pack, "trust_badge_alt_keywords", lang),
    }


def conversion_paths_for(pack, lang):
    """Language-resolved URL-path guesses for the secondary conversion page
    (pricing/plans for consumer-online, RFQ/quote for b2b-technical)."""
    return words_for(pack, "conversion_paths", lang)


def extract_main_text(html, fallback_text):
    """Main-page text for word-count/content signal. Prefers trafilatura's
    boilerplate-stripped extraction when installed; falls back to the parser's
    raw handle_data() join otherwise (identical to the pre-trafilatura script)."""
    if HAVE_TRAFILATURA:
        extracted = trafilatura.extract(html, include_comments=False, include_tables=False)
        if extracted:
            return extracted
    return fallback_text


class CompetitorPageParser(HTMLParser):
    """Parse competitor page for positioning data, scored against a resolved
    rules dict (see resolve_rules()) rather than hardcoded vocabulary."""

    def __init__(self, rules):
        super().__init__()
        self.rules = rules

        self.title = ""
        self.meta_description = ""
        self.og_title = ""
        self.og_description = ""
        self.h1_tags = []
        self.h2_tags = []
        self.pricing_indicators = []
        self.social_links = []
        self.trust_signals = []
        self.ctas = []
        self.testimonial_count = 0
        self.logo_count = 0

        self._in_title = False
        self._in_h1 = False
        self._in_h2 = False
        self._in_a = False
        self._in_button = False
        self._current_text = ""
        self._all_text = []
        self._current_href = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag == "title":
            self._in_title = True
            self._current_text = ""
        elif tag == "meta":
            name = attrs_dict.get("name", "").lower()
            prop = attrs_dict.get("property", "").lower()
            content = attrs_dict.get("content", "")
            if name == "description":
                self.meta_description = content
            elif prop == "og:title":
                self.og_title = content
            elif prop == "og:description":
                self.og_description = content
        elif tag == "h1":
            self._in_h1 = True
            self._current_text = ""
        elif tag == "h2":
            self._in_h2 = True
            self._current_text = ""
        elif tag == "a":
            self._in_a = True
            self._current_text = ""
            self._current_href = attrs_dict.get("href", "")
            social_platforms = {"twitter.com": "Twitter/X", "x.com": "Twitter/X",
                                "facebook.com": "Facebook", "linkedin.com": "LinkedIn",
                                "instagram.com": "Instagram", "youtube.com": "YouTube",
                                "tiktok.com": "TikTok", "github.com": "GitHub"}
            href = attrs_dict.get("href", "")
            for domain, name in social_platforms.items():
                if domain in href:
                    self.social_links.append({"platform": name, "url": href})
        elif tag == "button":
            self._in_button = True
            self._current_text = ""
        elif tag == "img":
            alt = attrs_dict.get("alt", "").lower()
            src = attrs_dict.get("src", "").lower()
            badge_words = self.rules["trust_badge_alt_keywords"]
            if any(word in alt for word in badge_words):
                self.logo_count += 1
            elif any(word in src for word in badge_words):
                self.logo_count += 1

    def handle_endtag(self, tag):
        if tag == "title" and self._in_title:
            self._in_title = False
            self.title = self._current_text.strip()
        elif tag == "h1" and self._in_h1:
            self._in_h1 = False
            text = self._current_text.strip()
            if text:
                self.h1_tags.append(text)
        elif tag == "h2" and self._in_h2:
            self._in_h2 = False
            text = self._current_text.strip()
            if text:
                self.h2_tags.append(text)
        elif tag == "a" and self._in_a:
            self._in_a = False
            text = self._current_text.strip()
            if any(w in text.lower() for w in self.rules["cta_words"]):
                self.ctas.append(text)
        elif tag == "button" and self._in_button:
            self._in_button = False
            text = self._current_text.strip()
            if text:
                self.ctas.append(text)

    def handle_data(self, data):
        if self._in_title or self._in_h1 or self._in_h2 or self._in_a or self._in_button:
            self._current_text += data
        self._all_text.append(data.strip())

        text_lower = data.lower().strip()
        if not text_lower:
            return

        for pattern in self.rules["pricing_patterns"]:
            if re.search(pattern, text_lower):
                self.pricing_indicators.append(data.strip())
                break

        if any(w in text_lower for w in self.rules["testimonial_words"]):
            self.testimonial_count += 1

    def get_raw_text(self):
        return " ".join(self._all_text)

    def get_results(self, main_text=None):
        full_text = main_text if main_text is not None else self.get_raw_text()
        word_count = len(full_text.split())

        return {
            "positioning": {
                "headline": self.h1_tags[0] if self.h1_tags else self.title,
                "tagline": self.meta_description,
                "og_title": self.og_title,
                "og_description": self.og_description,
                "key_sections": self.h2_tags[:10]
            },
            "pricing": {
                "has_pricing_info": len(self.pricing_indicators) > 0,
                "pricing_mentions": list(set(self.pricing_indicators))[:10]
            },
            "trust": {
                "social_platforms": [s["platform"] for s in self.social_links],
                "social_link_count": len(self.social_links),
                "estimated_logo_count": self.logo_count,
                "has_testimonials": self.testimonial_count > 0
            },
            "ctas": list(set(self.ctas))[:10],
            "content": {
                "word_count": word_count,
                "sections": len(self.h2_tags)
            }
        }


def fetch_page(url):
    """Fetch a webpage."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml",
    }

    req = urllib.request.Request(url, headers=headers)
    try:
        response = urllib.request.urlopen(req, timeout=15, context=ctx)
        return response.read().decode("utf-8", errors="replace")
    except Exception:
        return None


def scan_competitor(url, forced_type=None):
    """Scan a competitor website."""
    if not url.startswith("http"):
        url = "https://" + url

    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")

    result = {
        "url": url,
        "domain": domain,
        "status": "success"
    }

    html = fetch_page(url)
    if not html:
        result["status"] = "error"
        result["message"] = "Could not fetch page"
        return result

    lang = detect_lang(html)
    packs = load_all_packs()

    if forced_type:
        if forced_type not in packs:
            result["status"] = "error"
            result["message"] = f"Unknown --type '{forced_type}'. Known: {', '.join(KNOWN_PACKS)}"
            return result
        business_type = forced_type
    else:
        business_type = detect_business_type(html.lower(), packs, lang)

    pack = packs[business_type] if business_type else merge_packs(*packs.values())
    rules = resolve_rules(pack, lang)

    parser = CompetitorPageParser(rules)
    try:
        parser.feed(html)
    except Exception:
        result["status"] = "error"
        result["message"] = "Could not parse page"
        return result

    main_text = extract_main_text(html, parser.get_raw_text())
    result["business_type"] = business_type or "unresolved"
    result["lang"] = lang or "unknown (all languages used)"
    result["data"] = parser.get_results(main_text)

    # Try to fetch the conversion page (pricing for consumer-online, RFQ/quote for b2b-technical)
    conversion_page = {"found": False}
    for path in conversion_paths_for(pack, lang):
        candidate_url = f"https://{parsed.netloc}{path}"
        candidate_html = fetch_page(candidate_url)
        if candidate_html and len(candidate_html) > 1000:
            candidate_parser = CompetitorPageParser(rules)
            try:
                candidate_parser.feed(candidate_html)
                candidate_data = candidate_parser.get_results()
                conversion_page = {
                    "url": candidate_url,
                    "found": True,
                    "pricing_mentions": candidate_data["pricing"]["pricing_mentions"],
                    "sections": candidate_data["positioning"]["key_sections"]
                }
            except Exception:
                pass
            break

    result["conversion_page"] = conversion_page
    return result


def scan_multiple(urls, forced_type=None):
    """Scan multiple competitor URLs."""
    return [scan_competitor(url, forced_type) for url in urls]


def main():
    parser = argparse.ArgumentParser(
        description="Scans competitor websites for positioning, pricing, and trust signals",
        add_help=False,
    )
    parser.add_argument("urls", nargs="*")
    parser.add_argument("--type", dest="business_type", choices=KNOWN_PACKS, default=None,
                        help="Force a business-type fingerprint pack instead of auto-detecting")
    parser.add_argument("-h", "--help", action="store_true", dest="help")
    args = parser.parse_args()

    if args.help or not args.urls:
        print(json.dumps({
            "usage": "python3 competitor_scanner.py [--type consumer-online|b2b-technical] <url1> [url2] ...",
            "example": "python3 competitor_scanner.py calendly.com acuityscheduling.com",
            "example_b2b": "python3 competitor_scanner.py --type b2b-technical idt-dichtungen.de",
            "description": "Scans competitor websites for positioning, pricing, and trust signals. "
                            "Business type is auto-detected from on-page signals unless --type is given."
        }, indent=2))
        return

    if len(args.urls) == 1:
        result = scan_competitor(args.urls[0], args.business_type)
        print(json.dumps(result, indent=2, default=str))
    else:
        results = scan_multiple(args.urls, args.business_type)
        print(json.dumps({"competitors": results}, indent=2, default=str))


if __name__ == "__main__":
    main()
