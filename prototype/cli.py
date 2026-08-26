"""
CLI --- v0.1 Prototype

Interactive loop for testing the adaptive navigation engine.

Usage:
    python cli.py           -- start a new case
    python cli.py <file>    -- resume from a saved case file

The loop:
    Open case → user input → proposal → decision → mission →
    observation → case update → next proposal
"""

import sys
from pathlib import Path

from case_file import (
    CaseFile,
    GOAL_ACTIVE, GOAL_ABANDONED, GOAL_COMPLETED,
    DECISION_ACCEPT, DECISION_MODIFY, DECISION_REJECT,
    DECISION_EXPLORE, DECISION_GIVE_UP,
    MISSION_ACTIVE, MISSION_COMPLETED,
)
from engine import Engine, Proposal


# --- Display helpers ---

def banner(text: str):
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}\n")


def section(text: str):
    print(f"\n--- {text} ---\n")


def show_proposal(proposal: Proposal):
    section("ENGINE PROPOSAL")
    print(f"  Current:    {proposal.current}")
    print(f"  Desired:    {proposal.desired}")
    print()
    print(f"  Suggestion: {proposal.suggestion}")
    print(f"  Reason:     {proposal.reason}")
    print()
    if proposal.mission_description:
        print(f"  Mission:    {proposal.mission_description}")
    if proposal.definition_of_done:
        print(f"  Done when:  {', '.join(proposal.definition_of_done)}")
    print()


def show_case_summary(case: CaseFile):
    section("CASE FILE SUMMARY")
    print(f"  Case ID:    {case.id}")
    print(f"  Situation:  {case.current_situation or '(not yet described)'}")
    print()
    if case.goals:
        print("  Goals:")
        for g in case.goals:
            marker = {"ACTIVE": "●", "COMPLETED": "✓", "ABANDONED": "✗"}
            print(f"    {marker.get(g.status, '?')} [{g.status}] {g.desired_direction}  (id: {g.id})")
        print()
    if case.missions:
        active_missions = [m for m in case.missions if m.status == MISSION_ACTIVE]
        if active_missions:
            print("  Active missions:")
            for m in active_missions:
                print(f"    → {m.description}  (id: {m.id})")
            print()
    if case.observations:
        recent = case.observations[-3:]  # show last 3
        print(f"  Recent observations ({len(case.observations)} total):")
        for o in recent:
            print(f"    • {o.text}")
        print()


def prompt(text: str) -> str:
    """Get user input with a prompt."""
    try:
        return input(f"  {text}> ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n\n  Goodbye.\n")
        sys.exit(0)


def choose(options: list, prompt_text: str = "Choose") -> str:
    """Present numbered options and get a choice."""
    for i, opt in enumerate(options, 1):
        if isinstance(opt, dict):
            print(f"    {i}. {opt.get('label', opt.get('id', '?'))}")
        else:
            print(f"    {i}. {opt}")
    print()
    while True:
        choice = prompt(prompt_text)
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return options[idx] if not isinstance(options[idx], dict) else options[idx]["id"]
        except ValueError:
            pass
        print(f"    Please enter a number 1-{len(options)}.")


# --- Main loop phases ---

def phase_open_case(filepath: str = None) -> CaseFile:
    """Open or create a Case File."""
    if filepath and Path(filepath).exists():
        case = CaseFile.load(filepath)
        banner("RESUMING CASE")
        show_case_summary(case)
        return case

    banner("NEW CASE")
    case = CaseFile()
    print(f"  Case created: {case.id}\n")
    return case


