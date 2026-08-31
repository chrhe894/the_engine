# the_engine-integration med the_auth (v0.1)

Hur the_engine (Python/Flask-prototypen i `prototype/`) använder den centrala
auth-tjänsten. Bygger på [auth-tjänstens kontrakt](auth-service-contract-v0.1.md).

## Bakgrund och roller

the_engine är i nuläget ett **utvecklings-/adminverktyg**, inte slutprodukten för
vanliga användare. Slutanvändare möter engine inuti the_app (långt senare).

- **admin** (du): bygger färdiga rutter/utmaningar, rensar cases, ser allt.
- **user** (även du, samt testanvändare): testkör engine med ett riktigt konto.
- Att engine-sidan senare döljs för vanliga användare styrs av **behörigheter**
  (roll), inte genom att ta bort funktionalitet.

## Trestegsplan

### Steg 1 — Login-grind (KLART)
- Man måste logga in för att nå engine. Session i Flask-cookie.
- the_engine anropar `POST /auth/login` och lagrar token + user i sessionen.
- Token verifieras genom `GET /auth/me` vid behov (ingen delad JWT-nyckel i Python).
- Rollen (`admin`/`user`) läses från user-objektet.
- Rör inte case-hanteringen.

### Steg 2 — Cases per användare (KLART)
- `CaseFile` fick fältet `owner_id` (serialiseras; `None` för äldre filer).
- `/cases` är ny startsida: listar användarens egna cases (+ oägda legacy-cases);
  admin ser alla. Skapa/öppna/radera därifrån.
- `/cases/new` stämplar `owner_id` = inloggad användare.
- `/cases/open/<id>` kontrollerar åtkomst (ägare eller admin) innan det väljs.
- `/cases/delete/<id>` är admin-only.
- `before_request`-grinden laddar det valda caset (från `session["case_id"]`)
  in i den globala `case`-variabeln före varje engine-route; saknas val →
  redirect till `/cases`. De befintliga engine-routerna lämnades orörda.

**Känd begränsning (medveten för v0.1):** the_engine använder fortfarande en
modul-global `case`-variabel som laddas per request. Det räcker för ett
enanvändar-/admin-utvecklingsverktyg, men **två samtidiga användare skulle kunna
krocka**. Om engine ska köras av flera samtidigt behöver caset flyttas till
per-request-scope (t.ex. Flask `g`) i stället för en global. Uppskjutet.

### Steg 3 — Admin-verktyg (planerat)
- Skapa färdiga rutter/utmaningar som mallar.
- Rensa cases; ev. se/hantera andras cases.
- Gömma admin-funktioner för `user` via rollkontroll.

## Tekniska beslut (Steg 1)

- **Verifiering:** login + `/auth/me` mot the_auth. the_engine verifierar inte
  JWT själv (ingen delad hemlighet i Python).
- **Session:** JWT + user lagras i Flask-session-cookien, signerad med
  `FLASK_SECRET_KEY`.
- **Konfiguration** (i `prototype/.env`, ej i git):
  - `AUTH_BASE_URL` = `https://the-auth.onrender.com`
  - `FLASK_SECRET_KEY` = långt slumpmässigt värde
- **Filer:** `prototype/src/auth_client.py` (HTTP mot the_auth),
  auth-wiring i `prototype/src/web.py` (`login_required`, `before_request`-grind,
  `/login`, `/logout`, login-sida).

## Verifierat (Steg 1)

- Oinloggad `/` → 302 till `/login`.
- Login-sida laddar; fel inloggning ger fel (mot live the_auth).
- Lyckad login (testanvändare via live the_auth) → session satt, user-bar visas.
- Logout → session rensad, grinden aktiv igen.
- Testanvändaren städades bort via `DELETE /auth/account`.
