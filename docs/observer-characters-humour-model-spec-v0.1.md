# Observer Characters & Humour — Model Specification v0.1

## Status
**Exploration / model change**

This specification introduces an Observer layer and a controlled humour/character mechanism into the Engine model. It is a model specification, not a final implementation specification.

## 1. Purpose
The Engine should be capable of:
- observing its own proposals and trajectory;
- noticing repetition, narrowness, weak assumptions, or excessive certainty;
- deliberately introducing an unexpected perspective when useful;
- occasionally using humour, absurdity, or a character to break a local loop;
- helping the participant discover possibilities not explicit in the original Vision;
- adapting Observer characters to the evolving participant profile and Vision.

The purpose is **not to make the AI into a comedian**. Humour is a mechanism for surprise, perspective, connection, and possible escape from a too-narrow trajectory.

## 2. Core principle
> **The Engine proposes. The participant decides. Reality answers.**

With the Observer:
> **The Engine proposes. The Observer notices and challenges. The participant decides. Reality answers.**

The Observer does not become an autonomous decision-maker.

## 3. Two kinds of observation

### Participant / world observation
What happened after a Mission. These are observations about reality.

### Engine observation
What the Observer notices about the reasoning process, proposal, trajectory, or Case File. These must remain distinguishable from participant observations.

## 4. Observer role
The Observer is a conceptual Engine role. It may eventually be implemented by the same AI with a separate role, another model, deterministic rules, or several agents/models. The important requirement is behavioural separation: a proposal can be observed and questioned without the Observer directly changing the Case File.

## 5. Observer responsibilities
An Observer may assess:
- **Trajectory:** repetition or excessive narrowness.
- **Assumptions:** uncertain interpretations treated as established.
- **Scale:** Missions that are too large, vague, or difficult.
- **Evidence:** whether proposals are grounded in observations.
- **Direction:** whether the participant still wants the current direction.
- **Opportunity:** unexplored directions.
- **Surprise:** whether an unexpected perspective could help.

## 6. Observer characters
Characters are presentation and reasoning perspectives, not necessarily separate AIs.

Initial examples:

- **The Skeptic** — questions assumptions.
- **The Contrarian** — explores the opposite interpretation.
- **The Accountant** — insists on observable completion and manageable scope.
- **The Gardener** — looks for conditions that allow something to grow.
- **The Zebra** — looks for unexpected but meaningful connections.
- **The Negative Relative** — provides a deliberately skeptical, familiar challenge.
- **The Mushroom Inspector** — deliberately absurd and potentially irrelevant, used to create a cognitive break rather than provide a serious recommendation.

These are examples, not a fixed taxonomy.

## 7. Character library
The system should eventually support many characters. Characters may differ in perspective, scepticism, absurdity, humour style, domain, social tone, risk tolerance, preferred exploration stage, Vision types, and participant profiles.

Character selection should be data-driven where practical rather than hard-coded into the core reasoning loop.

## 8. Character selection
Selection may depend on:

### Participant profile
The profile is gradually discovered rather than assumed. Signals may include preferred challenge level, reactions to humour, tolerance for ambiguity, interests, experience, accepted/rejected proposals, and whether provocation produces useful observations.

Do not prematurely construct a rigid personality profile.

### Vision / direction
The Vision can influence useful characters. For example, community work may benefit from a Social Observer; engineering from a Skeptic; creative work from an Artist/Fool; conventional trajectories from the Zebra; stuck trajectories from the Contrarian.

## 9. Humour mechanism
Humour is optional and should not appear on every turn. Possible triggers:
- repeated similar proposals;
- stalled exploration;
- fixation on one interpretation;
- predictable proposal sequences;
- participant choosing an exploratory mode;
- previous positive response to humour;
- an appropriate transition between interpretations;
- Observer identifies a perspective-shift opportunity.

Exact frequency remains configurable and experimental.

## 10. Humour is not required to be funny
Success is not measured only by laughter. A humorous intervention may succeed if it causes a new thought, correction, rejection of an assumption, new Goal, new Observation, clarification of Vision, renewed engagement, or recognition that the current path is wrong.

