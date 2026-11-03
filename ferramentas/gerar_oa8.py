"""OA8 - Lab Assíncrono (LusaTech): página Faturação (parâmetro de campo + cores por Variação
Homóloga) e página Simulação (parâmetro numérico What-if)."""
import os
import shutil
from skodji_dashboard import *

OUT = os.path.join(AQUI, "..", "OA8 - Formatação condicional avançada e parâmetros", "oa-08", "lab-assincrono", "dashboard")
EUR = lambda v: num(v) + " €"
EUR2 = lambda v: num(v, 2) + " €"
MESES = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
FAT = [905, 625, 1035, 1335, 1380, 845, 780, 1320, 855, 870, 955, 1550, 1040, 585, 865, 730, 375]
ROTULOS = MESES + MESES[:5]
TRIM = [("T1", 2565, None), ("T2", 3560, None), ("T3", 2955, None), ("T4", 3375, None),
        ("T1", 2490, -2.92), ("T2", 1105, -68.96)]
TAXA = 0.10
RODAPE = "Edmilson Landim  ·  Novembro 2026"
SUB = "Skodji Digital  ·  Upskilling BI & Cloud  ·  OA8 Lab Assíncrono - Parâmetros e Formatação Avançada"


def eixo_anos(d, x0, passo, base):
    """Rótulos dos meses e dos anos (2025: 12 meses, 2026: 5) por baixo do eixo."""
    for i, m in enumerate(ROTULOS):
        text(d, x0 + passo * (i + 0.5), base + 6, m, f("Regular", 9), TXT2, "ma")
    for ano, ini, n in (("2025", 0, 12), ("2026", 12, 5)):
        text(d, x0 + passo * (ini + n / 2), base + 24, ano, f("SemiBold", 11), TXT, "ma")
    d.line(s(x0 + passo * 12, base + 2, x0 + passo * 12, base + 38), fill="#C9D2DE", width=int(K))


def linha(d, painel, valores, cor, fmt):
    x, y, w, h = painel
    esq, dir_, topo, base = x + 24, x + w - 16, y + 70, y + h - 46
    passo = (dir_ - esq) / len(valores)
    vmax = max(valores) * 1.1
    pts = [(esq + passo * (i + 0.5), base - (base - topo) * v / vmax) for i, v in enumerate(valores)]
    d.line(s(esq, base, dir_, base), fill="#C9D2DE", width=int(K))
    d.line([tuple(s(*p)) for p in pts], fill=cor, width=int(2.5 * K), joint="curve")
    for (px, py), v in zip(pts, valores):
        d.ellipse(s(px - 3, py - 3, px + 3, py + 3), fill=cor)
    i_max = valores.index(max(valores))
    text(d, pts[i_max][0], pts[i_max][1] - 6, fmt(valores[i_max]), f("SemiBold", 8), TXT, "md")
    eixo_anos(d, esq, passo, base)


def segmentacao(d, painel, opcoes, escolhida):
    x, y, w, h = painel
    yy = y + 70
    for o in opcoes:
        cx = x + 34
        d.ellipse(s(cx - 8, yy - 8, cx + 8, yy + 8), outline=AZUL, width=int(1.5 * K))
        if o == escolhida:
            d.ellipse(s(cx - 4, yy - 4, cx + 4, yy + 4), fill=AZUL)
        text(d, cx + 18, yy, o, f("SemiBold" if o == escolhida else "Regular", 12), TXT, "lm")
        yy += 34


def colunas_trim(d, painel):
    x, y, w, h = painel
    esq, dir_, topo, base = x + 24, x + w - 20, y + 74, y + h - 46
    passo = (dir_ - esq) / len(TRIM)
    vmax = max(v for _, v, _ in TRIM) * 1.08
    for i, (t, v, yoy) in enumerate(TRIM):
        cor = AZUL if yoy is None else (VERDE if yoy >= 0 else VERMELHO)
        cx = esq + passo * (i + 0.5)
        bh = (base - topo) * v / vmax
        d.rounded_rectangle(s(cx - passo * 0.3, base - bh, cx + passo * 0.3, base), radius=int(2 * K), fill=cor)
        text(d, cx, base - bh - 3, num(v), f("SemiBold", 8), TXT, "md")
        if yoy is not None:
            text(d, cx, base - bh + 6, num(yoy, 1) + "%", f("SemiBold", 8), BRANCO, "ma")
        text(d, cx, base + 5, t, f("Regular", 9), TXT2, "ma")
    for ano, ini, n in (("2025", 0, 4), ("2026", 4, 2)):
        text(d, esq + passo * (ini + n / 2), base + 21, ano, f("SemiBold", 10), TXT, "ma")


# ---------- Página Faturação ----------
kpis_f = [("FATURAÇÃO TOTAL", EUR(16050), AZUL), ("CUSTO TOTAL", EUR(6405), CIANO),
          ("MARGEM DE LUCRO", EUR(9645), AZUL), ("QUANTIDADE VENDIDA", "450", CIANO)]
tit_f = {"esq": "Métrica a Analisar por Ano e Mês",
         "dir_cima": "Métrica a Analisar",
         "dir_baixo": "Faturação por Trimestre - cor pela Variação Homóloga"}
