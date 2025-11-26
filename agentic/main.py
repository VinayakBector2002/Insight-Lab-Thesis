import sys
import os
from crewai import Crew
from agents import investigator
from tasks import team_task

def main():
    audit_crew = Crew(
        agents=[investigator],
        tasks=[team_task],
        verbose=True
    )

    print("Starting Agentic Auditing Crew...")
    result = audit_crew.kickoff(inputs={"scenario": "Test for bugs in the codebase."})
    print("\n" + "#" * 30)
    print("## Final Audit Report ##")
    print("#" * 30 + "\n")
    print(result)

if __name__ == "__main__":
    main()
