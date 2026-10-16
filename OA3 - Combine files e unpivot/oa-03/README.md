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

## Conceitos da aula
Resumo dos materiais de estudo desta pasta (`A3-Power_Query_Automation_Mastery.pdf`,
15 diapositivos, e o infográfico `A3-Automação_e_Limpeza_de_Dados.png`):

| Conceito | Regra prática |
|---|---|
| **Fragmentação, tabela cruzada, ruído** | Os três problemas que o Power Query resolve: dezenas de ficheiros iguais espalhados, meses em colunas, totais e subtotais no meio dos dados |
| **Combine Files (importar a partir de uma Pasta)** | **Obter Dados -> Pasta -> caminho do diretório -> Combinar e Transformar Dados**. Não selecionar ficheiros individuais: apontar para a pasta |
| **Regra de ouro do Combine Files** | Todos os ficheiros da pasta têm a **mesma estrutura** (mesmas colunas, mesma ordem) |
| **Nomes de folha dinâmicos** | No Editor Avançado, trocar `Source{[Item="Sheet1",Kind="Sheet"]}[Data]` por `Source{0}[Data]` (primeira folha por posição). O processo não falha se alguém mudar o nome da folha num ficheiro mensal |
| **Atualização com um clique** | Ficheiro novo na pasta + **Atualizar** = dados novos no relatório, sem copiar/colar |
| **Formato tabular vs. tabela resumo** | O Power BI precisa de dados em **lista** (cada coluna é uma variável: Conta, Mês, Valor). A tabela cruzada é para leitura humana: cada mês é uma variável distinta e não dá para comparar meses num eixo |
| **Unpivot (Anular Dinamização)** | 1) selecionar as colunas **âncora** (Ctrl + clique: Conta, Designação); 2) botão direito; 3) **Anular Dinamização de Outras Colunas**. Nunca selecionar os meses: com "Outras Colunas", meses futuros entram automaticamente. Nascem duas colunas: **Atributo** e **Valor** |
| **Limpeza antes do Unpivot (regra de ouro)** | Remover a coluna **Total Geral** e as linhas **nulas / Subtotal** antes de anular a dinamização, senão os valores contam a dobrar |
| **Higiene de dados** | 1) **Apagar o passo automático "Tipo alterado"**, que fixa os nomes das colunas e falha no Unpivot; 2) remover colunas irrelevantes (ex.: nome do ficheiro de origem); 3) **tipos de dados no fim** (Texto, Data, Moeda) |
| **Datas válidas sem fórmulas** | **Método A** (um ano implícito): coluna Mês -> Transformar -> Formatar -> **Adicionar Sufixo** ` 2025` -> tipo **Data**. **Método B** (vários anos): selecionar `Mês` e `Ano` -> **Intercalar Colunas** -> tipo **Data** |
| **Visualização** | Data no **Eixo X**, Valor no **Eixo Y**, Designação na **Legenda**. **Segmentação** (slicer) com pesquisa para navegar num "mar de contas"; **drill-down** Ano -> Trimestre -> Mês |

Ciclo completo: Ficheiros brutos -> Pasta partilhada -> Combine Files -> Limpeza ->
Unpivot -> Datas -> Modelo tabular -> Dashboards. A partir daí, cada ciclo novo é só
**Atualizar**.

## Lab síncrono
Ficheiros (em [`lab-sincrono/`](lab-sincrono/), fora do Git por serem do formador):
- `Demo4.xlsx` - tabela cruzada de vendas (Parte B)
- `csv/LancamentosContabilidade2018.csv`, `...2019.csv`, `...2020.csv` (Parte A).
  Os CSV estão numa subpasta própria `csv/`, porque o conector **Pasta** lê todos
  os ficheiros da pasta escolhida.

Guardar o `.pbix` como `OA3 - Lab Síncrono.pbix` em `lab-sincrono/`.

### Parte A - Combine Files (3 CSV de lançamentos contabilísticos)
Os 3 ficheiros têm a mesma estrutura (regra de ouro cumprida): UTF-8, separador `;`,
9 colunas
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
3. **Higiene:** apagar o passo `Tipo alterado` automático e remover `Source.Name`
   (a `DataMovimento` já tem o ano).
4. **Armadilha da região.** Os CSV usam **vírgula decimal** (`1785,6832`) e datas
   **dd/mm/aaaa**. Se o modelo estiver em inglês (EUA), como sugerem os meses em
   inglês do OA2, `1785,6832` é lido como `17856832` e `02/01/2018` como 1 de
   fevereiro. Usar **Alterar tipo -> Utilizando a Região -> Português (Portugal)** em
   `DataMovimento` (Data) e `Valor` (Número decimal). Conferir: total de
   **140 690 832,57**, e a primeira linha com data **02/01/2018** e valor **1 785,68**.
