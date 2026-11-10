# OA10 - Lab Assíncrono: Projeto Final "EcoLogística S.A." (Dashboard de Comando)

- Abriu: 30/10/2026 às 17:15 - data limite: **20/11/2026 às 23:59**
- Peso: trabalho final do módulo (avaliação: 30% labs assíncronos + 70% trabalho final).
- Dados: `OA10- dados Iniciais.xlsx` (do formador, nesta pasta, fora do Git).
- Projeto **novo**, de raiz: **Ficheiro -> Novo** -> guardar nesta pasta como
  `EdmilsonLandim-dd-mm-yyyy.pbix`. (O `EdmilsonLandim-09-11-2026-oa9.pbix` que está aqui só
  serve para copiar elementos da Landing Page: **Ctrl+C** num ficheiro, **Ctrl+V** no outro.)
- Tema: **Ver -> Temas -> Procurar temas** -> [`dashboard/tema-skodji.json`](dashboard/tema-skodji.json).
- Páginas no fim: **Landing Page** | Análise Financeira | Produtos e Motoristas | Simulação |
  Tooltip Entregas (oculta).

## Os dados (perfil do Excel)
| Folha | Linhas | Colunas | Notas |
|---|---|---|---|
| `Entregas` | 31 | Data, ID Veículo, ID Motorista, Distância (km), Custo Combustível (€), Valor Entrega (€), Status | 15/01/2024 a 15/06/2026; Status `Entregue` (24) / `Atrasado` (7) |
| `Frota` | 3 | ID Veículo, Modelo, Capacidade (kg) | V001 Ford Transit 1200, V002 Mercedes Sprinter 1500, V003 Iveco Daily 2000 |
| `Motoristas` | 10 | ID Motorista, Nome, Região | M01-M10; Norte 4, Centro 3, Sul 3 |
| `Sheet1` | - | cabeçalho + `#NAME?` | **não importar** (folha de lixo) |

Os nomes das colunas no Excel não são iguais aos do enunciado (`Custo Combustível (€)` vs.
`Custo Combustível`, `Valor Entrega (€)` vs. `Valor da Entrega`). O guia renomeia-os no
Power Query para as medidas ficarem como no enunciado.

## Fase 1 - Modelação e limpeza
### 1.1 Importar
1. **Base -> Livro do Excel** -> `OA10- dados Iniciais.xlsx` -> marcar **Entregas**,
   **Frota**, **Motoristas** (não `Sheet1`) -> **Transformar dados**.
2. Consulta **Entregas** -> **Editor Avançado** -> substituir pelo código abaixo (ajustar o
   caminho) -> **Concluído**:

```m
let
    Origem = Excel.Workbook(File.Contents("C:\Skodji Digital\U2-M5 - BI & Cloud Default - Ed2\OA10 - Avaliação e próximos passos\oa-10\lab-assincrono\OA10- dados Iniciais.xlsx"), null, true),
    Entregas_Sheet = Origem{[Item = "Entregas", Kind = "Sheet"]}[Data],
    #"Cabeçalhos promovidos" = Table.PromoteHeaders(Entregas_Sheet, [PromoteAllScalars = true]),
    #"Tipo alterado" = Table.TransformColumnTypes(#"Cabeçalhos promovidos", {
        {"Data", type date}, {"ID Veículo", type text}, {"ID Motorista", type text},
        {"Distância (km)", Int64.Type}, {"Custo Combustível (€)", type number},
        {"Valor Entrega (€)", type number}, {"Status", type text}}),
    #"Colunas renomeadas" = Table.RenameColumns(#"Tipo alterado", {
        {"Distância (km)", "Distância Percorrida (km)"},
        {"Custo Combustível (€)", "Custo Combustível"},
        {"Valor Entrega (€)", "Valor da Entrega"}})
in
    #"Colunas renomeadas"
```

3. **Frota** e **Motoristas**: confirmar cabeçalhos promovidos; `ID Veículo`, `Modelo`,
   `ID Motorista`, `Nome`, `Região` em **Texto**; `Capacidade (kg)` em **Número inteiro**.
   Remover linhas vazias se aparecerem (**Base -> Remover linhas -> Remover linhas em branco**).
4. **Fechar e aplicar**.

### 1.2 Tabela `Calendario` (de raiz, DAX)
**Modelação -> Nova tabela**:

