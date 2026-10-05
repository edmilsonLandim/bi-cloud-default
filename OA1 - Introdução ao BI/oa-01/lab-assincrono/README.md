# OA1 - Lab Assíncrono: Introdução ao Power BI

- Data limite: 20/11/2026 às 23:59
- Ficheiro de entrega: `EdmilsonLandim_dd-mm-yyyy.pbix` (nome + data do dia)
- Dados: `Dados Colaboradores Exemplo.xlsx` - tabela `Tabela1` (folha `Folha1`),
  101 pessoas, 7 colunas

## Parte 1 - Criação do relatório e importação de dados
1. Power BI Desktop -> **Ficheiro -> Novo** -> **Guardar como**
   `EdmilsonLandim_dd-mm-yyyy.pbix` nesta pasta.
2. **Livro do Excel** -> `Dados Colaboradores Exemplo.xlsx` -> no Navegador
   selecionar **Tabela1** -> **Transformar Dados** (não "Carregar", para abrir o
   Power Query).

## Parte 2 - Transformação no Power Query
1. **Género: M -> Masculino, F -> Feminino**
   Selecionar a coluna `Género` -> Base -> **Substituir Valores**:
   - Valor a localizar `M`, substituir por `Masculino`
   - Repetir para `F` -> `Feminino`
   - Em *Opções avançadas*, marcar **Corresponder ao conteúdo de célula inteira**
     (evita substituir a letra dentro de outros textos).
2. **Colunas de data -> tipo Data**
   `Data de entrada` e `Data Nascimento` vêm do Excel como números (ex.: 44915),
   porque as células estão em formato "Geral". Clicar no ícone do tipo no
   cabeçalho de cada coluna -> **Data**. O número converte-se na data correta
   (44915 -> 20/12/2022).
3. **Base -> Fechar e Aplicar**.

Código M esperado (Base -> Editor Avançado), para conferir:

```m
let
    Origem = Excel.Workbook(File.Contents("...\Dados Colaboradores Exemplo.xlsx"), null, true),
    Tabela1_Table = Origem{[Item="Tabela1",Kind="Table"]}[Data],
    #"Tipo Alterado" = Table.TransformColumnTypes(Tabela1_Table,{
        {"Nº de Entrada", Int64.Type}, {"Data de entrada", type date},
        {"Nome do Cliente", type text}, {"Área  de Inscrição", type text},
        {"Freguesia", type text}, {"Género", type text},
        {"Data Nascimento", type date}}),
    #"Valor Substituído" = Table.ReplaceValue(#"Tipo Alterado","M","Masculino",Replacer.ReplaceValue,{"Género"}),
    #"Valor Substituído1" = Table.ReplaceValue(#"Valor Substituído","F","Feminino",Replacer.ReplaceValue,{"Género"})
in
    #"Valor Substituído1"
```

Nota: a coluna `Área  de Inscrição` tem **dois espaços** entre "Área" e "de"
no Excel original.

## Parte 3 - Relatório no Power BI Desktop
1. **Cartão - número de pessoas**: visual *Cartão* -> arrastar `Nº de Entrada`
   -> no campo, mudar a agregação para **Contagem** (ou **Contagem (Distinta)**).
   Resultado esperado: **101**. Título sugerido: "Número de Pessoas".
2. **Gráfico de barras - pessoas por Área de Inscrição**: visual *Gráfico de
   barras agrupadas* -> Eixo Y: `Área  de Inscrição`; Eixo X: `Nº de Entrada`
   (Contagem). Resultado esperado:

   | Área de Inscrição | Pessoas |
   |---|---|
   | Assistente Administrativo | 27 |
   | Profissional de Apoio na Área Administrativa | 21 |
   | Operador de Jardinagem | 18 |
   | Formação para a vida ativa e Profissional | 18 |
   | Empregado de Andares | 17 |

3. **Publicar** (Base -> Publicar -> "A minha área de trabalho"), se a conta
   permitir. Guardar captura do relatório no Power BI Service em `evidencias/`.
4. Submeter o `.pbix` no Moodle.

Verificação extra: por género, 55 Feminino e 46 Masculino.

