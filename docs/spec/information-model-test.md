# Information Model — Stress Test

## Status

**Discovery — Phase 1**

This document tests the current Generic Information Model against the
underlying operations and concrete cases developed during Phase 1.

The current candidate information forms are:

- Thing
- Statement
- Observation
- Intention
- Relationship
- Context
- Transition

Higher-level concepts such as Identity, Opportunity, Mission, Goal, Vision,
Obstacle and Constraint are currently interpretations, projections or
mechanisms rather than mandatory primitive types.

The test question is:

> Can the candidate information model support the operations and cases
> without introducing method-specific or domain-specific types?

---

# Test 1 — Identity

## Requirement

Represent the relevant current configuration of a person, organisation,
district, event or other Thing.

## Candidate representation

A Thing is described by Statements, Observations and Relationships within a
Context.

Example:

```text
Student
  ├── knows → Python
  ├── speaks → Arabic
  ├── located-at → Kalmar
  ├── seeks → software experience
  └── knows → Business Owner
```

The relevant subset becomes the current Identity.

## Result

**PASS**

Identity does not need to be a primitive stored type.

### Remaining issue

We need to define how a collection of relevant information becomes a
recognisable Identity projection without turning Identity into a fixed
schema.

---

# Test 2 — Identity Bricks

## Requirement

Represent context-dependent building blocks such as:

```text
programming capability
language capability
professional network
available premises
visitor reach
community participation
```

## Candidate representation

A Brick is a conceptual label for a relevant aspect represented by one or
more Statements, Observations or Relationships.

## Result

**PASS — provisionally**

No universal Brick type is required.

### Remaining issue

The model must eventually support measurable and qualitative aspects of
Bricks without defining a fixed list of Brick types.

---

# Test 3 — Observe

## Requirement

Establish what appears to be happening.

## Candidate representation

Observation records information about a Thing, Relationship or situation,
within Context and with possible source, time and confidence.

## Result

**PASS**

Observation is directly supported.

### Important distinction

Verification and Validation can both use Observation, while remaining
different activities.

- Verification asks whether something conforms to what was intended or
  specified.
- Validation asks whether the resulting change works in the relevant
  reality.

This distinction belongs primarily to the operation/process layer, not
necessarily the information layer.

---

# Test 4 — Frame

## Requirement

Determine what matters in the current context.

## Candidate representation

Context + relevant Statements + Observations + Intentions.

Framing is an operation performed over information rather than a new
information type.

## Result

**PASS**

No `Frame` type appears necessary.

---

# Test 5 — Imagine / Desired Future

## Requirement

Represent a possible future configuration or Desired Identity.

## Candidate representation

Intention expresses a desired direction, future state, outcome or change.

A Desired Identity is a contextual projection of desired Statements /
configurations.

## Result

**PASS — provisionally**

No `Vision` or `Goal` primitive is required.

### Important observation

The future may be incomplete or uncertain.

Therefore the model must support partial and emerging Intentions.

---

# Test 6 — "I Don't Know"

## Requirement

Represent a situation in which the user cannot yet state a meaningful
Desired Identity.

## Candidate representation

The system can begin with observations and an unresolved or incomplete
Intention.

Exploration produces candidate future Statements / configurations, from
which an Intention can emerge.

```text
Current situation
      ↓
Exploration
      ↓
candidate futures
      ↓
user selection
      ↓
emerging Intention
```

## Result

**PASS**

No `UnknownIntent` type is required.

The absence or incompleteness of an Intention is itself meaningful state.

---

# Test 7 — Analysis

## Requirement

Break a situation apart to identify gaps, causes, dependencies,
constraints and missing capabilities.

## Candidate representation

Analysis operates over:

- Statements
- Observations
- Relationships
- Context
- Intentions

It can produce additional Statements, candidate interpretations and
questions.

## Result

**PASS**

Analysis is an operation, not an information type.

---

# Test 8 — Synthesis

## Requirement

Combine capabilities, resources and relationships to create new
possibilities.

Example:

```text
empty premises
    +
artist
    +
café
    +
association
    ↓
new collective capability
```

## Candidate representation

Relationships + Statements + Context + Intention can represent the
ingredients.

