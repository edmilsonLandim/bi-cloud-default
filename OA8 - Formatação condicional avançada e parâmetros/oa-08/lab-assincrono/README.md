# OA8 - Lab Assíncrono: Parâmetros e Formatação Avançada

- Data limite: 20/11/2026 às 23:59
- Base: o exercício do OA7 (LusaTech). Usar o próprio:
  [`../../../OA7 - Tooltips e formatação condicional/oa-07/lab-assincrono/EdmilsonLandim-03-11-2026.pbix`](../../../OA7%20-%20Tooltips%20e%20formatação%20condicional/oa-07/lab-assincrono/EdmilsonLandim-03-11-2026.pbix)
  -> **Guardar como** `EdmilsonLandim-dd-mm-yyyy.pbix` **nesta pasta**. Alternativa do
  formador: `OA7-Exercicio resolvido.pbix`.
- Objetivo: escolher a métrica do gráfico (parâmetro de campo), colorir colunas pela
  Variação Homóloga e simular crescimento (parâmetro numérico / What-if).

## Parte 1 - Parâmetro de campo `Métrica a Analisar`
1. Abrir a página **Faturação**.
2. **Modelação -> Novo parâmetro -> Campos**.
3. Nome: **`Métrica a Analisar`**.
4. Em **Campos**, abrir `_Medidas` e marcar, por esta ordem, `Total Faturação`,
   `Total Custo`, `Total Margem`. Deixar **Adicionar segmentação a esta página** ligado ->
   **Criar**.
5. O Power BI cria a tabela `Métrica a Analisar` e uma segmentação na página.
6. Selecionar a segmentação -> **Formatar visual -> Visual -> Definições da segmentação ->
   Seleção** -> **Seleção única** ligado. (Opcional: **Opções -> Estilo** = **Mosaico** ou
   **Lista vertical**.)
7. Novo visual **Gráfico de linhas**:
   - **Eixo X**: `Calendario[Ano]` e depois `Calendario[Mês Nome]`.
   - **Eixo Y**: o campo **`Métrica a Analisar`** (da tabela nova).
   - No visual, **Expandir tudo um nível abaixo** (seta dupla para baixo) para ver os meses.
8. Testar: escolher cada opção na segmentação; o eixo Y e o título mudam.

Valores esperados por mês:

| Mês | Faturação | Custo | Margem |
|---|---|---|---|
| Jan 2025 | 905 € | 370 € | 535 € |
| Fev 2025 | 625 € | 250 € | 375 € |
| Mar 2025 | 1.035 € | 410 € | 625 € |
| Abr 2025 | 1.335 € | 530 € | 805 € |
| Mai 2025 | 1.380 € | 535 € | 845 € |
| Jun 2025 | 845 € | 360 € | 485 € |
| Jul 2025 | 780 € | 310 € | 470 € |
| Ago 2025 | 1.320 € | 500 € | 820 € |
| Set 2025 | 855 € | 350 € | 505 € |
| Out 2025 | 870 € | 360 € | 510 € |
| Nov 2025 | 955 € | 360 € | 595 € |
| Dez 2025 | **1.550 €** (máximo) | 650 € | 900 € |
| Jan 2026 | 1.040 € | 415 € | 625 € |
| Fev 2026 | 585 € | 240 € | 345 € |
| Mar 2026 | 865 € | 340 € | 525 € |
| Abr 2026 | 730 € | 300 € | 430 € |
| Mai 2026 | 375 € | 125 € | 250 € |
| **Total** | **16.050 €** | **6.405 €** | **9.645 €** |

Seleção única é obrigatória ("Golden Rule" do material de estudo): com várias métricas
escolhidas ao mesmo tempo, valores incompatíveis misturam-se no mesmo eixo.

## Parte 2 - Cores das colunas pela Variação Homóloga
1. Selecionar o **gráfico de colunas** da página Faturação (Faturação Total por Ano e
   Trimestre, do OA5).
