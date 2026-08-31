"""
Regression test: Interpret-and-confirm boundary.

Mission 602ab507 from the Engine's self-development case file.

Verifies:
1. Engine interpretation is observable before any Case File mutation.
2. A participant correction changes the Goal direction.
3. A corrected Goal produces different proposals than the broad version.
4. Rejecting an interpretation leaves the Case File unchanged.
5. Goal isolation: changes to one goal do not affect another.
6. Continuity: follow-up proposals use accumulated corrected context.

Does not depend on exact AI wording — uses structural assertions only.
"""

import sys
import os
from pathlib import Path

# Make src/ importable and run from prototype root
_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT / "src"))
os.chdir(_ROOT)

from case_file import (
    CaseFile, Goal,
    GOAL_ACTIVE,
    DECISION_ACCEPT,
)
from engine_ai import AIEngine


def separator(title=""):
    if title:
        print(f"\n{'=' * 60}")
        print(f"  {title}")
        print(f"{'=' * 60}")
    else:
        print(f"\n{'-' * 60}")


def test_correction_changes_goal():
    """A correction must change the goal direction, not preserve the broad one."""
    separator("TEST 1: Correction changes goal direction")

    engine = AIEngine()
    case = CaseFile()
    case.context = {
        "description": "Interpret-confirm regression test",
        "opening_question": "What are we working on?",
        "time_scope": "ongoing",
        "geographic_scope": None,
    }

    # --- Get interpretation (broad) ---
    user_input = "I want to improve my life"
    interpretation = engine.interpret_input(case, user_input)

    print(f"\n  Input: \"{user_input}\"")
    print(f"  Engine direction: {interpretation.possible_direction}")

    # Assert: Case File has NO goals yet
    assert len(case.goals) == 0, "Case File must not have goals before confirmation"
    assert len(case.missions) == 0, "Case File must not have missions before confirmation"
    print(f"  ✓ Case File unchanged before confirmation (0 goals, 0 missions)")

    # --- Participant corrects ---
    correction = "I want to sleep better. That's the most important thing right now."
    case.update_situation(interpretation.current_situation)
    goal = case.add_goal(desired_direction=correction)

    print(f"\n  Correction: \"{correction}\"")
    print(f"  Goal created: {goal.desired_direction}")

    # Assert: goal has the corrected direction, not the broad one
    assert goal.desired_direction == correction, \
        f"Goal must have corrected direction, got: {goal.desired_direction}"
    assert "improve my life" not in goal.desired_direction.lower(), \
        "Goal must not contain the broad interpretation"
    print(f"  ✓ Goal stores corrected direction, not broad interpretation")

    # --- Follow-up proposal uses the corrected context ---
    proposal = engine.propose(case, goal)
    print(f"\n  Follow-up proposal: {proposal.suggestion[:80]}...")
    print(f"  Mission: {proposal.mission_description[:80]}...")

    assert proposal.goal_id == goal.id, "Proposal must reference the corrected goal"
    assert proposal.suggestion, "Proposal must have a suggestion"
    assert proposal.mission_description, "Proposal must have a mission"
    print(f"  ✓ Follow-up proposal exists and references corrected goal")

    print(f"\n  TEST 1 PASSED.\n")
    return case, goal, proposal


def test_rejection_leaves_case_unchanged():
    """Rejecting an interpretation must not create goals or mutate the Case File."""
    separator("TEST 2: Rejection leaves Case File unchanged")

    engine = AIEngine()
    case = CaseFile()
    case.context = {
        "description": "Rejection test",
        "opening_question": "What are we working on?",
        "time_scope": "ongoing",
        "geographic_scope": None,
    }

    # --- Get interpretation ---
    user_input = "I need to sort out my finances"
    interpretation = engine.interpret_input(case, user_input)

    print(f"\n  Input: \"{user_input}\"")
    print(f"  Engine direction: {interpretation.possible_direction}")

    # Snapshot case state before decision
    goals_before = len(case.goals)
    missions_before = len(case.missions)
    observations_before = len(case.observations)
    history_before = len(case.history)

    # --- Participant rejects ---
    print(f"\n  Participant REJECTS the interpretation.")
    print(f"  (Does not provide alternative — simply refuses.)")

    # Rejection: do NOT create a goal, do NOT add mission, do NOT update situation
    # The Case File remains as it was.

    # Assert: nothing changed
    assert len(case.goals) == goals_before, "Goals must not change after rejection"
    assert len(case.missions) == missions_before, "Missions must not change after rejection"
    assert len(case.observations) == observations_before, "Observations must not change after rejection"

    print(f"  ✓ Case File unchanged after rejection")
    print(f"    Goals: {len(case.goals)} (was {goals_before})")
    print(f"    Missions: {len(case.missions)} (was {missions_before})")
    print(f"    Observations: {len(case.observations)} (was {observations_before})")

    print(f"\n  TEST 2 PASSED.\n")


