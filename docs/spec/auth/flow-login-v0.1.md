# Flöde: Inloggning (v0.1)

Detaljspec för att logga in mot den centrala auth-tjänsten.
Bygger på [auth-tjänstens kontrakt](auth-service-contract-v0.1.md).

Endpoint: `POST /auth/login`

---

## 1. Syfte

Verifiera användarnamn + lösenord och, vid framgång, utfärda en signerad token
(JWT) som appen använder för att identifiera användaren i efterföljande anrop.
Ersätter dagens osäkra `profile_id`-tillit i the_app.

---

## 2. Indata

```jsonc
{ "username": "…", "password": "…" }
```
Båda krävs. Saknas något → `400`.

---

## 3. Steg (serverside)

1. **Validera** att `username` och `password` finns. Annars `400`.
2. **Slå upp profil** där:
   - `subject = 'Användarprofil'`
   - `phase <> 'pending_deletion'`
   - `name` (skiftlägesokänsligt) **eller** `content_blob.credentials.username`
     matchar `username`.
3. **Ingen profil** → `401` "Fel användarnamn eller lösenord".
4. **Konto under avslutning** (`phase = 'pending_deletion'`) → `403`
   "Kontot är avslutat och väntar på permanent radering".
   > Not: uppslaget i steg 2 exkluderar redan `pending_deletion`. Dessutom
   > anonymiseras namnet och credentials/e-post nollas vid avslut (se
   > [avsluta konto](flow-close-account-v0.1.md)), så ett avslutat konto går i
   > praktiken inte längre att slå upp via användarnamn/e-post och ger då `401`.
   > `403` gäller det fall där kontot ändå kan identifieras (t.ex. uppslag via id).
5. **Verifiera lösenord** mot `content_blob.credentials.password_hash`:
   - börjar hashen med `$2b$`/`$2a$` → `bcrypt.compare`
   - annars **legacy plaintext-jämförelse** (tillfälligt under migrering)
6. **Fel lösenord** → `401` (samma svar som okänd användare).
7. **Utfärda token** (JWT, HS256, 7 dagar) med `sub` = profilens id.
8. **Svar `200`** enligt nedan.

---

## 4. Utdata

Lyckad inloggning `200`:
```jsonc
{
  "token": "<JWT>",
  "user": { "id": "…", "username": "…", "full_name": "…" }
}
```

Felsvar:
| Status | När | Meddelande |
|--------|-----|------------|
| `400` | saknat användarnamn/lösenord | "Användarnamn och lösenord krävs" |
| `401` | okänd användare **eller** fel lösenord | "Fel användarnamn eller lösenord" |
| `403` | konto under avslutning | "Kontot är avslutat och väntar på permanent radering" |
| `500` | internt fel | — |

> Viktigt: okänd användare och fel lösenord ger **samma** `401`. Avslöja inte om
> användaren finns.

---

## 5. Token-användning efter login

- Appen lagrar token **säkert** (inte lösenord i klartext, till skillnad från
  dagens the_app som sparar username+lösenord i AsyncStorage).
- Token skickas med i skyddade anrop (t.ex. `Authorization: Bearer <JWT>`).
- Varje app/tjänst verifierar signaturen lokalt och läser `sub` för identitet.
- När token gått ut (7 dagar) loggar användaren in igen. Ingen refresh i v0.1.

---

## 6. Migrering av the_app (senare, backend-först)

- the_app:s befintliga `POST /api/auth/login` kan bakom kulisserna delegera till
  auth-tjänsten och börja returnera en token, utan ändring i mobil-binären.
- Full övergång där appen använder token i alla anrop kräver ny app-binär och
  planeras när App Store-läget tillåter.

---

## 7. Säkerhetsnoteringar

- All inloggning över HTTPS.
- Överväg enkel rate limiting / fördröjning vid upprepade `401` (skydd mot
  brute force) – kan läggas till utan att kontraktet ändras.
- Legacy plaintext-stöd är tillfälligt; se uppskjuten migreringspunkt i backloggen.


