#!/usr/bin/env python3
"""
Generate a beautiful, filterable HTML page showing all PoE2 unique items.
Merges data from the official GGG trade API and poe2db.tw stats.
"""

import json
import os

# Input files
TRADE_API_PATH = r"C:\Users\R6X\opencode\poe2_uniques.json"
POE2DB_PATH = r"C:\Users\R6X\AppData\Local\Temp\opencode\poe2_uniques.json"
OUT_PATH = r"C:\Users\R6X\opencode\poe2_unique_items.html"

# Load trade API data (has name, baseType, category)
with open(TRADE_API_PATH, 'r', encoding='utf-8') as f:
    trade_data = json.load(f)

# Load poe2db data (has name, baseType, category, reqLevel, summary)
poe2db_data = []
if os.path.exists(POE2DB_PATH):
    with open(POE2DB_PATH, 'r', encoding='utf-8') as f:
        poe2db_data = json.load(f)

# Build lookup from poe2db by name
poe2db_lookup = {}
for item in poe2db_data:
    key = item['name'].lower()
    poe2db_lookup[key] = item

# Merge: enrich trade data with poe2db stats
items = []
seen = set()
for t in trade_data:
    name = t['name']
    if name.lower() in seen:
        continue
    seen.add(name.lower())

    db = poe2db_lookup.get(name.lower(), {})
    items.append({
        'name': name,
        'baseType': t.get('type', ''),
        'category': db.get('category') or t.get('category', 'Other'),
        'reqLevel': db.get('reqLevel'),
        'summary': db.get('summary', '')
    })

# Add any poe2db items not in trade API
for db in poe2db_data:
    if db['name'].lower() not in seen:
        seen.add(db['name'].lower())
        items.append({
            'name': db['name'],
            'baseType': db.get('baseType', ''),
            'category': db.get('category', 'Other'),
            'reqLevel': db.get('reqLevel'),
            'summary': db.get('summary', '')
        })

# Sort by category then name
cat_order = {
    'One-Hand Mace': 1, 'One-Hand Spear': 2, 'One-Hand Sword': 3, 'One-Hand Axe': 4,
    'Dagger': 5, 'Claw': 6, 'Wand': 7, 'Sceptre': 16, 'Flail': 18, 'Sword': 3,
    'Two-Hand Mace': 8, 'Spear': 2, 'Staff': 10, 'Bow': 11, 'Crossbow': 12, 'Quarterstaff': 13,
    'Weapon': 14, 'Talisman': 15, 'Trap': 17, 'Accessories': 20, 'Ring': 21, 'Amulet': 22,
    'Belt': 23, 'Amulets': 22, 'Body Armour': 30, 'Helmet': 31, 'Glove': 32,
    'Boot': 33, 'Shield': 34, 'Buckler': 34, 'Focus': 36, 'Quiver': 37,
    'Armour': 35, 'Jewel': 40, 'Flask': 41, 'Charm': 42, 'Life Flask': 41, 'Mana Flask': 41,
    'Waystone': 50, 'Tablet': 51, 'Map Fragment': 52, 'Misc Map Items': 52,
    'Relic': 55, 'Other': 99
}

def cat_sort_key(cat):
    return cat_order.get(cat, 999)

items.sort(key=lambda x: (cat_sort_key(x['category']), x.get('reqLevel') or 0, x['name']))

