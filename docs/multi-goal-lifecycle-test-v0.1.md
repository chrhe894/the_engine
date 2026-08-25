# Multi-Goal Lifecycle Test --- v0.1

## Purpose

This test stresses the Case File with several Goals that are alive at
the same time.

The Goals deliberately have different:

-   purposes
-   time limits
-   geographic scopes
-   participants
-   Missions
-   evidence requirements
-   completion conditions

One Goal is deliberately abandoned.

The test asks:

> **Can one Case File contain several independently evolving Goals
> without one Goal's lifecycle invalidating the others?**

------------------------------------------------------------------------

# 1. Starting Case File

Scenario: Södra Öland / Skördefesten.

``` text
CASE FILE
│
├── Context
│     Södra Öland
│     Skördefesten
│
├── Goal A
│     Explore local places
│
├── Goal B
│     Increase youth participation
│
└── Goal C
      Test a new visitor experience
```

All three Goals belong to the same Case File.

They are related, but they are not the same Goal.

------------------------------------------------------------------------

# 2. Goal A --- Local Exploration

``` text
Goal A

Purpose
  Encourage people to discover local places.

Time
  1 May → 30 September

Geographic scope
  Södra Öland

Participants
  Open to participants in the area.

Execution
  Visit selected places.

Evidence
  GPS verification.

Definition of Done
  Visit 8 selected places.
```

Lifecycle:

``` text
PROPOSED
   ↓
ACCEPTED
   ↓
ACTIVE
```

Goal A remains active throughout the test.

------------------------------------------------------------------------

# 3. Goal B --- Youth Participation

``` text
Goal B

Purpose
  Increase meaningful youth participation.

Time
  January → October

Geographic scope
  Selected festival locations.

Participants
  Festival organisation
  Young participants
  Local organisations

Execution
  Co-design and test an activity.

Evidence
  Participant feedback
  Activity record

Definition of Done
  One activity designed and tested.
```

Lifecycle:

``` text
PROPOSED
   ↓
ACCEPTED
   ↓
ACTIVE
```

Goal B also remains active.

------------------------------------------------------------------------

# 4. Goal C --- New Visitor Experience

``` text
Goal C

Purpose
  Test a new visitor experience.

Time
  June → August

Geographic scope
  One selected festival area.

Participants
  Visitors
  Local businesses

Execution
  Create and test a new experience.

Evidence
  Visitor feedback
  Participation count

Definition of Done
  One pilot completed and evaluated.
```

Lifecycle:

``` text
PROPOSED
   ↓
ACCEPTED
   ↓
ACTIVE
```

At this point:

``` text
CASE FILE
│
├── Goal A — ACTIVE
├── Goal B — ACTIVE
└── Goal C — ACTIVE
```

------------------------------------------------------------------------

# 5. Different Contexts Within One Case File

The Goals do not inherit one universal context.

``` text
CASE FILE
│
├── Goal A
│     Time: May–September
│     Area: Södra Öland
│     Participants: open
│
├── Goal B
│     Time: January–October
│     Area: selected festival locations
│     Participants: youth + organisations
│
└── Goal C
      Time: June–August
      Area: one selected area
      Participants: visitors + businesses
```

This is important.

The Case File provides the shared context.

Each Goal carries the context that is specific to its own lifecycle.

------------------------------------------------------------------------

# 6. Goal A Progresses

Participants complete several location challenges.

``` text
Goal A

Completed visits:
  5 / 8

Evidence:
  GPS verification

Observation:
  Participants are completing the
  challenges but some locations
  are difficult to reach.
```

Goal A remains:

``` text
ACTIVE
```

The observation may influence future Missions without affecting Goals B
or C.

------------------------------------------------------------------------

# 7. Goal B Progresses

A co-design Mission is completed.

``` text
Goal B

Mission:
  Co-design youth activity

Observation:
  Young participants prefer
  shorter activities.

Evidence:
  Participant feedback.

Updated direction:
  Design a shorter activity.
```

Goal B remains:

``` text
ACTIVE
```

------------------------------------------------------------------------

# 8. Goal C Fails

The visitor experience is tested.

The result is poor.

