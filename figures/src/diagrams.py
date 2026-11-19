"""Method diagrams of the thesis (Figures 1.1, 3.1-3.5) as SVG, converted to vector PDF.

    python3 figures/src/diagrams.py            # writes figures/src/*.svg and figures/diag_*.pdf

Needs only the standard library and rsvg-convert (Homebrew librsvg). Units are points:
the drawing width 418 pt equals the text width (147.5 mm), so font sizes are the printed sizes.
Colour code used in every figure: blue = reference window, amber = current window, red = alarm.
"""
import os
import random
import subprocess
import sys

SRC = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.dirname(SRC)
FONT = "Times New Roman"
INK, MUT, RULE, PROC = "#1E2B3A", "#56636F", "#A3ADB8", "#EEF1F4"
REF, REFT = "#2F6497", "#DCE7F3"
CUR, CURT = "#B5710B", "#F8E8C8"
ALM, ALMT = "#A3302F", "#F6DCDA"
NULLC = "#B7C0CA"
W = 418


def Wsub(sub, fs, color=None):
    c = f' fill="{color}"' if color else ""
    return (f'<tspan font-style="italic"{c}>W</tspan>'
            f'<tspan font-size="{fs * 0.68:.1f}" baseline-shift="-{fs * 0.2:.1f}"{c}>{sub}</tspan>')


class Drawing:
    def __init__(self, h, w=W):
        self.w, self.h, self.e = w, h, []

    def rect(self, x, y, w, h, fill="white", stroke=RULE, r=0, sw=0.7, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.e.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{r}" fill="{fill}"{s}{d}/>')

    def circle(self, x, y, r, fill, stroke=None, sw=0.7):
        s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.e.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{fill}"{s}/>')

    def text(self, x, y, s, fs=8, anchor="start", weight="normal", fill=INK, style="normal"):
        self.e.append(f'<text x="{x:.2f}" y="{y:.2f}" font-family="{FONT}" font-size="{fs}" text-anchor="{anchor}" '
                      f'font-weight="{weight}" font-style="{style}" fill="{fill}">{s}</text>')

    def lines(self, x, y, rows, fs=7.6, lead=1.22, **kw):
        for i, s in enumerate(rows):
            self.text(x, y + i * fs * lead, s, fs, **kw)

    def line(self, pts, color=MUT, sw=0.8, dash=None, head=True):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        m = f' marker-end="url(#h{color[1:]})"' if head else ""
        p = " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
        self.e.append(f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="{sw}"{d}{m} '
                      f'stroke-linejoin="round"/>')

    def badge(self, x, y, label, fill=INK):
        w = 6 + 4.3 * len(label)
        self.rect(x, y, w, 10.5, fill, None, r=5.25)
        self.text(x + w / 2, y + 7.6, label, 7.2, "middle", "bold", "white")
        return w

    def num(self, x, y, n):
        self.circle(x, y, 6.2, INK)
        self.text(x, y + 2.7, n, 7.6, "middle", "bold", "white")

    def save(self, name):
        heads = "".join(
            f'<marker id="h{c[1:]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5.5" markerHeight="5.5" '
            f'markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1.2 L10,5 L0,8.8 z" fill="{c}"/></marker>'
            for c in (INK, MUT, REF, CUR, ALM))
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}pt" height="{self.h}pt" '
               f'viewBox="0 0 {self.w} {self.h}"><defs>{heads}</defs>' + "\n".join(self.e) + "</svg>\n")
        path = os.path.join(SRC, name + ".svg")
        with open(path, "w") as f:
            f.write(svg)
        subprocess.run(["rsvg-convert", "-f", "pdf", "-o", os.path.join(FIG, f"diag_{name}.pdf"), path], check=True)
        if len(sys.argv) > 1:  # preview folder
            subprocess.run(["rsvg-convert", "-z", "3", "-b", "white", "-o",
                            os.path.join(sys.argv[1], f"diag_{name}.png"), path], check=True)


