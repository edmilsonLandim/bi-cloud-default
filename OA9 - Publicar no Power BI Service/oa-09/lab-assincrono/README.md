# OA9 - Lab Assíncrono: A "App" LusaTech (Landing Page, navegação e publicação)

- Abriu: 29/10/2026 às 19:45 - data limite: 20/11/2026 às 23:59
- Base: o exercício do OA8 (LusaTech). Usar o próprio:
  [`../../../OA8 - Formatação condicional avançada e parâmetros/oa-08/lab-assincrono/EdmilsonLandim-09-11-2026.pbix`](../../../OA8%20-%20Formatação%20condicional%20avançada%20e%20parâmetros/oa-08/lab-assincrono/EdmilsonLandim-09-11-2026.pbix)
  -> **Guardar como** `EdmilsonLandim-dd-mm-yyyy.pbix` **nesta pasta**. Alternativa do
  formador: `OA8-Exercicio resolvido.pbix`.
- Logótipo: `LusaTeck.png` (do formador, nesta pasta) ou a versão recortada com fundo
  transparente [`dashboard/logo-lusatech.png`](dashboard/logo-lusatech.png).
- Páginas do relatório no fim: **Landing Page** | Faturação | Matriz | Produtos |
  Tooltip_Produto | Simulação.

## Parte 1 - Landing Page (a "Home")
1. **+** (nova página) -> nome **`Landing Page`**.
2. Arrastar o separador para o **início** (à esquerda de Faturação). Botão direito no
   separador -> **Definir como página de destino** (*Set as landing page*; o nome exato
   varia com a versão). Sem esta opção, o relatório abre na página ativa quando se guarda:
   guardar e publicar sempre com a Landing Page selecionada.
3. **Fundo**: clicar numa zona vazia -> **Formatar página -> Fundo da tela** -> imagem
   [`dashboard/fundo-landing.png`](dashboard/fundo-landing.png), Ajuste **Ajustar**,
   transparência **0%**. (Alternativa do enunciado: cor sólida; o material de estudo
   sugere imagem com transparência 60% se for uma fotografia.)
4. **Navegador de páginas**: **Inserir -> Botões -> Navegador -> Navegador de páginas**.
   - **Geral -> Propriedades**: X 64, Y 352, Largura 1152, Altura 64.
   - **Visual -> Grelha de layout**: orientação **Horizontal**, espaçamento 16.
   - **Visual -> Páginas**: **Mostrar páginas ocultas** = **Ligado** (ver Parte 2) e desligar
     `Landing Page` e `Tooltip_Produto` na lista. Ficam 4 botões: Faturação, Matriz,
     Produtos, Simulação.
   - **Visual -> Estilo**: Estado **Predefinido** -> Preenchimento `#1E55A2`, texto branco,
     Poppins/Segoe UI SemiBold 16, cantos arredondados 10; Estado **Ao pairar** ->
     preenchimento `#32B2E7`; Estado **Selecionado** -> `#163F7A`.
5. **Logótipo**: **Inserir -> Imagem** -> `LusaTeck.png` (ou `logo-lusatech.png`) ->
   canto superior esquerdo, dentro do cartão branco do fundo: X 48, Y 26, 244 x 112.
   Opcional (material de estudo, "ponto de fuga web"): **Formatar imagem -> Ação** ->
   Tipo **URL da Web** com o site da empresa.
6. **Botão Voltar em todas as outras páginas** (Faturação, Matriz, Produtos, Simulação;
   **não** na Tooltip_Produto):
   - Em Faturação: **Inserir -> Botões -> Voltar**. **Ação** -> Tipo **Voltar** (regressa à
     página anterior). Alternativa mais previsível: Tipo **Navegação de página** ->
     Destino **Landing Page**.
   - Posição no cabeçalho, entre o subtítulo e a faixa da marca: X 880, Y 18, 90 x 36;
     texto **Início**, preenchimento branco, ícone/texto `#1E55A2`
     ([`dashboard/mockup-botao-voltar.png`](dashboard/mockup-botao-voltar.png)).
   - Copiar o botão (**Ctrl+C**) e colar (**Ctrl+V**) nas outras 3 páginas: fica na mesma
     posição.
7. Testar no Desktop: **Ctrl + clique** nos botões (no Service basta um clique).

Valores dos cartões opcionais da Landing Page (posições no mockup): Faturação Total
**16.050 €**, Margem de Lucro **9.645 €**, Produtos **5** (Contagem distinta de ID
Produto), Período **Jan 2025 - Mai 2026** (caixa de texto).

