---
name: launch
description: Use when the user is launching a product, service, or feature and needs a launch plan — timeline, channels, announcement assets, metrics, and post-launch review.
argument-hint: <product>
metadata:
  version: 3.0.0
---

# Product/Service Launch Playbook Generator

## Skill Purpose
Generate a complete, week-by-week launch playbook for any product, service, or feature launch. This skill produces a tactical plan with templates, checklists, email sequences, social posts, and metrics tracking -- everything needed to execute a successful launch.

## When to Use
- User is planning to launch a new product, service, feature, or offering
- User asks for a launch plan, go-to-market strategy, or launch checklist
- User wants to coordinate a multi-channel launch campaign
- Triggered by `/marketkit:launch` or `/marketkit:launch <product description>`

## How to Execute

### Step 0: Grounding and Business Context

Before gathering anything else:

1. Read `${CLAUDE_PLUGIN_ROOT}/references/grounding.md` and load any `_grounding/` folder it finds.
2. Read `${CLAUDE_PLUGIN_ROOT}/references/business-context.md`, resolve the business type, and load the single matching example pack.
3. Read `${CLAUDE_PLUGIN_ROOT}/references/output-location.md`. Ask the user for an explicit domain or customer scope before writing any file — never invent one. The scope must contain only letters, numbers, dots, and hyphens. Resolve today's output path now:

   ```
   python "${CLAUDE_PLUGIN_ROOT}/scripts/resolve_audit_output.py" --purpose LAUNCH-PLAYBOOK --scope <scope> --extension md
   ```

   Use `python3` on macOS/Linux. Retain the exact `output_path` for the final write.

Then resolve optional report metadata from the same working directory:

```
python "${CLAUDE_PLUGIN_ROOT}/scripts/resolve_report_metadata.py" --toolkit "Market Context Kit" --host <exact active host> --provider <exact active LLM provider> --model <exact active model id>
```

Never guess a runtime value. Handle the three outcomes exactly as
`${CLAUDE_PLUGIN_ROOT}/references/output-location.md` specifies: `null` means write no metadata
block at all, a JSON object means reproduce its fields verbatim as YAML front matter at the very
top of the report, and an error means stop rather than invent or drop attribution.

The pack supplies the launch channels, pre-launch calendar, announcement templates and success metrics. A consumer launch and a technical launch share only the phase structure — everything inside the phases differs, including how long the launch runs and what counts as success.

### Step 1: Gather Launch Context
Before generating the playbook, collect these inputs from the user (ask if not provided):

1. **What are you launching?** (product, service, feature, course, event)
2. **Who is the target audience?** (demographics, pain points, existing list size)
3. **What is the primary launch goal?** (revenue target, signups, downloads, awareness)
4. **What is the launch date?** (or desired timeline)
5. **What channels do you have access to?** (email list size, social following, ad budget, partnerships)
6. **What is the commercial model?** (price point, RFQ, sales-led, distributor-led, enrollment, donation, or hybrid)
7. **Do you have existing customers/users?** (for beta, testimonials, case studies)
8. **What is the budget?** (bootstrapped, moderate, well-funded)

### Step 2: Determine Launch Type
Select the primary launch strategy based on the user's context:

| Launch Type | Best For | Key Channel | Timeline |
|---|---|---|---|
| Product Hunt | SaaS, dev tools, consumer apps | Product Hunt + Twitter/X | 4-6 weeks prep |
| Email List Launch | Course, info product, SaaS with existing list | Email | 6-8 weeks |
| Social Media Launch | Consumer product, personal brand | Twitter/X, LinkedIn, Instagram | 4-6 weeks |
| Paid Ads Launch | E-commerce, established product | Facebook/Google Ads | 2-4 weeks prep |
| Community Launch | Niche product, developer tools | Reddit, Discord, Slack communities | 6-8 weeks |
| Partner Launch | B2B, enterprise, marketplace | Partner channels | 8-12 weeks |
| Industrial / RFQ Launch | Technical products, industrial services, regulated B2B | Sales team, LinkedIn, Google Search, trade media, distributors | 8-12 weeks |
| Course / Certification Launch | Academy, training, professional education | Email, LinkedIn, associations, events | 6-10 weeks |
| Regulatory / Thought Leadership Launch | Compliance, technical guides, knowledge-led B2B | Newsletter, LinkedIn, trade press, webinars | 4-8 weeks |
| Hybrid Launch | Any high-stakes launch | Multi-channel coordinated | 8-12 weeks |

### Step 3: Generate the 8-Week Launch Timeline

#### Weeks 1-2: Foundation
**Objective:** Lock in positioning, build assets, set up infrastructure.

