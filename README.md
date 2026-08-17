# Adaptive Navigation Engine

## Vision

<One paragraph describing the vision.>

---

## Repository Workflow

The repository is the single source of truth.

Ideas are discussed first.
Once agreed upon, they are documented before implementation begins.

```
BACKLOG
      ↓

CURRENT
      ↓

Documentation
      ↓

Review
      ↓

Implementation
      ↓

CHANGELOG
```

---

## Repository Structure

| File/Folder | Purpose |
|-------------|---------|
| README.md | Project overview and workflow |
| BACKLOG.md | Long-term roadmap |
| CURRENT.md | Current phase and immediate focus |
| CHANGELOG.md | Evolution of the model |
| docs/design | Design principles, assumptions and terminology |
| docs/spec | Formal specification |
| docs/project | Project vision, discoveries and decisions |

---

## Guiding Principle

The information model defines the implementation.

The implementation never defines the information model.

## Big picture model

@startuml
title Adaptive Change — Working Model

skinparam shadowing false
skinparam roundcorner 12

rectangle "CURRENT\nIDENTITY" as CI

rectangle "OBSTACLES\n\nWhat constrains or blocks\nthe transition?" as O

rectangle "OPPORTUNITIES\n\nWhat makes new possibilities\nvisible or possible?" as OP

rectangle "TRANSITION\n\nWhat actually changes\nIdentity?" as T

rectangle "NEW\nIDENTITY" as NI

rectangle "MOTIVATION\n\nWhy is this transition\nworth making?" as M

rectangle "FEEDBACK\n\nWhat tells us what\nchanged?" as F

CI --> T : transition
O --> T : constrains
OP --> T : enables
M --> T : drives
T --> NI : changes

NI --> F : observe change
F --> M : affects motivation
F --> CI : becomes current reality

note right of CI
Candidate primitive.

Questions:
- What constitutes Identity?
- Is Identity a state?
- Is Identity individual, collective,
  organizational, systemic?
- Which properties matter?
end note

note right of T
Candidate primitive.

Questions:
- Is Transition the fundamental
  mechanism of change?
- Can Transition contain many
  smaller transitions?
- Is Action a sub-brick of Transition?
- Is learning a type of Transition?
end note

note right of O
Candidate concept.

Questions:
- Is an Obstacle a thing,
  a relationship, or an interpretation?
- Can an obstacle become an opportunity?
end note

note right of OP
Candidate concept.

Questions:
- Can opportunities exist between actors?
- Is cooperation an opportunity,
  a mechanism, or an emergent capability?
end note

note right of NI
Potentially the same type as
CURRENT IDENTITY.

Hypothesis:

Identity₀ → Identity₁

rather than:

Current State → Ideal State
end note

note bottom of M
Important hypothesis:

Motivation may not be an object being
"managed". It may be an emergent property
of meaningful, appropriately sized transitions.
end note

@enduml

Next:

@startuml
title Adaptive Identity Transition Loop

start

partition "Current State" {
  :IDENTITY N;
}

partition "Context" {
  fork
    :OPPORTUNITY;

    note right
      Possibilities
      Cooperation
      Resources
    end note
  fork again
    :OBSTACLES / CONSTRAINTS;
  end fork
}

partition "Transition" {
  :MOTIVATION;

  note right
    Why is this transition
    worth making?
  end note

  :TRANSITION;
}

partition "Result" {
  :IDENTITY N+1;
}

partition "Feedback" {
  :FEEDBACK / OBSERVATION;
}

:Use feedback to update
understanding of current Identity;

-> IDENTITY N;

stop

@enduml

Next:

@startuml
title Adaptive Identity Transition Loop

while (Continue towards desired Identity?) is (yes)

  partition "Current Identity" {
    :IDENTITY N;
  }

  partition "Situation" {
    fork
      :OPPORTUNITIES;

      note right
        Possibilities
        Cooperation
        Resources
      end note
    fork again
      :OBSTACLES / CONSTRAINTS;
    end fork
  }

  :MOTIVATION;

  note right
    What makes the transition
    meaningful and worth pursuing?
  end note

  :TRANSITION;

  partition "Result" {
    :IDENTITY N+1;
  }

  partition "Feedback" {
    :FEEDBACK / OBSERVATION;
  }

endwhile (no)

stop
@enduml

Next:

@startuml
title Adaptive Identity Transition Loop

while (Continue towards desired Identity?) is (yes)

partition "Current Identity" {
  :IDENTITY N;

  note right
    Identity is context-dependent.

    May contain:
    - capabilities
    - knowledge
    - resources
    - relationships
    - context
    - behaviours
    - values
    - needs
    - aspirations

    The actual building blocks depend
    on what is being modelled.
  end note
}

partition "Situation" {
  fork
    :OPPORTUNITIES;

    note right
      Factors may include:

      - Possibilities
      - Cooperation / Samverkan
      - Matchmaking
      - Available resources
      - Available capabilities
      - Relationships
      - Unused capacity
      - Complementary needs
      - New combinations
      - Timing
      - External developments

      An Opportunity may exist between
      several identities.

      Matchmaking may discover an
      Opportunity by connecting:

      HAS / CAN PROVIDE
              ↕
      NEEDS / SEEKS
    end note

  fork again
    :OBSTACLES / CONSTRAINTS;

    note right
      Factors may include:

      - Legal issues
      - Regulations
      - Safety
      - Competition
      - Lack of resources
      - Lack of capabilities
      - Conflicting interests
      - Conflicting desired identities
      - Time constraints
      - Dependencies
      - Physical limitations
      - Social or organisational barriers

      An obstacle does not necessarily
      have to be solved.

      A viable transition may instead
      go around, through, or together
      with the constraint.
    end note

  end fork
}

:MOTIVATION;

note right
  What makes the transition
  meaningful and worth pursuing?

  Motivation may be influenced by:

  - Meaning
  - Expected progress
  - Challenge
  - Relevance to desired Identity
  - Autonomy
  - Feedback
  - Recognition
  - Social connection

  Hypothesis:

  The size of the transition should be
  appropriate to the current Identity.

  Too large → difficult to start.
  Too small → insufficiently meaningful.
end note

:TRANSITION;

note right
  A Transition changes one or more
  Identity building blocks.

  A Transition may affect:

  - one Identity
  - several identities
  - relationships between identities
  - a collective Identity

  A Mission / Task / Assignment is a
  possible concrete mechanism for
  inducing a Transition.

  The complete path toward the desired
  Identity does not need to be known
  in advance.
end note

partition "Result" {
  :IDENTITY N+1;

  note right
    Identity N+1 may differ in:

    - capabilities
    - knowledge
    - resources
    - relationships
    - context
    - behaviour
    - motivation
    - available opportunities

    The new Identity becomes the basis
    for the next loop.
  end note
}

partition "Feedback" {
  :FEEDBACK / OBSERVATION;

  note right
    Observe what actually changed.

    Feedback may reveal:

    - progress
    - unexpected effects
    - new opportunities
    - new obstacles
    - changed motivation
    - changed relationships
    - previously unknown capabilities
    - changed desired Identity

    Observations may be accumulated
    across loops for later analysis.
  end note
}

endwhile (no)

stop
@enduml

Next:

@startuml
title Generic Information Model — Working Concept

skinparam shadowing false
skinparam roundcorner 12

rectangle "THING" as Thing

rectangle "STATEMENT" as Statement

rectangle "OBSERVATION" as Observation

rectangle "INTENTION" as Intention

rectangle "RELATIONSHIP" as Relationship

rectangle "CONTEXT" as Context

rectangle "TRANSITION" as Transition

rectangle "MISSION" as Mission

Thing --> Statement : has / participates in
Statement --> Context : interpreted within
Observation --> Statement : describes
Intention --> Statement : desires
Relationship --> Thing : connects
Transition --> Thing : changes / involves
Mission --> Transition : induces

note right of Thing
  A person, organisation,
  place, resource, group,
  capability, etc.

  The information model does
  not prescribe the domain.
end note

note right of Statement
  A meaningful assertion
  about something.

  Example:

  Student
    seeks
  software experience
end note

note right of Context
  Time, perspective, domain,
  situation, source or other
  conditions under which
  information has meaning.
end note

note right of Transition
  Represents change from
  one configuration to another.

  May involve one or many
  Things simultaneously.
end note

note bottom of Statement
  Identity is a contextual
  projection of relevant
  Statements about a Thing.

  A "Brick" is a relevant
  aspect represented by such
  statements, not necessarily
  a universal data type.
end note

@enduml