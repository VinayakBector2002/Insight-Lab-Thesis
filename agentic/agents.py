from crewai import Agent
from llm_config import llm
from crewai_tools import FileReadTool

file_tool = FileReadTool()
investigator = Agent(
    role="Investigator",
    goal="Detect Bugs in the code in the codebase",
    backstory="You are a security researcher. Your job is to find bugs in the codebase.",
    tools=[file_tool],
    llm=llm,
    verbose=True
)