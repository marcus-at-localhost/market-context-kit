---
name: report
description: Use when the user wants prior audit and analysis outputs combined into one Markdown marketing report with a scorecard and prioritized action plan.
argument-hint: <url>
metadata:
  version: 3.0.0
---

# Marketing Report Generator (Markdown Format)

## Phase 0: Grounding and Business Context

Read `${CLAUDE_PLUGIN_ROOT}/references/grounding.md` and load any `_grounding/` folder it finds. Client documentation outranks every default in this skill, and any claim rules it contains bind the output. Name the loaded files at the top of what you produce.

State which grounding files informed the report, and flag any benchmark you quote as market-specific rather than universal.

Read `${CLAUDE_PLUGIN_ROOT}/references/business-context.md`, resolve the business type, and load the single matching example pack. **The scorecard in Step 2 is not business-type-neutral** — several factors are worded for a self-serve demand-generation model and score a different model as deficient when it is merely different. The pack supplies the yardsticks that make those factors measurable for the business at hand: its `Channels` cadence column and its `Lifecycle → sequence` table. Name the resolved business type and the loaded pack in the report's methodology section.

If the business type cannot be resolved, follow the fallback in `business-context.md`: load no pack, and treat every factor marked *pack-relative* in Step 2 as unscorable under "Channel purpose the rubric does not measure" below.

Also read `${CLAUDE_PLUGIN_ROOT}/references/output-location.md`. Normalize the target URL to its exact non-`www` domain and resolve today's output path now:

```
python "${CLAUDE_PLUGIN_ROOT}/scripts/resolve_audit_output.py" --purpose MARKETING-REPORT --scope <domain> --extension md
```

Use `python3` on macOS/Linux. Retain `audit_dir` — Step 1 below reads prior skill output from it (same exact domain scope only), and the final report is written to the returned `output_path`.

Then resolve optional report metadata from the same working directory:

```
python "${CLAUDE_PLUGIN_ROOT}/scripts/resolve_report_metadata.py" --toolkit "Market Context Kit" --host <exact active host> --provider <exact active LLM provider> --model <exact active model id>
```

Never guess a runtime value. Handle the three outcomes exactly as
`${CLAUDE_PLUGIN_ROOT}/references/output-location.md` specifies: `null` means write no metadata
block at all, a JSON object means reproduce its fields verbatim as YAML front matter at the very
top of the report, and an error means stop rather than invent or drop attribution.

Read `${CLAUDE_PLUGIN_ROOT}/references/search-context-integration.md`. If the user supplies a `SEARCH-CONTEXT.v1.json` path, or its discovery rule finds exactly one in the active audit folder's flat `data/` for the exact domain and, if requested, the exact reporting period, validate it before using any values. Keep the artifact optional and retain its path, reporting period, and source statuses for the data-source appendix.

---

## Skill Purpose
Generate a comprehensive, professionally formatted marketing report in Markdown. This skill compiles data from all previous audit and analysis results into a single, client-ready document with scores, findings, recommendations, and a prioritized action plan with revenue impact estimates.

## When to Use
- User wants a full marketing report for a client or their own business
- User has completed one or more audit skills and wants a compiled report
- User asks for a marketing assessment, scorecard, or analysis document
- Triggered by `/marketkit:report` or `/marketkit:report <domain>`

## How to Execute

### Step 1: Collect All Available Data
Before generating the report, check for any existing audit data from previous skill runs. Look only inside the `audit_dir` resolved in Phase 0, for the exact same domain scope — never search older audit folders.

