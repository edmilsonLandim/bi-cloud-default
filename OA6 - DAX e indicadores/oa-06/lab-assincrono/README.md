# OA6 - Lab Assíncrono: Medidas DAX e Inteligência Temporal

- Abriu: 20/10/2026 às 19:45 - data limite: 20/11/2026 às 23:59
- Base: o exercício do OA5 (LusaTech). Usar o próprio:
  [`../../../OA5 - Introdução ao DAX/oa-05/lab-assincrono/EdmilsonLandim-02-11-2026.pbix`](../../../OA5%20-%20Introdução%20ao%20DAX/oa-05/lab-assincrono/EdmilsonLandim-02-11-2026.pbix)
  -> **Guardar como** `EdmilsonLandim-dd-mm-yyyy.pbix` **nesta pasta** (o ficheiro do OA5
  fica intacto). Alternativa do formador: `OA5-Exercicio resolvido.pbix` (mesmos nomes:
  `Vendas`, `Calendario`, `Faturação Total`...).
- Objetivo: trocar as medidas implícitas por **medidas explícitas**, analisar o **peso %**
  e a **variação homóloga** (ano atual vs. ano anterior)

## Parte 1 - Tabela `_Medidas`
1. **Base -> Introduzir Dados** -> nome **`_Medidas`** -> **Carregar** (o `_` põe-na no
   topo da lista).
2. Será o repositório de todas as medidas a seguir: para criar cada uma, selecionar
   `_Medidas` no painel Dados -> **Nova medida**.

## Parte 2 - Medidas base (explícitas)
Uma medida de cada vez (**Nova medida** -> colar -> Enter):

```dax
Total Faturação = SUM ( Vendas[Faturação Total] )
```
```dax
Total Custo = SUM ( Vendas[Custo Total] )
```
```dax
Total Margem = SUM ( Vendas[Margem de Lucro] )
```

Formato: **Ferramentas de medida -> Formato -> Moeda (€)**, 0 ou 2 casas decimais.

4. Apagar a coluna vazia: na tabela `_Medidas`, botão direito em **Coluna 1** -> **Eliminar
   do modelo**. O ícone da tabela passa a **calculadora** (às vezes só depois de guardar
   ou de recolher/expandir o painel Dados).

Conferir: Total Faturação **16.050 €**, Total Custo **6.405 €**, Total Margem **9.645 €**
(os mesmos totais das colunas calculadas do OA5).

## Parte 3 - Inteligência temporal (YoY)
```dax
Faturação Ano Anterior =
CALCULATE ( [Total Faturação], SAMEPERIODLASTYEAR ( Calendario[Date] ) )
```
```dax
Variação Homóloga % =
DIVIDE ( [Total Faturação] - [Faturação Ano Anterior], [Faturação Ano Anterior] )
```

3. `Variação Homóloga %` -> **Ferramentas de medida -> Formato -> Percentagem** (2 casas).

`SAMEPERIODLASTYEAR` usa `Calendario[Date]` (a tabela marcada como tabela de datas no OA5),
**nunca** `Vendas[Data da Venda]`.

## Parte 4 - % do total
```dax
% Faturação Total =
DIVIDE ( [Total Faturação], CALCULATE ( [Total Faturação], ALL ( Calendario ) ) )
```

2. Formato **Percentagem** (2 casas). O `ALL(Calendario)` faz com que o denominador seja
   sempre **16.050 €**, seja qual for a linha da matriz (ano, mês ou trimestre).

## Parte 5 - Matriz
1. Nova página -> visual **Matriz**.
2. **Linhas**: `Calendario[Ano]` e `Calendario[Mês Nome]` (o Mês Nome já está ordenado por
   Mês Num desde o OA5).
3. **Valores**, por esta ordem: `Total Faturação`, `Faturação Ano Anterior`,
   `Variação Homóloga %`, `% Faturação Total`.
4. Expandir: botão **Expandir tudo um nível abaixo** (seta dupla para baixo) no visual.
5. Renomear a página para **Matriz**.

### Resultado esperado
| Ano / Mês | Total Faturação | Faturação Ano Anterior | Variação Homóloga % | % Faturação Total |
|---|---|---|---|---|
| **2025** | **12.455 €** | | | **77,60%** |
| Jan ... Dez 2025 | 905 € ... 1.550 € | | | 5,64% ... 9,66% |
| **2026** | **3.595 €** | **12.455 €** | **-71,14%** | **22,40%** |
| Jan | 1.040 € | 905 € | **14,92%** | 6,48% |
| Fev | 585 € | 625 € | -6,40% | 3,64% |
| Mar | 865 € | 1.035 € | -16,43% | 5,39% |
| Abr | 730 € | 1.335 € | -45,32% | 4,55% |
| Mai | 375 € | 1.380 € | -72,83% | 2,34% |
| Jun ... Dez | | 845 € ... 1.550 € | **-100,00%** | |
| **Total** | **16.050 €** | **12.455 €** | **28,86%** | **100,00%** |

