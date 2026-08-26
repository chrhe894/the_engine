# Prototype Findings --- v0.1

## Purpose

This document records observations from running the v0.1 prototype
implementation against two test cases:

1. Complete Loop test (individual: "I want to become a software developer")
2. Skördefesten / Södra Öland golden case

It is a findings document, not a specification.

It does not propose solutions, new architecture, or redesigns.

------------------------------------------------------------------------

# 1. What the Prototype Successfully Demonstrated

## Observed behaviour

The following were exercised and produced expected results:

### Case File as continuity mechanism

- A Case File was created, updated through multiple phases, and saved
  to JSON.
- The same Case File survived: initial input, interpretation, goal
  creation, proposal, decision (MODIFY then ACCEPT), mission creation,
  mission completion, observation recording, situation update, and a
  subsequent proposal.
- A saved Case File was reloaded with all data intact (goals, missions,
  observations, decisions, history).

### The adaptive loop

The complete loop executed:

```
User input → Interpretation → Proposal → Decision → Mission →
Result/Observation → Case File Update → Next Proposal
```

This was demonstrated in both the individual case and the Skördefesten
case.

### Goal lifecycle independence

- Three goals were created within a single Case File.
- One goal was abandoned (GIVE UP).
- The remaining goals retained ACTIVE status.
- History, missions, and observations belonging to other goals were
  unaffected by the abandonment.
- The abandoned goal's reason was preserved in history.

### Decision vocabulary

All five decision types were exercised across the two tests:

- ACCEPT — created a mission from a proposal.
- MODIFY — altered a proposal before acceptance.
- REJECT — (exercised structurally; not in the Skördefesten run).
- EXPLORE FURTHER — (exercised structurally; not in the Skördefesten run).
- GIVE UP — triggered reassessment and goal abandonment.

### Continuity

The next proposal after a completed mission referenced the observation
text from that mission. This was verified programmatically in both tests.

### Genericity

The same code path handled both:

- an individual occupational exploration, and
- a multi-actor festival/geographic case.

No domain-specific branching was required.

------------------------------------------------------------------------

# 2. What Is Currently Simulated or Deliberately Simplistic

## Observed behaviour

The following are present in the prototype but operate as stubs or
simulations rather than meaningful implementations:

| Element | Current state |
|---------|--------------|
| Engine reasoning | Rule-based string templates. No actual interpretation of content. |
| Interpretation | Echoes user input back as "The participant describes: {text}". |
| Proposal generation | Fixed patterns: "Explore what X means" (first), "Build on what was discovered: Y" (subsequent). |
| Observation | Free-text string provided by the test script. No structure, confidence, or source distinction. |
| Evidence | Not exercised. The field exists but was not populated beyond type labels. |
| Definition of Done | A list of strings. No evaluation mechanism. |
| Mission completion | Set to COMPLETED by the test script. No verification against Definition of Done. |
| MODIFY flow | The test script manually replaced proposal fields. No Engine re-generation. |
| EXPLORE FURTHER | Returns the same proposal pattern again. No deeper exploration. |
| Challenge (micro-transition) | Produces a fixed "15 minutes" template. No reasoning about scope reduction. |
| Situation update | Manually composed by the test script, not derived by the Engine. |
| Geographic/time scope | Stored as context metadata. Not used in any reasoning. |
| Participant identity | Not represented. The Case File has no participant model. |
| Multiple participants | Not tested. Only one implicit participant per case. |

------------------------------------------------------------------------

# 3. Observations from the Complete Loop Test

## Observed behaviour

- The first proposal for a new goal is always the same structural
  pattern regardless of content: "Explore what X means concretely."
- After one mission with an observation, the second proposal quotes the
  observation verbatim and suggests "take one next step."
- Persistence round-trip (save → load) preserved all fields correctly
  including nested dataclass objects.

## Interpretation

- The continuity mechanism works at the data level: information flows
  from observation into the next proposal.
- The continuity mechanism does not yet work at the semantic level: the
  Engine does not reason about what the observation means or what would
  logically follow from it.

## Open questions

- What constitutes "meaningful continuity" beyond data availability?
  The current test verifies that the observation text appears in the
  next proposal. Is that sufficient, or must the Engine demonstrate
  that it has changed its reasoning based on the observation?
- Should the Engine distinguish between observations that confirm a
  direction and observations that challenge it?

------------------------------------------------------------------------