# ---------------------------------------------------------------- Figure 3.1
def overview():
    d = Drawing(306)
    # panel A heading and legend
    d.text(1, 10, 'The detector <tspan font-weight="normal" fill="%s">(Sections 3.2 to 3.4)</tspan>' % MUT, 9.2,
           weight="bold")
    bw = d.badge(W - 150, 2.5, "H1")
    d.text(W - 150 + bw + 4, 10, "hypothesis that tests the component", 7.4, fill=MUT)

    # the stream: cells since the last alarm; reservoir picks in blue, newest 200 in amber
    x0, cw, n, y0, ch = 30, 6, 63, 30, 10
    rnd = random.Random(4)
    picks = set(rnd.sample(range(n - 9), 15))
    for i in range(n):
        fill = CUR if i >= n - 9 else (REF if i in picks else "white")
        d.rect(x0 + i * cw, y0, cw, ch, fill, "white" if fill != "white" else RULE, sw=0.5)
    d.rect(x0, y0, n * cw, ch, "none", MUT, sw=0.6)
    d.text(x0 - 4, y0 + 7.4, "stream", 7.6, "end", style="italic", fill=MUT)
    d.text(x0, y0 - 4, "since the last alarm", 7.2, fill=MUT)
    d.text(x0 + n * cw, y0 - 4, "now; a check every 50 samples", 7.2, "end", fill=MUT)
    d.text(x0 + 30, y0 + ch + 10, Wsub("ref", 8, REF) + ': 500 samples drawn uniformly from the past (reservoir)',
           8, fill=REF)
    d.text(x0 + n * cw, y0 + ch + 10, Wsub("cur", 8, CUR) + ": newest 200", 8, "end", fill=CUR)
    d.line([(x0 + 10, y0 + ch), (x0 + 10, 76)], MUT)

    # four stages
    cy, chh, cwid, gap = 76, 122, 95, 12
    xs = [1 + i * (cwid + gap) for i in range(4)]
    titles = ["Two windows", "C2ST", "Permutation test", "Alarm"]
    body = [["reservoir reference and", "newest window become", "the two classes"],
            ["LightGBM separates the", "windows; the 5-fold AUC", "must reach 0.7"],
            ["null AUCs from earlier", "windows of the stream;", "ASPT stops early"],
            ["TreeSHAP ranks the", "features; a new", "reference starts"]]
    for i, x in enumerate(xs):
        d.rect(x, cy, cwid, chh, "white", RULE, r=3)
        d.num(x + 10, cy + 11, str(i + 1))
        d.text(x + 20, cy + 14, titles[i], 9, weight="bold")
        d.lines(x + 7, cy + 84, body[i], 7.6, fill=MUT)
        if i < 3:
            d.line([(x + cwid, cy + 48), (x + cwid + gap - 0.5, cy + 48)], INK)
    gy = cy + 24  # glyph area top
    # 1: the two windows, widths 500 : 200
    x = xs[0]
    d.rect(x + 9, gy + 12, 50, 16, REF, None, r=1.5)
    d.rect(x + 63, gy + 12, 20, 16, CUR, None, r=1.5)
    d.text(x + 34, gy + 23, Wsub("ref", 8.5, "white"), 8.5, "middle", fill="white")
    d.text(x + 73, gy + 23, Wsub("cur", 8.5, "white"), 8.5, "middle", fill="white")
    d.text(x + 34, gy + 39, "label 0", 7.2, "middle", fill=REF)
    d.text(x + 73, gy + 39, "label 1", 7.2, "middle", fill=CUR)
    # 2: two point clouds and an axis-aligned (tree) boundary
    x = xs[1]
    px, py, pw, ph = x + 18, gy, 60, 46
    d.rect(px, py, pw, ph, "white", RULE, sw=0.5)
    r2 = random.Random(11)
    for k in range(22):
        d.circle(px + 5 + r2.random() * 30, py + 18 + r2.random() * 24, 1.5, REF)
        d.circle(px + 25 + r2.random() * 30, py + 4 + r2.random() * 24, 1.5, CUR)
    d.line([(px + 3, py + 34), (px + 22, py + 34), (px + 22, py + 22), (px + 38, py + 22), (px + 38, py + 9),
            (px + pw - 3, py + 9)], INK, 0.9, "2.2,1.6", head=False)
    # 3: histogram of null AUCs, observed AUC in the tail
    x = xs[2]
    base = gy + 40
    hs = [3, 8, 15, 22, 25, 20, 13, 7, 3, 1]
    for k, h in enumerate(hs):
        d.rect(x + 12 + k * 6, base - h, 5.2, h, NULLC, None)
    d.line([(x + 10, base), (x + 86, base)], MUT, 0.6, head=False)
    d.line([(x + 83, base), (x + 83, gy + 6)], CUR, 1.4, head=False)
    d.text(x + 81, gy + 6, "observed", 7, "end", fill=CUR)
    d.text(x + 40, base + 8, "null AUCs", 7, "middle", fill=MUT)
    # 4: alarm and feature ranking
    x = xs[3]
    d.rect(x + 9, gy - 1, 34, 11, ALM, None, r=5.5)
    d.text(x + 26, gy + 7, "alarm", 7.4, "middle", "bold", "white")
    for k, (lab, v) in enumerate([("x3", 52), ("x7", 44), ("x1", 13), ("x9", 9), ("x5", 6)]):
        yy = gy + 15 + k * 6.2
        d.text(x + 20, yy + 4.4, lab, 6.4, "end", style="italic", fill=MUT)
        d.rect(x + 23, yy, v, 4.6, INK if k < 2 else NULLC, None)
    # hypotheses tested by each component; the classifier is shared with D3-LightGBM
    d.badge(xs[0] + 7, cy + chh - 15, "H1")
    d.text(xs[1] + 7, cy + chh - 7, "same as D3-LightGBM", 7.2, style="italic", fill=MUT)
    bx = xs[2] + 7
    bx += d.badge(bx, cy + chh - 15, "H2") + 3
    d.badge(bx, cy + chh - 15, "H3")
    d.badge(xs[3] + 7, cy + chh - 15, "H4")
    # after an alarm the last current window starts a new reference
    fy = cy - 7
    d.line([(xs[3] + 60, cy), (xs[3] + 60, fy), (xs[0] + 60, fy), (xs[0] + 60, cy)], ALM, 0.8, "3,2")
    d.text((xs[0] + xs[3]) / 2 + 60, fy - 3, "after an alarm: a new reference from the last current window", 7.2,
           "middle", style="italic", fill=ALM)

    # panel B: the evaluation
    by = cy + chh
    d.text(1, by + 22, 'The evaluation <tspan font-weight="normal" fill="%s">(Sections 3.5 to 3.10)</tspan>' % MUT,
           9.2, weight="bold")
    d.line([(150, by), (150, by + 34)], INK)
    d.text(155, by + 20, "EADD is run beside two baselines under one setup", 7.4, style="italic", fill=MUT)
    ey, ew, eh, eg = by + 34, 74.4, 66, 11
    boxes = [("Streams", ["synthetic, injected", "and INSECTS drift;", "no drift; AR(1)"], "3.7"),
             ("Detectors", ["EADD, D3 and", "D3-LightGBM, same", "windows and checks"], "3.5, 3.6"),
             ("Metrics", ["recall, MTD, false", "alarms, precision@k,", "null draws per test"], "3.8"),
             ("Registered tests", ["Wilcoxon with Holm,", "TOST, Friedman", "over stream means"], "3.9, 3.10"),
             ("Decisions", ["H1 to H4 supported", "or not by the", "registered rules"], "Chapter 4")]
    for i, (t, rows, sec) in enumerate(boxes):
        x = 1 + i * (ew + eg)
        last = i == len(boxes) - 1
        d.rect(x, ey, ew, eh, PROC if not last else "white", INK if last else None, r=3, sw=1.0)
        d.text(x + 6, ey + 13, t, 8.6, weight="bold")
        d.lines(x + 6, ey + 25, rows, 7.4, fill=MUT)
        d.text(x + ew - 5, ey + eh - 5, sec, 6.8, "end", style="italic", fill=MUT)
        if not last:
            d.line([(x + ew, ey + eh / 2), (x + ew + eg - 0.5, ey + eh / 2)], INK)
    d.save("overview")


