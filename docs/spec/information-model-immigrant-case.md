# Information Model — End-to-End Case Test

## Case

An 18-year-old immigrant arrives in Sweden.

The person wants, or gradually discovers that they want, to become a
software developer.

The case is intentionally simplified but contains:

- an initially unclear Intent
- exploration
- candidate futures
- capabilities
- language
- relationships
- a business owner
- cooperation
- matchmaking
- Missions
- multiple Identities changing simultaneously
- observations
- feedback
- motivation
- a possible transition toward employment / software development

The purpose is not to design the application workflow.

The purpose is to see whether the Generic Information Model can represent
the meaning of the case.

---

# 1. Initial Situation

We begin with a Thing:

```text
Person A
```

Known information may include:

```text
age = 18
location = Sweden
recently arrived = true
speaks Language X
limited Swedish
limited professional network
no established software-development career
```

These are Statements and/or Observations in a Context.

We can derive a contextual projection:

```text
Current Identity A
```

but we do not need to store `Identity A` as a special universal type.

## Model test

```text
Thing
 ├── Statement
 ├── Statement
 ├── Observation
 └── Relationship
```

### Result

**Works.**

---

# 2. The Initial "I Don't Know" State

Suppose we ask:

> What do you want to do?

The answer is:

> I don't know.

This is important.

There is no useful specific Intention yet.

The system should not interpret this as an error.

Instead:

```text
Current Identity
       │
       ▼
insufficient / unresolved Intent
       │
       ▼
Exploration
```

The information model can represent the incomplete or absent Intention.

### Result

**Works.**

No `UnknownIntent` type is required.

---

# 3. Exploration Through Occupation Cards

The person is presented with a set of possible occupations.

For example:

```text
software developer
electrician
nurse
chef
mechanic
graphic designer
teacher
...
```

The person rejects occupations that are:

- uninteresting
- impossible
- clearly unsuitable

Four remain.

At this point the system has learned something meaningful.

It does not yet necessarily have a final Intention.

It has:

```text
Candidate A
Candidate B
Candidate C
Candidate D
```

with relationships to the Person and Statements expressing preferences or
rejections.

For example:

```text
Person A
  interested-in → software development

Person A
  rejected → occupation X

Person A
  considers → occupation Y
```

## Model test

The existing model can represent the Statements and Relationships.

### But:

We now have a concrete example of the missing concept identified in the
previous stress test:

> **Candidate future configuration**

A candidate occupation is not quite:

- a Thing in the ordinary sense
- an Intention
- a Transition
- an Observation

It is a **possible configuration / possibility being considered**.

### Result

**PARTIAL PASS — important gap discovered.**

We should not immediately create `CandidateFuture` as a primitive.

First determine whether a more general concept can represent:

> "a possible state/configuration that can be considered without being
> currently true or intended."

---

# 4. Emerging Intent

Suppose the person selects:

> I want to become a software developer.

Now an Intention exists.

Conceptually:

```text
Person A
    │
    └── Intention →
            become capable of working
            as a software developer
```

This does not mean the person currently *is* a software developer.

The Intention describes a desired future configuration.

## Model test

```text
Thing
   │
   └── Intention
```

works.

### Result

**PASS.**

But the selected Intention should remain connected to the candidate that
was previously explored.

That history may matter later.

---

# 5. Desired Identity

We now need to describe what "software developer" means in this context.

It might include relevant building blocks such as:

```text
programming capability
software-development knowledge
ability to work in a development environment
communication capability
professional network
work experience
portfolio / evidence of capability
```

The exact bricks are context-dependent.

We do not create:

```text
SoftwareDeveloperIdentity
```

Instead we describe a desired configuration through relevant Statements.

Conceptually:

```text
Desired Identity
    ├── capability → programming
    ├── capability → software development
    ├── relationship → professional network
    ├── evidence → completed work
    └── ...
```

### Result

**PASS — provisionally.**

The desired configuration is again exposing the need for a generic
representation of a configuration that does not yet exist.

---

# 6. Analysis

We now ask:

> What stands between the current situation and the desired situation?

Possible observations / statements include:

```text
limited Swedish
limited professional network
no Swedish work experience
limited knowledge of Swedish employment practices
limited software-development experience
uncertain educational pathway
```

This is Analysis.

We decompose the desired transition into relevant gaps and constraints.

The result is not necessarily a list of "problems".

