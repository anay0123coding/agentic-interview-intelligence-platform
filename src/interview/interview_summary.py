from src.llm import llm
from src.interview.schemas import InterviewSummary

def generate_interview_summary(interview_state):
    scores = [
        evaluation.score
        for evaluation in interview_state.evaluation_history
    ]

    average_score = sum(scores) / len(scores) if scores else 0.0

    if average_score <= 3:
        overall_rating = "weak"
    elif average_score <= 7:
        overall_rating = "average"
    else:
        overall_rating = "strong"

    structured_llm = llm.with_structured_output(
        InterviewSummary,
        method="json_mode"
    )

    evaluations = []

    for evaluation in interview_state.evaluation_history:
        evaluations.append({
            "rating": evaluation.rating,
            "score": evaluation.score,
            "feedback": evaluation.feedback,
            "strengths": evaluation.strengths,
            "weaknesses": evaluation.weaknesses
        })

    prompt = f"""
You are analyzing the overall performance of a candidate
after a technical interview.

PROJECT NAME:
{interview_state.project_analysis.project_name}

PROJECT PURPOSE:
{interview_state.project_analysis.purpose}

QUESTIONS:
{interview_state.question_history}

CANDIDATE ANSWERS:
{interview_state.answer_history}

ANSWER EVALUATIONS:
{evaluations}

The deterministic interview metrics have already been calculated.

OVERALL RATING:
{overall_rating}

AVERAGE SCORE:
{average_score}

Analyze the candidate's performance across the complete interview.

Identify recurring strengths and weaknesses.

Provide specific and practical recommendations for improvement.

You MUST return this exact JSON structure:

{{
    "overall_rating": "{overall_rating}",
    "average_score": {average_score},
    "strengths": [
        "strength 1",
        "strength 2"
    ],
    "weaknesses": [
        "weakness 1",
        "weakness 2"
    ],
    "summary": "A concise summary of the candidate's overall interview performance.",
    "recommendations": [
        "recommendation 1",
        "recommendation 2",
        "recommendation 3"
    ]
}}

IMPORTANT RULES:

1. Use exactly these field names:
overall_rating
average_score
strengths
weaknesses
summary
recommendations

2. Do not rename any fields.

3. Do not use camelCase.

4. Do not omit any field.

5. strengths MUST always be a JSON list.

6. weaknesses MUST always be a JSON list.

7. recommendations MUST always be a JSON list.

8. Even if there is only one strength, weakness, or recommendation,
return it inside a list.

Correct:
"recommendations": ["Study Pydantic validation"]

Incorrect:
"recommendations": "Study Pydantic validation"

9. Use these exact values:

overall_rating: "{overall_rating}"
average_score: {average_score}

Return only valid JSON matching the structure above.
"""

    response = structured_llm.invoke(prompt)

    return response