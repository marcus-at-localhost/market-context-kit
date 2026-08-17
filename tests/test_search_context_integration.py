from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_reference_requires_schema_domain_period_and_source_validation():
    text = read("references/search-context-integration.md")
    for phrase in ("schema_version", "exact target domain", "reporting period", "source status"):
        assert phrase in text


def test_reference_keeps_artifact_out_of_data_manifest():
    text = read("references/search-context-integration.md")
    assert "never goes on the Data Manifest" in text
    assert "must not change an audit score" in text


def test_audit_loads_search_context_only_for_orchestrator_synthesis():
    text = read("skills/audit/SKILL.md")
    assert "references/search-context-integration.md" in text
    assert "orchestrator-only" in text
    assert "Do not paste Search Context data into any subagent prompt" in text
    assert "do not change the six audit scores" in text


def test_report_and_seo_use_shared_reference():
    for path in ("skills/report/SKILL.md", "skills/seo/SKILL.md"):
        text = read(path)
        assert "references/search-context-integration.md" in text
        assert "SEARCH-CONTEXT.v1.json" in text


def test_reference_uses_flat_active_audit_artifacts_only():
    text = read("references/search-context-integration.md")
    assert "data/SEARCHKIT - SEARCH-CONTEXT-V1-<PERIOD> - <domain>.json" in text
    assert "active audit folder" in text
    assert "never search older audit folders" in text
    assert "more than one" in text and "require" in text


def test_consumers_keep_exact_domain_and_period_selection():
    for path in ("skills/audit/SKILL.md", "skills/report/SKILL.md", "skills/seo/SKILL.md"):
        text = read(path)
        assert "exact domain" in text
        assert "reporting period" in text
        assert "active audit" in text


def test_readme_documents_optional_companion():
    text = read("README.md")
    assert "Search Context Kit" in text
    assert "optional companion" in text
    assert "does not change audit scores" in text
