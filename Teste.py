from regras.regras_de_prioridade import  regras 
paciente1 = {"idade": 65}
paciente2 = {"idade": 30, "gestante": True}
paciente3 = {"idade": 40,  "deficiencia": True}
paciente4= {"idade": 25}

def teste_prioridade(regras, paciente):
    for regra in regras:
        condicao = regra["condicao"]
        atributo, operador, valor = condicao
        if paciente.get(atributo) is None:
            pass
        else:
            if operador == "==":
                if  paciente[atributo] == valor:
                    paciente["prioridade"] = True
                    paciente["tipo_prioridade"] = regra["prioridade"]
            elif operador == ">=":
                if paciente[atributo] >= valor:
                    paciente["prioridade"] = True
                    paciente["tipo_prioridade"] = regra["prioridade"]


teste_prioridade(regras, paciente1)
teste_prioridade(regras, paciente2)
teste_prioridade(regras, paciente3)
teste_prioridade(regras, paciente4)
print(paciente1)  # Deve ter prioridade "deficiencia"
print(paciente2)  # Deve ter prioridade "gestante"
print(paciente3)  # Deve ter prioridade "deficiencia"
print(paciente4)  # Não deve ter prioridade