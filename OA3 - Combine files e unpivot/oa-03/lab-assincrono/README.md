# OA3 - Lab Assíncrono: Unpivot

- Abre: 08/10/2026 às 19:45 - data limite: 20/11/2026 às 23:59
- Ficheiro de entrega: `EdmilsonLandim_dd-mm-yyyy.pbix` (nome + data do dia)
- Dados: `Mapa contabilistico.xlsx` - folha `Mapa Contabilistico 2025` (sem tabela
  Excel): balancete com **99 contas SNC** nas linhas e os **12 meses de 2025** nas
  colunas (tabela cruzada)

## Enunciado
1. Novo ficheiro `NomeApelido_dd-mm-yyyy.pbix`; importar `Mapa contabilistico.xlsx`.
2. Power Query: **Unpivot**, limpando antes colunas e linhas vazias; outras
   transformações necessárias; **tipos de dados**.
3. Relatório: **cartão** com o total do campo valor; **gráfico de linhas** com a
   evolução ao longo do ano; **segmentação** (slicer) por **designação**; publicar no
   Power BI Service; submeter no Moodle.

## Perfil dos dados (para conferir)
Estrutura da folha (intervalo usado `B2:P102`):

| Linha / coluna | Conteúdo |
|---|---|
| Coluna A | **vazia** |
| Linha 1 | **vazia** |
| Linha 2 | cabeçalhos: `Conta SNC`, `Designação SNC`, *(coluna D sem nome)*, `jan` ... `dez` |
| Coluna D | **vazia** (separador entre a designação e os meses) |
| Linha 3 | **vazia** |
| Linhas 4 a 102 | 99 contas |

Outros pontos encontrados:
- 1 188 células de valor (99 x 12): **123 vazias** (contas sem movimento nesse mês) e
  47 com `0`.
- `Conta SNC` é texto no Excel (`'11`, `'27819012`) e deve continuar **Texto**: é um
  código, não um número para somar.
- **Contas repetidas**: `221` (2 designações), `438` (5), `7816` (2).
- **Designações repetidas** em contas diferentes: `Outros` (6888 gastos e 7888
  rendimentos), `Perdas por imparidade acumuladas` (219 e 339), os ativos fixos em
  43x e 438. Na segmentação por designação estas aparecem juntas.
- Grafia inconsistente: `adiantamentos de clientes` e `reservas legais` em minúsculas,
  `MATERIAS PRIMAS SUB. DE CONSUMO` em maiúsculas, `Rendimentos a reconhceer`.
- Os saldos são **acumulados** (ex.: Vendas, conta 71, passa de -45 630 em janeiro para
  -4 984 251 em dezembro). Somar os 12 meses é o que o enunciado pede para o cartão,
  mas, numa análise real, o valor do ano é o de dezembro, não a soma.

## Parte 1 - Criação do relatório e importação
1. **Ficheiro -> Novo** -> **Guardar como** `EdmilsonLandim_dd-mm-yyyy.pbix` nesta pasta.
2. **Livro do Excel** -> `Mapa contabilistico.xlsx` -> folha `Mapa Contabilistico 2025`
   -> **Transformar Dados**. Renomear a consulta para `Mapa Contabilístico`.

## Parte 2 - Power Query
Ordem recomendada (limpeza -> Unpivot -> datas -> tipos no fim):

1. **Apagar o passo automático `Tipo alterado`** (fixa os nomes `jan` ... `dez` e
   converteria `Conta SNC` em número).
2. **Linhas vazias**: Base -> Remover Linhas -> **Remover Linhas em Branco**. Se a
   linha de cabeçalhos não ficar no topo, **Utilizar Primeira Linha como Cabeçalhos**.
3. **Colunas vazias**: remover a coluna sem nome entre `Designação SNC` e `jan`
   (e a da coluna A, se aparecer). Atalho: selecionar `Conta SNC`, `Designação SNC` e
   `jan` ... `dez` -> **Remover Outras Colunas**.
4. **Unpivot**: selecionar `Conta SNC` e `Designação SNC` (Ctrl + clique) -> botão
   direito -> **Anular Dinamização de Outras Colunas**. Renomear `Atributo` -> `Mês`.
   As 123 células vazias desaparecem sozinhas. Resultado: **1 065 linhas**.
