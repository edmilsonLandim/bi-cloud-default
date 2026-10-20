# OA4 - Lab Assíncrono: Modelo de Dados Relacional

- Abre: 13/10/2026 às 19:45 - data limite: 20/11/2026 às 23:59
- Ficheiro de entrega: `EdmilsonLandim_dd-mm-yyyy.pbix` (nome + data do dia)
- Dados: `dCategories.xlsx` - folha `DimCategories`, 8 categorias

## Enunciado
**Parte 1 - Modelo de dados.** *No ficheiro de Power BI criado hoje* (o do lab síncrono):
1. Importar a tabela das categorias (`dCategories.xlsx`).
2. Relacioná-la com a tabela de subcategorias.

**Parte 2 - Relatório.**
1. Nova página com o nome **Categories**.
2. **Gráfico de barras** com a distribuição de `SalesAmount` por categoria.
3. **Segmentação** (slicer) por `BrandName` da tabela `Products`.
4. Publicar no Power BI Service.
5. Submeter no Moodle.

Ponto de partida: abrir `lab-sincrono/OA4 - Lab Síncrono.pbix` e **Guardar como**
`EdmilsonLandim_dd-mm-yyyy.pbix` nesta pasta. O modelo do síncrono (Sales, Products,
SubCategories, Stores, Locations) tem de estar completo e relacionado.

## Perfil dos dados
| ID_ProductCategory | ProductCategoryName | Subcategorias | SalesAmount |
|---|---|---|---|
| 1 | Audio | 8 | 6 656 109,04 |
| 2 | TV and Video | 5 | 55 556 881,62 |
| 3 | Computers | 8 | 131 979 789,88 |
| 4 | Cameras and camcorders | 5 | 99 305 681,83 |
| 5 | Cell phones | 4 | 36 227 492,97 |
| 6 | Music, Movies and Audio Books | 3 | 6 249 888,02 |
| 7 | Games and Toys | 3 | **sem vendas** |
| 8 | Home Appliances | 8 | **sem vendas** |
| | **Total** | **44** | **335 975 843,35** |

Pontos de atenção:
- A chave tem **nomes diferentes** nas duas tabelas: `ID_ProductCategory` em
  `dCategories` e `ProductCategoryKey` em `SubCategories`. Na relação conta o
  **conteúdo e o tipo**, não o nome. No modelo do formador a coluna aparece como
  `ProductCategoryKey`: renomear para ficar coerente.
- As categorias 7 e 8 têm subcategorias e produtos, mas nenhuma venda em `Sales`. No
  gráfico de barras só aparecem 6 barras. Para as mostrar com valor vazio: no campo da
  categoria, **Mostrar itens sem dados**.

## Parte 1 - Modelo de dados
1. **Livro do Excel** -> `dCategories.xlsx` -> folha `DimCategories` -> **Transformar Dados**.
2. Power Query (consulta `Categories`):
   - apagar o passo `Tipo alterado` automático
   - renomear `ID_ProductCategory` -> `ProductCategoryKey` e `ProductCategoryName` ->
     `Category` (como no modelo do formador)
   - `ProductCategoryKey` -> **Texto** (igual a `SubCategories[ProductCategoryKey]`, que
     no síncrono ficou Texto); `Category` -> Texto
   - **Fechar e Aplicar**
3. **Vista de Modelo**: arrastar `Categories[ProductCategoryKey]` para
   `SubCategories[ProductCategoryKey]` -> **Um para muitos (1:\*)**, direção **Única**.
   Se o Power BI não deixar criar, os tipos não coincidem (número vs texto).
4. **Ocultar** `SubCategories[ProductCategoryKey]` (lado "muitos").

Modelo final (floco de neve completo, igual ao PDF do formador):
`Locations -> Stores -> Sales <- Products <- SubCategories <- Categories`.

```m
let
    Origem = Excel.Workbook(File.Contents("...\lab-assincrono\dCategories.xlsx"), null, true),
    DimCategories = Origem{[Item = "DimCategories", Kind = "Sheet"]}[Data],
    #"Cabeçalhos promovidos" = Table.PromoteHeaders(DimCategories, [PromoteAllScalars = true]),
    #"Colunas com nome mudado" = Table.RenameColumns(#"Cabeçalhos promovidos", {{"ID_ProductCategory", "ProductCategoryKey"}, {"ProductCategoryName", "Category"}}),
    #"Tipo alterado" = Table.TransformColumnTypes(#"Colunas com nome mudado", {{"ProductCategoryKey", type text}, {"Category", type text}})
in
    #"Tipo alterado"
```

### Problema encontrado e resolvido: tudo em "(Vazio)"
Sintoma: o gráfico mostrava uma só barra **(Vazio)** com os 336 M. A relação existia, mas
nenhuma chave coincidia. Causa: no lab síncrono, a consulta `SubCategories` tinha ficado
**sem `ProductSubcategoryKey`** (só 2 colunas) e a coluna chamada `ProductCategoryKey` não
continha as chaves das categorias. Correção: refazer a consulta com as 3 colunas
(`ProductSubcategoryKey`, `ProductSubcategoryName`, `ProductCategoryKey`, todas Texto) -
código em [`../lab-sincrono/power-query-subcategories.m`](../lab-sincrono/power-query-subcategories.m) -
e confirmar as relações `SubCategories[ProductSubcategoryKey]` -> `Products` e
`Categories` -> `SubCategories[ProductCategoryKey]`.

