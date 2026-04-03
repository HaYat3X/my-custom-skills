#!/usr/bin/env python3
"""
analyze_repo.py
Gitリポジトリの構造・言語・依存関係を解析して、README生成に必要な情報をJSON出力する。

Usage:
    python analyze_repo.py <repo_path>
    python analyze_repo.py .
"""

import sys
import os
import json
from pathlib import Path
from collections import defaultdict

# ===============================
# 設定
# ===============================

IGNORE_DIRS = {
    ".git", "node_modules", "__pycache__", ".next", "dist", "build",
    ".venv", "venv", ".env", "coverage", ".cache", ".turbo", "out"
}

IGNORE_FILES = {
    ".DS_Store", "Thumbs.db", "*.pyc", "*.pyo", "*.log"
}

LANGUAGE_MAP = {
    ".py": "Python", ".ts": "TypeScript", ".tsx": "TypeScript",
    ".js": "JavaScript", ".jsx": "JavaScript", ".cs": "C#",
    ".go": "Go", ".rs": "Rust", ".java": "Java", ".rb": "Ruby",
    ".php": "PHP", ".cpp": "C++", ".c": "C", ".swift": "Swift",
    ".kt": "Kotlin", ".vue": "Vue", ".svelte": "Svelte",
    ".sh": "Shell", ".bash": "Shell", ".sql": "SQL",
    ".html": "HTML", ".css": "CSS", ".scss": "SCSS",
    ".md": "Markdown", ".yaml": "YAML", ".yml": "YAML",
    ".json": "JSON", ".toml": "TOML",
}

# ===============================
# 解析関数
# ===============================

def build_file_tree(root: Path, max_depth: int = 3, current_depth: int = 0) -> list:
    """ファイルツリーを構築（深さ制限あり）"""
    if current_depth >= max_depth:
        return []

    entries = []
    try:
        items = sorted(root.iterdir(), key=lambda x: (x.is_file(), x.name))
        for item in items:
            if item.name in IGNORE_DIRS or item.name.startswith("."):
                continue
            if item.is_dir():
                children = build_file_tree(item, max_depth, current_depth + 1)
                entries.append({
                    "name": item.name,
                    "type": "dir",
                    "children": children
                })
            else:
                entries.append({
                    "name": item.name,
                    "type": "file"
                })
    except PermissionError:
        pass

    return entries


def detect_languages(root: Path) -> dict:
    """使用言語と行数を集計"""
    lang_lines = defaultdict(int)
    lang_files = defaultdict(int)

    for path in root.rglob("*"):
        if any(ignored in path.parts for ignored in IGNORE_DIRS):
            continue
        if path.is_file():
            ext = path.suffix.lower()
            lang = LANGUAGE_MAP.get(ext)
            if lang and lang not in ("Markdown", "JSON", "YAML", "TOML"):
                try:
                    lines = len(path.read_text(encoding="utf-8", errors="ignore").splitlines())
                    lang_lines[lang] += lines
                    lang_files[lang] += 1
                except Exception:
                    pass

    # 行数順にソート
    sorted_langs = sorted(lang_lines.items(), key=lambda x: x[1], reverse=True)
    return {
        lang: {"lines": lines, "files": lang_files[lang]}
        for lang, lines in sorted_langs[:8]  # 上位8言語まで
    }


