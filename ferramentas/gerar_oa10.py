"""OA10 - Projeto final EcoLogística S.A.: Landing Page, Análise Financeira, Produtos e
Motoristas, Simulação e a página de descrição (tooltip).

Lê os valores de 'OA10- dados Iniciais.xlsx' (material do formador, fica fora do Git)."""
import collections
import os
import shutil
import openpyxl
from PIL import Image, ImageDraw
from skodji_dashboard import *

LAB = os.path.join(AQUI, "..", "OA10 - Avaliação e próximos passos", "oa-10", "lab-assincrono")
OUT = os.path.join(LAB, "dashboard")
EUR = lambda v: num(v) + " €"
EUR2 = lambda v: num(v, 2) + " €"
MESES = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
SUB = "Skodji Digital  ·  Upskilling BI & Cloud  ·  OA10 Projeto Final - Dashboard de Comando"
RODAPE = "Edmilson Landim  ·  Novembro 2026"

# ---------- dados ----------
wb = openpyxl.load_workbook(os.path.join(LAB, "OA10- dados Iniciais.xlsx"), data_only=True)
ENT = [r for r in wb["Entregas"].iter_rows(min_row=2, values_only=True) if r[0]]
MOT = {r[0]: (r[1], r[2]) for r in wb["Motoristas"].iter_rows(min_row=2, values_only=True) if r[0]}
FROTA = {r[0]: (r[1], r[2]) for r in wb["Frota"].iter_rows(min_row=2, values_only=True) if r[0]}

N = len(ENT)
CUSTO = sum(r[4] for r in ENT)
FAT = sum(r[5] for r in ENT)
MARG = FAT - CUSTO
ATRASOS = sum(r[6] == "Atrasado" for r in ENT)
KM = sum(r[3] for r in ENT)

fat_mes, custo_mes, ent_mes = [0] * 12, [0] * 12, [0] * 12
fat_am = collections.defaultdict(float)
for r in ENT:
    m = r[0].month - 1
    fat_mes[m] += r[5]
    custo_mes[m] += r[4]
    ent_mes[m] += 1
    fat_am[(r[0].year, r[0].month)] += r[5]
por_mot = collections.Counter(r[2] for r in ENT)
por_veic = collections.Counter(r[1] for r in ENT)
ranking = sorted(por_mot.items(), key=lambda t: (-t[1], MOT[t[0]][0]))
rank_dense = {}
for mid, n in ranking:
    rank_dense[mid] = sorted(set(por_mot.values()), reverse=True).index(n) + 1
top_n = [t for t in ranking if t[1] >= ranking[4][1]]  # Top 5 com empates


def colunas_empilhadas(d, painel):
    x, y, w, h = painel
    esq, dir_, topo, base = x + 24, x + w - 16, y + 84, y + h - 30
    passo = (dir_ - esq) / 12
    vmax = max(a + b for a, b in zip(fat_mes, custo_mes)) * 1.08
    for i in range(12):
        cx = esq + passo * (i + 0.5)
        bw = passo * 0.6
        hf = (base - topo) * fat_mes[i] / vmax
        hc = (base - topo) * custo_mes[i] / vmax
        d.rectangle(s(cx - bw / 2, base - hf, cx + bw / 2, base), fill=AZUL)
        d.rectangle(s(cx - bw / 2, base - hf - hc, cx + bw / 2, base - hf), fill=CIANO)
        text(d, cx, base - hf - hc - 3, num(fat_mes[i] + custo_mes[i]), f("SemiBold", 8), TXT, "md")
        text(d, cx, base - hf / 2, num(fat_mes[i]), f("SemiBold", 8), BRANCO, "mm")
        text(d, cx, base + 6, MESES[i], f("Regular", 10), TXT2, "ma")
    d.line(s(esq, base, dir_, base), fill="#C9D2DE", width=int(K))
    legenda(d, x + w - 20, y + 62, [("Faturação Total", AZUL), ("Custo Total", CIANO)])


def legenda(d, lx, ly, itens):
    for nome, cor in reversed(itens):
        tw = d.textlength(nome, font=f("Regular", 10)) / K
        lx -= tw
        text(d, lx, ly, nome, f("Regular", 10), TXT, "lm")
        d.rounded_rectangle(s(lx - 14, ly - 5, lx - 5, ly + 5), radius=int(2 * K), fill=cor)
        lx -= 28


