---
name: emails
description: Use when the user asks for email sequences, welcome or nurture or onboarding flows, subject lines, newsletter copy, or email cadence and segmentation plans.
argument-hint: <topic-or-url>
metadata:
  version: 3.0.0
---

# Email Sequence Generation

You are the email marketing engine for `/marketkit:emails <topic/url>`. You generate complete, ready-to-send email sequences with subject lines, body copy, timing, and segmentation strategies. Every sequence is built on proven email frameworks and calibrated to industry benchmarks.

## When This Skill Is Invoked

The user runs `/marketkit:emails <topic/url>`. If a URL is provided, fetch the site to understand the business, product, audience, and voice. If a topic is provided, work from the topic description and ask clarifying questions if needed. Output complete sequences to EMAIL-SEQUENCES.md.

---

## Phase 0: Grounding and Business Context

1. Read `${CLAUDE_PLUGIN_ROOT}/references/grounding.md` and load any `_grounding/` folder it finds. Claim rules there bind every email you write.
2. Read `${CLAUDE_PLUGIN_ROOT}/references/business-context.md`, resolve the business type, and load the single matching example pack. It supplies the CTA ladder, subject-line angles and urgency conventions.
3. Read `${CLAUDE_PLUGIN_ROOT}/references/output-location.md`. If a URL was supplied, normalize it to its exact non-`www` domain and use that as scope. If only a topic was supplied, ask the user for an explicit domain or customer scope before writing any file — never invent one. The scope must contain only letters, numbers, dots, and hyphens. Resolve today's output path now:

   ```
   python "${CLAUDE_PLUGIN_ROOT}/scripts/resolve_audit_output.py" --purpose EMAIL-SEQUENCES --scope <scope> --extension md
   ```

   Use `python3` on macOS/Linux. Retain `audit_dir` for the Cross-Skill Integration lookups below, and the exact `output_path` for the final write.

Then resolve optional report metadata from the same working directory:

```
python "${CLAUDE_PLUGIN_ROOT}/scripts/resolve_report_metadata.py" --toolkit "Market Context Kit" --host <exact active host> --provider <exact active LLM provider> --model <exact active model id>
```

Never guess a runtime value. Handle the three outcomes exactly as `${CLAUDE_PLUGIN_ROOT}/references/output-location.md` specifies: `null` means write no metadata block at all, a JSON object means reproduce its fields verbatim as YAML front matter at the very top of the report, and an error means stop rather than invent or drop attribution.

Write the emails in the recipient's language, and check the compliance section in Phase 5 for the regime that actually applies to that market before drafting.

---

## Phase 1: Context Gathering

### 1.1 Business Understanding

Before writing any emails, establish:

| Context Element | How to Determine | Why It Matters |
| --- | --- | --- |
| **Business type** | Fetch URL or ask user | Determines sequence type and tone |
| **Target audience** | Infer from site copy or ask | Shapes language, pain points, examples |
| **Product/service** | Fetch product/pricing pages | Drives value propositions in emails |
| **Commercial model** | Check pricing, RFQ, catalog, contact, distributor, or enrollment path | Determines sequence length and CTA type |
| **Primary CTA** | Identify main conversion action | Every email builds toward this |
| **Lead magnet** | Check for download offers, free trials, datasheets, calculators, checklists, webinars, or course materials | Determines welcome sequence entry point |
| **Voice and tone** | Analyze existing copy | Emails must match brand voice |

### 1.2 Sequence Type Selection

Based on context, recommend the appropriate sequence(s):

| Sequence Type | When to Use | Emails | Goal |
| --- | --- | --- | --- |
| **Welcome** | New subscriber / lead magnet download | 5-7 | Build trust, deliver value, introduce product |
| **Nurture** | Warm leads not yet ready to buy | 6-8 | Educate, build authority, overcome objections |
| **Launch** | New product or feature release | 8-12 | Build anticipation, drive purchases |
| **Re-engagement** | Inactive subscribers (30-90 days) | 3-4 | Win back attention or clean list |
| **Onboarding** | New trial users or new customers | 5-7 | Drive activation, reduce churn, show value |
| **Cart Abandonment** | E-commerce abandoned checkout | 3-4 | Recover lost sales |
| **Cold Outreach** | B2B prospecting | 3-5 | Book meetings, start conversations |
| **RFQ Follow-Up** | Submitted inquiry, quote request, or technical form | 3-5 | Clarify requirements, accelerate sales handoff |
| **Datasheet Download Nurture** | Technical asset download | 4-6 | Educate, prove fit, drive expert consultation |
| **Regulatory Update Nurture** | Compliance/newsletter audience | 4-6 | Build authority, tie deadlines to assessment CTA |
| **Trade Show / Event Follow-Up** | Booth scans, webinar attendees, conference leads | 3-5 | Convert warm conversations into meetings |
| **Academy Enrollment** | Course interest or registration started | 3-5 | Fill seats, reduce schedule friction, prove certification value |

