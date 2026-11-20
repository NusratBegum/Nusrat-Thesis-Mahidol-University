"""Method diagrams of the thesis (Figures 1.1, 3.1-3.5) in the MU-IEEE-Paper print system.

    python3 figures/src/diagrams.py [preview_dir]   # writes figures/src/*.svg and figures/diag_*.pdf

Needs only the standard library and rsvg-convert (Homebrew librsvg). Units are points: the drawing
width 418 pt is the thesis text width (147.5 mm), so sizes print as drawn. The system
(docs/design/MU-IEEE-Paper.md in the workspace; Claude design system "MU-IEEE-Paper"):
Arial labels 8-9 pt, 1 pt borders, no shadows, palette below, and every role coded twice
(colour and line style) so the figures read in black and white:
  reference window  Mahidol Blue, dashed border, blue tint
  current window    ICT Green, solid fill, white text
  alarm             Amber, dotted border, amber tint
  neutral process   #595959 solid border, white
"""
import os
import random
import subprocess
import sys

SRC = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.dirname(SRC)
FONT = "Arial, Helvetica, sans-serif"
GREEN, BLUE, AMBER, NEUT, TEXT = "#006C6C", "#0035AD", "#D55E00", "#595959", "#1A1A1A"
GTINT, BTINT, ATINT, LIGHT = "#E6F0F0", "#E6EBF7", "#FBEADF", "#BFBFBF"
W = 418
B = 1.0  # border width, pt


def sub(base, s, fs, color=None, italic=True):
    c = f' fill="{color}"' if color else ""
    st = ' font-style="italic"' if italic else ""
    return (f'<tspan{st}{c}>{base}</tspan>'
            f'<tspan font-size="{fs * 0.72:.1f}" baseline-shift="-{fs * 0.22:.1f}" font-style="normal"{c}>{s}</tspan>')


def Wr(fs, color=None):
    return sub("W", "ref", fs, color)


def Wc(fs, color=None):
    return sub("W", "cur", fs, color)


class Drawing:
    def __init__(self, h, w=W):
        self.w, self.h, self.e = w, h, []

    def rect(self, x, y, w, h, fill="white", stroke=NEUT, r=2, sw=B, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.e.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{r}" fill="{fill}"{s}{d}/>')

    # the three roles
    def ref(self, x, y, w, h):
        self.rect(x, y, w, h, BTINT, BLUE, dash="3,1.6")

    def cur(self, x, y, w, h):
        self.rect(x, y, w, h, GREEN, None)

    def alarm(self, x, y, w, h):
        self.rect(x, y, w, h, ATINT, AMBER, sw=1.3, dash="0.1,2.2")
        self.e[-1] = self.e[-1].replace("/>", ' stroke-linecap="round"/>')

    def circle(self, x, y, r, fill, stroke=None, sw=B):
        s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.e.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{fill}"{s}/>')

    def text(self, x, y, s, fs=8, anchor="start", weight="normal", fill=TEXT, style="normal"):
        self.e.append(f'<text x="{x:.2f}" y="{y:.2f}" font-family="{FONT}" font-size="{fs}" text-anchor="{anchor}" '
                      f'font-weight="{weight}" font-style="{style}" fill="{fill}">{s}</text>')

    def lines(self, x, y, rows, fs=8, lead=1.25, **kw):
        for i, s in enumerate(rows):
            self.text(x, y + i * fs * lead, s, fs, **kw)

    def line(self, pts, color=NEUT, sw=B, dash=None, head=True):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        m = f' marker-end="url(#h{color[1:]})"' if head else ""
        p = " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
        self.e.append(f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="{sw}"{d}{m} '
                      f'stroke-linejoin="miter"/>')

    def save(self, name):
        heads = "".join(
            f'<marker id="h{c[1:]}" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="5" markerHeight="5" '
            f'markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0.8 L10,5 L0,9.2 z" fill="{c}"/></marker>'
            for c in (TEXT, NEUT, BLUE, GREEN, AMBER))
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}pt" height="{self.h}pt" '
               f'viewBox="0 0 {self.w} {self.h}"><defs>{heads}</defs>'
               f'<rect width="{self.w}" height="{self.h}" fill="white"/>' + "\n".join(self.e) + "</svg>\n")
        path = os.path.join(SRC, name + ".svg")
        with open(path, "w") as f:
            f.write(svg)
        subprocess.run(["rsvg-convert", "-f", "pdf", "-o", os.path.join(FIG, f"diag_{name}.pdf"), path], check=True)
        if len(sys.argv) > 1:
            subprocess.run(["rsvg-convert", "-z", "3", "-o", os.path.join(sys.argv[1], f"diag_{name}.png"), path],
                           check=True)


