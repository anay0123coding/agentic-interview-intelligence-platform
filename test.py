from src.llm import llm

response=llm.invoke("Explain what an AI agent is in two sentences.")

print(response.content)