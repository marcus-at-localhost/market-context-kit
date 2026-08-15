# Market Context Kit

**This is 100% AI slop copied from AI-slop bros on YouTube. It is no substitute for an agency that would charge you thousands of money, and it won’t produce content your business can use as-is. At best, it gives you a fresh perspective and a few rough ideas to develop yourself.**

A context-aware marketing skill kit for [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Audit websites, generate copy and campaigns, build content plans, analyze competitors, and produce client-ready reports — all from your terminal.

**Built for anyone doing marketing work with Claude Code** — in-house teams, agencies, consultants, and solo operators alike. It handles consumer and self-serve businesses as well as industrial, technical and regulated B2B, and it keeps the two apart: business-type-specific playbooks live in swappable example packs rather than in the skills themselves, so an RFQ-led manufacturer never gets advice built for a DTC brand.

---

## What This Does

Type a command in Claude Code and get instant, actionable marketing analysis:

```
> /marketkit:audit https://calendly.com

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

### Updating an existing `ai-marketing` clone

The local folder may stay at `.claude/skills/ai-marketing`; the manifest controls the plugin namespace. Point the clone at the new repository, pull, and restart Claude Code:

```bash
git remote set-url origin https://github.com/marcus-at-localhost/market-context-kit.git
git pull
```

The v3 command namespace is intentionally shorter: for example, `/ai-marketing:market-audit` becomes `/marketkit:audit` and `/ai-marketing:market-content-plan` becomes `/marketkit:content-plan`.

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
|---------|-------------|
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
- **Subagents inherit it.** `audit` builds a grounding digest and passes it into all five parallel agents; they share no context otherwise and would otherwise analyze against generic defaults while the orchestrator does not.
- **Every output declares it.** Reports name the grounding files they loaded, so you can tell which conclusions came from your documentation and which came from the suite's defaults.

No grounding folder is required. Without one the suite works from site evidence alone and says so.

## Multiple clients from one install

The suite is not tied to a single client — one install can serve as many as you have folders for. Both the `_grounding/` lookup and every skill's output path (`MARKETING-AUDIT.md`, `MARKETING-REPORT.md`, `MARKETING-REPORT-<domain>.pdf`, …) resolve **relative to the current working directory**, not from any config file or setting. There is nothing named "output folder" to configure — CWD is the only lever.

Within that CWD, output actually lands one level down, in a dated folder — `YYYY-MM-DD - Marketing Audit/`, shared by every skill run that day, versioned to `-01`, `-02`, ... on same-day reruns rather than overwritten. See `references/output-location.md` for the exact rule. This gives you history across days automatically; it does not give you history across clients — two clients run the same day from the same CWD still land in the same dated folder and still collide.

That gives you two ways to run more than one client through the same install:

- **One folder per client, same project.** `clientA/_grounding/`, `clientB/_grounding/`, each with its own subfolder for working files. As long as your CWD is inside `clientA/` when you run a command, its grounding is the nearest one found walking up, and its outputs land next to it. The lookup stops at the first `_grounding/` it finds — nearest wins — but it does not stop at a client boundary you haven't drawn yourself. If CWD is the repo root, or a client subfolder that hasn't got its own `_grounding/` yet, the search keeps walking up and can pick up a *different* client's folder instead. Wrong grounding loads silently — no error.
- **One project per client (recommended once CLAUDE.md is client-specific).** Separate repo/folder per client, each with its own `.claude/skills/` clone (or a symlink back to one shared install — the plugin keeps no state outside its own folder, so either works). This is the safer default once a top-level `CLAUDE.md` starts naming one client by name, the way this repo's does for IDT: mixing a second client into the same tree means their outputs and grounding both depend on you never running a command from the wrong directory.

Either way, most output filenames are generic (`MARKETING-AUDIT.md`, `SEO-AUDIT.md`, `MARKETING-REPORT.md`) — not client- or domain-namespaced. The dated folder protects same-client reruns from overwriting each other; it does not namespace by client, so two clients sharing one folder on the same day still overwrite each other's files inside it. Only the PDF report auto-namespaces beyond that (`MARKETING-REPORT-<domain>.pdf`).

One thing that does hold regardless of how you lay the folders out: the five audit subagents cannot reach across a client boundary, because they cannot reach the filesystem at all. They carry no file-discovery tools and may open only the paths the orchestrator names in that run's **Data Manifest** (`skills/audit/SKILL.md`, 0.1), which excludes previous audit reports and analytics exports by rule. A second client's numbers sitting in the same tree therefore cannot surface in the wrong report. That protects the analysis; it does not protect grounding lookup or output filenames, which still depend on your CWD as described above.

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
| AIDA (Attention-Interest-Desire-Action) | `copy` | [Wikipedia](https://en.wikipedia.org/wiki/AIDA_(marketing)) |
| PAS (Problem-Agitate-Solve) | `copy` | [Copywrite Matters](https://www.copywritematters.com/pas-classic-copywriting-formula/) |
| Before-After-Bridge | `copy` | [Blak Sheep Creative](https://blaksheepcreative.com/digital-marketing/content-marketing/copywriting/before-after-bridge/) |
| 4U Formula (Useful/Ultra-specific/Unique/Urgent) | `copy`, `landing` | [AWAI](https://www.awai.com/2001/06/a-review-of-the-4-us/) (originating org) |
| Value Proposition Canvas | `copy` | [Strategyzer](https://www.strategyzer.com/library/mastering-value-propositions) (Osterwalder's own) |
| E-E-A-T | `seo`, `market-technical` | [Google Search Central](https://developers.google.com/search/blog/2022/12/google-raters-guidelines-e-e-a-t) |
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

Want to add an external concept, framework, or piece of research (a report, an
article, a survey) to the suite? See [EXTENDING.md](EXTENDING.md) — where it
should land, how to cite it, and how to keep pack files independent.

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

## Origin and attribution

Market Context Kit began as a fork of Zubair Trabzada's [AI Marketing Suite for Claude Code](https://github.com/zubair-trabzada/ai-marketing-claude). It has since added a skills-directory plugin architecture, project grounding, context-specific example packs, B2B and regulated-industry workflows, and broader regional guidance.

The complete Git history is retained. The original MIT copyright notice remains in [LICENSE](LICENSE), alongside the copyright notice for subsequent work.

---

## License

MIT License — see [LICENSE](LICENSE) for details.
