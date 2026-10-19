import glob, json, os, random, hashlib
import genanki

D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D, "DeskStrat_Rates_Credit_VP_London.apkg")

SUBDECKS = {
    "01_govies": "Rates::1 Govies, Futures & Repo",
    "02_swaps_curves": "Rates::2 Swaps & Curve Construction",
    "03_rates_options": "Rates::3 Options & Vol",
    "04_inflation": "Rates::4 Inflation & Linkers",
    "05_credit_cds": "Credit::1 Bonds, CDS & Indices",
    "06_credit_models_cln": "Credit::2 Models, Curves & CLNs",
    "07_converts_loans": "Credit::3 Converts, Loans & CLOs",
    "08_coding_numerics": "Quant & Coding::Numerical Methods",
    "09_scenarios_markets_reg": "Markets::Scenarios, Microstructure & Regulation",
    "10_xva_funding": "XVA & Funding::XVA, Funding & Capital",
    "11_repo_financing": "Rates::5 Repo, Financing & Balance Sheet",
    "12_structured_exotics": "Structured Products::Exotics & Structuring",
}
ROOT = "DeskStrat VP London"

def did(name):
    return int(hashlib.md5(name.encode()).hexdigest()[:8], 16)

CSS = """
.card{font-family:Arial,Helvetica,sans-serif;font-size:17px;line-height:1.45;text-align:left;color:#1b1b1b;background:#fff;max-width:760px;margin:auto;padding:8px}
.nightMode .card,.night_mode .card{color:#e8e8e8;background:#1e1e1e}
b{color:#0b5394}.nightMode b,.night_mode b{color:#8ab4f8}
table{border-collapse:collapse;margin:6px 0}td,th{border:1px solid #999;padding:3px 8px}
code,pre{font-family:Consolas,monospace;font-size:15px;background:rgba(128,128,128,.15);padding:1px 4px;border-radius:3px}
pre{padding:8px;overflow-x:auto}
hr#answer{margin:12px 0}
.src{font-size:12px;color:#888;margin-top:10px}
"""

BASIC = genanki.Model(
    1607392319, "DeskStrat Basic",
    fields=[{"name": "Front"}, {"name": "Back"}, {"name": "Topic"}],
    templates=[{"name": "Card 1",
                "qfmt": "{{Front}}<div class='src'>{{Topic}}</div>",
                "afmt": "{{FrontSide}}<hr id=answer>{{Back}}"}],
    css=CSS)
CLOZE = genanki.Model(
    1607392320, "DeskStrat Cloze",
    model_type=genanki.Model.CLOZE,
    fields=[{"name": "Text"}, {"name": "Extra"}, {"name": "Topic"}],
    templates=[{"name": "Cloze",
                "qfmt": "{{cloze:Text}}<div class='src'>{{Topic}}</div>",
                "afmt": "{{cloze:Text}}<br><hr id=answer>{{Extra}}"}],
    css=CSS)


import re
_TAG=re.compile(r'</?(b|i|br|ul|ol|li|code|pre|table|tr|td|th|thead|tbody|sup|sub|u|p|div|span|em|strong|hr)\b[^>]*>',re.I)
def _math(m):
    return m.group(0).replace('<',' \\lt ').replace('>',' \\gt ').replace('&','&amp;') if False else m.group(0).replace('<',' \\lt ').replace('>',' \\gt ')
def clean(t):
    t=re.sub(r'\\\((.+?)\\\)',_math,t,flags=re.S)
    t=re.sub(r'\\\[(.+?)\\\]',_math,t,flags=re.S)
    # protect real tags, escape stray < >
    keep=[];
    def stash(m): keep.append(m.group(0)); return '\x00%d\x00'%(len(keep)-1)
    t=_TAG.sub(stash,t)
    t=t.replace('<','&lt;').replace('>','&gt;')
    t=re.sub(r'\x00(\d+)\x00',lambda m:keep[int(m.group(1))],t)
    # newlines -> <br> outside <pre>
    parts=re.split(r'(<pre.*?</pre>)',t,flags=re.S|re.I)
    parts=[p if p.lower().startswith('<pre') else re.sub(r'(?<!<br>)(?<!</li>)(?<!</ul>)(?<!</ol>)(?<!</table>)\n+','<br>',p) for p in parts]
    return ''.join(parts)

decks = {ROOT: genanki.Deck(did(ROOT), ROOT)}
n = 0
for f in sorted(glob.glob(os.path.join(D, "cards", "*.json"))):
    key = os.path.basename(f)[:-5].replace("_deep", "")
    name = f"{ROOT}::{SUBDECKS[key]}"
    for part in range(1, name.count("::") + 1):
        pass
    parts = name.split("::")
    for i in range(2, len(parts) + 1):
        nm = "::".join(parts[:i])
        decks.setdefault(nm, genanki.Deck(did(nm), nm))
    deck = decks[name]
    for c in json.load(open(f, encoding="utf-8")):
        tags = [t.replace(" ", "_") for t in c.get("tags", [])]
        topic = parts[-1]
        guid = genanki.guid_for(c["front"])
        if c["type"] == "cloze":
            note = genanki.Note(CLOZE, fields=[clean(c["front"]), clean(c.get("back", "")), topic], tags=tags, guid=guid)
        else:
            note = genanki.Note(BASIC, fields=[clean(c["front"]), clean(c["back"]), topic], tags=tags, guid=guid)
        deck.add_note(note); n += 1

genanki.Package(list(decks.values())).write_to_file(OUT)
print("notes:", n, "->", OUT)
