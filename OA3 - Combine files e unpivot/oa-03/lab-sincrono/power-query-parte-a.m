// OA3 - Lab Síncrono | Parte A - consulta "Lançamentos" (Combine Files: pasta csv\ com 3 ficheiros)
// Funções auxiliares geradas pelo Power BI: "Ficheiro de exemplo", "Transformar ficheiro".
// Resultado: 76 672 linhas, Soma de Valor 140 690 832,57.
let
  Origem = Folder.Files("C:\Skodji Digital\U2-M5 - BI & Cloud Default - Ed2\OA3 - Combine files e unpivot\oa-03\lab-sincrono\csv"),
  #"Ficheiros ocultos filtrados" = Table.SelectRows(Origem, each [Attributes]?[Hidden]? <> true),
  #"Personalizado adicionado" = let
    rootPath = Text.TrimEnd(Value.Metadata(Value.Type(#"Ficheiros ocultos filtrados"))[FileSystemTable.RootPath]?, "\"),
    combinePaths = (path1, path2) => Text.Combine({Text.TrimEnd(path1, "\"), path2}, "\"),
    getRelativePath = (path, relativeTo) => Text.Middle(path, Text.Length(relativeTo) + 1)
in
    Table.AddColumn(#"Ficheiros ocultos filtrados", "Relative Path", each getRelativePath(combinePaths([Folder Path], [Name]), rootPath), type text),
  #"Invocar função personalizada" = Table.AddColumn(#"Personalizado adicionado", "Transformar ficheiro", each #"Transformar ficheiro"([Content])),
  #"Colunas com nome mudado" = Table.RenameColumns(#"Invocar função personalizada", {{"Relative Path", "Source.Name"}}),
  #"Outras colunas removidas" = Table.SelectColumns(#"Colunas com nome mudado", {"Source.Name", "Transformar ficheiro"}),
  #"Coluna de tabela expandida" = Table.ExpandTableColumn(#"Outras colunas removidas", "Transformar ficheiro", Table.ColumnNames(#"Transformar ficheiro"(#"Ficheiro de exemplo"))),
  #"Tipo de coluna alterada" = Table.TransformColumnTypes(#"Coluna de tabela expandida", {{"CodFilial", Int64.Type}, {"DataMovimento", type date}, {"CodConta", Int64.Type}, {"CodCentroCusto", Int64.Type}, {"StatusLançamento", type text}, {"TipoLancamento", type text}, {"Lote", Int64.Type}, {"LoteItem", Int64.Type}, {"Valor", type number}}),
  // Higiene: nome do ficheiro removido (o ano vem da DataMovimento)
  #"Colunas removidas" = Table.RemoveColumns(#"Tipo de coluna alterada", {"Source.Name"}),
  #"Tipo de coluna alterada 1" = Table.TransformColumnTypes(#"Colunas removidas", {{"DataMovimento", type date}}),
  // Região Português (Portugal): vírgula decimal e datas dd/mm/aaaa
  #"Tipo de coluna com região alterada" = Table.TransformColumnTypes(#"Tipo de coluna alterada 1", {{"DataMovimento", type date}}, "pt-PT"),
  #"Tipo de coluna com região alterada 1" = Table.TransformColumnTypes(#"Tipo de coluna com região alterada", {{"Valor", type number}, {"CodFilial", type text}, {"CodConta", type text}, {"CodCentroCusto", type text}, {"Lote", type text}, {"LoteItem", type text}}, "pt-PT"),
  #"Valor substituído" = Table.ReplaceValue(#"Tipo de coluna com região alterada 1", "D", "Débito", Replacer.ReplaceText, {"TipoLancamento"}),
  #"Valor substituído 1" = Table.ReplaceValue(#"Valor substituído", "C", "Crédito", Replacer.ReplaceText, {"TipoLancamento"}),
  #"Ano inserido" = Table.AddColumn(#"Valor substituído 1", "Ano", each Date.Year([DataMovimento]), type nullable number)
in
  #"Ano inserido"
