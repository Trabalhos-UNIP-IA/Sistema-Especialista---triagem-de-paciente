import json
with open(r"regras/regras_de_classificação.json", "r",encoding="utf-8") as f:
    regras = json.load(f)
with open(r"regras/regras_de_prioridade.json", "r",encoding="utf-8") as f:
    regras_priorizacao = json.load(f)

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
for regra in regras:
    print(regra)
for regra in regras_priorizacao["prioridade"]:
    print(regra)
    print(paciente_teste[regra])
    if paciente_teste[regra] == True or paciente_teste[regra] > 60:
        break
    else:
        print("Paciente não é prioridade")
