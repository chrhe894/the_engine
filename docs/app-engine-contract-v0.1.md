# App ↔ Engine Contract --- Working v0.1

## Purpose

This document defines the **semantic conversation** between the existing
App and the Engine.

It deliberately does not prescribe JSON, REST, GraphQL, WebSockets,
event streaming, database structures, or AI providers.

First define **what the two sides need to communicate**. Select the
transport representation afterwards.

## Architectural Boundary

> **The App is the vehicle. The Engine is the adaptive reasoning
> mechanism. The protocol is the language between them.**

The App is responsible primarily for:

-   user interaction
-   presenting questions and suggestions
-   executing Missions
-   GPS and other device capabilities
-   collecting evidence and observations
-   communicating results

The Engine is responsible primarily for:

-   interpreting the current situation
-   identifying possible directions
-   suggesting opportunities and transitions
-   reasoning about obstacles and constraints
-   creating/recommending Missions
-   interpreting observations
-   proposing next transitions

The user remains the decision-maker.

## Core Conversation

``` text
ContextOpened
    ↓
UserInput
    ↓
Interpretation
    ↓
Question / Suggestion
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
Observation / Evidence
    ↓
NextStep
    ↓
next loop
```

## Messages

### App → Engine: ContextOpened

Communicates that a participant has entered an opened context.

``` text
ContextOpened
    context
    participant
```

### App → Engine: UserInput

The user's current input.

``` text
UserInput
    context
    participant
    text
```

The input may be unstructured. The Engine must not require a fully
structured Identity before the conversation can begin.

### Engine → App: Interpretation

The Engine communicates its current understanding.

``` text
Interpretation

Current focus:
    Festival attractiveness

Possible desired direction:
    Attract more young visitors

Uncertainty:
    High
```

Interpretations are suggestions and may be corrected by the user.

### Engine → App: Question

The Engine may request clarification whenever uncertainty matters.

Example:

> Do you mean attracting young visitors as tourists, or getting more
> young people from Öland involved?

### Engine → App: Suggestion

The Engine may suggest questions, opportunities, obstacles to explore,
possible directions, or possible transitions.

A suggestion is not a decision.

### App → Engine: Selection

The participant selects a suggestion or direction.

The Engine must distinguish user selection from AI-generated suggestion.

### Engine → App: TransitionProposal

A candidate change from the current situation toward a desired future.

``` text
Current:
    Festival has limited engagement with young visitors.

Desired:
    Festival has meaningful youth participation.

Proposed transition:
    Create and test one youth-oriented festival activity.
```

### App → Engine: Decision

The participant explicitly chooses what to do.

Possible decisions:

``` text
ACCEPT
MODIFY
REJECT
EXPLORE FURTHER
GIVE UP
```

`GIVE UP` is intentionally different from `REJECT`.

### Engine → App: Mission

A concrete executable step belonging to a chosen Transition.

Conceptually:

``` text
Mission
    id
    purpose
    description
    DefinitionOfDone
    suggested evidence
    context
    status
```

This is a conceptual contract, not a commitment to a database table.

### App → Engine: MissionResult

Reports what happened.

``` text
MissionResult
    mission
    status
    evidence
    observation
```

Evidence may include GPS confirmation, participant confirmation, another
person's verification, survey response, system observation, or
self-report.

The prototype does not need to settle the evidence architecture.

### Engine → App: NextStep

The Engine interprets the new situation and offers possible next
transitions.

``` text
Observation:
    Youth participation increased.

Possible next transitions:
    1. Repeat activity at larger scale.
    2. Develop three additional activities.
    3. Investigate why some youth did not participate.
    4. Stop — sufficient improvement achieved.
```

The participant chooses.

## GIVE UP

`GIVE UP` is not an ordinary rejection.

`REJECT` means:

> I reject this particular proposal.

`GIVE UP` means:

> I want to disengage from the current transition as currently framed.

It therefore triggers a **Reassessment**.

The Engine may ask:

``` text
You're about to give up. That's okay.

What is happening?

1. I'm done.
2. The goal is still worth it, but this approach isn't.
3. I don't know anymore.
4. Challenge me.
```

If the participant explicitly chooses `CHALLENGE ME`, the Engine may
offer one deliberately small challenge.

The purpose is not generic motivation. It is to test whether the current
transition can be reduced to a manageable next step.

This may produce a **micro-transition** or micro-mission.

Giving up remains a legitimate outcome.

> **It's never too late to give up.**

## Important Principle

> The Engine proposes. The user decides.

AI-generated interpretations, suggestions and transitions are not
automatically adopted.

## API vs Information Model

The protocol is not the Information Model.

The Information Model describes what the Engine needs to understand.

The App ↔ Engine contract describes what needs to cross the boundary.

The two are related but deliberately not identical.

## Open Questions

-   JSON or another representation?
-   Request/response API or event-based communication?
-   Which messages require stable identifiers?
-   Which messages are persisted?
-   Authentication and permissions?
-   Partial/offline App operation?
-   Contract versioning?
