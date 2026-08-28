import os
import zipfile
import tempfile
import shutil

MAX_ZIP_SIZE = 50 * 1024 * 1024
MAX_FILES = 500
MAX_TOTAL_SIZE = 100 * 1024 * 1024

IGNORED_DIRECTORIES = {
    "venv",
    ".venv",
    "node_modules",
    ".git",
    "__pycache__",
    "dist",
    "build"
}


def is_safe_path(base_path, target_path):
    base_path = os.path.abspath(base_path)
    target_path = os.path.abspath(target_path)

    return os.path.commonpath(
        [base_path, target_path]
    ) == base_path


def extract_project_zip(uploaded_file):
    if uploaded_file.size > MAX_ZIP_SIZE:
        raise ValueError(
            "ZIP file is too large. Maximum allowed size is 50 MB."
        )

    temp_dir = tempfile.mkdtemp()

    try:
        zip_path = os.path.join(
            temp_dir,
            "uploaded_project.zip"
        )

        with open(zip_path, "wb") as file:
            file.write(uploaded_file.getbuffer())

        extract_path = os.path.join(
            temp_dir,
            "project"
        )

        with zipfile.ZipFile(zip_path, "r") as zip_file:

            file_infos = zip_file.infolist()

            if len(file_infos) > MAX_FILES:
                raise ValueError(
                    "Project contains too many files."
                )

            total_size = sum(
                file_info.file_size
                for file_info in file_infos
            )

            if total_size > MAX_TOTAL_SIZE:
                raise ValueError(
                    "Extracted project is too large."
                )

            for file_info in file_infos:

                target_path = os.path.join(
                    extract_path,
                    file_info.filename
                )

                if not is_safe_path(
                    extract_path,
                    target_path
                ):
                    raise ValueError(
                        "Unsafe ZIP file detected."
                    )

                path_parts = file_info.filename.split("/")

                if any(
                    part in IGNORED_DIRECTORIES
                    for part in path_parts
                ):
                    continue

                if file_info.is_dir():
                    continue

                os.makedirs(
                    os.path.dirname(target_path),
                    exist_ok=True
                )

                with zip_file.open(file_info) as source:
                    with open(target_path, "wb") as target:
                        shutil.copyfileobj(
                            source,
                            target
                        )

        items = os.listdir(extract_path)

        if len(items) == 1:
            possible_project_path = os.path.join(
                extract_path,
                items[0]
            )

            if os.path.isdir(possible_project_path):
                return possible_project_path

        return extract_path

    except Exception:
        shutil.rmtree(
            temp_dir,
            ignore_errors=True
        )
        raise