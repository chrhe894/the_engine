# Challenge-Authoring Top-Layer (IOOIS) — Draft Proposal v0.1

> **Status:** DRAFT — captured from a reasoning session. Not yet agreed,
> not yet a build spec. This is a thinking artifact to resume from.
>
> **Scope discipline:** The information model stays **intact**. Everything
> here lives in the *interpretation / top-layer* on top of the existing
> seven primitives. Several downstream questions are deliberately **parked**
> (see §9).

---

## 1. What we are trying to do

Use `the_engine` as a **tool for authoring location-based challenges**, and
prove it with a first concrete case. A challenge is:

- built in an **area** (e.g. Södra Öland, Linköping, Chiang Mai),
- made of **routes** (walking / biking / car / tuk-tuk …),
- where each route is an ordered **sequence of places**,
- a **place** is typically a GPS point with a ~10–20 m radius,
- oriented around **themes** (birds, history, museums, beer tour, temples,
  street food … anything).

The engine already presents *goals* you can enter to get *sub-proposals*,
and the goals persist so you can switch between them. We want to put a
**setup layer** in front of that loop (who's authoring, what "done" means)
and make the loop's output a **structured, refinable artifact** (places and
routes) rather than free-text missions — ending in a **tree** to hand to
`the_app` (that handoff is parked).

This is called the **top-layer**: one of potentially many framings over the
same untouched model. We build **one concrete vertical slice first**
(challenge authoring), and only later consider extracting a general
"top-layer profile" mechanism (generic loop / ABCD org / immigrant case as
instances). Option B first, then A.

---

## 2. The IOOIS lens

`IOOIS = Identity, Obstacles, Opportunities, Ideal State.`

