# Generic Information Model

## Status

**Working concept — Phase 1**

This document defines the semantic information model of the system.

It does **not** define:

- database tables
- API resources
- UI components
- implementation classes
- programming-language types

The implementation must follow the information model.

The model is intentionally generic. It should be possible to represent
different domains without requiring domain-specific concepts to become
fundamental system types.

## Purpose

The information model provides a generic substrate for representing
situations, change and navigation between states.

It should be capable of representing, among other things:

- individuals
- organisations
- businesses
- events
- places
- communities
- capabilities
- resources
- relationships
- observations
- intentions
- transitions

The model supports the adaptive loop established during Phase 1:

    Identity N
        │
        ├── Opportunities
        ├── Obstacles / Constraints
        ├── Motivation
        │
        ▼
    Transition
        │
        ▼
    Identity N+1
        │
        ▼
    Feedback / Observation
        │
        └──────────────→ next transition

The complete path from a Current Identity to a Desired Identity does not
need to be known in advance.

## Design Principles

### Semantic model before implementation

The information model must describe meaning before implementation choices.

A database schema, API structure or programming-language model must not
be allowed to determine the semantic concepts.

### Generic before domain-specific

The information model should not require concepts such as software
developer, visitor, business owner, painter, student, festival or district
to become fundamental types.

These should be representable through the generic model.

### Interpretation before classification

Concepts such as Identity, Opportunity, Goal, Vision and Mission may be
interpretations or projections of underlying information rather than
mandatory primitive types.

### Time matters

Information may describe a situation at a particular point in time.

An observation is not necessarily a permanent truth.

The model should support change without requiring history to be overwritten.

## Working Hypothesis

The current hypothesis is that the system needs a small number of generic
information forms from which more specific concepts can be expressed.

The current candidate forms are:

- **Thing**
- **Statement**
- **Observation**
- **Intention**
- **Relationship**
- **Context**
- **Transition**

`Mission` is currently treated as a concrete mechanism for inducing a
Transition rather than necessarily as a fundamental information type.

Likewise, `Identity`, `Opportunity`, `Vision`, `Goal`, `Obstacle` and
`Constraint` are currently treated as higher-level interpretations of
information.

This is a working hypothesis, not a finalized ontology.

## Thing

A **Thing** is something that the system can refer to.

Examples include:

- a person
- an organisation
- a business
- a place
- an event
- a community
- a resource
- a group

The information model must not require a fixed universal taxonomy of Things.

A Thing may participate in relationships, be described by statements,
undergo transitions and be the subject of observations.

## Statement

A **Statement** expresses meaningful information about a Thing or about a
relationship between Things.

Examples:

    Student → knows → Python
    Student → seeks → software experience
    Café → provides → meeting space
    Business owner → can provide → mentorship
    Artist → seeks → exhibition space

A Statement may describe a capability, resource, need, preference,
relationship, characteristic, activity or another meaningful assertion.

The exact vocabulary used by a Statement should not be confused with a
fixed set of system types.

## Identity

Identity is a **context-dependent configuration of relevant information
about a Thing**.

Identity is therefore not necessarily a separate stored object.

A person's Identity in one context may be described by:

- capabilities
- knowledge
- resources
- relationships
- context
- behaviour
- values
- needs
- aspirations

Another Thing may require completely different building blocks.

A district, for example, may be described through safety, activity,
meeting places, culture, business vitality, accessibility and local
participation.

The relevant building blocks are discovered from the context.

### Identity building blocks

A "Brick" is a useful conceptual name for a relevant aspect of an Identity.

A Brick is not necessarily a universal data type.

A Brick may correspond to one or more Statements, Observations or
Relationships.

## Observation

An **Observation** records something observed about a Thing, relationship
or situation.

Conceptually an observation may include:

    subject
    aspect
    value
    time
    source
    context
    confidence

The exact structure remains open.

Observations are important because the system is intended to remain
adaptive.

A Transition may produce new observations, and those observations may
change the understanding of the current Identity.

Historical observations should not need to be overwritten merely because
the current understanding has changed.

## Intention

An **Intention** represents a desired direction, future state, outcome or
change.

Examples:

    Student → wants to become capable of → building software
    District → wants to become → more attractive
    Festival → wants to become → a more distinctive event

Intentions may be:

- explicit
- partial
- uncertain
- emerging
- revised during the process

An unresolved situation such as "I don't know what I want to do" is not
necessarily a missing-data error.

The system may use exploration to help an Intention emerge.

### Exploration and Emerging Intent

Exploration can itself be part of the transition process.

For example, a person may review a set of possible occupations and reject
those that are uninteresting or impossible.

    Unresolved Intent
          │
          ▼
       Exploration
          │
          ▼
    Candidate futures
          │
          ▼
      Emerging Intent
          │
          ▼
    Possible Desired Identity

The user remains the decision-maker.

AI may generate suggestions, comparisons or interpretations, but the user
selects the way forward.

## Relationship

A **Relationship** connects Things or connects a Thing to another relevant
piece of information.

Examples:

    Student → knows → Developer
    Café → located-at → Place
    Business → employs → Person
    Artist → seeks → Exhibition space

Relationships are particularly important for Opportunities and
matchmaking.

A potential Opportunity may emerge when:

    HAS / CAN PROVIDE
            ↕
       NEEDS / SEEKS

aligns across different identities.

This may involve two or many Things.

## Context

Information has meaning within a context.

Context may include:

- time
- place
- situation
- domain
- perspective
- source
- purpose
- other relevant conditions

Context is important because the same Thing may have different relevant
Identity building blocks in different situations.

The model should therefore avoid assuming that one universal description
fully defines an Identity.