**Possible data sources** (`MARKETKIT - <PURPOSE> - <domain>.md` unless noted):
- `MARKETING-AUDIT` -- from `/marketkit:audit`
- `COMPETITOR-REPORT` -- from `/marketkit:competitors`
- `SEO-AUDIT` -- from `/marketkit:seo`
- `AD-CAMPAIGNS` -- from `/marketkit:ads`
- `BRAND-VOICE` -- from `/marketkit:brand`
- `CONTENT-PLAN` -- from `/marketkit:content-plan`
- `COPY-SUGGESTIONS` -- from `/marketkit:copy`
- `EMAIL-SEQUENCES` -- from `/marketkit:emails`
- `FUNNEL-ANALYSIS` -- from `/marketkit:funnel`
- `LANDING-CRO` -- from `/marketkit:landing`
- `LAUNCH-PLAYBOOK` -- from `/marketkit:launch`
- `CLIENT-PROPOSAL` -- from `/marketkit:proposal`
- `SOCIAL-CALENDAR` -- from `/marketkit:social`
- Validated `data/SEARCHKIT - SEARCH-CONTEXT-V1-<period> - <domain>.json` -- optional measured query, page, engagement, and indexing evidence; apply `references/search-context-integration.md`

If no previous data exists, inform the user and offer to:
1. Run a quick audit first (recommended)
2. Generate a report based on available information (website URL, user-provided data)
3. Create a report template they can fill in

When valid Search Context evidence is present, use measured traffic, query, landing-page, engagement, and indexing fields only in the matching deep dives. Name the artifact period and provider beside material figures. Never invent absent analytics, treat `null` or failed sources as zero, convert search estimates into revenue facts, or infer form inquiries without an explicitly supplied form dataset. Search Context may prioritize recommendations but does not replace or retroactively alter existing audit scores.

### Step 2: Calculate the Marketing Scorecard

Score across 6 categories, each worth up to 100 points. The overall score is the weighted average.

#### Category 1: Website & Conversion (Weight: 25%)
Evaluate based on landing page analysis, CRO findings, and UX assessment.

| Factor | Points Available | Criteria |
|---|---|---|
| Page load speed | 15 | Under 2s = 15, Under 3s = 10, Under 5s = 5, Over 5s = 0 |
| Mobile responsiveness | 15 | Fully responsive = 15, Mostly = 10, Partially = 5, Not = 0 |
| Clear value proposition | 20 | Immediately clear = 20, Takes effort = 12, Vague = 5, Missing = 0 |
| CTA effectiveness | 20 | Strong and clear = 20, Present but weak = 12, Unclear = 5, Missing = 0 |
| Social proof | 15 | Multiple types = 15, Some = 10, Minimal = 5, None = 0 |
| Form optimization | 15 | Optimized = 15, Adequate = 10, Needs work = 5, Broken = 0 |

#### Category 2: SEO & Organic (Weight: 20%)
Evaluate based on SEO audit findings.

| Factor | Points Available | Criteria |
|---|---|---|
| Title tags & meta descriptions | 15 | Optimized = 15, Present = 10, Partial = 5, Missing = 0 |
| Header hierarchy (H1-H6) | 10 | Proper = 10, Mostly = 7, Needs work = 3, Missing = 0 |
| Content quality (E-E-A-T) | 25 | Excellent = 25, Good = 17, Average = 10, Poor = 3 |
| Technical SEO | 20 | No issues = 20, Minor issues = 13, Major issues = 7, Critical = 0 |
| Internal linking | 15 | Strategic = 15, Present = 10, Minimal = 5, None = 0 |
| Schema markup | 15 | Eligible rich-result types covered = 15, main types only = 10, minimal = 5, none where types are eligible = 0 |

Two notes on this category:

- **E-E-A-T bands rest on Google's helpful-content evidence** — who produced the content, how (including disclosed automation), and why it exists. A search-engine-first red flag (mass production across topics the site has no expertise in, undisclosed AI generation at scale, dates changed without the content changing) caps this factor at Poor whatever the surface quality looks like.
- **Schema is scored for rich-result eligibility and entity clarity**, not AI visibility. It is not a ranking factor, and Google states no schema.org markup is required for generative AI search. A page type with no eligible rich-result type is not counted against this factor.

