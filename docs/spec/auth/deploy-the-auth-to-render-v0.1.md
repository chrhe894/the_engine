# Deploya the_auth till Render (v0.1)

Steg-för-steg för att köra auth-tjänsten som en egen Render-tjänst mot the_app:s
delade databas. Själva klicken i Render gör du; koden och konfigurationen är
förberedd (`the_auth/render.yaml`).

---

## Förutsättningar

- `the_auth` ligger i ett git-repo som Render kan nå (GitHub/GitLab). Om det inte
  redan är pushat: skapa ett repo och pusha `c:\repo\the_auth`.
- Du har the_app:s **delade databas**-URL (den riktiga, inte test-kopian).
  Hämtas i Render på databasens sida ("Internal Database URL" om auth-tjänsten
  ligger i samma Render-region/konto, annars "External Database URL").

---

## Alternativ 1: Blueprint (rekommenderat, konfig som kod)

1. I Render: **New +** → **Blueprint**.
2. Välj repot för `the_auth`. Render läser `render.yaml`.
3. Render skapar en web service `the-auth`. Vid prompten för hemligheter, fyll i:
   - `DATABASE_URL` = den delade databasens connection string
   - `JWT_SECRET` = ett långt slumpmässigt värde (se nedan)
4. Kontrollera att `region` i `render.yaml` matchar databasens region. Justera vid behov.
5. Deploya. När den är uppe, testa `https://<din-tjänst>.onrender.com/health`
   → ska ge `{"status":"ok"}`.

## Alternativ 2: Manuell Web Service

1. **New +** → **Web Service**, välj repot.
2. Inställningar:
   - Runtime: **Node**
   - Build command: `npm install`
   - Start command: `npm start`
   - Health check path: `/health`
   - Plan: minst **Starter** (betald, ingen cold start).
3. Lägg till miljövariabler:
   | Nyckel | Värde |
   |--------|-------|
   | `NODE_ENV` | `production` |
   | `DATABASE_URL` | delad databas connection string |
   | `DATABASE_SSL` | `true` |
   | `JWT_SECRET` | långt slumpmässigt värde |
   | `JWT_EXPIRES_IN` | `7d` |
   | `JWT_ISSUER` | `the_auth` |
4. Deploya och testa `/health`.

---

## Generera en JWT_SECRET

Ett långt slumpmässigt värde. T.ex. i en terminal:
```
node -e "console.log(require('crypto').randomBytes(48).toString('base64url'))"
```
Spara det säkert. **Samma** värde måste delas med varje tjänst som ska verifiera
token (i första hand the_engine).

---

## Viktigt om produktion

- **NODE_ENV=production** gör att tjänsten vägrar starta utan `JWT_SECRET`
  (medvetet skyddsnät) och att dev-sändaren för glömt-lösenord-koder vägrar
  "skicka" (kräver riktig e-post/SMS-leverantör innan det flödet används skarpt).
- Tjänsten skapar tabellen `auth_password_resets` vid uppstart. Övriga tabeller
  (`information_items` m.fl.) finns redan i the_app:s databas.
- Tjänsten rör **inte** the_app:s kod. Den läser/skriver bara delade
  `Användarprofil`-rader.

---

## Efter deploy

- Notera tjänstens URL (`https://the-auth-….onrender.com`). Den blir
  `AUTH_BASE_URL` som the_engine anropar.
- Nästa steg: bygg the_engine mot denna URL (login + JWT-verifiering).
