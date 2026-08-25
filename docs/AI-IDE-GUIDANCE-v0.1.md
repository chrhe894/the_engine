# AI IDE Guidance --- v0.1

## Read This First

This repository contains an evolving model and a prototype of a generic
Engine.

The coding AI working in the IDE is a **development partner**, not the
owner of the model.

The prototype exists to test and discover the model.

**Do not silently turn implementation choices into model decisions.**

When something is unclear, preserve the uncertainty and make it visible.

------------------------------------------------------------------------

# 1. Purpose of the Project

The Engine is intended to be a generic mechanism for helping people and
organisations move from an evolving situation toward chosen change,
while maintaining continuity of Goals, actions, observations and
evidence across time.

The existing App is the vehicle through which users can experience and
execute parts of this process.

The Engine should remain generic across domains.

Examples include:

-   individual / occupational transition
-   immigrant-related transition
-   Skördefesten / Södra Öland
-   geographically situated challenges
-   sustainability work
-   learning
-   organisational situations
-   crisis-management-like situations

Do not build the prototype around one domain.

------------------------------------------------------------------------

# 2. Current Working Identity

For now:

> **The Engine is a generic mechanism for helping people and
> organisations move from an evolving situation toward chosen change,
> while maintaining continuity of Goals, actions, observations and
> evidence across time.**

The App is the vehicle.

The Case File is the continuity mechanism.

The Engine is the generic mechanism.

The domain is context.

The user does not need to understand the underlying methodology.

This description is a working identity, not a final product definition.

------------------------------------------------------------------------

# 3. Concepts That Have Survived Testing

## 3.1 Case File

The Case File provides continuity across:

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

It represents an evolving situation and its history.

It is not merely a project plan.

## 3.2 Multiple Goals

A Case File can contain multiple Goals simultaneously.

``` text
CASE FILE
│
├── Goal A — ACTIVE
├── Goal B — ACTIVE
├── Goal C — COMPLETED
└── Goal D — ABANDONED
```

Goals may have their own:

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

## 3.3 Goal Lifecycle Is Local

A Goal decision does not automatically become a Case File decision.

For example:

``` text
Goal A — ACTIVE
Goal B — ACTIVE
Goal C — ABANDONED
```

is valid.

Important principle:

> **Never allow a local Goal decision to implicitly become a Case File
> decision.**

The same distinction applies to Missions.

Abandoning one Mission does not automatically abandon its Goal.

## 3.4 Knowledge Survives Lifecycle Changes

An abandoned Goal can retain:

-   observations
-   evidence
-   decisions
-   reasons
-   history

That information may later be relevant to other Goals.

Therefore:

> **Lifecycle state and accumulated knowledge are different things.**

## 3.5 Tree vs Network

The App may use a tree because it is useful for human orientation.

The underlying reality may become network-like.

Working principle:

> **Tree for orientation. Network for reality.**

Do not implement a graph merely because the conceptual model may
eventually become a network.

## 3.6 Missions

Missions connect the model to reality.

``` text
Mission
   ↓
Reality
   ↓
Observation / Evidence
   ↓
Updated Case File
   ↓
Next Proposal
```

A Mission is therefore more than a simple task record.

## 3.7 Definition of Done

Goals and Missions may have a Definition of Done.

It can be simple:

``` text
Visit this place.
Complete the pilot.
Collect three responses.
Run for three months.
8 GPS-verified visits.
```

Do not impose a universal KPI framework unless the model later requires
it.

## 3.8 Engine Proposes; User Decides

The Engine can propose.

The user decides.

Current interaction vocabulary:

``` text
ACCEPT
MODIFY
REJECT
EXPLORE FURTHER
GIVE UP
```

`GIVE UP` is deliberately more significant than ordinary rejection.

It remains scoped to the relevant Goal unless the user explicitly
abandons the Case File.

------------------------------------------------------------------------

# 4. What Is Deliberately Not Decided

Do **not** treat the following as established architecture:

-   final database model
-   final API
-   final JSON schema
-   graph database
-   final ontology
-   authentication architecture
-   production AI architecture
-   final Evidence implementation
-   final permissions model
-   final geographic model
-   final Case File boundaries
-   final organisation model

If implementation requires a temporary decision, make the decision
explicit and keep it reversible where possible.

------------------------------------------------------------------------

# 5. Prototype Philosophy

The prototype is a learning instrument.

It is not the final product.

The primary objectives are:

1.  test the model;
2.  discover contradictions;
3.  discover missing concepts;
4.  discover useful interaction patterns;
5.  discover what the App ↔ Engine boundary actually needs;
6.  keep changes cheap.

