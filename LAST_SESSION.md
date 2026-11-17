# LAST_SESSION — skolan-caset (hemmasittare) och motorns nästa nivå

Sammanfattning av sessionen så att tråden inte tappas. Skriven på svenska.
Inget i motorns kod ändrades under sessionen. Fyra experiment kördes mot motorns
AI via tillfälliga skript som togs bort igen (se avsnitt 4 och 10). Avsnitt 9 och
10 är tillägg från senare i samma session.

---

## 1. Mål med sessionen

Se om motorn kan ta emot en **lägesuppfattning** (idag kallad "identitet") sedd
ur ett perspektiv, och ett **idealtillstånd**, och sedan föreslå en väg framåt
med konkreta förslag, delmål och milstolpar. Aldrig order eller "skärp dig".

Ägaren av processen i skolan-caset är Christer, som vill blogga om processen.
Det är ett **tankeexperiment**, inte ett arbete med riktiga barn.

---

## 2. Skolan-caset

### Frågan
Vi har ett "problem" med hemmasittare. Tankeexperiment: alla hemmasittare får
en helt ny skola. Slutmålet är att alla som gått i skolan upp till 9 eller 12
år uppfyller både en form av **fostran** och **kunskapsnivåer motsvarande
dagens skola, eller bättre**. **Full frihet** från allt dagens skola erbjuder:
klassrum, lektioner, lärare, schema, närvaroplikt, betyg, nationella prov.

### Underlaget (sammanfattat från ca 200 berättelser, elevperspektiv, föräldrar med)

Lägesuppfattning:

| # | Attribut | Vad vi undersöker |
|---|---|---|
| 1 | Överbelastning | Ljud, människor, intryck och miljö blir för mycket. |
| 2 | Brist på trygghet | Eleven känner oro, stress eller rädsla inför skoldagen. |
| 3 | Brist på tillhörighet | Eleven upplever sig inte passa in i gruppen eller skolans sammanhang. |
| 4 | Att inte bli sedd | Elevens signaler, behov och svårigheter uppmärksammas inte. |
| 5 | Bristande inflytande | Eleven har liten möjlighet att påverka sin situation eller sitt arbetssätt. |
| 6 | Felaktiga förväntningar | Samma krav och arbetssätt används trots olika förutsättningar. |
| 7 | Brist på begriplighet | Det är oklart vad eleven ska göra, hur eller varför. |
| 8 | Förlorad motivation | Skolarbetet upplevs som meningslöst, ointressant eller omöjligt. |
| 9 | Upplevelse av misslyckande | Eleven får återkommande erfarenheter av att inte räcka till. |
| 10 | Förlorad framtidstro | Skolan leder till uppgivenhet, frånvaro eller känslan av att framtiden stängs. |

Idealtillstånd:

| # | Attribut | Vad det innebär |
|---|---|---|
| 1 | Trygghet | Jag känner mig trygg och behöver inte kämpa för att orka vara här. |
| 2 | Tillhörighet | Jag har en självklar plats och är accepterad som jag är. |
| 3 | Individuell anpassning | Skolan fungerar med mina förutsättningar, inte tvärtom. |
| 4 | Meningsfullhet | Jag förstår varför jag lär mig något och vad jag kan använda det till. |
| 5 | Nyfikenhet | Jag får utforska sådant som väcker mitt intresse. |
| 6 | Utveckling | Jag får utmaningar som hjälper mig att växa, oavsett var jag börjar. |
| 7 | Självbestämmande | Jag har inflytande över hur jag lär mig och kan påverka min väg. |
| 8 | Begriplighet | Jag förstår målet, nästa steg och vad som förväntas av mig. |
| 9 | Framsteg och självtillit | Jag får uppleva att jag kan, lyckas och komma vidare. |
| 10 | Framtidstro | Jag ser möjligheter och kan föreställa mig en framtid som känns värdefull. |

