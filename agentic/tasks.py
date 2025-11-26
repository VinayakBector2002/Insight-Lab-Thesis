from crewai import Task
from agents import investigator

team_task = Task(
    description="""
    You are auditing a codebase for bugs.
    
    Your goal is to:
    1. Analyze the codebase for bugs.
    2. Report the bugs.
    

    path to codebase: 
    - /Users/vbector/Developer/Research/Insight-Lab-Thesis/agentic/agents.py
    - /Users/vbector/Developer/Research/Insight-Lab-Thesis/agentic/tasks.py
    - /Users/vbector/Developer/Research/Insight-Lab-Thesis/agentic/main.py
    - /Users/vbector/Developer/Research/Insight-Lab-Thesis/agentic/llm_config.py

    IMPORTANT: Provide your report directly as the Final Answer. Do NOT write it to a file.
    """,
    expected_output="Markdown report of bugs found in the codebase.",
    agent=investigator
)