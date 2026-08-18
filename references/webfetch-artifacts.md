# Known Page-Extraction Artifacts

Covers both ways page text reaches a report: `WebFetch` (markdown conversion plus a small model)
and any hand-run extraction of fetched HTML.

`WebFetch` is fine for reading body copy, tone, and claims. It is not a DOM parser, and it
regularly promotes non-structural elements into what reads like page structure. Nothing below
should reach a subagent prompt or a report as a structural fact unless confirmed against raw HTML
(`analyze_page.py` or a direct fetch).

## Never hand-roll HTML extraction

Do not write an ad-hoc regex HTML-to-text script to pull page copy. Regex cannot model nesting,
comments, CDATA, or unclosed tags, and its failures are silent — the output looks like clean prose
whether or not the text was ever rendered.

Use in this order:

1. **`scripts/analyze_page.py`** — the bundled extractor. Built on `html.parser.HTMLParser`, so
   comments route to `handle_comment` and never enter the text stream.
2. **A real parser** (`html.parser`, `lxml`, BeautifulSoup) when the bundled script does not
   expose the field you need.
3. **`WebFetch`** for prose and tone, subject to the artifact list below.

Anything quoted as on-page evidence must be text a visitor actually sees. If an extraction step
cannot distinguish rendered text from source text, it is not evidence.

## The list

- **SVG `<title>` / `aria-labelledby` text → fake H1.** An inline `<svg role="img"
  aria-labelledby="logo-title"><title id="logo-title">…</title></svg>` sits at the top of the DOM
  (often the logo) and markdown converters routinely promote it to a top-level heading. This is
  what produced a 2026-08-15 false finding: a company's own name, sitting in the header logo as
  its accessible name, was reported by three subagents as an identical H1 across all 459 pages of
  a site. Verified per-page H1s were unique and page-specific.
- **HTML comments → fake live content.** Markup inside `<!-- … -->` is in the source but never
  rendered. A regex that strips `<[^>]+>` cannot close a comment that contains tags, so the
  commented markup survives as ordinary-looking prose and only a stray `-->` hints at it. A
  2026-08-18 brand-voice run hit exactly this: a homepage hero carried four campaign CTAs with
  three commented out, and a disabled seasonal CTA from a prior year was reported as a stale live
  element — an 18-month-old greeting still on the front page. It had not been visible to anyone.
  Deactivated campaign blocks, seasonal banners, and A/B variants are the usual residents of this
  space, which is exactly the material that reads as a damning staleness finding.
- **`aria-label` text → fake visible label.** Accessible-name text on a button or link can surface
  in the markdown as if it were displayed copy, when the visible label is different or absent.
- **`<figcaption>` → fake heading or body claim.** Caption text under an image can read as a
  standalone assertion in the markdown, disconnected from the image it describes.
- **Visually-hidden text → fake content.** `sr-only`, `visually-hidden`, `clip`-based CSS patterns
  keep text present in the DOM for screen readers while invisible on screen. Markdown conversion
  has no concept of "hidden" and includes it as if it were on-page content.
- **Repeated boilerplate → false page-uniqueness or false page-sameness.** Nav and footer markup
  appears identically on every page. A model reading one page's markdown in isolation can mistake
  boilerplate for that page's unique content — or, symmetrically, mistake several pages'
  boilerplate-heavy markdown for evidence the pages are near-duplicates.
- **JSON-LD → leaks as prose.** Structured data in `<script type="application/ld+json">` is not
  meant for display, but markdown conversion has no reason to suppress it; its field values can
  appear as ordinary sentences in the converted text.

## Rule of thumb

If a WebFetch-derived claim is about **what the page says** (a headline, a claim, a value
proposition), it's usable — quote it, but still sanity-check against the live page if a finding
built on it will be rated Critical or High. If the claim is about **the page's structure** (H1,
heading hierarchy, meta tags, canonical, schema, gating/auth, form field markup), it is not usable
on its own. Confirm it against raw HTML first.

A third case sits between them: a claim about **what the page does not say, or no longer says** —
stale content, a missing CTA, a removed section, an outdated banner. These are absence and
currency claims, and both known false findings on this suite were of that kind. Before writing
one, open the raw HTML at the quoted string and confirm it is neither commented out nor
visually hidden. State the line number in the working notes.

## Before a finding ships

For any finding that quotes page text as evidence of a defect:

- [ ] The quote came from `analyze_page.py`, a real parser, or a verified raw-HTML read — not
      from an ad-hoc regex script.
- [ ] The string was located in the raw HTML and is outside `<!-- -->`, `sr-only`/hidden CSS,
      JSON-LD, and `aria-*` attributes.
- [ ] Structural claims (H1, meta, canonical, schema) were confirmed against raw HTML.
- [ ] Staleness and absence claims name the source line that proves it.

See `skills/audit/SKILL.md` Phase 1.4 (Provenance Rule) and Phase 2.5 (Verification Before
Synthesis) for where this applies in the audit flow.
