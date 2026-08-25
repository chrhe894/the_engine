# Reality Check --- State of the Model v0.2

## Purpose

This is a checkpoint, not a final specification.

It records what we currently believe after the modelling and
prototype-design iterations, what has survived the examples, what has
changed, and what remains deliberately unresolved.

The purpose is to decide whether we are ready to move from conceptual
exploration into a very small prototype.

------------------------------------------------------------------------

# 1. Current Best Description

> **A generic mechanism for maintaining continuity around evolving
> intentions, Goals, actions, observations and evidence across people,
> organisations, places and time.**

This is our current working description, not a final product definition.

The domain is context rather than the identity of the system.

------------------------------------------------------------------------

# 2. Emerging Conceptual Stack

``` text
DOMAIN / REALITY
       │
       ▼
    CASE FILE
       │
       ├── Goal A
       ├── Goal B
       ├── Goal C
       └── ...
       │
       ▼
   MISSIONS / ACTIONS
       │
       ▼
 REALITY HAPPENS
       │
       ▼
 OBSERVATIONS / EVIDENCE
       │
       ▼
   CASE UPDATED
       │
       └──────────► NEXT LOOP
```

The App provides the human-facing interaction.

The Engine provides generic proposal/reasoning mechanisms.

The Case File provides continuity.

------------------------------------------------------------------------

# 3. What Has Survived Testing

## Genericity

The same broad mechanism has been applied to very different examples:

-   individual / occupational exploration
-   immigrant-related transition
-   Skördefesten / Södra Öland
-   geographically situated challenges
-   multiple simultaneous Goals

The model has not required a separate domain-specific Engine for each
example.

## Case File as Continuity

The Case File has become the central structural idea.

It provides continuity between:

-   turns
-   sessions
-   people
-   organisations
-   App
-   Engine
-   Missions
-   observations
-   evidence
-   time

It represents an evolving situation and its history rather than merely a
project plan.

## Multiple Goals

A Case File can contain several Goals simultaneously:

``` text
CASE FILE
│
├── Goal A — ACTIVE
├── Goal B — ACTIVE
├── Goal C — COMPLETED
└── Goal D — ABANDONED
```

Each Goal may have its own:

-   desired outcome
-   time limit
-   geographic scope
-   route / places
-   participants
-   constraints
-   Missions
-   Definition of Done
-   evidence requirements
-   lifecycle

## Local Goal Lifecycle

A Goal's lifecycle does not automatically control the Case File.

``` text
Goal A — ACTIVE
Goal B — ACTIVE
Goal C — ABANDONED
```

is valid.

Working principle:

> **Never allow a local Goal decision to implicitly become a Case File
> decision.**

The same distinction applies to Missions.

## Knowledge Survives Lifecycle Changes

An abandoned Goal can retain:

-   observations
-   evidence
-   decisions
-   reasons
-   history

Those results may later be relevant to other Goals.

Therefore:

> **Lifecycle state and accumulated knowledge are different things.**

## Tree vs Network

The App can use a tree for human orientation:

``` text
Vision
  ↓
Goal
  ↓
Mission
```

The underlying reality increasingly looks relational:

``` text
Goal
 ↔ Person
 ↔ Organisation
 ↔ Place
 ↔ Capability
 ↔ Mission
 ↔ Observation
 ↔ Evidence
 ↔ another Goal
```

Working principle:

> **Tree for orientation. Network for reality.**

We should not implement a graph prematurely.

## App vs Underlying Model

The App may show:

``` text
What are we working on?
       ↓
What could we explore?
       ↓
Your challenge
       ↓
What happened?
       ↓
What next?
```

while the underlying model may contain richer concepts such as:

``` text
Current Situation
Desired Direction
Goal
Mission
Decision
Definition of Done
Observation
Evidence
Reassessment
```

The user should not have to learn the model.

## Engine Proposes; User Decides

A useful working pattern is:

``` text
ENGINE
  ↓
PROPOSAL
  ↓
USER
  ├── ACCEPT
  ├── MODIFY
  ├── REJECT
  ├── EXPLORE FURTHER
  └── GIVE UP
```

`GIVE UP` is deliberately more significant than ordinary rejection, but
remains scoped to the relevant Goal unless the user explicitly abandons
the Case File.

## Missions Connect the Model to Reality

A Mission creates an opportunity for reality to provide new information:

``` text
Mission
   ↓
Reality
   ↓
Observation / Evidence
   ↓
Updated Case File
   ↓
New Proposal
```

## Definition of Done

A Mission or Goal can have a Definition of Done.

It may be simple:

``` text
Visit this place.
Complete the pilot.
Collect three responses.
Run for three months.
8 GPS-verified visits.
```

The important principle is:

> **Define what "done" means sufficiently to recognize completion.**

We do not need a universal KPI framework.

------------------------------------------------------------------------

# 4. What Has Changed

## From Transition Model Toward Continuity Mechanism

Attention has shifted from merely describing transition toward the
mechanism that maintains continuity while transition happens.

This includes:

``` text
Situation
Intentions
Goals
Actions
Observations
Evidence
Decisions
History
```

## From Single Goal Toward Multiple Living Goals

Testing showed that a Case File must support several Goals living
simultaneously.

## From Tree Toward Possible Network

The App tree remains useful, but we no longer assume the underlying
representation should be hierarchical.

## From Evidence Model Toward Evidence Capability

We deliberately stopped trying to define every evidence mechanism.

GPS, human confirmation, surveys, observations, system events and other
mechanisms may all become relevant.

The model needs to accept evidence; engineering can determine how
individual mechanisms work.

------------------------------------------------------------------------

# 5. What We Have Not Proven

## Conflicting Goals

Two Goals may genuinely compete.

## Multiple Organisations

Several organisations may own Goals, participate, provide evidence,
propose Missions, have different permissions, or disagree.

## Conflicting Observations

Two credible participants may report different things. The model should
not automatically collapse them into one "truth".

## Goal Dependencies

One Goal may depend on another:

``` text
Goal A
  prepare location
      ↓
Goal B
  run activity
```

This differs from Goals merely being related.

## Permissions and Access

Information may have different visibility for people and organisations.

This is important, but should not distort the conceptual model
prematurely.

## Case File Boundaries

Not yet tested:

-   merging Case Files
-   splitting Case Files
-   transferring ownership
-   creating a Goal from another Case File
-   one person participating in many Cases

## Geographic Complexity

We have discussed points, routes, polygons, cities, countries and local
areas, but have not yet established how geographic scopes relate.

------------------------------------------------------------------------

# 6. What We Should Not Turn Into Architecture Yet

Do not prematurely turn every useful concept into:

-   a database table
-   a class
-   an API resource
-   a UI component
-   a permanent ontology term
-   a graph node
-   a workflow engine
-   a microservice

A concept can be useful for thinking without becoming an implementation
object.

------------------------------------------------------------------------

# 7. Prototype Philosophy

The prototype is not intended to prove the final system is correct.

It is intended to **make the model encounter reality**.

> **Build only enough machinery to make the model encounter reality.**

The prototype should be small enough that changing the model remains
cheap.

------------------------------------------------------------------------

# 8. Smallest Useful Prototype

``` text
OPEN CASE
   ↓
USER INPUT
   ↓
CASE FILE UPDATE
   ↓
ENGINE PROPOSAL
   ↓
USER DECISION
   ↓
MISSION
   ↓
REALITY
   ↓
OBSERVATION / EVIDENCE
   ↓
CASE FILE UPDATE
   ↓
NEXT PROPOSAL
```

It does not need to solve production concerns.

------------------------------------------------------------------------

# 9. App ↔ Engine Boundary

Treat the first contract as a semantic conversation rather than a final
technical API.

Conceptually:

``` text
APP
  ↓
context + user input
  ↓
ENGINE
  ↓
proposal
  ↓
APP
  ↓
user decision
  ↓
ENGINE
  ↓
mission / next action
  ↓
APP
  ↓
result
  ↓
ENGINE
```

JSON is a plausible implementation format, but not yet a conceptual
requirement.

The important question is:

> **What information must cross the boundary?**

not:

> **What JSON schema should we freeze?**

------------------------------------------------------------------------

# 10. Role of the Existing App

The existing App is not being replaced.

It is the vehicle through which transition can happen.

It can provide mechanisms such as:

-   GPS
-   cards
-   places
-   challenges
-   surveys
-   user interaction
-   verification

The Engine can generate or coordinate generic content that the App
consumes.

The App can translate Engine output into its existing structures.

------------------------------------------------------------------------

# 11. Three Different Questions

### What is the user experiencing?

