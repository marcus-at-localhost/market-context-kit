"""Resolve the shared Audit/ output contract, standalone.

Mirrors Search Context Kit's public algorithm exactly without importing it,
so Market Context Kit stays a standalone repository.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import re
import subprocess


TOKEN_RE = re.compile(r"^[A-Z0-9]+(?:-[A-Z0-9]+)*$")
SCOPE_RE = re.compile(r"^[A-Za-z0-9.-]+$")


@dataclass(frozen=True)
class AuditOutput:
    project_root: Path
    audit_dir: Path
    data_dir: Path
    output_path: Path


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


def build_filename(toolkit: str, purpose: str, scope: str, extension: str) -> str:
    if not TOKEN_RE.fullmatch(toolkit) or not TOKEN_RE.fullmatch(purpose):
        raise ValueError("toolkit and purpose must be uppercase kebab tokens")
    if not SCOPE_RE.fullmatch(scope) or scope in {".", ".."}:
        raise ValueError("scope must be a domain or explicit customer token")
    suffix = extension.removeprefix(".")
    if not re.fullmatch(r"[A-Za-z0-9]+", suffix):
        raise ValueError("extension must be alphanumeric")
    return f"{toolkit} - {purpose} - {scope}.{suffix}"


def _validate_filename(filename: str) -> None:
    if Path(filename).name != filename:
        raise ValueError("filename must not contain a path")
    stem, separator, extension = filename.rpartition(".")
    if not separator:
        raise ValueError("filename must have an extension")
    parts = stem.split(" - ")
    if len(parts) != 3 or build_filename(*parts, extension) != filename:
        raise ValueError("filename must contain toolkit, purpose, and scope")


def resolve_audit_output(start: Path, filename: str, *, data: bool = False) -> AuditOutput:
    _validate_filename(filename)
    project_root = find_project_root(start)
    audit_dir = project_root / "Audit"
    data_dir = audit_dir / "data"
    output_path = (data_dir if data else audit_dir) / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return AuditOutput(project_root, audit_dir, data_dir, output_path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Resolve the active Audit/ output path for a MarketKit write"
    )
    parser.add_argument("--purpose", required=True)
    parser.add_argument("--scope", required=True)
    parser.add_argument("--extension", required=True)
    parser.add_argument("--data", action="store_true")
    args = parser.parse_args()
    try:
        filename = build_filename("MARKETKIT", args.purpose, args.scope, args.extension)
        result = resolve_audit_output(Path.cwd(), filename, data=args.data)
    except ValueError as exc:
        parser.exit(status=2, message=f"{exc}\n")
    print(
        json.dumps(
            {
                "project_root": str(result.project_root),
                "audit_dir": str(result.audit_dir),
                "data_dir": str(result.data_dir),
                "output_path": str(result.output_path),
            },
            ensure_ascii=False,
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    main()
