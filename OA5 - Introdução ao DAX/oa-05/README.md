# OA5 - Introdução ao DAX e cálculos no Power BI

## Sumário
- Introdução ao DAX.
- Criar tabelas e colunas calculadas.
- Trabalhar com o editor DAX.
- A importância da tabela de datas.

## Calendário
| Atividade | Estado |
|---|---|
| Pré-teste | concluído |
| Lab síncrono | ver abaixo |
| Lab assíncrono | prazo 20/11/2026 23:59 |
| Pós-teste | concluído |

## Conceitos da aula
Resumo dos materiais de estudo na pasta do OA (`Power_BI_DAX_Blueprints (1).pdf`,
15 diapositivos, e o infográfico `Guia_de_DAX_e_Datas (1).png`):

| Conceito | Regra prática |
|---|---|
| **Ciclo de BI** | 1) ETL no Power Query -> **2) Modelação e cálculos DAX** (cálculo tabular, tabela de datas, relações) -> 3) Visualização -> 4) Distribuição. Este OA é a fase 2: a fundação lógica antes dos visuais |
| **Excel vs. DAX** | No Excel a unidade é a **célula** (`=A1+B1`), a função muda com o idioma (`=SE()`) e a fórmula arrasta-se. No DAX a unidade é a **coluna inteira**, as funções são sempre em **inglês** (`IF()`, `YEAR()`) e o cálculo propaga-se sozinho |
| **3 pilares do cálculo** | **Coluna calculada** (avaliação linha a linha, ocupa memória; uso: categorizar, extrair partes de datas). **Tabela calculada** (tabela física criada com código; uso: tabela de datas). **Medida** (cálculo virtual "on the fly", conforme os filtros; tema do próximo OA) |
| **Código limpo** | `Nome da Coluna =` antes da fórmula; `//` para comentários; `[` ou TAB para chamar colunas da mesma tabela (não escrever nomes à mão); **Shift + Enter** para mudar de linha |
| **Separador de argumentos** | Em DAX usa-se a **vírgula** `,`, não o ponto e vírgula `;` do Excel em português (erro de sintaxe com sublinhado vermelho) |
| **Exemplo: margem e ABC** | `GM_Product = [UnitPrice] - [UnitCost]`; `ABC = IF([GM_Product] < 100, "C", IF([GM_Product] < 500, "B", "A"))` |
| **Porquê uma tabela de datas** | 1) **Recursos**: sem ela o Power BI cria tabelas ocultas para cada coluna de data; 2) **personalização** (semana, semestre, feriados, ano fiscal); 3) **Time Intelligence** (YoY, YTD) exige datas contínuas, de 1 jan a 31 dez, sem dias em falta |
| **Motor do calendário** | `Calendar = CALENDAR(DATE(2021, 1, 1), DATE(YEAR(TODAY()) + 1, 12, 31))`: início fixo no ano do registo mais antigo, fim dinâmico que avança sozinho todos os anos |
| **Marcar como tabela de datas** | Selecionar a tabela -> **Marcar como tabela de datas** -> coluna `[Date]`. Acaba com as hierarquias "parasitas" penduradas nas colunas de data |
| **Enriquecer o calendário** | `YEAR([Date])` -> 2024; `"Q" & QUARTER([Date])` -> Q3; `MONTH([Date])` -> 8; `IF(MONTH([Date]) <= 6, "S1", "S2")` -> S2 |
| **FORMAT e idioma** | `FORMAT([Date], "MMM")` Jan; `"MMMM"` Janeiro; `"DDD"` Seg. Sem o 3.º argumento usa o idioma do sistema; com `"pt-PT"` força o português (`FORMAT([Date], "MMMM", "pt-PT")` -> agosto) |
| **Ordenação indireta** | Texto ordena-se por ordem alfabética (Abr, Ago, Dez...). Selecionar a coluna do nome do mês -> **Ordenar por coluna** -> coluna numérica do mês (que pode ficar oculta) |
| **Gráfico vazio** | Sintoma: gráfico em branco ou barras iguais. Causa: falta a relação ou os **tipos são diferentes** (`Calendar[Date]` Data vs `Sales[DateKey]` Texto). O formato visual (DD/MM ou MM/DD) não interessa, o tipo sim |
| **Interações entre visuais** | Por defeito a segmentação filtra tudo. Selecionar a segmentação -> **Formatar -> Editar interações** -> ícone **Nenhum** no visual que deve ficar isolado |

