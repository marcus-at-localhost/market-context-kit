---
name: audit
description: Use when the user asks for a full marketing audit, a marketing score, or a client-ready assessment of a whole website covering content, conversion, SEO, competition, brand, and growth at once.
argument-hint: <url>
allowed-tools: Bash(python "${CLAUDE_PLUGIN_ROOT}/scripts/"*), Bash(python3 "${CLAUDE_PLUGIN_ROOT}/scripts/"*), Bash(curl -s *)
metadata:
  version: 3.2.0
---

# Marketing Audit Orchestrator

You are the full marketing audit engine for `/marketkit:audit <url>`. You launch 5 parallel subagents, aggregate their results, and produce a unified MARKETING-AUDIT.md report that is client-ready and revenue-focused.

## When This Skill Is Invoked

The user runs `/marketkit:audit <url>`. This is the flagship command of the entire suite. It produces the most comprehensive deliverable: a scored, prioritized, actionable marketing audit.

---

## Phase 0: Grounding

Read `${CLAUDE_PLUGIN_ROOT}/references/grounding.md` and load any `_grounding/` folder it finds. If one exists, build a **grounding digest** now — the list of loaded files plus a condensed extract covering positioning, target industries and buyers, competitors, claim rules and tone. You will paste that digest into all five subagent prompts in Phase 2; they share none of your context and cannot rediscover it.

Then read `${CLAUDE_PLUGIN_ROOT}/references/business-context.md`. The classification in Phase 1.2 below feeds the same pack-selection logic, and grounding overrides it where the two disagree.

Also read `${CLAUDE_PLUGIN_ROOT}/references/output-location.md`. Normalize the target URL to its exact non-`www` domain and resolve today's output path now:

```
python "${CLAUDE_PLUGIN_ROOT}/scripts/resolve_audit_output.py" --purpose MARKETING-AUDIT --scope <domain> --extension md
```

Use `python3` on macOS/Linux. Retain the JSON's `output_path` (the exact `MARKETKIT - MARKETING-AUDIT - <domain>.md` path) and `audit_dir` — Phase 3 writes there, not into the bare working directory, and Cross-Skill Integration uses `audit_dir` to find same-scope sibling reports.

Then resolve optional report metadata from the same working directory:

```
python "${CLAUDE_PLUGIN_ROOT}/scripts/resolve_report_metadata.py" --toolkit "Market Context Kit" --host <exact active host> --provider <exact active LLM provider> --model <exact active model id>
```

Never guess a runtime value. Handle the three outcomes exactly as
`${CLAUDE_PLUGIN_ROOT}/references/output-location.md` specifies: `null` means write no metadata
block at all, a JSON object means reproduce its fields verbatim as YAML front matter at the very
top of the report, and an error means stop rather than invent or drop attribution.

Read `${CLAUDE_PLUGIN_ROOT}/references/search-context-integration.md`. Resolve and validate a `SEARCH-CONTEXT.v1.json` artifact only when the user supplies an explicit path, or the reference's discovery rule finds exactly one in the active audit folder's flat `data/` for the exact domain and, if requested, the exact reporting period. Retain a valid artifact as **orchestrator-only** evidence for Phase 3; do not use it during discovery or scoring.

Read `${CLAUDE_PLUGIN_ROOT}/references/google-search-guidance.md`. Its `Myth Guardrail` binds every
recommendation this command emits, `Grounding Precedence` governs what happens when a grounding
criterion asks for a myth check anyway, and `Schema Scoring` sets how structured data is scored. You
paste the guardrail into two subagent prompts in Phase 2 and apply the whole file yourself in Phase 3.

### 0.1 Build the Data Manifest

The five subagents have no file-discovery tools and are instructed to open nothing you have not named. Decide now what that list is: the **Data Manifest** is the complete set of file paths any subagent may `Read` on this run, and you paste it verbatim into all five prompts.

