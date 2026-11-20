# Skolan / hemmasittare: underlag att klistra in

Tankeexperiment, inte ett arbete med riktiga barn. Punkterna är sammanfattade
från ca 200 berättelser (elevperspektiv, föräldrar med). Inga berättelser, namn
eller uppgifter som kan identifiera någon ska in här, eftersom texten skickas till
AI-tjänsten.

Det här är samma text som användes i experimenten (se `LAST_SESSION.md`).

## Så kör du

1. Starta `python src/web.py` (starta om den om den redan körs, så att nya
   ändringar följer med), logga in och välj *Nytt case*. Skriv rubriken,
   till exempel `Ny skola för hemmasittare`, och tryck *Skapa*.
2. På första sidan klistrar du in **Lägesuppfattning** under *Hur ser det ut idag?*
   och **Idealtillstånd** under *Hur vill du att det ska vara?* (båda nedan).
   Du kan fylla i bara det ena.
3. Tryck *Visa möjliga riktningar* för fyra förslag, eller *Kör deep mode direkt*
   för fler och mer skilda förslag (tar en stund).
4. På sidan med förslag fungerar det som en enarmad bandit. På varje förslag finns
   *Behåll* (ligger kvar när du kör om), *Dela upp* (fyra delar av just det
   förslaget), *Redigera* och *Lägg undan*. *Kör om de andra* ersätter allt du inte
   behållit med nya förslag genom en slumpad lins. De ersatta finns kvar under
   *Tidigare förslag*, där du kan ta tillbaka dem. *Deep mode* kan köras på
   varje nivå.

Det finns inga mål eller "uppdrag" i det här flödet. Under huven skapas ett
dolt rotmål som förslagen hänger under, men det syns inte.

Tips: i experimenten gav samma två listor fyra koncept (lärandebyar, pakt,
verkstad, moln). Pröva också att lägga in pakten som egen punkt (se nedan) och
öppna den, för att jämföra med de gamla körningarna.

---

## Pakten som egen punkt (valfritt)

Om du vill börja i pakten, och inte i de förslag motorn ger: välj *Lägg till egen
punkt*, skriv namnet `Individuell lärandepakt` och klistra in meningen nedan som text.
Öppna sedan punkten och tryck *Dela upp i fyra punkter*.

```
Individuell lärandepakt: eleven, vårdnadshavaren, en mentor och det offentliga, med lärande i många miljöer.
```

---

## Lägesuppfattning (klistras in under "Hur ser det ut idag?")

```
Lägesuppfattning (elevperspektiv, sammanfattat från ca 200 berättelser om hemmasittare):
1. Överbelastning: ljud, människor, intryck och miljö blir för mycket.
2. Brist på trygghet: eleven känner oro, stress eller rädsla inför skoldagen.
3. Brist på tillhörighet: eleven upplever sig inte passa in i gruppen eller skolans sammanhang.
4. Att inte bli sedd: elevens signaler, behov och svårigheter uppmärksammas inte.
5. Bristande inflytande: eleven har liten möjlighet att påverka sin situation eller sitt arbetssätt.
6. Felaktiga förväntningar: samma krav och arbetssätt används trots olika förutsättningar.
7. Brist på begriplighet: det är oklart vad eleven ska göra, hur eller varför.
8. Förlorad motivation: skolarbetet upplevs som meningslöst, ointressant eller omöjligt.
9. Upplevelse av misslyckande: eleven får återkommande erfarenheter av att inte räcka till.
10. Förlorad framtidstro: skolan leder till uppgivenhet, frånvaro eller känslan av att framtiden stängs.
```

---

## Idealtillstånd (klistras in under "Hur vill du att det ska vara?")

```
Idealtillstånd (elevens röst):
1. Trygghet: jag känner mig trygg och behöver inte kämpa för att orka vara här.
2. Tillhörighet: jag har en självklar plats och är accepterad som jag är.
3. Individuell anpassning: skolan fungerar med mina förutsättningar, inte tvärtom.
4. Meningsfullhet: jag förstår varför jag lär mig något och vad jag kan använda det till.
5. Nyfikenhet: jag får utforska sådant som väcker mitt intresse.
6. Utveckling: jag får utmaningar som hjälper mig att växa, oavsett var jag börjar.
7. Självbestämmande: jag har inflytande över hur jag lär mig och kan påverka min väg.
8. Begriplighet: jag förstår målet, nästa steg och vad som förväntas av mig.
9. Framsteg och självtillit: jag får uppleva att jag kan, lyckas och komma vidare.
10. Framtidstro: jag ser möjligheter och kan föreställa mig en framtid som känns värdefull.

Slutmål: alla som gått i skolan upp till 9 eller 12 år ska uppfylla både en form av fostran och
kunskapsnivåer motsvarande dagens skola, eller bättre. Full frihet från allt dagens skola erbjuder:
klassrum, lektioner, lärare, schema, närvaroplikt, betyg, nationella prov med mera.
```

---

## Anteckningar

- Lägesuppfattningen är i tredje person och idealet i första person. Det är samma
  text som i experimenten, så resultaten går att jämföra. Om du vill ha samma röst
  på båda sidor kan du skriva om en av dem och se om svaren ändras.
- Lägesuppfattningen beskriver bara brister. Lägg gärna till en rad om vad som
  fungerar redan (en lärare, en situation där det går bra) och se om förslagen
  förändras.
- Två dimensioner saknar motsvarighet på andra sidan: *Överbelastning* och *Att inte
  bli sedd* (inget ideal), samt *Nyfikenhet* och *Utveckling* (inget nuläge).