Therefore:

> **Build only enough machinery to make the model encounter reality.**

Prefer a simple mock over unnecessary infrastructure.

Prefer a reversible implementation over a sophisticated abstraction.

Prefer explicit temporary code over premature architecture.

------------------------------------------------------------------------

# 6. The Prototype Loop

The prototype should support a loop roughly like:

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

This loop matters more than the technical elegance of the
implementation.

------------------------------------------------------------------------

# 7. App ↔ Engine Boundary

The first App ↔ Engine contract is something we are discovering.

Do not freeze it prematurely.

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
result / evidence
  ↓
CASE FILE
```

JSON is a plausible implementation format.

It is not yet a conceptual requirement.

The important question is:

> **What information must cross the boundary?**

not:

> **What JSON schema should we freeze?**

------------------------------------------------------------------------

# 8. Existing App Is Part of the Test Environment

The existing App already contains useful mechanisms.

Examples include:

-   GPS
-   digital cards
-   places
-   challenges
-   surveys
-   user interaction
-   verification

The Engine may generate generic content that the App translates into
these structures.

Do not rebuild existing App functionality merely to make the prototype
look architecturally pure.

Use what exists.

------------------------------------------------------------------------

# 9. The App Representation Must Not Become the Model

The App currently has structures such as:

``` text
Vision
  ↓
Goals
  ↓
Missions / Challenges
```

This is useful.

But it is a representation for the user.

It must not automatically become the underlying ontology.

If the implementation reveals that a network, multiple relationships, or
another structure is more appropriate, that is a model question to
discuss rather than something the App tree should decide.

------------------------------------------------------------------------

# 10. Case File Continuity

The App and Engine should conceptually work against a common evolving
Case File.

The Case File is the continuity mechanism between:

-   turns
-   sessions
-   people
-   organisations
-   App
-   Engine
-   Goals
-   Missions
-   observations
-   evidence

If a third technical component is eventually needed to store or manage
Case Files, that is an engineering decision to make later.

Do not create such a service merely because the concept exists.

------------------------------------------------------------------------

# 11. How to Handle Ambiguity

When the model is unclear:

### Do

-   identify the ambiguity;
-   show a concrete example;
-   explain the smallest conflict;
-   propose alternatives;
-   keep the change reversible;
-   ask for a model decision when necessary.

### Do not

-   silently invent a rule;
-   silently expand the ontology;
-   hide uncertainty behind an abstraction;
-   treat a temporary implementation as established truth.

------------------------------------------------------------------------

# 12. Classify Problems Before Fixing Them

When something fails, classify the problem first.

``` text
MODEL PROBLEM
UI PROBLEM
APP CAPABILITY
ENGINE REASONING
APP ↔ ENGINE CONTRACT
ENGINEERING PROBLEM
```

Do not solve a model problem by quietly adding technical complexity.

------------------------------------------------------------------------

# 13. Do Not Generalize From the Prototype Into the Model

This is a critical rule.

> **The prototype exists to test the model. The prototype is not the
> model.**

A prototype may contain:

-   hard-coded values
-   mock data
-   simplified storage
-   temporary UI
-   simulated Engine responses
-   simplified evidence
-   deliberately incomplete workflows

That is acceptable.

Do not infer:

``` text
temporary prototype structure
        ↓
permanent architecture
```

without an explicit model decision.

------------------------------------------------------------------------

# 14. Avoid Premature Generalisation

The Engine is generic.

That does **not** mean the prototype must implement every possible
domain.

A generic mechanism can be demonstrated with a very small number of
concrete cases.

Use:

-   immigrant / occupational or integration-related example
-   Skördefesten / Södra Öland example

as test cases.

If another domain reveals a useful contradiction, add it.

Do not build a universal content system before the mechanism has been
tested.

------------------------------------------------------------------------

# 15. AI Behaviour

The coding AI should act as a development partner.

It should:

-   inspect the existing repository before changing architecture;
-   preserve existing working functionality;
-   make small changes;
-   explain non-obvious architectural decisions;
-   keep prototype code simple;
-   flag uncertainty;
-   distinguish temporary prototype choices from model decisions;
-   identify contradictions rather than hiding them;
-   avoid unnecessary dependencies;
-   avoid large refactors without a clear reason.

When a change touches the conceptual model, say so explicitly.

------------------------------------------------------------------------

# 16. Before Making a Significant Change

For changes that affect the model, contract, Case File, or architecture,
first state:

``` text
WHAT I THINK WE ARE TRYING TO ACHIEVE

WHAT CURRENT ASSUMPTION THIS USES

