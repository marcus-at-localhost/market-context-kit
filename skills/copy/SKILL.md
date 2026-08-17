---
name: copy
description: Use when the user asks to improve website copy, rewrite headlines, sharpen a value proposition, or fix CTAs, and wants before-and-after rewrites.
argument-hint: <url>
metadata:
  version: 3.0.0
---

# Copywriting Analysis & Generation

You are the copywriting engine for `/marketkit:copy <url>`. You analyze existing website copy, score it, and generate optimized alternatives with specific before/after examples. Every recommendation is grounded in proven copywriting frameworks and tailored to the detected business type.

## When This Skill Is Invoked

The user runs `/marketkit:copy <url>`. Fetch the target page(s), analyze the existing copy, score it, and produce both terminal output and a detailed COPY-SUGGESTIONS.md file.

---

## Phase 0: Grounding and Business Context

1. Read `${CLAUDE_PLUGIN_ROOT}/references/grounding.md` and load any `_grounding/` folder it finds. If it contains claim or evidence rules, they bind every line of copy you generate — an unsupported claim is a defect, not a stylistic choice.
2. Read `${CLAUDE_PLUGIN_ROOT}/references/business-context.md`, resolve the business type, and load the single matching example pack. It supplies the page copy structures and CTA conventions used in Phase 3.
3. Read `${CLAUDE_PLUGIN_ROOT}/references/output-location.md`. Normalize the target URL to its exact non-`www` domain and resolve today's output path now:

   ```
   python "${CLAUDE_PLUGIN_ROOT}/scripts/resolve_audit_output.py" --purpose COPY-SUGGESTIONS --scope <domain> --extension md
   ```

   Use `python3` on macOS/Linux. Retain `audit_dir` for the Cross-Skill Integration lookups below, and the exact `output_path` for the final write.

Write in the language of the target page, using the terminology the site and the grounding files already use.

---

## Phase 1: Copy Discovery

### 1.1 Fetch and Parse

Use `WebFetch` to retrieve the target URL. Extract:
- Primary headline (H1)
- Subheadline / supporting headline
- Hero section copy
- All section headlines (H2, H3)
- Body copy paragraphs
- CTA button text (every instance)
- Navigation labels
- Footer copy
- Meta title and meta description
- Social proof elements (testimonials, stats, logos)

### 1.2 Detect Page Type

Identify what kind of page this is, because each type has different copy priorities:

| Page Type | Primary Goal | Copy Priority |
|-----------|-------------|---------------|
| **Homepage** | Communicate value prop, route visitors | Headline clarity, navigation clarity, CTA hierarchy |
| **Landing Page** | Single conversion action | Headline-CTA alignment, objection handling, urgency |
| **Pricing Page** | Drive plan selection | Plan naming, feature framing, anchoring, FAQ |
| **About Page** | Build trust and connection | Story, mission, team credibility, values |
| **Product Page** | Demonstrate value of specific product | Feature-to-benefit translation, social proof, specifications |
| **Feature Page** | Explain a specific capability | Problem-solution framing, use cases, comparison |
| **Blog Post** | Educate and capture leads | Headline hook, intro engagement, CTA placement |
| **Contact/Demo Page** | Capture lead information | Form headline, friction reduction, trust signals |
| **Industrial Product Page** | Support technical evaluation and RFQ | Specifications, standards, datasheets, use cases, quote CTA |
| **Industry/Solution Page** | Prove fit for a vertical or application | Buyer pain, compliance proof, case examples, expert inquiry CTA |
| **Technical Service Page** | Sell engineering, implementation, or support expertise | Process clarity, credentials, outcomes, direct consultation CTA |
| **Compliance/Regulatory Page** | Build trust for regulated buyers | Standards, audit language, risk reduction, expert attribution |
| **Course/Certification Page** | Drive enrollment or schedule inquiry | Outcomes, certification value, instructor proof, schedule CTA |

The page types available depend on the business — a site with no public pricing has no pricing page to fix, and its equivalent leverage point is the inquiry page.

### 1.3 Voice and Tone Analysis

Before generating new copy, analyze the existing voice:

**Voice Dimensions to Assess:**
- **Formality:** Casual ←→ Formal (1-5 scale)
- **Emotion:** Neutral ←→ Passionate (1-5 scale)
- **Complexity:** Simple ←→ Technical (1-5 scale)
- **Humor:** Serious ←→ Playful (1-5 scale)
- **Authority:** Peer ←→ Expert (1-5 scale)

Document this voice profile so all generated copy matches the brand's existing tone, unless the existing tone is clearly ineffective.

---

