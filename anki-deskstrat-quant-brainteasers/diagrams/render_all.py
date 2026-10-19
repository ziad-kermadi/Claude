"""Render every registered figure. Usage: python3 diagrams/render_all.py [module_substring] [--no-preview]"""
import glob, importlib, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import qcfig

only = [a for a in sys.argv[1:] if not a.startswith("--")]
for f in sorted(glob.glob(os.path.join(HERE, "d_*.py"))):
    mod = os.path.basename(f)[:-3]
    if only and not any(o in mod for o in only):
        continue
    importlib.import_module(mod)
for name in sorted(qcfig.REGISTRY):
    qcfig.render(name, preview="--no-preview" not in sys.argv)
print(len(qcfig.REGISTRY), "figures rendered")
