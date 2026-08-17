# Case File Snapshots --- Genericity Test v0.1

## Purpose

This document tests whether the Case File can represent two very
different situations without forcing either situation into a
domain-specific structure.

The two cases are:

1.  An individual exploring a new occupational direction.
2.  Skördefesten / Södra Öland exploring increased youth participation.

The test is deliberately semantic.

It does not define the final API, database, UI, or information model.

The question is:

> **Can the same underlying Case File structure follow both situations
> through several iterations while allowing the user-facing
> representation to remain simple and domain-appropriate?**

------------------------------------------------------------------------

# 1. The Generic Pattern

Before looking at the examples, the common structure appears to be:

``` text
CONTEXT
   ↓
CURRENT SITUATION
   ↓
DESIRED DIRECTION
   ↓
POSSIBILITIES
   ↓
DECISION
   ↓
ACTION / MISSION
   ↓
REALITY
   ↓
OBSERVATION / EVIDENCE
   ↓
UPDATED SITUATION
   ↓
NEXT LOOP
```

The terms used above are intentionally generic.

They do not prescribe exactly how the Engine must reason.

------------------------------------------------------------------------

# 2. Case A --- Individual / Occupational Direction

## t0 --- Initial Case File

### Underlying Case File

``` text
Context
  Participant: individual
  Scope: personal
  Time: ongoing

Current Situation
  No clear occupational direction.

Desired Direction
  Not yet defined.

Vision
  Not yet defined.

Goals
  Not yet defined.

Transitions
  None.

Missions
  None.

Observations
  None.

Evidence
  None.

Uncertainties
  What does the participant actually want?
  What is realistic?
  What capabilities already exist?
```

### User-facing representation

The user does not need to see any of this terminology.

The App can simply show:

> **What are we working on right now?**

User:

> I don't know what I want to do.

------------------------------------------------------------------------

# 3. Case A --- t1

The Engine interprets the input and proposes exploration.

### Underlying Case File

``` text
Current Situation
  No clear occupational direction.

Interpretation
  The participant is uncertain about future work.

Possible Directions
  Explore occupations.

Proposed next action
  Review a set of occupation cards.

Decision
  Not yet made.
```

### User-facing representation

``` text
What could we explore?

[ Explore occupations ]

[ Something else ]
```

The user does not need to know that this is an Engine-generated
interpretation.

------------------------------------------------------------------------

# 4. Case A --- t2

The participant explores occupation cards.

Suppose 50 occupations were available and the participant reduces them
to four.

### Underlying Case File

``` text
Current Situation
  No single occupational direction selected.

Observation
  46 occupations rejected.
  4 remain interesting.

Possible Directions
  Occupation A
  Occupation B
  Occupation C
  Occupation D

New uncertainty
  Which direction is worth exploring further?
```

### User-facing representation

``` text
You've narrowed it down to four.

Which one would you like to explore?

[ A ]
[ B ]
[ C ]
[ D ]

[ Explore further ]
```

Again, the user is simply making choices.

The underlying model can retain much richer information.

------------------------------------------------------------------------

# 5. Case A --- t3

The participant selects software development.

### Underlying Case File

``` text
Current Situation
  Software development appears most interesting.

Desired Direction
  Determine whether software development is a
  realistic and worthwhile direction.

Possible Transition
  Test the occupation through a small real-world
  experience.

Decision
  ACCEPT
```

### User-facing representation

``` text
You seem interested in software development.

Want to try a small real-world test?

[ Yes ]
[ Change the idea ]
[ Explore further ]
```

The user never needs to encounter the word "Transition".

------------------------------------------------------------------------

# 6. Case A --- t4

The Engine creates a Mission.

### Underlying Case File

``` text
Mission

Purpose
  Test interest in software development.

Action
  Talk to one software developer.

Definition of Done
  - conversation completed
  - three questions asked
  - reflection recorded

Suggested Evidence
  participant observation
```

### User-facing representation

``` text
YOUR CHALLENGE

Talk to a software developer.

Ask:
  1. What do you actually do during a normal day?
  2. What was difficult when you started?
  3. What would you recommend to someone starting now?

When you're done, tell us what you learned.

[ Start challenge ]
```

The App translates the generic Mission into its own user-facing
representation.

------------------------------------------------------------------------

# 7. Case A --- t5

The participant completes the Mission.

### Underlying Case File

``` text
Mission
  Completed.

Observation
  "Software development seems interesting.
   It looks difficult, but I would like to try it."

Evidence
  Participant-recorded observation.

Updated Current Situation
  Interest has increased.
  Difficulty is perceived as a possible obstacle.

New Possibilities
  Try a small programming exercise.
  Learn what skills are required.
  Talk to another developer.
```

### User-facing representation

