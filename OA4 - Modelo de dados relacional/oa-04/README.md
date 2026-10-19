# OA4 - Criar um modelo de dados relacional. Outras boas práticas

## Calendário
| Atividade | Abre | Fecha |
|---|---|---|
| Lab assíncrono | 13/10/2026 19:45 | 20/11/2026 23:59 |
| Pós-teste | - | 20/11/2026 23:59 |

## Conceitos da aula
Resumo dos materiais de estudo na pasta do OA (`The_Power_BI_Data_Blueprint.pdf`,
15 diapositivos; infográfico `Modelação_de_Dados_Relacional_Eficiente.png`; e o modelo
final do formador `2026-07-08 15_57_16-Modelo 06-07-2026.pdf`):

| Conceito | Regra prática |
|---|---|
| **Mega tabela vs. modelo relacional** | Repetir nome de produto, loja e continente em 65 798 linhas é redundante, lento e difícil de escalar. Separar **eventos (factos)** de **descritores (dimensões)** e relacionar em vez de duplicar |
| **Factos (`f`)** | Tabela **longa e estreita**: muitas linhas, poucas colunas; chaves estrangeiras + métricas (`SalesAmount` = 335 M) |
| **Dimensões (`d`)** | Tabela **curta e larga**: poucas linhas, colunas descritivas; uma linha por código único |
| **Fluxo do arquiteto** | 1) Ingestão e limpeza (Power Query) -> 2) Modelação relacional -> 3) Enriquecimento semântico -> 4) Fundação visual. Um bom dashboard depende das fases 1 a 3 |
| **Fontes heterogéneas** | Excel, XML e TXT harmonizados no Power Query. No XML, usar o botão **Expandir** no cabeçalho em vez de clicar no link `Table` (que gera passos redundantes) e desmarcar *Utilizar o nome da coluna original como prefixo* |
| **Leis de ouro do Power Query** | **Eficiência**: apagar o passo automático `Tipo alterado`. **Exatidão**: tipos explícitos, valores financeiros como **Número decimal fixo** (Moeda). **Prevenção**: remover cedo as colunas inúteis; usar **Distribuição de colunas** para confirmar que as chaves primárias são 100% únicas |
| **Região (locale)** | Fonte com ponto decimal (`7.59`) num Windows em português dá erro ou valores errados. Botão direito -> **Alterar tipo -> Utilizando a Região** -> Número decimal fixo / **Inglês (Estados Unidos)** |
| **Bisturi vs. lógica** | **Substituir Valores** para erros exatos e isolados (`the Netherlands` -> `Netherlands`, com célula inteira: substituir `the ` às cegas estraga palavras, ex. "Nerlands"). **Coluna Condicional** para correções que dependem de outra coluna (`Country = Australia` -> `Continent = Oceania`) |
| **Relação 1 para muitos (1:\*)** | Chave **primária** sem duplicados no lado 1 (dimensão), chave **estrangeira** repetida no lado \* (factos). **O tipo de dados tem de ser idêntico dos dois lados (Texto -> Texto)**; o nome do campo não importa |
| **Direção do filtro** | **Única (Single)**: a seta vai da dimensão para os factos. Os filtros fluem das extremidades descritivas para o centro financeiro |
| **Floco de neve (snowflake)** | `Locations -> Stores -> Sales <- Products <- SubCategories <- Categories` |
| **Enriquecimento semântico** | Nomes que façam sentido para quem lê o relatório (`EnglishProductName` -> `Product Name`, `RegionCountryName` -> `Country`). **Ocultar as chaves no lado "muitos"** para obrigar a filtrar pela dimensão |
| **Categoria de dados** | `Continent` e `Country` -> **Ferramentas de coluna -> Categoria de dados -> Continente / País**. Sem isto, "Denmark" pode cair num condado da Austrália. Usar o visual **Azure Maps** (o "Map" antigo, Bing, está obsoleto) |
| **Grupos de dados** | Botão direito em `Country` -> **Novo grupo** -> Ctrl + clique (ex.: France, Germany -> `European Union`) -> marcar **Incluir outro grupo** -> segmentação por bloco, sem DAX |
| **Tema e formatação** | Aplicar o **tema JSON antes** de construir os visuais (mudar no fim estraga tamanhos e cores). Formatar na **coluna** (ex.: `SalesAmount` Moeda, 2 casas), nunca visual a visual |

Checklist do arquiteto: passo `Tipo alterado` removido? Chaves como **Texto** dos dois
lados? Setas das dimensões (1) para os factos (\*)? Chaves do lado "muitos" ocultas?
Campos financeiros e geográficos pré-formatados (Moeda, Categoria de dados)?

## Lab síncrono
Ficheiros do formador em `lab-sincrono/OA4 - Lab Síncrono-20261019/` (fora do Git).
Guardar o `.pbix` como `OA4 - Lab Síncrono.pbix` em `lab-sincrono/`.

