# Referens: the_app – nuvarande lösning för användare & inloggning (v0.1)

Detta dokument beskriver hur **the_app** hanterar användare och inloggning i dag.
Det är en **nulägesbeskrivning** (reverse-engineered från koden), inte en design för
the_engine. Syftet är att ge en gemensam utgångspunkt innan vi specar hur
the_engine och the_app ska **dela samma användare**.

Beslut (från diskussion): **the_app + dess databas är källan (source of truth)
för användare.** the_engine ska återanvända dessa användare. Hur the_engine
loggar in mot dem är ännu inte bestämt.

Källor i koden:
- `the_app/api-server/server.js` (Express + Postgres, ca 2600 rader)
- `the_app/mobile-app/src/hooks/useAuth.ts` (klientflöden)
- `the_app/mobile-app/src/api.ts` (fetch-wrapper)

---

## 1. Datamodell – en användare är ett "information_item"

the_app har **ingen dedikerad users-tabell** och **ingen separat auth-tjänst**.
En användare lagras som en rad i den generiska tabellen `information_items`:

- `subject = 'Användarprofil'`
- `content_blob.type = 'user_profile'`
- `name` = användarnamnet
- `phase` = `'active'` normalt, `'pending_deletion'` vid avslutat konto

Relevanta fält i `content_blob`:

```jsonc
{
  "type": "user_profile",
  "credentials": {
    "username": "…",
    "password_hash": "$2b$…"   // bcrypt, se nedan
  },
  "email":  { "value": "namn@exempel.se" },
  "phone":  { "value": "+46…" },
  "full_name": "…",
  "subscriptions": ["SYSTEM_CHANNEL", "LIVE_CHANNEL", …],
  "deletion": {                 // finns endast vid pending_deletion
    "requested_at": "…",
    "delete_after": "…",
    "action": "delete_account_after_grace_period"
  }
}
```

> Obs: `item_verifications`-tabellen i the_app är **innehållsverifiering**
> (support/verify/like på items) och har inget med kontoverifiering att göra.

---

## 2. Registrering (skapa konto)

Endpoint: `POST /api/items` (samma generiska endpoint som för allt annat innehåll).
Profil-specifik logik körs när `content_blob.type === 'user_profile'` eller
`subject === 'Användarprofil'`.

Regler som gäller vid registrering:
- **Obligatoriskt:** `name` och `subject` (icke-tomma strängar), samt en avsändare (`from`).
- **`admin` är reserverat** som användarnamn (403).
- **Unikhetskontroller** mot alla profiler som inte är `pending_deletion`:
  - användarnamn (`name` eller `content_blob.credentials.username`) → 409 "Användarnamnet är redan taget"
  - e-post (`content_blob.email.value`, skiftlägesokänslig) → 409 "E-postadressen används redan"
  - telefon (`content_blob.phone.value`, mellanslag/bindestreck normaliseras) → 409 "Telefonnumret används redan"
- **Lösenord hashas** med bcrypt vid spara om det inte redan är en bcrypt-hash
  (`$2b$`/`$2a$`). Plaintext skickas alltså in i `credentials.password_hash`
  och hashas serverside.

Det finns även en hjälpendpoint `GET /api/users/check?username=&email=&phone=`
som returnerar `{ username, email, phone }` som booleaner för att kontrollera
tillgänglighet innan registrering.

---

## 3. Inloggning

Endpoint: `POST /api/auth/login` med `{ username, password }`.

Flöde serverside:
1. Slår upp profil där `subject = 'Användarprofil'`, `phase <> 'pending_deletion'`,
   och `name` (skiftlägesokänsligt) eller `content_blob->>'username'` matchar.
2. Saknas profil → **401** "Fel användarnamn eller lösenord".
3. `phase = 'pending_deletion'` → **403** "Kontot är avslutat och väntar på permanent radering".
4. Verifierar lösenord:
   - bcrypt-hash → `bcrypt.compare`
   - annars **legacy plaintext-jämförelse** (för migreringsperiod)
5. Fel lösenord → **401**. Rätt → **200** med hela profil-objektet.

### Viktig begränsning: ingen session/token
- Login returnerar **bara profil-objektet**. Det finns **ingen JWT och ingen serverside-session**.
- Klienten sparar `username` + `password` i klartext i `AsyncStorage`
  (`saved_username`, `saved_password`) och håller `activeProfile` i minnet.
