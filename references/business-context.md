# Business Context Resolution

Every skill in this suite produces advice that only makes sense for some kinds of business. A
free-trial CTA is right for self-serve software and wrong for a gasket manufacturer. A hashtag
tier strategy is right for a DTC brand and irrelevant to a distributor.

So: resolve the business context first, then load only the matching example pack. The packs live
in `${CLAUDE_PLUGIN_ROOT}/references/examples/`.

## Step 1 — Resolve

In order of authority:

1. **Grounding** — if `_grounding/` was found (see `references/grounding.md`), it states the
   industry, buyers and commercial model. Use it. Stop here.
2. **User statement** — if the user described the business, use that.
3. **Site evidence** — classify from the signals below.

## Step 2 — Classify

| Business Type | Detection Signals | Pack |
|---|---|---|
| **Self-serve SaaS** | Free trial or freemium CTA, pricing tiers, "login", API docs | `consumer-online` |
| **E-commerce / DTC** | Product listings, cart, checkout, reviews, shipping info | `consumer-online` |
| **Creator / Course / Info product** | Lead magnets, email capture, course listings, community links | `consumer-online` |
| **Agency / Services** | Case studies, portfolio, "work with us", contact forms | `consumer-online` (commercial model is closest to it; take proof patterns from `b2b-technical`) |
| **Marketplace** | Two-sided messaging, buyer/seller flows, listing pages | `consumer-online` |
| **Local business** | Address, phone, opening hours, map embed, service area | `consumer-online` |
| **B2B industrial manufacturer** | Product categories, datasheets, certifications, RFQ/inquiry CTAs, industry solution pages | `b2b-technical` |
| **Technical supplier / Distributor** | Catalog search, stock or availability claims, part numbers, downloads, customer portal | `b2b-technical` |
| **Regulated / Compliance-driven** | Standards, audits, certifications, safety or compliance language | `b2b-technical` |
| **Training / Academy** | Course pages, schedules, instructor bios, certifications, enrollment CTAs | `b2b-technical` |
| **Knowledge-led B2B** | White papers, webinars, newsletter, content hub, named expert authors | `b2b-technical` |
| **Enterprise sales-led software** | "Book a demo" only, no public pricing, security/compliance pages, procurement content | `b2b-technical` |

Businesses combine. A manufacturer that also runs a training academy and publishes technical
guides is all three — load `b2b-technical` once and apply every relevant section. Do not force a
single label.

## Step 3 — Load the pack

Read the matching file and use its examples in place of anything this skill would otherwise
invent:

- `${CLAUDE_PLUGIN_ROOT}/references/examples/consumer-online.md`
- `${CLAUDE_PLUGIN_ROOT}/references/examples/b2b-technical.md`

Read only the pack you resolved to. Loading both re-introduces exactly the bias this split
exists to remove.

## Fallback — ambiguous type

If the signals conflict or the site is too thin to classify, **load no pack**. Derive hooks, CTAs,
objections and channels from the site's own vocabulary and from grounding, and state in the
output:

```markdown
> Business type could not be resolved from the site. Examples below are derived from your own
> copy rather than a standard playbook.
```

A wrong pack is worse than no pack. Consumer tactics applied to an industrial buyer read as
incompetence to that buyer, and the reverse costs a consumer brand its voice.

## Benchmarks

Conversion, open-rate and CPA figures throughout this suite are US-market averages unless the
table says otherwise. Treat them as order-of-magnitude orientation, not targets, and say which
market a number came from whenever you quote one. Long-cycle B2B, regulated procurement and
non-US markets deviate enough that a "below benchmark" verdict is meaningless without that note.