## Parte 2 - Preparar a publicação
1. **Ocultar** (botão direito no separador -> **Ocultar página**): Faturação, Matriz,
   Produtos, Simulação. A `Tooltip_Produto` já está oculta. Fica visível só a **Landing Page**.
   - **Armadilha**: por defeito, o navegador de páginas **não mostra páginas ocultas**.
     Depois de ocultar, os botões desaparecem se **Mostrar páginas ocultas** não estiver
     ligado (passo 1.4).
2. Selecionar a Landing Page, **Ctrl+S** e **Base -> Publicar -> O meu espaço de trabalho**.
   Se perguntar, **Substituir** o conjunto de dados com o mesmo nome.
3. Verificar em [app.powerbi.com](https://app.powerbi.com): **O meu espaço de trabalho** ->
   abrir o relatório.
   - Abre na Landing Page? O painel **Páginas** só mostra a Landing Page?
   - Cada botão abre a página certa? O **Início** volta à Landing Page?
   - A descrição (tooltip) da página Faturação e os segmentadores (Métrica, Simulação)
     continuam a funcionar?

## Parte 3 - Publicar na Web (público)
1. No relatório, no Service: **Ficheiro -> Incorporar relatório -> Publicar na Web
   (público)**.
2. Ler o aviso -> **Criar código de incorporação** -> **Publicar**. Copiar o **link**
   (não o código HTML do iframe).
3. Testar numa **janela anónima** (Ctrl+Shift+N no Chrome/Edge): o relatório abre e é
   interativo sem início de sessão.

- Só com dados de demonstração (como estes). O link fica acessível a qualquer pessoa e
  não tem controlo de acesso (material de estudo: "Segurança: Nula").
- Se aparecer **"Contacte o administrador"**, o administrador da organização tem a
  opção Publicar na Web desativada (comum em contas de escola/empresa). Nesse caso, fazer
  uma captura da mensagem para a evidência e indicar no Moodle.
- Para remover o link depois: **Definições (roda dentada) -> Gerir códigos de
  incorporação** -> **Eliminar**.

Link público: *(colar aqui depois de gerado)*

## Mockups (identidade Skodji Digital)
Ficheiros em [`dashboard/`](dashboard/): `fundo-landing.png`, `mockup-landing.png`,
`mockup-botao-voltar.png`, `logo-lusatech.png`, `tema-skodji.json`.

| Elemento | Tipo | X | Y | Largura | Altura |
|---|---|---|---|---|---|
| Logótipo LusaTech | Imagem | 48 | 26 | 244 | 112 |
| Navegador de páginas | Botões -> Navegador | 64 | 352 | 1152 | 64 |
| Cartão Faturação Total | Cartão (opcional) | 54 | 540 | 260 | 50 |
| Cartão Margem de Lucro | Cartão (opcional) | 358 | 540 | 260 | 50 |
| Cartão Produtos | Cartão (opcional) | 662 | 540 | 260 | 50 |
| Período | Caixa de texto (opcional) | 966 | 540 | 260 | 50 |
| Botão Voltar (restantes páginas) | Botões -> Voltar | 880 | 18 | 90 | 36 |

## Evidências
Guardar em [`evidencias/`](evidencias/):
- `01-landing-page.png` - Landing Page no Desktop (logótipo + navegador)
- `02-paginas-ocultas.png` - separadores com as páginas ocultas (ícone do olho riscado)
- `03-publicar-sucesso.png`
- `04-service-navegacao.png` - relatório aberto em app.powerbi.com (Landing Page ou uma
  página aberta pelo botão)
- `05-publicar-na-web.png` - janela com o link (ou a mensagem do administrador)
- `06-janela-anonima.png` - relatório aberto pelo link público em modo anónimo
- `07-submissao-moodle.png`

## Estado
- [x] Parte 1 - Landing Page (primeira, página de destino), fundo, navegador, logótipo - [`evidencias/01-landing-page.png`](evidencias/01-landing-page.png)
- [x] Parte 1.6 - botão Voltar em Faturação, Matriz, Produtos, Simulação
- [x] Parte 2 - páginas ocultas (exceto Landing Page), publicado em O meu espaço de trabalho ([`EdmilsonLandim-09-11-2026-oa9.pbix`](EdmilsonLandim-09-11-2026-oa9.pbix), [`evidencias/03-publicar-sucesso.png`](evidencias/03-publicar-sucesso.png))
- [x] Parte 3 - Publicar na Web (sem captura do link no repositório)
- [x] Submetido no Moodle (09/11/2026 16:25) - [`evidencias/07-submissao-moodle.png`](evidencias/07-submissao-moodle.png)