# ---------------------------------------------------------------- Figure 3.2
def diamond(d, cx, cy, hw, hh, label):
    pts = f"{cx},{cy - hh} {cx + hw},{cy} {cx},{cy + hh} {cx - hw},{cy}"
    d.e.append(f'<polygon points="{pts}" fill="white" stroke="{INK}" stroke-width="0.8"/>')
    d.text(cx, cy + 3, label, 8.2, "middle")


def pipeline():
    d = Drawing(352)
    cx = 168
    # stream
    d.rect(cx - 120, 2, 240, 20, PROC, None, r=3)
    d.text(cx, 15.5, 'Data stream <tspan font-style="italic">x</tspan><tspan font-size="5.6" baseline-shift="-1.6">1</tspan>, '
                     '<tspan font-style="italic">x</tspan><tspan font-size="5.6" baseline-shift="-1.6">2</tspan>, ..., '
                     'checked every 50 samples', 8.4, "middle")
    # the two windows
    wy, wh = 38, 40
    d.rect(cx - 140, wy, 132, wh, REFT, REF, r=2, sw=0.8)
    d.text(cx - 134, wy + 13, "Reservoir reference " + Wsub("ref", 8.6), 8.6, weight="bold", fill=REF)
    d.lines(cx - 134, wy + 24, ["500 samples drawn uniformly from all", "samples since the last alarm"], 7.4, fill=INK)
    d.rect(cx + 8, wy, 132, wh, CURT, CUR, r=2, sw=0.8)
    d.text(cx + 14, wy + 13, "Current window " + Wsub("cur", 8.6), 8.6, weight="bold", fill=CUR)
    d.lines(cx + 14, wy + 24, ["the newest 200 samples; a sample", "enters the reservoir when it leaves"], 7.4)
    for x in (cx - 74, cx + 74):
        d.line([(x, 22), (x, wy)], MUT)
        d.line([(x, wy + wh), (x, 96)], MUT)
    # C2ST
    d.rect(cx - 140, 96, 280, 32, "white", INK, r=3, sw=0.8)
    d.text(cx, 109, '<tspan font-weight="bold">C2ST:</tspan> label ' + Wsub("ref", 8.4) + " as 0 and " + Wsub("cur", 8.4)
           + " as 1; LightGBM,", 8.4, "middle")
    d.text(cx, 121, "stratified 5-fold cross-validation, out-of-fold AUC", 8.4, "middle")
    d.line([(cx, 128), (cx, 140)], INK)
    diamond(d, cx, 158, 64, 18, 'AUC ≥ <tspan font-style="italic">τ</tspan> = 0.7?')
    d.line([(cx, 176), (cx, 192)], INK)
    d.text(cx + 4, 187, "yes", 7.4, fill=MUT)
    # ASPT
    d.rect(cx - 140, 192, 280, 42, "white", INK, r=3, sw=0.8)
    d.text(cx, 205, '<tspan font-weight="bold">ASPT with the history null:</tspan> AUCs of earlier 200-sample', 8.4, "middle")
    d.text(cx, 216, "windows of the stream (one start every 10 samples) against " + Wsub("ref", 8.4) + ",", 8.4, "middle")
    d.text(cx, 227, "drawn one at a time in random order, at most 199", 8.4, "middle")
    d.line([(cx, 234), (cx, 246)], INK)
    diamond(d, cx, 264, 64, 18, 'reject <tspan font-style="italic">H</tspan><tspan font-size="5.8" '
                                'baseline-shift="-1.6">0</tspan> at <tspan font-style="italic">α</tspan> = 0.05?')
    d.line([(cx, 282), (cx, 294)], INK)
    d.text(cx + 4, 291, "yes", 7.4, fill=MUT)
    # alarm and what follows
    d.rect(cx - 30, 294, 60, 15, ALM, None, r=7.5)
    d.text(cx, 304.6, "Alarm", 8.6, "middle", "bold", "white")
    for x0, title, rows in ((cx - 140, "TreeSHAP ranking", ["features ranked by mean |SHAP| of a", "model trained on all 700 samples"]),
                            (cx + 8, "New reference", ["the last " + Wsub("cur", 7.4) + " plus the next 300 samples;",
                                                       "the next check comes 500 samples later"])):
        d.rect(x0, 318, 132, 32, ALMT, None, r=3)
        d.text(x0 + 6, 329, title, 8.4, weight="bold", fill=ALM)
        d.lines(x0 + 6, 339.5, rows, 7.4)
    d.line([(cx - 10, 309), (cx - 10, 313), (cx - 74, 313), (cx - 74, 318)], ALM, head=True)
    d.line([(cx + 10, 309), (cx + 10, 313), (cx + 74, 313), (cx + 74, 318)], ALM, head=True)
    # no alarm
    nx = 352
    d.rect(nx - 46, 194, 92, 38, PROC, None, r=3)
    d.text(nx, 209, "No alarm", 8.4, "middle", "bold")
    d.text(nx, 221, "next check in 50 samples", 7.4, "middle", fill=MUT)
    d.line([(cx + 64, 158), (nx, 158), (nx, 194)], MUT)
    d.text(cx + 70, 155, "no", 7.4, fill=MUT)
    d.line([(cx + 64, 264), (nx, 264), (nx, 232)], MUT)
    d.text(cx + 70, 261, "no", 7.4, fill=MUT)
    d.save("pipeline")


