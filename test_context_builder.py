from src.project_analyzer.file_reader import read_project_files
from src.project_analyzer.context_builder import build_project_context

files=read_project_files(".")

project_context=build_project_context(files)

print(project_context)
print(f"\nTotal characters: {len(project_context)}")