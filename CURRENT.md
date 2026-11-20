# Current focus

## Shared identity & authentication (active)
Central auth service so the_app, the_engine and future apps share the same users.
See `docs/spec/auth/` and decision D-001 in `DECISIONS.md`.

Done:
[x] Reference doc of the_app's current auth solution
[x] Architecture & decision (central auth service + JWT)
[x] Auth service contract (endpoints + token model)
[x] Locked v0.1 defaults in contract §7
[x] Per-flow spec: registration
[x] Per-flow spec: login
[x] Per-flow spec: change password
[x] Per-flow spec: close account

[x] Precise close-account rules verified against the_app (3-day grace,
    hourly purge, transfer-vs-delete of owned Plats/Samling content)
[x] Consistency review of contract + four flow specs
[x] Roles & authorization spec (admin / user / demo_user)
[x] Forgot-password spec (server-side code via email/SMS)

Decisions:
- Deploy: /auth/* routes in the_app's existing Render service (gsis-api),
  sharing its Postgres DB and env vars (JWT_SECRET). Separate service later.
- Email/phone verification deferred until we build around it (may need a paid
  provider). Forgot-password needs an email/SMS provider too.

Build (in progress) — separate service at c:\repo\the_auth:
[x] Project skeleton (Express + pg + bcrypt + jsonwebtoken + env config)
[x] DB data layer for Användarprofil items (shared with the_app)
[x] JWT issue/verify + requireAuth middleware
[x] POST /auth/register, /auth/login, GET /auth/check, GET /auth/me
[x] POST /auth/password/change, DELETE /auth/account (soft delete + grace)
[x] POST /auth/password/forgot + /reset (dev sender logs code; provider deferred)
[x] Hourly purge job + auth_password_resets table bootstrap
[x] End-to-end logic verified against in-memory DB fake (16/17; the 1 is a
    fake limitation — closed accounts are anonymized so login gives 401 not 403,
    now noted in the login spec)

Real DB test: separate empty test DB on Render (option 2).
[x] Fixed register INSERT to satisfy information_items NOT NULL columns
    (location/time/scope/intent) — would have failed against the real schema
[x] scripts/init-test-schema.sql (incl. auth_password_resets)
[x] scripts/verify-against-db.js (full flow over real HTTP + DB, self-cleaning)
[x] VERIFIED: 12/12 pass against real Render Postgres

the_auth service is complete and verified for v0.1.

Deploy the_auth to Render (chosen: paid service already provisioned):
[x] render.yaml blueprint (starter plan, /health check, secrets sync:false)
[x] engines.node >=20 pinned; production fails fast without JWT_SECRET (verified)
[x] Deploy guide: docs/spec/auth/deploy-the-auth-to-render-v0.1.md
[x] Pushed to github.com/chrhe894/the_auth (main)
[x] Deployed to Render (free tier for now — spins down when idle; upgrade later);
    /health returns {"status":"ok"} against the shared DB
[x] AUTH_BASE_URL = https://the-auth.onrender.com (verified /auth/check reads shared DB)
[ ] Later: upgrade the_auth web service off free tier to avoid cold starts

the_engine integration (spec: docs/spec/auth/engine-integration-v0.1.md):
[x] Step 1 — login gate: auth_client.py + Flask session + /login /logout,
    before_request guard, login page, user bar. Verified end-to-end against
    live the_auth (login, session, logout). the_engine is Python/Flask.

[x] Step 2 — cases per user: owner_id on CaseFile, /cases landing (my cases;
    admin sees all), create/open/delete, before_request loads selected case.
    Verified: owner stamped, ownership isolation (user2 can't see/open user1's
    case), admin-only delete. Known limit: global `case` var = single-user only.

Admin utilities in the_auth (used against the real shared DB):
[x] scripts/set-password.js (hidden prompt, bcrypt, one account)
[x] scripts/set-role.js (admin|user|demo_user, one account)
[x] chrhe894 password set + role=admin; verified admin mode in the_engine
    (sees all cases, "Ta bort" button works). Role is read at login, so
    role changes require a re-login.

Next:
[ ] Step 3 — admin tools (templates for routes/challenges, bulk clear cases)
[ ] (If engine ever multi-user concurrent) move `case` off module global

---

## Skolan-caset / konceptträd (konceptläge, redigering och deep mode byggda)
Bakgrund och resonemang: `LAST_SESSION.md` (avsnitt 2-10).
Metod: en mening in, fyra punkter ut, ägaren väljer, upprepas. Konceptläge är
det som gav koncept; dagens `suggest` ger uppgifter.

Att realisera:
[x] Konceptläge: egen prompt/funktion som tar lägesuppfattning + idealtillstånd
    + vald mening och ger 4 punkter (separat från `suggest`).
    Byggt: `src/engine_concepts.py`, `ConceptNode` i `case_file.py`, routes
    `/concepts/...` i `web.py`, knapp "Koncept (fyra punkter)" i målvyn.
    Verifierat mot fejkad AI (routes, redigering, parkering, gamla ärenden
    laddas) och en riktig körning (generate + deep med 3 linser). Ej gjort:
    jämförelse av kvalitet mot de gamla experimenten.
    BESLUT: en nod = namn + ren, redigerbar text. Inga fasta fält i lagringen.
    Prompten ber fortfarande modellen ta med vilken funktion i dagens skola
    punkten ersätter/bevarar, hur den möter idealtillståndet och största risk
    (det var det som gav djupet), men svaret sparas och redigeras som text.
    Fält extraheras först när en vy behöver dem (t.ex. täckningsvyn), på begäran.
    Ej testat om fri text ger samma djup som de fem fälten; jämför vid bygget.
[x] Per nod: välja *dela upp* eller *variera* (två knappar, och ett val i deep mode).
[x] Redigera varje punkt (namn + text), lägga till egen, välja, **parkera** och
    ta tillbaka. Gamla texten sparas i historiken. "Dela" = öppna punkten och dela
    upp den. "Byta ut" = parkera + lägg till egen. EJ byggt: slå ihop två punkter.
[x] Knapp "Deep mode" när de fyra har kommit fram: 1-5 körningar (förval 4), var
    och en genom en egen lins, körs parallellt. Modellen grupperar punkter som säger
    samma sak; stabil/variant räknas i kod (minst ca 60 % av linserna, aldrig under 2).
    Redan valda punkter som återfinns markeras i stället för att dupliceras.
    Ägaren väljer bland kandidaterna. EJ byggt: att AI varierar indatan mellan
    körningarna (bara linsen skiljer dem åt). Kvaliteten på grupperingen är inte
    utvärderad.
[x] Linsbibliotek (hypotes, ej testat; i `engine_concepts.py`): koncept, mål/resultat, filosofisk,
    byggare, den berörde, systemtänkare, regelverk/resurser, kritiker/provokatör.
    Lins = hur indatan läses; läge = vilken sorts utdata.
[ ] Täckningsvy: vilka idealtillstånd ingen nod möter, vilka linser som inte
    använts, återkommande risker över grenar.
[x] Lagring: `CaseFile.concepts` med standardvärde; gamla ärenden laddas
    (verifierat mot `cases/6d41beab.json`). Versionsnyckel finns inte än, och
    `ConceptNode(**c)` är strikt, så nya fält kräver samma försiktighet som övriga.
[x] Mänsklig kontroll: motorn föreslår, ägaren bestämmer. Prompten förbjuder
    påhittade belägg och order; sidan visar en notis om att allt är antaganden.
[ ] Integritet: notis finns vid textrutorna, men ingen teknisk spärr. Skicka bara
    sammanfattade punkter till AI-tjänsten, inte berättelser.

[x] Ny första sida (ersätter "Vad jobbar vi med?"): två frågor på vanlig svenska
    ("Hur ser det ut idag?" / "Hur vill du att det ska vara?", ordet
    lägesuppfattning/idealtillstånd bara som liten etikett), sedan antingen
    "Visa möjliga riktningar" (4 förslag) eller "Kör deep mode direkt". Ett dolt
    rotmål (`context.root_goal_id`) bär förslagen; målvyn syns inte för sådana
    case. Äldre case med mål behåller översikten. Den gamla `/start`-vägen finns
    kvar i koden men nås inte från sidan. Verifierat med fejkad AI och en
    riktig körning (18 s, fyra förslag). Ej provat i riktig webbläsare.
[x] Bandit-flödet: förslagen är fyra platser. *Behåll*/*Släpp* (ACTIVE/CANDIDATE),
    *Lägg undan*/*Ta tillbaka* (PARKED), *Dela upp* per förslag (öppnar och delar
    upp direkt; förslaget behålls), *Kör om de andra* (ersätter öppna platser, en
    slumpad lins per omkörning som inte upprepar förra, ersatta förslag läggs undan
    och listas för modellen så de inte upprepas). Redigering ändrar inte status:
    bara *Behåll* gör ett förslag behållet (Dela upp och Variera behåller fortfarande
    förslaget de körs på, så att det inte byts ut under arbetet).
    Deep mode har inget radioval längre: variera på första nivån, dela upp under en
    punkt. Linsen visas som liten etikett ("genom: …"). Verifierat med fejkad AI
    (34 kontroller) och en riktig körning (behåll 1, kör om 3 genom "Den berörde").
    Samma tre statusvärden som förut, så inga case behöver migreras.
[x] Varians (deep mode + Variera). Mätt mot riktig AI i ditt case: den gamla deep
    mode gav 16 punkter -> 5 grupper, 4 av dem fanns redan, 1 ny (dela upp
    konvergerar, linsen är för svag, körningarna vet inget om vad som finns). Nu
    visas det som finns (titel + början av texten, högst 12) och varje körning ska
    skilja sig i *mekanism* längs namngivna axlar (vem bestämmer, var/när, hur
    organiserat, vilka och vilka roller, hur framsteg visas, vad som bär kostnaden).
    Deep mode använder alltid "variera", på alla nivåer, med valfri egen vinkel.
    Per förslag finns *Variera* (fyra varianter, samma avsikt, annan mekanism,
    valfri vinkel; förslaget behålls; varianterna märks "variant av: …").
    Första omgången i ett case behåller det mjuka formuläget (ingen "mekanism"-
    instruktion när inget finns). Ny mätning: 16 punkter -> 8 nya, 0 fanns redan
    (4 linser), Variera gav fyra tydligt olika mekanismer.
    Reservation: bara titlar och början av texter lästa. Variansen kostar viss
    närhet till föräldern. Kvaliteten är inte utvärderad.
[x] Läsbarhet: varje förslag skrivs som två stycken (kärnan först, sedan varifrån den
    kommer, hur den möter idealet, funktion och risk). Modellen får två fält
    (core/reasoning) som sparas som en ren text med tom rad emellan. Mätt: 16/16
    (en enda fält gav bara 12/16, ibland utan kärnan). JSON-tolkningen tål nu
    radbrytning inuti strängar.
[x] Förstärk + Spikad + trädvy (byggt).
    *Förstärk* per förslag (valfri riktning): ger ett utkast med konkretare text och
    ett förslag på de fyra spikdelarna. Inget ändras förrän ägaren trycker *Använd*
    (gamla texten sparas i historiken) eller *Släng*. Är förslaget för övergripande
    lämnar motorn spikdelarna tomma och säger att det behöver delas upp först
    (mätt: ett övergripande förslag fick tomt, ett förslag på tredje nivån fick alla
    fyra delar ifyllda).
    *Spikad* = mål i en mening, hur vi ser att det är nått, vem som gör det, första
    aktivitet. Alla fyra krävs. Spikat förslag behålls automatiskt, överlever
    *Kör om*, och har inte längre Dela upp/Variera/Släpp. Ta bort spikning behåller
    texten. Spikdelarna lagras som fyra korta fält (`ConceptNode.spec`): avvikelse
    från "ren text", motiverad av att de ska kunna bli en Mission senare.
    *Visa trädet*: översikt med indrag, behållna/öppna/spikade, n/4 per punkt,
    de fyra delarna för spikade, undanlagda räknas men visas inte.
    Verifierat med fejkad AI (36 kontroller) och riktiga körningar. JSON-tolkningen
    tål nu avslutande kommatecken (en riktig körning föll på det).
[x] Deep mode, gruppering (efter Projekt 13): grupperingssteget föll en gång och gav
    16 ogrupperade förslag. Kunde inte återskapas (0 fel på 8+3 körningar med samma
    data). Misstanke: dolda resonemangstokens (mätt 500-1450) mot en gräns på 2000.
    Åtgärder: gräns 6000, ett omförsök, felet (typ, finish_reason, försök) visas i
    meddelandet och skrivs som `deep_group_failed` i case-filens historik, och utan
    gruppering sätts ingen stabil/variant-etikett. Nästa fel går alltså att läsa ur
    case-filen. Obs: även när grupperingen lyckas ger tvingad variation ca 14 nya av
    16 punkter, så "många förslag" är delvis avsiktligt. Öppen fråga: begränsa/rangordna
    (t.ex. visa 6 och lägg resten undan, eller gruppera på tema).
[x] Deep mode samlas i fyra teman (Christers val 2 + 3): varje lins ger 2 punkter
    (inte 4), modellen samlar dem i exakt 4 teman (färre bara om det finns färre
    punkter), ett förslag per tema visas, övriga punkter i temat läggs undan med
    "variant av" och temanamn, och punkter från teman över gränsen sparas undanlagda.
    Stabil/variant räknas per tema (hur många linser temat finns i). "Hittad igen"
    mot befintliga punkter är borttagen i deep mode: körningarna får redan se vad som
    finns. Mätt (riktig AI, kopia av Projekt 13): 8 punkter -> 4 teman, 2 av 2 körningar;
    en tidigare variant utan "exakt 4" gav bara 3. Observera att två teman kan ligga
    nära varandra när fyra tvingas fram (t.ex. två om interna prognosmarknader).
    Tokenåtgång för en deep-körning med fyra linser: ca 20 000 in och 5 400 ut
    (varav 2 700 resonemang), 5 anrop, ca 20 s.
[x] *Samla i teman* för förslag som redan finns: när de öppna förslagen på en nivå är fler
    än de lediga platserna (4 minus behållna) sorterar knappen dem i lika många teman,
    behåller ett förslag per tema öppet och lägger resten undan med tema och "variant av".
    Inget tas bort; misslyckas grupperingen ändras ingenting. Provat på en kopia av Projekt 13:
    15 öppna -> 4 teman, 11 undanlagda.
[x] Loggning: `src/app_log.py`. Fil `logs/engine.log` (roterar vid 1 MB, 5 gamla sparas, i
    .gitignore) plus konsolen. Loggas: varje AI-anrop (syfte, tid, token in/ut/resonemang,
    finish_reason, fel), varje webbanrop (metod, sökväg, status, tid, användar-id, case-id)
    och ohanterade fel med traceback. Loggas INTE: prompts, svar, texter eller formulärinnehåll.
    Miljövariabler: LOG_LEVEL, ENGINE_LOG_DIR. Äldre `print`-felmeddelanden i AI-lagret och
    Observer går nu till loggen. CLI och run-skripten är orörda.
[x] Startlista (byggd): *Samla startlista* på trädsidan läser BÅDA texterna (lägesuppfattning
    och önskat läge) plus alla behållna punkter och föreslår konkreta handlingar i två lager:
    *Grund* (vad som måste göras för att alls kunna börja; kommer ur de två texterna, inte ur
    noderna, och måste efterfrågas uttryckligen) och *Från punkterna* (gemensamma förutsättningar
    i beroendeordning). En handling markeras först. Ägaren godkänner (blir ett uppdrag med
    "klart när" under det dolda rotmålet, "Gör nu"), redigerar, tar bort eller tar tillbaka;
    *Markera klart* sparar resultatet som observation (current_situation rörs inte). Ny insamling
    ersätter bara obeslutade förslag (läggs undan, inte raderas); godkända ligger kvar och skickas
    med så de inte föreslås igen. Punkter utan görbar handling listas ("dela upp mer").
    *Pingen* är en banner utan AI-anrop: visas när en behållen punkt på nivå 2+ har alla fyra
    spikdelar och ingen lista finns; AI-anropet görs först vid knapptryck.
    Verifierat: 42 kontroller med fejkad AI och två riktiga körningar på en kopia av Projekt 13
    (19-29 s, ca 3 400 tokens in, 2 000-2 700 ut). Båda körningarna lade projektuppsättning
    (Python-projekt, syntetisk testomgång) som grund och gemensamma "definiera X" som nästa lager,
    men olika sak som första handling (avgränsa prototypen resp. skapa Pythonprojektet).
    OBS: "ingen görbar handling"-signalen har inte kunnat prövas, eftersom modellen lät alla
    åtta punkter få en handling i båda körningarna. Inget uttryckligt repo/versionshantering
    nämndes. Stegen efter grunden är fortfarande designartefakter.
[x] Slutprodukt (byggt): motorn tolkar vad ägaren siktar mot ur de två texterna och visar det överst
    på förslags- och trädsidan: *Siktar mot* (vad som finns när det är nått), *Kan framställas
    härifrån* (kod, dokument, plan ...), art, skala (liten/medel/stor), säkerhet, andra tolkningar
    och vid behov EN fråga (obligatorisk vid låg säkerhet eller när tolkningarna skiljer sig i art).
    Sparas i `context["product"]`. Ägaren kan ändra den (källa "owner", ingen fråga mer), svara på
    frågan (tolkas om med svaret) eller trycka *Tolka om*. Den följer med i ALLA senare prompts
    (Variera, Förstärk, Dela upp, Kör om, deep mode, startlista). Vid nytt case körs tolkningen
    parallellt med de första fyra förslagen, som därför görs utan den; äldre case får den första
    gången den behövs. Misslyckas den blockeras inget. Är saken *liten* visas en banner om att gå
    direkt till startlistan, och startlistan fungerar då utan behållna punkter.
    Verifierat: 33 kontroller med fejkad AI och riktiga körningar (cykelstället: liten, fråga,
    startlista på 7 s med två konkreta handlingar; "må bättre": låg säkerhet + fråga; Projekt 13:
    mjukvara, hög säkerhet). Ej gjort: tolkningen uppdateras inte om ägaren ändrar texterna efteråt
    (tryck *Tolka om*), alternativen går inte att klicka på, och säkerheten är modellens egen
    bedömning (samma text gav "hög" i ett prov och "medel" + fråga i ett annat).
[ ] Startlista, kvar: koppla färdiga uppdrag till nästa förslag (observation -> ny insamling),
    välja en gren, och en regel som avgör när en nod är för övergripande.
[ ] Täckningsvy: hur många av de tio idealpunkterna de behållna/spikade punkterna
    möter. Inte påbörjat.
[ ] Etiketter: ordförrådet (mål, uppdrag, punkt, förslag) ska växa fram ur
    förslagen i stället för att styras uppifrån. Inte påbörjat.

Öppet innan eller vid sidan av:
[ ] Köra nivåidén ("nivåer med kvitto") som koncept i motorn.
[ ] Linstest på pakt-punkten för att se om linser ger olika svar.
[ ] Vilken är öppningsfrågan? (läge + önskan + perspektiv, se LAST_SESSION §9)
[ ] Begreppet "identitet" -> "lägesuppfattning" i det användaren ser?

Kända fel i motorn (ej åtgärdade, se LAST_SESSION §6): Observer kraschar utan
API-nyckel (`_generate_intervention` anropar `_fallback_intervention` med fel
argument), GIVE UP i webben saknar omprövning, strikt laddning bryter gamla
ärenden, inga tester för web/Observer/spara-ladda.

---

# Model work (parallel track)

[ ] Reality / Model Assessment
[ ] Phase 1/2 DoD
[ ] Golden Case — Immigrant
[ ] Golden Case — Skördefest
[ ] Primitive-concept check
[ ] Information Model cleanup
[ ] Transition ↔ Mission ↔ DoD
[ ] Model v0.1
              │
              ▼
       Prototype specification
              │
              ▼
          BUILD IT