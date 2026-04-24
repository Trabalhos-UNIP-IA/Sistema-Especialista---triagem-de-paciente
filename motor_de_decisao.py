
import json
with open(r"regras/regras_de_classificação.json", "r",encoding="utf-8") as f:
    regras = json.load(f)
with open(r"regras/regras_de_prioridade.json", "r",encoding="utf-8") as f:
    regras_priorizacao = json.load(f)
operadores ={ 
            "==": lambda a, b: a == b,
            ">=": lambda a, b: a >= b,
            "<= ": lambda a, b: a <= b,
            ">": lambda a, b: a > b,
            "<": lambda a, b: a < b,
            "entre": lambda a, b: b[0] <= a <= b[1],
            "fora": lambda a, b: a < b[0] or a > b[1]
        }

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
def teste_logico(paciente, condicao):
    atributo, operador, valor = condicao
    if paciente.get(atributo) is None:
        return False
    else:

        return operadores[operador](paciente[atributo], valor)


def validador_de_prioridade(regras, paciente):
    for regra in regras:
        condicao = regra["condicao"]
        if teste_logico(paciente, condicao):
                paciente["prioridade"] = True
                paciente["tipo_prioridade"] = regra["prioridade"]


def operador_logico(condicoes, operador,paciente):
    if operador == "e":
        return all(teste_logico(paciente, condicao) for condicao in condicoes)
    elif operador == "ou":
        return any(teste_logico(paciente, condicao) for condicao in condicoes)

def triagem(regras,paciente):
    for regra in regras:
        condicoes = regra["condicoes"]
        operador = regra["operadores"]

        if operador_logico(condicoes, operador, paciente):
            paciente
            paciente["nivel_prioridade"] = regra["nivel"]
            paciente["cor"] = regra["cor"]
            paciente["tempo_maximo"] = regra["tempo_maximo"]
            validador_de_prioridade(regras_priorizacao, paciente)
            return paciente
    else:
        paciente["nivel_prioridade"] = "Não urgente"
        paciente["cor"] = "azul"
        paciente["tempo_maximo"] = 120
        return paciente
    

triagem
print