# ---------------------------------------------------------------- Figure 3.3
def reference():
    d = Drawing(150)
    X = lambda s: 74 + s * 0.0569  # samples since the last alarm -> pt; 5,800 samples
    dr, t = 4000, 5000
    d.rect(X(dr), 4, X(t) - X(dr), 118, "#F3F4F6", None)
    # share of the new concept
    top, bot = 10, 34
    d.e.append(f'<polygon points="{X(dr)},{bot} {X(t)},{top} {X(5800)},{top} {X(5800)},{bot}" fill="{NULLC}"/>')
    d.line([(X(0), bot), (X(dr), bot), (X(t), top), (X(5800), top)], INK, 0.9, head=False)
    d.text(X(0) - 3, bot + 2.5, "0", 7.2, "end", fill=MUT)
    d.text(X(0) - 3, top + 2.5, "1", 7.2, "end", fill=MUT)
    d.text(X(0) + 2, bot - 5, "share of samples from the new concept", 7.4, fill=MUT)
    rows = [("Sliding", "(D3)", 62), ("Reservoir", "(EADD)", 98)]
    for name, det, y in rows:
        d.text(66, y - 4, name, 8.4, "end", "bold")
        d.text(66, y + 6, det, 7.6, "end", fill=MUT)
        d.line([(X(0), y + 6), (X(5800), y + 6)], RULE, 0.6, head=False)
        d.rect(X(t - 200), y - 6, X(t) - X(t - 200), 12, CUR, None)
    # sliding: the 500 samples just before the current window
    y = 62
    d.rect(X(t - 700), y - 6, X(t - 200) - X(t - 700), 12, REF, None)
    d.text(X(t - 450), y - 9, Wsub("ref", 8, REF), 8, "middle")
    d.text(X(t) + 3, y + 3, Wsub("cur", 8, CUR), 8)
    d.text(X(dr) - 6, y + 2, "both windows partly new: hard to separate", 7.4, "end", style="italic", fill=INK)
    # reservoir: 500 samples spread over the whole period
    y = 98
    r = random.Random(7)
    for k in range(70):
        s = r.random() * (t - 200)
        d.rect(X(s), y - 6 + r.random() * 9, 1.6, 3, REF, None)
    d.text(X(t) + 3, y + 3, Wsub("cur", 8, CUR), 8)
    d.text(X(1900), y + 17, Wsub("ref", 8, REF) + ": 500 samples spread over the period, most from before the drift",
           7.6, "middle", fill=REF)
    # markers and axis
    for s, lab in ((dr, "drift starts"), (t, "check")):
        d.line([(X(s), 4), (X(s), 126)], INK, 0.6, "2,1.6", head=False)
    d.text(X(dr) - 2, 3.5 + 128, "drift starts", 7.2, "end", fill=MUT)
    d.text(X(t) + 2, 3.5 + 128, "check", 7.2, fill=MUT)
    d.line([(X(0), 138), (X(5800) + 6, 138)], INK, 0.7)
    for s, lab in ((0, "last alarm"), (dr, "d"), (t, "t")):
        d.line([(X(s), 135), (X(s), 141)], INK, 0.7, head=False)
        d.text(X(s), 149, lab, 7.4, "middle", style="italic" if len(lab) == 1 else "normal", fill=MUT)
    d.text(X(5800) + 2, 148, "time", 7.4, "end", fill=MUT)
    d.save("reference")


