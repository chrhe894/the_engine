# Flöde: Glömt lösenord (återställning) (v0.1)

Detaljspec för att återställa ett lösenord **utan att vara inloggad**.
Bygger på [auth-tjänstens kontrakt](auth-service-contract-v0.1.md).

Endpoints:
- `POST /auth/password/forgot` – begär återställningskod
- `POST /auth/password/reset` – lös in kod och sätt nytt lösenord

> Detta ersätter the_app:s nuvarande glömt-lösenord, som är **klientdrivet/demo**
> (koden genereras i appen och visas i en Alert). Här görs allt serverside med
> en kod som aldrig lämnar servern annat än via e-post/SMS till användaren.

---

## 1. Syfte

Låta en användare som glömt sitt lösenord bevisa att den kontrollerar sin
registrerade e-post eller telefon, och därefter sätta ett nytt lösenord – utan
att flödet avslöjar om ett konto finns.

Tvåstegsflöde:
1. **Begär kod:** användaren anger användarnamn (eller e-post). Finns kontot
   skickas en engångskod till den registrerade kanalen.
2. **Lös in kod:** användaren anger koden + nytt lösenord. Vid giltig kod byts
   lösenordet.

---

## 2. Steg 1 – begär kod: `POST /auth/password/forgot`

### Indata
```jsonc
{
  "identifier": "…",              // användarnamn eller e-post
  "method": "email"               // "email" | "sms"
}
```

### Steg (serverside)
1. **Slå upp** konto via `identifier` (användarnamn eller e-post),
   `phase <> 'pending_deletion'`.
2. **Alltid samma svar** oavsett om kontot finns (se §5 om integritet).
3. Om kontot finns och har den begärda kanalen (e-post/telefon):
   - Generera en **engångskod serverside** (kryptografiskt slumpad, 6 siffror).
   - Spara en **hash** av koden (inte koden i klartext) tillsammans med:
     `user_id`, `expires_at` (10 min), `attempts = 0`, `method`.
   - **Skicka koden** via vald kanal (e-post/SMS) till den registrerade adressen.
     (Utskicksmekanismen är en infrastrukturdetalj; se §7.)
4. **Svar `200`** (alltid): "Om kontot finns har en kod skickats."

### Rate limiting
- Max **3 begärda koder** per konto per rullande timme.
- Minst **60 sekunder** mellan begäranden.
- En ny kod **ogiltigförklarar** tidigare kod för samma konto.

---

## 3. Steg 2 – lös in kod: `POST /auth/password/reset`

### Indata
```jsonc
{
  "identifier": "…",
  "code": "123456",
  "new_password": "…"
}
```

### Steg (serverside)
1. **Hämta aktiv återställningspost** för kontot. Saknas/utgången → `400`
   "Ogiltig eller utgången kod".
2. **Kontrollera utgångstid** (`expires_at`). Utgången → `400`.
3. **Verifiera koden** mot den sparade hashen.
   - Fel kod → öka `attempts`. Vid **5 felförsök** ogiltigförklaras posten och
     användaren måste begära ny kod. Svar `400`/`429` (se §6).
4. **Validera `new_password`** (minst 8 tecken). Annars `400`.
5. Vid giltig kod:
   - **Hasha nytt lösenord** (bcrypt) och uppdatera
     `content_blob.credentials.password_hash` (merge, bevara övriga fält).
   - **Förbruka koden** (radera/markera återställningsposten som använd).
6. **Svar `200`**: "Lösenordet har återställts."

---

## 4. Lagring av återställningskoder

Koder lagras **aldrig i klartext**. En separat lagring (tabell eller
`content_blob`-fält, beslut vid implementation) håller per aktiv begäran:

```jsonc
{
  "user_id": "…",
  "code_hash": "…",        // hash av engångskoden
  "method": "email",       // "email" | "sms"
  "expires_at": "<nu+10min>",
  "attempts": 0,
  "created_at": "<nu>"
}
```
- Endast **en** aktiv post per konto (ny begäran ersätter tidigare).
- Poster som är använda eller utgångna städas bort (kan piggybacka på purge-jobbet).

---

## 5. Integritet: avslöja aldrig om konto finns

- `POST /auth/password/forgot` returnerar **alltid** samma `200`-svar, oavsett om
  kontot finns eller om kanalen (e-post/telefon) är registrerad.
- Detta hindrar att flödet används för att kartlägga vilka användarnamn/e-post
  som finns.
- Motsvarande: `POST /auth/password/reset` skiljer inte i sitt felmeddelande på
  "okänt konto" och "fel kod" – båda ger samma generiska fel.

---

## 6. Felsvar

| Endpoint | Status | När |
|----------|--------|-----|
| forgot | `400` | saknad `identifier`/`method`, ogiltig `method` |
| forgot | `429` | för många begäranden (rate limit) |
| forgot | `200` | alltid annars (även om kontot inte finns) |
| reset | `400` | ogiltig/utgången kod, fel kod, ogiltigt nytt lösenord |
| reset | `429` | för många felförsök |
| reset | `200` | lyckad återställning |

---

## 7. Beroende: utskick av kod (e-post/SMS)

Att faktiskt skicka koden kräver en utskickskanal:
- **E-post:** en e-postleverantör (SMTP eller API-baserad tjänst).
- **SMS:** en SMS-leverantör.

Valet av leverantör är ett infrastrukturbeslut som tas vid implementation. Detta
är också skälet till att glömt-lösenord var uppskjutet: det kräver mer än bara
kod i tjänsten. Specen ovan är oberoende av vilken leverantör som väljs.

---

## 8. Klientflöde (rekommenderat)

1. Användaren väljer "Glömt lösenord", anger användarnamn/e-post och kanal.
2. Klienten anropar `POST /auth/password/forgot` och visar ett neutralt
   "Om kontot finns har en kod skickats".
3. Användaren anger koden + nytt lösenord.
4. Klienten anropar `POST /auth/password/reset`. Vid `200` → skicka till login.

---

## 9. Skillnad mot the_app i dag

| | the_app (nu) | Denna spec |
|-|--------------|-----------|
| Kodgenerering | i klienten (`Math.random`) | serverside, kryptografiskt slumpad |
| Kodvisning | i en Alert | skickas via e-post/SMS |
| Kodlagring | ingen (klienten håller den) | hash serverside, med utgångstid |
| Integritet | avslöjar om användaren finns | neutralt svar |
| Rate limiting | i klientens minne | serverside per konto |

---

## 10. Uppskjutet

- Val och integration av e-post-/SMS-leverantör (infrastruktur).
- Eventuell länkbaserad återställning (magisk länk) som alternativ till kod.
