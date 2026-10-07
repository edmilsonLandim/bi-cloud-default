// OA2 - Lab Assíncrono | Consulta "Lançamentos" (Acrescentar Consultas como Nova - 12 folhas)
// As 12 consultas Janeiro ... Dezembro (4 passos cada: Origem, Navegação, Cabeçalhos
// promovidos, Tipo alterado) têm o carregamento desativado.
let
    // Parte 2.1 - Append Queries: 12 folhas -> 27 472 linhas
    Origem = Table.Combine({Janeiro, Fevereiro, Março, Abril, Maio, Junho, Julho, Agosto, Setembro, Outubro, Novembro, Dezembro}),
    // Parte 2.2 - códigos como texto (não se somam), data sem hora, valor decimal
    #"Tipo alterado" = Table.TransformColumnTypes(Origem, {
        {"DataMovimento", type date}, {"CodFilial", type text}, {"CodConta", type text},
        {"CodCentroCusto", type text}, {"TipoLancamento", type text}, {"Valor", type number}}),
    // Parte 2.2 - D/C por extenso (célula inteira)
    #"Valor substituído" = Table.ReplaceValue(#"Tipo alterado", "D", "Débito", Replacer.ReplaceValue, {"TipoLancamento"}),
    #"Valor substituído 1" = Table.ReplaceValue(#"Valor substituído", "C", "Crédito", Replacer.ReplaceValue, {"TipoLancamento"})
in
    #"Valor substituído 1"