**Tasks:**
- [ ] Define launch positioning statement: "For [TARGET] who [PROBLEM], [PRODUCT] is a [CATEGORY] that [KEY BENEFIT]. Unlike [ALTERNATIVE], we [DIFFERENTIATOR]."
- [ ] Create launch one-pager (internal alignment doc)
- [ ] Set up landing page / waitlist page
- [ ] Set up analytics and tracking (UTM parameters, conversion goals, event tracking)
- [ ] Create launch-specific email list/segment
- [ ] Draft all email sequences (see Email Templates below)
- [ ] Brief design team on visual assets needed
- [ ] Identify 10-20 potential beta testers or early access users
- [ ] Research and list 20+ communities, forums, and groups where target audience gathers
- [ ] Set up social media content calendar tool

**Deliverables:**
- Positioning statement
- Landing page live
- Email sequences drafted
- Beta tester list

#### Weeks 3-4: Audience Building
**Objective:** Build anticipation, grow waitlist, recruit beta testers.

**Tasks:**
- [ ] Begin content seeding: publish 2-3 pieces on the problem the launch solves
- [ ] Start engaging in the communities, forums or trade channels where the buyers are
- [ ] Recruit beta testers, pilot customers or reference installations with personal invitations
- [ ] Collect early feedback and permission to quote results
- [ ] Begin partner, distributor or influencer outreach (see Partner Coordination below)
- [ ] Build the pre-launch capture mechanism (waitlist, notification list, or sales-qualified interest list)
- [ ] Create anticipation or evidence content, whichever this audience responds to — see the loaded pack
- [ ] Record a demo, walkthrough or technical explainer
- [ ] Write press release or media pitch; trade press needs 4-12 weeks of lead time, so start here

**Content Calendar (Weeks 3-4):**

Build it from the loaded example pack — `Launch — channels, calendar and post templates` in `consumer-online.md`, `Launch — industrial / technical timeline` in `b2b-technical.md`. The consumer version runs a daily-cadence anticipation calendar; the technical version front-loads evidence and channel enablement instead, because the buyer cannot act on anticipation.

**Deliverables:**
- 4-6 content pieces published
- Beta testers onboarded and providing feedback
- Waitlist growing
- Partner/influencer commitments secured

#### Weeks 5-6: Pre-Launch Intensification
**Objective:** Maximize anticipation, finalize assets, prep launch infrastructure.

**Tasks:**
- [ ] Send pre-launch email sequence to waitlist (see Email Templates)
- [ ] Increase social media posting frequency to daily
- [ ] Publish case study or results from beta testers
- [ ] Finalize pricing and offer structure
- [ ] Create launch-day content package (all posts, emails, and graphics ready)
- [ ] Brief partners/affiliates on launch plan and provide swipe copy
- [ ] Set up live chat or support for launch day
- [ ] Test all purchase/signup flows end-to-end
- [ ] Prepare FAQ document for support team
- [ ] Create urgency mechanism (early bird pricing, limited spots, bonus expiration)
- [ ] Rehearse launch day by walking through every step
- [ ] Set up real-time dashboard for launch metrics

**Deliverables:**
- All launch assets finalized and scheduled
- Partners briefed and ready
- Checkout/signup flow tested
- Support team prepared

#### Week 7: LAUNCH WEEK
**Objective:** Execute the launch with maximum impact and coordinated effort.

**Day-by-Day Breakdown:**

**Monday - Soft Launch / VIP Access:**
- Send early access email to VIPs, beta testers, and top waitlist members
- Post on social: "We're live for our early supporters"
- Collect first-day feedback and testimonials
- Monitor for bugs and issues
- Goal: First 50-100 users/customers

**Tuesday - Public Announcement:**
- Send main launch email to full list
- Publish launch blog post
- Post launch announcement on all social channels
- Submit to any launch platform in use, at that platform's own cutover time in its own timezone
- Activate partner/affiliate promotions
- Begin paid ad campaigns (if applicable)
- Goal: Maximum visibility and traffic

**Wednesday - Social Proof Push:**
- Share first customer testimonials and results
- Repost/retweet customer reactions
- Send "look what people are saying" email
- Post in communities (with genuine value, not spam)
- Respond to every comment, mention, and question
- Goal: Build momentum through social proof

**Thursday - Objection Handling:**
- Publish FAQ or "everything you need to know" post
- Send email addressing top 3 objections
- Host live Q&A or AMA (Twitter Space, LinkedIn Live, webinar)
- Share comparison content (why this vs alternatives)
- Goal: Convert fence-sitters

**Friday - Urgency and Scarcity:**
- Send "early bird pricing ends soon" email
- Post countdown content on social
- Share final testimonials and case studies
- Activate scarcity mechanisms (limited spots, bonus expires)
- Goal: Drive final wave of conversions

