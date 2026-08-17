# Live Case File Loop --- Prototype Gate v0.1

## Purpose

This is the smallest executable/prototypable loop for making the Case
File "live".

The purpose is **not** to build the production Engine.

The purpose is to test whether:

-   a Case File can persist through multiple turns;
-   App and Engine can exchange meaningful information;
-   decisions can change the Case File;
-   Missions can produce observations;
-   observations can change the next proposal;
-   the user can remain unaware of the underlying model concepts.

The prototype should deliberately be small.

------------------------------------------------------------------------

# 1. Prototype Principle

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
CASE FILE UPDATE
   ↓
MISSION
   ↓
OBSERVATION / EVIDENCE
   ↓
CASE FILE UPDATE
   ↓
NEXT PROPOSAL
```

The loop should be capable of repeating.

The Case File is the continuity mechanism between iterations.

------------------------------------------------------------------------

# 2. Prototype Boundary

For this gate, do **not** solve:

-   production AI
-   authentication
-   organisation management
-   permissions architecture
-   database selection
-   graph database
-   production synchronization
-   final API
-   complete Mission system
-   complete Evidence system
-   final UI
-   all possible domain types

The prototype only needs enough structure to expose problems in the
model.

------------------------------------------------------------------------

# 3. Minimal Case File

The prototype can begin with a deliberately small representation.

Conceptually:

``` text
CaseFile
│
├── id
├── context
├── current_situation
├── desired_direction
├── active_items
├── decisions
├── missions
├── observations
├── evidence
└── history
```

The names are provisional.

The structure should remain easy to change.

------------------------------------------------------------------------

# 4. Events

The App and Engine should not need to exchange the entire universe on
every interaction.

A small event vocabulary is sufficient for the prototype.

Examples:

``` text
CASE_OPENED
USER_INPUT
USER_DECISION
MISSION_ACCEPTED
MISSION_COMPLETED
OBSERVATION_ADDED
EVIDENCE_ADDED
CASE_UPDATED
```

These are examples, not a final protocol.

------------------------------------------------------------------------

# 5. App → Engine

The App sends information that is relevant to the current situation.

Example:

``` text
{
  "type": "USER_INPUT",
  "case_id": "case-001",
  "content": {
    "text": "I don't know what I want to do."
  }
}
```

The App may also provide situated information when relevant.

For example:

``` text
{
  "type": "USER_INPUT",
  "case_id": "case-001",
  "context": {
    "location": "Södra Öland",
    "available_capabilities": [
      "location_cards",
      "mission_cards",
      "gps_verification"
    ]
  },
  "content": {
    "text": "I want to find something interesting to explore."
  }
}
```

The exact representation is intentionally not fixed.

------------------------------------------------------------------------

# 6. Engine Response

The Engine should return a **proposal**, not silently mutate the Case
File.

Example:

``` text
{
  "type": "PROPOSAL",
  "case_id": "case-001",
  "proposal": {
    "kind": "exploration",
    "description": "Explore possible occupations."
  },
  "choices": [
    "ACCEPT",
    "MODIFY",
    "REJECT",
    "EXPLORE_FURTHER",
    "GIVE_UP"
  ]
}
```

The App decides how this is presented to the user.

------------------------------------------------------------------------

# 7. User Decision

The App records the user's decision.

Example:

``` text
{
  "type": "USER_DECISION",
  "case_id": "case-001",
  "decision": "ACCEPT",
  "proposal_id": "proposal-001"
}
```

The important semantic rule is:

> **The Engine proposes. The user decides.**

------------------------------------------------------------------------

# 8. Case File Update

The Case File then changes.

For example:

``` text
Before

Current Situation:
  No clear occupational direction.

Desired Direction:
  Unknown.
```

After acceptance:

``` text
Current Situation:
  No clear occupational direction.

Desired Direction:
  Explore possible occupations.

Active Item:
  Occupational exploration.
```

The previous state should remain available in history where useful.

------------------------------------------------------------------------

# 9. Mission Creation

The Engine may propose a Mission as a consequence of the Case File.

Example:

``` text
{
  "type": "MISSION_PROPOSAL",
  "case_id": "case-001",
  "mission": {
    "title": "Talk to a software developer",
    "purpose": "Test interest in software development",
    "definition_of_done": [
      "conversation completed",
      "three questions asked",
      "reflection recorded"
    ]
  }
}
```

The App can translate this into its existing Mission representation.

The user should not need to understand that the Engine created a
"Mission object".

------------------------------------------------------------------------

# 10. Mission Execution

The App is responsible for execution.

For example:

``` text
App
  ↓
show challenge
  ↓
user performs activity
  ↓
App gathers result
  ↓
App verifies available evidence
  ↓
App sends result to Engine
```

The App may use its existing capabilities:

-   GPS
-   cards
-   forms
-   surveys
-   confirmations
-   local context
-   user input

------------------------------------------------------------------------

# 11. Mission Result

Example:

``` text
{
  "type": "MISSION_COMPLETED",
  "case_id": "case-001",
  "mission_id": "mission-001",
  "result": {
    "completed": true,
    "observation": "Software development seems interesting.",
    "evidence": [
      {
        "type": "USER_RECORDED_OBSERVATION"
      }
    ]
  }
}
```

The prototype does not need a sophisticated Evidence framework yet.

The important thing is that **something happened in reality and the Case
File can learn from it**.

------------------------------------------------------------------------

# 12. Observation Changes the Case File

This is the most important test.

Before the Mission:

``` text
Interest:
  unknown
```

After the Mission:

``` text
Observation:
  "Software development seems interesting."