The key grammar (the user's framing, which reconciled cleanly with the model):

| Layer | Question | Holds |
|---|---|---|
| **Identity** | What? Why? | The maker's current stance: what they intend, why it matters |
| **Ideal State** | What? Why? — *fulfilled* | The improved Identity. Where we **evaluate / validate** |
| **Opportunities** | enables *How? / With what?* | Suggestions / affordances for means |
| **Obstacles** | constrains *How? / With what?* | Restrictions on means |
| *(everything between Identity and Ideal State)* | **How? With what?** | The transition — proposals, missions, the assembled content |

Two disciplines that make it land:

1. **How? / With what? does NOT live in Identity.** It lives in the
   transition, *shaped by* Obstacles and Opportunities. (Travel mode, assets,
   constraints therefore split out of Identity into O/O.)
2. **Identity and Ideal State are the same shape** (both answer What/Why).
   Ideal State is the Identity with its intents fulfilled — this is the
   model's `Identity₀ → Identity₁`, not "current → ideal." It gives a natural
   validation check: *does the result actually realize the What/Why?*

---

## 3. How IOOIS maps onto the existing model (nothing new invented)

The model (`docs/spec/information-model.md`, `primitive-concepts.md`) has
**seven primitives**: Thing, Statement, Observation, Intention,
Relationship, Context, Transition. Everything else — Identity, Ideal State,
Opportunity, Obstacle, Goal, Mission, Vision — is explicitly a
**higher-level interpretation / projection**, *not* a stored type.

So IOOIS is exactly the kind of lens the model is designed to carry:

| IOOIS element | Model's own term |
|---|---|
| Identity | "context-dependent configuration of relevant information about a Thing" (Bricks) |
| Ideal State | "Desired Identity" (`Vision/Ideal State → Desired Identity → desired changes → Transitions → Missions`) |
| Opportunities | "potentially beneficial possibility for transition" |
| Obstacles | "restrict or complicate possible Transitions" |
| *the "in-between"* | **Transition**, induced by **Missions** |

The challenge domain maps onto primitives directly:

- **Thing** = the challenge-maker; and later each **place**, **route**, **area**.
- **Statement** = Identity Bricks ("intends walking challenges", "interested in birds").
- **Intention** = the Ideal State / Desired Identity.
- **Relationship** = "route contains places", "place located-at GPS point".
- **Observation** = discovered obstacles/opportunities and feedback.
- **Transition / Mission** = the goals→missions loop assembling the challenge.

IOOIS = the adaptive loop, renamed with What/Why vs How/With-what discipline.

The model spec's "generic before domain-specific" rule is respected: our
form is **not a new primitive**. It is a *template for producing Statements*
about a Thing. "themes: birds" just becomes `maker → interested-in → birds`.

---

## 4. "Same formula, different ingredients"

Three layers, only the middle is the reusable artifact:

1. **Formula (shape)** — invariant: "someone intends to create a
   location-based challenge in an area, made of routes built from places,
   around themes, for an audience, by some travel mode." Never changes.
2. **Form (fields)** — the reusable questionnaire. Same fields every time.
3. **Ingredients (values)** — vary per case.

Worked examples (same slots, different fills):

| Field | Södra Öland | Linköping | Chiang Mai |
|---|---|---|---|
| area | Södra Öland | Linköping | Chiang Mai |
| themes | birds, history | museums, beer tour | temples, street food |
| travel_mode | walking | walking | tuk-tuk |

**Reusability test:** no field is bird- or Öland-specific. Birds live in
`themes`; Öland lives in `area`. Test passes.

This is the seed of the eventual "top-layer profile" idea — discovered from
the concrete case rather than designed abstractly.

---

## 5. The challenge-maker Identity form (first sketch)

Organized by IOOIS. **Values are free text / lists; the *fields* are fixed.**

**Identity (What/Why — the maker's stance)**
- `area` — where.
- `themes` — what it's about. (The big ingredient slot. Flat list of strings
  for now; free-text notes may ride along. Open: keep flat vs. structured.)
- `purpose` — why / intended experience.
- `audience` — who it's for (aspiration; the *constraint* it imposes is an Obstacle).

**Ideal State (What/Why fulfilled — validation target)**
- `challenge_shape` — target properties: rough count of places, count of
  routes, rough duration/length, difficulty.
- **completeness criteria** — what each item must have to count as "done"
  (e.g. place needs {name, gps, description}; image required: yes/no). This
  drives the "are we done?" check. Making it a *field* keeps images etc.
  optional without deciding now.

**Opportunities (enables How/With-what)**
- `travel_modes` — walking / biking / car / tuk-tuk …
- `assets` — what the maker already has (photos, GPS tracks, contacts, sources).
- *(engine may add more as the loop runs)*

**Obstacles (constrains How/With-what)**
- `constraints` — no car, avoid private land, seasonal, accessibility,
  budget, ≤3 km for kids …
- *(engine may add more as the loop runs)*

**Minimum to start (rest optional / can emerge):** `area` + `themes` +
`travel_mode`. Consistent with the model's "path not known in advance" and
"intent can emerge."

**Obstacles/Opportunities are living, not static:** the setup *seeds* them;
the loop *discovers more* (each Observation can surface a new O/O or revise
the Ideal State). Matches the model's feedback loop.

---

## 6. The way of working (target walkthrough)

The user's walkthrough, which the design must support:

1. web.py reads the Identity/Ideal-State setup → seeds goals. Infers target
   counts from `challenge_shape` (e.g. ~50 candidate places, ~10 routes).
2. **Places goal:** engine proposes candidate places; maker approves /
   verifies / removes / suggests others. Per-item control.
3. **Routes goal** (after places): engine proposes routes (ordered sequences
   of approved places); maker rejects / edits / approves; asks for more.
   Goals persist and are switchable (existing tree behaviour).
4. **"Are we done?"** — validated against the Ideal State's completeness
   criteria (descriptions, GPS present, counts met). If not, keep proposing
   transitions that close the gap ("refine until Ideal State reached").
5. Out comes a **tree** of places/routes to export to `the_app` (parked).

---

## 7. What's already there vs. the one real gap

Most of the walkthrough is the **existing loop** with different content:

- Seeding goals from setup ≈ existing `confirm_name` goal creation.
- suggest → select → decide (ACCEPT / MODIFY / REJECT / EXPLORE / GIVE_UP) already exists.
- Goals persist + switch = existing tree view.
- Feedback/observations already feed the next proposal via `_build_context_message`.
- All reasoning is LLM in `engine_ai.py` (model `gpt-5.6-luna`) with a
  rule-based fallback in `engine.py`.

**The one real gap — items vs. missions.** Today a decision produces *one
Mission* (a described action). The walkthrough needs the loop's output to be
**content items that accumulate into a structured, refinable set**: place-
and route-objects with fields, refined over passes until they meet the Ideal
State.

At the **model** level this is not new: places/routes are **Things**, "route
contains place" is a **Relationship**, "place has GPS X" is a
**Statement/Observation**, "needs a description" is the gap between current
and Desired Identity. At the **code** level the current `CaseFile` has no
home for "a set of domain items under construction." That's the additive
work.

---

## 8. Decisions taken this session

- **D-A. Identity = the maker, not the half-built challenge.** area / routes /
  places live in Ideal State + result, not in Identity. Keeps the loop a real
  navigation, not a form-filler, and makes the maker Identity reusable across
  many challenges.
- **D-B. How?/With-what? restrictions & suggestions live in Obstacles /
  Opportunities**, not Identity.
- **D-C. Themes / audience-aspiration = Identity (What/Why); travel mode /
  assets = Opportunities; prohibitions / limits = Obstacles.** Audience
  splits: aspiration → Identity; the constraint it imposes → Obstacle.
- **D-D. Build a reusable challenge-authoring form** ("same formula, different
  ingredients"); Öland / Linköping / Chiang Mai are instances.
- **D-E. Heavier target, thin first slice.** Places/routes are **first-class,
  per-item refinable** items (heavier). But build a **thin slice first**:
  *places only*, minimal fields {name, gps, description}, with a completeness
  check — before adding routes and refinement.
- **D-F. Model stays intact.** No new primitive. Interpretation-layer form +
  sharper prompt/context "hints" so the LLM reasons in model vocabulary
  (Identity/Intention/Obstacle/Opportunity/Transition/Mission).
- **D-G. Images & multi-user participation are solved in `the_app`, not the
  engine.** The "who uploads the first image?" problem becomes an
  **Opportunity**: the first participant at a place in the_app is asked to
  upload the image. (IOOIS in the wild — problem → opportunity.)
- **D-H. Places live inside a case-file, but can be shared/reused across
  case-files.** A challenge stays one case (not a city-mega-case). Multiple
  cases may reference the same places/routes. Implication: a place needs a
  **stable identity** (e.g. GPS-based id) so two cases can point at the same
  place. (See §13.)
- **D-I. Create the challenge-authoring case via the "pre-evolved case"
  shortcut now (Option 1); the config-generates-case approach (Option 2) is
  the later graduation.** The IOOIS setup form (§5) *is* the pre-evolved
  starting point. (See §13.)

---

## 9. Parked (deliberately, do not decide yet)

- **the_app contract / tree format** — nothing built there yet; wait.
  (`docs/engine-to-app-handoff-v0.1.md` exists but is not yet consulted.)
- **Export mechanism** — downloadable/preview JSON vs. HTTP push to the_app; wait.
- **Depth of structure beyond the thin slice** (routes, refinement passes,
  richer place fields) — target is heavier, but sequence it after the slice.
- **Multi-user co-authoring inside the engine** — collides with the known
  single-user `case` global limit; note, don't build toward it. (User
  participation belongs to the_app per D-G.)
- **themes flat vs. structured** — flat list for now; revisit if needed.
- **Option 2 (config-generates-case)** — later graduation of Option 1; build
  when case-copying becomes frequent friction. (See §13.)
- **Shared place pool across cases** — places are case-local in the thin
  slice; cross-case place reuse (via stable GPS-based ids) is a later step.
  (See §13 / D-H.)

---

## 10. Proposed thin first slice (target for a build spec, when ready)

Smallest thing that makes the way-of-working visibly real:

1. **Setup**: capture the IOOIS form (§5) into the CaseFile
   (interpretation-layer fields; model untouched). Minimum: area + themes +
   travel_mode + a `challenge_shape` with place count and completeness
   criteria.
2. **Item collection**: add a generic "artifact items" structure to the
   CaseFile for **places** only — `{id, name, gps, description, status}`.
3. **Item loop**: engine proposes a *set* of candidate places (count hinted by
   `challenge_shape`); maker approves / edits / rejects / requests-more
   **per item**. Reuse existing decision vocabulary where it fits.
4. **Completeness check**: compare places against the Ideal State criteria;
   surface what's missing ("3 places lack GPS", "need 7 more places") to drive
   "are we done?".
5. **Stop when Ideal State (places portion) is met.** Routes, refinement,
   export = later.

**Explicitly out of the thin slice:** routes, images, export, multi-user.

---

## 13. How a challenge-authoring case comes into being

A normal case starts empty and *discovers*, over several loops, that "what I
need is a challenge made of routes and places in an area, and here's the
Ideal-State output I want." That discovery is real work. Challenge authoring
wants to **skip that discovery** and begin already at that conclusion. Two
ways to do it:

### Option 1 — "Pre-evolved" case (do this now)

Create a case-file that **starts already shaped** as if the early loops had
happened: it opens knowing "this is a challenge = routes + places in an
area," with the Ideal State / desired output already defined, ready to go
straight into proposing places.

The IOOIS setup form (§5) **is** this pre-evolved starting point, baked into
the case at creation. No new machinery — filling in the form writes a
pre-shaped case. Reuse for another location = **copy the case and change the
ingredients** (Öland birds → Chiang Mai temples).

### Option 2 — Configuration file that generates the case (later)

The reusable thing is a **separate configuration file** (the "formula"): fill
in area / themes / travel-mode / Ideal-State shape, and the engine **reads
the config and stamps out a fresh case-file** from it. The config is the
template; the case is the instance. This is exactly the
"configuration-driven top-layer / profile" from §1 (and the user's very first
message: "define it so the top-level corresponds to ABCD / immigrant /
challenge").

### Relationship — Option 1 is the thin slice of Option 2

They produce nearly the same starting case; the difference is where the
reusable template lives and how you reuse it.

| | Option 1 (pre-evolved case) | Option 2 (config → case) |
|---|---|---|
| Reusable thing | A case you copy & edit | A config file you fill in |
| Reuse elsewhere | Copy case, change ingredients | Write new config, generate case |
| "Formula" location | Implicit, in a case's structure | Explicit, own file |
| Maps to | "case as template" | The §1 top-layer profile |

**Decision (D-I):** do **Option 1 now**; treat the setup form as the *seed*
of the Option-2 config later. The form's fields **are** the config's fields —
we just aren't putting them in a separate reusable file yet. Graduating to
Option 2 is then a small step: "load config → stamp out a pre-evolved case"
is Option 1 with values coming from a file instead of a screen.

**Natural trigger to graduate:** if you find yourself *copying cases
constantly*, that friction is the signal to build Option 2.

### Places: in-case but shareable (D-H)

Places live **inside** a case-file. But multiple case-files may reference the
**same** places/routes. For that reuse to be honest, a place needs a
**stable identity** (e.g. a GPS-based id) so two cases can point at the same
real-world place. Noted for whenever we design the place item (§10.2). Keep
the thin slice case-local; shared-place reuse is a deliberate later step.

---

## 11. Relevant code (for whoever resumes)

- `src/web.py` — the entire Flask top-layer: routes, inline templates, the
  navigation loop, case ownership. Single-user module-global `case` (~line 55;
  known limit). Loop routes: `/propose/<goal_id>`, `/select`, `/decide`,
  `/goal/<goal_id>`, tree at `/`.
- `src/engine_ai.py` — all LLM calls: `suggest` (sub-proposals), `propose` /
  `propose_for_selection` (missions), plus `SYSTEM_PROMPT` and
  `_build_context_message` (where the "hints" would be injected).
- `src/engine.py` — rule-based fallback; `Proposal`, `Interpretation`.
- `src/case_file.py` — data model + JSON persistence: `CaseFile`, `Goal`,
  `Mission`, `Observation`, `Decision`, `ObserverEventRecord`. This is where
  the item collection (§10.2) would be added.
- `src/observer.py` — optional "character" perspectives; never mutates the case.
- `cases/6d41beab.json` — real sample: "Linköping då och nu", a photo-walk
  challenge. Already a challenge-authoring case in free-text form — evidence
  the engine has been used this way; what's missing is setup framing + a
  structured, exportable result.

---

## 12. Next thinking (not yet done)

- Exact fields/JSON for the IOOIS setup on the CaseFile.
- Exact shape of the place item and the completeness criteria.
- How the setup seeds goals and how the LLM prompt/context carries the IOOIS
  "hints" in model vocabulary.
- Then: turn §10 into an agreed build spec.
