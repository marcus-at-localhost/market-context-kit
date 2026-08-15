---
name: help
description: Index of the Market Context Kit commands. Manual reference only.
disable-model-invocation: true
metadata:
  version: 3.0.0
---

# Market Context Kit — Command Index

Fifteen marketing skills for analyzing websites, generating content, auditing funnels, and producing client deliverables. Each one is its own command — invoke it directly. There is no routing step.

The suite loads as a plugin, so the `marketkit:` prefix is part of every trigger. Dropping it does not resolve.

| Command | What it does | Output |
|---------|--------------|--------|
| `/marketkit:audit <url>` | Full marketing audit, 5 parallel subagents, scored 0-100 | `MARKETING-AUDIT.md` |
| `/marketkit:copy <url>` | Copy analysis and before/after rewrites | `COPY-SUGGESTIONS.md` |
| `/marketkit:seo <url>` | SEO content audit, on-page + E-E-A-T + technical | `SEO-AUDIT.md` |
| `/marketkit:landing <url>` | Landing page CRO, section by section | `LANDING-CRO.md` |
| `/marketkit:funnel <url>` | Funnel mapping and drop-off analysis | `FUNNEL-ANALYSIS.md` |
| `/marketkit:competitors <url>` | Competitive intelligence and gap analysis | `COMPETITOR-REPORT.md` |
| `/marketkit:brand <url>` | Brand voice analysis and guidelines | `BRAND-VOICE.md` |
| `/marketkit:content-plan <url>` | Topic research, content plan, article drafts | `CONTENT-PLAN.md` + `articles/*.md` |
| `/marketkit:emails <topic>` | Email sequences with subject lines and cadence | `EMAIL-SEQUENCES.md` |
| `/marketkit:social <topic>` | 30-day social calendar and platform posts | `SOCIAL-CALENDAR.md` |
| `/marketkit:ads <url>` | Ad creative, targeting, and budget plan | `AD-CAMPAIGNS.md` |
| `/marketkit:launch <product>` | Launch playbook and timeline | `LAUNCH-PLAYBOOK.md` |
| `/marketkit:proposal <client>` | Client-ready services proposal | `CLIENT-PROPOSAL.md` |
| `/marketkit:report <url>` | Combined Markdown report from prior outputs | `MARKETING-REPORT.md` |
| `/marketkit:report-pdf <url>` | Same report as a branded PDF with charts | `MARKETING-REPORT-<domain>.pdf` |

Namespaced forms also work: `/marketkit:audit`. Claude invokes these on its own when a request matches — you do not have to type the command.

## Which one to start with

- **Whole site, do not know where to start** → `/marketkit:audit`
- **One page underperforming** → `/marketkit:landing`, or `/marketkit:copy` for wording only
- **Not enough traffic** → `/marketkit:seo`, then `/marketkit:content-plan`
- **Traffic but no leads** → `/marketkit:funnel`
- **Pitching a client** → `/marketkit:audit`, then `/marketkit:report-pdf`, then `/marketkit:proposal`

## How they chain

These skills read each other's output files from the working directory when present, so order matters:

- `/marketkit:audit` — incorporates `COMPETITOR-REPORT.md` and `BRAND-VOICE.md` if they exist
- `/marketkit:copy` — sharper after `/marketkit:brand`
- `/marketkit:emails` — uses `/marketkit:funnel` findings
- `/marketkit:content-plan` — consumes `/marketkit:brand`, `/marketkit:competitors`, `/marketkit:seo`; offers to run them if missing
- `/marketkit:report` and `/marketkit:report-pdf` — compile everything available

## Grounding and business context

Every command starts by looking for a `_grounding/` folder in the working directory or its parents. If one exists, the client's own positioning, target industries, competitor set and claim rules override the suite's defaults, and each output names the files it loaded. See `${CLAUDE_PLUGIN_ROOT}/references/grounding.md`.

Each command then resolves the business type and loads exactly one example pack — `consumer-online` or `b2b-technical` — so hooks, CTAs, objections and launch plans match how the business actually sells. See `${CLAUDE_PLUGIN_ROOT}/references/business-context.md`. When the type is unclear, no pack is loaded and examples are derived from the site's own copy.

## Requirements

Python 3 for the bundled scripts (`analyze_page.py`, `competitor_scanner.py`, `social_calendar.py`, `generate_pdf_report.py`) — stdlib only, no install needed. `/marketkit:report-pdf` additionally needs `reportlab`; `competitor_scanner.py` optionally uses `trafilatura` for cleaner content extraction if present, and falls back to its stdlib parser if not:

```bash
pip install reportlab
pip install trafilatura   # optional
```