2. **Formatar visual -> Visual -> Colunas -> Cor** -> botão **fx**.
3. Configurar:
   - **Estilo de formatação** = **Regras**.
   - **Em que campo devemos basear isto?** = `_Medidas` -> **Variação Homóloga %**.
4. Regra 1 (quebras, vermelho): Se o valor **>=** *(apagar o 0, a caixa fica vazia =
   Mínimo)* **Número** **e** **<** `0` **Número** -> vermelho `#DF3131`.
5. **+ Nova regra**. Regra 2 (crescimentos, verde): Se o valor **>=** `0` **Número** **e**
   **<=** *(caixa vazia = Máximo)* **Número** -> verde `#2E9E5B`.
6. **OK**.

Resultado esperado:

| Coluna | Faturação | Ano anterior | Variação Homóloga % | Cor |
|---|---|---|---|---|
| 2025 T1-T4 | 2.565 / 3.560 / 2.955 / 3.375 € | - | vazio | cor padrão |
| 2026 T1 | 2.490 € | 2.565 € | **-2,92%** | vermelho |
| 2026 T2 | 1.105 € | 3.560 € | **-68,96%** | vermelho |

- 2025 não tem histórico (o calendário começa em 2025): fica com a cor padrão.
- 2026 fica todo a vermelho: os dois trimestres caíram. O T2 só tem dados até 03/05/2026,
  daí a quebra tão grande.
- No OA5 este gráfico tinha as cores alternadas por ano (`Cor Ano`, valor do campo). As
  regras substituem essa formatação: só há um **fx** por cor.

## Parte 3 - Simulação de cenários (What-if)
1. Nova página -> nome **`Simulação`**.
2. Visual **Gráfico de colunas agrupadas**: **Eixo X** `Calendario[Ano]` e
   `Calendario[Mês Nome]`; **Eixo Y** `[Total Faturação]`. Expandir um nível abaixo.
3. **Modelação -> Novo parâmetro -> Intervalo numérico**:

   | Campo | Valor |
   |---|---|
   | Nome | `Simulação Crescimento` |
   | Tipo de dados | **Número decimal** |
   | Mínimo | `0` |
   | Máximo | `0,2` (20%) |
   | Incremento | `0,05` |
   | Predefinição | `0,1` |
   | Adicionar segmentação a esta página | ligado |

   Com o Power BI em português, escrever as casas decimais com **vírgula**.
4. O Power BI cria a tabela `Simulação Crescimento` (coluna `Simulação Crescimento` e medida
   `Valor de Simulação Crescimento`) e uma segmentação. Se não for deslizador: **Formatar ->
   Definições da segmentação -> Estilo** = **Valor único**.
5. Em `_Medidas` -> **Nova medida** (formato **Moeda**, €):

```dax
Faturação Simulada =
[Total Faturação] * ( 1 + 'Simulação Crescimento'[Valor de Simulação Crescimento] )
```

6. Juntar `[Faturação Simulada]` ao **Eixo Y** do gráfico, por baixo de `Total Faturação`.
7. Formatar a coluna do parâmetro: painel **Dados** -> `Simulação Crescimento` -> coluna
   **`Simulação Crescimento`** -> **Ferramentas de coluna -> Formato** = **Percentagem**,
   **0** casas decimais. A segmentação passa a mostrar 0%, 5%, 10%, 15%, 20%.
8. Testar com o deslizador:

| Simulação Crescimento | Faturação Simulada (total) | 2025 | 2026 |
|---|---|---|---|
| 0% | 16.050,00 € | 12.455,00 € | 3.595,00 € |
| 5% | 16.852,50 € | 13.077,75 € | 3.774,75 € |
| **10% (predefinido)** | **17.655,00 €** | **13.700,50 €** | **3.954,50 €** |
| 15% | 18.457,50 € | 14.323,25 € | 4.134,25 € |
| 20% | 19.260,00 € | 14.946,00 € | 4.314,00 € |

Exemplo por mês a 10%: Dez 2025 1.550 € -> **1.705 €**; Mai 2026 375 € -> **412,50 €**.