Updated understanding:
  interest appears positive.

New uncertainty:
  Is the perceived difficulty acceptable?
```

The Engine should now reason from the **new situation**, not simply
continue the old plan.

------------------------------------------------------------------------

# 13. The Loop

The entire prototype can therefore be represented as:

``` text
┌──────────────────────┐
│      CASE FILE       │
└──────────┬───────────┘
           │
           ▼
     Current state
           │
           ▼
┌──────────────────────┐
│       ENGINE         │
│      proposes        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│        APP           │
│   presents choice    │
└──────────┬───────────┘
           │
           ▼
        USER
           │
           ▼
     Decision
           │
           ▼
┌──────────────────────┐
│        APP           │
│      executes        │
└──────────┬───────────┘
           │
           ▼
      Reality
           │
           ▼
 Observation / Evidence
           │
           ▼
┌──────────────────────┐
│      CASE FILE       │
│       updated        │
└──────────┬───────────┘
           │
           └──────────► next loop
```

------------------------------------------------------------------------

# 14. User Experience

The underlying protocol may be relatively sophisticated.

The visible App should remain simple.

A possible interaction:

``` text
WHAT ARE WE WORKING ON RIGHT NOW?

> I don't know what I want to do.

────────────────────────

HERE'S SOMETHING WE COULD TRY

Explore a few occupations and see
which ones make you curious.

[ ACCEPT ]

[ MODIFY ]

[ REJECT ]

[ EXPLORE FURTHER ]

[ GIVE UP ]
```

After acceptance:

``` text
YOUR NEXT CHALLENGE

Talk to someone who works in a field
you are curious about.

[ START ]
```

After completion:

``` text
WHAT DID YOU DISCOVER?

> It seems interesting, but difficult.

────────────────────────

WHAT SHOULD WE DO NOW?

[ Try a small programming challenge ]
[ Learn what skills are needed ]
[ Talk to someone else ]
[ Explore another direction ]
[ Give up ]
```

The user experiences a natural conversation.

The Case File underneath maintains continuity.

------------------------------------------------------------------------

# 15. Skördefesten Test

The same loop should work with a completely different case.

``` text
Opening context:
  Södra Öland / Skördefesten

User:
  We want more young people involved.

Engine:
  proposes exploration

User:
  ACCEPT

Engine:
  proposes a small co-design challenge

App:
  executes challenge

Reality:
  young people participate

Evidence:
  feedback / survey / confirmation

Observation:
  they like the idea but timing is wrong

Case File:
  updated

Engine:
  proposes changing the timing
```

No special "Skördefesten Engine" should be required.

------------------------------------------------------------------------

# 16. The App as Translator

The App may translate between:

``` text
GENERIC CASE FILE / ENGINE
             ↕
        APP LANGUAGE
             ↕
           USER
```

For example:

``` text
Engine concept:
  Desired Direction

App:
  What would you like to achieve?

Engine concept:
  Mission

App:
  Your Challenge

Engine concept:
  Observation

App:
  What did you discover?

Engine concept:
  Reassessment

App:
  Has anything changed?
```

This mapping is not fixed.

The App representation can evolve without requiring the underlying model
to change.

------------------------------------------------------------------------

# 17. The Case File Should Be Able to Change Shape

The prototype must not assume that the Case File is always:

``` text
Vision
  ↓
Goal
  ↓
Mission
```

It should be possible to encounter:

``` text
Current situation
  ↔
Obstacle
  ↔
Opportunity
  ↔
Person
  ↔
Capability
  ↔
Mission
  ↔
Observation
```

The current App tree can still provide the user's orientation.

The underlying representation remains free to evolve toward a network.

------------------------------------------------------------------------

# 18. Prototype Success Criteria

The prototype is successful if we can demonstrate:

### 1. Continuity

A Case File can survive multiple interactions.

### 2. Separation

App representation and underlying Case File can differ.

### 3. Proposal / decision separation

The Engine can propose without making the user's decision.

### 4. Reality feedback

A Mission can produce an Observation.

### 5. Adaptation

An Observation can change what the Engine proposes next.

### 6. Genericity

The same mechanism works for both:

-   individual occupational exploration
-   Skördefesten / Södra Öland

### 7. Simplicity

The user does not need to understand:

-   Transition
-   Evidence model
-   Case File
-   Engine
-   ontology
-   protocol

------------------------------------------------------------------------

# 19. What We Should Watch For

During the prototype, record every point where we say:

> "We need another concept here."

Do not immediately add the concept.

First ask:

1.  Is the problem actually in the model?
2.  Is it merely a UI problem?
3.  Is it merely an App capability?
4.  Is it merely an Engine reasoning problem?
5.  Is it an information exchange problem?
6.  Is it an engineering problem?

This is important.

The prototype itself is now part of our method development.

------------------------------------------------------------------------

# 20. Next Gate

Once this loop exists, the next gate is not "build more".

Instead:

> **Run the loop until it breaks.**

Use:

1.  Immigrant example
2.  Skördefesten example

Then deliberately introduce:

-   conflicting intentions
-   a failed Mission
-   an unexpected observation
-   `MODIFY`
-   `REJECT`
-   `EXPLORE FURTHER`
-   `GIVE UP`
-   a change of Goal
-   a new participant

Record where the Case File or protocol becomes inadequate.

Those failures become the next inputs to model development.

------------------------------------------------------------------------

# Working Principle

> **Build only enough machinery to make the model encounter reality.**

The purpose of the prototype is not to prove that the model is correct.

It is to discover where it is wrong.
