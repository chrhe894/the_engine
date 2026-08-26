"""
Engine v0.2 --- AI-Assisted Proposal Generator

Uses GPT-5.6 Luna to produce proposals from Case File context.

Preserves the existing Case File, Goal, Mission, Observation, Decision
structures. Does not redesign anything.

The AI must not invent evidence or claim that a Mission has been completed.

Falls back to the rule-based Engine (v0.1) if the API call fails or
no API key is available.

Usage:
    from engine_ai import AIEngine
    engine = AIEngine()  # reads OPENAI_API_KEY from env or .env file
    proposal = engine.propose(case, goal)
"""

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from case_file import (
    CaseFile, Goal, Mission, Observation,
    GOAL_ACTIVE, MISSION_COMPLETED,
)
from engine import Engine, Proposal, Interpretation


# --- Configuration ---

MODEL = "gpt-5.6-luna"
MAX_COMPLETION_TOKENS = 1200


def _load_api_key() -> Optional[str]:
    """Load API key from environment or .env file."""
    key = os.environ.get("OPENAI_API_KEY")
    if key:
        return key
    # Try .env file in prototype directory
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line.startswith("OPENAI_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


# --- System prompt ---

SYSTEM_PROMPT = """\
You are the reasoning component of an Adaptive Navigation Engine.

Your role: interpret the current Case File context and propose the next
meaningful transition for the participant.

CONSTRAINTS:
- You must NEVER invent evidence or claim that a Mission has been completed.
- You must NEVER fabricate observations.
- You propose. The user decides.
- Keep proposals concrete, actionable, and appropriately sized.
- If the desired direction is unclear, propose exploration rather than commitment.
- If previous observations exist, build on them rather than ignoring them.
- The participant should not need to understand methodology or internal concepts.

OUTPUT FORMAT (JSON):
{
  "interpretation": "Your understanding of the current situation",
  "uncertainty": "What remains unclear or questionable",
  "suggestion": "What you propose as the next step",
  "reason": "Why this is the next useful step",
  "mission_name": "A short label for this mission (1-3 words, like a tab title)",
  "mission_description": "A concrete, executable action",
  "mission_purpose": "What this mission is meant to achieve",
  "definition_of_done": ["condition 1", "condition 2", ...]
}

Respond ONLY with the JSON object. No markdown, no explanation outside the JSON.
"""


def _build_context_message(case: CaseFile, goal: Goal) -> str:
    """Build the user message with relevant Case File context."""
    parts = []

    # Case context
    parts.append("CASE CONTEXT:")
    if case.context.get("description"):
        parts.append(f"  Description: {case.context['description']}")
    if case.context.get("opening_question"):
        parts.append(f"  Opening question: {case.context['opening_question']}")
    if case.context.get("geographic_scope"):
        parts.append(f"  Geographic scope: {case.context['geographic_scope']}")
    if case.context.get("time_scope"):
        parts.append(f"  Time scope: {case.context['time_scope']}")

    # Current situation
    parts.append(f"\nCURRENT SITUATION:")
    parts.append(f"  {case.current_situation or 'Not yet described.'}")

    # The goal we're working on
    parts.append(f"\nGOAL:")
    parts.append(f"  Desired direction: {goal.desired_direction}")
    parts.append(f"  Status: {goal.status}")

    # Other active goals (for awareness, not action)
    other_goals = [g for g in case.goals if g.id != goal.id and g.status == GOAL_ACTIVE]
    if other_goals:
        parts.append(f"\nOTHER ACTIVE GOALS (for context only, do not propose for these):")
        for g in other_goals:
            parts.append(f"  - {g.desired_direction}")

    # Missions for this goal
    goal_missions = [m for m in case.missions if m.goal_id == goal.id]
    if goal_missions:
        parts.append(f"\nMISSIONS FOR THIS GOAL:")
        for m in goal_missions:
            parts.append(f"  [{m.status}] {m.description}")
            if m.result:
                parts.append(f"    Result: {m.result}")

    # Observations related to this goal's missions
    goal_mission_ids = [m.id for m in goal_missions]
    goal_observations = [o for o in case.observations if o.mission_id in goal_mission_ids]
    if goal_observations:
        parts.append(f"\nOBSERVATIONS FROM THIS GOAL'S MISSIONS:")
        for o in goal_observations:
            parts.append(f"  - {o.text}")

    # Recent decisions
    goal_decisions = [d for d in case.decisions if d.goal_id == goal.id]
    if goal_decisions:
        parts.append(f"\nRECENT DECISIONS:")
        for d in goal_decisions[-5:]:  # last 5
            entry = f"  [{d.decision_type}] {d.context}"
            if d.reason:
                entry += f" — reason: {d.reason}"
            parts.append(entry)

    parts.append(f"\nProduce a proposal for the next step on this goal.")
    return "\n".join(parts)


class AIEngine:
    """
    AI-assisted Engine v0.2.

    Calls GPT-5.6 Luna for proposal generation.
    Falls back to rule-based Engine v0.1 on failure.
    """

    def __init__(self, api_key: str = None):
        self._api_key = api_key or _load_api_key()
        self._fallback = Engine()
        self._client = None

        if self._api_key:
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=self._api_key)
            except Exception as e:
                print(f"  [AIEngine] OpenAI client init failed: {e}")
                self._client = None

    @property
    def available(self) -> bool:
        """Whether the AI engine is available."""
        return self._client is not None

    def interpret_input(self, case: CaseFile, user_text: str) -> Interpretation:
        """
        Interpret user input using AI.
        Falls back to rule-based interpretation on failure.
        """
        if not self._client:
            return self._fallback.interpret_input(case, user_text)

        try:
            prompt = f"""Interpret this user input in the context of adaptive change navigation.

CONTEXT:
  {json.dumps(case.context, ensure_ascii=False)}

USER INPUT:
  "{user_text}"

Respond with JSON:
{{
  "current_situation": "your interpretation of the current situation",
  "possible_direction": "what direction or desired change this suggests",
  "uncertainty": "high/medium/low"
}}

Respond ONLY with the JSON object."""

            response = self._client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "You interpret user input for an adaptive navigation system. Respond only with JSON."},
                    {"role": "user", "content": prompt},
                ],
                max_completion_tokens=400,
            )

            result = json.loads(response.choices[0].message.content.strip())
            return Interpretation(
                current_situation=result.get("current_situation", user_text),
                possible_direction=result.get("possible_direction", user_text),
                uncertainty=result.get("uncertainty", "high"),
            )
        except Exception as e:
            print(f"  [AIEngine] interpret_input failed: {e}")
            return self._fallback.interpret_input(case, user_text)

    def propose(self, case: CaseFile, goal: Goal) -> Proposal:
        """
        Produce a proposal using AI reasoning.
        Falls back to rule-based Engine on failure.
        """
        if not self._client:
            return self._fallback.propose(case, goal)

        try:
            context_message = _build_context_message(case, goal)

            response = self._client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": context_message},
                ],
                max_completion_tokens=MAX_COMPLETION_TOKENS,
            )

            raw = response.choices[0].message.content.strip()
            # Handle possible markdown code fences
            if raw.startswith("```"):
                raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
                if raw.endswith("```"):
                    raw = raw[:-3]
                raw = raw.strip()

            result = json.loads(raw)

            return Proposal(
                goal_id=goal.id,
                current=result.get("interpretation", ""),
                desired=goal.desired_direction,
                suggestion=result.get("suggestion", ""),
                reason=result.get("reason", ""),
                mission_name=result.get("mission_name", ""),
                mission_description=result.get("mission_description", ""),
                mission_purpose=result.get("mission_purpose", ""),
                definition_of_done=result.get("definition_of_done", []),
            )
        except Exception as e:
            print(f"  [AIEngine] propose failed: {e}")
            print(f"  [AIEngine] Falling back to rule-based engine.")
            return self._fallback.propose(case, goal)

    def propose_after_give_up(self, case: CaseFile, goal: Goal) -> dict:
        """
        Reassessment after GIVE UP.
        Uses the same structure as v0.1 — this is a UI flow, not AI reasoning.
        """
        return self._fallback.propose_after_give_up(case, goal)

    def propose_challenge(self, case: CaseFile, goal: Goal) -> Proposal:
        """
        Produce a micro-transition challenge using AI.
        Falls back to rule-based on failure.
        """
        if not self._client:
            return self._fallback.propose_challenge(case, goal)

        try:
            context_message = _build_context_message(case, goal)
            challenge_prompt = f"""{context_message}

The participant has said GIVE UP and then asked to be challenged.

Propose the SMALLEST possible meaningful step. Something that takes
15 minutes or less. Something concrete and specific to their situation.

Do not propose a large mission. Do not motivate. Simply offer one tiny,
concrete action that tests whether this direction still has meaning.

Respond with the same JSON format as a normal proposal."""

            response = self._client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": challenge_prompt},
                ],
                max_completion_tokens=MAX_COMPLETION_TOKENS,
            )

            raw = response.choices[0].message.content.strip()
            if raw.startswith("```"):
                raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
                if raw.endswith("```"):
                    raw = raw[:-3]
                raw = raw.strip()

            result = json.loads(raw)

            return Proposal(
                goal_id=goal.id,
                current=result.get("interpretation", ""),
                desired=goal.desired_direction,
                suggestion=result.get("suggestion", ""),
                reason=result.get("reason", ""),
                mission_name=result.get("mission_name", ""),
                mission_description=result.get("mission_description", ""),
                mission_purpose=result.get("mission_purpose", ""),
                definition_of_done=result.get("definition_of_done", []),
            )
        except Exception as e:
            print(f"  [AIEngine] propose_challenge failed: {e}")
            return self._fallback.propose_challenge(case, goal)