5 leis da sessão: pensar em colunas, não em células; editor DAX limpo (Shift+Enter,
`[`, `//`); impor o calendário e marcá-lo como tabela de datas; chaves com o mesmo tipo
de dados; ordenar textos por colunas numéricas ocultas.

## Lab síncrono
Ficheiro do formador: [`lab-sincrono/Modelo 13-10-2026.pbix`](lab-sincrono/) - o
modelo do OA4 (Sales, Products, SubCategories, Categories, Stores, Locations) com 2
páginas já feitas: página 1 com cartão (SalesAmount), tabela (produto x vendas),
treemap (BrandName) e barras (Subcategory); página 2 com Azure Map (Country).
Abrir e **Guardar como** `OA5 - Lab Síncrono.pbix` (o original fica intacto).

### 1. Desligar a data/hora automática
**Ficheiro -> Opções e definições -> Opções -> Ficheiro atual -> Carregamento de
dados** -> desmarcar **Data/hora automática**. As hierarquias automáticas desaparecem
das colunas de data.

### 2. Colunas calculadas em Products
Vista de Tabela -> `Products` -> **Nova coluna**:

```dax
GM_Product =
// Margem bruta por unidade
Products[UnitPrice] - Products[UnitCost]
```

```dax
ABC =
// Classificação pela margem bruta
IF (
    Products[GM_Product] < 100, "C",
    IF ( Products[GM_Product] < 500, "B", "A" )
)
```

Conferir (1 692 produtos): **A 54** / **B 830** / **C 808**. GM_Product vai de
-959,82 a 668,01: **70 produtos têm margem negativa** (preço abaixo do custo) e caem na
classe C.

### 3. Tabela de datas
Vista de Tabela -> **Nova tabela**:

```dax
Calendar =
CALENDAR ( DATE ( 2021, 1, 1 ), DATE ( YEAR ( TODAY () ) + 1, 12, 31 ) )
```

Em 2026 dá 01/01/2021 a 31/12/2027 = **2 556 dias** (as vendas vão de 2021 a 2025).
`[Date]` -> tipo **Data**. Depois, **Ferramentas de tabela -> Marcar como tabela de
datas** -> `Date`.

Colunas calculadas em `Calendar` - **uma fórmula de cada vez**: Ferramentas de tabela ->
**Nova coluna** -> colar uma só linha -> Enter; repetir 5 vezes (colar várias linhas na
mesma barra dá "A sintaxe está incorreta"):

```dax
Year = YEAR ( Calendar[Date] )
```
```dax
Month Num = MONTH ( Calendar[Date] )
```
```dax
Month Name = FORMAT ( Calendar[Date], "MMM", "pt-PT" )
```
```dax
Quarter = "T" & QUARTER ( Calendar[Date] )
```
```dax
Semester = IF ( MONTH ( Calendar[Date] ) <= 6, "S1", "S2" )
```

`Month Name` -> **Ordenar por coluna** -> `Month Num`; ocultar `Month Num`.

Se o editor sublinhar `Calendar[...]` a vermelho (o nome coincide com a função
`CALENDAR`), escrever a tabela entre plicas: `'Calendar'[Date]`.

### 4. Relação
Vista de Modelo: `Calendar[Date]` (1) -> `Sales[DateKey]` (\*), direção **Única**.
Os dois lados têm de ser **Data** (no OA4 `DateKey` ficou Data). Ocultar
`Sales[DateKey]`.

