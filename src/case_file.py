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


# --- Concept tree (concept mode) ---

CONCEPT_ACTIVE = "ACTIVE"        # one of the points the owner is working with
CONCEPT_CANDIDATE = "CANDIDATE"  # proposed (variation / deep mode), not yet chosen
CONCEPT_PARKED = "PARKED"        # set aside, kept so the space stays visible

CONCEPT_STATUSES = (CONCEPT_ACTIVE, CONCEPT_CANDIDATE, CONCEPT_PARKED)

# How a node came about.
CONCEPT_MODE_SPLIT = "split"   # parts that together make up the parent
CONCEPT_MODE_VARY = "vary"     # alternatives that differ from each other
CONCEPT_MODE_DEEP = "deep"     # produced by a deep-mode run (see lens)
CONCEPT_MODE_OWNER = "owner"   # written by the owner


# What a point needs before it counts as "spikad" (nailed): concrete enough to start
# working with, and to become a Mission later. Plain text, the owner fills it in.
SPEC_KEYS = ("goal", "done", "actor", "first_step")


@dataclass
class ConceptNode:
    """
    One point in a concept tree. Plain text on purpose: a name and a body the
    owner can edit freely. No fixed fields (decision: ren text).

    parent_id None means the node hangs directly under its goal. The goal's
    desired_direction is the 'sentence' the first level is derived from.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    goal_id: str = ""
    parent_id: Optional[str] = None
    title: str = ""
    text: str = ""
    status: str = CONCEPT_ACTIVE
    source: str = "ai"                 # ai | owner
    mode: str = CONCEPT_MODE_SPLIT     # split | vary | deep | owner
    lens: str = ""                     # lens id for deep-mode points
    stability: str = ""                # deep mode: "stable" | "variant" | ""
    seen_in: list = field(default_factory=list)  # lens ids where this point appeared
    edited: bool = False               # True once the owner has changed the AI text
    variant_of: Optional[str] = None   # id of the point this is a variation of (Variera)
    theme: str = ""                    # deep mode: the theme this point was collected under
    spec: dict = field(default_factory=dict)  # goal, done, actor, first_step (may be partial)
    spiked: bool = False               # owner has nailed it: all four spec parts are filled in
    draft_text: str = ""               # Förstärk proposal waiting for the owner's decision
    draft_spec: dict = field(default_factory=dict)
    draft_missing: str = ""            # what the Engine says is still unclear
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


# --- Start list (concrete things to do, collected from the whole tree) ---

ACTION_PROPOSED = "PROPOSED"      # suggested by the Engine, not yet decided
ACTION_ACCEPTED = "ACCEPTED"      # the owner took it on; it is now a Mission
ACTION_DISMISSED = "DISMISSED"    # set aside by the owner, or replaced by a newer collection

ACTION_LAYER_BASE = "base"        # needed before anyone can start at all (from situation + desired state)
ACTION_LAYER_POINTS = "points"    # a shared prerequisite for several points in the tree


@dataclass
class ActionItem:
    """
    One concrete thing to do, collected from the tree. It stays a proposal until the
    owner accepts it; accepting turns it into a Mission (with a definition of done)
    so the existing loop (result, observation) is reused.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    goal_id: str = ""
    title: str = ""
    done_when: str = ""
    layer: str = ACTION_LAYER_POINTS
    serves: list = field(default_factory=list)   # ids of the concept points it serves ([] = the whole case)
    needs: list = field(default_factory=list)    # ids of other actions that should come first
    first: bool = False                          # the Engine's pick for where to start
    order: int = 0
    status: str = ACTION_PROPOSED
    mission_id: Optional[str] = None
    edited: bool = False
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class CaseFile:
    """
    The persistent, evolving representation of a situation
    and its transition through time.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    owner_id: Optional[str] = None  # id of the user who owns this case (None = legacy/unowned)
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
    concepts: list = field(default_factory=list)  # list of ConceptNode (concept tree)
    actions: list = field(default_factory=list)  # list of ActionItem (the start list)
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

    # --- Concept tree operations ---

    def add_concept(self, goal_id: str, title: str, text: str,
                    parent_id: str = None, status: str = CONCEPT_ACTIVE,
                    source: str = "ai", mode: str = CONCEPT_MODE_SPLIT,
                    lens: str = "", stability: str = "",
                    seen_in: list = None, variant_of: str = None, theme: str = "") -> ConceptNode:
        """Add a point to the concept tree."""
        node = ConceptNode(
            goal_id=goal_id, parent_id=parent_id, title=title, text=text,
            status=status, source=source, mode=mode, lens=lens,
            stability=stability, seen_in=list(seen_in or []), variant_of=variant_of,
            theme=theme,
        )
        self.concepts.append(node)
        self._log("concept_added", {
            "concept_id": node.id, "goal_id": goal_id, "parent_id": parent_id,
            "source": source, "mode": mode, "status": status,
        })
        return node

    def get_concept(self, concept_id: str) -> Optional[ConceptNode]:
        """Find a concept node by id."""
        for c in self.concepts:
            if c.id == concept_id:
                return c
        return None

    def concepts_under(self, goal_id: str, parent_id: str = None) -> list:
        """Direct children of a parent (a goal root when parent_id is None)."""
        return [c for c in self.concepts
                if c.goal_id == goal_id and c.parent_id == parent_id]

    def edit_concept(self, concept_id: str, title: str, text: str) -> Optional[ConceptNode]:
        """Owner edit of a node's name and text. Keeps the previous text in history."""
        node = self.get_concept(concept_id)
        if node and (node.title != title or node.text != text):
            self._log("concept_edited", {
                "concept_id": concept_id,
                "old_title": node.title,
                "old_text": node.text,
            })
            node.title = title
            node.text = text
            node.edited = True
        return node

    def set_concept_status(self, concept_id: str, status: str) -> Optional[ConceptNode]:
        """Choose (ACTIVE), park (PARKED) or un-choose (CANDIDATE) a node."""
        node = self.get_concept(concept_id)
        if node and status in CONCEPT_STATUSES and node.status != status:
            old = node.status
            node.status = status
            self._log("concept_status", {
                "concept_id": concept_id, "old": old, "new": status,
            })
        return node

    def set_concept_draft(self, concept_id: str, text: str, spec: dict, missing: str) -> Optional[ConceptNode]:
        """Store a Förstärk proposal. It changes nothing until the owner uses it."""
        node = self.get_concept(concept_id)
        if node:
            node.draft_text = text
            node.draft_spec = {k: str(spec.get(k, "")).strip() for k in SPEC_KEYS}
            node.draft_missing = missing
            self._log("concept_draft", {"concept_id": concept_id})
        return node

    def use_concept_draft(self, concept_id: str) -> Optional[ConceptNode]:
        """The owner accepts the Förstärk proposal. The old text stays in history."""
        node = self.get_concept(concept_id)
        if node and node.draft_text:
            self.edit_concept(concept_id, node.title, node.draft_text)
            merged = dict(node.spec)
            for k in SPEC_KEYS:
                if node.draft_spec.get(k, "").strip():
                    merged[k] = node.draft_spec[k].strip()
            node.spec = merged
            node.draft_text, node.draft_spec, node.draft_missing = "", {}, ""
            self._log("concept_draft_used", {"concept_id": concept_id})
        return node

    def drop_concept_draft(self, concept_id: str) -> Optional[ConceptNode]:
        node = self.get_concept(concept_id)
        if node and node.draft_text:
            node.draft_text, node.draft_spec, node.draft_missing = "", {}, ""
            self._log("concept_draft_dropped", {"concept_id": concept_id})
        return node

    def set_concept_spec(self, concept_id: str, spec: dict) -> Optional[ConceptNode]:
        node = self.get_concept(concept_id)
        if node:
            node.spec = {k: str(spec.get(k, "")).strip() for k in SPEC_KEYS}
            self._log("concept_spec", {"concept_id": concept_id})
        return node

    @staticmethod
    def spec_complete(node: ConceptNode) -> bool:
        return all((node.spec.get(k) or "").strip() for k in SPEC_KEYS)

    def set_concept_spiked(self, concept_id: str, spiked: bool) -> Optional[ConceptNode]:
        """Nail (or un-nail) a point. Nailing needs all four spec parts, and a
        nailed point is also kept, so a re-run cannot replace it."""
        node = self.get_concept(concept_id)
        if not node:
            return None
        if spiked:
            if not self.spec_complete(node):
                return None
            node.spiked = True
            if node.status != CONCEPT_ACTIVE:
                self.set_concept_status(concept_id, CONCEPT_ACTIVE)
        else:
            node.spiked = False
        self._log("concept_spiked", {"concept_id": concept_id, "spiked": spiked})
        return node

    def set_concept_theme(self, concept_id: str, theme: str, variant_of: str = None) -> Optional[ConceptNode]:
        """Label a point with a theme; a point that is not yet a variation of anything
        becomes a variation of `variant_of` (the proposal that represents its theme)."""
        node = self.get_concept(concept_id)
        if node:
            node.theme = theme
            if variant_of and not node.variant_of and variant_of != concept_id:
                node.variant_of = variant_of
            self._log("concept_theme", {"concept_id": concept_id, "theme": theme})
        return node

    def set_concept_seen(self, concept_id: str, seen_in: list, stability: str) -> Optional[ConceptNode]:
        """Record that deep mode found an existing point again, and in which lenses."""
        node = self.get_concept(concept_id)
        if node:
            node.seen_in = list(seen_in)
            node.stability = stability
            self._log("concept_seen", {
                "concept_id": concept_id, "seen_in": list(seen_in), "stability": stability,
            })
        return node

    # --- Start list operations ---

    def get_action(self, action_id: str) -> Optional[ActionItem]:
        for a in self.actions:
            if a.id == action_id:
                return a
        return None

    def replace_proposed_actions(self, goal_id: str, items: list) -> list:
        """A new collection replaces the proposals that were never decided. The old
        ones are set aside (not deleted); accepted actions are left alone. `items` are
        dicts with title, done_when, layer, serves, needs (as indexes into `items`), first."""
        replaced = 0
        for a in self.actions:
            if a.goal_id == goal_id and a.status == ACTION_PROPOSED:
                a.status = ACTION_DISMISSED
                replaced += 1
        created = []
        for order, it in enumerate(items):
            created.append(ActionItem(
                goal_id=goal_id, title=it["title"], done_when=it.get("done_when", ""),
                layer=it.get("layer", ACTION_LAYER_POINTS), serves=list(it.get("serves", [])),
                first=bool(it.get("first")), order=order,
            ))
        for it, a in zip(items, created):
            a.needs = [created[i].id for i in it.get("needs", []) if 0 <= i < len(created) and created[i] is not a]
        self.actions.extend(created)
        self._log("actions_collected", {"goal_id": goal_id, "count": len(created), "replaced": replaced})
        return created

    def edit_action(self, action_id: str, title: str, done_when: str) -> Optional[ActionItem]:
        a = self.get_action(action_id)
        if a and (a.title != title or a.done_when != done_when):
            self._log("action_edited", {"action_id": action_id, "old_title": a.title, "old_done_when": a.done_when})
            a.title, a.done_when, a.edited = title, done_when, True
        return a

    def set_action_status(self, action_id: str, status: str) -> Optional[ActionItem]:
        """Dismiss, or take back (back to PROPOSED). Accepting goes through accept_action."""
        a = self.get_action(action_id)
        if a and status in (ACTION_DISMISSED, ACTION_PROPOSED) and a.status != ACTION_ACCEPTED and a.status != status:
            self._log("action_status", {"action_id": action_id, "old": a.status, "new": status})
            a.status = status
        return a

    def accept_action(self, action_id: str) -> Optional[ActionItem]:
        """The owner takes the action on. It becomes a Mission with a definition of done."""
        a = self.get_action(action_id)
        if not a or a.status == ACTION_ACCEPTED:
            return a
        titles = [c.title for c in self.concepts if c.id in a.serves]
        purpose = ("Tjänar: " + ", ".join(titles)) if titles else "Grundförutsättning för hela ärendet"
        m = self.add_mission(goal_id=a.goal_id, purpose=purpose, description=a.title,
                             definition_of_done=[a.done_when] if a.done_when else [],
                             name=a.title[:60])
        a.status, a.mission_id = ACTION_ACCEPTED, m.id
        self._log("action_accepted", {"action_id": action_id, "mission_id": m.id})
        return a

    def finish_action(self, action_id: str, result: str = "") -> Optional[ActionItem]:
        """Mark the Mission behind an accepted action as done, with what happened (optional).
        Unlike the old mission flow this does not overwrite current_situation."""
        a = self.get_action(action_id)
        if not a or not a.mission_id:
            return None
        m = self.get_mission(a.mission_id)
        if m and m.status == MISSION_ACTIVE:
            self.complete_mission(m.id, result or "Klart")
            if result:
                self.add_observation(result, mission_id=m.id)
        return a

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
            "owner_id": self.owner_id,
            "context": self.context,
            "current_situation": self.current_situation,
            "goals": [asdict(g) for g in self.goals],
            "missions": [asdict(m) for m in self.missions],
            "observations": [asdict(o) for o in self.observations],
            "decisions": [asdict(d) for d in self.decisions],
            "observer_events": [asdict(e) for e in self.observer_events],
            "concepts": [asdict(c) for c in self.concepts],
            "actions": [asdict(a) for a in self.actions],
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
        cf.owner_id = data.get("owner_id")  # None for legacy case files
        cf.context = data.get("context", cf.context)
        cf.current_situation = data.get("current_situation", "")
        cf.goals = [Goal(**g) for g in data.get("goals", [])]
        cf.missions = [Mission(**m) for m in data.get("missions", [])]
        cf.observations = [Observation(**o) for o in data.get("observations", [])]
        cf.decisions = [Decision(**d) for d in data.get("decisions", [])]
        cf.observer_events = [ObserverEventRecord(**e) for e in data.get("observer_events", [])]
        cf.concepts = [ConceptNode(**c) for c in data.get("concepts", [])]  # absent in older files
        cf.actions = [ActionItem(**a) for a in data.get("actions", [])]  # absent in older files
        cf.pending_proposals = data.get("pending_proposals", {})
        cf.history = data.get("history", [])
        cf.created = data.get("created", "")
        cf.updated = data.get("updated", "")
        return cf
