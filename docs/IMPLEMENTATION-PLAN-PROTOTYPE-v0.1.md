# Implementation Plan --- Minimal First Prototype v0.1

## 1. Purpose

This document defines the smallest useful implementation of the
Engine/App prototype.

It is deliberately an implementation plan, not a final architecture
specification.

The prototype exists to make the current model encounter reality.

The primary question is:

> **Can a Case File carry continuity through an App → Engine → User →
> Mission → Observation → Case File loop and produce a useful next
> step?**

If the answer is no, that is a successful prototype outcome: we have
discovered something that needs to change before building further.

------------------------------------------------------------------------

# 2. Scope

The first prototype should implement one complete, executable loop.

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
RESULT / OBSERVATION
   ↓
CASE FILE UPDATE
   ↓
NEXT PROPOSAL
```

The prototype should be small enough that the model can still be changed
cheaply.

------------------------------------------------------------------------

# 3. Prototype Boundaries

## 3.1 In Scope

The prototype should support:

-   opening a Case File;
-   entering an initial user/context description;
-   representing one or more Goals;
-   representing a Goal lifecycle;
-   producing an Engine proposal;
-   presenting the proposal to the user;
-   accepting a user decision;
-   creating a Mission from an accepted proposal;
-   recording a simulated result/observation;
-   updating the Case File;
-   using the updated Case File for the next Engine proposal;
-   maintaining multiple Goals independently;
-   demonstrating that `GIVE UP` on one Goal does not invalidate other
    Goals.

## 3.2 Deliberately Out of Scope

Do not implement production versions of:

-   authentication;
-   organisation permissions;
-   multi-tenant architecture;
-   production GPS verification;
-   sophisticated evidence management;
-   universal challenge generation;
-   final AI orchestration;
-   graph database;
-   production-scale storage;
-   advanced analytics;
-   production deployment architecture;
-   final App integration;
-   final API versioning strategy.

Where necessary, simulate these capabilities.

------------------------------------------------------------------------

# 4. Prototype Architecture

Use the simplest architecture that supports the loop.

Conceptually:

``` text
┌──────────────────────┐
│        APP           │
│                      │
│ User interaction     │
│ Case presentation    │
│ Proposal presentation│
│ Decision             │
│ Mission/result input │
└──────────┬───────────┘
           │
           │ prototype contract
           ▼
┌──────────────────────┐
│       ENGINE         │
│                      │
│ Case interpretation  │
│ Proposal generation  │
│ Next-step reasoning  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      CASE FILE       │
│                      │
│ Context              │
│ Goals                │
│ Missions             │
│ Decisions            │
│ Observations         │
│ Evidence             │
│ History              │
└──────────────────────┘
```

This is a conceptual arrangement.

Do not introduce separate services merely because the diagram contains
separate responsibilities.

------------------------------------------------------------------------

# 5. First Implementation Principle

> **Prefer simulation over infrastructure when infrastructure is not
> necessary to test the model.**

For example:

-   a simulated Engine is acceptable initially;
-   a local Case File is acceptable;
-   simulated observations are acceptable;
-   a simple in-memory store is acceptable;
-   a minimal API boundary is acceptable.

The first prototype should answer model questions, not infrastructure
questions.

------------------------------------------------------------------------

# 6. Minimal Case File

The Case File should contain only enough information to support
continuity.

A conceptual example:

``` text
Case File
│
├── identity / case metadata
│
├── context
│
├── goals[]
│    ├── desired direction
│    ├── status
│    ├── time scope
│    ├── geographic scope
│    ├── definition of done
│    ├── missions[]
│    └── history
│
├── observations[]
├── evidence[]
├── decisions[]
└── history
```

This is a working representation.

It is not a final schema.

Do not add fields merely because they might be useful someday.

------------------------------------------------------------------------

# 7. Goal Lifecycle

The first prototype needs only enough lifecycle states to demonstrate
independence.

For example:

``` text
ACTIVE
COMPLETED
ABANDONED
```

Additional states may be introduced if the prototype requires them.

The important rule is:

> **Goal lifecycle is local to the Goal.**

Example:

``` text
CASE FILE
│
├── Goal A — ACTIVE
├── Goal B — ACTIVE
└── Goal C — ABANDONED
```

The Case File remains active.

------------------------------------------------------------------------

# 8. Initial User Interaction

The first interaction should remain user-oriented rather than
methodology-oriented.

The prototype can begin with:

> **What are we working on right now?**

The user may then provide a free-form description.

The App/Engine can use that information to establish initial context.

Do not require the user to understand:

-   transition methodology;
-   Case Files;
-   Goals;
-   Missions;
-   Evidence models;
-   ontology.

Those are internal concepts.

------------------------------------------------------------------------

# 9. Identity / Direction

After the initial interaction, the prototype may receive a mildly
described desired identity or direction.

For example:

``` text
"I want to become more connected to my local community."
```

or:

``` text
"We want Skördefesten to improve the visitor experience next year."
```

The Engine may interpret this as a candidate Goal or desired direction.

The prototype should not force a rigid identity schema.

------------------------------------------------------------------------

# 10. Engine Proposal

The Engine receives sufficient Case File context to produce a proposal.

A proposal should contain enough information for the user to understand:

-   what is being proposed;
-   why it is relevant;
-   what the user could do next;
-   what completion might look like, where appropriate.

The proposal should not require the user to understand internal model
terminology.

A simplified conceptual result might be:

``` text
PROPOSAL

