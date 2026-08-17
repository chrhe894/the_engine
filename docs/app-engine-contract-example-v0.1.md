# App ↔ Engine Contract --- Concrete Examples v0.1

## Purpose

This document makes the semantic App ↔ Engine contract concrete by
showing example messages.

The examples are deliberately simple and are intended to expose gaps in
the contract before implementation.

**JSON is used only as an example representation. It is not yet the
final transport/API decision.**

The examples follow one complete loop:

``` text
ContextOpened
    ↓
UserInput
    ↓
Interpretation
    ↓
Suggestion / Question
    ↓
Selection
    ↓
TransitionProposal
    ↓
Decision
    ↓
Mission
    ↓
MissionResult
    ↓
NextStep
```

------------------------------------------------------------------------

# Example A --- Individual: "I don't know what I want to do"

## 1. ContextOpened

The participant enters an opened context.

``` json
{
  "message": "context_opened",
  "context": {
    "id": "demo-individual-001",
    "time_scope": {
      "type": "ongoing"
    },
    "geographic_scope": {
      "type": "country",
      "value": "SE"
    },
    "opening_question": "What are we working on right now?"
  },
  "participant": {
    "id": "participant-001"
  }
}
```

### Notes

The Engine receives enough context to understand where the interaction
belongs.

The participant does not need to have a fully defined Identity.

------------------------------------------------------------------------

## 2. UserInput

The participant answers the opening question.

``` json
{
  "message": "user_input",
  "context_id": "demo-individual-001",
  "participant_id": "participant-001",
  "text": "I don't know what I want to do."
}
```

------------------------------------------------------------------------

## 3. Interpretation

The Engine responds with a provisional understanding.

``` json
{
  "message": "interpretation",
  "context_id": "demo-individual-001",
  "interpretation": {
    "current_situation": "The participant does not currently have a clear occupational direction.",
    "uncertainty": "high"
  }
}
```

The interpretation is not a fact asserted by the system. It is an
editable working hypothesis.

------------------------------------------------------------------------

## 4. Suggestion

The Engine proposes an exploration method.

``` json
{
  "message": "suggestion",
  "context_id": "demo-individual-001",
  "suggestions": [
    {
      "id": "suggestion-001",
      "type": "exploration",
      "title": "Explore occupations",
      "description": "Look through possible occupations and remove those that are not interesting or realistic."
    }
  ]
}
```

This deliberately corresponds to the occupation-card method discussed
earlier.

------------------------------------------------------------------------

## 5. Selection

The participant selects the exploration.

``` json
{
  "message": "selection",
  "context_id": "demo-individual-001",
  "participant_id": "participant-001",
  "selected_id": "suggestion-001"
}
```

------------------------------------------------------------------------

## 6. Engine proposes a direction

Suppose the participant has explored a set of occupation cards and
retained four.

``` json
{
  "message": "transition_proposal",
  "context_id": "demo-individual-001",
  "current": {
    "description": "No clear occupational direction."
  },
  "desired": {
    "description": "Identify one occupational direction worth exploring."
  },
  "proposal": {
    "description": "Explore the four remaining occupations and identify which appears most obtainable and worthwhile."
  }
}
```

------------------------------------------------------------------------

## 7. Decision

The participant accepts.

``` json
{
  "message": "decision",
  "context_id": "demo-individual-001",
  "participant_id": "participant-001",
  "decision": "ACCEPT"
}
```

The important point is that the Engine proposed the transition, but the
participant made the decision.

------------------------------------------------------------------------

## 8. Mission

The Engine creates a concrete Mission.

``` json
{
  "message": "mission",
  "context_id": "demo-individual-001",
  "mission": {
    "id": "mission-001",
    "purpose": "Compare the four remaining occupational directions.",
    "description": "Investigate what each occupation involves and identify the most obtainable next direction.",
    "definition_of_done": [
      "All four occupations have been considered.",
      "At least one reason for interest or rejection has been recorded for each.",
      "One direction has been selected for further exploration."
    ]
  }
}
```

The App can now execute the Mission using its existing mechanisms.

------------------------------------------------------------------------

## 9. MissionResult

The participant completes the Mission.

``` json
{
  "message": "mission_result",
  "context_id": "demo-individual-001",
  "mission_id": "mission-001",
  "status": "completed",
  "observation": {
    "text": "Software development seems most interesting. It looks difficult, but I would like to try it."
  },
  "evidence": [
    {
      "type": "participant_recorded_observation"
    }
  ]
}
```

