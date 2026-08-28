from src.llm import llm
from src.interview.schemas import AnswerEvaluation

def evaluate_answer(project_analysis,question,candidate_answer):
    structured_llm=llm.with_structured_output(
        AnswerEvaluation,
        method="json_mode"
    )

    prompt=f"""
You are an expert technical interviewer evaluating a candidate.

Evaluate the candidate's answer based on the interview question and
the context of their project.

PROJECT:
{project_analysis.project_name}

PROJECT PURPOSE:
{project_analysis.purpose}

RELEVANT TECHNOLOGIES:
{project_analysis.technologies}

QUESTION:
{question.question}

TOPIC:
{question.topic}

EXPECTED DIFFICULTY:
{question.difficulty}

CANDIDATE ANSWER:
{candidate_answer}

Evaluate whether the answer demonstrates genuine understanding.

Use these ratings:

- strong: technically accurate and demonstrates clear understanding
- partial: partially correct but missing important details
- weak: incorrect, vague, or demonstrates little understanding

Give a score from 1 to 10.

Set should_follow_up to true if the candidate's answer is partial,
unclear, or worth probing further.

Return JSON matching this structure:

{{
    "rating":"strong, partial, or weak",
    "score":1,
    "feedback":"...",
    "strengths":["..."],
    "weaknesses":["..."],
    "should_follow_up":true
}}
"""

    response=structured_llm.invoke(prompt)

    return response