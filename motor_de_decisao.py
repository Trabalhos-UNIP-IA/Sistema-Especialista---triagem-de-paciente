import json
from datetime import datetime
with open(r"regras/regras_de_classificação.json", "r",encoding="utf-8") as f:
    regras = json.load(f)
with open(r"regras/regras_de_prioridade.json", "r",encoding="utf-8") as f:
    regras_priorizacao = json.load(f)
with open(r"Pacientes/paciente01.json", "r",encoding="utf-8") as f:
    paciente_teste = json.load(f)

operadores = {
    "==": lambda a, b: a == b,
    ">=": lambda a, b: a >= b,
    "<=": lambda a, b: a <= b,
    ">": lambda a, b: a > b,
    "<": lambda a, b: a < b,
    "entre": lambda a, b: b[0] <= a <= b[1],
    "fora": lambda a, b: a < b[0] or a > b[1],
}

cor = { '1':"\033[31m", '2':"\033[38;5;208m", '3':"\033[33m", '4':"\033[32m", '5':"\033[34m", }


def pegar_leitura_atual(paciente):
    if len(paciente["leituras"]) > 0:
        return paciente["leituras"][len(paciente["leituras"]) - 1]
    return None


def pegar_leitura_anterior(paciente):
    if len(paciente["leituras"]) >= 2:
        return paciente["leituras"][-2]
    return None

def validador_de_prioridade( paciente):
    for regra in regras_priorizacao:
        condicao = regra["condicao"]
        if teste_logico(paciente, condicao):
            paciente["prioridade"] = True
            paciente["tipo_prioridade"] = regra["prioridade"]
            break


def teste_logico(leitura, condicao):

    atributo, operador, valor = condicao
    if leitura.get(atributo) is None:
        return False
    else:
        return operadores[operador](leitura[atributo], valor)



def operador_logico(condicoes, operador,paciente):
    leitura = pegar_leitura_atual(paciente)
    if operador == "e":
        for condicao in condicoes:  
            resultado = teste_logico(leitura, condicao)
            valor = "N/A"
            if leitura.get(condicao[0]) is not None:
                valor = leitura[condicao[0]]
            print(f"Valor: {valor} | Condição: {condicao} -> {'Verdadeiro' if resultado else 'Falso'}")
        return all(teste_logico(leitura, condicao) for condicao in condicoes)
    elif operador == "ou":
        return any(teste_logico(leitura, condicao) for condicao in condicoes)


def triagem(paciente):
    for regra in regras:
        condicoes = regra["condicoes"]
        operador = regra["operadores"]
        print(f"\nTestando regra {regra['id']} ")
        if operador_logico(condicoes, operador, paciente):
            paciente['id_nivel'] = regra['id']
            validador_de_prioridade(paciente)
            if paciente.get("prioridade") and paciente["id_nivel"] >  1:
                paciente["id_nivel"] -=1
            break  

    paciente["nivel_prioridade"] = regras[paciente["id_nivel"]-1]["nivel"]
    paciente["cor"] = regras[paciente["id_nivel"]-1]["cor"]
    paciente["tempo_maximo"] = regras[paciente["id_nivel"]-1]["tempo_maximo"]
    return paciente

def aplicar_prioridade(paciente):
    paciente["prioridade"] = False
    paciente["tipo_prioridade"] = []

    for regra in regras_priorizacao:
        if teste_logico(paciente, regra["condicao"]):
            paciente["prioridade"] = True
            paciente["tipo_prioridade"].append(regra["prioridade"])

    return paciente


def subir_nivel(paciente):
    mapa = {
        "azul": ("verde", "Pouco urgente", 60),
        "verde": ("amarelo", "Urgente", 30),
        "amarelo": ("laranja", "Muito urgente", 10),
        "laranja": ("vermelho", "Emergência", 0),
    }

    cor = paciente["cor"]
    if cor in mapa:
        nova_cor, nivel, tempo = mapa[cor]
        paciente["cor"] = nova_cor
        paciente["nivel_prioridade"] = nivel
        paciente["tempo_maximo"] = tempo

    return paciente


# =========================
# E1 — Classificação inicial
# =========================
def classificar(paciente):
    for regra in regras:
        if operador_logico(regra["condicoes"], regra["operadores"], paciente):
            paciente["nivel_prioridade"] = regra["nivel"]
            paciente["cor"] = regra["cor"]
            paciente["tempo_maximo"] = regra["tempo_maximo"]
            return paciente

    paciente["nivel_prioridade"] = "Não urgente"
    paciente["cor"] = "azul"
    paciente["tempo_maximo"] = 120
    return paciente


# =========================
# E2 — Reavaliação contínua (placeholder estrutural)
# =========================
def reavaliacao_continua(paciente):
    # Aqui você poderia reprocessar em loop em sistema real
    return paciente


# =========================
# E3 — Prioridade (já aplicada separadamente)
# =========================


# =========================
# E4 — Piora do paciente
# =========================
def detectar_piora(paciente):
    anterior = pegar_leitura_anterior(paciente)
    atual = pegar_leitura_atual(paciente)

    if not anterior:
        return False

    # usa .get() para evitar erro
    spo2_atual = atual.get("spo2")
    spo2_ant = anterior.get("spo2")

    temp_atual = atual.get("temperatura")
    temp_ant = anterior.get("temperatura")

    glasgow_atual = atual.get("glasgow")
    glasgow_ant = anterior.get("glasgow")

    # compara só se ambos existirem
    if spo2_atual is not None and spo2_ant is not None:
        if spo2_atual < spo2_ant:
            return True

    if temp_atual is not None and temp_ant is not None:
        if temp_atual > temp_ant:
            return True

    if glasgow_atual is not None and glasgow_ant is not None:
        if glasgow_atual < glasgow_ant:
            return True

    return False


# =========================
# E5 — Violação de SLA
# =========================
def violou_sla(paciente):
    try:
        hora_entrada = datetime.strptime(paciente["hora_entrada"], "%H:%M")
        agora = datetime.now()

        minutos = (agora - hora_entrada).seconds / 60
        return minutos > paciente["tempo_maximo"]
    except:
        return False


# =========================
# MOTOR PRINCIPAL
# =========================
# def triagem(paciente):

#     # E1 — Classificação inicial
#     paciente = classificar(paciente)

#     # E3 — Prioridade (grupo vulnerável)
#     paciente = aplicar_prioridade(paciente)

#     if paciente["prioridade"]:
#         paciente = subir_nivel(paciente)

#     # E4 — Piora
#     if detectar_piora(paciente):
#         paciente = subir_nivel(paciente)

#     # E5 — SLA
#     if violou_sla(paciente):
#         paciente["cor"] = "vermelho"
#         paciente["nivel_prioridade"] = "Emergência"
#         paciente["tempo_maximo"] = 0

#     # E2 — Reavaliação (estrutura)
#     paciente = reavaliacao_continua(paciente)

#     return paciente


# # =========================
# ORDENAÇÃO (EMPATE)
# =========================
def ordenar_pacientes(lista):
    return sorted(
        lista, key=lambda p: (p["tempo_maximo"], not p.get("prioridade", False))
    )
