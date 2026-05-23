#!/usr/bin/env python3
"""Extract difficult English words from PoE sources and create a flashcard deck."""
import json, re

# Load PoE2 uniques
with open(r"C:\Users\R6X\opencode\poe2_uniques.json", 'r', encoding='utf-8') as f:
    uniques = json.load(f)

# Extract words from item names and types
raw_words = []
for item in uniques:
    for field in ('name', 'type', 'category'):
        val = item.get(field, '')
        raw_words.extend(re.findall(r'[A-Za-z]+', val))

# All unique item names as-is (keep compound names like "Carnage Heart")
item_names = list(set(item['name'].strip() for item in uniques))

# Hardcoded PoE mechanics & lore terms - rich vocabulary
poe_terms = [
    # Mechanics keywords from poe2db
    "ailment","ignite","chill","freeze","shock","poison","bleeding","electrocution","pin",
    "onslaught","tailwind","fortify","leech","recoup","culling","pierce","fork","chain","split",
    "maim","hinder","exposure","withered","corrupted","hexproof",
    "warcry","valour","glory","rage","endurance","frenzy","power","shatter",
    "slam","channelling","aura","herald","vaal","melee","trigger","totem","minion",
    "corpses","projectile","accuracy","crush","combo","blind","guard","aegis",
    "daze","aftershock","immobilised","magnitude","empower","banner","ammunition",
    "staged","grenade","detonator","shapeshift","companion","hazard","remnant",
    "sprinting","surrounded","consumed","thorns","break",
    # Damage/defense types
    "physical","elemental","chaos","fire","cold","lightning","overkill",
    "armour","evasion","resistance","penetration","conversion","reflection",
    "recharge","regeneration","recovery","energy","shield",
    # League mechanics
    "breach","abyss","legion","blight","delirium","scourge","crucible","harvest",
    "heist","expedition","ritual","sanctum","harbinger","synthesis",
    "delve","incursion","bestiary","nemesis","domination","ambush","torment",
    "essence","harbinger","metamorph","archnemesis","sentinel",
    "ultimatum","kalguur","affliction","necropolis","ancestors",
    # Game concepts
    "ascendancy","keystone","notable","passive","skill","gem","socket",
    "vendor","recipe","divination","currency","crafting","scour","alchemy",
    "transmute","augment","regal","exalted","divine","mirror","vaal",
    "chance","scouring","fusing","jeweller","chromatic","blessed",
    "map","waystone","atlas","pinnacle","fragment","splinter","catalyst",
    "omen","incubator","tablet","relic","charm","tincture",
    # Lore terms
    "thaumaturgy","thaumaturgist","thaumaturgical",
    "wraeclast","oriath","azmeri","maraketh","karui","ezomyte",
    "vaal","kalguur","faridun","caaltu",
    "atrocious","cataclysm","cataclysmic","precursor","primeval",
    "ascension","divinity","godhood","immortal","mortality",
    "blasphemy","heresy","heretic","penance","consecrate","desecrate",
    "sanctify","purge","purify","redemption","salvation",
    "torment","agony","despair","anguish","suffering","misery",
    "carnage","slaughter","massacre","atrocity","annihilate",
    "obliterate","decimate","devastate","ravage","scourge",
    "arcane","eldritch","occult","profane","infernal","abyssal",
    "celestial","astral","ethereal","spectral","phantasmal",
    "bastion","citadel","fortress","rampart","bulwark","garrison",
    "siege","conquest","dominion","sovereign","realm","empire",
    "legacy","lineage","dynasty","ancestry","heritage",
    "corruption","depravity","decay","blight","pestilence","plague",
    "zealot","fanatic","disciple","acolyte","templar","hierophant",
    "champion","gladiator","slayer","juggernaut","berserker",
    "chieftain","raider","deadeye","pathfinder","saboteur",
    "assassin","trickster","occultist","elementalist","necromancer",
    "guardian","inquisitor","assassin","harbinger",
    "sorcery","witchcraft","alchemy","enchant","incantation","invocation",
    "conjure","summon","banish","bind","cleave","rend","sunder",
    "cleave","lacerate","perforate","impale","eviscerate","disembowel",
    "cleave","cleaver","executioner","reaper","harvester",
    "cataclysm","armageddon","apocalypse","oblivion","annihilation",
    "void","abyss","chasm","maelstrom","vortex","tempest","cyclone",
    "volcano","magma","inferno","blaze","ember","cinder","scorch",
    "tundra","glacier","avalanche","blizzard","frost","hoarfrost",
    "lightning","thunder","tempest","storm","hurricane","typhoon",
    "quiver","quarrel","feud","vendetta","retribution","vengeance",
    "vigil","sentinel","warden","keeper","guardian","protector",
    "vision","prophecy","omen","augury","divination","revelation",
    "covenant","pact","sacrifice","offering","tithe","tribute",
    "chalice","grail","relic","artifact","talisman","fetish","idol",
    "golem","construct","automaton","effigy","simulacrum",
    "labyrinth","maze","crypt","tomb","catacomb","mausoleum",
    "shrine","temple","sanctuary","cathedral","monastery","abbey",
    "throne","crown","sceptre","mantle","regalia","raiment",
    "flesh","bone","marrow","sinew","viscera","entrail","gore",
    "wretched","forsaken","accursed","damned","condemned",
    "vigorous","relentless","merciless","ruthless","pitiless","remorseless",
    # PoE2-specific
    "auspex","facebreaker","reverie","hollow","breachstone",
    "biostatic","kinetic","vitalic","oneiric","mnemonic","grasping",
    "corona","absent","forking","precursor","breach",
    "unrevealed","ire","passion","betrayal","creativity","portent","lament",
    "verisium","crest","runic","alloy","imbued","expansive","mystic","swift",
    "archaic","retaliation","control","discovery","animosity","prowess",
    "splinters","titan","warding","reinforcement","protection","bravado",
    "epiphany","sidereus","revered","starlit","legacy",
    "paranoia","potent","melancholy","concentrated","isolation","suffering",
    "ruby","quartz","tourmaline","nephrite","catalyst",
    "lavish","ornate","revelatory","banded","signet",
    "azmerian","swarms","coiling","concussive","frostflame",
    "gemini","surge","repulsion","midnight","zenith","molten",
    "shower","righteous","descent","infusion","spiraling","conspiracy",
    "soaring","starborn","triskelion","cascade","aftermath",
    "resonance","focus","vivid","stampede","primal","bounty",
    "rite","restoration","gifts",
    # More
    "adversary","foe","nemesis","rival","challenger","contender",
    "duelist","combatant","warrior","knight","paladin","crusader",
    "barbarian","savage","marauder","outlaw","bandit","brigand",
    "exile","outcast","pariah","refugee","wanderer","nomad",
    "pilgrim","wayfarer","voyager","explorer","pioneer",
    "cartographer","scribe","archivist","chronicler","historian",
    "scholar","sage","seer","oracle","prophet","diviner",
    "alchemist","apothecary","physician","surgeon","leech",
    "butcher","hunter","trapper","poacher","stalker","predator",
    "serpent","viper","asp","cobra","python","hydra","dragon","wyrm",
    "griffin","phoenix","chimera","manticore","basilisk","gorgon",
    "spectre","wraith","phantom","apparition","shade","revenant",
    "lich","necromancer","death","undeath","resurrection",
    "crimson","scarlet","vermillion","carmine","burgundy",
    "azure","cobalt","sapphire","cerulean","indigo",
    "emerald","jade","verdant","viridian","malachite",
    "amber","topaz","citrine","golden","gilded",
    "onyx","obsidian","ebony","jet","pitch",
    "ivory","alabaster","marble","porcelain","pearl",
]

