# Information Model — Trajectory Investigation

## Status

**Discovery — Phase 1**

This document investigates the idea that "doing nothing" is itself a
meaningful alternative because reality continues to change.

The central question is:

> Should trajectory and projected configuration become semantic concepts in
> the information model, or are they simply reasoning operations over
> Configurations and Transitions?

The investigation uses the scenarios developed during Phase 1.

---

# 1. Working Hypothesis

A current Configuration does not remain static.

If no deliberate intervention is made, the relevant system may continue to
evolve because of:

- existing behaviour
- relationships
- external change
- competition
- environmental change
- learning
- decay
- demographic change
- technology
- market dynamics
- other forces

Therefore:

```text
CURRENT CONFIGURATION
        │
        │ continue current dynamics
        ▼
PROJECTED CONFIGURATION
```

This is not necessarily "doing nothing".

It is **continuing the current trajectory**.

An intentional Transition is one possible way of changing that trajectory.

---

# 2. Immigrant → Software Developer

## Current situation

```text
Person A

limited Swedish
limited professional network
little software experience
uncertain direction
```

Suppose nothing deliberate changes.

The person may:

- learn Swedish through ordinary life
- obtain another type of job
- develop unrelated skills
- establish relationships
- become discouraged
- eventually discover another direction

The exact result is uncertain.

Therefore the system should not claim:

> "Doing nothing results in X."

Instead it may represent:

```text
Current Configuration
        │
        ▼
Continuation Projection
        │
        ├── likely outcome A
        ├── possible outcome B
        └── risk / uncertainty
```

## Compare intervention

Suppose we introduce:

```text
Mission:
meet business owner
```

That may produce:

```text
new relationship
→ trainee opportunity
→ project
→ experience
```

Now we can compare:

```text
CONTINUE
vs.
INTERVENE
```

### Finding

**Strong support for trajectory reasoning.**

The value of the intervention is not simply that it performs an action.

It is that it may move the person toward a more desirable future than the
continuation projection.

---

# 3. Occupation Card Exploration

The person initially says:

> I don't know.

We explore occupations.

An interesting extension is:

```text
Candidate A: electrician
Candidate B: software developer
Candidate C: chef
Candidate D: mechanic
```

Each candidate can have its own projected trajectory.

For example:

```text
choose software development
    ↓
required capabilities
    ↓
possible transitions
    ↓
expected future configuration
```

versus:

```text
choose electrician
    ↓
different transitions
    ↓
different expected future configuration
```

And there remains:

```text
choose nothing
    ↓
continuation trajectory
```

### Finding

Trajectory reasoning works not only for "do nothing".

Every candidate path can have a **projected future configuration**.

---

# 4. Business Owner / Matchmaking

Business Owner B wants to build a network of young trainees.

Current configuration:

```text
Business Owner B
    café
    community relationships
    shared language
    desire to help young people
```

If nothing changes:

```text
current business continues
current relationships continue
network may or may not develop
```

A candidate transition is:

```text
interview five young people
```

Another might be:

```text
connect with local software companies
```

Another:

```text
create a trainee event
```

Each creates a different projected configuration.

This is useful because the engine can reason about:

```text
current trajectory
candidate transition A
candidate transition B
candidate transition C
```

### Finding

Matchmaking becomes especially powerful when the system can compare the
likely effects of connecting Things.

---

# 5. Öland Harvest Festival

Suppose the event organisation wants:

```text
more visitors
more business participation
stronger identity as an event
```

Current configuration:

```text
festival
businesses
artists
birdwatchers
visitors
existing attractions
existing relationships
```

## Continuation

If nothing changes:

```text
next festival resembles previous festivals
```

But this is only a projection.

External conditions may change:

- tourism trends
- weather
- competing events
- transport
- economy
- visitor interests

So the continuation trajectory has uncertainty.

## Candidate transition

Suppose we create:

```text
new matchmaking experience:
visitor ↔ local business ↔ artist
```

This creates a projected future configuration.

Another candidate:

```text
birdwatching weekend
```

Another:

```text
regional food network
```

The organisation can compare:

```text
continuation
vs.
candidate A
vs.
candidate B
vs.
candidate C
```

### Finding

This is a strong case for trajectory reasoning because the cost of
inaction may be gradual rather than immediate.

---

# 6. Attractive District

Consider a property company trying to increase the attractiveness of a
district.

Current configuration:

```text
residents
businesses
public spaces
services
traffic
safety
social relationships
```

Suppose attractiveness is gradually declining.

Then:

```text
CONTINUATION
    ↓
further decline
    ↓
lower investment
    ↓
fewer businesses
    ↓
further decline
```

This is a possible reinforcing trajectory.

An intervention may be:

```text
create a new meeting place
```

But the cost may be significant.

Another may be:

```text
connect existing businesses
```

with lower cost.

A third may be:

```text
change public space
```

with another risk/cost profile.

Now the important question becomes:

> What is the expected value of changing the trajectory compared with the
> expected cost of intervention?

### Finding

This is perhaps the clearest example so far of why **cost of inaction**
must be considered explicitly.

---

# 7. Football Team

Current configuration:

```text
team
players
fitness
skills
relationships
tactics
league position
```

Continuation:

```text
same training approach
same tactical approach
same player development
```

Possible intervention:

```text
change tactical configuration
```

Another:

```text
develop young players
```

Another:

```text
recruit a player
```

Each creates a different projected configuration.

There is also a feedback loop:

```text
match result
→ observation
→ revised configuration
→ revised transition
```

### Finding

This demonstrates that trajectory is not restricted to social or strategic
planning.

It is a generic property of adaptive systems.

---

# 8. Project Peace on Earth

This is the deliberately difficult case.

There may be:

- many Things
- many Intentions
- conflicting Intentions
- cooperation
- competition
- power differences
- external shocks
- long time horizons
- unintended consequences

The continuation trajectory is therefore not one deterministic future.

It is more useful to think in terms of:

```text
possible trajectories
```

or:

```text
trajectory hypotheses
```

For example:

```text
Current configuration
      │
      ├── trajectory A
      ├── trajectory B
      ├── trajectory C
      └── uncertain / unknown
```

Candidate interventions then alter the probability or plausibility of
different trajectories.

### Finding

The more complex the system becomes, the less useful a single predicted
future becomes.

This argues for representing **projections with uncertainty**, rather than
turning forecasts into facts.

---

# 9. "Doing Nothing" Is Not a Special Action

This is becoming clearer.

We should not model:

```text
Action = Nothing
```

Instead:

```text
Continuation trajectory
```

is the baseline against which intentional Transitions may be compared.

A user may choose:

```text
continue
```

but that is a **decision about whether to intervene**, not an action that
creates a special "nothing" object.

This is an important semantic distinction.

---

# 10. Cost of Inaction

The scenarios suggest that the system may need to reason about at least
three categories of consequence:

```text
Cost of intervention
Cost of continuation
Value of change
```

For example:

```text
Intervention A
    cost = 10
    expected improvement = 20

Continuation
    cost of inaction = 15
    expected improvement = 0
```

The numbers are illustrative only.

The important point is conceptual:

> An intervention should be evaluated against the trajectory that it may
> replace, not against an imaginary static baseline.

This can include:

- direct cost
- opportunity cost
- delay
- risk
- deterioration
- lost opportunities
- relationship effects
- capability decay
- irreversible consequences

---

# 11. Trajectory vs Configuration

A Configuration describes a state-like arrangement.

A Trajectory describes:

> how a Configuration is expected or observed to change over time.

Conceptually:

```text
CONFIGURATION A
      │
      ├──────────────► CONFIGURATION B
      │                    │
      │                    ▼
      │              CONFIGURATION C
      │
      └── transition ──► alternative path
```

Therefore:

```text
Configuration = state-like semantic object
Trajectory    = sequence / projection of changes
```

This suggests Trajectory is semantically different from Configuration.

---

# 12. Is Trajectory a Primitive?

There are two possibilities.

## Option A — Trajectory is a first-class semantic concept

```text
Trajectory
    starts from Configuration
    contains / predicts transitions
    leads toward projected Configurations
```

Advantages:

- explicit comparison of paths
- explicit cost of inaction
- explicit uncertainty
- useful for strategic reasoning

Risk:

- may become another large object with embedded methodology.

## Option B — Trajectory is a derived view

A trajectory is generated from:

```text
Configuration
+ observed history
+ known dynamics
+ candidate Transitions
+ Context
```

Advantages:

- smaller core
- no special trajectory storage required
- AI can generate projections dynamically

Risk:

- important reasoning may become implicit.

### Current assessment

**Keep Trajectory as a semantic concept, but do not yet make it a primitive
information type.**

We need more evidence.

---

# 13. Projection

The term **Projection** may be even more fundamental than Trajectory.

A Projection says:

> Given what we know and an assumed continuation or Transition, what
> configuration might result?

Examples:

```text continuation projection
intervention projection
candidate projection
backcasting projection
scenario projection
```

This unifies several things we have already discussed.

The distinction becomes:

```text CONFIGURATION
      │
      │ projection
      ▼
PROJECTED CONFIGURATION
```

The Projection may be based on:

- continuation
- candidate Transition
- assumptions
- models
- historical observations
- AI reasoning

And critically:

> A Projection is not an Observation.