### Fontes (perfil verificado)
| Ficheiro | Formato | Tabela no modelo | Linhas | Chave | Observações |
|---|---|---|---|---|---|
| `fSales.xlsx` (folha `fSales`) | Excel | `Sales` (factos) | 65 798 | - | datas 2021 a 2025; `SalesKey` **não é única** (32 233 repetidas, 3 699 linhas totalmente iguais) |
| `dProducts.xml` | XML | `Products` | 1 692 | `ProductKey` | valores com **ponto decimal** (`7.59`); 10 marcas (`BrandName`) |
| `dSubCategories.txt` | Texto, separador `;`, com aspas | `SubCategories` | 44 | `ProductSubcategoryKey` | `ProductSubcategoryDescription` = `Name` (redundante); chaves de 1 a 48 com falhas |
| `dStores+dLocations.xlsx` - `Folha1` | Excel | `Stores` | 306 | `StoreKey` | `CloseDate`/`CloseReason` com texto vazio em 294 lojas (só 12 fechadas) |
| `dStores+dLocations.xlsx` - `Folha2` | Excel | `Locations` | 671 | `GeographyKey` | 34 países; `the Netherlands`; **Australia em Asia** (47 localizações) |

Integridade: todas as `ProductKey`, `StoreKey`, `ProductSubcategoryKey` e
`GeographyKey` das tabelas do lado "muitos" existem na dimensão correspondente.

### Passos no Power Query
Em todas as consultas: **apagar o `Tipo alterado` automático** e definir os tipos no fim.

1. **Sales** (`fSales.xlsx`): remover `SalesKey` (não é chave nem métrica);
   `DateKey` -> Data; `StoreKey`, `ProductKey` -> **Texto**; `ReturnAmount`, `TotalCost`,
   `SalesAmount` -> **Número decimal fixo**.
2. **Products** (`dProducts.xml`): **Obter dados -> XML** -> no Navegador, `Products`
   -> **Transformar Dados** (se aparecer uma coluna `Table`, usar o botão **Expandir**,
   sem prefixo). Remover `ProductDescription` (texto longo, não usado) e
   `FinishedGoodsFlag`. Renomear `EnglishProductName` -> `Product Name`. `ProductKey`,
   `ProductSubcategoryKey` -> **Texto**; `UnitCost`, `UnitPrice` -> **Alterar tipo ->
   Utilizando a Região -> Número decimal fixo / Inglês (Estados Unidos)** (conferir:
   primeiro produto `UnitCost` 7,59 e `UnitPrice` 16,50).
3. **SubCategories** (`dSubCategories.txt`): **Obter dados -> Texto/CSV**, delimitador
   **Ponto e vírgula**. Remover `ProductSubcategoryLabel` e
   `ProductSubcategoryDescription`. `ProductSubcategoryKey`, `ProductCategoryKey` -> **Texto**.
4. **Stores** (`Folha1`): Substituir Valores `""` (vazio) -> `null` em `CloseDate` e
   `CloseReason`; `CloseDate`/`OpenDate` -> Data; `StoreKey`, `GeographyKey` -> **Texto**.
5. **Locations** (`Folha2`): renomear `ContinentName` -> `Continent`,
   `RegionCountryName` -> `Country`; **Substituir Valores** (célula inteira)
   `the Netherlands` -> `Netherlands`; Adicionar Coluna -> **Coluna Condicional**
   `Continent (corrigido)` = se `Country` = `Australia` então `Oceania` senão `Continent`
   (depois remover a original e renomear); `GeographyKey` -> **Texto**.
6. Renomear as consultas sem prefixo: `Sales`, `Products`, `SubCategories`, `Stores`,
   `Locations` (como no modelo do formador). **Fechar e Aplicar**.

### Vista de Modelo
| Dimensão (1) | Chave | Factos/dimensão (\*) | Direção |
|---|---|---|---|
| `Locations` | `GeographyKey` | `Stores[GeographyKey]` | Única |
| `Stores` | `StoreKey` | `Sales[StoreKey]` | Única |
| `Products` | `ProductKey` | `Sales[ProductKey]` | Única |
| `SubCategories` | `ProductSubcategoryKey` | `Products[ProductSubcategoryKey]` | Única |

Depois: **ocultar** as chaves do lado \* (`Sales[StoreKey]`, `Sales[ProductKey]`,
`Products[ProductSubcategoryKey]`, `Stores[GeographyKey]`); `Continent` e `Country` ->
Categoria de dados **Continente** / **País**; `SalesAmount`, `TotalCost`,
`ReturnAmount` -> formato **Moeda**, 2 casas.

### Valores para conferir
- `SalesAmount` total: **335 975 843,35**; `TotalCost` 92 241 161,52; `ReturnAmount` 2 252 865,34
- por ano: 2021 64,07 M / 2022 58,23 M / 2023 60,41 M / 2024 73,36 M / 2025 79,90 M
- por continente (com Austrália em Oceania): North America 195,88 M / Asia 74,47 M /
  Europe 61,92 M / Oceania 3,71 M. Sem a correção, Asia = 78,18 M
- por país (top 3): United States 189,51 M / China 46,84 M / Germany 26,24 M
- por marca (top 3): Fabrikam 72,73 M / Contoso 60,02 M / Adventure Works 45,54 M
- por subcategoria (top 3): Camcorders 49,27 M / Projectors & Screens 42,68 M / Laptops 42,06 M

Se um visual mostrar o **mesmo valor em todas as linhas** (ex.: 335,98 M em cada marca),
a relação falta ou tem a direção errada.

## Lab assíncrono
- Abre: 13/10/2026 às 19:45 - data limite: 20/11/2026 às 23:59
- Enunciado e guia: [`lab-assincrono/README.md`](lab-assincrono/README.md) - acrescentar
  `Categories` ao modelo do lab síncrono

## Estado
- [ ] Pré-teste
- [ ] Lab síncrono
- [ ] Lab assíncrono
- [x] Pós-teste - concluído
