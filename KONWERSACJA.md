# Historia konwersacji - Klepanka EN-PL

## Czym jest Klepanka
Aplikacja do nauki angielskich słówek przez fiszki. Statyczna strona (HTML+JS+CSS) hostowana na GitHub Pages.

**URL:** https://rgx78.github.io/klepanka/
**Repozytorium:** https://github.com/RGX78/klepanka
**Katalog lokalny:** `C:\Users\R6X\opencode\klepanka`

## Co zrobiliśmy - chronologicznie

### 1. Deck Cyberpunk 2077 (rozbudowa)
- Przeszukaliśmy internet (Wikipedia, wiki) dla lore Cyberpunka
- Rozbudowaliśmy `js/decks/cyberpunk.js` z 130 do **456 kart**
- Kategorie: postacie, frakcje, korporacje, lokacje, cyberware, broń, slang, lore, gameplay, Phantom Liberty
- Stworzyliśmy generator: `scripts/gen_cyberpunk_deck.py`
- Utworzyliśmy plik danych: `data/cyberpunk_deck.txt`
- Dodaliśmy tło z blur: `css/style.css` → `.cyberpunk-active::before` → `cyberpunk.jpeg`
- Poprawiliśmy ścieżkę z `Cyberpunk.jpg` na `cyberpunk.jpeg`

### 2. Pliki deck.txt dla Cyberpunka i Wiedźmina
- Skopiowaliśmy `js/decks/cyberpunk.js` → `data/cyberpunk_deck.txt` (456 kart)
- Skopiowaliśmy `js/decks/witcher.js` → `data/witcher_deck.txt` (73 karty)
- Format zgodny z innymi plikami w `data/`

### 3. Kopia zapasowa v2
- Skopiowaliśmy cały folder `klepanka` → `kopie zapasowe\klepanka v2`

### 4. Tło dla decków
- **Xanth:** dodaliśmy `xanth.jpg` jako tło z blur w CSS (`.xanth-active`)
- **Witcher:** poprawiliśmy `Witcher.jpg` → `witcher.jpg`
- **Baldur's Gate:** plik już się zgadzał (`BaldursGate.jpg`)

### 5. Baldur's Gate - tłumaczenie EN→PL
- ~4186 z 6026 słów było nieprzetłumaczonych (w `[nawiasach]`)
- Faza 1: `translate_baldursgate.py` → 377 przetłumaczonych
- Faza 2: `translate_baldursgate_p2.py` → 67 przetłumaczonych
- Faza 3: `translate_bg_final.py` → 740 przetłumaczonych
- **Rezultat: 3024/6026 (50.2%)** przetłumaczonych
- Zsyncowano `data/baldursgate_deck.txt`

### 6. Deck 7 Days to Die (rozbudowa)
- Przeszukaliśmy https://7daystodie.wiki.gg/ (zombie, broń, pancerze, perki)
- Rozbudowaliśmy z 664 do **934 kart**
- Dodaliśmy 238 nowych słów: nazwy zombie (Arlene, Boe, Wight), bronie (Pipe Shotgun, M60), pancerze (70+ części), perki (14), mechaniki (Blood Moon, Gamestage...)
- Skrypt: `scripts/expand_sevendays.py`
- Zsyncowano `data/seven_days_deck.txt`

### 7. Deck Once Human (rozbudowa)
- Przeszukaliśmy https://wikily.gg/once-human/ (kategorie przedmiotów, stworzenia, mody)
- Rozbudowaliśmy z 614 do **733 kart** (+119 słów)
- Kategorie: stworzenia (Bear Cub, Flamingo, Leopard...), przedmioty (Access Permit, Blueprint Fragments...), mody (Power Surge, Frost Vortex...), koncepty (Memetics, Stardust...)
- Skrypt: `scripts/expand_oncehuman.py`
- Zsyncowano `data/once_human_deck.txt`

### 8. Nowy deck Resident Evil
- Stworzyliśmy od zera `js/decks/residentevil.js` (208 kart)
- Dodaliśmy CSS dla `.residentevil-active` z tłem `residen evil.png`
- Dodaliśmy `<option>` w `index.html`
- Dodaliśmy class toggle w `js/app.js`
- Kategorie: wirusy (T-Virus, G-Virus...), postacie (16), frakcje, lokacje, broń, mechaniki

### 9. Kopia zapasowa v3
- `kopie zapasowe\klepanka v3`

### 10. Deployment na GitHub Pages
- Zainicjowaliśmy git w `klepanka`
- `gh auth login` - użytkownik RGX78
- `gh repo create klepanka --public`
- Git push
- `gh api repos/RGX78/klepanka/pages -X POST` - włączenie Pages
- **URL: https://rgx78.github.io/klepanka/**