#### Category 3: Content & Messaging (Weight: 15%)
Evaluate based on brand voice analysis and content audit.

| Factor | Points Available | Criteria |
|---|---|---|
| Brand voice consistency | 20 | Consistent = 20, Mostly = 13, Inconsistent = 7, No voice = 0 |
| Content quality | 25 | Expert-level = 25, Good = 17, Generic = 10, Poor = 3 |
| Content variety | 15 | Multiple formats = 15, Some = 10, Limited = 5, Single = 0 |
| Publishing frequency | 15 | Regular cadence = 15, Sporadic = 10, Rare = 5, None = 0 |
| Audience targeting | 25 | Precisely targeted = 25, Somewhat = 17, Broad = 10, Off-target = 3 |

#### Category 4: Social Media & Community (Weight: 15%)
Evaluate based on social media presence and engagement.

| Factor | Points Available | Criteria |
|---|---|---|
| Platform presence | 15 | Right platforms, active = 15, Present but inactive = 8, Missing key = 3 |
| Content quality | 25 | Engaging and on-brand = 25, Adequate = 15, Low quality = 7, Poor = 0 |
| Engagement rate | 25 | Above benchmark = 25, At benchmark = 17, Below = 10, Negligible = 3 |
| Posting consistency *(pack-relative)* | 15 | Matches the cadence the pack's `Channels` table gives for that channel = 15, roughly = 10, far below = 5, abandoned = 0 |
| Community building *(pack-relative)* | 20 | Fulfils the role the pack's `Channels` table assigns that channel = 20, partly = 13, present but off-role = 7, absent = 0 |

"Right platforms" and "on-brand" are resolved from the pack's `Channels` table and from grounding, not from a general-purpose channel list. A channel the pack does not list is not a gap.

#### Category 5: Email & Automation (Weight: 15%)
Evaluate based on email marketing assessment.

| Factor | Points Available | Criteria |
|---|---|---|
| List building mechanism | 20 | Multiple opt-ins = 20, One opt-in = 13, No visible opt-in = 5 |
| Email design & content | 20 | Professional and engaging = 20, Adequate = 13, Needs work = 7 |
| Lifecycle coverage *(pack-relative)* | 25 | Share of the **relevant** triggers in the pack's `Lifecycle → sequence` table that are served: most = 25, several = 15, few = 8, none = 0 |
| Segmentation *(pack-relative)* | 20 | Segments along the dimensions that govern this business's buying decision = 20, one dimension = 13, none = 5 |
| Sending cadence *(pack-relative)* | 15 | Matches the cadence the pack's `Channels` table gives for the owned email channel = 15, roughly = 10, erratic = 5, dormant = 0 |
| Deliverability signals | 15 | Strong = 15, Adequate = 10, Concerning = 5, Problems = 0 |

Category 5 totals 115 points; normalize to 100. Two notes that decide most of this category:

- **"Lifecycle coverage" replaced "Automation sequences".** Count triggers that exist in this business, not automation for its own sake. A model whose pack lists eight lifecycle triggers and serves three scores the same as any other model serving three of eight. Absence of a multi-step drip is only a deficiency where the pack's lifecycle table implies one.
- **Cadence is scored against the pack, never against an implied weekly ideal.** Where the pack gives a low-frequency cadence for the owned email channel, meeting it scores full marks. A low-frequency knowledge or news mail that hits its stated cadence is a complete answer, not a partial one — do not recommend increasing frequency, adding lead scoring, or adding behavioural drip sequences on the strength of this score alone.

#### Channel purpose the rubric does not measure

A channel sometimes serves a purpose none of the factors above measures — recruiting and employer branding are the common cases, and grounding may name others. Where **grounding or an explicit user statement** assigns a channel a purpose the rubric does not measure, that assignment outranks the rubric's assumed purpose (`references/grounding.md`, precedence rule).

Do not score such a category low. Instead:

1. **Exclude the category from the weighted total** and renormalize the remaining weights, exactly as for a category with no evidence at all. State the excluded weight.
2. **Assess it qualitatively against its actual purpose** in its deep-dive section: what the channel is for, whether it achieves that, and what is genuinely broken.
3. **Keep findings that survive the reframing.** Claim-rule violations, factual contradictions across channels, and broken mechanics are defects regardless of what a channel is for.
4. **Say which yardstick you did not apply, and why**, so the omission is legible rather than silent.

Never fill an excluded category with a midpoint score. A guessed number is indistinguishable from a measured one once it enters the weighted total.

#### Category 6: Paid Advertising (Weight: 10%)
Evaluate based on ad account audit (if applicable).

| Factor | Points Available | Criteria |
|---|---|---|
| Campaign structure | 20 | Well-organized = 20, Adequate = 13, Messy = 7, None = 0 |
| Targeting quality | 25 | Precise and layered = 25, Good = 17, Broad = 10, Wasteful = 3 |
| Ad creative quality | 25 | Compelling and varied = 25, Adequate = 17, Weak = 10, Poor = 3 |
| Landing page alignment | 15 | Perfect match = 15, Good = 10, Misaligned = 5, Broken = 0 |
| Tracking & attribution | 15 | Comprehensive = 15, Basic = 10, Minimal = 5, Missing = 0 |

#### Overall Score Calculation
```
Overall Score = (Website * 0.25) + (SEO * 0.20) + (Content * 0.15) + (Social * 0.15) + (Email * 0.15) + (Paid * 0.10)
```

**When a category is excluded** — no evidence at all, or a channel purpose the rubric does not
measure — drop its weight from both sides instead of substituting a value:

```
Overall Score = sum(score_i * weight_i) / sum(weight_i)   over scored categories only
```

The same rule applies one level down. A **single factor** that cannot be assessed from the
available evidence — deliverability without access to the sending system is the usual case — is
dropped from its category's denominator rather than guessed, and the category is normalized over
the points that remain. Name the dropped factor and what evidence would make it scorable.

Report the divisor with the score (e.g. "57/100, weights normalized over 60%"), list every
excluded category with its weight and the reason, and say plainly what the remaining number
covers. A score built on three of six categories is a partial score and must not be presented as
a whole-marketing verdict.

**Score Interpretation:**
| Score Range | Rating | Meaning |
|---|---|---|
| 85-100 | Excellent | Marketing is a competitive advantage. Optimize and scale. |
| 70-84 | Good | Solid foundation with clear improvement opportunities. |
| 55-69 | Average | Functional but leaving significant growth on the table. |
| 40-54 | Below Average | Multiple areas need attention. Significant opportunity cost. |
| 0-39 | Critical | Marketing is actively hurting growth. Immediate action required. |

### Step 3: Write Category Deep-Dives

For each of the 6 categories, provide:

1. **Score and Rating** -- X/100 with interpretation
2. **Key Findings** -- 3-5 specific observations with evidence
3. **What's Working** -- Positive elements to preserve and build on
4. **Gaps and Issues** -- Problems identified with severity ratings
5. **Recommendations** -- Specific, actionable improvements ranked by impact
6. **Revenue Impact Estimate** -- Estimated financial impact of implementing recommendations

**Revenue Impact Estimation Framework:**
```
Impact = (Estimated traffic change * Conversion rate change * Average deal value) * Confidence factor

Example:
- Current monthly traffic: 10,000
- Recommended SEO improvements could increase traffic 30%: +3,000 visits
- Current conversion rate: 2%, CRO could improve to 3%: +1% = +130 conversions
- Average deal value: $500
- Estimated monthly revenue impact: $65,000
- Confidence factor (conservative): 0.5
- Conservative estimate: $32,500/month additional revenue
```

### Step 4: Competitor Comparison Summary
If competitor data is available from `/marketkit:competitors`, include:

**Competitive Positioning Matrix:**
| Factor | Client | Competitor 1 | Competitor 2 | Competitor 3 |
|---|---|---|---|---|
| Website Quality | X/10 | X/10 | X/10 | X/10 |
| SEO Visibility | X/10 | X/10 | X/10 | X/10 |
| Content Quality | X/10 | X/10 | X/10 | X/10 |
| Social Presence | X/10 | X/10 | X/10 | X/10 |
| Overall Position | Xth/4 | Xth/4 | Xth/4 | Xth/4 |

**Competitive Advantages:** What the client does better
**Competitive Gaps:** Where competitors outperform the client
**Opportunities:** Spaces competitors are not addressing

### Step 5: Content Quality Assessment
Summarize content findings across all channels:

- **Website copy** -- Clarity, persuasiveness, brand alignment
- **Blog content** -- Depth, expertise, SEO optimization, publishing cadence
- **Social media content** -- Engagement quality, brand consistency, platform optimization
- **Email content** -- Subject line effectiveness, body copy quality, CTA strength
- **Ad creative** -- Messaging clarity, visual quality, offer presentation

### Step 6: Conversion Optimization Summary
Compile all conversion-related findings:

- **Primary conversion paths** -- How visitors become customers
- **Funnel leaks** -- Where potential customers drop off
- **CRO quick wins** -- Changes that can be implemented immediately
- **Testing opportunities** -- A/B tests recommended with hypotheses
- **Benchmark comparison** -- Current rates vs industry standards

### Step 7: SEO Snapshot
Summarize SEO health in a scannable format:

```
SEO Health Snapshot:
- Title Tags: [Optimized / Needs Work / Missing]
- Meta Descriptions: [Optimized / Needs Work / Missing]
- H1 Tags: [Proper / Issues / Missing]
- Image Alt Text: [Complete / Partial / Missing]
- Page Speed: [Fast / Moderate / Slow]
- Mobile-Friendly: [Yes / Partially / No]
- Schema Markup: [Present / Partial / Missing]
- Robots.txt: [Configured / Issues / Missing]
- Sitemap: [Present / Issues / Missing]
- HTTPS: [Yes / No]
- Core Web Vitals: [Pass / Needs Work / Fail]
```

`Schema Markup` reports rich-result eligibility and entity clarity, not AI visibility. If the client
asks why it matters, that is the answer — not "so AI can understand your site".

### Step 8: Build the Prioritized Action Plan

Organize all recommendations into three tiers:

#### Quick Wins (Implement This Week)
High impact, low effort changes. These should be implementable within 1-5 business days.

Format each item as:
```
- [ ] [Action item]: [Specific description]
  - Impact: [HIGH/MEDIUM/LOW]
  - Effort: [1-5 hours]
  - Expected Result: [Specific outcome]
  - Revenue Impact: [$X/month estimated]
```

#### Medium-Term (Implement This Month)
Moderate impact, moderate effort. These require 1-4 weeks.

#### Strategic (Implement This Quarter)
High impact, high effort. These are foundational changes that require planning and sustained effort.

### Step 9: Build the 30-60-90 Day Roadmap

**Days 1-30: Foundation & Quick Wins**
- Week 1: Implement all quick wins from the action plan
- Week 2: Set up tracking and analytics baseline
- Week 3: Begin medium-term improvements
- Week 4: First performance review and adjustment

**Days 31-60: Growth & Optimization**
- Week 5-6: Launch core campaign improvements
- Week 7: A/B testing program begins
- Week 8: Content strategy implementation

**Days 61-90: Scale & Expand**
- Week 9-10: Scale what's working, cut what isn't
- Week 11: Expand to new channels or campaigns
- Week 12: Comprehensive review, update strategy for next quarter

### Step 10: Appendix

Include methodology notes so the client understands how scores were derived:

**Scoring Methodology:**
- How each category was evaluated
- Data sources used
- Benchmarks referenced
- Limitations and assumptions
- Date of analysis

**Tools Used:**
- List any tools or scripts used in the analysis
- Reference to scripts/analyze_page.py if used
- If used, name `SEARCH-CONTEXT.v1.json`, its period, source statuses, and the Search Context Kit as an optional evidence source

**Glossary:**
- Define marketing terms that a non-marketer client may not know
- Keep it relevant to terms used in the report

## Output Format: MARKETKIT - MARKETING-REPORT - <domain>.md

Write the exact `output_path` resolved in Phase 0 (`${CLAUDE_PLUGIN_ROOT}/references/output-location.md`) with:

```markdown
[YAML front matter from the Phase 0 metadata resolver — exact shape in references/output-location.md. Omit the whole block when the resolver returned null.]
# Marketing Report
## [Company/Domain Name]
### Date: [Date]

---

## Executive Summary

### Overall Marketing Score: [X/100] -- [Rating]

[2-3 paragraph summary covering: current state assessment, top 3 findings, estimated revenue impact of implementing recommendations, and recommended first steps]

### Score Breakdown
| Category | Score | Rating |
|---|---|---|
| Website & Conversion | X/100 | [Rating] |
| SEO & Organic | X/100 | [Rating] |
| Content & Messaging | X/100 | [Rating] |
| Social Media | X/100 | [Rating] |
| Email & Automation | X/100 | [Rating] |
| Paid Advertising | X/100 | [Rating] |
| **Overall** | **X/100** | **[Rating]** |

### Top 3 Priority Actions
1. [Most impactful recommendation with revenue estimate]
2. [Second most impactful recommendation]
3. [Third most impactful recommendation]

---

## Detailed Findings

### 1. Website & Conversion [X/100]
[Deep-dive analysis with findings, what's working, gaps, recommendations]

### 2. SEO & Organic [X/100]
[Deep-dive analysis]

### 3. Content & Messaging [X/100]
[Deep-dive analysis]

### 4. Social Media [X/100]
[Deep-dive analysis]

### 5. Email & Automation [X/100]
[Deep-dive analysis]

### 6. Paid Advertising [X/100]
[Deep-dive analysis]

---

## Competitor Comparison
[Matrix and analysis]

---

## SEO Snapshot
[Health checklist]

---

## Conversion Optimization Summary
[Funnel analysis and CRO recommendations]

---

## Revenue Impact Summary
| Recommendation | Estimated Monthly Impact | Confidence | Priority |
|---|---|---|---|
| [Rec 1] | $X,XXX | High/Medium/Low | 1 |
| [Rec 2] | $X,XXX | High/Medium/Low | 2 |
| ... | ... | ... | ... |
| **Total Estimated Impact** | **$XX,XXX/month** | | |

---

## Prioritized Action Plan

### Quick Wins (This Week)
- [ ] [Action items with impact and effort]

### Medium-Term (This Month)
- [ ] [Action items]

### Strategic (This Quarter)
- [ ] [Action items]

---

## 30-60-90 Day Roadmap
[Week-by-week plan]

---

## Appendix
### Methodology
### Tools Used
### Glossary
### Data Sources
```

## Key Principles
- This report should be impressive enough to use as a sales tool. A well-crafted marketing report can open the door to a client engagement.
- Always lead with insights and opportunities, not criticism. Frame everything through the lens of growth potential.
- Quantify everything possible. "$32,000/month in unrealized revenue" is more compelling than "you're leaving money on the table."
- Make the action plan so specific that someone could hand it to a junior marketer and they could execute it.
- Use professional formatting: consistent headers, tables for data, checkboxes for action items, clear visual hierarchy.
- If data from previous skills is available, reference specific findings. If not, be transparent about what's based on analysis vs estimation.
- The report should tell a story: Here's where you are, here's where you could be, here's how to get there, and here's what it's worth.