def cartao_linhas(d, painel):
    """Cartão de várias linhas: 3 medidas lado a lado."""
    x, y, w, h = painel
    vals = [(str(N), "Total Entregas"), (EUR2(FAT), "Faturação Total"), (EUR2(MARG), "Margem de Lucro")]
    cw = (w - 40) / 3
    for i, (v, lab) in enumerate(vals):
        cx = x + 20 + cw * i
        d.rectangle(s(cx, y + 70, cx + 4, y + 150), fill=AZUL if i != 1 else CIANO)
        text(d, cx + 14, y + 100, v, f("SemiBold", 19), AZUL, "lm")
        text(d, cx + 14, y + 132, lab, f("Regular", 10), TXT2, "lm")


def matriz_regiao(d, painel):
    regioes = ["Centro", "Norte", "Sul"]
    ids = sorted(MOT)
    cab = ["Região"] + ids + ["Total"]
    linhas = []
    for rg in regioes:
        vals = [rg]
        for mid in ids:
            vals.append(str(por_mot[mid]) if MOT[mid][1] == rg and por_mot[mid] else "")
        vals.append(str(sum(por_mot[m] for m in ids if MOT[m][1] == rg)))
        linhas.append((1, vals, {}, False))
    linhas.append((2, ["Total"] + [str(por_mot[m]) for m in ids] + [str(N)], {}, True))
    matriz(d, painel, cab, linhas, [58] + [27] * 10 + [42], alt=30)


def barras_top(d, painel):
    x, y, w, h = painel
    topo, esq = y + 80, x + 190
    alt = (h - 110) / len(top_n)
    vmax = max(n for _, n in top_n)
    for i, (mid, n) in enumerate(top_n):
        yy = topo + i * alt
        bw = (w - 260) * n / vmax
        d.rounded_rectangle(s(esq, yy + alt * 0.2, esq + bw, yy + alt * 0.8), radius=int(3 * K), fill=AZUL if i == 0 else CIANO)
        text(d, esq - 12, yy + alt / 2, MOT[mid][0], f("Regular", 12), TXT, "rm")
        text(d, esq + bw + 10, yy + alt / 2, str(n), f("SemiBold", 13), TXT, "lm")
    text(d, x + 20, y + h - 18, "Filtro N Superior 5 por Total Entregas: 4 motoristas empatados com 3 entregas -> 6 barras",
         f("Regular", 9), TXT3, "lm")


def tabela_veiculos(d, painel):
    x, y, w, h = painel
    tx, ty, alt = x + 20, y + 58, 34
    cab, larg = ["ID Veículo", "Modelo", "Total Entregas"], [100, 170, 130]
    d.rectangle(s(tx, ty, tx + sum(larg), ty + 26), fill=AZUL)
    cx = tx
    for i, (c, lw) in enumerate(zip(cab, larg)):
        text(d, cx + (8 if i < 2 else lw - 8), ty + 13, c, f("SemiBold", 10), BRANCO, "lm" if i < 2 else "rm")
        cx += lw
    yy = ty + 26
    vmax = max(por_veic.values())
    for vid in sorted(FROTA):
        n = por_veic[vid]
        bx = tx + larg[0] + larg[1]
        d.rectangle(s(bx + 4, yy + 6, bx + 4 + (larg[2] - 36) * n / vmax, yy + alt - 6), fill="#8FD3F2")
        text(d, tx + 8, yy + alt / 2, vid, f("Regular", 11), TXT, "lm")
        text(d, tx + larg[0] + 8, yy + alt / 2, FROTA[vid][0], f("Regular", 11), TXT, "lm")
        text(d, tx + sum(larg) - 8, yy + alt / 2, str(n), f("SemiBold", 11), TXT, "rm")
        d.line(s(tx, yy + alt, tx + sum(larg), yy + alt), fill=LINHA, width=int(K))
        yy += alt


def tabela_ranking(d, painel):
    linhas = [(1, [MOT[mid][0], MOT[mid][1], str(n), str(rank_dense[mid])], {3: AZUL}, i == 0)
              for i, (mid, n) in enumerate(ranking)]
    matriz(d, painel, ["Motorista", "Região", "Entregas", "Ranking"], linhas, [150, 90, 80, 80], alt=18)