# 4. Observations from the Skördefesten / Södra Öland Test

## Observed behaviour

- The opening question ("What would make Södra Öland an even better
  place to live, work and visit?") was stored as context but not used
  by the Engine in any reasoning.
- The geographic scope ("Södra Öland") and time scope ("2026-09 to
  2026-10") were stored but not referenced in proposals.
- The Engine's first proposal was generic: "Explore what 'Increase
  meaningful youth participation in the festival' means concretely."
- The participant's MODIFY decision transformed a generic exploration
  into a specific co-design mission. This transformation was performed
  entirely by the participant (test script), not by the Engine.
- After the mission result, the Engine's next proposal quoted the full
  observation text (80+ words) rather than extracting a relevant
  insight from it.
- The GIVE UP → reassessment flow produced the four standard options.
  The participant selected "I'm done" and the goal was abandoned
  cleanly.

## Interpretation

- The Engine currently adds no domain-relevant intelligence. The
  meaningful content in the Skördefesten case came from the participant
  (MODIFY, observation text, situation description), not from the
  Engine.
- The MODIFY decision was the point where the generic prototype became
  domain-useful. This suggests that MODIFY may be a particularly
  important interaction for the first real version.
- The Engine's habit of quoting entire observations verbatim does not
  scale. With multiple missions and observations, proposals would
  become unreadably long.

## Open questions

- How should the Engine use geographic and time context in proposals?
- When the Engine quotes an observation, should it select or summarise
  rather than reproduce the full text?
- How should the Engine handle a MODIFY? Should it re-generate the
  proposal using the modification as new input, or is manual override
  sufficient?
- The Skördefesten case involves multiple actors (young people, café
  owners, artists, associations). The current prototype has no
  representation of these. At what point does that absence become a
  limitation?

------------------------------------------------------------------------

# 5. Multiple Goals / GIVE UP Behaviour

## Observed behaviour

- Three goals were added to a single Case File: youth participation,
  business cooperation, evening transport.
- GIVE UP on the transport goal triggered the reassessment flow.
- After abandonment, the transport goal retained status ABANDONED with
  a recorded reason.
- The youth goal's mission, observation, and history were unchanged.
- The business goal could still receive proposals from the Engine.
- The history log recorded the abandonment event with timestamp.
- `case.active_goals()` correctly returned only the two remaining
  active goals.

## Interpretation

- Goal independence works as designed at the data level.
- The current implementation has no mechanism for goals to interact
  (dependencies, conflicts, shared missions). This was not tested
  because it is explicitly out of scope for v0.1.

## Open questions

- When a goal is abandoned, should its observations remain available
  for reasoning about other goals? (Currently they do remain in the
  Case File, but the Engine does not cross-reference between goals.)
- Should the Engine notice when two goals might share a mission or
  observation?

------------------------------------------------------------------------

# 6. Continuity and Persistence Findings

## Observed behaviour

- Case File serialisation to JSON and deserialisation back to Python
  objects worked correctly.
- All nested structures (goals, missions, observations, decisions)
  survived the round-trip.
- The chronological history log captured 12 events for the Skördefesten
  case (goal additions, mission creation, completion, observations,
  decisions, situation updates, abandonment).
- UUIDs (truncated to 8 characters) provided stable identifiers across
  save/load.

## Interpretation

- JSON persistence is adequate for the current prototype scope.
- The history log provides an audit trail but is not yet used by the
  Engine for reasoning.
- The `updated` timestamp tracks when the Case File last changed but
  does not distinguish which field changed.

## Open questions

- Is the current flat history list sufficient, or will the Engine need
  structured access to "what happened to Goal X" without scanning the
  entire log?
- Should the Case File distinguish between "current state" and
  "historical state" more explicitly than it currently does?

------------------------------------------------------------------------

# 7. Limitations of the Current Rule-Based Engine

## Observed behaviour

The Engine produces proposals using three fixed patterns:

1. **No prior missions**: "Explore what X means concretely."
2. **Prior missions with observation**: "Build on what was discovered: Y"
3. **Prior missions without observation**: "Continue exploring: X"

The Engine does not:

- interpret the content of user input beyond storing it;
- distinguish between different types of observations;
- use geographic or time context;
- reason about relationships between goals;
- generate domain-appropriate mission descriptions;
- evaluate whether a Definition of Done has been met;
- reduce scope when a transition appears too large;
- identify opportunities or obstacles;
- perform matchmaking between capabilities and needs.

## Interpretation

- The Engine stub is sufficient to prove the loop works mechanically.
- It is not sufficient to test whether the Engine can produce useful
  proposals — that test has been deferred.
- The meaningful proposals in the Skördefesten case came from the
  participant's MODIFY decisions, not from the Engine.

## Open questions

- What is the minimum intelligence required for the Engine to produce
  a proposal that a participant would not need to MODIFY into something
  useful?
- Should the Engine's first response to new input be a question rather
  than a proposal? The current pattern always proposes; the contract
  document suggests that questions and suggestions should precede
  transition proposals.
- The contract document defines a message sequence:
  Interpretation → Question/Suggestion → Selection → TransitionProposal.
  The current prototype collapses this into a single Proposal. Is that
  collapse acceptable for testing, or does it hide an important
  interaction pattern?

------------------------------------------------------------------------

# 8. Questions and Discoveries

These emerged from the tests. They are recorded, not resolved.

### From the implementation

1. The Case File `current_situation` field is a single string. Multiple
   updates concatenate. This will become unmanageable after several
   loops. How should accumulated situation knowledge be structured?

2. The Engine currently receives the entire Case File. For a case with
   many goals and missions, this raises the question: what context does
   the Engine actually need for a single proposal?

3. Observations are free-text strings. The model describes observations
   as potentially having subject, aspect, value, time, source, context,
   and confidence. Should the prototype evolve toward structured
   observations, or is free text sufficient for the current gate?

4. The MODIFY flow currently requires the participant to provide the
   complete replacement. An alternative is that the participant provides
   a constraint or correction and the Engine regenerates. This was not
   tested.

### From the Skördefesten case

5. The participant in the test was "the festival organisation." The
   prototype has no participant model. When multiple participants enter
   the same Case File, how are their respective inputs and decisions
   attributed?

6. The co-design mission implicitly involved "young people" as actors.
   The prototype cannot represent these actors or their relationship to
   the mission. At what complexity level does this become a limitation?

7. The observation "evening timing worked well" is potentially relevant
   to the (now abandoned) transport goal. The prototype has no mechanism
   for cross-goal observation relevance.

### From the goal independence test

8. An abandoned goal retains its observations and history. The test
   verified this data persists. It did not test whether the Engine (or
   a future Engine) could usefully access that retained knowledge for
   other goals.

9. The reassessment flow offers four options but does not adapt those
   options to the specific goal context. Is contextual reassessment
   important, or are generic options sufficient?

### From the continuity test

10. Continuity was verified by checking whether the observation text
    appeared in the next proposal. This is a mechanical check. Semantic
    continuity — the Engine demonstrating changed reasoning — has not
    been tested and cannot be tested with the current stub.

------------------------------------------------------------------------

# 9. Summary

The v0.1 prototype demonstrates that:

- the adaptive loop can execute mechanically;
- the Case File can carry continuity across the loop;
- multiple goals can coexist with independent lifecycles;
- GIVE UP is locally scoped and does not invalidate other goals;
- the same code path handles different domains without branching;
- JSON persistence works for the current data structures.

The v0.1 prototype does not demonstrate that:

- the Engine can produce useful proposals without participant override;
- semantic continuity (changed reasoning) exists beyond data availability;
- the model handles multiple participants, actors, or organisations;
- geographic and time context influence reasoning;
- observations have structure beyond free text;
- the interaction pattern (interpretation → question → suggestion →
  proposal) from the contract document is necessary or sufficient;
- the Case File representation scales beyond a small number of loops.

These are not failures. They are the expected boundary of a first
prototype whose purpose is to make the loop executable and observable.

------------------------------------------------------------------------

# 10. Classification

Following the project's classification vocabulary:

| Finding | Classification |
|---------|---------------|
| Engine proposals are generic | ENGINE REASONING |
| Situation field concatenates without structure | ENGINEERING PROBLEM |
| No participant model | MODEL question |
| No cross-goal observation relevance | MODEL question |
| MODIFY requires full replacement | APP ↔ ENGINE CONTRACT |
| Geographic/time context unused | ENGINE REASONING |
| Interaction sequence collapsed | APP ↔ ENGINE CONTRACT |
| Observation lacks structure | MODEL question |

------------------------------------------------------------------------

This document records the state after the first prototype run.

It should be updated when subsequent tests reveal new findings.