### Iakttagelse 1: listorna är två ändar av samma dimensioner
Åtta par är nästan spegelbilder (låg ände = lägesuppfattning, hög ände = ideal):

| Dimension | Lägesuppfattning | Ideal |
|---|---|---|
| Trygghet | 2 | 1 |
| Tillhörighet | 3 | 2 |
| Anpassning | 6 | 3 |
| Meningsfullhet | 8 | 4 |
| Självbestämmande | 5 | 7 |
| Begriplighet | 7 | 8 |
| Framsteg/självtillit | 9 | 9 |
| Framtidstro | 10 | 10 |

Fyra är **ensidiga**: lägesuppfattning 1 Överbelastning och 4 Att inte bli sedd
saknar uttryckt ideal. Ideal 5 Nyfikenhet och 6 Utveckling saknar beskrivet
nuläge. Motorn kan föreslå den saknade änden; ägaren godkänner.

### Iakttagelse 2: problem att lösa i datan
- **Olika röst:** lägesuppfattningen är tredje person ("Eleven känner…"), idealet
  är första person ("Jag känner…"). Om sessionen är elevperspektiv bör båda
  sidor ha samma röst, eller så märks perspektivet tydligt.
- **Bara brister:** lägesuppfattningen beskriver bara underskott. Behövs även
  "vad fungerar redan" (undantag, resurser), annars föreslås bara reparationer.
- **Många steg gäller inte eleven:** anpassning, förväntningar och överbelastning
  ligger mest hos skola och hem. Ett steg behöver en **aktör** (elev, förälder,
  skola, annan), annars hamnar allt på eleven.
- **Sammanfattningar, inte fakta:** spara att de är tolkningar från 200
  berättelser och att nya berättelser kan ändra dem.
- **Integritet:** de tio sammanfattade punkterna kan skickas till AI-tjänsten,
  men inte själva berättelserna eller något som identifierar någon, utan en
  medveten bedömning.

### Idérymden som modellen saknar för nydesign
Strukturella luckor i modellen:
1. **Lösningsrymd, inte bara väg:** motorn föreslår steg från ett nuläge. Här
   ska hela alternativ (**koncept**) designas och jämföras.
2. **Golv vid sidan av mål:** "minst lika bra kunskap och fostran som idag" är
   ett minimikrav, inte en önskad position. Paradox: hur visar man att golvet
   nås när betyg och prov är borta?
3. **Dolda funktioner i dagens skola:** barnpassning, skolmåltid, skyddsnät
   (kurator, skolsköterska, att någon märker om ett barn far illa), likvärdig
   tillgång, sortering till nästa steg, intyg som andra system litar på. Frihet
   från **form**, men varje **funktion** måste bevaras, ersättas eller avskaffas.
4. **Spänningar mellan dimensioner:** frihet/struktur, tillhörighet/möte med
   olika människor, individuell anpassning/likvärdighet, frihet/skydd.
5. **Flera parter med olika ideal:** elev, förälder, samhälle, stat.
6. **Avstängda restriktioner:** lagar, ekonomi, vuxnas tid sätts ur spel i
   experimentet och kan slås på en i taget.
7. **Hypoteser utan verklig återkoppling:** allt är "antaget" tills det prövats.
   Koden har redan observationskällan `simulated`.
8. **Livsfaser:** samma dimension betyder olika saker vid 6, 12 och 17 år.

Dimensioner som saknas i dina listor (förslag att pröva):
kunskap och kompetens; fostran och socialt samspel; relationer och tillit till
vuxna; kropp, vila och rytm; kontakt med riktiga sammanhang; likvärdighet;
skydd och tillsyn; återhämtning (många hemmasittare har redan tagit skada).

