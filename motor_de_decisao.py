
# import json
# with open(r"regras/regras_de_classificação.json", "r",encoding="utf-8") as f:
#     regras = json.load(f)
# with open(r"regras/regras_de_prioridade.json", "r",encoding="utf-8") as f:
#     regras_priorizacao = json.load(f)
from regras.regras_de_prioridade import regras

paciente_teste = {
        "idade": 67,
        "gestante": False,
        "deficiencia": False,
        "hora_entrada": "14:00",
        "leituras": [
            {
                "hora": "14:00",
                "consciente": True,
                "glasgow": 15,
                "spo2": 95,
                "frequencia_cardiaca": 88,
                "temperatura": 37.2, 
                "escala_dor": 3,        
                "vomitos_por_hora": 0,
                "pulso_presente": True,
                "respirando": True
            }
        ]
    }
def tete_logico(paciente, condicao):
    atributo, operador, valor = condicao
    if paciente.get(atributo) is None:
        return False
    else:
        operadores ={ 
            "==": lambda a, b: a == b,
            ">=": lambda a, b: a >= b,
            "<= ": lambda a, b: a <= b,
            ">": lambda a, b: a > b,
            "<": lambda a, b: a < b,
            "entre": lambda a, b: b[0] <= a <= b[1]
        }

        return operadores[operador](paciente[atributo], valor)


def teste_prioridade(regras, paciente):
    for regra in regras:
        condicao = regra["condicao"]
        atributo, operador, valor = condicao
        if tete_logico(paciente, condicao):
                paciente["prioridade"] = True
                paciente["tipo_prioridade"] = regra["prioridade"]

paciente1 = {"idade": 65}
paciente2 = {"idade": 30, "gestante": True}
paciente3 = {"idade": 40,  "deficiencia": True}
paciente4= {"idade": 25}
teste_prioridade(regras, paciente1)
teste_prioridade(regras, paciente2)
teste_prioridade(regras, paciente3)
teste_prioridade(regras, paciente4)
print(paciente1)  # Deve ter prioridade "deficiencia"
print(paciente2)  # Deve ter prioridade "gestante"
print(paciente3)  # Deve ter prioridade "deficiencia"
print(paciente4) 