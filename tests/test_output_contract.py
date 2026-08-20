from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CORE = {
    "audit": "MARKETING-AUDIT",
    "competitors": "COMPETITOR-REPORT",
    "seo": "SEO-AUDIT",
    "report": "MARKETING-REPORT",
    "report-pdf": "MARKETING-REPORT",
}


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def test_core_writers_call_resolver_and_use_prefixed_names():
    for skill, purpose in CORE.items():
        text = read(f"skills/{skill}/SKILL.md")
        assert "scripts/resolve_audit_output.py" in text
        assert f"--purpose {purpose}" in text
        assert "MARKETKIT -" in text


PURPOSES = {
    "ads": "AD-CAMPAIGNS",
    "brand": "BRAND-VOICE",
    "content-plan": "CONTENT-PLAN",
    "copy": "COPY-SUGGESTIONS",
    "emails": "EMAIL-SEQUENCES",
    "funnel": "FUNNEL-ANALYSIS",
    "landing": "LANDING-CRO",
    "launch": "LAUNCH-PLAYBOOK",
    "proposal": "CLIENT-PROPOSAL",
    "social": "SOCIAL-CALENDAR",
}


def test_every_file_writing_skill_uses_the_shared_resolver():
    expected = {**CORE, **PURPOSES}
    for skill, purpose in expected.items():
        text = read(f"skills/{skill}/SKILL.md")
        assert "scripts/resolve_audit_output.py" in text
        assert f"--purpose {purpose}" in text


def test_readme_and_help_document_new_contract():
    for path in ("README.md", "skills/help/SKILL.md"):
        text = read(path)
        assert "Audit/" in text
        assert "MARKETKIT - <PURPOSE> - <SCOPE>" in text
        assert "config/reporting.config.json" in text
    assert "overwritten in place" in read("README.md")


def test_plugin_version_is_3_1_0():
    import json
    manifest = json.loads(read(".claude-plugin/plugin.json"))
    assert manifest["version"] == "3.1.0"


def test_output_reference_documents_shared_audit_algorithm():
    text = read("references/output-location.md")
    for phrase in (
        "Audit/",
        "<TOOLKIT> - <PURPOSE> - <SCOPE>",
        "data/",
        "overwritten in place",
        "git history is the version record",
    ):
        assert phrase in text


MARKDOWN_REPORT_WRITERS = sorted({**CORE, **PURPOSES}.keys() - {"report-pdf"})


def test_markdown_writers_resolve_report_metadata_in_their_own_phase_0():
    """The rule lives in references/output-location.md, but an agent follows the
    skill's own command list. If the call is not restated here, it gets skipped."""
    for skill in MARKDOWN_REPORT_WRITERS:
        text = read(f"skills/{skill}/SKILL.md")
        assert "scripts/resolve_report_metadata.py" in text, skill
        assert '--toolkit "Market Context Kit"' in text, skill


def test_markdown_writers_carry_a_front_matter_slot_in_their_template():
    """A template that opens on '# Title' reads as a complete file spec and
    silently overrides the reference."""
    for skill in MARKDOWN_REPORT_WRITERS:
        text = read(f"skills/{skill}/SKILL.md")
        assert "YAML front matter from the Phase 0 metadata resolver" in text, skill


SCORING_SKILLS = ("audit", "report")


def test_scoring_skills_resolve_the_business_type():
    """A rubric worded for one commercial model scores a different one as
    deficient when it is merely different. The packs carry the yardsticks that
    make the pack-relative factors measurable, so a scoring skill that never
    resolves the business type cannot apply them."""
    for skill in SCORING_SKILLS:
        text = read(f"skills/{skill}/SKILL.md")
        assert "references/business-context.md" in text, skill


