# OA3 - Aplicar o processo de combine files e unpivot

## Sumário
- Trabalhar o processo Combine files (Combinar ficheiros).
- Trabalhar com dados não normalizados. Tabelas cruzadas.

## Calendário
| Atividade | Abre | Fecha |
|---|---|---|
| Pré-teste | 06/10/2026 00:01 | - |
| Lab assíncrono | 08/10/2026 19:45 | 20/11/2026 23:59 |
| Pós-teste | 08/10/2026 20:30 | 20/11/2026 23:59 |

## Lab síncrono
Ficheiros (em [`lab-sincrono/`](lab-sincrono/), fora do Git por serem do formador):
- `Demo4.xlsx` - tabela cruzada de vendas (Parte B)
- `csv/LancamentosContabilidade2018.csv`, `...2019.csv`, `...2020.csv` (Parte A).
  Os CSV estão numa subpasta própria `csv/`, porque o conector **Pasta** lê todos
  os ficheiros da pasta escolhida.

Guardar o `.pbix` como `OA3 - Lab Síncrono.pbix` em `lab-sincrono/`.

### Parte A - Combine Files (3 CSV de lançamentos contabilísticos)
Os 3 ficheiros têm a mesma estrutura: UTF-8, separador `;`, 9 colunas
`CodFilial; DataMovimento; CodConta; CodCentroCusto; StatusLançamento; TipoLancamento; Lote; LoteItem; Valor`.

| Ano | Linhas | Soma de Valor | Observações |
|---|---|---|---|
| 2018 | 27 472 | 48 562 557,91 | os mesmos dados do OA2 Lab Assíncrono |
| 2019 | 28 476 | 55 422 121,13 | |
| 2020 | 20 724 | 36 706 153,54 | **ano incompleto** (01/01 a 10/09); 2 447 linhas `NÃO INTEGRADO` |
| **Total** | **76 672** | **140 690 832,57** | |

1. **Obter dados -> Mais... -> Pasta** -> selecionar `lab-sincrono\csv` -> **Combinar
   -> Combinar e Transformar Dados**. Na janela, escolher o primeiro ficheiro como
   exemplo, Delimitador **Ponto e vírgula**, Origem do ficheiro **65001: Unicode (UTF-8)**.
2. O Power BI cria a pasta *Funções Auxiliares* (Ficheiro de Exemplo, Parâmetro,
   Transformar Ficheiro) e a consulta `csv` com a coluna `Source.Name` (nome do
   ficheiro). Renomear a consulta para `Lançamentos`.
3. **Armadilha da região.** Os CSV usam **vírgula decimal** (`1785,6832`) e datas
   **dd/mm/aaaa**. Se o modelo estiver em inglês (EUA), como sugerem os meses em
   inglês do OA2, `1785,6832` é lido como `17856832` e `02/01/2018` como 1 de
   fevereiro. Apagar o passo `Tipo alterado` automático e usar **Alterar tipo ->
   Utilizando a Região -> Português (Portugal)** em `DataMovimento` (Data) e
   `Valor` (Número decimal). Conferir: total de **140 690 832,57**, e a primeira
   linha com data **02/01/2018** e valor **1 785,68**.
4. Restantes tipos: `CodFilial`, `CodConta`, `CodCentroCusto`, `Lote`, `LoteItem` ->
   **Texto** (são códigos).
5. `TipoLancamento`: Substituir Valores (célula inteira) `D` -> `Débito`,
   `C` -> `Crédito`.
6. `Source.Name`: remover, ou extrair o ano (Transformar -> Extrair -> Texto Entre
   Delimitadores `LancamentosContabilidade` e `.csv`) - a `DataMovimento` já tem o ano.
7. `StatusLançamento`: manter as linhas `NÃO INTEGRADO`, mas usá-las num filtro ou
   segmentação no relatório.

Vantagem do Combine Files: um CSV novo (ex.: `...2021.csv`) colocado na pasta
`csv/` entra no modelo com um simples **Atualizar**, sem mexer no Power Query.

### Parte B - Unpivot do `Demo4.xlsx` (tabela cruzada)
Folha `Serviços`, 49 linhas x 16 colunas: `Anos`, `Vendedor`, `Tipo`, `jan` ... `dez`,
`Total Geral`. Os dados não estão normalizados:

| Problema | Ferramenta |
|---|---|
| Meses em colunas (`jan` ... `dez`) | **Anular Dinamização de Outras Colunas** (Unpivot) com `Anos`, `Vendedor`, `Tipo` selecionadas |
| Coluna `Total Geral` (soma calculada) | **Remover Colunas** (antes do Unpivot, senão vira um "mês") |
| 13 linhas de subtotal: `Costa Total`, `2011 Total`, `Total Geral` ... (todas com `Tipo` vazio) | **Filtrar** `Tipo` -> desmarcar `(nulo)` |
| `Anos` mistura números e texto (`2011 Total`) | depois do filtro -> tipo **Número inteiro** |
| Mês em texto abreviado | coluna `Nº Mês` + coluna `Data` (1.º dia do mês), para ordenar e usar a hierarquia de datas |

Resultado: 36 linhas de detalhe (3 anos x 3 vendedores x 4 tipos) x 12 meses =
**432 linhas**, total **5 543 168,90** (igual à célula `Total Geral`).

```m
let
    Origem = Excel.Workbook(File.Contents("...\lab-sincrono\Demo4.xlsx"), null, true),
    Servicos = Origem{[Item = "Serviços", Kind = "Sheet"]}[Data],
    #"Cabeçalhos promovidos" = Table.PromoteHeaders(Servicos, [PromoteAllScalars = true]),
    #"Linhas filtradas" = Table.SelectRows(#"Cabeçalhos promovidos", each [Tipo] <> null),
    #"Colunas removidas" = Table.RemoveColumns(#"Linhas filtradas", {"Total Geral"}),
    #"Coluna não dinamizada" = Table.UnpivotOtherColumns(#"Colunas removidas", {"Anos", "Vendedor", "Tipo"}, "Mês", "Valor"),
    #"Tipo alterado" = Table.TransformColumnTypes(#"Coluna não dinamizada", {{"Anos", Int64.Type}, {"Vendedor", type text}, {"Tipo", type text}, {"Mês", type text}, {"Valor", type number}}),
    #"Nº Mês" = Table.AddColumn(#"Tipo alterado", "Nº Mês", each List.PositionOf({"jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"}, [Mês]) + 1, Int64.Type),
    Data = Table.AddColumn(#"Nº Mês", "Data", each #date([Anos], [Nº Mês], 1), type date)
in
    Data
```

Valores para conferir:
- por ano: 2011 1 844 258,37 / 2012 1 758 596,53 / 2013 1 940 314,00
- por vendedor: Silva 1 933 358,75 / Mendes 1 825 471,80 / Costa 1 784 338,34
- por tipo: Software 1 496 870,31 / Formação 1 435 235,32 / Serviços 1 393 286,83 / Hardware 1 217 776,44

No relatório, ordenar `Mês` pela coluna `Nº Mês` (**Ferramentas de coluna ->
Ordenar por coluna**), senão os meses aparecem por ordem alfabética (abr, ago, dez...).

## Lab assíncrono
- Abre: 08/10/2026 às 19:45 - data limite: 20/11/2026 às 23:59
- Enunciado e entrega: [`lab-assincrono/`](lab-assincrono/) *(a aguardar enunciado)*

## Estado
- [x] Pré-teste - concluído
- [ ] Lab síncrono
- [ ] Lab assíncrono
- [ ] Pós-teste
