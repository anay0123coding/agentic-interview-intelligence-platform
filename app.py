import streamlit as st

from src.project_analyzer.file_reader import read_project_files
from src.project_analyzer.context_builder import build_project_context
from src.project_analyzer.analyzer import analyze_project
from src.interview.interview_engine import InterviewEngine
from src.project_analyzer.zip_handler import extract_project_zip


st.set_page_config(
    page_title="Agentic Interview Platform",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Agentic Interview Intelligence Platform")

st.write(
    "Analyze your software project and practice with "
    "adaptive AI-generated interview questions."
)

st.divider()

st.header("📂 Analyze Your Project")

st.write(
    "Upload your project as a ZIP file or enter a local project path."
)

uploaded_file = st.file_uploader(
    "Upload your project ZIP file",
    type=["zip"]
)

project_path = st.text_input(
    "Or enter a local project path",
    value="."
)

if st.button("Analyze Project", type="primary"):

    with st.spinner("Analyzing your project..."):

        if uploaded_file is not None:

            project_path = extract_project_zip(
                uploaded_file
            )

        files = read_project_files(project_path)

        project_context = build_project_context(files)

        analysis = analyze_project(project_context)

        st.session_state.project_analysis = analysis

    st.success("Project analysis completed!")


if "project_analysis" in st.session_state:

    analysis = st.session_state.project_analysis

    st.subheader("Project Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Project Name")
        st.write(analysis.project_name)

        st.markdown("### Purpose")
        st.write(analysis.purpose)

        st.markdown("### Technologies")

        for technology in analysis.technologies:
            st.write(f"- {technology}")

    with col2:
        st.markdown("### Architecture")
        st.write(analysis.architecture)

        st.markdown("### Components")

        for component in analysis.components:
            st.write(f"- {component}")

    st.markdown("### Technical Concepts")

    for concept in analysis.technical_concepts:
        st.write(f"- {concept}")


st.divider()

st.header("🎯 Start Interview")

if "project_analysis" in st.session_state:

    if st.button("Start Interview", type="primary"):

        st.session_state.interview_engine = InterviewEngine(
            project_analysis=st.session_state.project_analysis
        )

        st.session_state.interview_started = True

        if "current_question" in st.session_state:
            del st.session_state.current_question

        if "current_evaluation" in st.session_state:
            del st.session_state.current_evaluation

        if "candidate_answer" in st.session_state:
            del st.session_state.candidate_answer

        if "interview_completed" in st.session_state:
            del st.session_state.interview_completed

        if "interview_summary" in st.session_state:
            del st.session_state.interview_summary

        st.success("Interview started!")


if (
    st.session_state.get("interview_started", False)
    and not st.session_state.get("interview_completed", False)
):

    st.divider()

    st.header("🧠 Interview")

    engine = st.session_state.interview_engine

    if "current_question" not in st.session_state:

        with st.spinner("Generating question..."):

            question = engine.get_next_question()

            st.session_state.current_question = question

    question = st.session_state.current_question

    st.subheader("Question")

    st.write(question.question)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Topic",
            question.topic
        )

    with col2:
        st.metric(
            "Difficulty",
            question.difficulty
        )

    with col3:
        if engine.state.is_follow_up:
            question_type = "Follow-up"
        else:
            question_type = "New Question"

        st.metric(
            "Question Type",
            question_type
        )

    st.divider()

    st.subheader("Your Answer")

    candidate_answer = st.text_area(
        "Write your answer here",
        height=200,
        placeholder="Explain your answer in detail..."
    )

    if st.button("Submit Answer", type="primary"):

        if not candidate_answer.strip():

            st.warning(
                "Please write an answer before submitting."
            )

        else:

            with st.spinner("Evaluating your answer..."):

                evaluation = engine.submit_answer(
                    candidate_answer
                )

            st.session_state.current_evaluation = evaluation
            st.session_state.candidate_answer = candidate_answer

            st.rerun()


    if "current_evaluation" in st.session_state:

        evaluation = st.session_state.current_evaluation

        st.divider()

        st.subheader("📊 Answer Evaluation")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Rating",
                evaluation.rating
            )

        with col2:
            st.metric(
                "Score",
                f"{evaluation.score}/10"
            )

        st.markdown("### Feedback")
        st.write(evaluation.feedback)

        st.markdown("### Strengths")

        if evaluation.strengths:

            for strength in evaluation.strengths:
                st.write(f"✅ {strength}")

        else:
            st.write("No major strengths identified.")

        st.markdown("### Areas to Improve")

        if evaluation.weaknesses:

            for weakness in evaluation.weaknesses:
                st.write(f"⚠️ {weakness}")

        else:
            st.write("No major weaknesses identified.")

        if evaluation.should_follow_up:

            st.info(
                "The next question may be a follow-up "
                "based on this answer."
            )


        if engine.is_interview_complete():

            st.success("🎉 Interview Complete!")

            if st.button(
                "View Final Summary",
                type="primary"
            ):

                with st.spinner(
                    "Generating final interview summary..."
                ):

                    summary = engine.get_summary()

                st.session_state.interview_summary = summary
                st.session_state.interview_completed = True

                st.rerun()

        else:

            if st.button(
                "Next Question",
                type="primary"
            ):

                del st.session_state.current_question
                del st.session_state.current_evaluation

                if "candidate_answer" in st.session_state:
                    del st.session_state.candidate_answer

                st.rerun()


if st.session_state.get("interview_completed", False):

    summary = st.session_state.interview_summary

    st.divider()

    st.header("🏁 Final Interview Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Overall Rating",
            summary.overall_rating
        )

    with col2:
        st.metric(
            "Average Score",
            f"{summary.average_score:.1f}/10"
        )

    st.subheader("Summary")
    st.write(summary.summary)

    st.subheader("Strengths")

    if summary.strengths:

        for strength in summary.strengths:
            st.write(f"✅ {strength}")

    else:
        st.write("No major strengths identified.")

    st.subheader("Areas to Improve")

    if summary.weaknesses:

        for weakness in summary.weaknesses:
            st.write(f"⚠️ {weakness}")

    else:
        st.write("No major weaknesses identified.")

    st.subheader("Recommendations")

    if summary.recommendations:

        for recommendation in summary.recommendations:
            st.write(f"💡 {recommendation}")



if st.session_state.get("interview_completed", False):

    st.divider()

    if st.button("🔄 Start New Interview", type="primary"):

        keys_to_remove = [
            "interview_engine",
            "interview_started",
            "current_question",
            "current_evaluation",
            "candidate_answer",
            "interview_summary",
            "interview_completed"
        ]

        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]

        st.rerun()