Direction:
Improve connection with local community.

Suggested Mission:
Visit three local meeting places and have one
structured conversation at each.

Why:
This provides direct observations about where
connection already exists and where it is missing.

Done when:
Three visits and three recorded observations
have been completed.
```

This is illustrative only.

The Engine must remain generic.

------------------------------------------------------------------------

# 11. User Decision

The prototype must support:

``` text
ACCEPT
MODIFY
REJECT
EXPLORE FURTHER
GIVE UP
```

## ACCEPT

Create or activate the corresponding Mission/next step.

## MODIFY

Allow the user to alter the proposal before continuing.

## REJECT

Discard the proposal without necessarily changing the Goal.

## EXPLORE FURTHER

Return additional exploration rather than committing to the Mission.

## GIVE UP

Abandon the relevant Goal.

Important:

> `GIVE UP` on Goal C must not invalidate Goal A or Goal B.

------------------------------------------------------------------------

# 12. Mission

An accepted proposal becomes a Mission.

A minimal Mission should contain enough information to:

-   describe what is to be done;
-   identify which Goal it belongs to;
-   identify relevant time/geographic scope where applicable;
-   record its status;
-   receive a result.

Example:

``` text
MISSION
Goal: Community connection

Action:
Visit three local meeting places.

Status:
ACTIVE

Definition of Done:
3 completed visits + observations.
```

Do not build a full task-management system.

------------------------------------------------------------------------

# 13. Result / Observation

For the first prototype, the user can submit a simulated result.

Example:

``` text
MISSION RESULT

Visited:
Place A
Place B
Place C

Observation:
Place B appears to be the strongest existing
connection point.

Unexpected:
A new organisation was identified.
```

The important thing is that the result becomes part of the Case File.

------------------------------------------------------------------------

# 14. Evidence

Evidence should initially be simple.

A prototype may use:

``` text
Evidence type:
USER_CONFIRMED
```

or:

``` text
Evidence type:
SIMULATED
```

GPS and other verification mechanisms can be added later.

Do not attempt to solve the complete evidence problem in v0.1.

The requirement is simply:

> **The Case File must be able to retain observations/evidence that
> influence later reasoning.**

------------------------------------------------------------------------

# 15. Case File Update

After the Mission result:

``` text
Mission
   ↓
Result
   ↓
Observation / Evidence
   ↓
Case File Update
```

The Case File must retain enough history that the Engine can
distinguish:

``` text
BEFORE
```

from:

``` text
AFTER
```

The next proposal should be based on the updated state.

------------------------------------------------------------------------

# 16. Continuity Test

This is one of the most important tests.

Run:

``` text
INITIAL INPUT
    ↓
PROPOSAL A
    ↓
MISSION A
    ↓
OBSERVATION A
    ↓