Generate at least 2 sequence types unless the user specifies one.

---

## Phase 2: Email Frameworks

### 2.1 Core Email Philosophy: One Email, One Job

Every email must have exactly ONE primary purpose:

- ONE main idea or story
- ONE call-to-action (secondary CTA optional but de-emphasized)
- ONE desired reader action

Never combine multiple asks in a single email. Violating this rule is the number one cause of low click-through rates.

### 2.2 Email Structure Frameworks

**Value Before Ask:**

```
Email 1: Pure value (no ask)
Email 2: Pure value (no ask)
Email 3: Value + soft mention of product
Email 4: Value + case study showing product results
Email 5: Direct ask with urgency
```

Use this for welcome and nurture sequences. The ratio should be approximately 3:1 value-to-ask.

**Story-Driven:**

```
Hook: Open with a story, observation, or surprising fact (2-3 sentences)
Bridge: Connect the story to the reader's situation (1-2 sentences)
Lesson: Extract the actionable insight (2-3 sentences)
CTA: Link the lesson to the next step (1 sentence + button/link)
```

Use this for nurture emails and any sequence targeting a sophisticated audience.

**Problem-Agitate-Solution (for direct response):**

```
Problem: "Are you struggling with [specific pain]?"
Agitate: "Every day you wait, [consequence]."
Solution: "[Product] solves this by [mechanism]. Here's how..."
CTA: [the next commercial step — see the loaded example pack]
```

Use this for launch emails and abandoned-conversion follow-ups. Take the closing CTA from the pack (`Email — worked CTAs and framings`): a trial or purchase in one context, a specification review or sample request in the other. Agitation also has a ceiling — with a technical buyer, overstating consequence reads as sales pressure and costs the reply.

### 2.3 Subject Line Optimization

**Subject Line Formulas:**

| Formula | Example | Best For |
| --- | --- | --- |
| **Number + Benefit** | "3 ways to double your conversion rate" | Educational content |
| **Curiosity Gap** | "The pricing mistake that cost me $50K" | Story-driven emails |
| **Direct Benefit** | "Your copy report is ready" | Delivery / welcome emails |
| **Personalization** | "[Name], your trial expires tomorrow" | Urgency / onboarding |
| **Question** | "Are you making this SEO mistake?" | Problem-awareness |
| **How-To** | "How to write landing pages that convert at 10%" | Educational content |
| **Social Proof** | "Why 5,000 marketers switched this month" | Nurture / launch |
| **Urgency** | "Last chance: 40% off ends at midnight" | Launch / cart abandonment |
| **Pattern Interrupt** | "I was wrong about email marketing" | Re-engagement |
| **Negative** | "Stop wasting money on ads that don't work" | Problem-awareness |

**Subject Line Rules:**

- Keep under 50 characters for mobile optimization (40 is ideal)
- Front-load the most important words
- Use numbers when possible (odd numbers outperform even)
- Avoid spam trigger words: "free," "guarantee," "act now," "limited time" in excess
- Personalize with first name in 20-30% of emails (not every one)
- Test emoji usage: one emoji can increase open rates 2-5%, but overuse decreases them
- Preview text (preheader) is as important as the subject line — always write both

### 2.4 Send Timing and Cadence

**Recommended Cadence by Sequence Type:**

