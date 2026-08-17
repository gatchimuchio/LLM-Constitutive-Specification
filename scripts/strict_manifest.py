#!/usr/bin/env python3
"""Strict repository inventory/content verifier backed by Git blob identities.

Manifest format:
    <40-hex git-blob-sha>  <repository-relative-path>

The manifest file itself is excluded to avoid self-reference.
"""
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path, PurePosixPath

HEX40 = re.compile(r"^[0-9a-f]{40}$")
DEFAULT_MANIFEST = "REPOSITORY_GIT_BLOB_MANIFEST.txt"


def run(*args: str, cwd: Path) -> str:
    p = subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or "command failed")
    return p.stdout


def safe_path(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name) and not p.is_absolute() and ".." not in p.parts and "." not in p.parts


def tracked_paths(root: Path, manifest_name: str) -> list[str]:
    raw = run("git", "ls-files", "-z", cwd=root)
    return sorted(x for x in raw.split("\0") if x and x != manifest_name)


def worktree_blob(root: Path, path: str) -> str:
    return run("git", "hash-object", "--", path, cwd=root).strip()


def parse_manifest(path: Path) -> dict[str, str]:
    if not path.exists():
        raise ValueError("manifest missing")
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        raise ValueError("manifest is empty")
    out: dict[str, str] = {}
    for line in lines:
        if "  " not in line:
            raise ValueError(f"invalid manifest line: {line}")
        sha, name = line.split("  ", 1)
        if not HEX40.fullmatch(sha):
            raise ValueError(f"invalid blob sha: {sha}")
        if not safe_path(name):
            raise ValueError(f"unsafe path: {name}")
        if name in out:
            raise ValueError(f"duplicate entry: {name}")
        out[name] = sha
    return out


def verify(root: Path, manifest: Path) -> tuple[bool, list[str]]:
    expected = parse_manifest(manifest)
    actual_paths = tracked_paths(root, manifest.name)
    errors: list[str] = []
    missing = sorted(set(expected) - set(actual_paths))
    extra = sorted(set(actual_paths) - set(expected))
    if missing:
        errors.append(f"missing: {missing}")
    if extra:
        errors.append(f"extra: {extra}")
    for name in sorted(set(actual_paths) & set(expected)):
        path = root / name
        if path.is_symlink():
            errors.append(f"symlink forbidden: {name}")
            continue
        actual = worktree_blob(root, name)
        if actual != expected[name]:
            errors.append(f"changed: {name} expected={expected[name]} actual={actual}")
    status = run("git", "status", "--porcelain", "--untracked-files=all", cwd=root)
    if status.strip():
        errors.append("working tree is not clean")
    return not errors, errors


def generate(root: Path, manifest: Path, confirmed: bool) -> None:
    if not confirmed:
        raise ValueError("refusing to update golden manifest without --confirm")
    paths = tracked_paths(root, manifest.name)
    lines = []
    for name in paths:
        path = root / name
        if path.is_symlink():
            raise ValueError(f"symlink forbidden: {name}")
        if not safe_path(name):
            raise ValueError(f"unsafe path: {name}")
        lines.append(f"{worktree_blob(root, name)}  {name}")
    if not lines:
        raise ValueError("refusing to write empty manifest")
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("verify", "generate"))
    parser.add_argument("--root", default=".")
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST)
    parser.add_argument("--confirm", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    manifest = root / args.manifest
    try:
        if args.mode == "generate":
            generate(root, manifest, args.confirm)
            print(f"WROTE {manifest}")
            return 0
        ok, errors = verify(root, manifest)
        if ok:
            print("STRICT_MANIFEST: ALL_OK")
            return 0
        for error in errors:
            print(f"ERROR {error}")
        return 1
    except (ValueError, RuntimeError) as exc:
        print(f"ERROR {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