The resulting Opportunity is an interpretation of a possible Transition.

## Result

**PASS — provisionally**

This is one of the strongest tests of the generic model.

No `Opportunity` type appears strictly necessary at this stage.

### Remaining issue

We need a precise way to represent a **candidate configuration that does
not yet exist**.

This may be more important than introducing an Opportunity type.

---

# Test 9 — Opportunity and Constraint

## Requirement

Represent the fact that the same information may enable one Transition
and constrain another.

Example:

```text
Team B is strong.
```

For Team A:

```text
Team A wants to win.
Team B is strong.
        ↓
constraint on Team A's transition
```

But the same fact may also support:

```text
Team B provides a strong opponent.
        ↓
opportunity to improve
```

## Candidate representation

A Statement or Observation is interpreted relative to:

- a Thing
- a Context
- an Intention
- a contemplated Transition

The resulting interpretation can be:

- enabling
- constraining
- neutral
- ambiguous

## Result

**PASS — strong conceptual support**

This supports the hypothesis that Opportunity and Constraint are not
necessarily primitive types.

### Important consequence

The model should not store:

```text
type = obstacle
```

as the only meaning of a fact.

The same information may have different effects relative to different
Transitions.

---

# Test 10 — Matchmaking

## Requirement

Find potential connections between many Things.

Example:

```text
A NEEDS X
B CAN PROVIDE X

       ↓

possible relationship
       ↓
candidate transition
```

## Candidate representation

Statements + Relationships + Context + Intentions.

## Result

**PASS — provisionally**

Matchmaking can operate over generic information.

### Remaining issue

Efficient discovery across thousands or millions of Things is an
implementation/query problem, not necessarily an information-model
problem.

---

# Test 11 — Mission

## Requirement

Represent a concrete assignment such as:

```text
Visit this address.
Talk to the business owner.
Interview five people.
Build a prototype.
```

## Candidate representation

Mission is a mechanism for inducing a Transition.

It can therefore be represented as information associated with a Transition,
without requiring Mission to be a universal primitive.

## Result

**PASS — provisionally**

### Remaining issue

We need to distinguish:

- intended Transition
- planned mechanism
- actual action
- observed outcome

without collapsing them into one record.

---

# Test 12 — Decision

## Requirement

Represent:

```text
Choose to proceed.
Choose to stop.
Choose to wait.
Choose a candidate future.
```

## Candidate representation

A Decision can be an event/transition that changes the situation and/or
Intention.

## Result

**PASS — provisionally**

No separate Decision primitive is currently required.

### Important consequence

Choose and Transition cannot always be separated.

A decision may itself be the smallest meaningful Transition.

---

# Test 13 — Multi-Identity Transition

## Requirement

One Mission or Transition may affect several Things.

Example:

```text
Artist
Café
Association
Festival
Visitors

        ↓

one cooperative activity

        ↓

multiple changed identities
```

## Candidate representation

Transition relates to multiple Things and their Relationships.

## Result

**PASS**

The model explicitly allows this.

---

# Test 14 — Collective / Multi-Scale Identity

## Requirement

Represent:

- person
- business
- organisation
- district
- festival
- community

and allow relationships between these levels.

## Candidate representation

All are Things.

Their relevant Identity is a contextual projection of their information.

## Result

**PASS — provisionally**

### Remaining issue

The model needs to represent containment, membership, participation and
other forms of collective structure.

This does not currently require separate Identity types.

---

# Test 15 — Strategic / Tactical / Operative

## Requirement

Represent the same underlying situation at different levels.

## Candidate representation

Context determines the relevant scope and resolution.

Strategic / Tactical / Operative are treated as perspectives or levels of
work, not information types.

## Result

**PASS**

No Strategic, Tactical or Operative primitive is currently necessary.

---

# Test 16 — What / How / With What

## Requirement

Represent a development process:

```text
WHAT?
HOW?
WITH WHAT?
VERIFY / VALIDATE
DELIVER
```

## Candidate representation

- What → Intention / framing
- How → candidate Transitions and configurations
- With What → resources, capabilities, relationships and selected means
- Verify / Validate → Observations interpreted through the relevant Context
- Deliver → Transition / action
- New What → new situation and emerging Intent

