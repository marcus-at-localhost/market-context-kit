# Extending this suite

This is a process doc, not a skill — nothing loads it automatically. Read it when
you (or an agent working with you) want to add an external concept, framework,
or piece of research to the suite. It's not a marketing deliverable, so it
doesn't get a `/marketkit:` command of its own.

## 1. Extract the mechanism, not the case study

Read the full source — the article/report itself and anything it links to that
looks load-bearing (see §4 if a link won't fetch). Pull out the *procedure* or
*finding*, stripped of anecdote: "buyers split evenly across three interaction
modes regardless of industry" is usable; "McKinsey surveyed 4,000 people" on its
own is not.

Then ask: does this change what a skill actually outputs or scores, or is it
another example of something the suite already does? Only the first justifies
new text — skills degrade as they bloat.

### Client evaluation data never lands here

This suite gets developed while running it against real client sites. That work
product — domains, page copy, company names, contact people, findings, numbers —
belongs to the consuming project and must never be committed to this repo.

When a real run teaches the suite something, keep the mechanism and drop the
identity:

| Instead of | Write |
|---|---|
| "the 2026-08-15 `<client>.example` run" | "a 2026-08-15 run" |
| a quoted client headline as illustration | the pattern the headline exhibits |
| a client domain in a CLI example or test fixture | `example.com` |
| a real name in a metadata or template example | `<resolver value>` |

Attribution belongs in the consuming project's `config/reporting.config.json`,
never in a skill, reference, or template.

`tests/test_output_contract.py` enforces this: an allowlist of domains the kit's
own docs may name, and a check that metadata examples carry placeholders only. A
new client domain fails the suite with its file and line. If you genuinely need
a new external domain in the docs, add it to `ALLOWED_DOMAINS` deliberately.

## 2. Decide where it lands

The suite has one file type per kind of change:

| What you're adding | Goes in |
|---|---|
| Tactic, example, or framing specific to one business type | `references/examples/<pack>.md` (new section or extend an existing one) |
| A new evaluative signal that should affect the audit score | The relevant `agents/market-<name>.md` scoring rubric, plus its output table |
| Behavior specific to one skill (when/how to apply something) | A pointer line in `skills/market-<name>/SKILL.md` — not the full content, just where to find it and when to use it |
| A new business type entirely | `references/business-context.md` resolution logic, plus a new pack file |

A pack section only earns its place if at least one skill's SKILL.md points to
it. The suite doesn't blanket-load whole pack files for every decision — skills
cite named sections (`` `CTA phrasing` ``, `` `Lifecycle → sequence` ``, etc.) at
the point they need them. Content with no pointer sits there unread.

Don't touch packs you weren't asked to change. A labelled "B2B only" example
still sits in context and still shapes output for whoever reads it — see
`README.md`'s "Business type and example packs" section for why this suite
keeps packs separate at all.

## 3. Provenance bar

Every externally-sourced stat or framework gets two things, not one:

1. **A short inline mention** wherever it's used — survey/author name + year is
   enough. This keeps the file self-contained if a future skill loads only that
   one pack or agent file, without the README.
2. **An entry in README's "External Research Cited" section** — full citation,
   link, and vintage, so the number stays checkable and someone can tell if
   it's gone stale.

Generic named frameworks that aren't proprietary research (AIDA, PAS, E-E-A-T)
don't need this — they're industry-standard terms, not a specific party's data
point. The bar is for claims someone could ask "says who, and when?" about.
Add the framework to README's "Frameworks Referenced" table instead, so
there's still a link for background reading.

## 4. Fetching linked sources

Some publishers (mckinsey.com among them) block or time out direct `WebFetch`
calls to their own domain. If that happens:

- Try `WebSearch` for the specific article/concept — search-engine summaries
  usually surface the load-bearing claims even when the page itself won't fetch.
- Otherwise, tell the user which URLs failed and ask them to paste the text.
  Don't silently drop a linked source because the fetch failed — say so.

## 5. Work through it as a conversation, not a batch edit

Scope narrows fast once you start asking:

- Which piece(s) of the source are actually worth building? (Often only part
  of a source is suite-relevant — internal-org findings, HR topics, and
  generic AI-hype claims usually aren't.)
- Where does each piece land, per §2?
- Present the concrete diff (files touched, section headings, one worked
  example row) before writing anything, and wait for a yes.

That's the same bounded-change gate every other change in this repo goes
through — nothing here waives it.

## Quick checklist

```
1. Read source (+ linked material that's load-bearing) → have the mechanism, not the anecdote
2. Confirm it changes skill output/scoring, not just decoration
3. Pick landing spot(s) per the table in §2
4. Present scope + landing spot + a worked example → get a yes
5. Write it — pointer lines in every consuming skill, not just the pack
6. Strip client identity: mechanism stays, domains/copy/names go (§1)
7. Add the provenance entry to README's External Research Cited
8. Run pytest — the domain and attribution guards must pass
```
