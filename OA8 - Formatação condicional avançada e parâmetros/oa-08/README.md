# OA8 - Aplicar formatação condicional avançada. Aplicar Parâmetros para mais dinamismo

## Sumário
- Formatação condicional nos outros visuais e com medidas.
- Trabalhar com parâmetros numéricos e de campo.

## Calendário
| Atividade | Estado |
|---|---|
| Pré-teste | concluído |
| Lab síncrono | concluído |
| Lab assíncrono | concluído (submetido no Moodle 09/11/2026) |
| Pós-teste | concluído |

## Conceitos da aula
Resumo dos materiais de estudo nesta pasta (`Advanced_Power_BI_Dynamics (2)_compressed.pdf`,
14 diapositivos, e o infográfico `Relatórios_Dinâmicos_e_Formatação_Condicional.png`):

| Conceito | Regra prática |
|---|---|
| **3 níveis de um relatório** | 1) Comunicação visual (formatação condicional com medidas); 2) Análise e tendência (DAX avançado, médias móveis); 3) Interatividade total (parâmetros controlados pelo utilizador) |
| **Formatação condicional além das tabelas** | Botão **fx** em Colunas, Fundos, Rótulos de dados e Cartões. Gradiente: 0% = valor mínimo e 100% = valor máximo do contexto. Destaca o melhor e o pior mês sem análise manual |
| **Regras com notação científica** | `6E7` = 60.000.000. Ex.: < 6E7 vermelho; 6E7 a 7E7 amarelo; > 7E7 verde. Evita erros a contar zeros |
| **Caixa vazia nas regras** | Apagar o valor = **Mínimo** ou **Máximo**. Tipo sempre **Número** |
| **Cor dinâmica via DAX** | `CF média semanal = IF([Total Sales] >= [média semanal], "Green", "#FF0000")` -> **fx -> Estilo: Valor do campo** -> esta medida. Preferir códigos hex (só há 147 nomes de cores) |
| **Vista de consultas DAX** | Sandbox para testar expressões de tabela com `EVALUATE` (ex.: `EVALUATE DATESBETWEEN(...)`) sem mexer no modelo |
| **Média móvel** | `AVERAGEX(DATESBETWEEN(Calendar[Date], MAX(Calendar[Date]) - 6, MAX(Calendar[Date])), [Total Sales])`: iteradora + janela de contexto + expressão. Aplana o ruído diário e mostra a tendência |
| **Parâmetros numéricos (What-if)** | **Modelação -> Novo parâmetro -> Intervalo numérico**: cria uma tabela com `GENERATESERIES` + medida `SELECTEDVALUE` (valor escolhido no deslizador) que se injeta noutras medidas (ex.: o 6 da média móvel passa a `[dias Value]`) |
| **Parâmetros de campo** | **Novo parâmetro -> Campos**: um visual, várias métricas escolhidas numa segmentação; o eixo adapta escala e formato. **Golden Rule**: segmentação em **seleção única** |
| **Qual parâmetro usar?** | Numérico: simular cenários e trocar valores fixos no DAX (dias, taxas, prazos). De campo: trocar eixos/medidas de um visual (Vendas, Lucro, % Variação) |
| **WEEKNUM(data, 21)** | Semanas ISO 8601 (o ano começa na semana com a primeira quinta-feira) |

## Lab síncrono
Concluído na sessão. Ficheiro do formador: `Modelo 22-10-2026.pbix` (fora do Git).

## Lab assíncrono
Enunciado e guia: [`lab-assincrono/README.md`](lab-assincrono/README.md) - LusaTech: parâmetro
de campo `Métrica a Analisar`, cores das colunas pela `Variação Homóloga %` e página
**Simulação** com o parâmetro numérico `Simulação Crescimento`.

## Estado
- [x] Pré-teste - concluído
- [x] Lab síncrono - concluído
- [x] Lab assíncrono - `EdmilsonLandim-09-11-2026.pbix` (parâmetro de campo, cores por medida, What-if); publicado e submetido no Moodle (09/11/2026)
- [x] Pós-teste - concluído
