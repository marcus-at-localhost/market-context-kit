"""Resolve optional project-scoped report metadata without host coupling."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
from typing import Mapping


CONFIG_NAME = "reporting.config.json"
CONFIG_KEYS = {"schema_version", "reporting"}
REPORTING_KEYS = {"prepared_by", "document_author"}


class ReportMetadataError(ValueError):
    """The optional project reporting configuration is present but invalid."""


def find_project_root(start: Path) -> Path:
    resolved = start.resolve()
    try:
        result = subprocess.run(
            ["git", "-C", str(resolved), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        )
        return Path(result.stdout.strip()).resolve()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return resolved


def resolve_report_metadata(
    start: Path,
    *,
    toolkit: str,
    host: str | None = None,
    provider: str | None = None,
    model: str | None = None,
    generated_at: str | None = None,
) -> dict[str, str] | None:
    config_path = find_project_root(start) / CONFIG_NAME
    if not config_path.is_file():
        return None
    config = _load_config(config_path)
    if not all(_nonempty(value) for value in (toolkit, host, provider, model)):
        raise ReportMetadataError(
            "enabled report metadata requires exact toolkit, host, provider, and model values"
        )
    reporting = config["reporting"]
    return {
        "prepared_by": reporting["prepared_by"],
        "document_author": reporting["document_author"],
        "toolkit": toolkit.strip(),
        "host": host.strip(),
        "llm_provider": provider.strip(),
        "llm_model": model.strip(),
        "generated_at": generated_at or datetime.now(timezone.utc).isoformat(),
    }


def _load_config(path: Path) -> Mapping[str, object]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReportMetadataError(f"invalid {CONFIG_NAME}: {exc}") from exc
    if not isinstance(data, dict):
        raise ReportMetadataError(f"{CONFIG_NAME} must contain a JSON object")
    if set(data) != CONFIG_KEYS or data.get("schema_version") != 1:
        raise ReportMetadataError(
            f"{CONFIG_NAME} requires only schema_version 1 and reporting"
        )
    reporting = data.get("reporting")
    if not isinstance(reporting, dict) or set(reporting) != REPORTING_KEYS:
        raise ReportMetadataError(
            "reporting requires only prepared_by and document_author"
        )
    if not all(_nonempty(reporting.get(key)) for key in REPORTING_KEYS):
        raise ReportMetadataError("reporting values must be non-empty strings")
    return data


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolve optional project report metadata")
    parser.add_argument("--toolkit", required=True)
    parser.add_argument("--host")
    parser.add_argument("--provider")
    parser.add_argument("--model")
    args = parser.parse_args()
    try:
        metadata = resolve_report_metadata(
            Path.cwd(),
            toolkit=args.toolkit,
            host=args.host,
            provider=args.provider,
            model=args.model,
        )
    except ReportMetadataError as exc:
        parser.error(str(exc))
    print(json.dumps(metadata, ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
