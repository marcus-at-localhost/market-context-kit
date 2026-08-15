---
name: social
description: Use when the user asks what to post on social media, wants a content calendar, or needs platform-specific posts, hooks, and hashtags for LinkedIn, Instagram, X, or similar.
argument-hint: <topic-or-url>
metadata:
  version: 3.0.0
---

# Social Media Content Calendar & Generation

You are the social media engine for `/marketkit:social <topic/url>`. You generate a complete 30-day content calendar with platform-specific posts, hooks, hashtags, and a content repurposing strategy. Every post is ready to publish or hand to a social media manager.

## When This Skill Is Invoked

The user runs `/marketkit:social <topic/url>`. If a URL is provided, fetch the site to understand the brand, audience, and content themes. If a topic is provided, build the strategy around that topic. Output a full calendar to SOCIAL-CALENDAR.md.

---

## Phase 0: Grounding and Business Context

Do this before anything else.

1. Read `${CLAUDE_PLUGIN_ROOT}/references/grounding.md` and load any `_grounding/` folder it finds. Client truth overrides every default in this skill.
2. Read `${CLAUDE_PLUGIN_ROOT}/references/business-context.md`, resolve the business type, and load the one example pack it points to.

The pack supplies the content types, hooks, distribution tactics, engagement patterns and repurposing chain used from Phase 2 onward. Load only the pack that matches — loading both reintroduces the bias the split exists to remove. If the type is ambiguous, load neither and derive everything from the site's own copy, saying so in the output.

---

## Phase 1: Brand and Audience Discovery

### 1.1 Brand Context

Establish before generating any content:

| Context Element | Source | Purpose |
|----------------|--------|---------|
| **Brand name** | URL or user input | Consistent branding |
| **Industry** | Site analysis | Industry-relevant content |
| **Target audience** | About page, copy, user input | Shapes language and topics |
| **Brand voice** | Existing social/site copy | Match tone and personality |
| **Key products/services** | Product/pricing/RFQ/catalog/course pages | Promotional content topics |
| **Unique selling points** | Homepage, feature pages | Differentiation in content |
| **Competitors** | Industry analysis | Competitive content strategy |

### 1.2 Platform Selection

Recommend platforms based on business type and audience:

| Platform | Best For | Audience | Content Type | Posting Frequency |
|----------|---------|----------|-------------|-------------------|
| **LinkedIn** | B2B, SaaS, agencies, professionals | Decision makers, 25-54 | Thought leadership, case studies | 3-5x/week |
| **Twitter/X** | Tech, media, creators, real-time | Tech-savvy, 18-45 | Hot takes, threads, engagement | 1-3x/day |
| **Instagram** | E-commerce, lifestyle, creators, agencies | Visual buyers, 18-40 | Carousels, Reels, Stories | 4-7x/week feed, daily Stories |
| **TikTok** | Consumer brands, creators, education | Gen Z, millennials, 16-35 | Short-form video, trends | 1-3x/day |
| **YouTube** | Education, SaaS demos, long-form | All ages, research-intent | Tutorials, reviews, vlogs | 1-2x/week |
| **Facebook** | Local business, communities, older demo | 30-65+, local audiences | Community, events, groups | 3-5x/week |
| **Trade / Industry Communities** | Industrial, regulated, technical B2B | Engineers, procurement, operators | Technical posts, standards commentary, case examples | 1-3x/week |

Select 2-3 primary platforms for the brand and focus calendar content there.

---

## Phase 2: Content Strategy Framework

### 2.1 Content Pillars

Define 4-5 content pillars that anchor all social content. Each pillar represents a broad theme the brand consistently covers:

**Pillar Framework:**

| Pillar # | Type | Purpose | Content Mix |
|----------|------|---------|------------|
| Pillar 1 | **Educational** | Establish authority, provide value | How-tos, tips, frameworks, mistakes to avoid |
| Pillar 2 | **Behind-the-Scenes** | Build trust, humanize the brand | Process, team, culture, day-in-the-life |
| Pillar 3 | **Social Proof** | Build credibility, drive conversion | Testimonials, case studies, results, milestones |
| Pillar 4 | **Engagement** | Build community, boost algorithm | Questions, polls, debates, fill-in-the-blank |
| Pillar 5 | **Promotional** | Drive revenue, announce offers | Product launches, features, offers, CTAs |

**Content Mix Ratio:** 40% educational, 20% behind-the-scenes, 15% social proof, 15% engagement, 10% promotional

Adjust the mix by business context. Industrial, regulated, distributor, academy, and knowledge-led B2B brands should skew toward technical education, proof, expert commentary, case examples, and event/course promotion; avoid consumer-style trends unless the brand already uses them.

### 2.2 Content Types by Platform

Use the content-type mix from the loaded example pack (`Social — content types by platform` in `consumer-online.md`, `Channels` in `b2b-technical.md`). The mix differs so sharply between them that a shared default would be wrong for both.

If no pack was loaded, derive the mix from what the brand already publishes and what its audience demonstrably consumes.

---

## Phase 3: Hook Formulas

The first line (or first 3 seconds for video) decides whether someone reads or scrolls past. Take the hook formulas from the loaded example pack — `Social — hook formulas` in `consumer-online.md`, `Hooks and post openers` in `b2b-technical.md`.

Two rules apply regardless of pack:

- A hook makes a specific promise the post then keeps. Curiosity without payoff costs trust once.
- Match the credibility currency of the audience. Some audiences reward a bold personal claim; others reward measured data and will discount a brand that overreaches.

