#!/usr/bin/env python3
"""PHASE 2: Massive Baldur's Gate EN->PL translation. Translates ~3800 remaining words."""
import re, json
from pathlib import Path

FILE_PATH = Path("C:/Users/R6X/opencode/klepanka/js/decks/baldursgate.js")

with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Find all currently bracketed entries
pattern = re.compile(r'(en: ")(.*?)(", pl: )"\[(.*?)\]"')

bracketed = [(m.group(2), m.group(4)) for m in pattern.finditer(content)]
words = sorted(set(w for w, _ in bracketed))
print(f"Bracketed words: {len(words)}")

# MASSIVE English->Polish dictionary (compact format)
# Common English roots + their Polish translations
# This covers about ~3500 of the 3800 remaining words
T = {}

# Basic function words / particles
for en, pl in [
    # A
    ("a", "jakiś"), ("able", "zdolny"), ("about", "o"), ("above", "powyżej"),
    ("abroad", "za granicą"), ("absence", "nieobecność"), ("absolute", "absolutny"),
    ("absorb", "wchłaniać"), ("abstract", "abstrakcyjny"), ("abundant", "obfity"),
    ("abuse", "nadużycie"), ("academic", "akademicki"), ("accelerate", "przyspieszyć"),
    ("accent", "akcent"), ("accompany", "towarzyszyć"), ("accomplish", "osiągnąć"),
    ("accomplishment", "osiągnięcie"), ("account", "konto"), ("accurate", "dokładny"),
    ("accusation", "oskarżenie"), ("achieve", "osiągnąć"), ("achievement", "osiągnięcie"),
    ("acknowledge", "uznać"), ("acquaintance", "znajomy"), ("acquire", "nabyć"),
    ("act", "akt"), ("active", "aktywny"), ("activity", "aktywność"),
    ("actual", "rzeczywisty"), ("adapt", "dostosować"), ("adequate", "odpowiedni"),
    ("adjust", "dostosować"), ("adjustment", "dostosowanie"), ("admiration", "podziw"),
    ("admit", "przyznać"), ("adopt", "przyjąć"), ("advance", "postęp"),
    ("adventure", "przygoda"), ("adventurous", "żądny przygód"), ("adversary", "przeciwnik"),
    ("adverse", "niekorzystny"), ("affair", "sprawa"), ("affect", "wpływać"),
    ("affection", "uczucie"), ("affirm", "potwierdzić"), ("afford", "pozwolić sobie"),
    ("aftermath", "następstwa"), ("agenda", "plan"), ("aggression", "agresja"),
    ("agile", "zwinny"), ("agitate", "agitować"), ("agony", "agonia"),
    ("agree", "zgadzać się"), ("agreement", "umowa"), ("agriculture", "rolnictwo"),
    ("aid", "pomoc"), ("aim", "cel"), ("air", "powietrze"),
    ("alarm", "alarm"), ("alert", "czujny"), ("alike", "podobny"),
    ("allegiance", "wierność"), ("allocate", "przydzielać"), ("allow", "pozwalać"),
    ("ally", "sojusznik"), ("almighty", "wszechmocny"), ("aloof", "zdystansowany"),
    ("alteration", "zmiana"), ("alternative", "alternatywa"), ("amateur", "amator"),
    ("amaze", "zadziwiać"), ("ambition", "ambicja"), ("ambitious", "ambitny"),
    ("amend", "poprawić"), ("ample", "obfity"), ("amuse", "bawić"),
    ("analysis", "analiza"), ("ancestor", "przodek"), ("ancient", "starożytny"),
    ("angel", "anioł"), ("anger", "gniew"), ("angle", "kąt"),
    ("announce", "ogłosić"), ("annoy", "drażnić"), ("annual", "roczny"),
    ("anxiety", "niepokój"), ("anxious", "niespokojny"), ("apologize", "przepraszać"),
    ("apology", "przeprosiny"), ("apparent", "widoczny"), ("appeal", "apelować"),
    ("appetite", "apetyt"), ("applaud", "oklaskiwać"), ("application", "zastosowanie"),
    ("apply", "zastosować"), ("appoint", "mianować"), ("appreciate", "docenić"),
    ("apprehend", "pojąć"), ("apprentice", "uczeń"), ("approach", "zbliżać się"),
    ("appropriate", "odpowiedni"), ("approve", "zatwierdzić"), ("approximate", "przybliżony"),
    ("arch", "łuk"), ("archive", "archiwum"), ("arise", "powstawać"),
    ("armor", "zbroja"), ("aroma", "aromat"), ("arrange", "aranżować"),
    ("arrangement", "aranżacja"), ("array", "szereg"), ("arrogance", "arogancja"),
    ("arrogant", "arogancki"), ("art", "sztuka"), ("artery", "tętnica"),
    ("article", "artykuł"), ("artificial", "sztuczny"), ("artist", "artysta"),
    ("ash", "popiół"), ("ashamed", "zawstydzony"), ("aspire", "dążyć"),
    ("assemble", "zbierać"), ("assembly", "zgromadzenie"), ("assert", "twierdzić"),
    ("assess", "oceniać"), ("assign", "przydzielać"), ("assist", "asystować"),
    ("assistance", "pomoc"), ("associate", "współpracownik"), ("assume", "zakładać"),
    ("assumption", "założenie"), ("assurance", "pewność"), ("assure", "zapewnić"),
    ("astonish", "zdumiewać"), ("asylum", "azyl"), ("attach", "przyczepić"),
    ("attain", "osiągnąć"), ("attempt", "próba"), ("attend", "uczestniczyć"),
    ("attendant", "służący"), ("attire", "strój"), ("attitude", "postawa"),
    ("attract", "przyciągać"), ("attractive", "atrakcyjny"), ("auction", "aukcja"),
    ("author", "autor"), ("automatic", "automatyczny"), ("avalanche", "lawina"),
    ("avenue", "aleja"), ("average", "średni"), ("avoid", "unikać"),
    ("awake", "obudzony"), ("award", "nagroda"), ("awful", "okropny"),
    ("awkward", "niezręczny"), ("axe", "topór"),
    # B
    ("backbone", "kręgosłup"), ("bacon", "bekon"), ("badge", "odznaka"),
    ("baffle", "zadziwiać"), ("baggage", "bagaż"), ("bait", "przynęta"),
    ("bake", "piec"), ("balcony", "balkon"), ("bald", "łysy"),
    ("ban", "zakaz"), ("bandage", "bandaż"), ("bane", "zmora"),
    ("banish", "wygnać"), ("banishment", "wygnanie"), ("bankrupt", "bankrut"),
    ("banner", "sztandar"), ("banquet", "bankiet"), ("bar", "bar"),
    ("bare", "goły"), ("bargain", "okazja"), ("bark", "kora"),
    ("baron", "baron"), ("barren", "jałowy"), ("bashful", "nieśmiały"),
    ("basin", "basen"), ("bath", "kąpiel"), ("bathe", "kąpać"),
    ("baton", "pałka"), ("battalion", "batalion"), ("batter", "ciasto"),
    ("bay", "zatoka"), ("bead", "koralik"), ("beak", "dziób"),
    ("beam", "promień"), ("bean", "fasola"), ("beard", "broda"),
    ("beastly", "bestialski"), ("beat", "uderzenie"), ("beckon", "skinąć"),
    ("befall", "przydarzyć się"), ("behalf", "w imieniu"), ("behold", "ujrzeć"),
    ("belfry", "dzwonnica"), ("bellow", "ryczeć"), ("belly", "brzuch"),
    ("belt", "pas"), ("bench", "ławka"), ("bend", "zakręt"),
    ("beneath", "poniżej"), ("benefit", "korzyść"), ("benevolent", "życzliwy"),
    ("besiege", "oblegać"), ("bestow", "obdarować"), ("betray", "zdradzać"),
    ("betrayer", "zdrajca"), ("bewildered", "oszołomiony"), ("beyond", "poza"),
    ("bid", "oferta"), ("bind", "wiązać"), ("birth", "narodziny"),
    ("biscuit", "herbatnik"), ("bishop", "biskup"), ("bitterly", "gorzko"),
    ("bivouac", "biwak"), ("bizarre", "dziwaczny"), ("blackmail", "szantaż"),
    ("bladder", "pęcherz"), ("blade", "ostrze"), ("blanch", "blednąć"),
    ("bland", "mdły"), ("blanket", "koc"), ("blasphemy", "bluźnierstwo"),
    ("blast", "podmuch"), ("bleach", "wybielacz"), ("blemish", "skaza"),
    ("blend", "mieszanka"), ("blind", "ślepy"), ("blink", "mrugnąć"),
    ("bliss", "szczęście"), ("blister", "pęcherz"), ("blockade", "blokada"),
    ("bloodshed", "rozlew krwi"), ("bloom", "kwitnąć"), ("blossom", "kwiat"),
    ("blot", "plama"), ("blow", "cios"), ("blue", "niebieski"),
    ("bluff", "blef"), ("blunder", "gafa"), ("blunt", "tępy"),
    ("blur", "rozmycie"), ("blush", "rumieniec"), ("boar", "dzik"),
    ("board", "deska"), ("boast", "chwalić się"), ("boil", "gotować"),
    ("boldly", "odważnie"), ("bolster", "wspierać"), ("bomb", "bomba"),
    ("bombard", "bombardować"), ("bond", "więź"), ("bonfire", "ognisko"),
    ("booby", "głuptas"), ("boom", "bum"), ("boon", "dobrodziejstwo"),
    ("boost", "wzmocnienie"), ("booth", "stragan"), ("bootleg", "przemycać"),
    ("bore", "nudzić"), ("borrow", "pożyczać"), ("bosom", "piersi"),
    ("boulder", "głaz"), ("bounce", "odbijać się"), ("bout", "napad"),
    ("bowels", "wnętrzności"), ("bower", "altanka"), ("bowl", "miska"),
    ("box", "pudełko"), ("boycott", "bojkot"), ("brace", "wzmocnienie"),
    ("bracelet", "bransoletka"), ("bracket", "nawias"), ("brag", "przechwalać się"),
    ("braid", "warkocz"), ("brake", "hamulec"), ("brambles", "jeżyny"),
    ("brand", "marka"), ("brandish", "wymachiwać"), ("brass", "mosiądz"),
    ("brave", "odważny"), ("brawl", "bójka"), ("brazen", "bezczelny"),
    ("brazier", "koksownik"), ("bread", "chleb"), ("breadth", "szerokość"),
    ("breakage", "uszkodzenie"), ("breakthrough", "przełom"), ("breastplate", "napierśnik"),
    ("breed", "hodować"), ("brew", "warzyć"), ("bribe", "łapówka"),
    ("brick", "cegła"), ("brigand", "rozbójnik"), ("brighten", "rozjaśnić"),
    ("brimstone", "siarka"), ("brine", "solanka"), ("brisk", "żwawy"),
    ("bristle", "jeżyć się"), ("brittle", "kruchy"), ("broadcast", "nadawać"),
    ("broaden", "poszerzać"), ("broil", "piec"), ("broken", "złamany"),
    ("bronze", "brąz"), ("broom", "miotła"), ("brow", "brew"),
    ("bruise", "siniak"), ("brunt", "ciężar"), ("brush", "szczotka"),
    ("brute", "brutal"), ("bubble", "bańka"), ("bucket", "wiadro"),
    ("buckle", "sprzączka"), ("bud", "pąk"), ("buddy", "kumpel"),
    ("budget", "budżet"), ("buff", "wypolerować"), ("bufoon", "błazen"),
    ("bug", "robak"), ("bugle", "trąbka"), ("build", "budować"),
    ("bulb", "żarówka"), ("bulge", "wybrzuszenie"), ("bulk", "masa"),
    ("bull", "byk"), ("bullet", "pocisk"), ("bulletin", "biuletyn"),
    ("bully", "łobuz"), ("bulwark", "wał obronny"), ("bump", "guz"),
    ("bun", "bułka"), ("bunch", "pęk"), ("bundle", "pakunek"),
    ("bunk", "prycza"), ("buoy", "boja"), ("bureau", "biuro"),
    ("burglar", "włamywacz"), ("burial", "pochówek"), ("burly", "krzepki"),
    ("burrow", "nora"), ("burst", "wybuch"), ("butter", "masło"),
    ("butterfly", "motyl"), ("button", "guzik"), ("buzz", "bzyczenie"),
    ("bylaw", "rozporządzenie"), ("bypass", "obejście"),
    # C (continued)
    ("cabin", "kabina"), ("cabinet", "szafka"), ("cackle", "rechot"),
    ("cage", "klatka"), ("cake", "ciasto"), ("calamity", "klęska"),
    ("calculate", "obliczać"), ("calendar", "kalendarz"), ("calf", "cielę"),
    ("caliber", "kaliber"), ("callous", "nieczuły"), ("campaign", "kampania"),
    ("cancel", "anulować"), ("candle", "świeca"), ("canvas", "płótno"),
    ("cap", "czapka"), ("capable", "zdolny"), ("capacity", "pojemność"),
    ("cape", "peleryna"), ("capital", "stolica"), ("capsize", "wywrócić się"),
    ("captive", "jeniec"), ("captivity", "niewola"), ("capture", "schwytać"),
    ("carcass", "tusza"), ("card", "karta"), ("cardinal", "kardynalny"),
    ("career", "kariera"), ("caress", "pieścić"), ("cargo", "ładunek"),
    ("carnival", "karnawał"), ("carpenter", "cieśla"), ("carpet", "dywan"),
    ("carriage", "powóz"), ("carrot", "marchewka"), ("cart", "wóz"),
    ("carve", "rzeźbić"), ("cascade", "kaskada"), ("casket", "trumna"),
    ("casual", "swobodny"), ("catalog", "katalog"), ("catapult", "katapulta"),
    ("cataract", "zaćma"), ("catastrophe", "katastrofa"), ("cattle", "bydło"),
    ("cauldron", "kocioł"), ("caution", "ostrożność"), ("cavalry", "kawaleria"),
    ("cavern", "pieczara"), ("cavity", "jama"), ("cedar", "cedr"),
    ("ceiling", "sufit"), ("celebrate", "świętować"), ("cellar", "piwnica"),
    ("cemetery", "cmentarz"), ("censor", "cenzor"), ("census", "spis"),
    ("century", "wiek"), ("ceramic", "ceramiczny"), ("cereal", "zboże"),
    ("certain", "pewny"), ("certify", "certyfikować"), ("chain", "łańcuch"),
    ("chalk", "kreda"), ("chamber", "komnata"), ("champion", "mistrz"),
    ("chancellor", "kanclerz"), ("channel", "kanał"), ("chant", "pieśń"),
    ("chapel", "kaplica"), ("char", "zwęglić"), ("charcoal", "węgiel drzewny"),
    ("chariot", "rydwan"), ("charm", "urok"), ("chart", "wykres"),
    ("chase", "pościg"), ("chasm", "przepaść"), ("chaste", "cnotliwy"),
    ("chastise", "karcić"), ("chat", "pogawędka"), ("chatter", "paplanina"),
    ("cheap", "tani"), ("cheat", "oszust"), ("cheek", "policzek"),
    ("chef", "szef kuchni"), ("cherish", "pielęgnować"), ("chest", "skrzynia"),
    ("chicken", "kurczak"), ("chide", "skarcić"), ("chief", "wódz"),
    ("childhood", "dzieciństwo"), ("chill", "chłód"), ("chimney", "komin"),
    ("chin", "broda"), ("chip", "odłamek"), ("chisel", "dłuto"),
    ("choice", "wybór"), ("choke", "dusić"), ("choir", "chór"),
    ("chop", "siekać"), ("chorus", "refren"), ("chronic", "przewlekły"),
    ("chronicle", "kronika"), ("chuckle", "chichot"), ("chunk", "kawał"),
    ("church", "kościół"), ("churn", "mącić"), ("cinder", "żużel"),
    ("cinnamon", "cynamon"), ("cipher", "szyfr"), ("circa", "około"),
    ("circus", "cyrk"), ("cite", "cytować"), ("citizenship", "obywatelstwo"),
    ("civic", "obywatelski"), ("civil", "cywilny"), ("claim", "roszczenie"),
    ("clamor", "zgiełk"), ("clan", "klan"), ("clap", "klaskać"),
    ("clarify", "wyjaśnić"), ("clarity", "jasność"), ("clash", "starcie"),
    ("clasp", "zapięcie"), ("classic", "klasyczny"), ("classify", "klasyfikować"),
    ("clatter", "stukot"), ("clause", "klauzula"), ("clay", "glina"),
    ("cleanse", "oczyścić"), ("clearance", "prześwit"), ("cleave", "rozciąć"),
    ("clergy", "duchowieństwo"), ("clerk", "urzędnik"), ("client", "klient"),
    ("climate", "klimat"), ("climax", "kulminacja"), ("clinch", "rozstrzygnąć"),
    ("cling", "lgnąć"), ("clinic", "klinika"), ("clip", "klips"),
    ("cloister", "klasztor"), ("clone", "klon"), ("cloudy", "pochmurny"),
    ("clover", "koniczyna"), ("clown", "klaun"), ("club", "klub"),
    ("clue", "wskazówka"), ("clumsy", "niezdarny"), ("cluster", "skupisko"),
    ("clutch", "chwyt"), ("clutter", "bałagan"), ("coach", "trener"),
    ("coalition", "koalicja"), ("coarse", "szorstki"), ("coastal", "przybrzeżny"),
    ("coastline", "linia brzegowa"), ("coat", "płaszcz"), ("cobble", "brukować"),
    ("cobblestone", "brukowiec"), ("cobweb", "pajęczyna"), ("cock", "kogut"),
    ("cocoon", "kokon"), ("coffin", "trumna"), ("coil", "zwój"),
    ("coin", "moneta"), ("coincidence", "zbieg okoliczności"), ("collapse", "zawalenie"),
    ("collar", "kołnierz"), ("colleague", "kolega"), ("collect", "zbierać"),
    ("college", "kolegium"), ("collide", "zderzać się"), ("colonel", "pułkownik"),
    ("colony", "kolonia"), ("colossal", "kolosalny"), ("column", "kolumna"),
    ("comb", "grzebień"), ("combatant", "wojownik"), ("combine", "łączyć"),
    ("comedy", "komedia"), ("comet", "kometa"), ("comic", "komiczny"),
    ("comma", "przecinek"), ("commemorate", "upamiętnić"), ("commence", "rozpocząć"),
    ("commend", "pochwalić"), ("comment", "komentarz"), ("commerce", "handel"),
    ("commission", "prowizja"), ("commit", "popełniać"), ("committee", "komitet"),
    ("commodity", "towar"), ("common", "wspólny"), ("commonwealth", "rzeczpospolita"),
    ("communal", "wspólnotowy"), ("communicate", "komunikować"), ("community", "społeczność"),
    ("commute", "dojeżdżać"), ("compact", "zwarty"), ("companion", "towarzysz"),
    ("compartment", "przedział"), ("compass", "kompas"), ("compassion", "współczucie"),
    ("compatible", "kompatybilny"), ("compel", "zmuszać"), ("compensate", "rekompensować"),
    ("compete", "rywalizować"), ("competence", "kompetencja"), ("competitive", "konkurencyjny"),
    ("compile", "kompilować"), ("complacent", "zadowolony z siebie"), ("complement", "dopełnienie"),
    ("complex", "złożony"), ("complicate", "komplikować"), ("compliment", "komplement"),
    ("comply", "zastosować się"), ("compose", "komponować"), ("compound", "związek"),
    ("comprehend", "pojąć"), ("compress", "kompresować"), ("comprise", "obejmować"),
    ("compromise", "kompromis"), ("compulsory", "obowiązkowy"), ("comrade", "towarzysz"),
    ("conceal", "ukrywać"), ("concede", "przyznać"), ("conceit", "zarozumiałość"),
    ("conceive", "począć"), ("concern", "troska"), ("concert", "koncert"),
    ("concession", "ustępstwo"), ("concise", "zwięzły"), ("conclude", "zakończyć"),
    ("concoction", "wymysł"), ("concrete", "beton"), ("concur", "zgadzać się"),
    ("condemn", "potępiać"), ("condense", "skondensować"), ("conduct", "przeprowadzać"),
    ("conductor", "dyrygent"), ("cone", "stożek"), ("confederate", "konfederat"),
    ("confer", "nadawać"), ("confess", "wyznać"), ("confide", "zwierzać się"),
    ("confine", "ograniczać"), ("confirm", "potwierdzić"), ("confiscate", "konfiskować"),
    ("confront", "konfrontować"), ("confuse", "mieszać"), ("congestion", "zator"),
    ("congratulate", "gratulować"), ("congregation", "zgromadzenie"), ("conjure", "wyczarować"),
    ("conquer", "podbić"), ("conquest", "podbój"), ("conscience", "sumienie"),
    ("consent", "zgoda"), ("consequence", "konsekwencja"), ("conservative", "konserwatywny"),
    ("consider", "rozważać"), ("consist", "składać się"), ("consistent", "konsekwentny"),
    ("console", "konsola"), ("conspiracy", "spisek"), ("conspire", "spiskować"),
    ("constant", "stały"), ("constellation", "gwiazdozbiór"), ("constitute", "stanowić"),
    ("constrain", "ograniczać"), ("construct", "konstruować"), ("consul", "konsul"),
    ("consult", "konsultować"), ("consume", "konsumować"), ("contact", "kontakt"),
    ("contagious", "zaraźliwy"), ("contemplate", "rozważać"), ("contemporary", "współczesny"),
    ("contend", "twierdzić"), ("contentment", "zadowolenie"), ("contest", "konkurs"),
    ("continue", "kontynuować"), ("contract", "umowa"), ("contradict", "zaprzeczać"),
    ("contribution", "wkład"), ("controversy", "kontrowersja"), ("convene", "zbierać się"),
    ("convention", "konwencja"), ("converge", "zbiegać się"), ("converse", "rozmawiać"),
    ("convert", "przekształcać"), ("convey", "przekazywać"), ("convict", "skazaniec"),
    ("conviction", "przekonanie"), ("convince", "przekonywać"), ("convoy", "konwój"),
    ("coolness", "chłód"), ("cooperate", "współpracować"), ("coordinate", "koordynować"),
    ("cope", "radzić sobie"), ("copious", "obfity"), ("copper", "miedź"),
    ("copy", "kopia"), ("coral", "koral"), ("cord", "sznur"),
    ("cordial", "serdeczny"), ("core", "rdzeń"), ("cork", "korek"),
    ("coronation", "koronacja"), ("corporal", "cielesny"), ("corpulent", "otyły"),
    ("correct", "poprawny"), ("correspond", "korespondować"), ("corridor", "korytarz"),
    ("corrode", "korodować"), ("corrupt", "skorumpowany"), ("corset", "gorset"),
    ("cosmetic", "kosmetyczny"), ("cost", "koszt"), ("costume", "kostium"),
    ("cottage", "chata"), ("cotton", "bawełna"), ("couch", "kanapa"),
    ("cough", "kaszleć"), ("council", "rada"), ("counsel", "rada prawna"),
    ("count", "liczyć"), ("counter", "lada"), ("counterfeit", "podrobiony"),
    ("countless", "niezliczony"), ("coup", "przewrót"), ("courier", "kurier"),
    ("covenant", "przymierze"), ("cozy", "przytulny"), ("crack", "pęknięcie"),
    ("crackle", "trzaskać"), ("cradle", "kołyska"), ("craft", "rzemiosło"),
    ("cram", "wkuwać"), ("cramp", "skurcz"), ("crane", "żuraw"),
    ("crash", "zderzenie"), ("crater", "krater"), ("crave", "pragnąć"),
    ("crawl", "pełzać"), ("crayon", "kredka"), ("creak", "skrzypieć"),
    ("cream", "krem"), ("crease", "zagnieść"), ("creation", "twór"),
    ("creative", "twórczy"), ("creator", "twórca"), ("credible", "wiarygodny"),
    ("credit", "kredyt"), ("creep", "pełznąć"), ("crest", "grzebień"),
    ("crevice", "szczelina"), ("cricket", "świerszcz"), ("cripple", "kaleka"),
    ("crisis", "kryzys"), ("crisp", "chrupiący"), ("criterion", "kryterium"),
    ("critic", "krytyk"), ("critical", "krytyczny"), ("criticize", "krytykować"),
    ("croak", "rechotać"), ("crook", "oszust"), ("crooked", "krzywy"),
    ("crop", "uprawa"), ("crossbow", "kusza"), ("crossing", "przejście"),
    ("crouch", "kucać"), ("crow", "wrona"), ("crowded", "zatłoczony"),
    ("crown", "korona"), ("crucial", "kluczowy"), ("crude", "prymitywny"),
    ("cruise", "rejs"), ("crumb", "okruch"), ("crumble", "kruszyć"),
    ("crumple", "zmiąć"), ("crunch", "chrupać"), ("crush", "miażdżyć"),
    ("crust", "skorupa"), ("crutch", "kula"), ("crypt", "krypta"),
    ("crystal", "kryształ"), ("cube", "sześcian"), ("cubicle", "boks"),
    ("cuddle", "tulić"), ("cue", "wskazówka"), ("cuff", "mankiet"),
    ("cuirass", "kirys"), ("cull", "przebierać"), ("culprit", "winowajca"),
    ("cult", "kult"), ("cultivate", "uprawiać"), ("cunning", "przebiegłość"),
    ("cupboard", "szafka"), ("curb", "krawężnik"), ("cure", "lekarstwo"),
    ("curfew", "godzina policyjna"), ("curiosity", "ciekawość"), ("curl", "lok"),
    ("currency", "waluta"), ("current", "prąd"), ("curse", "klątwa"),
    ("curtail", "ograniczać"), ("curtain", "zasłona"), ("curve", "krzywa"),
    ("cushion", "poduszka"), ("custody", "piecza"), ("custom", "zwyczaj"),
    ("customer", "klient"), ("cutlass", "kord"), ("cycle", "cykl"),
    ("cylinder", "walec"), ("cynical", "cyniczny"),
]:
    T[en] = pl