## Dashboard com a identidade Skodji Digital
Ficheiros em [`dashboard/`](dashboard/):
- `mockup-dashboard.png` - aspeto final pretendido (valores reais dos dados)
- `fundo-dashboard.png` - fundo para a tela (1920x1080, 16:9), com cabeçalho,
  ícone à esquerda, logótipo `logo.svg` à direita, títulos e cartões já desenhados
- `tema-skodji.json` - tema com as cores da marca (azul `#1E55A2`, ciano `#32B2E7`)

### 1. Tema e fundo
1. **Ver -> Temas -> Procurar temas** -> `tema-skodji.json`.
2. Clicar numa zona vazia da tela -> painel **Formatar página**:
   - *Definições da tela*: Tipo **16:9** (1280 x 720)
   - *Fundo da tela*: **Imagem** -> Procurar -> `fundo-dashboard.png`;
     Ajuste da imagem **Ajustar**; Transparência **0%**
   - *Fundo do papel de parede*: cor `#ECEFF4`

### 2. Visuais e posições
Para todos os visuais, em **Formatar -> Geral**: desligar **Título** e
**Fundo** (os títulos e os cartões brancos já estão no fundo). Posição e tamanho
em **Geral -> Propriedades -> Tamanho e posição**:

| Visual | Campos | X | Y | Largura | Altura |
|---|---|---|---|---|---|
| Cartão - Total de pessoas | Contagem de `Nº de Entrada` | 38 | 122 | 270 | 50 |
| Cartão - Feminino | Contagem de `Nº de Entrada` + filtro do visual `Género` = Feminino | 350 | 122 | 270 | 50 |
| Cartão - Masculino | Contagem de `Nº de Entrada` + filtro do visual `Género` = Masculino | 662 | 122 | 270 | 50 |
| Cartão - Áreas de inscrição | Contagem (Distinta) de `Área  de Inscrição` | 974 | 122 | 270 | 50 |
| Barras - Pessoas por Área | Eixo Y `Área  de Inscrição`; Eixo X Contagem de `Nº de Entrada` | 34 | 242 | 756 | 444 |
| Anel - Género | Legenda `Género`; Valores Contagem de `Nº de Entrada` | 826 | 242 | 420 | 160 |
| Barras - Top 3 Freguesias | Eixo Y `Freguesia`; Eixo X Contagem de `Nº de Entrada`; filtro **N Principais = 3** | 826 | 478 | 420 | 208 |

Nos cartões: desligar o **Rótulo da categoria** e alinhar o valor à esquerda.
Nos gráficos de barras: ligar **Rótulos de dados** e desligar o título dos eixos.
No anel: Feminino em ciano `#32B2E7` e Masculino em azul `#1E55A2`.

### Qualidade dos dados (extra)
A coluna `Freguesia` tem `Serzedo - VNG` (5) e `Serzedo - VNGaia` (1), que são a
mesma freguesia. Pode uniformizar no Power Query com **Substituir Valores**
(`Serzedo - VNGaia` -> `Serzedo - VNG`, célula inteira). Não altera o Top 3.

## Evidências
Guardar em [`evidencias/`](evidencias/):
- `01-dados-transformados.png` - vista de tabela: Género por extenso, datas em tipo Data
- `02-relatorio.png` - dashboard final no Power BI Desktop

Código M final da consulta: [`power-query.m`](power-query.m).
- `03-publicar-sucesso.png` - publicação concluída a partir do Power BI Desktop
- `04-power-bi-service.png` - relatório aberto em app.powerbi.com ("A minha área de trabalho")
- `05-submissao-moodle.png` - submissão no Moodle (Submetido para avaliação, 05/10/2026 13:04)

## Estado
- [x] Parte 1 - ficheiro criado e dados importados (`EdmilsonLandim_05-10-2026.pbix`)
- [x] Parte 2 - Género substituído, datas em tipo Data
- [x] Parte 3 - cartão (101) e gráfico de barras, dashboard com identidade Skodji
- [x] Publicado no Power BI Service ("A minha área de trabalho")
- [x] Submetido no Moodle - 05/10/2026 13:04, 46 dias antes do prazo
