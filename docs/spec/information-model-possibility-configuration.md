# Information Model — Possibility and Configuration

## Status

**Discovery — Phase 1**

This document investigates the first major gap found by the end-to-end
immigrant case:

> How can the model represent something that is possible, but not yet
> actual, intended, selected or performed?

The investigation deliberately avoids introducing a `CandidateFuture`,
`Scenario`, `Option`, `Goal` or similar domain-specific primitive until the
underlying semantics are understood.

---

# 1. The Problem

The system needs to represent things such as:

```text
"I could become a software developer."

"These four occupations are possible directions."

"This business owner could provide a useful connection."

"We could turn this empty building into a community space."

"Team A could use this tactical formation."

"Solution B might satisfy the requirement."
```

These are not ordinary observations.

They are also not necessarily intentions.

They are **possibilities under consideration**.

A possibility can be:

- generated
- discovered
- compared
- evaluated
- rejected
- selected
- revised
- combined with another possibility

without becoming true.

---

# 2. Configuration

A useful candidate concept is **Configuration**.

A Configuration describes a meaningful arrangement of information.

Examples:

```text
Person A
    has programming capability
    has a relationship with Company C
    has completed one software project
```

or:

```text
District
    has active public spaces
    has local businesses participating
    has increased evening activity
```

or:

```text
Festival
    connects visitors with local businesses
    contains new cultural activities
    attracts 5,000 additional visitors
```

A Configuration does not inherently say whether it is:

- current
- desired
- possible
- historical
- planned

Those meanings can arise from Context and its relationship to other
information.

---

# 3. Current Configuration

The current situation can be understood as a Configuration.

For example:

```text
Person A
    speaks → Language X
    limited Swedish
    knows → few local employers
    seeks → direction
```

This supports the current Identity projection.

Therefore:

> **Identity may be a contextual interpretation of a Configuration.**

This preserves the existing model.

---

# 4. Candidate Configuration

Now consider:

```text
Candidate Configuration A

Person A
    trains as → electrician
```

and:

```text
Candidate Configuration B

Person A
    develops software
    has a portfolio
    has a professional network
```

Neither configuration is necessarily true.

Neither is necessarily intended.

They are simply configurations that can be considered.

This gives us:

```text
CURRENT CONFIGURATION
          │
          ▼
    POSSIBLE CONFIGURATIONS
       ┌────┼────┐
       A    B    C
       │    │    │
       └────┼────┘
            ▼
         evaluate
            │
            ▼
          choose
            │
            ▼
       INTENTION
```

This appears to solve an important gap without creating a
`CandidateFuture` type.

---

# 5. Configuration as a Set of Statements

A possible Configuration may be represented by Statements.

For example:

```text
Configuration B

Person A
    capable-of → software development

Person A
    connected-to → Company C

Person A
    has-evidence-of → completed project
```

The Configuration is therefore not necessarily a new kind of Thing.

It can be a **grouping / interpretation of Statements**.

This is attractive because the same underlying Statements can participate
in different configurations.

---

# 6. But a Configuration Needs Identity

A simple collection of Statements is not sufficient.

We need to know:

```text
Which Statements belong together
as one contemplated Configuration?
```

For example:

```text
A:
    software capability
    Company C relationship

B:
    software capability
    university education

C:
    software capability
    freelance experience
```

The configurations are alternatives.

Therefore the model probably needs some way to refer to a configuration
as a unit, even if Configuration is not a domain-specific type.

This is a significant design question.

---

# 7. Configuration May Be Abstract

A Configuration does not have to describe every detail.

For example:

```text
"Become a software developer"
```

may be an intentionally incomplete Configuration.

Later it can become more specific:

```text
"Become a junior web developer within two years."
```

Later still:

```text
"Obtain a junior developer position at Company C."
```

Therefore a Configuration can have different levels of resolution.

This is important for the Strategic / Tactical / Operative distinction.

---

# 8. Configuration and Identity

A useful distinction is emerging:

### Configuration

> What is arranged / true / contemplated in a particular context?

### Identity

> What does that configuration mean about the Thing in the relevant
> context?

For example:

```text
Configuration
    programming capability
    portfolio
    employer relationship
    work experience

             ↓ interpretation

Identity
    "junior software developer"
```

Identity therefore remains a projection rather than a primitive.

