---
name: content-plan
description: Use when the user asks what content to write, wants a content plan, editorial calendar, topic clusters, or article drafts researched from their own site and niche.
argument-hint: <url>
allowed-tools: Bash(python "${CLAUDE_PLUGIN_ROOT}/scripts/"*), Bash(python3 "${CLAUDE_PLUGIN_ROOT}/scripts/"*), Bash(curl -s *)
metadata:
  version: 3.0.0
---

# Content Plan — Research, Strategy & Article Drafts

You are the content strategy engine for `/marketkit:content-plan <url>`. You research a site's niche at industry depth, identify content opportunities competitors are missing, build a full topical cluster architecture, output a structured content plan for user approval, then draft complete articles for each approved row. No publishing — output stops at local markdown files.

## Phase 0: Grounding

Read `${CLAUDE_PLUGIN_ROOT}/references/grounding.md` and load any `_grounding/` folder it finds. Client documentation outranks every default in this skill, and any claim rules it contains bind the output. Name the loaded files at the top of what you produce.

Grounding supplies the niche, target industries, content pillars and claim rules that this plan must stay inside.

Read `${CLAUDE_PLUGIN_ROOT}/references/output-location.md`. Normalize the target URL to its exact non-`www` domain and resolve today's output path now:

```
python "${CLAUDE_PLUGIN_ROOT}/scripts/resolve_audit_output.py" --purpose CONTENT-PLAN --scope <domain> --extension md
```

Use `python3` on macOS/Linux. Retain `audit_dir` — Phase 1's dependency check and every Phase 6 article resolve inside it too — and the exact `output_path` for the Phase 5 write.

Then resolve optional report metadata from the same working directory:

```
python "${CLAUDE_PLUGIN_ROOT}/scripts/resolve_report_metadata.py" --toolkit "Market Context Kit" --host <exact active host> --provider <exact active LLM provider> --model <exact active model id>
```

Never guess a runtime value. Handle the three outcomes exactly as `${CLAUDE_PLUGIN_ROOT}/references/output-location.md` specifies: `null` means write no metadata block at all, a JSON object means reproduce its fields verbatim as YAML front matter at the very top of the report, and an error means stop rather than invent or drop attribution.

Read `${CLAUDE_PLUGIN_ROOT}/references/webfetch-artifacts.md` before quoting page copy or asserting anything about a page's structure, staleness, or absence. Page text used as evidence must come from `scripts/analyze_page.py` or another real parser — never an ad-hoc regex HTML-to-text script — and must be text a visitor actually sees, not commented-out, hidden, or attribute-only markup.

---

## Skill Purpose

Build a comprehensive, research-backed content plan for any website. Starting from a URL, you map what content already exists, mine every available source for topic ideas, cluster them into pillar-and-support architecture, score them by strategic value, and produce a ready-to-execute editorial calendar. After user approval of the plan, you draft each article in full — complete with front-matter, structured outlines, FAQ sections, and internal links — matching the site's brand voice and SEO requirements.

## When to Use

- User provides a URL and asks for a content plan, content strategy, or editorial calendar
- User wants to identify content gaps relative to competitors
- User wants to build out topical authority in their niche
- User wants full article drafts, not just titles or outlines
- Triggered by `/marketkit:content-plan <url>` or `/marketkit:content-plan`

---

## How to Execute

### Phase 1: Configuration Resolution & Dependency Check

Before doing any research, pull existing data from prior skill runs. This dramatically improves output quality and reduces token cost.

#### 1.1 Variable Resolution Table

Resolve each variable using the priority order shown. Stop at the first successful source.

