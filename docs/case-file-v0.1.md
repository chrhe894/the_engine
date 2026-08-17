# Case File --- Working Concept v0.1

## Purpose

The **Case File** is the continuity mechanism for an evolving
transition.

It allows the work to continue across:

-   turns
-   sessions
-   time
-   participants
-   individuals
-   organisations
-   App and Engine
-   different activities and Missions

The Case File is not primarily a database concept.

It is a **semantic concept**: a persistent representation of what is
being worked on, what is currently understood, what has been decided,
what has happened, and what remains possible.

Where the Case File is physically stored is an engineering question and
is deliberately left open.

------------------------------------------------------------------------

# 1. Core Idea

A Case File represents an evolving situation.

``` text
Case File at t0
      ↓
Decision
      ↓
Mission
      ↓
Reality happens
      ↓
Evidence / Observation
      ↓
Case File changes
      ↓
New situation
      ↓
Next decision
```

The Case File therefore should not be regarded as a static record of an
original plan.

> **The Case File is a living representation of the transition.**

It may contain things that are:

-   established
-   observed
-   decided
-   proposed
-   uncertain
-   rejected
-   completed
-   abandoned
-   superseded

These states must not be confused.

------------------------------------------------------------------------

# 2. Relationship to the App and Engine

The App and Engine may both work with the same Case File.

They do not necessarily own the same information.

``` text
                         CASE FILE
                             │
              ┌──────────────┴──────────────┐
              │                             │
             APP                          ENGINE
              │                             │
      situated knowledge             reasoning
      execution                      interpretation
      device capabilities            transitions
      local state                    suggestions
      user interaction               adaptation
              │                             │
              └──────────────┬──────────────┘
                             │
                       shared continuity
```

The App may contribute:

-   current user/context information
-   location
-   available capabilities
-   completed Missions
-   GPS confirmations
-   survey responses
-   user interaction
-   locally available cards or challenges

The Engine may contribute:

-   interpretations
-   questions
-   suggested directions
-   opportunities to explore
-   obstacles to explore
-   Transition proposals
-   Mission proposals
-   reassessments
-   suggested next steps

Both may contribute observations and changes initiated by their
respective roles.

------------------------------------------------------------------------

# 3. Case File Structure

A conceptual Case File may contain:

``` text
CASE FILE
│
├── Context
│   ├── Time
│   ├── Geography
│   └── Participants
│
├── Current Situation
│
├── Vision
│
├── Goals
│   ├── Goal A
│   │   ├── Mission 1
│   │   └── Mission 2
│   │
│   └── Goal B
│
├── Transitions
│
├── Decisions
│
├── Observations
│
├── Evidence
│
└── History
```

This is a conceptual view, not a required database structure.

The existing App structure of:

``` text
Vision
  ↓
Goals
  ↓
Missions / Challenges
```

should be treated as an existing and important structural component
rather than replaced by a new Engine-specific hierarchy.

------------------------------------------------------------------------

# 4. Context

The Context establishes where and when the Case File applies.

It may contain:

-   geographic scope
-   time scope
-   opening question
-   participating actors
-   access/permissions
-   contextual description

Examples:

``` text
Södra Öland
    defined period
    festival-related context
```

or:

``` text
Individual participant
    ongoing
    personal transition
```

A Case File can therefore represent both an individual and a
multi-organisation situation.

------------------------------------------------------------------------

# 5. Current Situation

The Case File should maintain a representation of the current situation.

This is not necessarily objective truth.

It may contain:

-   observed conditions
-   participant descriptions
-   interpretations
-   known constraints
-   uncertainties
-   relevant circumstances

Important distinction:

``` text
FACT / OBSERVATION
        ≠
INTERPRETATION
        ≠
ASSUMPTION
```

The Case File should be able to preserve these distinctions.

Example:

``` text
Observation:
    Only 12 young people participated.

Interpretation:
    Young people may not find the current activities attractive.

Assumption:
    A co-designed activity may increase participation.
```

This allows the Case File to evolve without silently turning hypotheses
into facts.

------------------------------------------------------------------------

# 6. Vision

Vision represents a desired future state at an appropriate level.

It may be broad and long-lived.

Example:

> Make Södra Öland an even better place to live, work and visit.

Or:

> Become capable of working as a software developer.

A Vision does not necessarily describe the next action.

It provides direction.

------------------------------------------------------------------------

# 7. Goals

Goals provide more specific desired states within a Vision.

Example:

``` text
Vision
    Make Södra Öland an even better place to live,
    work and visit.

Goal
    Increase meaningful youth participation
    in the festival.
```

