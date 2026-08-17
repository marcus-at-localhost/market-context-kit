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
        assert "Audit-YYYY-MM-DD" in text
        assert "MARKETKIT - <PURPOSE> - <SCOPE>" in text
        assert "config/reporting.config.json" in text
    assert "2026-08-17-02" in read("README.md")


def test_plugin_version_is_3_1_0():
    import json
    manifest = json.loads(read(".claude-plugin/plugin.json"))
    assert manifest["version"] == "3.1.0"


def test_output_reference_documents_shared_audit_algorithm():
    text = read("references/output-location.md")
    for phrase in (
        "Audit-YYYY-MM-DD",
        "Audit-YYYY-MM-DD-NN",
        "<TOOLKIT> - <PURPOSE> - <SCOPE>",
        "highest-numbered",
        "data/",
        "never overwrite",
    ):
        assert phrase in text
