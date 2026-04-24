import json
import os
from motor_de_decisao import triagem, ordenar_pacientes

PASTA_PACIENTES = "Pacientes"
cor = { '1':"\033[31m", '2':"\033[38;5;208m", '3':"\033[33m", '4':"\033[32m", '5':"\033[34m", }

pacientes = []

# 1. Ler todos os arquivos JSON da pasta
for arquivo in os.listdir(PASTA_PACIENTES):
    if arquivo.endswith(".json"):
        caminho = os.path.join(PASTA_PACIENTES, arquivo)

        with open(caminho, "r", encoding="utf-8") as f:
            paciente = json.load(f)

            # 2. Aplicar triagem
            resultado = triagem(paciente)
            pacientes.append(resultado)

# 3. Ordenar pacientes (empate)
pacientes_ordenados = ordenar_pacientes(pacientes)

# 4. Exibir resultados
print("\n=== RESULTADOS DA TRIAGEM ===")

for i, p in enumerate(pacientes_ordenados, 1):
    print(f"{cor[str(p['id_nivel'])]}       \n--- Paciente {i} ---")
    print(f"id: {p['id']}")
    print(f"cor: {p['cor']}")
    print(f"nivel: {p['nivel_prioridade']}")
    print(f"tempo_maximo: {p['tempo_maximo']}")
    print(f"prioridade: {p.get('prioridade', False)}")
    print(f"tipo_prioridade: {p.get('tipo_prioridade', [])}\033[0m")
