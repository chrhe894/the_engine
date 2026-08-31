# Flöde: Byta lösenord (inloggad) (v0.1)

Detaljspec för att en inloggad användare byter sitt lösenord.
Bygger på [auth-tjänstens kontrakt](auth-service-contract-v0.1.md).

Endpoint: `POST /auth/password/change`

> Detta gäller en **inloggad** användare som kan sitt nuvarande lösenord.
> Att återställa ett *glömt* lösenord (utan att vara inloggad) är ett separat,
> uppskjutet flöde – se avsnitt 7.

---

## 1. Syfte

Låta en inloggad användare byta sitt lösenord på ett säkert sätt: identiteten
kommer från en verifierad token, och det nuvarande lösenordet bekräftas innan
bytet genomförs.

---

## 2. Indata

Kräver giltig token (`Authorization: Bearer <JWT>`).

```jsonc
{
  "current_password": "…",   // krävs
  "new_password": "…"        // krävs
}
```

### Valideringsregler
| Fält | Regel |
|------|-------|
| token | krävs och giltig; `sub` identifierar användaren |
| `current_password` | krävs |
| `new_password` | krävs, minst 8 tecken, får inte vara samma som nuvarande |

---

## 3. Steg (serverside)

1. **Verifiera token.** Saknad/ogiltig/utgången token → `401`.
2. **Hämta användaren** via `sub` från token. Saknas → `401`.
3. **demo_user-spärr:** om `content_blob.role = 'demo_user'` → `403`
   (demokontot får inte byta lösenord). Se
   [roller och behörighet](roles-and-authorization-v0.1.md).
4. **Konto under avslutning** (`phase = 'pending_deletion'`) → `403`.
6. **Validera** `current_password` och `new_password` finns, och att
   `new_password` uppfyller reglerna. Annars `400`.
7. **Verifiera nuvarande lösenord** mot
   `content_blob.credentials.password_hash`:
   - bcrypt-hash → `bcrypt.compare`
   - legacy plaintext → direkt jämförelse (tillfälligt under migrering)
   - Fel → `401` "Nuvarande lösenord är felaktigt".
8. **Hasha nytt lösenord** med bcrypt.
9. **Uppdatera** `content_blob.credentials.password_hash`. Övriga fält i
   `content_blob` (e-post, telefon, prenumerationer m.m.) bevaras oförändrade
   (merge, ej överskrivning).
10. **Svar `200`.**

> Not: identiteten tas alltid från token (`sub`), aldrig från ett `profile_id`
> i request. Detta är skillnaden mot the_app:s nuvarande `PUT /api/items/:id`.

---

## 4. Utdata

Lyckat byte `200`:
```jsonc
{ "message": "Lösenordet har uppdaterats" }
```

Felsvar:
| Status | När |
|--------|-----|
| `400` | saknade/ogiltiga fält, eller nytt = nuvarande |
| `401` | ogiltig token, eller fel nuvarande lösenord |
| `403` | konto under avslutning |
| `500` | internt fel |

---

## 5. Sessionshantering efter byte

- I v0.1 (enkel token utan refresh) **invalideras inte** befintliga tokens
  automatiskt vid lösenordsbyte. En redan utfärdad token fortsätter gälla till
  `exp` (7 dagar).
- Detta är en medveten förenkling. När vi inför refresh-tokens (senare) kan vi
  lägga till möjlighet att återkalla sessioner vid lösenordsbyte.

---

## 6. Klientflöde (rekommenderat)

1. Användaren anger nuvarande + nytt lösenord (med bekräftelse i UI).
2. Klienten skickar `POST /auth/password/change` med token.
3. Vid `200`: visa bekräftelse. Token behöver inte bytas ut i v0.1.
4. Vid `401` (fel nuvarande lösenord): visa fel utan att logga ut.

---

## 7. Uppskjutet

- Återkallande av befintliga sessioner vid lösenordsbyte (kräver refresh-tokens).

Se även: **glömt lösenord** (ej inloggad) är ett separat flöde, se
[glömt-lösenord-flödet](flow-forgot-password-v0.1.md).