The Engine does not need to assume that the participant's conclusion is
objectively correct.

It receives an observation and continues the loop.

------------------------------------------------------------------------

## 10. NextStep

``` json
{
  "message": "next_step",
  "context_id": "demo-individual-001",
  "based_on": [
    "mission-001"
  ],
  "suggestions": [
    {
      "id": "suggestion-002",
      "type": "exploration",
      "title": "Talk to a software developer",
      "description": "Learn what the work is actually like before committing to a larger transition."
    },
    {
      "id": "suggestion-003",
      "type": "exploration",
      "title": "Try a small programming task",
      "description": "Test whether programming itself is interesting before investing heavily."
    }
  ]
}
```

The loop is now ready to continue.

------------------------------------------------------------------------

# Example B --- Skördefesten / Södra Öland

The same contract is used in a very different context.

## 1. ContextOpened

``` json
{
  "message": "context_opened",
  "context": {
    "id": "skordefest-sodra-oland-2026",
    "time_scope": {
      "type": "period",
      "from": "2026-09-01",
      "to": "2026-10-31"
    },
    "geographic_scope": {
      "type": "named_area",
      "value": "Södra Öland"
    },
    "opening_question": "What would make Södra Öland an even better place to live, work and visit?"
  },
  "participant": {
    "id": "organisation-001"
  }
}
```

The participant could be a person, business, association, municipality
or another organisation.

------------------------------------------------------------------------

## 2. UserInput

``` json
{
  "message": "user_input",
  "context_id": "skordefest-sodra-oland-2026",
  "participant_id": "organisation-001",
  "text": "We want more young people to become involved in the festival."
}
```

------------------------------------------------------------------------

## 3. Interpretation

``` json
{
  "message": "interpretation",
  "context_id": "skordefest-sodra-oland-2026",
  "interpretation": {
    "current_focus": "Youth participation",
    "possible_desired_direction": "Increase meaningful participation by young people",
    "uncertainty": "medium"
  }
}
```

------------------------------------------------------------------------

## 4. Suggestions

The Engine may suggest several directions.

``` json
{
  "message": "suggestion",
  "context_id": "skordefest-sodra-oland-2026",
  "suggestions": [
    {
      "id": "suggestion-youth-001",
      "type": "exploration",
      "title": "Ask young people",
      "description": "Find out what they would actually like to do."
    },
    {
      "id": "suggestion-youth-002",
      "type": "opportunity",
      "title": "Connect existing capabilities",
      "description": "Look for existing businesses, artists, associations or activities that could be combined into something new."
    }
  ]
}
```

This illustrates that **opportunities and obstacles are not necessarily
separate information kinds**. They may be different ways of reasoning
about the same situation.

------------------------------------------------------------------------

## 5. Selection

``` json
{
  "message": "selection",
  "context_id": "skordefest-sodra-oland-2026",
  "participant_id": "organisation-001",
  "selected_id": "suggestion-youth-002"
}
```

------------------------------------------------------------------------

## 6. TransitionProposal

``` json
{
  "message": "transition_proposal",
  "context_id": "skordefest-sodra-oland-2026",
  "current": {
    "description": "Existing festival capabilities are not yet connected into a clear youth-oriented activity."
  },
  "desired": {
    "description": "A small youth-oriented activity exists and has been tested."
  },
  "proposal": {
    "description": "Combine existing local capabilities into one small pilot activity for young people."
  }
}
```

------------------------------------------------------------------------

## 7. Decision

``` json
{
  "message": "decision",
  "context_id": "skordefest-sodra-oland-2026",
  "participant_id": "organisation-001",
  "decision": "MODIFY",
  "modification": {
    "text": "The pilot should involve young people in designing the activity, not only participating in it."
  }
}
```

This is important: `MODIFY` means the proposal itself can evolve before
commitment.

------------------------------------------------------------------------

## 8. Updated Transition

The Engine returns the modified proposal.

``` json
{
  "message": "transition_proposal",
  "context_id": "skordefest-sodra-oland-2026",
  "proposal": {
    "description": "Co-design and test one small festival activity with young people."
  }
}
```

The participant can now accept it.

------------------------------------------------------------------------

## 9. Decision

``` json
{
  "message": "decision",
  "context_id": "skordefest-sodra-oland-2026",
  "participant_id": "organisation-001",
  "decision": "ACCEPT"
}
```

------------------------------------------------------------------------

## 10. Mission

