# Known WebFetch Artifacts

`WebFetch` converts a page to markdown and has a small model answer a prompt against that
conversion. It is fine for reading body copy, tone, and claims. It is not a DOM parser, and it
regularly promotes non-structural elements into what reads like page structure. Nothing below
should reach a subagent prompt or a report as a structural fact unless confirmed against raw HTML
(`analyze_page.py` or a direct fetch).

## The list

- **SVG `<title>` / `aria-labelledby` text → fake H1.** An inline `<svg role="img"
  aria-labelledby="logo-title"><title id="logo-title">…</title></svg>` sits at the top of the DOM
  (often the logo) and markdown converters routinely promote it to a top-level heading. This is
  what produced the 2026-08-15 false finding on idt-dichtungen.de: "IDT – The Sealing Technology
  Specialist" is the logo's accessible name, reported by three subagents as an identical H1 across
  459 pages. Verified per-page H1s were unique and page-specific.
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

See `skills/audit/SKILL.md` Phase 1.4 (Provenance Rule) and Phase 2.5 (Verification Before
Synthesis) for where this applies in the audit flow.
