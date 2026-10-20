// OA4 - Consulta "SubCategories" (dSubCategories.txt, separador ";")
// Resultado: 3 colunas, 44 linhas. ProductSubcategoryKey único (lado 1 da relação com Products);
// ProductCategoryKey repetido (lado * da relação com Categories).
let
    Origem = Csv.Document(
        File.Contents("C:\Skodji Digital\U2-M5 - BI & Cloud Default - Ed2\OA4 - Modelo de dados relacional\oa-04\lab-sincrono\OA4 - Lab Síncrono-20261019\dSubCategories.txt"),
        [Delimiter = ";", Columns = 5, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    #"Cabeçalhos promovidos" = Table.PromoteHeaders(Origem, [PromoteAllScalars = true]),
    // Remover só as colunas redundantes (Label = código interno; Description = igual ao Name)
    #"Colunas removidas" = Table.RemoveColumns(#"Cabeçalhos promovidos", {"ProductSubcategoryLabel", "ProductSubcategoryDescription"}),
    // Chaves como Texto (iguais a Products[ProductSubcategoryKey] e Categories[ProductCategoryKey])
    #"Tipo alterado" = Table.TransformColumnTypes(#"Colunas removidas", {
        {"ProductSubcategoryKey", type text},
        {"ProductSubcategoryName", type text},
        {"ProductCategoryKey", type text}})
in
    #"Tipo alterado"
