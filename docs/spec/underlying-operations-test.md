# Underlying Operations — Cross-Method Test

## Status

**Discovery — Phase 1**

This is the first comparative test of the candidate underlying operations
against several methods and process models discussed during Phase 1.

The purpose is not to prove that the methods are equivalent. The purpose is
to identify recurring operations and, especially, the places where the
candidate language fails to explain something important.

---

# Candidate Operations

| Code | Operation | Working meaning |
|---|---|---|
| O | Observe | Establish what appears to be happening. |
| F | Frame | Determine what matters in the current context. |
| I | Imagine | Describe possible different situations. |
| E | Explore | Investigate possibilities, relationships and constraints. |
| V | Evaluate | Assess alternatives and implications. |
| C | Choose | Select a way forward, including deliberate non-action. |
| A | Act | Induce a transition in reality. |
| O' | Observe again | Determine what actually changed. |

`Explore` currently contains two complementary modes:

- **Analysis** — decompose.
- **Synthesis** — combine.

---

# Test 1 — OODA

OODA is treated here at the level of what each named step actually does,
rather than preserving the military terminology.

| OODA step | Underlying operation(s) | Observation |
|---|---|---|
| Observe | O | Direct correspondence. |
| Orient | F + E + V | Orientation appears to contain several operations rather than one. It uses context, experience, interpretation and assessment. |
| Decide | C | Direct correspondence, although deciding may itself be a Transition. |
| Act | A | Direct correspondence. |
| Result / new situation | O' | The consequence feeds the next loop. |

### Finding

OODA strongly supports the idea that named methodology steps can be
**bundles of underlying operations**.

`Orient` is especially important. It should probably not become a primitive
in our model.

---

# Test 2 — ABCD

ABCD is treated according to the four stages discussed during discovery.

| ABCD step | Underlying operation(s) | Observation |
|---|---|---|
| Awareness | F + I | Establish shared understanding and desired direction. |
| Baseline | O + F + E | Establish current reality and identify relevant gaps. |
| Creative solutions | E | Especially Synthesis, but informed by Analysis. |
| Decide / plan | V + C + A | Prioritise, choose a path and turn it into action. |

### Finding

ABCD reinforces the distinction between **Analysis and Synthesis**.

It also reinforces that a "plan" does not have to mean a complete future
path. It can be a prioritised way forward.

---

# Test 3 — Backcasting

| Backcasting activity | Underlying operation(s) | Observation |
|---|---|---|
| Define desired future | I | Imagine a different future. |
| Understand present | O + F | Establish current reality and relevant context. |
| Work backwards | E + V | Explore intermediate configurations and assess their plausibility. |
| Identify steps | C + A | Select and initiate transitions. |
| Reassess | O' | Reality determines whether the assumed path remains useful. |

### Finding

Backcasting primarily changes the **direction from which exploration is
performed**.

It does not require a different information substrate.

The desired future can be used as the starting point for exploration, while
the actual process still proceeds through repeated forward transitions.

---

# Test 4 — Strategic / Tactical / Operative

This test treats the three levels as a dimension separate from the
operations.

| Level | Typical activity | Underlying operations |
|---|---|---|
| Strategic | Establish direction / Vision | F + I + C |
| Tactical | Understand and navigate possibilities | O + F + E + V + C |
| Operative | Perform concrete transition | A + O' |
| Feedback | Reassess | O + F |

### Finding

This is strong evidence that **level and operation are different
dimensions**.

The same operation can occur at different levels.

For example:

- Strategic Observe: observe a major environmental change.
- Tactical Observe: observe a capability gap.
- Operative Observe: observe whether a Mission succeeded.

Therefore Strategic / Tactical / Operative should not become a hierarchy of
information types.

---

# Test 5 — What → How → With What → Verify / Validate → Deliver

| Development step | Underlying operation(s) | Observation |
|---|---|---|
| What? | F + I | Establish what change is wanted or worth pursuing. |
| How? | E + V | Explore and assess possible system-level approaches. |
| With what? | V + C + A | Select means and implement them. |
| Verification | O | Did we build what was specified? |
| Validation | O + V | Did it actually produce the intended effect? |
| Roll out / deliver | A | Put the change into reality. |
| New What? | O' + F | New reality creates the next question. |