``` text
You did it.

What did you discover?

> Software development seems interesting.
> It looks difficult, but I would like to try it.

What next?

[ Try programming ]
[ Learn what skills are needed ]
[ Talk to another developer ]
[ I'm not sure ]
```

------------------------------------------------------------------------

# 8. Case A --- t6: GIVE UP

Suppose the participant says:

> This is too difficult. I give up.

### Underlying Case File

``` text
Decision
  GIVE_UP

Current Commitment
  Terminated.

Reassessment
  Required.

Possible interpretations
  - Goal no longer desirable.
  - Current approach is too difficult.
  - Scope is too large.
  - Participant needs another direction.
```

### User-facing representation

``` text
It's never too late to give up.

What do you mean?

[ I'm done with this ]
[ I still want the goal, but not this approach ]
[ I don't know anymore ]
[ Challenge me ]
```

If the participant chooses `CHALLENGE ME`, the Engine can propose a much
smaller step.

------------------------------------------------------------------------

# 9. Case B --- Skördefesten / Södra Öland

Now use the same underlying structure.

The content is completely different.

## t0 --- Initial Case File

``` text
Context
  Geographic scope: Södra Öland
  Time: defined festival period
  Participants: organisations / businesses / individuals

Current Situation
  Existing festival ecosystem.

Desired Direction
  Not yet defined.

Vision
  Make Södra Öland an even better place to live,
  work and visit.

Goals
  Not yet defined.

Transitions
  None.

Missions
  None.

Observations
  None.

Evidence
  Existing information / observations.
```

### User-facing representation

The Context might simply ask:

> **What would make Södra Öland an even better place to live, work and
> visit?**

A participant answers:

> We want more young people to become involved in the festival.

------------------------------------------------------------------------

# 10. Case B --- t1

### Underlying Case File

``` text
Current Situation
  Young people have limited involvement.

Desired Direction
  Increase meaningful youth participation.

Uncertainty
  Why is participation limited?

Possible Directions
  Ask young people.
  Examine existing activities.
  Connect existing local capabilities.
```

### User-facing representation

``` text
What could we explore?

[ Ask young people ]
[ Look at existing activities ]
[ Find something we could combine ]
[ Something else ]
```

The same generic mechanism is being used as in Case A.

------------------------------------------------------------------------

# 11. Case B --- t2

The participant chooses to look for combinations.

The Engine may identify:

``` text
Existing capabilities
  Café
  Artist
  Local association
  Bird guide
  Young participants
  Festival locations
```

### Underlying Case File

``` text
Possible Opportunity

Existing capabilities can potentially be combined
into a new youth-oriented activity.

Uncertainty
  No evidence yet that young people would value it.

Possible Transition
  Co-design and test one small activity with young people.
```

### User-facing representation

``` text
We found an idea worth testing.

Could we create something new by combining
people and activities that already exist here?

[ Let's explore ]
[ Change the idea ]
[ Not interested ]
```

------------------------------------------------------------------------

# 12. Case B --- t3

The participant modifies the proposal.

### Underlying Case File

``` text
Original Proposal
  Create a youth-oriented activity.

Participant Modification
  Young people should participate in designing it,
  not merely participate in the finished activity.

Updated Desired Direction
  Co-design and test one small activity.

Decision
  ACCEPT
```

### User-facing representation

``` text
Let's change the idea.

Young people shouldn't just be the audience.
They should help create it.

[ Accept ]
[ Change it again ]
[ Explore further ]
```

The App does not need to explain the underlying Transition object.

------------------------------------------------------------------------

# 13. Case B --- t4

### Underlying Case File

``` text
Mission

Purpose
  Co-design and test a small youth-oriented activity.

Definition of Done
  - young participants involved
  - activity defined
  - pilot completed
  - observations recorded

Suggested Evidence
  participant confirmation
  activity record
  survey / feedback
  optional GPS evidence
```

### User-facing representation

``` text
YOUR CHALLENGE

Get a small group of young people together
and create one festival activity with them.

When you've tested it, we'll look at what happened.

[ Start challenge ]
```

Again, this is almost identical to the individual case at the structural
level.

------------------------------------------------------------------------

# 14. Case B --- t5

Suppose the pilot is completed.

### Underlying Case File

``` text
Mission
  Completed.

Observation
  Young people were interested,
  but the proposed time was unsuitable.

Evidence
  Participant feedback
  Survey responses

Updated Current Situation
  Interest exists.
  Timing is an obstacle.

New Possibilities
  Change activity timing.
  Create a shorter activity.
  Try another audience.
```

### User-facing representation

``` text
The test is complete.

What did we learn?

Young people were interested,
but the timing didn't work.

What should we try next?

[ Change the time ]
[ Make it shorter ]
[ Try another idea ]
[ Explore further ]
```

