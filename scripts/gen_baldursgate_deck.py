"""
Generate Baldur's Gate deck with EN-PL translations.
Uses existing translations from klepanka.html + fallback.
"""

import re

def load_existing_translations(html_path):
    translations = {}
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    pattern = r'\{\s*en:\s*["\']([^"\']+)["\'],\s*pl:\s*["\']([^"\']+)["\']\s*\}'
    for match in re.finditer(pattern, content):
        en_word = match.group(1).lower().strip()
        pl_word = match.group(2).strip()
        if en_word not in translations:
            translations[en_word] = pl_word
    return translations

def read_cefr_words(filepath):
    words = []
    current_level = None
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            level_match = re.match(r'^\s*(B1|B2|C1|C2) WORDS', line)
            if level_match:
                current_level = level_match.group(1)
                continue
            word_match = re.match(r'^(\S+)\s+freq:\s+([\d.]+)\s+appears:\s+(\d+)x', line)
            if word_match and current_level:
                words.append({
                    "word": word_match.group(1),
                    "level": current_level,
                })
    return words

def main():
    html_path = "C:\\Users\\R6X\\opencode\\klepanka.html"
    cefr_path = "C:\\Users\\R6X\\opencode\\cefr_b1_c2_words.txt"
    import os
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../js/decks/baldursgate.js"))
    
    print("Loading existing translations...")
    translations = load_existing_translations(html_path)
    print(f"Loaded {len(translations)} translations")
    
    print("Reading CEFR words...")
    words = read_cefr_words(cefr_path)
    print(f"Found {len(words)} words")
    
    missing = sum(1 for w in words if w["word"] not in translations)
    print(f"Missing translations: {missing}")
    
    js_lines = ['const WORDS_BALDURSGATE = [']
    for w in words:
        en_word = w["word"]
        pl = translations.get(en_word, f"[{en_word}]")
        pl = pl.replace('"', '\\"')
        js_lines.append(f'  {{ en: "{en_word}", pl: "{pl}" }},')
    js_lines.append('];')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(js_lines))
    
    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    main()
