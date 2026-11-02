"""Fundos e mockups de dashboards Power BI com a identidade Skodji Digital.

Tela lógica 1280x720 (Power BI 16:9), exportada a 1920x1080 (K = 1.5).
Logótipos: icone.png (favicon do skodjidigital.cv) e logo_skodji.png (extraído de
OA1 - Introdução ao BI/oa-01/lab-assincrono/dashboard/logo.svg), na mesma pasta.
"""
import os
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "Fonts")

K, W, H = 1.5, 1280, 720
AZUL, CIANO, AZUL_ESC = "#1E55A2", "#32B2E7", "#163F7A"
AMARELO, NAVY, VERMELHO, VERDE = "#F5B800", "#0E3A75", "#DF3131", "#2E9E5B"
FUNDO, BRANCO = "#ECEFF4", "#FFFFFF"
TXT, TXT2, TXT3, LINHA = "#212121", "#646464", "#8F8F8F", "#E3E8F0"
KPI_Y, KPI_H, KPI_W = 88, 88, 296
PAINEIS = {"esq": (24, 192, 776, 504), "dir_cima": (816, 192, 440, 220), "dir_baixo": (816, 428, 440, 268)}


def f(peso, tam):
    return ImageFont.truetype(os.path.join(FONTS, f"Poppins-{peso}.ttf"), int(tam * K))


def s(*v):
    return [int(round(x * K)) for x in v]


def text(d, x, y, t, font, fill=TXT, anchor="la"):
    d.text(s(x, y), t, font=font, fill=fill, anchor=anchor)


def num(v, casas=0):
    t = f"{v:,.{casas}f}"
    return t.replace(",", " ").replace(".", ",").replace(" ", ".")


def kpi_x(i):
    return 24 + i * (KPI_W + 16)


def fundo(titulo, subtitulo, kpis, titulos, rodape):
    im = Image.new("RGB", s(W, H), FUNDO)
    d = ImageDraw.Draw(im)
    d.rectangle(s(0, 0, W, 72), fill=AZUL)
    d.polygon([tuple(s(1000, 0)), tuple(s(W, 0)), tuple(s(W, 72)), tuple(s(980, 72))], fill=AZUL_ESC)
    d.polygon([tuple(s(1060, 0)), tuple(s(W, 0)), tuple(s(W, 72)), tuple(s(1040, 72))], fill=CIANO)
    for nome, alt, pos in (("logo_skodji.png", 46, None), ("icone.png", 52, (20, 10))):
        lg = Image.open(os.path.join(AQUI, nome)).convert("RGBA")
        h = int(alt * K)
        lg = lg.resize((int(lg.width * h / lg.height), h), Image.LANCZOS)
        xy = tuple(s(*pos)) if pos else (int((W - 22) * K) - lg.width, int(13 * K))
        im.paste(lg, xy, lg)
    text(d, 84, 8, titulo, f("SemiBold", 22), BRANCO)
    text(d, 85, 44, subtitulo, f("Regular", 11), "#D6E6F7")
    for i, (lab, _, cor) in enumerate(kpis):
        x = kpi_x(i)
        d.rounded_rectangle(s(x, KPI_Y, x + KPI_W, KPI_Y + KPI_H), radius=int(10 * K), fill=BRANCO)
        d.rounded_rectangle(s(x, KPI_Y, x + 6, KPI_Y + KPI_H), radius=int(3 * K), fill=cor)
        text(d, x + 20, KPI_Y + 12, lab, f("Medium", 10), TXT2)
    for chave, t in titulos.items():
        x, y, w, h = PAINEIS[chave]
        d.rounded_rectangle(s(x, y, x + w, y + h), radius=int(10 * K), fill=BRANCO)
        text(d, x + 20, y + 12, t, f("SemiBold", 14), TXT)
        d.rectangle(s(x + 20, y + 38, x + 60, y + 41), fill=CIANO)
    rod = f("Regular", 9)
    text(d, 24, 711, rodape, rod, TXT3, "lm")
    text(d, W - 24, 711, "skodjidigital.cv", rod, TXT3, "rm")
    return im


def valores_kpi(d, kpis, cores_valor=None):
    for i, (_, val, _) in enumerate(kpis):
        cor = (cores_valor or {}).get(i, AZUL)
        text(d, kpi_x(i) + 20, KPI_Y + 30, val, f("SemiBold", 32), cor)


