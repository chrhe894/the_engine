"""
Generic simulation runner.

Three layers:
  Scenario    = starting conditions (scenarios/*.json)
  Simulation  = repeatable participant responses (simulations/*.json)
  Case File   = accumulated state produced by the run (cases/*.json)

Usage:
    python run_simulation.py simulations/making-money.json
    python run_simulation.py simulations/skordefest.json

The runner:
1. Loads the scenario (context, opening question, initial input).
2. Sends initial input to the Engine → gets interpretation.
3. Shows interpretation to participant → participant confirms, corrects, or rejects.
4. Creates Goal from the confirmed/corrected direction.
5. Gets first proposal → ACCEPTs → creates Mission.
6. Feeds each simulation turn as a mission result/observation.
7. After each turn, asks the Engine for the next proposal.
8. Prints everything. Saves the final Case File.

The AI produces the proposals. The simulation provides the evidence.
We do not pre-write what the AI should conclude.

Simulation format:
  {
    "scenario": "scenarios/file.json",
    "description": "...",
    "interpretation_response": {              ← OPTIONAL
      "decision": "accept" | "modify" | "reject",
      "correction": "..."                     ← required if decision is "modify"
      "alternative": "..."                    ← required if decision is "reject"
    },
    "turns": [...]
  }

If interpretation_response is absent, the interpretation is accepted as-is
(backward compatible).
"""

import _bootstrap  # noqa: F401

import json
import sys
from pathlib import Path

from case_file import (
    CaseFile,
    DECISION_ACCEPT,
)
from engine_ai import AIEngine


