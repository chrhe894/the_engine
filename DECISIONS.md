# Decisions

A log of significant design and architecture decisions.

---

## D-001 — Central authentication service for shared users

**Date:** 2026-08-31

**Context**
Multiple apps must share the same users: the_app (in production, under App Store
review), the_engine (under construction), and 3–4 future apps using the same
information model. the_app has no shareable login today — login returns only the
profile object and protected calls trust a client-supplied `profile_id`. There is
no token another app can rely on.

**Decision**
Build a small, own central authentication service that all apps use as the source
of truth for identity and login. It issues signed JWTs that each app verifies
independently. Stack: Node/Express + Postgres + bcrypt + JWT, reusing the_app's
existing user storage (`information_items` / `Användarprofil`) so the database
remains the source of user data.

**Rationale**
- Standard pattern (OAuth2/OIDC "identity provider") for many-apps-one-identity.
- Letting the_engine call the_app's current endpoints is not safe: no shareable
  token, and `profile_id` trust can be forged.
- An external IdP (Auth0/Clerk/Keycloak) is robust but slower to adopt, costs
  money, and puts user data with a third party. The token-based design keeps a
  future switch cheap.

**Migration principle**
Backend-first. Do not touch the mobile app binary while App Store review is
pending (backend/API changes need no review; a new binary does). Keep the
database as the source, extract auth logic from the_app into the service, build
the_engine against it from the start, and move the_app binary to JWT later as a
deliberate step.

**Deferred (designed, not built first)**
Server-side forgot-password with email/SMS, real email/phone verification,
migration away from legacy plaintext passwords, and moving the_app binary to JWT.

**References**
- docs/spec/auth/architecture-and-decision-v0.1.md
- docs/spec/auth/auth-service-contract-v0.1.md
- docs/spec/auth/the-app-current-solution-v0.1.md

---

## D-002 — Three user roles: admin, user, demo_user

**Date:** 2026-08-31

**Context**
Authorization was unspecified. the_app detects admin ad hoc via
`content_blob.role === 'administrator'` or capabilities (`manage_channels`,
`system_admin`), and uses a profile named `demo_user` as a default login, but has
no explicit role model.

**Decision**
Define three roles stored in `content_blob.role`: `admin` (full access),
`user` (default for new accounts, owns/manages own resources), and `demo_user`
(read-only demo/guest account). Authorization is decided server-side from the
token's `sub` plus the role looked up from the database (role is not an
authoritative token claim in v0.1, so role changes take effect immediately).

**Backward compatibility**
A user counts as admin if `role` is `admin` OR the legacy `administrator`, or if
capabilities include `manage_channels`/`system_admin`. This keeps the_app working.
`demo_user` is identified by `role === 'demo_user'`; the_app's existing demo
account should get this role set (backend-only).

**Deferred**
Normalize `administrator` -> `admin`, an admin endpoint to change roles (audited),
an admin close-account endpoint, and caching role in the token once refresh
tokens exist.

**References**
- docs/spec/auth/roles-and-authorization-v0.1.md

---

## D-003 — Auth as a separate service (own repo), sharing the_app's database

**Date:** 2026-08-31

**Context**
Need to decide where the auth service lives. Constraints: avoid touching the_app
(in App Store review), don't block progress, prefer the right long-term shape.

**Decision**
Build the auth service as a **separate project** in its own repo (`c:\repo\the_auth`),
deployed as its own Render service. It does not modify the_app's code, but connects
to the **same Postgres database** and reads/writes the same `Användarprofil` items,
so users are shared. Stack: Node/Express + pg + bcrypt + jsonwebtoken.

Cold start is a non-issue: the service runs on a paid Render tier.

**Rationale**
- Zero risk to the_app and the ongoing App Store review.
- Cleaner separation for the long term (the shared-service goal), which the user
  approved.
- the_engine and future apps consume it via JWT from day one.

**Build order**
Skeleton -> DB data layer -> JWT issue/verify middleware -> register + login ->
me, change-password, close-account, forgot-password (without provider sending).

**References**
- docs/spec/auth/auth-service-contract-v0.1.md (§7)
