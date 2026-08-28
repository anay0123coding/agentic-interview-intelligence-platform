from pathlib import Path

IGNORE_DIRS = {
    "venv",
    ".venv",
    ".git",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    ".next",
    ".cache",
    "coverage"
}

IGNORE_FILES = {
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "poetry.lock",
    "Pipfile.lock"
}

ALLOWED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".html",
    ".css",
    ".json",
    ".md"
}

MAX_FILE_SIZE = 20_000
MAX_TOTAL_SIZE = 60_000


def read_project_files(project_path):
    project_path = Path(project_path)

    files_content = {}
    total_size = 0

    for file_path in project_path.rglob("*"):

        if not file_path.is_file():
            continue

        if any(part in IGNORE_DIRS for part in file_path.parts):
            continue

        if file_path.name in IGNORE_FILES:
            continue

        if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue

        try:
            if file_path.stat().st_size > MAX_FILE_SIZE:
                continue

            content = file_path.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            content_size = len(content)

            if total_size + content_size > MAX_TOTAL_SIZE:
                break

            relative_path = file_path.relative_to(project_path)

            files_content[str(relative_path)] = content

            total_size += content_size

        except Exception:
            continue

    return files_content