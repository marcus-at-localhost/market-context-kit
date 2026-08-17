---
name: funnel
description: Use when the user asks where visitors drop off, wants their sales or signup or RFQ funnel mapped and benchmarked, or asks why traffic is not converting into leads.
argument-hint: <url>
metadata:
  version: 3.0.0
---

# Sales Funnel Analysis & Optimization

You are the funnel analysis engine for `/marketkit:funnel <url>`. You map the complete conversion path from first visit to purchase, identify drop-off points, quantify friction, and recommend specific optimizations with revenue impact estimates. Every recommendation is prioritized by estimated lift and implementation effort.

## When This Skill Is Invoked

The user runs `/marketkit:funnel <url>`. Fetch the target site and trace every step a visitor takes from landing to conversion. Analyze each step for friction, clarity, and effectiveness. Output a complete analysis to FUNNEL-ANALYSIS.md.

---

## Phase 0: Grounding and Business Context

1. Read `${CLAUDE_PLUGIN_ROOT}/references/grounding.md` and load any `_grounding/` folder it finds.
2. Read `${CLAUDE_PLUGIN_ROOT}/references/business-context.md`, resolve the business type, and load the single matching example pack. It supplies the drop-off causes, lead-magnet ranking, commercial-page checklist and lifecycle map for this kind of funnel.
3. Read `${CLAUDE_PLUGIN_ROOT}/references/output-location.md`. Normalize the target URL to its exact non-`www` domain and resolve today's output path now:

   ```
   python "${CLAUDE_PLUGIN_ROOT}/scripts/resolve_audit_output.py" --purpose FUNNEL-ANALYSIS --scope <domain> --extension md
   ```

   Use `python3` on macOS/Linux. Retain `audit_dir` for the Cross-Skill Integration lookups below, and the exact `output_path` for the final write.

The conversion event itself differs: a signup or checkout in one context, a qualified request in the other. Everything downstream of that difference — what friction means, what a good lead magnet is, what the last step should promise — follows from the pack, not from this file.

---

## Phase 1: Funnel Discovery and Mapping

### 1.1 Identify the Funnel Type

Detect which funnel type the site uses:

| Funnel Type | Business Model | Typical Steps | Key Metric |
|-------------|---------------|---------------|------------|
| **Lead Gen** | Services, agencies, B2B | Landing page -> Form -> Thank you -> Nurture -> Sales call | Lead-to-close rate |
| **SaaS Trial** | SaaS products | Homepage -> Pricing -> Signup -> Onboarding -> Upgrade | Trial-to-paid rate |
| **SaaS Demo** | Enterprise SaaS | Homepage -> Features -> Demo request -> Sales call -> Close | Demo-to-close rate |
| **E-commerce** | Online stores | Product page -> Cart -> Checkout -> Upsell -> Thank you | Cart-to-purchase rate |
| **Webinar** | Courses, coaches, SaaS | Opt-in -> Confirmation -> Reminder -> Live -> Offer -> Checkout | Webinar-to-sale rate |
| **Application** | Premium services, programs | Info page -> Application form -> Review -> Interview -> Accept | Application-to-accept rate |
| **Community** | Memberships, communities | Landing -> Free trial/preview -> Engage -> Paid membership | Free-to-paid rate |
| **Content** | Media, publishers | Blog -> Email capture -> Nurture -> Premium content -> Subscribe | Reader-to-subscriber rate |
| **B2B RFQ** | Industrial, manufacturing, technical services | Homepage -> Product/Solution -> Datasheet/Proof -> RFQ/Inquiry -> Sales follow-up | Inquiry-to-opportunity rate |
| **Technical Catalog** | Suppliers, distributors, parts businesses | Search/category -> Product detail -> Datasheet/Stock -> Quote/order/portal | Product-to-RFQ or reorder rate |
| **Regulated Procurement** | Pharma, chemical, finance, healthcare, safety-critical B2B | Trust/compliance proof -> Solution page -> Technical validation -> Inquiry | Qualified inquiry rate |
| **Training Enrollment** | Academies, courses, certifications | Course page -> Schedule -> Instructor/proof -> Enrollment/contact | Enrollment completion rate |

