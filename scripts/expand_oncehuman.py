#!/usr/bin/env python3
"""Expand Once Human deck with wiki terms from wikily.gg."""
import re

new_words = [
    # ===== CREATURES =====
    ("bear", "niedźwiedź"),
    ("bear cub", "niedźwiadek"),
    ("boar", "dzik"),
    ("boar piglet", "mały dzik"),
    ("buck", "rogacz"),
    ("capybara", "kapibara"),
    ("crocodile", "krokodyl"),
    ("crocodile hatchling", "mały krokodyl"),
    ("doe", "łania"),
    ("ewe", "owca"),
    ("fawn", "jelonek"),
    ("flamingo", "flaming"),
    ("fox", "lis"),
    ("leopard", "lampart"),
    ("lamb", "jagnię"),
    ("little capybara", "mała kapibara"),
    ("little flamingo", "mały flaming"),
    ("little leopard", "mały lampart"),
    ("polar bear", "niedźwiedź polarny"),

    # ===== ITEM CATEGORIES =====
    ("access permit", "zezwolenie dostępu"),
    ("ammo", "amunicja"),
    ("battle pass token", "token karnetu bojowego"),
    ("blueprint fragments", "fragmenty planów"),
    ("blueprints", "plany"),
    ("bonus", "bonus"),
    ("bottoms", "dolna część garderoby"),
    ("calibration blueprints", "plany kalibracji"),
    ("charm", "amulet"),
    ("collection", "kolekcja"),
    ("consumable", "materiał eksploatacyjny"),
    ("cradle charms", "ozdoby kolebki"),
    ("decorative item", "przedmiot dekoracyjny"),
    ("deviations", "odchylenia"),
    ("door card", "karta dostępu"),
    ("emblem", "godło"),
    ("expression", "ekspresja"),
    ("eyewear", "okulary"),
    ("facewear", "nakrycie twarzy"),
    ("facilities", "obiekty"),
    ("fashion trial card", "karta próbna mody"),
    ("feed", "pasza"),
    ("festival item", "przedmiot festiwalowy"),
    ("food", "jedzenie"),
    ("formula", "receptura"),
    ("fuel", "paliwo"),
    ("gear", "ekwipunek"),
    ("gear mod", "modyfikacja ekwipunku"),
    ("gloves", "rękawice"),
    ("gun", "broń palna"),
    ("hairstyle", "fryzura"),
    ("headwear", "nakrycie głowy"),
    ("impasse material", "materiał specjalny"),
    ("large fish", "duża ryba"),
    ("makeup", "makijaż"),
    ("material", "materiał"),
    ("materials", "materiały"),
    ("medal", "medal"),
    ("medium fish", "średnia ryba"),
    ("melee weapon", "broń biała"),
    ("mission item", "przedmiot misji"),
    ("motorcycle", "motocykl"),
    ("off-roader", "pojazd terenowy"),
    ("pickup truck", "pickup"),
    ("plate trailer", "przyczepa"),
    ("profiles", "profile"),
    ("seeds", "nasiona"),
    ("shoes", "buty"),
    ("small fish", "mała ryba"),
    ("survival device", "urządzenie przetrwania"),
    ("tactical item", "przedmiot taktyczny"),
    ("tops", "górna część garderoby"),
    ("trial card", "karta próbna"),
    ("voucher", "talon"),
    ("weapon accessory", "akcesorium broni"),
    ("weapon charm", "amulet broni"),
    ("weapon skin", "skórka broni"),
    ("weapons", "broń"),

    # ===== WEAPON TYPES =====
    ("crossbow", "kusza"),
    ("shotgun", "strzelba"),
    ("sniper", "snajperka"),
    ("assault rifle", "karabin szturmowy"),
    ("pistol", "pistolet"),
    ("submachine gun", "pistolet maszynowy"),
    ("rifle", "karabin"),
    ("bow", "łuk"),
    ("melee", "walka wręcz"),
    ("light machine gun", "lekki karabin maszynowy"),

    # ===== MOD KEYWORDS =====
    ("burn", "ogień"),
    ("power surge", "przepięcie"),
    ("frost vortex", "mroźny wir"),
    ("the bull's eye", "bycze oko"),
    ("fortress warfare", "wojna forteczna"),
    ("unstable bomber", "niestabilny bombowiec"),
    ("fast gunner", "szybki strzelec"),
    ("bounce", "rykoszet"),
    ("shrapnel", "szrapnel"),
    ("normal", "zwykły"),

    # ===== GAME CONCEPTS =====
    ("memetics", "memetyka"),
    ("cradle", "kolebka"),
    ("blueprint", "plan"),
    ("stardust", "gwiezdny pył"),
    ("eternaland", "eternaland"),
    ("tech workbench", "warsztat techniczny"),
    ("build planner", "planer budowy"),
    ("crescent", "półksiężyc"),
    ("downstar", "downstar"),
    ("mirror", "lustro"),
    ("resistance", "odporność"),
    ("resonance", "rezonans"),
    ("wild", "dziki"),
    ("phantasmal", "fantomowy"),
    ("shiny", "lśniący"),
    ("mod dust", "pył modyfikacyjny"),
    ("mod selection crate", "skrzynia z modyfikacjami"),
    ("suffix mod crate", "skrzynia z przyrostkami"),

    # ===== MORE GAME TERMS =====
    ("extraction permit", "zezwolenie wydobycia"),
    ("refinery permit", "zezwolenie rafinerii"),
    ("access card", "karta dostępu"),
    ("season pass", "karnet sezonowy"),
    ("premium", "premium"),
    ("crafting", "rzemiosło"),
    ("planner", "planer"),
    ("calculator", "kalkulator"),
    ("cosmetic", "kosmetyk"),
    ("deviation", "odchylenie"),
    ("anomaly", "anomalia"),
    ("artifact", "artefakt"),
    ("mutant", "mutant"),
]

deck_path = "C:/Users/R6X/opencode/klepanka/js/decks/oncehuman.js"
with open(deck_path, "r", encoding="utf-8") as f:
    content = f.read()

existing = set()
for m in re.finditer(r'en: "(.*?)", pl:', content):
    existing.add(m.group(1).lower().replace(" ", "").replace("-", ""))

# Filter new words
unique_new = []
for en, pl in new_words:
    key = en.lower().replace(" ", "").replace("-", "")
    if key not in existing:
        existing.add(key)
        unique_new.append((en, pl))

print(f"New unique words: {len(unique_new)}")

# Insert new entries before closing bracket
closing = content.rfind('];')
new_entries = ""
for en, pl in unique_new:
    new_entries += f',\n  {{ en: "{en}", pl: "{pl}" }}'

new_content = content[:closing] + new_entries + "\n];\n"

with open(deck_path, "w", encoding="utf-8") as f:
    f.write(new_content)

total = len(re.findall(r'en: "', new_content))
print(f"Total entries: {total}")