``` json
{
  "message": "mission",
  "context_id": "skordefest-sodra-oland-2026",
  "mission": {
    "id": "mission-youth-001",
    "purpose": "Co-design a small youth-oriented festival activity.",
    "description": "Bring together a small group of young people and relevant local capabilities to design one pilot activity.",
    "definition_of_done": [
      "Young participants have been involved.",
      "A pilot activity has been defined.",
      "Responsibilities have been agreed.",
      "The pilot has been run or a concrete test has been completed.",
      "Observations have been recorded."
    ],
    "suggested_evidence": [
      "participant confirmation",
      "activity record",
      "survey or feedback",
      "optional GPS/location evidence"
    ]
  }
}
```

------------------------------------------------------------------------

# Example C --- GIVE UP

`GIVE UP` deserves its own example because it is semantically different
from the other decisions.

## Participant gives up

``` json
{
  "message": "decision",
  "context_id": "skordefest-sodra-oland-2026",
  "participant_id": "organisation-001",
  "decision": "GIVE_UP",
  "reason": "This is becoming too complicated."
}
```

The Engine should not simply generate another Mission.

It should enter **Reassessment**.

------------------------------------------------------------------------

## Engine reassesses

``` json
{
  "message": "reassessment",
  "context_id": "skordefest-sodra-oland-2026",
  "current_transition": "Co-design and test one small festival activity with young people.",
  "question": "What is happening?",
  "options": [
    {
      "id": "done",
      "label": "I'm done."
    },
    {
      "id": "change",
      "label": "The goal is still worth it, but this approach isn't."
    },
    {
      "id": "uncertain",
      "label": "I don't know anymore."
    },
    {
      "id": "challenge",
      "label": "Challenge me."
    }
  ]
}
```

## Challenge

If the participant selects `Challenge me`:

``` json
{
  "message": "challenge",
  "context_id": "skordefest-sodra-oland-2026",
  "description": "Forget the whole festival activity. Can you talk to one young person for 15 minutes and ask what would make them want to participate?"
}
```

This is deliberately smaller.

The Engine is not trying to manufacture motivation. It is reducing the
scope of the transition.

The participant may still decline.

------------------------------------------------------------------------

# What these examples are testing

The examples are intentionally testing several assumptions.

## 1. Same language, different domains

The individual case and the Skördefesten case use the same message
vocabulary.

There is no:

``` text
ImmigrantMission
FestivalMission
MunicipalityMission
```

The domain-specific content remains inside the generic conversation.

## 2. The participant can be different

The participant may be:

-   an individual
-   an organisation
-   a group
-   another actor

The protocol should not require the Engine to know the entire
domain-specific structure in advance.

## 3. The Engine proposes, the participant decides

AI-generated interpretation, suggestion and transition do not become
reality automatically.

## 4. Mission is the App boundary

The Engine can reason about a transition.

The App executes the Mission.

The App returns the result.

## 5. Evidence is deliberately open

The examples include several possible evidence forms, but do not freeze
the evidence model.

## 6. GIVE UP is a state change

`GIVE_UP` is not just another rejected suggestion.

It means:

``` text
current commitment
       ↓
loss of commitment
       ↓
reassessment
       ↓
stop / change / uncertainty / challenge
```

## 7. The loop can shrink

If a transition is too large, the Engine can propose a smaller
transition rather than creating a longer plan.

This supports the working principle:

> If the transition is too difficult, the current loop scope may be too
> large.

------------------------------------------------------------------------

# Deliberately Unresolved Questions

These examples expose questions that should be answered by the next
prototype iteration.

### Identity

Does `participant_id` eventually point to a generic Identity
representation, or is Identity represented differently?

### Context

Does every message need `context_id`, or can context be implicit in a
session?

### Suggestions

Should suggestions have stable IDs?

### Decisions

Should `MODIFY` create a new proposal ID or mutate the existing one?

### Missions

Does a Mission belong to exactly one Transition?

### Evidence

Should evidence be sent as part of `MissionResult`, or as separate
messages?

### Observations

Are observations distinct from evidence?

### AI

Should the Engine distinguish AI-generated content from system-generated
or user-generated content?

### Versioning

How can the App and Engine evolve independently without breaking the
conversation?

### Transport

Only after these questions are understood should we decide whether the
concrete representation should remain JSON and what transport mechanism
should carry it.

------------------------------------------------------------------------

# Prototype Rule

The concrete protocol should be allowed to change.

The purpose of this document is not to freeze the API.

It is to make the conversation sufficiently concrete that implementation
and testing can expose where the model is wrong.

> **The first protocol is an experiment, not a contract with the
> future.**