## Transition

A **Transition** represents meaningful change from one configuration to
another.

    Identity N
        │
        │ Transition
        ▼
    Identity N+1

A Transition may affect:

- one Identity
- several Identities
- relationships between Identities
- a collective Identity

A Transition does not necessarily correspond to a long sequence of
actions.

In some situations the smallest meaningful Transition may be a decision.

A decision may:

- select one path among alternatives
- establish or change an Intention
- commit an Identity to a desired future
- enable subsequent transitions
- deliberately select non-action or waiting

The amount of subsequent work does not determine the conceptual size of
the Transition.

## Mission

A **Mission / Task / Assignment** is a possible concrete mechanism for
inducing a Transition.

Examples:

    Visit this address and talk to the business owner.
    Interview five people under twenty.
    Build a small working application.
    Bring an artist and a café owner together.

A Mission may affect multiple Identities simultaneously.

The external representation of a Mission should remain simple and
intuitive even if the internal reasoning around it is complex.

## Opportunity

An Opportunity is currently understood as a **potentially beneficial
possibility for transition**.

It may arise from:

- available capabilities
- resources
- relationships
- cooperation
- unused capacity
- complementary needs
- timing
- external developments
- matchmaking

An Opportunity may exist between multiple Identities.

Matchmaking is therefore currently considered a mechanism for discovering
Opportunities, not necessarily a fundamental information type.

## Obstacles and Constraints

Obstacles and Constraints restrict or complicate possible Transitions.

Examples include:

- legal issues
- regulations
- safety requirements
- competition
- lack of resources
- lack of capabilities
- conflicting interests
- conflicting desired identities
- time constraints
- dependencies
- physical limitations
- social or organisational barriers

An obstacle does not necessarily need to be solved.

A viable Transition may instead go around, through, or together with the
constraint.

External or normative constraints may exist outside an individual
Identity.

Their formal treatment remains an open question.

## Motivation

Motivation influences which Transitions are meaningful and worth pursuing.

Possible factors include:

- meaning
- expected progress
- challenge
- relevance
- autonomy
- feedback
- recognition
- social connection

A working hypothesis is that the size of a Transition matters.

A Transition that is too difficult may reduce motivation.

A Transition that is too trivial may fail to create meaningful progress.

The system should therefore investigate the smallest meaningful Transition
that moves the process forward.

Motivation is currently not treated as a fundamental information type.

## Feedback and Observation

After a Transition, the system observes what actually changed.

Feedback may reveal:

- progress
- unexpected effects
- new Opportunities
- new Obstacles
- changed Motivation
- changed Relationships
- previously unknown capabilities
- changed Intentions
- changed Desired Identities

The new situation becomes the basis for the next loop.

This means the system is not primarily a static planner.

It is intended to support continuous navigation through changing reality.

## Vision, Ideal State and Goal

These concepts remain useful in the human-facing vocabulary.

They are not currently defined as fundamental information types.

A possible interpretation is:

    Vision / Ideal State
            ↓
      Desired Identity
            ↓
    desired changes in relevant building blocks
            ↓
       possible Transitions
            ↓
          Missions

A Goal may describe a desired change or milestone in this chain.

These interpretations should remain open until the information model has
been tested further.

## Backcasting

Backcasting may be used to reason from a Desired Identity toward possible
intermediate states.

It does not imply that the entire path is known in advance.

    Desired Identity
          ↑
    Candidate intermediate Identity
          ↑
    Candidate intermediate Identity
          ↑
      Current Identity

The actual process then navigates forward through repeated observations and
Transitions.

The system should be able to revise the path when reality changes.

## Matchmaking

Matchmaking is considered a potentially central capability.

Given many Things and their relevant information, the system may discover
connections such as:

    Identity A
      NEEDS → X

    Identity B
      CAN PROVIDE → X

             ↓

         Opportunity
             ↓
        Possible Mission
             ↓
        Transitions in A and B

More complex Opportunities may involve several Things:

    A needs X
    B provides X but needs Y
    C provides Y

             ↓

      multi-actor Opportunity
             ↓
         shared Mission
             ↓
      multiple Transitions

The information model must therefore support relationships between many
participants without requiring special domain-specific types.

## AI as a Reasoning Participant

AI is considered an opportunity rather than a fundamental part of the
information model.

The system may use AI to:

- interpret information
- discover potential Opportunities
- suggest Transitions
- suggest Missions
- identify patterns
- generate alternatives
- ask useful questions
- compare candidate futures
- help form emerging Intent

The user remains responsible for selecting the way forward.

The information model must not depend on a specific AI provider or model.

The AI should reason over the information model rather than define it.

## Information Model Diagram

See [diagram](diagrams/information-model.puml).

The diagram is intentionally conceptual.

It must not be interpreted as a database schema.

## Open Questions

1. What is the smallest generic information form required?
2. Are Thing and Statement genuinely fundamental, or can they be reduced
   further?
3. How should values, measurements and qualitative characteristics be
   represented?
4. How should uncertainty and confidence be represented?
5. How should conflicting Statements be represented?
6. How should conflicting Intentions be represented?
7. How should external and normative Constraints be represented?
8. How should collective and multi-scale Identities be represented?
9. How should time and historical state be represented?
10. How should a Transition be represented without turning it into a
    conventional transaction record?
11. How should Missions relate to Transitions?
12. How should emerging Intent be represented?
13. How should Decisions be represented?
14. How should the model support matchmaking efficiently across thousands
    or millions of Things?
15. Which parts of this model should be directly visible to users?
16. Which information should remain internal to the reasoning engine?
17. What is the minimum representation that an AI needs in order to reason
    effectively over the model?
