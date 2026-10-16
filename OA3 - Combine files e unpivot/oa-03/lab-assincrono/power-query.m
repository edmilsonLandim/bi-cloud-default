// OA3 - Lab Assíncrono | Consulta "Mapa Contabilístico" (Unpivot do balancete 2025)
// Resultado: 1 065 linhas (99 contas x 12 meses - 123 células vazias), Soma de Valor 7 721 393,64.
let
    Origem = Excel.Workbook(File.Contents("C:\Skodji Digital\U2-M5 - BI & Cloud Default - Ed2\OA3 - Combine files e unpivot\oa-03\lab-assincrono\Mapa contabilistico.xlsx"), null, true),
    Folha = Origem{0}[Data],                                   // primeira folha, por posição
    // Parte 2.1 - limpeza antes do Unpivot: linhas vazias (1 e 3) e colunas vazias (A e D)
    #"Linhas em branco removidas" = Table.SelectRows(Folha, each not List.IsEmpty(List.RemoveMatchingItems(Record.FieldValues(_), {"", null}))),
    #"Cabeçalhos promovidos" = Table.PromoteHeaders(#"Linhas em branco removidas", [PromoteAllScalars = true]),
    #"Outras colunas removidas" = Table.SelectColumns(#"Cabeçalhos promovidos", {"Conta SNC", "Designação SNC", "jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"}),
    // Parte 2.1 - Unpivot com as âncoras Conta SNC e Designação SNC
    #"Coluna não dinamizada" = Table.UnpivotOtherColumns(#"Outras colunas removidas", {"Conta SNC", "Designação SNC"}, "Mês", "Valor"),
    // Parte 2.2 - data (Método A: sufixo do ano + tipo Data em pt-PT)
    #"Sufixo adicionado" = Table.TransformColumns(#"Coluna não dinamizada", {{"Mês", each _ & " 2025", type text}}),
    #"Tipo de coluna com região alterada" = Table.TransformColumnTypes(#"Sufixo adicionado", {{"Mês", type date}}, "pt-PT"),
    #"Colunas com nome mudado" = Table.RenameColumns(#"Tipo de coluna com região alterada", {{"Mês", "Data"}}),
    // Parte 2.2 - tipos de dados no fim
    #"Tipo alterado" = Table.TransformColumnTypes(#"Colunas com nome mudado", {{"Conta SNC", type text}, {"Designação SNC", type text}, {"Valor", Currency.Type}}),
    // Classe SNC (1.º dígito da conta) para o gráfico por classe
    #"Personalizado adicionado" = Table.AddColumn(#"Tipo alterado", "Classe SNC", each {"1 Meios fin. líquidos", "2 Contas a rec./pagar", "3 Inventários", "4 Investimentos",
        "5 Capital e reservas", "6 Gastos", "7 Rendimentos", "8 Resultados"}{Number.From(Text.Start([Conta SNC], 1)) - 1})
in
    #"Personalizado adicionado"
