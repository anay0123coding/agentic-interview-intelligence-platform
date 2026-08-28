# Agentic Interview Intelligence Platform

An AI-powered platform that analyzes a software project and conducts an adaptive technical interview based on the project's actual implementation, architecture, technologies, and technical concepts.

Users can upload their own project as a ZIP file, receive an AI-generated project analysis, and participate in a dynamic interview where questions adapt according to their answers.

## Features

- Upload a software project as a ZIP file
- Analyze project source code using an LLM
- Generate a project summary including architecture, technologies, components, and technical concepts
- Generate project-specific technical interview questions
- Adapt interview difficulty based on candidate performance
- Generate follow-up questions when weaknesses are detected
- Track weak technical topics
- Avoid unnecessary repetition of previously covered topics
- Limit follow-up questions for the same topic
- Automatically determine when an interview should end
- Evaluate candidate answers with detailed feedback
- Generate a final interview performance summary
- Support both local project paths and uploaded ZIP projects

## How It Works

```text
Project Upload / Local Project
            ↓
      Read Project Files
            ↓
    Build Project Context
            ↓
      LLM Project Analysis
            ↓
      Project Summary
            ↓
      Start Interview
            ↓
Generate Project-Specific Question
            ↓
      Candidate Answer
            ↓
       Answer Evaluation
            ↓
Difficulty / Follow-up Decision
            ↓
      Next Question
            ↓
    Final Interview Summary