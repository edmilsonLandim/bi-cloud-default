// OA3 - Lab Síncrono | Parte B - consulta "Serviços" (Unpivot do Demo4.xlsx)
// Resultado: 432 linhas (36 x 12 meses), Soma de Valor 5 543 168,90.
let
    Origem = Excel.Workbook(File.Contents("C:\Skodji Digital\U2-M5 - BI & Cloud Default - Ed2\OA3 - Combine files e unpivot\oa-03\lab-sincrono\Demo4.xlsx"), null, true),
    Servicos = Origem{0}[Data],                     // primeira folha, por posição
    #"Cabeçalhos promovidos" = Table.PromoteHeaders(Servicos, [PromoteAllScalars = true]),
    // Limpeza antes do Unpivot: 13 linhas de subtotal (Tipo vazio) e coluna Total Geral
    #"Linhas filtradas" = Table.SelectRows(#"Cabeçalhos promovidos", each [Tipo] <> null),
    #"Colunas removidas" = Table.RemoveColumns(#"Linhas filtradas", {"Total Geral"}),
    // Unpivot: âncoras Anos, Vendedor, Tipo -> meses passam a linhas
    #"Coluna não dinamizada" = Table.UnpivotOtherColumns(#"Colunas removidas", {"Anos", "Vendedor", "Tipo"}, "Mês", "Valor"),
    #"Nº Mês" = Table.AddColumn(#"Coluna não dinamizada", "Nº Mês", each List.PositionOf({"jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"}, [Mês]) + 1, Int64.Type),
    Data = Table.AddColumn(#"Nº Mês", "Data", each #date([Anos], [Nº Mês], 1), type date),
    // Tipos no fim
    #"Tipo alterado" = Table.TransformColumnTypes(Data, {{"Anos", Int64.Type}, {"Vendedor", type text}, {"Tipo", type text}, {"Mês", type text}, {"Valor", type number}})
in
    #"Tipo alterado"
