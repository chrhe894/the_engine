# Flöde: Registrering (v0.1)

Detaljspec för att skapa ett nytt konto mot den centrala auth-tjänsten.
Bygger på [auth-tjänstens kontrakt](auth-service-contract-v0.1.md).

Endpoint: `POST /auth/register`

---

## 1. Syfte

Skapa en ny användare, spara den i den delade databasen (samma
`Användarprofil`-representation som the_app använder), och logga in användaren
direkt genom att returnera en token.

---

## 2. Indata

```jsonc
{
  "username": "…",                 // krävs
  "password": "…",                 // krävs
  "email":     "namn@exempel.se",  // valfritt men rekommenderat
  "phone":     "+46…",             // valfritt
  "full_name": "…"                 // valfritt
}
```

### Valideringsregler
| Fält | Regel |
|------|-------|
| `username` | krävs, icke-tom efter trim; `admin` är reserverat |
| `password` | krävs, minst 8 tecken |
| `email` | om angivet: giltigt e-postformat |
| `phone` | om angivet: normaliseras (mellanslag/bindestreck tas bort) före jämförelse |

---

## 3. Steg (serverside)

1. **Validera indata** enligt tabellen ovan. Fel → `400` med tydligt felmeddelande.
2. **Reserverat namn:** om `username` (skiftlägesokänsligt) är `admin` → `403`
   "Reserverat användarnamn".
3. **Unikhetskontroll** mot konton som *inte* är `pending_deletion`:
   - användarnamn (`name` eller `content_blob.credentials.username`) → `409`
     "Användarnamnet är redan taget"
   - e-post (`content_blob.email.value`, skiftlägesokänslig) → `409`
     "E-postadressen används redan"
   - telefon (normaliserad `content_blob.phone.value`) → `409`
     "Telefonnumret används redan"
4. **Hasha lösenord** med bcrypt.
5. **Skapa användaren** som ett `information_items` med rollen `user` (se
   [roller och behörighet](roles-and-authorization-v0.1.md)):
   ```jsonc
   {
     "subject": "Användarprofil",
     "name": "<username>",
     "phase": "active",
     "content_blob": {
       "type": "user_profile",
       "role": "user",
       "credentials": { "username": "<username>", "password_hash": "$2b$…" },
       "email": { "value": "<email>" },   // endast om angivet
       "phone": { "value": "<phone>" },   // endast om angivet
       "full_name": "<full_name>"         // endast om angivet
     }
   }
   ```
6. **Utfärda token** (JWT, HS256, 7 dagars giltighet) med `sub` = användarens id.
7. **Svar `201`** enligt nedan.

---

## 4. Utdata

Lyckad registrering `201`:
```jsonc
{
  "token": "<JWT>",
  "user": {
    "id": "…",
    "username": "…",
    "full_name": "…"
  }
}
```
Lösenordshash, e-post och telefon returneras **inte** i svaret.

Felsvar:
| Status | När |
|--------|-----|
| `400` | saknade/ogiltiga fält |
| `403` | reserverat användarnamn (`admin`) |
| `409` | användarnamn, e-post eller telefon upptaget |
| `500` | internt fel |

---

## 5. Kanttfall

- **Race condition** (två samtidiga registreringar av samma namn): unikhetskoll
  följs av databasens unikhetsgaranti; vid krock → `409`.
- **Konto under avslutning** med samma namn/e-post/telefon blockerar inte
  registrering (uniktkontrollen exkluderar `pending_deletion`). Vid behov att
  återanvända en identitet hanteras det separat i avsluta-konto-flödet.
- **Legacy plaintext:** gäller inte registrering – nya konton hashas alltid.

---

## 6. Klientflöde (rekommenderat)

1. (Valfritt) Anropa `GET /auth/check` medan användaren fyller i, för att visa
   tillgänglighet på användarnamn/e-post/telefon i realtid.
2. Skicka `POST /auth/register`.
3. Vid `201`: lagra token säkert och betrakta användaren som inloggad.
4. Vid `409`: visa vilket fält som krockar.

---

## 7. Uppskjutet

- E-post-/telefonverifiering efter registrering (designas separat).
- Krav på verifierad e-post innan vissa åtgärder.
