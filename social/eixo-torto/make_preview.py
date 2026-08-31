# -*- coding: utf-8 -*-
"""Prévia local dos posts (mesma geometria do make_pptx), para conferência
visual antes do import no Canva.

Uso: python3 make_preview.py <dir_fontes> <dir_charts> <dir_saida>
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import make_pptx as mk
from make_pptx import ACCENT, BG, COL, H, INK, MARGIN, MUTED, POSTS, W, n_lines

FONT_DIR = Path(sys.argv[1])
CHARTS = Path(sys.argv[2])
OUT = Path(sys.argv[3])
OUT.mkdir(parents=True, exist_ok=True)

F = {
    ("Archivo Black", False): FONT_DIR / "ArchivoBlack-Regular.ttf",
    ("Space Grotesk", False): FONT_DIR / "SpaceGrotesk-Regular.ttf",
    ("Space Grotesk", True): FONT_DIR / "SpaceGrotesk-Bold.ttf",
}


def hexc(h):
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def wrap(text, font, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if font.getlength(trial) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def text(img, d, t, x, y, w, size, fam, color, bold=False, ls=1.0):
    font = ImageFont.truetype(str(F[(fam, bold)]), size)
    for ln in wrap(t, font, w):
        d.text((x, y), ln, font=font, fill=hexc(color))
        y += int(size * ls)
    return y


def image(img, path, x, y, w):
    pic = Image.open(path).convert("RGBA")
    r = w / pic.width
    pic = pic.resize((w, int(pic.height * r)), Image.LANCZOS)
    img.alpha_composite(pic, (int(x), int(y)))
    return y + pic.height


def build(post):
    img = Image.new("RGBA", (W, H), hexc(BG) + (255,))
    d = ImageDraw.Draw(img)
    text(img, d, post["kicker"], MARGIN, MARGIN, COL, 26, "Space Grotesk",
         ACCENT, bold=True)
    y = text(img, d, post["h1"], MARGIN, MARGIN + 52, COL, post["h1_size"],
             "Archivo Black", INK, ls=1.04)
    y += 34
    if post.get("hero"):
        image(img, CHARTS / "marca_eixo_torto_hero.png", W - MARGIN - 330, y + 40, 330)
        text(img, d, post["body"], MARGIN, y + 70, 540, 36, "Space Grotesk",
             INK, ls=1.25)
        text(img, d, post["cta"], MARGIN, H - MARGIN - 44 - 150, COL, 32,
             "Space Grotesk", ACCENT, bold=True, ls=1.2)
    else:
        y = image(img, CHARTS / post["chart"], (W - 936) / 2, y + 6, 936)
        y = text(img, d, post["caption"], MARGIN, y + 30, COL, 31,
                 "Space Grotesk", INK, ls=1.25)
        text(img, d, post["cta"], MARGIN, y + 26, COL, 29, "Space Grotesk",
             ACCENT, bold=True, ls=1.2)
    fy = H - MARGIN - 44
    image(img, CHARTS / "marca_eixo_torto.png", MARGIN, fy + 2, 40)
    text(img, d, "Richard Guilherme · ciência de dados & risco de crédito",
         MARGIN + 58, fy + 8, COL - 58, 24, "Space Grotesk", MUTED)
    name = post["arquivo"].replace(".pptx", ".png")
    img.convert("RGB").save(OUT / name)
    print("ok", name)


if __name__ == "__main__":
    for p in POSTS:
        build(p)