### Análise (Parte 5.4)
- **O "Ano Anterior" está certo:** em 2026 mostra **12.455 €**, que é exatamente a
  faturação de 2025; em cada mês de 2026 mostra o mesmo mês de 2025 (Jan 905 €, Fev 625 €...).
- **2025 não tem ano anterior:** o `Calendario` começa em 01/01/2025 e não há vendas de 2024,
  por isso `Faturação Ano Anterior` e `Variação Homóloga %` ficam vazias (o DIVIDE evita o
  erro de divisão por zero).
- **O -71,14% de 2026 engana:** compara 2026 até maio (os dados acabam em 03/05/2026) com o
  ano de 2025 completo. Comparando o mesmo período, Jan-Mai 2026 (3.595 €) vs. Jan-Mai 2025
  (5.280 €), a quebra real é de **-31,9%**. Mesmo assim é quebra: só janeiro cresceu
  (+14,92%) e a descida acentua-se de mês para mês até maio (-72,83%).
- **Jun-Dez 2026 a -100%:** esses meses existem no calendário mas ainda não têm vendas, e o
  ano anterior tem. Não é uma quebra real, é falta de dados.
- **Linha Total (28,86%):** compara o total geral (2025 + 2026) com 2025; não tem leitura
  de negócio.

Melhoria opcional (não pedida): esconder a variação quando ainda não há vendas.

```dax
Variação Homóloga % =
IF (
    ISBLANK ( [Total Faturação] ),
    BLANK (),
    DIVIDE ( [Total Faturação] - [Faturação Ano Anterior], [Faturação Ano Anterior] )
)
```

## Dashboard da página Matriz (identidade Skodji Digital)
Ficheiros em [`dashboard/`](dashboard/): `fundo-matriz.png`, `mockup-matriz.png`,
`tema-skodji.json`. Fundo **Ajustar**, transparência 0%; visuais sem título nem fundo.

| Visual | Campos | X | Y | Largura | Altura | Valor esperado |
|---|---|---|---|---|---|---|
| Cartão - Total Faturação | `[Total Faturação]` | 38 | 122 | 270 | 50 | 16.050 € |
| Cartão - Total Margem | `[Total Margem]` | 350 | 122 | 270 | 50 | 9.645 € |
| Cartão - Variação homóloga 2026 | `[Variação Homóloga %]` + filtro do visual `Ano` = 2026 | 662 | 122 | 270 | 50 | -71,1% |
| Cartão - % faturação 2026 | `[% Faturação Total]` + filtro do visual `Ano` = 2026 | 974 | 122 | 270 | 50 | 22,4% |
| **Matriz** (pedido) | Linhas `Ano`, `Mês Nome`; Valores as 4 medidas | 34 | 242 | 756 | 444 | tabela acima |
| Colunas - Faturação vs Ano Anterior | Eixo X `Mês Nome`; Eixo Y `[Total Faturação]` e `[Faturação Ano Anterior]`; filtro `Ano` = 2026 e `Mês Num` <= 5 | 826 | 242 | 420 | 160 | Jan 1.040 vs 905 ... Mai 375 vs 1.380 |
| Anel - % por ano | Legenda `Ano`; Valores `[Total Faturação]` | 826 | 478 | 420 | 208 | 2025 77,6% / 2026 22,4% |

Cores da variação (verde a subir, vermelho a descer): selecionar a Matriz -> **Formatar ->
Elementos da célula** -> série `Variação Homóloga %` -> **Cor do tipo de letra** -> **fx** ->
Estilo **Regras**: se o valor >= 0 -> `#2E9E5B`; se < 0 -> `#DF3131`.

## Evidências
Guardar em [`evidencias/`](evidencias/):
- `01-tabela-medidas.png` - painel Dados com `_Medidas` (ícone de calculadora) e as 6 medidas
- `02-matriz.png` - página Matriz
- `03-publicar-sucesso.png` / `04-submissao-moodle.png`

## Estado
- [x] Parte 1 - tabela `_Medidas` ([`EdmilsonLandim-02-11-2026 oa-06.pbix`](EdmilsonLandim-02-11-2026%20oa-06.pbix))
- [x] Parte 2 - Total Faturação (16.050 €), Total Custo, Total Margem (9.645 €); Coluna 1 eliminada
- [x] Parte 3 - Faturação Ano Anterior, Variação Homóloga % (2026: -71,14%)
- [x] Parte 4 - % Faturação Total (2025 77,60% / 2026 22,40%)
- [x] Parte 5 - página Matriz (cores por regra) e análise; publicado no Power BI Service
- [x] Submetido no Moodle (02/11/2026 16:57) - [`evidencias/04-submissao-moodle.png`](evidencias/04-submissao-moodle.png)
