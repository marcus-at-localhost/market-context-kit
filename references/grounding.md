# Grounding

Client truth beats every default in this suite. When a project ships a grounding folder, load it
before analyzing anything and let it override the skill's own examples, benchmarks and phrasing.

## Discovery

Look for a `_grounding/` directory in the current working directory, then in each parent
directory, stopping at the repository root or after three levels.

If none exists, continue with site evidence only. Never block on it, never ask the user to create
one, never invent its contents.

## What to load

Read `_grounding/README.md` first. A well-formed grounding folder maps tasks to files, e.g.:

```
- Artikelideen: 00_master_context.md, 03_industries_and_target_groups.md, ...
- Website-Audit: 00_master_context.md, 10_website_audit_rules.md, ...
- Wettbewerbsanalyse: 00_master_context.md, 07_competitors_and_market.md, ...
```

Use that map and load the entry closest to the task at hand. If there is no map, load
`00_master_context.md` plus any file whose name matches the task (positioning, competitors,
content rules, claims, audit rules).

Load whole files. Do not skim a grounding file for one keyword — the constraints in it are the
point.

## Precedence

```
grounding file  >  observed site evidence  >  skill default example
```

A skill default that contradicts grounding is **dropped, not blended**. If grounding says the
company sells through distributors and RFQ, do not soften it into "consider adding a free trial
alongside your RFQ path". If grounding names the tone, do not average it with the tone this
skill's examples happen to use.

Site evidence still wins over grounding on matters of fact about the live site — grounding
describes intent, the page describes reality. Where they disagree, report the gap; that gap is
usually a finding.

## Claim discipline

If the folder contains a claims or evidence file (e.g. `11_claims_and_evidence.md`), it governs
what may be asserted in generated copy: which superlatives are allowed, which certifications may
be named, which numbers are approved. Apply it to every headline, ad, email and landing-page line
you produce. Unsupported claims are a defect, not a stylistic choice.

## Language

Grounding is usually written in the client's working language. Produce output in the language of
the target website unless the user asks otherwise, and take terminology from the grounding files
rather than translating your own.

## Reporting

Every output that used grounding names the files it loaded, near the top:

```markdown
> Grounding: `_grounding/00_master_context.md`, `_grounding/10_website_audit_rules.md`,
> `_grounding/11_claims_and_evidence.md`
```

If no grounding folder was found, say so once in the same place. A reader must be able to tell
which claims came from client truth and which came from this skill's defaults.

## Passing grounding to subagents

Subagents share none of the orchestrator's context and cannot be relied on to rediscover
`_grounding/`. Any skill that dispatches subagents must include a **grounding digest** in each
prompt: the list of loaded files plus a condensed extract covering positioning, target industries
and buyers, competitors, claim rules and tone. Without it the subagents fall back to this suite's
defaults while the orchestrator does not, and the merged report contradicts itself.