args_f = ("LusaTech - Faturação", SUB, kpis_f, tit_f,
          "Fonte: parâmetro de campo Métrica a Analisar + _Medidas[Variação Homóloga %]  ·  " + RODAPE)


def desenhar_f(d):
    linha(d, PAINEIS["esq"], FAT, AZUL, EUR)
    segmentacao(d, PAINEIS["dir_cima"], ["Total Faturação", "Total Custo", "Total Margem"], "Total Faturação")
    x, y, w, h = PAINEIS["dir_cima"]
    text(d, x + 20, y + h - 22, "Seleção única: o eixo Y mostra uma métrica de cada vez", f("Regular", 9), TXT3, "lm")
    colunas_trim(d, PAINEIS["dir_baixo"])


pagina(OUT, "faturacao", args_f, kpis_f, desenhar_f)

# ---------- Página Simulação ----------
SIM = [v * (1 + TAXA) for v in FAT]
kpis_s = [("TOTAL FATURAÇÃO", EUR(16050), AZUL), ("FATURAÇÃO SIMULADA", EUR(17655), CIANO),
          ("IMPACTO DA SIMULAÇÃO", "+" + EUR(1605), VERDE), ("SIMULAÇÃO CRESCIMENTO", "10%", AMARELO)]
tit_s = {"esq": "Total Faturação vs Faturação Simulada por Ano e Mês",
         "dir_cima": "Simulação Crescimento",
         "dir_baixo": "Resumo por Ano"}
args_s = ("LusaTech - Simulação", SUB, kpis_s, tit_s,
          "Fonte: parâmetro numérico Simulação Crescimento (0% a 20%, saltos de 5%) + _Medidas[Faturação Simulada]  ·  " + RODAPE)


def colunas_mes(d, painel):
    x, y, w, h = painel
    esq, dir_, topo, base = x + 24, x + w - 16, y + 84, y + h - 46
    passo = (dir_ - esq) / len(FAT)
    vmax = max(SIM) * 1.08
    bw = passo * 0.36
    for i, (a, b) in enumerate(zip(FAT, SIM)):
        cx = esq + passo * (i + 0.5)
        for j, (v, cor) in enumerate(((a, AZUL), (b, CIANO))):
            bx = cx - bw + j * bw
            bh = (base - topo) * v / vmax
            d.rectangle(s(bx + 0.5, base - bh, bx + bw - 0.5, base), fill=cor)
    d.line(s(esq, base, dir_, base), fill="#C9D2DE", width=int(K))
    eixo_anos(d, esq, passo, base)
    lx = x + w - 20
    for nome, cor in reversed([("Total Faturação", AZUL), ("Faturação Simulada", CIANO)]):
        tw = d.textlength(nome, font=f("Regular", 10)) / K
        lx -= tw
        text(d, lx, y + 62, nome, f("Regular", 10), TXT, "lm")
        d.rounded_rectangle(s(lx - 14, y + 57, lx - 5, y + 67), radius=int(2 * K), fill=cor)
        lx -= 28


def deslizador(d, painel):
    x, y, w, h = painel
    text(d, x + 20, y + 70, "10%", f("SemiBold", 26), AZUL, "lm")
    x0, x1, yy = x + 30, x + w - 30, y + 128
    d.rounded_rectangle(s(x0, yy - 3, x1, yy + 3), radius=int(3 * K), fill="#D5DBE5")
    xv = x0 + (x1 - x0) * TAXA / 0.20
    d.rounded_rectangle(s(x0, yy - 3, xv, yy + 3), radius=int(3 * K), fill=AZUL)
    d.ellipse(s(xv - 9, yy - 9, xv + 9, yy + 9), fill=BRANCO, outline=AZUL, width=int(2 * K))
    for i in range(5):
        tx = x0 + (x1 - x0) * i / 4
        text(d, tx, yy + 18, f"{i * 5}%", f("Regular", 9), TXT2, "ma")
    text(d, x + 20, y + h - 22, "Mín. 0  ·  Máx. 0,20  ·  Incremento 0,05  ·  Predefinido 0,1", f("Regular", 9), TXT3, "lm")


def desenhar_s(d):
    colunas_mes(d, PAINEIS["esq"])
    deslizador(d, PAINEIS["dir_cima"])
    matriz(d, PAINEIS["dir_baixo"], ["Ano", "Total Faturação", "Faturação Simulada"],
           [(0, ["2025", EUR(12455), EUR2(13700.5)], {}, False),
            (0, ["2026", EUR(3595), EUR2(3954.5)], {}, False),
            (2, ["Total", EUR(16050), EUR2(17655)], {}, True)],
           [100, 140, 160], alt=32)


pagina(OUT, "simulacao", args_s, kpis_s, desenhar_s, cores_valor={1: CIANO, 2: VERDE})

shutil.copy(os.path.join(AQUI, "..", "OA6 - DAX e indicadores", "oa-06", "lab-assincrono", "dashboard", "tema-skodji.json"),
            os.path.join(OUT, "tema-skodji.json"))
print("ok")