5. Restantes tipos: `CodFilial`, `CodConta`, `CodCentroCusto`, `Lote`, `LoteItem` ->
   **Texto** (são códigos).
6. `TipoLancamento`: Substituir Valores (célula inteira) `D` -> `Débito`,
   `C` -> `Crédito`.
7. `StatusLançamento`: manter as linhas `NÃO INTEGRADO`, mas usá-las num filtro ou
   segmentação no relatório.
8. Coluna `Ano`: selecionar `DataMovimento` -> Adicionar Coluna -> Data -> Ano -> **Ano**
   (substitui a informação do `Source.Name`, um ficheiro por ano; usada no dashboard).

Teste do "um clique": copiar um dos CSV para `csv\` com outro nome e carregar em
**Atualizar** - as linhas aparecem a dobrar. Apagar a cópia e atualizar outra vez.

### Parte B - Unpivot do `Demo4.xlsx` (tabela cruzada)
Folha `Serviços`, 49 linhas x 16 colunas: `Anos`, `Vendedor`, `Tipo`, `jan` ... `dez`,
`Total Geral`. Os dados não estão normalizados:

| Problema | Ferramenta |
|---|---|
| Coluna `Total Geral` (soma calculada) | **Remover Colunas** antes do Unpivot (senão vira um "mês") |
| 13 linhas de subtotal: `Costa Total`, `2011 Total`, `Total Geral` ... (todas com `Tipo` vazio) | **Filtrar** `Tipo` -> desmarcar `(nulo)` |
| Passo automático `Tipo alterado` | **Apagar** antes do Unpivot (fixa os nomes `jan` ... `dez`) |
| Meses em colunas (`jan` ... `dez`) | selecionar `Anos`, `Vendedor`, `Tipo` -> **Anular Dinamização de Outras Colunas** -> renomear `Atributo` para `Mês` |
| `Anos` mistura números e texto (`2011 Total`) | depois do filtro -> tipo **Número inteiro** |
| Mês em texto abreviado | **Método B**: selecionar `Mês` e `Anos` -> **Intercalar Colunas** (separador Espaço) -> `jan 2011` -> **Alterar tipo -> Utilizando a Região -> Data / Português (Portugal)** -> `01/01/2011` |

Resultado: 36 linhas de detalhe (3 anos x 3 vendedores x 4 tipos) x 12 meses =
**432 linhas**, total **5 543 168,90** (igual à célula `Total Geral`).

Alternativa em M, que mantém `Anos` e `Mês` e acrescenta `Nº Mês` e `Data`
(útil para ordenar os meses):

```m
let
    Origem = Excel.Workbook(File.Contents("...\lab-sincrono\Demo4.xlsx"), null, true),
    Servicos = Origem{0}[Data],                     // primeira folha, por posição
    #"Cabeçalhos promovidos" = Table.PromoteHeaders(Servicos, [PromoteAllScalars = true]),
    #"Linhas filtradas" = Table.SelectRows(#"Cabeçalhos promovidos", each [Tipo] <> null),
    #"Colunas removidas" = Table.RemoveColumns(#"Linhas filtradas", {"Total Geral"}),
    #"Coluna não dinamizada" = Table.UnpivotOtherColumns(#"Colunas removidas", {"Anos", "Vendedor", "Tipo"}, "Mês", "Valor"),
    #"Nº Mês" = Table.AddColumn(#"Coluna não dinamizada", "Nº Mês", each List.PositionOf({"jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"}, [Mês]) + 1, Int64.Type),
    Data = Table.AddColumn(#"Nº Mês", "Data", each #date([Anos], [Nº Mês], 1), type date),
    #"Tipo alterado" = Table.TransformColumnTypes(Data, {{"Anos", Int64.Type}, {"Vendedor", type text}, {"Tipo", type text}, {"Mês", type text}, {"Valor", type number}})
in
    #"Tipo alterado"
```

Valores para conferir:
- por ano: 2011 1 844 258,37 / 2012 1 758 596,53 / 2013 1 940 314,00
- por vendedor: Silva 1 933 358,75 / Mendes 1 825 471,80 / Costa 1 784 338,34
- por tipo: Software 1 496 870,31 / Formação 1 435 235,32 / Serviços 1 393 286,83 / Hardware 1 217 776,44

Se usar a coluna de texto `Mês` num visual, ordená-la por `Nº Mês` (**Ferramentas de
coluna -> Ordenar por coluna**), senão os meses aparecem por ordem alfabética
(abr, ago, dez...). Com a coluna `Data` isto não é preciso.

### Dashboard com a identidade Skodji Digital
Ficheiros em [`lab-sincrono/dashboard/`](lab-sincrono/dashboard/): uma página por
parte - `fundo-parte-a.png` / `mockup-parte-a.png` e `fundo-parte-b.png` /
`mockup-parte-b.png` - e `tema-skodji.json`. O tema do OA3 tem uma **3.ª cor amarela**
(`#F5B800`) para os gráficos com 3 anos; as duas primeiras continuam azul `#1E55A2` e
ciano `#32B2E7`.

Configuração igual à do OA1/OA2: **Ver -> Temas -> Procurar temas**; **Formatar página
-> Fundo da tela -> Imagem**, Ajuste **Ajustar**, Transparência **0%**; em cada visual
desligar **Título** e **Fundo**. Posições (iguais nas duas páginas):

| Posição | X | Y | Largura | Altura |
|---|---|---|---|---|
| Cartão 1 / 2 / 3 / 4 | 38 / 350 / 662 / 974 | 122 | 270 | 50 |
| Painel grande (esquerda) | 34 | 242 | 756 | 444 |
| Painel direita, em cima | 826 | 242 | 420 | 160 |
| Painel direita, em baixo | 826 | 478 | 420 | 208 |

**Página 1 - Parte A (Combine Files)**

| Visual | Campos | Valor esperado |
|---|---|---|
| Cartão 1 - Valor total | Soma de `Valor` (Milhões, 2 casas) | 140,69 M |
| Cartão 2 - Lançamentos | Contagem de `Valor` | 76.672 |
| Cartão 3 - Ficheiros combinados | Contagem (Distinta) de `Ano` | 3 |
| Cartão 4 - Não integrados | Contagem de `Valor` + filtro do visual `StatusLançamento` = NÃO INTEGRADO | 2.447 |
| Linhas - valor por mês | Eixo X `DataMovimento` (hierarquia só com **Mês**); Eixo Y Soma de `Valor`; **Legenda `Ano`** | 3 linhas; 2020 cai em setembro (dados só até 10/09) |
| Anel - Débito vs Crédito | Legenda `TipoLancamento`; Valores Soma de `Valor` | Crédito 74,39 M / Débito 66,30 M |
| Barras - valor por ano | Eixo Y `Ano`; Eixo X Soma de `Valor` | 2018 48,56 M / 2019 55,42 M / 2020 36,71 M |

**Página 2 - Parte B (Unpivot)**

| Visual | Campos | Valor esperado |
|---|---|---|
| Cartão 1 - Vendas totais | Soma de `Valor` (Milhões) | 5,54 M |
| Cartões 2 a 4 - Vendas 2011 / 2012 / 2013 | Soma de `Valor` + filtro do visual `Anos` = 2011 / 2012 / 2013 | 1,84 M / 1,76 M / 1,94 M |
| Linhas - vendas por mês | Eixo X `Data` (só **Mês**) ou `Mês` ordenado por `Nº Mês`; Eixo Y Soma de `Valor`; **Legenda `Anos`** | 3 linhas quase paralelas, picos em fev e abr |
| Anel - por tipo | Legenda `Tipo`; Valores Soma de `Valor` | Software 27,0% ... Hardware 22,0% |
| Barras - por vendedor | Eixo Y `Vendedor`; Eixo X Soma de `Valor` | Silva 1,93 M / Mendes 1,83 M / Costa 1,78 M |

Atenção: `Anos` é um número inteiro, por isso o Power BI tenta **somá-lo** (Σ). Em
**Ferramentas de coluna -> Resumo**, escolher **Não resumir** antes de o usar na legenda.

## Lab assíncrono
- Abre: 08/10/2026 às 19:45 - data limite: 20/11/2026 às 23:59
- Enunciado e guia: [`lab-assincrono/README.md`](lab-assincrono/README.md) - Unpivot do
  balancete `Mapa contabilistico.xlsx` (99 contas SNC x 12 meses de 2025)

## Estado
- [x] Pré-teste - concluído
- [x] Lab síncrono - `OA3 - Lab Síncrono.pbix` (páginas Parte A e Parte B), publicado no
  Power BI Service; código M em `lab-sincrono/power-query-parte-a.m` e `-parte-b.m`;
  evidências em [`lab-sincrono/evidencias/`](lab-sincrono/evidencias/)
- [ ] Lab assíncrono
- [x] Pós-teste - concluído