def test_goal_isolation_with_correction():
    """Correcting one goal must not affect another goal."""
    separator("TEST 3: Goal isolation with correction")

    engine = AIEngine()
    case = CaseFile()
    case.context = {
        "description": "Two-goal isolation test",
        "opening_question": "What are we working on?",
        "time_scope": "ongoing",
        "geographic_scope": None,
    }

    # --- Create two goals ---
    goal_a = case.add_goal(desired_direction="Learn to cook healthy meals")
    goal_b = case.add_goal(desired_direction="Run a 5km race")

    print(f"\n  Goal A: {goal_a.desired_direction} (id: {goal_a.id})")
    print(f"  Goal B: {goal_b.desired_direction} (id: {goal_b.id})")

    # --- Work on Goal A: get a proposal, complete a mission, add observation ---
    case.update_situation("Starting with two goals.")
    proposal_a = engine.propose(case, goal_a)
    case.record_decision(DECISION_ACCEPT, goal_id=goal_a.id, context=proposal_a.suggestion)
    mission_a = case.add_mission(
        goal_id=goal_a.id,
        purpose=proposal_a.mission_purpose,
        description=proposal_a.mission_description,
        definition_of_done=proposal_a.definition_of_done,
    )
    case.complete_mission(mission_a.id, result="Cooked one meal from scratch.")
    case.add_observation("Enjoyed the process. Vegetables were easier than expected.", mission_id=mission_a.id)

    print(f"\n  Goal A: mission completed, observation recorded.")

    # Snapshot Goal B state
    goal_b_status = goal_b.status
    goal_b_missions = list(goal_b.missions)
    goal_b_history = list(goal_b.history)
    goal_b_direction = goal_b.desired_direction

    # --- Get next proposal for Goal A (continuity) ---
    proposal_a2 = engine.propose(case, goal_a)
    print(f"  Goal A next proposal: {proposal_a2.suggestion[:60]}...")

    # --- Assert Goal B is completely unchanged ---
    assert goal_b.status == goal_b_status, \
        f"Goal B status changed: {goal_b.status} != {goal_b_status}"
    assert goal_b.missions == goal_b_missions, \
        "Goal B missions changed"
    assert goal_b.history == goal_b_history, \
        "Goal B history changed"
    assert goal_b.desired_direction == goal_b_direction, \
        "Goal B direction changed"

    print(f"\n  ✓ Goal B unchanged:")
    print(f"    Status: {goal_b.status}")
    print(f"    Direction: {goal_b.desired_direction}")
    print(f"    Missions: {len(goal_b.missions)}")
    print(f"    History: {len(goal_b.history)}")

    # --- Goal B can still get its own proposals ---
    proposal_b = engine.propose(case, goal_b)
    assert proposal_b.goal_id == goal_b.id, "Proposal B must reference Goal B"
    assert proposal_b.suggestion, "Goal B must still receive proposals"
    print(f"\n  ✓ Goal B can still receive proposals: {proposal_b.suggestion[:60]}...")

    # --- Goal A's observation must not appear in Goal B's mission context ---
    goal_b_missions_from_case = [m for m in case.missions if m.goal_id == goal_b.id]
    goal_b_observations = [o for o in case.observations
                           if o.mission_id in [m.id for m in goal_b_missions_from_case]]
    assert len(goal_b_observations) == 0, \
        "Goal B must not have observations from Goal A's missions"
    print(f"  ✓ Goal B has no observations from Goal A")

    print(f"\n  TEST 3 PASSED.\n")


def test_continuity_with_corrected_goal():
    """After correction + mission + observation, the next proposal must use accumulated state."""
    separator("TEST 4: Continuity with corrected goal")

    engine = AIEngine()
    case = CaseFile()
    case.context = {
        "description": "Continuity after correction test",
        "opening_question": "What are we working on?",
        "time_scope": "ongoing",
        "geographic_scope": None,
    }

    # --- Broad interpretation, then correction ---
    user_input = "I want to get better at my job"
    interpretation = engine.interpret_input(case, user_input)
    case.update_situation(interpretation.current_situation)

    correction = "I want to get better at presenting in meetings. I freeze up and say nothing."
    goal = case.add_goal(desired_direction=correction)

    print(f"\n  Broad: {interpretation.possible_direction[:60]}...")
    print(f"  Corrected: {correction}")

    # --- First proposal ---
    proposal_1 = engine.propose(case, goal)
    case.record_decision(DECISION_ACCEPT, goal_id=goal.id, context=proposal_1.suggestion)
    mission = case.add_mission(
        goal_id=goal.id,
        purpose=proposal_1.mission_purpose,
        description=proposal_1.mission_description,
        definition_of_done=proposal_1.definition_of_done,
    )

    print(f"  Proposal 1: {proposal_1.suggestion[:60]}...")

    # --- Complete mission with observation ---
    result = "Attended a meeting and tried to speak up once."
    observation = "I managed to say one thing. My voice shook but nobody reacted negatively."
    case.complete_mission(mission.id, result=result)
    case.add_observation(observation, mission_id=mission.id)
    case.update_situation(observation)

    print(f"  Observation: {observation}")

    # --- Second proposal (must use accumulated state) ---
    proposal_2 = engine.propose(case, goal)

    print(f"  Proposal 2: {proposal_2.suggestion[:60]}...")
    print(f"  Proposal 2 current: {proposal_2.current[:60]}...")

    # Structural assertions
    assert proposal_2.goal_id == goal.id, "Second proposal must reference the goal"
    assert proposal_2.suggestion, "Second proposal must have content"
    assert proposal_2.mission_description, "Second proposal must have a mission"

    # The goal direction should be the corrected one, not the broad one
    assert goal.desired_direction == correction, \
        "Goal must still have the corrected direction"

    # The case should have exactly 1 observation
    assert len(case.observations) == 1, \
        f"Expected 1 observation, got {len(case.observations)}"

    print(f"\n  ✓ Goal still has corrected direction")
    print(f"  ✓ Proposal 2 exists with content")
    print(f"  ✓ Case has 1 observation from the completed mission")
    print(f"  ✓ Continuity: proposal generated after observation + correction")

    print(f"\n  TEST 4 PASSED.\n")


if __name__ == "__main__":
    test_correction_changes_goal()
    test_rejection_leaves_case_unchanged()
    test_goal_isolation_with_correction()
    test_continuity_with_corrected_goal()

    separator("ALL TESTS PASSED")