### 11. Eksport/Import postępu
- Dodaliśmy przyciski ⬇ (eksport) i ⬆ (import) w `index.html`
- Funkcje `exportProgress()` i `importProgress()` w `js/app.js`
- Zapisuje wszystkie talie + ustawienia do pliku JSON
- Działa między urządzeniami

### 12. Fix mobilny
- Dodaliśmy `@media (max-width: 520px)` w `css/style.css`
- Na telefonie select na całą szerokość, przyciski mniejsze (32px) w rzędzie poniżej

---

## Stan obecny - wszystkie decki

| Deck | Plik JS | Karty | Status |
|------|---------|-------|--------|
| Final Fantasy | `js/decks/finalfantasy.js` | ? | istniał wcześniej |
| Baldur's Gate | `js/decks/baldursgate.js` | 6026 | 50% przetłumaczony |
| The Witcher | `js/decks/witcher.js` | 73 | gotowy |
| Cyberpunk 2077 | `js/decks/cyberpunk.js` | 456 | gotowy |
| Path of Exile | `js/decks/poe.js` | ? | istniał wcześniej |
| Once Human | `js/decks/oncehuman.js` | 733 | gotowy |
| 7 Days to Die | `js/decks/sevendays.js` | 934 | gotowy |
| Xanth | `js/decks/xanth.js` | ? | istniał wcześniej |
| Resident Evil | `js/decks/residentevil.js` | 208 | gotowy |

## Struktura plików (ważne)

```
klepanka/
├── index.html          # główna strona
├── css/style.css       # style + tła decków z blur
├── js/
│   ├── app.js          # logika aplikacji
│   └── decks/          # pliki talii (JS)
│       ├── finalfantasy.js
│       ├── baldursgate.js
│       ├── witcher.js
│       ├── cyberpunk.js
│       ├── poe.js
│       ├── oncehuman.js
│       ├── sevendays.js
│       ├── xanth.js
│       └── residentevil.js
├── data/               # kopie zapasowe decków (.txt)
├── scripts/            # generatory i narzędzia Python
├── *.jpg, *.png        # obrazy tła dla decków
└── .gitignore
```

## Jak dodać nowy deck (przepis)

1. Stwórz `js/decks/nazwa.js` z formatem:
   ```js
   var WORDS_NAZWA = [
     { en: "word", pl: "tłumaczenie" },
     ...
   ];
   ```

2. Dodaj `<option value="nazwa">Nazwa EN-PL</option>` w `index.html` do `#deckSelect`

3. W `css/style.css`:
   - Dodaj `body.nazwa-active` do listy `background-color: transparent`
   - Dodaj bloki `body.nazwa-active::before` i `body.light-theme.nazwa-active::before` z odpowiednim obrazkiem i `blur(5px)`

4. W `js/app.js`:
   - Dodaj `document.body.classList.toggle('nazwa-active', deckName === 'nazwa');`
   - Jeśli deck nazywa się inaczej niż `WORDS_NAZWA`, obsłuż mapowanie w `loadDeckScript()`

5. Dla słów EN→PL: wrzuć słowa na https://deepl.com/translator i skopiuj tłumaczenia

6. Po utworzeniu: `git add . && git commit -m "..." && git push`

## Deployment
- Repozytorium: https://github.com/RGX78/klepanka
- GitHub Pages włączone na branch `master`, folder `/`
- URL: https://rgx78.github.io/klepanka/
- Aby zaktualizować: `git add . && git commit -m "..." && git push`

## Ustawienia systemowe
- OS: Windows (PowerShell 5.1)
- Python: dostępny
- Node.js: v24.14.1
- Git: 2.51.0
- GitHub CLI: zainstalowany, zalogowany jako RGX78
- Kopia zapasowa: `C:\Users\R6X\opencode\kopie zapasowe\klepanka v3\`

## Jak uruchomić OpenCode z DeepSeek

To okno działa na modelu **DeepSeek V4 Pro** (`deepseek/deepseek-v4-pro`).

Dostępne modele DeepSeek przez OpenCode (w konsoli):

```powershell
# DeepSeek Reasoner / R1 - model rozumujący
opencode -m deepseek/deepseek-reasoner

# DeepSeek Chat / V3 - standardowy czat
opencode -m deepseek/deepseek-chat

# DeepSeek V4 Flash - szybki model
opencode -m deepseek/deepseek-v4-flash
```

Aby kontynuować pracę nad tym projektem w nowej sesji, wrzuć ten plik (`deepseek/KONWERSACJA.md`) do OpenCode jako kontekst startowy.