UPDATED CASE FILE
    ↓
PROPOSAL B
```

Then verify:

> Proposal B reflects information discovered during Mission A.

If Proposal B could have been generated without knowing anything about
Mission A, the continuity mechanism has not yet been demonstrated.

------------------------------------------------------------------------

# 17. Multiple Goal Test

Create:

``` text
Goal A — ACTIVE
Goal B — ACTIVE
Goal C — ACTIVE
```

Then:

``` text
GIVE UP → Goal C
```

Expected:

``` text
Goal A — ACTIVE
Goal B — ACTIVE
Goal C — ABANDONED
```

The Case File remains valid.

Goal A and Goal B remain usable.

Their histories remain intact.

------------------------------------------------------------------------

# 18. App ↔ Engine Contract

The first implementation should expose only the information necessary
for the loop.

Conceptually:

### App → Engine

``` text
Case context
User input
Current Goal context
Relevant history
User decision
Mission result
Observation / evidence
```

### Engine → App

``` text
Proposal
Reason / explanation
Suggested next step
Mission
Relevant Definition of Done
```

The exact transport format is intentionally undecided.

JSON is acceptable for v0.1 if convenient.

Do not treat the v0.1 JSON structure as the final API.

------------------------------------------------------------------------

# 19. Suggested v0.1 Message Shape

If a concrete format is needed, use a deliberately simple envelope.

Illustrative only:

``` json
{
  "case_id": "case-001",
  "message_type": "proposal_request",
  "context": {},
  "goal_id": "goal-001",
  "payload": {}
}
```

And:

``` json
{
  "case_id": "case-001",
  "message_type": "proposal",
  "goal_id": "goal-001",
  "payload": {
    "proposal": {},
    "reason": ""
  }
}
```

This is not the final contract.

The coding AI should be free to suggest a better minimal representation
if implementation experience shows that something is missing or
unnecessary.

------------------------------------------------------------------------

# 20. Test Cases

## Test 1 --- Open Case

Input:

``` text
What are we working on right now?
```

Expected:

-   Case File created/opened.
-   Initial context stored.

------------------------------------------------------------------------

## Test 2 --- Establish Direction

Input:

``` text
A mildly described desired identity/direction.
```

Expected:

-   Engine can represent it as context and/or candidate Goal.
-   User is not required to understand the internal terminology.

------------------------------------------------------------------------

## Test 3 --- Proposal

Expected:

-   Engine produces a useful proposal.
-   Proposal is understandable without reading the model documentation.

------------------------------------------------------------------------

## Test 4 --- Accept

Expected:

-   Proposal becomes an actionable Mission.
-   Mission is attached to the correct Goal.

------------------------------------------------------------------------

## Test 5 --- Modify

Expected:

-   User can alter the proposal.
-   Modified version becomes the relevant Mission/proposal state.

------------------------------------------------------------------------

## Test 6 --- Reject

Expected:

-   Proposal is rejected.
-   Goal remains available unless separately abandoned.

------------------------------------------------------------------------

## Test 7 --- Explore Further

Expected:

-   Engine continues exploration.
-   No premature commitment to a Mission.

------------------------------------------------------------------------

## Test 8 --- Give Up

Expected:

-   Relevant Goal becomes `ABANDONED`.
-   Other Goals remain unchanged.

------------------------------------------------------------------------

## Test 9 --- Mission Result

Expected:

-   Mission result is stored.
-   Observation/evidence is stored.
-   Case File changes.

------------------------------------------------------------------------

## Test 10 --- Continuity

Expected:

-   Next Engine proposal can use the newly stored result.

------------------------------------------------------------------------

## Test 11 --- Multiple Goals

Expected:

-   Several Goals coexist.
-   Each has independent lifecycle.
-   A decision on one does not unexpectedly change another.

------------------------------------------------------------------------

# 21. Prototype Acceptance Criteria

The first prototype is good enough when all of the following are
demonstrable:

### A. Case continuity

A Case can be opened and updated.

### B. Goal independence

At least three Goals can coexist and one can be abandoned without
invalidating the others.

### C. Proposal loop

The Engine can propose a next step from Case File context.

### D. User agency

The user can:

``` text
ACCEPT
MODIFY
REJECT
EXPLORE FURTHER
GIVE UP
```

### E. Mission connection

An accepted proposal can become a Mission.

### F. Reality feedback

A Mission can produce a simulated result/observation.

### G. Updated reasoning

The result changes the information available for the next loop.

### H. App independence

The underlying Case File logic is not dependent on the App's current
tree representation.

------------------------------------------------------------------------

# 22. What Success Does NOT Mean

Success does not mean:

-   we have found the final architecture;
-   we have solved AI generation;
-   we have solved evidence;
-   we have solved permissions;
-   we have solved multi-organisation operation;
-   we have solved GPS;
-   we have created a production-ready App;
-   we have validated the complete model.

Success means:

> **We have made the core loop executable and observable.**

------------------------------------------------------------------------

# 23. What to Record During Development

When something unexpected happens, record it.

Use a simple structure:

``` text
OBSERVATION