```dax
Calendario = CALENDAR ( DATE ( 2024, 1, 1 ), DATE ( 2026, 12, 31 ) )
```

Os dados vão de 2024 a 2026: a fórmula do OA5 (`YEAR(TODAY())-1`) começaria em 2025 e
perdia 2024. São **1.096 dias** (2024 é bissexto). Depois, **uma coluna de cada vez**
(selecionar `Calendario` -> **Nova coluna**):

```dax
Ano = YEAR ( Calendario[Date] )
```
```dax
Mês Num = MONTH ( Calendario[Date] )
```
```dax
Mês Nome =
VAR m = FORMAT ( Calendario[Date], "MMM", "pt-PT" )
RETURN UPPER ( LEFT ( m, 1 ) ) & MID ( m, 2, 2 )
```
```dax
Trimestre = "T" & QUARTER ( Calendario[Date] )
```

- `Mês Nome` -> **Ferramentas de coluna -> Ordenar por coluna -> Mês Num**.
- `Ano` -> **Resumo: Não resumir**.
- `Calendario` -> **Ferramentas de tabela -> Marcar como tabela de datas** -> coluna `Date`.

### 1.3 Modelo em estrela
**Vista de modelo** -> arrastar (ou **Gerir relações -> Nova**):

| De (1) | Para (*) | Direção |
|---|---|---|
| `Calendario[Date]` | `Entregas[Data]` | Única |
| `Frota[ID Veículo]` | `Entregas[ID Veículo]` | Única |
| `Motoristas[ID Motorista]` | `Entregas[ID Motorista]` | Única |

- Todas **1:\*** com direção de filtro **Única** (critério de avaliação).
- Ocultar na vista de relatório as chaves do lado "muitos": `Entregas[Data]`,
  `Entregas[ID Veículo]`, `Entregas[ID Motorista]` (usar sempre as colunas das dimensões).

### 1.4 Tabela `_Medidas` e métricas base
**Base -> Introduzir dados** -> nome `_Medidas` -> **Carregar**. Criar as medidas (selecionar
`_Medidas` -> **Nova medida**, uma de cada vez) e só depois apagar a `Coluna 1`.

```dax
Total Entregas = COUNTROWS ( Entregas )
```
```dax
Custo Total = SUM ( Entregas[Custo Combustível] )
```
```dax
Faturação Total = SUM ( Entregas[Valor da Entrega] )
```

Formatos: `Total Entregas` número inteiro; `Custo Total` e `Faturação Total` **Moeda (€)**,
2 casas. Conferir: **31**, **1.784,30 €**, **6.060,00 €**.

## Fase 2 - DAX avançado e performance
### 2.1 KPIs
```dax
Margem de Lucro = [Faturação Total] - [Custo Total]
```
```dax
Margem por Entrega = DIVIDE ( [Margem de Lucro], [Total Entregas] )
```
```dax
% Atrasos =
DIVIDE (
    CALCULATE ( [Total Entregas], Entregas[Status] = "Atrasado" ),
    [Total Entregas]
)
```

| Medida | Valor | Formato |
|---|---|---|
| Margem de Lucro | **4.275,70 €** | Moeda, 2 casas |
| Margem por Entrega | **137,93 €** | Moeda, 2 casas |
| % Atrasos | **22,58%** (7 de 31) | Percentagem, 2 casas |

O enunciado chama "Margem por Entrega (Faturação - Custo)" à margem e usa "[Margem de Lucro]"
no cartão: o guia cria as duas. `Margem de Lucro` é o total (Faturação - Custo) e
`Margem por Entrega` divide-o pelo número de entregas.

### 2.2 Inteligência temporal (MoM)
```dax
Faturação LM = CALCULATE ( [Faturação Total], DATEADD ( Calendario[Date], -1, MONTH ) )
```
```dax
Variação MoM % =
VAR lm = [Faturação LM]
RETURN DIVIDE ( [Faturação Total] - lm, lm )
```

- `Faturação LM` (*Last Month*) = faturação do mês anterior; `Variação MoM %` = a variação
  pedida (formato Percentagem, 2 casas). O `VAR` calcula o mês anterior uma só vez (OA9:
  performance com variáveis).
- O `Calendario` vai até Dez 2026: Jul 2026 aparece com Faturação LM 210 € e -100%. Na
  matriz, juntar o filtro do visual **`Faturação Total` não está em branco**.