def colunas_simples(d, painel, valores, cor, fmt):
    x, y, w, h = painel
    esq, dir_, topo, base = x + 24, x + w - 16, y + 84, y + h - 30
    passo = (dir_ - esq) / len(valores)
    vmax = max(valores) * 1.1
    for i, v in enumerate(valores):
        cx = esq + passo * (i + 0.5)
        bh = (base - topo) * v / vmax
        d.rounded_rectangle(s(cx - passo * 0.3, base - bh, cx + passo * 0.3, base), radius=int(2 * K), fill=cor)
        text(d, cx, base - bh - 3, fmt(v), f("SemiBold", 9), TXT, "md")
        text(d, cx, base + 6, MESES[i], f("Regular", 10), TXT2, "ma")
    d.line(s(esq, base, dir_, base), fill="#C9D2DE", width=int(K))


def segmentacao(d, painel, opcoes, escolhida):
    x, y, w, h = painel
    yy = y + 76
    for o in opcoes:
        cx = x + 34
        d.ellipse(s(cx - 8, yy - 8, cx + 8, yy + 8), outline=AZUL, width=int(1.5 * K))
        if o == escolhida:
            d.ellipse(s(cx - 4, yy - 4, cx + 4, yy + 4), fill=AZUL)
        text(d, cx + 18, yy, o, f("SemiBold" if o == escolhida else "Regular", 12), TXT, "lm")
        yy += 36
    text(d, x + 20, y + h - 22, "Parâmetro de campo, seleção única", f("Regular", 9), TXT3, "lm")


def tabela_mom(d, painel):
    linhas = []
    for m in range(1, 7):
        v = fat_am[(2026, m)]
        lm = fat_am[(2026, m - 1)] if m > 1 else fat_am[(2025, 12)]
        var = (v - lm) / lm * 100
        linhas.append((1, [MESES[m - 1] + " 2026", EUR(v), EUR(lm), num(var, 2) + "%"],
                       {3: VERDE if var >= 0 else VERMELHO}, False))
    matriz(d, painel, ["Mês", "Faturação", "Faturação LM", "Variação MoM %"], linhas, [100, 90, 100, 110], alt=26)


# ---------- páginas ----------
def pagina_af():
    kpis = [("CUSTO TOTAL", EUR2(CUSTO), AZUL), ("MARGEM POR ENTREGA", EUR2(MARG / N), CIANO),
            ("% ATRASOS", num(ATRASOS / N * 100, 2) + "%", VERMELHO), ("DISTÂNCIA TOTAL", num(KM) + " km", CIANO)]
    tit = {"esq": "Faturação Total e Custo Total por Mês",
           "dir_cima": "KPIs - Cartão de várias linhas",
           "dir_baixo": "Total Entregas por Região e Motorista"}
    args = ("EcoLogística - Análise Financeira", SUB, kpis, tit,
            "Fonte: OA10- dados Iniciais.xlsx (Entregas, Frota, Motoristas) + Calendario (DAX)  ·  " + RODAPE)

    def desenhar(d):
        colunas_empilhadas(d, PAINEIS["esq"])
        cartao_linhas(d, PAINEIS["dir_cima"])
        matriz_regiao(d, PAINEIS["dir_baixo"])
    pagina(OUT, "analise-financeira", args, kpis, desenhar, cores_valor={2: VERMELHO})


def pagina_pm():
    nome1 = MOT[ranking[0][0]][0]
    kpis = [("MOTORISTAS", str(len(MOT)), AZUL), ("VEÍCULOS", str(len(FROTA)), CIANO),
            ("MOTORISTA Nº 1", nome1, AZUL), ("ENTREGAS DO Nº 1", str(ranking[0][1]), CIANO)]
    tit = {"esq": "Top 5 Motoristas por Total Entregas",
           "dir_cima": "Entregas por Veículo (barras de dados)",
           "dir_baixo": "Ranking Motoristas (RANKX)"}
    args = ("EcoLogística - Produtos e Motoristas", SUB, kpis, tit,
            "Fonte: Entregas, Frota[Modelo], Motoristas[Nome]  ·  descrição personalizada no gráfico de barras  ·  " + RODAPE)

    def desenhar(d):
        barras_top(d, PAINEIS["esq"])
        tabela_veiculos(d, PAINEIS["dir_cima"])
        tabela_ranking(d, PAINEIS["dir_baixo"])
    pagina(OUT, "produtos-motoristas", args, kpis, desenhar)