5. **Data (Método A da aula, ano implícito 2025)**: selecionar `Mês` -> Transformar ->
   Formatar -> **Adicionar Sufixo** ` 2025` (com espaço) -> `jan 2025` -> **Alterar tipo
   -> Utilizando a Região -> Data / Português (Portugal)** -> `01/01/2025`. Renomear para
   `Data`. Se preferir manter o texto do mês, duplicar a coluna antes.
6. **Tipos de dados (no fim)**: `Conta SNC` Texto; `Designação SNC` Texto; `Data` Data;
   `Valor` **Número decimal fixo** (moeda) ou Número decimal.
7. (opcional) Coluna `Classe SNC` = Adicionar Coluna -> Extrair -> **Primeiros
   Caracteres** (1) de `Conta SNC`. Útil para uma segunda segmentação.
8. (opcional) Coluna `Conta - Designação` = selecionar `Conta SNC` e `Designação SNC`
   -> Adicionar Coluna -> **Intercalar Colunas** com separador ` - `. Resolve as
   designações repetidas na segmentação (`6888 - Outros` vs `7888 - Outros`).
9. **Fechar e Aplicar**.

Código M de referência:

```m
let
    Origem = Excel.Workbook(File.Contents("...\lab-assincrono\Mapa contabilistico.xlsx"), null, true),
    Folha = Origem{0}[Data],                                   // primeira folha, por posição
    #"Linhas em branco removidas" = Table.SelectRows(Folha, each not List.IsEmpty(List.RemoveMatchingItems(Record.FieldValues(_), {"", null}))),
    #"Cabeçalhos promovidos" = Table.PromoteHeaders(#"Linhas em branco removidas", [PromoteAllScalars = true]),
    #"Outras colunas removidas" = Table.SelectColumns(#"Cabeçalhos promovidos", {"Conta SNC", "Designação SNC", "jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"}),
    #"Coluna não dinamizada" = Table.UnpivotOtherColumns(#"Outras colunas removidas", {"Conta SNC", "Designação SNC"}, "Mês", "Valor"),
    #"Sufixo adicionado" = Table.TransformColumns(#"Coluna não dinamizada", {{"Mês", each _ & " 2025", type text}}),
    #"Tipo de coluna com região alterada" = Table.TransformColumnTypes(#"Sufixo adicionado", {{"Mês", type date}}, "pt-PT"),
    #"Colunas com nome mudado" = Table.RenameColumns(#"Tipo de coluna com região alterada", {{"Mês", "Data"}}),
    #"Tipo alterado" = Table.TransformColumnTypes(#"Colunas com nome mudado", {{"Conta SNC", type text}, {"Designação SNC", type text}, {"Valor", Currency.Type}})
in
    #"Tipo alterado"
```

## Parte 3 - Relatório
1. **Cartão - total do campo Valor**: Soma de `Valor` -> **7 721 393,64**
   (Unidades "Milhões": **7,72 M**).
2. **Gráfico de linhas - evolução ao longo do ano**: Eixo X `Data` (hierarquia só com
   **Mês**); Eixo Y Soma de `Valor`.

   | Mês | Soma de Valor | Mês | Soma de Valor |
   |---|---|---|---|
   | jan | 0,00 | jul | 201 882,87 |
   | fev | -45 058,84 | ago | 277 353,25 |
   | mar | -61 462,59 | set | 467 208,60 |
   | abr | -56 916,05 | out | 401 999,85 |
   | mai | 58 549,46 | nov | 318 403,22 |
   | jun | 26 999,52 | dez | 6 132 434,34 |

   Janeiro dá **0,00** porque o balancete está equilibrado (débitos = créditos). O salto
   de dezembro vem do apuramento de fim de ano.
3. **Segmentação por designação**: visual **Segmentação de dados** com `Designação SNC`
   (ou `Conta - Designação`). Em Formatar -> Definições da segmentação: estilo **Lista
   pendente** e ligar a **pesquisa** (Mais opções `...` -> Pesquisar), como mostra a aula.
   Teste: escolher `Caixa` -> cartão **15 000,05**.
4. **Publicar** -> "A minha área de trabalho".
5. Submeter o `.pbix` no Moodle.

