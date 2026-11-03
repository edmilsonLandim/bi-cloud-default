"""OA7 - Lab Assíncrono (LusaTech): página Produtos (ranking, formatação condicional, Word Cloud)
e página de descrição Tooltip_Produto."""
import os
import shutil
from PIL import Image, ImageDraw
from skodji_dashboard import *

OUT = os.path.join(AQUI, "..", "OA7 - Tooltips e formatação condicional", "oa-07", "lab-assincrono", "dashboard")
EUR = lambda v: num(v) + " €"
T = 16050

# (ID Produto, Total Faturação, Ranking, Variação Homóloga % sem filtro de ano)
PRODUTOS = [("P001", 3275, 1, 20.18), ("P005", 3250, 2, 30.00), ("P002", 3240, 3, 35.00),
            ("P004", 3150, 4, 22.81), ("P003", 3135, 5, 38.41)]
CORES_PROD = {"P001": "#1E55A2", "P002": "#32B2E7", "P003": "#F5B800", "P004": "#0E3A75", "P005": "#8FD3F2"}
# Tooltip de exemplo: coluna 2025 T1 da página Faturação
T1_2025 = [("P001", 650), ("P002", 600), ("P003", 480), ("P004", 585), ("P005", 250)]

kpis = [("TOTAL FATURAÇÃO", EUR(T), AZUL), ("PRODUTO Nº 1", "P001", CIANO),
        ("FATURAÇÃO DO Nº 1", EUR(3275), AZUL), ("Nº DE PRODUTOS", "5", CIANO)]
titulos = {"esq": "Ranking de Produtos - Faturação e Variação Homóloga",
           "dir_cima": "Word Cloud - Faturação por Produto",
           "dir_baixo": "Descrição Tooltip_Produto (ex.: 2025 T1)"}
args = ("LusaTech - Produtos", "Skodji Digital  ·  Upskilling BI & Cloud  ·  OA7 Lab Assíncrono - Tooltips, Ranking e Formatação Condicional",
        kpis, titulos, "Fonte: Vendas[ID Produto] e _Medidas (Total Faturação, Ranking Vendas, Variação Homóloga %)  ·  Edmilson Landim  ·  Novembro 2026")


def mistura(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(a, b))


def seta(d, x, y, cima):
    """Seta de 12x14 com o centro em (x, y)."""
    if cima:
        pts = [(x, y - 7), (x + 6, y - 1), (x + 2, y - 1), (x + 2, y + 7), (x - 2, y + 7), (x - 2, y - 1), (x - 6, y - 1)]
    else:
        pts = [(x, y + 7), (x + 6, y + 1), (x + 2, y + 1), (x + 2, y - 7), (x - 2, y - 7), (x - 2, y + 1), (x - 6, y + 1)]
    d.polygon([tuple(s(*p)) for p in pts], fill=VERDE if cima else VERMELHO)


def tabela(d):
    x, y, w, h = PAINEIS["esq"]
    tx, ty, alt = x + 20, y + 58, 46
    cab = ["ID Produto", "Total Faturação", "Ranking Vendas", "Variação Homóloga %"]
    larg = [150, 210, 160, 216]
    d.rectangle(s(tx, ty, x + w - 20, ty + 32), fill=AZUL)
    cx = tx
    for i, (c, lw) in enumerate(zip(cab, larg)):
        if i == 0:
            text(d, cx + 10, ty + 16, c, f("SemiBold", 11), BRANCO, "lm")
        else:
            text(d, cx + lw - 10, ty + 16, c, f("SemiBold", 11), BRANCO, "rm")
        cx += lw
    vmin, vmax = min(p[1] for p in PRODUTOS), max(p[1] for p in PRODUTOS)
    yy = ty + 32
    for pid, v, rk, yoy in PRODUTOS + [("Total", T, None, 28.86)]:
        total = pid == "Total"
        if total:
            d.rectangle(s(tx, yy, x + w - 20, yy + alt), fill="#DCE6F4")
        else:
            # gradiente: menor valor branco, maior valor azul
            cor = mistura("#FFFFFF", "#5B9BD5", (v - vmin) / (vmax - vmin))
            d.rectangle(s(tx + larg[0], yy, tx + larg[0] + larg[1], yy + alt), fill=cor)
        fonte = f("SemiBold" if total else "Regular", 12)
        cx = tx
        text(d, cx + 10, yy + alt / 2, pid, fonte, TXT, "lm")
        cx += larg[0]
        text(d, cx + larg[1] - 10, yy + alt / 2, EUR(v), fonte, TXT, "rm")
        cx += larg[1]
        text(d, cx + larg[2] - 10, yy + alt / 2, "" if rk is None else str(rk), f("SemiBold", 12), AZUL, "rm")
        cx += larg[2]
        text(d, cx + larg[3] - 34, yy + alt / 2, num(yoy, 2) + "%", fonte, TXT, "rm")
        seta(d, cx + larg[3] - 18, yy + alt / 2, yoy >= 0)
        d.line(s(tx, yy + alt, x + w - 20, yy + alt), fill=LINHA, width=int(K))
        yy += alt
    leg = f("Regular", 10)
    ly = yy + 30
    for i in range(40):
        d.rectangle(s(tx + i * 2, ly - 6, tx + i * 2 + 2, ly + 6), fill=mistura("#FFFFFF", "#5B9BD5", i / 39))
    d.rectangle(s(tx, ly - 6, tx + 80, ly + 6), outline="#C9D2DE", width=int(K))
    text(d, tx + 90, ly, "Cor do fundo: gradiente branco (menor) -> azul (maior)", leg, TXT2, "lm")
    seta(d, tx + 6, ly + 26, True)
    text(d, tx + 18, ly + 26, ">= 0", leg, TXT2, "lm")
    seta(d, tx + 60, ly + 26, False)
    text(d, tx + 72, ly + 26, "< 0   Ícones à direita (regras com tipo Número)", leg, TXT2, "lm")
    text(d, tx, ly + 52, "Sem filtro de ano, a Variação Homóloga % compara o total (2025 + 2026) com 2025:",
         leg, TXT3, "lm")
    text(d, tx, ly + 68, "por isso todos os produtos ficam a verde. Com Ano = 2026 ficam todos a vermelho.",
         leg, TXT3, "lm")


