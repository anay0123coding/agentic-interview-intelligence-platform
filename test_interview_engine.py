from src.project_analyzer.file_reader import read_project_files
from src.project_analyzer.context_builder import build_project_context
from src.project_analyzer.analyzer import analyze_project
from src.interview.interview_engine import InterviewEngine

files = read_project_files(".")

project_context = build_project_context(files)

analysis = analyze_project(project_context)

engine = InterviewEngine(
    project_analysis=analysis
)

round_number = 1

while not engine.is_interview_complete():

    print(f"\n{'=' * 50}")
    print(f"INTERVIEW ROUND {round_number}")
    print(f"{'=' * 50}")

    question = engine.get_next_question()

    print("\nQUESTION TYPE:")

    if engine.state.is_follow_up:
        print("Follow-up Question")
    else:
        print("New Question")

    print("\nQUESTION:")
    print(question.question)

    print("\nTOPIC:")
    print(question.topic)

    print("\nDIFFICULTY:")
    print(question.difficulty)

    candidate_answer = input("\nYour answer: ")

    evaluation = engine.submit_answer(candidate_answer)

    print("\nRATING:")
    print(evaluation.rating)

    print("\nSCORE:")
    print(evaluation.score)

    print("\nFEEDBACK:")
    print(evaluation.feedback)

    print("\nFOLLOW-UP NEEDED:")
    print(evaluation.should_follow_up)

    print("\nNEXT DIFFICULTY:")
    print(engine.state.current_difficulty)

    round_number += 1



summary = engine.get_summary()

print(f"\n{'=' * 50}")
print("FINAL INTERVIEW SUMMARY")
print(f"{'=' * 50}")

print("\nOVERALL RATING:")
print(summary.overall_rating)

print("\nAVERAGE SCORE:")
print(summary.average_score)

print("\nSTRENGTHS:")
for strength in summary.strengths:
    print("-", strength)

print("\nWEAKNESSES:")
for weakness in summary.weaknesses:
    print("-", weakness)

print("\nSUMMARY:")
print(summary.summary)

print("\nRECOMMENDATIONS:")
for recommendation in summary.recommendations:
    print("-", recommendation)