Default it to empty. The grounding digest, the page map, and the Structural Facts block all travel inline in the prompt, so in the ordinary case no subagent needs to open a file at all. Add a path only when a subagent genuinely needs the full text of something the digest cannot carry — typically a long `_grounding/` source — and then only to the prompts that need it.

Never on the manifest, whatever else is in the workspace:

| Excluded | Why |
|---|---|
| Any `MARKETKIT - MARKETING-AUDIT - *.md`, in any folder, from any run | Score anchoring. A subagent that sees a previous score calibrates to it instead of scoring the site, and the five dimensions stop being independent. Run-over-run comparison is yours to do in Phase 3. Do not quote a prior score into a subagent prompt either — not as context, not as an example. |
| Analytics, traffic, and performance exports (`*Analytics*`, GA4/Matomo/GSC dumps, KPI sheets) | Cross-client contamination. In a multi-client workspace a subagent cannot tell whose figures these are, and a foreign number reaches the report looking like a measurement of this client. |
| `SEARCH-CONTEXT.v1.json` and its raw provider files | Orchestrator-only evidence. It never goes on the Data Manifest, even after exact-domain validation. |
| Any other client's folder or deliverable | Same. |
| `COMPETITOR-REPORT.md`, `BRAND-VOICE.md`, and other sibling-skill output | Orchestrator-only inputs — see Cross-Skill Integration. Feeding them to a subagent pre-loads its conclusions. |

If the manifest is empty, write that into the prompt explicitly:

```
## Data Manifest
Empty. You may not open any file on this run. Everything you need is in this prompt.
```

Do not simply leave the section out. An absent manifest reads to a subagent as an absent constraint, which is the failure this exists to prevent.

Two facts about this run that make the rule concrete, and that you should state in the prompt when they apply: the workspace holds more than one client, and it holds output from previous audits of this same client. Both are normal. Neither is available to the subagents.

---

## Phase 1: Discovery (Pre-Analysis)

Before launching subagents, perform these discovery steps:

### 1.1 Fetch the Target URL

Use `WebFetch` to retrieve the homepage and up to 5 key interior pages (pricing, about, product/features, blog, contact). Store raw content for subagent consumption. WebFetch output is a small model's summary of a markdown conversion, not a measurement — see the Provenance Rule (1.4) before this content goes anywhere near a subagent prompt.

Then build the **Structural Facts** block: run the bundled page analyzer against the same set of pages — homepage plus the up to 5 interior pages fetched via WebFetch above. This is raw HTML parsing, not a WebFetch summary — it is the only source subagents may cite for H1, heading hierarchy, title, meta description, canonical, and schema type claims.

```bash
# macOS / Linux
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/analyze_page.py" "<url>"
# Windows
python "${CLAUDE_PLUGIN_ROOT}/scripts/analyze_page.py" "<url>"
```

Run it once per selected URL (homepage + up to 5 interior). Use `python3` on macOS and Linux, `python` on Windows. Do not try `python3` first on Windows: it resolves to the Microsoft Store alias stub, which opens the Store instead of failing cleanly. If the script errors on a given URL, continue without that page and note the gap — do not fall back to a WebFetch read for the same page and pass that off as structural fact.

Assemble the results into a table, one row per URL analyzed. `Schema types` comes from `analysis.technical.schema_types` in the JSON — top-level nodes only. Entities one level down live in `analysis.technical.schema_types_nested`, a `{type: count}` map covering an `Article`'s `author` Person, an `Organization`'s `subOrganization` LocalBusiness entries, a `FAQPage`'s questions. Read both before calling a schema type absent; the counts include `@id` references, so a type may be counted more often than it is defined.

```markdown
### Structural Facts (raw HTML, not WebFetch — analyze_page.py)
| URL | H1 (count) | H1 text | Title | Canonical | Schema types | Heading issues |
|---|---|---|---|---|---|---|
| / | 1 | "…" | "…" | https://…/ | Organization, WebSite | — |
| /produkte/… | 1 | "…" | "…" | https://…/ | Product | — |
```

### 1.2 Detect Business Type

Classify the business into one of these categories. This classification shapes every subagent's analysis focus:

| Business Type | Detection Signals | Analysis Focus |
|---------------|-------------------|----------------|
| **SaaS/Software** | Free trial CTA, pricing tiers, feature pages, "login" link, API docs | Trial-to-paid conversion, onboarding, feature differentiation, churn signals |
| **E-commerce** | Product listings, cart, checkout, product categories, reviews | Product pages, cart abandonment, upsells, reviews, AOV optimization |
| **Agency/Services** | Case studies, portfolio, "work with us", testimonials, contact forms | Trust signals, case studies, positioning, lead qualification |
| **Local Business** | Address, phone number, hours, "near me", Google Maps embed | Local SEO, Google Business Profile, reviews, NAP consistency |
| **Creator/Course** | Lead magnets, email capture, course listings, community links | Email capture rate, funnel design, testimonials, content quality |
| **Marketplace** | Two-sided messaging, buyer/seller flows, listing pages | Supply/demand balance, trust mechanisms, network effects |
| **B2B Industrial Manufacturer** | Product categories, datasheets, certifications, RFQ/contact CTAs, industry solution pages | RFQ paths, technical proof, compliance trust, product/category clarity, inquiry conversion |
| **Technical Supplier/Distributor** | Catalog search, stock/availability claims, part numbers, downloads, customer portal | Product findability, repeat-order paths, quote requests, cross-reference tools, delivery confidence |
| **Regulated/Compliance-Driven Business** | Standards, audits, certifications, safety/compliance language, regulated industries | Audit readiness, risk reduction, proof above the fold, schema, expert credibility |
| **Training/Academy** | Course pages, schedules, instructor bios, certifications, enrollment CTAs | Course clarity, certification outcomes, enrollment friction, Course schema, post-training nurture |
| **Knowledge-Led B2B Brand** | White papers, webinars, newsletter, podcast, content hub, expert authors | Authority building, gated assets, expert attribution, nurture flows, sales enablement |

If multiple contexts apply, combine them instead of forcing one category. A manufacturer that is also a distributor, runs a training academy and publishes technical guides is all four at once, and an audit that picks one label will miss three quarters of the conversion paths.

### 1.3 Identify Key Pages

Map the site architecture to identify:
- Homepage
- Primary landing pages
- Pricing page (if exists)
- RFQ, inquiry, contact, quote, or consultation page
- Product/feature pages
- Product category, catalog, datasheet, downloads, certification, or portal pages
- Industry solution, use-case, service, course, event, or training pages
- About/team page
- Blog/content hub
- Contact/signup/trial/RFQ/enrollment page
- Legal pages (privacy, terms)

Store this page map for all subagents to reference.

### 1.4 Provenance Rule

`WebFetch` output is a small model's summary of a markdown conversion of the page — not a measurement. Markdown converters routinely promote an SVG `<title>`, an `aria-label`, a `<figcaption>`, or visually-hidden text into what reads as a top-level heading or a structural element that isn't one. See `${CLAUDE_PLUGIN_ROOT}/references/webfetch-artifacts.md` for the known list before treating any WebFetch-derived structural claim as fact.

Anything you (the orchestrator) carry from a WebFetch read into a subagent prompt — as opposed to a direct quote of body copy — must be either:
- confirmed against the Structural Facts block (1.1) or a raw fetch (`curl`), or
- explicitly tagged `[unverified: WebFetch]` in the prompt, so the subagent knows not to treat it as ground truth.

This applies to your own prose, too: do not write "downloads appear to be gated" or similar observational claims into a subagent prompt as if established. Either verify it (`curl -sI <asset-url>` — status code, content-type, no auth redirect) or tag it unverified and let the subagent investigate.

### 1.5 Sample Scope Rule

This one is about how far a measurement generalizes across the site. It is unrelated to the Data Manifest in 0.1, which governs which files a subagent may open.

`analyze_page.py` results — from Phase 1.1 and any Phase 2.5 re-run — describe only the URL(s) actually analyzed. When citing them in a subagent prompt, say "homepage only" or "sampled N pages (list)," never "sitewide" or "across the site." A finding true of one page is not evidence about the other 458.

