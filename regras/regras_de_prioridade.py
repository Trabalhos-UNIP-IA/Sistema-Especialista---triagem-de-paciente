prioridade=[ "idade","gestante", "deficiencia"]
regras_prioridade = [
    {
        "condicao": ("gestante", "==", True),
        "prioridade": "idade"
    },
    {
        "condicao": ("deficiencia", "==", True),
        "prioridade": "gestante"
    },
    {
        "condicao": ("idade", ">=", 60),
        "prioridade": "deficiencia"
    }
]