### 1.2 Map Every Funnel Step

For each page in the funnel, document:

```
STEP [#]: [Page Name]
  URL: [url]
  Page Type: [landing/product/pricing/catalog/solution/datasheet/RFQ/cart/checkout/form/enrollment/thank-you]
  Primary Action: [what the user should do on this page]
  Next Step: [where the user should go next]
  Exit Points: [where users might leave instead]
  Friction Elements: [anything that slows or confuses]
  Trust Elements: [anything that builds confidence]
  Load Time: [estimated based on page complexity]
```

### 1.3 Visual Funnel Map

Create an ASCII funnel map showing the flow:

```
VISITOR JOURNEY MAP
===================

Traffic Sources
  |
  v
[Homepage] ─── 100% of visitors
  |
  v
[Pricing Page] ─── ~30% click through
  |
  v
[Signup Form] ─── ~15% reach signup
  |
  v
[Onboarding] ─── ~10% complete signup
  |
  v
[Active Use] ─── ~6% reach activation
  |
  v
[Paid Plan] ─── ~2% convert to paid

Overall: 2% visitor-to-paid conversion
```

Adjust this template to match the actual funnel discovered on the site.

---

## Phase 2: Page-by-Page Analysis

### 2.1 Analysis Framework

For each page in the funnel, score these dimensions:

| Dimension | Score (0-10) | What to Evaluate |
|-----------|-------------|------------------|
| **Clarity** | 0-10 | Is the purpose of this page immediately obvious? |
| **Continuity** | 0-10 | Does it logically continue from the previous step? |
| **Motivation** | 0-10 | Does it give enough reason to take the next action? |
| **Friction** | 0-10 | How easy is it to complete the desired action? (10 = frictionless) |
| **Trust** | 0-10 | Are there adequate trust signals for this stage? |

**Page Score = Average of all 5 dimensions (0-10)**

### 2.2 Common Drop-Off Points and Fixes

**Homepage to Next Step:**
| Drop-Off Cause | Detection Signal | Fix |
|----------------|-----------------|-----|
| Unclear value proposition | Vague headline, no specificity | Rewrite headline with specific outcome |
| No clear CTA | Multiple equal-weight CTAs, CTA below fold | Single primary CTA above the fold |
| Slow load time | Heavy images, excessive scripts | Optimize images, defer non-critical JS |
| Poor mobile experience | Text too small, buttons too close | Mobile-first responsive redesign |

**Conversion-step drop-off** — pricing, signup and checkout for self-serve businesses; RFQ, inquiry and catalog pages for request-led ones. The cause-signal-fix tables are in the loaded example pack: `Funnel — drop-off causes and fixes` in `consumer-online.md` or `Funnel — friction causes and fixes` in `b2b-technical.md`.

Work through every table in the pack against the actual funnel steps mapped in Phase 1, and record which causes are present with the evidence that shows it.

### 2.3 Lead Magnet Effectiveness

If the funnel includes a lead magnet, evaluate:

**Lead Magnet Scoring:**
| Criteria | Score (0-10) | Evaluation |
|----------|-------------|------------|
| **Relevance** | 0-10 | Does it directly address the target audience's main pain? |
| **Specificity** | 0-10 | Is it a specific deliverable (not vague "free guide")? |
| **Perceived value** | 0-10 | Would the buyer trade their contact details for it? |
| **Time to value** | 0-10 | How quickly does it help — minutes for consumer, one evaluation cycle for technical |
| **Product alignment** | 0-10 | Does it naturally lead toward the commercial action? |
| **Opt-in friction** | 0-10 | Is the form simple, and is anything gated that should not be? |

