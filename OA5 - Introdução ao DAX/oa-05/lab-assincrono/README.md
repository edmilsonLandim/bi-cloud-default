# OA5 - Lab Assíncrono: Modelação e Análise Temporal no Power BI

- Data limite: 20/11/2026 às 23:59
- Ficheiro de entrega: **`EdmilsonLandim-dd-mm-yyyy.pbix`** - atenção: neste enunciado o
  separador é **hífen** (`NomeApelido-dd-mm-yyyy`), não underscore como nos OA anteriores
- Contexto: a empresa **LusaTech** quer analisar as vendas por ano, trimestre e mês e
  perceber as margens de lucro

## Perfil dos dados (Google Sheet pública)
URL (ligação **Web**, sem login):
`https://docs.google.com/spreadsheets/d/1Xqjoskhl9tcghJZVNbfimLmvSu4HogFuyAw9O3oOP5M/export?format=csv`

CSV em UTF-8, separador **vírgula**, 50 vendas, 5 colunas:
`Data da Venda`, `ID Produto`, `Quantidade Vendida`, `Custo Unitário (€)`, `Preço Unitário (€)`.

| Produto | Custo unitário | Preço unitário | Vendas | Faturação |
|---|---|---|---|---|
| P001 | 10 € | 25 € | 12 | 3.275 € |
| P002 | 50 € | 120 € | 9 | 3.240 € |
| P003 | 5 € | 15 € | 11 | 3.135 € |
| P004 | 20 € | 45 € | 10 | 3.150 € |
| P005 | 100 € | 250 € | 8 | 3.250 € |

- Datas de **10/01/2025 a 03/05/2026**, em formato **dd/mm/aaaa**.
- **Armadilha da região:** 21 das 50 datas têm dia ≤ 12. Com o modelo em inglês (EUA),
  `10/01/2025` passa a 1 de outubro e as datas com dia > 12 dão **erro**. Usar **Alterar
  tipo -> Utilizando a Região -> Data / Português (Portugal)**. Conferir: a primeira
  linha tem de ser **10/01/2025** e não pode haver erros na coluna.

Totais para conferir: **Faturação 16.050 €**, **Custo 6.405 €**, **Margem 9.645 €**,
**450 unidades**.

## Parte 1 - Relatório e importação
1. Novo ficheiro -> **Guardar como** `EdmilsonLandim-dd-mm-yyyy.pbix` nesta pasta.
2. **Obter dados -> Web** -> colar o URL (Básico) -> **OK** -> Anónimo -> **Transformar Dados**.
3. Power Query:
   - renomear a consulta para **`Vendas`**
   - apagar o passo `Tipo alterado` automático; confirmar `Cabeçalhos promovidos`
   - `Data da Venda` -> **Data** com região **Português (Portugal)**
   - `ID Produto` -> Texto; `Quantidade Vendida` -> Número inteiro;
     `Custo Unitário (€)` e `Preço Unitário (€)` -> **Número decimal fixo**
   - **Fechar e Aplicar**

```m
let
    Origem = Csv.Document(Web.Contents("https://docs.google.com/spreadsheets/d/1Xqjoskhl9tcghJZVNbfimLmvSu4HogFuyAw9O3oOP5M/export?format=csv"), [Delimiter = ",", Columns = 5, Encoding = 65001, QuoteStyle = QuoteStyle.None]),
    #"Cabeçalhos promovidos" = Table.PromoteHeaders(Origem, [PromoteAllScalars = true]),
    #"Tipo com região" = Table.TransformColumnTypes(#"Cabeçalhos promovidos", {{"Data da Venda", type date}}, "pt-PT"),
    #"Tipo alterado" = Table.TransformColumnTypes(#"Tipo com região", {{"ID Produto", type text}, {"Quantidade Vendida", Int64.Type}, {"Custo Unitário (€)", Currency.Type}, {"Preço Unitário (€)", Currency.Type}})
in
    #"Tipo alterado"
```

## Parte 2 - Tabela de datas (de raiz)
1. Desligar as hierarquias automáticas: **Ficheiro -> Opções e definições -> Opções ->
   Ficheiro atual -> Carregamento de dados** -> desmarcar **Data/hora automática**.
2. Vista de Tabela -> **Nova tabela**:

   ```dax
   Calendario =
   // De 1 de janeiro do ano passado a 31 de dezembro do ano atual (dinâmico)
   CALENDAR (
       DATE ( YEAR ( TODAY () ) - 1, 1, 1 ),
       DATE ( YEAR ( TODAY () ), 12, 31 )
   )
   ```

   Em 2026 gera **01/01/2025 a 31/12/2026 = 730 dias**, e cobre todas as vendas
   (10/01/2025 a 03/05/2026).
3. Coluna `Date` -> tipo **Data** (só data); formato à escolha (ex.: `dd/mm/aaaa`).
4. **Ferramentas de tabela -> Marcar como tabela de datas** -> coluna `Date`.

## Parte 3 - Colunas calculadas em `Calendario`
```dax
Ano = YEAR ( Calendario[Date] )
```
```dax
Mês Num = MONTH ( Calendario[Date] )
```
```dax
Mês Nome =
// "jan" em pt-PT -> "Jan" (1.ª letra maiúscula, 3 letras)
VAR m = FORMAT ( Calendario[Date], "MMM", "pt-PT" )
RETURN UPPER ( LEFT ( m, 1 ) ) & MID ( m, 2, 2 )
```
```dax
Trimestre = "T" & QUARTER ( Calendario[Date] )
```