---

## Phase 2: Analysis (Parallel Subagent Execution)

Issue **five `Agent` tool calls in a single message** — that is what makes them run in parallel. Five separate messages run them one after another and waste most of the benefit.

| # | `subagent_type` | Produces |
|---|---|---|
| 1 | `marketkit:market-content` | Content & Messaging |
| 2 | `marketkit:market-conversion` | Conversion Optimization |
| 3 | `marketkit:market-competitive` | Competitive Positioning |
| 4 | `marketkit:market-technical` | SEO & Discoverability |
| 5 | `marketkit:market-strategy` | Brand & Trust, Growth & Strategy |

If a `subagent_type` is rejected as unknown, the plugin has not reloaded since the agent files changed — tell the user to run `/reload-plugins` or restart, then retry. Do not silently fall back to analyzing everything yourself.

Subagents share none of your conversation. Every prompt must therefore carry, in full:

- the target URL
- the detected business type (including combined contexts)
- the page map from Phase 1.3
- **the grounding digest from Phase 0** — loaded file names plus the condensed extract. Omitting it is the single most common failure of this command: the orchestrator knows the client and the five subagents do not, so they analyze against generic defaults and the merged report contradicts itself. If no grounding folder was found, say that explicitly in the prompt rather than leaving it out.
- **the Structural Facts block from 1.1**, in every one of the five prompts, with this instruction attached: "Any H1, heading hierarchy, meta tag, canonical, or schema claim in your output must come from this table. Do not derive it from your own WebFetch read — WebFetch reliably misreads SVG titles, aria-labels and hidden text as page structure. If a page you need isn't in this table, say so as a gap rather than asserting structure for it." This is the fix for a 2026-08-15 run in which three of five subagents reported a WebFetch-sourced SVG logo title as an identical H1 across all 459 pages of a site.
- **the Data Manifest from 0.1**, verbatim, in every one of the five prompts — including the `Empty.` form. This is the fix for the second half of that same run, in which `market-conversion` located an unrelated analytics file and a previous audit report on its own and calibrated its score against them.
- for `market-technical` only: the full `analyze_page.py` JSON from Phase 1.1 (not just the Structural Facts table — technical gets the whole payload)
- **the `Myth Guardrail` table from `${CLAUDE_PLUGIN_ROOT}/references/google-search-guidance.md`**, pasted verbatim under a `## Myth Guardrail` heading, in the `market-technical` and `market-content` prompts **only** — the other three never recommend schema or `llms.txt`, so paying those tokens five times buys nothing. Attach this sentence to the block: "These bind your recommendations. If the grounding digest asks for one of these checks anyway, run it and report the fact — never as a scored gap or a severity-rated issue."

Close every prompt with the return contract, so the declaration comes back in a form you can reconcile:

```
End your output with these two sections, even if both are empty:

### Files Read
- [every path you opened, or: none]

### Out-of-Scope Material Noticed
- [path or description, plus why it looked relevant, or: none]
```

### Subagent 1: market-content

**Focus:** Content quality, messaging clarity, copy effectiveness

Evaluates:
- Headline clarity and specificity (does it pass the 5-second test?)
- Value proposition strength (is the unique value immediately obvious?)
- Body copy persuasion (does it speak to pain points and desired outcomes?)
- Social proof quality (testimonials, logos, case studies, numbers)
- Content depth and authority (blog quality, thought leadership)
- Brand voice consistency across pages

**Scores:** Content & Messaging (0-100)

### Subagent 2: market-conversion

**Focus:** CRO, funnels, landing pages, signup flows

Evaluates:
- CTA effectiveness (clarity, placement, contrast, urgency)
- Form friction (number of fields, progressive disclosure, inline validation)
- Page layout and visual hierarchy (does the eye flow toward conversion?)
- Trust signals near conversion points (guarantees, security badges, testimonials)
- Mobile conversion experience
- Signup/checkout/RFQ/inquiry/enrollment flow steps and drop-off risk
- Commercial action page effectiveness (pricing, RFQ, inquiry, catalog, datasheet, demo, or course enrollment)

