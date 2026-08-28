from pydantic import BaseModel,Field

class ProjectAnalysis(BaseModel):
    project_name:str=Field(
        description="Name of the project if identifiable, otherwise a suitable descriptive name"
    )
    purpose:str=Field(
        description="Main purpose of the project"
    )
    technologies:list[str]=Field(
        description="Programming languages, frameworks, libraries, and important technologies used"
    )
    architecture:str=Field(
        description="High-level architecture and organization of the project"
    )
    components:list[str]=Field(
        description="Important modules or components and their responsibilities"
    )
    technical_concepts:list[str]=Field(
        description="Important technical concepts demonstrated by the project"
    )