# -*- coding: utf-8 -*-
"""Gera os diagramas da série "Glossário de Risco" (um termo por post).

Mesmo sistema visual da série Eixo Torto, com acento verde-lima. Todos os
diagramas usam dado sintético/didático e são renderizados em 2x (dpi=200).

Uso: python3 make_charts.py <dir_fontes> <dir_saida>
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch

BG = "#0E0F12"
INK = "#F4F1EA"
MUTED = "#9BA1AB"
FAINT = "#3A3F47"
GRID = "#22262C"
DIM = "#2A2F36"
ACCENT = "#BEF264"  # verde-lima da série

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
    return px * 0.72


def fig_axes(w, h, **kw):
    return plt.subplots(figsize=(w / 100, h / 100), dpi=200, **kw)


def strip(ax, keep_bottom=True, keep_left=False, grid_y=False):
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_visible(keep_left)
    ax.spines["bottom"].set_visible(keep_bottom)
    ax.tick_params(length=0, labelsize=pt(22))
    if grid_y:
        ax.grid(axis="y", color=GRID, linewidth=1.2)
        ax.set_axisbelow(True)


def fmt_br(v, dec=2):
    return f"{v:.{dec}f}".replace(".", ",")


def save(fig, name):
    fig.savefig(OUT / name, dpi=200)
    plt.close(fig)
    print("ok", name)


# ---------------------------------------------------------------- PD
# Matriz de ícones 10x10: probabilidade mostrada do jeito honesto.
def pd_chart():
    fig, ax = fig_axes(936, 470)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.97, bottom=0.05)
    ax.set_xlim(0, 20.5)
    ax.set_ylim(-0.6, 10.2)
    ax.axis("off")
    ax.set_aspect("equal")

    lit = {(4, 2), (7, 6)}  # 2 em 100
    for i in range(10):
        for j in range(10):
            cor = ACCENT if (i, j) in lit else DIM
            ax.add_patch(FancyBboxPatch(
                (i * 0.92, j * 0.92), 0.72, 0.72,
                boxstyle="round,pad=0,rounding_size=0.12",
                fc=cor, ec="none"))
    ax.text(10.6, 6.4, "PD = 2%", fontsize=pt(52), family=AB, color=INK)
    ax.text(10.6, 4.55, "2 em cada 100 clientes\nparecidos com esse",
            fontsize=pt(26), family=SGM, color=MUTED, linespacing=1.3)
    ax.text(10.6, 2.6, "no horizonte de 12 meses",
            fontsize=pt(22), family=SGM, color=ACCENT)
    save(fig, "verbete_pd.png")


# ---------------------------------------------------------------- LGD
# Barra única de exposição: o que volta e o que não volta.
def lgd_chart():
    fig, ax = fig_axes(936, 400)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.86, bottom=0.10)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 10)
    ax.axis("off")

    y0, hh = 4.6, 2.6
    ax.add_patch(FancyBboxPatch((0, y0), 55, hh,
                                boxstyle="round,pad=0,rounding_size=0.35",
                                fc=FAINT, ec="none"))
    ax.add_patch(FancyBboxPatch((55.8, y0), 44.2, hh,
                                boxstyle="round,pad=0,rounding_size=0.35",
                                fc=ACCENT, ec="none"))
    ax.text(0, y0 + hh + 0.9, "exposição no default (EAD): R$ 100",
            fontsize=pt(24), family=SGB, color=INK)
    ax.text(27.5, y0 + hh / 2, "volta: R$ 55", ha="center", va="center",
            fontsize=pt(26), family=SGB, color=INK)
    ax.text(77.9, y0 + hh / 2, "não volta: R$ 45", ha="center", va="center",
            fontsize=pt(26), family=SGB, color=BG)
    ax.text(77.9, y0 - 1.75, "LGD = 45%", ha="center",
            fontsize=pt(40), family=AB, color=ACCENT)
    ax.text(0, y0 - 1.75, "recuperações + garantias,\nlíquidas do custo e do tempo",
            fontsize=pt(21), family=SGM, color=MUTED, va="top", linespacing=1.3)
    save(fig, "verbete_lgd.png")


# ---------------------------------------------------------------- KS
# Distância máxima entre as acumuladas de bons e maus.
def ks_chart():
    from math import erf, sqrt

    def cdf(x, mu, sd):
        return 0.5 * (1 + erf((x - mu) / (sd * sqrt(2))))

    s = np.linspace(300, 900, 400)
    maus = np.array([cdf(v, 500, 130) for v in s])
    bons = np.array([cdf(v, 620, 130) for v in s])
    gap = maus - bons
    i = int(np.argmax(gap))
    ks = gap[i]

    fig, ax = fig_axes(936, 520)
    fig.subplots_adjust(left=0.04, right=0.96, top=0.90, bottom=0.15)
    ax.plot(s, maus * 100, color=ACCENT, lw=4.5, solid_capstyle="round", zorder=3)
    ax.plot(s, bons * 100, color=INK, lw=4.5, solid_capstyle="round", zorder=3)
    ax.vlines(s[i], bons[i] * 100, maus[i] * 100, color=ACCENT, lw=3,
              linestyle=(0, (4, 3)), zorder=2)

    strip(ax, grid_y=True)
    ax.set_yticks([])
    ax.set_xticks([350, 600, 850])
    ax.set_xticklabels(["score baixo", "ponto de maior separação", "score alto"],
                       fontsize=pt(21))
    ax.set_ylim(0, 108)

    ax.text(322, 60, f"KS = {round(ks*100)} p.p.",
            fontsize=pt(34), family=AB, color=ACCENT)
    ax.text(322, 88, "% acumulado de maus", fontsize=pt(23), family=SGB,
            color=ACCENT)
    ax.text(322, 76, "% acumulado de bons", fontsize=pt(23), family=SGB,
            color=INK)
    save(fig, "verbete_ks.png")


# ---------------------------------------------------------------- PSI
# Distribuição do score: desenvolvimento vs. hoje.
def psi_chart():
    def pdf(x, mu, sd):
        return np.exp(-0.5 * ((x - mu) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))

    s = np.linspace(250, 950, 500)
    dev = pdf(s, 615, 88)
    hoje = pdf(s, 565, 94)

    # PSI em 10 faixas de mesmo passo, com as densidades integradas por faixa
    edges = np.linspace(250, 950, 11)
    def bin_p(mu, sd):
        from math import erf, sqrt
        c = lambda x: 0.5 * (1 + erf((x - mu) / (sd * sqrt(2))))
        p = np.diff([c(e) for e in edges])
        return p / p.sum()
    p_dev, p_hoje = bin_p(615, 88), bin_p(565, 94)
    psi = float(np.sum((p_hoje - p_dev) * np.log(p_hoje / p_dev)))

    fig, ax = fig_axes(936, 500)
    fig.subplots_adjust(left=0.03, right=0.97, top=0.88, bottom=0.16)
    ax.fill_between(s, hoje * 100, color=ACCENT, alpha=0.28, zorder=2)
    ax.plot(s, hoje * 100, color=ACCENT, lw=4, solid_capstyle="round", zorder=3)
    ax.plot(s, dev * 100, color=INK, lw=3.2, linestyle=(0, (5, 4)), zorder=3)

    strip(ax)
    ax.set_yticks([])
    ax.set_xticks([350, 600, 850])
    ax.set_xticklabels(["score baixo", "", "score alto"], fontsize=pt(21))
    ax.set_ylim(0, 0.62)

    ax.text(0.03, 0.90, "no desenvolvimento", transform=ax.transAxes,
            fontsize=pt(23), family=SGB, color=INK)
    ax.text(0.03, 0.79, "a carteira hoje", transform=ax.transAxes,
            fontsize=pt(23), family=SGB, color=ACCENT)
    ax.text(0.97, 0.90, f"PSI = {fmt_br(psi)}", transform=ax.transAxes,
            ha="right", fontsize=pt(34), family=AB, color=ACCENT)
    ax.text(0.97, 0.79, "› 0,25: investigar", transform=ax.transAxes,
            ha="right", fontsize=pt(22), family=SGM, color=MUTED)
    ax.text(0.5, -0.145, "referência usual: ‹ 0,10 estável · 0,10–0,25 atenção · › 0,25 alerta",
            transform=ax.transAxes, ha="center", fontsize=pt(20), color=MUTED)
    save(fig, "verbete_psi.png")


# ---------------------------------------------------------------- SAFRA
# Curvas vintage: % com problema por meses desde a originação.
def safra_chart():
    m = np.arange(0, 19)

    def curva(nivel, k=0.22):
        return nivel * (1 - np.exp(-k * m))

    fig, ax = fig_axes(936, 540)
    fig.subplots_adjust(left=0.05, right=0.86, top=0.93, bottom=0.14)

    for nivel, cor, lw in [(4.4, FAINT, 3.2), (3.8, FAINT, 3.2), (4.9, MUTED, 3.2)]:
        ax.plot(m, curva(nivel), color=cor, lw=lw, solid_capstyle="round", zorder=2)

    m_j = np.arange(0, 11)
    ruim = 8.6 * (1 - np.exp(-0.22 * m_j))
    ax.plot(m_j, ruim, color=ACCENT, lw=5, solid_capstyle="round", zorder=4)
    ax.annotate("a safra nova, ainda jovem,\njá acima de todo mundo",
                (m_j[-1], ruim[-1]), xytext=(-10, 26),
                textcoords="offset points", ha="right", va="bottom",
                fontsize=pt(23), family=SGB, color=ACCENT, linespacing=1.25)

    strip(ax, grid_y=True)
    ax.set_yticks([2, 4, 6, 8])
    ax.set_yticklabels(["2%", "4%", "6%", "8%"], fontsize=pt(21))
    ax.set_xticks([0, 6, 12, 18])
    ax.set_xticklabels(["originação", "6 meses", "12 meses", "18 meses"],
                       fontsize=pt(21))
    ax.set_ylim(0, 9.6)
    ax.set_xlim(-0.4, 18.6)
    ax.text(18.5, curva(4.9)[-1] - 0.02, "safras\nanteriores", fontsize=pt(21),
            family=SGM, color=MUTED, va="center", ha="left", linespacing=1.25)
    save(fig, "verbete_safra.png")


# ---------------------------------------------------------------- marca
# O sinal de definição "≔" da série: dois pontos + duas barras.
def marca(nome, tamanho, escala):
    fig = plt.figure(figsize=(tamanho / 100, tamanho / 100), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    ax.patch.set_alpha(0)
    fig.patch.set_alpha(0)
    lw = 14 * escala
    ax.plot([16, 16], [63, 35], color=ACCENT, lw=0, marker="o",
            markersize=lw * 1.5, markerfacecolor=ACCENT, markeredgewidth=0)
    ax.plot([40, 88], [63, 63], color=ACCENT, lw=lw, solid_capstyle="round")
    ax.plot([40, 88], [35, 35], color=ACCENT, lw=lw, solid_capstyle="round")
    fig.savefig(OUT / nome, dpi=200, transparent=True)
    plt.close(fig)
    print("ok", nome)


if __name__ == "__main__":
    pd_chart()
    lgd_chart()
    ks_chart()
    psi_chart()
    safra_chart()
    marca("marca_glossario.png", 60, 0.62)
    marca("marca_glossario_hero.png", 340, 1.0)