| Variable | Source Priority |
| --- | --- |
| `WEBSITE_URL` | CLI argument (required — ask user if missing) |
| `LANGUAGE_CODE` | `<html lang>` attribute on homepage → ask user |
| `COUNTRY_CODE` | TLD heuristic (`.de`→`de`, `.it`→`it`, `.fr`→`fr`, `.es`→`es`, `.co.uk`→`uk`, `.com.au`→`au`) → ask user |
| `WEBSITE_NICHE` | `MARKETKIT - BRAND-VOICE - <domain>.md` "Brand Description" section → homepage meta description → ask user |
| `BRAND_VOICE_PROFILE` | `MARKETKIT - BRAND-VOICE - <domain>.md` full document if present |
| `COMPETITORS` | `MARKETKIT - COMPETITOR-REPORT - <domain>.md` direct + indirect competitor list |
| `EXISTING_KEYWORDS` | `MARKETKIT - SEO-AUDIT - <domain>.md` primary + secondary keyword tables |
| `CONTENT_GAPS_KNOWN` | `MARKETKIT - SEO-AUDIT - <domain>.md` "Content Gap Analysis" section |
| `AUDIT_PRIORITIES` | `MARKETKIT - MARKETING-AUDIT - <domain>.md` priority recommendations if present |

#### 1.2 Dependency Detection

Check for prerequisite files inside the Phase 0 `audit_dir`, same exact domain scope only — never search older audit folders:

1. `MARKETKIT - BRAND-VOICE - <domain>.md` — brand positioning, niche description, voice profile
2. `MARKETKIT - COMPETITOR-REPORT - <domain>.md` — competitor URLs for sitemap mining
3. `MARKETKIT - SEO-AUDIT - <domain>.md` — existing keyword data, known content gaps

**For each missing file**, present a single prompt to the user listing what is missing:

```
The following prerequisite files are missing:
- MARKETKIT - BRAND-VOICE - <domain>.md (provides niche context and brand voice)
- MARKETKIT - COMPETITOR-REPORT - <domain>.md (provides competitor URLs for topic mining)

Options:
  [auto-run] Run /marketkit:brand, /marketkit:competitors, /marketkit:seo first, then resume content plan
  [skip]     Continue without these files (self-research mode — higher token cost, lower precision)

Which would you prefer?
```

- If user selects `auto-run`: invoke the missing skills in dependency order (`brand` → `competitors` → `seo`), wait for each to complete, then resume Phase 2. If any auto-run sub-skill fails or errors, do not abort — present the user with the specific failure and offer to skip that dependency individually.
- If user selects `skip`: set `SELF_RESEARCH_MODE=true` and continue. Flag this prominently at the top of `MARKETKIT - CONTENT-PLAN - <domain>.md` when output is written.
- **Never hard-refuse.** Always offer a path forward.

---

### Phase 2: Site & Niche Research

**MANDATORY: Run `analyze_page.py` first. Do not substitute WebFetch for script output — WebFetch summarizes through a second model, so it cannot give you the exact tag-level data the plan depends on.**

#### 2.1 Homepage Analysis (Script-First)

```bash
# macOS / Linux
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/analyze_page.py" "<WEBSITE_URL>"
# Windows
python "${CLAUDE_PLUGIN_ROOT}/scripts/analyze_page.py" "<WEBSITE_URL>"
```

`${CLAUDE_PLUGIN_ROOT}` resolves to this plugin's directory on any machine — never hardcode a path, and never look for a `scripts/` folder relative to the working directory. Use `python3` on macOS and Linux, `python` on Windows; do not try `python3` first on Windows, where it resolves to the Microsoft Store alias stub and opens the Store instead of failing cleanly.

Capture from script output:

- Title tag → infers primary positioning
- Meta description → infers niche and value proposition
- H1/H2 structure → reveals content priorities
- Internal link structure → reveals topical coverage already in nav
- Schema types present → content categories the site uses

#### 2.2 Sitemap Enumeration

Use curl, not WebFetch, for raw crawlable content — WebFetch converts pages to markdown, which mangles XML and directive text:

```bash
curl -s "<WEBSITE_URL>/sitemap.xml"
curl -s "<WEBSITE_URL>/sitemap_index.xml"
curl -s "<WEBSITE_URL>/robots.txt"
```

