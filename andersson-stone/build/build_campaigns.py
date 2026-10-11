# Builds the 4 Andersson Stone Search campaigns (PAUSED) via GoogleAdsService.Mutate. Token in memory only.
import sys, json, csv, re, collections, urllib.request
SD=sys.argv[1]; sys.path.insert(0,SD)
from gads import token, CID, LOGIN
from adcopy import build
MODE=sys.argv[2]   # "plan" (print counts only) | "shared" | "SE"/"DE"/"NL"/"DK"
REPO="/home/user/Claude/andersson-stone"
rows=[r for r in csv.DictReader(open(f"{REPO}/search-keywords.csv")) if r['status']=="launch"]
GEO={"SE":2752,"DK":2208,"DE":2276,"NL":2528}; LANG={"SE":"sv","DK":"da","DE":"de","NL":"nl"}
LC={"en":1000,"de":1001,"da":1009,"nl":1010,"sv":1015}
BUDGET={"SE":250,"DE":250,"NL":200,"DK":200}
MEN={"sv":["herr","herrar","man","kille"],"de":["herren","männer","mann","herr"],"nl":["heren","mannen","man","jongens"],"da":["mænd","herre","mand","drenge"],"en":["men","mens","man","boys"]}
EAR={"sv":["hängande","creoler"],"de":["hängend","creolen"],"nl":["hangers","creolen"],"da":["hængende","creoler"],"en":["drop","dangle"]}
RING={"sv":["vigselring","allians","par","storlek","hand","finger"],"de":["ehering","trauring","paar","größe","hand","finger"],"nl":["trouwring","set","maat","hand","vinger"],"da":["vielsesring","par","størrelse","hånd","finger"],"en":["wedding","set","size","hand","finger"]}
SITE={"sv":[("Diamantörhängen","earrings"),("Tennisarmband","tennis-bracelets"),("Förlovningsringar","rings"),("Konfliktfria diamanter","CF")],
      "de":[("Diamant-Ohrstecker","earrings"),("Tennisarmbänder","tennis-bracelets"),("Verlobungsringe","rings"),("Konfliktfreie Diamanten","CF")],
      "nl":[("Diamanten oorbellen","earrings"),("Tennisarmbanden","tennis-bracelets"),("Verlovingsringen","rings"),("Conflictvrije diamanten","CF")],
      "da":[("Diamant øreringe","earrings"),("Tennisarmbånd","tennis-bracelets"),("Forlovelsesringe","rings"),("Konfliktfri diamanter","CF")]}
CALL={"sv":["Försäkrad DHL Express","30 dagars fri retur","Certifierade diamanter","Betala med Klarna"],
      "de":["Versicherter DHL Express","30 Tage gratis Rückgabe","Zertifizierte Diamanten","Sichere Bezahlung"],
      "nl":["Verzekerd DHL Express","30 dagen gratis retour","Gecertificeerd","Veilig betalen"],
      "da":["Forsikret DHL Express","30 dages gratis retur","Certificerede diamanter","Sikker betaling"]}
shared=[]; sec=None
for l in open(f"{REPO}/negative-keywords.txt"):
    l=l.strip()
    if l.startswith("## "): sec=l
    elif l and not l.startswith("#") and sec and sec.startswith("## SHARED"): shared.append(l)
shared=sorted(set(shared))
# conflict check: shared negative contained (as whole words) in a launch keyword
allkw=[r['keyword'] for r in rows]
conf=[(n,k) for n in shared for k in allkw if re.search(r'(^| )'+re.escape(n)+r'( |$)',k)]
assert not conf, conf
def R(kind,i): return f"customers/{CID}/{kind}/{i}"
def post(ops):
    body={"mutateOperations":ops,"partialFailure":False}
    req=urllib.request.Request(f"https://googleads.googleapis.com/v22/customers/{CID}/googleAds:mutate",data=json.dumps(body).encode(),method="POST",
        headers={"Authorization":"Bearer "+token(),"login-customer-id":LOGIN,"Content-Type":"application/json"})
    try: return 200, json.load(urllib.request.urlopen(req))
    except urllib.error.HTTPError as e: return e.code, e.read().decode()[:4000]
if MODE=="shared":
    ops=[{"sharedSetOperation":{"create":{"resourceName":R("sharedSets",-1),"name":"AS | Shared negatives","type":"NEGATIVE_KEYWORDS"}}}]
    ops+=[{"sharedCriterionOperation":{"create":{"sharedSet":R("sharedSets",-1),"keyword":{"text":n,"matchType":"PHRASE"}}}} for n in shared]
    c,res=post(ops); print(c, json.dumps(res)[:600] if c==200 else res); sys.exit()
