---
name: market-competitors
description: Use when the user asks who their competitors are, how they compare, where the market gaps or content gaps sit, or wants a competitive intelligence report.
argument-hint: <url>
allowed-tools: Bash(python "${CLAUDE_PLUGIN_ROOT}/scripts/"*), Bash(python3 "${CLAUDE_PLUGIN_ROOT}/scripts/"*)
metadata:
  version: 2.0.0
---

# Competitive Intelligence Analysis

You are the competitive intelligence engine for `/ai-marketing:market-competitors <url>`. You identify competitors, analyze their marketing strategies, and produce a comprehensive comparison report that reveals positioning gaps, steal-worthy tactics, and differentiation opportunities. Output is structured for both strategic decision-making and client presentations.

## When This Skill Is Invoked

The user runs `/ai-marketing:market-competitors <url>`. Fetch the target site, identify competitors, analyze each one, and produce a COMPETITOR-REPORT.md with actionable intelligence.

---

## Phase 1: Competitor Identification

### 1.1 Competitor Categories

Identify competitors across three tiers:

| Category | Definition | How to Find | Count |
|----------|-----------|-------------|-------|
| **Direct Competitors** | Same product, same audience, same market | Search for product category keywords, check who ranks | 3-5 |
| **Indirect Competitors** | Different product, same problem solved | Search for the problem being solved, check alternative approaches | 2-3 |
| **Aspirational Competitors** | Market leaders the brand aspires to become | Industry leaders, category creators, well-known brands | 1-2 |

### 1.2 Competitor Discovery Methods

Use multiple methods to identify competitors:

**Method 1: Keyword-Based Discovery**
- Search for the target site's primary keywords
- Note which companies rank on page 1
- Search for "[product category] software/service/tool"
- For industrial or technical suppliers, also search for "[product category] manufacturer/supplier/distributor", "[standard/certification] [product]", "[application] [product]", and "[brand] equivalent/alternative"
- Search for "[target brand] alternatives"
- Search for "[target brand] vs"

**Method 2: Site-Based Discovery**
- Look for comparison pages on the target site
- Check footer links for industry associations
- Look for "integrations" pages that mention similar tools
- Check the target site's blog for competitor mentions

**Method 3: Review Platform Discovery**
- Search G2, Capterra, Trustpilot for the product category
- Note top-rated competitors in the same category
- Check "Compare" features on review sites
- For B2B industrial, regulated, or local categories where software review sites are irrelevant, use trade directories, industry associations, procurement directories, trade press, certification bodies, distributor listings, and forum/community discussions instead.

**Method 4: Social and Community Discovery**
- Search Reddit for "[product category] recommendations"
- Check Twitter/X for conversations about the product category
- Look at LinkedIn for companies followed by the target's audience

### 1.3 Automated Data Collection

Use the bundled `competitor_scanner.py` for automated data collection. It takes one or more URLs as **positional** arguments — there are no `--url` or `--output` flags — and always prints JSON:

```bash
# macOS / Linux
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/competitor_scanner.py" "<url1>" "<url2>" "<url3>"
# Windows
python "${CLAUDE_PLUGIN_ROOT}/scripts/competitor_scanner.py" "<url1>" "<url2>" "<url3>"
```

`${CLAUDE_PLUGIN_ROOT}` resolves to this plugin's directory on any machine — never hardcode a path. Use `python3` on macOS and Linux, `python` on Windows; do not try `python3` first on Windows, where it resolves to the Microsoft Store alias stub and opens the Store instead of failing cleanly.

A single URL returns one object; multiple URLs return `{"competitors": [...]}`. A `{"usage": ...}` banner means no URL argument arrived.

The script can collect:
- Homepage content and metadata
- Pricing page data (if public)
- RFQ/contact/catalog/datasheet/distributor data (if pricing is not public)
- Blog post count and recent topics
- Social media profile links and follower counts
- Technology stack detection
- Page speed metrics

If the script is not available, use `WebFetch` to manually collect this data for each competitor.

---

## Phase 2: Competitor Analysis Framework

### 2.1 Website and Messaging Analysis

For each competitor, analyze:

**Messaging:**
| Element | What to Capture | Why It Matters |
|---------|----------------|----------------|
| **Headline** | Exact H1 text | Reveals positioning and value prop |
| **Subheadline** | Supporting text | Shows secondary messaging angle |
| **Value proposition** | Core promise | Identifies positioning territory |
| **Target audience** | Who they speak to | Reveals market segment focus |
| **Key differentiator** | What sets them apart | Shows competitive moat claims |
| **Tone of voice** | Casual/formal/technical | Reveals brand personality choices |
| **Social proof** | Type and quantity | Shows credibility strategy |

**Positioning Map:**
Plot each competitor on two axes:
- X-axis: Perceived simplicity ←→ Perceived power
- Y-axis: Perceived affordability ←→ Perceived premium

```
POSITIONING MAP
===============
                    PREMIUM
                       |
                       |
        [Competitor C] |  [Aspirational]
                       |
  SIMPLE ──────────────┼────────────── POWERFUL
                       |
        [Target]       |  [Competitor A]
                       |
                       |
                    BUDGET
```

Adjust axes based on what matters most in the specific industry.

### 2.2 Pricing / Commercial Model Comparison

Build the matrix that fits the business model. For SaaS and e-commerce, use pricing/plan rows. For RFQ-led, regulated, industrial, distributor, academy, or services businesses, compare commercial path and proof instead of forcing SaaS tiers.

```markdown
| Feature/Plan | [Target] | Competitor A | Competitor B | Competitor C |
|-------------|----------|-------------|-------------|-------------|
| Free Plan | Yes/No | Yes/No | Yes/No | Yes/No |
| Starter Price | $X/mo | $X/mo | $X/mo | $X/mo |
| Pro Price | $X/mo | $X/mo | $X/mo | $X/mo |
| Enterprise | Custom | Custom | $X/mo | Custom |
| Free Trial | X days | X days | X days | X days |
| Annual Discount | X% | X% | X% | X% |
| Per-User Pricing | Yes/No | Yes/No | Yes/No | Yes/No |
| Usage Limits | [detail] | [detail] | [detail] | [detail] |
```

```markdown
| Commercial Factor | [Target] | Competitor A | Competitor B | Competitor C |
|-------------------|----------|--------------|--------------|--------------|
| Public Pricing | Yes/No/Partial | | | |
| Primary Conversion | RFQ / Contact / Buy / Enroll / Distributor | | | |
| Quote Path Clarity | Strong / Medium / Weak | | | |
| Datasheets / Downloads | Open / Gated / Missing | | | |
| Certifications / Standards | [list] | | | |
| Product Finder / Selector | Yes/No/Partial | | | |
| Stock / Lead-Time Signals | Yes/No/Partial | | | |
| Distributor / Partner Locator | Yes/No | | | |
| Proof Assets | Case studies / test data / testimonials / logos | | | |
```

**Pricing Strategy Assessment:**
- Is the target priced above, below, or at market average?
- Is pricing transparent or hidden (requiring sales calls)?
- What pricing model is used (per-user, per-usage, flat-rate, tiered)?
- Are there pricing anchoring tactics being used?
- Does the pricing page communicate value before showing numbers?
- If pricing is hidden by category norm, does the RFQ/contact path reduce uncertainty with response time, technical fields, proof, and clear next steps?
- For industrial/regulatory categories, compare standards, approvals, test data, engineering access, distributor coverage, and delivery confidence as commercial differentiators.

### 2.3 Feature Comparison Matrix

Build a comprehensive feature comparison:

```markdown
| Feature Category | Feature | [Target] | Comp A | Comp B | Comp C |
|-----------------|---------|----------|--------|--------|--------|
| Core | [Feature 1] | Full | Full | Partial | No |
| Core | [Feature 2] | Full | Full | Full | Full |
| Core | [Feature 3] | Partial | Full | No | Full |
| Advanced | [Feature 4] | No | Full | No | Full |
| Advanced | [Feature 5] | Full | No | Full | No |
| Integration | [Feature 6] | Full | Full | No | Partial |
| Support | [Feature 7] | Full | Partial | Full | Full |
```

