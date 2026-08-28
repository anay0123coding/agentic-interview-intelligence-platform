from typing import List, Optional

from src.interview.schemas import AnswerEvaluation


class InterviewPolicy:

    def should_follow_up(
        self,
        evaluation: AnswerEvaluation,
        follow_up_count: int,
        max_follow_ups: int = 2
    ) -> bool:

        if not evaluation.should_follow_up:
            return False

        return follow_up_count < max_follow_ups


    def update_difficulty(
        self,
        score: int
    ) -> str:

        if score <= 3:
            return "easy"

        elif score <= 7:
            return "medium"

        return "hard"


    def is_interview_complete(
        self,
        evaluations: List[AnswerEvaluation],
        max_questions: int = 5
    ) -> bool:

        if len(evaluations) >= max_questions:
            return True

        if len(evaluations) < 3:
            return False

        recent_scores = [
            evaluation.score
            for evaluation in evaluations[-3:]
        ]

        average_score = (
            sum(recent_scores) / len(recent_scores)
        )

        if average_score <= 2:
            return True

        if average_score >= 9:
            return True

        return False


    def normalize_topic(
        self,
        topic: Optional[str]
    ) -> str:

        if not topic:
            return ""

        return topic.lower().strip()


    def select_next_topic(
        self,
        technical_concepts: List[str],
        topic_history: List[str],
        weak_topics: List[str]
    ) -> Optional[str]:

        normalized_history = {
            self.normalize_topic(topic)
            for topic in topic_history
        }

        unexplored_topics = [
            topic
            for topic in technical_concepts
            if self.normalize_topic(topic) not in normalized_history
        ]

        if unexplored_topics:
            return unexplored_topics[0]

        if weak_topics:
            return weak_topics[0]

        if technical_concepts:
            return technical_concepts[0]

        return None