It is an inference about a possible future.

---

# 14. Observation vs Projection

This distinction now looks fundamental.

```text OBSERVATION
"Company C offered a trainee position."

vs.

PROJECTION
"If Person A accepts the position, they may gain
software experience within six months."
```

The first is evidence about reality.

The second is reasoning about a possible future.

The system must never silently treat the second as if it were the first.

This is especially important for AI.

---

# 15. Projection and Uncertainty

The Peace example shows that projections should be able to express
uncertainty.

For example:

```text Projection A
    likelihood: unknown / high / medium / low
    confidence: ...
    assumptions: ...
```

But these should not yet become fixed fields.

The semantic requirement is:

> A Projection must be distinguishable from an Observation and its
> assumptions / uncertainty must be recoverable.

---

# 16. Projection and Cost

A Projection can be associated with consequences.

For example:

```text Continuation Projection
    → expected decline

Intervention Projection A
    → expected improvement
    → cost
    → risk

Intervention Projection B
    → smaller improvement
    → lower cost
```

This enables the system to reason about:

```text expected value of intervention
vs.
expected cost of intervention
vs.
expected cost of continuation
```

Again, the model should represent the underlying claims and assumptions,
not pretend that these are objective truths.

---

# 17. Important New Distinction

We now appear to have three different semantic categories:

### Observation

> What happened / what is observed.

### Configuration

> How relevant information can be understood as a state.

### Projection

> What might happen / what a configuration may become under assumptions.

And then:

### Transition

> A change that connects configurations.

This gives us:

```text
OBSERVATION
     │
     ▼
CONFIGURATION
     │
     ├── projected continuation ──► PROJECTION
     │
     ├── candidate Transition ────► PROJECTION
     │
     └── actual Transition ───────► CONFIGURATION
```

This is a much more precise model of the reasoning we have been discussing.

---

# 18. The Engine's Decision Problem

The engine may eventually help answer:

> "Given what we currently know, which Transition is worth pursuing?"

It can construct:

```text
Current Configuration
       │
       ├── continuation Projection
       │
       ├── Transition A
       │      └── Projection A
       │
       ├── Transition B
       │      └── Projection B
       │
       └── Transition C
              └── Projection C
```

Then compare them against:

```text Intent
Constraints
Motivation
Resources
Cost
Risk
Uncertainty
```

The user then chooses.

This fits our existing principle:

> **AI suggests; the user selects.**

---

# 19. What This Adds to the Generic Model

We now have a potentially coherent semantic cycle:

```text
REALITY
  │
  ▼
OBSERVATIONS
  │
  ▼
CONFIGURATION
  │
  ├───────────────┐
  │               │
  │          INTENTION
  │               │
  ▼               ▼
CONTINUATION    CANDIDATE
PROJECTION      TRANSITIONS
  │               │
  │               ▼
  │           PROJECTIONS
  │               │
  └───────┬───────┘
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
      OBSERVATION
          │
          └────────→ ...
```

This is much closer to the actual reasoning problem than a simple
"problem → solution" model.

---

# 20. Findings

## F-001 — Doing nothing is not a zero-transition state

Reality continues to evolve.

Therefore continuation must be considered as a possible trajectory.

## F-002 — Cost of inaction is real

The value of an intervention cannot be evaluated against a static baseline
alone.

The continuation trajectory is a legitimate comparison case.

## F-003 — Projection is distinct from Observation

This distinction is essential.

Especially for AI-generated reasoning.

## F-004 — Trajectory may be a derived concept

Trajectory can potentially be constructed from Configurations, Transitions,
Observations and Projections.

It should not yet become a primitive.

## F-005 — Projection appears more fundamental

Projection may be the generic concept behind:

- continuation forecasts
- intervention forecasts
- scenarios
- backcasting candidates
- expected outcomes

## F-006 — Uncertainty belongs to projections

A projection must not silently become fact.

Its assumptions, evidence and uncertainty need to remain distinguishable.

---

# 21. Revised Semantic Backbone

The model is now tentatively:

```text
             OBSERVATION
                  │
                  ▼
             CONFIGURATION
                  │
        ┌─────────┼─────────┐
        │         │         │
        ▼         ▼         ▼
 continuation  candidate  desired
 projection   transition configuration
        │         │
        │         ▼
        │      PROJECTION
        │         │
        └────┬────┘
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
         OBSERVATION
```

This is still discovery, not a final information model.

---

# 22. Next Question

We now have enough material to ask a much sharper question:

> **What is the smallest semantic core that can represent Reality,
> Information, Configuration, Projection and Transition?**

If we can answer that, we should probably be ready to revise the main
`information-model.md` rather than continuing to add exploratory documents.