### Ide att pröva: nivåer i stället för betyg ("levels, inte labels")
Inget bedömande betyg. Eleven får **kvitto** på att en viss nivå är klarad (t.ex.
i matte), som på universitet, med möjlighet att tenta om många gånger. Närliggande
begrepp: *mastery learning* och *kompetensbaserad utbildning*.
- Svarar mot dimensionerna misslyckande/framsteg, anpassning och begriplighet.
- Kvittot kan vara **beläggen** för golvet och ersätter intygsfunktionen.
- Risk: nivåer kan bli betyg i förklädnad om de används för rangordning. Skriv
  ner det som en spänning, inte som skäl att avstå.

---

## 3. Modellen: vad vi kom fram till

- **"Identitet" är bara en totalbild av läget.** Det spelar ingen roll om det är
  en person, en organisation eller en kris.
- **Det är alltid lägesuppfattningar, inte en lägesbild.** En uppfattning har en
  bärare och ett perspektiv. En **gemensam lägesuppfattning** är ett av
  huvudmålen, och kan själv vara ett idealtillstånd (och ett bra första, litet
  steg: ingen behöver ändra sig, bara beskriva sin position).
- **Skillnader mellan perspektiv (elev/förälder) är information**, inte fel.
- **Ren text i botten.** Identitet/lägesuppfattning och vision/idealtillstånd kan
  vara fri text. Dimensioner är en **härledd vy**: AI:n föreslår en uppdelning på
  begäran, ägaren godkänner eller ändrar. Ingen struktur ska behöva fyllas i.
- **Skala = två beskrivna ändar**, inte "0 är sämst, 5 är bäst". Mellansteg
  beskrivs bara när de behövs. Närliggande metoder: Goal Attainment Scaling,
  rubriker med beteendeankare, CEFR/Dreyfus-nivåer. Inte KPI:er.
- **Arbetsfördelning:** motorn föreslår, ägaren väljer, ändrar och lägger till
  input. Klart (delvis) är när ägaren säger det, med en översikt per
  idealpåstående: uppnått / delvis / inte rört / inte längre relevant.

Skiss över dimension (härledd vy, inte lagringskrav):

```
Dimension
  namn, låg ände, hög ände
  positioner (en per perspektiv): läge, säkerhet (observerat/rapporterat/tolkat/antaget), belägg
  mål (önskad position)
  vad fungerar redan
  aktör för steg
```

### Två lägen i motorn (förslag)
1. **Vidga:** generera koncept utan hänsyn till dagens form. Observer-karaktärerna
   Zebran, Mushroom Inspector och Contrarian passar. Varje koncept anger vilken
   funktion det ersätter.
2. **Jorda:** pröva mot golvet, spänningarna och återinkopplade restriktioner.
   Skeptikern och Revisorn passar.

Och två nivåer: **problemrymd** (dimensioner, positioner, mål, golv) och
**designrymd** (koncept som bedöms mot dimensionerna). Befintlig
föreslå/välj/besluta-loop kan användas, men "uppdraget" blir en designhypotes.

Ny begreppsapparat som behövs: **koncept, funktion, golv, spänning, avstängd
restriktion, aktör**.

---

## 4. Experimentet (körde motorns egen AI mot caset)

Texten (lägesuppfattning + vision) gick rakt in. Inget sparades i `cases/`.
Modell i koden: `gpt-5.6-luna`.

**Körning A, motorn som den är (`suggest`)** gav fyra arbetsuppgifter: skissa
skolans grundmodell, definiera mål utan skoltvång, designa elevens första steg,
pröva modellen mot elevberättelser. Rimliga, men inga koncept. Ingen nivå- eller
betygsidé. Orsak (från koden): `SYSTEM_PROMPT` ber om "concrete, actionable,
appropriately sized", och ett förslag blir ett uppdrag med definition av klart.

**Körning B, konceptläge** med en ny systemprompt. Reglerna i den (för att kunna
återskapa den, skriptet är borttaget):
- föreslå KONCEPT (hela sätt att organisera lärande och uppväxt), inte små uppdrag
- alla former i dagens skola får släppas, men ange vilken FUNKTION varje koncept
  ersätter eller bevarar (omsorg, skydd, intyg, kunskapsuppbyggnad, socialt samspel)