# ---------------------------------------------------------------- Figure 3.4
def history_null():
    d = Drawing(212)
    hx0, hx1, cw = 14, 316, 44
    # history and the current window
    d.text(hx0, 11, "history since the last alarm (at most the newest 5,000 samples)", 7.6, fill=MUT)
    d.rect(hx0, 16, hx1 - hx0, 14, PROC, RULE, sw=0.6)
    d.rect(hx1, 16, cw, 14, CUR, None)
    d.text(hx1 + cw / 2, 26, Wsub("cur", 8.4, "white"), 8.4, "middle", fill="white")
    # earlier windows: 200 samples, one start every 10 samples
    for k in range(6):
        d.rect(hx0 + 4.5 * k, 35 + 5 * k, cw, 3.6, "#7F8B98", None)
        d.rect(hx1 - cw - 4.5 * (5 - k), 35 + 5 * k, cw, 3.6, "#7F8B98", None)
    d.text((hx0 + hx1) / 2, 52, "· · ·", 9, "middle", fill=MUT)
    d.line([(hx1, 14), (hx1, 70)], INK, 0.6, "2,1.6", head=False)
    d.text(hx1 - 3, 72, "all end before " + Wsub("cur", 7.4), 7.4, "end", fill=MUT)
    d.text(hx0, 75, "earlier 200-sample windows, one starting every 10 samples", 7.4, fill=MUT)
    # the two C2STs share the reference
    by, bh = 96, 34
    d.rect(hx0, by, 150, bh, "white", INK, r=3, sw=0.8)
    d.text(hx0 + 75, by + 13, "each earlier window vs " + Wsub("ref", 8.2), 8.2, "middle", weight="bold")
    d.text(hx0 + 75, by + 25, "same 5-fold C2ST: a null AUC", 7.6, "middle", fill=MUT)
    d.rect(258, by, 146, bh, "white", INK, r=3, sw=0.8)
    d.text(331, by + 13, Wsub("cur", 8.2) + " vs " + Wsub("ref", 8.2), 8.2, "middle", weight="bold")
    d.text(331, by + 25, "5-fold C2ST: the observed AUC", 7.6, "middle", fill=MUT)
    d.rect(186, by + 7, 50, 20, REF, None, r=2)
    d.text(211, by + 20.5, Wsub("ref", 8.4, "white"), 8.4, "middle", fill="white")
    d.line([(186, by + 17), (hx0 + 151, by + 17)], REF)
    d.line([(236, by + 17), (257, by + 17)], REF)
    d.text(211, by - 4, "reservoir", 7.2, "middle", fill=REF)
    d.line([(hx0 + 60, 79), (hx0 + 60, by)], MUT)
    d.line([(hx1 + cw / 2, 30), (hx1 + cw / 2, by)], CUR)
    # null distribution and p-value
    base, hx = 196, 120
    hs = [4, 10, 19, 28, 33, 29, 21, 13, 7, 3, 1]
    for k, h in enumerate(hs):
        d.rect(hx + k * 9, base - h, 8, h, NULLC, None)
    d.line([(hx - 6, base), (hx + 120, base)], MUT, 0.6, head=False)
    d.line([(hx + 112, base), (hx + 112, base - 38)], CUR, 1.6, head=False)
    d.text(hx + 48, base + 10, "null AUCs (at most 199, random order)", 7.4, "middle", fill=MUT)
    d.text(hx + 116, base - 30, "observed", 7.4, fill=CUR)
    d.line([(hx0 + 75, by + bh), (hx0 + 75, 182), (hx - 4, 182)], MUT)
    d.line([(331, by + bh), (331, 146), (hx + 112, 146), (hx + 112, base - 39)], CUR)
    d.rect(276, 162, 128, 40, PROC, None, r=3)
    d.text(340, 176, '<tspan font-style="italic">p</tspan> = (<tspan font-style="italic">c</tspan> + 1) / '
                     '(<tspan font-style="italic">B</tspan> + 1)', 9, "middle")
    d.text(340, 187, '<tspan font-style="italic">c</tspan>: null AUCs ≥ observed', 7.4, "middle", fill=MUT)
    d.text(340, 197, '<tspan font-style="italic">B</tspan>: draws; ASPT can stop early', 7.4, "middle", fill=MUT)
    d.save("history_null")


