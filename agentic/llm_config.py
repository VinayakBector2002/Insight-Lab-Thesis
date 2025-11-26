from crewai import LLM

llm = LLM(
    model="ollama/llama3.1:8b",
    base_url="http://localhost:11434"
)