# Also PoE1 unique items with interesting names
poe1_cards = [
    "aberration","abundance","alacrity","annihilate","arrogance",
    "atonement","avarice","benevolence","bereavement","blasphemy",
    "cataclysm","clemency","communion","condemnation","consecration",
    "conviction","corruption","delirium","denial","desecration",
    "destiny","devastation","discord","dominion","enlightenment",
    "epiphany","eternity","excavation","extinction","famine",
    "fidelity","frenzy","gambler","greed","harmony",
    "hatred","hubris","humility","immortality","incantation",
    "insanity","isolation","judgement","lament","legacy",
    "malediction","malevolence","mortality","nemesis","obliteration",
    "obscurity","oppression","penance","perfection","perseverance",
    "pestilence","piety","premonition","privilege","prosperity",
    "providence","prudence","purity","redemption","reflection",
    "regret","remorse","resilience","retribution","revelation",
    "reverence","sacrifice","salvation","savagery","schism",
    "scourge","serenity","solitude","sorrow","supremacy",
    "surrender","sustenance","tempest","temptation","torment",
    "tranquility","treachery","tribulation","triumph","tyranny",
    "unity","vanity","vengeance","vigil","vindication",
    "violence","virtue","void","whisper","wrath","zealotry",
]

# Combine all, deduplicate
all_raw = set()
for w in raw_words:
    if len(w) >= 4:
        all_raw.add(w.lower())

