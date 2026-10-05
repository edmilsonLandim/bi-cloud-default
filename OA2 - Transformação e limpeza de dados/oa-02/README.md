# OA2 - Principais ferramentas de transformação e limpeza de dados. Utilizar o processo Append Queries

## Sumário
- Identificar e aplicar as principais ferramentas de tratamento e limpeza de dados.
- Aplicar o processo de Append Queries.

## Calendário
| Atividade | Abre | Fecha |
|---|---|---|
| Pré-teste | 04/10/2026 00:01 | - (conta a nota mais alta) |
| Lab assíncrono | 06/10/2026 19:45 | 20/11/2026 23:59 |
| Pós-teste | 06/10/2026 20:30 | 20/11/2026 23:59 (conta a nota mais alta) |

## Lab síncrono
Fontes:
- [`Demo 1.xlsx`](../Demo%201.xlsx) - original mantido intacto na raiz do OA
- Página web: https://cotacao-euro.pt/

Guardar o `.pbix` em [`lab-sincrono/`](lab-sincrono/).

### Parte A - Limpeza do `Demo 1.xlsx`
Tabela `HR_Master` (folha `HR Master`): 290 funcionários AdventureWorks, 15 colunas.

| Problema encontrado | Ferramenta no Power Query |
|---|---|
| `BirthDate` e `HireDate` são números (ex.: 26434), formato "Geral" | Alterar tipo -> **Data** |
| `Gender` M/F e `MaritalStatus` M/S em códigos | **Substituir Valores** (célula inteira): Masculino/Feminino, Casado/Solteiro |
| `SalariedFlag` com `0` / `-1` (estilo Access) | Alterar tipo -> **Verdadeiro/Falso** (-1 = Verdadeiro) ou Substituir Valores -> Sim/Não |
| `CurrentFlag` tem sempre `-1` (não acrescenta informação) | **Remover Colunas** |
| `rowguid` é um identificador técnico | **Remover Colunas** |
| `LoginID` = `adventure-works\guy1` | **Dividir Coluna** por delimitador `\` -> ficar só com o utilizador |
| `Title` = `Production Technician - WC60` | **Dividir Coluna** por delimitador ` - ` -> `Title` + `Work Center` (nulo quando não existe) |
| `ManagerID` nulo numa linha (EmployeeID 109, Chief Executive Officer) | Normal - o CEO não tem chefia. Não remover |

Armadilha: o `LoginID` `adventure-works\john0` aparece **duas vezes** (EmployeeID 16 e
18), mas são **pessoas diferentes** (NationalIDNumber e ContactID distintos).
**Remover Duplicados** sobre `LoginID` apagaria um funcionário - o identificador
correto para duplicados é `EmployeeID`.

Contagens para conferir: 290 linhas; Gender 206 M / 84 F; MaritalStatus 146 M / 144 S;
SalariedFlag 52 assalariados (-1) / 238 não.

### Parte B - Cotações da web + Append Queries
1. **Obter dados -> Web** -> `https://cotacao-euro.pt/`. O Navegador mostra duas
   tabelas HTML com as mesmas colunas:
   - tabela 1: moedas do BCE (28 linhas)
   - tabela 2: outras moedas (124 linhas, inclui **Cabo Verde - CVE - escudo**)
2. Em **cada** consulta (renomear para `Cotações BCE` e `Cotações Outras`):
   - Remover as colunas vazias/sem interesse (as duas primeiras, `Gráfico`,
     `Conversor de moedas`)
   - Os números vêm com **ponto decimal** (`1.1204`). Com o Windows em português,
     mudar o tipo diretamente lê `1.1204` como `11204`. Usar **Alterar tipo ->
     Utilizando a Região -> Decimal / Inglês (Estados Unidos)** em
     `Cotação por 1 €`, `Câmbio` e `Câmbio inverso`
   - (opcional) Adicionar Coluna -> **Coluna Personalizada** `Origem` com `"BCE"` /
     `"Outras"`, para distinguir as linhas depois de juntar
3. **Base -> Acrescentar Consultas -> Acrescentar Consultas como Nova** ->
   `Cotações BCE` + `Cotações Outras` -> renomear para `Cotações`.
   Resultado: **152 linhas** (28 + 124).
4. Nas duas consultas de origem: botão direito -> desmarcar **Ativar carregamento**
   (só `Cotações` vai para o modelo).

Verificação: `CVE` ≈ 110 escudos por 1 € (a 05/10/2026: 109,9211). O valor muda
todos os dias, porque a fonte é atualizada.

## Lab assíncrono
- Abre: 06/10/2026 às 19:45 - data limite: 20/11/2026 às 23:59
- Enunciado e entrega: [`lab-assincrono/`](lab-assincrono/) *(a aguardar enunciado)*

## Estado
- [x] Pré-teste - todas as respostas certas (05/10/2026)
- [ ] Lab síncrono
- [ ] Lab assíncrono
- [ ] Pós-teste
