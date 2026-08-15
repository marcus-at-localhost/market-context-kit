<p align="center">
  <img src="banner.svg" alt="AI Marketing Suite for Claude Code" width="100%">
</p>

# AI Marketing Suite for Claude Code

A comprehensive marketing analysis and automation skill system for [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Audit any website's marketing, generate copy, build email sequences, create content calendars, analyze competitors, and produce client-ready PDF reports — all from your terminal.

**Built for anyone doing marketing work with Claude Code** — in-house teams, agencies, consultants, and solo operators alike. It handles consumer and self-serve businesses as well as industrial, technical and regulated B2B, and it keeps the two apart: business-type-specific playbooks live in swappable example packs rather than in the skills themselves, so an RFQ-led manufacturer never gets advice built for a DTC brand.

---

## What This Does

Type a command in Claude Code and get instant, actionable marketing analysis:

```
> /ai-marketing:market-audit https://calendly.com

Launching 5 parallel agents...
✓ Content & Messaging Analysis     — Score: 72/100
✓ Conversion Optimization          — Score: 58/100
✓ SEO & Discoverability            — Score: 81/100
✓ Competitive Positioning          — Score: 64/100
✓ Brand & Trust                    — Score: 76/100
✓ Growth & Strategy                — Score: 61/100

Overall Marketing Score: 69/100

Full report saved to MARKETING-AUDIT.md
```

---

## Installation

This is a Claude Code **skills-directory plugin**: clone it into a skills directory and it loads itself. There is no installer, nothing is copied anywhere, and there is nothing to uninstall — delete the folder and it is gone.

### One project only (recommended)

```bash
git clone https://github.com/marcus-at-localhost/ai-marketing-claude.git .claude/skills/ai-marketing
```

Run that from the project root. Accept the workspace trust dialog when Claude Code asks — project-scope plugins do not load until you do.

### Every project on this machine

```bash
git clone https://github.com/marcus-at-localhost/ai-marketing-claude.git ~/.claude/skills/ai-marketing
```

No trust dialog needed for this one.

### Verify

Restart Claude Code, then:

```bash
claude plugin list          # expect: ai-marketing@skills-dir
```

Type `/ai-marketing:market` for the command index. Updating is `git pull` in the folder.

### Optional: PDF Report Support

```bash
pip install reportlab
```

Everything else runs on the Python standard library. Windows, macOS, and Linux are all supported.

---

## Commands

Each skill is its own command. There is no router — `market` is just an index you can print.

Because this loads as a plugin, every command is namespaced `ai-marketing:`. That prefix is part of the trigger, not an optional long form — a bare `/market-audit` does not resolve. Claude also invokes these on its own when a request matches, so you rarely have to type one.

| Command | What It Does |
|---------|-------------|
| `/ai-marketing:market` | Index of every command, with a "which one first" guide |
| `/ai-marketing:market-audit <url>` | Full marketing audit with 5 parallel agents |
| `/ai-marketing:market-copy <url>` | Generate optimized copy with before/after examples |
| `/ai-marketing:market-emails <topic>` | Generate complete email sequences |
| `/ai-marketing:market-social <topic>` | 30-day social media content calendar |
| `/ai-marketing:market-ads <url>` | Ad creative and copy for all platforms |
| `/ai-marketing:market-funnel <url>` | Sales funnel analysis and optimization |
| `/ai-marketing:market-competitors <url>` | Competitive intelligence report |
| `/ai-marketing:market-landing <url>` | Landing page CRO analysis |
| `/ai-marketing:market-launch <product>` | Product launch playbook |
| `/ai-marketing:market-proposal <client>` | Client proposal generator |
| `/ai-marketing:market-report <url>` | Full marketing report (Markdown) |
| `/ai-marketing:market-report-pdf <url>` | Professional marketing report (PDF) |
| `/ai-marketing:market-seo <url>` | SEO content audit |
| `/ai-marketing:market-brand <url>` | Brand voice analysis and guidelines |
| `/ai-marketing:market-content-plan <url>` | Topic research + content plan + article drafts |

`market` carries `disable-model-invocation: true`, so Claude never picks the index on its own — type it when you want the menu.

---

## Architecture

```
ai-marketing/                           # clone target: .claude/skills/ai-marketing
├── .claude-plugin/plugin.json          # Makes the folder load as a plugin
│
├── skills/                             # 15 skills + index
│   ├── market/SKILL.md                 # Command index (manual invocation only)
│   ├── market-audit/SKILL.md           # Full audit orchestration
│   ├── market-copy/SKILL.md            # Copywriting analysis & generation
│   ├── market-emails/SKILL.md          # Email sequence generation
│   ├── market-social/SKILL.md          # Social media content calendar
│   ├── market-ads/SKILL.md             # Ad creative & copy
│   ├── market-funnel/SKILL.md          # Funnel analysis & optimization
│   ├── market-competitors/SKILL.md     # Competitive intelligence
│   ├── market-landing/SKILL.md         # Landing page CRO
│   ├── market-launch/SKILL.md          # Launch playbook generation
│   ├── market-proposal/SKILL.md        # Client proposal generator
│   ├── market-report/SKILL.md          # Marketing report (Markdown)
│   ├── market-report-pdf/SKILL.md      # Marketing report (PDF)
│   ├── market-seo/SKILL.md             # SEO content audit
│   ├── market-brand/SKILL.md           # Brand voice analysis
│   └── market-content-plan/SKILL.md    # Topic research & content planning
│
├── agents/                             # 5 parallel subagents
│   ├── market-content.md               # Content & messaging analysis
│   ├── market-conversion.md            # CRO & funnel optimization
│   ├── market-competitive.md           # Competitive positioning
│   ├── market-technical.md             # Technical SEO & tracking
│   └── market-strategy.md              # Brand, pricing & growth strategy
│
├── references/                         # Loaded on demand by the skills
│   ├── grounding.md                    # How to find and apply a _grounding/ folder
│   ├── business-context.md             # Business type → example pack resolution
│   └── examples/
│       ├── consumer-online.md          # Creator, e-commerce, self-serve SaaS, local
│       └── b2b-technical.md            # Industrial, distributor, regulated, academy
│
├── scripts/                            # Python utility scripts
│   ├── analyze_page.py                 # Webpage marketing analysis
│   ├── competitor_scanner.py           # Competitor website scanner
│   ├── social_calendar.py              # Social content calendar generator
│   └── generate_pdf_report.py          # PDF report generator
│
├── templates/                          # Marketing templates
│   ├── email-welcome.md                # Welcome email sequence (5 emails)
│   ├── email-nurture.md                # Lead nurture sequence (6 emails)
│   ├── email-launch.md                 # Product launch sequence (8 emails)
│   ├── proposal-template.md            # Client proposal template
│   ├── content-calendar.md             # 30-day content calendar
│   ├── launch-checklist.md             # Launch checklist
│   ├── content-brief.md                # Per-article content brief template
│   └── content-plan.md                 # Content plan table template
│
├── requirements.txt                    # Python dependencies (reportlab only)
└── LICENSE                             # MIT License
```

Nothing here is copied anywhere at install time. Skills reference the bundled scripts through `${CLAUDE_PLUGIN_ROOT}`, which Claude Code expands to this folder's real path on any machine, so there are no absolute paths to maintain and no second copy that can drift.

---

## Grounding: teaching the suite about your business

Every command looks for a `_grounding/` folder in the working directory (and up to three parent directories). If it finds one, it loads it and treats it as the highest authority — above the site's own evidence for matters of intent, and above every default in the skills.

A grounding folder is just markdown. Anything you would tell a new agency on day one belongs there:

```
_grounding/
├── README.md                       # optional: maps tasks → which files to load
├── 00_master_context.md            # who you are, what you sell, to whom
├── 02_brand_positioning.md         # positioning, tone, what you never say
├── 03_industries_and_target_groups.md
├── 07_competitors_and_market.md    # the competitor set that actually matters
└── 11_claims_and_evidence.md       # what may be asserted, and on what evidence
```

If `README.md` contains a task-to-files map, the skills follow it and load only what the task needs. Without one, they load `00_master_context.md` plus whatever filenames match the task.

What this changes in practice:

- **Claims are bounded.** A claims file stops the suite generating superlatives you cannot support — which matters when ad platforms reject them and regulated industries police them.
- **Competitors are yours.** Competitive analysis starts from your named competitor set rather than from `"[category] alternatives"` search results.
- **Subagents inherit it.** `market-audit` builds a grounding digest and passes it into all five parallel agents; they share no context otherwise and would otherwise analyze against generic defaults while the orchestrator does not.
- **Every output declares it.** Reports name the grounding files they loaded, so you can tell which conclusions came from your documentation and which came from the suite's defaults.

No grounding folder is required. Without one the suite works from site evidence alone and says so.

## Business type and example packs

The skills themselves contain no worked examples for a specific kind of business. Hooks, CTAs, objection sets, page structures and launch timelines live in `references/examples/`, and each skill loads exactly one pack after resolving the business type — from grounding if present, otherwise from site signals.

This is deliberate rather than cosmetic: a labelled "for consumer brands only" example still sits in the context window and still influences the output. Keeping the wrong pack out of context is the only reliable way to keep a TikTok hook from reaching an industrial gasket manufacturer.

When the business type cannot be resolved, no pack is loaded and examples are derived from the site's own vocabulary, with a note saying so.

---

## Scoring Methodology

The full marketing audit scores websites across 6 dimensions:

| Category | Weight | What It Measures |
|----------|--------|------------------|
| Content & Messaging | 25% | Copy quality, value props, headlines, CTAs |
| Conversion Optimization | 20% | Funnels, forms, social proof, friction, urgency |
| SEO & Discoverability | 20% | On-page SEO, technical SEO, content structure |
| Competitive Positioning | 15% | Differentiation, market awareness, alternatives |
| Brand & Trust | 10% | Design quality, trust signals, authority |
| Growth & Strategy | 10% | Pricing, acquisition channels, retention |

**Overall Marketing Score** = Weighted average of all categories (0-100)

### External Research Cited

Most scoring dimensions and reference content are the suite's own synthesis of established
practice. Where a specific stat or framework instead comes from a named third party, it's listed
here so its origin and vintage stay traceable — the pack files carry only a short inline mention.

- **Buyer archetypes** (Adapter / Innovator / Seeker, `references/examples/b2b-technical.md`) and
  **Channel/Path Coverage** scoring (`agents/market-conversion.md`) — McKinsey, [Five fundamental
  truths: How B2B winners keep growing](https://www.mckinsey.com/capabilities/growth-marketing-and-sales/our-insights/five-fundamental-truths-how-b2b-winners-keep-growing)
  (2024 B2B Pulse Survey, ~4,000 respondents). Percentages are global-survey directional, not any
  specific client's measured mix.

Add an entry here whenever a new externally-sourced stat or framework goes into the suite.

### Frameworks Referenced

Named frameworks the skills apply, for background reading — these are established
methods, not claims that need checking, so they sit here rather than in
External Research Cited above.

| Framework | Used in | Reference |
|---|---|---|
| AIDA (Attention-Interest-Desire-Action) | `market-copy` | [Wikipedia](https://en.wikipedia.org/wiki/AIDA_(marketing)) |
| PAS (Problem-Agitate-Solve) | `market-copy` | [Copywrite Matters](https://www.copywritematters.com/pas-classic-copywriting-formula/) |
| Before-After-Bridge | `market-copy` | [Blak Sheep Creative](https://blaksheepcreative.com/digital-marketing/content-marketing/copywriting/before-after-bridge/) |
| 4U Formula (Useful/Ultra-specific/Unique/Urgent) | `market-copy`, `market-landing` | [AWAI](https://www.awai.com/2001/06/a-review-of-the-4-us/) (originating org) |
| Value Proposition Canvas | `market-copy` | [Strategyzer](https://www.strategyzer.com/library/mastering-value-propositions) (Osterwalder's own) |
| E-E-A-T | `market-seo`, `market-technical` | [Google Search Central](https://developers.google.com/search/blog/2022/12/google-raters-guidelines-e-e-a-t) |
| SWOT Analysis | `market-competitors` | [Wikipedia](https://en.wikipedia.org/wiki/SWOT_analysis) |

---

## How It Works

1. **You type a command** — e.g., `/ai-marketing:market-audit https://example.com`
2. **Claude reads the skill files** — they tell Claude exactly how to analyze the site
3. **5 subagents launch in parallel** — each one analyzes a different dimension
4. **Python scripts run** — automated page analysis, competitor scanning
5. **Results are compiled** — into a scored, prioritized, actionable report
6. **Output is saved** — as a Markdown file or professional PDF

---

## Use Cases

All commands below take the `ai-marketing:` prefix — shortened here for readability.

### For Agencies and Consultants
- Run `market-audit` on a prospect's website before a sales call
- Generate `market-proposal` with specific findings and pricing
- Deliver `market-report-pdf` as a professional client deliverable

### For In-House B2B and Industrial Teams
- Point the suite at a `_grounding/` folder so every command works from your own positioning, industries, competitors and claim rules
- Audit RFQ, datasheet, catalog and course-enrollment paths — not just signup funnels
- Generate technical content plans, trade-media angles and RFQ-stage email sequences
- Check landing pages against the objections your buyers actually raise: standards, approvals, lead time, application fit

### For Solo Operators and Creators
- Use `market-copy` to optimize your own landing pages
- Generate `market-emails` for your product launches
- Build `market-social` calendars for consistent posting
- Plan launches with `market-launch`, analyze your funnel with `market-funnel`

---

## Extending the Suite

Want to add an external concept, framework, or piece of research (a report, an
article, a survey) to the suite? See [EXTENDING.md](EXTENDING.md) — where it
should land, how to cite it, and how to keep pack files independent.

---

## Uninstall

Delete the folder:

```bash
rm -rf .claude/skills/ai-marketing
```

Nothing was ever copied outside it, so that is the whole uninstall. To keep the files but stop loading them:

```bash
claude plugin disable ai-marketing@skills-dir
```

---

## Learn More

Want to learn how to build a marketing agency powered by AI tools like this?

**[Join the AI Workshop Community](https://www.skool.com/aiworkshop)** — Learn AI automations, vibe coding, and how to build AI-powered services for clients.

---

## License

MIT License — see [LICENSE](LICENSE) for details.
