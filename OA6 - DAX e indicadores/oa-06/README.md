# OA6 - Aplicar DAX ao cálculo de diferentes indicadores

## Sumário
- Trabalhar com medidas.
- Medidas implícitas vs. explícitas.
- Criar tabela para medidas.
- Cálculo de indicadores.

## Calendário
| Atividade | Estado |
|---|---|
| Pré-teste | concluído |
| Lab síncrono | concluído |
| Lab assíncrono | concluído (submetido no Moodle 02/11/2026) |
| Pós-teste | concluído |

## Conceitos da aula
Resumo dos materiais de estudo nesta pasta (`DAX_Architecture_Blueprint_compressed.pdf`,
15 diapositivos, e o infográfico `Guia_de_Medidas_em_Análise.png`):

| Conceito | Regra prática |
|---|---|
| **Medidas implícitas** (amador) | Arrastar uma coluna numérica para o visual e deixar o Power BI somar. Flexibilidade baixa: não dá rácios, percentagens nem variações temporais; a fórmula fica escondida no visual e não se reutiliza |
| **Medidas explícitas** (profissional) | Escritas em DAX (**Nova medida**). Controlo total sobre o contexto e os filtros; funcionam como variáveis globais reutilizáveis |
| **Tabela de medidas** | 1) **Introduzir Dados** -> tabela `Medidas` (ou `_Medidas`, para ficar no topo) -> Carregar; 2) mover as medidas soltas para lá (Ferramentas de medida -> **Tabela base**); 3) apagar a `Coluna 1` (Eliminar do modelo); 4) o ícone passa a **calculadora** |
| **Medidas base (filosofia modular)** | `Total Sales = SUM(Sales[SalesAmount])`, `# Sales = COUNTROWS(Sales)`, `AVG Sales = DIVIDE([Total Sales], [# Sales])`. **Regra de ouro**: nunca reescrever uma agregação que já existe; invocar a medida entre `[ ]` |
| **DIVIDE** | Divisão segura: devolve vazio (Blank) em vez de erro quando o denominador é zero |
| **Contexto de avaliação** | A mesma medida recalcula-se conforme o ano, a marca ou a região do visual. Não é preciso uma medida "Vendas Europa" e outra "Vendas Ásia" |
| **Paradoxo das percentagens** | Com segmentações, o denominador também é filtrado e tudo dá 100%. Solução: forçar o denominador a ignorar o filtro |
| **CALCULATE** | `CALCULATE(expressão, modificador)`: a única forma de alterar o contexto de avaliação |
| **ALL** | `All Sales = CALCULATE([Total Sales], ALL(Products))` congela o denominador (ex.: 335 M em todas as linhas); `DIVIDE([Total Sales], [All Sales])` dá a % de contribuição. Base da **análise de Pareto (80/20)** |
| **SAMEPERIODLASTYEAR** | `Total Sales Last Year = CALCULATE([Total Sales], SAMEPERIODLASTYEAR(Calendar[Date]))`. Exige uma **tabela de calendário contínua** (1 jan a 31 dez, sem datas repetidas); nunca usar a data da tabela de factos |
| **Variação homóloga** | Passo 1: `[Total Sales] - [Total Sales Last Year]`; passo 2: `DIVIDE(diferencial, [Total Sales Last Year])` |
| **Visualizar o impacto** | Gráfico de colunas da variação com rótulos de dados e **linha constante no zero** (Analítica -> Linha constante): meses de quebra saltam à vista |

Os 4 pilares do arquiteto: **Estrutura** (tabela de medidas), **Modularidade** (medidas
base reutilizadas), **Segurança** (DIVIDE), **Controlo** (CALCULATE e Time Intelligence).

## Lab síncrono
Concluído na sessão. Ficheiro do formador: `lab-sincrono/Modelo 15-10-2026.pbix`
(modelo Contoso com as páginas Geral, Mapa e Tempo; fora do Git).

## Lab assíncrono
Enunciado e guia: [`lab-assincrono/README.md`](lab-assincrono/README.md) - LusaTech: tabela
`_Medidas`, medidas explícitas, Faturação do ano anterior, Variação Homóloga %, % do total
e página **Matriz**.

## Estado
- [x] Pré-teste - concluído
- [x] Lab síncrono - concluído
- [x] Lab assíncrono - medidas, YoY, % do total e página Matriz; publicado e submetido no Moodle (02/11/2026)
- [x] Pós-teste - concluído
