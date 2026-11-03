# OA7 - Lab Assíncrono: Tooltips, Ranking e Formatação Condicional

- Abriu: 22/10/2026 às 19:45 - data limite: 20/11/2026 às 23:59
- Base: o exercício do OA6 (LusaTech). Usar o próprio:
  [`../../../OA6 - DAX e indicadores/oa-06/lab-assincrono/EdmilsonLandim-02-11-2026 oa-06.pbix`](../../../OA6%20-%20DAX%20e%20indicadores/oa-06/lab-assincrono/EdmilsonLandim-02-11-2026%20oa-06.pbix)
  -> **Guardar como** `EdmilsonLandim-dd-mm-yyyy.pbix` **nesta pasta**. Alternativa do
  formador: `OA6-Exercicio resolvido.pbix` (mesmos nomes: `Vendas`, `_Medidas`,
  `Total Faturação`, `Variação Homóloga %`).
- Objetivo: descrição (tooltip) em página de relatório, ranking de produtos com `RANKX`,
  alertas com formatação condicional e um visual personalizado do AppSource.

## Parte 1 - Página de descrição `Tooltip_Produto`
1. Nova página (**+** em baixo) -> duplo clique no nome -> **`Tooltip_Produto`**.
2. Botão direito no separador -> **Ocultar página**.
3. Clicar numa zona vazia da página -> **Formatar página** -> **Informações da página** ->
   **Tipo de página** -> **Descrição**. A página encolhe (320 x 240).
4. **Definições da tela** -> Tipo **Personalizado**.
5. **Largura** = **350** px (a altura fica 240).
6. Visual **Gráfico circular**: **Valores** `_Medidas[Total Faturação]`; **Legenda**
   `Vendas[ID Produto]`.
7. Formatar o gráfico:
   - **Geral -> Propriedades**: X 0, Y 0, Largura 350, Altura 240 (ocupa a página toda).
   - **Geral -> Título**: desligado; **Subtítulo**: desligado.
   - **Visual -> Legenda**: ligada, **Posição** = **Superior esquerda**.
8. Voltar à página **Faturação** -> selecionar o **gráfico de colunas** (Total Faturação por
   Ano e Trimestre).
9. **Formatar visual -> Geral -> Descrições** (Tooltips): ligado, **Tipo** = **Página de
   relatório**, **Página** = `Tooltip_Produto`.
10. Passar o rato numa coluna: aparece a pizza filtrada por esse ano e trimestre.

Valores esperados na descrição (a pizza mostra a repartição por produto da coluna):

| Coluna | P001 | P002 | P003 | P004 | P005 | Total |
|---|---|---|---|---|---|---|
| 2025 T1 | 650 € | 600 € | 480 € | 585 € | 250 € | 2.565 € |
| 2025 T2 | 725 € | 720 € | 645 € | 720 € | 750 € | 3.560 € |
| 2025 T3 | 475 € | 120 € | 660 € | 450 € | 1.250 € | 2.955 € |
| 2025 T4 | 875 € | 960 € | 480 € | 810 € | 250 € | 3.375 € |
| 2026 T1 | 550 € | 360 € | 495 € | 585 € | 500 € | 2.490 € |
| 2026 T2 | - | 480 € | 375 € | - | 250 € | 1.105 € |

Mockup da descrição: [`dashboard/mockup-tooltip-produto.png`](dashboard/mockup-tooltip-produto.png)
(2025 T1).

## Parte 2 - Ranking com DAX
1. Selecionar `_Medidas` -> **Nova medida**:

```dax
Ranking Vendas = RANKX ( ALL ( Vendas[ID Produto] ), [Total Faturação], , DESC, Dense )
```

2. Formato: **Número inteiro** (0 casas decimais).
3. Nova página -> nome **`Produtos`**.
4. Visual **Tabela** com `Vendas[ID Produto]`, `[Total Faturação]`, `[Ranking Vendas]`.
   Ordenar por `Ranking Vendas` (clicar no cabeçalho até ficar crescente).

| Ranking | ID Produto | Total Faturação |
|---|---|---|
| 1 | P001 | 3.275 € |
| 2 | P005 | 3.250 € |
| 3 | P002 | 3.240 € |
| 4 | P004 | 3.150 € |
| 5 | P003 | 3.135 € |

Porquê o `ALL`: sem ele, cada linha só "vê" o seu produto e todos ficam em 1.º lugar.
O `ALL(Vendas[ID Produto])` remove esse filtro e compara cada produto com a lista toda.
`Dense`: em caso de empate, o seguinte não salta posições (1, 1, 2 em vez de 1, 1, 3).

Na linha **Total** o ranking aparece **1** (o total comparado com os produtos). Opcional,
para o deixar vazio:

```dax
Ranking Vendas =
IF (
    ISINSCOPE ( Vendas[ID Produto] ),
    RANKX ( ALL ( Vendas[ID Produto] ), [Total Faturação], , DESC, Dense )
)
```

## Parte 3 - Formatação condicional
1. **Escala de cores**: em **Colunas** do visual, seta (ou botão direito) em
   `Total Faturação` -> **Formatação condicional** -> **Cor do fundo**:
   - Estilo **Gradação de cores**; **Valor mínimo** -> branco `#FFFFFF`;
     **Valor máximo** -> azul `#5B9BD5` (ou verde). OK.
   - P001 fica o mais escuro e P003 branco.
