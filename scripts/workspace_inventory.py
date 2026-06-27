#!/usr/bin/env python3
"""Workspace inventory helper for Forge.

Scans a workspace for project signals and emits a human Markdown summary plus
an optional JSON fact index. The script is read-only except for explicit output
paths passed by the caller.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

MANIFEST_TYPES = {
    "package.json": "node",
    "pyproject.toml": "python",
    "requirements.txt": "python",
    "Cargo.toml": "rust",
    "go.mod": "go",
    "pom.xml": "java",
    "build.gradle": "java",
    "composer.json": "php",
    "Gemfile": "ruby",
    "pubspec.yaml": "dart",
    "mix.exs": "elixir",
    "deno.json": "deno",
    "Dockerfile": "container",
}

DOC_NAMES = ["README.md", "QUICKSTART.md", "CONFIG.md", "TESTING.md", "TROUBLESHOOTING.md"]
TEST_DIR_NAMES = {"test", "tests", "__tests__", "spec", "specs"}
TEST_FILE_PREFIXES = ("test_",)
TEST_FILE_SUFFIXES = ("_test.py", ".test.js", ".test.ts", ".spec.js", ".spec.ts", ".test.tsx", ".spec.tsx")
IGNORED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    "dist",
    "build",
    ".mypy_cache",
    ".ruff_cache",
    ".idea",
    ".vscode",
}
LANGUAGE_EXTS = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".go": "go",
    ".rs": "rust",
    ".java": "java",
    ".kt": "kotlin",
    ".swift": "swift",
    ".php": "php",
    ".rb": "ruby",
    ".vue": "vue",
    ".svelte": "svelte",
}
RUN_SCRIPT_NAMES = {"dev", "start", "serve"}
TEST_SCRIPT_NAMES = {"test", "tests"}
BUILD_SCRIPT_NAMES = {"build", "compile"}
PROJECT_CONTAINER_DIRS = {"apps", "packages", "services", "frontend", "backend"}


def _rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _iter_files(root: Path, max_files: int, notes: set[str] | None = None):
    seen = 0
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        kept_dirs = []
        for dirname in dirnames:
            if dirname in IGNORED_DIRS or dirname.startswith(".cache"):
                if notes is not None:
                    notes.add(f"skipped_dir={_rel(current / dirname, root)}")
                continue
            kept_dirs.append(dirname)
        dirnames[:] = kept_dirs
        for filename in filenames:
            seen += 1
            if seen > max_files:
                if notes is not None:
                    notes.add(f"file_limit_reached={max_files}")
                return
            yield Path(dirpath) / filename


def _has_code(root: Path, max_files: int = 300) -> bool:
    for path in _iter_files(root, max_files):
        if path.suffix.lower() in LANGUAGE_EXTS:
            return True
    return False


def _manifest_names(root: Path) -> list[str]:
    return sorted(name for name in MANIFEST_TYPES if (root / name).exists())


def _has_project_signal(root: Path) -> bool:
    if _manifest_names(root):
        return True
    if (root / ".git").exists() and _has_code(root):
        return True
    if (root / "README.md").exists() and _has_code(root):
        return True
    return False


def _children(root: Path) -> list[Path]:
    try:
        return sorted(root.iterdir())
    except OSError:
        return []


def _candidate_project_roots(root: Path) -> list[Path]:
    child_projects = _child_project_roots(root)
    if _has_project_signal(root):
        return [root] + child_projects if child_projects else [root]

    return child_projects


def _child_project_roots(root: Path) -> list[Path]:
    candidates: list[Path] = []
    for child in _children(root):
        if child.name in IGNORED_DIRS or child.name.startswith("."):
            continue
        if not child.is_dir():
            continue
        if _has_project_signal(child):
            candidates.append(child)
            continue
        if child.name not in PROJECT_CONTAINER_DIRS and root != child.parent:
            continue
        for grandchild in _children(child):
            if grandchild.name in IGNORED_DIRS or grandchild.name.startswith(".") or not grandchild.is_dir():
                continue
            if _has_project_signal(grandchild):
                candidates.append(grandchild)
    return candidates


def _package_scripts(root: Path) -> list[str]:
    package_json = root / "package.json"
    if not package_json.exists():
        return []
    try:
        payload = json.loads(package_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ["package.json scripts unreadable"]
    scripts = payload.get("scripts")
    if not isinstance(scripts, dict):
        return []
    return sorted(str(key) for key in scripts)


def _package_manager(root: Path) -> str:
    if (root / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (root / "yarn.lock").exists():
        return "yarn"
    return "npm"


def _script_command(manager: str, script: str) -> str:
    if manager == "npm" and script == "test":
        return "npm test"
    if manager == "npm" and script == "start":
        return "npm start"
    return f"{manager} run {script}"


def _make_targets(root: Path) -> set[str]:
    makefile = root / "Makefile"
    if not makefile.exists():
        return set()
    targets: set[str] = set()
    pattern = re.compile(r"^([A-Za-z0-9_.-]+):")
    try:
        for line in makefile.read_text(encoding="utf-8", errors="ignore").splitlines():
            match = pattern.match(line)
            if match:
                targets.add(match.group(1))
    except OSError:
        return set()
    return targets


def _command_hints(root: Path, scripts: list[str], test_indicators: set[str]) -> dict[str, list[str]]:
    manager = _package_manager(root)
    run_commands: set[str] = set()
    test_commands: set[str] = set()
    build_commands: set[str] = set()
    tooling: set[str] = set()

    if scripts:
        tooling.add(manager)
    for script in scripts:
        if script in RUN_SCRIPT_NAMES:
            run_commands.add(_script_command(manager, script))
        if script in TEST_SCRIPT_NAMES or script.startswith("test:"):
            test_commands.add(_script_command(manager, script))
        if script in BUILD_SCRIPT_NAMES:
            build_commands.add(_script_command(manager, script))

    targets = _make_targets(root)
    if targets:
        tooling.add("make")
    for target in targets:
        if target in RUN_SCRIPT_NAMES:
            run_commands.add(f"make {target}")
        if target in TEST_SCRIPT_NAMES:
            test_commands.add(f"make {target}")
        if target in BUILD_SCRIPT_NAMES:
            build_commands.add(f"make {target}")

    if (root / "Dockerfile").exists():
        tooling.add("docker")
        run_commands.add(f"docker build -t {root.name or 'project'} .")
    if any((root / name).exists() for name in ("docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml")):
        tooling.add("docker compose")
        run_commands.add("docker compose up")
    if any((root / name).exists() for name in ("pyproject.toml", "requirements.txt")) and test_indicators:
        test_commands.add("python -m pytest")

    return {
        "run_commands": sorted(run_commands),
        "test_commands": sorted(test_commands),
        "build_commands": sorted(build_commands),
        "tooling": sorted(tooling),
    }


def _summarize_project(project_root: Path, workspace_root: Path, max_files: int, notes: set[str]) -> dict[str, Any]:
    manifests = _manifest_names(project_root)
    manifest_types = sorted({MANIFEST_TYPES[name] for name in manifests})
    languages: set[str] = set()
    test_indicators: set[str] = set()
    file_count = 0

    for path in _iter_files(project_root, max_files, notes):
        file_count += 1
        suffix = path.suffix.lower()
        if suffix in LANGUAGE_EXTS:
            languages.add(LANGUAGE_EXTS[suffix])
        name = path.name
        if path.parent.name in TEST_DIR_NAMES:
            test_indicators.add(path.parent.name)
        if name.startswith(TEST_FILE_PREFIXES) or name.endswith(TEST_FILE_SUFFIXES):
            test_indicators.add(name)

    for dirname in TEST_DIR_NAMES:
        if (project_root / dirname).is_dir():
            test_indicators.add(dirname)

    docs = [name for name in DOC_NAMES if (project_root / name).exists()]
    scripts = _package_scripts(project_root)
    commands = _command_hints(project_root, scripts, test_indicators)
    risk_flags: list[str] = []
    if "README.md" not in docs:
        risk_flags.append("missing_readme")
    if not test_indicators:
        risk_flags.append("missing_test_signal")
    if (project_root / ".git").exists() and not (project_root / ".gitignore").exists():
        risk_flags.append("missing_gitignore")

    if len(manifest_types) > 1:
        project_type = "mixed"
    elif manifest_types:
        project_type = manifest_types[0]
    elif languages:
        project_type = "codebase"
    else:
        project_type = "unknown"

    return {
        "path": _rel(project_root, workspace_root),
        "absolute_path": str(project_root),
        "project_type": project_type,
        "manifests": manifests,
        "languages": sorted(languages),
        "docs": docs,
        "scripts": scripts,
        "test_indicators": sorted(test_indicators),
        **commands,
        "risk_flags": risk_flags,
        "file_count_sampled": file_count,
    }


def _next_options(status: str) -> list[dict[str, str]]:
    if status == "no_project":
        return [
            {"option": "选择项目目录", "why": "当前目录没有明显 manifest 或代码信号。"},
            {"option": "创建新项目骨架", "why": "如果这里本来就是起点，可以先搭最小结构。"},
            {"option": "粘贴已有资料", "why": "如果项目资料不在本机，可以先用文档做规划。"},
        ]
    if status == "multiple_projects":
        return [
            {"option": "确认目标项目", "why": "多个候选项目需要先选定主工作区。"},
            {"option": "生成总览索引", "why": "适合 monorepo 或前后端分离项目。"},
            {"option": "进入多智能体规划", "why": "不同子项目可由不同角色处理。"},
        ]
    return [
        {"option": "做风险自查", "why": "先处理 README、测试、配置、提交风险。"},
        {"option": "拆下一轮任务", "why": "把工程优化拆成可验收的小任务。"},
        {"option": "准备多智能体分工", "why": "当任务跨前端、后端、测试或文档时使用。"},
    ]


def scan_workspace(project: Path | str = ".", max_files: int = 2000) -> dict[str, Any]:
    if max_files < 1:
        raise ValueError("--max-files must be a positive integer")

    root = Path(project).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Invalid workspace path: {root}")

    project_roots = _candidate_project_roots(root)
    if not project_roots:
        status = "no_project"
    elif len(project_roots) == 1:
        status = "single_project"
    else:
        status = "multiple_projects"

    scan_notes: set[str] = set()
    projects = [_summarize_project(path, root, max_files, scan_notes) for path in project_roots]
    return {
        "schema_version": "1.0",
        "workspace": str(root),
        "status": status,
        "projects": projects,
        "next_options": _next_options(status),
        "limits": {
            "max_files_sampled_per_project": max_files,
            "ignored_dirs": sorted(IGNORED_DIRS),
        },
        "scan_notes": sorted(scan_notes),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Workspace Summary",
        "",
        "功能目标：检测当前工作区是否包含可迭代项目，并汇总可用于下一步规划的事实。",
        f"输入：{result['workspace']}",
        "输出：Markdown 项目摘要；如指定 `--json`，同时输出机器可读索引。",
        f"状态：{result['status']}",
        "异常情况：未读取 secret 内容；大型依赖、缓存和构建目录会被跳过。",
        "限制：这是静态扫描，不代表项目已经能运行或测试通过。",
        "",
        "## Projects",
    ]
    if not result["projects"]:
        lines.append("- 未检测到明显项目。")
    for project in result["projects"]:
        lines.extend(
            [
                f"- Path: `{project['path']}`",
                f"  - Type: {project['project_type']}",
                f"  - Manifests: {', '.join(project['manifests']) or 'none'}",
                f"  - Languages: {', '.join(project['languages']) or 'unknown'}",
                f"  - Docs: {', '.join(project['docs']) or 'none'}",
                f"  - Scripts: {', '.join(project['scripts']) or 'none'}",
                f"  - Run commands: {', '.join(project['run_commands']) or 'none inferred'}",
                f"  - Test commands: {', '.join(project['test_commands']) or 'none inferred'}",
                f"  - Tests: {', '.join(project['test_indicators']) or 'none detected'}",
                f"  - Risks: {', '.join(project['risk_flags']) or 'none obvious'}",
            ]
        )
    lines.extend(["", "## 下一步"])
    for index, item in enumerate(result["next_options"], start=1):
        lines.append(f"{index}. {item['option']}：{item['why']}")
    lines.append("")
    return "\n".join(lines)


def _write_text(path: str | None, text: str) -> None:
    if not path:
        return
    target = Path(path).expanduser()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def _write_log(log_path: str | None, result: dict[str, Any], outputs: list[str]) -> None:
    if not log_path:
        return
    lines = [
        "workspace_inventory",
        f"workspace={result['workspace']}",
        f"status={result['status']}",
        f"project_count={len(result['projects'])}",
        f"outputs={', '.join(outputs) or 'stdout'}",
        "note=secret values are not read or logged",
    ]
    lines.extend(result.get("scan_notes", []))
    _write_text(log_path, "\n".join(lines) + "\n")


def run(
    project: str = ".",
    markdown_path: str | None = None,
    json_path: str | None = None,
    log_path: str | None = None,
    max_files: int = 2000,
) -> int:
    try:
        result = scan_workspace(project, max_files=max_files)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    markdown = render_markdown(result)
    outputs: list[str] = []
    try:
        if markdown_path:
            _write_text(markdown_path, markdown)
            outputs.append(markdown_path)
        else:
            print(markdown)
        if json_path:
            _write_text(json_path, json.dumps(result, ensure_ascii=False, indent=2) + "\n")
            outputs.append(json_path)
        _write_log(log_path, result, outputs)
    except OSError as exc:
        print(f"Failed to write output: {exc}", file=sys.stderr)
        return 2
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan a workspace and emit a Forge workspace summary.")
    parser.add_argument("workspace", nargs="?", default=".", help="Workspace directory, defaults to current directory")
    parser.add_argument("--markdown", help="Write Markdown summary to this path")
    parser.add_argument("--json", dest="json_path", help="Write JSON fact index to this path")
    parser.add_argument("--log", dest="log_path", help="Write sanitized scan log to this path")
    parser.add_argument("--max-files", type=int, default=2000, help="Max files sampled per detected project")
    args = parser.parse_args()
    return run(args.workspace, args.markdown, args.json_path, args.log_path, args.max_files)


if __name__ == "__main__":
    raise SystemExit(main())
