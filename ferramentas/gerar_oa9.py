"""OA9 - Lab Assíncrono (LusaTech): Landing Page da "App" e botão de voltar nas outras páginas."""
import os
import shutil
from PIL import Image, ImageDraw
from skodji_dashboard import *

LAB = os.path.join(AQUI, "..", "OA9 - Publicar no Power BI Service", "oa-09", "lab-assincrono")
OUT = os.path.join(LAB, "dashboard")
os.makedirs(OUT, exist_ok=True)

# Navegador de páginas: X 64, Y 352, 1152 x 64, 4 botões com 16 px de espaçamento
NAV_X, NAV_Y, NAV_W, NAV_H, GAP = 64, 352, 1152, 64, 16
BOTOES = [("Faturação", "KPIs, métrica dinâmica e cores por variação homóloga"),
          ("Matriz", "Ano anterior, variação homóloga e % do total"),
          ("Produtos", "Ranking, alertas visuais e Word Cloud"),
          ("Simulação", "Cenários de crescimento de 0% a 20%")]
KPIS = [("FATURAÇÃO TOTAL", "16.050 €"), ("MARGEM DE LUCRO", "9.645 €"),
        ("PRODUTOS", "5"), ("PERÍODO", "Jan 2025 - Mai 2026")]


def logo_lusatech():
    """Recorta o logótipo do formador (fundo branco) e torna o branco transparente."""
    im = Image.open(os.path.join(LAB, "LusaTeck.png")).convert("RGBA")
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, _ = px[x, y]
            if min(r, g, b) > 235:
                px[x, y] = (255, 255, 255, 0)
    im = im.crop(im.getbbox())
    im.save(os.path.join(OUT, "logo-lusatech.png"), optimize=True)
    return im


def fundo_landing():
    im = Image.new("RGB", s(W, H), FUNDO)
    d = ImageDraw.Draw(im)
    # faixa "hero"
    d.rectangle(s(0, 0, W, 300), fill=AZUL)
    d.polygon([tuple(s(900, 0)), tuple(s(W, 0)), tuple(s(W, 300)), tuple(s(820, 300))], fill=AZUL_ESC)
    d.polygon([tuple(s(1010, 0)), tuple(s(W, 0)), tuple(s(W, 300)), tuple(s(930, 300))], fill=CIANO)
    # cartão branco para o logótipo (o logótipo é inserido como imagem no Power BI)
    d.rounded_rectangle(s(40, 32, 300, 152), radius=int(12 * K), fill=BRANCO)
    text(d, 40, 186, "Relatório de Vendas LusaTech", f("SemiBold", 34), BRANCO)
    text(d, 42, 240, "Faturação, margens, ranking de produtos e simulação de cenários  ·  2025-2026",
         f("Regular", 14), "#D6E6F7")
    ic = Image.open(os.path.join(AQUI, "icone.png")).convert("RGBA")
    h = int(150 * K)
    ic = ic.resize((int(ic.width * h / ic.height), h), Image.LANCZOS)
    im.paste(ic, (int(1080 * K), int(70 * K)), ic)
    # painel do navegador
    d.rounded_rectangle(s(40, 300 + 24 - 6, W - 40, 486), radius=int(12 * K), fill=BRANCO)
    text(d, 64, 330 - 6, "Escolha uma página", f("SemiBold", 13), TXT)
    bw = (NAV_W - GAP * 3) / 4
    for i, (_, desc) in enumerate(BOTOES):
        x = NAV_X + i * (bw + GAP)
        text(d, x + bw / 2, NAV_Y + NAV_H + 22, desc, f("Regular", 10), TXT2, "ma")
    # cartões de resumo
    cw = (W - 80 - 3 * 16) / 4
    for i, (lab, _) in enumerate(KPIS):
        x = 40 + i * (cw + 16)
        d.rounded_rectangle(s(x, 510, x + cw, 610), radius=int(10 * K), fill=BRANCO)
        d.rounded_rectangle(s(x, 510, x + 6, 610), radius=int(3 * K), fill=AZUL if i % 2 == 0 else CIANO)
        text(d, x + 22, 526, lab, f("Medium", 10), TXT2)
    # rodapé com a marca Skodji
    lg = Image.open(os.path.join(AQUI, "logo_skodji.png")).convert("RGBA")
    h = int(40 * K)
    lg = lg.resize((int(lg.width * h / lg.height), h), Image.LANCZOS)
    d.rounded_rectangle(s(W - 40 - 190, 640, W - 40, 696), radius=int(10 * K), fill=CIANO)
    im.paste(lg, (int((W - 40 - 95) * K - lg.width / 2), int(648 * K)), lg)
    text(d, 40, 656, "Skodji Digital  ·  Upskilling BI & Cloud  ·  OA9 Lab Assíncrono - A \"App\" LusaTech",
         f("Regular", 11), TXT2, "lm")
    text(d, 40, 680, "Edmilson Landim  ·  Novembro 2026  ·  Navegação: Ctrl + clique no Power BI Desktop, clique simples no Service",
         f("Regular", 10), TXT3, "lm")
    return im


