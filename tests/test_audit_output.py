import json
from pathlib import Path
import subprocess
import sys

import pytest

from scripts.resolve_audit_output import build_filename, resolve_audit_output


ROOT = Path(__file__).resolve().parent.parent


def test_market_filename_contract():
    assert build_filename(
        "MARKETKIT", "MARKETING-AUDIT", "example.com", "md"
    ) == "MARKETKIT - MARKETING-AUDIT - example.com.md"
    with pytest.raises(ValueError, match="uppercase kebab"):
        build_filename("MARKETKIT", "MARKETING_AUDIT", "example.com", "md")


def test_every_target_resolves_into_the_single_active_audit_folder(tmp_path):
    name = "MARKETKIT - MARKETING-AUDIT - example.com.md"
    first = resolve_audit_output(tmp_path, name)
    first.output_path.write_text("first", encoding="utf-8")

    second = resolve_audit_output(tmp_path, name)
    assert second.audit_dir == first.audit_dir
    assert second.audit_dir.name == "Audit"

    search = resolve_audit_output(tmp_path, "SEARCHKIT - GSC-Q2-2026 - example.com.md")
    assert search.audit_dir == first.audit_dir


def test_rerun_overwrites_the_existing_report_in_place(tmp_path):
    name = "MARKETKIT - MARKETING-AUDIT - example.com.md"
    first = resolve_audit_output(tmp_path, name)
    first.output_path.write_text("first run", encoding="utf-8")

    second = resolve_audit_output(tmp_path, name)
    second.output_path.write_text("second run", encoding="utf-8")

    assert second.output_path == first.output_path
    assert second.output_path.read_text(encoding="utf-8") == "second run"


def test_data_output_is_flat(tmp_path):
    result = resolve_audit_output(
        tmp_path,
        "MARKETKIT - PAGE-ANALYSIS - example.com.json",
        data=True,
    )
    assert result.output_path.parent == result.audit_dir / "data"


def test_cli_prints_exact_output_json(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "resolve_audit_output.py"),
            "--purpose", "COMPETITOR-REPORT",
            "--scope", "example.com",
            "--extension", "md",
        ],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    assert Path(payload["output_path"]).name == (
        "MARKETKIT - COMPETITOR-REPORT - example.com.md"
    )
