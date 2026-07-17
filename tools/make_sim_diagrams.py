"""
Regenerate the simulator diagrams (assets/sim_architecture.png and
assets/sim_ibm_flow.png) so their contents can be kept in sync with the
simulator code instead of living only inside a PNG.

Facts encoded here are audited against the simulator repo:
  - 6 node-error modes  (nodes.NodeMode: local, device-averaged twin,
    layout-aware twin, Aer device model, equations, IBM live)
  - 7 built-in link channels (quantum_network.BUILTIN_CHANNEL_IDS —
    photon loss is an input to the fiber-attenuation channel, not a
    separate channel)
  - collector fields (data_collector.harvest_backend_properties)

Usage:  python3 tools/make_sim_diagrams.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ASSETS = Path(__file__).resolve().parent.parent / "assets"

BG      = "#111527"
PANEL   = "#171c30"
TEXT    = "#eef1f8"
MUTED   = "#9aa5bd"
PURPLE  = "#a78bfa"
TEAL    = "#5eead4"
PINK    = "#e377c2"
BLUE    = "#60a5fa"
ORANGE  = "#fbbf24"
GREEN   = "#4ade80"

TITLE_LH = 0.0235   # axis-fraction line height per title point-size unit
BODY_LH  = 0.0195


def _box(ax, x, y, w, h, edge, title, body="", ts=13, bs=10,
         title_color=None):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.006,rounding_size=0.012",
        facecolor=PANEL, edgecolor=edge, linewidth=1.8))
    n_t = title.count("\n") + 1
    ty = y + h - 0.016
    ax.text(x + w / 2, ty, title, ha="center", va="top", fontsize=ts,
            fontweight="bold", color=title_color or TEXT, linespacing=1.25)
    if body:
        by = ty - n_t * TITLE_LH * (ts / 13.0) - 0.010
        ax.text(x + w / 2, by, body, ha="center", va="top", fontsize=bs,
                color=MUTED, linespacing=1.4)


def _group(ax, x, y, w, h, edge, label, sublabel):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.006,rounding_size=0.014",
        facecolor="none", edgecolor=edge, linewidth=1.6,
        linestyle=(0, (5, 3))))
    ax.text(x + 0.018, y + h - 0.022, label, fontsize=14.5,
            fontweight="bold", color=edge, va="top")
    ax.text(x + 0.018, y + h - 0.052, sublabel, fontsize=11, color=MUTED,
            style="italic", va="top")


def _arrow(ax, x0, y0, x1, y1, color, rad=0.12):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=2.2,
                                shrinkA=2, shrinkB=2,
                                connectionstyle=f"arc3,rad={rad}"))


def architecture():
    fig, ax = plt.subplots(figsize=(11.6, 9.2), dpi=150)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(.5, .985, "Quantum Network Simulator — Architecture",
            ha="center", va="top", fontsize=22, fontweight="bold", color=TEXT)
    ax.text(.5, .948, "Nodes are modelled on real superconducting processors"
                      "  ·  links model the photonic channel between them",
            ha="center", va="top", fontsize=12.5, color=MUTED)

    # ---- NODE group ------------------------------------------------------
    _group(ax, .02, .445, .46, .455, PURPLE,
           "NODE — a quantum processor (QPU)",
           "6 interchangeable sources of a node's error rates")
    modes = [
        ("Local", "fixed textbook rates\non Qiskit's Aer", PURPLE),
        ("Digital twin\n(device-averaged)",
         "fitted from a real QPU's\ncalibration history", TEAL),
        ("Digital twin\n(layout-aware)",
         "only the qubits a job\nactually runs on", PINK),
        ("Aer device model", "Aer's own per-qubit\nNoiseModel.from_backend",
         BLUE),
        ("Equations", "derived from device\nphysics — no data", GREEN),
        ("IBM live", "runs on the real\nQPU via the cloud", PURPLE),
    ]
    bw, bh = .202, .112
    for i, (t, b, c) in enumerate(modes):
        col, row = i % 2, i // 2
        _box(ax, .038 + col * .215, .698 - row * .125, bw, bh, c, t, b,
             ts=11, bs=8.8)

    # ---- LINK group --------------------------------------------------------
    _group(ax, .52, .445, .46, .455, TEAL,
           "LINK — the photonic channel between nodes",
           "7 built-in error channels, each a function of distance")
    _box(ax, .538, .698, .205, .112, TEAL, "Optical fiber",
         "standard telecom fiber,\n1550 nm light, losing\n0.2 dB per km",
         ts=12, bs=9)
    _box(ax, .758, .698, .205, .112, TEAL, "Free space",
         "wireless / satellite path\nwith atmospheric\nturbulence",
         ts=12, bs=9)
    _box(ax, .538, .465, .425, .21, TEAL, "Link error channels (7)",
         "fiber attenuation (absorbs photon loss\n+ detector inefficiency)"
         " · polarization drift\nphase noise · timing jitter\nchromatic"
         " dispersion · detector dark counts\nenvironmental decoherence",
         ts=12.5, bs=9.5)

    # ---- Protocols ----------------------------------------------------------
    _box(ax, .225, .30, .55, .105, BLUE,
         "Protocols — what runs over the network",
         "entanglement distribution · teleportation · BB84 QKD\ndata"
         " transmission (the experiment shown below) · distance sweeps",
         ts=13, bs=9.8)
    _arrow(ax, .25, .445, .36, .405, PURPLE)
    _arrow(ax, .75, .445, .64, .405, TEAL)

    # ---- Data / generation ----------------------------------------------------
    _box(ax, .05, .135, .41, .115, ORANGE,
         "Data collection (SQLite database)",
         "calibration snapshots · fitted twin models\nhardware experiments"
         " · full run history", ts=12.5, bs=9.5)
    _box(ax, .54, .135, .41, .115, GREEN, "Generation",
         "synthesize new nodes from hardware parameters\nand new channels"
         " from fitted equations", ts=12.5, bs=9.5)
    _arrow(ax, .42, .30, .30, .25, ORANGE)
    _arrow(ax, .58, .30, .70, .25, GREEN)
    _arrow(ax, .463, .19, .537, .19, ORANGE, rad=0)

    # ---- Glossary -----------------------------------------------------------
    ax.plot([.03, .97], [.112, .112], color="#2a3150", lw=1)
    ax.text(.03, .102, "GLOSSARY", fontsize=10, fontweight="bold",
            color=MUTED, va="top")
    gloss = [
        ("QPU", "quantum processing unit: the quantum chip",
         "Aer", "Qiskit's local circuit simulator"),
        ("T1 / T2", "how long a qubit keeps its energy / its phase",
         "BB84", "the standard quantum key-distribution (QKD) protocol"),
        ("1550 nm", "the standard low-loss telecom wavelength",
         "0.2 dB/km", "fiber signal loss: ~4.5% of photons lost per km"),
    ]
    for i, (k1, v1, k2, v2) in enumerate(gloss):
        y = .062 - i * .027
        ax.text(.03, y, k1, fontsize=9.5, fontweight="bold", color=TEXT)
        ax.text(.115, y, "— " + v1, fontsize=9.5, color=MUTED)
        ax.text(.52, y, k2, fontsize=9.5, fontweight="bold", color=TEXT)
        ax.text(.605, y, "— " + v2, fontsize=9.5, color=MUTED)

    fig.savefig(ASSETS / "sim_architecture.png", facecolor=BG,
                bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)


def ibm_flow():
    fig, ax = plt.subplots(figsize=(11.2, 8.2), dpi=150)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(.5, .98, "Real IBM Hardware Integration — Data Flow",
            ha="center", va="top", fontsize=22, fontweight="bold", color=TEXT)
    ax.text(.5, .938, "What is collected from real superconducting QPUs, "
                      "and how it drives the simulator",
            ha="center", va="top", fontsize=12.5, color=MUTED)

    _box(ax, .28, .775, .44, .115, PURPLE, "IBM Quantum backends",
         "ibm_fez · ibm_kingston · ibm_marrakesh\nHeron-class"
         " superconducting QPUs", ts=14, bs=10.5)
    _arrow(ax, .5, .775, .5, .715, BLUE, rad=0)
    ax.text(.515, .748, "properties()", fontsize=10.5, color=BLUE,
            style="italic")

    _box(ax, .21, .55, .58, .16, BLUE,
         "Background collector — free, metadata only",
         "reads device properties every 6 h (no quota used):\nT1 · T2 ·"
         " per-gate errors & durations · asymmetric readout pair\nper-edge"
         " 2-qubit errors · faulty qubits · IBM calibration timestamps",
         ts=13.5, bs=9.8)
    _arrow(ax, .5, .55, .5, .49, ORANGE, rad=0)

    _box(ax, .28, .365, .44, .12, ORANGE, "SQLite data store",
         "calibration snapshots (per-qubit + averages)\npersisted across"
         " restarts", ts=13.5, bs=10)

    _arrow(ax, .37, .365, .25, .30, TEAL)
    ax.text(.13, .345, "fit twin models", fontsize=10.5, color=TEAL,
            style="italic")
    _arrow(ax, .73, .832, .80, .30, PURPLE, rad=-0.25)
    ax.text(.845, .56, "live circuits", fontsize=10.5, color=PURPLE,
            style="italic", rotation=270)
    ax.text(.5, .325, "two ways the calibration data drives the nodes",
            ha="center", fontsize=11, color=MUTED, style="italic")

    _box(ax, .03, .115, .45, .175, TEAL,
         "USE 1 · Digital-twin nodes (offline)",
         "full calibration history → device-averaged twin\nlayout-aware"
         " twin: only the qubits a job runs on,\nwith the per-qubit"
         " asymmetric readout pair\nruns on local Aer · costs no quota",
         ts=12.5, bs=9.5)
    _box(ax, .52, .115, .455, .175, PURPLE,
         "USE 2 · Real-time live node (IBM-live)",
         "transpile + submit circuits via Qiskit Runtime\nasync job IDs"
         " polled until counts return\nquota-guarded: 10 min/month tracker"
         " checks every\njob before submission · billed time recorded",
         ts=12.5, bs=9.5)

    _box(ax, .17, .005, .66, .082, GREEN, "Quantum network simulator",
         "node modes: local · device-avg twin · layout twin · Aer model"
         " · equations · live   +   photonic links", ts=13, bs=9.3)
    _arrow(ax, .27, .115, .38, .09, TEAL)
    _arrow(ax, .73, .115, .62, .09, PURPLE)

    fig.savefig(ASSETS / "sim_ibm_flow.png", facecolor=BG,
                bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)


if __name__ == "__main__":
    architecture()
    ibm_flow()
    print(f"wrote {ASSETS/'sim_architecture.png'} and {ASSETS/'sim_ibm_flow.png'}")
