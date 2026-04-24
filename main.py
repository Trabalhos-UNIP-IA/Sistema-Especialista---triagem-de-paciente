import json
import os
from motor_de_decisao import triagem, ordenar_pacientes

PASTA_PACIENTES = "Pacientes"
<<<<<<< HEAD
cor = { '1':"\033[31m", '2':"\033[38;5;208m", '3':"\033[33m", '4':"\033[32m", '5':"\033[38;2;100;180;255m", }
=======
cor = {
    "1": "\033[31m",
    "2": "\033[38;5;208m",
    "3": "\033[33m",
    "4": "\033[32m",
    "5": "\033[38;2;100;180;255m",
}
>>>>>>> 922beb2 (Atualizando os pacientes)

pacientes = []

# # 1. Ler todos os arquivos JSON da pasta
# for arquivo in os.listdir(PASTA_PACIENTES):
#     if arquivo.endswith(".json"):
#         caminho = os.path.join(PASTA_PACIENTES, arquivo)

#         with open(caminho, "r", encoding="utf-8") as f:
#             paciente = json.load(f)

#             # 2. Aplicar triagem
#             resultado = triagem(paciente)
#             pacientes.append(resultado)

# # 3. Ordenar pacientes (empate)
# pacientes_ordenados = ordenar_pacientes(pacientes)

# 4. Exibir resultados
print("\n=== RESULTADOS DA TRIAGEM ===")

<<<<<<< HEAD
pacientes_ordenados = sorted(pacientes, key=lambda x: (x['id_nivel'], x['tempo_maximo']))
with open(r"Pacientes/paciente04.json", "r",encoding="utf-8") as f:
    paciente_teste = json.load(f)

paciente_teste = triagem(paciente_teste)
print(f"{cor[str(paciente_teste['id_nivel'])]}       \n--- Paciente {paciente_teste['id']} ---")
=======
pacientes_ordenados = sorted(
    pacientes, key=lambda x: (x["id_nivel"], x["tempo_maximo"])
)
with open(r"Pacientes/paciente04.json", "r", encoding="utf-8") as f:
    paciente_teste = json.load(f)

paciente_teste = triagem(paciente_teste)
print(
    f"{cor[str(paciente_teste['id_nivel'])]}       \n--- Paciente {paciente_teste['id']} ---"
)
>>>>>>> 922beb2 (Atualizando os pacientes)
print(f"id: {paciente_teste['id']}")
print(f"cor: {paciente_teste['cor']}")
print(f"nivel: {paciente_teste['nivel_prioridade']}")
print(f"tempo_maximo: {paciente_teste['tempo_maximo']}\033[0m")
<<<<<<< HEAD
if paciente_teste.get('prioridade', False):
    print(f"{cor[str(paciente_teste['id_nivel'])]}prioridade: {paciente_teste['prioridade']}")
=======
if paciente_teste.get("prioridade", False):
    print(
        f"{cor[str(paciente_teste['id_nivel'])]}prioridade: {paciente_teste['prioridade']}"
    )
>>>>>>> 922beb2 (Atualizando os pacientes)
    print(f"tipo_prioridade: {paciente_teste['tipo_prioridade']}\033[0m")

# for i, p in enumerate(paciente, 1):
#     print(f"{cor[str(p['id_nivel'])]}       \n--- Paciente {i} ---")
#     print(f"id: {p['id']}")
#     print(f"cor: {p['cor']}")
#     print(f"nivel: {p['nivel_prioridade']}")
#     print(f"tempo_maximo: {p['tempo_maximo']}")
#     print(f"prioridade: {p.get('prioridade', False)}")
#     print(f"tipo_prioridade: {p.get('tipo_prioridade', [])}\033[0m")
