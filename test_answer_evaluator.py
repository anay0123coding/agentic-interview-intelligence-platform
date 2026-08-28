from src.project_analyzer.file_reader import read_project_files
from src.project_analyzer.context_builder import build_project_context
from src.project_analyzer.analyzer import analyze_project
from src.interview.question_generator import generate_question
from src.interview.answer_evaluator import evaluate_answer

files=read_project_files(".")

project_context=build_project_context(files)

project_analysis=analyze_project(project_context)

question=generate_question(project_analysis)

print("\nQUESTION:")
print(question.question)

candidate_answer=input("\nYour answer: ")

evaluation=evaluate_answer(
    project_analysis,
    question,
    candidate_answer
)

print("\nRATING:")
print(evaluation.rating)

print("\nSCORE:")
print(evaluation.score)

print("\nFEEDBACK:")
print(evaluation.feedback)

print("\nSTRENGTHS:")
for strength in evaluation.strengths:
    print("-",strength)

print("\nWEAKNESSES:")
for weakness in evaluation.weaknesses:
    print("-",weakness)

print("\nFOLLOW-UP NEEDED:")
print(evaluation.should_follow_up)