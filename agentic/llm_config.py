from crewai import LLM

llm = LLM(
    model="ollama/dolphin-llama3:latest",
    base_url="http://localhost:11434"
)
