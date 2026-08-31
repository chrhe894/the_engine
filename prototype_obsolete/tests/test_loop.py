"""
Test script --- exercises the complete prototype loop non-interactively.

Run: python test_loop.py

This verifies:
1. Case File creation and persistence
2. Goal lifecycle (add, complete, abandon)
3. Engine proposal from context
4. Mission creation from accepted proposal
5. Observation recording
6. Continuity: next proposal reflects previous observation
7. Multiple goals coexist independently
8. GIVE UP on one goal does not affect others
"""

import sys
import os
from pathlib import Path

# Make src/ importable and run from prototype root
_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT / "src"))
os.chdir(_ROOT)

from case_file import (
    CaseFile,
    GOAL_ACTIVE, GOAL_ABANDONED, GOAL_COMPLETED,
    DECISION_ACCEPT, DECISION_GIVE_UP,
    MISSION_COMPLETED,
)
from engine import Engine


def test_complete_loop():
    """Test the full adaptive loop."""
    print("=" * 60)
    print("  TEST: Complete Loop")
    print("=" * 60)

    engine = Engine()
    case = CaseFile()

    # --- Step 1: User input and interpretation ---
    user_text = "I want to become a software developer"
    interpretation = engine.interpret_input(case, user_text)
    case.update_situation(interpretation.current_situation)
    goal = case.add_goal(desired_direction=user_text)

    print(f"\n  [1] Case created: {case.id}")
    print(f"      Goal: {goal.desired_direction} ({goal.id})")
    print(f"      Situation: {case.current_situation}")

    # --- Step 2: Engine proposal ---
    proposal = engine.propose(case, goal)
    print(f"\n  [2] Proposal: {proposal.suggestion}")
    print(f"      Mission: {proposal.mission_description}")
    print(f"      Reason: {proposal.reason}")

    # --- Step 3: Accept → Mission created ---
    case.record_decision(DECISION_ACCEPT, goal_id=goal.id, context=proposal.suggestion)
    mission = case.add_mission(
        goal_id=goal.id,
        purpose=proposal.mission_purpose,
        description=proposal.mission_description,
        definition_of_done=proposal.definition_of_done,
    )
    print(f"\n  [3] Mission created: {mission.description} ({mission.id})")

    # --- Step 4: Simulate result and observation ---
    case.complete_mission(mission.id, result="Completed the exploration")
    observation = case.add_observation(
        "Programming seems interesting. Python was approachable.",
        mission_id=mission.id,
    )
    case.update_situation(f"Interest confirmed. {observation.text}")

    print(f"\n  [4] Mission completed.")
    print(f"      Observation: {observation.text}")
    print(f"      Updated situation: {case.current_situation}")

    # --- Step 5: Next proposal (continuity test) ---
    proposal_2 = engine.propose(case, goal)
    print(f"\n  [5] Next proposal: {proposal_2.suggestion}")
    print(f"      Mission: {proposal_2.mission_description}")

    # CONTINUITY CHECK: proposal_2 should reference the observation
    assert "Programming seems interesting" in proposal_2.suggestion or \
           "Programming seems interesting" in proposal_2.mission_description, \
        "CONTINUITY FAILURE: Next proposal does not reflect previous observation!"

    print("\n  ✓ CONTINUITY VERIFIED: Next proposal reflects previous observation.")

    # --- Step 6: Persistence test ---
    filepath = case.save(directory="cases")
    loaded = CaseFile.load(str(filepath))
    assert loaded.id == case.id
    assert len(loaded.goals) == len(case.goals)
    assert len(loaded.missions) == len(case.missions)
    assert len(loaded.observations) == len(case.observations)
    print(f"\n  ✓ PERSISTENCE VERIFIED: Saved and loaded from {filepath}")

    print("\n  TEST PASSED.\n")


def test_multiple_goals_and_give_up():
    """Test that GIVE UP on one goal does not affect others."""
    print("=" * 60)
    print("  TEST: Multiple Goals + GIVE UP")
    print("=" * 60)

    engine = Engine()
    case = CaseFile()
    case.update_situation("Starting a multi-goal case.")

    # Add three goals
    goal_a = case.add_goal("Learn Swedish")
    goal_b = case.add_goal("Find housing in Linköping")
    goal_c = case.add_goal("Get a driver's license")

    print(f"\n  [1] Three goals created:")
    print(f"      A: {goal_a.desired_direction} [{goal_a.status}]")
    print(f"      B: {goal_b.desired_direction} [{goal_b.status}]")
    print(f"      C: {goal_c.desired_direction} [{goal_c.status}]")

    # Run a mission on Goal A
    proposal_a = engine.propose(case, goal_a)
    mission_a = case.add_mission(
        goal_id=goal_a.id,
        purpose=proposal_a.mission_purpose,
        description=proposal_a.mission_description,
        definition_of_done=proposal_a.definition_of_done,
    )
    case.complete_mission(mission_a.id, result="Attended first Swedish class")
    case.add_observation("Basic greetings learned. Motivated to continue.", mission_id=mission_a.id)

    print(f"\n  [2] Goal A: mission completed, observation recorded.")

    # GIVE UP on Goal C
    case.record_decision(DECISION_GIVE_UP, goal_id=goal_c.id, context="Too expensive right now")
    case.abandon_goal(goal_c.id, reason="Too expensive right now")

    print(f"\n  [3] GIVE UP on Goal C: {goal_c.desired_direction}")
    print(f"      Goal C status: {goal_c.status}")

    # Verify other goals survive
    assert goal_a.status == GOAL_ACTIVE, f"Goal A should be ACTIVE, got {goal_a.status}"
    assert goal_b.status == GOAL_ACTIVE, f"Goal B should be ACTIVE, got {goal_b.status}"
    assert goal_c.status == GOAL_ABANDONED, f"Goal C should be ABANDONED, got {goal_c.status}"

    print(f"\n  [4] Verification:")
    print(f"      Goal A: {goal_a.status} ✓")
    print(f"      Goal B: {goal_b.status} ✓")
    print(f"      Goal C: {goal_c.status} ✓")

    # Verify Goal A's history is intact
    assert len([m for m in case.missions if m.goal_id == goal_a.id]) == 1
    assert len([o for o in case.observations if o.mission_id == mission_a.id]) == 1
    print(f"      Goal A history intact ✓")

    # Goal B can still receive proposals
    proposal_b = engine.propose(case, goal_b)
    assert proposal_b.goal_id == goal_b.id
    print(f"      Goal B can still receive proposals ✓")

    # Active goals should only include A and B
    active = case.active_goals()
    assert len(active) == 2
    print(f"      Active goals: {len(active)} (A and B) ✓")

    # Case File history records everything
    give_up_events = [h for h in case.history if h["event"] == "goal_abandoned"]
    assert len(give_up_events) == 1
    print(f"      GIVE UP recorded in history ✓")

    print("\n  TEST PASSED.\n")


if __name__ == "__main__":
    test_complete_loop()
    test_multiple_goals_and_give_up()
    print("=" * 60)
    print("  ALL TESTS PASSED")
    print("=" * 60)