def campaign_ops(mk, shared_set_rn):
    lang=LANG[mk]; ops=[]; n=[-100]
    def tid():
        n[0]-=1; return n[0]
    b=R("campaignBudgets",-1); camp=R("campaigns",-2)
    ops.append({"campaignBudgetOperation":{"create":{"resourceName":b,"name":f"S-{mk} | Non-brand","amountMicros":str(BUDGET[mk]*1_000_000),"deliveryMethod":"STANDARD","explicitlyShared":False}}})
    ops.append({"campaignOperation":{"create":{"resourceName":camp,"name":f"S-{mk} | Non-brand","status":"PAUSED","advertisingChannelType":"SEARCH",
        "campaignBudget":b,"manualCpc":{"enhancedCpcEnabled":False},
        "networkSettings":{"targetGoogleSearch":True,"targetSearchNetwork":False,"targetContentNetwork":False,"targetPartnerSearchNetwork":False},
        "geoTargetTypeSetting":{"positiveGeoTargetType":"PRESENCE","negativeGeoTargetType":"PRESENCE"},
        "containsEuPoliticalAdvertising":"DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING"}}})
    ops.append({"campaignCriterionOperation":{"create":{"campaign":camp,"location":{"geoTargetConstant":f"geoTargetConstants/{GEO[mk]}"}}}})
    for l in (lang,"en"): ops.append({"campaignCriterionOperation":{"create":{"campaign":camp,"language":{"languageConstant":f"languageConstants/{LC[l]}"}}}})
    ops.append({"campaignSharedSetOperation":{"create":{"campaign":camp,"sharedSet":shared_set_rn}}})
    groups=collections.OrderedDict()
    for r in rows:
        if r['campaign']==f"S-{mk} | Non-brand": groups.setdefault(r['ad_group'],[]).append(r)
    for ag,rs in groups.items():
        cat,theme=ag.split(" | ")[0],ag.split(" | ")[1]; l=rs[0]['language']
        g=R("adGroups",tid())
        ops.append({"adGroupOperation":{"create":{"resourceName":g,"campaign":camp,"name":ag,"status":"ENABLED","type":"SEARCH_STANDARD",
            "cpcBidMicros":str(int(float(rs[0]['ad_group_max_cpc_sek'])*1_000_000))}}})
        for r in rs:
            for m in ("EXACT","PHRASE"):
                ops.append({"adGroupCriterionOperation":{"create":{"adGroup":g,"status":"ENABLED","keyword":{"text":r['keyword'],"matchType":m}}}})
        negs=[]
        if cat in("Earrings","Rings"): negs+=MEN[l]
        if cat=="Earrings": negs+=EAR[l]
        if cat=="Rings": negs+=RING[l]
        for nk in negs:
            assert not any(re.search(r'(^| )'+re.escape(nk)+r'( |$)',r['keyword']) for r in rs),(nk,ag)
            ops.append({"adGroupCriterionOperation":{"create":{"adGroup":g,"negative":True,"keyword":{"text":nk,"matchType":"PHRASE"}}}})
        h,d,p=build(cat,theme,l,mk)
        ops.append({"adGroupAdOperation":{"create":{"adGroup":g,"status":"ENABLED","ad":{"finalUrls":[rs[0]['final_url']],
            "responsiveSearchAd":{"headlines":[{"text":x} for x in h],"descriptions":[{"text":x} for x in d],"path1":p}}}}})
    pre={"sv":"/sv","da":"/da","de":"/de","nl":"/nl"}[lang]
    for txt,slug in SITE[lang]:
        a=R("assets",tid()); url=f"https://anderssonstone.com{pre}/pages/conflict-free-diamonds" if slug=="CF" else f"https://anderssonstone.com{pre}/collections/{slug}"
        ops.append({"assetOperation":{"create":{"resourceName":a,"finalUrls":[url],"sitelinkAsset":{"linkText":txt}}}})
        ops.append({"campaignAssetOperation":{"create":{"campaign":camp,"asset":a,"fieldType":"SITELINK"}}})
    for txt in CALL[lang]:
        a=R("assets",tid())
        ops.append({"assetOperation":{"create":{"resourceName":a,"calloutAsset":{"calloutText":txt}}}})
        ops.append({"campaignAssetOperation":{"create":{"campaign":camp,"asset":a,"fieldType":"CALLOUT"}}})
    return ops
if MODE=="plan":
    tot=1+len(shared)
    for mk in GEO:
        o=campaign_ops(mk,"customers/x/sharedSets/1"); tot+=len(o)
        print(mk,len(o),"ops", collections.Counter(list(x.keys())[0] for x in o))
    print("shared negatives",len(shared),"| total ops",tot); sys.exit()
ss=sys.argv[3]
c,res=post(campaign_ops(MODE,ss)); print(c, json.dumps(res)[:300] if c==200 else res)