# ---------------------------------------------------------------- Figure 3.1
def overview():
    d = Drawing(244)
    # EADD as a block diagram inside its boundary
    d.text(0, 10, "EADD", 9, weight="bold")
    d.rect(56, 16, 362, 128, "none", NEUT, r=3, sw=0.8, dash="4,2")
    # input stream
    d.text(0, 62, "Stream", 9, weight="bold")
    for k in range(13):
        d.line([(2 + k * 3.4, 70), (2 + k * 3.4, 78)], NEUT, 0.8, head=False)
    d.text(0, 90, sub("x", "1", 8) + ", " + sub("x", "2", 8) + ", ...", 8)
    d.line([(46, 74), (54, 74), (54, 55), (63.5, 55)], NEUT)
    d.line([(54, 74), (54, 103), (63.5, 103)], NEUT)
    # windows
    d.ref(64, 38, 86, 34)
    d.text(70, 52, "Reference " + Wr(9, BLUE), 9, weight="bold", fill=BLUE)
    d.text(70, 64, "reservoir of 500", 8)
    d.cur(64, 86, 86, 34)
    d.text(70, 100, "Current " + Wc(9, "white"), 9, weight="bold", fill="white")
    d.text(70, 112, "newest 200", 8, fill="white")
    d.line([(150, 55), (157, 55), (157, 72), (163.5, 72)], BLUE)
    d.line([(150, 103), (157, 103), (157, 86), (163.5, 86)], GREEN)
    # classifier test
    d.rect(164, 58, 62, 42)
    d.text(195, 73, "C2ST", 9, "middle", "bold")
    d.lines(195, 84, ["LightGBM,", "5-fold AUC"], 8, anchor="middle")
    d.line([(226, 79), (271.5, 79)], NEUT)
    d.text(249, 74, "AUC ≥ 0.7", 8, "middle")
    # permutation test
    d.rect(272, 56, 64, 46)
    d.lines(304, 70, ["History-null", "test (ASPT)"], 9, lead=1.15, anchor="middle", weight="bold")
    d.text(304, 94, '<tspan font-style="italic">p</tspan>-value', 8, "middle")
    d.line([(336, 79), (361.5, 79)], NEUT)
    d.text(349, 74, '<tspan font-style="italic">p</tspan> ≤ <tspan font-style="italic">α</tspan>', 8, "middle")
    # alarm and attribution
    d.alarm(362, 64, 50, 30)
    d.text(387, 82, "Alarm", 9, "middle", "bold", AMBER)
    d.rect(346, 108, 66, 28)
    d.text(379, 120, "TreeSHAP", 9, "middle", "bold")
    d.text(379, 131, "feature ranking", 8, "middle")
    d.line([(387, 94), (387, 107.5)], AMBER)
    d.line([(387, 64), (387, 28), (107, 28), (107, 37.5)], AMBER, dash="3,2")
    d.text(247, 25, "reference reset", 8, "middle", fill=AMBER)
    # hypothesis tested by each component, under the block
    d.text(107, 131, "H1", 8, "middle", "bold", GREEN)
    d.text(304, 113, "H2, H3", 8, "middle", "bold", GREEN)
    d.text(340, 125, "H4", 8, "end", "bold", GREEN)

    # evaluation
    ey = 176
    d.text(0, ey - 8, "Evaluation", 9, weight="bold")
    d.line([(236, 144), (236, ey - 0.5)], NEUT)
    d.rect(0, ey, W, 66, "white", NEUT, r=3)
    segs = [("Streams", ["synthetic,", "injected drift,", "INSECTS,", "no drift"]),
            ("Detectors", ["EADD,", "D3-LightGBM, D3;", "identical setup"]),
            ("Metrics", ["recall, MTD,", "false alarms,", "precision@k,", "permutations"]),
            ("Registered tests", ["Wilcoxon, Holm,", "TOST, Friedman,", "stream means"]),
            ("Decisions", ["H1 to H4", "by registered", "decision rules"])]
    sw = W / len(segs)
    for i, (t, rows) in enumerate(segs):
        x = i * sw
        d.text(x + 7, ey + 14, t, 9, weight="bold", fill=GREEN if i == 4 else TEXT)
        d.lines(x + 7, ey + 27, rows, 8)
        if i:
            d.line([(x - 4, ey + 40), (x + 3.5, ey + 40)], NEUT, head=True)
            d.line([(x, ey + 8), (x, ey + 30)], LIGHT, 0.5, head=False)
            d.line([(x, ey + 50), (x, ey + 60)], LIGHT, 0.5, head=False)
    d.save("overview")


