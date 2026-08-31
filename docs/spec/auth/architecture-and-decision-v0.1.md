# Delad identitet & inloggning – arkitektur och beslut (v0.1)

Detta dokument fastställer **hur the_app, the_engine och framtida appar ska dela
samma användare och inloggning**. Det är avsiktligt kortfattat och förklarande,
inte tungt tekniskt. Detaljspec per flöde (registrering, login, glömt lösenord,
avsluta konto) görs i separata dokument efter detta.

Relaterat: [the_app – nuvarande lösning](the-app-current-solution-v0.1.md)

---

## 1. Problemet vi löser

Flera appar ska dela samma användare:
- **the_app** (redan i drift, under App Store-granskning)
- **the_engine** (under uppbyggnad)
- **3–4 framtida appar** med samma informationsmodell

I dag har the_app ingen delbar inloggning: login returnerar bara profil-objektet,
och skyddade anrop "auktoriseras" genom ett `profile_id` som servern litar på.
Det finns ingen token som en annan app kan lita på. Alltså finns inget att
återanvända – vi måste införa en riktig, delbar mekanism.

---

## 2. Beslut

**Vi bygger en egen, central autentiseringstjänst (auth-tjänst) som alla appar
använder.** Den är source of truth för identitet och inloggning. Efter inloggning
delar den ut en **signerad token (JWT)** som varje app kan verifiera på egen hand.
Alla appar litar på samma tjänst.

Detta är standardmönstret (OAuth2 / OpenID Connect, "identity provider") för
just detta problem: många appar, en gemensam identitet.

### Varför detta och inte alternativen

- **Låta the_engine anropa the_app:s nuvarande endpoints:** går inte på ett säkert
  sätt – det finns ingen token att dela, och `profile_id`-tillit kan förfalskas.
- **Kopiera användare mellan databaser:** skapar två sanningar som glider isär.
- **Extern IdP (Auth0/Clerk/Keycloak):** robust men långsammare att komma igång med,
  kostar, och lägger användardata hos tredje part. Kan bli aktuellt senare – vår
  design gör ett sådant byte billigt eftersom apparna redan pratar "token-språket".

### Teknikval (rätt-nog och snabbt)

En **liten egen auth-tjänst** på samma stack som the_app redan kör:
Node/Express + Postgres + bcrypt + JWT. Du äger tjänsten och datan, den kan växa,
och den är byggd på sådant teamet redan kan.

---

## 3. Hur det hänger ihop

```
                 ┌───────────────────────────┐
                 │      Auth-tjänst           │
                 │  (identitet + login)       │
                 │  bcrypt · JWT · Postgres   │
                 └─────────────┬─────────────┘
                               │  användardata (source of truth)
                    ┌──────────┴──────────┐
                    │  Databas (Postgres) │  ← the_app:s befintliga DB
                    └─────────────────────┘
                               ▲
        signerad token (JWT)   │   signerad token (JWT)
        ┌──────────────────────┼──────────────────────┐
        │                      │                       │
   ┌────┴─────┐          ┌─────┴──────┐          ┌─────┴──────┐
   │  the_app │          │ the_engine │          │ framtida   │
   │          │          │            │          │ appar 3–4  │
   └──────────┘          └────────────┘          └────────────┘
```

Grundidé:
1. Användaren loggar in mot **auth-tjänsten**.
2. Auth-tjänsten verifierar lösenordet (bcrypt) och returnerar en **JWT**.
3. Appen skickar med JWT i efterföljande anrop. Varje app/tjänst kan **verifiera
   signaturen** utan att fråga auth-tjänsten varje gång.
4. Token säger "vem" på ett sätt som inte kan förfalskas – ersätter dagens
   `profile_id`-tillit.

---

## 4. Migreringsplan (skyddar App Store-granskningen)

Princip: **backend-först. Vi rör inte mobil-app-binären medan granskning pågår.**
Backend/API kan ändras fritt utan ny granskning; ny app-binär kräver ny granskning.

Steg:
1. **Behåll databasen som källa.** Auth-tjänsten läser/skriver samma Postgres
   och samma användarrepresentation (`Användarprofil`-items) som the_app redan använder.
2. **Extrahera auth-logiken** (registrering, login, lösenordshash, avsluta konto)
   ur `the_app/api-server/server.js` till den nya auth-tjänsten. the_app:s
   `/api/auth/login` m.fl. kan bakom kulisserna delegera dit – ingen ändring i appen.
3. **Bygg the_engine mot auth-tjänsten från start**, med JWT. the_engine ärver
   aldrig de svaga bitarna.
4. **Migrera the_app till JWT** som ett senare, medvetet steg (kräver ny app-binär →
   planeras när granskningen tillåter det).

---

## 5. Vad vi specar nu vs. skjuter upp

**Nu (för att komma framåt):**
- Auth-tjänstens ansvar och gränssnitt (endpoints/kontrakt).
- Token-modell (vad en JWT innehåller, hur den signeras och verifieras, giltighetstid).
- Registrering, login, avsluta konto – mot den nya tjänsten.
- Hur the_engine använder tjänsten.

**Designat men uppskjutet (för fartens skull):**
- Riktigt serverside **glömt lösenord** med kod via e-post/SMS (dagens är demo/klientdrivet).
- Full **e-post-/telefonverifiering** (i dag finns bara unikhetskontroll).
- **Migrering bort från legacy plaintext-lösenord** (login stöder dem fortfarande).
- **the_app:s mobil-binär** flyttas till JWT (väntar på App Store-läget).

---

## 6. Öppna frågor att besluta i nästa steg

1. **Var körs auth-tjänsten?** Egen deploy bredvid the_app:s API, eller i samma repo till att börja med?
2. **Token-livslängd och förnyelse:** kort access-token + refresh-token, eller enklare modell först?
3. **Nyckelhantering:** delad hemlig nyckel (HS256) för start vs. nyckelpar (RS256) för renare separation mellan tjänster.
4. **Hur the_engine identifierar sig** mot auth-tjänsten (klient-id/hemlighet eller enklare i början).

> Nästa dokument: kontrakt för auth-tjänsten (endpoints + token-modell), följt av
> per-flödes-spec för registrering, login och avsluta konto.
