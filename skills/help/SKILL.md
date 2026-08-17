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

Every command writes `MARKETKIT - <PURPOSE> - <SCOPE>.<extension>` into the active `Audit-YYYY-MM-DD[-NN]/` audit folder — see `${CLAUDE_PLUGIN_ROOT}/references/output-location.md`. `SCOPE` is the exact target domain for URL-based commands; topic-only commands ask for an explicit domain or customer scope first.

| Command | What it does | Purpose |
|---------|--------------|--------|
| `/marketkit:audit <url>` | Full marketing audit, 5 parallel subagents, scored 0-100 | `MARKETING-AUDIT` |
| `/marketkit:copy <url>` | Copy analysis and before/after rewrites | `COPY-SUGGESTIONS` |
| `/marketkit:seo <url>` | SEO content audit, on-page + E-E-A-T + technical | `SEO-AUDIT` |
| `/marketkit:landing <url>` | Landing page CRO, section by section | `LANDING-CRO` |
| `/marketkit:funnel <url>` | Funnel mapping and drop-off analysis | `FUNNEL-ANALYSIS` |
| `/marketkit:competitors <url>` | Competitive intelligence and gap analysis | `COMPETITOR-REPORT` |
| `/marketkit:brand <url>` | Brand voice analysis and guidelines | `BRAND-VOICE` |
| `/marketkit:content-plan <url>` | Topic research, content plan, article drafts | `CONTENT-PLAN` + `ARTICLE-<SLUG>` |
| `/marketkit:emails <topic-or-url>` | Email sequences with subject lines and cadence | `EMAIL-SEQUENCES` |
| `/marketkit:social <topic-or-url>` | 30-day social calendar and platform posts | `SOCIAL-CALENDAR` |
| `/marketkit:ads <url>` | Ad creative, targeting, and budget plan | `AD-CAMPAIGNS` |
| `/marketkit:launch <product>` | Launch playbook and timeline | `LAUNCH-PLAYBOOK` |
| `/marketkit:proposal <client>` | Client-ready services proposal | `CLIENT-PROPOSAL` |
| `/marketkit:report <url>` | Combined Markdown report from prior outputs | `MARKETING-REPORT` (.md) |
| `/marketkit:report-pdf <url>` | Same report as a branded PDF with charts | `MARKETING-REPORT` (.pdf) + `REPORT-DATA` (.json, flat under `data/`) |

Namespaced forms also work: `/marketkit:audit`. Claude invokes these on its own when a request matches — you do not have to type the command.

## Which one to start with

- **Whole site, do not know where to start** → `/marketkit:audit`
- **One page underperforming** → `/marketkit:landing`, or `/marketkit:copy` for wording only
- **Not enough traffic** → `/marketkit:seo`, then `/marketkit:content-plan`
- **Traffic but no leads** → `/marketkit:funnel`
- **Pitching a client** → `/marketkit:audit`, then `/marketkit:report-pdf`, then `/marketkit:proposal`

## How they chain

These skills read each other's output from the active audit folder's exact same-scope filenames when present, so order matters:

- `/marketkit:audit` — incorporates `MARKETKIT - COMPETITOR-REPORT - <domain>.md` and `MARKETKIT - BRAND-VOICE - <domain>.md` if they exist
- `/marketkit:copy` — sharper after `/marketkit:brand`
- `/marketkit:emails` — uses `/marketkit:funnel` findings
- `/marketkit:content-plan` — consumes `/marketkit:brand`, `/marketkit:competitors`, `/marketkit:seo`; offers to run them if missing
- `/marketkit:report` and `/marketkit:report-pdf` — compile everything available

None of them search an older audit folder automatically — a prior day's run must be named explicitly.

## Grounding and business context

Every command starts by looking for a `_grounding/` folder in the working directory or its parents. One customer project keeps one shared `_grounding/`. If one exists, the client's own positioning, target industries, competitor set and claim rules override the suite's defaults, and each output names the files it loaded. See `${CLAUDE_PLUGIN_ROOT}/references/grounding.md`.

Each command then resolves the business type and loads exactly one example pack — `consumer-online` or `b2b-technical` — so hooks, CTAs, objections and launch plans match how the business actually sells. See `${CLAUDE_PLUGIN_ROOT}/references/business-context.md`. When the type is unclear, no pack is loaded and examples are derived from the site's own copy.

## Report metadata

Optional attribution reads from `config/reporting.config.json` at the Git project root; a legacy root-level `reporting.config.json` still works but warns to move. See `${CLAUDE_PLUGIN_ROOT}/references/output-location.md`.

## Requirements

Python 3 for the bundled scripts (`analyze_page.py`, `competitor_scanner.py`, `social_calendar.py`, `generate_pdf_report.py`) — stdlib only, no install needed. `/marketkit:report-pdf` additionally needs `reportlab`; `competitor_scanner.py` optionally uses `trafilatura` for cleaner content extraction if present, and falls back to its stdlib parser if not:

```bash
pip install reportlab
pip install trafilatura   # optional
```