- Parse the sitemap XML to extract every URL present on the site.
- If sitemap index exists, follow each child sitemap and collect all URLs from all of them.
- Extract URL slugs: they reveal the site's existing topical coverage.
- Group URLs by URL segment pattern (e.g., `/blog/`, `/guides/`, `/resources/`, `/news/`) to understand content architecture.
- Note `<lastmod>` dates to identify stale content opportunities.
- If all three sitemap requests return 404 or empty responses, note "No sitemap found" in the Coverage Map, use the homepage navigation links from the analyze_page.py output to infer site structure, and proceed with what is available.

Build **Existing Coverage Map** table:

| Cluster / Segment | URL Count | Sample URLs    | Oldest Last-Modified |
| ----------------- | --------- | -------------- | -------------------- |
| /blog/            | N         | [url1], [url2] | YYYY-MM-DD           |
| /guides/          | N         | ...            | ...                  |

#### 2.3 Deep Content Page Sampling

Use WebFetch to read 3-5 of the deepest, most content-rich interior pages (skip the homepage — you already have its data from analyze_page.py in step 2.1) (prefer blog posts, guides, or resource pages over category/product pages):

- Understand: audience language, pain points, product positioning, brand voice.
- Extract: recurring terminology, named entities (product names, certifications, brand-specific jargon), commercial intent signals.
- If no `MARKETKIT - BRAND-VOICE - <domain>.md` exists, perform a lightweight brand voice assessment here:
  - Formality level (1-10)
  - Persona being spoken to
  - Recurring phrases and avoided phrases

---

### Phase 3: Topic & Keyword Mining

Combine multiple research sources to build the widest possible topic surface area before filtering.

#### 3.1 Competitor Sitemap Mining

For each competitor URL from `MARKETKIT - COMPETITOR-REPORT - <domain>.md` (direct tier first, then indirect):

```bash
curl -s "<competitor-url>/sitemap.xml"
```

- Extract all blog/article/guide URLs from each competitor's sitemap.
- Parse URL slugs to identify their topical coverage.
- Do not read full competitor pages unless a topic title is ambiguous — slug parsing is sufficient for coverage mapping.

If no `MARKETKIT - COMPETITOR-REPORT - <domain>.md` exists, use WebSearch to identify the top 3 competitors:

```
WebSearch: "[WEBSITE_NICHE] competitors" OR "[WEBSITE_NICHE] alternatives" OR top [WEBSITE_NICHE] companies
```

Then fetch their sitemaps via curl as above.

#### 3.2 SERP Research

For each primary keyword from `MARKETKIT - SEO-AUDIT - <domain>.md` (or the 3-5 most obvious seed keywords inferred from the site if no audit exists):

```
WebSearch: <primary_keyword>
WebSearch: <primary_keyword> site:[country TLD if not .com]
```

From SERP results, extract:

- Top-10 page titles → reveal proven content formats and angles
- People Also Ask (PAA) questions → FAQ fodder + direct content ideas
- Related searches at bottom of SERP → long-tail cluster topics

#### 3.3 Community & Forum Research

```
WebSearch: site:reddit.com <niche> <problem> OR <question>
WebSearch: site:reddit.com <niche> recommendations
WebSearch: <niche> forum question <topic>
```

Reddit is a rich source for consumer, software and developer niches and a thin one for industrial, regulated and procurement-led ones. For those, mine specialist forums, association and standards-body publications, trade-press archives, LinkedIn discussion under expert posts, and the questions that arrive through the client's own support and sales channels — that last source is usually the best available and is often sitting unused in an inbox.

Extract from results:

- Natural language questions (verbatim phrasings are keyword goldmines)
- Recurring pain points and frustrations
- Jargon and terminology used by the community (not just the brand)
- Complaints about existing content ("every article just says X but doesn't explain Y")

#### 3.4 Video Research

```
WebSearch: site:youtube.com <niche> <topic>
WebSearch: site:youtube.com <niche> how to
```

Extract:

- Video titles with high view counts → validated demand signals
- Video description keywords → secondary keyword ideas
- Comment-section questions → PAA equivalents for article FAQ sections

#### 3.5 Industry News & Trends