It is information about the difference between configurations.

## Model test

Analysis operates over:

- Observations
- Statements
- Relationships
- Context
- Intention

### Result

**PASS.**

No `Problem` or `Gap` primitive is required.

---

# 7. Synthesis

Now we deliberately switch cognitive mode.

Instead of asking only:

> What is missing?

we ask:

> What already exists that can be combined to make progress possible?

We know:

```text
Person A
  speaks Language X

Business Owner B
  speaks Language X

Business Owner B
  wants to help young people

Business Owner B
  runs a café

Business Owner B
  wants more customers from the relevant community
```

There is now a potential combination:

```text
Person A
    +
Business Owner B
    +
shared language
    +
business owner's network
    +
software-development interest
    +
opportunity to meet people
```

This may produce a useful transition.

## Model test

The underlying information is represented through:

- Things
- Statements
- Relationships
- Context
- Intention

The **Opportunity** is an interpretation of the combination relative to
the desired Transition.

### Result

**PASS — conceptually.**

This is one of the strongest demonstrations so far that Opportunity does
not need to be a primitive type.

---

# 8. A Concrete Mission

We now select a small meaningful transition.

For example:

> Visit the café and talk to the business owner.

This is a Mission / Assignment.

The purpose is not simply to "complete a task".

It is to create an interaction that may change the situation.

The Mission may involve:

```text
Person A
Business Owner B
Place C
```

and have an intended effect:

```text
establish relationship
discover opportunity
learn about local businesses
possibly identify software-related contacts
```

## Model test

Mission can be treated as a mechanism associated with a Transition.

### Result

**PASS — provisionally.**

---

# 9. The Business Owner's Identity

The important point is that Business Owner B has an Identity of their own.

For example:

```text
Business Owner B
    ├── runs → Café
    ├── speaks → Language X
    ├── seeks → more customers
    ├── wants → help young people
    ├── can provide → local network
    └── seeks → people from community
```

The Mission therefore does not merely change Person A.

It may change both Identities.

This is a multi-actor Transition.

---

# 10. The Five-Person Brick

The business owner has a concrete objective:

> Interview five people under 20 in order to help build a network of
> skilled trainees.

This is interesting because the same activity may serve multiple
Intentions.

For Business Owner B:

```text
Desired change:
create a network of skilled trainees
```

For Person A:

```text
Desired change:
build professional network / gain experience
```

The same interaction may therefore contribute to different transitions.

## Model test

A shared Transition involving multiple Things can represent this.

### Result

**PASS.**

This reinforces the need for multi-actor Transitions and Relationships.

---

# 11. Observation

After the Mission:

```text
Person A visited café.
Conversation happened.
Business Owner B is interested.
Person A learned about three local companies.
One company may be looking for trainees.
```

These are Observations.

They should carry Context and eventually:

- time
- source
- confidence
- possibly provenance

The system does not simply replace the old situation.

It adds new information about what happened.

### Result

**PASS conceptually.**

Temporal and provenance semantics remain an open implementation-independent
information-model question.

---

# 12. New Opportunity

The conversation reveals:

```text
Company C
  seeks → junior trainee

Person A
  seeks → software-development experience
```

This creates another possible match.

The system may synthesise:

```text
Person A
    +
Company C
    +
available trainee opportunity
```

into a candidate Transition.

Again:

```text
Opportunity
```

is not necessarily stored as a primitive.

It is a **reasoned interpretation of relationships and information relative
to an Intention / Transition**.

---

# 13. Candidate Transition

Before anyone commits, we may have:

```text
Possible Transition:

Person A
    → meet Company C
    → explore trainee position
```

This is not yet an actual Transition.

It is a **candidate transition**.

This is the second major place where the model is under pressure.

We need to distinguish:

```text
possible
intended
selected
planned
actual
observed
```

without immediately turning every state into a separate type.

---

# 14. User Chooses

The user selects:

> Yes, let's pursue Company C.

This is a Decision.

It may itself change the situation:

```text
Intention becomes more specific.
A transition is selected.
A Mission can now be created.
```

Therefore:

```text
Choose
   │
   ├── may itself create a Transition
   │
   └── may authorize / initiate another Transition
```

### Result

**PASS conceptually.**

But this strengthens the need to distinguish **candidate** from **selected**
from **actual**.

---

# 15. Actual Transition

The person meets Company C.

Company C offers a trainee opportunity.

