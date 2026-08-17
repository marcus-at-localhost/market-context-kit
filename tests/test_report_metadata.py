from pathlib import Path
import subprocess

import pytest

from scripts.resolve_report_metadata import ReportMetadataError, resolve_report_metadata
from scripts.generate_pdf_report import apply_pdf_metadata


ROOT = Path(__file__).resolve().parent.parent


def test_missing_project_config_disables_metadata(tmp_path):
    assert resolve_report_metadata(tmp_path, toolkit="Market Context Kit") is None


def test_project_config_merges_with_exact_runtime_identity(tmp_path):
    (tmp_path / "reporting.config.json").write_text(
        '{"schema_version":1,"reporting":{"prepared_by":"Project Author","document_author":"Project Author"}}',
        encoding="utf-8",
    )
    metadata = resolve_report_metadata(
        tmp_path,
        toolkit="Market Context Kit",
        host="Claude Code",
        provider="Anthropic",
        model="claude-test",
        generated_at="2026-08-16T12:00:00Z",
    )
    assert metadata["prepared_by"] == "Project Author"
    assert metadata["toolkit"] == "Market Context Kit"
    assert metadata["llm_model"] == "claude-test"


def test_existing_config_requires_runtime_identity(tmp_path):
    (tmp_path / "reporting.config.json").write_text(
        '{"schema_version":1,"reporting":{"prepared_by":"A","document_author":"A"}}',
        encoding="utf-8",
    )
    with pytest.raises(ReportMetadataError, match="host, provider, and model"):
        resolve_report_metadata(tmp_path, toolkit="Market Context Kit")


def test_metadata_is_read_only_from_git_project_root(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    nested = tmp_path / "client" / "reports"
    nested.mkdir(parents=True)
    (tmp_path / "reporting.config.json").write_text(
        '{"schema_version":1,"reporting":{"prepared_by":"Root Author","document_author":"Root Author"}}',
        encoding="utf-8",
    )
    metadata = resolve_report_metadata(
        nested, toolkit="Market Context Kit", host="Codex", provider="OpenAI", model="gpt-test"
    )
    assert metadata["prepared_by"] == "Root Author"


def test_reusable_market_report_files_contain_no_project_identity():
    for relative in ("skills/report/SKILL.md", "templates/proposal-template.md"):
        assert "Marcus Obst" not in (ROOT / relative).read_text(encoding="utf-8")


def test_all_report_workflows_use_the_shared_metadata_contract():
    output_reference = (ROOT / "references/output-location.md").read_text(encoding="utf-8")
    assert "resolve_report_metadata.py" in output_reference
    for skill in ("audit", "seo", "competitors", "report", "report-pdf"):
        text = (ROOT / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
        assert "references/output-location.md" in text


def _write_reporting(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '{"schema_version":1,"reporting":{"prepared_by":"A","document_author":"A"}}',
        encoding="utf-8",
    )


def test_config_directory_is_primary(tmp_path):
    _write_reporting(tmp_path / "config" / "reporting.config.json")
    metadata = resolve_report_metadata(
        tmp_path, toolkit="Market Context Kit", host="Codex", provider="OpenAI", model="gpt-test"
    )
    assert metadata["prepared_by"] == "A"


def test_legacy_root_config_warns(tmp_path):
    _write_reporting(tmp_path / "reporting.config.json")
    with pytest.warns(FutureWarning, match="config/reporting.config.json"):
        resolve_report_metadata(
            tmp_path, toolkit="Market Context Kit", host="Codex", provider="OpenAI", model="gpt-test"
        )


def test_both_metadata_paths_fail(tmp_path):
    _write_reporting(tmp_path / "config" / "reporting.config.json")
    _write_reporting(tmp_path / "reporting.config.json")
    with pytest.raises(ReportMetadataError, match="both"):
        resolve_report_metadata(
            tmp_path, toolkit="Market Context Kit", host="Codex", provider="OpenAI", model="gpt-test"
        )


def test_pdf_metadata_separates_human_author_from_runtime_creator():
    class Canvas:
        def __init__(self):
            self.values = {}

        def setAuthor(self, value):
            self.values["author"] = value

        def setCreator(self, value):
            self.values["creator"] = value

        def setProducer(self, value):
            self.values["producer"] = value

        def setSubject(self, value):
            self.values["subject"] = value

        def setTitle(self, value):
            self.values["title"] = value

    canvas = Canvas()
    apply_pdf_metadata(canvas, {
        "document_author": "Project Author",
        "toolkit": "Market Context Kit",
        "host": "Codex",
        "llm_provider": "OpenAI",
        "llm_model": "gpt-test",
    })
    assert canvas.values["author"] == "Project Author"
    assert canvas.values["creator"] == "Market Context Kit; Codex; OpenAI gpt-test"