# ---------------------------------------------------------------- Figure 1.1
def roadmap():
    d = Drawing(196)
    cols = [(1, 128, "Problem of a sliding C2ST (D3)"), (146, 128, "Component of EADD"),
            (292, 66, "Hypothesis"), (378, 40, "Sections")]
    for x, w, h in cols:
        d.text(x, 10, h, 8.4, weight="bold")
    d.line([(1, 15), (W, 15)], INK, 0.6, head=False)
    rows = [(["the sliding reference moves", "with slow drift"], "Reservoir reference", "since the last alarm", "H1", "slow drift", "4.3, 5.1"),
            (["fixed AUC threshold: false", "alarms on autocorrelated data"], "History-null permutation test", "earlier windows as the null", "H2", "false alarms", "4.4, 5.2"),
            (["a full permutation test", "costs many model fits"], "ASPT", "stops when the result is clear", "H3", "cost", "4.5, 5.3"),
            (["no information on which", "features drifted"], "TreeSHAP ranking", "at every alarm", "H4", "attribution", "4.6, 5.4")]
    for i, (prob, comp, sub, h, what, sec) in enumerate(rows):
        y = 23 + i * 43
        d.rect(1, y, 128, 34, "white", RULE, r=3)
        d.lines(7, y + 14, prob, 7.8)
        d.rect(146, y, 128, 34, PROC, None, r=3)
        d.text(152, y + 14, comp, 8.2, weight="bold")
        d.text(152, y + 25, sub, 7.6, fill=MUT)
        bw = d.badge(292, y + 11.5, h)
        d.text(292 + bw + 4, y + 20, what, 8, fill=INK)
        d.text(378, y + 20, sec, 7.8, fill=MUT)
        d.line([(129, y + 17), (145.5, y + 17)], MUT)
        d.line([(274, y + 17), (290.5, y + 17)], MUT)
        if i < 3:
            d.line([(1, y + 38.5), (W, y + 38.5)], "#DDE1E6", 0.5, head=False)
    d.save("roadmap")


