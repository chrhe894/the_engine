"""
Skördefesten case --- run through the v0.1 prototype.

This script exercises the prototype with the Skördefesten / Södra Öland
golden case, simulating the participant's decisions non-interactively.

It demonstrates the full loop:
    Context → Input → Interpretation → Proposal → Decision →
    Mission → Result/Observation → Updated Case → Next Proposal

And multiple goals with independent lifecycles.
"""

from case_file import (
    CaseFile,
    GOAL_ACTIVE, GOAL_ABANDONED,
    DECISION_ACCEPT, DECISION_MODIFY, DECISION_GIVE_UP,
)
from engine import Engine


def separator(title=""):
    if title:
        print(f"\n{'=' * 60}")
        print(f"  {title}")
        print(f"{'=' * 60}")
    else:
        print(f"\n{'-' * 60}")


def main():
    separator("SKÖRDEFESTEN / SÖDRA ÖLAND — GOLDEN CASE")

    engine = Engine()
    case = CaseFile()
    case.context = {
        "description": "Skördefesten / Södra Öland",
        "opening_question": "What would make Södra Öland an even better place to live, work and visit?",
        "time_scope": "2026-09 to 2026-10",
        "geographic_scope": "Södra Öland",
    }

    print(f"\n  Case ID: {case.id}")
    print(f"  Context: {case.context['description']}")
    print(f"  Time: {case.context['time_scope']}")
    print(f"  Geography: {case.context['geographic_scope']}")
    print(f"\n  Opening question: {case.context['opening_question']}")

    # ─────────────────────────────────────────────────────────────────
    # PHASE 1: Initial input
    # ─────────────────────────────────────────────────────────────────
    separator("PHASE 1: Initial Input")

    user_input = "We want more young people to become involved in the festival"
    print(f"\n  Participant: \"{user_input}\"")

    interpretation = engine.interpret_input(case, user_input)
    case.update_situation(interpretation.current_situation)

    print(f"\n  Engine interpretation:")
    print(f"    Situation:   {interpretation.current_situation}")
    print(f"    Direction:   {interpretation.possible_direction}")
    print(f"    Uncertainty: {interpretation.uncertainty}")

    # Create first goal
    goal_youth = case.add_goal(desired_direction="Increase meaningful youth participation in the festival")
    print(f"\n  Goal created: {goal_youth.desired_direction}")
    print(f"    ID: {goal_youth.id}")
    print(f"    Status: {goal_youth.status}")

    # ─────────────────────────────────────────────────────────────────
    # PHASE 2: First proposal
    # ─────────────────────────────────────────────────────────────────
    separator("PHASE 2: First Proposal")

    proposal_1 = engine.propose(case, goal_youth)
    print(f"\n  ENGINE PROPOSAL:")
    print(f"    Current:    {proposal_1.current}")
    print(f"    Desired:    {proposal_1.desired}")
    print(f"    Suggestion: {proposal_1.suggestion}")
    print(f"    Reason:     {proposal_1.reason}")
    print(f"    Mission:    {proposal_1.mission_description}")
    print(f"    Done when:  {proposal_1.definition_of_done}")

    # ─────────────────────────────────────────────────────────────────
    # PHASE 3: Decision — MODIFY
    # ─────────────────────────────────────────────────────────────────
    separator("PHASE 3: Decision — MODIFY")

    print(f"\n  Participant decides: MODIFY")
    print(f"  Modification: \"Young people should help design the activity, not just participate.\"")

    case.record_decision(
        DECISION_MODIFY,
        goal_id=goal_youth.id,
        context=proposal_1.suggestion,
        reason="Young people should help design the activity, not just participate.",
    )

    # Update proposal with modification
    proposal_1.mission_description = "Co-design one small festival activity together with young people"
    proposal_1.mission_purpose = "Let young people shape the activity rather than only attend"
    proposal_1.definition_of_done = [
        "Young participants involved in design",
        "One pilot activity defined",
        "Pilot tested",
        "Observations recorded",
    ]

    print(f"\n  Updated proposal:")
    print(f"    Mission: {proposal_1.mission_description}")
    print(f"    Done when: {proposal_1.definition_of_done}")

    # ─────────────────────────────────────────────────────────────────
    # PHASE 4: Decision — ACCEPT modified proposal
    # ─────────────────────────────────────────────────────────────────
    separator("PHASE 4: Decision — ACCEPT")

    print(f"\n  Participant decides: ACCEPT")

    case.record_decision(
        DECISION_ACCEPT,
        goal_id=goal_youth.id,
        context=proposal_1.mission_description,
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
    # PHASE 5: Mission result and observation
    # ─────────────────────────────────────────────────────────────────
    separator("PHASE 5: Mission Result")

    print(f"\n  [Simulating: the pilot activity was run]")

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
    # PHASE 6: Next proposal (CONTINUITY TEST)
    # ─────────────────────────────────────────────────────────────────
    separator("PHASE 6: Next Proposal (Continuity Test)")

    proposal_2 = engine.propose(case, goal_youth)
    print(f"\n  ENGINE PROPOSAL (based on previous observation):")
    print(f"    Current:    {proposal_2.current}")
    print(f"    Desired:    {proposal_2.desired}")
    print(f"    Suggestion: {proposal_2.suggestion}")
    print(f"    Reason:     {proposal_2.reason}")
    print(f"    Mission:    {proposal_2.mission_description}")
    print(f"    Done when:  {proposal_2.definition_of_done}")

    # Verify continuity
    contains_obs = (
        "highly engaged" in proposal_2.suggestion or
        "highly engaged" in proposal_2.mission_description or
        observation_text[:30] in proposal_2.suggestion or
        observation_text[:30] in proposal_2.mission_description
    )
    print(f"\n  Continuity check: proposal references previous observation? {contains_obs}")

    # ─────────────────────────────────────────────────────────────────
    # PHASE 7: Add two more goals
    # ─────────────────────────────────────────────────────────────────
    separator("PHASE 7: Multiple Goals")

    goal_business = case.add_goal(desired_direction="Strengthen cooperation between local businesses during the festival")
    goal_transport = case.add_goal(desired_direction="Improve evening transport options for visitors")

    print(f"\n  Three goals now active:")
    for g in case.goals:
        print(f"    [{g.status}] {g.desired_direction} (id: {g.id})")

    # ─────────────────────────────────────────────────────────────────
    # PHASE 8: GIVE UP on transport goal
    # ─────────────────────────────────────────────────────────────────
    separator("PHASE 8: GIVE UP on transport goal")

    print(f"\n  Participant decides: GIVE UP on \"{goal_transport.desired_direction}\"")
    print(f"  Reason: \"Municipality won't fund evening buses this year.\"")

    case.record_decision(
        DECISION_GIVE_UP,
        goal_id=goal_transport.id,
        context="Improve evening transport options for visitors",
        reason="Municipality won't fund evening buses this year.",
    )

    # Reassessment
    reassessment = engine.propose_after_give_up(case, goal_transport)
    print(f"\n  Engine reassessment:")
    print(f"    Message: {reassessment['message']}")
    print(f"    Question: {reassessment['question']}")
    for opt in reassessment['options']:
        print(f"      • {opt['label']}")

    # Participant chooses: done
    print(f"\n  Participant chooses: \"I'm done.\"")
    case.abandon_goal(goal_transport.id, reason="Municipality won't fund evening buses this year.")

    # ─────────────────────────────────────────────────────────────────
    # PHASE 9: Verify goal independence
    # ─────────────────────────────────────────────────────────────────
    separator("PHASE 9: Verify Goal Independence")

    print(f"\n  All goals:")
    for g in case.goals:
        marker = {"ACTIVE": "●", "COMPLETED": "✓", "ABANDONED": "✗"}[g.status]
        print(f"    {marker} [{g.status}] {g.desired_direction}")

    print(f"\n  Active goals: {len(case.active_goals())}")
    assert goal_youth.status == GOAL_ACTIVE
    assert goal_business.status == GOAL_ACTIVE
    assert goal_transport.status == GOAL_ABANDONED
    print(f"  Youth goal: {goal_youth.status} ✓")
    print(f"  Business goal: {goal_business.status} ✓")
    print(f"  Transport goal: {goal_transport.status} ✓")

    # Youth goal history is intact
    youth_missions = [m for m in case.missions if m.goal_id == goal_youth.id]
    youth_observations = [o for o in case.observations if o.mission_id in [m.id for m in youth_missions]]
    print(f"\n  Youth goal history:")
    print(f"    Missions: {len(youth_missions)}")
    print(f"    Observations: {len(youth_observations)}")
    print(f"    Latest observation: {youth_observations[-1].text[:80]}...")

    # Business goal can still receive proposals
    proposal_biz = engine.propose(case, goal_business)
    print(f"\n  Business goal can still get proposals:")
    print(f"    Suggestion: {proposal_biz.suggestion}")

    # ─────────────────────────────────────────────────────────────────
    # PHASE 10: Final case summary
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
        print(f"    [{d.decision_type}] {d.context[:60]}")

    print(f"\n  History events: {len(case.history)}")

    # Save
    filepath = case.save(directory="cases")
    print(f"\n  Saved to: {filepath}")

    separator("SKÖRDEFESTEN CASE COMPLETE")


if __name__ == "__main__":
    main()