The person begins a small software project.

Now reality has changed.

The relevant Identity may have changed from:

```text
limited software experience
```

toward:

```text
some software-development experience
professional relationship
evidence of work
increased confidence
```

This is the transition:

```text
Identity N
    ↓
Transition
    ↓
Identity N+1
```

Again, Identity N+1 is a projection over new information.

It does not have to be a new hard-coded object type.

---

# 16. Verification

Suppose the intended transition was:

> Person A completes a small software project.

Verification asks:

> Was the project actually completed according to the agreed criteria?

Possible observations:

```text
project completed = true
required functionality = present
code delivered = true
```

This is primarily about conformance.

---

# 17. Validation

Validation asks:

> Did this actually move Person A toward the desired Identity?

Possible observations:

```text
Person A can now demonstrate software capability.
Person A has a professional reference.
Person A has a new relationship with Company C.
Person A is more motivated to continue.
```

This is not merely "did the task work?"

It asks:

> **Did the transition have the intended meaning in reality?**

---

# 18. New Identity

The information accumulated through the process now supports a new
Identity projection:

```text
Person A — Identity N+1

capability:
    basic software development

experience:
    completed project

relationship:
    Company C

network:
    several professional contacts

motivation:
    increased

Intent:
    continue toward software development
```

This becomes the basis for the next loop.

The system does not need to declare:

```text
Person A is now officially Identity N+1.
```

The new Identity is an interpretation of the current information.

---

# End-to-End Representation

The case can therefore be represented conceptually as:

```text
THING: Person A
       │
       ├── current Statements / Observations
       │
       ▼
CURRENT IDENTITY
       │
       ▼
UNRESOLVED INTENT
       │
       ▼
EXPLORATION
       │
       ├── candidate future A
       ├── candidate future B
       ├── candidate future C
       └── candidate future D
                    │
                    ▼
             USER SELECTION
                    │
                    ▼
                INTENTION
                    │
                    ▼
             DESIRED CONFIGURATION
                    │
             ┌──────┴──────┐
             │             │
         ANALYSIS       SYNTHESIS
             │             │
             │        Person + Café +
             │        shared language +
             │        network
             │             │
             └──────┬──────┘
                    ▼
           CANDIDATE TRANSITION
                    │
                 CHOOSE
                    │
                    ▼
                 MISSION
                    │
                    ▼
             ACTUAL TRANSITION
                    │
             ┌──────┴──────┐
             ▼             ▼
        VERIFICATION    VALIDATION
             │             │
             └──────┬──────┘
                    ▼
               OBSERVATION
                    │
                    ▼
             NEW IDENTITY
                    │
                    └────→ next loop
```

---

# What the Case Has Revealed

The model is surprisingly capable.

The major concepts that initially looked like types can continue to be
treated as interpretations:

```text
Identity       → projection
Vision         → desired configuration / Intent
Goal           → desired change / milestone
Opportunity    → enabling interpretation
Obstacle       → constraining interpretation
Mission        → mechanism for inducing Transition
Problem        → analytical framing
Solution       → candidate configuration / Transition
Decision       → choice that may itself cause Transition
```

This is exactly the direction we wanted.

---

# Three Things We Should NOT Do Yet

## 1. Do not create CandidateFuture just because we found the gap

We have discovered a real semantic requirement, but not yet the correct
primitive.

The question is:

> What is the most generic thing that can represent a possible but not
> actual configuration?

It may turn out to be a form of Statement, Context, Intention or
Transition.

## 2. Do not create separate types for planned / actual / observed Transition

We need to understand the semantics first.

The difference may be represented through status, temporal context,
provenance, relation or something more fundamental.

## 3. Do not turn Identity into a database object

The test continues to support Identity as a contextual projection.

---

# Current Conclusion

The immigrant case is a strong stress test.

The current information model can represent almost the entire process while
remaining generic.

The two most important unresolved questions are now:

### Q1 — What is a possible configuration?

We need to represent something that can be:

```text
considered
compared
evaluated
selected
rejected
```

without yet being:

```text
true
intended
actual
```

### Q2 — What is the semantic lifecycle of a Transition?

We need to distinguish, without prematurely creating types:

```text
possible
selected
planned
performed
observed
```

These two questions are now more important than adding further concepts.

The next information-model test should therefore focus specifically on
**Possibility / Configuration** and **Transition lifecycle**.