2. **Ícones**: juntar `[Variação Homóloga %]` à tabela -> seta no campo -> **Formatação
   condicional** -> **Ícones**:
   - **Estilo de formatação** = **Regras**; **Esquema de ícones** = **À direita dos dados**.
   - Regra 1: Se o valor **>=** `0` **Número** e **<=** `100` **Número** -> **seta verde
     para cima**.
   - Regra 2: Se o valor **>=** `-100` **Número** e **<** `0` **Número** -> **seta vermelha
     para baixo**.
   - Tipo **Número**, nunca **Percentagem** (a "armadilha do Percent" do material de
     estudo: Percentagem divide o intervalo mínimo-máximo e não o valor).

Valores na tabela (sem filtro de ano):

| ID Produto | Variação Homóloga % | Ícone |
|---|---|---|
| P001 | 20,18% | verde |
| P005 | 30,00% | verde |
| P002 | 35,00% | verde |
| P004 | 22,81% | verde |
| P003 | 38,41% | verde |
| Total | 28,86% | verde |

**Atenção, todos a verde não é erro.** A tabela não tem filtro de datas, por isso
`SAMEPERIODLASTYEAR` desloca 2025-2026 para 2024-2025 e o "ano anterior" é só 2025.
A variação compara o total (2025 + 2026) com 2025 e dá sempre positivo. Para testar as setas
vermelhas, filtrar a página por `Ano` = 2026 (segmentação ou painel Filtros): P003 -61,59%,
P002 -65,00%, P005 -70,00%, P004 -77,19%, P001 -79,82%; o ranking de 2026 passa a P003,
P002, P005, P004, P001.

## Parte 4 - Visual personalizado (AppSource)
1. Painel **Visualizações** -> **...** -> **Obter mais elementos visuais**.
   Pede início de sessão com a conta Microsoft / Power BI.
2. Pesquisar **Word Cloud** (Microsoft Corporation, selo azul de certificação) ->
   **Adicionar**. Aparece um ícone novo no painel Visualizações.
3. Inserir o Word Cloud na página **Produtos**: **Categoria** `Vendas[ID Produto]`;
   **Valores** `[Total Faturação]`.
4. As 5 palavras têm quase o mesmo tamanho (3.135 € a 3.275 €): é o resultado certo.

Alternativa sem AppSource: **...** -> **Importar um elemento visual de um ficheiro** ->
`.pbiviz` (ex.: o `enlightenWorldFlags...pbiviz` do lab síncrono, na pasta do OA7).

## Dashboard da página Produtos (identidade Skodji Digital)
Ficheiros em [`dashboard/`](dashboard/): `fundo-produtos.png`, `mockup-produtos.png`,
`mockup-tooltip-produto.png`, `tema-skodji.json`. Fundo **Ajustar**, transparência 0%;
visuais sem título nem fundo.

| Visual | Campos | X | Y | Largura | Altura | Valor esperado |
|---|---|---|---|---|---|---|
| Cartão - Total Faturação | `[Total Faturação]` | 38 | 122 | 270 | 50 | 16.050 € |
| Cartão - Produto Nº 1 | `Vendas[ID Produto]` + filtro do visual **N Superior** 1 por `[Total Faturação]` | 350 | 122 | 270 | 50 | P001 |
| Cartão - Faturação do Nº 1 | `[Total Faturação]` + `ID Produto` no filtro do visual, N Superior 1 | 662 | 122 | 270 | 50 | 3.275 € |
| Cartão - Nº de produtos | `Vendas[ID Produto]` -> **Contagem (Distinta)** | 974 | 122 | 270 | 50 | 5 |
| **Tabela** (pedido) | `ID Produto`, `Total Faturação`, `Ranking Vendas`, `Variação Homóloga %` | 34 | 242 | 756 | 444 | tabelas acima |
| **Word Cloud** (pedido) | Categoria `ID Produto`; Valores `[Total Faturação]` | 826 | 242 | 420 | 160 | P001...P005 |
| Tabela ou gráfico com descrição | ex.: gráfico de barras `ID Produto` x `[Total Faturação]` com **Descrições** -> `Tooltip_Produto` | 826 | 478 | 420 | 208 | opcional |

O painel de baixo à direita no mockup mostra a descrição como aparece ao passar o rato.

## Evidências
Guardar em [`evidencias/`](evidencias/):
- `01-tooltip-pagina.png` - página `Tooltip_Produto` (oculta, tipo Descrição, 350 px)
- `02-tooltip-hover.png` - página Faturação com a descrição aberta sobre uma coluna
- `03-produtos.png` - página Produtos (ranking, gradiente, ícones, Word Cloud)
- `04-publicar-sucesso.png` / `05-submissao-moodle.png`

## Estado
- [ ] Parte 1 - página `Tooltip_Produto` (oculta, Descrição, 350 px) ligada ao gráfico da Faturação
- [ ] Parte 2 - `Ranking Vendas` (RANKX + ALL) e página Produtos
- [ ] Parte 3 - gradiente em Total Faturação; ícones em Variação Homóloga %
- [ ] Parte 4 - Word Cloud (AppSource) na página Produtos
- [ ] Publicado no Power BI Service
- [ ] Submetido no Moodle
