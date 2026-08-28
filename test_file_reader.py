from src.project_analyzer.file_reader import read_project_files

project_path="."

files=read_project_files(project_path)

for file_name,content in files.items():
    print(f"\n{'='*50}")
    print(file_name)
    print(f"{'='*50}")
    print(content[:500])