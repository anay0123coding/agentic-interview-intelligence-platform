from src.project_analyzer.file_reader import read_project_files
from src.project_analyzer.context_builder import build_project_context
from src.project_analyzer.analyzer import analyze_project
from src.interview.question_generator import generate_question

files=read_project_files(".")

project_context=build_project_context(files)

project_analysis=analyze_project(project_context)

question=generate_question(project_analysis)

print("\nQUESTION:")
print(question.question)

print("\nTOPIC:")
print(question.topic)

print("\nDIFFICULTY:")
print(question.difficulty)