def read_dependency_files(root: Path) -> dict:
    """依存関係ファイルを読み取る"""
    deps = {}

    # package.json (Node.js)
    pkg = root / "package.json"
    if pkg.exists():
        try:
            data = json.loads(pkg.read_text(encoding="utf-8"))
            deps["package.json"] = {
                "name": data.get("name"),
                "description": data.get("description"),
                "scripts": list(data.get("scripts", {}).keys()),
                "dependencies": list(data.get("dependencies", {}).keys())[:15],
                "devDependencies": list(data.get("devDependencies", {}).keys())[:10],
            }
        except Exception:
            pass

    # requirements.txt (Python)
    req = root / "requirements.txt"
    if req.exists():
        try:
            lines = [l.strip() for l in req.read_text(encoding="utf-8").splitlines()
                     if l.strip() and not l.startswith("#")]
            deps["requirements.txt"] = lines[:20]
        except Exception:
            pass

    # pyproject.toml (Python modern)
    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        deps["pyproject.toml"] = pyproject.read_text(encoding="utf-8", errors="ignore")[:500]

    # go.mod (Go)
    gomod = root / "go.mod"
    if gomod.exists():
        deps["go.mod"] = gomod.read_text(encoding="utf-8", errors="ignore")[:300]

    # Cargo.toml (Rust)
    cargo = root / "Cargo.toml"
    if cargo.exists():
        deps["Cargo.toml"] = cargo.read_text(encoding="utf-8", errors="ignore")[:300]

    # .csproj (C#)
    csproj_files = list(root.glob("**/*.csproj"))[:2]
    if csproj_files:
        deps[".csproj"] = csproj_files[0].read_text(encoding="utf-8", errors="ignore")[:500]

    return deps


def detect_framework_hints(root: Path) -> list:
    """フレームワーク・ツールのヒントを検出"""
    hints = []
    markers = {
        "next.config.js": "Next.js",
        "next.config.ts": "Next.js",
        "vite.config.ts": "Vite",
        "vite.config.js": "Vite",
        "nuxt.config.ts": "Nuxt.js",
        "svelte.config.js": "SvelteKit",
        "astro.config.mjs": "Astro",
        "tailwind.config.js": "Tailwind CSS",
        "tailwind.config.ts": "Tailwind CSS",
        "prisma/schema.prisma": "Prisma",
        "docker-compose.yml": "Docker Compose",
        "docker-compose.yaml": "Docker Compose",
        "Dockerfile": "Docker",
        ".github/workflows": "GitHub Actions",
        "terraform": "Terraform",
        "fastapi": "FastAPI (directory hint)",
    }
    for marker, framework in markers.items():
        if (root / marker).exists():
            hints.append(framework)
    return hints


def read_existing_readme(root: Path) -> str | None:
    """既存READMEを読み取る（参考情報として）"""
    for name in ["README.md", "readme.md", "README.txt"]:
        f = root / name
        if f.exists():
            return f.read_text(encoding="utf-8", errors="ignore")[:1000]
    return None


def read_env_example(root: Path) -> list:
    """環境変数の例を読み取る"""
    for name in [".env.example", ".env.sample", ".env.local.example"]:
        f = root / name
        if f.exists():
            lines = [l.strip() for l in f.read_text(encoding="utf-8", errors="ignore").splitlines()
                     if l.strip() and not l.startswith("#") and "=" in l]
            return [l.split("=")[0] for l in lines[:20]]
    return []


def count_total_files(root: Path) -> dict:
    """総ファイル数をカウント"""
    total = 0
    code_files = 0
    for path in root.rglob("*"):
        if any(ignored in path.parts for ignored in IGNORE_DIRS):
            continue
        if path.is_file():
            total += 1
            if path.suffix.lower() in LANGUAGE_MAP:
                code_files += 1
    return {"total": total, "code": code_files}


# ===============================
# メイン
# ===============================

def analyze(repo_path: str) -> dict:
    root = Path(repo_path).resolve()
    if not root.exists():
        return {"error": f"Path not found: {repo_path}"}
    if not root.is_dir():
        return {"error": f"Not a directory: {repo_path}"}

    result = {
        "repo_path": str(root),
        "repo_name": root.name,
        "file_tree": build_file_tree(root),
        "languages": detect_languages(root),
        "dependencies": read_dependency_files(root),
        "framework_hints": detect_framework_hints(root),
        "env_variables": read_env_example(root),
        "file_counts": count_total_files(root),
        "existing_readme_snippet": read_existing_readme(root),
    }
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_repo.py <repo_path>", file=sys.stderr)
        sys.exit(1)

    result = analyze(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False, indent=2))
