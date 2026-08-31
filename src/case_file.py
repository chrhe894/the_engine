"""
Case File --- v0.1 Prototype

The Case File is the continuity mechanism.
It represents an evolving situation and its history.

This is a working implementation, not a final schema.
"""

import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional


# --- Goal Lifecycle ---

GOAL_ACTIVE = "ACTIVE"
GOAL_COMPLETED = "COMPLETED"
GOAL_ABANDONED = "ABANDONED"


# --- Decision vocabulary ---

DECISION_ACCEPT = "ACCEPT"
DECISION_MODIFY = "MODIFY"
DECISION_REJECT = "REJECT"
DECISION_EXPLORE = "EXPLORE_FURTHER"
DECISION_GIVE_UP = "GIVE_UP"


# --- Mission status ---

MISSION_ACTIVE = "ACTIVE"
MISSION_COMPLETED = "COMPLETED"
MISSION_FAILED = "FAILED"


# --- Data structures ---


@dataclass
class Observation:
    """Something observed about reality after or during a mission."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    text: str = ""
    source: str = "participant"  # participant, system, simulated
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    mission_id: Optional[str] = None


@dataclass
class Mission:
    """A concrete executable step belonging to a Goal."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""  # short label (1-3 words)
    goal_id: str = ""
    purpose: str = ""
    description: str = ""
    definition_of_done: list = field(default_factory=list)
    status: str = MISSION_ACTIVE
    result: Optional[str] = None
    observations: list = field(default_factory=list)  # list of Observation ids
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Goal:
    """A desired direction within the Case File."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    desired_direction: str = ""
    status: str = GOAL_ACTIVE
    missions: list = field(default_factory=list)  # list of Mission ids
    history: list = field(default_factory=list)  # list of event dicts
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Decision:
    """A recorded decision made by the participant."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    decision_type: str = ""  # ACCEPT, MODIFY, REJECT, EXPLORE_FURTHER, GIVE_UP
    goal_id: Optional[str] = None
    context: str = ""  # what was being decided
    reason: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ObserverEventRecord:
    """
    A persisted Observer event. An Engine observation (about reasoning),
    distinct from a participant Observation (about reality).

    Records what the Observer noticed, which character spoke, and the
    participant's reaction (if any). The Observer never changes Case File
    state on its own — only the participant's decision does that.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    goal_id: Optional[str] = None
    character: str = ""          # character id
    character_name: str = ""     # display name
    type: str = "observation"    # observation | challenge | provocation
    reason: str = ""             # why the Observer spoke up
    content: str = ""            # what the Observer said
    participant_reaction: Optional[str] = None  # free text or decision, if any
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class CaseFile:
    """
    The persistent, evolving representation of a situation
    and its transition through time.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    context: dict = field(default_factory=lambda: {
        "description": "",
        "opening_question": "What are we working on right now?",
        "time_scope": "ongoing",
        "geographic_scope": None,
    })
    current_situation: str = ""
    goals: list = field(default_factory=list)  # list of Goal
    missions: list = field(default_factory=list)  # list of Mission
    observations: list = field(default_factory=list)  # list of Observation
    decisions: list = field(default_factory=list)  # list of Decision
    observer_events: list = field(default_factory=list)  # list of ObserverEventRecord
    pending_proposals: dict = field(default_factory=dict)  # goal_id -> proposal dict
    history: list = field(default_factory=list)  # chronological event log
    created: str = field(default_factory=lambda: datetime.now().isoformat())
    updated: str = field(default_factory=lambda: datetime.now().isoformat())

    # --- Goal operations ---

    def add_goal(self, desired_direction: str) -> Goal:
        """Add a new active goal."""
        goal = Goal(desired_direction=desired_direction)
        self.goals.append(goal)
        self._log("goal_added", {"goal_id": goal.id, "direction": desired_direction})
        return goal

    def get_goal(self, goal_id: str) -> Optional[Goal]:
        """Find a goal by id."""
        for g in self.goals:
            if g.id == goal_id:
                return g
        return None

    def abandon_goal(self, goal_id: str, reason: str = "") -> Optional[Goal]:
        """
        Abandon a goal. This is local to the goal.
        It does not affect other goals or the Case File.
        """
        goal = self.get_goal(goal_id)
        if goal and goal.status == GOAL_ACTIVE:
            goal.status = GOAL_ABANDONED
            goal.history.append({
                "event": "abandoned",
                "reason": reason,
                "timestamp": datetime.now().isoformat(),
            })
            self._log("goal_abandoned", {"goal_id": goal_id, "reason": reason})
        return goal

    def complete_goal(self, goal_id: str) -> Optional[Goal]:
        """Mark a goal as completed."""
        goal = self.get_goal(goal_id)
        if goal and goal.status == GOAL_ACTIVE:
            goal.status = GOAL_COMPLETED
            goal.history.append({
                "event": "completed",
                "timestamp": datetime.now().isoformat(),
            })
            self._log("goal_completed", {"goal_id": goal_id})
        return goal

    def active_goals(self) -> list:
        """Return all active goals."""
        return [g for g in self.goals if g.status == GOAL_ACTIVE]

    # --- Mission operations ---

    def add_mission(self, goal_id: str, purpose: str, description: str,
                    definition_of_done: list = None, name: str = "") -> Mission:
        """Create a mission attached to a goal."""
        mission = Mission(
            name=name,
            goal_id=goal_id,
            purpose=purpose,
            description=description,
            definition_of_done=definition_of_done or [],
        )
        self.missions.append(mission)
        goal = self.get_goal(goal_id)
        if goal:
            goal.missions.append(mission.id)
        self._log("mission_added", {
            "mission_id": mission.id,
            "goal_id": goal_id,
            "purpose": purpose,
        })
        return mission

    def get_mission(self, mission_id: str) -> Optional[Mission]:
        """Find a mission by id."""
        for m in self.missions:
            if m.id == mission_id:
                return m
        return None

    def complete_mission(self, mission_id: str, result: str) -> Optional[Mission]:
        """Mark a mission as completed with a result."""
        mission = self.get_mission(mission_id)
        if mission and mission.status == MISSION_ACTIVE:
            mission.status = MISSION_COMPLETED
            mission.result = result
            self._log("mission_completed", {
                "mission_id": mission_id,
                "result": result,
            })
        return mission

    # --- Observation operations ---

    def add_observation(self, text: str, mission_id: str = None,
                        source: str = "participant") -> Observation:
        """Record an observation."""
        obs = Observation(text=text, source=source, mission_id=mission_id)
        self.observations.append(obs)
        if mission_id:
            mission = self.get_mission(mission_id)
            if mission:
                mission.observations.append(obs.id)
        self._log("observation_added", {
            "observation_id": obs.id,
            "text": text,
            "mission_id": mission_id,
        })
        return obs

    # --- Decision operations ---

    def record_decision(self, decision_type: str, goal_id: str = None,
                        context: str = "", reason: str = None) -> Decision:
        """Record a participant decision."""
        decision = Decision(
            decision_type=decision_type,
            goal_id=goal_id,
            context=context,
            reason=reason,
        )
        self.decisions.append(decision)
        self._log("decision_recorded", {
            "type": decision_type,
            "goal_id": goal_id,
            "context": context,
        })
        return decision

    # --- Observer operations ---

    def record_observer_event(self, goal_id: str, character: str,
                              character_name: str, event_type: str,
                              reason: str, content: str) -> "ObserverEventRecord":
        """
        Record an Observer event. This is an Engine observation about the
        reasoning process, not a participant observation about reality.
        It does not change any goal, mission, or situation state.
        """
        event = ObserverEventRecord(
            goal_id=goal_id,
            character=character,
            character_name=character_name,
            type=event_type,
            reason=reason,
            content=content,
        )
        self.observer_events.append(event)
        self._log("observer_event", {
            "goal_id": goal_id,
            "character": character,
            "type": event_type,
            "reason": reason,
        })
        return event

    def record_observer_reaction(self, event_id: str, reaction: str):
        """Record how the participant reacted to an Observer event."""
        for e in self.observer_events:
            if e.id == event_id:
                e.participant_reaction = reaction
                self._log("observer_reaction", {"event_id": event_id, "reaction": reaction})
                return e
        return None

    # --- Situation update ---

    def update_situation(self, new_situation: str):
        """Update the current situation description."""
        old = self.current_situation
        self.current_situation = new_situation
        self._log("situation_updated", {"old": old, "new": new_situation})

    # --- History ---

    def _log(self, event_type: str, data: dict):
        """Append to the chronological event log."""
        self.updated = datetime.now().isoformat()
        self.history.append({
            "event": event_type,
            "data": data,
            "timestamp": self.updated,
        })

    # --- Persistence ---

    def save(self, directory: str = "cases"):
        """Save the Case File as JSON."""
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        filepath = path / f"{self.id}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self._to_dict(), f, indent=2, ensure_ascii=False)
        return filepath

    @classmethod
    def load(cls, filepath: str) -> "CaseFile":
        """Load a Case File from JSON."""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls._from_dict(data)

    def _to_dict(self) -> dict:
        """Serialize to a plain dict."""
        return {
            "id": self.id,
            "context": self.context,
            "current_situation": self.current_situation,
            "goals": [asdict(g) for g in self.goals],
            "missions": [asdict(m) for m in self.missions],
            "observations": [asdict(o) for o in self.observations],
            "decisions": [asdict(d) for d in self.decisions],
            "observer_events": [asdict(e) for e in self.observer_events],
            "pending_proposals": self.pending_proposals,
            "history": self.history,
            "created": self.created,
            "updated": self.updated,
        }

    @classmethod
    def _from_dict(cls, data: dict) -> "CaseFile":
        """Deserialize from a plain dict."""
        cf = cls()
        cf.id = data["id"]
        cf.context = data.get("context", cf.context)
        cf.current_situation = data.get("current_situation", "")
        cf.goals = [Goal(**g) for g in data.get("goals", [])]
        cf.missions = [Mission(**m) for m in data.get("missions", [])]
        cf.observations = [Observation(**o) for o in data.get("observations", [])]
        cf.decisions = [Decision(**d) for d in data.get("decisions", [])]
        cf.observer_events = [ObserverEventRecord(**e) for e in data.get("observer_events", [])]
        cf.pending_proposals = data.get("pending_proposals", {})
        cf.history = data.get("history", [])
        cf.created = data.get("created", "")
        cf.updated = data.get("updated", "")
        return cf
