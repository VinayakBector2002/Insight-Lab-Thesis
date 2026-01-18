import sys
import os
from crewai import Crew, Process
from tasks import red_team_task, eval_task, investigate_task\nfrom agents import investigator, evaluator, red_teamer\nfrom llm_config import llm
import json
from datetime import datetime

# Add parent directory to path to import consts
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from consts.variants import VARIANTS


def log_to_file(variant_name, result, log_file="audit_log.json"):
    """Log results to a JSON file for dashboard visualization."""
    try:
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                logs = json.load(f)
        else:
            logs = {}

        logs[variant_name] = {
            "system_prompt": VARIANTS[variant_name]["system"],
            "user_prompt": VARIANTS[variant_name]["user"],
            "result": str(result),
            "timestamp": str(datetime.now()),
        }

        with open(log_file, "w") as f:
            json.dump(logs, f, indent=2)
    except Exception as e:
        print(f"Logging error: {e}")


def human_oversight_prompt(variant_name, result):
    """Interactive prompt for human oversight."""
    print(f"\n--- Human Oversight for '{variant_name}' ---")
    print("Agent result summary:")
    print(str(result)[:200] + "..." if len(str(result)) > 200 else str(result))
    response = input("Approve result? (y/n/modify): ").strip().lower()
    if response == "n":
        print("Result rejected. Skipping to next.")
        return False
    elif response.startswith("m"):
        new_result = input("Enter modified result: ")
        return new_result
    return True


def main():
    audit_crew = Crew(
        agents=[red_teamer, evaluator, investigator],
        tasks=[red_team_task, eval_task, investigate_task],
        verbose=True,
    )

    print("Starting Agentic Auditing Crew...")
    print(f"Testing {len(VARIANTS)} variants\n")

    interactive_mode = (
        input("Enable interactive human oversight? (y/n): ").strip().lower() == "y"
    )

    results = {}

    for i, (variant_name, variant) in enumerate(VARIANTS.items()):
        print("\n" + "=" * 60)
        print(f"VARIANT {i + 1}/{len(VARIANTS)}: {variant_name}")
        print("=" * 60)
        print(f"System: {variant['system'][:80]}...")
        print(f"User: {variant['user'][:80]}...")
        print("=" * 60 + "\n")

        try:
            result = audit_crew.kickoff(
                inputs={
                    "system_prompt": variant["system"],
                    "user_prompt": variant["user"],
                }
            )

            if interactive_mode:
                approval = human_oversight_prompt(variant_name, result)
                if approval is False:
                    continue
                elif isinstance(approval, str):
                    result = approval

            results[variant_name] = result
            log_to_file(variant_name, result)

            print("\n" + "#" * 60)
            print(f"## Audit Report for '{variant_name}' ##")
            print("#" * 60 + "\n")
            print(result)
            print("\n")

        except Exception as e:
            print(f"Error processing variant '{variant_name}': {e}")
            results[variant_name] = f"Error: {e}"
            log_to_file(variant_name, results[variant_name])

    # Summary
    print("\n" + "=" * 60)
    print("TESTING COMPLETE")
    print("=" * 60)
    print(f"Tested {len(results)} variants: {', '.join(results.keys())}")

    # Simple dashboard
    print("\n--- Summary Dashboard ---")
    for name, res in results.items():
        status = (
            "Refused"
            if "cannot" in str(res).lower() or "can't" in str(res).lower()
            else "Completed"
        )
        print(f"{name}: {status}")


if __name__ == "__main__":
    main()
