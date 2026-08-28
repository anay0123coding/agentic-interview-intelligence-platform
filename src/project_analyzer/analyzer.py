from src.llm import llm
from src.project_analyzer.schemas import ProjectAnalysis


MAX_CONTEXT_CHARS = 16_000


def analyze_project(project_context):

    project_context = project_context[:MAX_CONTEXT_CHARS]

    structured_llm = llm.with_structured_output(
        ProjectAnalysis,
        method="json_mode"
    )

    prompt = f"""
You are an expert software engineer analyzing a codebase.

Analyze the project context provided below.

Identify the project's purpose, technologies, architecture, important
components, and technical concepts.

Return the response as JSON matching this structure:

{{
    "project_name": "...",
    "purpose": "...",
    "technologies": ["..."],
    "architecture": "...",
    "components": ["..."],
    "technical_concepts": ["..."]
}}

Do not invent information that is not supported by the provided code.
If some information is unclear, mention that clearly in the relevant field.

PROJECT CONTEXT:

{project_context}
"""

    response = structured_llm.invoke(prompt)

    return response