def phase_initial_input(case: CaseFile, engine: Engine):
    """Get the initial user input and establish context."""
    question = case.context.get("opening_question", "What are we working on right now?")
    print(f"  {question}\n")
    user_text = prompt("Your answer")

    if not user_text:
        return

    # Engine interprets
    interpretation = engine.interpret_input(case, user_text)
    case.update_situation(interpretation.current_situation)

    section("ENGINE INTERPRETATION")
    print(f"  Situation:  {interpretation.current_situation}")
    print(f"  Direction:  {interpretation.possible_direction}")
    print(f"  Uncertainty: {interpretation.uncertainty}")
    print()

    # Create a goal from the input
    print("  Creating a goal from your description.\n")
    goal = case.add_goal(desired_direction=user_text)
    print(f"  Goal created: {goal.desired_direction} (id: {goal.id})\n")


def phase_add_goal(case: CaseFile):
    """Add another goal to the case."""
    section("ADD GOAL")
    direction = prompt("What direction or desired change?")
    if direction:
        goal = case.add_goal(desired_direction=direction)
        print(f"\n  Goal added: {goal.desired_direction} (id: {goal.id})\n")


def phase_proposal(case: CaseFile, engine: Engine, goal=None):
    """Get a proposal from the engine for a goal."""
    if goal is None:
        active = case.active_goals()
        if not active:
            print("  No active goals.\n")
            return None
        if len(active) == 1:
            goal = active[0]
        else:
            print("  Which goal?\n")
            choice_idx = choose(
                [f"{g.desired_direction} (id: {g.id})" for g in active],
                "Choose goal"
            )
            # Parse the choice back (choose returns the string)
            idx = [f"{g.desired_direction} (id: {g.id})" for g in active].index(choice_idx)
            goal = active[idx]

    proposal = engine.propose(case, goal)
    show_proposal(proposal)
    return proposal


def phase_decision(case: CaseFile, engine: Engine, proposal: Proposal):
    """Handle the user's decision on a proposal."""
    print("  What do you decide?\n")
    options = [
        DECISION_ACCEPT,
        DECISION_MODIFY,
        DECISION_REJECT,
        DECISION_EXPLORE,
        DECISION_GIVE_UP,
    ]
    decision = choose(options, "Decision")

    case.record_decision(
        decision_type=decision,
        goal_id=proposal.goal_id,
        context=proposal.suggestion,
    )

    if decision == DECISION_ACCEPT:
        return handle_accept(case, proposal)
    elif decision == DECISION_MODIFY:
        return handle_modify(case, engine, proposal)
    elif decision == DECISION_REJECT:
        return handle_reject(case, proposal)
    elif decision == DECISION_EXPLORE:
        return handle_explore(case, engine, proposal)
    elif decision == DECISION_GIVE_UP:
        return handle_give_up(case, engine, proposal)


def handle_accept(case: CaseFile, proposal: Proposal):
    """ACCEPT: create a mission from the proposal."""
    section("ACCEPTED")
    mission = case.add_mission(
        goal_id=proposal.goal_id,
        purpose=proposal.mission_purpose,
        description=proposal.mission_description,
        definition_of_done=proposal.definition_of_done,
    )
    print(f"  Mission created: {mission.description}")
    print(f"  Done when: {', '.join(mission.definition_of_done)}")
    print(f"  Mission ID: {mission.id}\n")
    return mission


def handle_modify(case: CaseFile, engine: Engine, proposal: Proposal):
    """MODIFY: let the user alter the proposal."""
    section("MODIFY")
    print(f"  Current suggestion: {proposal.suggestion}\n")
    modification = prompt("How would you change it?")
    if modification:
        # Update the proposal with the modification
        proposal.mission_description = modification
        proposal.suggestion = modification
        print(f"\n  Updated proposal: {modification}\n")
        # Now ask if they accept the modified version
        print("  Accept the modified version?\n")
        accept = prompt("y/n")
        if accept.lower() in ("y", "yes"):
            return handle_accept(case, proposal)
    return None


def handle_reject(case: CaseFile, proposal: Proposal):
    """REJECT: discard this proposal. Goal remains."""
    section("REJECTED")
    print("  Proposal rejected. The goal remains active.\n")
    return None


