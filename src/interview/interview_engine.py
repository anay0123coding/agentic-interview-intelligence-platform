from src.interview.schemas import InterviewState, InterviewQuestion
from src.interview.answer_evaluator import evaluate_answer
from src.interview.question_generator import generate_question
from src.interview.interview_summary import generate_interview_summary
from src.interview.interview_policy import InterviewPolicy

class InterviewEngine:

    def __init__(self, project_analysis):
        self.state = InterviewState(
            project_analysis=project_analysis
        )

        self.policy = InterviewPolicy()

    def set_question(self, question: str, topic: str, difficulty: str):
        interview_question = InterviewQuestion(
            question=question,
            topic=topic,
            difficulty=difficulty
        )

        self.state.current_question = interview_question
        self.state.current_topic = topic
        self.state.current_difficulty = difficulty

    def submit_answer(self, candidate_answer: str):
        evaluation = evaluate_answer(
            project_analysis=self.state.project_analysis,
            question=self.state.current_question,
            candidate_answer=candidate_answer
        )

        self.state.question_history.append(
            self.state.current_question.question
        )

        self.state.topic_history.append(
            self.state.current_topic
        )

        self.state.answer_history.append(
            candidate_answer
        )

        self.state.evaluation_history.append(
            evaluation
        )

        if evaluation.score <= 4:
            if self.state.current_topic not in self.state.weak_topics:
                self.state.weak_topics.append(
                    self.state.current_topic
                )

        elif evaluation.score >= 7:
            if self.state.current_topic in self.state.weak_topics:
                self.state.weak_topics.remove(
                    self.state.current_topic
                )

        self.state.current_difficulty = (
            self.policy.update_difficulty(evaluation.score)
        )

        return evaluation


    def select_next_topic(self):
        return self.policy.select_next_topic(
            technical_concepts=self.state.project_analysis.technical_concepts,
            topic_history=self.state.topic_history,
            weak_topics=self.state.weak_topics
        )

    def get_next_question(self):
        if not self.state.evaluation_history:
            self.state.is_follow_up = False

            selected_topic = self.select_next_topic()

            question = generate_question(
                project_analysis=self.state.project_analysis,
                question_history=self.state.question_history,
                topic_history=self.state.topic_history,
                weak_topics=self.state.weak_topics,
                target_topic=selected_topic,
                difficulty=self.state.current_difficulty
            )
        else:
            last_evaluation = self.state.evaluation_history[-1]

            topic = self.state.current_topic

            follow_up_count = self.state.follow_up_counts.get(
                topic,
                0
            )

            if self.policy.should_follow_up(
                evaluation=last_evaluation,
                follow_up_count=follow_up_count
            ):
                self.state.is_follow_up = True

                self.state.follow_up_counts[topic] = (
                    self.state.follow_up_counts.get(topic, 0) + 1
                )

                question = generate_question(
                    project_analysis=self.state.project_analysis,
                    previous_question=self.state.current_question,
                    evaluation=last_evaluation,
                    question_history=self.state.question_history,
                    topic_history=self.state.topic_history,
                    weak_topics=self.state.weak_topics,
                    difficulty=self.state.current_difficulty
                )
            else:
                self.state.is_follow_up = False

                selected_topic = self.select_next_topic()

                question = generate_question(
                    project_analysis=self.state.project_analysis,
                    question_history=self.state.question_history,
                    topic_history=self.state.topic_history,
                    weak_topics=self.state.weak_topics,
                    target_topic=selected_topic,
                    difficulty=self.state.current_difficulty
                )

        self.state.current_question = question
        self.state.current_topic = question.topic

        return question


    


    def get_summary(self):
        summary = generate_interview_summary(
            interview_state=self.state
        )

        return summary

    def is_interview_complete(self, max_questions: int = 5):
        return self.policy.is_interview_complete(
            evaluations=self.state.evaluation_history,
            max_questions=max_questions
        )


    