# ---------------------------------------------------------------- Figure 3.2
def diamond(d, cx, cy, hw, hh, label):
    pts = f"{cx},{cy - hh} {cx + hw},{cy} {cx},{cy + hh} {cx - hw},{cy}"
    d.e.append(f'<polygon points="{pts}" fill="white" stroke="{TEXT}" stroke-width="{B}"/>')
    d.text(cx, cy + 3, label, 8.5, "middle")


def pipeline():
    d = Drawing(364)
    cx = 170
    d.rect(cx - 116, 2, 232, 20, "white", NEUT)
    d.text(cx, 15.5, "Data stream " + sub("x", "1", 8.5) + ", " + sub("x", "2", 8.5) + ", ..., checked every 50 samples",
           8.5, "middle")
    wy, wh = 38, 40
    d.ref(cx - 140, wy, 132, wh)
    d.text(cx - 133, wy + 14, "Reservoir reference " + Wr(9, BLUE), 9, weight="bold", fill=BLUE)
    d.lines(cx - 133, wy + 26, ["500 samples drawn uniformly", "since the last alarm"], 8)
    d.cur(cx + 8, wy, 132, wh)
    d.text(cx + 15, wy + 14, "Current window " + Wc(9, "white"), 9, weight="bold", fill="white")
    d.lines(cx + 15, wy + 26, ["the 200 newest samples;", "they enter the reservoir on exit"], 8, fill="white")
    for x, c in ((cx - 74, BLUE), (cx + 74, GREEN)):
        d.line([(x, 22), (x, wy - 0.5)], NEUT)
        d.line([(x, wy + wh), (x, 95.5)], c)
    d.rect(cx - 140, 96, 280, 32)
    d.text(cx, 109, '<tspan font-weight="bold">C2ST:</tspan> label ' + Wr(8.5) + " as 0 and " + Wc(8.5)
           + " as 1; LightGBM with", 8.5, "middle")
    d.text(cx, 121, "stratified 5-fold cross-validation gives the out-of-fold AUC", 8.5, "middle")
    d.line([(cx, 128), (cx, 139.5)], TEXT)
    diamond(d, cx, 158, 62, 18, 'AUC ≥ <tspan font-style="italic">τ</tspan> = 0.7?')
    d.line([(cx, 176), (cx, 191.5)], TEXT)
    d.text(cx + 4, 187, "yes", 8, fill=NEUT)
    d.rect(cx - 140, 192, 280, 42)
    d.text(cx, 205, '<tspan font-weight="bold">ASPT with the history null:</tspan> AUCs of earlier 200-sample', 8.5,
           "middle")
    d.text(cx, 216.5, "windows (one start every 10 samples) against " + Wr(8.5) + ",", 8.5, "middle")
    d.text(cx, 228, "drawn one at a time in random order, at most 199", 8.5, "middle")
    d.line([(cx, 234), (cx, 245.5)], TEXT)
    diamond(d, cx, 264, 62, 18, 'reject ' + sub("H", "0", 8.5) + ' at <tspan font-style="italic">α</tspan> = 0.05?')
    d.line([(cx, 282), (cx, 292.5)], TEXT)
    d.text(cx + 4, 290, "yes", 8, fill=NEUT)
    d.alarm(cx - 32, 293, 64, 18)
    d.text(cx, 305.5, "Alarm", 9, "middle", "bold", AMBER)
    for x0, title, rows in ((cx - 144, "TreeSHAP ranking", ["features ranked by mean |SHAP|", "(model fit on all 700 samples)"]),
                            (cx + 4, "New reference", ["last " + Wc(8) + " plus the next", "300 samples"])):
        d.rect(x0, 322, 140, 40)
        d.text(x0 + 7, 334, title, 9, weight="bold")
        d.lines(x0 + 7, 345, rows, 8, lead=1.2)
    d.line([(cx - 12, 311), (cx - 12, 316), (cx - 74, 316), (cx - 74, 321.5)], AMBER)
    d.line([(cx + 12, 311), (cx + 12, 316), (cx + 74, 316), (cx + 74, 321.5)], AMBER)
    nx = 368
    d.rect(nx - 44, 194, 88, 38)
    d.text(nx, 209, "No alarm", 9, "middle", "bold")
    d.text(nx, 222, "next check: 50 samples", 8, "middle")
    d.line([(cx + 62, 158), (nx, 158), (nx, 193.5)], NEUT)
    d.text(cx + 68, 154, "no", 8, fill=NEUT)
    d.line([(cx + 62, 264), (nx, 264), (nx, 232.5)], NEUT)
    d.text(cx + 68, 260, "no", 8, fill=NEUT)
    d.save("pipeline")