Use: Full, Partial, No, or Beta to categorize.

Highlight:
- Features where the target has an advantage (competitive moats)
- Features where the target has a gap (vulnerability)
- Features unique to one competitor (potential differentiators)

### 2.4 SEO Competition Analysis

For each competitor, analyze:

**Content Strategy:**
| Metric | [Target] | Comp A | Comp B | Comp C |
|--------|----------|--------|--------|--------|
| Blog posts (estimated) | X | X | X | X |
| Publishing frequency | X/week | X/week | X/week | X/week |
| Content depth | Shallow/Medium/Deep | | | |
| Content types | Blog/Video/Podcast | | | |
| Key topics | [list] | [list] | [list] | [list] |

**Keyword Strategy:**
- What keywords is each competitor clearly targeting?
- Where do multiple competitors rank but the target does not? (content gaps)
- Are competitors creating comparison/alternatives content?
- What long-tail keywords are competitors ranking for?

**Content Gap Analysis:**
List topics that competitors cover but the target does not:
```
CONTENT GAPS (Competitors Cover, Target Does Not):
  1. [Topic] — covered by Comp A, B (high search intent)
  2. [Topic] — covered by Comp A, C (medium search intent)
  3. [Topic] — covered by Comp B (high search intent)
  4. [Topic] — covered by all competitors (critical gap)
```

### 2.5 Social Media Presence Comparison

| Platform | [Target] | Comp A | Comp B | Comp C |
|----------|----------|--------|--------|--------|
| LinkedIn followers | X | X | X | X |
| Twitter/X followers | X | X | X | X |
| Instagram followers | X | X | X | X |
| YouTube subscribers | X | X | X | X |
| TikTok followers | X | X | X | X |
| Posting frequency | X/week | X/week | X/week | X/week |
| Engagement rate | X% | X% | X% | X% |
| Top content type | [type] | [type] | [type] | [type] |

### 2.6 Review Mining

Analyze reviews on third-party platforms (G2, Capterra, Trustpilot, Reddit):

**For each competitor, extract:**
- Overall rating (stars)
- Number of reviews
- Top 3 praised features (what customers love)
- Top 3 complaints (what customers hate)
- Common switching reasons (why customers leave)
- Use cases mentioned most frequently

**Review Intelligence Matrix:**
```markdown
| Competitor | Rating | Reviews | Top Praise | Top Complaint | Switch Reason |
|-----------|--------|---------|-----------|---------------|--------------|
| Comp A | 4.5/5 | 500+ | Easy to use | Limited integrations | Price increase |
| Comp B | 4.2/5 | 200+ | Powerful features | Steep learning curve | Poor support |
| Comp C | 3.8/5 | 100+ | Good value | Buggy | Better alternatives |
```

---

## Phase 3: SWOT Analysis

### 3.1 SWOT for Each Competitor

For each identified competitor, produce a SWOT:

```
COMPETITOR: [Name]
URL: [url]

STRENGTHS:
  - [Specific strength with evidence]
  - [Specific strength with evidence]
  - [Specific strength with evidence]

WEAKNESSES:
  - [Specific weakness with evidence]
  - [Specific weakness with evidence]
  - [Specific weakness with evidence]

OPPORTUNITIES (for the target to exploit):
  - [Opportunity based on competitor weakness]
  - [Opportunity based on market gap]
  - [Opportunity based on unserved segment]

THREATS (competitor advantages to watch):
  - [Threat with potential impact]
  - [Threat with potential impact]
  - [Threat with potential impact]
```

### 3.2 Aggregate SWOT for the Target

Combine all competitor intelligence into a single SWOT for the target brand:

- **Strengths:** Where the target outperforms all or most competitors
- **Weaknesses:** Where the target lags behind all or most competitors
- **Opportunities:** Gaps in the market no competitor is addressing well
- **Threats:** Areas where competitors are significantly stronger

---

## Phase 4: Strategic Recommendations

### 4.1 "Steal-Worthy" Tactics

Identify specific marketing tactics from competitors worth adopting:

