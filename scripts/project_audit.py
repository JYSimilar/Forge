#!/usr/bin/env python3
"""Project audit helper.

Scans a project for common delivery risks:
- secrets patterns
- local absolute paths
- high-risk file names
- macOS/resource-fork artifacts
- virtualenv/cache/build artifacts
- missing core docs
- missing .gitignore
- temporary-code markers
- large files

Usage:
  python scripts/project_audit.py /path/to/project
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-\.]{12,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9_\-\.]{20,}"),
]

LOCAL_PATH_PATTERNS = [
    re.compile(r"/" r"Users/[^\s'\"]+"),
    re.compile(r"/" r"home/[^\s'\"]+"),
    # Matches escaped Windows paths often found in JSON/YAML: C:\\Users\\name
    re.compile(r"[A-Za-z]:\\\\Users\\\\[^\s'\"<>|]+", re.IGNORECASE),
    # Matches normal Windows paths often found in docs: C:\Users\name
    re.compile(r"[A-Za-z]:\\Users\\[^\s'\"<>|]+", re.IGNORECASE),
    # Matches Windows paths written with forward slashes: C:/Users/name
    re.compile(r"[A-Za-z]:/Users/[^\s'\"<>|]+", re.IGNORECASE),
]

IGNORED_DIRS = {
    ".git", ".venv", "venv", "env", "node_modules", "__pycache__", ".pytest_cache",
    "dist", "build", ".mypy_cache", ".ruff_cache", ".idea", ".vscode"
}

# These directories are skipped for speed, but should still be reported because
# they are common accidental-commit risks in zip packages and Git diffs.
WARN_IGNORED_DIRS = {
    ".venv", "venv", "env", "node_modules", "__pycache__", ".pytest_cache",
    "dist", "build", ".mypy_cache", ".ruff_cache"
}

ARTIFACT_NAMES = {".DS_Store"}
ARTIFACT_DIRS = {"__MACOSX"}
ARTIFACT_PREFIXES = ("._",)
HIGH_RISK_FILE_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    "id_rsa",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
}
HIGH_RISK_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".crt"}
DOC_CANDIDATES = ["README.md", "QUICKSTART.md", "CONFIG.md", "TESTING.md", "TROUBLESHOOTING.md"]
TEXT_EXTS = {".py", ".js", ".ts", ".tsx", ".vue", ".go", ".java", ".md", ".txt", ".yaml", ".yml", ".json", ".toml", ".env", ".sh", ".ps1"}
TEMP_MARKERS = ["TO" + "DO", "FIX" + "ME", "HA" + "CK", "X" + "XX"]
TEMP_MARKER_PATTERN = re.compile(r"\b(" + "|".join(TEMP_MARKERS) + r")\b", re.IGNORECASE)


def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTS or path.name.startswith(".env")


def is_high_risk_file(path: Path) -> bool:
    name = path.name.lower()
    return name in HIGH_RISK_FILE_NAMES or path.suffix.lower() in HIGH_RISK_SUFFIXES


def iter_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        rel_dir = current.relative_to(root)

        for dirname in list(dirnames):
            rel = rel_dir / dirname if str(rel_dir) != "." else Path(dirname)
            if dirname in ARTIFACT_DIRS:
                yield current / dirname, rel, "artifact_dir"
            elif dirname in WARN_IGNORED_DIRS:
                yield current / dirname, rel, "ignored_dir"

        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS and d not in ARTIFACT_DIRS]

        for name in filenames:
            path = current / name
            rel = path.relative_to(root)
            yield path, rel, "file"


def scan_project(root: Path) -> int:
    issues = []
    warnings = []
    ignored_dir_warnings = set()

    for path, rel, kind in iter_files(root):
        name = path.name

        if kind == "artifact_dir":
            issues.append((str(rel), "artifact_dir", "macOS 资源目录不应打包或提交"))
            continue

        if kind == "ignored_dir":
            ignored_dir_warnings.add(str(rel))
            continue

        if name in ARTIFACT_NAMES or name.startswith(ARTIFACT_PREFIXES):
            issues.append((str(rel), "artifact", "系统/临时文件可能不应提交"))

        if is_high_risk_file(path):
            issues.append((str(rel), "high_risk_file", "高风险文件名，请确认不是密钥、证书或本机环境配置"))

        try:
            size = path.stat().st_size
        except OSError:
            continue
        if size > 5 * 1024 * 1024:
            warnings.append((str(rel), "large_file", f"文件较大：{size / 1024 / 1024:.1f} MB"))

        if is_text_file(path):
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue

            for pat in SECRET_PATTERNS:
                if pat.search(text):
                    issues.append((str(rel), "secret_pattern", "疑似密钥/token/password，请人工确认"))
                    break

            # Avoid self-reporting examples/regex definitions in this audit tool itself.
            should_skip_local_path_warning = (
                str(rel).replace("\\", "/") == "scripts/project_audit.py"
                and "LOCAL_PATH_PATTERNS" in text
            )
            if not should_skip_local_path_warning:
                for pat in LOCAL_PATH_PATTERNS:
                    if pat.search(text):
                        warnings.append((str(rel), "local_path", "疑似本机绝对路径，请替换为通用路径"))
                        break

            # Markdown templates and task queues may contain example status words; avoid noisy false positives.
            rel_posix = str(rel).replace("\\", "/")
            skip_temp_marker = rel_posix.startswith("assets/templates/") or rel_posix in {"TASK_QUEUE.md", "AUTOMATION_PLAN.md", "OPTION_SET.md"}
            if not skip_temp_marker and TEMP_MARKER_PATTERN.search(text):
                warnings.append((str(rel), "todo_marker", "包含临时代码标记，提交前请确认是否可保留"))

    # Report skipped artifact/cache directories without recursively scanning them.
    for rel in sorted(ignored_dir_warnings):
        warnings.append((rel, "ignored_dir", "发现常见缓存/依赖/构建目录，已跳过扫描；提交或打包前请确认已被 .gitignore 排除"))

    existing_docs = {p.name for p in root.iterdir() if p.is_file()}
    missing_docs = [doc for doc in DOC_CANDIDATES if doc not in existing_docs]
    if (root / ".git").exists() and ".gitignore" not in existing_docs:
        warnings.append((".gitignore", "missing_gitignore", "缺少 .gitignore，容易误提交缓存、密钥或构建产物"))

    print("# Project Audit Report")
    print(f"Project: {root}")
    print()

    if issues:
        print("## High Priority Issues")
        for rel, typ, msg in issues:
            print(f"- [{typ}] {rel}: {msg}")
        print()
    else:
        print("## High Priority Issues")
        print("- 未发现明显高优先级问题。")
        print()

    if warnings:
        print("## Warnings")
        for rel, typ, msg in warnings:
            print(f"- [{typ}] {rel}: {msg}")
        print()
    else:
        print("## Warnings")
        print("- 未发现明显警告。")
        print()

    print("## Documentation")
    if missing_docs:
        print("建议补充：" + ", ".join(missing_docs))
    else:
        print("核心文档基本齐全。")
    print()

    print("## Recommendation")
    if issues:
        print("建议修改后再提交。")
        return 1
    print("可以继续提交，但请人工确认 warnings。")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scan a project for common delivery risks: secrets, local paths, cache/build artifacts, large files, missing docs, and temporary-code markers.",
        epilog="Example: python scripts/project_audit.py /path/to/project",
    )
    parser.add_argument("project", nargs="?", default=".", help="Project directory, defaults to current directory")
    args = parser.parse_args()

    root = Path(args.project).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        print(f"Invalid project path: {root}", file=sys.stderr)
        return 2
    return scan_project(root)


if __name__ == "__main__":
    raise SystemExit(main())