5. Selecionar `Mês Nome` -> **Ferramentas de coluna -> Ordenar por coluna -> Mês Num**.
   (Opcional: ocultar `Mês Num`.)

Conferir: 01/01/2025 -> Ano 2025, Mês Num 1, Mês Nome **Jan**, Trimestre **T1**;
15/08/2026 -> 2026, 8, **Ago**, **T3**.

## Parte 4 - Colunas calculadas em `Vendas`
```dax
Custo Total = Vendas[Quantidade Vendida] * Vendas[Custo Unitário (€)]
```
```dax
Faturação Total = Vendas[Quantidade Vendida] * Vendas[Preço Unitário (€)]
```
```dax
Margem de Lucro = Vendas[Faturação Total] - Vendas[Custo Total]
```

Totais: Custo Total **6.405 €**, Faturação Total **16.050 €**, Margem de Lucro **9.645 €**.

## Parte 5 - Relação e teste
1. Vista de Modelo: `Calendario[Date]` (1) -> `Vendas[Data da Venda]` (\*), direção
   **Única**. Os dois lados têm de ser **Data**; se o Power BI disser que os tipos são
   diferentes, a `Data da Venda` ficou texto no Power Query.
2. Ocultar `Vendas[Data da Venda]` (lado "muitos"): as datas passam a vir do calendário.
3. Gráfico de **colunas agrupadas**: Eixo X `Calendario[Ano]` e `Calendario[Trimestre]`;
   Eixo Y Soma de `Faturação Total` -> **Expandir tudo um nível abaixo na hierarquia**.
4. Ordenar pela dimensão temporal: `...` -> **Ordenar eixo -> Ano Trimestre** ->
   **Ordenação ascendente**.
5. Renomear a página para **Faturação**.

Resultado esperado (6 colunas; 2026 T3 e T4 existem no calendário mas não têm vendas,
por isso não aparecem):

| Ano | T1 | T2 | T3 | T4 |
|---|---|---|---|---|
| 2025 | 2.565 € | 3.560 € | 2.955 € | 3.375 € |
| 2026 | 2.490 € | 1.105 € | - | - |

Se aparecer **uma só coluna com 16.050 €** ou colunas iguais, a relação falta ou os
tipos não coincidem (ver "Gráfico vazio" nos conceitos da aula).

## Dashboard da página Faturação (identidade Skodji Digital)
Ficheiros em [`dashboard/`](dashboard/): `fundo-faturacao.png`,
`mockup-faturacao.png` e `tema-skodji.json`. Fundo **Ajustar**, transparência 0%;
visuais sem título nem fundo.

| Visual | Campos | X | Y | Largura | Altura | Valor esperado |
|---|---|---|---|---|---|---|
| Cartão - Faturação total | Soma de `Faturação Total` (0 casas, €) | 38 | 122 | 270 | 50 | 16.050 € |
| Cartão - Custo total | Soma de `Custo Total` | 350 | 122 | 270 | 50 | 6.405 € |
| Cartão - Margem de lucro | Soma de `Margem de Lucro` | 662 | 122 | 270 | 50 | 9.645 € |
| Cartão - Quantidade | Soma de `Quantidade Vendida` | 974 | 122 | 270 | 50 | 450 |
| **Colunas - Faturação por Ano e Trimestre** (pedido) | Eixo X `Ano`, `Trimestre`; Eixo Y Soma de `Faturação Total` | 34 | 242 | 756 | 444 | 6 colunas (tabela acima) |
| Barras - Faturação por produto | Eixo Y `ID Produto`; Eixo X Soma de `Faturação Total` | 826 | 242 | 420 | 160 | P001 3.275 € ... P003 3.135 € |
| Colunas - Margem por mês | Eixo X `Mês Nome`; Eixo Y Soma de `Margem de Lucro` | 826 | 478 | 420 | 208 | Jan 1.160 € ... Dez 900 €, de Jan a Dez |

Cores do gráfico principal como no mockup (2025 azul, 2026 ciano): nova coluna em
`Calendario` -> `Cor Ano = IF ( MOD ( Calendario[Ano], 2 ) = 1, "#1E55A2", "#32B2E7" )`;
no gráfico **Formatar visual -> Colunas -> Cor -> fx** -> **Valor do campo** ->
`Calendario[Cor Ano]` -> resumo **Primeiro**. Ocultar `Cor Ano`.

O último gráfico prova a Parte 3.5: sem **Ordenar por coluna**, os meses aparecem por
ordem alfabética (Abr, Ago, Dez, Fev...).

## Evidências
Guardar em [`evidencias/`](evidencias/):
- `01-power-query.png` - consulta `Vendas` com a data em tipo Data (região pt-PT)
- `02-calendario.png` - tabela `Calendario` com Ano, Mês Num, Mês Nome, Trimestre
- `03-modelo.png` - relação Calendario -> Vendas
- `04-faturacao.png` - página Faturação
- `05-publicar-sucesso.png` / `06-submissao-moodle.png` (se o Moodle pedir publicação)

## Estado
- [ ] Parte 1 - importação Web e tabela `Vendas`
- [ ] Parte 2 - `Calendario` em DAX, marcada como tabela de datas
- [ ] Parte 3 - Ano, Mês Num, Mês Nome (ordenado), Trimestre
- [ ] Parte 4 - Custo Total, Faturação Total, Margem de Lucro
- [ ] Parte 5 - relação e página Faturação
- [ ] Submetido no Moodle
