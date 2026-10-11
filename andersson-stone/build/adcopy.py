# Ad copy per (category, theme, language). Only claims that are on the site.
C = {}  # common per language: headlines, descriptions
C["sv"] = dict(h=["Andersson Stone","Försäkrad DHL Express","30 dagars fri retur","Certifierade diamanter","Konfliktfria diamanter","Leverans inom 10 dagar","Tillverkas efter beställning","Skickas från Sverige"],
  d=["Tillverkas efter beställning och levereras försäkrat med DHL Express inom 10 dagar.",
     "Konfliktfria diamanter med certifikat. 30 dagars fri retur. Betala smidigt med Klarna."])
C["de"] = dict(h=["Andersson Stone","Versicherter DHL Express","30 Tage gratis Rückgabe","Zertifizierte Diamanten","Konfliktfreie Diamanten","Lieferung in 10 Tagen","Auf Bestellung gefertigt","Versand aus Schweden"],
  d=["Auf Bestellung gefertigt und versichert per DHL Express in 10 Tagen geliefert.",
     "Konfliktfreie, zertifizierte Diamanten. 30 Tage kostenlose Rückgabe. Sicher bezahlen."])
C["nl"] = dict(h=["Andersson Stone","Verzekerd met DHL Express","30 dagen gratis retour","Gecertificeerde diamanten","Conflictvrije diamanten","Binnen 10 dagen geleverd","Op bestelling gemaakt","Verzonden uit Zweden"],
  d=["Op bestelling gemaakt en binnen 10 dagen verzekerd geleverd met DHL Express.",
     "Conflictvrije, gecertificeerde diamanten. 30 dagen gratis retour. Veilig betalen."])
C["da"] = dict(h=["Andersson Stone","Forsikret DHL Express","30 dages gratis retur","Certificerede diamanter","Konfliktfri diamanter","Levering inden 10 dage","Fremstilles på bestilling","Sendes fra Sverige"],
  d=["Fremstilles på bestilling og leveres forsikret med DHL Express inden for 10 dage.",
     "Konfliktfri, certificerede diamanter. 30 dages gratis retur. Sikker betaling."])
C["en"] = dict(h=["Andersson Stone","Insured DHL Express","30-Day Free Returns","Certified Diamonds","Conflict-Free Diamonds","Delivered Within 10 Days","Made to Order","Shipped From Sweden"],
  d=["Made to order and delivered insured with DHL Express within 10 days.",
     "Conflict-free, certified diamonds. 30-day free returns. Secure checkout."])
# price lines per market currency (only where verified: earrings & tennis 'from' prices)
P = {"SE":{"Earrings":"Från 5 649 kr","Tennis":"Från 20 299 kr"},"SE-en":{"Earrings":"From SEK 5,649","Tennis":"From SEK 20,299"},
     "DE":{"Earrings":"Ab 499 €","Tennis":"Ab 1.799 €"},"NL":{"Earrings":"Vanaf €499","Tennis":"Vanaf €1.799"},"NL-en":{"Earrings":"From €499","Tennis":"From €1,799"},
     "DK":{}}
