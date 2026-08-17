from datetime import date
import json
from pathlib import Path
import subprocess
import sys

import pytest

from scripts.resolve_audit_output import build_filename, resolve_audit_output


DAY = date(2026, 8, 17)
ROOT = Path(__file__).resolve().parent.parent


def test_market_filename_contract():
    assert build_filename(
        "MARKETKIT", "MARKETING-AUDIT", "idt-dichtungen.de", "md"
    ) == "MARKETKIT - MARKETING-AUDIT - idt-dichtungen.de.md"
    with pytest.raises(ValueError, match="uppercase kebab"):
        build_filename("MARKETKIT", "MARKETING_AUDIT", "idt-dichtungen.de", "md")


def test_duplicate_market_report_creates_second_audit_and_search_reuses_it(tmp_path):
    name = "MARKETKIT - MARKETING-AUDIT - idt-dichtungen.de.md"
    first = resolve_audit_output(tmp_path, name, today=DAY)
    first.output_path.write_text("first", encoding="utf-8")
    second = resolve_audit_output(tmp_path, name, today=DAY)
    assert second.audit_dir.name == "Audit-2026-08-17-02"
    search = resolve_audit_output(
        tmp_path,
        "SEARCHKIT - GSC-Q2-2026 - idt-dichtungen.de.md",
        today=DAY,
    )
    assert search.audit_dir == second.audit_dir


def test_data_output_is_flat(tmp_path):
    result = resolve_audit_output(
        tmp_path,
        "MARKETKIT - PAGE-ANALYSIS - idt-dichtungen.de.json",
        data=True,
        today=DAY,
    )
    assert result.output_path.parent == result.audit_dir / "data"


def test_cli_prints_exact_output_json(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "resolve_audit_output.py"),
            "--purpose", "COMPETITOR-REPORT",
            "--scope", "idt-dichtungen.de",
            "--extension", "md",
            "--date", "2026-08-17",
        ],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    assert Path(payload["output_path"]).name == (
        "MARKETKIT - COMPETITOR-REPORT - idt-dichtungen.de.md"
    )
