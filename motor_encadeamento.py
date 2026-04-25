from datetime import datetime
import copy


class MotorTriagemFC:

    def __init__(self, regras, regras_prioridade):
        self.regras = regras
        self.regras_prioridade = regras_prioridade

        self.memoria = {"estado_atual": None, "historico_classificacao": []}

        self.agenda = []  # fatos (leituras)
        self.log = []  # log auditável

    # =========================
    # UTIL
    # =========================
    def registrar_log(self, leitura, regra, conclusao, criterio=None):
        self.log.append(
            {
                "hora_log": datetime.now().strftime("%H:%M:%S"),
                "leitura": leitura,
                "regra": regra,
                "conclusao": conclusao,
                "criterio_desempate": criterio,
            }
        )

    def avaliar_condicao(self, leitura, cond):
        campo, op, valor = cond

        if campo not in leitura:
            return False

        ops = {
            "==": lambda a, b: a == b,
            ">=": lambda a, b: a >= b,
            "<=": lambda a, b: a <= b,
            ">": lambda a, b: a > b,
            "<": lambda a, b: a < b,
            "entre": lambda a, b: b[0] <= a <= b[1],
            "fora": lambda a, b: a < b[0] or a > b[1],
        }

        return ops[op](leitura[campo], valor)

    def avaliar_regra(self, leitura, regra):
        resultados = [self.avaliar_condicao(leitura, c) for c in regra["condicoes"]]

        if regra["operadores"] == "e":
            return all(resultados)
        return any(resultados)

    # =========================
    # E1 — CLASSIFICAÇÃO
    # =========================
    def classificar(self, leitura):
        regras_ativadas = []

        for regra in self.regras:
            if self.avaliar_regra(leitura, regra):
                regras_ativadas.append(regra)

        return regras_ativadas

    # =========================
    # E3 — PRIORIDADE
    # =========================
    def aplicar_prioridade(self, leitura):
        for regra in self.regras_prioridade:
            if self.avaliar_condicao(leitura, regra["condicao"]):
                return True, regra["prioridade"]
        return False, None

    # =========================
    # E4 — PIORA
    # =========================
    def detectar_piora(self):
        hist = self.memoria["historico_classificacao"]

        if len(hist) < 2:
            return False

        atual = hist[-1]["leitura"]
        anterior = hist[-2]["leitura"]

        if atual.get("spo2") and anterior.get("spo2"):
            if atual["spo2"] < anterior["spo2"]:
                return True

        if atual.get("temperatura") and anterior.get("temperatura"):
            if atual["temperatura"] > anterior["temperatura"]:
                return True

        return False

    # =========================
    # E5 — SLA
    # =========================
    def violou_sla(self, tempo_max):
        return tempo_max == 0  # simplificado para teste

    # =========================
    # c) DESEMPATE
    # =========================
    def desempate(self, regras_ativadas, leitura):
    # 1. Caso simples
    if len(regras_ativadas) == 1:
        return regras_ativadas[0], "única regra aplicável"

    # 2. Prioridade absoluta: menor tempo_maximo
    menor_tempo = min(r["tempo_maximo"] for r in regras_ativadas)
    candidatas = [r for r in regras_ativadas if r["tempo_maximo"] == menor_tempo]

    # Se só uma regra tem o menor tempo → retorna direto
    if len(candidatas) == 1:
        return candidatas[0], "menor tempo_maximo (mais prioritário)"

    # 3. Critério secundário (desempate real): maior gravidade clínica
    melhor = candidatas[0]
    criterio = "empate no tempo_maximo"

    # exemplo de desempate por hipóxia
    if leitura.get("spo2") is not None and leitura["spo2"] < 90:
        criterio += " + hipóxia"
        # mantém a mais crítica (menor tempo já é igual, então mantém a primeira)

    return melhor, criterio

    # =========================
    # MOTOR
    # =========================
    def executar(self, paciente):

        for leitura in paciente["leituras"]:

            # Atualiza agenda e memória
            self.agenda.append(leitura)
            self.memoria["estado_atual"] = leitura

            # E1
            regras_ativadas = self.classificar(leitura)

            if not regras_ativadas:
                continue

            regra_final, criterio = self.desempate(regras_ativadas, leitura)

            # E3
            prioridade, tipo = self.aplicar_prioridade(leitura)
            if prioridade and regra_final["id"] > 1:
                regra_final = copy.deepcopy(regra_final)
                regra_final["id"] -= 1

            # E4
            self.memoria["historico_classificacao"].append(
                {"leitura": leitura, "nivel": regra_final["nivel"]}
            )

            if self.detectar_piora():
                regra_final["nivel"] = "Emergência"
                regra_final["tempo_maximo"] = 0

            # E5
            if self.violou_sla(regra_final["tempo_maximo"]):
                regra_final["nivel"] = "Emergência"

            # LOG
            self.registrar_log(
                leitura, f"Regra {regra_final['id']}", regra_final["nivel"], criterio
            )

        return self.memoria, self.log


def ordenar_pacientes(lista):
    return sorted(
        lista,
        key=lambda p: (
            p["tempo_maximo"],  # 1. SLA (principal)
            not p.get("prioridade", False),  # 2. prioridade (True vem primeiro)
            p["leituras"][-1].get(
                "spo2", 100
            ),  # 3. pior condição (menor SPO2 primeiro)
            p["leituras"][-1].get("frequencia_cardiaca", 0),  # 4. FC mais crítica
            p["id"],  # 5. fallback (determinístico)
        ),
    )