### Finding

This model introduces a useful distinction inside `Observe` / `Evaluate`:

**Verification** can be about conformance to an intended construction.

**Validation** can be about whether the resulting change is actually useful
in the real situation.

That distinction should probably survive.

---

# Test 6 — Conventional Problem Solving

A simplified problem-solving process:

```text
Identify problem
→ analyse causes
→ decompose
→ generate solutions
→ select solution
→ implement
→ check result
```

Maps to:

```text
Frame
→ Explore / Analysis
→ Explore / Analysis
→ Explore / Synthesis
→ Evaluate
→ Choose
→ Act
→ Observe
```

### Finding

Problem solving fits almost completely.

However, it tends to begin from a **problem frame**.

Our model must not require the situation to be framed as a problem.

---

# Test 7 — Opportunity / Cooperation / Samverkan

A simplified process:

```text
Observe situation
→ notice capabilities / needs / resources
→ connect complementary things
→ imagine a new configuration
→ evaluate
→ choose
→ act
→ observe result
```

Maps to:

```text
Observe
→ Frame
→ Explore / Synthesis
→ Imagine
→ Evaluate
→ Choose
→ Act
→ Observe again
```

### Finding

This is the strongest support so far for treating **Synthesis as a first-class
mode inside Explore**.

The central operation is not "solve a problem".

It is:

> find combinations that make a different configuration possible.

Matchmaking is naturally part of this operation.

---

# Test 8 — "I Don't Know" / Exploration

Example:

```text
"I don't know what I want to do."

→ review occupation cards
→ reject impossible / unattractive alternatives
→ retain four
→ compare them
→ explore available opportunities
→ choose a direction
```

Maps to:

```text
Frame
→ Explore
→ Explore / Analysis
→ Evaluate
→ Explore / Synthesis
→ Choose
```

### Finding

This is important.

**Imagine does not necessarily come first.**

The system can begin with an unresolved Intent and use Exploration to make
candidate futures visible.

Therefore:

> `Imagine` is an operation that may emerge from or be interleaved with
> `Explore`, rather than a mandatory stage before it.

This weakens the original linear ordering.

---

# Test 9 — Decision-only Transition

Example:

```text
"Stop using snus."
```

or:

```text
Municipal council decides to proceed.
```

There may be little or no operative sequence before the decisive transition.

Possible mapping:

```text
Frame
→ Evaluate
→ Choose
→ Transition
→ Observe
```

### Finding

**Choose and Transition are not necessarily separate events.**

A decision can itself be the smallest meaningful Transition.

This means the model must not assume:

```text
Choose → many actions → Transition
```

A more accurate relationship is:

```text
Choose
   │
   ├── may itself constitute a Transition
   │
   └── may initiate further Missions / Transitions
```

---

# Cross-Method Findings

## Finding 1 — The candidate operations are not a linear process

This is the most important result of the first test.

The initial sequence:

```text
Observe
→ Frame
→ Imagine
→ Explore
→ Evaluate
→ Choose
→ Act
→ Observe
```

is useful as an explanatory sequence, but it is **not a required workflow**.

The operations can occur in different orders and can recur.

For example:

```text
Explore
  → Imagine
  → Explore
  → Evaluate
  → Imagine
  → Explore
  → Choose
```

or:

```text
Observe
  → Frame
  → Choose
```

or:

```text
Observe
  → Synthesis
  → Imagine
  → Choose
```

The engine therefore should support **navigation among operations**, not
force a pipeline.

---

## Finding 2 — Explore is currently the largest candidate operation

Explore currently contains:

- analysis
- synthesis
- discovery
- matchmaking
- gap identification
- constraint identification
- alternative generation
- relationship discovery

This is probably too broad.

It may need to be decomposed later.

However, decomposing it too early could simply recreate the terminology
problem we are trying to avoid.

**Keep it provisional.**

---

## Finding 3 — Imagine may not be primitive

