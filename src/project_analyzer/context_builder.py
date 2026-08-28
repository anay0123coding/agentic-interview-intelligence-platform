MAX_FILE_CHARS=10000
MAX_TOTAL_CHARS=50000

def build_project_context(files_content):
    project_context=[]
    total_chars=0

    for file_path,content in files_content.items():
        content=content[:MAX_FILE_CHARS]

        file_section=f"""
FILE: {file_path}

CONTENT:
{content}

{'='*60}
"""

        if total_chars+len(file_section)>MAX_TOTAL_CHARS:
            break

        project_context.append(file_section)
        total_chars+=len(file_section)

    return "\n".join(project_context)