- bedöm mot elevens idealtillstånd och mot golvet (kunskap och fostran minst som
  idag), och ange hur golvet visas
- var ärlig med spänningar och risker (likvärdighet, skydd, frihet/struktur)
- hitta inte på belägg, markera allt som antagande
- svenska, 5 koncept, minst två ovanliga

Resultat, fem koncept:
1. **Lärandebyar:** små blandade grupper (20–50) med fasta vuxna.
2. **Individuell lärandepakt:** elev, vårdnadshavare, mentor och det offentliga;
   lärande i många miljöer.
3. **Samhällsverkstaden:** lärande genom verkliga uppdrag med verkliga mottagare.
4. **Lärandemolnet:** adaptivt digitalt system med mänskligt yttersta ansvar.
5. **De tre livsrummen:** tryggt basrum, utforskarrum och samhällsrum.

Slutsatser:
- Nivåidén dök inte upp som eget koncept, men "verifierade kunskapsnivåer" och
  "kompetensintyg" finns i flera. Modellen går åt samma håll men gör det inte
  till kärnan.
- Konceptläget fungerar. Funktioner, golv och spänningar kom fram av sig själva
  (likvärdighet, skydd, frihet/struktur, risken för permanent undvikande).
- Modellen drar mot mjukare versioner av dagens skola (mentorer, planer,
  avstämningar). Alla fem koncept var "rimliga", ingen riktigt obekväm.
  Idérymden är bekväm, inte utforskad. Därför Zebran/Mushroom Inspector.
- Modellens samlade slutsats: fyra offentliga garantier behövs oavsett koncept:
  (1) ingen elev utan skyddande vuxenrelation, (2) centrala kunskaper verifieras
  oberoende av form, (3) social/demokratisk utveckling följs, (4) eleven kan
  påverka sin väg utan att ensam bära ansvaret för kvalitet och säkerhet.

---

## 5. Nästa steg (förslag, inget av detta är påbörjat)

1. **Prova nivåer med kvitto som eget koncept**: ägaren lägger in idén, motorn
   prövar den mot dimensioner, golv och spänningar. Troligen mest användbart.
2. **Vidga-körning med Zebran** som uttryckligen ska föreslå obekväma saker.
3. **Funktionsinventering av dagens skola** (vilka funktioner bevaras, ersätts,
   avskaffas). Troligen det som ger mest.
4. **Skriv en spec** (t.ex. `docs/spec/lagesuppfattning-och-idealtillstand-v0.1.md`)
   med begreppen ovan och skolan-caset som exempel. Pröva modellen på prompt-nivå
   innan koden ändras.
5. Beslut kvar att ta: byta begreppet "identitet" till "lägesuppfattning" i det
   användaren ser? Skriva om lägesuppfattningen i elevens röst eller märka
   perspektivet? Låta motorn föreslå de saknade ändarna för de fyra ensidiga
   dimensionerna?

### Hur det skulle kunna realiseras i nuvarande kod (ej bekräftat)
Mest tillägg: fält för dimensioner i `CaseFile` (bör ha standardvärde; jag läste
inte `_from_dict` till slutet, så ladda gamla ärenden behöver testas),
dimensionerna med i `_build_context_message`, mål kopplade till dimension,
uppdrag kopplade till aktör, ny AI-funktion för att komplettera ensidiga
dimensioner, ett konceptläge, och en regel i `SYSTEM_PROMPT` om att förslag aldrig
får vara order eller skuldbeläggning.

---

## 6. Motorns nuläge (genomgång under sessionen)

Konceptet ligger före koden. I docs finns Identity → Transition → Identity
(`QUESTIONS.md` Q-002, diagrammen i `README.md`, IOOIS-utkastet). I koden finns
ingen identitet: `Goal.desired_direction` är en sträng, "visionen" är
ärendets namn, `current_situation` är en sträng, och inget beskriver
deltagaren.

