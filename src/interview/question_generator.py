from src.llm import llm
from src.interview.schemas import InterviewQuestion

def generate_question(
    project_analysis,
    previous_question=None,
    evaluation=None,
    question_history=None,
    topic_history=None,
    weak_topics=None,
    target_topic=None,
    difficulty="medium"
):
    structured_llm = llm.with_structured_output(
        InterviewQuestion,
        method="json_mode"
    )

    adaptive_context = ""

    if evaluation and evaluation.should_follow_up:
        adaptive_context = f"""
PREVIOUS QUESTION:
{previous_question.question}

CANDIDATE PERFORMANCE:
Rating: {evaluation.rating}
Score: {evaluation.score}

WEAKNESSES:
{evaluation.weaknesses}

Generate a follow-up question that helps investigate the candidate's
understanding of the weak areas.

The follow-up should be related to the previous question but should
probe deeper into the concepts the candidate failed to explain.
"""

    elif question_history:
        adaptive_context = f"""
PREVIOUSLY ASKED QUESTIONS:
{question_history}

PREVIOUSLY COVERED TOPICS:
{topic_history}

IDENTIFIED WEAK TOPICS:
{weak_topics}

Generate a new question that explores an important technical concept.

Avoid repeating previously covered topics when other important
technical concepts from the project are still unexplored.

However, if a weak topic is important and has not been sufficiently
investigated, you may revisit that weak area with a different question.

Do not repeat or closely rephrase any previously asked question.

Prefer concepts from:

{project_analysis.technical_concepts}
"""

    else:
        adaptive_context = """
This is the first question of the interview.

Generate an important project-specific technical question.
"""
    topic_context = ""

    if target_topic:
        topic_context = f"""
    TARGET TOPIC:
    {target_topic}

    Generate the question specifically about this topic.
    Do not choose a different primary topic.
    """
    prompt = f"""
You are a technical interviewer.

You are interviewing a candidate about the following software project.

PROJECT NAME:
{project_analysis.project_name}

PROJECT PURPOSE:
{project_analysis.purpose}

TECHNOLOGIES:
{project_analysis.technologies}

ARCHITECTURE:
{project_analysis.architecture}

COMPONENTS:
{project_analysis.components}

TECHNICAL CONCEPTS:
{project_analysis.technical_concepts}

{topic_context}

{adaptive_context}

The question should test whether the candidate genuinely understands
their implementation and technical decisions.

Do not ask generic questions unless they are directly connected to
the project.

TARGET DIFFICULTY:
{difficulty}

Generate the question at the requested difficulty level.

Easy questions should focus on explaining components, architecture,
or basic implementation decisions.

Medium questions should require deeper understanding of design choices,
data flow, and technical trade-offs.

Hard questions should probe edge cases, limitations, scalability,
alternative approaches, or require deeper reasoning about the implementation.

Return JSON matching this structure:

{{
    "question": "...",
    "topic": "...",
    "difficulty": "{difficulty}"
}}
"""

    response = structured_llm.invoke(prompt)

    if target_topic:
        response.topic = target_topic

    elif previous_question:
        response.topic = previous_question.topic

    return response