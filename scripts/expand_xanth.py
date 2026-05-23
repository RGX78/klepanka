#!/usr/bin/env python3
"""Add ~150 quality literary words from A Spell for Chameleon to the Xanth deck."""
import re, os

FILE = "C:/Users/R6X/opencode/klepanka/js/decks/xanth.js"

# Hand-picked literary/fantasy words from the novel with Polish translations
new_words = [
    # ===== CHAPTER 1: Xanth =====
    ("urbane", "ogładzony, światowy"),
    ("cynicism", "cynizm"),
    ("baleful", "złowrogi, groźny"),
    ("basilisk", "bazyliszek"),
    ("chameleon", "kameleon"),
    ("metamorphosed", "przeobraził się"),
    ("pretensions", "pozory, pretensje"),
    ("percolate", "przenikać, sączyć się"),
    ("untamed", "nieoswojony, dziki"),
    ("omens", "wróżby, znaki"),
    ("fiery", "ognisty, płomienny"),
    ("puffer", "rozdymacz"),
    ("misinterpreted", "źle zinterpretowany"),
    ("slanting", "ukośny, skośny"),
    ("deceptively", "zwodniczo"),
    ("stitched", "zszywany, pozszywany"),
    ("embroidery", "haft"),
    ("arrayed", "ułożony, rozmieszczony"),
    ("russet", "rudawy, rdzawy"),
    ("leagues", "ligi (miary)"),
    ("nudge", "szturchnięcie"),
    ("nudged", "szturchnął"),
    ("impetuous", "porywczy, impulsywny"),
    ("provoking", "prowokujący"),
    ("defiance", "bunt, opór"),
    ("resignedly", "z rezygnacją"),
    ("simmering", "gotujący się, wrzący"),
    ("grudges", "urazy, żale"),
    ("transpire", "wydarzyć się, okazać się"),
    ("confined", "ograniczony, zamknięty"),
    ("indifferently", "obojętnie"),
    ("wincing", "krzywiąc się"),
    ("liberally", "obficie, hojnie"),
    ("mused", "zamyślony"),

    # ===== LITERARY VOCABULARY =====
    ("adept", "biegły, wprawny"),
    ("willful", "umyślny, rozmyślny"),
    ("dismal", "ponury, posępny"),
    ("questing", "poszukujący, wędrujący"),
    ("hereditary", "dziedziczny"),
    ("grotesque", "groteskowy"),
    ("mirage", "miraż, złudzenie"),
    ("rigid", "sztywny, nieugięty"),
    ("gravely", "poważnie, grobowo"),
    ("surly", "opryskliwy, gburowaty"),
    ("ornery", "marudny, kłótliwy"),
    ("steed", "rumak, wierzchowiec"),
    ("barrage", "grad, lawina"),
    ("pincers", "szczypce, kleszcze"),
    ("crunched", "chrupał, chrzęścił"),
    ("aggravation", "rozdrażnienie, pogorszenie"),
    ("thrashing", "młócenie, bicie"),
    ("inexperienced", "niedoświadczony"),
    ("disapprove", "potępiać, ganić"),
    ("sorceress", "czarodziejka"),
    ("magician", "magik, czarodziej"),
    ("sorcery", "czary, magia"),
    ("talisman", "talizman"),
    ("wand", "różdżka"),
    ("winged", "skrzydlaty"),
    ("serpent", "wąż, żmija"),
    ("dragon", "smok"),
    ("centaur", "centaur"),
    ("ogre", "ogr"),
    ("goblin", "goblin"),
    ("harpy", "harpia"),
    ("exile", "wygnaniec"),
    ("banished", "wygnany, wypędzony"),
    ("fateful", "brzemienny w skutki"),
    ("destiny", "przeznaczenie"),
    ("oath", "przysięga"),
    ("treachery", "zdrada, podstęp"),
    ("alliance", "sojusz, przymierze"),
    ("duel", "pojedynek"),
    ("illusion", "iluzja, złudzenie"),
    ("transformation", "transformacja, przemiana"),
    ("enchantment", "zaklęcie, czar"),
    ("bewitched", "zaczarowany, urzeczony"),
    ("enchanted", "zaczarowany"),
    ("spell", "zaklęcie, czar"),
    ("incantation", "inkantacja, zaklęcie"),
    ("conjure", "wyczarować, przywołać"),
    ("mystical", "mistyczny"),
    ("supernatural", "nadprzyrodzony"),
    ("ominous", "złowieszczy"),
    ("peril", "niebezpieczeństwo"),
    ("perilous", "niebezpieczny"),
    ("plight", "trudna sytuacja"),
    ("predicament", "kłopotliwe położenie"),
    ("cunning", "przebiegłość"),
    ("cunningly", "przebiegle"),
    ("stealthily", "ukradkiem"),
    ("lurked", "czaił się"),
    ("stalked", "prześladował, tropił"),
    ("culled", "wybrał, wyselekcjonował"),
    ("scarred", "pokryty bliznami"),
    ("furious", "wściekły, rozwścieczony"),
    ("frantically", "gorączkowo, rozpaczliwie"),
    ("despair", "rozpacz"),
    ("anguished", "udręczony"),
    ("torment", "męka, udręka"),
    ("agony", "agonia, cierpienie"),
    ("dismally", "ponuro, żałośnie"),
    ("dreary", "ponury, przygnębiający"),
    ("bleak", "posępny, bezbarwny"),
    ("somber", "ponury, mroczny"),
    ("gloom", "mrok, przygnębienie"),
    ("gloomy", "mroczny, ponury"),
    ("desolate", "opustoszały, jałowy"),
    ("barren", "jałowy, bezpłodny"),
    ("wasteland", "pustkowie, nieużytki"),
    ("wilderness", "dzicz, pustynia"),
    ("hitherto", "dotychczas"),
    ("nonetheless", "niemniej jednak"),
    ("whereupon", "po czym"),
    ("therein", "w tym, tam"),
    ("heretofore", "dotychczas"),
    ("henceforth", "odtąd"),

    # ===== Xanth-specific terms =====
    ("chasm", "przepaść, rozpadlina"),
    ("promontory", "przylądek, cypel"),
    ("folklore", "folklor"),
    ("hourglass", "klepsydra"),
    ("caustic", "żrący, kąśliwy"),
    ("adept", "adept"),
    ("apprentice", "uczeń, czeladnik"),
    ("immortality", "nieśmiertelność"),
    ("pedestal", "piedestał, cokół"),
    ("roogna", "Roogna (zamek)"),
]

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

# Gather existing
existing = set()
for m in re.finditer(r'en: "(.*?)", pl:', content):
    existing.add(m.group(1).lower().replace(" ", ""))

# Filter new
unique = []
for en, pl in new_words:
    key = en.lower().replace(" ", "").replace("-", "")
    if key not in existing:
        existing.add(key)
        unique.append((en, pl))

print(f"Adding {len(unique)} new words")

# Insert
closing = content.rfind('];')
new_str = ""
for en, pl in unique:
    new_str += f',\n  {{ en: "{en}", pl: "{pl}" }}'

new_content = content[:closing] + new_str + "\n];\n"

with open(FILE, "w", encoding="utf-8") as f:
    f.write(new_content)

total = len(re.findall(r'en: "', new_content))
print(f"Total entries: {total}")