Fynd att åtgärda (ingen är åtgärdad):
1. **Observer kraschar utan API-nyckel:** `_generate_intervention` anropar
   `_fallback_intervention(character, goal, reason)` men metoden tar bara
   `character_id`. TypeError i `/select`, som inte fångar det.
2. **GIVE UP i webben** avbryter målet direkt. Omprövningen (klar / ändra /
   osäker / utmana mig) finns bara i CLI och skript.
3. **Global `case` i Flask**: bara enanvändare. Ägarkontroll sker bara vid öppning.
4. **Strikt laddning** (`Goal(**g)` m.fl.) bryter gamla ärenden vid schemaändring.
   Ingen versionsnyckel.
5. **Oanvänt:** `MISSION_FAILED`, `Decision.reason`, `history`. Observer-events
   matas inte tillbaka till AI-kontexten.
6. **Tester:** inga för `web.py`, Observer eller spara/ladda. AI-testerna är
   utskriftsskript.
7. **Dubblering:** JSON-parsningen finns fyra gånger. `run_skordefest.py` och
   `run_scenario.py` överlappar.

Ordning på jobbet: skolan-caset först som exempel, sedan arbete med motorn.

---

## 7. Städning och beslut i repot

- **Linköping-caset** (`cases/6d41beab.json`, "Linköping då och nu") ska brytas
  ut till egen programvara. Motorn är för mer abstrakta och generiska
  utmaningar. De generiska delarna av utkastet
  `docs/spec/challenge-authoring-top-layer-v0.1-draft.md` (IOOIS, "samma formel,
  olika ingredienser", förskapat ärende) är värda att behålla. Plats- och
  ruttdelarna (§10, §13) hör till den nya programvaran.
- **`BACKLOG.md` innehåller bara auth-punkter** (2 KB, inte tom på disk). Den
  långsiktiga planen ligger i `ROADMAP.md`, vars rubrik säger "Project Backlog",
  och `README.md` beskriver fortfarande BACKLOG som långsiktig plan. Namn och
  innehåll bör rättas.
- **Ej incheckat** när sessionen gjordes: sex borttagna ärenden i `cases/`, det
  nya ärendet `8f36db16`, utkastet ovan och `the_engine.code-workspace`.
- `CURRENT.md` (auth-spåret + modellspåret) bedömdes som i gott skick.

---

## 8. the_app (kort, så det inte tappas)

- Appen är godkänd i App Store Connect. Den syntes inte i butiken eftersom
  **Trader Status** saknades (EU:s Digital Services Act). Christer deklarerade
  "inte näringsidkare" (hobby, gratis, inga intäkter). Det kan ändras när det
  blir kommersiellt eller används för att marknadsföra en verksamhet, och bör då
  uppdateras innan intäkter börjar.
- Statusen blev grön. Nästa: se att appen dyker upp i svenska butiken (kan ta
  upp till ett dygn), annars kontakta Apple Developer Support. Testa med familj
  via App Store-länken eller TestFlight.
- **Android:** arbetsplatsen kan ge en ny telefon, möjligen Android. Fråga IT om
  sidladdning av APK och eget Google-konto. Bygg med
  `eas build --platform android --profile preview`. Google Play för nya
  personkonton kräver slutet test med ett visst antal testare under 14 dagar
  (kolla aktuella siffror i Play Console). Emulator i Android Studio går som start.
- Andra punkter att ha koll på: backend på plan som inte somnar, backup av
  produktionsdatabasen, kontoradering nåbar i appen, integritetspolicy,
  övervakning/kraschrapporter. `the_auth` kör fortfarande på gratisnivå.

---

## 9. Tillägg: innehåller identiteten också dit man vill nå?

Tanke från slutet av sessionen, ännu inte avgjord:

- En första inmatning innehåller naturligt **både läge och önskan**. "Allt är
  skit" är nuläge men har ett outtalat "det borde inte vara så".
- Motorn gör redan så: `/start` tar en text och `interpret_input` delar den i
  `current_situation` och `possible_direction`, som en hypotes ägaren kan rätta.
- Möjlig förenkling: en enda pool av **påståenden** märkta med *läge eller
  önskat*, och *vems perspektiv*. Identitet och idealtillstånd är samma sak
  i olika tid.
- En brist är den låga änden av en dimension och pekar mot sin motsats. Motorn
  kan föreslå den höga änden som **hypotes**. Motsatsen till ett klagomål är
  inte alltid det man vill ha (stress → kanske "hanterbar stress"). Ägaren
  bekräftar alltid.
- **Öppen fråga: vilken är frågan?** Dagens öppningsfråga ("What are we working
  on right now?") frågar efter en uppgift, inte efter läge och önskan. Förslag
  att fundera på: *"Hur ser det ut just nu, och hur skulle du vilja att det såg
  ut?"*, gärna med *"Och vad fungerar ändå?"*. En bra fråga har tre delar: läge,
  önskan, vems perspektiv. Om bara en del ges ska motorn ställa **en**
  följdfråga om det som saknas, inte svara "jaha" och inte lista alternativ.
- Christer funderar vidare på själva frågan.

---

## 10. Fortsättning: lärandepakten, trädmetoden och deep mode

Sessionen fortsatte efter avsnitt 9. Fyra experiment körs totalt mot motorns AI
(skripten och utdata togs bort efter varje körning, inget sparades i `cases/`).
Experiment 1 och 2 beskrivs i avsnitt 4. Här är 3 och 4.

### 10.1 Senge (kort, från minnet, inte uppslaget)
Komplexa problem: dynamisk komplexitet (orsak och verkan långt ifrån varandra),
dagens problem kommer från gårdagens lösningar, tryck ger motryck, man kan inte
dela en elefant på mitten, hävstänger finns men sällan där man först tittar, och
skuld hjälper inte. Fem discipliner: personligt mästerskap (spänningen mellan vision
och verklighet), mentala modeller (göra olika bilder synliga = gemensam
lägesuppfattning), gemensam vision, teaminlärning, systemtänkande. Bok om skolor:
*Schools That Learn*. Slutsats för oss: lös inte hela systemet, hitta några
hävstänger och pröva i små experiment. Tyngden Christer kände är ett tecken på
att komplexiteten har setts, inte på att något är fel.

### 10.2 Ide: nivåer i stället för betyg, kombinerat med spår 1-3
Nivåer per ämne, kvitto när en nivå är klarad, obegränsade omprov, ett ämne i
taget. Bedömning (min analys, ej körd i motorn): stor effekt på misslyckande,
begriplighet, självbestämmande och anpassning; löser inte tillhörighet och
fostran. Nya risker: undvikande, proven blir bärande, provångest utan konsekvens,
kvitton som yttre belöning, "ett ämne i taget" är ett antagande, utan relation
blir det en provautomat, och vad som gäller vid åldersgräns. Öppna frågor: vad är
en nivå, vem prövar och hur blir proven likvärdiga, vilka belägg gäller för
fostran. Ännu inte körd som koncept i motorn.

### 10.3 Experiment 2: lärandepakten som valt spår (lägen A-F)
Motorns egen loop gav ett uppdrag (skriv ett tvåsidigt utkast till en pakt för ett
påhittat elevscenario). Observer-karaktärerna gav:
- **Zebran:** pakten som trafikljus. Grönt = eleven väljer själv, gult = kräver
  gemensam planering, rött = det ingen vuxen får kräva.
- **Contrarian:** rätten att avstå från mål, mentor och uppföljning under perioder,
  utan att säkerheten försvinner.
- **Skeptikern:** vem avgör när elevens val skyddar tryggheten och när det berövar
  möjligheter eller används för att sänka kraven?

Analysen: god på anpassning, meningsfullhet, nyfikenhet, självbestämmande; delvis
på trygghet, tillhörighet, utveckling, begriplighet, framsteg; framtidstro delvis
till god. Funktioner som **saknas eller är oklara**: mat/vila/fysisk miljö,
avlastning för vårdnadshavare under dagtid, vårdnadshavares arbete/studier.
Nästan alla föreslagna steg hade det offentliga som aktör; eleven och föräldern
nämndes knappt; gemensam lägesuppfattning kom inte upp som första steg. Allt är
modellens resonemang, inte belägg.

### 10.4 Min tolkning av "pakt" (inte körd, ej inlagd i någon prompt)
En pakt är ömsesidig, till skillnad från skolplikt (ensidig plikt), plan eller
åtgärdsprogram (experter om eleven) och betyg (utlåtande om eleven). Det nya är
att det offentliga blir skyldigt eleven något konkret. Delar att fråga efter:
parterna, vad var och en åtar sig, vad eleven bestämmer och vad som inte kan
förhandlas (trafikljuset), hur pakten ändras, vad som händer om någon bryter den
(särskilt om det är de vuxna), och hur man kan avstå. Nära Case File-idén: motorns
"föreslår/bestämmer", beslutsvokabulären och GIVE UP/omprövning är redan en
förhandling. Varningar: pakten med ett barn är inte jämlik; en pakt kan användas
mot barnet ("du lovade"), så rätten att ompröva utan skuld hör till idén.

### 10.5 Experiment 3: rent test, bara listorna + meningen
Fyra punkter ur "Individuell lärandepakt: eleven, vårdnadshavaren, en mentor och det
offentliga, med lärande i många miljöer." Körd två gånger. Tre punkter var samma
båda gånger, en skilde sig:

| | Körning 1 | Körning 2 |
|---|---|---|
| Pakten | Pakten som gemensamt ansvar | Gemensam lärandepakt |
| Miljöerna | Lärande i en ekologisk mångfald av miljöer | Lärande i en distribuerad miljö |
| Det offentliga | Offentlig kunskaps- och fostransgaranti | Offentlig kunskaps- och fostransgaranti |
| Fjärde | Elevägd lärandebana | Mentorn som kontinuitet och översättare |

Observationer: vårdnadshavaren fick ingen egen punkt; modellen kom själv fram till
att parterna har olika makt, att vissa rättigheter inte kan förhandlas bort, att
"eleven valde själv" kan bli ett sätt att lägga ansvaret på eleven, och att
garantin riskerar att återskapa prov och ranking med nya namn. Motorns egen
`suggest` gav fyra uppgifter (skissa pakten, designa vardagen, säkra kunskapsmål,
bygg pilot), alltså inte koncepten. **Christer behåller de fyra han fick ur första
körningen** (lärandebyar, individuell lärandepakt, samhällsverkstaden,
lärandemolnet) och valde att utforska pakten vidare.

### 10.6 Experiment 4: en nivå ner, på pakten
Indata: listorna + meningen + punkten "Gemensam lärandepakt". Tre av fyra var
samma i båda körningarna:

| | Körning 1 | Körning 2 |
|---|---|---|
| Vad som gäller | Lärandekonstitutionen | Gemensam grundöverenskommelse |
| Hur lärandet utformas | Personlig lärandedesign | Lärandemiljö som förhandlingsbar del |
| Hur framsteg syns | Levande bevis på lärande | Synlig progression och offentlig garanti |
| Fjärde | Ömsesidigt åtagande (vad var och en av de fyra åtar sig) | Eleven som medförfattare till lärvägen |

Ny risk: **gemensamt ansvar kan bli otydligt ansvar** (om alla ansvarar kan ingen
hållas ansvarig); pakten kan bli ett dokument som skyddar organisationen och inte
eleven, eller formuleras av vuxna och bara kallas gemensam. Fortfarande svagt:
rätten att avstå och vad som händer om någon bryter pakten. Nivåidén kom inte
upp, bara portfölj och "bevis".

### 10.7 Trädmetoden
En mening in, fyra punkter ut, ägaren väljer, och det upprepas. I experimenten bad
jag modellen om fem saker per punkt (vad den innebär, vilken del av föräldern den
kommer ur, hur den möter idealtillståndet, vilken funktion den ersätter eller
bevarar, största risk). Det var mitt val i prompten och inte ett gemensamt
beslut, och jag har inte testat att det var just fem fält som gav djupet. Det som
gjorde skillnad var troligen koncept-framställningen och kravet på funktion.

**Beslut (Christer): ren text.** En nod är ett namn och en redigerbar text. Inga
fasta fält i lagringen. Prompten kan fortfarande be om funktion, koppling till
idealet och risk, men svaret sparas som text. Fält extraheras bara när en vy
behöver dem, på begäran. Risk: extraktionen blir ungefärlig och täckningsvyn
mindre exakt. Ej testat om fri text ger samma djup; jämför vid bygget.

Härledda vyer (byggs senare, från texten): matris över vilka idealtillstånd varje
nod möter (luckor syns), funktionsinventering över alla "ersätter/bevarar", och
återkommande risker som trädets egna spänningar. Idé att pröva: hur skulle eleven
själv uttrycka detta?

### 10.8 Dela upp eller variera
Två olika operationer som motorn gjorde utan att vi bad om det:
- **Dela upp** = delar som tillsammans bildar föräldern (täckning). Pakt-nivån
  var detta.
- **Variera** = alternativ som skiljer sig åt (mångfald). Nivån över var mer detta.
Bör vara ett val per nod.

Redigering ensam täcker inte idérymden, eftersom man redigerar det man ser och de
fyra första ankrar. Behövs också: lägga till/byta ut/dela/slå ihop/parkera,
"variera den här", och en **täckningsvy** (vilka idealtillstånd ingen nod möter,
vilka linser som inte använts).

### 10.9 Linser (perspektiv på första inmatningen) — hypoteser, ej testade
Koncept; mål och resultat; filosofisk (vad betyder orden, vilka antaganden);
byggare/entreprenör (minsta prövbara sak); den berörde (elevens/förälderns ögon);
systemtänkare (återkopplingar, hävstänger, dolda funktioner); regelverk och
resurser (slå på restriktioner igen); kritiker och provokatör (Observer-
karaktärerna som läge för hela körningen). Skilj **lins** (hur indatan läses) från
**läge** (vilken sorts utdata: koncept, uppdrag, risker). Det är läget som gjort
skillnad hittills; effekten av linser är inte prövad.

### 10.10 Deep mode (idé)
4 till 5 körningar, var och en med en egen lins och en kort fast linsbeskrivning
(så att körningarna går att jämföra). Mellan körningarna kan motorn variera
indatan (lyfta en annan idealpunkt, be om "sådant som inte redan finns bland
förslagen"). Resultatet grupperas i **stabila** (återkommer) och **varianter**
(en lins, lins angiven). Ägaren väljer fyra eller fem och **parkerar** resten.
Varningar: stabilt är inte detsamma som rätt (kan vara modellens förförståelse
eller ankring i dagens skola, varianterna kan vara mer värda); linser kan bli
karikatyrer, så håll dem korta, spara vilken lins som gav vad, och gör dem
avstängbara.

### 10.11 Beslut och nästa steg
Beslut (Christer): behåll de fyra första koncepten; redigering av de fyra
förslagen ska finnas; en knapp för deep mode ska köras när de fyra kommit fram.
Konkreta punkter att realisera är lagda i `CURRENT.md`. Inget är påbörjat i
koden. Öppet: köra nivåidén som koncept; köra ett linstest på pakt-punkten
(byggare, den berörde, systemtänkare) för att se om linserna ger olika svar;
nästa nivå ner på någon av de fyra pakt-punkterna.
