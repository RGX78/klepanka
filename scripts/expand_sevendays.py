#!/usr/bin/env python3
"""Expand 7 Days to Die deck with all wiki terms - EN->PL translations."""

import os, re

# New words extracted from 7daystodie.wiki.gg
new_words = [
    # ===== ZOMBIE NAMES =====
    ("arlene", "Arlene"),
    ("marlene", "Marlene"),
    ("party girl", "imprezowiczka"),
    ("nurse", "pielęgniarka"),
    ("businessman", "biznesmen"),
    ("joe", "Joe"),
    ("steve", "Steve"),
    ("tom clark", "Tom Clark"),
    ("burnt zombie", "spalony zombie"),
    ("spider zombie", "pajęczy zombie"),
    ("boe", "Boe"),
    ("moe", "Moe"),
    ("yo", "Yo"),
    ("janitor", "woźny"),
    ("inmate", "więzień"),
    ("utility worker", "pracownik techniczny"),
    ("darlene", "Darlene"),
    ("lab worker", "pracownik laboratorium"),
    ("hazmat zombie", "zombie hazmat"),
    ("crawler", "pełzacz"),
    ("thug", "bandzior"),
    ("soldier", "żołnierz"),
    ("wight", "widmo"),
    ("biker", "motocyklista"),
    ("lumberjack", "drwal"),
    ("tourist", "turysta"),
    ("bowler", "kręglarz"),
    ("big mama", "gruba mama"),
    ("cop zombie", "zombie glina"),
    ("screamer", "krzykacz"),
    ("demolition zombie", "zombie burzyciel"),
    ("rancher", "ranczer"),
    ("chuck", "Chuck"),
    ("mutated zombie", "zmutowany zombie"),
    ("feral", "zdziczały"),
    ("radiated", "napromieniowany"),
    ("charged", "naładowany"),
    ("infernal", "piekielny"),

    # ===== ZOMBIE ANIMALS =====
    ("zombie dog", "zombie pies"),
    ("zombie vulture", "zombie sęp"),
    ("dire wolf", "wilk straszliwy"),
    ("zombie bear", "zombie niedźwiedź"),
    ("grace", "Grace"),
    ("boar", "dzik"),

    # ===== WEAPONS (MELEE) =====
    ("wooden club", "drewniana pałka"),
    ("baseball bat", "kij baseballowy"),
    ("steel club", "stalowa pałka"),
    ("candy cane club", "pałka z laseczki cukrowej"),
    ("stone sledgehammer", "kamienny młot"),
    ("iron sledgehammer", "żelazny młot"),
    ("steel sledgehammer", "stalowy młot"),
    ("stone spear", "kamienna włócznia"),
    ("iron spear", "żelazna włócznia"),
    ("steel spear", "stalowa włócznia"),
    ("bone knife", "nóż z kości"),
    ("hunting knife", "nóż myśliwski"),
    ("machete", "maczeta"),
    ("candy cane knife", "nóż z laseczki cukrowej"),
    ("knuckle wraps", "owijki na pięści"),
    ("iron knuckles", "żelazne kastety"),
    ("steel knuckles", "stalowe kastety"),
    ("pipe baton", "rurowa pałka"),
    ("stun baton", "pałka ogłuszająca"),
    ("wooden bow", "drewniany łuk"),
    ("primitive bow", "prymitywny łuk"),
    ("iron crossbow", "żelazna kusza"),
    ("compound bow", "łuk bloczkowy"),
    ("compound crossbow", "kusza bloczkowa"),

    # ===== WEAPONS (RANGED) =====
    ("pipe shotgun", "rurowa strzelba"),
    ("double barrel shotgun", "dwururka"),
    ("pump shotgun", "pompka"),
    ("auto shotgun", "strzelba automatyczna"),
    ("pipe rifle", "karabin rurowy"),
    ("hunting rifle", "karabin myśliwski"),
    ("lever-action rifle", "karabin dźwigniowy"),
    ("sniper rifle", "karabin snajperski"),
    ("pipe machine gun", "rurowy karabin maszynowy"),
    ("ak-47", "AK-47"),
    ("tactical assault rifle", "taktyczny karabin szturmowy"),
    ("m60", "M60"),
    ("pipe pistol", "pistolet rurowy"),
    ("pistol", "pistolet"),
    ("44 magnum", ".44 Magnum"),
    ("44 desert vulture", ".44 Desert Vulture"),
    ("smg-5", "SMG-5"),

    # ===== EXPLOSIVES & THROWABLES =====
    ("rocket launcher", "wyrzutnia rakiet"),
    ("exploding arrow", "wybuchająca strzała"),
    ("exploding crossbow bolt", "wybuchający bełt"),
    ("pipe bomb", "rurowa bomba"),
    ("grenade", "granat"),
    ("contact grenade", "granat kontaktowy"),
    ("timed charge", "ładunek czasowy"),
    ("molotov cocktail", "koktajl Mołotowa"),
    ("tin land mine", "mina z puszki"),
    ("cooking pot mine", "mina z garnka"),
    ("hub cap land mine", "mina z kołpaka"),
    ("air filter land mine", "mina z filtra powietrza"),
    ("rusty barrel", "zardzewiała beczka"),

    # ===== ROBOTICS =====
    ("robotic drone", "zrobotyzowany dron"),
    ("robotic sledge", "zrobotyzowany młot"),
    ("robotic turret", "zrobotyzowana wieżyczka"),

    # ===== ARMOR SETS =====
    ("primitive armor", "prymitywna zbroja"),
    ("light armor", "lekka zbroja"),
    ("medium armor", "średnia zbroja"),
    ("heavy armor", "ciężka zbroja"),
    ("athletic armor", "zbroja atletyczna"),
    ("enforcer armor", "zbroja egzekutora"),
    ("lumberjack armor", "zbroja drwala"),
    ("preacher armor", "zbroja kaznodziei"),
    ("rogue armor", "zbroja łotrzyka"),
    ("assassin armor", "zbroja skrytobójcy"),
    ("biker armor", "zbroja motocyklisty"),
    ("commando armor", "zbroja komandosa"),
    ("farmer armor", "zbroja farmera"),
    ("ranger armor", "zbroja strażnika"),
    ("scavenger armor", "zbroja złomiarza"),
    ("miner armor", "zbroja górnika"),
    ("nomad armor", "zbroja nomada"),
    ("nerd armor", "zbroja kujona"),
    ("raider armor", "zbroja najeźdźcy"),

    # ===== ARMOR PIECES =====
    ("primitive hood", "prymitywny kaptur"),
    ("primitive outfit", "prymitywny strój"),
    ("primitive gloves", "prymitywne rękawice"),
    ("primitive shoes", "prymitywne buty"),
    ("athletic hat", "czapka atletyczna"),
    ("athletic outfit", "strój atletyczny"),
    ("athletic gloves", "rękawice atletyczne"),
    ("athletic shoes", "buty atletyczne"),
    ("enforcer sunglasses", "okulary egzekutora"),
    ("enforcer outfit", "strój egzekutora"),
    ("enforcer gloves", "rękawice egzekutora"),
    ("enforcer shoes", "buty egzekutora"),
    ("lumberjack hat", "czapka drwala"),
    ("lumberjack outfit", "strój drwala"),
    ("lumberjack gloves", "rękawice drwala"),
    ("lumberjack boots", "buty drwala"),
    ("preacher hat", "kapelusz kaznodziei"),
    ("preacher outfit", "strój kaznodziei"),
    ("preacher gloves", "rękawice kaznodziei"),
    ("preacher boots", "buty kaznodziei"),
    ("rogue hood", "kaptur łotrzyka"),
    ("rogue outfit", "strój łotrzyka"),
    ("rogue gloves", "rękawice łotrzyka"),
    ("rogue boots", "buty łotrzyka"),
    ("assassin hood", "kaptur skrytobójcy"),
    ("assassin outfit", "strój skrytobójcy"),
    ("assassin gloves", "rękawice skrytobójcy"),
    ("assassin boots", "buty skrytobójcy"),
    ("biker helmet", "kask motocyklisty"),
    ("biker outfit", "strój motocyklisty"),
    ("biker gloves", "rękawice motocyklisty"),
    ("biker boots", "buty motocyklisty"),
    ("commando helmet", "hełm komandosa"),
    ("commando outfit", "strój komandosa"),
    ("commando gloves", "rękawice komandosa"),
    ("commando boots", "buty komandosa"),
    ("farmer hat", "kapelusz farmera"),
    ("farmer outfit", "strój farmera"),
    ("farmer gloves", "rękawice farmera"),
    ("farmer boots", "buty farmera"),
    ("ranger hat", "kapelusz strażnika"),
    ("ranger outfit", "strój strażnika"),
    ("ranger gloves", "rękawice strażnika"),
    ("ranger boots", "buty strażnika"),
    ("scavenger hat", "czapka złomiarza"),
    ("scavenger outfit", "strój złomiarza"),
    ("scavenger gloves", "rękawice złomiarza"),
    ("scavenger boots", "buty złomiarza"),
    ("miner helmet", "hełm górnika"),
    ("miner outfit", "strój górnika"),
    ("miner gloves", "rękawice górnika"),
    ("miner boots", "buty górnika"),
    ("nerd goggles", "gogle kujona"),
    ("nerd outfit", "strój kujona"),
    ("nerd gloves", "rękawice kujona"),
    ("nerd boots", "buty kujona"),
    ("nomad headgear", "nakrycie głowy nomada"),
    ("nomad outfit", "strój nomada"),
    ("nomad gloves", "rękawice nomada"),
    ("nomad boots", "buty nomada"),
    ("raider helmet", "hełm najeźdźcy"),
    ("raider outfit", "strój najeźdźcy"),
    ("raider gloves", "rękawice najeźdźcy"),
    ("raider boots", "buty najeźdźcy"),
    ("santa hat", "czapka Mikołaja"),

    # ===== PERKS & SKILLS =====
    ("pummel pete", "Pummel Pete"),
    ("skull crusher", "Miażdżyciel Czaszek"),
    ("boomstick", "Boomstick"),
    ("spear master", "Mistrz Włóczni"),
    ("demolitions expert", "Ekspert od Burzenia"),
    ("dead eye", "Martwe Oko"),
    ("the brawler", "Awanturnik"),
    ("machine gunner", "Karabinowy"),
    ("deep cuts", "Głębokie Cięcia"),
    ("archery", "Łucznictwo"),
    ("gunslinger", "Rewolwerowiec"),
    ("electrocutioner", "Elektrokuter"),
    ("robotics inventor", "Wynalazca Robotyki"),
    ("from the shadows", "Z Cienia"),

    # ===== ATTRIBUTES =====
    ("strength", "siła"),
    ("perception", "percepcja"),
    ("fortitude", "hart ducha"),
    ("agility", "zwinność"),
    ("intelligence", "inteligencja"),

    # ===== MECHANICS & STATUS EFFECTS =====
    ("blood moon", "krwawy księżyc"),
    ("gamestage", "etap gry"),
    ("structural integrity", "integralność strukturalna"),
    ("heatmap", "mapa ciepła"),
    ("feral sense", "zmysł zdziczenia"),
    ("dismemberment", "rozczłonkowanie"),
    ("stealth system", "system skradania"),
    ("stunned", "ogłuszony"),
    ("fatigue", "zmęczenie"),
    ("sprained leg", "skręcona noga"),
    ("sprained arm", "skręcona ręka"),
    ("laceration", "rany szarpane"),
    ("bleeding", "krwawienie"),
    ("infection", "infekcja"),
    ("rad remover mod", "mod na usuwanie radiacji"),
    ("stun resistance", "odporność na ogłuszenie"),
    ("critical injury resistance", "odporność na krytyczne obrażenia"),

    # ===== VEHICLES =====
    ("bicycle", "rower"),
    ("minibike", "minimotocykl"),
    ("motorcycle", "motocykl"),
    ("4x4 truck", "ciężarówka 4x4"),
    ("gyrocopter", "żyrokopter"),

    # ===== FOOD, DRINKS, ITEMS =====
    ("beer", "piwo"),
    ("small stone", "mały kamień"),
    ("snowball", "śnieżka"),
    ("stone axe", "kamienny topór"),
    ("claw hammer", "młotek ciesielski"),
    ("nailgun", "gwoździarka"),
    ("wood spike", "drewniany kolec"),
    ("hay bale", "bela siana"),
    ("rotting flesh", "gnijące mięso"),
    ("short iron pipe", "krótka żelazna rura"),
    ("repair kit", "zestaw naprawczy"),
    ("wood", "drewno"),
    ("stone", "kamień"),
    ("small stone", "kamyk"),
    ("bone", "kość"),
    ("cloth fragment", "kawałek materiału"),
    ("iron bar", "żelazny pręt"),
    ("dirt", "ziemia"),

    # ===== BIOMES =====
    ("burnt forest", "spalony las"),
    ("desert", "pustynia"),
    ("snow", "śnieg"),
    ("wasteland", "pustkowie"),
    ("pine forest", "las sosnowy"),
    ("navezgane", "Navezgane"),

    # ===== POINTS OF INTEREST / BUILDINGS =====
    ("point of interest", "punkt zainteresowania"),
    ("trader", "handlarz"),
    ("electric fence post", "słupek ogrodzenia elektrycznego"),

    # ===== GAME CONCEPTS =====
    ("armor rating", "współczynnik pancerza"),
    ("explosion resistance", "odporność na eksplozje"),
    ("crit resist", "odp. na krytyczne"),
    ("cold resist", "odp. na zimno"),
    ("heat resist", "odp. na ciepło"),
    ("mobility", "mobilność"),
    ("stamina regen", "regeneracja kondycji"),
    ("noise", "hałas"),
    ("durability", "wytrzymałość"),
    ("set bonus", "bonus zestawu"),
    ("lootstage", "etap łupów"),
    ("crouch", "kucać"),
    ("repair", "naprawiać"),
    ("salvage", "odzysk"),
    ("encumbrance", "obciążenie"),
    ("lockpicking", "otwieranie zamków"),
    ("bartering", "handel wymienny"),
]

