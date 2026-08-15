#!/usr/bin/env python3
"""
Social Media Calendar Generator — Utility script for AI Marketing Claude Code Skills
Generates a structured 30-day content calendar with channel-specific guidance.

Two business types are supported, because the channel mix and the voice differ
completely between them:

  consumer  creator, e-commerce, self-serve SaaS, local business  (default)
  b2b       industrial, technical supplier, regulated, academy, knowledge-led

Usage:
  python social_calendar.py <topic> [channel1,channel2,...] [days] [consumer|b2b]
"""

import sys
import json
from datetime import datetime, timedelta


BUSINESS_TYPES = ("consumer", "b2b")

# Default channel sets. A technical B2B brand posting to TikTok is the failure
# mode this split exists to prevent.
DEFAULT_CHANNELS = {
    "consumer": ["linkedin", "twitter", "instagram"],
    "b2b": ["linkedin", "newsletter", "trade_media"],
}

# Content pillar templates
CONTENT_PILLARS = {
    "educational": {
        "name": "Educational",
        "description": "Teach your audience something valuable",
        "formats": ["How-to thread", "Quick tip", "Myth-busting", "Framework share",
                     "Tool recommendation", "Industry insight", "Data breakdown"],
        "platforms": {
            "linkedin": "Long-form post with bullet points, share frameworks and data",
            "twitter": "Thread format (5-10 tweets), lead with controversial take or surprising stat",
            "instagram": "Carousel (5-10 slides), clean design, one insight per slide",
            "tiktok": "60-90s talking head or screen recording, hook in first 2 seconds",
            "youtube": "8-15 min deep dive, searchable title, strong thumbnail",
            "newsletter": "One technical topic per issue, standard or application named in the subject",
            "trade_media": "Editorial voice, no sales copy, cite test data and standards",
            "webinar": "Single application problem, 20 min content plus live Q&A",
        }
    },
    "behind_the_scenes": {
        "name": "Behind the Scenes",
        "description": "Show the real, unfiltered process",
        "formats": ["Day in the life", "Tool stack reveal", "Process walkthrough",
                     "Mistake/lesson learned", "Revenue/metrics share", "Team/workspace"],
        "platforms": {
            "linkedin": "Personal story format, vulnerability + lesson learned",
            "twitter": "Single tweet with photo or short thread, raw and unfiltered",
            "instagram": "Stories or Reels, casual and authentic, behind-the-scenes footage",
            "tiktok": "Raw footage, trending audio, authentic feel",
            "youtube": "Vlog style, 5-10 min, day-in-the-life or process reveal",
            "newsletter": "Capability feature: lab, test rig, production step, quality process",
            "trade_media": "Plant or lab report, investment or capability announcement",
            "webinar": "Live walkthrough of the test or production process",
        }
    },
    "social_proof": {
        "name": "Social Proof",
        "description": "Show results, testimonials, and credibility",
        "formats": ["Client win/case study", "Testimonial share", "Before/after",
                     "Revenue milestone", "User-generated content", "Award/recognition"],
        "platforms": {
            "linkedin": "Case study format with specific numbers, tag the client",
            "twitter": "Screenshot of result + brief context, celebrate publicly",
            "instagram": "Designed testimonial graphic or video testimonial clip",
            "tiktok": "Before/after reveal, transformation content",
            "youtube": "Full case study breakdown, 10-15 min",
            "newsletter": "Application case: constraint, what was specified, measured result",
            "trade_media": "Reference installation write-up, customer named where permitted",
            "webinar": "Customer or expert walks through the application on the call",
        }
    },
    "engagement": {
        "name": "Engagement",
        "description": "Start conversations and build community",
        "formats": ["Hot take/opinion", "Question post", "Poll", "This or that",
                     "Unpopular opinion", "Agree or disagree", "Fill in the blank"],
        "platforms": {
            "linkedin": "Start with bold statement, ask for opinions in comments",
            "twitter": "Short punchy take or poll, reply to every comment",
            "instagram": "Story polls/questions, interactive stickers",
            "tiktok": "Stitch or duet format, respond to comments",
            "youtube": "Community post with poll, or video asking for opinions",
            "newsletter": "Ask-the-expert: invite reader questions, answer them next issue",
            "trade_media": "Commentary on a standards revision or industry development",
            "webinar": "Open Q&A block; log every question as future content",
        }
    },
    "promotional": {
        "name": "Promotional",
        "description": "Direct promotion of product/service (use sparingly)",
        "formats": ["Product demo", "Feature highlight", "Special offer",
                     "Webinar/event promo", "Free resource", "Community invite"],
        "platforms": {
            "linkedin": "Value-first approach, lead with problem you solve",
            "twitter": "Brief pitch with link, or thread showing the tool in action",
            "instagram": "Reel demo or carousel showing benefits, link in bio",
            "tiktok": "Product demo with trending format, soft sell",
            "youtube": "Tutorial using your product, not a sales pitch",
            "newsletter": "New range, new approval, datasheet release, course dates",
            "trade_media": "Product or capability announcement with technical substance",
            "webinar": "Close with the next commercial step: sample, review, or quote",
        }
    }
}

