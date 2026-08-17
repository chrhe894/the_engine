# Context Opening --- Working Specification v0.1

## Purpose

The Engine can start with an **opened context**: a defined situation in
which people and organisations may participate in a common adaptive
loop.

A context may be a garden, neighbourhood, Södra Öland, Linköping
municipality, a festival, a project, or an individual situation.

A context may have a **time scope** and a **geographic scope**.

## Context

A working context may contain:

-   `id`
-   time scope
-   geographic scope
-   opening question
-   participation/access
-   opener/owner
-   description

Geographic scope may be a point, polygon, municipality/city, country, or
another meaningful boundary.

Time scope may be a point, period, or ongoing context.

The opening question is configurable. The default may be:

> What are we working on right now?

Examples:

> What would make Södra Öland an even better place to live, work and
> visit?

> What should we improve in this neighbourhood?

> What are we working on to make this year's festival the best yet?

## Participation

A context may contain individuals, organisations, groups, public bodies,
businesses and associations.

A participant may participate in several contexts simultaneously.

An organisation may therefore have different relevant identities,
intentions, capabilities and relationships in different contexts.

## Principle

The context is a **container for a situation**, not a new
domain-specific model type.

The Engine should operate on new contexts without requiring a new
application model for every domain.

## Relationship to the App

The App already has mechanisms for context, time, geographic position
and user interaction. The prototype should reuse those mechanisms where
practical.

The Engine should receive enough contextual information to reason about
the situation, while the App remains responsible for immediate user
interaction and local capabilities.

## Open Questions

-   Exact geographic representation.
-   Exact time representation.
-   Access-control model.
-   Persistent vs temporary contexts.
-   Whether contexts may contain other contexts.
-   How context ownership is represented.
