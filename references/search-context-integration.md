# Search Context artifact integration

Use this contract only when a Market Context Kit skill needs measured search or analytics evidence from the optional Search Context Kit companion.

## Resolve one artifact

1. Prefer an exact path explicitly supplied by the user.
2. Otherwise, search only the current client's working directory for `YYYY-MM-DD - Search Context/<exact target domain>/SEARCH-CONTEXT.v1.json`.
3. If more than one exact-domain artifact exists, prefer the newest valid reporting period and name the selected path. Do not combine artifacts implicitly.
4. Do not search another client's directory, infer domain ownership from a filename, or use a generic analytics export as a substitute.
5. If no candidate exists, continue without Search Context and state that the optional evidence was unavailable.

## Validate before reading values

Reject the candidate as evidence unless all checks pass:

- `schema_version` is exactly `1.0`.
- `domain` is the exact target domain after lowercase and terminal-dot normalization. A related brand domain, language domain, subdomain, or redirect target is not an automatic match.
- The reporting period contains valid ISO `start` and `end` dates and start is not after end.
- Every source status is visible and uses `ok`, `partial`, `error`, or `disabled`.
- Measurement collections are lists and no required top-level field is malformed.

Name the artifact path, domain, reporting period, and source status in the output. If the requested analysis is “current” but the period is stale, do not use it silently: state the age and ask for or recommend a fresh collection. Historical analysis may use an older period when it is named explicitly.

## Evidence boundaries

- `ok`: use present values for the named provider and period.
- `partial`: use only present values and repeat the limitation.
- `error` or `disabled`: do not treat the provider or its fields as zero.
- `null`: unknown, never zero.
- Search Context estimates remain estimates. Do not convert estimated clicks into revenue, conversions, or causation.
- Supplemental structured data and prose retain their own paths and provenance. A form export may support inquiry counts; Matomo visits alone may not.
- Distinguish measured values, user-supplied context, and inference in client-facing prose.

## Audit independence

The artifact is orchestrator-only evidence. `SEARCH-CONTEXT.v1.json` never goes on the Data Manifest and its content must not be pasted, summarized, or hinted into any audit subagent prompt. Do not paste Search Context data into any subagent prompt.

Load it only after the five audit subagents have returned independently and passed manifest reconciliation. It may prioritize or corroborate recommendations during synthesis, but it must not change an audit score, rescore a dimension, or serve as a replacement score. Specifically, do not change the six audit scores or the weighted composite because of Search Context evidence.

## Safe failure

On malformed JSON, unsupported schema, domain mismatch, invalid period, or missing source status:

1. Exclude the artifact.
2. Name the reason and path.
3. Continue with the skill's normal non-analytics workflow when possible.
4. Never “repair” or overwrite the source artifact from Market Context Kit.