- Só dá valores certos num visual com **Ano e Mês** (ou com filtro de ano). Com `Mês Nome`
  sozinho, cada mês junta 2024, 2025 e 2026.

Conferir numa matriz com `Ano` e `Mês Nome`:

| Mês | Faturação | Faturação LM | Variação MoM % |
|---|---|---|---|
| Jan 2024 | 280 € | - | vazio |
| Fev 2024 | 280 € | 280 € | 0,00% |
| Mar 2024 | 175 € | 280 € | -37,50% |
| Jan 2026 | 150 € | 180 € (Dez 2025) | -16,67% |
| Fev 2026 | 290 € | 150 € | 93,33% |
| Mar 2026 | 195 € | 290 € | -32,76% |
| Abr 2026 | 125 € | 195 € | -35,90% |
| Mai 2026 | 260 € | 125 € | 108,00% |
| Jun 2026 | 210 € | 260 € | -19,23% |

### 2.3 Ranking dos motoristas
```dax
Ranking Motoristas =
IF (
    ISINSCOPE ( Motoristas[Nome] ),
    RANKX ( ALL ( Motoristas ), [Total Entregas], , DESC, Dense )
)
```

`ALL ( Motoristas )` e não `ALL ( Motoristas[Nome] )`: numa tabela que também tem `Região`,
o `ALL` só da coluna Nome deixa o filtro da região ativo e o ranking passa a ser **dentro de
cada região** (Elsa 1, Diogo 1, Ana 1, Carla 2...). Com a tabela inteira, o ranking é global.

| Ranking | Motorista | Região | Entregas |
|---|---|---|---|
| 1 | Elsa Teixeira (M10) | Centro | 7 |
| 2 | Diogo Almeida (M09) | Sul | 4 |
| 3 | Ana Oliveira (M04), Carla Fernandes (M08), João Silva (M01), Ricardo Pereira (M05) | | 3 cada |
| 4 | Bruno Rocha (M07), Maria Santos (M02), Pedro Costa (M03), Sofia Martins (M06) | | 2 cada |

Com `Skip` em vez de `Dense`, os empatados com 3 ficam em 3.º e os seguintes em **7.º**.

### 2.4 Parâmetro de campo + página Simulação
1. Nova página -> nome **`Simulação`** (enunciado: "Altere o nome da página para Simulação").
2. **Modelação -> Novo parâmetro -> Campos** -> nome **`Métrica a Analisar`** -> campos
   `_Medidas[Total Entregas]` e `_Medidas[Faturação Total]` -> **Adicionar segmentação a esta
   página** ligado -> **Criar**.
3. Segmentação -> **Definições da segmentação -> Seleção -> Seleção única** ligado.

## Parte 3 - Base visual ("Dashboard de Comando")
Fundos em [`dashboard/`](dashboard/): **Formatar página -> Fundo da tela** -> imagem,
**Ajustar**, transparência 0%; nos visuais desligar **Título** e **Fundo** (os títulos estão
no fundo). Posições em px do Power BI (página 1280 x 720).

### 3.1 Página "Análise Financeira"
[`mockup-analise-financeira.png`](dashboard/mockup-analise-financeira.png) /
`fundo-analise-financeira.png`

| Visual | Campos | X | Y | Larg. | Alt. | Valor esperado |
|---|---|---|---|---|---|---|
| Cartão - Custo Total *(opcional)* | `[Custo Total]` | 38 | 122 | 270 | 50 | 1.784,30 € |
| Cartão - Margem por Entrega *(opcional)* | `[Margem por Entrega]` | 350 | 122 | 270 | 50 | 137,93 € |
| Cartão - % Atrasos *(opcional)* | `[% Atrasos]` | 662 | 122 | 270 | 50 | 22,58% |
| Cartão - Distância *(opcional)* | `Entregas[Distância Percorrida (km)]` Soma | 974 | 122 | 270 | 50 | 4.685 km |
| **Colunas empilhadas** (pedido) | Eixo X `Mês Nome`; Eixo Y `[Faturação Total]`, `[Custo Total]` | 34 | 242 | 756 | 444 | tabela abaixo |
| **Cartão de várias linhas** (pedido) | `[Total Entregas]`, `[Faturação Total]`, `[Margem de Lucro]` | 826 | 242 | 420 | 160 | 31 / 6.060,00 € / 4.275,70 € |
| **Matriz** (pedido) | Linhas `Região`; Colunas `ID Motorista` (Motoristas); Valores `[Total Entregas]` | 826 | 478 | 420 | 208 | tabela abaixo |