Totais por classe SNC (com a coluna opcional `Classe SNC`), para conferir:

| Classe | Descrição | Linhas | Soma de Valor |
|---|---|---|---|
| 1 | Meios financeiros líquidos | 29 | 7 267 454,61 |
| 2 | Contas a receber e a pagar | 290 | 38 249 396,23 |
| 3 | Inventários | 64 | 58 612 741,83 |
| 4 | Investimentos | 136 | 14 248 488,80 |
| 5 | Capital, reservas e resultados transitados | 36 | -103 637 597,58 |
| 6 | Gastos | 394 | 158 245 131,72 |
| 7 | Rendimentos | 109 | -167 612 758,50 |
| 8 | Resultados | 7 | 2 348 536,53 |
| | **Total** | **1 065** | **7 721 393,64** |

## Dashboard com a identidade Skodji Digital
Ficheiros em [`dashboard/`](dashboard/): `fundo-dashboard.png`, `mockup-dashboard.png`
e `tema-skodji.json` (o mesmo do lab síncrono do OA3). Configuração igual à dos labs
anteriores (tema, fundo **Ajustar** com transparência 0%, visuais sem título nem fundo).

Para este dashboard são precisas as duas colunas opcionais da Parte 2:
- `Conta - Designação` (passo 8): **`Conta SNC` sozinha só tem 93 valores distintos**
  e `Designação SNC` 91, por causa das repetições. Só o par dá as 99 contas.
- `Classe SNC` com nome, via Adicionar Coluna -> **Coluna Personalizada**:

  ```m
  {"1 Meios fin. líquidos", "2 Contas a rec./pagar", "3 Inventários", "4 Investimentos",
   "5 Capital e reservas", "6 Gastos", "7 Rendimentos", "8 Resultados"}
   {Number.From(Text.Start([Conta SNC], 1)) - 1}
  ```

| Visual | Campos | X | Y | Largura | Altura | Valor esperado |
|---|---|---|---|---|---|---|
| Cartão - Valor total | Soma de `Valor` (Milhões, 2 casas) | 38 | 122 | 270 | 50 | 7,72 M |
| Cartão - Contas SNC | Contagem (Distinta) de `Conta - Designação` | 350 | 122 | 270 | 50 | 99 |
| Cartão - Linhas após Unpivot | Contagem de `Valor` | 662 | 122 | 270 | 50 | 1.065 |
| Cartão - Dezembro | Soma de `Valor` + filtro do visual `Data` = 01/12/2025 | 974 | 122 | 270 | 50 | 6,13 M |
| Linhas - evolução no ano | Eixo X `Data` (só **Mês**); Eixo Y Soma de `Valor`; rótulos de dados ligados | 34 | 242 | 756 | 444 | jan 0,00 ... dez 6,13 M |
| Segmentação - Designação | `Designação SNC` (ou `Conta - Designação`); estilo **Lista pendente**; pesquisa ligada | 826 | 242 | 420 | 160 | `Caixa` -> cartão 15 000,05 |
| Barras - por classe SNC | Eixo Y `Classe SNC`; Eixo X Soma de `Valor`; ordenar por `Classe SNC` | 826 | 478 | 420 | 208 | 8 barras; 5 e 7 negativas |

No gráfico por classe, as classes 5 (Capital) e 7 (Rendimentos) ficam **negativas**: num
balancete os créditos têm sinal negativo. O Power BI desenha-as para a esquerda do zero
automaticamente.

## Evidências
Guardar em [`evidencias/`](evidencias/):
- `01-unpivot-power-query.png` - consulta com os passos aplicados e as colunas Conta SNC, Designação SNC, Data, Valor
- `02-relatorio.png` - cartão, gráfico de linhas e segmentação
- `03-publicar-sucesso.png` - publicação no Power BI Service
- `04-submissao-moodle.png` - submissão no Moodle

## Estado
- [ ] Parte 1 - ficheiro criado e Excel importado
- [ ] Parte 2 - limpeza, Unpivot (1 065 linhas), datas e tipos
- [ ] Parte 3 - cartão (7,72 M), gráfico de linhas e segmentação por designação
- [ ] Publicado no Power BI Service
- [ ] Submetido no Moodle