**Scores:** Conversion Optimization (0-100)

### Subagent 3: market-competitive

**Focus:** Competitive positioning, market landscape

Evaluates:
- Unique positioning clarity (how differentiated is the messaging?)
- Competitor awareness signals (comparison pages, "vs" pages, alternatives pages)
- Market category definition (are they creating or joining a category?)
- Commercial model relative to likely competitors (pricing, RFQ, distributor, self-serve, sales-led, partner-led)
- Feature differentiation signals
- Review/reputation presence on third-party sites

**Scores:** Competitive Positioning (0-100)

### Subagent 4: market-technical

**Focus:** Technical SEO, site architecture, page speed

Evaluates:
- Title tags, meta descriptions, header hierarchy
- URL structure and internal linking
- Image optimization (alt tags, file sizes, modern formats)
- Mobile responsiveness
- Page load speed indicators (DOM size, resource count, render-blocking)
- Schema markup / structured data — scored per `Schema Scoring` in `references/google-search-guidance.md`: rich-result-eligible types that are present, valid, and matching visible page content, not coverage of a type checklist
- Sitemap and robots.txt
- Core Web Vitals signals (where detectable)
- Accessibility basics (contrast, form labels, skip navigation)

**Scores:** SEO & Discoverability (0-100)

### Subagent 5: market-strategy

**Focus:** Overall strategy, commercial model, growth opportunities

Evaluates:
- Business model clarity
- Pricing/commercial strategy (public pricing, RFQ, sales-led, distributor-led, subscription, usage, course fee, donation, or hybrid)
- Growth loops (referral, viral, content, sales-led)
- Retention signals (loyalty programs, community, email nurture)
- Expansion revenue opportunities (upsells, cross-sells, tiers)
- Market timing and trends alignment
- Brand trust signals (about page, team, mission, social proof depth)

**Scores:** Brand & Trust (0-100), Growth & Strategy (0-100)

---

## Phase 2.4: Manifest Reconciliation

Run this before Phase 2.5 and before anything is merged. Verifying a finding that came from the wrong client's file is wasted work; scope comes first.

Each subagent ends its output with `### Files Read`. For each of the five:

1. **Compare every declared path against the Data Manifest from 0.1.** Exact paths, not "looks similar."
2. **Any path not on the manifest → do not merge that subagent's findings.** Not the offending finding — the whole dimension. You cannot tell which conclusions the out-of-scope file shaped, and a subagent that read last month's report may have anchored its score without ever mentioning the number.
3. **A missing `### Files Read` block counts as a violation.** Do not read it as "read nothing."
4. **Remedy, in order of preference:** rerun that one subagent with the manifest restated and the violation named. If a rerun isn't possible, mark the dimension `not scored — scope violation` in the report, state which file was read, and compute the composite over the remaining dimensions with their weights renormalized to 100%. Say in the report that you did this. Never carry a contaminated dimension forward silently, and never substitute your own estimate for its score.
5. **`Out-of-Scope Material Noticed` is a note to you, not evidence.** Read it to decide whether that path belongs on a future run's manifest. Do not forward it to a subagent mid-run, and do not treat the subagent's guess about its contents as a finding.

The declaration is a self-report, not an enforced boundary — it catches the honest case, which is the common one. Treat a clean declaration as the expected result, not as proof, and keep the manifest itself narrow.

---

## Phase 2.5: Verification Before Synthesis

Before any finding reaches the report, check whether it needs raw re-verification. A finding **requires** verification — not optional, not "if there's time" — when any of these hold:

1. It's rated Critical or High severity **and** it asserts a DOM/structural fact (H1, heading hierarchy, meta tag, form field, link target, gating/login requirement, or similar).
2. It asserts an asset is gated, restricted, or requires authentication.
3. It generalizes a single-page or homepage-only measurement to "the site," "all pages," or "sitewide."
4. **Two or more subagents disagree on a factual claim.** This is mandatory, not judgment — if content and conversion both discuss the same download and one says gated, one says open, that gets resolved here, not left for the report to inherit.