``` text
Goal C

Observation:
  Too few visitors participated.

Evidence:
  Participation count
  Visitor feedback

Assessment:
  Current concept does not justify
  another pilot at this time.
```

The user chooses:

``` text
GIVE UP
```

Goal C becomes:

``` text
ABANDONED
```

------------------------------------------------------------------------

# 9. Critical Test

The Case File now looks like:

``` text
CASE FILE
│
├── Goal A — ACTIVE
│
├── Goal B — ACTIVE
│
└── Goal C — ABANDONED
```

Nothing about Goal C's abandonment invalidates Goal A.

Nothing about Goal C's abandonment invalidates Goal B.

The Case File remains active.

This is a fundamental rule.

> **Goal lifecycle is local to the Goal unless an explicit relationship
> causes an effect elsewhere.**

------------------------------------------------------------------------

# 10. Goal C Can Still Produce Knowledge

Although Goal C is abandoned, it does not disappear.

``` text
Goal C
  │
  ├── Missions
  ├── Observations
  ├── Evidence
  ├── Decisions
  └── Abandonment reason
```

The result may be useful elsewhere.

For example:

``` text
Goal C
  │
  └── Observation
        "Visitors did not engage with
         long-form experiences."
                │
                ├────────► Goal A
                │
                └────────► Goal B
```

The Engine may later use this information when proposing Missions.

The abandoned Goal remains part of the Case history.

------------------------------------------------------------------------

# 11. A Goal Can Affect Another Goal

The Goals are independent, but they can be related.

For example:

``` text
Goal A
  Local exploration
       │
       │ discovers
       ▼
   local place
       │
       └────────► Goal B
                   youth activity
```

Or:

``` text
Goal C
  visitor experience
       │
       └── observation ──► Goal A
```

This suggests:

> **Independent lifecycle does not mean isolated information.**

A Goal can finish while its knowledge continues to exist.

------------------------------------------------------------------------

# 12. The Case File Is Not a Project Status Board

A tempting implementation would be:

``` text
Case File
 ├── Goal A
 ├── Goal B
 └── Goal C

status:
  active
  active
  abandoned
```

That is insufficient.

The Case File must preserve:

``` text
Goals
+
Goal-specific contexts
+
Goal lifecycles
+
Missions
+
Observations
+
Evidence
+
Relationships
+
History
```

The status is only one small part of the model.

------------------------------------------------------------------------

# 13. Different Clocks

The test also exposes another requirement.

The Goals have different time limits:

``` text
Goal A
May ───────────────── September

Goal B
January ───────────────────────── October

Goal C
June ───────── August
```

The Case File therefore cannot have one universal "deadline".

A Case File can contain many temporal scopes.

The same applies to:

-   geographic areas
-   routes
-   participant groups
-   access permissions
-   evidence requirements
-   Definitions of Done

These belong naturally to the relevant Goal or other relevant object.

------------------------------------------------------------------------

# 14. Geographic Scope

The same principle applies spatially.

``` text
CASE FILE
│
├── Goal A
│     Polygon: Södra Öland
│
├── Goal B
│     Locations: selected festival sites
│
└── Goal C
      Polygon: one visitor area
```

The App can use its GPS/location capabilities to execute the Goal.

The Engine does not necessarily need to know how GPS verification works.

It needs to understand the semantic result:

``` text
Evidence:
  participant was verified at location X
```

This keeps engineering mechanisms separate from the generic model.

------------------------------------------------------------------------

# 15. Multiple Missions

A Goal may contain several Missions simultaneously or sequentially.

``` text
Goal B
│
├── Mission 1 — Ask young people
│       ↓
│   Observation
│
├── Mission 2 — Design activity
│       ↓
│   Observation
│
└── Mission 3 — Pilot activity
        ↓
    Evidence
```

Some Missions may be:

``` text
COMPLETED
ACTIVE
BLOCKED
ABANDONED
```

One Mission being abandoned does not automatically abandon the Goal.

The Goal may instead be modified.

------------------------------------------------------------------------

# 16. Goal Lifecycle vs Mission Lifecycle

These should not be confused.

