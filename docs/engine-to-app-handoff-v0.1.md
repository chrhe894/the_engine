# Engine → App Handoff (Human-Sensor App) — Observation v0.1

## Status
**Observation / open question.** Discovered during prototype use. Not a spec yet.

## What we observed
While planning a goal in the Engine (example: a route-based challenge), the
Engine produced excellent, concrete next steps: sketch the route, write the
first clues, build difficulty levels, make a route draft.

These are not the end product. They are **planning**. At some point the
planned thing must leave the Engine and **drop into the App as an executable
challenge** — a route with places, clues, and GPS-verifiable steps.

## The insight
> The Engine reasons and plans. The App executes and senses reality.
> The human, using the App, becomes the sensor that closes the loop.

```text
ENGINE                         APP  (human sensor)
  reasons / plans                executes in reality
  proposes goals + missions      GPS, places, clues, cards, surveys
  produces a spec        ─────►  turns spec into a runnable challenge
                                       │
                                 human does it (walks route, answers)
                                       │
  updates Case File      ◄─────  observations / evidence (GPS-verified)
  proposes next step
```

## The handoff artifact (open)
At some point a mission becomes structured enough to hand over. Rough shape:

- what kind of App experience (route, single place, survey, ...)
- the concrete content (places, clues, questions, difficulty)
- how completion is verified (GPS, confirmation, survey response)
- what observation/evidence should flow back to the Case File

This is the App↔Engine contract meeting reality — the thing the docs said
we should discover, not freeze in advance.

## Open questions
1. When does a mission stop being "planning" and become an App-ready spec?
2. Who authors the concrete content — Engine, participant, or both?
3. What is the minimum handoff structure for a GPS route challenge?
4. How does GPS-verified evidence come back and update the Case File?
5. Is "route challenge" one App experience type among several, or the first
   of a family (route, place, survey, card, ...)?

## Not decided
- The handoff format (JSON or other).
- Whether the Engine or the App owns the route content.
- The evidence/verification model.

This is captured so it is not lost. Next step is thinking and specing,
not coding.

## Later note: two uses of the same engine
Discovered but deliberately deferred: the same Engine serves at least two
modes.
1. **Personal navigation** — a user drives their own change (what we build now).
2. **Admin / curator** — someone plans finished challenges that other users
   can "take on" when bored.

Same engine, different participant and different destination for the output.
Not to be solved now. Building and testing the engine comes first.

## Later note: three GPS geometry types
The App's spatial verification appears to need three geometry types:

1. **Place** — a point with a radius (e.g. 0–10 m). "Are you here?"
2. **Route** — an ordered/sequential collection of places. "Have you walked this?"
3. **Area** — a polygon / geographic region (municipality borders, districts).
   "Are you within this area?"

The hard, interesting nut: the **general information model** for passing this
back and forth — a shared language between the Engine and TheApp. The Engine
should describe intent generically; TheApp translates it into these concrete
geometries and verifies against real GPS.

Open: how generic must the Engine stay, and how much geometry vocabulary must
cross the boundary? To be designed later.