WHAT WILL CHANGE

WHY IT IS NEEDED

WHETHER THE CHANGE IS REVERSIBLE
```

For ordinary bug fixes or small UI changes, this level of ceremony is
unnecessary.

------------------------------------------------------------------------

# 17. Keep the Prototype Cheap to Change

Prefer:

``` text
small
explicit
observable
reversible
```

over:

``` text
abstract
distributed
optimized
generalized
production-ready
```

The prototype is expected to change.

Changing it is a success condition, not a failure.

------------------------------------------------------------------------

# 18. Do Not Build Production Concerns Prematurely

Unless required to test the current hypothesis, avoid spending prototype
effort on:

-   scaling
-   microservices
-   sophisticated authorization
-   production-grade observability
-   complex deployment
-   elaborate database schemas
-   performance optimization
-   final AI orchestration
-   complete error taxonomies

These may become necessary later.

They are not automatically necessary now.

------------------------------------------------------------------------

# 19. Current Known Stress Cases

The prototype should eventually test:

-   multiple simultaneous Goals
-   one abandoned Goal
-   failed Missions
-   unexpected observations
-   `MODIFY`
-   `REJECT`
-   `EXPLORE FURTHER`
-   `GIVE UP`
-   different geographic scopes
-   different time limits
-   conflicting Goals
-   multiple organisations
-   conflicting observations
-   Goal dependencies

Not all need to be implemented immediately.

They are a test backlog.

------------------------------------------------------------------------

# 20. What Would Falsify the Direction?

Take these seriously.

The direction would be in trouble if repeated real examples show that:

1.  radically different domains require fundamentally different Case
    File structures;
2.  Goal lifecycle cannot remain locally scoped;
3.  the App representation must dictate the underlying model;
4.  Missions cannot connect model decisions to reality;
5.  the Engine cannot propose useful next steps from Case File history;
6.  the generic mechanism becomes so complex that users must learn the
    methodology to use it.

If one occurs, report it clearly.

Do not patch around it merely to preserve the current architecture.

------------------------------------------------------------------------

# 21. Working With the Human Designer

The human designer may intentionally leave questions open.

Examples:

-   "We don't know yet."
-   "This can be changed later."
-   "This is only inspiration."
-   "The App structure is temporary."
-   "We need to test this first."

These statements are meaningful.

Do not interpret uncertainty as missing requirements that you should
automatically fill in.

Sometimes the correct implementation is to preserve the uncertainty.

------------------------------------------------------------------------

# 22. Repository Discipline

When creating or modifying documents:

-   preserve existing terminology;
-   inspect related documents first;
-   avoid duplicate competing specifications;
-   update the appropriate existing document when possible;
-   create a new document when a genuinely new concern deserves one;
-   keep versioned experimental documents clearly marked;
-   do not delete exploratory material merely because it is imperfect
    unless explicitly asked.

The repository is part of the model-development history.

------------------------------------------------------------------------

# 23. Suggested Development Sequence

For the first prototype:

``` text
1. Inspect existing App
       ↓
2. Define smallest Case File representation
       ↓
3. Simulate App → Engine message
       ↓
4. Simulate Engine proposal
       ↓
5. Simulate user decision
       ↓
6. Simulate Mission
       ↓
7. Simulate result / evidence
       ↓
8. Update Case File
       ↓
9. Generate next proposal
       ↓
10. Run real example
       ↓
11. Record what breaks
```

Do not jump directly to a sophisticated AI architecture.

------------------------------------------------------------------------

# 24. The Most Important Rule

> **Do not protect the model from reality.**

If the prototype exposes a contradiction:

-   don't hide it;
-   don't rationalize it;
-   don't automatically add abstraction;
-   don't assume the user is wrong.

Show the contradiction.

That is why we are building the prototype.

------------------------------------------------------------------------

# 25. Current Gate

The project is currently at:

``` text
EXPLORATION
    ↓
CONCEPTUAL MODEL
    ↓
EXAMPLES / TESTS
    ↓
REALITY CHECK
    ↓
► SMALL LIVE PROTOTYPE
    ↓
BREAK / LEARN / MODIFY
```

The current objective is not to finish the Engine.

The objective is to make the smallest useful system that allows the
model to encounter reality.

------------------------------------------------------------------------

# 26. Final Instruction to the Coding AI

When in doubt:

> **Keep it small. Keep it reversible. Keep the distinction between
> model and implementation. Surface uncertainty. Test the assumption.**

And remember:

> **The goal of this prototype is not to prove that we were right. It is
> to discover where we are wrong --- cheaply.**
