// OA2 - Lab Síncrono | Parte A - consulta "HR_Master" (Demo 1.xlsx)
// Linhas marcadas com "// CORRIGIDO" ou "// NOVO" diferem da primeira versão.
let
  Origem = Excel.Workbook(File.Contents("C:\Skodji Digital\U2-M5 - BI & Cloud Default - Ed2\OA2 - Transformação e limpeza de dados\Demo 1.xlsx"), null, true),
  #"Navegação 1" = Origem{[Item = "HR_Master", Kind = "Table"]}[Data],
  // CORRIGIDO: HireDate passa a Data (estava Int64 -> gráfico por ano de contratação não funcionava)
  #"Tipo de coluna alterada" = Table.TransformColumnTypes(#"Navegação 1", {{"EmployeeID", Int64.Type}, {"NationalIDNumber", Int64.Type}, {"ContactID", Int64.Type}, {"LoginID", type text}, {"ManagerID", Int64.Type}, {"Title", type text}, {"BirthDate", type date}, {"MaritalStatus", type text}, {"Gender", type text}, {"HireDate", type date}, {"SalariedFlag", Int64.Type}, {"VacationHours", Int64.Type}, {"SickLeaveHours", Int64.Type}, {"CurrentFlag", Int64.Type}, {"rowguid", type text}}),
  // CORRIGIDO: Replacer.ReplaceValue = célula inteira (ReplaceText troca a letra dentro de qualquer texto)
  #"Valor substituído" = Table.ReplaceValue(#"Tipo de coluna alterada", "M", "Masculino", Replacer.ReplaceValue, {"Gender"}),
  #"Valor substituído 1" = Table.ReplaceValue(#"Valor substituído", "F", "Feminino", Replacer.ReplaceValue, {"Gender"}),
  #"Valor substituído 2" = Table.ReplaceValue(#"Valor substituído 1", "M", "Casado", Replacer.ReplaceValue, {"MaritalStatus"}),
  #"Valor substituído 3" = Table.ReplaceValue(#"Valor substituído 2", "S", "Solteiro", Replacer.ReplaceValue, {"MaritalStatus"}),
  #"Tipo de coluna alterada 1" = Table.TransformColumnTypes(#"Valor substituído 3", {{"SalariedFlag", type logical}}),
  #"Colunas removidas" = Table.RemoveColumns(#"Tipo de coluna alterada 1", {"CurrentFlag", "rowguid"}),
  #"Dividir coluna por delimitador" = Table.SplitColumn(#"Colunas removidas", "LoginID", Splitter.SplitTextByDelimiter("\"), {"LoginID.1", "LoginID.2"}),
  #"Dividir coluna por delimitador 1" = Table.SplitColumn(#"Dividir coluna por delimitador", "Title", Splitter.SplitTextByDelimiter("-"), {"Title.1", "Title.2"}),
  #"Tipo de coluna alterada 2" = Table.TransformColumnTypes(#"Dividir coluna por delimitador 1", {{"LoginID.1", type text}, {"LoginID.2", type text}, {"Title.1", type text}, {"Title.2", type text}}),
  // NOVO: o split por "-" deixa espaços ("Production Technician " / " WC60") -> Aparar
  #"Texto aparado" = Table.TransformColumns(#"Tipo de coluna alterada 2", {{"Title.1", Text.Trim, type text}, {"Title.2", Text.Trim, type text}}),
  // NOVO: "adventure-works" é igual em todas as linhas -> remover; fica só o utilizador
  #"Colunas removidas 1" = Table.RemoveColumns(#"Texto aparado", {"LoginID.1"}),
  #"Colunas com nome mudado" = Table.RenameColumns(#"Colunas removidas 1", {{"Title.1", "Title"}, {"Title.2", "Work Center"}, {"LoginID.2", "LoginID"}})
in
  #"Colunas com nome mudado"