- Efterföljande skyddade anrop (t.ex. redigera profil, radera konto) auktoriseras
  genom att skicka med `profile_id` i request. Servern litar på detta `profile_id`
  (matchar ägare eller admin) — det finns **ingen kryptografiskt verifierad identitet**
  i anropen.

Detta är den enskilt viktigaste punkten för delad inloggning: **det finns i praktiken
ingen delbar autentiseringsmekanism (token) i dag.** Auth är "credential replay" +
tillit till ett `profile_id` i body/query.

---

## 4. Glömt lösenord

I dag **klientdrivet och demo-mässigt** (`useAuth.ts`):
- Återställningskoden genereras i **klienten** (`Math.random`, 4 siffror) och visas
  i en `Alert` ("Demo-kod: …"). Ingen kod skickas via e-post/SMS serverside.
- Klienten har rate limiting i minnet: koden giltig 5 min, max 5 felförsök
  (15 min lås), max 3 omsändningar, 60 s mellan omsändningar.
- Vid korrekt kod görs en `PUT /api/items/:id` med nytt lösenord (som sedan
  hashas serverside).

Detta är alltså **inte** ett säkert serverside-flöde och en tydlig kandidat att
göra om när vi ändå rör auth.

---

## 5. Byta lösenord (inloggad)

Endpoint: `PUT /api/items/:id` med `profile_id` + `current_password`.
- Kräver ägare (`item.id === profile_id`) eller admin.
- Om nytt lösenord anges tillsammans med `current_password` verifieras det gamla
  mot bcrypt-hashen (eller legacy plaintext) → annars **401** "Nuvarande lösenord är felaktigt".
- `content_blob` merge:as så att credentials/email/phone/verification bevaras.

---

## 6. Avsluta konto (soft delete + grace period)

Endpoint: `DELETE /api/items/:id?profile_id=…`.
- Tillåtet för ägaren (self-delete) eller admin, annars 403.
- **Hårdraderar inte direkt.** I stället:
  - `phase = 'pending_deletion'`
  - `credentials`, `email`, `phone` nollas i `content_blob`
  - `deletion = { requested_at, delete_after, action }` sätts
  - namn ersätts med `deleted_user_<id-prefix>`, media/bilder rensas
  - ägt innehåll köas för radering eller överförs till admin-kontot
- Ett bakgrundsjobb `purgeExpiredAccountDeletions()` hårdraderar profiler och
  innehåll vars `delete_after` passerats.

---

## 7. Sammanfattning inför the_engine-spec

Styrkor att bygga vidare på:
- Tydlig lagringsplats för användare (Postgres, `information_items` / `Användarprofil`).
- bcrypt-hashning finns redan.
- Unikhetsregler för användarnamn/e-post/telefon finns.
- Genomtänkt avsluta-konto med grace period.

Svagheter / öppna frågor som påverkar delad inloggning:
1. **Ingen delbar token/session.** the_engine kan inte "återanvända" en inloggning
   eftersom ingen sådan artefakt finns. Vi behöver troligen införa något
   (t.ex. JWT eller sessions) som **både** system kan lita på.
2. **`profile_id` som auktorisering** är osäkert (kan förfalskas). Bör ersättas
   med verifierad identitet.
3. **Glömt lösenord är demo/klientdrivet** — bör flyttas serverside med riktig
   kod-utskick (e-post/SMS).
4. **Ingen riktig e-post-/telefonverifiering** finns, bara unikhetskontroll.
5. **Legacy plaintext-lösenord** stöds fortfarande vid login (migrering pågår).

### Öppna designfrågor för delad användare (att besluta härnäst)
- Var lever auth-logiken? Kvar i the_app (som identitetsleverantör med nya
  endpoints) eller lyfts ut till en delad tjänst som båda anropar?
- Vilken mekanism delar systemen? (JWT signerad med delad nyckel, OAuth-liknande
  flöde, delad session-store, …)
- Hur undviker vi ändringar i mobil-app-binären under pågående App Store-granskning?
  (Prioritera backend-only-ändringar; app-binären kräver ny granskning, backend/API gör inte det.)

> Nästa dokument: förslag på hur the_engine autentiserar mot the_app:s användare
> utan att bryta det som redan finns.