def anel(d, painel, fatias, centro, fmt):
    x, y, w, h = painel
    cx, cy, ro, ri = x + 110, y + 128, 64, 41
    total, ini = sum(v for _, v, _ in fatias), -90
    for _, v, cor in fatias:
        fim = ini + 360 * v / total
        d.pieslice(s(cx - ro, cy - ro, cx + ro, cy + ro), ini, fim, fill=cor)
        ini = fim
    d.ellipse(s(cx - ri, cy - ri, cx + ri, cy + ri), fill=BRANCO)
    text(d, cx, cy, centro, f("SemiBold", 15), TXT, "mm")
    esp = 40 if len(fatias) <= 2 else 32
    y0 = y + 128 - esp * (len(fatias) - 1) / 2
    for j, (lab, v, cor) in enumerate(fatias):
        ly = y0 + j * esp
        d.rounded_rectangle(s(x + 210, ly - 6, x + 222, ly + 6), radius=int(2 * K), fill=cor)
        text(d, x + 230, ly, lab, f("Regular", 12), TXT, "lm")
        text(d, x + 420, ly, fmt(v), f("SemiBold", 11), TXT, "rm")


def colunas_duplas(d, painel, cats, serie_a, serie_b, cores, nomes, fmt):
    x, y, w, h = painel
    esq, dir_, topo, base = x + 24, x + w - 20, y + 84, y + h - 30
    vmax = max(max(serie_a), max(serie_b))
    passo = (dir_ - esq) / len(cats)
    bw = passo * 0.32
    d.line(s(esq, base, dir_, base), fill="#C9D2DE", width=int(K))
    for i, c in enumerate(cats):
        cx = esq + passo * (i + 0.5)
        for j, (v, cor) in enumerate(((serie_a[i], cores[0]), (serie_b[i], cores[1]))):
            bx = cx - bw + j * bw
            bh = (base - topo) * v / vmax
            d.rounded_rectangle(s(bx + 1, base - bh, bx + bw - 1, base), radius=int(2 * K), fill=cor)
            text(d, bx + bw / 2, base - bh - 3, fmt(v), f("SemiBold", 8), TXT, "md")
        text(d, cx, base + 6, c, f("Regular", 10), TXT2, "ma")
    lx = x + w - 20
    for nome, cor in reversed(list(zip(nomes, cores))):
        tw = d.textlength(nome, font=f("Regular", 10)) / K
        lx -= tw
        text(d, lx, y + 62, nome, f("Regular", 10), TXT, "lm")
        d.rounded_rectangle(s(lx - 14, y + 57, lx - 5, y + 67), radius=int(2 * K), fill=cor)
        lx -= 28


def matriz(d, painel, cabecalho, linhas, larguras, alt=24):
    """linhas: [(nivel, [valores...], {col: cor}, negrito)] - nivel 0 = ano, 1 = mês, 2 = total."""
    x, y, w, h = painel
    tx, ty = x + 20, y + 58
    d.rectangle(s(tx, ty, x + w - 20, ty + alt + 4), fill=AZUL)
    cx = tx
    for i, (c, lw) in enumerate(zip(cabecalho, larguras)):
        if i == 0:
            text(d, cx + 8, ty + (alt + 4) / 2, c, f("SemiBold", 10), BRANCO, "lm")
        else:
            text(d, cx + lw - 8, ty + (alt + 4) / 2, c, f("SemiBold", 10), BRANCO, "rm")
        cx += lw
    yy = ty + alt + 4
    for nivel, vals, cores, negrito in linhas:
        if nivel == 0:
            d.rectangle(s(tx, yy, x + w - 20, yy + alt), fill="#EAF2FB")
        elif nivel == 2:
            d.rectangle(s(tx, yy, x + w - 20, yy + alt), fill="#DCE6F4")
        cx = tx
        fonte = f("SemiBold" if negrito else "Regular", 10)
        for i, (v, lw) in enumerate(zip(vals, larguras)):
            cor = cores.get(i, TXT)
            if i == 0:
                text(d, cx + 8 + (18 if nivel == 1 else 0), yy + alt / 2, v, fonte, cor, "lm")
            else:
                text(d, cx + lw - 8, yy + alt / 2, v, fonte, cor, "rm")
            cx += lw
        d.line(s(tx, yy + alt, x + w - 20, yy + alt), fill=LINHA, width=int(K))
        yy += alt


def pagina(pasta, sufixo, args, kpis, desenhar, cores_valor=None):
    os.makedirs(pasta, exist_ok=True)
    fundo(*args).save(os.path.join(pasta, f"fundo-{sufixo}.png"), optimize=True)
    im = fundo(*args)
    d = ImageDraw.Draw(im)
    valores_kpi(d, kpis, cores_valor)
    desenhar(d)
    im.save(os.path.join(pasta, f"mockup-{sufixo}.png"), optimize=True)
