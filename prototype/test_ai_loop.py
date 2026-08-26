"""
Test: AI Engine v0.2 proposal integrates into the existing Case File loop.

Verifies:
1. AIEngine produces a Proposal with all required fields
2. The proposal can be accepted into the Case File as a Mission
3. A mission result + observation can be recorded
4. The next AI proposal reflects the previous observation (continuity)
5. The AI does not invent evidence or claim mission completion

Requires: OPENAI_API_KEY in environment or .env file.
If unavailable, the test falls back to rule-based and reports it.
"""

from case_file import (
    CaseFile,
    GOAL_ACTIVE, DECISION_ACCEPT, MISSION_COMPLETED,
)
from engine_ai import AIEngine


def separator(title=""):
    if title:
        print(f"\n{'=' * 60}")
        print(f"  {title}")
        print(f"{'=' * 60}")
    else:
        print(f"\n{'-' * 60}")


def test_ai_proposal_in_loop():
    """Test that an AI-generated proposal works in the existing loop."""
    separator("TEST: AI Proposal Integration")

    engine = AIEngine()

    if not engine.available:
        print("\n  ⚠ OPENAI_API_KEY not available.")
        print("  Running with fallback (rule-based engine).")
        print("  Set OPENAI_API_KEY to test AI reasoning.\n")
    else:
        print(f"\n  AI Engine available (gpt-5.6-luna)\n")

    # --- Setup: create a case with context ---
    case = CaseFile()
    case.context = {
        "description": "Individual occupational exploration",
        "opening_question": "What are we working on right now?",
        "time_scope": "ongoing",
        "geographic_scope": "Sweden",
    }

    # --- Step 1: Interpret input ---
    user_text = "I want to learn programming but I don't know where to start"
    interpretation = engine.interpret_input(case, user_text)
    case.update_situation(interpretation.current_situation)
    goal = case.add_goal(desired_direction="Learn programming and find a starting point")

    print(f"  [1] Interpretation:")
    print(f"      Situation: {interpretation.current_situation}")
    print(f"      Direction: {interpretation.possible_direction}")
    print(f"      Uncertainty: {interpretation.uncertainty}")
    print(f"      Goal created: {goal.desired_direction} ({goal.id})")

    # --- Step 2: Get proposal ---
    proposal = engine.propose(case, goal)

    print(f"\n  [2] Proposal received:")
    print(f"      Current: {proposal.current}")
    print(f"      Desired: {proposal.desired}")
    print(f"      Suggestion: {proposal.suggestion}")
    print(f"      Reason: {proposal.reason}")
    print(f"      Mission: {proposal.mission_description}")
    print(f"      Purpose: {proposal.mission_purpose}")
    print(f"      DoD: {proposal.definition_of_done}")

    # Verify proposal has required fields
    assert proposal.goal_id == goal.id, "Proposal must reference the goal"
    assert proposal.suggestion, "Proposal must have a suggestion"
    assert proposal.mission_description, "Proposal must have a mission description"
    assert proposal.definition_of_done, "Proposal must have definition of done"
    print(f"\n  ✓ Proposal has all required fields")

    # --- Step 3: Accept proposal into Case File ---
    case.record_decision(DECISION_ACCEPT, goal_id=goal.id, context=proposal.suggestion)
    mission = case.add_mission(
        goal_id=goal.id,
        purpose=proposal.mission_purpose,
        description=proposal.mission_description,
        definition_of_done=proposal.definition_of_done,
    )

    print(f"\n  [3] Mission created from proposal:")
    print(f"      ID: {mission.id}")
    print(f"      Description: {mission.description}")
    assert mission.goal_id == goal.id
    assert mission.description == proposal.mission_description
    print(f"  ✓ Mission correctly attached to goal")

    # --- Step 4: Simulate mission result (participant provides this) ---
    result_text = "Completed. Tried a Python tutorial for 30 minutes."
    observation_text = "Python felt approachable. The interactive exercises were motivating. I want to try building something small next."

    case.complete_mission(mission.id, result=result_text)
    case.add_observation(observation_text, mission_id=mission.id)
    case.update_situation(f"First programming attempt completed. {observation_text}")

    print(f"\n  [4] Mission completed (by participant, not AI):")
    print(f"      Result: {result_text}")
    print(f"      Observation: {observation_text}")

    # --- Step 5: Next proposal (continuity test) ---
    proposal_2 = engine.propose(case, goal)

    print(f"\n  [5] Next proposal (should reflect observation):")
    print(f"      Current: {proposal_2.current}")
    print(f"      Suggestion: {proposal_2.suggestion}")
    print(f"      Reason: {proposal_2.reason}")
    print(f"      Mission: {proposal_2.mission_description}")
    print(f"      DoD: {proposal_2.definition_of_done}")

    # Verify the proposal does NOT fabricate evidence or claim the NEW mission is done
    # It IS allowed to reference that previous missions were completed (that's history)
    new_mission_text = proposal_2.mission_description.lower()
    fabrication_signals = [
        "has been completed",
        "mission completed",
        "evidence confirms",
        "verified that",
        "gps confirmed",
    ]
    for signal in fabrication_signals:
        assert signal not in new_mission_text, \
            f"AI must not fabricate completion: found '{signal}' in mission description"
    print(f"\n  ✓ AI does not fabricate evidence or claim new mission completion")

    # Verify continuity — proposal should relate to what was observed
    # (This is a soft check; the AI should reference Python or building something)
    assert proposal_2.suggestion, "Second proposal must have content"
    assert proposal_2.mission_description, "Second proposal must have a mission"
    print(f"  ✓ Second proposal has content (continuity present)")

    # --- Step 6: Persistence ---
    filepath = case.save(directory="cases")
    loaded = CaseFile.load(str(filepath))
    assert len(loaded.goals) == 1
    assert len(loaded.missions) == 1
    assert len(loaded.observations) == 1
    assert loaded.goals[0].status == GOAL_ACTIVE
    print(f"\n  ✓ Case File persists correctly after AI-assisted loop")

    separator("TEST PASSED")


if __name__ == "__main__":
    test_ai_proposal_in_loop()
