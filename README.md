# 🏥 Sistema Especialista de Triagem Inteligente para UPA — SUS Brasil

**Disciplina:** Inteligência Artificial — J903
**Curso:** Ciência da Computação — 2026
**Entrega:** Microsoft Teams (com link do repositório Git)

---

## 📌 1. Contexto do Problema

O Sistema Único de Saúde (SUS) atende mais de 200 milhões de brasileiros e enfrenta diariamente o desafio de priorizar pacientes em Unidades de Pronto Atendimento (UPAs), onde os recursos são limitados e o estado clínico pode evoluir rapidamente.

No modelo tradicional, a triagem é realizada apenas na entrada. No entanto, estudos indicam que até 23% dos pacientes sofrem piora clínica durante a espera, sem reavaliação adequada.

Este projeto propõe uma solução baseada em **Sistemas Especialistas com Encadeamento Progressivo (Forward Chaining)**, permitindo:

* Classificação inicial baseada em sinais vitais
* Monitoramento contínuo do paciente
* Reclassificação automática conforme mudanças clínicas
* Tomada de decisão auditável em casos de empate

---

## 🎯 2. Objetivo

Desenvolver um sistema capaz de:

* Classificar pacientes conforme o Protocolo de Manchester (adaptado)
* Monitorar evolução clínica ao longo do tempo
* Aplicar regras de segunda ordem automaticamente
* Resolver empates de forma determinística, justa e auditável

---

## 🧠 3. Abordagem do Sistema

O sistema segue o modelo clássico de Sistemas Especialistas:

* **Base de conhecimento:** conjunto de regras médicas
* **Motor de inferência:** responsável por aplicar as regras
* **Memória de trabalho:** estado atual e histórico do paciente

Utiliza **encadeamento progressivo (forward chaining)**, onde:

1. Fatos são inseridos (dados do paciente)
2. Regras são avaliadas
3. Novos fatos são gerados
4. O processo se repete continuamente

---

## 🏥 4. Base de Conhecimento

### 4.1 Protocolo de Manchester (Adaptado SUS)

| Nível | Prioridade    | Tempo Máximo |
| ----- | ------------- | ------------ |
| 1     | Emergência    | 0 min        |
| 2     | Muito urgente | até 10 min   |
| 3     | Urgente       | até 30 min   |
| 4     | Pouco urgente | até 60 min   |
| 5     | Não urgente   | até 120 min  |

---

### 4.2 Regras Clínicas Primárias

Baseadas em sinais vitais como:

* SpO2
* Frequência cardíaca
* Escala de dor
* Temperatura
* Glasgow
* Vômitos por hora

Cada combinação de condições leva a uma classificação de nível.

---

### 4.3 Regra de Grupos Vulneráveis

Pacientes com:

* Idade ≥ 60 anos
* Gestantes
* Deficiência física grave

➡️ São automaticamente elevados um nível de prioridade.

---

### 4.4 Regras de Segunda Ordem (Encadeamento)

As regras abaixo são ativadas com base em conclusões anteriores:

* **E1:** Reclassificação rápida → evento crítico + notificação
* **E2:** Piora simultânea → aumento de prioridade
* **E3:** Violação de SLA → alerta + escalonamento
* **E4:** Vulnerável + aumento de temperatura → nível 2
* **E5:** Dupla violação de SLA → protocolo de sobrecarga

---

## 🧩 5. Representação das Regras (DOCUMENTAÇÃO)

As regras são representadas como **dados estruturados (dicionários Python)**.

### Estrutura geral:

```python
{
    "id": "R1",
    "tipo": "primaria",
    "condicoes": [...],
    "acao": {...}
}
```

### Exemplo:

```python
{
    "id": "R2",
    "tipo": "primaria",
    "condicoes": [
        {"campo": "spo2", "operador": "<", "valor": 90}
    ],
    "acao": {
        "tipo": "classificacao",
        "nivel": 2
    }
}
```

---

### Justificativa da Estrutura

A escolha por regras como dados permite:

* Separação entre lógica e conhecimento
* Facilidade de manutenção
* Escalabilidade
* Aderência ao modelo clássico de sistemas especialistas
* Atendimento ao requisito de não utilizar `if/elif`

---

## 🔄 6. Motor de Inferência

O motor implementa **encadeamento progressivo**, com:

* Memória de trabalho (estado atual + histórico)
* Agenda de fatos atualizada a cada leitura
* Propagação de conclusões entre regras

Fluxo:

1. Entrada dos dados do paciente
2. Avaliação das regras primárias
3. Atualização do nível
4. Disparo de regras de segunda ordem
5. Atualização contínua

---

## ⚖️ 7. Critério de Desempate (NÚCLEO DO TRABALHO)

Como o Protocolo de Manchester não define desempate, foi implementado um critério próprio baseado em:

1. Risco clínico objetivo
2. Velocidade de piora
3. Tempo restante para SLA
4. Tempo no nível atual
5. Ordem de chegada

---

### Cobertura dos Cenários

* Mesmo nível e mesma chegada → FIFO
* Piora clínica → prioridade para quem piorou
* Vulnerável vs piora → prioriza risco clínico
* SLA simultâneo → escalonamento + prioridade por tempo
* Reclassificação → prioridade para quem está há mais tempo no nível

---

### Propriedades Garantidas

* Determinismo
* Auditabilidade
* Equidade
* Ausência de inação

---

## 🧾 8. Log de Inferência

O sistema registra:

* Horário
* Fatos analisados
* Regra aplicada
* Resultado
* Justificativa

Exemplo:

```
[14:25] Regra E2 aplicada: piora simultânea → nível elevado para 2
```

---

## 🧪 9. Testes

O sistema inclui:

* Mínimo de 10 cenários
* 5 cenários de empate
* 2 cenários de piora progressiva
* 1 cenário com regra E4
* 1 cenário com regra E5

---

## 📥 10. Esquema de Entrada

O sistema recebe um dicionário com:

* Dados do paciente
* Lista de leituras ao longo do tempo

Campos ausentes são tratados sem gerar exceções.

---

## 🔒 11. Restrições Atendidas

* Python puro ✔
* Sem uso de Machine Learning ✔
* Regras como dados ✔
* Motor separado da base ✔
* Sem rebaixamento automático ✔
* Tratamento de dados ausentes ✔

---

## 🚀 12. Execução

```bash
git clone https://github.com/Trabalhos-UNIP-IA/Sistema-Especialista---triagem-de-paciente.git
cd Sistema-Especialista---triagem-de-paciente
python main.py
```

---

## 🧾 13. Reflexão (≤ 500 palavras)

O critério de desempate prioriza risco clínico e deterioração, garantindo respostas rápidas em cenários críticos.

Em situações de alta demanda (ex: 40 pacientes nível 3), o sistema tende a favorecer pacientes com piora ativa, podendo aumentar o tempo de espera de pacientes estáveis. No entanto, o uso de SLAs impede negligência prolongada.

Uma limitação observada é o possível atraso de pacientes estáveis em cenários extremos. Como mitigação, o sistema considera tempo no nível e proximidade de SLA.

Testes com diferentes perfis garantiram ausência de viés, pois atributos sensíveis não são utilizados.

---

## 👨‍💻 14. Autores

* Nome 1
* Nome 2

---

## 📎 15. Repositório

https://github.com/Trabalhos-UNIP-IA/Sistema-Especialista---triagem-de-paciente

---

## ❤️ 16. Considerações Finais

O sistema demonstra a aplicação prática de Sistemas Especialistas na saúde pública, promovendo decisões mais justas, transparentes e eficientes no atendimento de pacientes.
