regras  = [
{"id": 1,
    "nivel": "Emergência",
    "cor": "vermelho",
    "tempo_maximo":0, 
   "condicoes":    [
        ("consciente", "==", False),
        ("pulso_presente", "==", False),
        ("respirando", "==", False)
  ]  },

    {"id": 2,
     "nivel": "Muito urgente",
     "cor": "laranja",
      "tempo_maximo": 10,
        "condicoes":    [
        ("consciente", "==", True),
            ("glasgow", "<", 14),
            ("spo2", "<", 90),
            ("frequencia_cardiaca", "<", 40),
            ("frequencia_cardiaca", ">", 150),
            ("temperatura", "==", 39), 
            ("escala_dor", "entre", (8, 10)),        
            ("pulso_presente", "==", True),
            ("respirando", "==", True)
   ]   },

    {"id": 3,
     "nivel": "Urgente",
     "cor": "amarelo", 
     "tempo_maximo": 30, 
      "condicoes":    [
        ("consciente", "==", True),
            ("glasgow", "==", 14),
            ("spo2", "==", 90),
            ("frequencia_cardiaca", "entre", (120, 150)),
            ("temperatura", ">", 39),
            ("escala_dor", "entre", (5, 7)),
            ("vomitos_por_hora", ">", 3),
            ("pulso_presente", "==", True),
            ("respirando", "==", True)]
    },

    {"id": 4,
     "nivel": "Pouco urgente",
     "cor": "verde",
      "tempo_maximo": 60,
       "condicoes":    [
        ("consciente", "==", True),
            ("glasgow", "==", 15),
            ("spo2", "==", 95),
            ("frequencia_cardiaca", "entre", (50, 120)),
            ("temperatura", "==", 37.2), 
            ("escala_dor", "entre", (1, 4)),        
            ("vomitos_por_hora", "==", 3),
]
    },

    {"id": 5,
     "nivel": "Não urgente",
     "cor": "azul",
      "tempo_maximo": 120,
       "condicoes":    [
        ("consciente", "==", True),
        ("glasgow", "==", 15),
        ("spo2", "==", 95),
        ("frequencia_cardiaca", "entre", (50, 120)),
        ("temperatura", "==", 37.2), 
        ("escala_dor", "entre", (0, 0)),        
        ("vomitos_por_hora", "==", 0),
        ("pulso_presente", "==", True),
        ("respirando", "==", True)
       ]
    }
]