# ---------------------------------------------------------------- Figure 3.3
def reference():
    d = Drawing(156)
    X = lambda s: 78 + s * 0.0552  # samples since the last alarm -> pt (5,800 samples)
    dr, t, end = 4000, 5000, 5800
    d.rect(X(dr), 4, X(t) - X(dr), 122, "#F2F2F2", None, r=0)
    top, bot = 10, 34
    d.e.append(f'<polygon points="{X(dr)},{bot} {X(t)},{top} {X(end)},{top} {X(end)},{bot}" fill="{LIGHT}"/>')
    d.line([(X(0), bot), (X(dr), bot), (X(t), top), (X(end), top)], TEXT, 1.2, head=False)
    d.text(X(0) - 3, bot + 3, "0", 8, "end", fill=NEUT)
    d.text(X(0) - 3, top + 3, "1", 8, "end", fill=NEUT)
    d.text(X(0) + 2, bot - 5, "share of the new concept", 8, fill=NEUT)
    for name, det, y in (("Sliding", "(D3)", 64), ("Reservoir", "(EADD)", 102)):
        d.text(70, y - 3, name, 9, "end", "bold")
        d.text(70, y + 8, det, 8, "end", fill=NEUT)
        d.line([(X(0), y + 6), (X(end), y + 6)], LIGHT, 0.8, head=False)
        d.cur(X(t - 200), y - 6, X(t) - X(t - 200), 12)
        d.text(X(t) + 3, y + 4, Wc(8.5, GREEN), 8.5)
    y = 64
    d.ref(X(t - 700), y - 6, X(t - 200) - X(t - 700), 12)
    d.text(X(t - 450), y - 10, Wr(8.5, BLUE), 8.5, "middle")
    y = 102
    r = random.Random(7)
    for k in range(64):
        s = r.random() * (t - 200)
        d.rect(X(s), y - 6 + r.random() * 8, 1.4, 3.6, BLUE, None, r=0)
    d.text(X(1800), y + 20, Wr(8.5, BLUE) + ": uniform sample since the last alarm", 8, "middle", fill=BLUE)
    for s in (dr, t):
        d.line([(X(s), 4), (X(s), 130)], TEXT, 0.8, "2,1.6", head=False)
    d.line([(X(0), 142), (X(end) + 8, 142)], TEXT)
    for s, lab in ((0, "last alarm"), (dr, "d"), (t, "t")):
        d.line([(X(s), 139), (X(s), 145)], TEXT, head=False)
        d.text(X(s), 154, lab, 8, "middle", style="italic" if len(lab) == 1 else "normal", fill=NEUT)
    d.text(X(end) + 8, 154, "time", 8, "end", fill=NEUT)
    d.save("reference")


