"""OA6 - Lab Assíncrono (LusaTech): página Matriz."""
import os
from skodji_dashboard import *

OUT = os.path.join(AQUI, "..", "OA6 - DAX e indicadores", "oa-06", "lab-assincrono", "dashboard")
EUR = lambda v: num(v) + " €"
PCT = lambda v: num(v, 2) + "%"

f25 = [905, 625, 1035, 1335, 1380, 845, 780, 1320, 855, 870, 955, 1550]
f26 = [1040, 585, 865, 730, 375] + [0] * 7
MESES = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
T = 16050

kpis = [("TOTAL FATURAÇÃO", EUR(T), AZUL), ("TOTAL MARGEM", EUR(9645), CIANO),
        ("VARIAÇÃO HOMÓLOGA 2026", "-71,1%", AZUL), ("% FATURAÇÃO TOTAL 2026", "22,4%", CIANO)]
titulos = {"esq": "Matriz - Faturação, Ano Anterior, Variação Homóloga e % do Total",
           "dir_cima": "Total Faturação vs Ano Anterior (Jan-Mai)",
           "dir_baixo": "% Faturação Total por Ano"}
args = ("LusaTech - Medidas DAX", "Skodji Digital  ·  Upskilling BI & Cloud  ·  OA6 Lab Assíncrono - Medidas e Inteligência Temporal",
        kpis, titulos, "Fonte: tabela _Medidas (Total Faturação, Faturação Ano Anterior, Variação Homóloga %, % Faturação Total)  ·  Edmilson Landim  ·  Novembro 2026")


def linhas():
    out = [(0, ["+ 2025", EUR(12455), "", "", PCT(77.60)], {}, True),
           (0, ["- 2026", EUR(3595), EUR(12455), "-71,13%", PCT(22.40)], {3: VERMELHO}, True)]
    for i, m in enumerate(MESES):
        v, p = f26[i], f25[i]
        yoy = (v - p) / p * 100
        out.append((1, [m, EUR(v) if v else "", EUR(p), num(yoy, 2) + "%", PCT(v / T * 100) if v else ""],
                    {3: VERDE if yoy > 0 else VERMELHO}, False))
    out.append((2, ["Total", EUR(T), EUR(12455), "28,86%", "100,00%"], {}, True))
    return out


def desenhar(d):
    matriz(d, PAINEIS["esq"], ["Ano / Mês Nome", "Total Faturação", "Faturação Ano Anterior", "Variação Homóloga %", "% Faturação Total"],
           linhas(), [128, 140, 176, 160, 132])
    colunas_duplas(d, PAINEIS["dir_cima"], MESES[:5], f26[:5], f25[:5], [AZUL, CIANO],
                   ["Total Faturação (2026)", "Ano Anterior (2025)"], lambda v: num(v))
    anel(d, PAINEIS["dir_baixo"], [("2025", 12455, CIANO), ("2026", 3595, AZUL)], EUR(T),
         lambda v: f"{EUR(v)} ({num(100 * v / T, 1)}%)")


pagina(OUT, "matriz", args, kpis, desenhar, cores_valor={2: VERMELHO})
import shutil
shutil.copy(os.path.join(AQUI, "..", "OA5 - Introdução ao DAX", "oa-05", "lab-assincrono", "dashboard", "tema-skodji.json"),
            os.path.join(OUT, "tema-skodji.json"))
print("ok")