What happened?

WHY IT MATTERS

What assumption did it challenge?

CLASSIFICATION

MODEL
UI
APP CAPABILITY
ENGINE REASONING
CONTRACT
ENGINEERING

NEXT QUESTION

What should we investigate?
```

Do not automatically convert every observation into a requirement.

------------------------------------------------------------------------

# 24. Development Order

Implement in this order unless reality gives a good reason to change it:

``` text
1. Case File
      ↓
2. Goal
      ↓
3. Basic App interaction
      ↓
4. App → Engine boundary
      ↓
5. Engine proposal
      ↓
6. User decision
      ↓
7. Mission
      ↓
8. Result / Observation
      ↓
9. Case File update
      ↓
10. Next proposal
      ↓
11. Multiple Goal test
```

Only after this works should we expand.

------------------------------------------------------------------------

# 25. First Demonstration

The first meaningful demonstration should be possible without a large
amount of setup.

Ideally:

``` text
START
 ↓
"What are we working on?"
 ↓
describe direction
 ↓
proposal
 ↓
ACCEPT
 ↓
Mission
 ↓
simulate result
 ↓
Case File updated
 ↓
new proposal
```

Then:

``` text
add Goal A
add Goal B
add Goal C
 ↓
GIVE UP Goal C
 ↓
verify A and B remain alive
```

This is enough for the first gate.

------------------------------------------------------------------------

# 26. Stop Conditions

Stop implementation and review the model if:

-   the Case File becomes difficult to represent;
-   the App tree starts dictating the underlying model;
-   multiple Goals interfere unexpectedly;
-   the Engine cannot use accumulated history;
-   the App ↔ Engine boundary becomes unexpectedly large;
-   simple concepts require many special cases;
-   the prototype requires substantial infrastructure just to function.

These are signals, not failures.

------------------------------------------------------------------------

# 27. Explicit Non-Goals for v0.1

Do not attempt to solve:

``` text
EVERY DOMAIN
EVERY USER TYPE
EVERY ORGANISATION MODEL
EVERY EVIDENCE TYPE
EVERY GEOGRAPHIC MODEL
EVERY AI CAPABILITY
EVERY PERMISSION CASE
EVERY FAILURE MODE
```

The first prototype is deliberately narrow.

------------------------------------------------------------------------

# 28. Implementation Principle

> **If a simpler implementation can test the same model assumption,
> choose the simpler implementation.**

And:

> **If a feature cannot be justified by the current prototype loop,
> defer it.**

------------------------------------------------------------------------

# 29. First Gate

The first implementation gate is passed when we can run:

``` text
CASE
 ↓
GOAL
 ↓
PROPOSAL
 ↓
DECISION
 ↓
MISSION
 ↓
OBSERVATION
 ↓
CASE UPDATE
 ↓
NEXT PROPOSAL
```

and demonstrate:

``` text
Goal A — alive
Goal B — alive
Goal C — given up
```

without losing continuity.

At that point we stop and assess what reality taught us.

------------------------------------------------------------------------

# 30. Guiding Principle

> **Make the first prototype small enough to throw away, but real enough
> to teach us something.**

That is the purpose of v0.1.