# ---------------------------------------------------------------- Figure 3.4
def history_null():
    d = Drawing(214)
    hx0, hx1, cw = 14, 316, 44
    d.text(hx0, 11, "history since the last alarm (at most 5,000 samples)", 8, fill=NEUT)
    d.rect(hx0, 16, hx1 - hx0, 14, "white", NEUT, r=0)
    d.cur(hx1, 16, cw, 14)
    d.text(hx1 + cw / 2, 26.5, Wc(9, "white"), 9, "middle")
    for k in range(6):
        d.rect(hx0 + 4.5 * k, 35 + 5 * k, cw, 3.6, NEUT, None, r=0)
        d.rect(hx1 - cw - 4.5 * (5 - k), 35 + 5 * k, cw, 3.6, NEUT, None, r=0)
    d.text((hx0 + hx1) / 2, 52, ". . .", 9, "middle", fill=NEUT)
    d.line([(hx1, 14), (hx1, 70)], TEXT, 0.8, "2,1.6", head=False)
    d.text(hx0, 75, "earlier windows: length 200, stride 10", 8, fill=NEUT)
    by, bh = 96, 34
    d.rect(hx0, by, 150, bh)
    d.text(hx0 + 75, by + 14, "Earlier window vs " + Wr(9), 9, "middle", "bold")
    d.text(hx0 + 75, by + 26, "5-fold C2ST: null AUC", 8, "middle")
    d.rect(258, by, 146, bh)
    d.text(331, by + 14, Wc(9) + " vs " + Wr(9), 9, "middle", "bold")
    d.text(331, by + 26, "5-fold C2ST: observed AUC", 8, "middle")
    d.ref(186, by + 7, 50, 20)
    d.text(211, by + 20.5, Wr(9, BLUE), 9, "middle")
    d.line([(186, by + 17), (hx0 + 150.5, by + 17)], BLUE)
    d.line([(236, by + 17), (257.5, by + 17)], BLUE)
    d.line([(hx0 + 60, 80), (hx0 + 60, by - 0.5)], NEUT)
    d.line([(hx1 + cw / 2, 30), (hx1 + cw / 2, by - 0.5)], GREEN)
    base, hx = 198, 120
    hs = [4, 10, 19, 28, 33, 29, 21, 13, 7, 3, 1]
    for k, h in enumerate(hs):
        d.rect(hx + k * 9, base - h, 8, h, LIGHT, NEUT, r=0, sw=0.5)
    d.line([(hx - 6, base), (hx + 122, base)], TEXT, head=False)
    d.line([(hx + 112, base), (hx + 112, base - 38)], GREEN, 1.8, head=False)
    d.text(hx + 48, base + 11, "null distribution (at most 199 draws)", 8, "middle", fill=NEUT)
    d.text(hx + 116, base - 30, "observed", 8, fill=GREEN)
    d.line([(hx0 + 75, by + bh), (hx0 + 75, 184), (hx - 4.5, 184)], NEUT)
    d.line([(331, by + bh), (331, 146), (hx + 112, 146), (hx + 112, base - 39.5)], GREEN)
    d.rect(274, 164, 130, 42, "white", NEUT)
    d.text(339, 179, '<tspan font-style="italic">p</tspan> = (<tspan font-style="italic">c</tspan> + 1) / '
                     '(<tspan font-style="italic">B</tspan> + 1)', 9.5, "middle")
    d.text(339, 190.5, '<tspan font-style="italic">c</tspan>: null AUCs ≥ observed', 8, "middle", fill=NEUT)
    d.text(339, 200.5, '<tspan font-style="italic">B</tspan>: number of draws', 8, "middle", fill=NEUT)
    d.save("history_null")