``` text
Goal
│
├── Mission A — COMPLETED
├── Mission B — ABANDONED
├── Mission C — ACTIVE
│
└── Goal — ACTIVE
```

Possible consequence:

``` text
Mission B abandoned
        ↓
reassessment
        ↓
Mission C proposed
```

Not:

``` text
Mission B abandoned
        ↓
everything stops
```

------------------------------------------------------------------------

# 17. Goal-Level GIVE UP

`GIVE UP` at the Goal level means:

``` text
Goal C
   ↓
GIVE UP
   ↓
ABANDONED
```

It does **not** mean:

``` text
Case File
   ↓
GIVE UP
   ↓
everything abandoned
```

Unless the user explicitly chooses to abandon the entire Case File.

That distinction should remain explicit.

------------------------------------------------------------------------

# 18. Case-Level GIVE UP

A separate possibility exists:

``` text
CASE FILE
   ↓
GIVE UP
```

This would mean:

> The participant no longer wants to continue the overall effort
> represented by this Case File.

That is fundamentally different from abandoning one Goal.

The prototype should keep these as separate decisions.

------------------------------------------------------------------------

# 19. What Happens When a Goal Is Completed?

Completion is also local.

``` text
Goal A
   ↓
Definition of Done satisfied
   ↓
COMPLETED
```

The Case File continues:

``` text
CASE FILE
│
├── Goal A — COMPLETED
├── Goal B — ACTIVE
└── Goal C — ABANDONED
```

This is a perfectly valid state.

The Case File can contain:

-   completed Goals
-   active Goals
-   paused Goals
-   abandoned Goals
-   proposed Goals

at the same time.

------------------------------------------------------------------------

# 20. Result of the Stress Test

The model survives the test.

The following principle becomes stronger:

> **A Case File is a container for multiple independently evolving
> Goals.**

Each Goal may carry its own:

-   desired outcome
-   temporal scope
-   geographic scope
-   route or locations
-   participants
-   constraints
-   Missions
-   Definition of Done
-   Evidence requirements
-   lifecycle
-   history

Goals may interact, but one Goal's lifecycle does not automatically
determine another's.

------------------------------------------------------------------------

# 21. Emerging Structural Model

A more accurate conceptual picture is now:

``` text
                       CASE FILE
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
       GOAL A           GOAL B           GOAL C
          │                │                │
     lifecycle        lifecycle        lifecycle
          │                │                │
     Missions          Missions         Missions
          │                │                │
     Evidence          Evidence         Evidence
          │                │                │
          └──────────── relationships ──────┘
                           │
                      observations
                           │
                       history
```

This is already beginning to look like a network rather than a tree.

The tree remains useful as a user-facing representation.

------------------------------------------------------------------------

# 22. New Working Principle

> **The Case File provides continuity; Goals provide independently
> evolving commitments; Missions provide executable steps; observations
> and evidence provide feedback from reality.**

This is a working principle, not a final ontology.

------------------------------------------------------------------------

# 23. What We Have Now

We have tested:

-   different domains
-   multiple Goals
-   different time scopes
-   different geographic scopes
-   different participants
-   multiple Missions
-   Goal-level `GIVE UP`
-   Mission-level failure
-   Goal completion
-   knowledge surviving Goal abandonment
-   relationships between Goals

The model has not collapsed.

Instead, it has become slightly clearer.

------------------------------------------------------------------------

# 24. Next Unknowns

Do not solve these yet.

The next interesting tests would eventually include:

-   conflicting Goals
-   competing resources
-   multiple organisations
-   permissions and access
-   one observation affecting several Goals
-   one Goal depending on another
-   Goals created by different actors
-   changing ownership
-   conflicting evidence
-   Case File merging / splitting
-   geographic contexts nested inside one another

These are deliberately left for later.

------------------------------------------------------------------------

# Current Gate Result

**PASS --- with new constraints identified.**

The Case File can contain multiple independent Goal lifecycles.

The most important constraint discovered is:

> **Never allow a local Goal decision to implicitly become a Case File
> decision.**

------------------------------------------------------------------------

# Pause Point

This is a good place to stop and reflect.

We now have enough structure to begin seeing the architecture, but not
enough certainty to justify locking it down.

That is intentional.
