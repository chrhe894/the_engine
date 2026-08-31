# Current focus

## Shared identity & authentication (active)
Central auth service so the_app, the_engine and future apps share the same users.
See `docs/spec/auth/` and decision D-001 in `DECISIONS.md`.

Done:
[x] Reference doc of the_app's current auth solution
[x] Architecture & decision (central auth service + JWT)
[x] Auth service contract (endpoints + token model)
[x] Locked v0.1 defaults in contract §7
[x] Per-flow spec: registration
[x] Per-flow spec: login
[x] Per-flow spec: change password
[x] Per-flow spec: close account

[x] Precise close-account rules verified against the_app (3-day grace,
    hourly purge, transfer-vs-delete of owned Plats/Samling content)
[x] Consistency review of contract + four flow specs
[x] Roles & authorization spec (admin / user / demo_user)
[x] Forgot-password spec (server-side code via email/SMS)

Decisions:
- Deploy: /auth/* routes in the_app's existing Render service (gsis-api),
  sharing its Postgres DB and env vars (JWT_SECRET). Separate service later.
- Email/phone verification deferred until we build around it (may need a paid
  provider). Forgot-password needs an email/SMS provider too.

Build (in progress) — separate service at c:\repo\the_auth:
[x] Project skeleton (Express + pg + bcrypt + jsonwebtoken + env config)
[x] DB data layer for Användarprofil items (shared with the_app)
[x] JWT issue/verify + requireAuth middleware
[x] POST /auth/register, /auth/login, GET /auth/check, GET /auth/me
[x] POST /auth/password/change, DELETE /auth/account (soft delete + grace)
[x] POST /auth/password/forgot + /reset (dev sender logs code; provider deferred)
[x] Hourly purge job + auth_password_resets table bootstrap
[x] End-to-end logic verified against in-memory DB fake (16/17; the 1 is a
    fake limitation — closed accounts are anonymized so login gives 401 not 403,
    now noted in the login spec)

Real DB test: separate empty test DB on Render (option 2).
[x] Fixed register INSERT to satisfy information_items NOT NULL columns
    (location/time/scope/intent) — would have failed against the real schema
[x] scripts/init-test-schema.sql (incl. auth_password_resets)
[x] scripts/verify-against-db.js (full flow over real HTTP + DB, self-cleaning)
[x] VERIFIED: 12/12 pass against real Render Postgres

the_auth service is complete and verified for v0.1.

Deploy the_auth to Render (chosen: paid service already provisioned):
[x] render.yaml blueprint (starter plan, /health check, secrets sync:false)
[x] engines.node >=20 pinned; production fails fast without JWT_SECRET (verified)
[x] Deploy guide: docs/spec/auth/deploy-the-auth-to-render-v0.1.md
[x] Pushed to github.com/chrhe894/the_auth (main)
[x] Deployed to Render (free tier for now — spins down when idle; upgrade later);
    /health returns {"status":"ok"} against the shared DB
[x] AUTH_BASE_URL = https://the-auth.onrender.com (verified /auth/check reads shared DB)
[ ] Later: upgrade the_auth web service off free tier to avoid cold starts

the_engine integration (spec: docs/spec/auth/engine-integration-v0.1.md):
[x] Step 1 — login gate: auth_client.py + Flask session + /login /logout,
    before_request guard, login page, user bar. Verified end-to-end against
    live the_auth (login, session, logout). the_engine is Python/Flask.

[x] Step 2 — cases per user: owner_id on CaseFile, /cases landing (my cases;
    admin sees all), create/open/delete, before_request loads selected case.
    Verified: owner stamped, ownership isolation (user2 can't see/open user1's
    case), admin-only delete. Known limit: global `case` var = single-user only.

Next:
[ ] Step 3 — admin tools (templates for routes/challenges, clear cases)
[ ] Give your account role=admin in the DB when you want to test admin mode
[ ] (If engine ever multi-user concurrent) move `case` off module global

---

# Model work (parallel track)

[ ] Reality / Model Assessment
[ ] Phase 1/2 DoD
[ ] Golden Case — Immigrant
[ ] Golden Case — Skördefest
[ ] Primitive-concept check
[ ] Information Model cleanup
[ ] Transition ↔ Mission ↔ DoD
[ ] Model v0.1
              │
              ▼
       Prototype specification
              │
              ▼
          BUILD IT