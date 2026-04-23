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
    if paciente_teste["leituras"][0]["consciente"] == regra["condicoes"]["consciente"] or  paciente_teste["leituras"][0]["pulso_presente"] == regra["condicoes"]["pulso_presente"] or paciente_teste["leituras"][0]["respirando"] == regra["condicoes"]["respirando"]:
       # nivel = 1
       paciente_teste["nivel"] = regra["nivel"]
       print("Paciente é nível 1")
       break
    elif paciente_teste["leituras"][0]["glasgow"] <= regra["condicoes"]["glasgow"] and paciente_teste["leituras"][0]["spo2"] < regra["condicoes"]["spo2"] and (paciente_teste["leituras"][0]["frequencia_cardiaca"] > regra["condicoes"]["frequencia_cardiaca"]["max"] or  paciente_teste["leituras"][0]["frequencia_cardiaca"] < regra["condicoes"]["frequencia_cardiaca"]["min"]) and paciente_teste["leituras"][0]["escala_dor"] > regra["condicoes"]["escala_dor"]["min"]: 
        # nivel = 2
        paciente_teste["nivel"] = regra["nivel"]
        print("Paciente é nível 2")
        break

    elif paciente_teste["leituras"][0]["temperatura"] > regra["condicoes"]["temperatura"] and paciente_teste["leituras"][0]["vomitos_por_hora"] >= regra["condicoes"]["vomitos_por_hora"] and regra["condicoes"]["escala_dor"]["min"] < paciente_teste["leituras"][0]["escala_dor"] < regra["condicoes"]["escala_dor"]["max"] and (regra["condicoes"]["frequencia_cardiaca"][0]["min"] < paciente_teste["leituras"][0]["frequencia_cardiaca"] < regra["condicoes"]["escala_dor"][0]["max"] or regra["condicoes"]["frequencia_cardiaca"][1]["min"] < paciente_teste["leituras"][0]["frequencia_cardiaca"] < regra["condicoes"]["frequencia_cardiaca"][1]["max"]): 
        # nivel = 3
        paciente_teste["nivel"] = regra["nivel"]
        print("Paciente é nível 3")

        break
    else:
        pass
        paciente_teste["nivel"] = regra["nivel"]  
        
        # nivel = 5
    print(regra["condicoes"]["consciente"],regra["condicoes"]["glasgow"],regra["condicoes"]["spo2"],
          regra["condicoes"]["frequencia_cardiaca"],regra["condicoes"]["temperatura"],regra["condicoes"]["escala_dor"],
          regra["condicoes"]["vomitos_por_hora"],regra["condicoes"]["pulso_presente"],regra["condicoes"]["respirando"])
    paciente_teste["nivel"] = regra["nivel"]

for regra in regras_priorizacao["prioridade"]:
    print(regra)
    print(paciente_teste[regra])
    if paciente_teste[regra] == True or paciente_teste[regra] > 59:
        paciente_teste["Prioridade"] = True
        break
    print("Paciente não é prioridade")
print(paciente_teste["Prioridade"])
print(paciente_teste["nivel"])