## Result

**PASS**

The information model can support the process without adopting its
terminology.

---

# Test 17 — Backcasting

## Requirement

Represent reasoning from a Desired Identity toward possible intermediate
configurations.

## Candidate representation

Intention + candidate configurations + Transitions + Context.

## Result

**PASS**

Backcasting appears to be an operation/method over the information rather
than a required information type.

---

# Test 18 — Feedback and History

## Requirement

A Transition changes reality. New observations must be available without
destroying the previous understanding.

## Candidate representation

Observation + time + source + Context.

## Result

**PASS — conceptually**

### Remaining issue

Temporal modelling needs a deeper test.

We need to distinguish at least:

```text
what was believed
what was observed
what actually happened
what is currently inferred
```

The current candidate model does not yet define this precisely enough.

---

# Cross-Test Findings

## Finding 1 — The candidate information model survives the operations

The current seven candidate information forms can represent all tested
operations without introducing OODA, ABCD, Backcasting, Strategic,
Tactical or Operative as information types.

This is a strong result.

---

## Finding 2 — Identity remains a projection

Identity continues to work better as a contextual projection than as a
universal stored type.

This protects the model from domain-specific schemas.

---

## Finding 3 — Opportunity and Constraint should remain interpretations

The football example and other cases support treating the same underlying
information as enabling or constraining depending on the contemplated
Transition.

This means the information model should represent the underlying
information and its context, not permanently classify it as an Opportunity
or Obstacle.

---

## Finding 4 — Candidate futures are the biggest missing piece

The current model represents existing Things and Statements well.

It is less clear how to represent:

> "This configuration does not exist yet, but it is a candidate future
> configuration we are considering."

We need this for:

- Vision
- Desired Identity
- Goals
- candidate solutions
- synthesis
- backcasting
- AI-generated alternatives

This may be the most important open issue discovered by the test.

---

## Finding 5 — Intent is not enough by itself

An Intention says something about what is desired.

But the system also needs to reason about possible configurations that are
not yet intentions.

For example:

```text
Possible configuration A
Possible configuration B
Possible configuration C

        ↓
user selects B

        ↓
Intention toward B
```

Therefore candidate futures may need a representation that is more generic
than Intention.

---

## Finding 6 — Transition needs more semantic depth

We currently know that a Transition represents meaningful change.

But implementation will eventually need to distinguish:

- current configuration
- desired configuration
- candidate configuration
- planned transition
- actual transition
- observed outcome

We should not solve this by immediately creating six types.

We need to investigate the underlying semantics first.

---

## Finding 7 — Observation needs provenance and temporality

Observation has survived the conceptual test, but the eventual information
model will need to represent:

- when
- by whom / what source
- under which Context
- with what confidence
- whether it is direct observation or interpretation

This is important for an AI reasoning environment.

---

## Finding 8 — Relationships are probably more important than initially assumed

Many of the interesting capabilities of the model emerge from relationships:

- matchmaking
- cooperation
- competition
- membership
- participation
- capability/resource relationships
- multi-identity transitions

The Relationship concept should therefore be tested more deeply before
being simplified away.

---

# Current Assessment

The information model is **strong enough to continue**, but not ready to
freeze.

The most important unresolved concepts are now:

1. **Candidate future configuration**
2. **Transition semantics**
3. **Temporal/provenance semantics of Observation**
4. **Relationship semantics**
5. **How a contextual Identity projection is defined**

These are more fundamental than adding domain concepts such as Mission,
Goal, Vision, Opportunity or Obstacle.

---

# Recommended Next Test

Before designing a database or API, construct one complete information
example containing:

```text
Current Identity
        ↓
Observation
        ↓
Intent
        ↓
Candidate futures
        ↓
Analysis
        ↓
Synthesis
        ↓
Candidate Transition
        ↓
User chooses
        ↓
Mission
        ↓
Actual Transition
        ↓
Verification / Validation
        ↓
Observation
        ↓
New Identity
```

Use the **immigrant → software developer** case because it contains nearly
all of the phenomena we have discovered.

If we can express that case cleanly without inventing domain-specific
types, the information model will have passed a much stronger test.
