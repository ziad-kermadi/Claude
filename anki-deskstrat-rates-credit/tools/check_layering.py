"""Check that a layering rewrite changed structure only: fronts/tags/types/code/images/numbers/math preserved."""
import json, os, re, sys

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRE = sys.argv[1]
NUM = re.compile(r"\d[\d,]*\.?\d*")
PRE_BLOCK = re.compile(r"<pre.*?</pre>", re.S | re.I)
FIG = re.compile(r'<div class="fig">.*?</div></div>', re.S)
MATH = re.compile(r"\\\(.+?\\\)|\\\[.+?\\\]", re.S)


def toks(s):
    s = FIG.sub("", PRE_BLOCK.sub("", s))
    return {n.rstrip(".,") for n in NUM.findall(s)}


bad = 0
for f in sys.argv[2:]:
    old = json.load(open(os.path.join(PRE, f), encoding="utf-8"))
    new = json.load(open(os.path.join(D, "cards", f), encoding="utf-8"))
    if len(old) != len(new):
        print(f, "COUNT", len(old), len(new)); bad += 1; continue
    for i, (a, b) in enumerate(zip(old, new)):
        errs = []
        if a["type"] != b["type"]: errs.append("type")
        if a["front"] != b["front"]: errs.append("front changed")
        if sorted(a["tags"]) != sorted(b["tags"]): errs.append("tags")
        if sorted(PRE_BLOCK.findall(a["back"])) != sorted(PRE_BLOCK.findall(b["back"])): errs.append("code blocks changed")
        if sorted(FIG.findall(a["back"])) != sorted(FIG.findall(b["back"])): errs.append("figure changed")
        missing = toks(a["back"]) - toks(b["back"])
        if missing: errs.append("numbers lost: " + ",".join(sorted(missing)[:6]))
        extra = toks(b["back"]) - toks(a["back"])
        if len(extra) > 3: errs.append("numbers added: " + ",".join(sorted(extra)[:6]))
        ma, mb = set(MATH.findall(a["back"])), set(MATH.findall(b["back"]))
        if ma - mb: errs.append("math changed/lost: %d" % len(ma - mb))
        if len(b["back"]) > 1.6 * len(a["back"]) + 200: errs.append("too long")
        if "interview trap" in a["back"].lower() and "interview trap" not in b["back"].lower(): errs.append("trap line lost")
        if errs:
            bad += 1; print(f, i, "; ".join(errs))
print("BAD" if bad else "OK", bad)
sys.exit(1 if bad else 0)