def handle_explore(case: CaseFile, engine: Engine, proposal: Proposal):
    """EXPLORE FURTHER: get more exploration without committing."""
    section("EXPLORING FURTHER")
    print("  Not committing yet. Let's explore more.\n")
    # Generate another proposal for the same goal
    goal = case.get_goal(proposal.goal_id)
    if goal:
        new_proposal = engine.propose(case, goal)
        show_proposal(new_proposal)
        return phase_decision(case, engine, new_proposal)
    return None


def handle_give_up(case: CaseFile, engine: Engine, proposal: Proposal):
    """GIVE UP: reassessment flow."""
    goal = case.get_goal(proposal.goal_id)
    if not goal:
        return None

    reassessment = engine.propose_after_give_up(case, goal)
    section("REASSESSMENT")
    print(f"  {reassessment['message']}\n")
    print(f"  {reassessment['question']}\n")

    choice = choose(reassessment["options"], "What is happening?")

    if choice == "done":
        case.abandon_goal(goal.id, reason="Participant chose to stop.")
        print(f"\n  Goal abandoned: {goal.desired_direction}\n")
        print("  Other goals remain unaffected.\n")
    elif choice == "change":
        print("\n  The goal stays. Let's find a different approach.\n")
        new_direction = prompt("What approach would work better?")
        if new_direction:
            case.add_observation(f"Previous approach rejected. New idea: {new_direction}", source="participant")
    elif choice == "uncertain":
        print("\n  That's okay. The goal stays open. We can return to it.\n")
    elif choice == "challenge":
        section("CHALLENGE")
        challenge = engine.propose_challenge(case, goal)
        show_proposal(challenge)
        return phase_decision(case, engine, challenge)

    return None


def phase_mission_result(case: CaseFile):
    """Record a mission result and observation."""
    active_missions = [m for m in case.missions if m.status == MISSION_ACTIVE]
    if not active_missions:
        print("  No active missions.\n")
        return

    section("MISSION RESULT")
    if len(active_missions) == 1:
        mission = active_missions[0]
    else:
        print("  Which mission?\n")
        choice = choose(
            [f"{m.description} (id: {m.id})" for m in active_missions],
            "Choose mission"
        )
        idx = [f"{m.description} (id: {m.id})" for m in active_missions].index(choice)
        mission = active_missions[idx]

    print(f"  Mission: {mission.description}")
    print(f"  Done when: {', '.join(mission.definition_of_done)}\n")

    result = prompt("What happened? (result)")
    observation_text = prompt("What did you observe or learn?")

    if result:
        case.complete_mission(mission.id, result)
    if observation_text:
        case.add_observation(observation_text, mission_id=mission.id)
        # Update situation based on observation
        case.update_situation(
            f"{case.current_situation} Latest: {observation_text}"
            if case.current_situation else observation_text
        )

    print("\n  Mission completed. Case File updated.\n")


# --- Main command loop ---

def main_loop(case: CaseFile, engine: Engine):
    """The main interactive loop."""
    while True:
        section("WHAT WOULD YOU LIKE TO DO?")
        options = [
            "Get a proposal for a goal",
            "Record a mission result",
            "Add another goal",
            "View case summary",
            "Save and quit",
        ]
        action = choose(options, "Action")

        if action == options[0]:
            proposal = phase_proposal(case, engine)
            if proposal:
                phase_decision(case, engine, proposal)

        elif action == options[1]:
            phase_mission_result(case, engine)

        elif action == options[2]:
            phase_add_goal(case)

        elif action == options[3]:
            show_case_summary(case)

        elif action == options[4]:
            filepath = case.save(directory="cases")
            print(f"\n  Case saved to: {filepath}\n")
            print("  Goodbye.\n")
            break


def main():
    """Entry point."""
    filepath = sys.argv[1] if len(sys.argv) > 1 else None
    engine = Engine()

    case = phase_open_case(filepath)

    # If new case, do initial input
    if not case.goals:
        phase_initial_input(case, engine)

    # Enter main loop
    main_loop(case, engine)


if __name__ == "__main__":
    main()