**How to verify:**
- Structural/DOM claim → re-run `analyze_page.py` against the specific URL named in the finding (not just the Phase 1.1 sample, if the finding is about a page outside it).
- Asset/gating claim → `curl -sI "<asset-url>"` for status code and content-type, or `curl -s "<asset-url>" | wc -c` for a byte count if you need to confirm it isn't a redirect-to-login stub. No login flow, no cookie jar — if the asset returns 200 with the expected content-type on a bare request, it is not gated.
- Sitewide generalization → either widen the Structural Facts sample to cover it, or downgrade the claim to state its actual scope.

**Outcome:**
- Verified false → drop or rewrite the finding. Note the correction in the report (e.g. "market-content flagged X; verified against raw HTML, this does not hold — see Structural Facts").
- Verified true → keep it, and cite the raw evidence (URL + what the re-fetch showed) instead of the subagent's original wording.
- Can't be verified (asset behind real auth, page unreachable, etc.) → downgrade to "unverified — needs manual check," never present it as settled fact.

This phase exists because subagents without `Bash` (content, conversion, competitive, strategy) can only read the site through WebFetch, which converts pages to markdown and hands that to a small model — a channel that reliably fabricates structure (see `${CLAUDE_PLUGIN_ROOT}/references/webfetch-artifacts.md`). Only `market-technical` fetches raw HTML directly. Do not skip this phase because subagents agree with each other; three subagents converging on the same WebFetch artifact is exactly how the 2026-08-15 false H1 finding happened.

---

## Phase 3: Synthesis (Aggregation and Scoring)

### 3.1 Scoring Methodology

Compute the composite Marketing Score using weighted averages:

```
Marketing Score = (
    Content_Score      * 0.25 +
    Conversion_Score   * 0.20 +
    SEO_Score          * 0.20 +
    Competitive_Score  * 0.15 +
    Brand_Score        * 0.10 +
    Growth_Score       * 0.10
)
```

**Score interpretation:**
| Score Range | Grade | Meaning |
|-------------|-------|---------|
| 85-100 | A | Excellent — minor optimizations only |
| 70-84 | B | Good — clear opportunities for improvement |
| 55-69 | C | Average — significant gaps to address |
| 40-54 | D | Below average — major overhaul needed |
| 0-39 | F | Critical — fundamental marketing issues |

### 3.2 Aggregate Recommendations

Collect all recommendations from subagents. **Filter them against the `Myth Guardrail` in
`${CLAUDE_PLUGIN_ROOT}/references/google-search-guidance.md` before classifying.** A recommendation
matching a guardrail row is dropped, not downgraded or reclassified. Say so in the report
("`market-technical` proposed adding an llms.txt; dropped — Google Search ignores the file"), so the
removal is legible rather than silent. A myth check the grounding digest asked for still appears as a
reported fact in the technical section; it just never becomes a recommendation.

Then classify what remains:

**Quick Wins** (implement in < 1 week, low effort, high impact):
- Copy changes to headlines and CTAs
- Adding missing meta descriptions
- Adding trust signals near CTAs
- Fixing broken links or images
- Adding urgency or social proof

**Strategic Recommendations** (1-4 weeks, medium effort, high impact):
- Redesigning pricing, RFQ, inquiry, quote, or enrollment flow
- Building comparison/alternatives pages
- Creating lead magnets, gated technical assets, calculators, selectors, or content upgrades
- Email sequence implementation
- Landing page A/B test designs

**Long-Term Initiatives** (1-3 months, high effort, transformative impact):
- Content marketing strategy overhaul
- SEO content gap campaign
- Funnel redesign
- Brand repositioning
- New growth channel development

### 3.3 Revenue Impact Estimates

For each recommendation, estimate the revenue impact:

```
Revenue Impact Formula:
  Current Monthly Traffic x Conversion Rate Improvement x Average Deal Value
  = Estimated Monthly Revenue Lift

Example:
  10,000 visitors x 0.5% conversion lift x $99 ARPU = $4,950/month
```

Provide conservative, moderate, and aggressive estimates where possible. Use these qualifiers:

| Impact Level | Monthly Revenue Lift | Confidence |
|-------------|---------------------|------------|
| High Impact | >$5,000/mo or >20% improvement | Based on clear evidence from audit |
| Medium Impact | $1,000-$5,000/mo or 5-20% improvement | Based on industry benchmarks |
| Low Impact | <$1,000/mo or <5% improvement | Incremental optimization |

### 3.4 Competitor Comparison Table

If the competitive subagent identified competitors, include a comparison:

```markdown
| Factor | [Target] | Competitor A | Competitor B | Competitor C |
|--------|----------|-------------|-------------|-------------|
| Headline Clarity | 6/10 | 8/10 | 5/10 | 7/10 |
| Value Prop Strength | 5/10 | 7/10 | 6/10 | 8/10 |
| Trust Signals | 7/10 | 9/10 | 4/10 | 6/10 |
| CTA Effectiveness | 4/10 | 8/10 | 6/10 | 7/10 |
| Pricing Clarity | 6/10 | 7/10 | 8/10 | 5/10 |
| Content Depth | 5/10 | 9/10 | 3/10 | 6/10 |
```

---

## Output Format: MARKETKIT - MARKETING-AUDIT - <domain>.md

Write the final report to the exact `output_path` resolved in Phase 0 (`${CLAUDE_PLUGIN_ROOT}/references/output-location.md`) with this structure:

```markdown
[YAML front matter from the Phase 0 metadata resolver — exact shape in references/output-location.md. Omit the whole block when the resolver returned null.]
# Marketing Audit: [Business Name]
**URL:** [url]
**Date:** [current date]
**Business Type:** [detected type]
**Overall Marketing Score: [X]/100 (Grade: [letter])**

---

## Executive Summary

[3-5 paragraph summary for a non-technical stakeholder. Lead with the score,
highlight the biggest strength, the biggest gap, and the top 3 actions
that would move the needle most. Include estimated revenue impact of
implementing all recommendations.]

---

## Score Breakdown

| Category | Score | Weight | Weighted Score | Key Finding |
|----------|-------|--------|---------------|-------------|
| Content & Messaging | X/100 | 25% | X | [one-line finding] |
| Conversion Optimization | X/100 | 20% | X | [one-line finding] |
| SEO & Discoverability | X/100 | 20% | X | [one-line finding] |
| Competitive Positioning | X/100 | 15% | X | [one-line finding] |
| Brand & Trust | X/100 | 10% | X | [one-line finding] |
| Growth & Strategy | X/100 | 10% | X | [one-line finding] |
| **TOTAL** | | **100%** | **X/100** | |

---

## Quick Wins (This Week)

[Numbered list of 5-10 quick wins with specific implementation steps.
Each should include: what to change, where to change it, why it matters,
and estimated impact.]

## Strategic Recommendations (This Month)

[Numbered list of 3-7 strategic recommendations with rationale,
implementation steps, and expected outcomes.]

## Long-Term Initiatives (This Quarter)

[Numbered list of 2-5 long-term initiatives with business case,
resource requirements, and projected ROI.]

---

## Detailed Analysis by Category

### Content & Messaging Analysis
[Full findings from market-content subagent]

### Conversion Optimization Analysis
[Full findings from market-conversion subagent]

### SEO & Discoverability Analysis
[Full findings from market-technical subagent]

### Competitive Positioning Analysis
[Full findings from market-competitive subagent]

### Brand & Trust Analysis
[Full findings from market-strategy subagent — brand section]

### Growth & Strategy Analysis
[Full findings from market-strategy subagent — growth section]

---

## Competitor Comparison

[Comparison table from Section 3.4]

---

## Revenue Impact Summary

| Recommendation | Est. Monthly Impact | Confidence | Timeline |
|---------------|-------------------|------------|----------|
| [recommendation 1] | $X,XXX | High/Med/Low | X weeks |
| [recommendation 2] | $X,XXX | High/Med/Low | X weeks |
| ... | | | |
| **Total Potential** | **$XX,XXX/mo** | | |

---

## Next Steps

1. [Most critical action item]
2. [Second priority]
3. [Third priority]

*Generated by Market Context Kit — `/marketkit:audit`*
```

