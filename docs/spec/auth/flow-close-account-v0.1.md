# Flöde: Avsluta konto (v0.1)

Detaljspec för att en inloggad användare avslutar sitt eget konto.
Bygger på [auth-tjänstens kontrakt](auth-service-contract-v0.1.md).

Endpoint: `DELETE /auth/account`

Modellen är **soft delete med grace period**, samma princip som the_app använder
i dag, men med identitet från token i stället för `profile_id`.

---

## 1. Syfte

Låta en användare avsluta sitt konto på ett återställbart sätt under en
grace-period, och därefter permanent radera kontot och tillhörande data.

Två faser:
1. **Avsluta (soft delete):** kontot markeras som under avslutning, känsliga
   uppgifter nollas direkt, en tidsgräns för permanent radering sätts.
2. **Permanent radering (purge):** ett bakgrundsjobb raderar kontot och dess
   data när grace-perioden passerats.

---

## 2. Indata

Kräver giltig token (`Authorization: Bearer <JWT>`).
Ingen body krävs. Identiteten tas från `sub` i token.

Valfri body för framtida bruk (t.ex. bekräftelse eller anledning):
```jsonc
{ "confirm": true }
```

---

## 3. Steg – fas 1: Avsluta (soft delete)

1. **Verifiera token.** Saknad/ogiltig → `401`.
2. **Hämta användaren** via `sub`. Saknas → `404`.
3. **demo_user-spärr:** om `content_blob.role = 'demo_user'` → `403`
   (demokontot kan inte avslutas). Se
   [roller och behörighet](roles-and-authorization-v0.1.md).
4. **Redan under avslutning?** (`phase = 'pending_deletion'`) → `200` idempotent,
   returnera samma `delete_after` som redan är satt.
5. I en databastransaktion:
   - Sätt `phase = 'pending_deletion'`.
   - **Nolla känsliga uppgifter** i `content_blob`: `credentials`, `email`,
     `phone` tas bort.
   - Sätt `content_blob.deletion`:
     ```jsonc
     {
       "requested_at": "<nu>",
       "delete_after": "<nu + grace-period>",
       "action": "delete_account_after_grace_period"
     }
     ```
   - Ersätt `name` med `deleted_user_<id-prefix>`.
   - Rensa profilbilder/media (`image_ref`, `icon_ref`, `media_refs`).
   - **Direkt radering** av användarens interaktionsdata: kommentarer
     (`item_comments`), verifieringar (`item_verifications`) och kort-tillstånd
     (`card_interaction_states`) kopplade till profilen.
   - **Barn-items** (`parent_id = profilen`, utom `Plats`/`Samling`) raderas.
   - **Ägt innehåll** (`subject IN ('Plats', 'Samling')`, ägt via `owner_id`,
     `content_blob.created_by` eller `content_blob.creator`) hanteras per item
     enligt regeln i avsnitt 3.1.
6. **Svar `200`** med `delete_after`.

### 3.1 Ägt innehåll: överför vs. radera (exakt regel från the_app)
För varje ägt `Plats`/`Samling`-item:
- **Har kvarvarande bidrag från andra** (t.ex. kommentarer/verifieringar) →
  **överförs till admin-kontot**: `owner_id` sätts till admin, bilder/ikoner
  nollas, `deletion.action = 'transferred_to_admin'`, `deletion.previous_owner_id`
  = den avslutande användaren.
- **Inga kvarvarande bidrag** → **markeras `pending_deletion`** med
  `deletion.action = 'delete_after_grace_period'` och samma `delete_after` som
  kontot; raderas av purge-jobbet.
I båda fallen nollas `image_ref`/`icon_ref` och media köas för radering.

**Admin-kontot** identifieras (i prioritetsordning) via `structure_id =
'ADMIN_USER'`, annars `name = 'admin'`, annars `content_blob.role =
'administrator'`.

**Grace-period:** **3 dagar** (`delete_after = nu + 3 dygn`) — verifierat mot
the_app:s nuvarande värde (`server.js`). Kan justeras senare, men matchar i dag.

---

## 4. Steg – fas 2: Permanent radering (purge)

Ett bakgrundsjobb (`purgeExpiredAccountDeletions`, motsvarande the_app) körs
**vid uppstart och därefter varje timme** och:
1. Hittar profiler med `phase = 'pending_deletion'` där `delete_after <= nu`.
2. Raderar tillhörande innehåll och sedan profilen i en transaktion.
3. Rensar tillhörande media.

Detta flöde har ingen HTTP-endpoint; det är en schemalagd serverside-uppgift.

---

## 5. Effekt på inloggning

- Så länge kontot är `pending_deletion` kan användaren **inte logga in**
  (`POST /auth/login` → `403`, se login-flödet).
- En redan utfärdad token slutar fungera i praktiken eftersom skyddade flöden
  (t.ex. byta lösenord) avvisar `pending_deletion`-konton med `403`.

---

## 6. Utdata

Lyckad avslutning `200`:
```jsonc
{
  "message": "Kontot är avslutat och väntar på permanent radering",
  "delete_after": "<tidsstämpel>"
}
```

Felsvar:
| Status | När |
|--------|-----|
| `401` | ogiltig token |
| `404` | användaren finns inte |
| `500` | internt fel |

---

## 7. Återställning under grace-period

- I v0.1 finns **ingen självbetjänings-återställning** av ett avslutat konto
  (känsliga uppgifter är redan nollade). Återställning, om det behövs, hanteras
  manuellt/administrativt innan `delete_after`.
- Ett riktigt "ångra avslutning"-flöde kan specas senare om det behövs.

---

## 8. Skillnad mot the_app i dag

- Identiteten kommer från **token (`sub`)**, inte ett `profile_id` i query som
  servern litar på. Admin-radering av andras konton beskrivs i
  [roller och behörighet §6](roles-and-authorization-v0.1.md).
- Övrig soft delete-logik (grace period, nolla uppgifter, purge-jobb) återanvänds
  från the_app för att inte bryta befintligt beteende.