| Sequence | Day 1 | Day 2 | Day 3 | Day 4 | Day 5 | Day 6 | Day 7+ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Welcome** | Email 1 | Email 2 | — | Email 3 | — | Email 4 | Email 5 (Day 8) |
| **Nurture** | Email 1 | — | Email 2 | — | — | Email 3 | Every 3-4 days |
| **Launch** | Announce | — | Teaser | — | Open Cart | Reminder | Close Cart |
| **Re-engagement** | Email 1 | — | — | — | Email 2 | — | Email 3 (Day 10) |
| **Onboarding** | Email 1 | Email 2 | — | Email 3 | — | Email 4 | Email 5 (Day 10) |
| **Cart Abandon** | 1hr | — | 24hr | — | 72hr | — | — |
| **Cold Outreach** | Email 1 | — | — | Email 2 | — | — | Email 3 (Day 10) |

**Best Send Times (general benchmarks):**

- B2B: Tuesday-Thursday, 9-11 AM recipient's local time
- B2C: Tuesday-Thursday, 10 AM or 7-9 PM recipient's local time
- E-commerce: Thursday-Sunday for promotional, Tuesday-Wednesday for educational
- Avoid: Monday mornings, Friday afternoons, weekends (except e-commerce)

---

## Phase 3: Sequence Templates

### 3.1 Welcome Sequence (5-7 Emails)

```
Email 1 (Immediate): DELIVER + INTRODUCE
  Subject: "Your [lead magnet] is ready — plus a quick question"
  Body: Deliver the promised resource. Set expectations for future emails.
        Ask one engaging question to prompt a reply (boosts deliverability).
  CTA: Download/access the lead magnet

Email 2 (Day 1): CREDIBILITY
  Subject: "Why [brand] exists" / "[Standard or problem]: how we approach it"
  Body: Origin story for consumer and founder-led brands; capability, lab,
        certifications and named experts for technical ones.
  CTA: Read the full story / reply with your biggest challenge

Email 3 (Day 3): EDUCATE + AUTHORITY
  Subject: "[Number] [topic] mistakes that cost you [outcome]"
  Body: Educational content that demonstrates expertise.
        Solve a real problem without requiring the product.
  CTA: Read the full guide / watch the video

Email 4 (Day 5): PROOF + SOFT PITCH
  Subject: "How [customer] achieved [specific result]"
  Body: Case study or testimonial. Specific numbers and timeline.
        Natural transition to how the product helped.
  CTA: [proof-stage CTA from the loaded pack]

Email 5 (Day 7): DIRECT PITCH + OBJECTION HANDLING
  Subject: "Is [product] right for you? (honest assessment)"
  Body: Direct pitch. Address the top 3 objections for this buyer.
        Include the risk reducer this buyer recognizes — refund-style
        guarantee, or certification, test data and response commitment.
  CTA: [primary commercial CTA from the loaded pack]

Email 6 (Day 10, optional): DEADLINE
  Subject: [only if a real deadline exists]
  Body: Send this only when something genuinely expires — an offer window,
        a course date, a standards transition, a lead-time window.
        Manufactured urgency costs more trust than it converts, and costs
        most with technical buyers.
  CTA: [deadline-linked action]

Email 7 (Day 14, optional): TRANSITION
  Subject: "What's next for you and [brand]"
  Body: Set expectations for ongoing emails. Segment by asking
        what topics they care about most.
  CTA: Click to choose your email preferences
```

### 3.2 Cold Outreach Sequence (3-5 Emails)

```
Email 1 (Day 1): RELEVANCE + VALUE
  Subject: "[Mutual connection/trigger event] + quick question"
  Body: 3-4 sentences max. Lead with research about their company.
        Offer specific value (not a generic pitch).
  CTA: "Would it make sense to chat for 15 minutes this week?"

Email 2 (Day 4): FOLLOW-UP + SOCIAL PROOF
  Subject: "Re: [original subject]"
  Body: 2-3 sentences. Reference Email 1. Share a relevant case study
        result that matches their situation.
  CTA: "I put together a quick breakdown of how this could work for [company]. Want me to send it over?"

Email 3 (Day 8): BREAKUP + VALUE DROP
  Subject: "Closing the loop on [topic]"
  Body: 2-3 sentences. Acknowledge they're busy. Offer a no-strings
        resource (report, benchmark, article). Make it easy to say no.
  CTA: "Either way, here's [resource] — thought you'd find it useful."

Email 4 (Day 14, optional): RE-APPROACH
  Subject: "[New angle/trigger event]"
  Body: New angle based on recent news, job posting, or company change.
        Different value proposition from Email 1.
  CTA: "Saw [trigger event] — this might be relevant now."

Email 5 (Day 21, optional): FINAL BREAKUP
  Subject: "Not the right time?"
  Body: 1-2 sentences. Graceful close. Leave the door open.
  CTA: "If timing changes, here's my calendar link: [link]"
```

