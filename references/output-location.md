# Output Location

Every skill that writes a report file (`audit`, `seo`, `competitors`, `report`,
`report-pdf`) resolves where it writes through this rule instead of writing
straight into the working directory. Without it, reruns silently overwrite
each other and there is no history of past audits.

## The folder

Every write lands inside a dated folder, in the current working directory:

```
YYYY-MM-DD - Marketing Audit/
```

using today's date. This is one folder for the whole day, shared by every
skill in this suite — an audit run this morning and a competitor scan this
afternoon land side by side in it, the way a single audit session's outputs
belong together.

## Resolution steps

Run this before any Write tool call that produces one of this suite's report
files:

1. List directories in the current working directory matching today's date:
   `YYYY-MM-DD - Marketing Audit` or `YYYY-MM-DD-NN - Marketing Audit`.
2. None exist → target is `YYYY-MM-DD - Marketing Audit`. Create it, write
   there.
3. One or more exist → take the highest-numbered one (bare date sorts before
   `-01`, `-01` before `-02`, ...). Check whether it already contains a file
   with this skill's exact target filename (e.g. `MARKETING-AUDIT.md`).
   - Not present → reuse this folder. Different skill, same day, same
     folder.
   - Present → this is a rerun of the same skill, same day. Do not
     overwrite it. Create the next unused suffix (`-01` if only the bare
     folder exists, `-02` if `-01` is taken, ...) and write there instead.
4. State the resolved path in the terminal output, e.g. "Full report saved
   to: `2026-08-15 - Marketing Audit/MARKETING-AUDIT.md`".

## Reading prior output (report, report-pdf)

Skills that read other skills' output (`report`, `report-pdf`) look for
source files in today's resolved folder first. If several dated folders
exist for today (from reruns), prefer the highest-numbered one — it's the
most recent. If nothing for today exists, fall back to the flat working
directory, for files written before this convention existed or copied in
from elsewhere.

## Scope

This resolves paths within the current working directory only — it does not
walk parent directories the way grounding lookup does. Running this suite
against multiple clients from one install still means `cd` into each
client's own folder first (see README's "Multiple clients from one
install"); the dated folder nests under whichever directory you were in
when the skill ran.

## Optional report metadata

Before writing any report, run the plugin's
`scripts/resolve_report_metadata.py` from the project working directory with
`--toolkit "Market Context Kit"` and the exact active `--host`, `--provider`,
and `--model`. Use `python` on Windows and `python3` on macOS/Linux. Do not
guess any runtime value.

The resolver reads exactly `reporting.config.json` at the Git project root,
or in the current working directory outside Git:

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
