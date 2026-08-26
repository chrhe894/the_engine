"""
Engine --- v0.1 Prototype

The Engine interprets the current Case File and produces proposals.

This is a stub. It uses simple rules rather than AI.
The purpose is to test the loop, not the intelligence.

The Engine proposes. The user decides.
"""

from dataclasses import dataclass, field
from typing import Optional

from case_file import (
    CaseFile, Goal, Mission, Observation,
    GOAL_ACTIVE, MISSION_COMPLETED, MISSION_ACTIVE,
)


@dataclass
class Proposal:
    """A proposed next step from the Engine."""
    goal_id: str = ""
    current: str = ""  # description of current situation
    desired: str = ""  # description of desired direction
    suggestion: str = ""  # what the Engine proposes
    reason: str = ""  # why this is relevant
    mission_description: str = ""  # concrete next step if accepted
    mission_purpose: str = ""
    definition_of_done: list = field(default_factory=list)


@dataclass
class Interpretation:
    """The Engine's provisional understanding of user input."""
    current_situation: str = ""
    possible_direction: str = ""
    uncertainty: str = "high"  # high, medium, low


class Engine:
    """
    Stub Engine for v0.1.

    Produces proposals by reading Case File state.
    Uses simple heuristics, not AI.

    Replace internals later without changing the interface.
    """

    def interpret_input(self, case: CaseFile, user_text: str) -> Interpretation:
        """
        Produce a provisional interpretation of user input.
        This is an editable hypothesis, not a fact.
        """
        # Simple: echo back the user's words as the situation
        # A real engine would reason here
        return Interpretation(
            current_situation=f"The participant describes: {user_text}",
            possible_direction=user_text,
            uncertainty="high",
        )

    def propose(self, case: CaseFile, goal: Goal) -> Proposal:
        """
        Produce a proposal for the next step on a goal.

        The proposal uses Case File history to inform the suggestion.
        This is the continuity test: the proposal should reflect
        what has already happened.
        """
        # Gather what we know about this goal
        goal_missions = [m for m in case.missions if m.goal_id == goal.id]
        completed_missions = [m for m in goal_missions if m.status == MISSION_COMPLETED]
        goal_observations = [
            o for o in case.observations
            if o.mission_id in [m.id for m in goal_missions]
        ]

        # Build context from history
        current = self._describe_current(case, goal, completed_missions, goal_observations)
        suggestion, reason, mission_desc, mission_purpose, dod = self._generate_suggestion(
            case, goal, completed_missions, goal_observations
        )

        return Proposal(
            goal_id=goal.id,
            current=current,
            desired=goal.desired_direction,
            suggestion=suggestion,
            reason=reason,
            mission_description=mission_desc,
            mission_purpose=mission_purpose,
            definition_of_done=dod,
        )

    def propose_after_give_up(self, case: CaseFile, goal: Goal) -> dict:
        """
        When a participant gives up, offer reassessment options.
        Returns a reassessment structure.
        """
        return {
            "message": "It's never too late to give up.",
            "question": "What is happening?",
            "options": [
                {"id": "done", "label": "I'm done."},
                {"id": "change", "label": "The goal is still worth it, but this approach isn't."},
                {"id": "uncertain", "label": "I don't know anymore."},
                {"id": "challenge", "label": "Challenge me."},
            ],
        }

    def propose_challenge(self, case: CaseFile, goal: Goal) -> Proposal:
        """
        Produce a deliberately smaller proposal after GIVE UP + Challenge me.
        The idea: reduce scope to the smallest meaningful step.
        """
        return Proposal(
            goal_id=goal.id,
            current=case.current_situation,
            desired=goal.desired_direction,
            suggestion="Try the smallest possible version of this.",
            reason="Sometimes the scope is too large. A tiny step can reveal whether the direction is still meaningful.",
            mission_description=f"Spend 15 minutes on one small action related to: {goal.desired_direction}",
            mission_purpose="Test whether this direction is still worth pursuing at any scale.",
            definition_of_done=["15 minutes spent", "One observation recorded"],
        )

    # --- Internal helpers ---

    def _describe_current(self, case: CaseFile, goal: Goal,
                          completed_missions: list, observations: list) -> str:
        """Describe the current state relative to this goal."""
        if not completed_missions and not observations:
            return case.current_situation or "Starting point — no missions completed yet."

        parts = []
        if completed_missions:
            parts.append(f"{len(completed_missions)} mission(s) completed.")
        if observations:
            # Use the most recent observation
            latest = observations[-1]
            parts.append(f"Latest observation: {latest.text}")
        return " ".join(parts)

    def _generate_suggestion(self, case: CaseFile, goal: Goal,
                             completed_missions: list, observations: list):
        """
        Generate a suggestion based on what has happened.

        This is the core of the continuity test:
        the suggestion must reflect accumulated knowledge.
        """
        if not completed_missions:
            # First proposal for this goal — suggest exploration
            return (
                f"Explore what '{goal.desired_direction}' means concretely.",
                "No missions have been completed yet. A small exploration can reveal what the next useful step might be.",
                f"Take one small action to learn more about: {goal.desired_direction}",
                "Explore the direction before committing to a larger transition.",
                ["One concrete action taken", "One observation recorded"],
            )

        # We have history — build on it
        latest_obs = observations[-1] if observations else None

        if latest_obs:
            # The proposal reflects the latest observation
            return (
                f"Build on what was discovered: '{latest_obs.text}'",
                f"The previous mission revealed new information. The next step should use that knowledge.",
                f"Based on the observation that '{latest_obs.text}', take one next step that moves closer to: {goal.desired_direction}",
                "Use what was learned to make progress.",
                ["One step taken that builds on previous observation", "Result recorded"],
            )

        # Completed missions but no observations recorded
        return (
            f"Continue exploring: {goal.desired_direction}",
            f"{len(completed_missions)} mission(s) have been completed. Continue the exploration.",
            f"Take another step toward: {goal.desired_direction}",
            "Continue making progress.",
            ["One action completed", "One observation recorded"],
        )