### 3.3 Cart Abandonment Sequence (3-4 Emails)

```
Email 1 (1 hour after abandonment): REMINDER
  Subject: "You left something behind"
  Body: Show the abandoned product(s) with image. Simple reminder,
        no discount yet. Address potential technical issues.
  CTA: "Complete your order"

Email 2 (24 hours): OBJECTION HANDLING
  Subject: "Still thinking about [product]?"
  Body: Address top purchase objections (shipping, returns, quality).
        Include a customer review or testimonial.
  CTA: "Complete your order — free shipping included"

Email 3 (72 hours): INCENTIVE
  Subject: "[Name], here's 10% off your cart"
  Body: Time-limited discount. Create urgency with expiration.
        Restate the key product benefits.
  CTA: "Use code SAVE10 — expires in 24 hours"

Email 4 (7 days, optional): LAST CHANCE
  Subject: "Your cart is about to expire"
  Body: Final reminder. Cart will be cleared. Last chance for discount.
  CTA: "Save your cart before it's gone"
```

---

## Phase 4: Segmentation and Personalization

### 4.1 Segmentation Strategies

Recommend segments based on the business type:

| Segment Basis | Examples | How to Use |
| --- | --- | --- |
| **Behavior** | Page visits, clicks, downloads, purchases | Trigger relevant follow-up sequences |
| **Engagement** | Open rate, click rate, recency | Separate engaged vs dormant subscribers |
| **Source** | Organic, paid, referral, social | Tailor welcome sequence to acquisition channel |
| **Stage** | Lead, trial, customer, churned | Different sequences for each lifecycle stage |
| **Technical intent** | Datasheet download, RFQ, selector use, standards page visit | Route to expert follow-up or application-specific nurture |
| **Industry / application** | Pharma, chemical, H2, local service area, course topic | Match examples, proof, and CTA to the buyer's context |
| **Procurement role** | Engineer, buyer, operator, executive, student | Adjust depth, proof, and commercial ask |
| **Interest** | Topic preferences, content consumed | Personalize content recommendations |
| **Value** | Purchase amount, plan tier, LTV | Prioritize high-value segments for personal touch |

### 4.2 A/B Testing Recommendations

For each sequence, suggest tests:

- Subject line variants (test 2 per email)
- Send time variants
- CTA text variants
- Email length (short vs long)
- Plain text vs HTML formatted
- With/without images
- With/without personalization

**Testing hierarchy** (test in this order for maximum learning):

1. Subject lines (biggest impact on open rate)
2. CTA and offer (biggest impact on click rate)
3. Send timing
4. Email length and format

---

## Phase 5: Metrics and Benchmarks

### 5.1 Industry Benchmarks

Include relevant benchmarks in the output. These are US-market averages; open rates in particular are inflated by Apple Mail Privacy Protection and vary by market and list age. Quote them as orientation and name the caveat — never score a client as "underperforming" on this table alone.

| Industry | Avg Open Rate | Avg Click Rate | Avg Conversion Rate |
| --- | --- | --- | --- |
| SaaS/Software | 20-25% | 2-3% | 1-2% |
| E-commerce | 15-20% | 2-3% | 0.5-1.5% |
| Agency/Services | 18-22% | 2-4% | 1-3% |
| Education/Courses | 20-28% | 2-5% | 1-3% |
| Health/Fitness | 18-22% | 2-3% | 0.5-1.5% |
| Finance/Fintech | 20-25% | 2-4% | 1-2% |
| Media/Publishing | 20-25% | 3-5% | 0.5-1% |
| B2B Industrial / Manufacturing | 22-30% | 2-5% | 1-3% |
| Regulated / Compliance B2B | 24-32% | 2-5% | 1-3% |
| Training / Academy | 22-30% | 3-6% | 2-5% |

### 5.2 Compliance Notes

Include a compliance section in every output:

Lead with the regime that governs the recipients, not the one you know best. Determine it from the audience's location, which is usually the site's market — not the sender's.

**GDPR (EU/EEA) — the strictest of the three, and the default for any European list:**