def mockup_landing(logo):
    im = fundo_landing()
    d = ImageDraw.Draw(im)
    lg = logo.copy()
    h = int(104 * K)
    lg = lg.resize((int(lg.width * h / lg.height), h), Image.LANCZOS)
    im.paste(lg, (int(170 * K - lg.width / 2), int(40 * K)), lg)
    bw = (NAV_W - GAP * 3) / 4
    for i, (nome, _) in enumerate(BOTOES):
        x = NAV_X + i * (bw + GAP)
        d.rounded_rectangle(s(x, NAV_Y, x + bw, NAV_Y + NAV_H), radius=int(10 * K), fill=AZUL)
        text(d, x + bw / 2, NAV_Y + NAV_H / 2, nome, f("SemiBold", 16), BRANCO, "mm")
    cw = (W - 80 - 3 * 16) / 4
    for i, (_, val) in enumerate(KPIS):
        x = 40 + i * (cw + 16)
        text(d, x + 22, 552, val, f("SemiBold", 26 if i < 3 else 19), AZUL)
    return im


def mockup_voltar():
    """Cabeçalho de uma página interna com o botão Voltar (X 880, Y 18, 90 x 36)."""
    im = fundo("LusaTech - Faturação", "Skodji Digital  ·  Upskilling BI & Cloud  ·  OA8 Lab Assíncrono - Parâmetros e Formatação Avançada",
               [], {}, "")
    im = im.crop(s(0, 0, W, 120))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(s(880, 18, 970, 54), radius=int(8 * K), fill=BRANCO)
    d.polygon([tuple(s(*p)) for p in ((896, 36), (906, 28), (906, 33), (914, 33), (914, 39), (906, 39), (906, 44))], fill=AZUL)
    text(d, 920, 36, "Início", f("SemiBold", 12), AZUL, "lm")
    d.rectangle(s(0, 72, W, 120), fill=FUNDO)
    text(d, 24, 96, "Botão Voltar: X 880 · Y 18 · 90 x 36 · Ação Voltar (ou Navegação de página -> Landing Page)",
         f("Regular", 11), TXT2, "lm")
    return im


logo = logo_lusatech()
fundo_landing().save(os.path.join(OUT, "fundo-landing.png"), optimize=True)
mockup_landing(logo).save(os.path.join(OUT, "mockup-landing.png"), optimize=True)
mockup_voltar().save(os.path.join(OUT, "mockup-botao-voltar.png"), optimize=True)
shutil.copy(os.path.join(AQUI, "..", "OA6 - DAX e indicadores", "oa-06", "lab-assincrono", "dashboard", "tema-skodji.json"),
            os.path.join(OUT, "tema-skodji.json"))
print("ok")
