"""Shared style + helpers for deck diagrams.

Each d_*.py module registers figures with @figure("name"); render_all.py draws them to
svg/qc_<name>.svg (shipped in the .apkg) and _preview/qc_<name>.png (local QA only).
Cards reference a figure by name via "figs_back"/"figs_front" in the card JSON.
"""
import os, contextlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, Rectangle, Polygon

HERE = os.path.dirname(os.path.abspath(__file__))
SVG_DIR = os.path.join(HERE, "svg")
PNG_DIR = os.path.join(HERE, "_preview")

# Palette: ink + 4 semantic accents. Card CSS inverts images in night mode, so
# draw on a transparent background with dark ink.
INK, BLUE, ORANGE, GREEN, RED, GREY = "#1b1b1b", "#0b5394", "#c05a00", "#2e7d32", "#c62828", "#8a8a8a"
LIGHT_BLUE, LIGHT_ORANGE, LIGHT_GREEN, LIGHT_RED = "#cfe0f3", "#f6dcc3", "#d3ead4", "#f3cfcf"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "mathtext.fontset": "dejavusans", "font.size": 11,
    "axes.edgecolor": INK, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK,
    "text.color": INK, "axes.spines.top": False, "axes.spines.right": False,
    "axes.linewidth": 0.9, "lines.linewidth": 1.8, "svg.fonttype": "path",
    "svg.hashsalt": "quantcore", "savefig.transparent": True,
})

REGISTRY = {}

def figure(name, w=5.0, h=3.0, axis=True):
    """Decorator: fn(ax) draws on a fresh axes; axis=False hides axes (schematics)."""
    def deco(fn):
        assert name not in REGISTRY, f"duplicate figure name {name}"
        REGISTRY[name] = (fn, w, h, axis)
        return fn
    return deco

def render(name, preview=True):
    fn, w, h, axis = REGISTRY[name]
    fig, ax = plt.subplots(figsize=(w, h))
    if not axis:
        ax.set_axis_off()
    fn(ax)
    fig.tight_layout(pad=0.3)
    os.makedirs(SVG_DIR, exist_ok=True)
    fig.savefig(os.path.join(SVG_DIR, f"qc_{name}.svg"), metadata={"Date": None})
    if preview:
        os.makedirs(PNG_DIR, exist_ok=True)
        fig.savefig(os.path.join(PNG_DIR, f"qc_{name}.png"), dpi=110, facecolor="white", transparent=False)
    plt.close(fig)

# ---------- schematic helpers (axis=False figures, data coords) ----------

def node(ax, xy, label, r=0.32, fc="white", ec=INK, fs=11, lw=1.4):
    ax.add_patch(Circle(xy, r, fc=fc, ec=ec, lw=lw, zorder=3))
    ax.text(*xy, label, ha="center", va="center", fontsize=fs, zorder=4)

def box(ax, xy, label, w=1.6, h=0.6, fc="white", ec=INK, fs=10, lw=1.2):
    x, y = xy
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc=fc, ec=ec, lw=lw, zorder=3))
    ax.text(x, y, label, ha="center", va="center", fontsize=fs, zorder=4)

def arrow(ax, a, b, label=None, rad=0.0, color=INK, shrink=14, fs=10, lw=1.3, label_offset=(0, 0), style="-|>"):
    """Arrow between points a->b (curved by rad); label at the midpoint (offset in data units)."""
    ax.add_patch(FancyArrowPatch(a, b, connectionstyle=f"arc3,rad={rad}", arrowstyle=style,
                                 mutation_scale=12, color=color, lw=lw, shrinkA=shrink, shrinkB=shrink, zorder=2))
    if label is not None:
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        # push label toward the bulge of a curved arrow
        dx, dy = b[0] - a[0], b[1] - a[1]
        mx += dy * rad * 0.5 + label_offset[0]
        my += -dx * rad * 0.5 + label_offset[1]
        ax.text(mx, my, label, ha="center", va="center", fontsize=fs, color=color,
                bbox=dict(fc="white", ec="none", pad=0.6), zorder=5)

def self_loop(ax, xy, label=None, r=0.32, color=INK, fs=10, up=True):
    x, y = xy
    s = 1 if up else -1
    ax.add_patch(FancyArrowPatch((x - 0.18, y + s * r * 0.85), (x + 0.18, y + s * r * 0.85),
                                 connectionstyle=f"arc3,rad={-1.6 * s}", arrowstyle="-|>", mutation_scale=11,
                                 color=color, lw=1.2, zorder=2))
    if label is not None:
        ax.text(x, y + s * (r + 0.42), label, ha="center", va="center", fontsize=fs, color=color)

def frame(ax, xmin, xmax, ymin, ymax):
    ax.set_xlim(xmin, xmax); ax.set_ylim(ymin, ymax); ax.set_aspect("equal")

def caption(ax, text, fs=9.5, color=GREY):
    """Short caption under an axis=False figure (axes-fraction coords)."""
    ax.text(0.5, -0.02, text, transform=ax.transAxes, ha="center", va="top", fontsize=fs, color=color)