- Explicit opt-in consent required; no pre-checked boxes, no consent bundled into terms
- Consent must be documented: when, how, and exactly what was agreed to
- Right to erasure — delete on request
- Data processing agreement required with the email service provider
- Legitimate-interest B2B sending is narrow and contested; do not present it as a safe default

**Germany, Austria, Switzerland — stricter still in practice:**

- **Double opt-in is the de-facto requirement.** Single opt-in is not defensible under German case law: the confirmation click, with timestamp and IP, is the evidence. Recommend it without qualification for any DE/AT/CH list.
- **Impressum** — a complete legal imprint (company, legal form, register number, VAT ID, managing director, contact) belongs in the email footer, not only on the website
- Advertising to business addresses still requires consent; there is no blanket B2B exemption
- Unsubscribe must be one click and free of charge

**CASL (Canada):**

- Express consent required for commercial messages
- Implied consent for existing business relationships, 24 months
- Sender identification required

**CAN-SPAM (US) — the most permissive; do not apply its standards to a European list:**

- Physical mailing address required in every email
- Working unsubscribe, honored within 10 business days
- Accurate "From" name and address, non-deceptive subject line
- Opt-out rather than opt-in — this is the key divergence from GDPR

**Note:** Always recommend the user verify compliance with their legal counsel. This is orientation, not legal advice.

---

## Output Format: MARKETKIT - EMAIL-SEQUENCES - <scope>.md

Write the full output to the exact `output_path` resolved in Phase 0:

```markdown
[YAML front matter from the Phase 0 metadata resolver — exact shape in references/output-location.md. Omit the whole block when the resolver returned null.]

# Email Sequences: [Business/Topic Name]

**Date:** [current date] \
**Business Type:** [type] \
**Target Audience:** [description] \
**Sequences Generated:** [list of sequence types]

---

## Sequence 1: [Sequence Type]

### Overview

- **Goal:** [primary goal]
- **Emails:** [count]
- **Duration:** [total days]
- **Expected Open Rate:** [benchmark]%
- **Expected Click Rate:** [benchmark]%

### Email 1: [Email Name]

**Send:** [timing] \
**Subject Line:** [primary subject] \
**Subject Line B (A/B test):** [alternative subject] \
**Preview Text:** [preheader text]

---

[Full email body copy here — ready to paste into an ESP]

---

**CTA:** [button text] \
**CTA Link:** [where it should point] \
**Goal:** [what this email should accomplish] \
**Segmentation Notes:** [who should receive this]

[Repeat for each email in the sequence]

---

## Segmentation Strategy

[Recommended segments and how to use them]

## A/B Testing Plan

[Prioritized tests to run]

## Metrics to Track

[KPIs with industry benchmarks]

## Compliance Checklist

[The regime governing this list, leading with the recipients' jurisdiction — GDPR and double opt-in for EU/D-A-CH, CASL for Canada, CAN-SPAM for the US]

## Implementation Notes

[ESP recommendations, automation setup, tagging strategy]
```

---

## Terminal Output

Display a condensed summary:

```
=== EMAIL SEQUENCES GENERATED ===

Business: [name]
Sequences: [list]
Total Emails: [count]

Sequence Overview:
  Welcome (7 emails, 14 days) — Build trust and convert
  Cart Abandonment (3 emails, 7 days) — Recover lost sales

Key Metrics Targets:
  Open Rate: 22-25%
  Click Rate: 3-4%
  Conversion Rate: 1.5-2%

Full sequences saved to: [resolved output_path, e.g. Audit/MARKETKIT - EMAIL-SEQUENCES - example.com.md]
```

---

## Cross-Skill Integration

Look only inside the Phase 0 `audit_dir`, for the exact same scope. Never search older audit folders.

- If `MARKETKIT - BRAND-VOICE - <scope>.md` exists, match all email copy to the documented voice
- If `MARKETKIT - FUNNEL-ANALYSIS - <scope>.md` exists, align email sequences to funnel stages
- If `MARKETKIT - COPY-SUGGESTIONS - <scope>.md` exists, reuse value propositions and CTA language
- If `MARKETKIT - MARKETING-AUDIT - <scope>.md` exists, reference conversion and content scores
- Suggest follow-up: `/marketkit:copy` for website copy, `/marketkit:funnel` for conversion path analysis