def word_cloud(d):
    x, y, w, h = PAINEIS["dir_cima"]
    vmin, vmax = min(p[1] for p in PRODUTOS), max(p[1] for p in PRODUTOS)
    pos = {"P001": (x + 220, y + 130), "P005": (x + 110, y + 92), "P002": (x + 330, y + 92),
           "P004": (x + 115, y + 172), "P003": (x + 330, y + 172)}
    for pid, v, _, _ in PRODUTOS:
        tam = 22 + 16 * (v - vmin) / (vmax - vmin)
        text(d, *pos[pid], pid, f("SemiBold", tam), CORES_PROD[pid], "mm")


def pizza(d, caixa, fatias, legenda_tam=9):
    """Gráfico circular com a legenda em cima à esquerda."""
    x, y, w, h = caixa
    lx = x + 6
    for pid, _ in fatias:
        d.ellipse(s(lx, y + 5, lx + 8, y + 13), fill=CORES_PROD[pid])
        text(d, lx + 11, y + 9, pid, f("Regular", legenda_tam), TXT, "lm")
        lx += 46
    cx, cy = x + w / 2, y + 22 + (h - 22) / 2
    r = (h - 34) / 2
    tot, ini = sum(v for _, v in fatias), -90
    import math
    for pid, v in fatias:
        fim = ini + 360 * v / tot
        d.pieslice(s(cx - r, cy - r, cx + r, cy + r), ini, fim, fill=CORES_PROD[pid], outline=BRANCO, width=int(K))
        meio = math.radians((ini + fim) / 2)
        ex, ey = cx + (r + 8) * math.cos(meio), cy + (r + 8) * math.sin(meio)
        text(d, ex, ey, f"{num(v)} €", f("Regular", legenda_tam - 1), TXT2, "lm" if math.cos(meio) >= 0 else "rm")
        ini = fim


def tooltip_preview(d):
    x, y, w, h = PAINEIS["dir_baixo"]
    bx, by, bw, bh = x + 45, y + 54, 350, 196
    d.rounded_rectangle(s(bx + 3, by + 3, bx + bw + 3, by + bh + 3), radius=int(6 * K), fill="#D5DBE5")
    d.rounded_rectangle(s(bx, by, bx + bw, by + bh), radius=int(6 * K), fill=BRANCO, outline="#C9D2DE", width=int(K))
    pizza(d, (bx + 6, by + 4, bw - 12, bh - 8), T1_2025)


def desenhar(d):
    tabela(d)
    word_cloud(d)
    tooltip_preview(d)


pagina(OUT, "produtos", args, kpis, desenhar, cores_valor={1: CIANO, 3: CIANO})

# Página de descrição Tooltip_Produto: 350 x 240 px (largura pedida no enunciado; altura por defeito)
im = Image.new("RGB", s(350, 240), BRANCO)
pizza(ImageDraw.Draw(im), (8, 6, 334, 228), T1_2025, legenda_tam=10)
im.save(os.path.join(OUT, "mockup-tooltip-produto.png"), optimize=True)

shutil.copy(os.path.join(AQUI, "..", "OA6 - DAX e indicadores", "oa-06", "lab-assincrono", "dashboard", "tema-skodji.json"),
            os.path.join(OUT, "tema-skodji.json"))
print("ok")
