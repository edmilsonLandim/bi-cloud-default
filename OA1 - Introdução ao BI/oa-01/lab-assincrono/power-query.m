// OA1 - Lab Assíncrono | Consulta "Tabela1" (Power Query - Editor Avançado)
let
  Origem = Excel.Workbook(File.Contents("C:\Skodji Digital\U2-M5 - BI & Cloud Default - Ed2\OA1 - Introdução ao BI\oa-01\lab-assincrono\Dados Colaboradores Exemplo.xlsx"), null, true),
  #"Navegação 1" = Origem{[Item = "Tabela1", Kind = "Table"]}[Data],
  #"Tipo de coluna alterada" = Table.TransformColumnTypes(#"Navegação 1", {{"Nº de Entrada", Int64.Type}, {"Data de entrada", Int64.Type}, {"Nome do Cliente", type text}, {"Área  de Inscrição", type text}, {"Freguesia", type text}, {"Género", type text}, {"Data Nascimento", Int64.Type}}),
  // Parte 2.1 - Género: M -> Masculino, F -> Feminino (célula inteira)
  #"Valor substituído" = Table.ReplaceValue(#"Tipo de coluna alterada", "M", "Masculino", Replacer.ReplaceValue, {"Género"}),
  #"Valor substituído 1" = Table.ReplaceValue(#"Valor substituído", "F", "Feminino", Replacer.ReplaceValue, {"Género"}),
  // Parte 2.2 - colunas de data (número de série do Excel) -> tipo Data
  #"Tipo de coluna alterada 1" = Table.TransformColumnTypes(#"Valor substituído 1", {{"Data de entrada", type date}, {"Data Nascimento", type date}})
in
  #"Tipo de coluna alterada 1"