```
STEAL-WORTHY TACTICS
====================

1. [Competitor A] — [Tactic: e.g., "Interactive pricing calculator"]
   Why it works: [explanation]
   How to implement: [specific steps for the target]
   Estimated effort: [Low/Medium/High]
   Expected impact: [Low/Medium/High]

2. [Competitor B] — [Tactic: e.g., "Customer success story video series"]
   Why it works: [explanation]
   How to implement: [specific steps]
   Estimated effort: [Low/Medium/High]
   Expected impact: [Low/Medium/High]

[Continue for 5-10 tactics]
```

Focus on tactics that are:
- Proven (working for the competitor)
- Adaptable (can be customized for the target)
- Underutilized (the target is not currently doing this)

### 4.2 Messaging Differentiation Strategy

Based on the competitive analysis, recommend how the target should differentiate:

**Differentiation Framework:**
1. **Category:** Can the target create or own a sub-category? (e.g., "the [specific attribute] [category]")
2. **Audience:** Can the target own a specific audience segment competitors ignore?
3. **Feature:** Is there a unique feature or capability no competitor offers?
4. **Philosophy:** Can the target differentiate on values, approach, or methodology?
5. **Experience:** Can the target differentiate on customer experience, support, or community?

For each viable differentiation angle, provide:
- Positioning statement
- Headline recommendation
- Supporting evidence or proof points
- How it would manifest across the website

### 4.3 Alternative Page Strategy

Recommend creating "[Competitor] Alternative" pages:

**For each major competitor, outline:**
```
PAGE: [Target Brand] vs [Competitor Name]
URL: /vs/[competitor-name] or /alternatives/[competitor-name]

Headline: "Looking for a [Competitor] alternative? Here's why [X] teams chose [Target] instead."

Sections:
  1. Quick comparison table (features, pricing, ratings)
  2. Where [Target] wins (3-4 advantages with evidence)
  3. Where [Competitor] wins (honest, builds trust)
  4. Who [Target] is best for (ideal customer profile)
  5. Customer switching stories (testimonials from switchers)
  6. Migration guide or switching offer
  7. FAQ about switching
  8. CTA: "Try [Target] free" or "See how [Target] compares"
```

For industrial, regulated, services, or RFQ-led categories, replace SaaS elements with relevant proof:
- Quick comparison table: standards, applications, engineering access, lead time, datasheets, test data, service coverage
- Where each competitor wins: be honest about scale, certifications, tools, geography, or product breadth
- Switching offer: "Send us your existing specification", "Request equivalent recommendation", "Book technical review", or "Get RFQ response in [timeframe]"

**SEO value:** These pages target high-intent search queries like "[competitor] alternatives" and "[target] vs [competitor]" which are bottom-of-funnel searches.

### 4.4 Switching Narrative Development

Create a compelling narrative for customers considering switching from each competitor:

```
SWITCHING NARRATIVE: [Competitor] → [Target]

Why customers switch:
  1. [Primary reason based on review mining]
  2. [Secondary reason]
  3. [Tertiary reason]

Switching story template:
  "Like many [audience], [customer name] started with [Competitor] because
   [initial appeal]. But after [time/event], they realized [pain point].
   After switching to [Target], they [specific result with numbers]."

Switching offer:
  - Free migration assistance
  - Extended trial for [Competitor] users
  - Matching or discounting pricing
  - Dedicated onboarding for switchers
  - Technical specification review
  - Equivalent product / part-number cross-reference
  - Compliance documentation pack
  - Distributor or account-manager handoff
```

---

## Phase 5: Monitoring and Ongoing Intelligence

### 5.1 Competitive Monitoring Checklist

Recommend ongoing monitoring activities:

- [ ] Set Google Alerts for each competitor name
- [ ] Follow competitors on social media platforms
- [ ] Subscribe to competitor newsletters
- [ ] Check competitor pricing pages monthly
- [ ] Monitor competitor review sites quarterly
- [ ] Track competitor content publishing (topics, frequency)
- [ ] Watch for competitor product launches and feature updates
- [ ] Monitor competitor job postings (reveals strategic priorities)
- [ ] Track competitor ad spend and creative (use Meta Ad Library, Google Ads Transparency)
- [ ] Review competitor backlink profiles quarterly

