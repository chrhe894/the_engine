# Information Model — Configuration and Transition Test

## Status

**Discovery — Phase 1**

This document tests the current Configuration hypothesis against the
remaining semantic distinctions:

- current configuration
- candidate configuration
- desired configuration
- historical configuration
- intention
- possible transition
- selected transition
- mission
- actual transition
- observation
- resulting configuration

The purpose is to see whether these can be expressed without introducing
a collection of special-purpose primitives.

---

# 1. Working Hypothesis

The current hypothesis is:

> **Configuration is a meaningful arrangement of information that can
> describe a current, possible, desired or historical state.**

A Configuration is not necessarily a database entity.

It may be represented through a set of Statements, Relationships and
Context.

Identity is interpreted from a relevant Configuration.

Intention expresses a desired relationship to a Configuration.

Transition represents change between Configurations.

---

# 2. Current Configuration

Example:

```text
Person A

speaks → Language X
limited Swedish
limited professional network
seeks → direction
```

These Statements and Observations form the information from which the
current Identity can be understood.

Conceptually:

```text
Person A
    │
    └── current Configuration
```

## Result

**PASS**

No special `CurrentState` type is required.

"Current" appears to be contextual semantics rather than a separate kind
of information.

---

# 3. Historical Configuration

Suppose that later Person A has:

```text
software-development experience
professional network
completed project
```

We may still need to reason about the earlier state:

```text
before:
    no software-development experience
```

The same semantic structure can represent the earlier Configuration if the
relevant Statements / Observations are associated with time and Context.

Conceptually:

```text
Configuration A
    │
    │ time
    ▼
Configuration B
```

## Result

**PASS conceptually**

But this exposes a requirement:

> Temporal semantics must be first-class enough to reconstruct relevant
> historical configurations.

We should not solve this yet by creating a `HistoricalConfiguration` type.

---

# 4. Candidate Configuration

Example:

```text
Candidate A:
    Person A becomes electrician

Candidate B:
    Person A becomes software developer

Candidate C:
    Person A starts a technical education
```

These are not current.

They are not necessarily desired.

They are possibilities under consideration.

Conceptually:

```text
Current Configuration
        │
        ├── possible → Candidate A
        ├── possible → Candidate B
        └── possible → Candidate C
```

## Result

**PASS — with one important qualification**

We need a way to identify the candidate Configuration as a unit.

A loose collection of Statements is not sufficient if several alternatives
contain overlapping information.

This suggests that a Configuration may need to be **referable as a
configuration**, even if it is not a domain-specific object type.

---

# 5. Desired Configuration

Suppose Person A selects:

> Become a software developer.

We can express:

```text
Person A
    intends → Configuration B
```

where Configuration B contains the relevant desired arrangement.

For example:

```text
capable-of → software development
has → portfolio
has → professional experience
has → professional network
```

The desired configuration need not be completely specified.

## Result

**PASS**

This is a particularly clean representation:

```text
THING
  │
  └── intends → CONFIGURATION
```

This is currently one of the strongest hypotheses in the model.

---

# 6. Configuration Is Not Necessarily Identity

The distinction is useful.

A Configuration describes an arrangement of information.

Identity is an interpretation of that arrangement relative to a Thing and
Context.

For example:

```text
Configuration:

programming capability
portfolio
professional relationship
work experience

          ↓

Identity interpretation:

"junior software developer"
```

Therefore:

```text
Configuration
      ↓ interpretation
   Identity
```

## Result

**PASS**

This allows Identity to remain generic and context-dependent.

---

# 7. Possible Transition

Suppose we have:

```text
Current Configuration A
Desired Configuration B
```

We can reason about possible ways of getting from A to B.

A candidate Transition can therefore be represented conceptually as:

```text
Configuration A
       │
       └── possible Transition → Configuration B
```

The Transition is not yet performed.

## Result

**PASS conceptually**

This is potentially much simpler than defining Transition as a large
workflow object.

---

# 8. Multiple Possible Transitions

There may be several ways to reach the same Configuration:

```text
Current A
   │
   ├── Transition T1 → B
   ├── Transition T2 → B
   └── Transition T3 → B
```

For the software developer example:

