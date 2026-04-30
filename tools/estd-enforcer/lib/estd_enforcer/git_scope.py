"""Git and filesystem scope discovery."""

from __future__ import annotations

import subprocess
from pathlib import Path


def run_git(repo: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def is_excluded_estd_path(relative: str, standards_path: str) -> bool:
    standards_prefix = standards_path.strip("/")
    if relative == ".gitmodules":
        return True
    return bool(standards_prefix and (relative == standards_prefix or relative.startswith(standards_prefix + "/")))


def filter_source_files(files: list[str], standards_path: str) -> list[str]:
    return sorted(file_path for file_path in files if not is_excluded_estd_path(file_path, standards_path))


def list_repo_files(repo: Path, standards_path: str) -> list[str]:
    git_files = run_git(repo, ["ls-files"])
    if git_files.returncode == 0 and git_files.stdout.strip():
        return filter_source_files([line for line in git_files.stdout.splitlines() if line], standards_path)

    excluded_roots = {
        ".git",
        "build",
        "node_modules",
        ".next",
        "Library",
        "Temp",
    }
    files: list[str] = []
    for path in repo.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(repo).as_posix()
        first = relative.split("/", 1)[0]
        if first in excluded_roots or is_excluded_estd_path(relative, standards_path):
            continue
        files.append(relative)
    return sorted(files)


def changed_files(repo: Path, base: str, standards_path: str) -> list[str]:
    diff = run_git(repo, ["diff", "--name-only", "--diff-filter=ACMRTUXB", f"{base}...HEAD"])
    if diff.returncode != 0:
        diff = run_git(repo, ["diff", "--name-only", "--diff-filter=ACMRTUXB", base, "HEAD"])
    if diff.returncode == 0:
        return filter_source_files([line for line in diff.stdout.splitlines() if line], standards_path)
    return list_repo_files(repo, standards_path)