# ---------------------------------------------------------------- Figure 1.1
def roadmap():
    d = Drawing(178)
    cols = [(0, "Limitation of D3"), (170, "Component of EADD"), (336, "Hypothesis")]
    for x, h in cols:
        d.text(x, 10, h, 9, weight="bold")
    d.line([(0, 16), (W, 16)], TEXT, head=False)
    rows = [(["the sliding reference moves", "with slow drift"], "Reservoir reference", "since the last alarm", "H1", "slow drift"),
            (["a fixed AUC threshold raises false", "alarms on autocorrelated data"], "History-null test", "earlier windows as the null", "H2", "false alarms"),
            (["a full permutation test needs", "many model fits"], "ASPT", "stops once the result is clear", "H3", "cost"),
            (["no information on which", "features drifted"], "TreeSHAP ranking", "after every alarm", "H4", "attribution")]
    for i, (prob, comp, note, h, what) in enumerate(rows):
        y = 20 + i * 39
        d.lines(0, y + 15, prob, 8)
        d.line([(146, y + 18), (163.5, y + 18)], NEUT)
        d.text(170, y + 15, comp, 9, weight="bold")
        d.text(170, y + 26, note, 8, fill=NEUT)
        d.line([(312, y + 18), (329.5, y + 18)], NEUT)
        d.text(336, y + 15, h, 9, weight="bold", fill=GREEN)
        d.text(336, y + 26, what, 8)
        d.line([(0, y + 35), (W, y + 35)], TEXT if i == 3 else LIGHT, B if i == 3 else 0.5, head=False)
    d.save("roadmap")


# ---------------------------------------------------------------- Figure 3.5
def timeline():
    d = Drawing(96)
    stages = [("Initial runs", ["earlier EADD on", "13 real streams"], "seeds 42 to 442"),
              ("Benchmark", ["12 detectors;", "flaws fixed"], "seeds 42 to 442"),
              ("Confirmatory", ["revised H1 to H4,", "registered"], "seeds 1000 to 1009"),
              ("Final test", ["same schedule for", "all, registered"], "seeds 3000 to 3009"),
              ("Secondary", ["newer detectors,", "three checks"], "subsets of 3000 to 3009")]
    notes = ["four flaws identified", "H1 restricted to slow drift", "H2, H3a re-specified"]
    xs = [40 + i * 82 for i in range(5)]
    ly = 56
    d.line([(xs[0], ly), (xs[-1], ly)], NEUT, B, head=False)
    for i, ((t, rows, seeds), x) in enumerate(zip(stages, xs)):
        final = i == 3
        d.text(x, 10, t, 9, "middle", "bold", GREEN if final else TEXT)
        d.lines(x, 22, rows, 8, anchor="middle")
        d.circle(x, ly, 4.5 if final else 3.4, GREEN if final else "white", GREEN if final else NEUT, B)
        d.text(x, ly + 16, seeds, 8, "middle", fill=NEUT)
    for i, n in enumerate(notes):
        d.text((xs[i] + xs[i + 1]) / 2, ly + 30, n, 8, "middle", style="italic")
        d.line([((xs[i] + xs[i + 1]) / 2, ly + 21), ((xs[i] + xs[i + 1]) / 2, ly + 2)], LIGHT, 0.5, head=False)
    d.save("timeline")


if __name__ == "__main__":
    for f in (overview, pipeline, reference, history_null, roadmap, timeline):
        f()