Gráfico de colunas empilhadas (todos os anos somados por mês):

| Mês | Jan | Fev | Mar | Abr | Mai | Jun | Jul | Ago | Set | Out | Nov | Dez |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Faturação | 575 | 855 | 555 | 355 | 755 | 600 | 280 | 610 | 325 | 255 | 545 | 350 |
| Custo | 169,7 | 246,1 | 173 | 99 | 222,5 | 187 | 81 | 173 | 98 | 72 | 157 | 106 |

Matriz Região x ID Motorista (Total Entregas):

| Região | M01 | M02 | M03 | M04 | M05 | M06 | M07 | M08 | M09 | M10 | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Centro | | 2 | | | | 2 | | | | 7 | 11 |
| Norte | 3 | | | 3 | 3 | | 2 | | | | 11 |
| Sul | | | 2 | | | | | 3 | 4 | | 9 |
| **Total** | 3 | 2 | 2 | 3 | 3 | 2 | 2 | 3 | 4 | 7 | **31** |

- "Cartão de várias linhas" está no painel Visualizações (em versões novas também serve o
  **Cartão (novo)** com as 3 medidas).
- Nas colunas empilhadas o custo fica por cima da faturação: o topo da coluna (ex.: Fev 1.101)
  não é um valor de negócio. É o pedido do enunciado; os rótulos dentro de cada segmento é que
  contam.

### 3.2 Página "Produtos e Motoristas"
[`mockup-produtos-motoristas.png`](dashboard/mockup-produtos-motoristas.png) /
`fundo-produtos-motoristas.png`

| Visual | Campos | X | Y | Larg. | Alt. | Valor esperado |
|---|---|---|---|---|---|---|
| Cartão - Motoristas *(opcional)* | `Motoristas[ID Motorista]` Contagem | 38 | 122 | 270 | 50 | 10 |
| Cartão - Veículos *(opcional)* | `Frota[ID Veículo]` Contagem | 350 | 122 | 270 | 50 | 3 |
| Cartão - Motorista Nº 1 *(opcional)* | `Motoristas[Nome]` + filtro N Superior 1 por `[Total Entregas]` | 662 | 122 | 270 | 50 | Elsa Teixeira |
| Cartão - Entregas do Nº 1 *(opcional)* | `[Total Entregas]` + o mesmo filtro | 974 | 122 | 270 | 50 | 7 |
| **Barras (ranking)** (pedido) | Eixo Y `Motoristas[Nome]`; Eixo X `[Total Entregas]`; filtro **N Superior 5** | 34 | 242 | 756 | 444 | 6 barras (empate) |
| **Tabela de detalhe** (pedido) | `Frota[ID Veículo]`, `Frota[Modelo]`, `[Total Entregas]` + **barras de dados** | 826 | 242 | 420 | 160 | V001 11, V002 10, V003 10 |
| Tabela - ranking *(opcional)* | `Nome`, `Região`, `[Total Entregas]`, `[Ranking Motoristas]` | 826 | 478 | 420 | 208 | tabela 2.3 |

- **Filtro Top 5**: selecionar o gráfico -> painel **Filtros -> Filtros neste visual** ->
  `Nome` -> **Tipo de filtro: N Superior** -> **Superior 5** -> **Por valor**: arrastar
  `[Total Entregas]` -> **Aplicar filtro**.
- **Aparecem 6 barras e está certo**: Elsa 7, Diogo 4 e quatro motoristas empatados com 3
  (Ana, Carla, João, Ricardo). O N Superior inclui todos os empatados na 5.ª posição.
- **Barras de dados**: na tabela, seta em `Total Entregas` (área **Colunas**) ->
  **Formatação condicional -> Barras de dados** -> barra positiva `#8FD3F2` -> OK.
- Usar `Frota[ID Veículo]` (dimensão) e não `Entregas[ID Veículo]` para o `Modelo` filtrar
  corretamente.

### 3.3 Página "Simulação"
[`mockup-simulacao.png`](dashboard/mockup-simulacao.png) / `fundo-simulacao.png`

