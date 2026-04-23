prioridade=[ "idade","gestante", "deficiencia"]
regras = [
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