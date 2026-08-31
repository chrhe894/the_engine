# Auth-tjänst – kontrakt och token-modell (v0.1)

Detta dokument definierar **den centrala auth-tjänstens gränssnitt**: vilka
endpoints den erbjuder och hur inloggningstoken (JWT) ser ut. Det är grunden som
alla per-flödes-specar bygger på.

Relaterat:
- [Arkitektur och beslut](architecture-and-decision-v0.1.md)
- [the_app – nuvarande lösning](the-app-current-solution-v0.1.md)
- Per-flöde: [registrering](flow-registration-v0.1.md) ·
  [login](flow-login-v0.1.md) ·
  [byta lösenord](flow-change-password-v0.1.md) ·
  [glömt lösenord](flow-forgot-password-v0.1.md) ·
  [avsluta konto](flow-close-account-v0.1.md)
- [Roller och behörighet](roles-and-authorization-v0.1.md)

Status: **beslutad baslinje för v0.1.** Låsta beslut listas i avsnitt 7.

---

## 1. Tjänstens ansvar

Auth-tjänsten äger:
- Användaridentitet (registrering, unika användarnamn/e-post/telefon).
- Lösenord (bcrypt-hashning och verifiering).
- Inloggning och utfärdande av signerade tokens (JWT).
- Kontolivscykel (aktivt konto, avsluta konto med grace period).
- Roller och behörighet (`admin` / `user` / `demo_user`), se
  [roller och behörighet](roles-and-authorization-v0.1.md).

Auth-tjänsten äger **inte** appspecifik data (innehåll, platser, prenumerationer).
Den lagrar användare i samma Postgres som the_app använder i dag
(`information_items` med `subject = 'Användarprofil'`), så databasen förblir
källan för användardata.

Appar (the_app, the_engine, framtida appar) **verifierar tokens själva** och
frågar bara tjänsten vid inloggning, registrering och kontoändringar.

---

## 2. Token-modell (JWT)

En inloggning ger en **access-token** (JWT) som appen skickar med i skyddade anrop.

Innehåll (claims) i access-token:

| Claim  | Betydelse                                             |
|--------|-------------------------------------------------------|
| `sub`  | Användarens id (profilens UUID) – "vem"               |
| `iss`  | Utfärdare = auth-tjänsten                              |
| `aud`  | Avsedd mottagare (vilken app token är till för)       |
| `iat`  | Utfärdad-tidpunkt                                      |
| `exp`  | Utgångstid (kort livslängd, se avsnitt 7)             |
| `name` | Användarnamn (bekvämlighet, ej auktoritativt)         |

Principer:
- Token är **signerad** av auth-tjänsten. En app litar på token genom att
  verifiera signaturen – inget behov av att fråga tjänsten per anrop.
- Token ersätter dagens osäkra `profile_id`-tillit. Skyddade anrop identifierar
  användaren via `sub` i en verifierad token, inte via ett fritt `profile_id`.
- Känsliga fält (lösenordshash, e-post, telefon) läggs **aldrig** i en token.

Signering och livslängd för v0.1: **HS256** (delad hemlig nyckel), giltighet
**7 dagar** (`exp = iat + 7 dygn`), ingen refresh. Se beslut i avsnitt 7.
Lösenord hashas med **bcrypt (10 rundor)**, matchar the_app.

---

## 3. Endpoints (kontrakt)

Alla svar är JSON. Fel returneras som `{ "error": "…" }` med passande HTTP-status.
Bas-URL anges vid deploy (tjänsten körs i the_app:s stack först, se avsnitt 7).

### 3.1 `POST /auth/register` – skapa konto
Request:
```jsonc
{
  "username": "…",
  "password": "…",
  "email":    "namn@exempel.se",   // valfritt men rekommenderat
  "phone":    "+46…",              // valfritt
  "full_name":"…"                  // valfritt
}
```
Regler:
- `username` och `password` krävs (`password` minst 8 tecken).
- `admin` är reserverat → `403`.
- Unikt användarnamn/e-post/telefon (mot konton som inte är `pending_deletion`)
  → `409` vid krock, med tydligt felmeddelande om vilket fält som krockar.
- Lösenord hashas med bcrypt serverside.

Svar `201`: den skapade användaren (utan lösenordshash) **+ en utfärdad token**
(användaren är inloggad direkt). Detaljer i [registreringsflödet](flow-registration-v0.1.md).

### 3.2 `POST /auth/login` – logga in
Request: `{ "username": "…", "password": "…" }`
- Fel användarnamn/lösenord → `401`.
- Konto under avslutning (`pending_deletion`) → `403`.
- Lösenordsverifiering med bcrypt; **legacy plaintext accepteras tillfälligt**
  under migrering (se the_app-referensen).

Svar `200`:
```jsonc
{
  "token": "<JWT>",
  "user": { "id": "…", "username": "…", "full_name": "…" }
}
```

### 3.3 `GET /auth/check?username=&email=&phone=` – tillgänglighet
Returnerar booleaner: `{ "username": false, "email": false, "phone": false }`.
Används av registreringsflöden för att kontrollera innan man skickar in.

### 3.4 `GET /auth/me` – vem är inloggad
Kräver giltig token. Returnerar den inloggade användaren (från `sub`).
Ingen känslig data.

