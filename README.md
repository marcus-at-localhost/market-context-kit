<p align="center">
  <img src="banner.svg" alt="AI Marketing Suite for Claude Code" width="100%">
</p>

# AI Marketing Suite for Claude Code

A comprehensive marketing analysis and automation skill system for [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Audit any website's marketing, generate copy, build email sequences, create content calendars, analyze competitors, and produce client-ready PDF reports — all from your terminal.

**Built for entrepreneurs, agency builders, and solopreneurs who want to sell marketing services powered by AI.**

---

## What This Does

Type a command in Claude Code and get instant, actionable marketing analysis:

```
> /market-audit https://calendly.com

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

Type `/market` for the command index. Updating is `git pull` in the folder.

### Optional: PDF Report Support

```bash
pip install reportlab
```

Everything else runs on the Python standard library. Windows, macOS, and Linux are all supported.

---

## Commands

Each skill is its own command. There is no router — `/market` is just an index you can print. Claude also invokes these on its own when a request matches, so you rarely have to type one.

| Command | What It Does |
|---------|-------------|
| `/market` | Index of every command, with a "which one first" guide |
| `/market-audit <url>` | Full marketing audit with 5 parallel agents |
| `/market-copy <url>` | Generate optimized copy with before/after examples |
| `/market-emails <topic>` | Generate complete email sequences |
| `/market-social <topic>` | 30-day social media content calendar |
| `/market-ads <url>` | Ad creative and copy for all platforms |
| `/market-funnel <url>` | Sales funnel analysis and optimization |
| `/market-competitors <url>` | Competitive intelligence report |
| `/market-landing <url>` | Landing page CRO analysis |
| `/market-launch <product>` | Product launch playbook |
| `/market-proposal <client>` | Client proposal generator |
| `/market-report <url>` | Full marketing report (Markdown) |
| `/market-report-pdf <url>` | Professional marketing report (PDF) |
| `/market-seo <url>` | SEO content audit |
| `/market-brand <url>` | Brand voice analysis and guidelines |
| `/market-content-plan <url>` | Topic research + content plan + article drafts |

Namespaced forms work too: `/ai-marketing:market-audit`. Use them if a bare name collides with another skill.

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

---

## How It Works

1. **You type a command** — e.g., `/market-audit https://example.com`
2. **Claude reads the skill files** — they tell Claude exactly how to analyze the site
3. **5 subagents launch in parallel** — each one analyzes a different dimension
4. **Python scripts run** — automated page analysis, competitor scanning
5. **Results are compiled** — into a scored, prioritized, actionable report
6. **Output is saved** — as a Markdown file or professional PDF

---

## Use Cases

### For Agency Builders
- Run `/market-audit` on a prospect's website before a sales call
- Generate `/market-proposal` with specific findings and pricing
- Deliver `/market-report-pdf` as a professional client deliverable

### For Solopreneurs
- Use `/market-copy` to optimize your own landing pages
- Generate `/market-emails` for your product launches
- Build `/market-social` calendars for consistent posting

### For Content Creators
- Research competitors with `/market-competitors`
- Plan launches with `/market-launch`
- Analyze your funnel with `/market-funnel`

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