def pagina_sim():
    kpis = [("TOTAL ENTREGAS", str(N), AZUL), ("FATURAÇÃO TOTAL", EUR(FAT), CIANO),
            ("FATURAÇÃO MÉDIA POR ENTREGA", EUR2(FAT / N), AZUL), ("ÚLTIMO MÊS (JUN 2026)", EUR(fat_am[(2026, 6)]), CIANO)]
    tit = {"esq": "Métrica Selecionada por Mês",
           "dir_cima": "Métrica a Analisar",
           "dir_baixo": "Faturação vs Mês Anterior (2026)"}
    args = ("EcoLogística - Simulação", SUB, kpis, tit,
            "Fonte: parâmetro de campo (Total Entregas / Faturação Total) + _Medidas[Faturação LM]  ·  " + RODAPE)

    def desenhar(d):
        colunas_simples(d, PAINEIS["esq"], fat_mes, AZUL, num)
        segmentacao(d, PAINEIS["dir_cima"], ["Total Entregas", "Faturação Total"], "Faturação Total")
        tabela_mom(d, PAINEIS["dir_baixo"])
    pagina(OUT, "simulacao", args, kpis, desenhar)


def landing():
    paginas = [("Análise Financeira", "Faturação, custos, KPIs e entregas por região"),
               ("Produtos e Motoristas", "Top 5 motoristas, frota e ranking"),
               ("Simulação", "Alternar entre Entregas e Faturação")]
    nav_x, nav_y, nav_w, nav_h, gap = 64, 352, 1152, 64, 16

    def base():
        im = Image.new("RGB", s(W, H), FUNDO)
        d = ImageDraw.Draw(im)
        d.rectangle(s(0, 0, W, 300), fill=AZUL)
        d.polygon([tuple(s(900, 0)), tuple(s(W, 0)), tuple(s(W, 300)), tuple(s(820, 300))], fill=AZUL_ESC)
        d.polygon([tuple(s(1010, 0)), tuple(s(W, 0)), tuple(s(W, 300)), tuple(s(930, 300))], fill=CIANO)
        text(d, 42, 44, "EcoLogística S.A.  ·  Dashboard de Comando", f("Medium", 15), "#D6E6F7")
        text(d, 42, 240, "Eficiência das entregas, custos de combustível e pontualidade dos motoristas  ·  2024-2026",
             f("Regular", 14), "#D6E6F7")
        ic = Image.open(os.path.join(AQUI, "icone.png")).convert("RGBA")
        hh = int(150 * K)
        ic = ic.resize((int(ic.width * hh / ic.height), hh), Image.LANCZOS)
        im.paste(ic, (int(1080 * K), int(70 * K)), ic)
        d.rounded_rectangle(s(40, 318, W - 40, 486), radius=int(12 * K), fill=BRANCO)
        text(d, 64, 324, "Escolha uma página", f("SemiBold", 13), TXT)
        bw = (nav_w - gap * 2) / 3
        for i, (_, desc) in enumerate(paginas):
            text(d, nav_x + i * (bw + gap) + bw / 2, nav_y + nav_h + 22, desc, f("Regular", 10), TXT2, "ma")
        cw = (W - 80 - 3 * 16) / 4
        for i, lab in enumerate(["TOTAL ENTREGAS", "FATURAÇÃO TOTAL", "MARGEM DE LUCRO", "% ATRASOS"]):
            x = 40 + i * (cw + 16)
            d.rounded_rectangle(s(x, 510, x + cw, 610), radius=int(10 * K), fill=BRANCO)
            d.rounded_rectangle(s(x, 510, x + 6, 610), radius=int(3 * K), fill=VERMELHO if i == 3 else (AZUL if i % 2 == 0 else CIANO))
            text(d, x + 22, 526, lab, f("Medium", 10), TXT2)
        lg = Image.open(os.path.join(AQUI, "logo_skodji.png")).convert("RGBA")
        hh = int(40 * K)
        lg = lg.resize((int(lg.width * hh / lg.height), hh), Image.LANCZOS)
        d.rounded_rectangle(s(W - 40 - 190, 640, W - 40, 696), radius=int(10 * K), fill=CIANO)
        im.paste(lg, (int((W - 40 - 95) * K - lg.width / 2), int(648 * K)), lg)
        text(d, 40, 656, SUB, f("Regular", 11), TXT2, "lm")
        text(d, 40, 680, RODAPE + "  ·  Navegação: Ctrl + clique no Power BI Desktop, clique simples no Service",
             f("Regular", 10), TXT3, "lm")
        return im, bw

    im, _ = base()
    im.save(os.path.join(OUT, "fundo-landing.png"), optimize=True)
    im, bw = base()
    d = ImageDraw.Draw(im)
    text(d, 40, 150, "Relatório", f("SemiBold", 54), BRANCO, "lm")
    for i, (nome, _) in enumerate(paginas):
        x = nav_x + i * (bw + gap)
        d.rounded_rectangle(s(x, nav_y, x + bw, nav_y + nav_h), radius=int(10 * K), fill=AZUL)
        text(d, x + bw / 2, nav_y + nav_h / 2, nome, f("SemiBold", 16), BRANCO, "mm")
    cw = (W - 80 - 3 * 16) / 4
    for i, v in enumerate([str(N), EUR(FAT), EUR2(MARG), num(ATRASOS / N * 100, 2) + "%"]):
        text(d, 40 + i * (cw + 16) + 22, 552, v, f("SemiBold", 26), VERMELHO if i == 3 else AZUL)
    im.save(os.path.join(OUT, "mockup-landing.png"), optimize=True)