# ---------------------------------------------------------------- Figure 3.5
def timeline():
    d = Drawing(92)
    cw, g = 74.4, 11
    stages = [("Initial runs", ["earlier EADD on 13", "real streams"], "seeds 42 to 442"),
              ("Benchmark", ["12 detectors; flaws", "fixed; exploratory"], "seeds 42 to 442"),
              ("Confirmatory", ["revised H1 to H4,", "registered"], "seeds 1000 to 1009"),
              ("Final test", ["same schedule for all,", "registered"], "seeds 3000 to 3009"),
              ("Secondary", ["newer detectors and", "three checks"], "subsets of 3000 to 3009")]
    notes = ["four flaws found", "H1 revised to slow drift", "H2, H3a re-specified"]
    xs = [1 + i * (cw + g) + cw / 2 for i in range(5)]
    ly = 66
    d.line([(xs[0], ly), (xs[-1], ly)], RULE, 1.2, head=False)
    for i, ((t, rows, seeds), x) in enumerate(zip(stages, xs)):
        final = i == 3
        d.rect(x - cw / 2, 2, cw, 46, "white" if final else PROC, INK if final else None, r=3, sw=1.0)
        d.text(x - cw / 2 + 6, 15, t, 8.6, weight="bold")
        d.lines(x - cw / 2 + 6, 27, rows, 7.3, fill=MUT)
        d.line([(x, 48), (x, ly)], RULE, 0.6, head=False)
        d.circle(x, ly, 4.2 if final else 3.2, INK if final else "white", INK, 1.0)
        d.text(x, ly + 15, seeds, 7.3, "middle", style="italic", fill=MUT)
    for i, n in enumerate(notes):
        d.text((xs[i] + xs[i + 1]) / 2, ly - 4, n, 7, "middle", style="italic", fill=ALM)
    d.save("timeline")


if __name__ == "__main__":
    for f in (overview, pipeline, reference, history_null, roadmap, timeline):
        f()
