import json
import os
from motor_de_decisao import triagem, ordenar_pacientes

PASTA_PACIENTES = "Pacientes"

cor = {
    "1": "\033[31m",  # vermelho
    "2": "\033[38;5;208m",  # laranja
    "3": "\033[33m",  # amarelo
    "4": "\033[32m",  # verde
    "5": "\033[38;2;100;180;255m",  # azul
}

pacientes = []

# =========================
# 1. Ler e processar pacientes
# =========================
for arquivo in os.listdir(PASTA_PACIENTES):
    if arquivo.endswith(".json"):
        caminho = os.path.join(PASTA_PACIENTES, arquivo)

        with open(caminho, "r", encoding="utf-8") as f:
            paciente = json.load(f)

            resultado = triagem(paciente)

            # adiciona nome do arquivo (útil para log)
            resultado["arquivo_origem"] = arquivo

            pacientes.append(resultado)

# =========================
# 2. Ordenação (com desempate)
# =========================
pacientes_ordenados = ordenar_pacientes(pacientes)

# =========================
# 3. Exibir resultados
# =========================
print("\n=== RESULTADOS DA TRIAGEM ===\n")

for i, p in enumerate(pacientes_ordenados, 1):
    cor_terminal = cor.get(str(p["id_nivel"]), "\033[0m")

    print(f"{cor_terminal}--- {i}º na fila ---")
    print(f"Paciente: {p['id']}")
    print(f"Arquivo: {p['arquivo_origem']}")
    print(f"Cor: {p['cor']}")
    print(f"Nível: {p['nivel_prioridade']}")
    print(f"Tempo máximo: {p['tempo_maximo']} min")

    if p.get("prioridade", False):
        print(f"Prioridade: {p['tipo_prioridade']}")

    # =========================
    # Mostrar critério de desempate
    # =========================
    if p.get("criterio_desempate"):
        print(f"Desempate aplicado: {p['criterio_desempate']}")

    print("\033[0m")


# =========================
# 4. LOG AUDITÁVEL
# =========================
print("\n=== LOG DE INFERÊNCIA ===\n")

for p in pacientes_ordenados:
    if "log" in p:
        print(f"\nPaciente {p['id']}:")

        for log in p["log"]:
            print(f"- Hora: {log['hora']}")
            print(f"  Regra: {log['regra']}")
            print(f"  Conclusão: {log['conclusao']}")
            print(f"  Fatos: {log['fatos']}")

            if log.get("criterio"):
                print(f"  Desempate: {log['criterio']}")

            print()
