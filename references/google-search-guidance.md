# Google Search guidance

## Myth Guardrail

Never emit as a finding, recommendation, or scored gap — any severity, any skill:

| Do not recommend | Say this instead |
|---|---|
| "Add an llms.txt" | Google Search ignores it — neither harms nor helps |
| "Chunk content smaller so AI can parse it" | Google reads multi-topic pages and extracts sections in context |
| "Write in an AI-friendly style" / AI-targeted keyword variants | Synonyms and phrasing are handled; excess variants risk the spam policies |
| "Get more mentions across the web" as volume tactic | Ranking systems weigh content value; spam systems block manufactured mentions |
| "Add schema so AI can understand you" | Schema earns rich results and entity clarity, not generative-AI eligibility |

## Grounding Precedence

Grounding outranks this file (`grounding.md`): a myth check a criterion asks for still runs.
It never becomes a score.

- **Grounding asks** (e.g. a criterion asking whether `llms.txt` is current) → run it, report
  the fact with evidence, attach Google's verdict. Never a scored gap, severity rating, or
  revenue-impact recommendation.
- **Grounding silent** → do not raise the topic at all.
- **Non-myth criteria in the same block** (crawlability, sitemap presence, JS-only content,
  text-near versions) score normally — Google's AI guide lists them as real requirements.

## Schema Scoring

Schema stays recommended on SEO grounds: rich-result eligibility, entity clarity via
`Organization` + `sameAs`, Merchant Center feeds, machine-readable facts. Not a ranking
factor, and no generative-AI eligibility.

Score rich-result-eligible types that are **present, valid, and matching visible page
content** — not checklist coverage. A page type with no eligible type is not a gap for
lacking schema; most B2B service, about, and category pages qualify. Cap missing-schema
severity at Medium unless it breaks an existing rich result.

Eligible types change — resolve at audit time against Google's
[search gallery](https://developers.google.com/search/docs/appearance/structured-data/search-gallery),
not a memorized list; `FAQ` and `HowTo` are currently restricted.

## Provenance

- [AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide),
  [Mythbusting](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide#mythbusting)
- [Creating helpful content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- Fetched 2026-08-20.
