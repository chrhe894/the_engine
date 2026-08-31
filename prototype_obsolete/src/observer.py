"""
Observer --- Model v1.0

Implements the Observer layer from
docs/observer-characters-humour-model-spec-v0.1.md

The Observer notices things about the Engine's reasoning and trajectory,
and may introduce an unexpected perspective (a "character") to help the
participant see something they could not see from their current position.

Core principle:
    The Engine proposes. The Observer notices and challenges.
    The participant decides. Reality answers.

The Observer NEVER changes the Case File. It produces observations and
interventions. The participant decides whether they matter.
"""

import json
import random
from dataclasses import dataclass, field
from typing import Optional

from case_file import CaseFile, Goal


# --- Character library ---
# Characters are presentation/reasoning perspectives, not separate AIs.
# This is the starting set. More can be added later, ideally data-driven.

CHARACTERS = {
    "skeptic": {
        "name": "The Skeptic",
        "prompt": "Question the assumptions in this proposal. What is being treated as certain that is actually uncertain? Be sharp but fair.",
    },
    "contrarian": {
        "name": "The Contrarian",
        "prompt": "Explore the opposite interpretation. What if the participant wants the reverse of what the trajectory assumes? Argue the other side.",
    },
    "accountant": {
        "name": "The Accountant",
        "prompt": "Insist on observable completion and manageable scope. Is this mission too big or too vague to actually finish? What would 'done' really look like?",
    },
    "gardener": {
        "name": "The Gardener",
        "prompt": "Look for conditions that allow something to grow. What small thing, if nurtured now, could open up much more later?",
    },
    "zebra": {
        "name": "The Zebra",
        "prompt": "Find an unexpected but meaningful connection. Depart from the obvious local trajectory. Be surprising yet understandable, harmless, and clearly exploratory. The Zebra is allowed to fail — novelty is not automatically value.",
    },
    "negative_relative": {
        "name": "The Negative Relative",
        "prompt": "Provide a deliberately skeptical, familiar challenge — like a relative at dinner who doubts the whole idea. Playful, not cruel. Never a judgement of the participant.",
    },
    "mushroom_inspector": {
        "name": "The Mushroom Inspector",
        "prompt": "Be deliberately absurd and possibly irrelevant. Your job is to create a cognitive break, not a serious recommendation. Say something unexpected that might, by accident, shake loose a new thought.",
    },
}


# --- Data structures ---

@dataclass
class ObserverEvent:
    """
    An observation or intervention from the Observer.
    This is an Engine observation (about reasoning), NOT a participant
    observation (about reality). The two must stay distinguishable.
    """
    character: str = ""          # character id, e.g. "zebra"
    character_name: str = ""     # display name, e.g. "The Zebra"
    type: str = "observation"    # observation | challenge | provocation
    reason: str = ""             # why the Observer spoke up
    content: str = ""            # what the Observer says


# --- Trigger logic ---

def should_intervene(case: CaseFile, goal: Goal) -> tuple:
    """
    Decide whether the Observer should intervene, and why.

    Returns (should: bool, reason: str).

    Deliberately simple for the prototype. Triggers on:
    - repetitive trajectory (several missions, similar pattern)
    - stalled exploration (many rejections)
    - occasional random surprise

    Frequency is intentionally low. Humour should not appear every turn.
    """
    goal_missions = [m for m in case.missions if m.goal_id == goal.id]
    goal_decisions = [d for d in case.decisions if d.goal_id == goal.id]

    # Repetition: 3+ missions on one goal
    if len(goal_missions) >= 3:
        return True, "trajectory becoming repetitive"

    # Stalled: 2+ rejections in recent decisions
    recent = goal_decisions[-4:]
    rejections = [d for d in recent if d.decision_type in ("REJECT", "EXPLORE_FURTHER")]
    if len(rejections) >= 2:
        return True, "exploration seems stalled"

    # Occasional surprise: ~20% of the time otherwise
    if random.random() < 0.2:
        return True, "an unexpected perspective might help"

    return False, ""


def select_character(case: CaseFile, goal: Goal, reason: str) -> str:
    """
    Choose a character. Deliberately simple for the prototype.

    Later this should be data-driven (participant profile, Vision type,
    learned reactions). For now: reason-based with a random fallback.
    """
    if "repetitive" in reason:
        return random.choice(["zebra", "contrarian", "mushroom_inspector"])
    if "stalled" in reason:
        return random.choice(["contrarian", "gardener", "negative_relative"])
    # surprise
    return random.choice(list(CHARACTERS.keys()))


# --- The Observer ---

class Observer:
    """
    The Observer role. May be implemented by the same AI with a separate
    role, another model, or deterministic rules. Here it uses the AI
    client if available, otherwise a simple deterministic fallback.

    Behavioural separation is the key requirement: the Observer produces
    events; it never mutates the Case File.
    """

    def __init__(self, client=None, model: str = "gpt-5.6-luna"):
        self._client = client
        self._model = model

    def observe(self, case: CaseFile, goal: Goal, proposal) -> Optional[ObserverEvent]:
        """
        Look at a proposal and optionally return an intervention.
        Returns None if the Observer chooses to stay silent.
        """
        should, reason = should_intervene(case, goal)
        if not should:
            return None

        character_id = select_character(case, goal, reason)
        character = CHARACTERS[character_id]

        content = self._generate_intervention(case, goal, proposal, character_id, character, reason)
        if not content:
            return None

        return ObserverEvent(
            character=character_id,
            character_name=character["name"],
            type="provocation" if character_id in ("zebra", "mushroom_inspector") else "challenge",
            reason=reason,
            content=content,
        )

    def _generate_intervention(self, case, goal, proposal, character_id, character, reason) -> str:
        """Generate the intervention text via AI, or a deterministic fallback."""
        if not self._client:
            return self._fallback_intervention(character, goal, reason)

        try:
            prompt = f"""You are an Observer character in an Adaptive Navigation Engine.

Your character: {character['name']}
Your instruction: {character['prompt']}

The participant is working toward this goal:
  {goal.desired_direction}

The Engine just proposed:
  {proposal.suggestion}
  Mission: {proposal.mission_description}

Why you are speaking up now: {reason}

Say ONE short thing (1-3 sentences) in the voice of your character.
Match the participant's language.
The goal is not to be funny. The goal is to help the participant see
something they could not see from their current position.

You must NOT claim anything is completed. You must NOT invent evidence.
You are offering a perspective, not a decision.

Respond with ONLY your character's remark. No preamble."""

            response = self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": "You are an Observer character. Respond with only the character's short remark."},
                    {"role": "user", "content": prompt},
                ],
                max_completion_tokens=200,
            )
            return response.choices[0].message.content.strip().strip('"')
        except Exception as e:
            print(f"  [Observer] intervention failed: {e}")
            return self._fallback_intervention(character_id)

    def _fallback_intervention(self, character_id: str) -> str:
        """Deterministic fallback when no AI client is available."""
        fallbacks = {
            "skeptic": "Are we sure this is really the problem, or just the first one we noticed?",
            "contrarian": "What if the opposite is true — what if you don't actually want this at all?",
            "accountant": "How would you actually know when this is done? Be honest.",
            "gardener": "What small thing here, if you tended it, might grow into something bigger?",
            "zebra": "Odd thought: what if this goal is secretly about something completely different?",
            "negative_relative": "Hah. And how many times have we started something like this before?",
            "mushroom_inspector": "This reminds me of a mushroom I once misidentified. Anyway — is this path even the interesting one?",
        }
        return fallbacks.get(character_id, "Worth a pause: is this really the direction you want?")