### 3.5 `POST /auth/password/change` – byt lösenord (inloggad)
Kräver giltig token. Request: `{ "current_password": "…", "new_password": "…" }`.
- Fel nuvarande lösenord → `401`.

### 3.6 `DELETE /auth/account` – avsluta eget konto
Kräver giltig token. Utför **soft delete med grace period** (samma modell som
the_app i dag): `phase = 'pending_deletion'`, credentials/e-post/telefon nollas,
`deletion.delete_after` sätts (**3 dagar**), ägt innehåll köas/överförs. Ett
bakgrundsjobb hårdraderar efter grace-perioden (körs varje timme). Detaljer i
[avsluta-konto-flödet](flow-close-account-v0.1.md).

### 3.7 `POST /auth/password/forgot` + `POST /auth/password/reset` – glömt lösenord
Serverside återställning med engångskod via e-post/SMS. Neutralt svar som inte
avslöjar om konto finns. Detaljer i
[glömt-lösenord-flödet](flow-forgot-password-v0.1.md). Kräver en utskickskanal
(e-post/SMS) som är ett infrastrukturberoende.

### 3.8 Uppskjutet (designat, ej byggt först)
- `POST /auth/verify/email` + `POST /auth/verify/phone` – riktig verifiering.
- `POST /auth/token/refresh` – förnyelse av token (beror på token-livslängd, avsnitt 7).

---

## 4. Hur apparna använder tjänsten

- **Login:** appen anropar `POST /auth/login`, får token, lagrar den säkert
  (inte lösenord i klartext som i dag), och skickar med den i skyddade anrop.
- **Verifiering:** varje app/tjänst verifierar token-signaturen lokalt och läser
  `sub` för att veta vem användaren är.
- **the_engine** byggs mot detta från start.
- **the_app** kan bakom kulisserna delegera sin `/api/auth/login` till tjänsten
  utan ändring i mobil-binären; full övergång till token i appen är ett senare steg.

---

## 5. Datakontrakt (användare i databasen)

Oförändrat mot i dag för att inte bryta the_app: en användare är ett
`information_items` med `subject = 'Användarprofil'`, `content_blob.type =
'user_profile'`, och:
```jsonc
{
  "role": "user",                 // "admin" | "user" | "demo_user"
  "credentials": { "username": "…", "password_hash": "$2b$…" },
  "email": { "value": "…" },
  "phone": { "value": "…" },
  "full_name": "…"
}
```
Auth-tjänsten läser/skriver exakt denna form. Roller och behörighet definieras i
[roller och behörighet](roles-and-authorization-v0.1.md); bakåtkompatibilitet med
the_app:s nuvarande admin-detektering beskrivs där.

---

## 6. Säkerhetsregler (baslinje)

- Lösenord lagras endast som bcrypt-hash (10 rundor).
- Tokens är signerade (HS256) och tidsbegränsade (7 dagar); ingen känslig data i token.
- Fel användarnamn och fel lösenord ger **samma** `401`-svar (avslöja inte om
  användaren finns).
- Konton under avslutning kan inte logga in.
- All auth sker över HTTPS.

---

## 7. Beslut för v0.1 (låsta, kan skärpas senare)

Följande är beslutade som utgångspunkt. De prioriterar fart utan att låsa oss –
varje val kan skärpas senare utan att kontraktet ovan ändras i grunden.

| Fråga | Beslut för v0.1 | Skärps senare till |
|-------|-----------------|--------------------|
| Signering | **HS256** (delad hemlig nyckel) | RS256 (nyckelpar) när fler tjänster tillkommer |
| Token-livslängd | **Enkel token, 7 dagar**, ingen refresh | Kort access-token + refresh-token |
| Register-svar | **Token direkt** vid lyckad registrering | — |
| Deploy | **Separat tjänst** (eget repo `the_auth`), egen Render-tjänst, delar the_app:s Postgres | — |
| the_engine-identitet | **Enkelt** (ingen klientautentisering) | Klient-id/hemlighet när fler appar finns |

Konsekvenser av besluten:
- HS256 innebär att auth-tjänsten och varje app som verifierar token delar samma
  hemliga nyckel. Nyckeln lagras som **miljövariabel** (t.ex. `JWT_SECRET`),
  aldrig i repo.
- **Deploy-miljö:** auth-tjänsten är en **separat tjänst** (eget repo `the_auth`)
  med en egen Render-tjänst. Den **rör inte the_app:s kod** men använder **samma
  Postgres-databas** som the_app, och läser/skriver samma `Användarprofil`-items
  så användarna delas. Detta skyddar the_app (och pågående App Store-granskning)
  och ger den renare separationen på sikt.
- **Cold start:** tjänsten körs på betald Render-nivå, så inaktivitets-vila är
  inget problem.
- 7-dagars token utan refresh betyder att användaren loggar in igen efter att
  token gått ut. Enkelt och tillräckligt för v0.1.
- Token direkt vid registrering innebär att användaren är inloggad omedelbart.

Per-flödes-specarna (registrering, login, byta lösenord, avsluta konto) är
skrivna mot detta kontrakt och länkas överst i dokumentet.