The "I don't know" example demonstrates that futures can emerge through
exploration.

Therefore:

```text
Explore → Imagine
```

may be just as valid as:

```text
Imagine → Explore
```

This suggests that `Imagine` may describe a kind of information/result
rather than a fundamental operation.

This needs further testing.

---

## Finding 4 — Choose may be a Transition

A decision can itself change the situation.

Therefore `Choose` may not always be an operation preceding Transition.

It may be one mechanism through which a Transition occurs.

---

## Finding 5 — Act may also be a mechanism rather than a fundamental operation

An action induces a Transition.

It is not yet clear whether:

```text
Act
```

should remain a generic operation or whether the more fundamental concept
is simply:

```text
Transition
```

with Missions, Decisions and other mechanisms inducing it.

This is an important information-model question.

---

## Finding 6 — Observe is more than measurement

Observation includes:

- discovering what happened
- receiving feedback
- verification
- validation
- noticing environmental change

These may eventually need distinctions, but they currently share a common
role:

> establish information about reality.

---

## Finding 7 — Analysis and Synthesis appear genuinely different

This distinction survived all tests.

### Analysis

```text
whole
 ↓
parts
 ↓
causes / constraints / dependencies / gaps
```

### Synthesis

```text
parts
 ↓
relationships / combinations
 ↓
new configuration / capability / possibility
```

Both operate on the same situation but produce different kinds of useful
information.

This is currently the strongest candidate for a meaningful distinction
within the generic reasoning language.

---

## Finding 8 — Methods are compositions of operations

The tests suggest:

```text
Method
  =
  particular ordering,
  grouping,
  emphasis,
  vocabulary
  and constraints
  applied to underlying operations.
```

This may be one of the key architectural insights of the project.

The engine does not need to implement "OODA" as a special domain type.

It may implement the underlying capabilities that allow an OODA-like
workflow to emerge.

---

# Revised Working Vocabulary

After the first test, I would provisionally retain:

### Strong candidates

- **Observe**
- **Frame**
- **Explore**
  - Analysis
  - Synthesis
- **Evaluate**
- **Choose**

### Weaker candidates

- **Imagine**
- **Act**

Both may turn out to be better understood as information/results or
mechanisms of Transition.

### Cross-cutting concepts

- Context
- Motivation
- Intent
- Transition
- Decision
- Observation
- Mission

These are not necessarily operations.

---

# Current Working Model

Rather than a pipeline, the model is beginning to look like a set of
operations available around a Transition:

```text
                         ┌───────────────┐
                         │    OBSERVE    │
                         └───────┬───────┘
                                 │
                         ┌───────▼───────┐
                         │     FRAME     │
                         └───────┬───────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
              ┌─────▼─────┐             ┌────▼────┐
              │  ANALYSIS │             │SYNTHESIS│
              └─────┬─────┘             └────┬─────┘
                    │                         │
                    └────────────┬────────────┘
                                 │
                         ┌───────▼───────┐
                         │    IMAGINE    │
                         │ / alternatives│
                         └───────┬───────┘
                                 │
                         ┌───────▼───────┐
                         │    EVALUATE   │
                         └───────┬───────┘
                                 │
                         ┌───────▼───────┐
                         │     CHOOSE    │
                         └───────┬───────┘
                                 │
                              TRANSITION
                                 │
                                 ▼
                              REALITY
                                 │
                                 ▼
                              OBSERVE
                                 │
                                 └────→ ...
```

This is **not yet a final model**. In particular, the arrows should not be
read as mandatory sequencing.

---

# The Most Important Result

The first test did **not** reveal that we need more named methodologies.

It revealed that the common substrate may be closer to:

> **information + context + intent + operations on that information +
> transitions + observation of consequences**

than to any particular management framework.

The next question is therefore becoming sharper:

> **What information must exist for these operations to be possible?**

That takes us directly back to the Generic Information Model.

Before changing it, however, we should test one more thing:

> **Can the current candidate information forms — Thing, Statement,
> Observation, Intention, Relationship, Context, Transition — actually
> support these operations without introducing method-specific types?**

That is the next useful stress test.