---

## Terminal Output

In addition to the file, display a condensed summary in the terminal:

```
=== MARKETING AUDIT COMPLETE ===

Business: [name] ([type])
URL: [url]
Marketing Score: [X]/100 (Grade: [letter])

Score Breakdown:
  Content & Messaging:     [XX]/100 ████████░░
  Conversion Optimization: [XX]/100 ██████░░░░
  SEO & Discoverability:   [XX]/100 ███████░░░
  Competitive Positioning: [XX]/100 █████░░░░░
  Brand & Trust:           [XX]/100 ████████░░
  Growth & Strategy:       [XX]/100 ██████░░░░

Top 3 Quick Wins:
  1. [win]
  2. [win]
  3. [win]

Top 3 Strategic Moves:
  1. [move]
  2. [move]
  3. [move]

Estimated Revenue Impact: $X,XXX-$XX,XXX/month

Full report saved to: [resolved output_path, e.g. Audit-2026-08-17/MARKETKIT - MARKETING-AUDIT - example.com.md]
```

---

## Error Handling

- If the URL is unreachable, report the error and suggest checking the URL
- If a subagent fails, continue with remaining subagents and note the gap in the report
- If the site is behind authentication, note what was accessible and recommend manual review for gated content
- If the site has very little content (single page), adapt the analysis accordingly and note limited scope
- If a Phase 2.5 verification can't be completed (asset behind real auth, page unreachable, `curl` blocked), report the finding as "unverified — needs manual check," never as settled fact
- If a subagent fails Phase 2.4 reconciliation and cannot be rerun, mark its dimension `not scored — scope violation`, renormalize the remaining weights to 100%, and say so in the Score Breakdown table — do not merge the contaminated findings and do not invent a replacement score

## Cross-Skill Integration

**Everything in this section is yours alone.** These files are orchestrator context, they are read by you in Phase 3, and they never go on the Data Manifest. A subagent that sees a sibling skill's output inherits its conclusions instead of reaching its own, which is the whole reason the five run independently.

- If Phase 0 retained a valid `SEARCH-CONTEXT.v1.json`, apply `${CLAUDE_PLUGIN_ROOT}/references/search-context-integration.md` now. Do not paste Search Context data into any subagent prompt. Use its measured period and source statuses to corroborate or prioritize independently derived recommendations, label estimates and partial sources, and cite the artifact path. It may change ordering and confidence, but **do not change the six audit scores**, any subagent score, or the weighted composite.

- If `MARKETKIT - COMPETITOR-REPORT - <domain>.md` exists in the Phase 0 `audit_dir` under the same exact domain scope, incorporate its findings during Phase 3 synthesis — after `market-competitive` has returned its own, independently derived competitor set. Where the two disagree, say so in the report rather than quietly preferring one.
- If `MARKETKIT - BRAND-VOICE - <domain>.md` exists (same `audit_dir`, same exact domain scope), use it to contextualize the content analysis in Phase 3. It does not go into the `market-content` prompt; the grounding digest is what carries client voice to the subagents.
- Never search older audit folders automatically. A previous `MARKETKIT - MARKETING-AUDIT - <domain>.md` may be compared against this run only if the user explicitly supplies its path. If you report a delta, name both dates and state that the new scores were produced without sight of the old ones. That sentence is what makes the comparison worth anything.
- Reference other available analyses in the executive summary
- Suggest follow-up commands: `/marketkit:copy`, `/marketkit:funnel`, `/marketkit:competitors` for deeper dives

