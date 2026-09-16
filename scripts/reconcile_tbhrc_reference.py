#!/usr/bin/env python3
"""Verify the public FolderDesk TBHRC reference against current Workspace Skill truth.

Checks are deliberately bounded:
1. Router repository membership parity.
2. Material FolderDesk Fast Links into Workspace .folderdesk/skills resolve to real paths.
3. Material current docs contain no legacy tbhrc/skills links.
4. One consolidated report with FolderDesk + Workspace source SHAs.

The TBHRC profile is an expanded mature reference, not the default deployment topology.
The script reports drift; it does not mutate source truth.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REFERENCE = ROOT / "profiles" / "tbhrc-reference" / "folderdesk.reference.json"
MATERIAL_DOCS = (
    ROOT / "AGENTS.md",
    ROOT / "README.md",
    ROOT / "ARCHITECTURE.md",
    ROOT / "MANIFEST.md",
    ROOT / "VERIFY.md",
    ROOT / "profiles" / "tbhrc-reference" / "README.md",
)
WORKSPACE_SKILLS_URL_RE = re.compile(
    r"https://github\.com/tbhrc/workspace/(?P<kind>tree|blob)/main/\.folderdesk/skills/(?P<path>[^)\s>#]+)(?:#[^)\s>]*)?"
)
LEGACY_SKILLS_URL_RE = re.compile(
    r"https://github\.com/tbhrc/skills/(?P<kind>tree|blob)/main/(?P<path>[^)\s>#]+)(?:#[^)\s>]*)?"
)


class ReconcileError(RuntimeError):
    pass


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ReconcileError(f"Missing required file: {path}") from exc


def git_sha(path: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        raise ReconcileError(f"Not a readable Git checkout: {path}")
    return result.stdout.strip()


def router_repositories(router_path: Path) -> set[str]:
    data = load_json(router_path)
    if not isinstance(data, dict):
        raise ReconcileError("Router registry root must be an object")
    repos = set()
    for key in data:
        if not isinstance(key, str) or "/" not in key:
            raise ReconcileError(f"Invalid Router repository key: {key!r}")
        repos.add(key)
    return repos


def reference_repositories(reference_path: Path) -> tuple[str, set[str]]:
    data = load_json(reference_path)
    if not isinstance(data, dict):
        raise ReconcileError("Reference profile root must be an object")
    target = data.get("target")
    if not isinstance(target, dict) or not isinstance(target.get("owner"), str):
        raise ReconcileError("Reference profile requires target.owner")
    owner = target["owner"]
    rows = data.get("repositories")
    if not isinstance(rows, list):
        raise ReconcileError("Reference profile repositories must be a list")
    repos: set[str] = set()
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("name"), str):
            raise ReconcileError("Every reference repository requires a name")
        repos.add(f"{owner}/{row['name']}")
    return owner, repos


def _collect_links(pattern: re.Pattern[str], doc: Path, source: str) -> list[dict[str, str]]:
    text = doc.read_text(encoding="utf-8")
    links: list[dict[str, str]] = []
    for match in pattern.finditer(text):
        kind = match.group("kind")
        rel = unquote(match.group("path")).strip("/")
        document = str(doc.relative_to(ROOT)) if doc.is_relative_to(ROOT) else doc.name
        links.append({
            "document": document,
            "kind": kind,
            "path": rel,
            "url": match.group(0),
            "source": source,
        })
    return links


def material_skill_links(docs: tuple[Path, ...] = MATERIAL_DOCS) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    current: list[dict[str, str]] = []
    legacy: list[dict[str, str]] = []
    seen_current: set[tuple[str, str, str]] = set()
    seen_legacy: set[tuple[str, str, str]] = set()
    for doc in docs:
        if not doc.exists():
            continue
        for link in _collect_links(WORKSPACE_SKILLS_URL_RE, doc, "workspace"):
            key = (link["document"], link["kind"], link["path"])
            if key not in seen_current:
                seen_current.add(key)
                current.append(link)
        for link in _collect_links(LEGACY_SKILLS_URL_RE, doc, "legacy"):
            key = (link["document"], link["kind"], link["path"])
            if key not in seen_legacy:
                seen_legacy.add(key)
                legacy.append(link)
    return current, legacy


def verify_skill_links(skills_source: Path, links: list[dict[str, str]]) -> list[dict[str, str]]:
    broken: list[dict[str, str]] = []
    for link in links:
        target = skills_source / link["path"]
        ok = target.is_dir() if link["kind"] == "tree" else target.is_file()
        if not ok:
            broken.append(link)
    return broken


def build_report(skills_source: Path, reference_path: Path = DEFAULT_REFERENCE) -> dict[str, object]:
    router_path = skills_source / "templates" / "agents-repositories.json"
    router = router_repositories(router_path)
    _, reference = reference_repositories(reference_path)
    missing = sorted(router - reference)
    extra = sorted(reference - router)
    links, legacy_links = material_skill_links()
    broken = verify_skill_links(skills_source, links)
    status = "GREEN" if not missing and not extra and not broken and not legacy_links else "DRIFT"
    return {
        "status": status,
        "folderdesk_sha": git_sha(ROOT),
        "workspace_sha": git_sha(skills_source),
        "skill_root": ".folderdesk/skills",
        "router_repository_count": len(router),
        "reference_repository_count": len(reference),
        "missing_in_reference": missing,
        "extra_in_reference": extra,
        "checked_skill_fast_links": len(links),
        "broken_skill_fast_links": broken,
        "legacy_skill_fast_links": legacy_links,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Reconcile FolderDesk TBHRC expanded-reference parity")
    parser.add_argument("--skills-source", required=True, type=Path, help="Workspace .folderdesk/skills root")
    parser.add_argument("--reference", type=Path, default=DEFAULT_REFERENCE)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    try:
        report = build_report(args.skills_source.resolve(), args.reference.resolve())
        rendered = json.dumps(report, indent=2, sort_keys=True)
        print(rendered)
        if args.report:
            args.report.write_text(rendered + "\n", encoding="utf-8")
        return 0 if report["status"] == "GREEN" else 1
    except (ReconcileError, OSError, json.JSONDecodeError) as exc:
        print(f"FOLDERDESK RECONCILE ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