| Visual | Campos | X | Y | Larg. | Alt. | Valor esperado |
|---|---|---|---|---|---|---|
| Cartões *(opcionais)* | Total Entregas, Faturação Total, Faturação/Entrega, Jun 2026 | 38 / 350 / 662 / 974 | 122 | 270 | 50 | 31 / 6.060 € / 195,48 € / 210 € |
| **Colunas** (pedido) | Eixo X `Mês Nome`; Eixo Y **`Métrica a Analisar`** | 34 | 242 | 756 | 444 | Faturação: 575 ... 350; Entregas: 4, 3, 3, 3, 3, 3, 2 ... 2 |
| **Segmentação** `Métrica a Analisar` | seleção única | 826 | 242 | 420 | 160 | |
| Matriz MoM *(opcional)* | `Ano`, `Mês Nome`; `[Faturação Total]`, `[Faturação LM]`, `[Variação MoM %]`; filtro Ano = 2026 | 826 | 478 | 420 | 208 | tabela 2.2 |

Medidas dos cartões opcionais (em `_Medidas`):

```dax
Faturação Média por Entrega = DIVIDE ( [Faturação Total], [Total Entregas] )
```
```dax
Faturação Último Mês =
VAR ultimaData = MAX ( Entregas[Data] )
RETURN
    CALCULATE (
        [Faturação Total],
        Calendario[Ano] = YEAR ( ultimaData ),
        Calendario[Mês Num] = MONTH ( ultimaData )
    )
```

- `MAX(Entregas[Data])` = 15/06/2026 (a última entrega); o `CALCULATE` soma a faturação desse
  ano e mês: **210 €** (Moeda, 0 casas). Fica dinâmico: com novos dados passa sozinho para o
  mês seguinte; com um filtro Ano = 2025 mostra Dez 2025 (180 €).
- Rótulo dinâmico opcional (para não ter "JUN 2026" fixo no fundo): medida
  `Rótulo Último Mês = "ÚLTIMO MÊS (" & UPPER ( FORMAT ( MAX ( Entregas[Data] ), "mmm yyyy", "pt-PT" ) ) & ")"`
  -> Cartão -> **Rótulo da categoria** desligado -> **Título** ligado -> **fx** -> Valor do
  campo -> esta medida.

## Fase 3 - UX/UI e experiência "App"
### 3.1 Landing Page
[`mockup-landing.png`](dashboard/mockup-landing.png) / `fundo-landing.png`

1. Nova página **`Landing Page`** -> arrastar para o início -> botão direito ->
   **Definir como página de destino**.
2. **Caixa de texto** (Inserir -> Caixa de texto) com **"Relatório"**: X 40, Y 110,
   600 x 80, branco, 54 pt, negrito.
3. **Navegador de páginas** (Inserir -> Botões -> Navegador -> Navegador de páginas):
   X 64, Y 352, 1152 x 64, horizontal, espaçamento 16; **Páginas -> Mostrar páginas ocultas**
   ligado; desligar `Landing Page` e `Tooltip Entregas`. Estilo como no OA9 (preenchimento
   `#1E55A2`, texto branco 16 negrito; ao pairar `#32B2E7`).
4. Cartões *(opcionais)*: Total Entregas 31, Faturação Total 6.060 €, Margem de Lucro
   4.275,70 €, % Atrasos 22,58% (X 54 / 358 / 662 / 966, Y 540, 260 x 50).

### 3.2 Botão Voltar
**Inserir -> Botões -> Voltar** em Análise Financeira, Produtos e Motoristas e Simulação
(não na tooltip): X 880, Y 18, 90 x 36, texto "Início", Ação **Voltar** (ou **Navegação de
página -> Landing Page**). Criar num e copiar/colar nos outros.

### 3.3 Tooltip personalizada
[`mockup-tooltip.png`](dashboard/mockup-tooltip.png) (exemplo: Elsa Teixeira)

1. Nova página **`Tooltip Entregas`** -> **Ocultar página**.
2. **Formatar página -> Informações da página -> Tipo de página: Descrição** (320 x 240).
3. **Cartão** `[Total Entregas]`: X 0, Y 0, 320 x 70.
4. **Gráfico de linhas**: Eixo X `Mês Nome`; Eixo Y `[Faturação Total]`: X 0, Y 70, 320 x 170.

