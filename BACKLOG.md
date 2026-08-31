# Backlog

A list of concrete tasks and work items to be addressed.

---

## Shared identity & authentication

Goal: a central auth service that the_app, the_engine and future apps use to
share the same users. See `docs/spec/auth/`.

### Spec (in progress)
- [x] Reference: document the_app's current auth solution
      (`docs/spec/auth/the-app-current-solution-v0.1.md`)
- [x] Architecture & decision: central auth service + JWT
      (`docs/spec/auth/architecture-and-decision-v0.1.md`)
- [x] Auth service contract: endpoints + token model
      (`docs/spec/auth/auth-service-contract-v0.1.md`)
- [x] Resolve open decisions in contract §7 (locked v0.1 defaults:
      HS256, 7-day token, token on register, the_app stack, simple engine identity)
- [x] Per-flow spec: registration (`docs/spec/auth/flow-registration-v0.1.md`)
- [x] Per-flow spec: login (`docs/spec/auth/flow-login-v0.1.md`)
- [x] Per-flow spec: change password (`docs/spec/auth/flow-change-password-v0.1.md`)
- [x] Per-flow spec: close account (`docs/spec/auth/flow-close-account-v0.1.md`)
- [x] Roles & authorization: admin / user / demo_user
      (`docs/spec/auth/roles-and-authorization-v0.1.md`)
- [x] Per-flow spec: forgot password (server-side code via email/SMS)
      (`docs/spec/auth/flow-forgot-password-v0.1.md`)

### Deferred (designed, not built first)
- [ ] Choose & integrate email/SMS provider (needed for forgot-password;
      may require a paid service — decide when we build around it)
- [ ] Spec + build email/phone verification (spec it together with the
      provider work, not before)
- [ ] Migrate away from legacy plaintext passwords
- [ ] Move the_app mobile binary to JWT (requires new App Store review)
- [ ] Normalize legacy role value `administrator` -> `admin` in DB
- [ ] Set `role: demo_user` on the_app's existing demo_user account (backend-only)
- [ ] Admin endpoint to set/change roles (with audit log)
- [ ] Admin close-account endpoint (`DELETE /auth/admin/accounts/:id`)

### Build (after spec)
- [ ] Extract auth logic from the_app `api-server/server.js` into the service
- [ ] Build the_engine against the auth service from the start