The system has learned something that changes the Case File.

------------------------------------------------------------------------

# 15. Side-by-Side Comparison

The two cases are now very different in content.

  -----------------------------------------------------------------------
  Underlying element      Individual              Skördefesten
  ----------------------- ----------------------- -----------------------
  Context                 Personal                Geographic /
                                                  multi-actor

  Current situation       No occupational         Limited youth
                          direction               participation

  Desired direction       Explore software        Increase youth
                          development             participation

  Possibilities           Occupations / learning  Local capabilities /
                                                  activities

  Decision                Accept / modify / give  Accept / modify /
                          up                      explore

  Mission                 Talk to developer       Co-design activity

  Definition of Done      Conversation +          Pilot + observations
                          reflection              

  Evidence                Participant observation Feedback / survey / GPS
                                                  etc.

  Observation             Programming seems       Timing is an obstacle
                          interesting             

  Next loop               Try programming         Change timing
  -----------------------------------------------------------------------

The **content is radically different**.

The **structural pattern remains recognizable**.

This is the genericity we are looking for.

------------------------------------------------------------------------

# 16. What the User Sees

The underlying model may contain:

``` text
Situation
Intentions
Desired State
Transition
Opportunity
Obstacle
Decision
Mission
Definition of Done
Evidence
Observation
Reassessment
```

But the App can present:

``` text
What are we working on?
        ↓
What could we explore?
        ↓
Here's an idea
        ↓
What do you think?
        ↓
Your challenge
        ↓
What happened?
        ↓
What next?
```

This is deliberate.

> **The user should be able to use the system without learning the
> model.**

The App's current:

``` text
Vision
  ↓
Goals
  ↓
Missions / Challenges
```

is therefore treated as a **representation**, not as the underlying
ontology.

------------------------------------------------------------------------

# 17. What This Test Suggests

The two cases support the following working hypothesis:

> A generic Case File can represent radically different situations if it
> describes the evolving relationship between current situation, desired
> direction, decisions, actions, observations and resulting changes.

This is a hypothesis, not yet a proof.

------------------------------------------------------------------------

# 18. Important Discovery: The Structure Does Not Need to Be a Tree

The examples also expose a limitation of the existing App
representation.

The underlying Case File may contain relationships such as:

``` text
Goal
  ↔ obstacle
  ↔ opportunity
  ↔ participant
  ↔ capability
  ↔ mission
  ↔ observation
```

These relationships are not necessarily hierarchical.

The App can still present them as:

``` text
Vision
  ↓
Goal
  ↓
Challenge
```

because that may be easier for a human to understand.

Therefore:

> **The underlying Case File should not be constrained to the App's tree
> structure.**

The tree is a view.

The Case File is the underlying continuity structure.

------------------------------------------------------------------------

# 19. Another Important Discovery: Case Files Can Branch

A single Case File may generate several possible directions.

``` text
Current situation
       │
       ├── Direction A
       │
       ├── Direction B
       │
       └── Direction C
```

The participant may:

-   choose one
-   explore several
-   reject some
-   return to an earlier possibility
-   discover that two directions can be combined

The Case File should therefore be able to preserve alternatives without
treating every possibility as an active commitment.

------------------------------------------------------------------------

# 20. Another Important Discovery: The Case File Is Not a Plan

In both examples, the future was not known at the beginning.

The system learned through action.

``` text
Initial understanding
        ↓
small action
        ↓
new observation
        ↓
changed understanding
        ↓
new action
```

Therefore the Case File is better understood as:

> **a continuously updated representation of an evolving transition**

rather than:

> a plan describing everything that should happen.

------------------------------------------------------------------------

# 21. Genericity Test Result --- v0.1

### Result

**Promising.**

Both cases can be represented using the same underlying structural
vocabulary without introducing domain-specific Case File types.

### Still unproven

We have not yet tested:

-   multiple organisations with conflicting intentions
-   several simultaneous Goals
-   large geographic contexts
-   permissions and access
-   conflicting observations
-   multiple concurrent Missions
-   abandoned and resumed transitions
-   Cases where the desired direction changes completely
-   Cases where no useful transition can be found

These should be tested later rather than prematurely added to the
prototype.

------------------------------------------------------------------------

# 22. Next Step

The next logical step is to take these snapshots and turn them into the
**smallest possible mock Case File representation**.

Not a database.

Not a production schema.

Something that allows us to say:

``` text
load case
→ send event
→ update case
→ produce next proposal
→ record decision
→ execute mission
→ record observation
→ repeat
```

At that point we can finally begin testing the App ↔ Engine conversation
with something executable.

The prototype then becomes a test of both:

1.  the **Case File concept**, and
2.  the **App ↔ Engine language**.

If either one breaks, we revise the model before building more.