```
WebSearch: <niche> news [CURRENT_YEAR]
WebSearch: <niche> regulation OR law change [CURRENT_YEAR] (if applicable)
WebSearch: <niche> trends [CURRENT_YEAR+1]
```

(Use the current calendar year — today's date is available from context.)

Extract:

- Regulatory or compliance angle topics (evergreen + authoritative)
- Emerging trend topics (early-mover advantage, AI citability)
- Seasonal event hooks tied to the industry calendar

#### 3.6 Brand Entity Terms

Pull the brand entity terms surfaced in Phase 2.3 — product names, certifications, proprietary materials, regulatory codes, and any other named entities found on the site — and mine them as topical angles.

For each entity term identified:

- Generate 2-3 topic ideas that use the entity as the topical lens (e.g., site sells PFAS-free gaskets → entity term "PFAS-free" → topic ideas: "What Does PFAS-Free Mean for Industrial Seals?", "PFAS-Free vs. Standard Gasket Materials: Performance Comparison", "Regulations Driving PFAS-Free Material Adoption in 2025")
- Run a SERP check per entity term:
  ```
  WebSearch: "<entity term>" <niche>
  WebSearch: "<entity term>" site:[competitor domain]
  ```
- Note whether each competitor is actively targeting the entity term (landing pages, blog posts, or product copy built around it).
- Flag any entity term where **no competitor has dedicated content** — these are strong blind-spot candidates. Add these entity term topics to your raw candidate pool; in Phase 3.7, the sort step will typically place them in List 3 (blind spot) when competitor SERP coverage = 0.

Entity terms with unique angles (competitor coverage = 0) are the highest-priority blind spots generated by this phase.

#### 3.7 Produce the Three Master Lists

Before clustering, sort every candidate topic into exactly one list:

**List 1 — Already Covered (exclude from plan)** Topics clearly addressed by URLs already in the site's sitemap.

**List 2 — Competitor-Covered Gap (direct opportunity)** Topics covered by at least one competitor but absent from the target site. Sort by: number of competitors covering the topic (more = higher demand signal).

**List 3 — Industry Blind Spot (highest strategic value)** Topics actively discussed in community/SERP/YouTube but not well covered by any competitor. These are the highest-value opportunities: lower competition, differentiated positioning, strong AI citability potential.

---

### Phase 4: Cluster Architecture

Transform the topic lists into a structured pillar-and-cluster architecture.

#### 4.1 Cluster Formation Rules

- Group topics by semantic parent theme.
- Each cluster must have exactly 1 pillar piece and 4-8 supporting articles.
- Supporting articles must address a specific subtopic of the pillar, not the pillar topic itself.
- Every supporting article links up to its pillar. The pillar links down to all supporting articles.
- Clusters must not overlap significantly — if two candidate clusters share more than 2 supporting topics, merge them.

**Cluster size guidelines:**

| Role       | Content Type                                | Length Code |
| ---------- | ------------------------------------------- | ----------- |
| Pillar     | Comprehensive guide (covers the full topic) | xl          |
| Supporting | Deep-dive on one subtopic                   | md or lg    |
| Supporting | How-to or tutorial                          | md          |
| Supporting | FAQ or comparison                           | sm or md    |

#### 4.2 Topic Scoring (0-12 scale)

Score every candidate topic on 4 dimensions (0-3 each):

**Dimension 1: Search Intent Fit (0-3)**

- 3 = Intent directly matches site's commercial purpose (e.g., site sells X, topic targets buyers of X)
- 2 = Intent adjacent to commercial purpose (informational but directly supports purchase decision)
- 1 = Informational, tangentially related to offering
- 0 = Informational, no clear path to commercial outcome

**Dimension 2: Competition Gap (0-3)**

- 3 = Top 10 results are thin, outdated, or don't fully address the query
- 2 = Decent coverage exists but there is a clear angle or format gap
- 1 = Well-covered topic but site could match quality
- 0 = Saturated topic, no differentiation angle visible

**Dimension 3: Business Value (0-3)**

- 3 = Transactional — directly connects to product/service purchase
- 2 = Commercial investigation — comparison, review, "best X" format
- 1 = Informational close to product (how-to that requires the product)
- 0 = Pure informational, no product touchpoint

**Dimension 4: AI-Citability Potential (0-3)**

- 3 = Clear-answer query, factual, structured-answer-friendly (definition, how-to, comparison table) — strong candidate for ChatGPT/Perplexity citation
- 2 = Topic can be made citation-friendly with FAQ and structured sections
- 1 = Opinion or trend piece — lower citation potential
- 0 = Purely subjective or brand-specific, unlikely to be cited by AI engines

**Total score range: 0-12.** Topics scoring 9-12 are Priority 1. Topics scoring 6-8 are Priority 2. Topics scoring 0-5 are Priority 3 or cut.

---

### Phase 5: Content Plan Output

**This phase produces `MARKETKIT - CONTENT-PLAN - <domain>.md`. After writing the file, STOP and wait for user approval before proceeding to Phase 6.**

#### 5.1 Write MARKETKIT - CONTENT-PLAN - <domain>.md

Produce the file with the following sections in order:

**Header block:**

```markdown
[YAML front matter from the Phase 0 metadata resolver — exact shape in references/output-location.md. Omit the whole block when the resolver returned null.]

# Content Plan

## [Site Name / URL]

### Generated: [Date]
```

If `SELF_RESEARCH_MODE=true`, add this banner immediately after the header:

```markdown
> **Self-research mode** — This plan was built without BRAND-VOICE.md, COMPETITOR-REPORT.md, or SEO-AUDIT.md. Precision is lower than when prerequisite files exist. Run `/marketkit:brand`, `/marketkit:competitors`, `/marketkit:seo` for a higher-confidence plan.
```

**Section 1: Cluster Map (ASCII topology)**

Show the full pillar-and-cluster structure as an ASCII tree:

```
[Cluster Name]
├── [Pillar Title] (xl)
├── [Supporting Article 1] (md)
├── [Supporting Article 2] (lg)
├── [Supporting Article 3] (md)
└── [Supporting Article 4] (sm)

[Cluster 2 Name]
├── ...
```

**Section 2: Content Plan Table**

One row per article. Columns:

| # | Cluster | Pillar/Support | Target Keyword | Suggested Title | Content Type | Search Intent | Priority Score | Size | Internal Links | Schema Type | Source Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Column definitions:

- **#** — Sequential row number, used for approval references
- **Cluster** — Parent cluster name
- **Pillar/Support** — `Pillar` or `Support`
- **Target Keyword** — Primary keyword for this article
- **Suggested Title** — Working H1 title (revise after drafting)
- **Content Type** — Guide / How-To / Comparison / FAQ / Case Study / Listicle / News Analysis
- **Search Intent** — Informational / Commercial / Transactional / Navigational
- **Priority Score** — 0-12 score from Phase 4.2
- **Size** — `sm` (600-900w) / `md` (900-1500w) / `lg` (1500-2500w) / `xl` (2500-4000w)
- **Internal Links** — Row numbers of other articles this piece should link to
- **Schema Type** — Article / HowTo / FAQ / Product / Comparison / BreadcrumbList
- **Source Notes** — Brief source evidence (e.g., "Reddit: 47 questions found", "PAA box on [keyword]", "Competitor gap: 3/3 cover this")

Sort rows by: Priority Score descending, then Pillar before Support within same score.

**Section 3: Blind-Spot Opportunities**

List 3-5 List 3 topics (industry blind spots) from Phase 3.7 with rationale:

```markdown
## Blind-Spot Opportunities

These topics are actively discussed in forums/SERP/YouTube but no competitor covers them well. High strategic value: low competition, potential first-mover advantage, strong AI citability.

| Topic | Evidence of Demand | Why Competitors Miss It | Recommended Angle |
| ----- | ------------------ | ----------------------- | ----------------- |
| ...   | ...                | ...                     | ...               |
```

**Section 4: Editorial Calendar**

Suggest a publishing order over 8-12 weeks (if the plan has fewer than 16 articles total, compress to a 4-6 week calendar instead). Rules:

- Pillar pieces must be published before their cluster's supporting articles.
- Higher priority scores publish earlier.
- No more than 2 xl-size articles in the same week.
- Aim for consistent weekly cadence (2-4 pieces per week depending on total plan size).

```markdown
## Editorial Calendar (Suggested — 12-Week Plan)

| Week | Article # | Title | Size | Notes                                    |
| ---- | --------- | ----- | ---- | ---------------------------------------- |
| 1    | #1        | ...   | xl   | Pillar — publish first to anchor cluster |
| 1    | #3        | ...   | md   | Support — internal links to #1           |
| ...  |
```

**Section 5: Brand Voice Notes**

If `MARKETKIT - BRAND-VOICE - <domain>.md` is available:

- Excerpt the voice dimensions (formality, tone) and key vocabulary guidelines
- Note any explicit audience language preferences to apply during drafting

If not available, note what was inferred from Phase 2.3 and flag that full brand voice analysis would improve article quality.

**Section 6: Existing Coverage Map**

Paste the Existing Coverage Map table built in Phase 2.2 for reference.

#### 5.2 Gate: Wait for User Approval

After writing `MARKETKIT - CONTENT-PLAN - <domain>.md`, output this message and stop:

```
[resolved output_path, e.g. Audit/MARKETKIT - CONTENT-PLAN - example.com.md] has been written.

Please review the plan and confirm how to proceed:

  [approve-all]     Draft full articles for all rows
  [approve N,N,N]   Draft only the rows you specify (e.g., "approve 1,3,5")
  [revise]          Request changes before drafting

Waiting for your confirmation before writing any articles.
```

**Do not write any article files until the user explicitly approves.**

---

### Phase 6: Article Drafts

Execute only after explicit user approval from Phase 5.2. If approval was partial (e.g., `[approve 1,3,5]`), draft only the approved rows. Mark skipped rows with `status: deferred` in their front-matter and note them in a brief summary at the end of Phase 6 output: "X article(s) deferred — re-run Phase 6 to draft them."

For each approved row in the content plan, resolve and write one article:

```
python "${CLAUDE_PLUGIN_ROOT}/scripts/resolve_audit_output.py" --purpose ARTICLE-<UPPERCASE-KEBAB-SLUG> --scope <domain> --extension md
```

Run the resolver separately for every article filename, using the exact same `<domain>` scope as Phase 0. Write the exact returned `output_path` — flat in the active audit folder next to `MARKETKIT - CONTENT-PLAN - <domain>.md`, never a nested `articles/` subfolder.

#### 6.1 Slug Derivation

Derive the slug from the Target Keyword, then uppercase and kebab it for the resolver's `--purpose`:

- Lowercase, hyphen-separated
- Remove stop words (a, the, and, for, of, to, in, on, with)
- Maximum 6 words
- Example: "How to Choose the Best CRM Software" → slug `choose-best-crm-software` → `--purpose ARTICLE-CHOOSE-BEST-CRM-SOFTWARE` → `MARKETKIT - ARTICLE-CHOOSE-BEST-CRM-SOFTWARE - <domain>.md`

#### 6.2 Article Front-Matter

Every article begins with YAML front-matter:

```yaml
---
title: "[Suggested Title]"
target_keyword: "[Target Keyword]"
secondary_keywords:
  - "[kw2]"
  - "[kw3]"
  - "[kw4]"
search_intent: "[Informational|Commercial|Transactional]"
cluster: "[Cluster Name]"
role: "[Pillar|Support]"
internal_link_targets:
  - "[slug of article #N]"
  - "[slug of article #M]"
schema_type: "[Schema Type]"
size: "[sm|md|lg|xl]"
word_count_target: "[600-900|900-1500|1500-2500|2500-4000]"
date_planned: "[YYYY-MM-DD from editorial calendar]"
---
```

#### 6.3 Article Structure

Build the article outline by combining:

1. SERP top-10 structure (most common H2 headings across top-ranking pages for the target keyword)
2. PAA box questions (map each to an FAQ entry or an H2/H3 section)
3. Author angle (a specific perspective, opinion, or data point that differentiates from existing results — particularly important for AI citability)

**Required sections (all articles):**

**Hook paragraph (40-60 words)** Placed immediately after H1, before any other content. This is the featured-snippet candidate. It must:

- State the core answer or promise of the article in plain language
- Include the target keyword naturally in the first sentence
- Be complete enough to stand alone as a snippet

**Main body (H2/H3 hierarchy)**

- Every H2 maps to a major subtopic
- H3s break H2s into scannable subsections
- At least one H2 must contain the target keyword or a close variation
- Use numbered lists for processes/steps, unordered lists for collections/options
- Include at least one table where comparison or structured data is natural

**Entity coverage section**

- Name all relevant entities (people, organizations, products, standards, regulations) related to the topic
- Reference authoritative external sources for factual claims (link to gov sites, academic papers, industry bodies)
- This section does not need its own H2 — entities woven into body copy

**FAQ section** Must appear as a standalone H2 section titled "Frequently Asked Questions" or "FAQ: [Topic]":

- Source questions from PAA box (captured in Phase 3.2) and Reddit threads (Phase 3.3)
- 4-6 questions minimum
- Each answer: 40-80 words (featured-snippet friendly)
- Format: `### Question text` followed immediately by answer paragraph

This section enables `FAQPage` schema and directly boosts AI citability (ChatGPT and Perplexity preferentially cite FAQ-structured factual content).

**Internal links (3-5 per article)**

- Link to: the cluster's pillar (if this is a supporting article), other supporting articles in the cluster, and 1-2 existing site pages from the Coverage Map
- Use descriptive anchor text (not "click here" or "read more")
- Place links in the body copy at contextually natural points, not forced at the end

**CTA (call to action)** Final section before FAQ — one specific, benefit-led call to action aligned with the site's primary commercial intent:

- Aligned with site's commercial intent (e.g., "Try [Product]", "Get a free audit", "Download the guide", "Request a quote", "Download the datasheet", "Book technical consultation", "Reserve a course seat")
- If commercial intent is unclear, use a newsletter or resource CTA
- Single, specific CTA — not multiple competing actions

#### 6.4 Voice Application

If `MARKETKIT - BRAND-VOICE - <domain>.md` is available:

- Apply formality level, vocabulary preferences, and do/don't rules from the brand voice guide
- Replicate the brand's sentence length patterns and punctuation style
- Use vocabulary from the "Words We Use" list; avoid words from "Words We Avoid"

If no `MARKETKIT - BRAND-VOICE - <domain>.md`:

- Default to clear, professional, direct prose
- Match the approximate formality level inferred from Phase 2.3
- Add a note in the article front-matter: `brand_voice: "inferred — run /marketkit:brand for calibrated voice"`

#### 6.5 Word Count Targets by Size

| Size Code | Word Count Target | Typical Use |
| --- | --- | --- |
| sm | 600-900 words | FAQ pages, narrow how-tos, simple comparisons |
| md | 900-1500 words | Standard how-tos, supporting subtopic articles |
| lg | 1500-2500 words | In-depth guides, comparison articles, case studies |
| xl | 2500-4000 words | Pillar pieces, comprehensive topic guides |

#### 6.6 Progress Reporting

After each article is written, output a one-line status:

```
[3/8] MARKETKIT - ARTICLE-<SLUG> - <domain>.md — written (1,842 words, lg)
```

After all articles are complete:

```
Phase 6 complete. All N articles written to the active audit folder.

Summary:
- Total articles: N
- Total estimated word count: ~N,000 words
- Clusters covered: N
- Files written:
  - MARKETKIT - ARTICLE-<SLUG1> - <domain>.md
  - MARKETKIT - ARTICLE-<SLUG2> - <domain>.md
  ...

Next steps:
- Review the drafted articles for brand voice consistency
- Add site-specific CTAs where placeholders were used
- Run /marketkit:seo on final articles before publishing
- Run /marketkit:brand if brand voice was not pre-calibrated
```

---

## Output Format

```
MARKETKIT - CONTENT-PLAN - <domain>.md              ← Phase 5 output, exact output_path from Phase 0.
MARKETKIT - ARTICLE-<SLUG> - <domain>.md             ← Phase 6 output. One file per approved article, flat in the same audit folder.
```

### MARKETKIT - CONTENT-PLAN - <domain>.md Structure

```markdown
[YAML front matter from the Phase 0 metadata resolver — exact shape in references/output-location.md. Omit the whole block when the resolver returned null.]

# Content Plan

## [Site Name / URL]

### Generated: [Date]

> [Self-research mode banner if applicable]

---

## Cluster Map

[ASCII topology tree]

---

## Content Plan

| # | Cluster | Pillar/Support | Target Keyword | Suggested Title | Content Type | Search Intent | Priority Score | Size | Internal Links | Schema Type | Source Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

---

## Blind-Spot Opportunities

[Table of high-value uncovered topics with evidence and rationale]

---

## Editorial Calendar (Suggested — 12-Week Plan)

[Week-by-week publishing schedule]

---

## Brand Voice Notes

[Excerpt from BRAND-VOICE.md or inferred voice summary]

---

## Existing Coverage Map

[Table of current site content by URL segment]
```

### MARKETKIT - ARTICLE-<SLUG> - <domain>.md Structure

```markdown
---
[YAML front-matter block]
---

# [Article H1 Title]

[Hook paragraph — 40-60 words, featured-snippet candidate]

## [H2: Major Section 1]

[Body copy with internal links woven in naturally]

### [H3: Subsection if needed]

## [H2: Major Section 2]

[...]

## [Final H2: CTA Section]

[Single specific call to action]

## Frequently Asked Questions

### [Question from PAA box]

[Answer: 40-80 words]

### [Question 2]

[Answer]

[... 4-6 total FAQ entries]
```

---

## Key Principles

- **Research depth determines plan quality.** Skim the SERP and you get generic topics. Mine competitor sitemaps, Reddit threads, and YouTube titles, and you find angles no one is covering — those are the highest-value pieces.
- **Always run `analyze_page.py` first.** Per project rules, script output takes precedence over WebFetch for homepage structural data. This is not optional.
- **Use curl for raw sitemap and robots.txt content.** WebFetch converts HTML to markdown and cannot reliably parse XML. Sitemaps must be fetched with curl.
- **The gate in Phase 5 is real — never skip it.** Writing articles without user approval of the plan wastes time for both parties and produces content the user may not want. Always stop and wait.
- **Pillar before supporters.** The editorial calendar must reflect topical dependency. A supporting article that links to a pillar that doesn't exist yet creates orphaned internal links. Publish pillars in Week 1-2.
- **FAQ sections are mandatory, not optional.** ChatGPT, Perplexity, and other AI search engines preferentially surface FAQ-structured factual content. Skipping FAQs reduces AI citability meaningfully.
- **Hook paragraphs must be complete sentences that stand alone.** Google's featured snippet algorithm evaluates the first 40-60 words after an H1 or H2. A vague or teaser-style hook wastes this opportunity.
- **Self-research mode is lower precision — say so clearly.** If prerequisite files are missing and the user chose skip, the blind-spot opportunities and competitor gap analysis are based on inference, not systematic sitemap mining. The banner in `MARKETKIT - CONTENT-PLAN - <domain>.md` must make this explicit.
- **Never fabricate keyword metrics.** You do not have access to real-time search volume data. Use qualitative signals (competitor coverage count, Reddit thread volume, SERP result quality) to justify prioritization. Never invent numerical search volumes.
- **Brand voice consistency is a final check, not an afterthought.** If `MARKETKIT - BRAND-VOICE - <domain>.md` is available, re-read the voice chart and do/don't rules before writing each article. Inconsistent voice across a content cluster is harder to fix than inconsistent SEO.
- **Internal links must be planned before drafting begins.** The Internal Links column in the plan is the source of truth. Every article draft must honor those links — adding them during drafting, not retrofitting them after.
