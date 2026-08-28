from pathlib import Path

IGNORE_DIRS={
    "venv",
    ".git",
    "__pycache__",
    "node_modules"
}

ALLOWED_EXTENSIONS={
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

def read_project_files(project_path):
    project_path=Path(project_path)
    files_content={}

    for file_path in project_path.rglob("*"):
        if not file_path.is_file():
            continue

        if any(part in IGNORE_DIRS for part in file_path.parts):
            continue

        if file_path.suffix not in ALLOWED_EXTENSIONS:
            continue

        try:
            content=file_path.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            relative_path=file_path.relative_to(project_path)

            files_content[str(relative_path)]=content

        except Exception:
            continue

    return files_content