**Saturday/Sunday - Wrap Up:**
- Send "last chance" email for any time-limited offers
- Compile launch week results
- Thank early customers publicly
- Begin post-launch content planning

#### Week 8: Post-Launch
**Objective:** Maintain momentum, collect feedback, plan next iteration.

**Tasks:**
- [ ] Send post-launch survey to new customers
- [ ] Compile and analyze launch metrics (see Metrics section)
- [ ] Write launch retrospective (what worked, what didn't, what to change)
- [ ] Transition from launch pricing to regular pricing
- [ ] Set up onboarding email sequence for new customers
- [ ] Plan next content calendar based on launch learnings
- [ ] Follow up with media contacts and partners with results
- [ ] Identify top customers for case studies
- [ ] Begin planning v2 features based on feedback
- [ ] Set up ongoing marketing engine (content, ads, email nurture)

### Step 4: Email Sequence Templates

#### Pre-Launch Sequence (Weeks 5-6)

**Email 1: The Teaser (2 weeks before)**
Subject: Something big is coming...
Purpose: Build anticipation
Content: Hint at the product, share the problem it solves, tease the launch date. Don't reveal everything.
CTA: "Stay tuned" or "Make sure you're on the list"

**Email 2: The Reveal (1 week before)**
Subject: Here's what we've been building
Purpose: Show the product, build desire
Content: Reveal the product with screenshots/video. Share beta tester results. Announce launch date and any early bird offer.
CTA: "Mark your calendar" or "Get notified on launch day"

**Email 3: The Social Proof (3 days before)**
Subject: "[Beta Tester Name] got [Result] in [Timeframe]"
Purpose: Prove it works
Content: Feature 2-3 beta tester testimonials with specific results. Address the "does this actually work?" objection.
CTA: "Be ready for [launch day]"

#### Launch Sequence (Week 7)

**Email 4: The Launch (Day 1)**
Subject: It's live -- [Product Name] is here
Purpose: Drive immediate action
Content: Announce the launch. State the offer clearly. Include early bird pricing or bonus. Link directly to purchase/signup.
CTA: "Get [Product] now" with primary button

**Email 5: The Social Proof Follow-Up (Day 3)**
Subject: People are already seeing results
Purpose: Convert through social proof
Content: Share first-customer testimonials, screenshots of reactions, usage stats. Create FOMO.
CTA: "Join [X] others who already [outcome]"

**Email 6: The Objection Handler (Day 4)**
Subject: "But what if [common objection]?"
Purpose: Address hesitations
Content: List and answer top 3-5 objections. Include guarantee/risk reversal. Share FAQ.
CTA: "Try it risk-free"

**Email 7: The Urgency Close (Day 5-7)**
Subject: [X hours] left for [early bird / bonus / discount]
Purpose: Drive final conversions with urgency
Content: Remind of the deadline. Recap the value. Final testimonial. Clear, single CTA.
CTA: "Last chance to get [offer]"

### Step 5: Announcement Posts

Take the announcement templates from the loaded example pack:

- `consumer-online.md` → `Launch — channels, calendar and post templates`: X thread, LinkedIn founder post, Instagram visual post.
- `b2b-technical.md` → `Launch — industrial / technical timeline`: expert-profile post series, technical newsletter feature, trade-press pitch, distributor announcement.

Whichever applies, every announcement carries the same four elements: what it is, who it is for, the evidence it works, and the single next step. What differs is the voice, the proof type, and who publishes it — a founder's personal narrative in one case, a named engineer's finding in the other.

### Step 6: Press and Media Outreach

**Press Release Structure:**
1. Headline: [Company] Launches [Product] to Help [Audience] [Outcome]
2. Subheadline: [Supporting detail with a key stat or differentiator]
3. First paragraph: Who, what, when, where, why (the news)
4. Quote from founder/CEO
5. Product details and key features
6. Market context (why now, market size, trend)
7. Customer quote or early results
8. Availability and pricing
9. About the company (boilerplate)
10. Contact information

**Media Pitch Email Template:**
```
Subject: [Angle] -- [Product Name] launches to [outcome]

Hi [Name],

I'm reaching out because you've covered [related topic] and I thought [Product Name] might be interesting for your readers.

[One sentence about what it does and why it's newsworthy]

[One sentence about early traction or results]

[One sentence about what makes it different]

I'd love to offer you [exclusive story / early access / founder interview / demo].

Happy to share more details if you're interested.

Best,
[Name]
```

### Step 7: Influencer and Partner Coordination

**Partner Outreach Timeline:**
- Week 3: Initial outreach with personal message
- Week 4: Follow up, share product details and demo
- Week 5: Confirm participation, send swipe copy and affiliate links
- Week 6: Reminder with launch day schedule
- Week 7: Day-of coordination, thank you notes
- Week 8: Share results, pay commissions, plan ongoing partnership

**What to Provide Partners:**
- Product access (free account or sample)
- Swipe copy for email, social, and blog
- Branded graphics and assets
- Unique affiliate/referral link with tracking
- Commission structure or reciprocal promotion plan
- Launch day schedule with specific asks

### Step 8: Launch Metrics Dashboard

Track these metrics in real-time during launch week:

**Awareness Metrics:**
- Website traffic (total and by source)
- Social media impressions and reach
- Press mentions and backlinks
- Email open rates

**Engagement Metrics:**
- Time on site
- Pages per session
- Social media engagement rate
- Email click-through rates
- Demo video completion rate

**Conversion Metrics:**
- Signup/purchase conversion rate
- Revenue generated
- Average order value
- Cost per acquisition
- Email-to-conversion rate

**Retention Metrics (Post-Launch):**
- Day 1 / Day 7 retention
- Feature adoption rate
- Support ticket volume
- NPS score

### Step 9: Common Launch Mistakes to Avoid

1. **Launching to nobody** -- Build the audience BEFORE the product is ready
2. **No urgency mechanism** -- Without a deadline, people bookmark and forget
3. **Perfectionism** -- Ship at 80% quality; iterate based on real feedback
4. **Single-channel launch** -- Coordinate across email, social, communities, and partners
5. **No follow-up sequence** -- Most conversions happen on days 3-7, not day 1
6. **Ignoring time zones** -- Schedule launches and emails for your audience's active hours
7. **No support plan** -- Launch day will generate support requests; be ready
8. **Pricing confusion** -- Make the offer crystal clear; don't make people calculate
9. **Forgetting mobile** -- Test every email, page, and checkout on mobile
10. **No post-launch plan** -- The launch is the beginning, not the end

### Step 10: Budget Allocation Guide

| Budget Level | Allocation |
|---|---|
| **Bootstrapped ($0-500)** | 100% organic: content, communities, email list, personal outreach |
| **Moderate ($500-5,000)** | 40% paid ads, 30% influencer/partner, 20% tools/software, 10% design |
| **Well-Funded ($5,000-25,000)** | 35% paid ads, 25% influencer/partner, 20% PR/media, 10% events, 10% tools |
| **Enterprise ($25,000+)** | 30% paid ads, 20% events/webinars, 20% PR, 15% influencer, 10% content, 5% tools |

### Step 11: Post-Launch Analysis Framework

After the launch, generate a retrospective covering:

1. **Goal vs Actual**: Did you hit your targets?
2. **Channel Performance**: Which channels drove the most conversions?
3. **Email Performance**: Open rates, click rates, conversion rates by email
4. **Top Converting Content**: Which posts, pages, or ads drove the most action?
5. **Customer Feedback Themes**: What are people saying?
6. **What Worked**: Top 3 things that drove results
7. **What Didn't Work**: Top 3 things to change next time
8. **Unexpected Insights**: Surprises from the data
9. **Next Steps**: Immediate actions based on learnings

## Output Format: MARKETKIT - LAUNCH-PLAYBOOK - <scope>.md

Write the exact `output_path` resolved in Step 0 with:

```markdown
[YAML front matter from the Phase 0 metadata resolver — exact shape in references/output-location.md. Omit the whole block when the resolver returned null.]
# Launch Playbook: [Product Name]
## Launch Date: [Date]
## Launch Type: [Type]
## Primary Goal: [Goal with specific target]

---

## Week-by-Week Plan
[Detailed week-by-week tasks with checkboxes]

## Email Sequences
[Complete email templates customized for the product]

## Social Media Content
[Platform-specific posts ready to customize and schedule]

## Partner/Influencer Plan
[Outreach templates and coordination timeline]

## Launch Day Checklist
[Hour-by-hour launch day plan]

## Metrics Dashboard
[Metrics to track with target benchmarks]

## Budget Allocation
[Specific dollar amounts based on stated budget]

## Post-Launch Plan
[Week 8+ activities and analysis framework]
```

## Key Principles
- Every recommendation should be tied to the user's specific product, audience, and resources. Generic advice is useless.
- Include specific templates they can copy-paste and customize, not just frameworks.
- If the user has run previous skills (market audit, market landing, market brand), incorporate those findings into the launch plan.
- Time the playbook to their stated launch date and work backwards.
- Always include a "minimum viable launch" option for users with limited resources.
- Emphasize that launching is an event, not a moment -- the buildup and follow-through matter more than day one.