A Goal may change as understanding develops.

A Goal is therefore not necessarily permanent.

------------------------------------------------------------------------

# 8. Transitions

A Transition describes movement from a current state toward a desired
state.

Conceptually:

``` text
CURRENT
   │
   │ transition
   ▼
DESIRED
```

Example:

``` text
Current:
    Young people have limited involvement.

Desired:
    Young people participate in designing
    and running an activity.

Transition:
    Co-design and test one small activity.
```

Transitions are where the system moves from **understanding** toward
**doing**.

------------------------------------------------------------------------

# 9. Missions / Challenges

A Mission or Challenge is an executable part of a Transition.

The existing App already has mechanisms for Missions and Challenges.

The Engine should therefore be able to propose a Mission in a form that
the App can understand and execute.

A Mission should normally include a **Definition of Done**.

Example:

``` text
Mission:
    Talk to one software developer.

Definition of Done:
    - conversation completed
    - three questions asked
    - reflection recorded
```

or:

``` text
Mission:
    Test a youth-designed festival activity.

Definition of Done:
    - young participants involved
    - pilot activity defined
    - test completed
    - observations recorded
```

------------------------------------------------------------------------

# 10. Definition of Done

A Definition of Done describes what must be true for a Mission,
Transition, Goal, or potentially an entire Case File phase to be
considered complete.

It may contain:

-   observable conditions
-   evidence requirements
-   participant confirmation
-   measurements
-   time limits
-   completion criteria
-   qualitative judgments

It does not have to be complicated.

A Definition of Done may simply be:

> Complete the activity before 30 September.

Or:

> Three people have independently confirmed that the Mission was
> completed.

The Case File should preserve the Definition of Done that was in force
when the work was undertaken.

This is important because the Definition of Done itself may later
change.

------------------------------------------------------------------------

# 11. Decisions

The Case File should preserve significant decisions.

Examples:

``` text
ACCEPT
MODIFY
REJECT
EXPLORE FURTHER
GIVE UP
```

A decision should not be confused with a suggestion.

``` text
Engine suggestion
       ↓
Participant decision
       ↓
Case File change
```

This preserves the principle:

> **The Engine proposes. The user decides.**

------------------------------------------------------------------------

# 12. GIVE UP and Reassessment

`GIVE UP` is a special decision because it changes the commitment to the
current Transition.

It should trigger reassessment rather than simply remove the Transition.

Possible outcomes:

``` text
GIVE UP
   │
   ├── Stop
   │
   ├── Change the approach
   │
   ├── Reconsider the goal
   │
   └── Challenge me
          │
          ▼
     smaller transition
```

A genuine decision to stop must remain valid.

The system should not treat persistence as inherently better than
stopping.

> **It's never too late to give up.**

------------------------------------------------------------------------

# 13. Observations

An Observation records what was learned or perceived as a result of
something happening.

Examples:

-   participant reflection
-   survey response
-   measured outcome
-   discovered obstacle
-   newly identified opportunity
-   failed Mission
-   unexpected event

An Observation can change the Case File's understanding.

Example:

``` text
Previous assumption:
    Young people are not interested.

Observation:
    Young people were highly interested,
    but could not participate at the available times.

Updated understanding:
    Timing may be a larger obstacle than interest.
```

This is one of the main mechanisms through which the Case File evolves.

------------------------------------------------------------------------

# 14. Evidence

Evidence supports a claim or completion.

Evidence may come from many mechanisms.

Examples:

-   GPS
-   participant confirmation
-   another person's verification
-   survey response
-   system event
-   document
-   measurement
-   photograph
-   observation
-   time-based completion

The exact Evidence architecture remains deliberately open.

The principle is:

> **Evidence is a mechanism for establishing confidence, not a single
> fixed data type.**

------------------------------------------------------------------------

# 15. History

The Case File should preserve enough history to understand how the
current situation came to be.

History may include:

-   previous interpretations
-   decisions
-   completed Missions
-   rejected proposals
-   changed Goals
-   changed Definitions of Done
-   observations
-   evidence
-   reassessments

History is important because a current state without its path can be
misleading.

For example:

``` text
Current Goal:
    Increase youth participation.
```

does not explain that:

``` text
Original Goal:
    Increase visitor numbers.

Observation:
    Visitor numbers were already high.

Reassessment:
    Quality of participation became more important.

New Goal:
    Increase meaningful youth participation.
```

The history preserves that evolution.

------------------------------------------------------------------------

# 16. Current State vs History

The Case File should distinguish between:

### Current

What the system currently believes/knows/has committed to.

### Historical