```text
T1:
formal university education

T2:
vocational education

T3:
self-study + projects + trainee relationship

T4:
employment-based learning
```

The system can analyse and compare these.

This is important because the desired Configuration does not determine a
single path.

## Result

**PASS**

This supports the distinction between:

```text
desired Configuration
```

and:

```text
candidate Transition
```

---

# 9. Transition Can Also Change Several Things

The business owner example demonstrates:

```text
Person A
Business Owner B
Company C
```

may all change through related Transitions.

For example:

```text
Person A
    gains relationship / experience

Business Owner B
    gains trainee network

Company C
    gains potential trainee
```

Therefore a Transition may involve multiple Things and may transform more
than one relevant Configuration.

## Result

**PASS**

The Transition must not be modelled as a simple:

```text
one object → one new state
```

relationship.

It is potentially multi-participant.

---

# 10. Selected Transition

Before action, the user may select:

```text
T3:
self-study + projects + trainee relationship
```

Selection is not necessarily a new kind of Transition.

It changes the status / relevance of an existing candidate.

Conceptually:

```text
candidate Transition
       │
       └── selected
```

The system should preserve the alternatives that were considered.

This is important for later learning:

> Which alternatives were considered, and why was one selected?

## Result

**PASS conceptually**

But again, "selected" should not immediately become a hard-coded
`SelectedTransition` type.

---

# 11. Mission as Mechanism

Suppose T3 requires:

```text
Visit Business Owner B.
Talk about trainee possibilities.
```

This is a Mission.

The Mission is not identical to the desired Configuration or the
Transition.

It is a **mechanism for inducing or testing a Transition**.

Conceptually:

```text
Candidate Transition
       │
       └── Mission
              │
              ▼
             Action
```

## Result

**PASS**

This preserves our earlier distinction.

---

# 12. Actual Transition

The Mission is performed.

The person meets the business owner.

A relationship is established.

The person receives a software-related task.

Reality has changed.

We now have:

```text
Configuration A
       │
       │ actual Transition
       ▼
Configuration A'
```

This may not yet equal the Desired Configuration B.

That is important.

A Transition can move the process **toward** a desired Configuration
without reaching it.

## Result

**PASS**

This supports the original Identity N → Identity N+1 loop.

---

# 13. Observation of the Transition

After the Mission:

```text
Person A met Business Owner B.
Business Owner B offered an introduction.
Company C may need a trainee.
Person A completed a small coding task.
```

These become Observations.

The Observations provide evidence for the resulting Configuration.

Conceptually:

```text
Transition
    │
    ▼
Observation
    │
    ▼
resulting Configuration
```

## Result

**PASS conceptually**

But this exposes an important distinction:

> A Configuration is an interpretation of information, while an
> Observation is evidence about what happened.

This distinction should remain explicit.

---

# 14. Verification

Suppose the Mission was:

> Interview five people under 20.

Verification asks:

```text
Were five interviews actually completed?
```

The answer may be:

```text
4 completed
1 cancelled
```

The Transition did not produce the intended result.

This is an Observation about the Transition.

## Result

**PASS**

Verification does not require a new information primitive.

---

# 15. Validation

Suppose all five interviews happened.

Validation asks:

> Did this activity actually contribute to the intended change?

Perhaps:

```text
5 interviews completed
but no useful relationships resulted.
```

Or:

```text
5 interviews completed
and two promising trainee relationships emerged.
```

Verification and Validation therefore generate different interpretations
of observations.

They need not become separate information types.

## Result

**PASS**

---

# 16. Resulting Configuration

After several transitions:

```text
Person A

programming capability
completed projects
professional network
relationship with Company C
some Swedish workplace experience
increased confidence
```

This is now a new Configuration.

It may support a new Identity interpretation:

```text
"emerging software developer"
```

The process continues.

```text
Configuration N
       │
       ▼
Transition
       │
       ▼
Configuration N+1
       │
       ▼
new Identity interpretation
       │
       ▼
new Intent / revised Intent
```

## Result

**PASS**

---

# 17. Can We Eliminate Configuration?

This is an important counter-test.

Could we represent everything using only:

```text
Thing
Statement
Observation
Relationship
Context
Intention
Transition
```