# Generate HTML
items_json = json.dumps(items, ensure_ascii=False)

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Path of Exile 2 — Wszystkie Unikaty</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0a0a0f;color:#c8c8c8;font-family:'Segoe UI',system-ui,sans-serif;padding:16px}}
h1{{color:#af6025;font-size:1.3rem;margin-bottom:4px}}
.sub{{color:#555;font-size:.7rem;margin-bottom:16px}}

.search-bar{{position:sticky;top:0;z-index:10;background:#0a0a0f;padding:8px 0;display:flex;gap:8px;flex-wrap:wrap}}
.search-bar input,.search-bar select{{background:#1a1a2e;border:1px solid #2a2a3a;color:#ccc;padding:8px 14px;border-radius:8px;font-size:.8rem;outline:none}}
.search-bar input{{flex:1;min-width:200px}}
.search-bar input:focus,.search-bar select:focus{{border-color:#af6025}}

.summary{{display:flex;gap:12px;font-size:.7rem;color:#555;margin-bottom:12px;flex-wrap:wrap}}
.summary span{{background:#1a1a2e;padding:3px 10px;border-radius:12px;border:1px solid #2a2a3a}}
.summary .count{{color:#af6025;font-weight:700}}

.cat-header{{color:#af6025;font-size:.75rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;margin:20px 0 8px 0;padding:6px 10px;background:rgba(175,96,37,.08);border-left:3px solid #af6025;border-radius:0 6px 6px 0}}
.cat-count{{color:#555;font-weight:400;font-size:.65rem}}

.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:6px}}
.card{{background:#111119;border:1px solid #1e1e2e;border-radius:10px;padding:12px 14px;transition:all .15s;display:flex;flex-direction:column;gap:4px}}
.card:hover{{border-color:#af6025;background:#151520}}
.card.hidden{{display:none}}

.card .name{{color:#e8d4a8;font-weight:700;font-size:.85rem;line-height:1.2}}
.card .base{{color:#af6025;font-size:.65rem;font-weight:600;text-transform:uppercase;letter-spacing:.05em}}
.card .level{{color:#555;font-size:.6rem}}
.card .stats{{color:#7a7a8a;font-size:.65rem;line-height:1.5;margin-top:4px;border-top:1px solid #1e1e2e;padding-top:6px}}

.toast{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#af6025;color:#fff;padding:6px 16px;border-radius:16px;font-size:.7rem;z-index:100;opacity:0;transition:opacity .3s;pointer-events:none}}
.toast.show{{opacity:1}}

@media(max-width:600px){{.grid{{grid-template-columns:1fr}}h1{{font-size:1.1rem}}}}
</style>
</head>
<body>

<h1>Path of Exile 2 — Wszystkie Unikaty</h1>
<div class="sub">Dane z oficjalnego API GGG + poe2db.tw | v0.5 Return of the Ancients</div>

<div class="search-bar">
  <input type="text" id="search" placeholder="Szukaj unikatu..." oninput="filter()">
  <select id="catFilter" onchange="filter()">
    <option value="all">Wszystkie kategorie</option>
  </select>
</div>

<div class="summary">
  <span>Łącznie: <span class="count" id="totalCount">{len(items)}</span></span>
  <span>Z poziomem: <span class="count" id="leveledCount">{sum(1 for i in items if i.get('reqLevel'))}</span></span>
</div>

<div id="content"></div>

<div class="toast" id="toast"></div>

<script>
const items = {items_json};

// Build category filter
const cats = [...new Set(items.map(i => i.category))].sort();
const sel = document.getElementById('catFilter');
cats.forEach(c => {{ const o = document.createElement('option'); o.value = c; o.textContent = c; sel.appendChild(o); }});

// Group by category
function render(filtered) {{
  const content = document.getElementById('content');
  const grouped = {{}};
  filtered.forEach(i => {{
    const cat = i.category || 'Other';
    if (!grouped[cat]) grouped[cat] = [];
    grouped[cat].push(i);
  }});

  let html = '';
  for (const [cat, catItems] of Object.entries(grouped)) {{
    html += `<div class="cat-header">${{cat}} <span class="cat-count">(${{catItems.length}})</span></div>`;
    html += '<div class="grid">';
    catItems.forEach(i => {{
      const lvl = i.reqLevel ? `Lvl ${{i.reqLevel}}` : '';
      html += `<div class="card">
        <div class="name">${{i.name}}</div>
        <div class="base">${{i.baseType}}</div>
        ${{lvl ? `<div class="level">Wymaga poziomu ${{i.reqLevel}}</div>` : ''}}
        ${{i.summary ? `<div class="stats">${{i.summary}}</div>` : ''}}
      </div>`;
    }});
    html += '</div>';
  }}
  content.innerHTML = html;
  document.getElementById('totalCount').textContent = filtered.length;
}}

function filter() {{
  const q = document.getElementById('search').value.toLowerCase();
  const cat = document.getElementById('catFilter').value;
  let filtered = items;
  if (cat !== 'all') filtered = filtered.filter(i => i.category === cat);
  if (q) filtered = filtered.filter(i => i.name.toLowerCase().includes(q) || i.baseType.toLowerCase().includes(q));
  render(filtered);
}}

render(items);
</script>
</body>
</html>'''

with open(OUT_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Generated: {OUT_PATH}")
print(f"Total items: {len(items)}")
cats = {}
for i in items:
    cats[i['category']] = cats.get(i['category'], 0) + 1
for cat, count in sorted(cats.items()):
    print(f"  {cat}: {count}")
