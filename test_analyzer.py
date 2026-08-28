from src.project_analyzer.file_reader import read_project_files
from src.project_analyzer.context_builder import build_project_context
from src.project_analyzer.analyzer import analyze_project

files=read_project_files(".")

project_context=build_project_context(files)

analysis=analyze_project(project_context)

print("\nPROJECT NAME:")
print(analysis.project_name)

print("\nPURPOSE:")
print(analysis.purpose)

print("\nTECHNOLOGIES:")
print(analysis.technologies)

print("\nARCHITECTURE:")
print(analysis.architecture)

print("\nCOMPONENTS:")
for component in analysis.components:
    print("-",component)

print("\nTECHNICAL CONCEPTS:")
for concept in analysis.technical_concepts:
    print("-",concept)