without Configuration?

Possibly.

A Configuration could be represented as a Contextual grouping or projection
of Statements.

However, the concept is useful because it gives us a name for something
the system repeatedly needs to reason about:

> a coherent arrangement of information considered as a state.

Therefore the question is not whether Configuration is a database type.

The question is whether **Configuration is a necessary semantic concept**.

Current answer:

**Probably yes.**

---

# 18. Can We Eliminate Intention?

An Intention can potentially be represented as:

```text
Thing
    └── intends → Configuration
```

This suggests that Intention itself may not need to be a fundamental
information form.

It could be a particular kind of Relationship.

This is an important simplification.

The existing `Intention` concept in the working model may therefore be too
high-level.

---

# 19. Can We Eliminate Mission?

Mission may similarly be:

```text
Transition
    └── induced / tested by → Action mechanism
```

or:

```text
Transition
    └── operationalised as → Mission
```

This suggests Mission belongs closer to the operational layer than to the
semantic core.

It may not belong in the primitive information model at all.

---

# 20. Emerging Semantic Core

The current investigation suggests a possible core smaller than the
original seven candidate forms.

### Candidate semantic core

```text
THING
  │
  ├── participates in
  │
  ▼
CONFIGURATION
  │
  │ changes through
  ▼
TRANSITION
  │
  ▼
CONFIGURATION
```

Surrounding these:

```text
STATEMENT
RELATIONSHIP
OBSERVATION
CONTEXT
```

And higher-level concepts may be expressed through them:

```text
Identity       = interpretation of Configuration
Intention      = Thing → intends → Configuration
Opportunity    = enabling interpretation
Obstacle       = constraining interpretation
Vision         = desired / strategically relevant Configuration
Goal           = desired Configuration or change
Mission        = operational mechanism for Transition
Decision       = selection / commitment that may itself be a Transition
Problem        = analytical framing
Solution       = candidate Configuration / Transition
```

This is becoming significantly smaller than our initial model.

---

# 21. What Still Does Not Fit Cleanly

Several things remain deliberately unresolved.

## A. Configuration identity

How do we refer to a Configuration as a coherent candidate when several
Configurations share Statements?

## B. Temporal semantics

How do we reconstruct a Configuration at a particular point in time?

## C. Possibility semantics

How do we distinguish:

```text
possible
desired
selected
planned
actual
historical
```

without creating a type for each?

## D. Transition semantics

What exactly is a Transition?

Is it:

```text
a relation between Configurations
```

or:

```text
an event that changes Configurations
```

or both?

## E. Evidence versus inference

An Observation is evidence.

A Configuration may be an inference.

The model must not accidentally make inferred information look like
directly observed fact.

---

# 22. Current Assessment

This test strengthens rather than weakens the Configuration hypothesis.

The most promising structure currently looks like:

```text
                     THING
                       │
                       │ has / participates in
                       ▼
                CONFIGURATION
                       │
              ┌────────┴────────┐
              │                 │
           current            possible
              │                 │
              │              selected
              │                 │
              │              desired
              │                 │
              └────────┬────────┘
                       │
                    TRANSITION
                       │
                       ▼
                CONFIGURATION
                       │
                       ▼
                   OBSERVE
                       │
                       ▼
                 new information
```

But the labels around Configuration are currently **semantic
interpretations**, not database states.

---

# 23. Most Important New Insight

The model may be converging on a distinction between three things:

### Information

> What we know / observe / assert.

### Configuration

> How relevant information is arranged and understood as a state.

### Transition

> How a configuration changes.

Then:

```text
Information
     ↓
Configuration
     ↓
Transition
     ↓
Configuration
     ↓
Information
```

This is potentially the real backbone.

Everything else may be a way of reasoning about this cycle.

---

# 24. Next Step

Before changing the main `information-model.md`, we should test one final
question:

> **Can Configuration itself be represented without becoming a hidden
> traditional "object with fields"?**

In other words:

```text
Configuration
    =
    a coherent view / projection of information
```

rather than:

```text
Configuration
    =
    another entity with attributes
```

If we can establish that distinction cleanly, we may be very close to the
semantic foundation we have been looking for.