def load_json(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def separator(title=""):
    if title:
        print(f"\n{'=' * 60}")
        print(f"  {title}")
        print(f"{'=' * 60}")
    else:
        print(f"\n{'-' * 60}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_simulation.py <simulation_file>")
        print("Example: python run_simulation.py simulations/making-money.json")
        sys.exit(1)

    # --- Load simulation and scenario ---
    sim_path = sys.argv[1]
    simulation = load_json(sim_path)
    scenario_path = simulation["scenario"]
    scenario = load_json(scenario_path)
    turns = simulation["turns"]

    separator(f"{scenario['name'].upper()} — SIMULATION")

    engine = AIEngine()
    if engine.available:
        print(f"\n  Engine: AI (gpt-5.6-luna)")
    else:
        print(f"\n  Engine: FALLBACK (rule-based)")

    print(f"  Scenario: {scenario_path}")
    print(f"  Simulation: {sim_path}")
    print(f"  Turns: {len(turns)}")

    # --- Setup case from scenario ---
    case = CaseFile()
    case.context = {
        "description": scenario["name"],
        "opening_question": scenario["opening_question"],
        "time_scope": scenario.get("time_scope", "ongoing"),
        "geographic_scope": scenario.get("geographic_scope"),
    }

    print(f"\n  Case ID: {case.id}")
    print(f"  Context: {case.context['description']}")
    print(f"  Time: {case.context['time_scope']}")
    print(f"  Geography: {case.context['geographic_scope']}")
    print(f"  Opening question: {case.context['opening_question']}")

    # ─────────────────────────────────────────────────────────────────
    # TURN 0: Initial input → interpretation → confirm → goal
    # ─────────────────────────────────────────────────────────────────
    separator("TURN 0: Initial Input")

    user_input = scenario["initial_input"]
    print(f"\n  Participant: \"{user_input}\"")

    interpretation = engine.interpret_input(case, user_input)
    case.update_situation(interpretation.current_situation)

    print(f"\n  Engine interpretation:")
    print(f"    Situation:   {interpretation.current_situation}")
    print(f"    Direction:   {interpretation.possible_direction}")
    print(f"    Uncertainty: {interpretation.uncertainty}")

    # ─────────────────────────────────────────────────────────────────
    # Interpret and confirm: participant decides on the direction
    # ─────────────────────────────────────────────────────────────────
    interpretation_response = simulation.get("interpretation_response")
    goal_direction = interpretation.possible_direction  # default: accept as-is

    if interpretation_response is None:
        # Backward compatible: no response means accept
        print(f"\n  [No interpretation_response in simulation — accepting as-is]")
    else:
        decision = interpretation_response.get("decision", "accept")
        separator("TURN 0: Interpretation Response")

        if decision == "accept":
            print(f"\n  Participant confirms: the interpretation is correct.")

        elif decision == "modify":
            correction = interpretation_response["correction"]
            print(f"\n  Participant corrects the direction:")
            print(f"    Engine suggested: {interpretation.possible_direction}")
            print(f"    Participant says: \"{correction}\"")
            goal_direction = correction

        elif decision == "reject":
            alternative = interpretation_response["alternative"]
            print(f"\n  Participant rejects the interpretation entirely:")
            print(f"    Engine suggested: {interpretation.possible_direction}")
            print(f"    Participant instead: \"{alternative}\"")
            goal_direction = alternative

        else:
            print(f"\n  [Unknown decision '{decision}' — accepting as-is]")

        print(f"\n  Goal direction will be: {goal_direction}")

    # Create goal from the confirmed/corrected direction
    goal = case.add_goal(desired_direction=goal_direction)
    print(f"\n  Goal created: {goal.desired_direction}")
    print(f"    ID: {goal.id}")

    # First proposal
    separator("TURN 0: First Proposal")
    proposal = engine.propose(case, goal)
    print(f"\n  Suggestion: {proposal.suggestion}")
    print(f"  Reason:     {proposal.reason}")
    print(f"  Mission:    {proposal.mission_description}")
    print(f"  Done when:  {proposal.definition_of_done}")

    # Accept and create mission
    case.record_decision(DECISION_ACCEPT, goal_id=goal.id, context=proposal.suggestion)
    mission = case.add_mission(
        goal_id=goal.id,
        purpose=proposal.mission_purpose,
        description=proposal.mission_description,
        definition_of_done=proposal.definition_of_done,
        name=proposal.mission_name,
    )
    print(f"\n  → ACCEPTED. Mission: {mission.name or mission.id}")

    # ─────────────────────────────────────────────────────────────────
    # TURNS 1..N: Simulation provides results, Engine proposes next
    # ─────────────────────────────────────────────────────────────────
    for i, turn in enumerate(turns, 1):
        separator(f"TURN {i}: Participant Response")

        # Complete the current mission with simulated result
        result_text = turn["result"]
        observation_text = turn["observation"]

        print(f"\n  Result:      {result_text}")
        print(f"  Observation: {observation_text}")

        case.complete_mission(mission.id, result=result_text)
        case.add_observation(observation_text, mission_id=mission.id)
        case.update_situation(observation_text)

        # Engine proposes next step
        separator(f"TURN {i}: Engine Proposal")
        proposal = engine.propose(case, goal)

        print(f"\n  Current:    {proposal.current}")
        print(f"  Suggestion: {proposal.suggestion}")
        print(f"  Reason:     {proposal.reason}")
        print(f"  Mission:    {proposal.mission_description}")
        print(f"  Done when:  {proposal.definition_of_done}")

        # Accept and create next mission
        case.record_decision(DECISION_ACCEPT, goal_id=goal.id, context=proposal.suggestion)
        mission = case.add_mission(
            goal_id=goal.id,
            purpose=proposal.mission_purpose,
            description=proposal.mission_description,
            definition_of_done=proposal.definition_of_done,
            name=proposal.mission_name,
        )
        print(f"\n  → ACCEPTED. Mission: {mission.name or mission.id}")

    # ─────────────────────────────────────────────────────────────────
    # Final state
    # ─────────────────────────────────────────────────────────────────
    separator("FINAL CASE FILE STATE")

    print(f"\n  Case ID: {case.id}")
    print(f"  Situation: {case.current_situation}")
    print(f"\n  Goal: {goal.desired_direction} [{goal.status}]")
    print(f"\n  Missions ({len(case.missions)}):")
    for m in case.missions:
        print(f"    [{m.status:9}] {m.description[:80]}")

    print(f"\n  Observations ({len(case.observations)}):")
    for o in case.observations:
        print(f"    • {o.text}")

    print(f"\n  History events: {len(case.history)}")

    filepath = case.save(directory="cases")
    print(f"\n  Saved to: {filepath}")

    separator("SIMULATION COMPLETE")


if __name__ == "__main__":
    main()