# Read current deck
deck_path = "C:/Users/R6X/opencode/klepanka/js/decks/sevendays.js"
with open(deck_path, "r", encoding="utf-8") as f:
    content = f.read()

# Extract existing words
existing = set()
for m in re.finditer(r'en: "(.*?)", pl:', content):
    existing.add(m.group(1).lower().replace(" ", ""))

# Add new unique words
added = 0
for en, pl in new_words:
    key = en.lower().replace(" ", "").replace("-", "")
    if key not in existing:
        existing.add(key)
        added += 1

print(f"New unique words to add: {added}")

# Build new deck - read existing entries, append new ones
entries = re.findall(r'(\{ en: ".*?", pl: ".*?" \})', content)
if entries:
    last_entry_idx = content.rfind(entries[-1])
    after_last = content[last_entry_idx + len(entries[-1]):]
    closing = after_last[after_last.rfind(']'):]

    # Build new entries string
    new_entries_str = ""
    for en, pl in new_words:
        key = en.lower().replace(" ", "").replace("-", "")
        new_entries_str += f',\n  {{ en: "{en}", pl: "{pl}" }}'

    new_content = content[:last_entry_idx + len(entries[-1])]
    new_content += new_entries_str
    new_content += "\n" + closing.lstrip(",\n")

    with open(deck_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    # Count total
    total = len(re.findall(r'en: "', new_content))
    print(f"Total entries now: {total}")
else:
    print("ERROR: Could not parse deck format")
