# -*- coding: utf-8 -*-
"""O layout A (full-bleed) do verbete SAFRA em seis paletas de cores.

Reusa a geometria de make_alt_safra; muda apenas os papéis de cor:
fundo, tinta, apagado, grade, eixo, safras antigas e acento (safra-problema).

Uso: python3 make_a_palettes.py <dir_fontes> <dir_pptx> <dir_preview>
"""
from PIL import Image, ImageDraw, ImageFont

import make_alt_safra as base
from make_alt_safra import BYLINE, DEF, KICKER, NOME, PEG, CTA, H, W

PALETAS = [
    dict(nome="Cobalto", bg="0B1220", ink="EEF2F7", muted="8FA0B8",
         grid="172440", axis="384A6B", old="52678F", acc="4D9FFF"),
    dict(nome="Jornal", bg="F5F1E8", ink="191A1E", muted="837C6E",
         grid="E1DACA", axis="C4BAA5", old="B7AF9E", acc="E0442E"),
    dict(nome="Terminal", bg="070A08", ink="E6F2E8", muted="7E9B8C",
         grid="14231B", axis="2C4636", old="3E5A4C", acc="3DF08C"),
    dict(nome="Âmbar", bg="151009", ink="F6EFE2", muted="A8987B",
         grid="271F12", axis="463A22", old="6E604A", acc="FFB300"),
    dict(nome="Ultravioleta", bg="120F1E", ink="F1EEF8", muted="9D93BC",
         grid="1F1836", axis="372C55", old="55496F", acc="B57BFF"),
    dict(nome="Gelo", bg="EDF1F5", ink="10151B", muted="6E7B88",
         grid="D6DEE6", axis="BCC7D2", old="A6B1BC", acc="0F62FE"),
]


def layout_a(r, P):
    box = (-30, 120, 1140, 540)
    for gy in (200, 360, 520):
        r.rect(-2, gy, W + 4, 2, P["grid"])
    end = base.curvas(r, box, old_color=P["old"], bad_color=P["acc"])
    r.rect(-2, 660, W + 4, 2, P["axis"])
    r.text(KICKER, 84, 84, 912, 26, "Space Grotesk", P["acc"], bold=True)
    r.text("7,6% aos 10 meses", end[0] + 22, end[1] - 40, 380, 26,
           "Space Grotesk", P["acc"], bold=True)
    r.text("a safra nova", end[0] + 22, end[1] - 6, 380, 22,
           "Space Grotesk", P["muted"])
    r.text("safras anteriores", 848, 344, 200, 22, "Space Grotesk", P["muted"])
    r.text("originação", 84, 676, 300, 22, "Space Grotesk", P["muted"])
    r.text("18 meses", W - 84 - 300, 676, 300, 22, "Space Grotesk",
           P["muted"], align="r")

    y = r.text("SAFRA", 84, 740, 912, 118, "Archivo Black", P["ink"], ls=1.0)
    y = r.text(NOME, 84, y + 10, 912, 28, "Space Grotesk", P["muted"])
    y = r.text(DEF, 84, y + 18, 912, 29, "Space Grotesk", P["ink"], ls=1.28)
    y = r.text(PEG, 84, y + 18, 912, 29, "Space Grotesk", P["acc"], bold=True,
               ls=1.25)
    r.text(CTA, 84, y + 16, 912, 24, "Space Grotesk", P["muted"], bold=True)
    base.rodape(r, P["acc"], P["muted"])


def folha_de_contato(nomes):
    cw, ch, pad, cap = 360, 450, 24, 56
    cols, rows = 3, 2
    sheet = Image.new("RGB", (cols * cw + (cols + 1) * pad,
                              rows * (ch + cap) + (rows + 1) * pad),
                      (23, 25, 29))
    d = ImageDraw.Draw(sheet)
    font = ImageFont.truetype(str(base.TTF[("Space Grotesk", True)]), 22)
    for i, (nome, arq) in enumerate(nomes):
        cx = pad + (i % cols) * (cw + pad)
        cy = pad + (i // cols) * (ch + cap + pad)
        img = Image.open(base.OUT_PNG / f"{arq}.png").resize(
            (cw, ch), Image.LANCZOS)
        sheet.paste(img, (cx, cy))
        d.text((cx, cy + ch + 14), nome, font=font, fill=(244, 241, 234))
    out = base.OUT_PNG / "_folha_de_contato.png"
    sheet.save(out)
    print("ok _folha_de_contato")


if __name__ == "__main__":
    itens = []
    for P in PALETAS:
        slug = (P["nome"].lower().replace("â", "a").replace("é", "e")
                .replace(" ", "_"))
        arq = f"safra_a_{slug}"
        for r in (base.Pptx(P["bg"]), base.Png(P["bg"])):
            layout_a(r, P)
            r.save(arq)
        itens.append((f"{P['nome']}  ·  #{P['acc']}", arq))
        print("ok", arq)
    folha_de_contato(itens)
