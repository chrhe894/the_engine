"""
Continue an existing Case File interactively.

Usage:
    python continue_case.py engine
    python continue_case.py income
    python continue_case.py cases/826868e0.json

Flow:
1. Load the case file by name fragment, ID prefix, or path.
2. Show the active mission awaiting completion.
3. Ask for your result and observation.
4. Feed it to the AI Engine.
5. Show the next proposal.
6. Ask for your decision (ACCEPT / MODIFY / REJECT / EXPLORE FURTHER / GIVE UP).
7. Save the updated case file.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

from case_file import (
    CaseFile,
    DECISION_ACCEPT, DECISION_MODIFY, DECISION_REJECT,
    DECISION_EXPLORE, DECISION_GIVE_UP,
    MISSION_ACTIVE, MISSION_COMPLETED,
)
from engine_ai import AIEngine


def find_case_file(query):
    """Find a case file by name fragment, ID prefix, or full path."""
    path = Path(query)
    if path.exists():
        return str(path)

    cases_dir = Path("cases")
    if not cases_dir.exists():
        return None

    query_lower = query.lower()
    for f in sorted(cases_dir.glob("*.json")):
        if f.stem.startswith(query_lower):
            return str(f)
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            name = data.get("context", {}).get("description", "").lower()
            if query_lower in name:
                return str(f)
        except (json.JSONDecodeError, OSError):
            continue

    return None


def separator(title=""):
    if title:
        print(f"\n{'=' * 60}")
        print(f"  {title}")
        print(f"{'=' * 60}")
    else:
        print(f"\n{'-' * 60}")


def prompt(text):
    try:
        return input(f"  {text}> ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n\n  Goodbye.\n")
        sys.exit(0)


def show_mission(mission):
    """Display a mission."""
    label = mission.name or mission.id
    print(f"    Mission: {label} ({mission.id})")
    print(f"    Description: {mission.description}")
    if mission.purpose:
        print(f"    Purpose: {mission.purpose}")
    if mission.definition_of_done:
        print(f"    Done when:")
        for d in mission.definition_of_done:
            print(f"      - {d}")


def show_proposal(proposal):
    """Display a proposal from the Engine."""
    separator("ENGINE PROPOSAL")
    if proposal.mission_name:
        print(f"\n  Name:       {proposal.mission_name}")
    print(f"  Suggestion: {proposal.suggestion}")
    print(f"  Reason:     {proposal.reason}")
    print(f"  Mission:    {proposal.mission_description}")
    if proposal.mission_purpose:
        print(f"  Purpose:    {proposal.mission_purpose}")
    if proposal.definition_of_done:
        print(f"  Done when:")
        for d in proposal.definition_of_done:
            print(f"    - {d}")
    print()


def get_decision():
    """Ask the user for a decision."""
    print("  What do you decide?\n")
    print("    1. ACCEPT")
    print("    2. MODIFY")
    print("    3. REJECT")
    print("    4. EXPLORE FURTHER")
    print("    5. GIVE UP")
    print("    6. Quit (decide later)")
    print()

    while True:
        choice = prompt("Decision")
        decisions = {"1": DECISION_ACCEPT, "2": DECISION_MODIFY, "3": DECISION_REJECT,
                     "4": DECISION_EXPLORE, "5": DECISION_GIVE_UP, "6": None}
        if choice in decisions:
            return decisions[choice]
        print("    Please enter 1-6.")


def main():
    if len(sys.argv) < 2:
        print("\n  Usage: python continue_case.py <case_name_or_id>")
        print("  Example: python continue_case.py engine\n")
        sys.exit(1)

    query = sys.argv[1]
    filepath = find_case_file(query)
    if filepath is None:
        print(f"\n  No case file matching '{query}' found.\n")
        sys.exit(1)

    # Load case
    case = CaseFile.load(filepath)
    engine = AIEngine()

    name = case.context.get("description", "Unnamed")
    separator(f"{name}")

    if engine.available:
        print(f"\n  Engine: AI (gpt-5.6-luna)")
    else:
        print(f"\n  Engine: FALLBACK (rule-based)")

    print(f"  Case: {case.id}")
    print(f"  File: {filepath}")

    # Find active goal
    active_goals = case.active_goals()
    if not active_goals:
        print("\n  No active goals in this case.\n")
        return

    if len(active_goals) == 1:
        goal = active_goals[0]
    else:
        print(f"\n  Active goals:")
        for i, g in enumerate(active_goals, 1):
            print(f"    {i}. {g.desired_direction[:70]}")
        print()
        while True:
            choice = prompt("Which goal?")
            try:
                goal = active_goals[int(choice) - 1]
                break
            except (ValueError, IndexError):
                print(f"    Please enter 1-{len(active_goals)}.")

    print(f"\n  Goal: {goal.desired_direction}")

    # Find active mission for this goal
    active_missions = [m for m in case.missions
                       if m.goal_id == goal.id and m.status == MISSION_ACTIVE]

    if active_missions:
        mission = active_missions[0]
        separator("ACTIVE MISSION")
        show_mission(mission)

        # Ask for result
        separator("MISSION RESULT")

        # Show Definition of Done as a checklist
        if mission.definition_of_done:
            print("\n  Definition of Done:\n")
            for i, d in enumerate(mission.definition_of_done, 1):
                print(f"    {i}. {d}")
            print(f"\n  Mark items as done? (s = skip checklist)\n")
            first = prompt("Checklist? (y/s)")

            if first.lower() not in ("y", "yes"):
                print("  Skipping checklist.\n")
            else:
                done_items = []
                for i, d in enumerate(mission.definition_of_done, 1):
                    answer = prompt(f"  [{i}] Done? (y/n)")
                    done_items.append(answer.lower() in ("y", "yes"))

                completed_count = sum(done_items)
                total = len(mission.definition_of_done)
                print(f"\n  Progress: {completed_count}/{total} items done.\n")

                for i, (d, done) in enumerate(zip(mission.definition_of_done, done_items), 1):
                    mark = "[x]" if done else "[ ]"
                    print(f"    {mark} {d}")
                print()

        print("  What happened overall? (Leave empty to skip and get a new proposal)\n")
        result = prompt("Result")

        if result:
            observation_text = prompt("What did you observe or learn?")

            case.complete_mission(mission.id, result=result)
            if observation_text:
                case.add_observation(observation_text, mission_id=mission.id)
                case.update_situation(observation_text)
            else:
                case.update_situation(result)

            print(f"\n  Mission completed. Case updated.")

    else:
        print(f"\n  No active mission for this goal. Requesting a proposal.\n")

    # Get next proposal from Engine
    proposal = engine.propose(case, goal)
    show_proposal(proposal)

    # Ask for decision
    decision = get_decision()

    if decision is None:
        # Quit — save what we have
        case.save(directory="cases")
        print(f"\n  Saved. Come back later.\n")
        return

    case.record_decision(decision, goal_id=goal.id, context=proposal.suggestion)

    if decision == DECISION_ACCEPT:
        mission = case.add_mission(
            goal_id=goal.id,
            purpose=proposal.mission_purpose,
            description=proposal.mission_description,
            definition_of_done=proposal.definition_of_done,
            name=proposal.mission_name,
        )
        print(f"\n  ✓ ACCEPTED. Mission: {mission.name or mission.id}")

    elif decision == DECISION_MODIFY:
        print(f"\n  How would you modify it?\n")
        modification = prompt("Your version")
        if modification:
            mission = case.add_mission(
                goal_id=goal.id,
                purpose=proposal.mission_purpose,
                description=modification,
                definition_of_done=proposal.definition_of_done,
                name=proposal.mission_name,
            )
            print(f"\n  ✓ MODIFIED. Mission: {mission.name or mission.id}")

    elif decision == DECISION_REJECT:
        print(f"\n  Rejected. The goal remains active.\n")

    elif decision == DECISION_EXPLORE:
        print(f"\n  Exploring further. No commitment yet.\n")
        # Get another proposal
        proposal2 = engine.propose(case, goal)
        show_proposal(proposal2)

    elif decision == DECISION_GIVE_UP:
        reason = prompt("Reason (optional)")
        case.abandon_goal(goal.id, reason=reason)
        print(f"\n  Goal abandoned. Other goals remain unaffected.\n")

    # Save
    filepath = case.save(directory="cases")
    separator("SAVED")
    print(f"\n  Case saved to: {filepath}")
    print(f"  Run again: python continue_case.py {query}\n")


if __name__ == "__main__":
    main()
