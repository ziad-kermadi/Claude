import glob, json, os, re, hashlib, collections
import genanki

D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D, "DeskStrat_Quant_Brainteasers_VP_London.apkg")
ROOT = "DeskStrat VP London::Quant Interview Core"

SUBDECKS = {
    "00_toolkit": "0 Structure Toolkit & Recognition",
    "01_combinatorics": "1 Combinatorics & Counting",
    "02_conditioning_bayes": "2 Conditioning & Bayes",
    "03_expectation_variance": "3 Expectation, Indicators & Variance",
    "04_markov_walks_martingales": "4 Random Walks, Markov & Martingales",
    "05_continuous_geometric": "5 Continuous & Geometric Probability",
    "06_brainteasers_games": "6 Brainteasers, Logic & Games",
    "07_stochastic_derivatives": "7 Stochastic Calculus & Derivatives",
    "08_stats_regression_ml": "8 Statistics, Regression & ML",
    "09_linalg_calculus_pde": "9 Linear Algebra, Calculus & PDE",
    "10_mental_math_fermi_mm": "10 Mental Maths, Fermi & Market Making",
}

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
.prompt{font-size:13px;color:#a05a00;margin-top:8px}
"""

PROMPT = ("<div class='prompt'>Say it out loud first: structure, trigger, key move. "
          "Then solve. Then: what would break it?</div>")

BASIC = genanki.Model(
    1739204511, "QuantCore Basic",
    fields=[{"name": "Front"}, {"name": "Back"}, {"name": "Topic"}],
    templates=[{"name": "Card 1",
                "qfmt": "{{Front}}" + PROMPT + "<div class='src'>{{Topic}}</div>",
                "afmt": "{{Front}}<hr id=answer>{{Back}}<div class='src'>{{Topic}}</div>"}],
    css=CSS)
CLOZE = genanki.Model(
    1739204512, "QuantCore Cloze",
    model_type=genanki.Model.CLOZE,
    fields=[{"name": "Text"}, {"name": "Extra"}, {"name": "Topic"}],
    templates=[{"name": "Cloze",
                "qfmt": "{{cloze:Text}}<div class='src'>{{Topic}}</div>",
                "afmt": "{{cloze:Text}}<br><hr id=answer>{{Extra}}"}],
    css=CSS)

_TAG = re.compile(r'</?(b|i|br|ul|ol|li|code|pre|table|tr|td|th|thead|tbody|sup|sub|u|p|div|span|em|strong|hr)\b[^>]*>', re.I)

def _math(m):
    return m.group(0).replace('<', ' \\lt ').replace('>', ' \\gt ')

def clean(t):
    t = re.sub(r'\\\((.+?)\\\)', _math, t, flags=re.S)
    t = re.sub(r'\\\[(.+?)\\\]', _math, t, flags=re.S)
    keep = []
    def stash(m):
        keep.append(m.group(0)); return '\x00%d\x00' % (len(keep) - 1)
    t = _TAG.sub(stash, t)
    t = t.replace('<', '&lt;').replace('>', '&gt;')
    t = re.sub(r'\x00(\d+)\x00', lambda m: keep[int(m.group(1))], t)
    parts = re.split(r'(<pre.*?</pre>)', t, flags=re.S | re.I)
    parts = [p if p.lower().startswith('<pre') else
             re.sub(r'(?<!<br>)(?<!</li>)(?<!</ul>)(?<!</ol>)(?<!</table>)\n+', '<br>', p) for p in parts]
    return ''.join(parts)

decks = {}
def deck(name):
    parts = name.split("::")
    for i in range(1, len(parts) + 1):
        nm = "::".join(parts[:i])
        decks.setdefault(nm, genanki.Deck(did(nm), nm))
    return decks[name]

n, skipped, seen = 0, 0, set()
struct = collections.Counter()
for f in sorted(glob.glob(os.path.join(D, "cards", "*.json"))):
    key = os.path.basename(f)[:-5]
    name = f"{ROOT}::{SUBDECKS[key]}"
    dk = deck(name)
    for c in json.load(open(f, encoding="utf-8")):
        if c.get("type") not in ("basic", "cloze") or not c.get("front") or c["front"] in seen:
            skipped += 1; continue
        if c["type"] == "cloze" and "{{c" not in c["front"]:
            skipped += 1; continue
        seen.add(c["front"])
        tags = [t.strip().replace(" ", "_") for t in c.get("tags", []) if t.strip()]
        struct.update(t for t in tags if t.startswith("s_"))
        topic = SUBDECKS[key]
        guid = genanki.guid_for("quantcore", c["front"])
        if c["type"] == "cloze":
            note = genanki.Note(CLOZE, fields=[clean(c["front"]), clean(c.get("back", "")), topic], tags=tags, guid=guid)
        else:
            note = genanki.Note(BASIC, fields=[clean(c["front"]), clean(c.get("back", "")), topic], tags=tags, guid=guid)
        dk.add_note(note); n += 1

genanki.Package(list(decks.values())).write_to_file(OUT)
print("notes:", n, "skipped:", skipped, "->", OUT)
print("structure coverage:", ", ".join(f"{k}={v}" for k, v in struct.most_common()))
