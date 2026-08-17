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
