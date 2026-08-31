# -*- coding: utf-8 -*-
"""Gera os gráficos da série "Eixo Torto" (posts de imagem única).

Todos os gráficos são renderizados em 2x (dpi=200 sobre layout lógico de 1080px)
para ficarem nítidos no feed. Paleta e tipografia da série:

  fundo   #0E0F12   tinta #F4F1EA   cinza #9BA1AB   acento #FF4D00

Uso: python3 make_charts.py <dir_fontes> <dir_saida>
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.patches import Circle, FancyArrowPatch

BG = "#0E0F12"
INK = "#F4F1EA"
MUTED = "#9BA1AB"
FAINT = "#3A3F47"
GRID = "#22262C"
ACCENT = "#FF4D00"

FONT_DIR = Path(sys.argv[1] if len(sys.argv) > 1 else "fonts")
OUT = Path(sys.argv[2] if len(sys.argv) > 2 else "charts")
OUT.mkdir(parents=True, exist_ok=True)

for ttf in ["ArchivoBlack-Regular.ttf", "SpaceGrotesk-Regular.ttf",
            "SpaceGrotesk-Medium.ttf", "SpaceGrotesk-Bold.ttf"]:
    font_manager.fontManager.addfont(str(FONT_DIR / ttf))

SG = "Space Grotesk"
SGM = "Space Grotesk Medium"
SGB = "Space Grotesk Bold"
AB = "Archivo Black"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "font.family": SGM, "text.color": INK,
    "axes.edgecolor": FAINT, "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.linewidth": 1.6,
})


def pt(px):
    """Converte px lógicos (layout 1080) em pontos para dpi=200 (render 2x)."""
    return px * 0.72


def fig_axes(w, h, nrows=1, ncols=1, **kw):
    fig, axs = plt.subplots(nrows, ncols, figsize=(w / 100, h / 100), dpi=200, **kw)
    return fig, axs


def strip(ax, keep_bottom=True, keep_left=False, grid_y=False):
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_visible(keep_left)
    ax.spines["bottom"].set_visible(keep_bottom)
    ax.tick_params(length=0, labelsize=pt(22))
    if grid_y:
        ax.grid(axis="y", color=GRID, linewidth=1.2)
        ax.set_axisbelow(True)


def chip(ax, x, y, text, color, size=21):
    ax.text(x, y, text, transform=ax.transAxes, ha="left", va="center",
            fontsize=pt(size), family=SGB, color=color,
            bbox=dict(boxstyle="round,pad=0.55", fc="none", ec=color, lw=2))


def save(fig, name):
    fig.savefig(OUT / name, dpi=200)
    plt.close(fig)
    print("ok", name)


def fmt_br(v, dec=1):
    s = f"{v:,.{dec}f}".replace(",", "@").replace(".", ",").replace("@", ".")
    return s


# ---------------------------------------------------------------- crime 01
# Eixo cortado: os mesmos dois números, com o eixo começando em 97 e em 0.
def crime01():
    anos = ["2023", "2024"]
    vals = [97.2, 98.1]
    fig, (a, b) = fig_axes(936, 600, 1, 2)
    fig.subplots_adjust(left=0.015, right=0.985, top=0.80, bottom=0.17, wspace=0.22)

    for ax, ylim, color, tag, tagc in [
        (a, (97.0, 98.35), ACCENT, "COMO TE MOSTRAM", ACCENT),
        (b, (0.0, 110.0), INK, "O QUE ACONTECEU", MUTED),
    ]:
        bars = ax.bar(anos, vals, width=0.58, color=color, zorder=3)
        ax.set_ylim(*ylim)
        ax.set_xlim(-0.7, 1.7)
        strip(ax, grid_y=True)
        ax.set_yticks([])
        ax.tick_params(labelsize=pt(24))
        chip(ax, 0.0, 1.16, tag, tagc)
        for r, v in zip(bars, vals):
            ax.annotate(fmt_br(v), (r.get_x() + r.get_width() / 2, r.get_height()),
                        xytext=(0, 8), textcoords="offset points", ha="center",
                        fontsize=pt(26), family=SGB, color=INK, zorder=4)
    a.annotate("eixo começa em 97", (0.5, -0.24), xycoords="axes fraction",
               ha="center", fontsize=pt(20), color=ACCENT, family=SGM)
    b.annotate("eixo começa em 0", (0.5, -0.24), xycoords="axes fraction",
               ha="center", fontsize=pt(20), color=MUTED, family=SGM)
    save(fig, "crime01_eixo_cortado.png")


# ---------------------------------------------------------------- crime 02
# Dois eixos y independentes fazem duas séries quaisquer "coincidirem".
def crime02():
    meses = ["jan", "fev", "mar", "abr", "mai", "jun",
             "jul", "ago", "set", "out", "nov", "dez"]
    cafe = np.array([3.1, 3.4, 3.2, 3.8, 4.1, 3.9, 4.4, 4.6, 4.3, 4.8, 5.1, 4.9])
    rng = np.random.default_rng(4)
    bugs = cafe * 17 + rng.normal(0, 1.2, 12)

    fig, ax = fig_axes(936, 620)
    fig.subplots_adjust(left=0.09, right=0.91, top=0.82, bottom=0.12)
    ax2 = ax.twinx()

    ax.plot(meses, cafe, color=ACCENT, lw=4.5, solid_capstyle="round", zorder=3)
    ax2.plot(meses, bugs, color=INK, lw=4.5, solid_capstyle="round", zorder=3)
    ax.set_ylim(2.4, 5.6)
    ax2.set_ylim(2.4 * 17, 5.6 * 17)

    strip(ax, grid_y=True)
    for side in ["top", "left", "bottom"]:
        ax2.spines[side].set_visible(False)
    ax2.spines["right"].set_visible(True)
    ax2.tick_params(length=0, labelsize=pt(22), colors=MUTED)
    ax.spines["left"].set_visible(True)
    ax.spines["left"].set_color(ACCENT)
    ax2.spines["right"].set_color(FAINT)
    ax.tick_params(axis="y", colors=ACCENT)
    ax.yaxis.set_major_formatter(lambda v, _: fmt_br(v))

    ax.text(0.0, 1.13, "café na firma (xícaras/dia)", transform=ax.transAxes,
            fontsize=pt(24), family=SGB, color=ACCENT)
    ax.text(1.0, 1.13, "bugs em produção", transform=ax.transAxes, ha="right",
            fontsize=pt(24), family=SGB, color=INK)
    ax.text(0.985, 0.06, "r = 0,98*", transform=ax.transAxes, ha="right",
            fontsize=pt(30), family=AB, color=INK)
    ax.text(0.985, -0.16, "*correlação não é causa — e escala escolhida a dedo não é correlação",
            transform=ax.transAxes, ha="right", fontsize=pt(18), color=MUTED)
    save(fig, "crime02_dois_eixos.png")


# ---------------------------------------------------------------- crime 03
# Bolhas escaladas pelo raio: o valor dobra, a área quadruplica.
def crime03():
    fig, (a, b) = fig_axes(936, 600, 1, 2)
    fig.subplots_adjust(left=0.015, right=0.985, top=0.80, bottom=0.10, wspace=0.22)

    a.set_xlim(0, 10)
    a.set_ylim(0, 10)
    a.set_aspect("equal")
    a.axis("off")
    r1 = 1.35
    small = Circle((2.4, 4.6), r1, color=MUTED)
    big = Circle((6.6, 4.6), r1 * 2, color=ACCENT)
    a.add_patch(small)
    a.add_patch(big)
    a.text(2.4, 4.6, "10", ha="center", va="center", fontsize=pt(30), family=AB, color=BG)
    a.text(6.6, 4.6, "20", ha="center", va="center", fontsize=pt(42), family=AB, color=BG)
    a.text(6.6, 1.15, "2× o valor, 4× a área", ha="center",
           fontsize=pt(20), color=ACCENT, family=SGM)
    chip(a, 0.0, 1.16, "COMO DESENHAM", ACCENT)

    bars = b.bar([0, 1], [10, 20], width=0.58, color=[MUTED, INK], zorder=3)
    b.set_ylim(0, 24)
    b.set_xlim(-0.7, 1.7)
    strip(b, grid_y=True)
    b.set_yticks([])
    b.set_xticks([])
    for r, v in zip(bars, [10, 20]):
        b.annotate(str(v), (r.get_x() + r.get_width() / 2, r.get_height()),
                   xytext=(0, 8), textcoords="offset points", ha="center",
                   fontsize=pt(26), family=SGB, color=INK, zorder=4)
    chip(b, 0.0, 1.16, "A PROPORÇÃO REAL", MUTED)
    save(fig, "crime03_raio_area.png")


# ---------------------------------------------------------------- crime 04
# Janela conveniente: a mesma série rende -40% ou +18%, depende do corte.
def crime04():
    rng = np.random.default_rng(11)
    n = 36
    base = np.linspace(100, 51, n - 3)
    base += rng.normal(0, 2.2, n - 3) * np.linspace(1, 0.6, n - 3)
    base[0] = 100.0
    serie = np.concatenate([base, [53.5, 57.0, 60.0]])
    x = np.arange(n)

    fig, ax = fig_axes(936, 640)
    fig.subplots_adjust(left=0.04, right=0.96, top=0.86, bottom=0.14)
    ax.plot(x, serie, color=INK, lw=4, solid_capstyle="round", zorder=3)
    ax.plot(x[-4:], serie[-4:], color=ACCENT, lw=5, solid_capstyle="round", zorder=4)
    ax.axvspan(x[-4], x[-1] + 0.4, color=ACCENT, alpha=0.08, zorder=1)

    strip(ax, grid_y=True)
    ax.set_yticks([])
    ax.set_xticks([0, 12, 24, 35])
    ax.set_xticklabels(["há 3 anos", "há 2 anos", "há 1 ano", "hoje"], fontsize=pt(21))
    for lbl, ha in zip(ax.get_xticklabels(), ["left", "center", "center", "right"]):
        lbl.set_ha(ha)
    ax.set_xlim(-0.5, n + 0.2)
    ax.set_ylim(38, 116)

    ax.annotate("o recorte da\napresentação: +18%", (x[-2], 56.2),
                (0.78, 0.035), textcoords="axes fraction",
                fontsize=pt(24), family=SGB, color=ACCENT, ha="right", va="bottom",
                arrowprops=dict(arrowstyle="-", color=ACCENT, lw=1.6,
                                shrinkA=10, shrinkB=8))
    ax.text(0.015, 0.955, "a série completa: −40%", transform=ax.transAxes,
            fontsize=pt(24), family=SGB, color=INK)
    save(fig, "crime04_janela.png")


# ---------------------------------------------------------------- crime 05
# Acumulado sempre sobe: o total cresce até com o mês despencando.
def crime05():
    n = 24
    x = np.arange(1, n + 1)
    subida = np.linspace(600, 4800, 8)
    descida = 4800 * np.exp(-0.28 * np.arange(1, n - 7))
    novos = np.concatenate([subida, descida])
    acum = np.cumsum(novos)

    fig, (a, b) = fig_axes(936, 680, 2, 1, sharex=True,
                           gridspec_kw=dict(height_ratios=[1.5, 1.0]))
    fig.subplots_adjust(left=0.02, right=0.98, top=0.87, bottom=0.09, hspace=0.58)

    a.plot(x, acum / 1000, color=ACCENT, lw=4.5, solid_capstyle="round", zorder=3)
    a.fill_between(x, acum / 1000, color=ACCENT, alpha=0.12, zorder=2)
    strip(a, grid_y=True)
    a.set_yticks([])
    a.set_ylim(0, 46)
    chip(a, 0.0, 1.22, "O SLIDE: USUÁRIOS ACUMULADOS", ACCENT)
    a.annotate("sempre subindo", (n - 0.4, acum[-1] / 1000), xytext=(-8, -26),
               textcoords="offset points", ha="right",
               fontsize=pt(21), family=SGM, color=ACCENT)

    b.bar(x, novos / 1000, width=0.7, color=INK, zorder=3)
    strip(b, grid_y=True)
    b.set_yticks([])
    b.set_ylim(0, 5.4)
    chip(b, 0.0, 1.30, "A REALIDADE: NOVOS USUÁRIOS POR MÊS", MUTED)
    b.set_xticks([1, 8, 16, 24])
    b.set_xticklabels(["mês 1", "mês 8", "mês 16", "mês 24"], fontsize=pt(21))
    save(fig, "crime05_acumulado.png")


# ---------------------------------------------------------------- marca
# O "eixo torto": um eixo cartesiano com o braço horizontal entortado.
def marca(nome, tamanho, lw, cor=ACCENT):
    fig = plt.figure(figsize=(tamanho / 100, tamanho / 100), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    ax.patch.set_alpha(0)
    fig.patch.set_alpha(0)
    pts_v = [(16, 92), (16, 16)]
    pts_h = [(16, 16), (58, 16), (88, 40)]
    for pts in [pts_v, pts_h]:
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=cor, lw=lw, solid_capstyle="round",
                solid_joinstyle="round")
    fig.savefig(OUT / nome, dpi=200, transparent=True)
    plt.close(fig)
    print("ok", nome)


if __name__ == "__main__":
    crime01()
    crime02()
    crime03()
    crime04()
    crime05()
    marca("marca_eixo_torto.png", 60, 9)
    marca("marca_eixo_torto_hero.png", 340, 16)