A reaction such as:
> “That's ridiculous — but it reminds me that I actually hate working with people.”
may be more valuable than laughter.

The reaction itself becomes information.

## 11. The Zebra principle
The Zebra represents deliberate departure from the most obvious local trajectory.

```text
Current direction
       |
       v
  normal proposal
       |
       v
  Observer notices
       |
       +------> ordinary challenge
       |
       +------> unexpected connection
                       |
                       v
                    ZEBRA
                       |
             +---------+---------+
             |         |         |
           Reject    Explore   Accept
```

The Zebra is not random. It should be surprising, understandable, harmless, clearly exploratory, potentially useful, and allowed to fail. Novelty is not automatically value.

## 12. Participant control
Humorous/provocative interventions must not silently create, modify, complete, or abandon Case File state. They produce proposals or invitations to explore. The participant explicitly decides whether a new direction becomes relevant.

## 13. Relationship to modes

### Yellow / Creative / Build
Participant broadly knows what they want. Observer behaviour is light and infrequent; focus is improving what is known.

### Blue / Survival / Explore
Participant has a direction but uncertainty remains. Observer may challenge assumptions and introduce alternatives.

### Red / Hardcore / Discover
Participant deliberately enters less predictable exploration. Observer may be more provocative and willing to introduce unusual connections.

These are UX metaphors and should not unnecessarily constrain the Engine model.

## 14. Safety and boundaries
Humour must not undermine safety, dignity, or autonomy. Avoid cruelty, humiliation, discrimination, threats, manipulation, personal invasion, or inappropriate context. Characters such as the Negative Relative are playful perspectives, not judgements of the participant.

## 15. Case File representation
The Case File should preserve distinctions between ordinary reasoning, Observer observations, character interventions, participant reactions, and resulting decisions.

Illustrative only:

```json
{
  "observer_events": [
    {
      "character": "zebra",
      "type": "provocation",
      "reason": "trajectory becoming repetitive",
      "content": "..."
    }
  ],
  "participant_reaction": {
    "decision": "EXPLORE_FURTHER",
    "response": "..."
  }
}
```

The final App↔Engine protocol is not fixed by this document.

## 16. Learning from reactions
Character selection should improve through observed participant reactions. Repeatedly useful interventions can become more appropriate; repeatedly rejected ones can be reduced or stopped. Preferences should be learned from evidence rather than assumed.

## 17. Model change
The earlier conceptual flow was:

```text
Situation → Goal → Mission → Observation → next proposal
```

The expanded flow is:

```text
                    ENGINE
                      |
                   Reasoner
                      |
                   Proposal
                      |
                   OBSERVER
                      |
             notice / challenge /
                surprise
                      |
                 Participant
                      |
             Decision / Response
                      |
                    Mission
                      |
                   Reality
                      |
           Participant Observation
                      |
                  Case File
                      |
                next iteration
```

The Observer is therefore an explicit model element.

## 18. What this does NOT mean
This does not mean:
- constant jokes;
- random nonsense;
- a crazy alternative for every Goal;
- characters replacing reasoning;
- humour replacing useful Missions;
- App exposure of technical Engine concepts;
- a rigid personality taxonomy;
- a final API or JSON schema being decided.

This remains an experiment.

## 19. First prototype experiment
Keep the first implementation small:

1. Generate a normal proposal.
2. Run an Observer assessment.
3. Occasionally allow one character.
4. Present a sideways or humorous intervention.
5. Let the participant ACCEPT, MODIFY, REJECT, or EXPLORE FURTHER.
6. Record the reaction.
7. Verify that the Case File changes only through participant decision.
8. Verify that a humorous intervention can produce a useful new direction without being treated as fact.

Start with:
- Skeptic
- Contrarian
- Accountant
- Zebra
- Negative Relative
- Mushroom Inspector

Then let evidence determine what additional characters are useful.

## 20. Guiding principle
The objective is not:
> **Make the AI funny.**

It is:
> **Make the Engine capable of helping a human see something they could not see from their current position.**

Humour is one possible mechanism.

The ideal result is sometimes laughter, but the deeper result is:

> **“Wait... I hadn't thought of it that way.”**

That is the Zebra.

And the Zebra is allowed to become something else.
