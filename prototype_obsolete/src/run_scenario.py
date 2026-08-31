"""
Run a scenario through the Engine v0.2 (AI-assisted).

Usage:
    python run_scenario.py                          # default: scenarios/skordefest.json
    python run_scenario.py scenarios/income.json    # any scenario file

Requires: OPENAI_API_KEY in environment or .env file.
Falls back to rule-based engine if unavailable.
"""

import _bootstrap  # noqa: F401

import json
import sys
from pathlib import Path

from case_file import (
    CaseFile,
    GOAL_ACTIVE, GOAL_ABANDONED,
    DECISION_ACCEPT, DECISION_MODIFY, DECISION_GIVE_UP,
)
from engine_ai import AIEngine


# --- Scenario loading ---

DEFAULT_SCENARIO = Path(__file__).parent.parent / "scenarios" / "skordefest.json"


def load_scenario(filepath: str = None) -> dict:
    """Load scenario configuration from a JSON file."""
    path = Path(filepath) if filepath else DEFAULT_SCENARIO
    if not path.exists():
        print(f"  ERROR: Scenario file not found: {path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# --- Display helpers ---

def separator(title=""):
    if title:
        print(f"\n{'=' * 60}")
        print(f"  {title}")
        print(f"{'=' * 60}")
    else:
        print(f"\n{'-' * 60}")


def main():
    # Load scenario configuration
    scenario_path = sys.argv[1] if len(sys.argv) > 1 else None
    scenario = load_scenario(scenario_path)

    scenario_name = scenario["name"]
    separator(f"{scenario_name.upper()} v0.2 — AI-ASSISTED ENGINE")

    engine = AIEngine()

    if engine.available:
        print(f"\n  Engine: AI (gpt-5.6-luna)")
    else:
        print(f"\n  Engine: FALLBACK (rule-based, no API key)")
        print(f"  Set OPENAI_API_KEY to run with AI reasoning.")

    # ─────────────────────────────────────────────────────────────────
    # Setup: context from scenario configuration
    # ─────────────────────────────────────────────────────────────────
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
    # PHASE 1: Initial input from scenario configuration
    # ─────────────────────────────────────────────────────────────────
    separator("PHASE 1: Initial Input")

    user_input = scenario["initial_input"]
    print(f"\n  Participant: \"{user_input}\"")

    interpretation = engine.interpret_input(case, user_input)
    case.update_situation(interpretation.current_situation)

    print(f"\n  Engine interpretation:")
    print(f"    Situation:   {interpretation.current_situation}")
    print(f"    Direction:   {interpretation.possible_direction}")
    print(f"    Uncertainty: {interpretation.uncertainty}")

    goal_youth = case.add_goal(desired_direction="Increase meaningful youth participation in the festival")
    print(f"\n  Goal created: {goal_youth.desired_direction}")
    print(f"    ID: {goal_youth.id}")
    print(f"    Status: {goal_youth.status}")

    # ─────────────────────────────────────────────────────────────────
    # PHASE 2: First proposal
    # In v0.1 this was "Explore what X means concretely" — generic.
    # In v0.2 the AI should produce something more specific.
    # ─────────────────────────────────────────────────────────────────
    separator("PHASE 2: First Proposal (AI vs baseline)")

    proposal_1 = engine.propose(case, goal_youth)
    print(f"\n  ENGINE PROPOSAL:")
    print(f"    Current:    {proposal_1.current}")
    print(f"    Desired:    {proposal_1.desired}")
    print(f"    Suggestion: {proposal_1.suggestion}")
    print(f"    Reason:     {proposal_1.reason}")
    print(f"    Mission:    {proposal_1.mission_description}")
    print(f"    Purpose:    {proposal_1.mission_purpose}")
    print(f"    Done when:  {proposal_1.definition_of_done}")

    # ─────────────────────────────────────────────────────────────────
    # PHASE 3: Decision — ACCEPT directly
    # In v0.1 the participant had to MODIFY the generic proposal.
    # In v0.2 we test whether the AI proposal is good enough to accept
    # without modification. This is the A/B comparison point.
    # ─────────────────────────────────────────────────────────────────
    separator("PHASE 3: Decision — ACCEPT (no MODIFY needed?)")

    print(f"\n  [A/B COMPARISON POINT]")
    print(f"  v0.1 required MODIFY to make the proposal useful.")
    print(f"  v0.2 tests whether the AI proposal is directly acceptable.")
    print(f"\n  Participant decides: ACCEPT")

    case.record_decision(
        DECISION_ACCEPT,
        goal_id=goal_youth.id,
        context=proposal_1.suggestion,
    )

    mission_1 = case.add_mission(
        goal_id=goal_youth.id,
        purpose=proposal_1.mission_purpose,
        description=proposal_1.mission_description,
        definition_of_done=proposal_1.definition_of_done,
    )

    print(f"\n  Mission created:")
    print(f"    ID: {mission_1.id}")
    print(f"    Description: {mission_1.description}")
    print(f"    Purpose: {mission_1.purpose}")
    print(f"    Done when: {mission_1.definition_of_done}")

    # ─────────────────────────────────────────────────────────────────
    # PHASE 4: Mission result (same simulated result as v0.1)
    # The participant provides this — never the AI.
    # ─────────────────────────────────────────────────────────────────
    separator("PHASE 4: Mission Result (participant provides)")

    print(f"\n  [Simulating: the mission was executed]")

    result_text = "Pilot completed. Five young people co-designed a guided night walk combining local nature and storytelling."
    observation_text = "Young people were highly engaged when they had creative control. The proposed evening time worked well. Three participants said they would return for the festival."

    case.complete_mission(mission_1.id, result=result_text)
    obs = case.add_observation(observation_text, mission_id=mission_1.id)
    case.update_situation(
        "Youth participation pilot completed successfully. "
        "Young people responded well to creative ownership. "
        "Evening timing worked. Some would return for the festival."
    )

    print(f"\n  Result: {result_text}")
    print(f"\n  Observation: {observation_text}")
    print(f"\n  Updated situation: {case.current_situation}")

    # ─────────────────────────────────────────────────────────────────
    # PHASE 5: Next proposal (CONTINUITY TEST)
    # v0.1 quoted the observation verbatim.
    # v0.2 should reason about what it means and propose accordingly.
    # ─────────────────────────────────────────────────────────────────
    separator("PHASE 5: Next Proposal (Continuity — AI reasoning)")

    proposal_2 = engine.propose(case, goal_youth)
    print(f"\n  ENGINE PROPOSAL (after observation):")
    print(f"    Current:    {proposal_2.current}")
    print(f"    Desired:    {proposal_2.desired}")
    print(f"    Suggestion: {proposal_2.suggestion}")
    print(f"    Reason:     {proposal_2.reason}")
    print(f"    Mission:    {proposal_2.mission_description}")
    print(f"    Purpose:    {proposal_2.mission_purpose}")
    print(f"    Done when:  {proposal_2.definition_of_done}")

    # ─────────────────────────────────────────────────────────────────
    # PHASE 6: Add more goals + GIVE UP (same as v0.1)
    # ─────────────────────────────────────────────────────────────────
    separator("PHASE 6: Multiple Goals")

    goal_business = case.add_goal(desired_direction="Strengthen cooperation between local businesses during the festival")
    goal_transport = case.add_goal(desired_direction="Improve evening transport options for visitors")

    print(f"\n  Three goals now active:")
    for g in case.goals:
        print(f"    [{g.status}] {g.desired_direction} (id: {g.id})")

    # Get a proposal for the business goal (tests multi-goal context)
    separator("PHASE 6b: Proposal for business goal")

    proposal_biz = engine.propose(case, goal_business)
    print(f"\n  ENGINE PROPOSAL (business cooperation):")
    print(f"    Current:    {proposal_biz.current}")
    print(f"    Suggestion: {proposal_biz.suggestion}")
    print(f"    Reason:     {proposal_biz.reason}")
    print(f"    Mission:    {proposal_biz.mission_description}")
    print(f"    Done when:  {proposal_biz.definition_of_done}")

    # ─────────────────────────────────────────────────────────────────
    # PHASE 7: GIVE UP on transport goal (same as v0.1)
    # ─────────────────────────────────────────────────────────────────
    separator("PHASE 7: GIVE UP on transport goal")

    print(f"\n  Participant decides: GIVE UP on \"{goal_transport.desired_direction}\"")
    print(f"  Reason: \"Municipality won't fund evening buses this year.\"")

    case.record_decision(
        DECISION_GIVE_UP,
        goal_id=goal_transport.id,
        context="Improve evening transport options for visitors",
        reason="Municipality won't fund evening buses this year.",
    )

    reassessment = engine.propose_after_give_up(case, goal_transport)
    print(f"\n  Engine reassessment:")
    print(f"    Message: {reassessment['message']}")
    print(f"    Question: {reassessment['question']}")
    for opt in reassessment['options']:
        print(f"      • {opt['label']}")

    print(f"\n  Participant chooses: \"I'm done.\"")
    case.abandon_goal(goal_transport.id, reason="Municipality won't fund evening buses this year.")

    # ─────────────────────────────────────────────────────────────────
    # PHASE 8: Final state
    # ─────────────────────────────────────────────────────────────────
    separator("FINAL CASE FILE STATE")

    print(f"\n  Case ID: {case.id}")
    print(f"  Context: {case.context['description']}")
    print(f"  Situation: {case.current_situation}")
    print(f"\n  Goals ({len(case.goals)}):")
    for g in case.goals:
        marker = {"ACTIVE": "●", "COMPLETED": "✓", "ABANDONED": "✗"}[g.status]
        print(f"    {marker} [{g.status}] {g.desired_direction}")

    print(f"\n  Missions ({len(case.missions)}):")
    for m in case.missions:
        print(f"    [{m.status}] {m.description}")

    print(f"\n  Observations ({len(case.observations)}):")
    for o in case.observations:
        print(f"    • {o.text[:100]}")

    print(f"\n  Decisions ({len(case.decisions)}):")
    for d in case.decisions:
        line = f"    [{d.decision_type}] {d.context[:60]}"
        if d.reason:
            line += f" — {d.reason[:40]}"
        print(line)

    print(f"\n  History events: {len(case.history)}")

    # Save
    filepath = case.save(directory="cases")
    print(f"\n  Saved to: {filepath}")

    # ─────────────────────────────────────────────────────────────────
    # A/B COMPARISON SUMMARY
    # ─────────────────────────────────────────────────────────────────
    separator("A/B COMPARISON SUMMARY")

    print(f"""
  v0.1 (rule-based):
    First proposal: "Explore what X means concretely."
    Required MODIFY: Yes — participant had to rewrite the mission.
    Continuity: Quoted observation verbatim.
    Business goal: "Explore what X means concretely." (same template)

  v0.2 (AI-assisted):
    First proposal: {proposal_1.suggestion[:70]}...
    Required MODIFY: Not tested (accepted directly for comparison)
    Continuity: {proposal_2.suggestion[:70]}...
    Business goal: {proposal_biz.suggestion[:70]}...

  Goal independence: {"VERIFIED" if goal_youth.status == GOAL_ACTIVE and goal_transport.status == GOAL_ABANDONED else "FAILED"}
  AI fabrication check: Mission completion provided by participant only.
""")

    separator(f"{scenario_name.upper()} v0.2 COMPLETE")


if __name__ == "__main__":
    main()
