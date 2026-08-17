# Generic Information Model — Semantic Core Proposal

## Status

**Discovery — Phase 1**

This document records the current proposed semantic core after the
Configuration, Transition and Trajectory investigations.

It is a proposal for discussion, not yet the final `information-model.md`.

---

# 1. The Problem We Have Been Solving

We started with concepts such as:

- Identity
- Vision
- Goal
- Opportunity
- Obstacle
- Mission
- Decision
- Intention
- Situation
- Transition
- Observation

Testing them against OODA, ABCD, backcasting, strategic/tactical/operative,
software-development loops, matchmaking, the immigrant case, football,
Öland's Harvest Festival, district development and the "Peace on Earth"
case revealed a recurring pattern.

Many of these are not fundamental kinds of things.

They are **ways of interpreting, organising or operating on information**.

The information model therefore should not encode the vocabulary of every
method.

---

# 2. The Proposed Semantic Core

The smallest useful core currently appears to be:

```text
THING
  │
  │ participates in / is described by
  ▼
ASSERTION
  │
  │ organised within
  ▼
CONFIGURATION
  │
  │ may be changed by
  ▼
TRANSITION
  │
  ▼
CONFIGURATION
```

With:

```text
CONTEXT
```

as a cross-cutting dimension.

This gives us **four core semantic constructs plus Context**:

1. Thing
2. Assertion
3. Configuration
4. Transition

Everything else should first be treated as a role, interpretation,
relationship or operation over these constructs.

---

# 3. Reality Is Not an Information Type

This distinction is important.

The system does not contain Reality.

Reality is what the system is trying to understand and influence.

The system contains information **about** Reality.

Therefore:

```text
REALITY
   │
   │ observed / reported
   ▼
INFORMATION
   │
   ▼
MODEL
```

We should not create a `Reality` entity.

Likewise, the system should never silently confuse its model with reality.

---

# 4. Thing

A Thing is something that can participate in the situation being modelled.

Examples:

```text
Person
Business
Company
Football team
Festival
District
Building
Organisation
Place
Event
Capability
Resource
```

The model should not require a fixed universal taxonomy of Things.

A Thing can participate in many Relationships and Configurations.

---

# 5. Assertion

An Assertion is information that states something about Things or their
relationships.

Examples:

```text
Person A speaks Language X.

Person A knows Business Owner B.

Business Owner B runs a café.

Company C seeks a trainee.

Person A has completed a software project.
```

An Assertion should be able to retain relevant semantic context such as:

- source
- time
- provenance
- confidence
- scope
- whether it is observed, reported, inferred or projected
- other relevant contextual conditions

The exact representation is intentionally left open.

## Why Assertion instead of separate Statement and Observation?

Because:

```text
Statement
Observation
Inference
Projection
Intent
```

are increasingly looking like **different roles or epistemic modes of
information**, rather than fundamentally different structures.

For example:

```text
Observation:
"Company C offered Person A a trainee position."

Projection:
"Person A may become employable within six months."

Intention:
"Person A wants to become a software developer."
```

All express information about a possible relationship between Things,
Configurations or future conditions.

Their meaning differs in **status, provenance, modality and relationship
to reality**, not necessarily in their fundamental structure.

This is a hypothesis that now deserves implementation-level testing.

---

# 6. Context

Context determines how information should be interpreted.

Examples:

```text
time
location
organisation
event
scale
purpose
perspective
scenario
```

The same Assertion can have different meaning in different Contexts.

For example:

```text
"Team B is strong."
```

For one Intention this may be:

```text
Constraint
```

For another:

```text
Opportunity
```

For another:

```text
Reason to cooperate
```

Therefore the information model should store the underlying Assertion and
its relevant Context rather than permanently classifying it as an
Obstacle or Opportunity.

---

# 7. Configuration

A Configuration is a **coherent view of relevant information as a state or
arrangement**.

It is not necessarily a database object with fields.

It may be a projection over Assertions and Relationships.

Examples:

```text
Person A

programming capability
professional network
completed project
relationship with Company C
```

may constitute a Configuration that can be interpreted as:

```text
"emerging software developer"
```

Another Configuration might describe:

```text
District

active public spaces
participating businesses
local events
resident relationships
```

The same underlying information can participate in different
Configurations depending on Context and purpose.

---

# 8. Identity Is a Configuration Interpretation

Identity does not need to be a primitive type.

Identity answers:

> What does this Configuration mean about this Thing in this Context?

For example:

```text
Configuration
    programming capability
    portfolio
    work experience

        ↓

Identity interpretation

"junior software developer"
```

Therefore:

```text
Configuration → Identity interpretation
```

rather than:

```text
Thing → IdentityObject
```

This keeps Identity flexible across people, organisations, teams,
districts, events and other Things.

---

# 9. Projection

A Projection is not a fifth core data type.

It is a **derived assertion about a possible configuration or transition**.

Examples:

```text
If nothing changes, the district may become less attractive.

If Person A accepts the trainee opportunity,
Person A may gain relevant experience.

If the festival creates this cooperation,
visitor participation may increase.
```

The crucial distinction is:

```text
OBSERVATION
    = information about what happened / is observed

PROJECTION
    = information about what may happen
      under stated assumptions
```

Both can be represented as Assertions with different provenance,
temporality, modality and epistemic status.

This is one of the strongest simplifications discovered so far.

---

# 10. Continuation Is a Projection

"Doing nothing" is not a special Action.

Reality continues to evolve.

Therefore:

```text
Current Configuration
        │
        │ prevailing dynamics continue
        ▼
Continuation Projection
```

This gives us the baseline against which interventions can be evaluated.

The important comparison is:

```text
CONTINUATION PROJECTION
        vs.
INTERVENTION PROJECTION
```

This makes cost of inaction a normal part of reasoning.

---

# 11. Transition

A Transition represents meaningful change between Configurations.

Conceptually:

```text
Configuration A
       │
       │ Transition
       ▼
Configuration B
```

A Transition can involve multiple Things and multiple relevant
Configurations.

For example:

```text
Person A
Business B
Company C
```

may all change through one connected transition.

A Transition may be:

- possible
- selected
- intended
- planned
- performed
- observed as completed
- unsuccessful
- partially successful

These should **not automatically become different Transition types**.

They are semantic states or assertions about the Transition.

---

# 12. Candidate Transition

A Candidate Transition is simply a Transition being considered.

Example:

```text
Configuration A
       │
       ├── candidate Transition T1 → Configuration B
       ├── candidate Transition T2 → Configuration C
       └── candidate Transition T3 → Configuration D
```

The system can:

- generate candidates
- explore them
- compare them
- reject them
- revise them
- select one

This supports AI suggestions without making AI-generated suggestions into
facts.

---

# 13. Intention Is a Relationship / Assertion

A particularly strong hypothesis from the investigation is:

```text
Thing
  │
  └── intends → Configuration
```

For example:

```text
Person A
    intends →
        Configuration:
        capable of working as a software developer
```

This is cleaner than making Intention a large object.

The same pattern can support collective Intentions:

```text
Festival organisation
    intends → Configuration X

Business Owner B
    intends → Configuration Y
```

Conflicting Intentions are then simply different relationships to
different desired Configurations.

Their conflict becomes an interpretation relevant to a Transition or
Context.

---

# 14. Opportunity Is an Interpretation

An Opportunity is:

> an interpretation that some information or relationship may enable a
> useful Transition toward an Intention.

Example:

```text
Person A speaks Language X.
Business Owner B speaks Language X.
Business Owner B seeks young trainees.
Person A seeks software experience.

        ↓

Opportunity
```

The Opportunity does not need to be stored as a fundamental type.

It is a conclusion produced by reasoning over Assertions, Context,
Intentions and candidate Transitions.

---

# 15. Obstacle / Constraint Is an Interpretation

Likewise:

> a Constraint is information interpreted as limiting a contemplated
> Transition.

Example:

```text
Company C requires Swedish communication.

Person A currently has limited Swedish.

        ↓

Constraint for this Transition
```

But the same information could become an Opportunity for another
Transition.

Therefore:

```text
Opportunity / Constraint
```

should not be intrinsic classifications of the underlying Assertion.

---

# 16. Analysis and Synthesis

Analysis and Synthesis are operations over the semantic core.

## Analysis

```text
Configuration
      ↓
decompose
      ↓
Assertions / relationships / gaps / constraints
```

## Synthesis

```text
Assertions / relationships / capabilities
      ↓
combine
      ↓
Candidate Configuration / Transition
```

This is why both belong naturally in the reasoning layer rather than the
information model.

---

# 17. Mission

A Mission is an operational mechanism for inducing or testing a Transition.

Example:

```text
Candidate Transition:
Person A → meet Business Owner B

Mission:
Visit café and talk to Business Owner B.
```

The Mission does not need to be part of the semantic core.

It belongs to the operational layer.

