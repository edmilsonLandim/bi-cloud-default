# OA2 - Lab Assíncrono: Append Queries

- Abre: 06/10/2026 às 19:45 - data limite: 20/11/2026 às 23:59
- Ficheiro de entrega: `EdmilsonLandim_dd-mm-yyyy.pbix` (nome + data do dia)
- Dados: `All data by Month.xlsx` - **12 folhas** (Janeiro a Dezembro de 2025), sem
  tabelas Excel, com as mesmas 6 colunas:
  `DataMovimento`, `CodFilial`, `CodConta`, `CodCentroCusto`, `TipoLancamento`, `Valor`

## Perfil dos dados (para conferir)
| Mês | Linhas | Soma de Valor |
|---|---|---|
| Janeiro | 1 901 | 3 354 185,93 |
| Fevereiro | 1 554 | 2 160 276,26 |
| Março | 1 974 | 2 981 175,63 |
| Abril | 2 142 | 3 689 791,53 |
| Maio | 2 022 | 2 848 619,41 |
| Junho | 2 901 | 4 231 501,55 |
| Julho | 2 856 | 4 901 511,82 |
| Agosto | 2 862 | 4 832 280,38 |
| Setembro | 2 364 | 4 828 513,62 |
| Outubro | 2 570 | 5 139 354,41 |
| Novembro | 2 300 | 5 309 575,84 |
| Dezembro | 2 026 | 4 285 771,53 |
| **Total** | **27 472** | **48 562 557,91** |

Verificado: cabeçalhos iguais nas 12 folhas, sem células vazias, todas as datas
dentro do mês da folha. `TipoLancamento`: 21 424 `D` / 6 048 `C`. 4 filiais
(1001, 1002, 1003, 1004), 79 contas, 10 centros de custo.

## Parte 1 - Criação do relatório e importação
1. **Ficheiro -> Novo** -> **Guardar como** `EdmilsonLandim_dd-mm-yyyy.pbix`
   nesta pasta.
2. **Livro do Excel** -> `All data by Month.xlsx` -> no Navegador marcar **as 12
   folhas** -> **Transformar Dados**. Ficam 12 consultas, uma por mês. Em cada uma
   o Power BI já aplica `Cabeçalhos promovidos` e `Tipo alterado`.

## Parte 2 - Power Query
1. **Append Queries**: Base -> **Acrescentar Consultas -> Acrescentar Consultas
   como Nova** -> **Três ou mais tabelas** -> adicionar as 12 folhas por ordem
   (Janeiro ... Dezembro) -> renomear a nova consulta para `Lançamentos`.
   Resultado: **27 472 linhas**.
2. Transformações na consulta `Lançamentos`:
   - `DataMovimento` -> tipo **Data** (vem como Data/Hora com 00:00)
   - `CodFilial`, `CodConta`, `CodCentroCusto` -> tipo **Texto**. São códigos, não
     quantidades: em número, o Power BI soma-os nos visuais (ex.: "Soma de CodFilial")
   - `TipoLancamento`: **Substituir Valores** (célula inteira) `D` -> `Débito`,
     `C` -> `Crédito`
   - `Valor` -> **Número decimal**
   - (opcional) Adicionar Coluna -> Data -> Mês -> **Nome do Mês**, para o eixo
     do gráfico de linhas
3. Nas 12 consultas dos meses: botão direito -> desmarcar **Ativar carregamento**
   (só `Lançamentos` vai para o modelo).
4. **Fechar e Aplicar**.

Armadilhas:
- **Não usar Remover Duplicados.** Há 7 439 linhas repetidas, mas são lançamentos
  legítimos (mesmo dia, conta e valor). Remover baixaria o total e o cartão ficava
  errado.
- **Valores negativos** (284 linhas, mínimo -190 483,74) são estornos/correções:
  manter.
- `CodCentroCusto` = `0` em 87 linhas (sem centro de custo atribuído): manter, é
  um código válido.

Código M de referência da consulta `Lançamentos`:

```m
let
    Origem = Table.Combine({Janeiro, Fevereiro, Março, Abril, Maio, Junho, Julho, Agosto, Setembro, Outubro, Novembro, Dezembro}),
    #"Tipo alterado" = Table.TransformColumnTypes(Origem, {
        {"DataMovimento", type date}, {"CodFilial", type text}, {"CodConta", type text},
        {"CodCentroCusto", type text}, {"TipoLancamento", type text}, {"Valor", type number}}),
    #"Valor substituído" = Table.ReplaceValue(#"Tipo alterado", "D", "Débito", Replacer.ReplaceValue, {"TipoLancamento"}),
    #"Valor substituído 1" = Table.ReplaceValue(#"Valor substituído", "C", "Crédito", Replacer.ReplaceValue, {"TipoLancamento"})
in
    #"Valor substituído 1"
```

## Parte 3 - Relatório
1. **Cartão - total do campo Valor**: Soma de `Valor` -> **48 562 557,91**
   (com Unidades de visualização "Milhões": **48,56 M**).
2. **Gráfico de linhas - evolução ao longo do ano**: Eixo X `DataMovimento`
   (hierarquia só com **Mês**) ou a coluna `Nome do Mês` ordenada pelo número
   do mês; Eixo Y Soma de `Valor`. Pico em novembro (5,31 M), mínimo em fevereiro
   (2,16 M).
3. **Publicar** -> "A minha área de trabalho".
4. Submeter o `.pbix` no Moodle.

## Dashboard com a identidade Skodji Digital
Ficheiros em [`dashboard/`](dashboard/): `fundo-dashboard.png`,
`mockup-dashboard.png` e `tema-skodji.json`. Configuração igual à do OA1 e à do
lab síncrono (tema, fundo **Ajustar** com transparência 0%, visuais sem título nem
fundo).

| Visual | Campos | X | Y | Largura | Altura | Valor esperado |
|---|---|---|---|---|---|---|
| Cartão - Valor total | Soma de `Valor` (Milhões, 2 casas) | 38 | 122 | 270 | 50 | 48,56 M |
| Cartão - Lançamentos | Contagem de `Valor` (ou de linhas) | 350 | 122 | 270 | 50 | 27.472 |
| Cartão - Débito | Soma de `Valor` + filtro `TipoLancamento` = Débito | 662 | 122 | 270 | 50 | 23,09 M |
| Cartão - Crédito | Soma de `Valor` + filtro `TipoLancamento` = Crédito | 974 | 122 | 270 | 50 | 25,48 M |
| Linhas - evolução no ano | Eixo X Mês; Eixo Y Soma de `Valor`; rótulos de dados ligados | 34 | 242 | 756 | 444 | Jan 3,35 ... Dez 4,29 |
| Anel - por tipo | Legenda `TipoLancamento`; Valores Soma de `Valor` | 826 | 242 | 420 | 160 | Crédito 52,5% / Débito 47,5% |
| Barras - por filial | Eixo Y `CodFilial`; Eixo X Soma de `Valor` | 826 | 478 | 420 | 208 | 1001 34,59 M ... 1002 0,82 M |

Para a área sombreada do mockup, usar o visual **Gráfico de área** em vez de
Gráfico de linhas, ou no Gráfico de linhas ligar **Sombrear área**. O enunciado
pede um gráfico de linhas: as duas opções mostram a linha.

## Evidências
Guardar em [`evidencias/`](evidencias/):
- `01-append-power-query.png` - consulta `Lançamentos` com os passos aplicados
- `02-relatorio.png` - dashboard no Power BI Desktop
- `03-publicar-sucesso.png` - publicação concluída a partir do Power BI Desktop
- `04-submissao-moodle.png` - submissão no Moodle (Submetido para avaliação)

## Estado
- [x] Parte 1 - [`dashboard/EdmilsonLandim_07-10-2026.pbix`](dashboard/EdmilsonLandim_07-10-2026.pbix) com as 12 folhas importadas
- [x] Parte 2 - Append (27 472 linhas) e transformações ([`power-query.m`](power-query.m))
- [x] Parte 3 - cartão (48,56 M), gráfico de linhas e dashboard com identidade Skodji
- [x] Publicado no Power BI Service ("A minha área de trabalho")
- [x] Submetido no Moodle - 07/10/2026 15:09, 44 dias antes do prazo
