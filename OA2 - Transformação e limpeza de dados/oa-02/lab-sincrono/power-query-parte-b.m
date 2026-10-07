// OA2 - Lab Síncrono | Parte B - cotacao-euro.pt + Append Queries
// Linhas marcadas com "// NOVO" diferem da primeira versão.

// ---------- Consulta "Cotações BCE" (Ativar carregamento: desligado) ----------
let
  Origem = Web.BrowserContents("https://cotacao-euro.pt/"),
  #"Tabela extraída de HTML" = Html.Table(Origem, {{"Column0", "DIV.table_responsive.mb10social > TABLE.table.kurzy > * > TR > :nth-child(1)"}, {"Column1", "DIV.table_responsive.mb10social > TABLE.table.kurzy > * > TR > :nth-child(2)"}, {"Column2", "DIV.table_responsive.mb10social > TABLE.table.kurzy > * > TR > :nth-child(3)"}, {"Column3", "DIV.table_responsive.mb10social > TABLE.table.kurzy > * > TR > :nth-child(4)"}, {"Column4", "DIV.table_responsive.mb10social > TABLE.table.kurzy > * > TR > :nth-child(5)"}, {"Column5", "DIV.table_responsive.mb10social > TABLE.table.kurzy > * > TR > :nth-child(6)"}, {"Column6", "DIV.table_responsive.mb10social > TABLE.table.kurzy > * > TR > :nth-child(7)"}, {"Column7", "DIV.table_responsive.mb10social > TABLE.table.kurzy > * > TR > :nth-child(8)"}, {"Column8", "DIV.table_responsive.mb10social > TABLE.table.kurzy > * > TR > :nth-child(9)"}, {"Column9", "DIV.table_responsive.mb10social > TABLE.table.kurzy > * > TR > :nth-child(10)"}}, [RowSelector = "DIV.table_responsive.mb10social > TABLE.table.kurzy > * > TR"]),
  #"Cabeçalhos promovidos" = Table.PromoteHeaders(#"Tabela extraída de HTML", [PromoteAllScalars = true]),
  // NOVO: remover também as 2 primeiras colunas (sem cabeçalho: ícone/bandeira) -> ficam País, Código, Moeda, ...
  #"Colunas removidas" = Table.RemoveColumns(#"Cabeçalhos promovidos", {"Column1", "Column2", "Gráfico", "Conversor de moedas"}),
  #"Tipo de coluna com região alterada" = Table.TransformColumnTypes(#"Colunas removidas", {{"Cotação por 1 €", type number}, {"Câmbio", type number}, {"Câmbio inverso", type number}}, "en-US"),
  // NOVO: tipo texto na coluna personalizada (sem tipo fica "ABC123" = any)
  #"Personalizado adicionado" = Table.AddColumn(#"Tipo de coluna com região alterada", "Origem", each "BCE", type text)
in
  #"Personalizado adicionado"

// ---------- Consulta "Cotações Outras" (Ativar carregamento: desligado) ----------
// Igual à anterior, com o seletor "DIV.table_responsive.mb20-mt" e each "Outras".

// ---------- Consulta "Cotações" (Acrescentar Consultas como Nova) ----------
let
  Origem = Table.Combine({#"Cotações BCE", #"Cotações Outras"}),
  #"Linhas filtradas" = Table.SelectRows(Origem, each ([Código] <> "XAG" and [Código] <> "XAU")),
  #"Valor substituído" = Table.ReplaceValue(#"Linhas filtradas", "Ilhas Mlavinas", "Ilhas Malvinas", Replacer.ReplaceText, {"País"})
in
  #"Valor substituído"