The same Transition could be induced through different mechanisms.

---

# 18. Decision

A Decision is a selection or commitment.

It can be represented as an Assertion / event concerning a Transition or
Configuration.

Importantly:

> A Decision can itself constitute a Transition.

Example:

```text
"Proceed."

```

may immediately change the situation.

Therefore we should not require:

```text
Decision → Mission → Action → Transition
```

A more general model is:

```text
Decision
   │
   ├── may itself change Configuration
   │
   └── may initiate further Transitions
```

---

# 19. The Resulting Semantic Cycle

The current model can now be expressed without naming a methodology:

```text
                    REALITY
                       │
                       ▼
                  ASSERTIONS
                       │
                       ▼
                 CONFIGURATION
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
   continuation    candidate    desired
    projection     transitions configuration
          │            │
          │            ▼
          │        projections
          │            │
          └──────┬─────┘
                 ▼
              EVALUATE
                 │
               CHOOSE
                 │
                 ▼
             TRANSITION
                 │
                 ▼
               REALITY
                 │
                 ▼
             ASSERTIONS
                 │
                 └──────────→ next loop
```

This is not a workflow.

It is a semantic cycle.

The actual path through it depends on the situation.

---

# 20. What Happened to the Original Concepts?

The evolution of the model is now:

| Original concept | Current interpretation |
|---|---|
| Identity | Interpretation of Configuration |
| Vision | Desired / strategically relevant Configuration |
| Goal | Desired Configuration or Transition criterion |
| Intention | Assertion / relationship: Thing intends Configuration |
| Opportunity | Enabling interpretation |
| Obstacle | Constraining interpretation |
| Constraint | Contextual interpretation of information |
| Problem | Analytical framing |
| Solution | Candidate Configuration / Transition |
| Mission | Operational mechanism for Transition |
| Decision | Selection / commitment that may itself be a Transition |
| Observation | Assertion with observational provenance |
| Projection | Assertion about a possible future |
| OODA / ABCD / Backcasting | Methods / reasoning patterns over the core |
| Strategic / Tactical / Operative | Levels / perspectives over the same core |

This is exactly the direction we wanted:

> The external concepts remain useful, but the information model does not
> need to encode each one as a separate primitive.

---

# 21. The Minimal Core

The current best hypothesis is therefore:

## Core semantic constructs

### Thing

Something participating in the model.

### Assertion

Information about Things, Relationships, Configurations or possible
conditions.

### Configuration

A coherent view of relevant Assertions as a state / arrangement.

### Transition

Meaningful change involving Configurations.

## Cross-cutting dimension

### Context

The circumstances in which information and meaning are interpreted.

Everything else should initially be implemented as:

- relationships
- assertions
- interpretations
- projections
- operations
- views
- or application-layer mechanisms

rather than as new semantic primitives.

---

# 22. Why This May Be the Right Level of Abstraction

The model is generic enough to represent:

```text
person
football team
business
district
festival
organisation
community
```

without changing the semantic core.

It can support:

```text
problem solving
opportunity discovery
matchmaking
backcasting
OODA-like loops
ABCD-like processes
decision systems
software development
continuous improvement
```

without encoding those methods.

It can support AI reasoning because AI can operate on:

```text
Assertions
Configurations
Relationships
Contexts
Candidate Transitions
Projections
```

while keeping the user-facing experience simple.

And it preserves the principle:

> **The implementation must never define the information model.
> The information model defines the implementation.**

---

# 23. The Most Important Remaining Technical Question

We have probably reached the point where the semantic model is small enough
to begin designing the formal representation.

But one question must be resolved first:

> **How is a Configuration represented without becoming a traditional
> object with fields?**

The current hypothesis is:

```text
Configuration
    =
    a named/referable coherent view over Assertions
    within a Context
```

not:

```text
Configuration
    =
    object with predefined attributes
```

If this holds, the implementation can remain flexible:

```text
graph
documents
JSON
database
AI context
UI projections
```

can all be derived from the same semantic model.

---

# 24. Proposed Next Step

Do **not** create database tables yet.

Do **not** freeze JSON schemas yet.

Instead, define a tiny formal notation for the semantic core.

For example:

```text
Thing
Assertion
Context
Configuration
Transition
```

and test whether the immigrant, football, Öland and district cases can be
written in that notation.

The goal is to reach a point where we can say:

> **"This is the smallest language in which our problem can be expressed."**

Only after that should we let JSON, PlantUML, database structures and APIs
emerge from it.
