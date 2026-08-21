# Market Context Kit

**This is 100% AI slop copied from AI-slop bros on YouTube. It is no substitute for an agency that would charge you thousands of money, and it won’t produce content your business can use as-is. At best, it gives you a fresh perspective and a few rough ideas to develop yourself.**

**ACHTUNG** I haven’t tested some of the skills, such as content-plan or ads, because I don’t need them myself. Yet. The PDF creator is probably crap, too. But since you can tell the LLM, “Do it like this, Mr. Robot Sir, please,” you’ll probably end up with something workable. I believe in you, alleged human-in-the-loop.

---

A context-aware marketing skill kit for [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Audit websites, generate copy and campaigns, build content plans, analyze competitors, and produce client-ready reports — all from your terminal.

**Built for anyone doing marketing work with Claude Code** — in-house teams, agencies, consultants, and solo operators alike. It handles consumer and self-serve businesses as well as industrial, technical and regulated B2B, and it keeps the two apart: business-type-specific playbooks live in swappable example packs rather than in the skills themselves, so an RFQ-led manufacturer never gets advice built for a DTC brand.

---

## What This Does

Type a command in Claude Code and get instant, actionable marketing analysis:

```
> /marketkit:audit https://www.example.com/

Launching 5 parallel agents...
✓ Content & Messaging Analysis     — Score: 72/100
✓ Conversion Optimization          — Score: 58/100
✓ SEO & Discoverability            — Score: 81/100
✓ Competitive Positioning          — Score: 64/100
✓ Brand & Trust                    — Score: 76/100
✓ Growth & Strategy                — Score: 61/100

Overall Marketing Score: 69/100

Full report saved to Audit/MARKETKIT - MARKETING-AUDIT - example.com.md
```

---

## Installation

This is a Claude Code **skills-directory plugin**: clone it into a skills directory and it loads itself. There is no installer, nothing is copied anywhere, and there is nothing to uninstall — delete the folder and it is gone.

### One project only (recommended)

```bash
git clone https://github.com/marcus-at-localhost/market-context-kit.git .claude/skills/market-context-kit
```

Run that from the project root. Accept the workspace trust dialog when Claude Code asks — project-scope plugins do not load until you do.

### Every project on this machine

```bash
git clone https://github.com/marcus-at-localhost/market-context-kit.git ~/.claude/skills/market-context-kit
```

No trust dialog needed for this one.

### Verify

Restart Claude Code, then:

```bash
claude plugin list          # expect: marketkit@skills-dir
```

Type `/marketkit:help` for the command index. Updating is `git pull` in the folder.

### Optional: PDF Report Support

```bash
pip install reportlab
```

Everything else runs on the Python standard library. Windows, macOS, and Linux are all supported.

---

## Commands

Each skill is its own command. There is no router — `help` is just an index you can print.

Because this loads as a plugin, every command is namespaced `marketkit:`. That prefix is part of the trigger, not an optional long form — a bare `/audit` does not resolve. Claude also invokes these on its own when a request matches, so you rarely have to type one.

| Command | What It Does |
| --- | --- |
| `/marketkit:help` | Index of every command, with a "which one first" guide |
| `/marketkit:audit <url>` | Full marketing audit with 5 parallel agents |
| `/marketkit:copy <url>` | Generate optimized copy with before/after examples |
| `/marketkit:emails <topic>` | Generate complete email sequences |
| `/marketkit:social <topic>` | 30-day social media content calendar |
| `/marketkit:ads <url>` | Ad creative and copy for all platforms |
| `/marketkit:funnel <url>` | Sales funnel analysis and optimization |
| `/marketkit:competitors <url>` | Competitive intelligence report |
| `/marketkit:landing <url>` | Landing page CRO analysis |
| `/marketkit:launch <product>` | Product launch playbook |
| `/marketkit:proposal <client>` | Client proposal generator |
| `/marketkit:report <url>` | Full marketing report (Markdown) |
| `/marketkit:report-pdf <url>` | Professional marketing report (PDF) |
| `/marketkit:seo <url>` | SEO content audit |
| `/marketkit:brand <url>` | Brand voice analysis and guidelines |
| `/marketkit:content-plan <url>` | Topic research + content plan + article drafts |

`help` carries `disable-model-invocation: true`, so Claude never picks the index on its own — type it when you want the menu.

---

## Architecture

```
market-context-kit/                     # clone target: .claude/skills/market-context-kit
├── .claude-plugin/plugin.json          # Makes the folder load as a plugin
│
├── skills/                             # 15 skills + index
│   ├── help/SKILL.md                   # Command index (manual invocation only)
│   ├── audit/SKILL.md                  # Full audit orchestration
│   ├── copy/SKILL.md                   # Copywriting analysis & generation
│   ├── emails/SKILL.md                 # Email sequence generation
│   ├── social/SKILL.md                 # Social media content calendar
│   ├── ads/SKILL.md                    # Ad creative & copy
│   ├── funnel/SKILL.md                 # Funnel analysis & optimization
│   ├── competitors/SKILL.md            # Competitive intelligence
│   ├── landing/SKILL.md                # Landing page CRO
│   ├── launch/SKILL.md                 # Launch playbook generation
│   ├── proposal/SKILL.md               # Client proposal generator
│   ├── report/SKILL.md                 # Marketing report (Markdown)
│   ├── report-pdf/SKILL.md             # Marketing report (PDF)
│   ├── seo/SKILL.md                    # SEO content audit
│   ├── brand/SKILL.md                  # Brand voice analysis
│   └── content-plan/SKILL.md           # Topic research & content planning
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
│   ├── google-search-guidance.md       # Myth guardrail, grounding precedence, schema scoring
│   ├── examples/
│   │   ├── consumer-online.md          # Creator, e-commerce, self-serve SaaS, local
│   │   └── b2b-technical.md            # Industrial, distributor, regulated, academy
│   └── fingerprints/                   # competitor_scanner.py rule packs (same ids as examples/)
│       ├── consumer-online.json        # CTA/pricing/trust vocab, en/de/es/fr/it/nl
│       └── b2b-technical.json          # RFQ/cert/distributor vocab, en/de/es/fr/it/nl
│
├── scripts/                            # Python utility scripts
│   ├── analyze_page.py                 # Webpage marketing analysis
│   ├── competitor_scanner.py           # Competitor scanner — business-type-aware (see fingerprints/)
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

## Optional Search Context companion

[Search Context Kit](../search-context-kit/) is an optional companion that collects read-only Google Search Console, Bing Webmaster, and Matomo evidence into a versioned `SEARCH-CONTEXT.v1.json` artifact. It remains a separate plugin and Python package, so Market Context Kit does not inherit its provider packages, credentials, or MCP runtimes.

SearchKit keeps one independent profile per exact domain — `config/searchkit.<domain>.json` — never a copy of this suite's `_grounding/`. A project with three domains has three SearchKit profiles and one shared `_grounding/`.

Audit, report, and SEO workflows discover the artifact automatically: exactly one `data/SEARCHKIT - SEARCH-CONTEXT-V1-<period> - <domain>.json` inside the active `Audit/` folder, for the exact target domain. An explicit path always overrides discovery, for example:

```text
/marketkit:audit https://example.com and use "Audit/data/SEARCHKIT - SEARCH-CONTEXT-V1-Q2-2026 - example.com.json" during synthesis.
```

The artifact is used only after schema, exact-domain, reporting-period, and source-status validation. In the full audit it is orchestrator-only, never goes to the five scoring subagents, and does not change audit scores; it can only corroborate and prioritize independently derived recommendations. Missing, partial, mismatched, or stale evidence is disclosed rather than treated as zero. Archived or renamed audit folders are never searched automatically.

---

## Grounding: teaching the suite about your business

Every command looks for a `_grounding/` folder in the working directory (and up to three parent directories). If it finds one, it loads it and treats it as the highest authority — above the site's own evidence for matters of intent, and above every default in the skills. One customer project keeps one shared, multilingual `_grounding/` regardless of how many domains that customer runs.

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
- **Subagents inherit it.** `audit` builds a grounding digest and passes it into all five parallel agents; they share no context otherwise and would otherwise analyze against generic defaults while the orchestrator does not.
- **Every output declares it.** Reports name the grounding files they loaded, so you can tell which conclusions came from your documentation and which came from the suite's defaults.

No grounding folder is required. Without one the suite works from site evidence alone and says so.

## Output: the shared Audit/ workspace

One project holds one customer — not one project per domain. A customer with three domains still keeps one shared, multilingual `_grounding/` at the project root and one shared output workspace; only the SearchKit profile and the filename scope vary per domain.

Every command resolves its output path through `references/output-location.md` before writing, via the bundled `scripts/resolve_audit_output.py`. Output lands in the single active audit folder at the Git project root (or CWD outside Git):

```
Audit/
```

shared by every command, always — Market Context Kit and Search Context Kit alike. A same-purpose, same-scope rerun **overwrites the existing file in place**, and git history is the version record. Reports live directly in that folder; internal intermediates (PDF source JSON, SearchKit raw evidence) live flat under its `data/` subfolder. The resolver never searches an archived or renamed folder — when a project is finished, archive it yourself by renaming `Audit/`; a prior engagement's evidence is out of scope unless you name its path explicitly.

Every generated filename follows one contract, with no underscores:

```
MARKETKIT - <PURPOSE> - <SCOPE>.<extension>
```

`SCOPE` is the exact normalized target domain for URL-based commands (`audit`, `competitors`, `seo`, `ads`, `brand`, `content-plan`, `copy`, `funnel`, `landing`, `report`, `report-pdf`). For topic-only commands (`emails`, `launch`, `proposal`, and topic-only `social`), the skill asks you for an explicit domain or customer scope before writing anything — it never invents one.

**Worked example — MarketKit runs, then reruns days later, then SearchKit runs:**

```
> /marketkit:audit https://example.com
Full report saved to: Audit/MARKETKIT - MARKETING-AUDIT - example.com.md

> /marketkit:audit https://example.com                      # rerun days later, same domain
Full report saved to: Audit/MARKETKIT - MARKETING-AUDIT - example.com.md   # overwritten in place

> /searchkit:collect example.com Q2 2026                     # SearchKit targets the same Audit/
Artifact saved to: Audit/data/SEARCHKIT - SEARCH-CONTEXT-V1-Q2-2026 - example.com.json
```

The rerun writes to the exact same path as the first run. SearchKit resolves the same `Audit/` folder regardless of how much time has passed, so both toolkits' output for the whole engagement sits side by side.

### Optional project report metadata

The suite reads `config/reporting.config.json` at the Git project root first (or in the current working directory outside Git). A legacy `reporting.config.json` directly at the project root still works but warns that it should move under `config/`; if both exist, the resolver stops rather than pick one silently. If no file is found, reports contain no attribution or generation metadata. If present, it must match `config/reporting.schema.json`; report workflows merge its human attribution with the exact active toolkit, host, provider, and model. No user-global configuration or environment variable is consulted. Copy `config/reporting.example.json` to `config/reporting.config.json` to enable it.

### Client isolation

The five audit subagents cannot reach across a client boundary, because they cannot reach the filesystem at all. They carry no file-discovery tools and may open only the paths the orchestrator names in that run's **Data Manifest** (`skills/audit/SKILL.md`, 0.1), which excludes previous audit reports and analytics exports by rule. Keep one repository per customer — mixing two customers into the same tree means their `_grounding/` and Search Context evidence both depend on you never running a command from the wrong project.

## Business type and example packs

The skills themselves contain no worked examples for a specific kind of business. Hooks, CTAs, objection sets, page structures and launch timelines live in `references/examples/`, and each skill loads exactly one pack after resolving the business type — from grounding if present, otherwise from site signals.

This is deliberate rather than cosmetic: a labelled "for consumer brands only" example still sits in the context window and still influences the output. Keeping the wrong pack out of context is the only reliable way to keep a TikTok hook from reaching an industrial gasket manufacturer.

When the business type cannot be resolved, no pack is loaded and examples are derived from the site's own vocabulary, with a note saying so.

---

## Scoring Methodology

The full marketing audit scores websites across 6 dimensions:

| Category | Weight | What It Measures |
| --- | --- | --- |
| Content & Messaging | 25% | Copy quality, value props, headlines, CTAs |
| Conversion Optimization | 20% | Funnels, forms, social proof, friction, urgency |
| SEO & Discoverability | 20% | On-page SEO, technical SEO, content structure |
| Competitive Positioning | 15% | Differentiation, market awareness, alternatives |
| Brand & Trust | 10% | Design quality, trust signals, authority |
| Growth & Strategy | 10% | Pricing, acquisition channels, retention |

**Overall Marketing Score** = Weighted average of all categories (0-100)

### External Research Cited

Most scoring dimensions and reference content are the suite's own synthesis of established practice. Where a specific stat or framework instead comes from a named third party, it's listed here so its origin and vintage stay traceable — the pack files carry only a short inline mention.

- **Buyer archetypes** (Adapter / Innovator / Seeker, `references/examples/b2b-technical.md`) and **Channel/Path Coverage** scoring (`agents/market-conversion.md`) — McKinsey, [Five fundamental truths: How B2B winners keep growing](https://www.mckinsey.com/capabilities/growth-marketing-and-sales/our-insights/five-fundamental-truths-how-b2b-winners-keep-growing) (2024 B2B Pulse Survey, ~4,000 respondents). Percentages are global-survey directional, not any specific client's measured mix.

Add an entry here whenever a new externally-sourced stat or framework goes into the suite.

### Frameworks Referenced

Named frameworks the skills apply, for background reading — these are established methods, not claims that need checking, so they sit here rather than in External Research Cited above.

| Framework | Used in | Reference |
| --- | --- | --- |
| AIDA (Attention-Interest-Desire-Action) | `copy` | [Wikipedia](<https://en.wikipedia.org/wiki/AIDA_(marketing)>) |
| PAS (Problem-Agitate-Solve) | `copy` | [Copywrite Matters](https://www.copywritematters.com/pas-classic-copywriting-formula/) |
| Before-After-Bridge | `copy` | [Blak Sheep Creative](https://blaksheepcreative.com/digital-marketing/content-marketing/copywriting/before-after-bridge/) |
| 4U Formula (Useful/Ultra-specific/Unique/Urgent) | `copy`, `landing` | [AWAI](https://www.awai.com/2001/06/a-review-of-the-4-us/) (originating org) |
| Value Proposition Canvas | `copy` | [Strategyzer](https://www.strategyzer.com/library/mastering-value-propositions) (Osterwalder's own) |
| E-E-A-T | `seo`, `market-technical` | [Google Search Central](https://developers.google.com/search/blog/2022/12/google-raters-guidelines-e-e-a-t) |
| Google helpful-content self-assessment | `seo`, `report`, `market-content` | [Google Search Central](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) |
| Google generative-AI search guidance, incl. Mythbusting | `seo`, `audit`, `market-technical`, `market-content` | [Google Search Central](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) |
| SWOT Analysis | `competitors` | [Wikipedia](https://en.wikipedia.org/wiki/SWOT_analysis) |

---

## How It Works

1. **You type a command** — e.g., `/marketkit:audit https://example.com`
2. **Claude reads the skill files** — they tell Claude exactly how to analyze the site
3. **5 subagents launch in parallel** — each one analyzes a different dimension
4. **Python scripts run** — automated page analysis, competitor scanning
5. **Results are compiled** — into a scored, prioritized, actionable report
6. **Output is saved** — as a Markdown file or professional PDF

---

## Use Cases

All commands below take the `marketkit:` prefix — shortened here for readability.

### For Agencies and Consultants

- Run `audit` on a prospect's website before a sales call
- Generate `proposal` with specific findings and pricing
- Deliver `report-pdf` as a professional client deliverable

### For In-House B2B and Industrial Teams

- Point the suite at a `_grounding/` folder so every command works from your own positioning, industries, competitors and claim rules
- Audit RFQ, datasheet, catalog and course-enrollment paths — not just signup funnels
- Generate technical content plans, trade-media angles and RFQ-stage email sequences
- Check landing pages against the objections your buyers actually raise: standards, approvals, lead time, application fit

### For Solo Operators and Creators

- Use `copy` to optimize your own landing pages
- Generate `emails` for your product launches
- Build `social` calendars for consistent posting
- Plan launches with `launch`, analyze your funnel with `funnel`

---

## Extending the Suite

Want to add an external concept, framework, or piece of research (a report, an article, a survey) to the suite? See [EXTENDING.md](EXTENDING.md) — where it should land, how to cite it, and how to keep pack files independent.

---

## Uninstall

Delete the folder:

```bash
rm -rf .claude/skills/market-context-kit
```

Nothing was ever copied outside it, so that is the whole uninstall. To keep the files but stop loading them:

```bash
claude plugin disable marketkit@skills-dir
```

---

## Thoughts

There is a big chance of drift and false positives. Drift, because at one point the agent wanders off not knowing which is the most important Markdown document to follow, or the model changes. Another problem: the agent might decide to write its own ad-hoc parser without understanding the ins and outs of valid HTML. Same for the Python scripts. They might work for website A but not for website B. It's not mature software covering every edge case. And if the website you scan is protected by all kinds of security measures or is completely client-side rendered, you're mostly out of luck. You can work around it, but it takes extra effort.

So if you know the website you are scanning, you can correct the mistakes the agent might have made: tell it "This page returning a 404 is a deliberate choice because xyz," and it will correct the report.

If you run this on a website where you don't know the ins and outs, either put in the work to check the claims of the report and argue with the agent, or put a big fat disclaimer up front that this report might be wrong because xyz and dance around the issue that no one knows what they are doing.

## Origin and attribution

Market Context Kit began as a fork of Zubair Trabzada's [AI Marketing Suite for Claude Code](https://github.com/zubair-trabzada/ai-marketing-claude). It has since added a skills-directory plugin architecture, project grounding, context-specific example packs, B2B and regulated-industry workflows, and broader regional guidance.

The complete Git history is retained. The original MIT copyright notice remains in [LICENSE](LICENSE), alongside the copyright notice for subsequent work.

---

## License

MIT License — see [LICENSE](LICENSE) for details.
