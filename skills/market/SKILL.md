---
name: market
description: Index of the AI Marketing Suite commands. Manual reference only.
disable-model-invocation: true
metadata:
  version: 2.0.0
---

# AI Marketing Suite — Command Index

Fifteen marketing skills for analyzing websites, generating content, auditing funnels, and producing client deliverables. Each one is its own command — invoke it directly. There is no routing step.

The suite loads as a plugin, so the `ai-marketing:` prefix is part of every trigger. Dropping it does not resolve.

| Command | What it does | Output |
|---------|--------------|--------|
| `/ai-marketing:market-audit <url>` | Full marketing audit, 5 parallel subagents, scored 0-100 | `MARKETING-AUDIT.md` |
| `/ai-marketing:market-copy <url>` | Copy analysis and before/after rewrites | `COPY-SUGGESTIONS.md` |
| `/ai-marketing:market-seo <url>` | SEO content audit, on-page + E-E-A-T + technical | `SEO-AUDIT.md` |
| `/ai-marketing:market-landing <url>` | Landing page CRO, section by section | `LANDING-CRO.md` |
| `/ai-marketing:market-funnel <url>` | Funnel mapping and drop-off analysis | `FUNNEL-ANALYSIS.md` |
| `/ai-marketing:market-competitors <url>` | Competitive intelligence and gap analysis | `COMPETITOR-REPORT.md` |
| `/ai-marketing:market-brand <url>` | Brand voice analysis and guidelines | `BRAND-VOICE.md` |
| `/ai-marketing:market-content-plan <url>` | Topic research, content plan, article drafts | `CONTENT-PLAN.md` + `articles/*.md` |
| `/ai-marketing:market-emails <topic>` | Email sequences with subject lines and cadence | `EMAIL-SEQUENCES.md` |
| `/ai-marketing:market-social <topic>` | 30-day social calendar and platform posts | `SOCIAL-CALENDAR.md` |
| `/ai-marketing:market-ads <url>` | Ad creative, targeting, and budget plan | `AD-CAMPAIGNS.md` |
| `/ai-marketing:market-launch <product>` | Launch playbook and timeline | `LAUNCH-PLAYBOOK.md` |
| `/ai-marketing:market-proposal <client>` | Client-ready services proposal | `CLIENT-PROPOSAL.md` |
| `/ai-marketing:market-report <url>` | Combined Markdown report from prior outputs | `MARKETING-REPORT.md` |
| `/ai-marketing:market-report-pdf <url>` | Same report as a branded PDF with charts | `MARKETING-REPORT-<domain>.pdf` |

Namespaced forms also work: `/ai-marketing:market-audit`. Claude invokes these on its own when a request matches — you do not have to type the command.

## Which one to start with

- **Whole site, do not know where to start** → `/ai-marketing:market-audit`
- **One page underperforming** → `/ai-marketing:market-landing`, or `/ai-marketing:market-copy` for wording only
- **Not enough traffic** → `/ai-marketing:market-seo`, then `/ai-marketing:market-content-plan`
- **Traffic but no leads** → `/ai-marketing:market-funnel`
- **Pitching a client** → `/ai-marketing:market-audit`, then `/ai-marketing:market-report-pdf`, then `/ai-marketing:market-proposal`

## How they chain

These skills read each other's output files from the working directory when present, so order matters:

- `/ai-marketing:market-audit` — incorporates `COMPETITOR-REPORT.md` and `BRAND-VOICE.md` if they exist
- `/ai-marketing:market-copy` — sharper after `/ai-marketing:market-brand`
- `/ai-marketing:market-emails` — uses `/ai-marketing:market-funnel` findings
- `/ai-marketing:market-content-plan` — consumes `/ai-marketing:market-brand`, `/ai-marketing:market-competitors`, `/ai-marketing:market-seo`; offers to run them if missing
- `/ai-marketing:market-report` and `/ai-marketing:market-report-pdf` — compile everything available

## Grounding and business context

Every command starts by looking for a `_grounding/` folder in the working directory or its parents. If one exists, the client's own positioning, target industries, competitor set and claim rules override the suite's defaults, and each output names the files it loaded. See `${CLAUDE_PLUGIN_ROOT}/references/grounding.md`.

Each command then resolves the business type and loads exactly one example pack — `consumer-online` or `b2b-technical` — so hooks, CTAs, objections and launch plans match how the business actually sells. See `${CLAUDE_PLUGIN_ROOT}/references/business-context.md`. When the type is unclear, no pack is loaded and examples are derived from the site's own copy.

## Requirements

Python 3 for the bundled scripts (`analyze_page.py`, `competitor_scanner.py`, `social_calendar.py`, `generate_pdf_report.py`) — stdlib only, no install needed. `/ai-marketing:market-report-pdf` additionally needs `reportlab`:

```bash
pip install reportlab
```
