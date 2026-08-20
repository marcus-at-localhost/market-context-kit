# Output Location

Every skill that writes a report file (`audit`, `seo`, `competitors`, `report`,
`report-pdf`, and every other file-writing skill in this suite) resolves where
it writes through this rule instead of writing straight into the working
directory or inventing its own folder. This is the same shared contract
Search Context Kit uses, so both toolkits' outputs land side by side in one
place.

## The folder

Every write lands inside the single active audit folder, in the project's
Git root (or the current working directory outside Git):

```
Audit/
```

There is no per-day or per-run folder — `Audit/` is always the target,
shared by every skill in this suite and by Search Context Kit. A marketing
audit run this morning and a search report run three days later land side by
side in the same folder.

Re-running the same purpose/scope **overwrites the existing file in
place**; git history is the version record. When a project or engagement is
finished, archive it yourself by renaming `Audit/` to whatever you like (a
date, a number, a client tag) — the resolver and every skill in this suite
only ever target the live `Audit/`, never an archived or renamed sibling.

## Resolving a path

Run the resolver before any Write tool call that produces one of this suite's
files, from the project working directory:

```
python "${CLAUDE_PLUGIN_ROOT}/scripts/resolve_audit_output.py" ^
  --purpose MARKETING-AUDIT ^
  --scope example.com ^
  --extension md
```

On Windows, use `python` and either PowerShell line continuation (`` ` ``) or
one line; on macOS/Linux, use `python3`. Add `--data` for internal
intermediates that belong flat under `data/` instead of the audit root.

The command prints one compact JSON object:

```json
{"project_root":"...","audit_dir":"...","data_dir":"...","output_path":"..."}
```

`output_path` is authoritative. Use it exactly for the Write tool call and
state it in the terminal output, e.g. "Full report saved to:
`Audit/MARKETKIT - MARKETING-AUDIT - example.com.md`". Do not reconstruct
the path yourself or guess a folder name.

### The algorithm the resolver implements

1. Find the project root (`git rev-parse --show-toplevel`, or the current
   working directory outside Git).
2. Target `Audit/` at the project root, always — create it (and its `data/`
   subfolder when `--data` is set) if it does not exist yet.
3. Resolve `output_path` inside it. If a file with this exact target
   filename already exists there, it gets overwritten in place — git
   history is the version record, not a numbered sibling folder.

## Filename contract

Every generated name follows:

```
<TOOLKIT> - <PURPOSE> - <SCOPE>.<extension>
```

with no underscores. `TOOLKIT` is `MARKETKIT` for every file this suite
writes. `PURPOSE` is an uppercase-kebab token identifying the report or
artifact (`MARKETING-AUDIT`, `COMPETITOR-REPORT`, `SEO-AUDIT`,
`MARKETING-REPORT`, `AD-CAMPAIGNS`, `BRAND-VOICE`, `CONTENT-PLAN`,
`COPY-SUGGESTIONS`, `EMAIL-SEQUENCES`, `FUNNEL-ANALYSIS`, `LANDING-CRO`,
`LAUNCH-PLAYBOOK`, `CLIENT-PROPOSAL`, `SOCIAL-CALENDAR`, `REPORT-DATA`, and
per-article `ARTICLE-<UPPERCASE-KEBAB-SLUG>`). `SCOPE` is the exact
normalized target domain for URL-based workflows, or an explicit
customer/topic token the user supplied for topic-only workflows — never
invented.

Reports live directly in the active audit folder. Internal intermediates
(PDF source JSON, scratch data) live flat under its `data/` subfolder — never
in a nested `raw/` or per-domain subfolder.

## Reading prior output

Skills that read sibling output (`report`, `report-pdf`, and any skill
checking for a same-scope prerequisite) look **only inside the active
`Audit/` folder** resolved above, using the exact same-scope filename, for
example `MARKETKIT - COMPETITOR-REPORT - example.com.md` next to
`MARKETKIT - MARKETING-AUDIT - example.com.md`. Never search an archived or
renamed folder automatically — a prior engagement's evidence is out of
scope unless the user names its path explicitly.

## Scope

The resolver walks up from the current working directory to the Git project
root; it does not search parent directories beyond that. Running this suite
against multiple clients from one install still means `cd` into each
client's own project first (see README's "Multiple clients from one
install"); the audit folder lands at that project's root.

## Optional report metadata

Before writing any report, run the plugin's
`scripts/resolve_report_metadata.py` from the project working directory with
`--toolkit "Market Context Kit"` and the exact active `--host`, `--provider`,
and `--model`. Use `python` on Windows and `python3` on macOS/Linux. Do not
guess any runtime value.

The resolver reads `config/reporting.config.json` at the Git project root
first. A legacy `reporting.config.json` directly at the project root still
works but emits a `FutureWarning` asking it to move under `config/`; if both
exist, the resolver raises an error rather than pick one silently — move the
legacy file before continuing.

- Output `null`: omit all report metadata, including toolkit and model.
- Output JSON: reproduce those exact fields as YAML front matter in Markdown.
  For `report-pdf`, store the object unchanged as `report_metadata` in the
  intermediate JSON so the generator can set the visible credit and PDF
  properties.
- Error: stop. Report the invalid configuration or unavailable exact runtime
  identity instead of silently dropping or inventing metadata.

Never construct attribution directly from `AGENTS.md`, `CLAUDE.md`, a skill,
or a template. The tracked `config/reporting.example.json` documents the
schema but is never a metadata fallback.

### Canonical front-matter shape

When the resolver returns JSON, the Markdown file **begins** with the block —
first byte of the file, before the H1, before any grounding note. Copy the
resolver's values verbatim; do not reorder, rename, reformat, or add keys.

```markdown
---
prepared_by: <resolver value>
document_author: <resolver value>
toolkit: Market Context Kit
host: <exact active host>
llm_provider: <exact active provider>
llm_model: <exact active model id>
generated_at: <resolver ISO-8601 timestamp>
---
# Report Title
```

Keys and order come from the resolver's JSON; every value is filled from that
output and from nothing else. Never write a real person or organization into
this file, a skill, or a template — attribution exists only in the consuming
project's `config/reporting.config.json`. When the resolver returns `null`, no
`---` block is written at all; a report with empty or placeholder metadata keys
is a defect, not a degraded success.

### Why this step gets skipped

This section is the single source of truth, but a skill's own Phase 0 command
list and Output Format template are what an agent actually follows step by
step. If either omits metadata, it silently overrides this reference — a
template that opens on `# Title` reads as a complete file spec.

Every skill that writes a Markdown report therefore restates the resolver
call in its own Phase 0 **and** carries a front-matter slot at the top of its
Output Format template. `tests/test_output_contract.py` enforces both. When
adding a report-writing skill, add it to that test.