# Posting frequency recommendations. Times are local to the audience, not the sender.
POSTING_FREQUENCY = {
    "linkedin": {"ideal": "3-5x/week", "minimum": "2x/week", "best_times": "Tue-Thu 8-10am, 12pm"},
    "twitter": {"ideal": "3-5x/day", "minimum": "1x/day", "best_times": "9am, 12pm, 5pm"},
    "instagram": {"ideal": "4-7x/week (feed+reels)", "minimum": "3x/week", "best_times": "11am-1pm, 7-9pm"},
    "tiktok": {"ideal": "1-3x/day", "minimum": "3x/week", "best_times": "7-9am, 12-3pm, 7-11pm"},
    "youtube": {"ideal": "2-3x/week", "minimum": "1x/week", "best_times": "Thu-Sat 2-4pm"},
    "facebook": {"ideal": "3-5x/week", "minimum": "2x/week", "best_times": "Wed 11am, Fri 10-11am"},
    "newsletter": {"ideal": "monthly", "minimum": "quarterly", "best_times": "Tue-Thu morning"},
    "trade_media": {"ideal": "per editorial calendar", "minimum": "2-4x/year",
                    "best_times": "lead times run 4-12 weeks — plan backwards from the issue date"},
    "webinar": {"ideal": "4-8x/year", "minimum": "2x/year", "best_times": "Tue-Thu 10-11am or 2-3pm"},
}

# Hook formulas by channel, per business type. The consumer set trades on personal
# claim and curiosity; the b2b set trades on specificity and evidence, and the
# consumer formulas actively cost credibility with a technical buyer.
HOOK_FORMULAS = {
    "consumer": {
        "linkedin": [
            "I {did X} and {unexpected result}. Here's what I learned:",
            "Most people think {common belief}. They're wrong. Here's why:",
            "{Number} things I wish I knew before {action}:",
            "I spent {time} analyzing {topic}. Here are {number} findings:",
            "Stop {common mistake}. Do this instead:",
            "The {industry} is changing. Here's what nobody is talking about:"
        ],
        "twitter": [
            "{Topic} is broken. Here's a thread on how to fix it 🧵",
            "I studied {number} {things}. Here's what separates the best from the rest:",
            "Unpopular opinion: {bold statement}",
            "You don't need {thing}. You need {better thing}. Here's why:",
            "{Number} {things} that will {benefit} (thread):",
            "The biggest mistake in {topic}? {Mistake}. Let me explain:"
        ],
        "instagram": [
            "Save this for later ↓",
            "POV: You finally {desired outcome}",
            "{Number} things about {topic} that will blow your mind",
            "The {topic} cheat sheet you didn't know you needed",
            "If you're struggling with {problem}, try this →",
            "I turned {input} into {impressive output}. Here's how:"
        ],
        "tiktok": [
            "Wait for it... (transformation reveal)",
            "Things that just make sense in {niche}",
            "POV: You discover {useful thing}",
            "I can't believe {surprising thing} actually works",
            "Replying to @user — here's how I {do thing}",
            "Day {X} of {challenge/series}"
        ]
    },
    "b2b": {
        "linkedin": [
            "{Standard} changes in {year}. What it means for {application}:",
            "We cut open a failed {component} after {time} in service. Here's what we found:",
            "Why {common material} fails at {condition} — and what we specify instead",
            "The most common specification error we see in {industry} enquiries:",
            "A customer asked whether {assumption} holds. We tested it.",
            "{Application} at {condition}: the three specs that actually decide it"
        ],
        "newsletter": [
            "From our lab: {measurement} across {number} samples of {material}",
            "{Regulation} in practice: what auditors actually ask for",
            "Selecting for {application}: a decision path",
            "Reader question: {question}. The answer, with the caveats.",
            "What changed at {trade fair}: {number} things buyers are asking about"
        ],
        "trade_media": [
            "{Application} under {condition}: test results and interpretation",
            "How {industry} is responding to {regulation or standard}",
            "Failure analysis: {component} in {application}",
            "Material selection for {constraint}: a comparison"
        ],
        "webinar": [
            "Live: specifying {component} for {application}",
            "{Standard} explained, with a worked example",
            "Failure modes in {application} — and how to design them out",
            "Ask our engineers: {topic}"
        ]
    }
}


PILLAR_DISTRIBUTION = {
    "consumer": {
        "educational": "40%",
        "behind_the_scenes": "15%",
        "social_proof": "15%",
        "engagement": "20%",
        "promotional": "10%"
    },
    # Technical audiences reward depth and proof, and punish frequent promotion.
    "b2b": {
        "educational": "50%",
        "behind_the_scenes": "10%",
        "social_proof": "20%",
        "engagement": "10%",
        "promotional": "10%"
    },
}


