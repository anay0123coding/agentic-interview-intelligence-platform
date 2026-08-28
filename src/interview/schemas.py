from typing import List, Optional
from pydantic import BaseModel, Field
from src.project_analyzer.schemas import ProjectAnalysis

class InterviewQuestion(BaseModel):
    question: str = Field(
        description="A project-specific technical interview question"
    )
    topic: str = Field(
        description="The technical topic being tested"
    )
    difficulty: str = Field(
        description="Difficulty level: easy, medium, or hard"
    )

class AnswerEvaluation(BaseModel):
    rating: str = Field(
        description="Overall rating: strong, partial, or weak"
    )
    score: int = Field(
        description="Score from 1 to 10"
    )
    feedback: str = Field(
        description="Brief explanation of the quality of the answer"
    )
    strengths: List[str] = Field(
        description="Important things the candidate explained correctly"
    )
    weaknesses: List[str] = Field(
        description="Missing, incorrect, or weak parts of the answer"
    )
    should_follow_up: bool = Field(
        description="Whether a follow-up question is needed"
    )

class InterviewState(BaseModel):
    project_analysis: ProjectAnalysis
    current_question: Optional[InterviewQuestion] = None
    question_history: List[str] = Field(default_factory=list)
    topic_history: List[str] = Field(default_factory=list)
    weak_topics: List[str] = Field(default_factory=list)
    follow_up_counts: dict[str, int] = Field(default_factory=dict)
    answer_history: List[str] = Field(default_factory=list)
    evaluation_history: List[AnswerEvaluation] = Field(default_factory=list)
    current_difficulty: str = "medium"
    current_topic: Optional[str] = None
    is_follow_up: bool = False


class InterviewSummary(BaseModel):
    overall_rating: str = Field(
        description="Overall interview rating: strong, average, or weak"
    )
    average_score: float = Field(
        description="Average score across all interview answers"
    )
    strengths: List[str] = Field(
        description="Key strengths demonstrated during the interview"
    )
    weaknesses: List[str] = Field(
        description="Key weaknesses identified during the interview"
    )
    summary: str = Field(
        description="Overall summary of the candidate's performance"
    )
    recommendations: List[str] = Field(
        description="Specific recommendations for improvement"
    )