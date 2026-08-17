# Transition, Mission and Definition of Done

## Status

Working concept — Phase 1/2

## Transition

A Transition represents meaningful change from one configuration to another.

```text
Identity N
    │
    │ Transition
    ▼
Identity N+1
```

It may affect one or several Identity building blocks and may affect multiple Identities.

A Transition is conceptual, not necessarily a sequence of actions. The smallest meaningful Transition may be a decision or commitment.

## Mission

A Mission / Task / Assignment is a concrete mechanism intended to induce a Transition.

Examples:

```text
Visit this address and talk to the business owner.

Interview five people under twenty.

Build a small working application.

Bring an artist and a café owner together.
```

A Mission may affect several Identities.

The external representation should remain simple even if the reasoning behind it is complex.

## Definition of Done

A Definition of Done (DoD) is a pre-agreed description of the conditions under which a Transition is considered complete.

It answers:

> How will we recognise that we have arrived?

A DoD may contain any combination of:

- desired outcome
- changed capability or Identity brick
- observable condition
- quantitative threshold
- qualitative acceptance condition
- time limit
- boundary condition
- acceptance authority
- evidence expectation

The exact combination should be proportional to the Transition.

## Completion is not success

DoD and Definition of Success should not be conflated.

Example:

```text
Transition:
Introduce three new festival activities.

Definition of Done:
- three activities implemented
- activities available during the festival
- organiser confirms operation
```

The transition can be done without proving that it produced the larger desired effect.

Success might instead be evaluated through visitor satisfaction, business participation, return intention, economic activity or other relevant observations.

> **Done describes completion of the Transition. Success describes whether the completed Transition produced the desired larger effect.**

## Evidence

The model deliberately does not prescribe how completion or success is verified.

Possible mechanisms include:

- GPS confirmation
- application records
- human confirmation
- participant confirmation
- micro-surveys
- assessment
- repeated observation
- other sensors or system mechanisms

These are engineering and implementation choices.

The conceptual requirement is that observations can be associated with the relevant transition and used to reassess the resulting state.

## Relationship

```text
CURRENT IDENTITY
       │
       ▼
  INTENTION /
DESIRED CHANGE
       │
       ▼
   TRANSITION
       │
       ├── Definition of Done
       │
       └── Mission(s)
               │
               ▼
          REAL-WORLD
            CHANGE
               │
               ▼
       OBSERVATION /
          FEEDBACK
               │
               ▼
       IDENTITY N+1
```

This is a semantic relationship, not a prescribed database structure.

## Open questions

- whether Definition of Done should eventually be represented explicitly in the information model
- how multiple acceptance conditions are combined
- how conflicting acceptance authorities are handled
- how evidence confidence is represented
- how success is assessed over longer periods
- how much of this should be visible to users

These are not Phase 1/2 blockers unless a concrete prototype requires them.