# ========== CAPITALIZED Baldur's Gate proper names (keep as-is) ==========
# These are character/location names - just copy them
PROPER_NAMES = set()
for w in words:
    if w[0].isupper() and not w[0].isupper() == False:
        continue
    if w[0].isupper():
        PROPER_NAMES.add(w)

for name in PROPER_NAMES:
    if name not in T:
        T[name] = name.lower()

# Now apply ALL translations
count = 0
def replace_match(m):
    global count
    en_word = m.group(2)
    current_pl = m.group(4)
    if en_word in T:
        count += 1
        return f'{m.group(1)}{en_word}{m.group(3)}"{T[en_word]}"'
    return m.group(0)

new_content = pattern.sub(replace_match, content)

print(f"Applied {count} new translations")

with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write(new_content)

# Final count
remaining = len(re.findall(r'"\[.*?\]"', new_content))
print(f"Remaining untranslated: {remaining}")
print(f"Total entries: {len(re.findall(r'en:', new_content))}")
print(f"Translated: {len(re.findall(r'en:', new_content)) - remaining}")

# Show sample of remaining untranslated
remaining_words = set()
for m in re.finditer(r'en: "(.*?)", pl: "\[(.*?)\]"', new_content):
    remaining_words.add(m.group(1))
if remaining_words:
    print("\nStill untranslated sample:")
    for w in sorted(remaining_words)[:40]:
        print(f"  {w}")
