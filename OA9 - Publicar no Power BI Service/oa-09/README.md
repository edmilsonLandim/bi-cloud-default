# OA9 - Publicar e partilhar relatórios no Power BI Service

## Sumário
- Criar Landing page (página de entrada).
- Inserir e formatar elementos.
- Utilizar o Power BI Service.
- Tipo de contas.
- Criar Workspaces (Áreas de trabalho).
- Publicar e partilhar o relatório.

## Calendário
| Atividade | Estado |
|---|---|
| Pré-teste | concluído |
| Lab síncrono | concluído |
| Lab assíncrono | concluído (submetido no Moodle 09/11/2026) |
| Pós-teste | concluído |

## Conceitos da aula
Resumo dos materiais de estudo nesta pasta (`Power_BI_Deployment_Blueprint_compressed.pdf`,
14 diapositivos, e o infográfico `Guia_de_Design_e_Publicação.png`):

| Conceito | Regra prática |
|---|---|
| **A última milha** | 4 módulos: UX/UI (Landing Page e navegação), Ecossistema Cloud (relatório vs. modelo), Segurança e distribuição (permissões), Performance DAX (variáveis) |
| **Landing Page de excelência** | Fundo (imagem com transparência ~60% para não competir com a navegação), título principal, logótipo com **URL da Web** e descrição personalizada ("Saiba mais"), página de entrada definida com botão direito no separador |
| **Navegação centralizada** | **Inserir -> Botões -> Navegador -> Navegador de páginas**: cria os botões a partir dos nomes das páginas. Todas as páginas de destino têm um botão **Voltar**. No Desktop: **Ctrl + clique**; no Service: clique simples |
| **Perigo do .pbix** | Enviar o ficheiro dá acesso total ao modelo, ao ETL e às tabelas, e gera versões divergentes. Partilhar só via **Publicar** |
| **Divisão no Service** | Ao publicar, o .pbix divide-se em **Relatório** (camada visual, partilhada com o consumidor) e **Modelo semântico** (dados e medidas, fonte única da verdade) |
| **Workspaces** | **O meu espaço de trabalho**: cofre pessoal (contas gratuitas). Áreas de trabalho de equipa (Vendas, RH, Marketing): só com Pro/PPU |
| **Licenças** | Free: e-mail profissional/académico, só My Workspace, sem partilha direta. Pro (~14 €/mês): workspaces e partilha com outros Pro. PPU (~2x Pro): partilha universal. Trial Pro de 60 dias |
| **Formas de partilha** | **Publicar na Web**: segurança nula, grátis, só dados públicos. **Acesso direto**: segurança alta, Pro/PPU, permissões granulares. **Subscrições**: envio periódico por e-mail com snapshot |
| **Modo de apresentação** | **Ecrã inteiro** (Ver -> Ecrã inteiro), **Modo de foco** (um visual), **Destaque/Spotlight** (... -> Destaque: esbate o resto) |
| **Títulos dinâmicos** | `VAR ano = SELECTEDVALUE(Calendar[Year])` + `&` para texto; segmentação em seleção única; `IF` para anos sem homólogo. Título -> **fx** -> Valor do campo |
| **DAX com variáveis** | `VAR ... RETURN`: calcula uma vez e reutiliza (em vez de repetir `SELECTEDVALUE` 4 vezes) |
| **Checklist de deployment** | 1) UX/UI: navegação e Landing Page; 2) Performance: VAR/RETURN, seleção única; 3) Cloud: .pbix local, partilha pelo Service; 4) Segurança: Publicar na Web bloqueado para dados sensíveis |

## Lab síncrono
Concluído na sessão. Ficheiro do formador: `lab-sincrono/Modelo 27-10-2026.pbix` (fora do Git).

## Lab assíncrono
Enunciado e guia: [`lab-assincrono/README.md`](lab-assincrono/README.md) - "App" LusaTech:
Landing Page com logótipo e navegador de páginas, botões Voltar, páginas ocultas,
publicação em O meu espaço de trabalho e Publicar na Web.

## Estado
- [x] Pré-teste - concluído
- [x] Lab síncrono - concluído
- [x] Lab assíncrono - `EdmilsonLandim-09-11-2026-oa9.pbix` (Landing Page, navegação, páginas ocultas); publicado no Power BI Service e submetido no Moodle (09/11/2026)
- [x] Pós-teste - concluído