Lição: numa dimensão, a chave do lado 1 tem de ser **única** (Ver -> Distribuição de
colunas: "44 distintos, 44 únicos"). Testar cada relação com um visual simples logo
depois de a criar.

## Parte 2 - Relatório
1. Botão **+** no fundo -> nova página -> duplo clique -> **Categories**.
2. **Gráfico de barras agrupadas**: Eixo Y `Categories[Category]`; Eixo X Soma de
   `Sales[SalesAmount]`; ordenar decrescente; rótulos de dados em **Milhões**.

   | Category | SalesAmount |
   |---|---|
   | Computers | 131,98 M |
   | Cameras and camcorders | 99,31 M |
   | TV and Video | 55,56 M |
   | Cell phones | 36,23 M |
   | Audio | 6,66 M |
   | Music, Movies and Audio Books | 6,25 M |

   Se todas as barras mostrarem **335,98 M**, a relação Categories -> SubCategories
   falta ou os tipos das chaves são diferentes.
3. **Segmentação de dados** com `Products[BrandName]` (10 marcas). Teste: escolher
   **Contoso** -> Computers 16,36 M / TV and Video 15,23 M / Cameras and camcorders
   12,69 M / Cell phones 9,77 M / Music, Movies and Audio Books 3,07 M / Audio 2,89 M.
   Outras marcas vendem só 1 ou 2 categorias (ex.: Proseware, A. Datum, Litware).
4. **Publicar** -> "A minha área de trabalho".
5. Submeter o `.pbix` no Moodle.

## Dashboard da página Categories (identidade Skodji Digital)
Ficheiros em [`dashboard/`](dashboard/): `fundo-categories.png`, `mockup-categories.png`
e `tema-skodji.json` (o mesmo do OA3, com a 3.ª cor amarela). Na página **Categories**:
**Ver -> Temas -> Procurar temas**; **Formatar página -> Fundo da tela -> Imagem**,
Ajuste **Ajustar**, Transparência **0%**; em cada visual desligar **Título** e **Fundo**.

| Visual | Campos | X | Y | Largura | Altura | Valor esperado |
|---|---|---|---|---|---|---|
| Cartão - Vendas | Soma de `Sales[SalesAmount]` (Milhões, 2 casas) | 38 | 122 | 270 | 50 | 335,98 M |
| Cartão - Custo total | Soma de `Sales[TotalCost]` | 350 | 122 | 270 | 50 | 92,24 M |
| Cartão - Categorias | Contagem de `Categories[Category]` | 662 | 122 | 270 | 50 | 8 |
| Cartão - Marcas | Contagem (Distinta) de `Products[BrandName]` | 974 | 122 | 270 | 50 | 10 |
| **Barras - SalesAmount por categoria** (pedido) | Eixo Y `Categories[Category]`; Eixo X Soma de `SalesAmount`; ordenar decrescente; rótulos de dados | 34 | 242 | 756 | 444 | 6 barras, Computers 131,98 M |
| **Segmentação - BrandName** (pedido) | `Products[BrandName]`; estilo **Lista vertical**; pesquisa ligada (`...` -> Pesquisar) | 826 | 242 | 420 | 160 | 10 marcas |
| Barras - Top 5 subcategorias | Eixo Y `SubCategories[ProductSubcategoryName]`; Eixo X Soma de `SalesAmount`; filtro do visual **N Principais = 5** por SalesAmount | 826 | 478 | 420 | 208 | Camcorders 49,27 M ... Home Theater System 28,40 M |

Notas:
- A segmentação e os cartões filtram-se uns aos outros: ao escolher **Contoso**, o
  cartão Vendas passa a **60,02 M** e as barras mostram Computers 16,36 M no topo.
  O cartão Categorias fica sempre 8 (a tabela `Categories` não é filtrada pelas marcas,
  porque o filtro só desce das dimensões para os factos).
- O texto "Games and Toys e Home Appliances não têm vendas" só existe no mockup, como
  explicação. Pode acrescentá-lo com uma **Caixa de texto**.

## Evidências
Guardar em [`evidencias/`](evidencias/):
- `01-modelo.png` - Vista de Modelo com as 6 tabelas e as relações
- `02-pagina-categories.png` - página Categories com o gráfico e a segmentação
- `03-publicar-sucesso.png` - publicação no Power BI Service
- `04-submissao-moodle.png` - submissão no Moodle

## Estado
- [ ] Parte 1 - `Categories` importada e relacionada com `SubCategories`
- [ ] Parte 2 - página Categories, gráfico de barras e segmentação por BrandName
- [ ] Publicado no Power BI Service
- [ ] Submetido no Moodle
