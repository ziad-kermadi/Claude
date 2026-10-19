"""Append diagram images to card backs from diagram_maps/*.json (idempotent)."""
import glob, html, json, os, sys

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cards, bad, added = {}, [], 0
for m in sorted(glob.glob(os.path.join(D, "diagram_maps", "*.json"))):
    for e in json.load(open(m, encoding="utf-8")):
        f = e["file"]
        if f not in cards:
            cards[f] = json.load(open(os.path.join(D, "cards", f), encoding="utf-8"))
        img = os.path.join(D, "media", e["image"])
        i = e["index"]
        if not os.path.exists(img) or i >= len(cards[f]):
            bad.append((m, f, i, "missing image or index")); continue
        c = cards[f][i]
        if not c["front"].startswith(e.get("front_start", "")[:40]):
            bad.append((m, f, i, "front mismatch")); continue
        if e["image"] in c["back"]:
            continue
        cap = html.escape(e.get("caption", ""), quote=False)
        c["back"] += f'<div class="fig"><img src="{e["image"]}"><div class="cap">{cap}</div></div>'
        added += 1
for f, d in cards.items():
    json.dump(d, open(os.path.join(D, "cards", f), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("added", added)
for b in bad: print("SKIP", *b)
sys.exit(1 if bad else 0)
