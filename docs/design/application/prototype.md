# Application Prototype

## Status

**Prototype 0 — First Vertical Slice**

The prototype makes the semantic model real enough to expose missing concepts.
It does not define the final UI architecture or visual design.

## Scenario

Use the **18-year-old immigrant → software developer** case first.

Later test the same prototype with:

- football team
- Öland Harvest Festival
- district attractiveness
- multi-organisation cooperation

## Screen 1 — Situation

### Primary question

> **Where are you now?**

Example:

```text
You recently arrived in Sweden.

We currently understand that:
- you speak Arabic
- your Swedish is developing
- you have limited professional experience
- you are exploring what you want to do next
```

Controls:

```text
[That's right]
[Change something]
[Add something]
```

When useful, show provenance:

```text
You told us
Observed
Suggested
```

## Screen 2 — Direction

### Primary question

> **What would you like to change?**

Possible choices:

```text
I know what I want
I have some ideas
I don't know yet
```

If "I don't know yet", offer exploration rather than forcing an answer.

Occupation cards are one possible discovery mechanism.

## Screen 3 — Explore

### Primary question

> **What could move you forward?**

Possible sections:

```text
Possible directions
People and organisations
Opportunities
Constraints
What happens if nothing changes?
```

Example:

```text
Business Owner B
- speaks the same language
- runs a café
- wants to meet young people
- has local business connections
```

This is a suggestion, not a fact about what the user should do.

## Screen 4 — Choose

### Primary question

> **What seems worth pursuing?**

Show a small number of alternatives.

Example:

```text
A — Start formal education
B — Build skills through small projects
C — Meet local businesses and explore trainee opportunities
D — Continue as things are for now
```

For each, show relevant effects, requirements, benefits, constraints,
uncertainty, effort and cost where available.

The continuation alternative must be legitimate.

## Screen 5 — Transition

### Primary question

> **What is the next meaningful step?**

Example:

```text
Mission

Visit Business Owner B at the café.

Purpose:
Explore whether a trainee or project opportunity
could help you gain software-development experience.

Why this step:
- shared language
- relevant network
- low initial commitment
- may reveal additional opportunities
```

Controls:

```text
[Accept]
[Change]
[Choose another direction]
```

After completion:

```text
What happened?

Completed
Partly completed
Did not happen
Something unexpected happened
```

Return to Situation.

## Prototype loop

```text
Situation → Direction → Explore → Choose → Transition → Observe → Situation
```

## Success criteria

The prototype succeeds if a user can:

1. enter without lengthy onboarding
2. describe a situation naturally
3. remain uncertain without being blocked
4. discover candidate directions
5. see opportunities involving other Things
6. compare action against continuation
7. select one next step
8. understand why it is suggested
9. report what happened
10. see the situation evolve

## Explicit non-goals

The first prototype should not attempt to solve full account management,
enterprise administration, comprehensive AI generation, optimisation,
complete project management, complete social networking, final visual
design, or the final database schema.

The prototype is a semantic and experiential probe.