---

# 9. Configuration and Intention

An Intention expresses a desired relationship to a Configuration.

For example:

```text
Configuration:
    Person A works as a software developer.

Intention:
    Person A wants to reach this configuration.
```

This gives us a useful separation:

```text
CONFIGURATION
      │
      │ desired
      ▼
  INTENTION
```

But not every Configuration needs an Intention.

A candidate may simply be explored.

```text
Configuration A
Configuration B
Configuration C

        ↓
      explore

        ↓
   user selects B

        ↓
   Intention toward B
```

This directly supports the occupation-card example.

---

# 10. Configuration and Transition

A Transition changes one Configuration toward another.

```text
Configuration N
       │
       │ Transition
       ▼
Configuration N+1
```

A candidate Transition can therefore be understood as a relationship
between configurations that is being considered but has not yet occurred.

For example:

```text
Current Configuration
        │
        │ possible Transition
        ▼
Candidate Configuration
```

This is more general than treating `Mission` as the transition itself.

A Mission becomes one possible mechanism for inducing the Transition.

---

# 11. Configuration and Possibility

We may therefore not need a `Possibility` type.

Instead:

> **Possibility is a mode in which a Configuration or Transition is being
> considered.**

For example:

```text
Configuration B
    status / context:
        possible
```

or:

```text
Transition T
    status / context:
        possible
```

The exact representation of this "mode" is not yet decided.

The important semantic distinction is:

```text
possible ≠ true
possible ≠ desired
possible ≠ selected
possible ≠ performed
```

---

# 12. The Lifecycle We Need

The immigrant example suggests something like:

```text
possible
    │
    ├── rejected
    │
    ├── revised
    │
    └── selected
            │
            ▼
         intended
            │
            ▼
          planned
            │
            ▼
         performed
            │
            ▼
         observed
```

But this should **not yet become a fixed state machine**.

There may be shortcuts:

```text
possible → performed
```

or:

```text
possible → selected → performed
```

or:

```text
intended → revised → rejected
```

or:

```text
decision → immediate Transition
```

The model must support these without assuming a mandatory lifecycle.

---

# 13. Candidate Configuration and AI

This concept is especially useful for AI involvement.

AI can generate:

```text
Candidate Configuration A
Candidate Configuration B
Candidate Configuration C
```

The AI can explain:

- why each may be useful
- what it requires
- what opportunities support it
- what constraints affect it
- what transitions could lead toward it

But:

```text
AI generates possibilities
          ↓
User evaluates
          ↓
User selects
          ↓
Intention / Transition
```

The AI therefore does not create the user's Intent.

It creates **things to consider**.

This fits the principle:

> AI suggests; the user selects the way forward.

---

# 14. Candidate Configuration and Synthesis

Synthesis can create a candidate Configuration that did not previously
exist.

For example:

```text
Artist
+
Café
+
Empty premises
+
Festival
+
Birdwatching association

        ↓ synthesis

Candidate Configuration:

A combined cultural / visitor
experience in the empty premises.
```

Nothing in the current situation may directly correspond to the candidate
whole.

This is why Configuration is potentially more useful than Opportunity.

Opportunity is the interpretation:

> "This configuration may provide a useful path."

Configuration describes:

> "What the resulting arrangement could look like."

---

# 15. Candidate Configuration and Analysis

Analysis can also generate candidate Configurations.

For example:

```text
Current:
    limited Swedish
    limited network
    no work experience

Analysis:
    missing language capability
    missing professional network
    missing evidence

Candidate Configuration:

    improved Swedish
    local professional network
    completed project
```

Analysis identifies what a useful future configuration may need.

Synthesis may then discover a completely different configuration:

```text
shared-language mentor
+
local business
+
real project
+
professional introduction
```

Both modes can therefore produce candidate configurations.

---

# 16. Configuration and Measurement

A Configuration may contain qualitative or quantitative aspects.

For example:

```text
District

safety = high
local participation = 60%
evening activity = moderate
business participation = 40
```

or:

```text
Festival

visitors = 5,000
sponsors = 20
business participation = 80
```

This means Configuration cannot simply be treated as a textual description.

It may contain values, measurements and qualitative assertions.

The underlying representation of values remains an open information-model
question.

---

# 17. Configuration and Time

A Configuration can be:

- valid at a particular time
- historical
- current
- projected
- possible

Therefore temporal semantics matter.

For example:

```text
Configuration C
    valid during → 2028 festival
```

versus:

```text
Configuration C
    considered for → 2028 festival
```

The same conceptual configuration can therefore exist as a possibility
without being a historical or current state.

---

# 18. Configuration Does Not Mean Database Object

This is important.

The concept "Configuration" does not imply:

```text
ConfigurationTable
```

or:

```text
ConfigurationEntity
```

It is currently a semantic concept.

It may eventually be represented through:

- grouped Statements
- references
- assertions
- contextual scopes
- projections
- graph structures
- or some combination

The implementation must be derived from the semantic requirements.

---

# 19. Test Against the Main Cases

## Immigrant

Works:

```text
current configuration
→ candidate configurations
→ selected configuration
→ intended transition
→ actual transition
→ new configuration
```

## Football

Works:

```text
current team configuration
→ candidate tactical configuration
→ selected configuration
→ match transition
→ observed result
```

## Öland Harvest Festival

Works:

```text
current event configuration
→ candidate experience configurations
→ selected configuration
→ missions / transitions
→ new event configuration
```

## District attractiveness

Works:

```text
current district configuration
→ candidate configurations
→ selected direction
→ multiple transitions
→ observations
→ revised configuration
```

## "Project Peace on Earth"

Works conceptually, although the number of Things, Relationships,
Intentions and conflicting perspectives becomes very large.

This is useful because it tests scalability of the semantics rather than
just the number of database records.

---

# 20. Current Assessment

The concept of **Configuration** appears to solve the most important gap
found in the previous test.

It allows us to distinguish:

```text
what exists
what could exist
what is desired
what is selected
what actually happened
```

without immediately turning each distinction into a separate domain type.

The current working interpretation is:

> **Configuration is a meaningful arrangement of information that can be
> considered as a state or possible state of one or more Things within a
> Context.**

This is deliberately broader than Identity.

Identity is an interpretation of a Configuration.

Intention expresses a desired relationship to a Configuration.

Transition describes change between Configurations.

---

# 21. New Questions

The introduction of Configuration raises better questions than the ones
we started with.

### Q1 — What is the minimum semantic unit of a Configuration?

Is it:

```text
a set of Statements?
```

or:

```text
a set of Statements + Context?
```

or something more fundamental?

### Q2 — How is a Configuration referred to?

If two candidate configurations contain overlapping Statements, how do we
keep them distinct?

### Q3 — Are "current", "possible", "desired" and "historical" properties of
a Configuration?

Or are they relationships between a Configuration and a Context / Thing /
Intention / Transition?

### Q4 — Can Transition be defined entirely in terms of Configurations?

If so, Transition may become considerably simpler.

### Q5 — Is Identity simply a named projection of Configuration?

This currently appears plausible.

### Q6 — Is Intention a relationship between a Thing and a Configuration?

This is an especially promising hypothesis:

```text
Thing
  │
  └── intends → Configuration
```

### Q7 — Is a candidate Transition a relationship between two
Configurations?

For example:

```text
Configuration A
       │
       └── candidate transition → Configuration B
```

This could unify:

- backcasting
- planning
- Missions
- solution alternatives
- decision making

without introducing method-specific types.

---

# Current Hypothesis

The information model may be approaching a much smaller conceptual core:

```text
THING
  │
  ├── has / participates in
  │
  ▼
CONFIGURATION
  │
  ├── can be current
  ├── can be possible
  ├── can be desired
  └── can be historical
  │
  ▼
TRANSITION
  │
  ▼
CONFIGURATION
```

with:

```text
STATEMENT
OBSERVATION
RELATIONSHIP
CONTEXT
INTENTION
```

providing the information and meaning around those configurations.

This is **not a final model**.

But it is a much stronger hypothesis than simply adding more types.

---

# Next Test

The next step should be to test whether the following can all be expressed
without introducing additional primitives:

```text
Current Configuration
Candidate Configuration
Desired Configuration
Historical Configuration

Thing intends Configuration

Configuration A
    → possible Transition
    → Configuration B

Transition
    → Mission mechanism

Transition
    → Observation

Observation
    → new Configuration
```

If this works, we may have found the semantic backbone of the model.