for w in poe_terms:
    all_raw.add(w.lower())

for w in poe1_cards:
    all_raw.add(w.lower())

# Filter STOP_WORDS
STOP_WORDS = {
    'the','are','was','had','has','been','were','said','did','does',
    'this','that','from','with','have','they','their','what','when','where',
    'which','about','would','there','could','other','than','then','them',
    'these','those','such','only','also','even','very','also','into',
    'over','after','before','between','under','above','below','through',
    'upon','without','within','against','among','along','during','until',
    'because','should','might','shall','must','need','being','having',
    'every','some','most','many','much','more','less','same','both',
    'each','just','first','last','next','here','there','where','away',
    'back','again','still','always','never','once','twice','always',
    'anything','everything','nothing','something','everyone','someone',
    'year','time','people','place','world','life','hand','part','case',
    'made','make','come','goes','take','give','keep','find','tell',
    'work','know','think','want','mean','say','look','feel','seem',
    'thing','things','good','great','large','small','high','long','new',
    'old','young','right','left','down','side','front','kind','sort',
    'type','used','using','item','items','level','mod','mods','name',
    'ring','belt','body','boots','glove','gloves','shield','sword',
    'wand','staff','helm','helmet','armour','weapon','flask','jewel',
    'skill','mage','your','with','that','stone','base','wand','bow',
    'claw','unique','unset','iron','gold','load','link','note','list',
    'code','main','text','area','gate','tier','rare','base',
    'more','page','drop','also','each','next','once','line','will',
    'does','equip','grant','using','into','face','form','men','way',
    'gain','hold','king','lord','mind','open','play','pool','rest',
    'self','turn','upon','went','were','wide','wind','wood','word',
    'zeal','zone','remain','round','start','ends','based','done',
    'grants','grants','called','require','requires','found','added',
    'increased','reduced','maximum','minimum','chance','value',
    'spell','attack','damage','second','seconds','number','total',
    'icon','image','images','source','sources','stack','stacks',
    'melee','spells','attacks','cast','rate','deal','deals',
    'provide','instead','granted','radius','nearby','nearby',
    'data','latest','system','host','create','visit','about','wiki',
    'general','support','fandom','outpost','league','leagues',
    'harbor','harbour','subarea','subareas','subareas','bazaar',
    'portal','portals','device','mortal','immortal','resplendent',
    'monster','monsters','hidden','holy','unholy','description',
    'port','clear','cost','gems','single','early','vault','key',
    'hall','coin','coins','metre','metres','metres','hour','hours',
    'vastiri',
}

filtered = sorted(w for w in all_raw if w not in STOP_WORDS and len(w) >= 4)

# Priority score: words that appear in item names or PoE terms are most relevant
def priority(w):
    score = 0
    if w in (t.lower() for t in poe_terms): score += 10
    if any(w in it.lower().split() for it in item_names): score += 5
    if w in (c.lower() for c in poe1_cards): score += 5
    if len(w) >= 6: score += 2
    if len(w) >= 8: score += 2
    return score

scored = [(w, priority(w)) for w in filtered]
scored.sort(key=lambda x: -x[1])

# Take top ~250 words for curation
top_words = [w for w, s in scored[:250]]

print(f"Total raw words: {len(all_raw)}")
print(f"After stopword filter: {len(filtered)}")
print(f"Top candidates: {len(top_words)}")
print("\n--- Sample words ---")
for w in top_words[:50]:
    print(f"  {w}")