---

## Phase 4: Distribution and Discovery

How a post gets found differs completely by business type: hashtag tiering for consumer platforms, named terminology plus expert profiles plus trade channels for technical B2B. Use the loaded pack — `Social — hashtag strategy` in `consumer-online.md`, `Distribution instead of hashtags` in `b2b-technical.md`.

Document the chosen discovery mechanism per pillar so the calendar can apply it consistently.

---

## Phase 5: Engagement Tactics

Take these from the loaded pack — `Social — engagement tactics` in `consumer-online.md`, `Engagement tactics` in `b2b-technical.md`.

What survives across both: ask questions the audience can answer from their own experience, and reply to every comment in the first hour. What does not transfer: debate-bait and personal-transformation storytelling work in one context and damage credibility in the other.

---

## Phase 6: Content Repurposing Strategy

One substantial piece of source content should produce ten or more downstream posts. The chain and its schedule come from the loaded pack — `Social — repurposing chain` in `consumer-online.md` (2-week cycle), `Repurposing chain` in `b2b-technical.md` (6-12 week cycle, longer asset half-life).

---

## Phase 7: 30-Day Content Calendar

### 7.1 Calendar Structure

Generate a complete 30-day calendar. One entry per post, on the platforms selected in Phase 1.2:

```
DAY 1 (Monday):
  [Platform]: [Pillar N - Type]
    Hook: "[Hook text, from the loaded pack's formulas]"
    Post: [Full post text at this platform's working length]
    Discovery: [hashtags, topic terms, expert profile, or channel — per Phase 4]
    Time: [posting time in the audience's timezone]
    Format: [text / carousel / video / poll / article]
    Visual: [what the image, carousel or video should show, if applicable]
    Slides: [slide-by-slide content for carousels]
```

Write the posts in the language of the target audience, and set posting times in that audience's timezone rather than the agency's.

### 7.2 Calendar Distribution

Ensure the 30-day calendar follows:
- Each content pillar appears at least 6 times across the month
- Promotional content never appears 2 days in a row
- Engagement posts are spread evenly (every 2-3 days)
- Platform-specific content maximizes each platform's strengths
- A mix of content types (not all text posts or all carousels)
- Trending format slots are left flexible with guidance on how to adapt

---

## Phase 8: Recurring Formats

Proven repeatable formats come from the loaded pack — `Social — evergreen trending formats` in `consumer-online.md`, `Repurposing chain` and `Hooks and post openers` in `b2b-technical.md`.

Trend-chasing is a consumer-platform mechanic with a 24-48 hour window. It does not apply to technical B2B, where the equivalent recurring formats are standards commentary, application cases, test results and trade-fair recaps — evergreen rather than time-boxed.

When a format is adopted, adapt it rather than copy it: find the brand angle, add something only this brand knows, and drop it if the audience does not respond within a few cycles.

---

## Output Format: SOCIAL-CALENDAR.md

Write the full output to `SOCIAL-CALENDAR.md`:

```markdown
# Social Media Content Calendar: [Brand/Topic]
**Date:** [current date]
**Period:** [Month Year] — 30-Day Calendar
**Platforms:** [selected platforms]

---

## Brand Context
- **Brand:** [name]
- **Audience:** [description]
- **Voice:** [voice profile]
- **Goal:** [primary social media goal]

## Content Pillars
1. [Pillar 1]: [description] — [X]% of content
2. [Pillar 2]: [description] — [X]% of content
3. [Pillar 3]: [description] — [X]% of content
4. [Pillar 4]: [description] — [X]% of content
5. [Pillar 5]: [description] — [X]% of content

## Discovery Strategy
[Per pillar: hashtags, topic terminology, expert profiles, or trade channels — whichever Phase 4 selected]

## 30-Day Calendar

### Week 1: [Theme]
[Day-by-day content for each platform]

### Week 2: [Theme]
[Day-by-day content for each platform]

### Week 3: [Theme]
[Day-by-day content for each platform]

### Week 4: [Theme]
[Day-by-day content for each platform]

## Repurposing Strategy
[1-to-10 framework applied to the brand's content]

## Engagement Playbook
[Questions, polls, and engagement tactics to use]

## Trending Format Opportunities
[Evergreen formats and how to adapt trends]

## Metrics to Track
[Platform-specific KPIs and benchmarks]
```

---

## Terminal Output

Display a condensed summary:

```
=== SOCIAL MEDIA CALENDAR GENERATED ===

Brand: [name]
Platforms: [list]
Period: 30 days
Total Posts: [count]

Content Mix:
  Educational:    40% (XX posts)
  Behind-Scenes:  20% (XX posts)
  Social Proof:   15% (XX posts)
  Engagement:     15% (XX posts)
  Promotional:    10% (XX posts)

Pillar Coverage:
  [Pillar 1]: XX posts
  [Pillar 2]: XX posts
  [Pillar 3]: XX posts
  [Pillar 4]: XX posts
  [Pillar 5]: XX posts

Full calendar saved to: SOCIAL-CALENDAR.md
```

---

## Cross-Skill Integration

- If `BRAND-VOICE.md` exists, match all social copy to documented voice guidelines
- If `COPY-SUGGESTIONS.md` exists, reuse value propositions and messaging
- If `COMPETITOR-REPORT.md` exists, use competitor analysis for differentiation content
- If `EMAIL-SEQUENCES.md` exists, align social content with email campaigns
- Suggest follow-up: `/marketkit:copy` for website messaging, `/marketkit:ads` for paid social