# category/theme specific headlines + first description
T = {
 ("Earrings","sv"):(["Diamantörhängen","Diamantörhängen i guld","Örhängen med diamanter","Välj form, karat och guld","Labbodlade eller naturliga"],
                    "Diamantörhängen i 9K–18K guld, naturliga eller labbodlade diamanter. Välj form och karat."),
 ("Earrings","de"):(["Diamant-Ohrstecker","Diamant-Ohrstecker in Gold","Ohrstecker mit Diamanten","Form, Karat und Gold wählen","Labor- oder Naturdiamant"],
                    "Diamant-Ohrstecker in 9K–18K Gold, natürliche oder Labordiamanten. Form und Karat wählen."),
 ("Earrings","nl"):(["Diamanten Oorbellen","Diamanten Oorknopjes","Oorbellen in Goud","Kies Vorm, Karaat en Goud","Lab Grown of Natuurlijk"],
                    "Diamanten oorknopjes in 9K–18K goud, natuurlijk of lab grown. Kies vorm en karaat."),
 ("Earrings","da"):(["Diamant Øreringe","Diamant Ørestikker i Guld","Øreringe med Diamanter","Vælg Form, Karat og Guld","Lab Grown eller Naturlig"],
                    "Diamant ørestikker i 9K–18K guld, naturlige eller lab grown diamanter. Vælg form og karat."),
 ("Earrings","en"):(["Diamond Stud Earrings","Lab-Grown Diamond Studs","Diamond Studs in Gold","Choose Shape, Carat & Gold","Lab-Grown or Natural"],
                    "Diamond studs in 9K–18K gold with natural or lab-grown diamonds. Choose shape and carat."),
 ("Tennis","sv"):(["Tennisarmband med Diamanter","Diamantarmband i Guld","Tennisarmband 3–7 Karat","Längder 15–22 cm","Labbodlade eller Naturliga"],
                  "Tennisarmband med diamanter i 9K–18K guld. Labbodlade eller naturliga, cirka 3–7 karat."),
 ("Tennis","de"):(["Tennisarmband mit Diamanten","Tennisarmband in Gold","Tennisarmband 3–7 Karat","Längen 15–22 cm","Labor- oder Naturdiamant"],
                  "Tennisarmband mit Diamanten in 9K–18K Gold. Labor- oder Naturdiamanten, ca. 3–7 Karat."),
 ("Tennis","nl"):(["Tennisarmband met Diamanten","Tennisarmband in Goud","Tennisarmband 3–7 Karaat","Lengtes 15–22 cm","Lab Grown of Natuurlijk"],
                  "Tennisarmband met diamanten in 9K–18K goud. Lab grown of natuurlijk, ca. 3–7 karaat."),
 ("Tennis","da"):(["Tennisarmbånd med Diamanter","Tennisarmbånd i Guld","Tennisarmbånd 3–7 Karat","Længder 15–22 cm","Lab Grown eller Naturlig"],
                  "Tennisarmbånd med diamanter i 9K–18K guld. Lab grown eller naturlige, ca. 3–7 karat."),
 ("Tennis","en"):(["Diamond Tennis Bracelets","Lab-Grown Tennis Bracelet","Tennis Bracelets in Gold","Approx. 3–7 Carat","Lengths 15–22 cm"],
                  "Diamond tennis bracelets in 9K–18K gold. Lab-grown or natural diamonds, approx. 3–7 carat."),
 ("Rings","sv"):(["Förlovningsringar i Guld","Förlovningsring med Diamant","Designa din Förlovningsring","Välj Infattning och Diamant","Solitär, Trestens & Pavé"],
                 "Bygg din förlovningsring: välj infattning, guld och en naturlig eller labbodlad diamant."),
 ("Rings","de"):(["Verlobungsringe in Gold","Verlobungsring mit Diamant","Verlobungsring gestalten","Fassung und Diamant wählen","Solitär, Trilogie & Pavé"],
                 "Gestalten Sie Ihren Verlobungsring: Fassung, Gold und natürlicher oder Labordiamant."),
 ("Rings","nl"):(["Verlovingsringen in Goud","Verlovingsring met Diamant","Ontwerp je Verlovingsring","Kies Zetting en Diamant","Solitair, Trilogy & Pavé"],
                 "Ontwerp je verlovingsring: kies zetting, goud en een natuurlijke of lab grown diamant."),
 ("Rings","da"):(["Forlovelsesringe i Guld","Forlovelsesring med Diamant","Design din Forlovelsesring","Vælg Fatning og Diamant","Solitaire, Trestens & Pavé"],
                 "Design din forlovelsesring: vælg fatning, guld og en naturlig eller lab grown diamant."),
 ("Rings","en"):(["Lab-Grown Engagement Rings","Lab-Grown Diamond Rings","Engagement Rings in Gold","Design Your Engagement Ring","Choose Setting and Diamond"],
                 "Design your engagement ring: choose the setting, gold and a natural or lab-grown diamond."),
}
# theme-specific lead headline (keyword theme first)
LEAD = {
 ("Earrings","Gold","sv"):"Diamantörhängen i Guld",("Earrings","Gold","de"):"Diamant-Ohrstecker Gold",("Earrings","Gold","nl"):"Diamanten Oorbellen Goud",("Earrings","Gold","da"):"Diamant Øreringe i Guld",
 ("Earrings","Lab grown","sv"):"Labbodlade Diamantörhängen",("Earrings","Lab grown","de"):"Lab Grown Diamant-Ohrringe",("Earrings","Lab grown","nl"):"Lab Grown Diamant Oorbellen",("Earrings","Lab grown","da"):"Lab Grown Diamant Øreringe",
 ("Earrings","Lab grown","en"):"Lab-Grown Diamond Earrings",("Earrings","Carat / shape","de"):"Diamant-Ohrstecker 1 Karat",("Earrings","Carat / shape","nl"):"Diamanten Oorbellen 1 Karaat",("Earrings","Carat / shape","da"):"Diamant Ørestikker 1 Carat",
 ("Tennis","Gold","sv"):"Tennisarmband i Guld",("Tennis","Gold","de"):"Tennisarmband Gold 585",("Tennis","Gold","nl"):"Tennisarmband in Goud",("Tennis","Gold","da"):"Tennisarmbånd i Guld",
 ("Tennis","Men","sv"):"Tennisarmband Herr",("Tennis","Men","de"):"Tennisarmband für Herren",("Tennis","Men","nl"):"Tennisarmband Heren",("Tennis","Men","da"):"Tennisarmbånd til Mænd",
 ("Tennis","Lab grown","sv"):"Labbodlat Tennisarmband",("Tennis","Lab grown","de"):"Tennisarmband Labordiamant",("Tennis","Lab grown","nl"):"Lab Grown Tennisarmband",("Tennis","Lab grown","da"):"Lab Grown Tennisarmbånd",
 ("Tennis","Lab grown","en"):"Lab-Grown Tennis Bracelet",
 ("Rings","Lab grown","sv"):"Labbodlad Diamantring",("Rings","Lab grown","de"):"Verlobungsring Labordiamant",("Rings","Lab grown","nl"):"Lab Grown Diamant Ring",("Rings","Lab grown","da"):"Lab Grown Diamantring",
 ("Rings","Lab grown","en"):"Lab-Grown Engagement Rings",
 ("Rings","Diamond ring","de"):"Diamantringe für Damen",("Rings","Diamond ring","nl"):"Diamanten Ringen",("Rings","Diamond ring","da"):"Diamantringe til Damer",
 ("Rings","Solitaire / diamond ring","sv"):"Solitärringar med Diamant",("Rings","Engagement ring","en"):"Engagement Rings Sweden",
}
MEN_D = {"sv":"Tennisarmband för herr i längder upp till 21,6 cm. 9K–18K guld med diamanter.",
         "de":"Tennisarmband für Herren in Längen bis 21,6 cm. 9K–18K Gold mit Diamanten.",
         "nl":"Tennisarmband voor heren in lengtes tot 21,6 cm. 9K–18K goud met diamanten.",
         "da":"Tennisarmbånd til mænd i længder op til 21,6 cm. 9K–18K guld med diamanter."}