``` text
What are we working on?
What could we try?
Your challenge.
What happened?
What next?
```

### What is the Engine reasoning about?

``` text
Situation
Intentions
Goals
Possibilities
Decisions
Missions
Observations
Evidence
Reassessment
```

### What is the engineering implementation?

``` text
API
JSON
database
GPS service
authentication
AI
graph / relational storage
etc.
```

These three layers must not be confused.

------------------------------------------------------------------------

# 12. Current Best Picture

``` text
                         REALITY
                            │
                            ▼
                      OBSERVATIONS
                            │
                            ▼
                         EVIDENCE
                            │
                            ▼
                       CASE FILE
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
           GOAL A         GOAL B         GOAL C
             │              │              │
         lifecycle      lifecycle      lifecycle
             │              │              │
         Missions       Missions       Missions
             │              │              │
             └──────── relationships ─────┘
                            │
                            ▼
                          ENGINE
                            │
                         proposal
                            │
                            ▼
                           APP
                            │
                            ▼
                          USER
                            │
                            └──── decision ────►
```

This is our current conceptual picture, not implementation architecture.

------------------------------------------------------------------------

# 13. Current Confidence

### Strong

-   genericity across domains
-   Case File as continuity mechanism
-   multiple Goals
-   independent Goal lifecycles
-   App/model separation
-   Engine proposal / user decision
-   Mission → reality → observation loop
-   Definition of Done
-   tree as user representation

### Promising but not settled

-   network-like underlying structure
-   Goal-to-Goal relationships
-   richer evidence
-   geographic context
-   organisation participation
-   Case File boundaries

### Explicitly unresolved

-   final data model
-   final API
-   storage technology
-   AI architecture
-   graph vs relational implementation
-   permissions architecture
-   production evidence mechanisms

------------------------------------------------------------------------

# 14. What Would Falsify the Direction?

The direction would be in trouble if repeated real examples show that:

1.  radically different domains require fundamentally different Case
    File structures;
2.  Goal lifecycle cannot remain locally scoped;
3.  the App representation must dictate the underlying model;
4.  Missions cannot connect model decisions to reality;
5.  the Engine cannot propose useful next steps from Case File history;
6.  the generic mechanism becomes so complex that users must learn the
    methodology to use it.

These are meaningful failure conditions.

------------------------------------------------------------------------

# 15. Current Assessment

The model is **not finished**.

But it is sufficiently coherent to justify a prototype.

The reason is not that we know the final architecture.

It is that we now know enough about what must remain flexible to make a
small prototype without accidentally committing to the wrong
architecture.

------------------------------------------------------------------------

# 16. Next Gate

## LIVE CASE FILE PROTOTYPE

Use the prototype to run at least two real examples:

1.  Immigrant / occupational or integration-related example.
2.  Skördefesten / Södra Öland example.

Then deliberately introduce:

-   multiple simultaneous Goals
-   one abandoned Goal
-   a failed Mission
-   an unexpected observation
-   `MODIFY`
-   `REJECT`
-   `EXPLORE FURTHER`
-   `GIVE UP`
-   different geographic scopes
-   different time limits

When something breaks, first classify it:

``` text
MODEL PROBLEM?
UI PROBLEM?
APP CAPABILITY?
ENGINE REASONING?
APP ↔ ENGINE CONTRACT?
ENGINEERING PROBLEM?
```

Do not immediately repair every break.

The classification is itself part of the method.

------------------------------------------------------------------------

# 17. Current Working Identity

For now:

> **The Engine is a generic mechanism for helping people and
> organisations move from an evolving situation toward chosen change,
> while maintaining continuity of Goals, actions, observations and
> evidence across time.**

The App is the vehicle.

The Case File is the continuity mechanism.

The Engine is the generic mechanism.

The domain is context.

The user does not need to know any of this.

------------------------------------------------------------------------

# 18. Checkpoint

``` text
             EXPLORATION
                  │
                  ▼
        CONCEPTUAL MODEL
                  │
                  ▼
        EXAMPLES / TESTS
                  │
                  ▼
        REALITY CHECK  ← WE ARE HERE
                  │
                  ▼
        SMALL PROTOTYPE
                  │
                  ▼
       BREAK / LEARN / MODIFY
                  │
                  └──────► next loop
```

**Assessment: good enough to proceed.**

Not because the model is complete, but because it is now structured
enough to learn from implementation without pretending that
implementation is the answer.