### 5. Testar
Gráfico de colunas: Eixo X `Calendar[Year]` + `Calendar[Quarter]`, Eixo Y Soma de
`SalesAmount` -> **Expandir tudo um nível abaixo**. Valores (M):

| Ano | T1 | T2 | T3 | T4 | Total |
|---|---|---|---|---|---|
| 2021 | 12,50 | 17,44 | 15,86 | 18,26 | 64,07 |
| 2022 | 12,35 | 14,63 | 14,77 | 16,48 | 58,23 |
| 2023 | 13,38 | 15,81 | 15,47 | 15,75 | 60,41 |
| 2024 | 16,01 | 19,10 | 18,61 | 19,63 | 73,36 |
| 2025 | 16,33 | 20,63 | 21,16 | 21,79 | 79,90 |

SalesAmount por classe ABC: B 216,36 M / C 93,76 M / A 25,86 M.

### Dashboard (identidade Skodji Digital)
Ficheiros em [`lab-sincrono/dashboard/`](lab-sincrono/dashboard/):
`fundo-calendar-abc.png`, `mockup-calendar-abc.png`, `tema-skodji.json`. Nova página
com o fundo (**Ajustar**, transparência 0%), visuais sem título nem fundo:

| Visual | Campos | X | Y | Largura | Altura | Valor esperado |
|---|---|---|---|---|---|---|
| Cartão - Vendas | Soma de `Sales[SalesAmount]` | 38 | 122 | 270 | 50 | 335,98 M |
| Cartão - Dias no calendário | Contagem de `Calendar[Date]` | 350 | 122 | 270 | 50 | 2.556 |
| Cartão - Produtos classe A | Contagem de `Products[ProductKey]` + filtro `ABC` = A | 662 | 122 | 270 | 50 | 54 |
| Cartão - Margem < 0 | Contagem de `Products[ProductKey]` + filtro `GM_Product` é menor que 0 | 974 | 122 | 270 | 50 | 70 |
| Colunas - por ano e trimestre | Eixo X `Year`, `Quarter` (expandido); Eixo Y Soma de `SalesAmount` | 34 | 242 | 756 | 444 | 20 colunas, 2021 T1 a 2025 T4 |
| Anel - produtos por classe | Legenda `ABC`; Valores Contagem de `ProductKey` | 826 | 242 | 420 | 160 | A 3,2% / B 49,1% / C 47,8% |
| Barras - vendas por classe | Eixo Y `ABC`; Eixo X Soma de `SalesAmount` | 826 | 478 | 420 | 208 | B 216,36 M |

Cores alternadas por ano (como no mockup): nova coluna em `Calendar`

```dax
Cor Ano =
// Anos ímpares azul, anos pares ciano (2021 azul, 2022 ciano, ...)
IF ( MOD ( Calendar[Year], 2 ) = 1, "#1E55A2", "#32B2E7" )
```

Gráfico -> **Formatar visual -> Colunas -> Cor -> fx** -> Estilo de formato **Valor do
campo**, campo `Calendar[Cor Ano]`, resumo **Primeiro** -> OK. Só funciona sem campo em
**Legenda** e com uma única medida no Eixo Y. Ocultar `Cor Ano` na vista de relatório.

## Lab assíncrono
Enunciado e guia: [`lab-assincrono/README.md`](lab-assincrono/README.md) - LusaTech:
dados da web (Google Sheet), tabela `Calendario` em DAX, colunas calculadas e gráfico
de Faturação por ano e trimestre.

## Estado
- [x] Pré-teste - concluído
- [x] Lab síncrono - `OA5 - Lab Síncrono.pbix` (Calendar, GM_Product, ABC, cores por ano),
  publicado; evidências em [`lab-sincrono/evidencias/`](lab-sincrono/evidencias/)
- [ ] Lab assíncrono
- [x] Pós-teste - concluído