### 3.4 Ligar a tooltip ao gráfico de barras
Página **Produtos e Motoristas** -> selecionar o gráfico de barras -> **Formatar visual ->
Geral -> Descrições** -> **Tipo: Página de relatório** -> **Página: Tooltip Entregas**.

Testar (passar o rato): **Elsa Teixeira** -> 7; Fev 855 €, Abr 125 €, Mai 255 €, Ago 610 €.
**Diogo Almeida** -> 4; Jan 130 €, Set 160 €, Out 125 €, Nov 270 €.

## Fase 4 - Publicação e partilha
1. Ocultar **Análise Financeira**, **Produtos e Motoristas**, **Simulação** (a tooltip já está
   oculta). Fica visível só a **Landing Page**; confirmar que os 3 botões do navegador
   continuam lá.
2. Selecionar a Landing Page -> **Ctrl+S** -> **Base -> Publicar -> O meu espaço de trabalho**.
3. Testar em app.powerbi.com (botões, Início, tooltip, segmentação).
4. Submeter o `.pbix` no Moodle (se não for possível publicar, só submeter o ficheiro).

## Critérios de avaliação - auto-verificação
| Critério | Como confirmar |
|---|---|
| **Modelo** em estrela, relações unidirecionais | Vista de modelo: 3 dimensões (Calendario, Frota, Motoristas) ligadas a Entregas, todas 1:\* e seta única |
| **DAX** explícito | Nenhum visual usa somas automáticas de colunas (exceto o cartão opcional da distância: trocar por uma medida `Distância Total = SUM(...)` para ficar 100% explícito) |
| **Performance** | `% Atrasos` com `CALCULATE` + `DIVIDE`; `Margem por Entrega` e `Variação MoM %` com `DIVIDE`; `VAR` na variação |
| **UX** | Landing Page de entrada, navegador, botão Início em todas as páginas, tooltip personalizada, páginas ocultas |

## Evidências
Guardar em [`evidencias/`](evidencias/):
- `01-modelo.png` - vista de modelo (estrela)
- `02-medidas.png` - painel Dados com `_Medidas`
- `03-landing-page.png`, `04-analise-financeira.png`, `05-produtos-motoristas.png`,
  `06-simulacao.png`, `07-tooltip.png` (descrição aberta sobre uma barra)
- `08-publicar-sucesso.png`, `09-submissao-moodle.png`

## Estado
- [x] Fase 1 - importação, Calendario (2024-2026), modelo em estrela, `_Medidas` + 3 medidas base ([`EdmilsonLandim-10-11-2026.pbix`](EdmilsonLandim-10-11-2026.pbix))
- [x] Fase 2 - Margem, % Atrasos, Faturação LM / Variação MoM %, Ranking, parâmetro de campo
- [x] Parte 3 - páginas Análise Financeira, Produtos e Motoristas, Simulação ([`04`](evidencias/04-analise-financeira.png), [`05`](evidencias/05-produtos-motoristas.png), [`06`](evidencias/06-simulacao.png))
- [x] Fase 3 - Landing Page ([`03`](evidencias/03-landing-page.png)), botão Início no logótipo Skodji ([`07b`](evidencias/07b-botao-inicio-logo.png)), tooltip ligada às barras ([`07`](evidencias/07-tooltip.png))
- [x] Fase 4 - páginas ocultas, publicado em O meu espaço de trabalho ([`08`](evidencias/08-publicar-sucesso.png))
- [x] Submetido no Moodle (10/11/2026 15:54) - [`09`](evidencias/09-submissao-moodle.png)

Correções recomendadas antes do prazo (Moodle -> **Editar submissão** até 20/11/2026):
- [x] Simulação: o cartão **Total Entregas** mostra **10** (deve ser **31**): usar a medida `[Total Entregas]`
- [x] Produtos e Motoristas: **Ranking** por região (1, 1, 1, 2...): trocar para `ALL ( Motoristas )` (secção 2.3) - [`05b`](evidencias/05b-ranking-corrigido.png)
- [x] Simulação: matriz MoM com Jul 2026 a -100%: filtro `Faturação Total` não está em branco - [`06b`](evidencias/06b-matriz-mom-filtro.png)
- [ ] Opcionais: cartão de várias linhas com **Unidades de apresentação = Nenhuma** (6.060,00 € em vez de 6 K €); medida `Distância Total = SUM ( Entregas[Distância Percorrida (km)] )` em vez da soma implícita
