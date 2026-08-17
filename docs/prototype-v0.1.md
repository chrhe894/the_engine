# Prototype v0.1 --- Working Specification

## Purpose

The prototype tests the smallest complete adaptive loop against reality.

It is not intended to implement the whole Engine.

The test is:

> Can a participant enter with an unclear or desired change, receive
> editable suggestions, select a transition, commit to it, receive a
> concrete Mission, execute it through the existing App, return with an
> observation, and receive an appropriate next step?

## First Interaction

The user should not need to understand the Engine's concepts.

The first interaction is:

> **What are we working on right now?**

The question can be supplied by the current Context.

## Minimal User Flow

``` text
Open Context
    ↓
"What are we working on right now?"
    ↓
User input
    ↓
Engine interpretation
    ↓
Suggestions / questions
    ↓
User choice
    ↓
Transition proposal
    ↓
Commitment / decision
    ↓
Mission
    ↓
Existing App executes Mission
    ↓
Evidence / observation
    ↓
Engine interpretation
    ↓
Next step
```

## No Heavy Onboarding

Do not require a long classification process.

The system should learn context progressively from the actual situation.

Initial input may be completely open:

> I want to become a software developer.

> We want more visitors to Skördefesten.

> We need to make our neighbourhood more attractive.

> I don't know what I want to do.

## Interpretation

The Engine may produce a provisional interpretation:

``` text
I think we're working on:

Desired future:
    Become a software developer

Possible things to explore:
    What does "software developer" mean for you?
    What do you already know?
    What could you try?
    Who could help?
    What might stand in the way?
```

The participant can accept, change or reject the interpretation.

## Suggestions

The Engine may suggest questions, opportunities, obstacles, directions,
or transitions.

Suggestions remain suggestions until selected.

## Commitment

The prototype may experiment with:

### Explore

> Let's see what happens.

### Commit

> I'm willing to take a concrete step.

### Dare

> Give me a real transition. I'll stay with it until the Definition of
> Done is reached.

Commitment is voluntary.

## Decision Actions

``` text
ACCEPT
MODIFY
REJECT
EXPLORE FURTHER
GIVE UP
```

### GIVE UP

`GIVE UP` signals disengagement from the current transition and starts a
Reassessment.

Possible reassessment:

``` text
I'm done.
The goal is still worth it, but this approach isn't.
I don't know anymore.
Challenge me.
```

If the participant chooses `Challenge me`, the Engine may reduce the
current scope to a deliberately small challenge.

The Engine must also accept genuine termination.

> **It's never too late to give up.**

## Mission

A selected Transition becomes an executable Mission.

Example:

``` text
Mission:
    Talk to a software developer.

Purpose:
    Explore the profession.

Definition of Done:
    - conversation completed
    - three questions asked
    - reflection recorded
```

The existing App should execute the Mission where possible.

## Existing App as Vehicle

``` text
                ENGINE
                  │
          creates/recommends
                  │
                  ▼
               MISSION
                  │
                  ▼
                 APP
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
       GPS      Tasks     Surveys
        │         │         │
        └─────────┼─────────┘
                  ▼
          Evidence / Result
                  │
                  ▼
                ENGINE
```

The Mission must have a representation understood by both sides. The App
does not need to understand the reasoning that produced it.

## Prototype Definition of Done

> A user can enter an arbitrary change they want to work on, receive
> editable suggestions, select a transition, commit to it, receive a
> concrete Mission, complete or fail the Mission, record an Observation,
> and receive an appropriate next step --- without the prototype
> requiring the case to belong to a predefined domain.

If the prototype requires domain-specific branches such as:

``` text
if immigrant:
    ...
elif skordefest:
    ...
```

the genericity test has failed.

## Golden Cases

### Immigrant

Starting point:

> I don't know what I want to do.

Possible exploration:

-   occupation cards
-   reject impossible/uninteresting occupations
-   retain a small set
-   explore remaining directions
-   select a transition
-   perform a small Mission
-   observe what was learned
-   continue

### Skördefesten

Starting point:

> Make the festival more attractive / create more value.

Possible areas:

-   visitor experience
-   business cooperation
-   new audiences
-   activities
-   transport
-   evening experiences

The Engine may discover opportunities by combining capabilities and
intentions.

Example:

``` text
café
  +
artist
  +
bird guide
  +
visitor interest
  ↓
new pilot experience
```

The same transition machinery must work despite the different domain and
scale.

## Context Test

The prototype should run inside an opened geographical/time context.

Example:

``` text
Context:
    Södra Öland

Time:
    defined period

Geography:
    defined area

Opening question:
    What would make Södra Öland an even better
    place to live, work and visit?
```

The same mechanism could later be used for Linköping, a municipality, a
festival, a neighbourhood, a project, or an individual.

## Prototype Scope

Do not implement yet:

-   complete identity management
-   complex KPI management
-   sophisticated matchmaking
-   autonomous AI agents
-   complete evidence architecture
-   advanced analytics
-   every possible mission type
-   complete organisational administration

Only prove:

``` text
START
  ↓
UNDERSTAND
  ↓
CHOOSE
  ↓
COMMIT
  ↓
MISSION
  ↓
OBSERVE
  ↓
ADAPT
```

## Design Principle

> The prototype is itself a transition.

``` text
Model v0.1
    ↓
Prototype
    ↓
Observation
    ↓
Model v0.2
```

We are not trying to predict the final product before building the first
useful experiment.
