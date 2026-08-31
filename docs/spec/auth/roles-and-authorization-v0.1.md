# Roller och behörighet (v0.1)

Definierar användarrollerna och vad varje roll får göra i auth-tjänsten och de
appar som använder den. Bygger på [auth-tjänstens kontrakt](auth-service-contract-v0.1.md).

Relaterat: [the_app – nuvarande lösning](the-app-current-solution-v0.1.md),
[avsluta konto](flow-close-account-v0.1.md)

---

## 1. Roller

Tre roller i v0.1:

| Roll | Syfte |
|------|-------|
| `admin` | Administratör. Full behörighet: hantera andra konton och innehåll. |
| `user` | Vanlig användare. Standard för alla nya konton. Äger och hanterar sitt eget. |
| `demo_user` | Demo-/gästkonto för att prova appen utan att registrera sig. Begränsat. |

Rollen lagras i `content_blob.role` på användarens `Användarprofil`-item:
```jsonc
{ "content_blob": { "role": "user" } }   // "admin" | "user" | "demo_user"
```

**Standard:** ett nytt konto får `role = 'user'` om inget annat anges vid registrering.

---

## 2. Bakåtkompatibilitet med the_app

the_app avgör i dag admin så här (`isAdminFromProfile` i `server.js`):
- `content_blob.role === 'administrator'`, **eller**
- `content_blob.capabilities` innehåller `manage_channels` eller `system_admin`

För att inte bryta the_app behandlar auth-tjänsten **både** det gamla och det nya
som admin. En användare räknas som `admin` om något av följande gäller:
- `content_blob.role === 'admin'` (ny form), **eller**
- `content_blob.role === 'administrator'` (the_app:s nuvarande form), **eller**
- `content_blob.capabilities` innehåller `manage_channels` eller `system_admin`

`demo_user` identifieras av `content_blob.role === 'demo_user'`. the_app använder
i dag ett konto med namnet `demo_user` som standardprofil; det kontot bör få
`role = 'demo_user'` satt (en engångsuppdatering, backend-only).

> Not: `administrator` behålls som synonym under en migreringsperiod. Nya konton
> skrivs med `admin`. En städning som normaliserar gamla värden är en uppskjuten
> backlog-punkt.

---

## 3. Behörighet per åtgärd

| Åtgärd | `admin` | `user` | `demo_user` |
|--------|:------:|:------:|:-----------:|
| Registrera konto | – | – | – (öppet, ingen roll krävs) |
| Logga in | ✔ | ✔ | ✔ |
| Se/ändra **egen** profil | ✔ | ✔ | ✖ |
| Byta **eget** lösenord | ✔ | ✔ | ✖ |
| Avsluta **eget** konto | ✔ | ✔ | ✖ |
| Skapa/äga innehåll | ✔ | ✔ | ✖ (endast läsa) |
| Ändra/radera **andras** konton | ✔ | ✖ | ✖ |
| Ändra/radera **andras** innehåll | ✔ | ✖ | ✖ |
| Hantera kanaler / systeminställningar | ✔ | ✖ | ✖ |

Principer:
- **`user`** får göra allt med sitt eget, inget med andras.
- **`admin`** får göra allt, inklusive andras konton och innehåll.
- **`demo_user`** är i praktiken skrivskyddat: kan logga in och titta, men inte
  skapa innehåll, ändra profil, byta lösenord eller avsluta konto. Detta skyddar
  demokontot från att förändras av olika besökare.

---

## 4. Hur behörighet avgörs (serverside)

1. Identiteten kommer från **token `sub`** (aldrig från `profile_id` i request).
2. Tjänsten läser användarens roll från `content_blob.role` (med
   bakåtkompatibiliteten i avsnitt 2).
3. **Ägarskap:** en `user` får ändra en resurs om resursen ägs av `sub`
   (profilens id matchar, eller innehållets `owner_id`/`created_by`/`creator`).
4. **Admin-override:** en `admin` passerar ägarkontrollen och får ändra vad som helst.
5. **demo_user-spärr:** skrivande åtgärder avvisas för `demo_user` innan
   ägarkontroll ens görs.

Felkoder:
- Saknad/ogiltig token → `401`.
- Giltig token men otillräcklig roll/ägarskap → `403`.

---

## 5. Rollen i token?

Rollen läggs **inte** som en auktoritativ claim i token i v0.1. Skälet: roller
kan ändras, och en token lever i 7 dagar. Tjänsten slår upp aktuell roll från
databasen vid varje skyddad åtgärd, så en nedgraderad admin tappar behörighet
direkt i stället för att behålla den tills token går ut.

(När refresh-tokens införs kan rollen cachas kortlivat i access-token för
prestanda. Uppskjutet.)

---

## 6. Admin-åtgärder mot andra konton

Detta preciserar den öppna punkten i [avsluta-konto §8](flow-close-account-v0.1.md).

- **Avsluta annans konto:** `admin` kan avsluta ett annat konto. Samma soft
  delete-flöde som self-delete (3 dagars grace, purge-jobb), men målets id anges
  av admin och admin-behörighet krävs.
- **Endpoint (förslag):** `DELETE /auth/admin/accounts/:id` (kräver admin-token),
  separat från `DELETE /auth/account` (eget konto).
- En `user` som försöker avsluta annans konto → `403`.

---

## 7. Regler och skydd

- **`admin` kan inte avsluta sitt eget sista admin-konto** utan att en annan
  admin finns (skydd mot att låsa ut all administration). Kontrolleras serverside.
- **Rolländring** (t.ex. göra någon till admin) är i sig en admin-åtgärd och
  loggas. Endpoint specas vid behov.
- `admin`-användarnamnet `admin` är reserverat vid registrering (se
  [registreringsflödet](flow-registration-v0.1.md)); rollen `admin` sätts inte
  automatiskt av registrering.

---

## 8. Uppskjutet

- Normalisera `administrator` → `admin` i databasen (migrering).
- Endpoint för att sätta/ändra roll (`admin`-only) med revisionslogg.
- Finare behörigheter (capabilities) om enkla roller inte räcker.
- Roll cachad i access-token när refresh-tokens finns.
