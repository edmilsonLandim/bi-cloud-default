# OA7 - Utilizar Tooltips para melhorar a qualidade da informação. Introdução à formatação condicional

## Sumário
- Trabalhar com tooltips (descrições).
- Ranking com DAX.
- Adicionar visuais personalizados.
- Introdução à formatação condicional.

## Calendário
| Atividade | Estado |
|---|---|
| Pré-teste | concluído |
| Lab síncrono | concluído |
| Lab assíncrono | concluído (submetido no Moodle 03/11/2026) |
| Pós-teste | concluído |

## Conceitos da aula
Resumo dos materiais de estudo nesta pasta (`Power_BI_Interactivity_Architecture_compressed.pdf`,
15 diapositivos, e o infográfico `Análise_Avançada_de_Dados.png`):

| Conceito | Regra prática |
|---|---|
| **Objetivo: zero esforço cognitivo** | Se o utilizador pega no telemóvel para fazer contas (5818 - 5806 = ?), o relatório falhou. O design antecipa as perguntas |
| **Gráfico de cascata** | Revela a variação: total inicial, subidas a verde, descidas a vermelho, total acumulado. Sem eixo Y, só rótulos |
| **Tooltips standard** | Arrastar medidas extra (ex.: Diferença Nominal, % Crescimento) para **Descrições** do visual: aparecem só no hover, o gráfico fica limpo |
| **Tooltips personalizadas** | Página de relatório como descrição: 1) criar e **ocultar** a página; 2) **Informações da página -> Tipo: Descrição** e **Definições da tela -> Personalizado**; 3) no visual principal **Propriedades -> Descrições -> Página de relatório**. A página filtra-se pelo ponto onde está o rato |
| **Modo de foco** | Botão no canto do visual para o ampliar durante apresentações |
| **Visuais personalizados** | **Obter mais elementos visuais** (AppSource, pede conta) ou **Importar de um ficheiro** `.pbiviz` (ex.: World Flags: `Location[Country]` -> bandeira) |
| **RANKX** | `RANKX(ALL(tabela/coluna), [medida])`: função iterante; a tabela é onde se avalia; a expressão dita a posição. O mesmo motor dá o Top por cliente, produto ou região |
| **ALL no ranking** | Sem `ALL` cada linha só se compara consigo própria (1.º lugar para todos). Com `ALL` compara com a lista global: ranking real |
| **Escala de cores** | Gradiente no fundo/texto: encontrar anomalias em matrizes densas |
| **Barras de dados** | Direção e magnitude; com negativos, eixo neutro no 0 (vermelho à esquerda, verde à direita); opção **Mostrar apenas barra** |
| **Ícones** | KPIs e tolerâncias: ex. < 0 seta vermelha; 0-5% seta amarela; > 5% seta verde. Ícones **à direita** do valor |
| **Armadilha do Percent** | Nas regras, usar sempre o tipo **Número** (valores decimais literais: -0,05; 0; 0,05). **Percentagem** divide o intervalo mínimo-máximo em percentis cegos |
| **Parâmetros no Power Query** | Parâmetro de texto `Dir` com a pasta: `Csv.Document(File.Contents(Dir & "Sales.csv"))`. Se a origem mudar de computador, só se altera o parâmetro |
| **Escolher o gráfico** (`Visual Chart Guide.pdf`) | Categorias -> barras; tempo -> linha/colunas; parte do todo -> barras 100%/treemap (pizza e anel "not recommended"); valor exato -> número/tabela. Evitar eixo Y truncado, 3D, mais de 4 séries e cores sem significado |

Síntese ("Zero-Click Insight"): tabela com barras de dados na variação nominal, ícones de
tolerância à direita, ranking `RANKX` + `ALL` e uma descrição personalizada no hover.

## Lab síncrono
Concluído na sessão. Ficheiro do formador: `lab-sincrono/Modelo 20-10-2026.pbix`
(fora do Git); visual World Flags em `enlightenWorldFlags...pbiviz` (fora do Git).

## Lab assíncrono
Enunciado e guia: [`lab-assincrono/README.md`](lab-assincrono/README.md) - LusaTech: página
de descrição `Tooltip_Produto`, `Ranking Vendas` com RANKX, gradiente e ícones na página
**Produtos** e o visual Word Cloud.

## Estado
- [x] Pré-teste - concluído
- [x] Lab síncrono - concluído
- [x] Lab assíncrono - `EdmilsonLandim-03-11-2026.pbix` (tooltip, ranking, formatação condicional, Word Cloud); publicado e submetido no Moodle (03/11/2026)
- [x] Pós-teste - concluído
