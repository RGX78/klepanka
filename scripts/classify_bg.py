#!/usr/bin/env python3
"""Classify remaining untranslated Baldur's Gate words."""
import re

with open("C:/Users/R6X/opencode/klepanka/js/decks/baldursgate.js", "r", encoding="utf-8") as f:
    content = f.read()

ms = re.findall(r'en: "(.*?)", pl: "\[.*?\]"', content)
words = sorted(set(ms))

# Known Baldur's Gate / Forgotten Realms proper names
BG_PROPER = {
    'abdel', 'abdels', 'abel', 'adrian', 'aiid', 'ain', 'aldous', 'alfredo', 'alice', 'angelo',
    'baltimore', 'xan', 'xzar', 'yeslick', 'zhent', 'zhentarim', 'zhents',
    'khelben', 'elminster', 'drizzt', 'mirt', 'sarevok', 'gorion',
    'imoen', 'jaheira', 'minsc', 'khalid', 'dynaheir', 'viconia', 'edwin',
    'aerie', 'nalia', 'valygar', 'keldorn', 'mazzy', 'cernd', 'haer', 'jan',
    'yoshimo', 'korgan', 'anomen', 'bodhi', 'irenicus', 'melissan', 'saemon',
    'elhan', 'arvoreen', 'sune', 'tyr', 'helm', 'torm', 'loviatar', 'umberlee',
    'talos', 'auril', 'bane', 'bhaal', 'cyric', 'mask', 'mystra', 'oghma',
    'selune', 'shar', 'silvanus', 'tempus', 'tymora', 'waukeen', 'lathander',
    'malar', 'kelemvor', 'gond', 'ilmater', 'azuth', 'beshaba', 'chauntea',
    'deneir', 'eldath', 'gargauth', 'grumbar', 'gwaeron', 'hoar', 'ishtishia',
    'kossuth', 'leira', 'lurue', 'mielikki', 'milil', 'rath', 'knight',
    'savras', 'shaundakul', 'shiallia', 'siamorphe', 'ulutiu', 'valkur',
    'vhaeraun', 'akadi', 'istishia', 'raphael', 'rafael', 'beaverville',
    'baltimore', 'coran', 'montaron', 'quayle', 'tiax', 'branwen', 'faldorn',
    'garrick', 'skye', 'sharteel', 'skee', 'safana', 'alaric', 'alatos',
    'albert', 'alyth', 'andrew', 'angela', 'arkush', 'arno', 'augustus',
    'barth', 'beador', 'belgin', 'bently', 'bheren', 'brendan', 'briel',
    'bub', 'cadderly', 'caius', 'carl', 'carston', 'cernick', 'charlotte',
    'clarence', 'conrad', 'corinth', 'cromwell', 'cyric', 'daevorn',
    'daitel', 'davaeorn', 'diamon', 'dradeel', 'drasus', 'elence',
    'ellisime', 'elora', 'entilis', 'erdane', 'ethel', 'fabricate',
    'fenten', 'firkraag', 'flamsterd', 'galvarey', 'gellana', 'gen',
    'gentrus', 'gillian', 'giovanni', 'girard', 'glimmer', 'glorius',
    'gorken', 'gustav', 'habib', 'haegan', 'jek', 'jardak', 'jeb',
    'jendra', 'jermsy', 'johan', 'ketta', 'kiel', 'lendar', 'lenore',
    'logan', 'lucille', 'maheer', 'malficus', 'marcus', 'maria',
    'marlowe', 'marcellus', 'melinda', 'mendes', 'merella', 'meronia',
    'mike', 'mulahey', 'nathan', 'neera', 'nemphre', 'norton', 'norton',
    'peter', 'pheirkas', 'piergeiron', 'pique', 'poquelin', 'prid',
    'quallo', 'ramazith', 'ratchild', 'rayic', 'reiltar', 'renfeld',
    'rien', 'rogovich', 'rothgar', 'samantha', 'sandr', 'scar', 'schmidt',
    'sellius', 'sendai', 'severin', 'shalane', 'skeezer', 'smael',
    'surgeon', 'taerom', 'tahazzar', 'taylor', 'tazok', 'tella',
    'thalanthyr', 'thessaly', 'tiax', 'tilly', 'tranzig', 'trent',
    'unger', 'vail', 'vander', 'vay', 'viktor', 'vincent', 'wieland',
    'winthrop', 'winski', 'yago', 'yoshimo', 'zavrian', 'zeke',
    # Common BG creature/monster names
    'gnoll', 'gnolls', 'goblin', 'goblins', 'hobgoblin', 'ogre', 'ogres',
    'gibberling', 'gibberlings', 'kobold', 'kobolds', 'skeleton', 'necromancer',
    'ankheg', 'basilisk', 'beholder', 'carrion', 'centaur', 'chimera',
    'cockatrice', 'doppelganger', 'dracolich', 'dryad', 'ettercap', 'ettin',
    'ghast', 'ghoul', 'golem', 'griffon', 'harpy', 'hellhound', 'homunculus',
    'hydra', 'imp', 'leprechaun', 'lich', 'manticore', 'medusa', 'mimic',
    'minotaur', 'mummy', 'naga', 'ooze', 'orc', 'orcs', 'otyugh',
    'owlbear', 'pegasus', 'phantom', 'pixie', 'pseudodragon', 'rakshasa',
    'roc', 'sahuagin', 'salamander', 'satyr', 'shambling', 'shrieker',
    'sphinx', 'stirge', 'tarrasque', 'treant', 'troglodyte', 'troll',
    'umberhulk', 'unicorn', 'wight', 'will', 'wisp', 'worg', 'wraith',
    'wyvern', 'yuan', 'zombie',
    # Spell/ability names
    'magic', 'missile', 'fireball', 'lightning', 'bolt', 'haste',
    'bless', 'curse', 'cure', 'dispel', 'invisibility', 'polymorph',
    'teleport', 'gate', 'wish', 'time', 'stop',
    # Location names
    'baldurs', 'candlekeep', 'friendly', 'arm', 'inn', 'nashkel',
    'beregost', 'cloakwood', 'durlags', 'tower', 'throne', 'bhaal',
    'suldanessellar', 'saradush', 'amkethran', 'ulcaster', 'firewine',
    'gully', 'kin', 'high', 'hedge', 'larswood', 'peldvale', 'wood',
    'sharp', 'teeth', 'spiders', 'bane', 'xvart', 'village', 'gully',
    'pirate', 'cove', 'werewolf', 'island', 'ice', 'lab',
}

common = []
bg_names = []
for w in words:
    if w in BG_PROPER:
        bg_names.append(w)
    elif w[0].isupper() and all(c.isalpha() for c in w[1:]) and len(w) > 3 and w.lower() not in {'a', 'i'}:
        # Capitalized words are likely proper names
        bg_names.append(w)
    else:
        common.append(w)

print(f"Total remaining: {len(words)}")
print(f"Common English words: {len(common)}")
print(f"BG proper names: {len(bg_names)}")
print(f"\nSample common words:")
for w in common[:50]:
    print(f"  {w}")
print(f"\nSample BG names:")
for w in sorted(bg_names)[:30]:
    print(f"  {w}")