def tooltip():
    """Página de descrição 320 x 240: cartão Total Entregas + linha Faturação por mês (ex.: Elsa Teixeira)."""
    mid = ranking[0][0]
    fm = [0] * 12
    for r in ENT:
        if r[2] == mid:
            fm[r[0].month - 1] += r[5]
    im = Image.new("RGB", s(320, 240), BRANCO)
    d = ImageDraw.Draw(im)
    text(d, 12, 10, MOT[mid][0], f("SemiBold", 11), TXT2)
    text(d, 12, 30, str(por_mot[mid]), f("SemiBold", 28), AZUL)
    text(d, 60, 48, "Total Entregas", f("Regular", 10), TXT2, "lm")
    esq, dir_, topo, base = 16, 308, 96, 212
    passo = (dir_ - esq) / 12
    vmax = max(fm) * 1.15
    pts = [(esq + passo * (i + 0.5), base - (base - topo) * v / vmax) for i, v in enumerate(fm)]
    d.line(s(esq, base, dir_, base), fill="#C9D2DE", width=int(K))
    # meses sem entregas ficam em branco: a linha liga só os meses com valor
    com_valor = [(p, v) for p, v in zip(pts, fm) if v]
    d.line([tuple(s(*p)) for p, _ in com_valor], fill=AZUL, width=int(2 * K), joint="curve")
    for (px, py), v in com_valor:
        d.ellipse(s(px - 2.5, py - 2.5, px + 2.5, py + 2.5), fill=AZUL)
        text(d, px, py - 4, num(v), f("SemiBold", 7), TXT, "md")
    for i, m in enumerate(MESES):
        text(d, esq + passo * (i + 0.5), base + 4, m, f("Regular", 7), TXT2, "ma")
    text(d, 12, 78, "Faturação Total por Mês", f("Medium", 9), TXT2)
    im.save(os.path.join(OUT, "mockup-tooltip.png"), optimize=True)


os.makedirs(OUT, exist_ok=True)
landing()
pagina_af()
pagina_pm()
pagina_sim()
tooltip()
shutil.copy(os.path.join(AQUI, "..", "OA6 - DAX e indicadores", "oa-06", "lab-assincrono", "dashboard", "tema-skodji.json"),
            os.path.join(OUT, "tema-skodji.json"))
print("ok", N, FAT, round(CUSTO, 2), round(MARG, 2), ATRASOS, [(MOT[m][0], n, rank_dense[m]) for m, n in ranking])
print("fat_mes", fat_mes, "custo_mes", [round(c, 1) for c in custo_mes], "ent_mes", ent_mes)
