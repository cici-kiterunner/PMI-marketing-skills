#!/usr/bin/env python3
"""Install this repository's skill into local Codex or Claude Code.

Uses only Python's standard library. No network or package installation.
Managed cloud hosts should use their native skill manager instead.
"""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from uuid import uuid4


SKILL_NAME = "optimize-pr-geo"
REPO_ROOT = Path(__file__).resolve().parents[1]


def verify_bundle():
    source = REPO_ROOT / "skills" / SKILL_NAME
    manifest = json.loads((REPO_ROOT / "manifest.json").read_text(encoding="utf-8"))
    version = (REPO_ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if manifest.get("version") != version or manifest.get("skill_name") != SKILL_NAME:
        raise ValueError("VERSION and manifest.json do not match.")
    expected = manifest.get("files", {})
    if not expected or not source.is_dir():
        raise ValueError("Skill source or checksum list is missing.")
    actual = {}
    for item in sorted(source.rglob("*")):
        if item.is_symlink():
            raise ValueError("Skill source must not contain symbolic links.")
        if item.is_file():
            relative = item.relative_to(REPO_ROOT).as_posix()
            actual[relative] = hashlib.sha256(item.read_bytes()).hexdigest()
    if actual != expected:
        raise ValueError("Skill files do not match manifest.json; restore a complete release.")
    if not (source / "SKILL.md").is_file():
        raise ValueError("SKILL.md is missing.")
    metadata = json.loads((source / "release.json").read_text(encoding="utf-8"))
    if metadata.get("version") != version:
        raise ValueError("Installed release metadata does not match VERSION.")
    return source, version


def install(args):
    source, version = verify_bundle()
    if args.scope == "project":
        if args.project_root is None:
            raise ValueError("--project-root is required for --scope project.")
        base = args.project_root.expanduser().resolve()
    else:
        if args.project_root is not None:
            raise ValueError("Use --project-root only with --scope project.")
        base = Path.home().resolve()
    if not base.is_dir():
        raise ValueError("The user or project root must already exist.")
    host_directory = ".agents" if args.agent == "codex" else ".claude"
    destination = base / host_directory / "skills" / SKILL_NAME
    # Refuse redirects at any install path component; never write to another scope.
    if any(item.is_symlink() for item in (base / host_directory, destination.parent, destination)):
        raise ValueError("Install path contains a symbolic link; use the host's native installation workflow.")
    if destination == source or source.is_relative_to(destination) or destination.is_relative_to(source):
        raise ValueError("Source and installation directory must be separate.")
    exists = destination.exists()
    if exists and not destination.is_dir():
        raise ValueError("The installation path is occupied by a non-directory file.")
    report = {
        "skill": SKILL_NAME,
        "version": version,
        "source": str(source),
        "destination": str(destination),
        "existing_installation": exists,
        "dry_run": args.dry_run,
    }
    if args.dry_run:
        report["next_step"] = "Use --replace after review to back up and update." if exists else "Run without --dry-run to install."
        return report
    if exists and not args.replace:
        raise ValueError("A same-name skill already exists. Review it first; use --replace to back up and update.")

    backup = None
    if exists:
        backup_root = base / ".agent-skill-backups"
        if backup_root.is_symlink() or (backup_root / SKILL_NAME).is_symlink():
            raise ValueError("Backup path contains a symbolic link; choose the manual backup workflow.")
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        backup = backup_root / SKILL_NAME / (stamp + "-" + uuid4().hex[:8])
        backup.parent.mkdir(parents=True, exist_ok=True)
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Complete the new copy before moving the old version. Staging is outside
    # the scanned skills directory; rename remains on the same local volume.
    with tempfile.TemporaryDirectory(prefix=".skill-stage-", dir=destination.parent.parent) as staging:
        staged = Path(staging) / SKILL_NAME
        shutil.copytree(source, staged)
        if backup is not None:
            destination.rename(backup)
        try:
            staged.rename(destination)
        except OSError:
            if backup is not None and not destination.exists():
                backup.rename(destination)
            raise
    report["backup"] = str(backup) if backup else None
    report["installed"] = True
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", choices=("codex", "claude-code"), required=True)
    parser.add_argument("--scope", choices=("user", "project"), required=True)
    parser.add_argument("--project-root", type=Path)
    parser.add_argument("--dry-run", action="store_true", help="Verify source and show paths without writing files.")
    parser.add_argument("--replace", action="store_true", help="Back up a same-name installation before updating.")
    args = parser.parse_args()
    try:
        report = install(args)
    except (OSError, ValueError, KeyError) as exc:
        print("Installation stopped: " + str(exc), file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