PATH = {("Earrings","sv"):"orhangen",("Earrings","de"):"ohrstecker",("Earrings","nl"):"oorbellen",("Earrings","da"):"oreringe",("Earrings","en"):"earrings",
        ("Tennis","sv"):"tennisarmband",("Tennis","de"):"tennisarmband",("Tennis","nl"):"tennisarmband",("Tennis","da"):"tennisarmband",("Tennis","en"):"tennis",
        ("Rings","sv"):"forlovningsring",("Rings","de"):"verlobungsring",("Rings","nl"):"verlovingsring",("Rings","da"):"forlovelsesring",("Rings","en"):"rings"}
def build(cat, theme, lang, market):
    h=[]; lead=LEAD.get((cat,theme,lang))
    if theme=="Men": lead=LEAD[(cat,"Men",lang)]
    if lead: h.append(lead)
    h+=T[(cat,lang)][0]
    pk=market+("-en" if lang=="en" and market in("SE","NL") else "")
    if cat in P.get(pk,{}): h.append(P[pk][cat])
    h+=C[lang]["h"]
    seen=[]; [seen.append(x) for x in h if x.lower() not in [s.lower() for s in seen]]
    h=seen[:15]
    d=[MEN_D[lang] if theme=="Men" else T[(cat,lang)][1]]+C[lang]["d"]
    return h,d,PATH[(cat,lang)]
if __name__=="__main__":
    bad=0
    for (cat,lang),v in T.items():
        for th in ["Core","Gold","Lab grown","Men","Carat / shape","Diamond ring"]:
            if th=="Men" and cat!="Tennis": continue
            if th=="Men" and lang=="en": continue
            for mk in ["SE","DE","NL","DK"]:
                h,d,p=build(cat,th,lang,mk)
                for x in h:
                    if len(x)>30: print("H>30",len(x),x); bad+=1
                for x in d:
                    if len(x)>90: print("D>90",len(x),x); bad+=1
                if len(p)>15: print("P>15",p); bad+=1
    print("problems:",bad)