def generate_calendar(topic, platforms=None, days=30, brand_name=None,
                      business_type="consumer"):
    """Generate a content calendar for the given channels and business type."""
    if business_type not in BUSINESS_TYPES:
        business_type = "consumer"
    if platforms is None:
        platforms = list(DEFAULT_CHANNELS[business_type])

    hooks = HOOK_FORMULAS[business_type]

    start_date = datetime.now()
    calendar = {
        "topic": topic,
        "brand": brand_name or topic,
        "business_type": business_type,
        "platforms": platforms,
        "duration_days": days,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": (start_date + timedelta(days=days)).strftime("%Y-%m-%d"),
        "posting_schedule": {p: POSTING_FREQUENCY.get(p, {}) for p in platforms},
        "content_pillars": {
            k: {"name": v["name"], "description": v["description"], "frequency": ""}
            for k, v in CONTENT_PILLARS.items()
        },
        "pillar_distribution": PILLAR_DISTRIBUTION[business_type],
        "hook_formulas": {p: hooks.get(p, []) for p in platforms},
        "calendar": []
    }

    # Generate 30 days of content ideas
    pillar_rotation = ["educational", "engagement", "educational", "behind_the_scenes",
                       "educational", "social_proof", "promotional",
                       "educational", "engagement", "educational"]

    for day in range(days):
        date = start_date + timedelta(days=day)
        day_of_week = date.strftime("%A")

        # Skip weekends for LinkedIn-heavy calendars
        pillar_key = pillar_rotation[day % len(pillar_rotation)]
        pillar = CONTENT_PILLARS[pillar_key]

        format_idx = day % len(pillar["formats"])
        content_format = pillar["formats"][format_idx]

        day_entry = {
            "day": day + 1,
            "date": date.strftime("%Y-%m-%d"),
            "day_of_week": day_of_week,
            "pillar": pillar["name"],
            "format": content_format,
            "topic_angle": f"{content_format} about {topic}",
            "platforms": {}
        }

        for platform in platforms:
            if platform in pillar["platforms"]:
                day_entry["platforms"][platform] = {
                    "guidance": pillar["platforms"][platform],
                    "post": True
                }

        calendar["calendar"].append(day_entry)

    # Add repurposing strategy
    calendar["repurposing_strategy"] = REPURPOSING[business_type](topic)

    return calendar


REPURPOSING = {
    "consumer": lambda topic: {
        "description": "Turn 1 piece of content into 10+ posts across platforms",
        "cycle": "2 weeks per source piece",
        "workflow": [
            f"1. Create a long-form piece about {topic} (blog post or video)",
            "2. Extract 5-7 key insights as individual social posts",
            "3. Turn each insight into a platform-specific format",
            "4. Create a carousel/thread from the full piece",
            "5. Cut a short-form video summary",
            "6. Pull quotes for image posts",
            "7. Create a poll or question from one insight",
            "8. Share behind-the-scenes of creating the content",
            "9. Reshare top-performing posts 2-4 weeks later",
            "10. Create a 'best of' compilation monthly"
        ]
    },
    "b2b": lambda topic: {
        "description": "Turn 1 technical asset into 10+ touchpoints across channels",
        "cycle": "6-12 weeks per source asset; technical assets stay usable for years",
        "workflow": [
            f"1. Produce the source asset on {topic} (whitepaper, test report, application study)",
            "2. Build a webinar or technical talk on the same material",
            "3. Adapt it into a trade-press article in editorial voice",
            "4. Publish a LinkedIn series from the expert's profile, one finding per post",
            "5. Feature it in the technical newsletter",
            "6. Cite the finding on the relevant product or solution page",
            "7. Update the datasheet or selection guide",
            "8. Produce a sales and distributor one-pager",
            "9. Convert the questions it raised into FAQ entries",
            "10. Record a short explainer for the most-asked question"
        ]
    },
}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python social_calendar.py <topic> [channel1,channel2,...] [days] [consumer|b2b]",
            "examples": [
                "python social_calendar.py 'AI automation' linkedin,twitter,instagram 30 consumer",
                "python social_calendar.py 'flange sealing' linkedin,newsletter,trade_media 30 b2b",
            ],
            "description": "Generates a content calendar for the given channels and business type",
            "business_types": list(BUSINESS_TYPES),
            "default_channels": DEFAULT_CHANNELS,
            "available_channels": list(POSTING_FREQUENCY.keys())
        }, indent=2))
        return

    topic = sys.argv[1]
    business_type = sys.argv[4] if len(sys.argv) > 4 else "consumer"
    if business_type not in BUSINESS_TYPES:
        business_type = "consumer"
    platforms = (sys.argv[2].split(",") if len(sys.argv) > 2
                 else list(DEFAULT_CHANNELS[business_type]))
    days = int(sys.argv[3]) if len(sys.argv) > 3 else 30

    calendar = generate_calendar(topic, platforms, days, business_type=business_type)
    print(json.dumps(calendar, indent=2))


if __name__ == "__main__":
    main()