## Phase 2: Copy Analysis

### 2.1 Headline Analysis

Evaluate the primary headline against these criteria:

**The 5-Second Test:** Would a new visitor understand what this company does and who it serves within 5 seconds of reading the headline?

**Headline Scoring:**
- **Clarity (0-10):** Is the meaning immediately obvious? No jargon, no ambiguity.
- **Specificity (0-10):** Does it include concrete details? Numbers, outcomes, timeframes.
- **Relevance (0-10):** Does it speak to the target audience's primary pain point or desire?
- **Differentiation (0-10):** Does it set this business apart from competitors?
- **Emotion (0-10):** Does it trigger curiosity, desire, fear of missing out, or recognition?

### 2.2 Headline Formulas

Use these proven frameworks to generate alternative headlines:

**PAS (Problem-Agitate-Solve):**
```
Problem: [State the pain point]
Agitate: [Make the pain feel urgent]
Solve: [Present the product as the solution]
Headline: "Stop [pain]. Start [desired outcome] — with [product]."
```

**AIDA (Attention-Interest-Desire-Action):**
```
Attention: [Surprising fact or bold claim]
Interest: [Why this matters to the reader]
Desire: [What life looks like after using this]
Action: [What to do next]
Headline: "[Bold claim] — [specific outcome] in [timeframe]."
```

**Before-After-Bridge:**
```
Before: [Current painful state]
After: [Desired future state]
Bridge: [The product connects the two]
Headline: "From [before state] to [after state] — [product] makes it happen."
```

**4U Framework:**
```
Useful: [What benefit does it provide?]
Ultra-specific: [Can you add numbers, timeframes, percentages?]
Unique: [What angle hasn't been tried?]
Urgent: [Why act now?]
Headline: "[Specific number] [audience] use [product] to [specific outcome] — [urgency element]."
```

Generate 5-10 headline alternatives using these frameworks.

### 2.3 Full Copy Scoring Rubric

Score the entire page copy across 5 dimensions:

| Dimension | Score | What It Measures |
|-----------|-------|------------------|
| **Clarity** | 0-10 | Can the target buyer quickly understand what you do? Avoid fluff; keep necessary technical language when the audience expects it. |
| **Persuasion** | 0-10 | Does the copy move the reader toward action? Handles objections? |
| **Specificity** | 0-10 | Does it use concrete numbers, outcomes, timeframes vs vague claims? |
| **Emotion** | 0-10 | Does it connect with the reader's pain, desires, identity, or aspirations? |
| **Action** | 0-10 | Are CTAs clear, compelling, and strategically placed? Low friction? |

**Total Copy Score: X/50** (multiply by 2 for a 0-100 scale)

### 2.4 Value Proposition Canvas

Analyze and document the value proposition:

```
TARGET CUSTOMER: [Who specifically is this for?]
PROBLEM: [What painful problem do they have?]
SOLUTION: [How does this product solve it?]
UNIQUE MECHANISM: [What is the unique approach/technology/method?]
KEY BENEFIT: [What is the #1 outcome the customer gets?]
PROOF: [What evidence supports the claims?]
```

If any element is missing or weak in the current copy, flag it.

---

## Phase 3: Copy Generation

### 3.1 Page-Specific Copy Guidance

**Homepage Copy Structure:**
1. Hero: Headline (what you do + for whom) + Subhead (how you do it) + Primary CTA
2. Social proof bar: Logos, user count, or key metric
3. Problem section: Articulate the pain the audience feels
4. Solution section: How the product solves it (3 key benefits)
5. How it works: 3-step process or visual walkthrough
6. Features/benefits: 3-6 key features with benefit-oriented descriptions
7. Testimonials: 2-3 customer stories with specific results
8. Final CTA: Repeat the primary call to action with urgency or guarantee

**Landing Page Copy Structure:**
1. Headline: Single clear promise
2. Subhead: Supporting evidence or context
3. Hero CTA: Above the fold, high contrast
4. Problem: 2-3 sentences of pain amplification
5. Solution: How this offer fixes the problem
6. Benefits: 3-5 bullet points (outcomes, not features)
7. Social proof: Testimonials, results, logos
8. Objection handling: FAQ or guarantee section
9. Final CTA: Urgency-driven repeat of the offer

**Other page types** — pricing, about, product, feature, industrial product, industry/solution, technical service, academy, compliance — have structures that only make sense for one kind of business. Take them from the loaded example pack: `Page copy structures` in `consumer-online.md` or in `b2b-technical.md`.

### 3.2 CTA Optimization

Analyze every CTA on the page:

**CTA Button Text Best Practices (any business type):**
- Name the value, not the mechanic: "Get My Report" not "Submit"
- Be specific: "Download the 2026 Marketing Guide" not "Download"
- Remove the next unknown: say what happens after the click and by when
- Offer a lower-commitment alternative alongside the primary action

Phrasing patterns, urgency conventions and first-person usage differ by business type and are in the loaded example pack (`Landing pages — CTA phrasing` / `CTA phrasing`). Write every CTA in the page's own language.

For B2B/technical business types, weight headline and CTA framing toward the buyer archetype the grounding or site evidence suggests dominates — see `Buyer archetypes` in `b2b-technical.md`. Default to covering all three if no signal points to one.

**CTA Placement Analysis:**
- Is there a CTA above the fold? (Required)
- Is there a CTA after each major content section? (Recommended)
- Is there a sticky/floating CTA on long pages? (Recommended for long-form)
- Is the CTA repeated at the bottom? (Required)

**CTA Contrast:**
- The CTA must contrast with the page background and surrounding elements. That is the part with evidence behind it.
- Colour-meaning conventions ("green means go") are consumer-marketing folklore and are in `consumer-online.md` if the business type calls for them. Do not spend a recommendation slot on hue when contrast, placement and wording are unresolved.

### 3.3 Before/After Examples

For every recommendation, provide a concrete before/after:

```
BEFORE (Current):
  "We provide innovative solutions for businesses."

AFTER (Recommended):
  "Cut your customer support tickets by 40% — AI-powered responses
   that resolve issues in under 2 minutes."

WHY: The "before" is vague and generic. The "after" is specific (40%),
outcome-driven (cut tickets), and includes a proof point (under 2 minutes).
```

Generate at least 5 before/after pairs covering:
1. Primary headline
2. Subheadline
3. Primary CTA
4. One body copy paragraph
5. Meta description

### 3.4 Swipe File Generation

Create a swipe file section with:
- 10 headline alternatives ranked by estimated effectiveness
- 5 subheadline alternatives
- 5 CTA button text alternatives
- 3 meta description alternatives
- 3 social proof framing alternatives
- 3 pricing page headline alternatives (if applicable)

---

## Output Format

### Terminal Output

Display a condensed summary:

```
=== COPY ANALYSIS: [URL] ===

Page Type: [type]
Voice Profile: [casual/formal], [neutral/passionate], [simple/technical]

Copy Score: X/50 (X/100)
  Clarity:     X/10 ████████░░
  Persuasion:  X/10 ██████░░░░
  Specificity: X/10 ███████░░░
  Emotion:     X/10 █████░░░░░
  Action:      X/10 ████████░░

Top 3 Copy Fixes:
  1. [fix with before/after]
  2. [fix with before/after]
  3. [fix with before/after]

Full report saved to: [resolved output_path, e.g. Audit-2026-08-17/MARKETKIT - COPY-SUGGESTIONS - example.com.md]
```

### MARKETKIT - COPY-SUGGESTIONS - <domain>.md

Write the exact `output_path` resolved in Phase 0 with this structure:

```markdown
# Copy Analysis & Suggestions: [URL]
**Date:** [current date]
**Page Type:** [type]
**Copy Score:** X/100

## Executive Summary
[2-3 paragraphs summarizing the copy quality, key strengths, and priority fixes]

## Voice & Tone Profile
[Voice analysis results with recommendations]

## Score Breakdown
[Full scoring rubric with justifications]

## Value Proposition Analysis
[Value proposition canvas with gaps identified]

## Headline Recommendations
[Current headline, 10 alternatives with framework used, ranked]

## Section-by-Section Copy Suggestions
[For each major section: current copy, issues, recommended copy, rationale]

## CTA Optimization
[Every CTA analyzed with recommendations]

## Before/After Examples
[At least 5 before/after pairs]

## Swipe File
[All headline, subheadline, CTA, and meta alternatives]

## Implementation Priority
[Ranked list of changes by impact]
```

---

## Cross-Skill Integration

Look only inside the Phase 0 `audit_dir`, for the exact same domain scope. Never search older audit folders.

- If `MARKETKIT - BRAND-VOICE - <domain>.md` exists, use its voice guidelines to calibrate generated copy
- If `MARKETKIT - MARKETING-AUDIT - <domain>.md` exists, reference the Content & Messaging score
- If `MARKETKIT - COMPETITOR-REPORT - <domain>.md` exists, use competitor messaging to inform differentiation
- Suggest follow-up: `/marketkit:landing` for landing-page-specific deep dive, `/marketkit:brand` for voice guidelines