Medida opcional para o cartão de impacto:

```dax
Impacto Simulação = [Faturação Simulada] - [Total Faturação]
```

## Dashboards (identidade Skodji Digital)
Ficheiros em [`dashboard/`](dashboard/): `fundo-faturacao.png`, `mockup-faturacao.png`,
`fundo-simulacao.png`, `mockup-simulacao.png`, `tema-skodji.json`. Fundo **Ajustar**,
transparência 0%; visuais sem título nem fundo.

### Página Faturação (nova disposição)
O gráfico de linhas precisa de largura para os 17 meses, por isso passa para o painel grande.
O de colunas por trimestre vai para baixo à direita. Saem dois visuais: a barra por produto
(já existe na página Produtos) e a margem por mês (o gráfico de linhas mostra-a quando se
escolhe Total Margem).

| Visual | Campos | X | Y | Largura | Altura |
|---|---|---|---|---|---|
| 4 cartões (iguais ao OA5) | Faturação, Custo, Margem, Quantidade | 38 / 350 / 662 / 974 | 122 | 270 | 50 |
| **Gráfico de linhas** | Eixo X `Ano`, `Mês Nome`; Eixo Y `Métrica a Analisar` | 34 | 242 | 756 | 444 |
| **Segmentação** `Métrica a Analisar` | seleção única | 826 | 242 | 420 | 160 |
| **Colunas por trimestre** (cores pela Variação Homóloga) | Eixo X `Ano`, `Trimestre`; Eixo Y `[Total Faturação]` | 826 | 478 | 420 | 208 |

Se o fundo do OA5 for substituído por `fundo-faturacao.png`, os títulos dos painéis já estão
na imagem.

### Página Simulação
| Visual | Campos | X | Y | Largura | Altura | Valor (10%) |
|---|---|---|---|---|---|---|
| Cartão - Total Faturação | `[Total Faturação]` | 38 | 122 | 270 | 50 | 16.050 € |
| Cartão - Faturação Simulada | `[Faturação Simulada]` | 350 | 122 | 270 | 50 | 17.655 € |
| Cartão - Impacto | `[Impacto Simulação]` (opcional) | 662 | 122 | 270 | 50 | 1.605 € |
| Cartão - Taxa | `[Valor de Simulação Crescimento]` (Percentagem) | 974 | 122 | 270 | 50 | 10% |
| **Colunas agrupadas** | Eixo X `Ano`, `Mês Nome`; Eixo Y `[Total Faturação]`, `[Faturação Simulada]` | 34 | 242 | 756 | 444 | |
| **Segmentação** `Simulação Crescimento` | Valor único | 826 | 242 | 420 | 160 | 10% |
| Tabela - Resumo por Ano | `Ano`, `[Total Faturação]`, `[Faturação Simulada]` | 826 | 478 | 420 | 208 | 13.700,50 € / 3.954,50 € |

## Evidências
Guardar em [`evidencias/`](evidencias/):
- `01-parametro-campo-e-cores.png` - página Faturação: segmentação, gráfico de linhas e
  colunas com 2026 a vermelho
- `03-simulacao.png` - página Simulação (com o deslizador em 10% ou 15%)
- `04-publicar-sucesso.png` / `05-submissao-moodle.png`

## Estado
- [x] Parte 1 - parâmetro de campo `Métrica a Analisar` (seleção única) + gráfico de linhas ([`EdmilsonLandim-09-11-2026.pbix`](EdmilsonLandim-09-11-2026.pbix))
- [x] Parte 2 - cores das colunas por `Variação Homóloga %` (2026 T1 e T2 a vermelho)
- [x] Parte 3 - parâmetro `Simulação Crescimento`, medida `Faturação Simulada` (17.655 € a 10%), página Simulação
- [x] Publicado no Power BI Service - [`evidencias/04-publicar-sucesso.png`](evidencias/04-publicar-sucesso.png)
- [x] Submetido no Moodle (09/11/2026 15:30, "Submetido para avaliação")
