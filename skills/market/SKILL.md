---
name: market
description: Index of the AI Marketing Suite commands. Manual reference only.
disable-model-invocation: true
metadata:
  version: 2.0.0
---

# AI Marketing Suite — Command Index

Fifteen marketing skills for analyzing websites, generating content, auditing funnels, and producing client deliverables. Each one is its own command — invoke it directly. There is no routing step.

| Command | What it does | Output |
|---------|--------------|--------|
| `/market-audit <url>` | Full marketing audit, 5 parallel subagents, scored 0-100 | `MARKETING-AUDIT.md` |
| `/market-copy <url>` | Copy analysis and before/after rewrites | `COPY-SUGGESTIONS.md` |
| `/market-seo <url>` | SEO content audit, on-page + E-E-A-T + technical | `SEO-AUDIT.md` |
| `/market-landing <url>` | Landing page CRO, section by section | `LANDING-CRO.md` |
| `/market-funnel <url>` | Funnel mapping and drop-off analysis | `FUNNEL-ANALYSIS.md` |
| `/market-competitors <url>` | Competitive intelligence and gap analysis | `COMPETITOR-REPORT.md` |
| `/market-brand <url>` | Brand voice analysis and guidelines | `BRAND-VOICE.md` |
| `/market-content-plan <url>` | Topic research, content plan, article drafts | `CONTENT-PLAN.md` + `articles/*.md` |
| `/market-emails <topic>` | Email sequences with subject lines and cadence | `EMAIL-SEQUENCES.md` |
| `/market-social <topic>` | 30-day social calendar and platform posts | `SOCIAL-CALENDAR.md` |
| `/market-ads <url>` | Ad creative, targeting, and budget plan | `AD-CAMPAIGNS.md` |
| `/market-launch <product>` | Launch playbook and timeline | `LAUNCH-PLAYBOOK.md` |
| `/market-proposal <client>` | Client-ready services proposal | `CLIENT-PROPOSAL.md` |
| `/market-report <url>` | Combined Markdown report from prior outputs | `MARKETING-REPORT.md` |
| `/market-report-pdf <url>` | Same report as a branded PDF with charts | `MARKETING-REPORT-<domain>.pdf` |

Namespaced forms also work: `/ai-marketing:market-audit`. Claude invokes these on its own when a request matches — you do not have to type the command.

## Which one to start with

- **Whole site, do not know where to start** → `/market-audit`
- **One page underperforming** → `/market-landing`, or `/market-copy` for wording only
- **Not enough traffic** → `/market-seo`, then `/market-content-plan`
- **Traffic but no leads** → `/market-funnel`
- **Pitching a client** → `/market-audit`, then `/market-report-pdf`, then `/market-proposal`

## How they chain

These skills read each other's output files from the working directory when present, so order matters:

- `/market-audit` — incorporates `COMPETITOR-REPORT.md` and `BRAND-VOICE.md` if they exist
- `/market-copy` — sharper after `/market-brand`
- `/market-emails` — uses `/market-funnel` findings
- `/market-content-plan` — consumes `/market-brand`, `/market-competitors`, `/market-seo`; offers to run them if missing
- `/market-report` and `/market-report-pdf` — compile everything available

## Requirements

Python 3 for the bundled scripts (`analyze_page.py`, `competitor_scanner.py`, `social_calendar.py`, `generate_pdf_report.py`) — stdlib only, no install needed. `/market-report-pdf` additionally needs `reportlab`:

```bash
pip install reportlab
```