### 5.2 Competitive Response Playbook

Provide guidance on how to respond to competitor moves:

| Competitor Move | Response Strategy | Timeline |
|----------------|-------------------|----------|
| Price cut | Emphasize value and quality, not price war | 1 week |
| New feature launch | Assess relevance, communicate roadmap to customers | 2 weeks |
| Aggressive ad campaign | Double down on owned channels and retention | Ongoing |
| Negative comparison content | Create factual, balanced comparison content | 1 week |
| Major funding / acquisition | Reassure customers, emphasize stability and focus | 1-2 days |
| Customer reviews / complaints | Monitor for opportunities, address shared concerns | Ongoing |

---

## Output Format: COMPETITOR-REPORT.md

Write the full output to `COMPETITOR-REPORT.md`:

```markdown
# Competitive Intelligence Report: [Target Brand]
**URL:** [url]
**Date:** [current date]
**Competitors Analyzed:** [count]
**Competitive Position: [Strong/Moderate/Weak]**

---

## Executive Summary
[3-4 paragraphs covering competitive landscape, target's position,
biggest competitive advantage, biggest competitive threat, and
top 3 strategic recommendations]

---

## Competitor Overview

### Direct Competitors
[Summary table with name, URL, positioning, pricing, key differentiator]

### Indirect Competitors
[Summary table]

### Aspirational Competitors
[Summary table]

---

## Detailed Competitor Profiles

### [Competitor A Name]
[Full analysis: messaging, pricing, features, SWOT, social presence, reviews]

### [Competitor B Name]
[Full analysis]

[Repeat for each competitor]

---

## Comparison Tables

### Feature Comparison
[Full feature matrix]

### Pricing Comparison
[Full pricing matrix]

### Review Ratings
[Review intelligence matrix]

### Social Media Presence
[Platform comparison table]

---

## Positioning Map
[Visual positioning map with explanation]

---

## Content & SEO Gap Analysis
[Content gaps, keyword opportunities, comparison page strategy]

---

## SWOT Analysis — [Target Brand]
[Aggregate SWOT based on competitive intelligence]

---

## Strategic Recommendations

### Steal-Worthy Tactics
[5-10 tactics with implementation guidance]

### Differentiation Strategy
[Recommended positioning angles]

### Alternative Pages to Create
[Competitor vs pages with outlines]

### Switching Narratives
[Switching stories and offers for each major competitor]

---

## Competitive Monitoring Plan
[Ongoing monitoring checklist and response playbook]

---

## Next Steps
1. [Most critical competitive action]
2. [Second priority]
3. [Third priority]
```

---

## Terminal Output

```
=== COMPETITIVE INTELLIGENCE REPORT ===

Target: [name]
Competitors Analyzed: [count]
Competitive Position: [Strong/Moderate/Weak]

Competitive Landscape:
  Direct:      [Comp A] (Rating: X/5), [Comp B] (Rating: X/5)
  Indirect:    [Comp C], [Comp D]
  Aspirational: [Comp E]

Key Findings:
  Biggest Advantage: [specific advantage]
  Biggest Threat: [specific threat]
  Biggest Opportunity: [specific opportunity]

Feature Gaps: [X] features competitors have that target lacks
Content Gaps: [X] topics competitors cover that target doesn't
Pricing Position: [Above/At/Below] market average

Top 3 Actions:
  1. [action]
  2. [action]
  3. [action]

Full report saved to: COMPETITOR-REPORT.md
```

---

## Cross-Skill Integration

- If `MARKETING-AUDIT.md` exists, reference competitive positioning scores
- If `COPY-SUGGESTIONS.md` exists, use messaging analysis for differentiation
- If `FUNNEL-ANALYSIS.md` exists, compare funnel effectiveness with competitors
- If `AD-CAMPAIGNS.md` exists, use competitor intelligence for ad angles
- Suggest follow-up: `/ai-marketing:market-copy` for differentiated messaging, `/ai-marketing:market-ads` for competitive ad campaigns, `/ai-marketing:market-funnel` for conversion comparison