def test_report_rubric_keeps_its_pack_relative_factors_and_escape_hatch():
    """Both halves are load-bearing. Pack-relative factors without the escape
    hatch still force a score onto a channel serving an unmeasured purpose;
    the escape hatch without renormalization silently rewards exclusion."""
    text = read("skills/report/SKILL.md")
    assert "*(pack-relative)*" in text
    assert "Lifecycle coverage" in text
    assert "Channel purpose the rubric does not measure" in text
    assert "over scored categories only" in text


PAGE_READING_SKILLS = (
    "ads", "audit", "brand", "competitors", "content-plan", "copy", "funnel",
    "landing", "seo",
)


def test_page_reading_skills_point_at_the_extraction_artifact_list():
    for skill in PAGE_READING_SKILLS:
        text = read(f"skills/{skill}/SKILL.md")
        assert "webfetch-artifacts.md" in text, skill


def test_artifact_list_covers_html_comments_and_bans_regex_extraction():
    text = read("references/webfetch-artifacts.md")
    assert "HTML comments" in text
    assert "Never hand-roll HTML extraction" in text
    assert "analyze_page.py" in text


def test_output_location_documents_the_canonical_front_matter_shape():
    text = read("references/output-location.md")
    assert "Canonical front-matter shape" in text
    assert "prepared_by:" in text
    assert "generated_at:" in text


def test_no_real_attribution_is_hard_coded_in_reusable_files():
    """Attribution belongs to the consuming project's config/reporting.config.json.
    A skill, reference, or template must never name a person or organization."""
    metadata_keys = ("prepared_by:", "document_author:")
    for path in ROOT.rglob("*.md"):
        if any(part in {".git", "node_modules"} for part in path.parts):
            continue
        rel = path.relative_to(ROOT)
        if rel.parts[0] not in {"skills", "references", "templates", "agents", "docs"}:
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for key in metadata_keys:
                if key in line:
                    value = line.split(key, 1)[1].strip()
                    assert value.startswith("<") and value.endswith(">"), (
                        f"{rel}:{lineno} hard-codes attribution: {line.strip()!r}"
                    )


# Reserved placeholder domains plus third-party references the docs legitimately
# name (platforms, public brands used as archetype illustrations, tool vendors).
# A client domain from an evaluation run must never end up here — add a real
# domain only when it is genuinely part of the kit's own documentation.
ALLOWED_DOMAINS = {
    "example.com", "example.org", "example.net",
    "github.com", "anthropic.com", "json-schema.org", "google.com",
    "schema.org",  # the structured-data vocabulary the SEO rubrics score against
    "wikipedia.org", "linkedin.com", "youtube.com", "instagram.com",
    "facebook.com", "twitter.com", "x.com", "tiktok.com", "reddit.com",
    "calendly.com", "acuityscheduling.com", "strategyzer.com",
    "mckinsey.com", "basf.com",
    "copywritematters.com", "blaksheepcreative.com", "awai.com",
}

DOMAIN_RE = __import__("re").compile(
    r"\b[a-z0-9][a-z0-9-]*\.(?:com|de|org|net|io|es|eu|gmbh|co\.uk)\b"
)


def test_no_client_domains_leak_into_the_kit():
    """The kit is evaluated against real client sites. Their domains, copy, and
    identities stay in the consuming project and never in this repo."""
    import subprocess

    tracked = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True
    ).stdout.decode("utf-8").split("\0")

    offenders = []
    for name in filter(None, tracked):
        path = ROOT / name
        if path.suffix not in {".md", ".py", ".json"} or not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if rel.name == "test_output_contract.py":  # the allowlist itself
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for domain in DOMAIN_RE.findall(line.lower()):
                if domain not in ALLOWED_DOMAINS:
                    offenders.append(f"{rel}:{lineno} {domain}")
    assert not offenders, (
        "Undeclared domain(s) found. If this is a client domain from an "
        "evaluation run, remove it; if it belongs to the kit's own docs, add "
        "it to ALLOWED_DOMAINS:\n  " + "\n  ".join(offenders)
    )