**Ranking by effectiveness** differs sharply by business type — see `Lead magnets` in the loaded pack. Note that gating is itself a decision: a datasheet behind a form loses more qualified technical buyers than it captures.

---

## Phase 3: Funnel Metrics and Benchmarks

### 3.1 Key Funnel Metrics

Calculate (or estimate based on industry benchmarks) these metrics:

```
FUNNEL METRICS
==============

Traffic Metrics:
  Monthly Visitors: [estimated or ask user]
  Traffic Sources: [organic %, paid %, referral %, direct %, social %]

Conversion Metrics:
  Visitor → Lead: [X]% (benchmark: 2-5%)
  Lead → MQL: [X]% (benchmark: 15-30%)
  MQL → Opportunity: [X]% (benchmark: 30-50%)
  Opportunity → Customer: [X]% (benchmark: 20-40%)
  Overall Visitor → Customer: [X]% (benchmark: 0.5-3%)

Revenue Metrics (state the currency once, use the client's):
  Average Order Value (AOV): [X]
  Customer Lifetime Value (LTV): [X]
  Customer Acquisition Cost (CAC): [X]
  LTV:CAC Ratio: [X]:1 (target: 3:1 or higher)
  Revenue Per Visitor (RPV): [X]
  For quoted-price businesses, substitute average order value with average
  contract or annual supply value, and add inquiry-to-quote and quote-to-win rates.

Engagement Metrics:
  Pages Per Session: [X]
  Average Session Duration: [X] min
  Bounce Rate: [X]% (benchmark: 30-60%)
```

### 3.2 Revenue-Per-Visitor Calculation

This is the single most important metric for funnel optimization:

```
RPV = (Monthly Revenue) / (Monthly Visitors)

Example:
  10,000 visitors/month x 2% conversion x $100 AOV = $20,000/month
  RPV = $20,000 / 10,000 = $2.00 per visitor

If we improve conversion from 2% to 2.5%:
  10,000 x 2.5% x $100 = $25,000/month
  RPV = $2.50 per visitor
  Revenue lift = $5,000/month = $60,000/year
```

Use this framework to quantify the impact of every recommendation.

### 3.3 Funnel Benchmarks by Type

Published US-market figures. Use them for orientation and name that caveat when you quote one — long-cycle B2B, regulated procurement and non-US markets deviate enough that a "below benchmark" verdict means nothing on its own. Where the client has its own historical data, that data wins.

| Funnel Type | Good Conversion | Great Conversion | Elite Conversion |
|-------------|----------------|-----------------|-----------------|
| Lead Gen (form) | 3-5% | 5-10% | 10-20% |
| SaaS Free Trial | 2-5% | 5-10% | 10-15% |
| Trial to Paid | 10-15% | 15-25% | 25-40% |
| E-commerce (browse to buy) | 1-3% | 3-5% | 5-8% |
| Cart to Purchase | 50-60% | 60-70% | 70-80% |
| Webinar Registration | 20-40% | 40-55% | 55-70% |
| Webinar Attendance | 30-40% | 40-55% | 55-65% |
| Webinar to Sale | 2-5% | 5-10% | 10-20% |
| Cold Email Reply | 3-5% | 5-10% | 10-20% |
| Demo to Close | 15-25% | 25-40% | 40-60% |
| B2B RFQ Form | 1-3% | 3-6% | 6-10% |
| Datasheet Download to Inquiry | 5-10% | 10-20% | 20-30% |
| Course Enrollment Page | 3-8% | 8-15% | 15-25% |

---

## Phase 4: Optimization Recommendations

### 4.1 Prioritization Matrix

Rank every recommendation using this framework:

| Priority | Impact | Effort | When to Implement |
|----------|--------|--------|-------------------|
| **P1 (Do Now)** | High impact (>10% lift) | Low effort (<1 day) | This week |
| **P2 (Plan)** | High impact (>10% lift) | Medium effort (1-5 days) | This month |
| **P3 (Schedule)** | Medium impact (5-10% lift) | Low effort (<1 day) | This month |
| **P4 (Backlog)** | Medium impact (5-10% lift) | High effort (5+ days) | This quarter |
| **P5 (Nice to Have)** | Low impact (<5% lift) | Any effort | When resources allow |

### 4.2 Funnel-Stage-Specific Optimizations

**Top of Funnel (Awareness to Interest):**
- Headline A/B testing (expected lift: 10-30%)
- Social proof placement (expected lift: 5-15%)
- Page speed optimization (expected lift: 5-20%)
- Exit-intent popup with lead magnet (expected lift: 2-5% of exiting visitors)

**Middle of Funnel (Interest to Consideration):**
- Case study and testimonial pages (expected lift: 10-20%)
- Feature comparison pages (expected lift: 5-15%)
- Interactive product demos (expected lift: 15-30%)
- Datasheets, calculators, selectors, configurators, technical proof, and compliance guides (expected lift: 10-30% for technical buyers)
- Retargeting email sequences (expected lift: 10-25%)

**Bottom of Funnel (Consideration to Purchase/RFQ/Enrollment):**
- Pricing, RFQ, inquiry, enrollment, or quote-flow redesign (expected lift: 10-25%)
- Checkout/signup/RFQ/enrollment friction reduction (expected lift: 5-15%)
- Risk reduction (guarantees, trials, certifications, standards, delivery SLA, sample request, named expert access) (expected lift: 10-20%)
- Authentic urgency elements (regulatory deadlines, event dates, lead times, limited course seats, capacity) (expected lift: 5-15%)
- Cart/order/RFQ abandonment recovery (expected recovery: 5-15% of abandoned flows)

**Post-Purchase (Retention and Expansion):**
- Onboarding email sequence (expected impact: 10-20% reduction in churn)
- Upsell/cross-sell on thank-you page (expected lift: 5-15% of AOV)
- Referral program (expected lift: 5-15% new customers)
- NPS survey at 30 days (identifies at-risk customers)

### 4.3 Commercial Action Page Optimization

Since pricing, RFQ, inquiry, quote, and enrollment pages are often the highest-leverage optimization point:

Use the checklist from the loaded example pack — `Pricing page checklist` in `consumer-online.md` when public pricing exists, `RFQ / inquiry / enrollment page checklist` in `b2b-technical.md` when pricing is quoted or sales-led. A site can have both; audit each against its own checklist.

### 4.4 Checkout/Signup Flow Optimization

**Friction Audit:**
- Count total form fields (target: 3-5 for lead gen, 5-8 for checkout)
- Count total steps (target: 1-3 steps maximum)
- Check for progress indicators on multi-step forms
- Verify mobile form usability (input types, autocomplete, button size)
- Look for unnecessary required fields
- Check for inline validation (real-time error feedback)
- Verify error messages are helpful (not just "Invalid input")
- Check if users can save progress and return later

---

## Phase 5: Nurture Sequence Integration

### 5.1 Funnel-to-Email Mapping

For each funnel stage, recommend the appropriate follow-up sequence. The stage-to-sequence map is in the loaded example pack — `Lifecycle → email sequence` in `consumer-online.md`, `Lifecycle → sequence` in `b2b-technical.md`.

The stages themselves differ: there is no trial user in a quoted-price business, and no dormant-account reactivation play in a self-serve one.

For B2B/technical business types, sequence intensity should account for archetype mix — see `Buyer archetypes` in `b2b-technical.md`. An Adapter-heavy funnel needs a human step before automation; a Seeker-heavy funnel needs every stage automation-ready with no gaps.

### 5.2 Traffic Source Alignment

Different traffic sources need different funnel entry points:

| Traffic Source | Intent Level | Best Entry Point | Recommended Funnel |
|---------------|-------------|-----------------|-------------------|
| Branded search | High | Pricing / signup / RFQ / contact page | Short (direct to trial/buy/inquiry) |
| Non-branded search | Medium | Blog / landing page | Medium (educate then convert) |
| Paid social | Low-Medium | Lead magnet / content | Long (capture, nurture, convert) |
| Referral | Medium-High | Homepage / product page | Medium (trust is pre-built) |
| Direct | High | Homepage | Short (they know you) |
| Email | Medium | Specific landing page | Targeted (match email topic) |
| Trade/directories | High | Solution page / catalog / RFQ page | Short (validate proof, then inquire) |

---

## Output Format: MARKETKIT - FUNNEL-ANALYSIS - <domain>.md

Write the full output to the exact `output_path` resolved in Phase 0:

```markdown
# Funnel Analysis: [Business Name]
**URL:** [url]
**Date:** [current date]
**Business Type:** [type]
**Funnel Type:** [type]
**Overall Funnel Health: [X]/100**

---

## Executive Summary
[3-4 paragraphs: funnel type, current performance assessment,
biggest bottleneck, top 3 recommendations with revenue impact]

---

## Funnel Map

[ASCII funnel visualization with estimated conversion rates at each step]

---

## Page-by-Page Analysis

### Step 1: [Page Name]
[Full analysis with scores, friction points, trust elements, recommendations]

### Step 2: [Page Name]
[Continue for each step]

---

## Funnel Metrics
[Current metrics vs benchmarks, with gaps highlighted]

## Revenue Impact Analysis
[RPV calculations, improvement scenarios]

## Optimization Recommendations

### Priority 1 — Do Now (This Week)
[Specific actions with expected lift]

### Priority 2 — Plan (This Month)
[Specific actions with expected lift]

### Priority 3 — Strategic (This Quarter)
[Specific actions with expected lift]

---

## Commercial Action Page Assessment
[Detailed pricing/RFQ/inquiry/enrollment page audit with checklist]

## Lead Magnet Assessment
[If applicable: scoring and recommendations]

## Email Nurture Integration
[Funnel-to-email mapping recommendations]

## Traffic Source Alignment
[Which traffic to send where]

## Next Steps
1. [Most critical action]
2. [Second priority]
3. [Third priority]
```

---

## Terminal Output

```
=== FUNNEL ANALYSIS COMPLETE ===

Business: [name]
Funnel Type: [type]
Steps: [count]
Funnel Health: [X]/100

Conversion Flow:
  Visitors     → Leads:     [X]% (benchmark: [X]%)
  Leads        → Next Step: [X]% (trial/RFQ/enrollment/opportunity benchmark: [X]%)
  Next Step    → Customer:  [X]% (benchmark: [X]%)
  Overall:                  [X]% (benchmark: [X]%)

Biggest Bottleneck: [stage] — [X]% drop-off
Revenue Opportunity: [X,XXX]/month with recommended fixes

Top 3 Fixes:
  1. [fix] — est. [X]% lift
  2. [fix] — est. [X]% lift
  3. [fix] — est. [X]% lift

Full analysis saved to: [resolved output_path, e.g. Audit-2026-08-17/MARKETKIT - FUNNEL-ANALYSIS - example.com.md]
```

---

## Cross-Skill Integration

Look only inside the Phase 0 `audit_dir`, for the exact same domain scope. Never search older audit folders.

- If `MARKETKIT - MARKETING-AUDIT - <domain>.md` exists, reference conversion scores
- If `MARKETKIT - COPY-SUGGESTIONS - <domain>.md` exists, apply copy improvements to funnel pages
- If `MARKETKIT - EMAIL-SEQUENCES - <domain>.md` exists, verify alignment with funnel stages
- If `MARKETKIT - COMPETITOR-REPORT - <domain>.md` exists, compare funnel effectiveness
- Suggest follow-up: `/marketkit:copy` for page-specific copy, `/marketkit:emails` for nurture sequences, `/marketkit:landing` for CRO deep dive