What was previously believed, proposed, decided, completed or rejected.

For example:

``` text
CURRENT

Goal:
    Increase youth participation.


HISTORY

Previous Goal:
    Increase total visitor numbers.

Previous Transition:
    Create more advertising.

Decision:
    Rejected.

Observation:
    Awareness was not the main obstacle.
```

A historical item should not silently become current again merely
because it exists in the Case File.

------------------------------------------------------------------------

# 17. Provisional Information

Not everything in a Case File has the same confidence.

The Case File should be capable of distinguishing:

``` text
confirmed
observed
reported
interpreted
assumed
proposed
uncertain
rejected
superseded
```

The exact vocabulary is not yet fixed.

The important principle is that **uncertainty must be representable**.

This is especially important for Engine-generated interpretations.

------------------------------------------------------------------------

# 18. Case File Evolution

A Case File evolves through a loop.

``` text
CURRENT SITUATION
       │
       ▼
UNDERSTANDING
       │
       ▼
POSSIBLE TRANSITIONS
       │
       ▼
DECISION
       │
       ▼
MISSION
       │
       ▼
REALITY
       │
       ▼
OBSERVATION / EVIDENCE
       │
       ▼
UPDATED CASE FILE
       │
       └──────────────► next loop
```

This is the continuity mechanism.

------------------------------------------------------------------------

# 19. App ↔ Engine Update Pattern

The conceptual interaction may therefore become:

``` text
APP
 │
 │ current Case File state
 │ + new event / observation
 ▼
ENGINE
 │
 │ reasoning
 │
 ▼
proposed Case File changes
 │
 ▼
APP / participant
 │
 │ decision / execution
 ▼
updated Case File
```

The Engine should not silently overwrite the Case File.

Where a meaningful decision is required, the participant remains the
authority.

------------------------------------------------------------------------

# 20. Multiple Participants

A Case File may involve many participants.

Example:

``` text
CASE FILE: Youth participation at Skördefesten

Participants:
    festival organisation
    municipality
    local businesses
    associations
    young people
    visitors
```

Different participants may contribute different:

-   observations
-   intentions
-   capabilities
-   evidence
-   decisions

The Case File provides continuity across those contributions.

This is one reason the concept must not be reduced to a personal task
list.

------------------------------------------------------------------------

# 21. Multiple Organisations

The same Case File may span organisational boundaries.

For example:

``` text
Municipality
     +
Festival organisation
     +
Local business
     +
Association
     +
Individual participants
```

The Case File does not require all participants to have the same role or
internal system.

Access and visibility remain separate engineering concerns.

------------------------------------------------------------------------

# 22. What the Case File Is Not

The Case File is not:

-   merely a task list
-   merely a project plan
-   merely a CRM record
-   merely an AI conversation history
-   merely a Mission tree
-   merely a database record
-   merely a collection of documents

It can contain aspects of all of these, but its defining purpose is:

> **maintaining continuity of an evolving transition across time,
> participants and system boundaries.**

------------------------------------------------------------------------

# 23. What Is Deliberately Not Decided

This document does not decide:

-   physical storage
-   database technology
-   replication strategy
-   synchronization protocol
-   API transport
-   authentication
-   authorization implementation
-   event sourcing
-   versioning mechanism
-   conflict-resolution implementation
-   AI provider
-   exact JSON schema

Those are engineering decisions.

The semantic concept comes first.

------------------------------------------------------------------------

# 24. Prototype Questions

The first prototype should test whether this Case File concept is
actually useful.

Questions to test:

1.  Can the same Case File support the immigrant example and
    Skördefesten?
2.  Can the App maintain its existing Vision → Goals →
    Missions/Challenges structure without being replaced?
3.  Can the Engine add interpretations and proposed transitions without
    owning the whole Case File?
4.  Can an observation change a Goal or Transition?
5.  Can a failed Mission be useful rather than simply marked as failure?
6.  Can `GIVE UP` cause a meaningful reassessment?
7.  Can several participants contribute without turning the Case File
    into an administrative monster?
8.  Can the Case File remain understandable to a human?
9.  Can the same Case File survive multiple sessions?
10. Can the App and Engine work with the Case File without either one
    needing to know the other's internal implementation?

------------------------------------------------------------------------

# 25. Working Definition

> **A Case File is the persistent, evolving representation of a
> situation and its transition through time. It connects context,
> understanding, vision, goals, transitions, missions, decisions,
> observations and evidence, allowing the App, Engine and participants
> to maintain continuity without requiring them to share the same
> internal implementation.**

This is a working concept, not a final specification.

The next prototype should be allowed to change it.
